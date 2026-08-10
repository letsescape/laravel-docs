#!/usr/bin/env node
import {createServer} from 'node:http';
import {createReadStream, existsSync, statSync} from 'node:fs';
import {join, normalize, extname} from 'node:path';
import {fileURLToPath} from 'node:url';

const REPO_ROOT = fileURLToPath(new URL('..', import.meta.url));
const BUILD_ROOT = join(REPO_ROOT, 'build');

const MIME_TYPES = new Map([
  ['.html', 'text/html; charset=utf-8'],
  ['.css', 'text/css; charset=utf-8'],
  ['.js', 'text/javascript; charset=utf-8'],
  ['.json', 'application/json; charset=utf-8'],
  ['.xml', 'application/xml; charset=utf-8'],
  ['.txt', 'text/plain; charset=utf-8'],
  ['.svg', 'image/svg+xml'],
  ['.png', 'image/png'],
  ['.jpg', 'image/jpeg'],
  ['.jpeg', 'image/jpeg'],
  ['.webp', 'image/webp'],
  ['.avif', 'image/avif'],
  ['.ico', 'image/x-icon'],
  ['.woff2', 'font/woff2'],
  ['.map', 'application/json; charset=utf-8'],
]);

function argValue(name, fallback) {
  const idx = process.argv.indexOf(name);
  return idx >= 0 && process.argv[idx + 1] ? process.argv[idx + 1] : fallback;
}

const host = argValue('--host', process.env.HOST || '127.0.0.1');
const port = Number(argValue('--port', process.env.PORT || '3000'));

function safeJoin(root, urlPath) {
  const decoded = decodeURIComponent(urlPath);
  const normalized = normalize(decoded).replace(/^(\.\.[/\\])+/, '');
  const full = join(root, normalized);
  if (!full.startsWith(root)) return null;
  return full;
}

function sendFile(req, res, filePath, statusCode = 200) {
  const ext = extname(filePath);
  const stat = statSync(filePath);
  res.writeHead(statusCode, {
    'content-type': MIME_TYPES.get(ext) || 'application/octet-stream',
    'content-length': stat.size,
  });
  if (req.method === 'HEAD') {
    res.end();
    return;
  }
  createReadStream(filePath).pipe(res);
}

function notFound(req, res) {
  const html404 = join(BUILD_ROOT, '404.html');
  if (existsSync(html404)) {
    sendFile(req, res, html404, 404);
    return;
  }
  res.writeHead(404, {'content-type': 'text/plain; charset=utf-8'});
  res.end('Not found');
}

if (!existsSync(BUILD_ROOT)) {
  console.error('[serve-build] build/ not found. Run `npm run build` first.');
  process.exit(2);
}

const server = createServer((req, res) => {
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    res.writeHead(405, {'content-type': 'text/plain; charset=utf-8'});
    res.end('Method not allowed');
    return;
  }

  const fallbackHost = `${host}:${port}`;
  const requestHost = req.headers.host || fallbackHost;
  const url = new URL(req.url || '/', `http://${requestHost}`);
  const pathFromRoot = safeJoin(BUILD_ROOT, url.pathname.replace(/^\/+/, ''));
  if (!pathFromRoot) {
    notFound(req, res);
    return;
  }

  if (existsSync(pathFromRoot)) {
    const stat = statSync(pathFromRoot);
    if (stat.isDirectory()) {
      const indexPath = join(pathFromRoot, 'index.html');
      if (existsSync(indexPath)) {
        sendFile(req, res, indexPath);
        return;
      }
    } else if (stat.isFile()) {
      sendFile(req, res, pathFromRoot);
      return;
    }
  }

  const htmlPath = `${pathFromRoot}.html`;
  if (existsSync(htmlPath) && statSync(htmlPath).isFile()) {
    sendFile(req, res, htmlPath);
    return;
  }

  notFound(req, res);
});

server.listen(port, host, () => {
  console.log(`[serve-build] Serving build/ at http://${host}:${port}/`);
});

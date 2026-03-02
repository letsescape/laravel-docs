/**
 * Script to generate SEO frontmatter for Laravel Korean documentation files.
 *
 * - Extracts H1 title and first meaningful paragraph
 * - Generates title, description, keywords
 * - Preserves existing frontmatter fields (slug, sidebar_position, etc.)
 *
 * Usage: node scripts/generate-frontmatter.js [version]
 *   e.g. node scripts/generate-frontmatter.js 12.x
 *        node scripts/generate-frontmatter.js        (processes 12.x and 11.x)
 */
const fs = require('fs');
const path = require('path');

// Skip these files/directories
const SKIP_FILES = ['origin', 'documentation.md', 'readme.md', 'license.md', 'intro.md'];

// Keyword map: filename -> [Korean keyword, English keyword]
const KEYWORD_MAP = {
  'installation': ['라라벨 설치', 'Laravel installation'],
  'configuration': ['라라벨 설정', 'Laravel configuration'],
  'routing': ['라라벨 라우팅', 'Laravel routing'],
  'middleware': ['라라벨 미들웨어', 'Laravel middleware'],
  'controllers': ['라라벨 컨트롤러', 'Laravel controllers'],
  'requests': ['라라벨 HTTP 요청', 'Laravel requests'],
  'responses': ['라라벨 HTTP 응답', 'Laravel responses'],
  'views': ['라라벨 뷰', 'Laravel views'],
  'blade': ['라라벨 블레이드', 'Laravel Blade templates'],
  'session': ['라라벨 세션', 'Laravel session'],
  'validation': ['라라벨 유효성 검사', 'Laravel validation'],
  'errors': ['라라벨 에러 처리', 'Laravel error handling'],
  'logging': ['라라벨 로깅', 'Laravel logging'],
  'artisan': ['라라벨 아티즌', 'Laravel Artisan CLI'],
  'broadcasting': ['라라벨 브로드캐스팅', 'Laravel broadcasting'],
  'cache': ['라라벨 캐시', 'Laravel cache'],
  'collections': ['라라벨 컬렉션', 'Laravel collections'],
  'container': ['라라벨 서비스 컨테이너', 'Laravel service container'],
  'contracts': ['라라벨 Contracts', 'Laravel contracts'],
  'events': ['라라벨 이벤트', 'Laravel events'],
  'filesystem': ['라라벨 파일 스토리지', 'Laravel filesystem'],
  'helpers': ['라라벨 헬퍼 함수', 'Laravel helpers'],
  'mail': ['라라벨 메일', 'Laravel mail'],
  'notifications': ['라라벨 알림', 'Laravel notifications'],
  'packages': ['라라벨 패키지 개발', 'Laravel packages'],
  'queues': ['라라벨 큐', 'Laravel queues'],
  'scheduling': ['라라벨 작업 스케줄링', 'Laravel scheduling'],
  'testing': ['라라벨 테스팅', 'Laravel testing'],
  'database': ['라라벨 데이터베이스', 'Laravel database'],
  'migrations': ['라라벨 마이그레이션', 'Laravel migrations'],
  'seeding': ['라라벨 시딩', 'Laravel seeding'],
  'queries': ['라라벨 쿼리 빌더', 'Laravel query builder'],
  'pagination': ['라라벨 페이지네이션', 'Laravel pagination'],
  'eloquent': ['라라벨 Eloquent ORM', 'Laravel Eloquent'],
  'eloquent-relationships': ['라라벨 Eloquent 관계', 'Laravel Eloquent relationships'],
  'eloquent-collections': ['라라벨 Eloquent 컬렉션', 'Laravel Eloquent collections'],
  'eloquent-mutators': ['라라벨 Eloquent 뮤테이터', 'Laravel Eloquent mutators'],
  'eloquent-resources': ['라라벨 API 리소스', 'Laravel API resources'],
  'eloquent-serialization': ['라라벨 Eloquent 직렬화', 'Laravel Eloquent serialization'],
  'eloquent-factories': ['라라벨 모델 팩토리', 'Laravel model factories'],
  'authentication': ['라라벨 인증', 'Laravel authentication'],
  'authorization': ['라라벨 권한 부여', 'Laravel authorization'],
  'encryption': ['라라벨 암호화', 'Laravel encryption'],
  'hashing': ['라라벨 해싱', 'Laravel hashing'],
  'passwords': ['라라벨 비밀번호 재설정', 'Laravel password reset'],
  'csrf': ['라라벨 CSRF 보호', 'Laravel CSRF protection'],
  'localization': ['라라벨 다국어 처리', 'Laravel localization'],
  'frontend': ['라라벨 프론트엔드', 'Laravel frontend'],
  'vite': ['라라벨 Vite', 'Laravel Vite'],
  'urls': ['라라벨 URL 생성', 'Laravel URL generation'],
  'http-client': ['라라벨 HTTP 클라이언트', 'Laravel HTTP client'],
  'http-tests': ['라라벨 HTTP 테스트', 'Laravel HTTP tests'],
  'console-tests': ['라라벨 콘솔 테스트', 'Laravel console tests'],
  'database-testing': ['라라벨 데이터베이스 테스트', 'Laravel database testing'],
  'mocking': ['라라벨 모킹', 'Laravel mocking'],
  'billing': ['라라벨 결제', 'Laravel billing'],
  'cashier-paddle': ['라라벨 Cashier Paddle', 'Laravel Cashier Paddle'],
  'deployment': ['라라벨 배포', 'Laravel deployment'],
  'homestead': ['라라벨 Homestead', 'Laravel Homestead'],
  'sail': ['라라벨 Sail', 'Laravel Sail Docker'],
  'valet': ['라라벨 Valet', 'Laravel Valet'],
  'horizon': ['라라벨 Horizon', 'Laravel Horizon'],
  'telescope': ['라라벨 Telescope', 'Laravel Telescope'],
  'passport': ['라라벨 Passport', 'Laravel Passport OAuth'],
  'sanctum': ['라라벨 Sanctum', 'Laravel Sanctum API'],
  'socialite': ['라라벨 Socialite', 'Laravel Socialite OAuth'],
  'scout': ['라라벨 Scout', 'Laravel Scout search'],
  'dusk': ['라라벨 Dusk', 'Laravel Dusk browser testing'],
  'envoy': ['라라벨 Envoy', 'Laravel Envoy'],
  'fortify': ['라라벨 Fortify', 'Laravel Fortify'],
  'folio': ['라라벨 Folio', 'Laravel Folio'],
  'pennant': ['라라벨 Pennant', 'Laravel Pennant feature flags'],
  'prompts': ['라라벨 Prompts', 'Laravel Prompts CLI'],
  'pulse': ['라라벨 Pulse', 'Laravel Pulse monitoring'],
  'reverb': ['라라벨 Reverb', 'Laravel Reverb WebSocket'],
  'octane': ['라라벨 Octane', 'Laravel Octane'],
  'pint': ['라라벨 Pint', 'Laravel Pint code style'],
  'precognition': ['라라벨 Precognition', 'Laravel Precognition'],
  'processes': ['라라벨 프로세스', 'Laravel processes'],
  'providers': ['라라벨 서비스 프로바이더', 'Laravel service providers'],
  'redis': ['라라벨 Redis', 'Laravel Redis'],
  'releases': ['라라벨 릴리스 노트', 'Laravel release notes'],
  'structure': ['라라벨 디렉터리 구조', 'Laravel directory structure'],
  'strings': ['라라벨 문자열 처리', 'Laravel strings'],
  'upgrade': ['라라벨 업그레이드 가이드', 'Laravel upgrade guide'],
  'verification': ['라라벨 이메일 인증', 'Laravel email verification'],
  'context': ['라라벨 Context', 'Laravel context'],
  'concurrency': ['라라벨 동시성', 'Laravel concurrency'],
  'contributions': ['라라벨 기여 가이드', 'Laravel contribution guide'],
  'facades': ['라라벨 파사드', 'Laravel facades'],
  'lifecycle': ['라라벨 요청 라이프사이클', 'Laravel request lifecycle'],
  'mix': ['라라벨 Mix', 'Laravel Mix'],
  'mongodb': ['라라벨 MongoDB', 'Laravel MongoDB'],
  'rate-limiting': ['라라벨 속도 제한', 'Laravel rate limiting'],
  'redirects': ['라라벨 리다이렉트', 'Laravel redirects'],
  'starter-kits': ['라라벨 스타터 킷', 'Laravel starter kits'],
};

/**
 * Parse existing frontmatter from a markdown file
 */
function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---\n/);
  if (!match) return { fields: {}, body: content };

  const frontmatterText = match[1];
  const fields = {};

  for (const line of frontmatterText.split('\n')) {
    const kvMatch = line.match(/^(\w[\w-]*)\s*:\s*(.+)$/);
    if (kvMatch) {
      fields[kvMatch[1]] = kvMatch[2].trim();
    }
  }

  const body = content.slice(match[0].length);
  return { fields, body };
}

/**
 * Extract H1 title from markdown body
 */
function extractH1(body) {
  const match = body.match(/^#\s+(.+)$/m);
  return match ? match[1].trim() : null;
}

/**
 * Extract Korean and English parts from title like "라우팅 (Routing)"
 */
function parseTitleParts(h1) {
  // Pattern: "Korean Title (English Title)"
  const match = h1.match(/^(.+?)\s*\(([^)]+)\)\s*$/);
  if (match) {
    return { ko: match[1].trim(), en: match[2].trim() };
  }
  // Pattern: "Eloquent: Korean Title (Eloquent: English Title)"
  const match2 = h1.match(/^(.+?):\s*(.+?)\s*\((.+?)\)\s*$/);
  if (match2) {
    return { ko: `${match2[1]}: ${match2[2]}`.trim(), en: match2[3].trim() };
  }
  return { ko: h1, en: '' };
}

/**
 * Extract first meaningful paragraph after the TOC section
 */
function extractFirstParagraph(body) {
  const lines = body.split('\n');
  let pastTOC = false;
  let paragraphLines = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Skip H1
    if (line.match(/^#\s+/)) continue;

    // Skip TOC lines (lines starting with - [ or indented -)
    if (line.match(/^\s*-\s+\[/) || line.match(/^\s*-\s+\(/)) continue;

    // Skip empty lines in TOC area
    if (!pastTOC && line.trim() === '') continue;

    // Skip anchor tags
    if (line.match(/^<a\s+name=/)) {
      pastTOC = true;
      continue;
    }

    // Skip H2/H3 headers
    if (line.match(/^#{2,}\s+/)) {
      pastTOC = true;
      continue;
    }

    // Once we're past the TOC, collect paragraph lines
    if (pastTOC || (!line.match(/^\s*-\s/) && line.trim() !== '')) {
      pastTOC = true;

      if (line.trim() === '') {
        if (paragraphLines.length > 0) break;
        continue;
      }

      // Skip code blocks
      if (line.match(/^```/)) break;

      // Skip admonitions
      if (line.match(/^:::/)) continue;

      paragraphLines.push(line.trim());
    }
  }

  return paragraphLines.join(' ');
}

/**
 * Truncate text to maxLen, ending at a sentence or word boundary
 */
function truncate(text, maxLen = 155) {
  if (text.length <= maxLen) return text;

  // Remove markdown links syntax
  let clean = text.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
  // Remove backticks
  clean = clean.replace(/`([^`]+)`/g, '$1');

  if (clean.length <= maxLen) return clean;

  const truncated = clean.substring(0, maxLen);
  // Try to end at a sentence boundary
  const lastPeriod = truncated.lastIndexOf('.');
  if (lastPeriod > maxLen * 0.6) {
    return truncated.substring(0, lastPeriod + 1);
  }
  // End at a word boundary
  const lastSpace = truncated.lastIndexOf(' ');
  if (lastSpace > maxLen * 0.6) {
    return truncated.substring(0, lastSpace) + '...';
  }
  return truncated + '...';
}

/**
 * Generate frontmatter for a single file
 */
function generateFrontmatter(filePath, version) {
  const content = fs.readFileSync(filePath, 'utf8');
  const { fields: existingFields, body } = parseFrontmatter(content);

  const h1 = extractH1(body);
  if (!h1) {
    console.warn(`  [SKIP] No H1 found: ${path.basename(filePath)}`);
    return null;
  }

  const { ko, en } = parseTitleParts(h1);
  const basename = path.basename(filePath, '.md');
  const paragraph = extractFirstParagraph(body);

  // Generate title
  const title = en
    ? `${ko} (${en}) - Laravel ${version} 한국어 문서`
    : `${ko} - Laravel ${version} 한국어 문서`;

  // Generate description
  let description;
  if (paragraph) {
    description = truncate(paragraph);
  } else {
    description = en
      ? `라라벨 ${ko}에 대한 한국어 문서입니다. Laravel ${version} ${en} 가이드.`
      : `라라벨 ${ko}에 대한 한국어 문서입니다. Laravel ${version} 가이드.`;
  }

  // Generate keywords
  const kwPair = KEYWORD_MAP[basename];
  const keywords = kwPair
    ? [kwPair[0], kwPair[1], `Laravel ${version}`]
    : [ko, en || basename, `Laravel ${version}`].filter(Boolean);

  // Build new frontmatter, preserving existing non-SEO fields
  const newFields = {};
  // Preserve structural fields like slug, sidebar_position first
  for (const [key, value] of Object.entries(existingFields)) {
    if (!['title', 'description', 'keywords'].includes(key)) {
      newFields[key] = value;
    }
  }
  newFields.title = title;
  newFields.description = description;
  newFields.keywords = `[${keywords.join(', ')}]`;

  // Build frontmatter string
  const lines = ['---'];
  for (const [key, value] of Object.entries(newFields)) {
    if (key === 'keywords') {
      lines.push(`${key}: ${value}`);
    } else {
      // Use single quotes to avoid YAML escape issues with backslashes
      // Single-quoted YAML strings treat everything literally except '' for '
      const needsQuote = /[:#{}\[\],&*?|<>=!%@`\\"]/.test(value);
      if (needsQuote) {
        // In YAML single-quoted strings, single quotes are escaped as ''
        lines.push(`${key}: '${value.replace(/'/g, "''")}'`);
      } else {
        lines.push(`${key}: ${value}`);
      }
    }
  }
  lines.push('---');
  lines.push('');

  const newContent = lines.join('\n') + body;
  return newContent;
}

/**
 * Process all markdown files in a version directory
 */
function processVersion(version) {
  const versionDir = path.join(__dirname, '..', 'versioned_docs', `version-${version}`);
  if (!fs.existsSync(versionDir)) {
    console.error(`Version directory not found: ${versionDir}`);
    return;
  }

  const files = fs.readdirSync(versionDir).filter(f => {
    if (!f.endsWith('.md')) return false;
    if (SKIP_FILES.includes(f)) return false;
    return true;
  });

  console.log(`\nProcessing version ${version}: ${files.length} files`);

  let updated = 0;
  let skipped = 0;

  for (const file of files) {
    const filePath = path.join(versionDir, file);

    // Check if frontmatter already has title + description
    const content = fs.readFileSync(filePath, 'utf8');
    const { fields } = parseFrontmatter(content);

    if (!force && fields.title && fields.description) {
      console.log(`  [KEEP] ${file} (already has title+description)`);
      skipped++;
      continue;
    }

    const newContent = generateFrontmatter(filePath, version);
    if (newContent) {
      fs.writeFileSync(filePath, newContent, 'utf8');
      console.log(`  [OK] ${file}`);
      updated++;
    } else {
      skipped++;
    }
  }

  console.log(`  => Updated: ${updated}, Skipped: ${skipped}`);
}

// Main
const rawArgs = process.argv.slice(2);
const force = rawArgs.includes('--force');
const args = rawArgs.filter(a => !a.startsWith('--'));
const versions = args.length > 0 ? args : ['12.x', '11.x'];

for (const version of versions) {
  processVersion(version);
}

console.log('\nFrontmatter generation complete!');

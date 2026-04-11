import {test, expect} from '@playwright/test';
import {existsSync} from 'fs';
import {resolve} from 'path';

test.describe('Build verification', () => {
  test('build output directory exists', () => {
    const buildDir = resolve(__dirname, '../build');
    expect(existsSync(buildDir)).toBe(true);
  });

  test('build output contains index.html', () => {
    const indexFile = resolve(__dirname, '../build/index.html');
    expect(existsSync(indexFile)).toBe(true);
  });

  test('build output contains static assets', () => {
    const imgDir = resolve(__dirname, '../build/img');
    const assetsDir = resolve(__dirname, '../build/assets');
    expect(existsSync(imgDir) || existsSync(assetsDir)).toBe(true);
  });
});

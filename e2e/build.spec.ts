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
    const staticDir = resolve(__dirname, '../build/img');
    expect(existsSync(staticDir)).toBe(true);
  });
});

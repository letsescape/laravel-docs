import {defineConfig, devices} from '@playwright/test';

const port = Number(process.env.PLAYWRIGHT_PORT ?? '3000');
const baseURL =
  process.env.PLAYWRIGHT_BASE_URL ?? `http://127.0.0.1:${port}`;
const webServerTimeout = Number(
  process.env.PLAYWRIGHT_WEB_SERVER_TIMEOUT ?? '600000',
);

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : 2,
  timeout: 60_000,
  reporter: 'html',
  use: {
    baseURL,
    trace: 'on-first-retry',
    navigationTimeout: 45_000,
  },
  projects: [
    {
      name: 'chromium',
      use: {...devices['Desktop Chrome']},
    },
  ],
  webServer: {
    command: `npm run build && npm run serve -- --host 127.0.0.1 --port ${port}`,
    url: baseURL,
    reuseExistingServer: process.env.PLAYWRIGHT_REUSE_SERVER === '1',
    timeout: webServerTimeout,
  },
});

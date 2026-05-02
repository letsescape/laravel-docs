import {defineConfig, devices} from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : 2,
  timeout: 60_000,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    navigationTimeout: 45_000,
  },
  projects: [
    {
      name: 'chromium',
      use: {...devices['Desktop Chrome']},
    },
  ],
  // 사이트 e2e는 Docusaurus 개발 서버(`npm run start`) 위에서 동작한다.
  // 정적 빌드 산출물 검증, redirect HTML 생성, anchor 매칭 같은 CI/CD 단계는
  // 모두 .github/docs-updater 의 Python 도구가 deploy 워크플로우에서 처리한다.
  webServer: {
    command: 'npm run start -- --no-open --port 3000 --host 127.0.0.1',
    url: 'http://127.0.0.1:3000/',
    reuseExistingServer: !process.env.CI,
    timeout: 240_000,
  },
});

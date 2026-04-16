// Playwright cross-engine config.
// Runs the same specs against Chromium (Blink), Firefox (Gecko), and WebKit
// (the engine Safari uses). The site has engine-specific canvas paths —
// Firefox's CPU-bound ctx.filter is the notable one — that static review
// alone can't catch. See ADR-004 in the ops repo for rationale.

import { defineConfig, devices } from '@playwright/test';

const PORT = Number(process.env.PW_PORT || 8768);

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  fullyParallel: false,       // canvas perf measurements fight for GPU; serialize
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: `http://127.0.0.1:${PORT}`,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  // WebKit is kept in the config but flagged off by default because Ubuntu
  // 25.10's ICU76 isn't ABI-compatible with the libicudata.so.74 WebKit's
  // Playwright build links against. Opt in with `PW_WEBKIT=1` once your
  // distro's libicu74 is available (older Ubuntus, or a dev container).
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox',  use: { ...devices['Desktop Firefox'] } },
    ...(process.env.PW_WEBKIT
      ? [{ name: 'webkit', use: { ...devices['Desktop Safari'] } }]
      : []),
  ],
  webServer: {
    command: `python3 -m http.server ${PORT} -d site/output`,
    url: `http://127.0.0.1:${PORT}/`,
    reuseExistingServer: !process.env.CI,
    timeout: 5_000,
    stdout: 'ignore',
    stderr: 'pipe',
  },
});

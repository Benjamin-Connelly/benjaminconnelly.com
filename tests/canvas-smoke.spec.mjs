// Smoke-test every canvas piece across Chromium, Firefox, and WebKit.
//
// For each page:
//   1. Load and confirm no console errors fire during first 1.5 s.
//   2. Measure frame time over 2 s under default (idle) state.
//   3. Save a reference screenshot under test-results/.
//
// Fails the project if:
//   - any console error is logged
//   - average frame time > 33 ms (i.e., under 30 fps)
//
// Does NOT cover: interaction states (hold-S chaos, mode cycling, modals),
// visual regression (no pixel diff against a baseline), or mobile viewports.
// Those are worth adding later; start with a guard rail, not a moat.

import { test, expect } from '@playwright/test';

// maxMeanMs is the per-frame ceiling in headless render for each page.
// tb303 is allowed a looser budget — its renderer does ~20k fillText
// calls per frame against a pre-drawn 303 chassis, which Firefox's text
// pipeline handles slower than Chromium's. See benjaminconnelly_com bd
// issue for the optimization follow-up.
const PAGES = [
  { name: 'landing',    path: '/',                maxMeanMs: 33 },
  { name: 'mirrorball', path: '/mirrorball.html', maxMeanMs: 33 },
  { name: 'smiley',     path: '/smiley.html',     maxMeanMs: 33 },
  { name: 'tb303',      path: '/tb303.html',      maxMeanMs: 50 },
];

for (const page of PAGES) {
  test.describe(page.name, () => {
    test(`no console errors + under ${page.maxMeanMs}ms frame time`, async ({ page: pw, browserName }) => {
      const errors = [];
      pw.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
      pw.on('pageerror', err => errors.push(String(err)));

      await pw.goto(page.path, { waitUntil: 'load' });
      await pw.waitForTimeout(1500);

      const fpsReport = await pw.evaluate(async () => {
        // Wake the page up — some pages only animate on mouse activity.
        window.dispatchEvent(new MouseEvent('mousemove',
          { clientX: window.innerWidth / 2, clientY: window.innerHeight / 2 }));
        await new Promise(r => setTimeout(r, 200));

        const times = [];
        let last = performance.now();
        const start = last;
        await new Promise(resolve => {
          function tick(now) {
            times.push(now - last);
            last = now;
            if (now - start < 2000) requestAnimationFrame(tick);
            else resolve();
          }
          requestAnimationFrame(tick);
        });
        times.sort((a, b) => a - b);
        const mean = times.reduce((a, b) => a + b, 0) / times.length;
        return {
          frames: times.length,
          meanMs: mean,
          medianMs: times[times.length >> 1],
          p95Ms: times[Math.floor(times.length * 0.95)],
          fps: 1000 / mean,
        };
      });

      await pw.screenshot({
        path: `test-results/${browserName}-${page.name}.png`,
        fullPage: false,
      });

      expect(errors, `console errors on ${page.name} in ${browserName}`).toEqual([]);
      expect(fpsReport.meanMs,
        `${page.name} frame time in ${browserName} ` +
        `(mean ${fpsReport.meanMs.toFixed(1)}ms, p95 ${fpsReport.p95Ms.toFixed(1)}ms, ~${fpsReport.fps.toFixed(0)} fps)`
      ).toBeLessThan(page.maxMeanMs);
    });
  });
}

// Generate 1200×630 Open Graph / Twitter preview images for each page.
// Run after `make build`. Output lands in site/static/img/og-*.png which
// the build copies to site/output/img/ on the next `make build`.
//
//   node scripts/gen-og-images.mjs
//
// Uses Playwright's Chromium (already installed by `make test-setup`).
// Captures at the recommended Facebook/OG size (1200×630, 1.91:1) which
// Twitter also accepts for summary_large_image cards. LinkedIn requires
// 1200×627+ so this clears that threshold too.

import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { writeFile, mkdir } from 'node:fs/promises';
import { setTimeout as sleep } from 'node:timers/promises';

const PORT = 8769;
const OUT_DIR = 'site/static/img';
const PAGES = [
  { name: 'home',       path: '/',               waitMs: 1500 },
  { name: 'mirrorball', path: '/mirrorball.html', waitMs: 2500 },
  { name: 'smiley',     path: '/smiley.html',     waitMs: 1800 },
  { name: 'tb303',      path: '/tb303.html',      waitMs: 1800 },
];

async function main() {
  await mkdir(OUT_DIR, { recursive: true });

  // Spin up a local static server pointed at the already-built output.
  const server = spawn('python3', ['-m', 'http.server', String(PORT), '-d', 'site/output'],
                      { stdio: ['ignore', 'ignore', 'pipe'] });
  await sleep(400);

  const browser = await chromium.launch();
  try {
    for (const page of PAGES) {
      const ctx = await browser.newContext({
        viewport: { width: 1200, height: 630 },
        deviceScaleFactor: 2,  // retina-quality output for sharp preview
      });
      const pw = await ctx.newPage();
      await pw.goto(`http://127.0.0.1:${PORT}${page.path}`, { waitUntil: 'load' });
      // Wake any mouse-only animations and let the scene settle.
      await pw.mouse.move(600, 315);
      await sleep(page.waitMs);
      const out = `${OUT_DIR}/og-${page.name}.png`;
      await pw.screenshot({ path: out, fullPage: false });
      console.log(`  → ${out}`);
      await ctx.close();
    }
  } finally {
    await browser.close();
    server.kill('SIGTERM');
  }
}

main().catch(e => { console.error(e); process.exit(1); });

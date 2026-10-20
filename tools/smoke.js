#!/usr/bin/env node
/* Browser smoke test: opens the built HTML files in headless Chrome and reports script errors (failed font downloads are ignored).
     node tools/smoke.js
   Needs puppeteer-core (or puppeteer) and a Chrome; set CHROME=/path/to/chrome if it isn't found. */
'use strict';
const path = require('path'), fs = require('fs');
let pptr;
for (const m of ['puppeteer-core', 'puppeteer', '/opt/npm-tools/node_modules/puppeteer-core', '/opt/npm-tools/node_modules/puppeteer'])
  try { pptr = require(m); break; } catch (e) { /* next */ }
if (!pptr) { console.log('smoke: puppeteer not available, skipped'); process.exit(0); }
const chrome = process.env.CHROME || ['/opt/pw-browsers/chromium-1194/chrome-linux/chrome', '/usr/bin/chromium', '/usr/bin/google-chrome']
  .find(p => fs.existsSync(p));
const ROOT = path.join(__dirname, '..');

(async () => {
  const browser = await pptr.launch({ executablePath: chrome, headless: true, args: ['--no-sandbox'] });
  let bad = 0;
  for (const f of ['three-bases-game.html', 'three-bases-scenarios.html']) {
    const page = await browser.newPage(), errs = [];
    page.on('pageerror', e => errs.push(e.message));
    page.on('console', m => { if (m.type() === 'error' && !/^Failed to load resource/.test(m.text())) errs.push(m.text()); });
    await page.setViewport({ width: 1400, height: 900 });
    await page.goto('file://' + path.join(ROOT, f));
    await new Promise(r => setTimeout(r, 1500));
    console.log(f + ': ' + (errs.length ? errs.slice(0, 3).join(' | ') : 'ok'));
    bad += errs.length;
    await page.close();
  }
  await browser.close();
  process.exit(bad ? 1 : 0);
})();

#!/usr/bin/env node
/* Browser play test: plays real games in the built HTML files and fails on any script error.
   Game: for each faction, its two premade decks against each other (the player's actions are picked from listActions,
   the computer plays itself), up to N player actions. Scenarios: loads every board and plays a few actions on it.
   Card checks (first, in a started game): every card's text renders live; deck lists are sorted by cost, then name;
   each faction shows exactly 5 champions on its cards and deck items; every keyword word in a text has its hover.
     node tools/playtest.js [faction letters, e.g. cd] [--actions N]   (default: all factions, 20 actions)
   Needs puppeteer-core (or puppeteer) and a Chrome, as tools/smoke.js. */
'use strict';
const path = require('path'), fs = require('fs');
let pptr;
for (const m of ['puppeteer-core', 'puppeteer', '/opt/npm-tools/node_modules/puppeteer-core', '/opt/npm-tools/node_modules/puppeteer'])
  try { pptr = require(m); break; } catch (e) { /* next */ }
if (!pptr) { console.log('playtest: puppeteer not available: FAIL'); process.exit(1); }
const chrome = process.env.CHROME || ['/opt/pw-browsers/chromium-1194/chrome-linux/chrome', '/usr/bin/chromium', '/usr/bin/google-chrome']
  .find(p => fs.existsSync(p));
const ROOT = path.join(__dirname, '..');
const args = process.argv.slice(2), ni = args.indexOf('--actions');
const N = ni >= 0 ? +args[ni + 1] : 20;
const facs = (args.find(a => /^[a-z]+$/.test(a) && a !== String(N)) || 'cdabsol').split('');

// in the page: play up to n actions of player 0 (seeded picks), waiting for animations and the computer
const PLAY = async (n, seed) => {
  const wait = async (f, ms = 20000) => { const t = Date.now(); while (!f()) { if (Date.now() - t > ms) return false; await new Promise(r => setTimeout(r, 50)); } return true; };
  let x = seed;
  const rnd = k => { x = (x * 1103515245 + 12345) % 2147483648; return x % k; };
  let done = 0;
  for (; done < n || (game && game.pending && done < n + 5); done++) {  // finish an open choice before stopping
    if (!await wait(() => game && (game.winner != null || (game.cur === 0 && !busy && !aiThinking)))) return `stuck after ${done} actions`;
    if (game.winner != null) break;
    const acts = listActions(game, false).filter(a => a.t !== 'pass');
    const a = acts.length && rnd(4) ? acts[rnd(acts.length)] : { t: 'pass' };
    await act(a);
  }
  return `${done} actions, round ${game.round}`;
};

// in the page, during a game: the card checks; returns a list of problems
const CARD_CHECKS = () => {
  const bad = [], keys = Object.keys(CARDS).filter(k => !CARDS[k].base);
  textSide = 0;
  for (const k of keys) { try { cardHtml(k); } catch (e) { bad.push(`${k}: text does not render (${e.message})`); } }
  textSide = null;
  const facs = [...new Set(keys.map(k => CARDS[k].fac).filter(Boolean))];
  for (const f of facs) {
    const list = keys.filter(k => CARDS[k].fac === f && !CARDS[k].token).sort(byDeckOrder);
    for (let i = 1; i < list.length; i++) {
      const A = CARDS[list[i - 1]], B = CARDS[list[i]];
      if (cardCost(A) === cardCost(B) && A.name.localeCompare(B.name) > 0) { bad.push(`deck order, faction ${f}: ${A.name} before ${B.name}`); break; }
    }
    const champs = list.filter(k => /class="card [^"]*\bchamp\b/.test(cardHtml(k)) && /\bchamp\b/.test(deckItemHtml(k, 1, false)));
    if (list.some(k => CARDS[k].champion) && champs.length !== 5) bad.push(`faction ${f}: ${champs.length} champions shown, need 5`);
  }
  const forms = w => (w === 'Wind' ? 'wind|winds|winding' : w === 'Strike' ? 'strike|strikes' : w.replace(/-/g, '\\-'));
  for (const k of keys) {
    const c = CARDS[k]; if (!c.text) continue;
    const shown = cardText(c).replace(/<span class="kw"[^>]*>[^<]*<\/span>/g, '').replace(/<[^>]*>[^<]*<\/span>/g, '');
    const hov = new Set([...cardText(c).matchAll(/data-k="([^"]+)"/g)].map(m => m[1].toLowerCase()));
    for (const w of Object.keys(KEYWORDS))
      if (!hov.has(w.toLowerCase()) && new RegExp('\\b(' + forms(w) + ')\\b', 'i').test(shown.replace(/\b(am|is|are|was|be|been|gets|get) wound\b/gi, ''))) bad.push(`${c.name}: '${w}' has no hover`);
  }
  return bad;
};

(async () => {
  const browser = await pptr.launch({ executablePath: chrome, headless: true, args: ['--no-sandbox'] });
  let bad = 0;
  const open = async f => {
    const page = await browser.newPage(), errs = [];
    page.on('pageerror', e => errs.push(e.message + ' @ ' + ((e.stack || '').split('\n')[1] || '').trim()));
    page.on('console', m => { if (m.type() === 'error' && !/^Failed to load resource/.test(m.text())) errs.push(m.text()); });
    await page.setViewport({ width: 1400, height: 900 });
    await page.goto('file://' + path.join(ROOT, f));
    await new Promise(r => setTimeout(r, 1200));
    return [page, errs];
  };
  const report = (what, res, errs) => { console.log(`${what}: ${errs.length ? 'FAIL ' + errs.slice(0, 3).join(' | ') : 'ok'} (${res})`); bad += errs.length; };

  {
    const [page, errs] = await open('three-bases-game.html');
    let res = [];
    try {
      res = await page.evaluate(async checks => {
        deckStore.pick = 'p-c1'; deckStore.opp = 'p-c2'; startGame();
        const t = Date.now(); while ($('#mull').hidden && Date.now() - t < 10000) await new Promise(r => setTimeout(r, 50));
        return (eval('(' + checks + ')'))();
      }, CARD_CHECKS.toString());
    } catch (e) { errs.push(e.message); }
    report('card checks', res.length ? res.length + ' problems' : 'all cards', errs.concat(res));
    await page.close();
  }
  for (const f of facs) {
    const [page, errs] = await open('three-bases-game.html');
    let res = '';
    try {
      res = await page.evaluate(async (f, n, play) => {
        deckStore.pick = `p-${f}1`; deckStore.opp = `p-${f}2`;
        if (!deckById(deckStore.pick) || !deckById(deckStore.opp)) return 'premade decks missing';
        startGame();
        const t = Date.now(); while ($('#mull').hidden && Date.now() - t < 10000) await new Promise(r => setTimeout(r, 50));
        $('#mullGo').click();
        return await (eval('(' + play + ')'))(n, 7);
      }, f, N, PLAY.toString());
    } catch (e) { errs.push(e.message); }
    report(`game ${f}1 vs ${f}2`, res, errs);
    await page.close();
  }

  const [p0] = await open('three-bases-scenarios.html');
  const count = await p0.evaluate(() => SCENARIOS.length);
  await p0.close();
  for (let i = 0; i < count; i++) {  // a fresh page per board, so one board's state can't leak into the next
    const [page, errs] = await open('three-bases-scenarios.html');
    let res = '';
    try {
      res = await page.evaluate(async (i, play) => {
        await loadScenario(i);
        return await (eval('(' + play + ')'))(4, i + 1);
      }, i, PLAY.toString());
    } catch (e) { errs.push(e.message); }
    report(`scenario ${i + 1}`, res, errs);
    await page.close();
  }
  await browser.close();
  console.log(bad ? `playtest: FAIL (${bad} errors)` : 'playtest: PASS');
  process.exit(bad ? 1 : 0);
})();

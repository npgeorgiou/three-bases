#!/usr/bin/env node
/* Behaviour checks for the keywords of the seven factions of 4 Nov 2026 (Geared, Offering, Onrush, Flanker, Retaliate, Omen,
   Perennial, Entrenched, Marked, Toll, Barrage, Reserve): each sets up a small board and checks one effect.
   The checks are in tools/fxtest-checks.js.   node tools/fxtest.js */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const SRC = path.join(__dirname, '..', 'src', 'game');
const parts = fs.readFileSync(path.join(SRC, 'parts.txt'), 'utf8').split('\n').map(s => s.trim()).filter(n => /^js\/(00-intro|cards\/|rules\/|ai\/)/.test(n));
const ctx = { console, performance: { now: () => 0 }, structuredClone };
vm.createContext(ctx);
const checks = fs.readFileSync(path.join(__dirname, 'fxtest-checks.js'), 'utf8');
vm.runInContext(parts.map(n => fs.readFileSync(path.join(SRC, n), 'utf8')).join('') + ';globalThis.__t = function () {\n' + checks + '\n};', ctx);
const r = ctx.__t(); console.log(r); process.exit(/failed/.test(r) ? 1 : 0);

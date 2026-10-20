/** The keywords of card k explained, as a column of black panels (empty if it has none). */
function keywordPanel(k, extra = '', states = []) {
  const keywords = [...states, ...keywordsOf(k)], refs = cardRefs(k);
  return keywords.length || refs.length ? `<span class="kwcol ${extra}">${keywords.map(n => `<span class="kwbox"><b>${n}</b>${KEYWORDS[n]}</span>`).join('')}`
    + refs.map(r => `<span class="kwref">${cardHtml(r)}</span>`).join('') + '</span>' : '';
}
/** Cards a card's text names (Shade, Abomination, Doux...), each once: shown beside it with its keywords. */
/** Cards a card names, each once: linked ({{card:…}}, {{need:…}}) or named by plain name in its text or in its keywords' texts. */
let NAME_RE = null;
function cardRefs(k) {
  if (!NAME_RE) {
    const names = Object.keys(CARDS).filter(x => !CARDS[x].base).map(x => [CARDS[x].name, x]).sort((a, b) => b[0].length - a[0].length);
    NAME_RE = { map: new Map(names.map(([n, x]) => [n.toLowerCase(), x])), re: new RegExp('\\b(' + names.map(([n]) => n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|') + ')s?\\b', 'gi') };
  }
  const text = CARDS[k].text || '', out = [...text.matchAll(/\{\{(?:card|need):(\w+)/g)].map(x => x[1]);
  for (const t of [plainText(text.replace(/\{\{(?:card|need):[^}]*\}\}/g, '')), ...keywordsOf(k).map(n => KEYWORDS[n])]) for (const m of t.matchAll(NAME_RE.re)) out.push(NAME_RE.map.get(m[1].toLowerCase()));
  return [...new Set(out)].filter(x => x && CARDS[x] && x !== k);
}

/** Hovering a placed unit: its card, its state this round and its keywords explained. */
function showUnitTip(u, x, y) {
  const tip = $('#tip'), key = [u.id, u.card, u.dmg || 0, u.mv || 0, u.attacked ? 1 : 0, strengthOf(u), defenceOf(u), u.blight ? 1 : 0, JSON.stringify(u.kw || {})].join(':');
  if (tip.dataset.k !== key) {
    const used = usedThisRound(u);
    const notes = (u.dmg > 0 ? `<div class="dmgnote">${u.dmg} shield${u.dmg > 1 ? 's' : ''} lost</div>` : '')
      + (used.length ? `<div class="dmgnote">This round: ${used.join(', ')}</div>` : '');
    const printed = keywordsOf(u.card), gained = KW_FLAGS.filter(f => u.kw && u.kw[f] && !printed.includes(KW_NAME[f])).map(f => KW_NAME[f]).filter(n => KEYWORDS[n]);
    const states = [isBloodied(u) && 'Bloodied', u.blight && 'Blighted', u.tInc && !kw(u, 'incorp') && 'Incorporeal', ...gained].filter(Boolean);
    const boxes = keywordPanel(u.card, '', states);
    tip.innerHTML = `<div class="tipw"><div>${cardHtml(u.card, u)}${notes}</div>${boxes}</div>`;
    tip.dataset.k = key;
  }
  tip.hidden = false;
  // beside the unit's lane, never over it: right of the lane if it fits, else left (keywords then on the far left)
  const box = laneScreenBox(u.lane), gap = 14, w = tip.offsetWidth;
  const fitsRight = box.right + gap + w <= innerWidth - 8, fitsLeft = box.left - gap - w >= 8;
  const right = fitsRight || (!fitsLeft && innerWidth - box.right >= box.left);
  tip.querySelector('.tipw').classList.toggle('flip', !right);
  const h = tip.offsetHeight;
  tip.style.left = Math.max(8, right ? Math.min(box.right + gap, innerWidth - w - 8) : box.left - gap - w) + 'px';
  tip.style.top = Math.max(8, Math.min(innerHeight - h - 8, y - h / 2)) + 'px';
}
/** Screen left/right edges of a lane (both camps). */
function laneScreenBox(lane) {
  const m = $('#board').getScreenCTM(), a = new DOMPoint(LANE_X[lane], 0).matrixTransform(m), b = new DOMPoint(LANE_X[lane] + COLS * CELL, 0).matrixTransform(m);
  return { left: a.x, right: b.x };
}
const hideTip = () => { $('#tip').hidden = true; };

/** A log line with every card name marked (hovering a name shows its card left of the log). */
const LOG_NAME_RE = new RegExp('\\b(' + Object.values(CARDS).map(c => c.name).sort((a, b) => b.length - a.length)
  .map(n => n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|') + ')\\b', 'g');
const CARD_BY_NAME = Object.fromEntries(Object.entries(CARDS).map(([k, c]) => [c.name, k]));
const logHtml = m => m.replace(LOG_NAME_RE, n => `<span class="lname" data-k="${CARD_BY_NAME[n]}">${n}</span>`);
function showLogCard(e) {
  const nm = e.target.closest && e.target.closest('#log .lname'), box = $('#logcard');
  if (!nm) { box.hidden = true; return; }
  if (box.dataset.k !== nm.dataset.k) { box.innerHTML = cardHtml(nm.dataset.k); box.dataset.k = nm.dataset.k; }
  box.hidden = false;
  const r = nm.getBoundingClientRect(), side = $('#log').closest('aside') || $('#log');
  const w = box.offsetWidth, h = box.offsetHeight, left = side.getBoundingClientRect().left;
  box.style.left = Math.max(8, left - w - 12) + 'px';
  box.style.top = Math.max(8, Math.min(innerHeight - h - 8, r.top + r.height / 2 - h / 2)) + 'px';
}

/** Hovering a discard pile: its top card and keywords, left of the pile. */
function showPileTip(e) {
  const el = e.target.closest && e.target.closest('.ptop[data-k]'), tip = $('#pileTip');
  if (!el) { tip.hidden = true; return; }
  const k = el.dataset.k;
  if (tip.dataset.k !== k) { tip.innerHTML = `<div class="tipw flip">${cardHtml(k)}${keywordPanel(k)}</div>`; tip.dataset.k = k; }
  tip.hidden = false;
  const r = el.getBoundingClientRect(), w = tip.offsetWidth, h = tip.offsetHeight;
  tip.style.left = Math.max(8, r.left - w - 6) + 'px';
  tip.style.top = Math.max(8, Math.min(innerHeight - h - 8, r.top + r.height / 2 - h / 2)) + 'px';
}

/** Card texts start large and shrink only as far as needed to fit their card. */
function fitCardText(root) {
  for (const el of root.querySelectorAll ? root.querySelectorAll('.card .ab') : []) {
    el.style.fontSize = '';
    if (!el.clientHeight) continue;
    let f = parseFloat(getComputedStyle(el).fontSize);
    const min = f * 0.6;
    while (el.scrollHeight > el.clientHeight + 1 && f > min) { f *= 0.95; el.style.fontSize = f + 'px'; }
  }
}
let fitQueued = false;
const fitQueue = new Set();
function queueFit(node) {
  fitQueue.add(node);
  if (fitQueued) return;
  fitQueued = true;
  requestAnimationFrame(() => { fitQueued = false; const nodes = [...fitQueue]; fitQueue.clear(); nodes.forEach(n => n.isConnected && fitCardText(n)); });
}

function showKeywordTip(e) {
  const kw = e.target.closest && e.target.closest('.kw'), tip = $('#kwtip');
  if (!kw || kw.closest('.cardbtn, .bcard, .kwcol')) { tip.hidden = true; return; }
  tip.innerHTML = `<b>${kw.dataset.k}</b>${KEYWORDS[kw.dataset.k] || ''}`;
  tip.hidden = false;
  const r = kw.getBoundingClientRect(), w = tip.offsetWidth, h = tip.offsetHeight;
  tip.style.left = Math.max(8, Math.min(innerWidth - w - 8, r.left + r.width / 2 - w / 2)) + 'px';
  tip.style.top = (r.top - h - 8 < 8 ? r.bottom + 8 : r.top - h - 8) + 'px';
}


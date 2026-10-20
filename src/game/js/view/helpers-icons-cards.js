/* =====================================================================
   VIEW: helpers, icons and card rendering
   ===================================================================== */
const $ = sel => document.querySelector(sel);
const $$ = sel => [...document.querySelectorAll(sel)];
const SVG_NS = 'http://www.w3.org/2000/svg';
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

/** Create an SVG element with attributes, optionally appended to parent. */
function svgEl(tag, attrs, parent) {
  const e = document.createElementNS(SVG_NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}

/* Bread (supply) icon: outline plus score lines. BREAD_PLAIN has no inner lines, for numbers. */
const BREAD = ['M3 14C3 8.5 7 6 12 6S21 8.5 21 14V16.5A1.5 1.5 0 0 1 19.5 18H4.5A1.5 1.5 0 0 1 3 16.5Z', 'M8.5 9.5L7.5 12.5M12.5 9L11.5 12.5M16.5 9.5L15.5 12.5'];
const BREAD_PLAIN = 'M2 13.5C2 7.5 6.5 4 12 4S22 7.5 22 13.5V18.5A2 2 0 0 1 20 20.5H4A2 2 0 0 1 2 18.5Z';
const ROLE_GLYPH = { melee: 'M6 18L18 6M8 13l3 3M5 19l2-2', ranged: 'M8 4Q21 12 8 20M8 4V20M4 12H19M16 9l3 3-3 3' };

/** Bread icon as HTML; `kind` picks its style (sup, cost, empty, spent, next, gain, pend). */
function breadHtml(kind = 'sup') {
  return `<svg viewBox="0 0 24 24" class="ico k-${kind}" aria-hidden="true"><path class="b" d="${BREAD[0]}"/><path class="d" d="${BREAD[1]}"/></svg>`;
}
/** Bread icon drawn into an SVG group. */
function svgBread(parent, kind, x, y, size) {
  const icon = svgEl('svg', { x, y, width: size, height: size, viewBox: '0 0 24 24', class: 'ico k-' + kind }, parent);
  svgEl('path', { class: 'b', d: BREAD[0] }, icon);
  svgEl('path', { class: 'd', d: BREAD[1] }, icon);
  return icon;
}
const artSvg = key => `<svg viewBox="0 0 100 100" class="art" aria-hidden="true"><path d="${ART[key]}"/></svg>`;
/** A card's icon (inner SVG): one glyph per card; every unit has a glyph of its own. */
const artInner = k => `<path d="${ART[CARDS[k].art]}"/>`;
const cardArt = k => `<svg viewBox="0 0 100 100" class="art" aria-hidden="true">${artInner(k)}</svg>`;
const deckArt = fac => artSvg(fac === 't' ? 'wreath' : fac === 'x' ? 'lantern' : 'fangs');

/* ---------- keywords ---------- */
const KEYWORD_RE = /\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g;
/** Card text with [[Keyword]] / [[shown|Keyword]] turned into hoverable spans. */
const keywordHtml = text => text.replace(KEYWORD_RE, (m, shown, key) => KEYWORDS[key || shown] ? `<span class="kw" data-k="${key || shown}">${shown}</span>` : shown);

/** Keywords that explain a card: those in its text. */
function keywordsOf(k) {
  const c = CARDS[k], found = new Map();
  for (const [, shown, key] of (c.text || '').matchAll(KEYWORD_RE)) {
    const name = key || shown;
    if (!found.has(name.toLowerCase())) found.set(name.toLowerCase(), name);
  }
  return [...found.values()].filter(name => KEYWORDS[name]);
}

/* ---------- cards ---------- */
const digits = n => String(n).length;

/** Red (strength) or blue (defence) square with a number. */
function statBadge(kind, n) {
  return `<svg viewBox="0 0 24 24" class="ico bdg sq k-${kind}" aria-label="${n}"><rect class="b" x="1.5" y="1.5" width="21" height="21" rx="6"/>`
    + `<text x="12" y="12" dy=".36em" class="numc w" font-size="${digits(n) > 1 ? 11 : 15}">${n}</text></svg>`;
}
/** Bread with a number: yellow for supply, red for a tactic's cost. */
function supplyBadge(n, isCost) {
  return `<svg viewBox="0 0 24 24" class="ico bdg k-${isCost ? 'cost' : 'sup'}" aria-label="${n}"><path class="b" d="${BREAD_PLAIN}"/>`
    + `<text x="12" y="12.9" dy=".36em" class="numc${isCost ? ' lt' : ''}" font-size="${digits(n) > 1 ? 10 : 13}">${n}</text></svg>`;
}
/** Small picture of a unit's shape. */
function shapeMini(card) {
  const cells = shapeCells(card.size, 'h');
  const w = Math.max(...cells.map(x => x[1])) + 1, h = Math.max(...cells.map(x => x[0])) + 1;
  return `<svg viewBox="0 0 ${w * 10} ${h * 10}" class="mini" style="width:calc(var(--cw)*${0.075 * w});height:calc(var(--cw)*${0.075 * h})" aria-label="Size ${card.size}">`
    + cells.map(([r, c]) => `<rect x="${c * 10 + 1}" y="${r * 10 + 1}" width="8" height="8" rx="1.5"/>`).join('') + '</svg>';
}
const corner = (pos, badge) => `<span class="cb ${pos}">${badge}</span>`;
/** Strength (top left) or defence (top right) as a tab that is part of the card's corner. */
const cornerStat = (pos, kind, n, ref = n) => `<span class="cs ${pos} k-${kind}${digits(n) > 1 ? ' two' : ''}${n > ref ? ' up' : n < ref ? ' down' : ''}" aria-label="${n}">${n}</span>`;

/** Card text; with a unit u, its ability hit numbers include u's strength bonus (shown highlighted). */
/** The side whose hand is being drawn (card texts that read its discard pile or carry-over), or null. */
let textSide = null;
function cardText(c, u) {
  const bonus = u ? strengthOf(u) - printedStr(u) : 0, up = n => (bonus > 0 ? `<b class="hup">${n}</b>` : n);
  const side = u && game ? ctl(u) : textSide, live = side !== null && game;
  // Aurelius: which of the cards it needs are in the discard pile; Ossuary Tithe: what it would give now
  const text = c.text.replace(/\{\{need:(\w+)\}\}/g, (m, k) => {
    const name = CARDS[k].name.split(' ')[0];
    return live ? `<b class="need ${game.players[side].discard.includes(k) ? 'ok' : 'no'} cref" data-c="${k}">${name}</b>` : `<span class="cref" data-c="${k}">${name}</span>`;
  }).replace(/\{\{card:(\w+)\|([^}]+)\}\}/g, (m, k, n) => `<span class="cref" data-c="${k}">${n}</span>`).replace('{{debt}}', live ? ` <b class="hup">(now ${debtCost(game, side)})</b>` : '').replace('{{tithe}}', live ? ` <b class="hup">(now +${titheGain(game, side)})</b>` : '');
  return keywordHtml(text.replace(/\{\{(\d+|\+)\}\}/g, (m, n) => (n === '+' ? (bonus > 0 ? `, plus ${up(bonus)}` : '') : up(Math.max(0, +n + bonus)))));
}
function cardHtml(k, u) {
  const c = CARDS[k];
  const text = c.text ? `<span class="ab">${cardText(c, u)}</span>` : '';
  if (c.tactic) {
    return `<div class="card f-${c.fac} tac">${corner('tm', supplyBadge(c.costLabel || c.cost, true))}`
      + `<span class="nm">${c.name}</span>${cardArt(k)}${text}</div>`;
  }
  return `<div class="card f-${c.fac}">${corner('tm', supplyBadge(c.sup))}`
    + (c.str || (c.mods && c.mods.ps) ? cornerStat('tl', 'str', Math.max(0, c.str + ((c.mods && c.mods.ps) || 0)), c.str) : '')
    + (c.def ? cornerStat('tr', 'def', Math.max(1, c.def + ((c.mods && c.mods.pd) || 0)), c.def) : '')
    + `<span class="shape">${shapeMini(c)}</span><span class="nm">${c.name}</span>${cardArt(k)}${text}</div>`;
}


/* =====================================================================
   PANELS: piles, hands, side panel, tooltips
   ===================================================================== */
function stackShadow(n, dir) {
  const layers = [];
  for (let i = 1; i <= Math.min(24, Math.ceil(n / 1.5)); i++) layers.push(`${dir * i * 1.1}px ${i * 1.6}px 0 ${i % 2 ? 'var(--edge)' : 'var(--edge2)'}`);
  return layers.join(',');
}

const CROWN_SVG = '<svg viewBox="0 0 32 24" aria-hidden="true"><path d="M3 20L1.5 6L9.5 12L16 2L22.5 12L30.5 6L29 20Z"/><path d="M3 22H29"/><circle cx="16" cy="2.5" r="2"/><circle cx="1.8" cy="6" r="1.6"/><circle cx="30.2" cy="6" r="1.6"/></svg>';

function carryHtml(p, reserve) {
  const slots = Array.from({ length: MAX_CARRY }, (_, i) => `<span data-slot="${i}">${breadHtml(i < reserve ? 'sup' : 'empty')}</span>`).join('');
  return `<div class="carry" data-p="${p}"><span class="clbl">Carry</span><span class="cslots">${slots}</span></div>`;
}

/** Decks with carry-over, and discard piles, for state B (live or snapshot). */
function renderStacks(B) {
  const v = viewer(), o = other(v);
  for (const [p, sel] of [[o, '#deckOpp'], [v, '#deckMe']]) {
    const P = B.players[p], n = P.drawN !== undefined ? P.drawN : P.draw.length, fac = DECKS[P.deck].fac;
    const crown = B.starter === p ? `<div class="crown">${CROWN_SVG}</div>` : '';
    const stack = `<div class="stack">${crown}<div class="back f-${fac}" style="box-shadow:${n ? stackShadow(n, 1) : 'none'};${n ? '' : 'opacity:.25'}">`
      + `${deckArt(fac)}<span class="dcount">${n}</span></div></div>`
      + `<div class="plabel">${p === v ? 'Your' : 'Their'} deck</div><div class="plabel">In hand · ${P.handN !== undefined ? P.handN : P.hand.length}</div>`;
    const carry = carryHtml(p, P.reserve);
    $(sel).innerHTML = p === o ? stack + carry : carry + stack;
  }
  for (const [p, sel] of [[o, '#pileOpp'], [v, '#pileMe']]) {
    const pile = B.players[p].discard, top = pile[pile.length - 1];
    $(sel).innerHTML = `<div class="stack mirror">${top ? `<div class="ptop" data-k="${top}" style="box-shadow:${stackShadow(pile.length, -1)}">${cardHtml(top)}</div>` : '<div class="pempty"></div>'}</div>`
      + `<div class="plabel">${p === v ? 'Your' : 'Their'} discard · ${pile.length}</div>`;
  }
}

/** The hovered action's simulated result: the carry-over it would use pulses, the carry-over it would add shows green. */
let actPreview = null;
function updateCarryPreview() {
  if (!game) return;
  const t = actPreview && actPreview.state;
  for (const box of $$('.carry')) {
    const p = +box.dataset.p, reserve = game.players[p].reserve, after = t ? t.players[p].reserve : reserve;
    const from = Math.min(reserve, after), to = Math.max(reserve, after);
    for (const slot of box.querySelectorAll('[data-slot]')) {
      const i = +slot.dataset.slot, icon = slot.firstElementChild;
      icon.classList.toggle('k-gain', after > reserve && i >= from && i < to);
      icon.classList.toggle('k-pend', after < reserve && i >= from && i < to);
    }
  }
}

const cardPlayable = i => LANES.some(l => canDeployInLane(i, l));
/** Can hand card i be played in `lane`? */
const cardFitsLane = (i, lane) => canDeployInLane(i, lane);

function renderHand() {
  const v = viewer(), show = myTurn() || settings.mode === 'ai' || busy;
  textSide = v;
  $('#hand').innerHTML = show ? game.players[v].hand.map((k, i) => {
    const classes = ['cardbtn', ui.hi === i && ui.mode && 'on', !(myTurn() && cardPlayable(i)) && 'dim', dragSrc === i && 'dragsrc'].filter(Boolean).join(' ');
    return `<button class="${classes}" data-i="${i}" aria-label="${CARDS[k].name}">${cardHtml(k)}${keywordPanel(k, 'kwside')}</button>`;
  }).join('') : '';
  textSide = null;
  const fac = DECKS[game.players[other(v)].deck].fac;
  $('#oppHand').innerHTML = game.players[other(v)].hand.map(() => `<div class="oback f-${fac}">${deckArt(fac)}</div>`).join('');
  layoutHands();
  markCardsForLane();
}

/** While a lane is hovered, lift the cards that can be played there and dim the rest. */
function markCardsForLane() {
  const active = hoverLane !== null && myTurn() && (!ui.mode || ui.mode === 'unit');
  for (const b of $$('#hand .cardbtn')) {
    const fits = active && cardFitsLane(+b.dataset.i, hoverLane);
    b.classList.toggle('fit', fits);
    b.classList.toggle('nofit', active && !fits);
  }
}

/** Spread cards across a row, overlapping only when they don't fit. */
function spreadRow(box, gap, margin, stackUp) {
  const items = [...box.children];
  if (!items.length) return;
  const width = box.clientWidth, cw = items[0].offsetWidth, n = items.length;
  const step = n > 1 ? Math.min(cw + gap, (width - cw - 2 * margin) / (n - 1)) : 0;
  const start = Math.max(margin, (width - (cw + step * (n - 1))) / 2);
  items.forEach((item, i) => { item.style.left = start + i * step + 'px'; if (stackUp) item.style.zIndex = i + 1; });
}
function layoutHands() {
  spreadRow($('#oppHand'), 22, 12, false);
  const first = $('#hand').firstElementChild;
  const cw = first ? first.offsetWidth : 0;
  spreadRow($('#hand'), Math.max(22, cw * 0.3), Math.max(12, cw * 0.14), true);
  for (const b of $('#hand').children) b.classList.toggle('kwl', b.getBoundingClientRect().right + 260 > innerWidth);
}

function sideTags(p) {
  return (game.starter === p ? '<span class="tagp">started round</span>' : '')
    + (game.passed === p ? '<span class="tagp">passed</span>' : '')
    + (game.cur === p && game.winner === null ? '<span class="tagp go1">to act</span>' : '');
}

const HELP = {
  idle: 'Each action is one turn: deploy, move or attack, then the other side acts. Unit actions cost the unit\'s supply. Each lane\'s supply is used in that lane; carry-over works anywhere. Pass when you\'re done; when both sides pass in a row, the round ends. Space = Pass.',
  deploy: 'Drag the card into a camp with a blue border, or click a cell there.',
};
const rotateButton = () => `<button data-a="rotate">Rotate` + (ui.o === 'h' ? ' · horizontal' : ui.o === 'v' ? ' · vertical' : '') + '</button>';
const usedThisRound = u => [u.moved && 'moved', u.attacked && 'attacked'].filter(Boolean);

function selectedUnitHelp(u) {
  const c = cardOf(u), used = usedThisRound(u);
  let text = `<b>${c.name}</b> selected. Each action costs its supply (${unitSupply(u)}). It can move once and attack once per round`
    + (used.length ? ` (already ${used.join(' and ')})` : '') + '. Green cells: where it can move (R or mouse wheel rotates). ';
  text += c.fixed ? 'It can\'t move. ' : '';
  text += strengthOf(u) > 0
    ? `Click an orange-outlined enemy to attack${c.ranged ? ' (ranged: any enemy in this lane)' : ' (melee: the cells around it; from your front row also the enemy front-row cells facing it' + (c.reach ? ', and as a Pike also from your second row' : '') + ')'}; a red outline means it dies. `
    : 'It can\'t attack. ';
  return `<p class="hint">${text}</p><div class="btns">${orientationsOf(u).length > 1 ? rotateButton() : ''}</div>`;
}

function renderSide() {
  const sel = selectedUnit();
  let html;
  if (!myTurn()) html = `<p class="hint">${game.winner !== null ? '' : busy && isHuman(game.cur) ? 'Resolving…' : 'The other side is acting.'}</p>`;
  else if (ui.mode === 'unit' && sel) html = selectedUnitHelp(sel);
  else if (ui.mode) {
    const k = handCard(ui.hi), rotatable = ui.mode === 'deploy' && k && (CARDS[k].size === 2 || CARDS[k].size === 3);
    html = `<p class="hint">${HELP[ui.mode]}</p><div class="btns">${rotatable ? rotateButton() : ''}</div>`;
  } else html = `<p class="hint">${HELP.idle}</p>`;
  if (myTurn() && ui.mode) html += '<div class="btns"><button data-a="cancel" class="quiet">Cancel (right-click)</button></div>';
  if (ui.err) html += `<p class="err" role="alert">${ui.err}</p>`;
  $('#panel').innerHTML = html;
  renderPassButton();
  showToast(ui.err);

  $('#log').innerHTML = game.log.slice(0, 40).map(x =>
    `<li class="${x.side === null || x.side === undefined ? '' : x.side === viewer() ? 'lme' : 'lop'}">${logHtml(x.m)}</li>`).join('');
  const v = viewer(), o = other(v);
  const line = p => `<b>${deckName(game, p)}</b> ${game.players[p].hand.length} in hand · ${basesHeld(game, p)} bases${sideTags(p)}`;
  $('#oppLine').innerHTML = line(o);
  $('#meLine').innerHTML = line(v);
  renderStacks(game);
  updateCarryPreview();
}

function renderPassButton() {
  const b = $('#passBtn'), mine = myTurn();
  b.disabled = !mine;
  b.textContent = !mine ? (game.winner !== null ? 'Battle over' : 'Waiting…') : game.passed !== null ? 'Pass · end round' : 'Pass';
}

/** Refusal reasons show briefly over the board (the info panel may be closed). */
let toastTimer = null, lastToast = '';
function showToast(msg, kind = 'error') {
  if (!msg || msg === lastToast) { if (!msg) lastToast = ''; return; }
  lastToast = msg;
  const t = $('#toast'), r = $('#board').getBoundingClientRect();
  t.textContent = msg;
  t.className = kind;
  t.hidden = false;
  t.style.left = r.left + r.width / 2 + 'px';
  t.style.top = r.top + 6 + 'px';
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { t.hidden = true; lastToast = ''; }, 2600);
}

/** The info panel starts at the right edge of the board's last lane. */
function placeInfoPanel() {
  const panel = $('#infoPanel'), wrap = $('#boardWrap').getBoundingClientRect(), board = $('#board');
  const m = board.getScreenCTM();
  if (!m) return;
  const edge = new DOMPoint(LANE_X[2] + CELL * 3 + 8, 0).matrixTransform(m).x;
  panel.style.left = Math.max(0, edge - wrap.left) + 'px';
}
function toggleInfoPanel() {
  const panel = $('#infoPanel'), open = panel.hidden;
  panel.hidden = !open;
  $('#infoBtn').setAttribute('aria-pressed', open);
  if (open) placeInfoPanel();
}

function renderStatus() {
  const s = game;
  if (s.winner !== null) $('#status').textContent = s.winner === 'draw' ? 'Draw.' : s.winner === 'lost' ? 'Both sides lose.' : `${deckName(s, s.winner)} wins.`;
  else $('#status').textContent = `Round ${s.round} · ${deckName(s, s.cur)} to act` + (s.passed !== null ? ` · ${deckName(s, s.passed)} passed` : '');
}

function render() {
  renderBoard();
  renderSide();
  renderHand();
  renderStatus();
}


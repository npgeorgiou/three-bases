/* =====================================================================
   DECKS: start page, decks page, deck builder (stored in this browser)
   ===================================================================== */
const DECK_STORE = 'threeBases.v2.decks';
const DECK_MIN = 30, DECK_MAX = 40, COPY_MAX = 3;
const FAC_DECK = Object.fromEntries(Object.entries(DECKS).map(([key, d]) => [d.fac, key]));   // faction -> premade deck key
const deckStore = (() => {
  let st = null;
  try { st = JSON.parse(localStorage.getItem(DECK_STORE) || 'null'); } catch (e) { st = null; }
  const copy = d => ({ id: d.id, name: d.name, cards: { ...d.cards } });
  if (!st || !Array.isArray(st.decks)) st = { decks: PREMADE.map(copy), pick: 'p-t1', opp: 'p-h1', seenPre: PREMADE.map(d => d.id) };
  // the earlier placeholder premade decks are dropped; premade decks this browser hasn't seen yet join the list once
  st.decks = st.decks.filter(d => !['pre-tagma', 'pre-horde', 'pre-exanimati'].includes(d.id));
  delete st.seen;
  st.seenPre = st.seenPre || [];
  for (const d of PREMADE) if (!st.seenPre.includes(d.id)) { st.seenPre.push(d.id); if (!st.decks.some(x => x.id === d.id)) st.decks.push(copy(d)); }
  // new premade lists replace the stored copies of the premade decks (the player's own decks are kept)
  if (st.preVer !== PREMADE_VERSION) { for (const d of PREMADE) { const i = st.decks.findIndex(x => x.id === d.id); if (i >= 0) st.decks[i] = copy(d); else st.decks.push(copy(d)); } st.preVer = PREMADE_VERSION; }
  for (const d of st.decks) for (const k of Object.keys(d.cards)) if (!CARDS[k] || CARDS[k].token) delete d.cards[k];
  return st;
})();
function saveDecks() { try { localStorage.setItem(DECK_STORE, JSON.stringify(deckStore)); } catch (e) { /* kept for this visit only */ } }
const deckCount = d => Object.values(d.cards).reduce((a, n) => a + n, 0);
const deckFac = d => { const k = Object.keys(d.cards).find(k => d.cards[k] > 0); return k ? CARDS[k].fac : null; };
const deckReady = d => { const n = deckCount(d); return n >= DECK_MIN && n <= DECK_MAX && Object.values(d.cards).every(x => x <= COPY_MAX); };
/** Test games: any deck with cards can be played and built, and both sides have unlimited supply. Remembered in this browser. */
const TEST_STORE = 'threeBases.v2.test', IDLE_STORE = 'threeBases.v2.testIdle';
/** In test games the computer opponent only passes (on unless switched off). */
let testIdle = (() => { try { return localStorage.getItem(IDLE_STORE) !== '0'; } catch (e) { return true; } })();
function setTestIdle(on) { testIdle = on; try { localStorage.setItem(IDLE_STORE, on ? '1' : '0'); } catch (e) { /* not remembered */ } }
let testGames = (() => { try { return localStorage.getItem(TEST_STORE) === '1'; } catch (e) { return false; } })();
function setTestGames(on) { testGames = on; try { localStorage.setItem(TEST_STORE, on ? '1' : '0'); } catch (e) { /* not remembered */ } }
const deckPlayable = d => (testGames ? deckCount(d) > 0 : deckReady(d));
const deckById = id => deckStore.decks.find(d => d.id === id) || null;
const facName = f => (f ? DECKS[FAC_DECK[f]].name : 'No faction yet');
/** Deck order: cost (a unit's supply, a tactic's cost), then strength, then defence, then name. */
const cardCost = c => (c.tactic ? (typeof c.cost === 'number' ? c.cost : 0) : c.sup);
const byDeckOrder = (a, b) => {
  const A = CARDS[a], B = CARDS[b];
  return cardCost(A) - cardCost(B) || (A.str ?? -1) - (B.str ?? -1) || (A.def ?? -1) - (B.def ?? -1) || A.name.localeCompare(B.name);
};
/** A unit's shape, small, for deck-list items. */
function dliShape(card) {
  const cells = shapeCells(card.size, 'h'), w = Math.max(...cells.map(x => x[1])) + 1, h = Math.max(...cells.map(x => x[0])) + 1;
  return `<svg viewBox="0 0 ${w * 10} ${h * 10}" class="mini" style="width:${w * 7}px;height:${h * 7}px" aria-label="Size ${card.size}">`
    + cells.map(([r, c]) => `<rect x="${c * 10 + 1}" y="${r * 10 + 1}" width="8" height="8" rx="1.5"/>`).join('') + '</svg>';
}
/** A card drawn as an oblong deck-list-item; as a button when it can be clicked. */
function deckItemHtml(k, n, clickable) {
  const c = CARDS[k], tag = clickable ? 'button' : 'div';
  const inner = (c.tactic ? supplyBadge(c.costLabel || c.cost, true) : supplyBadge(c.sup))
    + `<span class="dn">${c.name}</span>${cardArt(k)}${c.tactic ? '' : dliShape(c)}`
    + (c.str ? statBadge('str', c.str) : '') + (c.def ? statBadge('def', c.def) : '');
  return `<div class="dli"><${tag} class="dlit f-${c.fac}${c.tactic ? ' tac' : ''}" data-k="${k}"${clickable ? `` : ''}>${inner}</${tag}><span class="dc">×${n}</span></div>`;
}
const deckListHtml = (d, clickable) => {
  const keys = Object.keys(d.cards).filter(k => d.cards[k] > 0).sort(byDeckOrder);
  return keys.length ? keys.map(k => deckItemHtml(k, d.cards[k], clickable)).join('') : '<p class="empty">No cards yet.</p>';
};
const deckStatusHtml = d => {
  const n = deckCount(d);
  const t = `${n} card${n === 1 ? '' : 's'}`;
  return deckReady(d) ? t + ' · <span class="dok">Ready</span>' : `<span class="dbad">${t}</span>`;
};

function showPage(id) { for (const x of ['#setup', '#decksPage', '#builder']) $(x).hidden = x !== id; }

/* ---------- start page ---------- */
function renderHome() {
  const mine = deckById(deckStore.pick);
  if (mine && !deckPlayable(mine)) deckStore.pick = null;
  const d = deckById(deckStore.pick);
  $('#homeDeck').innerHTML = d
    ? `<div class="dhead"><b>${escapeHtml(d.name)}</b><span class="dmeta">${facName(deckFac(d))} · ${deckStatusHtml(d)}</span></div><div class="dlist homelist">${deckListHtml(d, false)}</div>`
    : '<p class="empty">No deck picked. Pick a deck or create one to start a battle.</p>';
  $('#editDeckBtn').disabled = !d;
  const fac = d ? deckFac(d) : null;
  const opps = deckStore.decks.filter(x => deckPlayable(x) && fac);   // any ready deck, the same faction included
  if (deckStore.opp !== 'random' && !opps.some(x => x.id === deckStore.opp)) deckStore.opp = opps.length ? opps[0].id : null;
  $('#oppDeck').innerHTML = `<option value="random"${deckStore.opp === 'random' ? ' selected' : ''}>Random deck</option>` + opps.map(x => `<option value="${x.id}"${x.id === deckStore.opp ? ' selected' : ''}>${escapeHtml(x.name)} (${facName(deckFac(x))}, ${deckCount(x)})</option>`).join('');
  $('#oppDeck').disabled = !opps.length;
  $('#oppDeckLbl').textContent = settings.mode === 'ai' ? "Opponent's deck" : "Second player's deck";
  $('#testGames').checked = testGames;
  $('#testIdle').checked = testIdle;
  $('#testIdle').disabled = !testGames;
  $('#testIdle').closest('label').classList.toggle('off', !testGames);
  const why = !d ? 'Pick a deck first.' : !opps.length ? 'No ready deck to play against.' : '';
  $('#startWhy').textContent = why;
  $('#startWhy').hidden = !why;
  $('#startBtn').disabled = !!why;
  saveDecks();
}
const escapeHtml = t => String(t).replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[ch]);

/* ---------- decks page ---------- */
function renderDecksPage() {
  $('#dFacs').innerHTML = Object.values(FAC_DECK).map(key => DECKS[key]).map(D => `<button class="bfac f-${D.fac}" data-fac="${D.fac}" aria-pressed="${dFacs.has(D.fac)}">${artSvg(FAC_ART[D.fac])}${D.name}</button>`).join('');
  $('#deckTiles').innerHTML = deckStore.decks.filter(d => !dFacs.size || dFacs.has(deckFac(d))).map(d => {
    const f = deckFac(d), ready = deckPlayable(d), on = d.id === deckStore.pick;
    return `<div class="dtile${f ? ' f-' + f : ''}${on ? ' on' : ''}${ready ? ' pickable' : ''}" data-id="${d.id}"><b>${escapeHtml(d.name)}</b>`
      + `<span class="dmeta">${facName(f)}</span><span class="dmeta">${deckStatusHtml(d)}</span>`
      + `<div class="choice"><button data-a="edit">Edit</button><button data-a="del" class="danger">Delete</button></div></div>`;
  }).join('') || '<p class="empty">No decks yet.</p>';
}
function deleteDeck(id) {
  const d = deckById(id);
  if (!d || !confirm(`Delete the deck "${d.name}"?`)) return false;
  deckStore.decks = deckStore.decks.filter(x => x.id !== id);
  if (deckStore.pick === id) deckStore.pick = null;
  if (deckStore.opp === id) deckStore.opp = null;
  saveDecks();
  return true;
}

/* ---------- deck builder ---------- */
let edit = null;   // { id, name, cards, dirty }
/** Each faction's symbol (an existing card art) and the factions the card list shows (none picked: all). */
const FAC_ART = { t: 'shield', h: 'fangs', x: 'skull' };
const bFacs = new Set(), dFacs = new Set(), bTypes = new Set();   // bTypes: 'u' units, 's' spells (none picked: both)
let bExclude = false;   // search toggle: include (green) or exclude (red) the matches   // the builder's and the decks page's faction filters
function openBuilder(id) {
  const d = id ? deckById(id) : null;
  edit = { id: d ? d.id : null, name: d ? d.name : 'New deck', cards: d ? { ...d.cards } : {}, dirty: false };
  $('#bName').value = edit.name;
  $('#bSearch').value = '';
  showPage('#builder');
  renderBuilder();
}
function renderBuilder() {
  const fac = deckFac(edit);
  $('#bStat').innerHTML = `${facName(fac)} · ${deckStatusHtml(edit)} · ` + (testGames ? 'test games are on: no card limits' : `up to ${COPY_MAX} of each card`);
  $('#bList').innerHTML = deckListHtml(edit, true);
  $('#bDel').hidden = !edit.id;
  $('#bClear').hidden = !$('#bSearch').value;
  const total = deckCount(edit), terms = $('#bSearch').value.toLowerCase().split(',').map(t => t.trim()).filter(Boolean);
  const shown = k => (!bTypes.size || bTypes.has(CARDS[k].tactic ? 's' : 'u')) && (!terms.length || terms.some(t => cardMatches(k, t)) !== bExclude);
  const facs = Object.values(FAC_DECK).map(key => DECKS[key]);
  $('#bFacs').innerHTML = facs.map(D => `<button class="bfac f-${D.fac}" data-fac="${D.fac}" aria-pressed="${bFacs.has(D.fac)}">${artSvg(FAC_ART[D.fac])}${D.name}</button>`).join('');
  $('#bTypes').innerHTML = [['u', 'Units'], ['s', 'Spells']].map(([t, n]) => `<button class="btype" data-t="${t}" aria-pressed="${bTypes.has(t)}">${n}</button>`).join('');
  $('#bMode').classList.toggle('ex', bExclude); $('#bMode').textContent = bExclude ? 'Exclude' : 'Include'; $('#bMode').setAttribute('aria-pressed', bExclude);
  $('#bCards').innerHTML = (facs.filter(D => !bFacs.size || bFacs.has(D.fac)).map(D => {
    const keys = Object.keys(CARDS).filter(k => CARDS[k].fac === D.fac && !CARDS[k].token && !CARDS[k].base && shown(k)).sort(byDeckOrder);
    if (!keys.length) return '';
    return `<h3 class="f-${D.fac}">${artSvg(FAC_ART[D.fac])}${D.name}</h3><div class="bgrid">` + keys.map(k => {
      const n = edit.cards[k] || 0, other = fac && fac !== D.fac, full = !testGames && (n >= COPY_MAX || total >= DECK_MAX);
      return `<button class="bcard${full && !other ? ' full' : ''}" data-k="${k}"${other || full ? ' disabled' : ''} aria-label="Add ${CARDS[k].name}">${cardHtml(k)}`
        + `<span class="cnt${n ? ' has' : ''}">${testGames ? n : n + '/' + COPY_MAX}</span>${keywordPanel(k, 'kwside')}</button>`;
    }).join('') + '</div>';
  }).join('')) || '<p class="bnone">No card matches the search.</p>';
}
/** Deck-builder search: the card's name, its text as shown, or one of its keywords contains the query. */
/** Deck-builder search: the card's name or text, its keywords and their texts, or the name or text of a card it names. */
function cardMatches(k, query) {
  if (!query) return true;
  const c = CARDS[k], kws = keywordsOf(k), own = k2 => [CARDS[k2].name, plainText(CARDS[k2].text || '')];
  const linked = [...(c.text || '').matchAll(/\{\{(?:card|need):(\w+)/g)].map(x => x[1]).filter(x => CARDS[x]);
  return [...own(k), ...kws, ...kws.map(n => KEYWORDS[n]), ...linked.flatMap(own)].some(x => x.toLowerCase().includes(query));
}
const plainText = t => t.replace(/\[\[([^\]|]+)(\|[^\]]*)?\]\]/g, '$1').replace(/\{\{card:\w+\|([^}]+)\}\}/g, '$1')
  .replace(/\{\{need:(\w+)\}\}/g, (m, k) => CARDS[k].name).replace(/\{\{([^}]*)\}\}/g, '$1');
function changeCard(k, delta) {
  const n = (edit.cards[k] || 0) + delta, fac = deckFac(edit);
  if (n < 0 || (delta > 0 && ((fac && fac !== CARDS[k].fac) || (!testGames && (n > COPY_MAX || deckCount(edit) >= DECK_MAX))))) return;
  if (n) edit.cards[k] = n; else delete edit.cards[k];
  edit.dirty = true;
  renderBuilder();
}
function saveBuilder() {
  edit.name = $('#bName').value.trim() || 'New deck';
  if (edit.id) Object.assign(deckById(edit.id), { name: edit.name, cards: { ...edit.cards } });
  else { edit.id = 'd' + Date.now().toString(36); deckStore.decks.push({ id: edit.id, name: edit.name, cards: { ...edit.cards } }); }
  if (deckPlayable(edit)) deckStore.pick = edit.id;
  edit = null;
  saveDecks();
  showPage(builderReturn);
  if (builderReturn === '#decksPage') renderDecksPage(); else renderHome();
}
let builderReturn = '#setup';
function leaveBuilder() {
  if (edit && (edit.dirty || $('#bName').value.trim() !== edit.name) && !confirm('Leave without saving your changes?')) return;
  edit = null;
  showPage(builderReturn);
  if (builderReturn === '#decksPage') renderDecksPage(); else renderHome();
}

function setupDeckPages() {
  $('#pickDeckBtn').addEventListener('click', () => { renderDecksPage(); showPage('#decksPage'); });
  $('#newDeckBtn').addEventListener('click', () => { builderReturn = '#setup'; openBuilder(null); });
  $('#editDeckBtn').addEventListener('click', () => { if (deckById(deckStore.pick)) { builderReturn = '#setup'; openBuilder(deckStore.pick); } });
  $('#endEditBtn').addEventListener('click', () => { if (!deckById(deckStore.pick)) return; $('#endDlg').hidden = true; builderReturn = '#setup'; openBuilder(deckStore.pick); });
  $('#bEmpty').addEventListener('click', () => { if (!deckCount(edit)) return; edit.cards = {}; edit.dirty = true; renderBuilder(); });
  $('#bTypes').addEventListener('click', e => { const b = e.target.closest('.btype'); if (!b) return; const t = b.dataset.t; if (bTypes.has(t)) bTypes.delete(t); else bTypes.add(t); renderBuilder(); });
  $('#bMode').addEventListener('click', () => { bExclude = !bExclude; renderBuilder(); });
  $('#decksNew').addEventListener('click', () => { builderReturn = '#decksPage'; openBuilder(null); });
  $('#decksBack').addEventListener('click', () => { showPage('#setup'); renderHome(); });
  $('#deckTiles').addEventListener('click', e => {
    const tile = e.target.closest('.dtile'), b = e.target.closest('button[data-a]');
    if (!tile) return;
    const id = tile.dataset.id;
    if (!b) { if (deckPlayable(deckById(id))) { deckStore.pick = id; saveDecks(); showPage('#setup'); renderHome(); } return; }
    if (b.dataset.a === 'edit') { builderReturn = '#decksPage'; openBuilder(id); }
    if (b.dataset.a === 'del' && deleteDeck(id)) renderDecksPage();
  });
  $('#bCards').addEventListener('click', e => { const b = e.target.closest('.bcard'); if (b && !b.disabled) changeCard(b.dataset.k, 1); });
  $('#bList').addEventListener('click', e => { const b = e.target.closest('button.dlit'); if (b) changeCard(b.dataset.k, -1); });
  $('#bName').addEventListener('input', () => { edit.dirty = true; });
  $('#bSearch').addEventListener('input', renderBuilder);
  $('#bClear').addEventListener('click', () => { $('#bSearch').value = ''; renderBuilder(); $('#bSearch').focus(); });
  $('#dFacs').addEventListener('click', e => { const b = e.target.closest('.bfac'); if (!b) return; const f = b.dataset.fac; if (dFacs.has(f)) dFacs.delete(f); else dFacs.add(f); renderDecksPage(); });
  $('#bFacs').addEventListener('click', e => { const b = e.target.closest('.bfac'); if (!b) return; const f = b.dataset.fac; if (bFacs.has(f)) bFacs.delete(f); else bFacs.add(f); renderBuilder(); });
  $('#bSave').addEventListener('click', saveBuilder);
  $('#bBack').addEventListener('click', leaveBuilder);
  $('#bDel').addEventListener('click', () => { if (edit.id && deleteDeck(edit.id)) { edit = null; showPage(builderReturn); builderReturn === '#decksPage' ? renderDecksPage() : renderHome(); } });
  $('#oppDeck').addEventListener('change', () => { deckStore.opp = $('#oppDeck').value; saveDecks(); });
  // builder cards: keyword panels go left of cards near the right edge
  $('#bCards').addEventListener('mouseover', e => { const b = e.target.closest('.bcard'); if (b) b.classList.toggle('kwl', b.getBoundingClientRect().right + 270 > innerWidth); });
  // deck-list items: hovering shows the card and its keywords beside the list
  document.addEventListener('mouseover', e => {
    const it = e.target.closest && e.target.closest('.dlit'), box = $('#dlcard');
    if (!it) { box.hidden = true; return; }
    if (box.dataset.k !== it.dataset.k) { box.innerHTML = `<div class="tipw">${cardHtml(it.dataset.k)}${keywordPanel(it.dataset.k)}</div>`; box.dataset.k = it.dataset.k; }
    box.hidden = false;
    const r = it.closest('.dli').getBoundingClientRect(), w = box.offsetWidth, h = box.offsetHeight;
    box.style.left = Math.min(innerWidth - w - 8, r.right + 12) + 'px';
    box.style.top = Math.max(8, Math.min(innerHeight - h - 8, r.top + r.height / 2 - h / 2)) + 'px';
  });
  renderHome();
}
/** The deck a battle side plays: its cards, named after its army. */
function battleDeck(key, d) {
  const fac = deckFac(d);
  DECKS[key] = { name: DECKS[FAC_DECK[fac]].name, fac, list: Object.entries(d.cards).filter(([, n]) => n > 0) };
  return key;
}
/** Both armies of the same faction: tell the sides apart by adding who plays them to their names. */
function nameMirrorSides() {
  if (DECKS.side0.fac !== DECKS.side1.fac) return;
  const ai = settings.mode === 'ai';
  DECKS.side0.name += ai ? ' (you)' : ' (player 1)';
  DECKS.side1.name += ai ? ' (computer)' : ' (player 2)';
}


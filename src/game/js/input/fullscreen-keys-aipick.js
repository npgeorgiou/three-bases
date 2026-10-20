/* ---------- full screen ---------- */
/** Full screen needs a click (browsers forbid it otherwise); Start battle and the toolbar button ask for it. */
function enterFullscreen() {
  const el = document.documentElement;
  if (!document.fullscreenElement && el.requestFullscreen) el.requestFullscreen({ navigationUI: 'hide' }).catch(() => {});
}
/** In full screen, Chrome and Edge let the game keep Esc (a short press cancels a choice; holding Esc leaves full screen). */
function onFullscreenChange() {
  const on = !!document.fullscreenElement;
  $('#fsBtn').setAttribute('aria-pressed', on);
  $('#fsBtn').setAttribute('aria-label', on ? 'Leave full screen' : 'Full screen');
  if (navigator.keyboard && navigator.keyboard.lock) { if (on) navigator.keyboard.lock(['Escape']).catch(() => {}); else navigator.keyboard.unlock(); }
}

function onKey(e) {
  if (e.target.closest && e.target.closest('input, textarea, select')) return;   // typing in a field
  if (e.key === 'Enter' && !e.repeat) {                  // Enter presses the only button of an open dialog
    const dlg = ['#endDlg', '#cover', '#mull', '#setup'].map(id => $(id)).find(d => !d.hidden);
    if (dlg) { e.preventDefault(); dlg.querySelector('.go').click(); return; }
  }
  if (!game) return;
  if ((e.key === 'r' || e.key === 'R') && canRotate()) rotate();
  if (e.key === 'Escape') cancel();
  if (e.code === 'Space' && !e.repeat) { e.preventDefault(); passOrDone(); }
}

/** Space / the Pass button: pass, or finish a follow-up choice that allows it. */
function passOrDone() {
  if (!myTurn()) return;
  if (game.pending) { if (listActions(game).some(a => a.t === 'done')) act({ t: 'done' }); return; }
  act({ t: 'pass' });
}

function pressToggle(attr, value) {
  settings[attr] = value;
  for (const b of $$(`[data-${attr}]`)) b.setAttribute('aria-pressed', b.dataset[attr] === value);
  if (attr === 'mode') { $('#aiPick').hidden = value !== 'ai'; renderHome(); }
}
/** The computer-player choice in the setup dialog. */
function setupAiPick() {
  $('#testGames').addEventListener('change', () => { setTestGames($('#testGames').checked); renderHome(); });
  $('#testIdle').addEventListener('change', () => setTestIdle($('#testIdle').checked));
  $('#aiKind').value = aiChoice.kind;
  $('#aiKind').addEventListener('change', () => { aiChoice.kind = $('#aiKind').value; saveAiChoice(); });
}


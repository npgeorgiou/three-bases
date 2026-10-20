/* =====================================================================
   SOUND
   Synthesized with Web Audio for now; to be replaced by free sound files.
   ===================================================================== */
const Sound = (() => {
  let ctx = null, noiseBuffer = null;

  function audio() {
    if (!ctx) {
      try { ctx = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { return null; }
    }
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }

  function noise(a) {
    if (!noiseBuffer) {
      noiseBuffer = a.createBuffer(1, a.sampleRate, a.sampleRate);
      const data = noiseBuffer.getChannelData(0);
      for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
    }
    return noiseBuffer;
  }

  function envelope(a, t, dur, gain, attack) {
    const g = a.createGain();
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(gain, t + attack);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    g.connect(a.destination);
    return g;
  }

  /** Filtered noise burst. */
  function burst(t, dur, gain, type, freq, q = 1, freqEnd) {
    const a = audio(); if (!a) return;
    const src = a.createBufferSource(), filter = a.createBiquadFilter();
    src.buffer = noise(a);
    filter.type = type;
    filter.frequency.setValueAtTime(freq, t);
    if (freqEnd) filter.frequency.exponentialRampToValueAtTime(freqEnd, t + dur);
    filter.Q.value = q;
    src.connect(filter);
    filter.connect(envelope(a, t, dur, gain, 0.006));
    src.start(t, Math.random() * 0.5);
    src.stop(t + dur + 0.02);
  }

  /** Oscillator tone, optionally sliding to freqEnd. */
  function tone(t, dur, gain, type, freq, freqEnd) {
    const a = audio(); if (!a) return;
    const osc = a.createOscillator();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, t);
    if (freqEnd) osc.frequency.exponentialRampToValueAtTime(freqEnd, t + dur);
    osc.connect(envelope(a, t, dur, gain, 0.01));
    osc.start(t);
    osc.stop(t + dur + 0.02);
  }

  const now = () => { const a = audio(); return a ? a.currentTime : null; };

  return {
    unlock: audio,
    draw() { const t = now(); if (t === null) return; burst(t, 0.16, 0.18, 'bandpass', 1800, 0.9, 5200); burst(t + 0.05, 0.08, 0.06, 'highpass', 4000); },
    place() { const t = now(); if (t === null) return; tone(t, 0.3, 0.5, 'sine', 110, 42); burst(t, 0.14, 0.3, 'lowpass', 500); burst(t + 0.02, 0.25, 0.08, 'bandpass', 2600, 3); },
    hit() { const t = now(); if (t === null) return; burst(t, 0.13, 0.45, 'bandpass', 1400, 1.2, 500); tone(t, 0.12, 0.25, 'square', 190, 70); },
    death() { const t = now(); if (t === null) return; tone(t, 0.6, 0.28, 'sawtooth', 240, 40); burst(t, 0.5, 0.3, 'lowpass', 900, 1, 120); },
    /** A group marching: several feet per step, two steps per cell moved. */
    march(cells, durationMs) {
      const t0 = now(); if (t0 === null) return;
      const steps = Math.max(2, cells * 2), gap = durationMs / 1000 / steps;
      for (let i = 0; i < steps; i++) {
        const t = t0 + i * gap;
        tone(t, 0.09, 0.22, 'sine', 78, 45);
        for (let k = 0; k < 6; k++) burst(t + Math.random() * 0.045, 0.07, 0.07 + Math.random() * 0.05, 'lowpass', 260 + Math.random() * 260, 0.7);
        burst(t + 0.01, 0.05, 0.03, 'highpass', 3000);
      }
    },
    /** Soft chime: shields restored. */
    heal() { const t = now(); if (t === null) return; tone(t, 0.5, 0.12, 'sine', 880, 1320); tone(t + 0.08, 0.5, 0.08, 'sine', 1320, 1760); },
    /** Clock tick: the turn passes to the other side. */
    tick() { const t = now(); if (t === null) return; tone(t, 0.035, 0.25, 'square', 2300, 1700); burst(t, 0.03, 0.12, 'highpass', 5000); tone(t + 0.11, 0.03, 0.15, 'square', 1900, 1500); },
    /** Gong: a new round begins. */
    gong() {
      const t = now(); if (t === null) return;
      burst(t, 0.25, 0.25, 'lowpass', 900, 1, 200);
      [[98, 0.45, 3.2], [157, 0.25, 2.6], [231, 0.18, 2.2], [312, 0.12, 1.8], [439, 0.08, 1.4]]
        .forEach(([f, g, d]) => tone(t, d, g, 'sine', f, f * 0.985));
    },
    capture() {
      const t = now(); if (t === null) return;
      [[196, 0], [262, 0.16], [330, 0.32], [392, 0.48]].forEach(([f, d]) => {
        const len = d === 0.48 ? 0.8 : 0.3;
        tone(t + d, len, 0.12, 'sawtooth', f);
        tone(t + d, len, 0.1, 'triangle', f * 2);
      });
    },
  };
})();


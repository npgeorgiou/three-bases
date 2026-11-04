const DECKS = {
  siegeworks:{name:'Siegeworks',fac:'g',list:[]},
  arcanists:{name:'Arcanists',fac:'r',list:[]},
  wanderers:{name:'Wanderers',fac:'w',list:[]},
  echoes:{name:'Echoes',fac:'e',list:[]},
  monoliths:{name:'Monoliths',fac:'m',list:[]},
  horologers:{name:'Horologers',fac:'c',list:[]},
};
/** Premade decks: each built around one side of its faction. */
const PREMADE_VERSION = 6;   // raising it replaces the premade decks stored in a browser with these lists
const PREMADE = [
  { id: 'p-g1', name: 'Siegeworks — Big Guns', cards: { g_loader: 3, g_monkey: 3, g_ballista: 3, g_mangonel: 3, g_stone: 3, g_firepot: 3, g_mantlet: 3, g_wagon: 3, g_mastergun: 2, g_ordnance: 2, g_volley: 2, g_makeready: 2, g_breach: 2 } },
  { id: 'p-g2', name: 'Siegeworks — Walls and Sappers', cards: { g_mantlet: 3, g_gabion: 3, g_palisade: 3, g_sapper: 3, g_architect: 2, g_sappercap: 2, g_pioneer: 3, g_wagon: 3, g_handgunner: 3, g_arbalist: 3, g_fortify: 2, g_brace: 2, g_demolish: 1 } },
  { id: 'p-r1', name: 'Arcanists — Spark College', cards: { r_initiate: 3, r_apprentice: 3, r_familiar: 3, r_scribe: 3, r_conduit: 3, r_well: 3, r_prodigy: 2, r_stormcaller: 2, r_kindle: 3, r_brilliance: 2, r_firebolt: 3, r_chain: 2, r_study: 2 } },
  { id: 'p-r2', name: 'Arcanists — Golems and Wards', cards: { r_alchemist: 3, r_artificer: 3, r_golemist: 2, r_wardmage: 3, r_sentinel: 3, r_spellguard: 3, r_mentor: 2, r_archivist: 2, r_conjure: 3, r_lesson2: 3, r_mirrorshield: 2, r_surge: 3, r_fireball: 2 } },
  { id: 'p-w1', name: 'Wanderers — Riders of the Steppe', cards: { w_outrider: 3, w_lancer: 3, w_raider: 3, w_harrier: 3, w_beacon: 3, w_mule: 3, w_wagon: 3, w_pathfinder: 2, w_raiderchief: 2, w_windseer: 2, w_ride: 3, w_shot: 3, w_bolas: 2 } },
  { id: 'p-w2', name: 'Wanderers — Caravans and Exiles', cards: { w_camelteam: 3, w_caravanmaster: 2, w_merchant: 3, w_trader: 3, w_spearman: 3, w_guard: 3, w_elder: 2, w_sweeper: 3, w_khan: 2, w_exile: 3, w_trade: 2, w_volley: 2, w_mend: 2 } },
  { id: 'p-e1', name: 'Echoes — Mirror Host', cards: { e_twin: 3, e_mirror: 3, e_reflect: 3, e_resonator: 3, e_lens: 2, e_seer: 3, e_oldman: 3, e_loopknight: 3, e_chronarch: 1, e_echospell: 3, e_chorus: 2, e_pastblow: 3, e_rewind: 2 } },
  { id: 'p-e2', name: 'Echoes — Chroniclers', cards: { e_acolyte: 3, e_scribe: 3, e_chronicler: 3, e_conductor: 2, e_recaller: 2, e_sentinel: 3, e_oldman: 3, e_oracle: 3, e_paradox: 2, e_timekeeper: 2, e_remember: 2, e_twice: 3, e_again: 2, e_rewind: 1 } },
  { id: 'p-m1', name: 'Monoliths — Waking Spirits', cards: { m_shrine: 3, m_obelisk: 3, m_cairn: 3, m_spiritcaller: 3, m_arch: 2, m_hearth: 3, m_effigy: 3, m_sunpyramid: 1, m_oraclestone: 2, m_awaken: 3, m_rally: 2, m_sunbeam: 3, m_inscribe: 2 } },
  { id: 'p-m2', name: 'Monoliths — The Stone Line', cards: { m_totem: 3, m_pillar: 3, m_menhir: 3, m_dolmen: 3, m_statue: 3, m_hearth: 3, m_wall: 2, m_ancestor: 2, m_waking: 2, m_ley: 3, m_rockfall: 3, m_consecrate: 2, m_judgement: 2 } },
  { id: 'p-c1', name: 'Horologers — The Gear Train', cards: { c_ticker: 3, c_cogsoldier: 3, c_mainspring: 3, c_ratchet: 3, c_drummer: 2, c_gearsmith: 2, c_escapement: 2, c_foundry: 2, c_tower: 1, c_orrery: 1, c_horologer: 1, c_key: 3, c_trainwind: 2, c_fullwind: 2, c_blueprints: 2, c_boiler: 2 } },
  { id: 'p-c2', name: 'Horologers — The Scrap Yard', cards: { c_spentspring: 3, c_bomb: 3, c_scrapper: 3, c_salvager: 2, c_partsman: 2, c_scrapgolem: 2, c_mistress: 1, c_colossus: 1, c_journeyman: 2, c_toymaker: 2, c_rewinder: 2, c_sentinel: 2, c_key: 3, c_strip: 2, c_unwind: 2, c_rights: 2, c_blueprints: 2 } },
];


const DECKS = {
  horologers:{name:'Horologers',fac:'c',list:[]},
  sunfeeders:{name:'Sunfeeders',fac:'d',list:[]},
  impi:{name:'Impi',fac:'a',list:[]},
  hospice:{name:'Hospice Knights',fac:'b',list:[]},
  starpriests:{name:'Star Priests',fac:'s',list:[]},
  rootkin:{name:'Rootkin',fac:'o',list:[]},
  longguns:{name:'The Long Guns',fac:'l',list:[]},
};
/** Premade decks: each built around one side of its faction. */
const PREMADE_VERSION = 7;   // raising it replaces the premade decks stored in a browser with these lists
const PREMADE = [
  { id: 'p-c1', name: 'Horologers — The Gear Train', cards: { c_ticker: 3, c_cogsoldier: 3, c_mainspring: 3, c_ratchet: 3, c_drummer: 2, c_gearsmith: 2, c_escapement: 2, c_foundry: 2, c_tower: 1, c_orrery: 1, c_horologer: 1, c_key: 3, c_trainwind: 2, c_fullwind: 2, c_boiler: 3, c_draughts: 2 } },
  { id: 'p-c2', name: 'Horologers — The Scrap Yard', cards: { c_spentspring: 3, c_bomb: 3, c_scrapper: 3, c_salvager: 2, c_partsman: 2, c_scrapgolem: 2, c_mistress: 1, c_colossus: 1, c_journeyman: 1, c_rewinder: 2, c_sentinel: 2, c_key: 3, c_strip: 1, c_unwind: 1, c_rights: 1, c_pendulum: 2, c_mender: 1, c_tighten: 3, c_boiler: 2, c_patron: 1, c_gate: 2 } },
  { id: 'p-d1', name: 'Sunfeeders — The Cutting Rain', cards: { d_knifedancer: 3, d_youth: 3, d_jaguarscout: 3, d_flintcutter: 2, d_tollwarrior: 2, d_jaguar: 3, d_obsidianknight: 2, d_eagle: 2, d_heartpriest: 2, d_jaguarknight: 1, d_executioner: 1, d_cut: 3, d_heart: 3, d_rain: 2, d_codex: 2 } },
  { id: 'p-d2', name: 'Sunfeeders — The Temple Steps', cards: { d_victim: 3, d_marigold: 3, d_captivetaker: 2, d_bloodletter: 2, d_sundancer: 3, d_altarpriest: 3, d_priestess: 1, d_rackkeeper: 1, d_lady: 1, d_stepspriest: 2, d_templeguard: 2, d_conch: 1, d_suneater: 1, d_captives: 2, d_drop: 1, d_path: 1, d_feed: 2, d_rain: 2, d_heart: 2, d_wailer: 1, d_tribute: 3 } },
  { id: 'p-a1', name: 'Impi — The Wave', cards: { a_runner: 3, a_warrior: 3, a_spearboy: 3, a_drummer: 2, a_induna: 2, a_induna2: 2, a_twinspear: 2, a_bushman: 2, a_regdrum: 2, a_praisesinger: 1, a_regiment: 2, a_warsong: 3, a_again: 2, a_onrush: 2, a_rally: 1, a_hornwarrior: 2, a_stab: 1, a_chest: 3 } },
  { id: 'p-a2', name: 'Impi — Horns and Loins', cards: { a_hornboy: 3, a_hornwarrior: 3, a_chest: 3, a_loinboy: 3, a_loinwarrior: 3, a_horncaptain: 1, a_oldbull: 1, a_kingspear: 1, a_hornrunner: 2, a_reserveleader: 2, a_loinvet: 2, a_chestcap: 1, a_charge: 2, a_advance: 2, a_stab: 2, a_raider: 2, a_raid: 2, a_stabber: 2 } },
  { id: 'p-b1', name: 'Hospice Knights — The Bastion', cards: { b_squire: 3, b_sergeant: 3, b_shieldbro: 3, b_knight: 3, b_bastionguard: 2, b_nurse: 3, b_orderly: 2, b_chaplain: 2, b_castellan: 1, b_mother: 1, b_grandmaster: 1, b_flagbearer: 2, b_mend: 3, b_bookhours: 2, b_prayer: 2, b_granary: 3, b_penitent: 2, b_harden: 1 } },
  { id: 'p-b2', name: 'Hospice Knights — The Thorn Hedge', cards: { b_thorn: 3, b_spikeshield: 3, b_watch: 2, b_gatekeeper: 2, b_thornknight: 3, b_sortieknight: 2, b_challenger: 2, b_sortiecap: 1, b_galley: 1, b_hedge: 1, b_marshal: 1, b_challenge: 1, b_feint: 1, b_sortie: 1, b_bookhours: 1, b_victualler: 2, b_bastionguard: 2, b_shieldbro: 2, b_sergeant: 3, b_mend: 2, b_orderly: 1, b_granary: 1 } },
  { id: 'p-s1', name: 'Star Priests — Fire from the Ziggurat', cards: { s_stargazer: 3, s_astrologer: 3, s_ziggurat: 2, s_highastro: 1, s_starseer: 2, s_exorcist: 3, s_stormcaller: 2, s_lfire: 3, s_lstorm: 2, s_firebolt: 3, s_starfall: 2, s_burn: 3, s_reading: 2, s_tithespell: 2, s_templeguard: 3 } },
  { id: 'p-s2', name: 'Star Priests — The Omen Guards', cards: { s_omenchild: 3, s_bullcalf: 3, s_sealbearer: 2, s_bullman: 3, s_bullgate: 1, s_ward: 2, s_kingseer: 1, s_starofseven: 1, s_chiefscribe: 1, s_lward: 3, s_blessing: 3, s_quicksign: 3, s_charmspell: 3, s_invoke: 2, s_laying: 2, s_reading: 2, s_lfire: 2, s_granary: 3 } },
  { id: 'p-o1', name: 'Rootkin — The Thicket', cards: { o_acorn: 3, o_seedpod: 3, o_hazel: 3, o_mushring: 2, o_leaflitter: 2, o_toadstool: 3, o_mother: 1, o_druid: 1, o_elder: 2, o_compost: 1, o_scatter: 3, o_fall: 2, o_rain: 2, o_whisper: 2, o_mossbed: 2, o_rootling: 3 } },
  { id: 'p-o2', name: 'Rootkin — The Old Grove', cards: { o_youngoak: 3, o_rowan: 3, o_oak: 3, o_ash: 2, o_beech: 2, o_pine: 2, o_deeproot: 1, o_eldest: 1, o_yew: 1, o_rootling: 3, o_nettle: 2, o_vines: 2, o_growth: 3, o_whisper: 2, o_mossbed: 3, o_ivy: 1, o_seedpod: 3 } },
  { id: 'p-l1', name: 'The Long Guns — The Grand Battery', cards: { l_mortar: 3, l_stokes: 2, l_battery: 3, l_greatgun: 2, l_howitzergreat: 1, l_depot: 3, l_runner: 2, l_quarter: 2, l_infantry: 3, l_private: 3, l_gunner: 2, l_bombardier: 2, l_qmgeneral: 1, l_barrage: 2, l_orders: 2, l_observer: 3 } },
  { id: 'p-l2', name: 'The Long Guns — Spot and Strike', cards: { l_observer: 3, l_spotter: 2, l_flare: 2, l_fieldgun: 3, l_sniper: 2, l_howitzer: 3, l_chiefobs: 1, l_major: 1, l_sergeant: 2, l_veteran: 2, l_infantry: 3, l_sandbag: 2, l_spotround: 3, l_overthetop: 2, l_longrange: 2, l_dig: 2, l_depot: 3 } },
];

/** Decks saved from the AI lab ("Use in the game") take the place of premade lists in this browser: the game, the scenarios
 *  and the lab read the same store. The lab's workers have no browser store and get the saved decks with their program. */
const PREMADE_SAVED_STORE = 'threeBases.savedPremades';
const PREMADE_SAVED = (() => {
  try {
    if (typeof localStorage !== 'undefined') return JSON.parse(localStorage.getItem(PREMADE_SAVED_STORE) || 'null');
    return (typeof self !== 'undefined' && self.PREMADE_SAVED_DATA) || null;
  } catch (e) { return null; }
})();
if (PREMADE_SAVED && PREMADE_SAVED.decks) for (const d of PREMADE) {
  const s = PREMADE_SAVED.decks[d.id];
  if (!s || !s.cards) continue;
  const fac = CARDS[Object.keys(d.cards)[0]].fac;
  const cards = Object.fromEntries(Object.entries(s.cards).filter(([k, n]) => CARDS[k] && !CARDS[k].token && CARDS[k].fac === fac && n > 0));
  const n = Object.values(cards).reduce((a, b) => a + b, 0);
  if (n >= 30 && n <= 40 && Object.values(cards).every(x => x <= 3)) { d.cards = cards; d.name = s.name || d.name; d.saved = true; }
}

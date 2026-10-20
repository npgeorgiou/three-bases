const DECKS = {
  tagma:{name:'Tagma',fac:'t',list:[]},
  horde:{name:'Ashfang Horde',fac:'h',list:[]},
  exanimati:{name:'Exanimati',fac:'x',list:[]},
};
/** Premade decks: three per faction, each built around one side of it. */
const PREMADE_VERSION = 4;   // raising it replaces the premade decks stored in a browser with these lists
const PREMADE = [
  { id: 'p-t1', name: 'Tagma — Shield Line', cards: { pavisarios: 3, stratiotes: 3, skoutatoi: 3, kontarioi: 3, hiereus: 3, komes: 3, menavlatoi: 3, thureophoroi: 3, strategos: 2, synaspismos: 3, hodegetria: 2 } },
  { id: 'p-t2', name: 'Tagma — Riders and Archers', cards: { kursor: 3, mandator: 3, stratiotes: 3, toxotes: 3, tourmarches: 3, kavallarios: 3, sphendonetes: 2, hippotoxotai: 3, reform: 3, annona: 3, greekfire: 2 } },
  { id: 'p-t3', name: 'Tagma — Guard and Envoys', cards: { stratiotes: 3, mitaton: 3, voukinator: 3, monomachos: 3, presbeutes: 3, komes: 2, doryphoroi: 3, varangoi: 3, varangianguard: 3, monomachia: 3, bribe: 2 } },
  { id: 'p-h1', name: 'Ashfang Horde — Warhorns', cards: { warhorn: 3, gutsack: 3, fleshshield: 3, bilebloater: 3, undyingreaver: 3, carrionchief: 3, bonebreaker: 3, bloodidol: 3, scarredvet: 2, cull: 2, hellfire: 2 } },
  { id: 'p-h2', name: 'Ashfang Horde — Blood Rites', cards: { paineater: 3, bloodletter: 3, cinderimp: 3, blooddrum: 3, bleedingogre: 3, gorehound: 3, cavetroll: 3, pitfighter: 3, scarredvet: 3, rainblood: 2, cuts: 2, hellfire: 2 } },
  { id: 'p-h3', name: 'Ashfang Horde — Sacrifices', cards: { gutsack: 3, fleshshield: 3, bilebloater: 3, undyingreaver: 3, bloodidol: 3, carrionchief: 3, bonebreaker: 3, ironbehemoth: 2, martyrdom: 3, bloodtithe: 2, carrionfeast: 3 } },
  { id: 'p-x1', name: 'Exanimati — The Mist', cards: { gravewisp: 3, mourner: 3, ashenpenitent: 3, wakecandle: 3, lanternwisp: 3, corpsecandle: 3, strix: 3, bellringer: 2, shadeshepherd: 2, reaper: 2, gravetoll: 2, lastrites: 2, massgrave: 2, danse: 2, debt: 2 } },
  { id: 'p-x2', name: 'Exanimati — The Returned', cards: { bonethrall: 3, labourer: 3, barrowrevenant: 3, embalmer: 3, tombwarden: 3, ninthknight: 3, weepingbride: 2, mardoc: 2, banner: 2, clerk: 2, embalming: 3, lastrites: 2 } },
  { id: 'p-x3', name: 'Exanimati — Plague and Withering', cards: { bonethrall: 3, acolyte: 3, flagellant: 2, feverseer: 3, plagueslinger: 3, duelist: 3, executioner: 3, plagueherald: 2, leperknight: 2, ophra: 2, miasma: 2, creepingrot: 2, hymn: 2, contagion: 2, execution: 2 } },
];


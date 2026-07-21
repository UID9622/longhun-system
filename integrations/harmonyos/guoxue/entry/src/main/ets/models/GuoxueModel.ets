// entry/src/main/ets/models/GuoxueModel.ets
// 龍魂 · 国学创作数据模型
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622
// CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

// === DNA常量 ===
export const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
export const MASTER_UID = "9622";
export const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// === 创作类型 ===
export enum CreationType {
  COUPLET = 'couplet',           // 对联
  CLASSICAL_PROSE = 'prose',     // 文言文
  ACROSTIC_POEM = 'acrostic',   // 藏头诗
  HISTORICAL_FIGURE = 'figure', // 历史人物
  DAO_DE_JING = 'daodejing',    // 道德经
  HE_TU = 'hetu',               // 河图
  LUO_SHU = 'luoshu',           // 洛书
  WU_XING = 'wuxing',           // 五行
  BA_GUA = 'bagua',             // 八卦
  XING_XIU = 'xingxiu',        // 二十八星宿
  FENG_SHUI = 'fengshui'       // 风水
}

// === 通用签名 ===
class Signable {
  protected hashCode(str: string): string {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash = hash & hash;
    }
    return Math.abs(hash).toString(16).substring(0, 16);
  }
}

// === 对联数据 ===
export class CoupletData extends Signable {
  id: string;
  upper: string;
  lower: string;
  horizontal: string;
  theme: string;
  tonePattern: string;
  wordCount: number;
  dnaSignature: string;

  constructor(data: Partial<CoupletData> = {}) {
    super();
    this.id = data.id || `COUPLET-${Date.now()}`;
    this.upper = data.upper || '';
    this.lower = data.lower || '';
    this.horizontal = data.horizontal || '';
    this.theme = data.theme || '';
    this.tonePattern = data.tonePattern || '';
    this.wordCount = data.wordCount || 7;
    this.dnaSignature = `SM3-${this.hashCode(`${this.id}-${this.upper}-${this.lower}-${Date.now()}`)}`;
  }
}

// === 藏头诗数据 ===
export class AcrosticPoemData extends Signable {
  id: string;
  headWord: string;
  lines: string[];
  theme: string;
  style: string;
  dnaSignature: string;

  constructor(data: Partial<AcrosticPoemData> = {}) {
    super();
    this.id = data.id || `ACROSTIC-${Date.now()}`;
    this.headWord = data.headWord || '';
    this.lines = data.lines || [];
    this.theme = data.theme || '';
    this.style = data.style || '七言';
    this.dnaSignature = `SM3-${this.hashCode(`${this.id}-${this.headWord}-${Date.now()}`)}`;
  }
}

// === 历史人物数据 ===
export class HistoricalFigure extends Signable {
  id: string;
  name: string;
  dynasty: string;
  era: string;
  achievements: string[];
  personality: string;
  famousQuotes: string[];
  relatedEvents: string[];
  dnaSignature: string;

  constructor(data: Partial<HistoricalFigure> = {}) {
    super();
    this.id = data.id || `FIGURE-${Date.now()}`;
    this.name = data.name || '';
    this.dynasty = data.dynasty || '';
    this.era = data.era || '';
    this.achievements = data.achievements || [];
    this.personality = data.personality || '';
    this.famousQuotes = data.famousQuotes || [];
    this.relatedEvents = data.relatedEvents || [];
    this.dnaSignature = `SM3-${this.hashCode(`${this.id}-${this.name}-${Date.now()}`)}`;
  }
}

// === 道德经章节 ===
export class DaoDeJingChapter extends Signable {
  id: string;
  chapter: number;
  title: string;
  original: string;
  translation: string;
  interpretation: string;
  keywords: string[];
  dnaSignature: string;

  constructor(data: Partial<DaoDeJingChapter> = {}) {
    super();
    this.id = data.id || `DAO-${Date.now()}`;
    this.chapter = data.chapter || 1;
    this.title = data.title || '';
    this.original = data.original || '';
    this.translation = data.translation || '';
    this.interpretation = data.interpretation || '';
    this.keywords = data.keywords || [];
    this.dnaSignature = `SM3-${this.hashCode(`${this.id}-${this.chapter}-${Date.now()}`)}`;
  }
}

// === 五行数据 ===
export class WuXingData extends Signable {
  id: string;
  element: string;
  generation: string;
  restriction: string;
  color: string;
  direction: string;
  season: string;
  organ: string;
  emotion: string;
  dnaSignature: string;

  constructor(data: Partial<WuXingData> = {}) {
    super();
    this.id = data.id || `WUXING-${Date.now()}`;
    this.element = data.element || '';
    this.generation = data.generation || '';
    this.restriction = data.restriction || '';
    this.color = data.color || '';
    this.direction = data.direction || '';
    this.season = data.season || '';
    this.organ = data.organ || '';
    this.emotion = data.emotion || '';
    this.dnaSignature = `SM3-${this.hashCode(`${this.id}-${this.element}-${Date.now()}`)}`;
  }
}

// === 八卦数据 ===
export class BaGuaData extends Signable {
  id: string;
  name: string;
  symbol: string;
  nature: string;
  attribute: string;
  family: string;
  direction: string;
  number: number;
  dnaSignature: string;

  constructor(data: Partial<BaGuaData> = {}) {
    super();
    this.id = data.id || `BAGUA-${Date.now()}`;
    this.name = data.name || '';
    this.symbol = data.symbol || '';
    this.nature = data.nature || '';
    this.attribute = data.attribute || '';
    this.family = data.family || '';
    this.direction = data.direction || '';
    this.number = data.number || 1;
    this.dnaSignature = `SM3-${this.hashCode(`${this.id}-${this.name}-${Date.now()}`)}`;
  }
}

// === 二十八星宿数据 ===
export class XingXiuData extends Signable {
  id: string;
  name: string;
  direction: string;
  animal: string;
  constellation: string;
  auspicious: boolean;
  meaning: string;
  dnaSignature: string;

  constructor(data: Partial<XingXiuData> = {}) {
    super();
    this.id = data.id || `XINGXIU-${Date.now()}`;
    this.name = data.name || '';
    this.direction = data.direction || '';
    this.animal = data.animal || '';
    this.constellation = data.constellation || '';
    this.auspicious = data.auspicious ?? true;
    this.meaning = data.meaning || '';
    this.dnaSignature = `SM3-${this.hashCode(`${this.id}-${this.name}-${Date.now()}`)}`;
  }
}

// === 创作统计 ===
export interface GuoxueStats {
  totalCouplets: number;
  totalAcrostics: number;
  totalFigures: number;
  totalDaoChapters: number;
  totalWuXing: number;
  totalBaGua: number;
  totalXingXiu: number;
}

// === 全局创作状态 ===
@Observed
export class GuoxueState {
  couplets: CoupletData[] = [];
  acrostics: AcrosticPoemData[] = [];
  figures: HistoricalFigure[] = [];
  daoChapters: DaoDeJingChapter[] = [];
  wuXingList: WuXingData[] = [];
  baGuaList: BaGuaData[] = [];
  xingXiuList: XingXiuData[] = [];
  currentType: CreationType = CreationType.COUPLET;
  currentResult: string = '';

  get statistics(): GuoxueStats {
    return {
      totalCouplets: this.couplets.length,
      totalAcrostics: this.acrostics.length,
      totalFigures: this.figures.length,
      totalDaoChapters: this.daoChapters.length,
      totalWuXing: this.wuXingList.length,
      totalBaGua: this.baGuaList.length,
      totalXingXiu: this.xingXiuList.length
    };
  }

  persist(): void {
    AppStorage.setOrCreate('guoxue_couplets', JSON.stringify(this.couplets.slice(-50)));
    AppStorage.setOrCreate('guoxue_acrostics', JSON.stringify(this.acrostics.slice(-50)));
    AppStorage.setOrCreate('guoxue_figures', JSON.stringify(this.figures.slice(-20)));
  }
}

export const guoxueState = new GuoxueState();
AppStorage.setOrCreate('guoxueState', guoxueState);

/**
 * 🐉 龙魂·易经推演数据模型
 * DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-YIJING-MODELS-v1.0
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 * 创建者: 诸葛鑫（UID9622）
 * GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
 * 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
 */

/**
 * 八卦（三爻卦）— 先天八卦序
 * 乾1兑2离3震4巽5坎6艮7坤8
 */
export enum Trigram {
  QIAN = 0,  // 乾 ☰ 天 · 金
  DUI  = 1,  // 兑 ☱ 泽 · 金
  LI   = 2,  // 离 ☲ 火 · 火
  ZHEN = 3,  // 震 ☳ 雷 · 木
  XUN  = 4,  // 巽 ☴ 风 · 木
  KAN  = 5,  // 坎 ☵ 水 · 水
  GEN  = 6,  // 艮 ☶ 山 · 土
  KUN  = 7,  // 坤 ☷ 地 · 土
}

/** 八卦名称 */
export const TRIGRAM_NAMES: Record<number, string> = {
  0: '乾', 1: '兑', 2: '离', 3: '震',
  4: '巽', 5: '坎', 6: '艮', 7: '坤',
};

/** 八卦符号 */
export const TRIGRAM_SYMBOLS: Record<number, string> = {
  0: '☰', 1: '☱', 2: '☲', 3: '☳',
  4: '☴', 5: '☵', 6: '☶', 7: '☷',
};

/** 八卦五行 */
export const TRIGRAM_WUXING: Record<number, string> = {
  0: '金', 1: '金', 2: '火', 3: '木',
  4: '木', 5: '水', 6: '土', 7: '土',
};

/**
 * 六十四卦完整数据
 */
export interface Hexagram {
  id: number;              // 1-64（周易卦序）
  name: string;            // 卦名（纯中文）
  symbol: string;          // Unicode卦符（䷀-䷿）
  upperTrigram: Trigram;   // 上卦（外卦）
  lowerTrigram: Trigram;   // 下卦（内卦）
  description: string;     // 卦辞
  interpretation: string;  // 彖辞/大象传
  yaoText: string[];       // 爻辞 [初六/初九, ..., 上六/上九]
  image: string;           // 象辞
  attribute: string;       // 卦德/属性标签
}

/**
 * 六爻
 */
export interface Yao {
  position: number;        // 1-6（初=1，上=6）
  name: string;            // 初九/初六, 九二/六二, ...
  isYang: boolean;         // true=阳爻(九), false=阴爻(六)
  isMoving: boolean;       // 是否为动爻
  changed: boolean;        // 是否已变
  sixRelation: string;     // 六亲：父母/兄弟/子孙/妻财/官鬼
  sixSpirit: string;       // 六神：青龙/朱雀/勾陈/腾蛇/白虎/玄武
  shiYing: string;         // 世/应
  text: string;            // 爻辞
}

/**
 * 完整推演结果
 */
export interface HexagramReading {
  dna: string;
  timestamp: string;
  ganzhiTime: string;           // 干支四柱时间
  question: string;             // 所问之事

  // 本卦
  originalHexagram: Hexagram;
  originalYaos: Yao[];
  originalName: string;

  // 变卦（有动爻时）
  changedHexagram?: Hexagram;
  changedYaos?: Yao[];
  changedName?: string;

  // 互卦（本卦的二三四爻为下卦，三四五爻为上卦）
  mutualHexagram?: Hexagram;
  mutualName?: string;

  // 动爻信息
  movingYaoIndices: number[];

  // 世应
  shiPosition: number;
  yingPosition: number;

  // 六亲/六神
  sixRelations: { position: number; relation: string }[];
  sixSpirits: { position: number; spirit: string }[];

  // 综合解读（纯中文）
  interpretation: string;
  suggestion: string;
  warning?: string;

  // 主权锚定
  sovereignty: string;
  confirmCode: string;
  gpg: string;

  // 三色审计
  auditStatus: string;   // 🟢🟡🔴
  auditRScore: number;
  auditDetail?: string;
}

/**
 * 起卦方式枚举
 */
export enum DivinationMethod {
  COINS = 'coins',     // 六爻金钱卦
  TIME  = 'time',      // 时间起卦（梅花易数）
  NUMBERS = 'numbers', // 数字起卦
}

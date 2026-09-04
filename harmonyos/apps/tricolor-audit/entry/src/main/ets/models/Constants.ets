/**
 * 龙魂·全局常量 — 焊死不可改
 * DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-CONSTANTS
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 * 创建者: 诸葛鑫（UID9622）
 */

/** 主权锚点 — 焊死 */
export const SOVEREIGNTY = {
  CREATOR: 'UID9622·诸葛鑫·龍芯北辰',
  ROOT_DNA: '#龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-ROOT',
  GPG_FINGERPRINT: 'A2D0092CEE2E5BA87035600924C3704A8CC26D5F',
  CONFIRM_CODE: '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z',
  SHIELD: '🇨🇳',
  FLAG: '🐉',
  SCALE: '⚖️',
  PACT: '♠️'
};

/** 369不动点 */
export const ANCHOR_369 = {
  SN: 369,
  LOG: 5.911,
  PERM: 108
};

/** 审计维度定义 */
export const AUDIT_DIMENSIONS = [
  { name: '人类福祉', weight: 25 },
  { name: '公平', weight: 20 },
  { name: '可控', weight: 15 },
  { name: '透明', weight: 15 },
  { name: '可追溯', weight: 15 },
  { name: '隐私', weight: 10 }
];

/** 三色阈值 */
export const AUDIT_THRESHOLDS = {
  GREEN: 0.70,
  YELLOW: 0.40
};

/** 颜色映射 */
export const COLOR_MAP: Record<string, { bg: string; text: string; label: string }> = {
  '🟢': { bg: '#1B5E20', text: '#4CAF50', label: '通过' },
  '🟡': { bg: '#F57F17', text: '#FFC107', label: '待核' },
  '🔴': { bg: '#B71C1C', text: '#F44336', label: '红线' }
};

/** 暗金主题色 */
export const DARK_GOLD = {
  PRIMARY: '#D4AF37',
  SECONDARY: '#B8960C',
  BG_DARK: '#0D0D1A',
  BG_CARD: '#1A1A2E',
  TEXT_PRIMARY: '#E0E0E0',
  TEXT_SECONDARY: '#888888',
  BORDER: '#D4AF371A',
  SUCCESS: '#4CAF50',
  WARNING: '#FFC107',
  ERROR: '#F44336'
};

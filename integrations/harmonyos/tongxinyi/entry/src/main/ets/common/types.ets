/*
 * ==========================================================================
 * 通心译 — 统一类型定义
 * DNA:#龍芯⚡️丙午·丙申·癸丑·午时·需-TONGXINYI-TYPES-v1.0
 * ==========================================================================
 * 六层来源链: 道统(曾仕强)·精神(Steve Jobs)·设备(Huawei/HarmonyOS)
 *             ·技术(Open Source)·系统(UID9622)·生命(CNSH)
 * ==========================================================================
 */

/** 翻译模式 */
export enum TranslationMode {
  ZH_TO_EN = 'zh2en',
  EN_TO_ZH = 'en2zh',
  BILINGUAL = 'bilingual'
}

/** 三色审计等级 */
export enum AuditLevel {
  GREEN = 'GREEN',
  YELLOW = 'YELLOW',
  RED = 'RED'
}

/** 三色审计 Emoji */
export const AUDIT_EMOJI: Record<AuditLevel, string> = {
  [AuditLevel.GREEN]: '🟢',
  [AuditLevel.YELLOW]: '🟡',
  [AuditLevel.RED]: '🔴'
};

/** 三层监督 */
export enum SupervisionLayer {
  LOGIC = '逻辑层',
  ETHICS = '价值观层',
  TECHNICAL = '技术层'
}

/** 术语类别 */
export enum TermCategory {
  AI_CORE = 'AI核心',
  PROGRAMMING = '编程术语',
  SYSTEM = '系统术语',
  SECURITY = '安全术语',
  DRAGON_SOUL = '龍魂专属',
  SEVEN_LAYER = '七层协议',
  CUSTOM = '自定义'
}

/** 术语条目 */
export interface TermEntry {
  en: string;
  zh: string;
  enExplanation: string;
  zhExplanation: string;
  category: TermCategory;
}

/** 翻译结果 */
export interface TranslationResult {
  original: string;
  translated: string;
  mode: TranslationMode;
  dnaCode: string;
  auditLevel: AuditLevel;
  auditScore: number;
  timestamp: number;
}

/** 审计记录 */
export interface AuditRecord {
  timestamp: number;
  score: number;
  level: AuditLevel;
  logicPass: boolean;
  ethicsPass: boolean;
  technicalPass: boolean;
  issues: string[];
}

/** 学习反馈 */
export interface LearningFeedback {
  timestamp: number;
  original: string;
  translated: string;
  feedbackType: '👍' | '👎' | '💡' | '🌟';
  comment: string;
}

/** 用户偏好 */
export interface UserPreferences {
  preferredMode: TranslationMode;
  culturalStrictness: 'strict' | 'normal' | 'loose';
  sovereignCharPreference: 'auto' | 'traditional' | 'simplified';
  favoriteTerms: Record<string, string>;
  avoidedTerms: Record<string, { badTranslation: string; reason: string }>;
}

/** HTTP 请求选项 */
export interface HttpOptions {
  method?: string;
  header?: Record<string, string>;
  extraData?: string | Object;
  connectTimeout?: number;
  readTimeout?: number;
  maxRetries?: number;
  retryDelayMs?: number;
}

/** HTTP 请求结果 */
export interface HttpResult<T> {
  success: boolean;
  data?: T;
  errorCode?: number;
  errorMessage?: string;
}

/** 龍魂系统常量 */
export const DRAGON_SOUL_MARKS = {
  DNA: '#龍芯⚡️丙午·丙申·癸丑·午时·需-TONGXINYI-HARMONYOS-v1.0',
  CONFIRM: '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z',
  SEAL: '#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL',
  VERSION: '1.0.0',
  SIX_LAYER: [
    '① 宇宙物理层 (Cosmic-Physical)',
    '② 龍魂DNA层 (Dragon-Soul-DNA)',
    '③ 心智感知层 (Mind-Perception)',
    '④ 文化传承层 (Cultural-Legacy)',
    '⑤ 技术实现层 (Technical-Implementation)',
    '⑥ 应用交互层 (Application-Interface)'
  ],
  AI_TRUTH: '[AI-TRUTH-PROTOCOL v3.0 | 非机器生成确信 | 人类-龍魂协同校验]',
  CHIP_BASE: '华为芯片+鸿蒙底座·通心译 v1.0'
} as const;

/** 五大铁律 */
export const FIVE_LAWS = [
  '铁律1: 中英各自独立生成·非镜像 — 各自重新写·逻辑深度相等',
  '铁律2: 不是镜像·是共鸣 — 比喻可不同·精神必须对上',
  '铁律3: 比喻优先于公式 — 0公式·追求"啊！我懂了"的时刻',
  '铁律4: 古今打通 — 古人问的问题·现代物理给了答案',
  '铁律5: 永远在线·永远迭代 — 比喻不贴切就改·逻辑有漏洞就补'
] as const;

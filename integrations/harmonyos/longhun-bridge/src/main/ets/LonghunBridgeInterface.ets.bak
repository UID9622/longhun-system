// DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-HARMONYOS-BRIDGE-v1.0-UID9622
// CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
// 创建者: 诸葛鑫（UID9622）
//
// 龍魂·鸿蒙桥接器 · 核心接口定义
// 龙魂内核 → ArkTS 服务包 · 三层监督 · 记忆查询 · 进化引擎

/**
 * 监督配置
 */
export interface SupervisionConfig {
  /** 监督灵敏度 (0.0-1.0) */
  sensitivity: number;
  /** 是否启用 DNA 校验 */
  dnaVerify: boolean;
  /** 是否启用三色审计 */
  auditEnabled: boolean;
  /** 最大偏差容忍度 */
  maxDeviation: number;
}

/**
 * 三色审计标记
 */
export enum AuditMark {
  GREEN = 'green',   // 🟢 通过
  YELLOW = 'yellow', // 🟡 待核
  RED = 'red',       // 🔴 红线
}

/**
 * 监督报告
 */
export interface SupervisionReport {
  score: number;
  audit: AuditMark;
  dnaValid: boolean;
  deviations: Deviation[];
  timestamp: string;
  recommendations: string[];
}

/**
 * 偏差条目
 */
export interface Deviation {
  field: string;
  expected: string;
  actual: string;
  severity: AuditMark;
}

/**
 * 记忆条目
 */
export interface MemoryEntry {
  id: string;
  priority: 'P0' | 'P1' | 'P2' | 'P3';
  content: string;
  dna: string;
  tags: string[];
  createdAt: string;
  updatedAt: string;
  frozen: boolean;
}

/**
 * 记忆查询结果
 */
export interface MemoryQueryResult {
  entries: MemoryEntry[];
  total: number;
  queryTimeMs: number;
}

/**
 * 进化快照
 */
export interface EvolutionSnapshot {
  version: string;
  dna: string;
  timestamp: string;
  changes: string[];
}

/**
 * 进化结果
 */
export interface EvolutionResult {
  success: boolean;
  newVersion: string;
  dna: string;
  message: string;
}

/**
 * 龍魂鸿蒙桥接核心接口
 *
 * 用法:
 *   const bridge = LonghunBridge.getInstance();
 *   const result = await bridge.runSupervision(defaultConfig);
 */
export interface LonghunBridgeInterface {
  /**
   * 运行三层监督
   * @param config 监督配置
   * @returns 监督报告
   */
  runSupervision(config: SupervisionConfig): Promise<SupervisionReport>;

  /**
   * 查询记忆
   * @param query 搜索关键词
   * @returns 记忆条目列表
   */
  queryMemory(query: string): Promise<MemoryQueryResult>;

  /**
   * 执行进化
   * @param snapshot 当前状态快照
   * @returns 进化结果
   */
  evolve(snapshot: EvolutionSnapshot): Promise<EvolutionResult>;

  /**
   * 获取系统健康状态
   * @returns 健康状态 JSON
   */
  getHealth(): Promise<string>;

  /**
   * 初始化桥接器（加载 .so 库）
   */
  initialize(): Promise<void>;

  /**
   * 释放资源
   */
  dispose(): void;
}

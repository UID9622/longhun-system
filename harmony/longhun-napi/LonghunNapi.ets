// DNA: #龍芯⚡️丙午·丙申·壬子·子时·䷕贲-HARMONY-NAPI-ETS-v1.0-UID9622
// 创建者: 诸葛鑫（UID9622）
// 协议: MulanPSL v2 (工程层)
// 用途: 鸿蒙 ArkTS NAPI 封装 — 调用 liblonghun_napi.so
// 用法:
//   import { LonghunNapi } from './LonghunNapi';
//   let result = LonghunNapi.governanceCheck("测试内容");
//   console.log(`审计: ${result.auditMark}`);

/**
 * 治理自检结果
 */
export interface GovernanceResult {
  auditMark: string;       // 🟢/🟡/🔴
  vetoClean: boolean;
  gateClean: boolean;
  blackholeHits: string[];
  recommendations: string[];
  timestamp: string;
  dna: string;
}

/**
 * 数据黑洞检测结果
 */
export interface BlackholeResult {
  hit: boolean;
  level?: number;
  description?: string;
}

/**
 * 否决词检测结果
 */
export interface VetoResult {
  hit: boolean;
  word?: string;
  description?: string;
}

/**
 * 监督报告
 */
export interface SupervisionReport {
  score: number;           // 0-100
  audit: string;           // green/yellow/red
  dnaValid: boolean;
  deviations: Deviation[];
  recommendations: string[];
  timestamp: string;
}

export interface Deviation {
  field: string;
  expected: string;
  actual: string;
  severity: string;
}

/**
 * 熔断状态
 */
export interface MeltdownState {
  level: string;
  levelName: string;
  reason: string;
  triggered: boolean;
  recoverable: boolean;
  recoveryCondition: string;
  affectedScope: string;
  summary: string;
}

/**
 * 记忆条目
 */
export interface MemoryEntry {
  id: string;
  content: string;
  tags: string[];
  priority: string;
  createdAt: string;
  dna: string;
}

/**
 * 门控报告
 */
export interface GateReport {
  total: number;
  passed: number;
  failed: number;
  isClean: boolean;
}

/**
 * 龍魂 HarmonyOS NAPI 封装类
 */
export class LonghunNapi {
  // Native 方法由 liblonghun_napi.so 提供

  /**
   * 治理自检 — 最常用入口
   */
  static governanceCheck(content: string): GovernanceResult {
    try {
      const json = napiLonghunGovernanceCheck(content);
      return JSON.parse(json) as GovernanceResult;
    } catch (e) {
      return {
        auditMark: '🔴',
        vetoClean: false,
        gateClean: false,
        blackholeHits: [],
        recommendations: [`NAPI调用失败: ${e}`],
        timestamp: new Date().toISOString(),
        dna: 'ERROR'
      };
    }
  }

  /**
   * 数据黑洞检测
   */
  static checkBlackhole(content: string): BlackholeResult {
    const json = napiLonghunCheckBlackhole(content);
    return JSON.parse(json) as BlackholeResult;
  }

  /**
   * 否决词检测
   */
  static detectVeto(content: string): VetoResult {
    const json = napiLonghunDetectVeto(content);
    return JSON.parse(json) as VetoResult;
  }

  /**
   * 禁止场景检测
   */
  static detectForbidden(content: string): string[] {
    const json = napiLonghunDetectForbidden(content);
    return JSON.parse(json) as string[];
  }

  /**
   * 运行监督
   */
  static runSupervision(configJson?: string): SupervisionReport {
    const json = napiLonghunRunSupervision(configJson || '');
    return JSON.parse(json) as SupervisionReport;
  }

  /**
   * 触发熔断
   */
  static triggerMeltdown(level: string, reason: string, detail: string): MeltdownState {
    const json = napiLonghunTriggerMeltdown(level, reason, detail);
    return JSON.parse(json) as MeltdownState;
  }

  /**
   * 查询记忆
   */
  static queryMemory(query: string): MemoryEntry[] {
    const json = napiLonghunQueryMemory(query);
    return JSON.parse(json) as MemoryEntry[];
  }

  /**
   * 创建记忆
   */
  static createMemory(content: string, tags: string[]): MemoryEntry {
    const json = napiLonghunCreateMemory(content, JSON.stringify(tags));
    return JSON.parse(json) as MemoryEntry;
  }

  /**
   * 门控审计
   */
  static gateCheck(content: string): GateReport {
    const json = napiLonghunGateCheck(content);
    const parsed = JSON.parse(json);
    return {
      total: parsed.total,
      passed: parsed.passed,
      failed: parsed.failed,
      isClean: parsed.overall === 'Pass'
    };
  }

  /**
   * 版本信息
   */
  static version(): string {
    return napiLonghunVersion();
  }
}

// ═══════════════════════════════════════════════════════════════
// Native 函数声明（链接 liblonghun_napi.so）
// ═══════════════════════════════════════════════════════════════

declare function napiLonghunGovernanceCheck(content: string): string;
declare function napiLonghunCheckBlackhole(content: string): string;
declare function napiLonghunDetectVeto(content: string): string;
declare function napiLonghunDetectForbidden(content: string): string;
declare function napiLonghunRunSupervision(configJson: string): string;
declare function napiLonghunTriggerMeltdown(level: string, reason: string, detail: string): string;
declare function napiLonghunQueryMemory(query: string): string;
declare function napiLonghunCreateMemory(content: string, tagsJson: string): string;
declare function napiLonghunGateCheck(content: string): string;
declare function napiLonghunVersion(): string;

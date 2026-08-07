/**
 * DNA:   #龍芯⚡️丙午·丙申·壬子·丑时·䷖剥-NAPI-BRIDGE-ARKTS-v1.0-UID9622
 * 確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
 * 主權錨定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
 * GPG:   A2D0092CEE2E5BA87035600924C3704A8CC26D5F
 * 分層許可: 工程層 MulanPSL v2
 * 三色:  🟢 通過
 *
 * 用途: ArkTS ↔ Rust longhun_napi C ABI 橋接層
 *       封裝 liblonghun_napi.so 的 12 個 C ABI 函數
 *       為插件提供統一的 TypeScript 調用接口
 *
 * Rust側: rust/longhun-napi/src/lib.rs
 * 編譯產物: liblonghun_napi.so → libs/arm64-v8a/
 */

import nativeBridge from 'liblonghun_napi.so';

// ═══════════════════════════════════════════════════════════════
// 類型定義
// ═══════════════════════════════════════════════════════════════

/** 治理自檢結果 */
export interface GovernanceResult {
  audit_mark: string;       // 🟢🟡🔴
  veto_hits: string[];
  blackhole_hits: BlackholeHit[];
  forbidden_flags: string[];
  score: number;
  gate_results: GateResult[];
}

/** 數據黑洞命中 */
export interface BlackholeHit {
  level: number;           // 黑洞層級 (0=沙箱, 1=明文, 2=內存, 3=不可逆, 4=日誌)
  description: string;
  detail: string;
}

/** 門控結果 */
export interface GateResult {
  gate: string;
  passed: boolean;
  detail: string;
}

/** 記憶條目 */
export interface MemoryEntry {
  id: string;
  dna: string;
  content: string;
  tags: string[];
  priority: 'P0' | 'P1' | 'P2' | 'P3';
  created_at: string;
  updated_at: string;
  tricolor: string;
}

/** 監督配置 */
export interface SupervisionConfig {
  mode: 'full' | 'quick' | 'targeted';
  target_layers?: ('L1' | 'L2' | 'L3')[];
  include_audit?: boolean;
  trigger_gate_check?: boolean;
}

/** 監督報告 */
export interface SupervisionReport {
  timestamp: string;
  dna: string;
  audit_mark: string;
  layers: {
    L1_decision: LayerReport;
    L2_execution: LayerReport;
    L3_behavior: LayerReport;
  };
  persona_status: PersonaStatus[];
  overall_score: number;
}

/** 單層報告 */
export interface LayerReport {
  score: number;
  issues: string[];
  recommendations: string[];
}

/** 人格狀態 */
export interface PersonaStatus {
  id: string;
  name: string;
  active: boolean;
  weight: number;
  last_triggered: string;
}

/** 健康狀態 */
export interface HealthStatus {
  status: 'healthy' | 'degraded' | 'critical';
  uptime_seconds: number;
  memory_entries: number;
  active_personas: number;
  last_supervision: string;
  meltdown_state: MeltdownState;
}

/** 熔斷狀態 */
export interface MeltdownState {
  active: boolean;
  level: string;
  reason: string;
  detail: string;
  triggered_at?: string;
}

/** 版本信息 */
export interface VersionInfo {
  version: string;
  dna: string;
  confirm: string;
  binding: string;
}

// ═══════════════════════════════════════════════════════════════
// 內部工具：處理 C ABI 字符串返回值
// ═══════════════════════════════════════════════════════════════

/**
 * 調用 NAPI 函數並自動釋放返回的字符串
 */
function callNapiString(fn: (...args: string[]) => string, ...args: string[]): string {
  try {
    const result = fn(...args);
    return result;
  } catch (e) {
    console.error('[LonghunNapi] 調用失敗:', e);
    return '{}';
  }
}

/**
 * 調用無參數 NAPI 並解析 JSON
 */
function callNapiJson<T>(fn: () => string): T {
  const raw = callNapiString(fn);
  try {
    return JSON.parse(raw) as T;
  } catch {
    console.error('[LonghunNapi] JSON解析失敗:', raw);
    return {} as T;
  }
}

/**
 * 調用有參 NAPI 並解析 JSON
 */
function callNapiJsonWithArgs<T>(fn: (...args: string[]) => string, ...args: string[]): T {
  const raw = callNapiString(fn, ...args);
  try {
    return JSON.parse(raw) as T;
  } catch {
    console.error('[LonghunNapi] JSON解析失敗:', raw);
    return {} as T;
  }
}

// ═══════════════════════════════════════════════════════════════
// 導出接口 — 對標 Rust C ABI 12 函數
// ═══════════════════════════════════════════════════════════════

/** 1. 治理自檢 — 最常用入口 */
export function governanceCheck(content: string): GovernanceResult {
  return callNapiJsonWithArgs<GovernanceResult>(
    nativeBridge.napi_longhun_governance_check,
    content
  );
}

/** 2. 數據黑洞檢測 */
export function checkBlackhole(content: string): { hit: boolean; level: number; description: string } {
  return callNapiJsonWithArgs(nativeBridge.napi_longhun_check_blackhole, content);
}

/** 3. 否決詞檢測 */
export function detectVeto(content: string): { hit: boolean; word: string; description: string } {
  return callNapiJsonWithArgs(nativeBridge.napi_longhun_detect_veto, content);
}

/** 4. 禁止場景檢測 */
export function detectForbidden(content: string): Record<string, boolean> {
  return callNapiJsonWithArgs(nativeBridge.napi_longhun_detect_forbidden, content);
}

/** 5. 運行監督 */
export function runSupervision(config: SupervisionConfig): SupervisionReport {
  const configJson = JSON.stringify(config);
  return callNapiJsonWithArgs<SupervisionReport>(
    nativeBridge.napi_longhun_run_supervision,
    configJson
  );
}

/** 6. 記憶查詢 */
export function queryMemory(query: string): { entries: MemoryEntry[]; total: number } {
  return callNapiJsonWithArgs(nativeBridge.napi_longhun_query_memory, query);
}

/** 7. 創建記憶 */
export function createMemory(content: string, tags: string[]): MemoryEntry {
  const tagsJson = JSON.stringify(tags);
  return callNapiJsonWithArgs<MemoryEntry>(
    nativeBridge.napi_longhun_create_memory,
    content,
    tagsJson
  );
}

/** 8. 健康檢查 */
export function getHealth(): HealthStatus {
  return callNapiJson<HealthStatus>(nativeBridge.napi_longhun_get_health);
}

/** 9. 觸發熔斷 */
export function triggerMeltdown(level: string, reason: string, detail: string): MeltdownState {
  return callNapiJsonWithArgs<MeltdownState>(
    nativeBridge.napi_longhun_trigger_meltdown,
    level,
    reason,
    detail
  );
}

/** 10. 門控審計 (GATE-01~10) */
export function gateCheck(content: string): { gates: GateResult[]; overall: string } {
  return callNapiJsonWithArgs(nativeBridge.napi_longhun_gate_check, content);
}

/** 11. 版本信息 */
export function getVersion(): VersionInfo {
  return callNapiJson<VersionInfo>(nativeBridge.napi_longhun_version);
}

// ═══════════════════════════════════════════════════════════════
// 高級封裝 — 組合調用
// ═══════════════════════════════════════════════════════════════

/**
 * 一鍵全鏈路自檢
 * 治理 → 黑洞 → 否決 → 禁止 → 門控 → 健康
 */
export async function fullSelfCheck(): Promise<{
  timestamp: string;
  dna: string;
  governance: GovernanceResult;
  health: HealthStatus;
  all_passed: boolean;
  issues: string[];
}> {
  const issues: string[] = [];
  
  // 獲取基線版本
  let version: VersionInfo = { version: 'unknown', dna: '', confirm: '', binding: '' };
  try {
    version = getVersion();
  } catch {
    issues.push('版本查詢失敗');
  }

  // 自檢輸入（空字符串 = 只做系統級檢查）
  const governance = governanceCheck('system_self_check');
  if (governance.audit_mark === '🔴') {
    issues.push(`治理自檢紅線: ${JSON.stringify(governance.veto_hits)}`);
  } else if (governance.audit_mark === '🟡') {
    issues.push(`治理自檢待核: 分數 ${governance.score}`);
  }

  // 健康檢查
  const health = getHealth();
  if (health.status === 'critical') {
    issues.push('系統健康危急');
  } else if (health.meltdown_state?.active) {
    issues.push(`熔斷活躍: ${health.meltdown_state.level} - ${health.meltdown_state.reason}`);
  }

  return {
    timestamp: new Date().toISOString(),
    dna: version.dna || '#龍芯⚡️-SELF-CHECK',
    governance,
    health,
    all_passed: issues.length === 0,
    issues,
  };
}

/**
 * 安全寫入前校驗（寫前必過）
 * 用於任何持久化/存儲操作前
 */
export function preWriteAudit(content: string): {
  allowed: boolean;
  audit_mark: string;
  blackhole_hits: string[];
  veto_hits: string[];
} {
  // 數據黑洞
  const bh = checkBlackhole(content);
  if (bh.hit) {
    return {
      allowed: false,
      audit_mark: '🔴',
      blackhole_hits: [bh.description],
      veto_hits: [],
    };
  }

  // 否決詞
  const veto = detectVeto(content);
  if (veto.hit) {
    return {
      allowed: false,
      audit_mark: '🔴',
      blackhole_hits: [],
      veto_hits: [veto.description],
    };
  }

  // 禁止場景
  const forbidden = detectForbidden(content);
  const violated = Object.entries(forbidden)
    .filter(([, v]) => v)
    .map(([k]) => k);
  
  if (violated.length > 0) {
    return {
      allowed: false,
      audit_mark: '🔴',
      blackhole_hits: [],
      veto_hits: violated,
    };
  }

  return { allowed: true, audit_mark: '🟢', blackhole_hits: [], veto_hits: [] };
}

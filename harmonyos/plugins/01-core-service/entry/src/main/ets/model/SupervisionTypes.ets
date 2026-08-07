/**
 * 🐉 龍魂·监督类型定义 (Supervision Types)
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-SUPERVISION-TYPES-UID9622
 * 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
 * 分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
 */

// ─── 三色审计枚举 ───
export enum Tricolor {
  GREEN = '🟢',   // 通过
  YELLOW = '🟡',  // 待核
  RED = '🔴'      // 红线
}

// ─── 人格状态 ───
export interface PersonaState {
  id: string;              // P00-P15
  name: string;            // 人格名称
  layer: string;           // 战略/执行/文化/守护
  role: string;            // 职能描述
  weight: number;          // 权重 1-15
  active: boolean;         // 是否激活
  tricolor: Tricolor;     // 三色状态
  isolationRate?: number;  // 情感隔离率（P02专用）
  lastActive?: string;     // 最后活跃时间
}

// ─── 监督层结果 ───
export interface LayerResult {
  tricolor: Tricolor;
  interceptCount: number;
  details: string;
}

// ─── 监督周期结果 ───
export interface SupervisionResult {
  cycle: number;
  timestamp: string;
  L1_decision: LayerResult;   // 决策监督层
  L2_execution: LayerResult;  // 执行监督层
  L3_behavior: LayerResult;   // 行为监督层
  overall_tricolor: Tricolor;
  persona_states: PersonaState[];
  total_intercepts: number;
}

// ─── 主权验证结果 ───
export interface SovereigntyVerifyResult {
  passed: boolean;
  checks: SovereigntyCheck[];
  timestamp: string;
  dna: string;
}

// ─── 主权验证单项 ───
export interface SovereigntyCheck {
  name: string;
  passed: boolean;
  expected: string;
  actual: string;
  tricolor: Tricolor;
}

// ─── 进化指标 ───
export interface EvolutionMetrics {
  intercept_rate: number;     // 拦截率
  red_team_success: number;   // 红队成功率
  entropy: number;            // 系统熵值
  cycle: number;              // 进化周期
  timestamp: string;
}

// ─── 芯片信息 ───
export interface ChipInfo {
  manufacturer: string;
  model: string;
  architecture: string;
  cores: number;
  maxFreq: string;
  gpuModel: string;
}

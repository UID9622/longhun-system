// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.1
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

/** 服务器连接配置 */
export class ServerConfig {
  host: string = 'uid9622.cn'
  useTls: boolean = true
  ports: Record<string, number> = {
    knowledge: 8766,
    antenna: 8769,
    guanlan: 8770,
    xiaoyi: 8799
  }

  /** 构建完整API URL */
  baseUrl(service: string): string {
    const scheme = this.useTls ? 'https' : 'http'
    const port = this.ports[service] ?? 8766
    return `${scheme}://${this.host}:${port}`
  }
}

/** 通用API响应结构 */
export class ApiResponse<T> {
  code: number = 0
  message: string = ''
  data?: T
  dna?: string
  audit?: AuditMark
}

/** 审计标记 */
export class AuditMark {
  timestamp: string = ''
  checksum: string = ''
  level: string = 'L3'
  color: string = '🟢'
}

/** 聊天消息 */
export class ChatMessage {
  id: string = ''
  role: 'user' | 'assistant' | 'system' = 'user'
  content: string = ''
  persona?: string
  dna?: string
  timestamp: number = Date.now()
  isError: boolean = false
}

/** 系统状态快照 */
export class SystemStatus {
  cpu_percent: number = 0
  memory_percent: number = 0
  disk_percent: number = 0
  uptime_seconds: number = 0
  active_personas: number = 0
  engines_healthy: number = 0
  engines_total: number = 0
  circuit_breaker_tripped: boolean = false
  last_update: number = 0
}

/** 观澜引擎信息 */
export class EngineInfo {
  name: string = ''
  type: string = 'local'  // local | cloud
  status: string = 'unknown'
  version: string = ''
}

/** 观澜路由请求/响应 */
export class RouteRequest {
  task: string = ''
  preference?: string
  force_local: boolean = false
}

export class RouteResponse {
  engine: string = ''
  result: string = ''
  persona?: string
  confidence: number = 0
  audit: string = '🟢'
}

/** 蚁触推理请求/响应 */
export class InferRequest {
  text: string = ''
  bagua_hint?: string
}

export class InferResponse {
  bagua: string = ''
  gate_name: string = ''
  element: string = ''
  route: string = ''
  confidence: number = 0
  reasoning: string = ''
}

/** 八门卦象 */
export class BaguaGate {
  name: string = ''
  gua: string = ''
  element: string = ''
  direction: string = ''
  function: string = ''
  color: string = ''
}

/** DNA追溯条目 */
export class DnaEntry {
  dna: string = ''
  module: string = ''
  action: string = ''
  timestamp: string = ''
  creator: string = 'UID9622'
  audit_color: string = '🟢'
  device_code?: string
  cached: boolean = false
}

/** 网络连接状态 */
export enum ConnectionState {
  ONLINE = 'online',
  OFFLINE = 'offline',
  RECONNECTING = 'reconnecting'
}

// ══════ v1.1 新增类型 ══════

/** v1.1 API标准请求头 */
export class ApiHeaders {
  'X-LongHun-DNA': string = ''
  'X-LongHun-UID': string = '9622'
  'X-LongHun-Confirm': string = '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z'
  'X-LongHun-Timestamp': string = ''
  'X-LongHun-Device': string = 'HM-9622-001'
  'X-LongHun-Signature': string = ''
}

/** v1.1 API标准响应体 */
export class PersonaResponse {
  dna: string = ''
  persona: string = ''
  route: string = ''
  result: string = ''
  audit: {
    timestamp: string
    checksum: string
    level: string
  } = { timestamp: '', checksum: '', level: 'L3' }
}

/** 种子人格执行结果（端侧） */
export class SeedPersonaOutput {
  code: string = ''
  name: string = ''
  action: string = ''
  confidence: number = 0
  reasoning: string = ''
  audit: string = '🟢'
}

/** 离线模式状态 */
export class OfflineState {
  dna_loaded: boolean = false
  dna_count: number = 0
  dna_loaded_at: number = 0
  audit_log_count: number = 0
  chat_history_count: number = 0
  storage_bytes: number = 0
}

/** 本地DNA查询参数 */
export class LocalDnaQuery {
  layer?: string
  status?: string
  module?: string
  keyword: string = ''
  limit: number = 50
}

/** 语音录制的状态 */
export enum VoiceState {
  IDLE = 'IDLE',
  RECORDING = 'RECORDING',
  PROCESSING = 'PROCESSING',
  DONE = 'DONE',
  ERROR = 'ERROR'
}

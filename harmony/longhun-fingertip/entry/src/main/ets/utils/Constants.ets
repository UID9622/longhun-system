// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.1
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

/** 龍魂·指尖 — 全局常量 */
export class Constants {
  // ── 身份 ──
  static readonly UID: string = '9622'
  static readonly CONFIRM_CODE: string = '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z'
  static readonly DNA_PREFIX: string = '#龍芯⚡️'

  // ── 鲲鹏服务器（默认） ──
  static readonly DEFAULT_HOST: string = 'uid9622.cn'
  static readonly DEFAULT_PORTS: Record<string, number> = {
    knowledge: 8766,   // 知识中枢
    antenna: 8769,     // 蚁触·八门路由
    guanlan: 8770,     // 观澜浏览器路由
    xiaoyi: 8799       // 小艺桥接
  }

  // ── API路径 ──
  static readonly API = {
    // 观澜 (8770)
    GUANLAN_HEALTH: '/health',
    GUANLAN_STATUS: '/status',
    GUANLAN_ROUTE: '/route',
    GUANLAN_CIRCUIT_BREAKER: '/circuit-breaker',
    GUANLAN_ENGINES: '/engines',
    GUANLAN_LEDGER: '/ledger',
    GUANLAN_GATEWAY: '/gateway',
    GUANLAN_ANNOTATE: '/annotate',
    GUANLAN_COMPARE: '/compare',
    GUANLAN_PRIVACY_SCAN: '/privacy/scan',

    // 蚁触·八门 (8769)
    ANTENNA_HEALTH: '/health',
    ANTENNA_INFER: '/infer',
    ANTENNA_BATCH: '/batch',
    ANTENNA_WUXING: '/wuxing',
    ANTENNA_MESH: '/mesh',
    ANTENNA_BAGUA: '/bagua',
    ANTENNA_BENCHMARK: '/benchmark',

    // 知识中枢 (8766)
    KNOWLEDGE_STATUS: '/v1/li/status',
    KNOWLEDGE_CHAT: '/v1/li/chat',
    KNOWLEDGE_MODELS: '/v1/li/models',

    // 小艺桥接 (8799)
    XIAOYI_STATUS: '/api/v1/xiaoyi/status',
    XIAOYI_CHAT: '/api/v1/chat',
    XIAOYI_MODELS: '/api/v1/chat/models',
    XIAOYI_HEALTH: '/api/v1/xiaoyi/health',
    XIAOYI_CAPABILITIES: '/api/v1/xiaoyi/capabilities'
  }

  // ── 缓存 ──
  static readonly CACHE_PREFIX_DNA: string = 'lh_dna_'
  static readonly CACHE_PREFIX_CHAT: string = 'lh_chat_'
  static readonly CACHE_PREFIX_STATUS: string = 'lh_status_'
  static readonly MAX_CACHE_ITEMS: number = 500
  static readonly CACHE_TTL_MS: number = 7 * 24 * 60 * 60 * 1000  // 7天

  // ── UI ──
  static readonly COLORS = {
    BG_PRIMARY: '#0a0a0a',
    BG_SECONDARY: '#1a1a1a',
    BG_CARD: '#1e1e1e',
    GOLD: '#FFD700',
    GOLD_DIM: '#B8960F',
    TEXT_PRIMARY: '#FFFFFF',
    TEXT_SECONDARY: '#AAAAAA',
    GREEN: '#00FF88',
    RED: '#FF4444',
    BLUE: '#4488FF',
    BORDER: '#333333'
  }

  // ── 网络 ──
  static readonly REQUEST_TIMEOUT: number = 30_000  // 30s
  static readonly RECONNECT_DELAY: number = 3_000    // 3s
  static readonly MAX_RETRIES: number = 3

  // ── 设备标识 ──
  static readonly DEVICE_CODE: string = 'HM-9622-001'
  static readonly DEVICE_TYPE: string = 'harmonyos'

  // ── 离线模式 ──
  static readonly MAX_OFFLINE_DNA_CACHE: number = 500
  static readonly DNA_SYNC_INTERVAL_MS: number = 24 * 60 * 60 * 1000  // 24小时

  // ── 种子人格 ──
  static readonly SEED_PERSONAS: string[] = ['P00-文心', 'P02-宝宝', 'P77-黑天使']
  static readonly PERSONA_TIMEOUT_MS: number = 5_000  // 种子人格推理超时5s

  // ── 语音 ──
  static readonly VOICE_MAX_DURATION_MS: number = 60_000   // 最长录音60s
  static readonly VOICE_SAMPLE_RATE: number = 16000         // 采样率16kHz
  static readonly VOICE_CHANNELS: number = 1                // 单声道
  static readonly VOICE_FORMAT: string = 'audio/mp4a-latm'  // AAC格式

  // ── 数据主权护栏（v1.1新增·焊死） ──
  // 以下数据永不进入分布式计算·仅本地存储·不传输原始数据
  static readonly SOVEREIGN_DATA_KEYS: string[] = [
    'dna_registry',    // DNA注册表
    'audit_log',       // 审计日志
    'chat_history',    // 记忆库
    'user_prefs'       // 用户偏好
  ]

  // ── WebSocket ──
  static readonly WS_RECONNECT_DELAY: number = 5_000   // WS重连延迟5s
  static readonly WS_MAX_RECONNECT: number = 10         // WS最大重连次数
}

// DNA: #龍芯⚡️丙午·癸未·甲子·既济-编辑器落地-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

/** 龍魂·编辑器 — 全局常量 */
export class Constants {
  // ── 身份 ──
  static readonly UID: string = '9622'
  static readonly CONFIRM_CODE: string = '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z'
  static readonly DNA_PREFIX: string = '#龍芯⚡️'

  // ── 鲲鹏服务器 ──
  static readonly DEFAULT_HOST: string = 'uid9622.cn'
  static readonly DEFAULT_PORTS: Record<string, number> = {
    antenna: 8769,     // 蚁触·八门路由
    guanlan: 8770,     // 观澜浏览器路由
    audit: 8766,       // 知识中枢（审计代理）
    xiaoyi: 8799       // 小艺桥接（预留）
  }

  // ── 编辑器API路径（匹配鲲鹏实际端点） ──
  static readonly API = {
    // 观澜路由 (8770) — 代码/文案/审查
    GUANLAN_ROUTE: '/route',
    GUANLAN_AUDIT: '/plugin/audit',
    GUANLAN_HEALTH: '/health',

    // 蚁触推理 (8769) — 自动意图路由
    ANTENNA_INFER: '/infer',
    ANTENNA_HEALTH: '/health'
  }

  // ── AI按钮配置（匹配鲲鹏实际端点） ──
  static readonly AI_BUTTONS: AiButtonConfig[] = [
    {
      icon: '🤖',
      label: '代码',
      task: 'code',
      service: 'guanlan',
      endpoint: '/route',
      personas: '宝宝+鲁班',
      description: '生成/补全代码'
    },
    {
      icon: '✍️',
      label: '文案',
      task: 'copywriting',
      service: 'guanlan',
      endpoint: '/route',
      personas: '李白+文心',
      description: '润色/生成文案'
    },
    {
      icon: '🔍',
      label: '审查',
      task: 'audit',
      service: 'guanlan',
      endpoint: '/plugin/audit',
      personas: '雯雯+法律引擎',
      description: '代码/文案审查'
    },
    {
      icon: '⚡',
      label: '路由',
      task: 'auto_route',
      service: 'antenna',
      endpoint: '/infer',
      personas: '诸葛亮+八门路由',
      description: '自动判断意图分配人格'
    }
  ]

  // ── UI主题 ──
  static readonly COLORS = {
    BG_PRIMARY: '#0a0a0a',
    BG_SECONDARY: '#1a1a1a',
    BG_CARD: '#1e1e1e',
    BG_INPUT: '#151515',
    GOLD: '#FFD700',
    GOLD_DIM: '#B8960F',
    GOLD_DARK: '#8B7500',
    TEXT_PRIMARY: '#FFFFFF',
    TEXT_SECONDARY: '#AAAAAA',
    TEXT_DIM: '#666666',
    GREEN: '#00FF88',
    RED: '#FF4444',
    YELLOW: '#FFD700',
    BLUE: '#4488FF',
    BORDER: '#333333',
    BORDER_GOLD: '#FFD70044'
  }

  // ── 网络 ──
  static readonly REQUEST_TIMEOUT: number = 30_000
  static readonly RECONNECT_DELAY: number = 3_000
  static readonly MAX_RETRIES: number = 3

  // ── 设备标识 ──
  static readonly DEVICE_CODE: string = 'HM-9622-001'
  static readonly DEVICE_TYPE: string = 'harmonyos'

  // ── 语音 ──
  static readonly VOICE_MAX_DURATION_MS: number = 60_000
  static readonly VOICE_SAMPLE_RATE: number = 16000

  // ── DNA ──
  static readonly DNA_PROJECT: string = '编辑器落地'
  static readonly DNA_VERSION: string = 'v1.0'
  static readonly MAX_DNA_LOG: number = 200

  // ── 离线缓存 ──
  static readonly CACHE_PREFIX_DRAFT: string = 'editor_draft_'
  static readonly CACHE_PREFIX_HISTORY: string = 'editor_history_'
  static readonly MAX_HISTORY_ITEMS: number = 100
}

/** AI按钮配置 */
export class AiButtonConfig {
  icon: string = ''
  label: string = ''
  task: string = ''
  service: string = ''
  endpoint: string = ''
  personas: string = ''
  description: string = ''
}

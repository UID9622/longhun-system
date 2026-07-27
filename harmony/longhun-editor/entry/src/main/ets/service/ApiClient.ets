// DNA: #龍芯⚡️丙午·癸未·甲子·既济-编辑器落地-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import http from '@ohos.net.http'
import { Constants } from '../utils/Constants'

/**
 * 龍魂·编辑器 API统一客户端 v1.0
 *
 * 复用指尖ApiClient架构，适配编辑器四按钮场景：
 * - 代码 POST /api/v1/guanlan/infer (task=code)
 * - 文案 POST /api/v1/guanlan/infer (task=copywriting)
 * - 审查 POST /api/v1/audit/submit (task=audit)
 * - 路由 POST /api/v1/antenna/route (auto_route=true)
 */
export class ApiClient {
  private host: string = Constants.DEFAULT_HOST
  private useTls: boolean = true
  private dnaGenDna: string = ''

  setServer(host: string, useTls: boolean = true): void {
    this.host = host
    this.useTls = useTls
  }

  /** 构建基本URL */
  private baseUrl(service: string): string {
    const scheme = this.useTls ? 'https' : 'http'
    const port = Constants.DEFAULT_PORTS[service] ?? 8770
    return `${scheme}://${this.host}:${port}`
  }

  /** 构建v1.0标准请求头 */
  private buildHeaders(): Record<string, string> {
    const now = new Date().toISOString()
    return {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-LongHun-DNA': `${Constants.DNA_PREFIX}${this.dnaGenDna || '丙午·癸未·甲子·既济-编辑器落地-v1.0'}`,
      'X-LongHun-UID': Constants.UID,
      'X-LongHun-Confirm': Constants.CONFIRM_CODE,
      'X-LongHun-Timestamp': now,
      'X-LongHun-Device': Constants.DEVICE_CODE,
      'X-LongHun-Signature': `HM-SHA256-${Constants.UID}-${now.substring(0, 10)}-${Constants.DEVICE_CODE}`
    }
  }

  // ══════ 四个AI按钮专用方法 ══════

  /** 代码生成/补全 → POST /route (guanlan:8770) */
  async inferCode(context: string): Promise<EditorResponse> {
    const raw = await this.post<GuanlanRouteRaw>('guanlan', Constants.API.GUANLAN_ROUTE, {
      task: 'code',
      context: context
    })
    return this.mapGuanlanRoute(raw, '代码生成')
  }

  /** 文案润色/生成 → POST /route (guanlan:8770) */
  async inferCopywriting(context: string): Promise<EditorResponse> {
    const raw = await this.post<GuanlanRouteRaw>('guanlan', Constants.API.GUANLAN_ROUTE, {
      task: 'copywriting',
      context: context
    })
    return this.mapGuanlanRoute(raw, '文案润色')
  }

  /** 代码/文案审查 → POST /plugin/audit (guanlan:8770) */
  async submitAudit(content: string): Promise<EditorResponse> {
    const raw = await this.post<GuanlanAuditRaw>('guanlan', Constants.API.GUANLAN_AUDIT, {
      permissions: ['code', 'text'],
      content: content
    })
    return this.mapGuanlanAudit(raw, content)
  }

  /** 自动意图路由 → POST /infer (antenna:8769) */
  async autoRoute(intent: string): Promise<EditorResponse> {
    const raw = await this.post<AntennaInferRaw>('antenna', Constants.API.ANTENNA_INFER, {
      text: intent,
      bagua_hint: null
    })
    return this.mapAntennaInfer(raw, intent)
  }

  // ══════ 响应映射（实际API→EditorResponse） ══════

  private mapGuanlanRoute(raw: GuanlanRouteRaw, action: string): EditorResponse {
    const out = new EditorResponse()
    out.dna = `#龍芯⚡️丙午·癸未·甲子·既济-${action}-v1.0-HM-9622`
    out.persona = raw['路由']?.['引擎'] ?? 'Ollama'
    out.route = raw['路由字符串'] ?? ''
    out.result = `[${raw['路由']?.['引擎'] ?? 'Ollama'}] 已接收任务: ${raw['任务'] ?? ''}`
    out.process_log = [
      `文心·理解意图 → ${raw['任务']}`,
      `诸葛亮·路由决策 → ${raw['路由']?.['引擎']}`,
      `${raw['路由']?.['引擎']}·执行推理`
    ]
    out.audit = {
      timestamp: new Date().toISOString(),
      checksum: '',
      level: 'L3'
    }
    return out
  }

  private mapGuanlanAudit(raw: GuanlanAuditRaw, content: string): EditorResponse {
    const passed = raw['结果']?.['过'] ?? false
    const out = new EditorResponse()
    out.dna = `#龍芯⚡️丙午·癸未·甲子·既济-审查-v1.0-HM-9622`
    out.persona = '雯雯+法律引擎'
    out.route = raw['结果']?.['状态'] ?? ''
    out.result = passed
      ? `审查通过 ✅ — ${content.substring(0, 50)}...`
      : `审查发现问题 ⚠️ — 违规: ${(raw['结果']?.['违规'] ?? []).join(', ')}`
    out.process_log = [
      `雯雯·接收审查请求`,
      `法律引擎·权限扫描 → ${raw['权限']?.length ?? 0}项权限`,
      `审计判定 → ${passed ? '🟢 通过' : '🔴 拒绝'}`
    ]
    out.audit = {
      timestamp: new Date().toISOString(),
      checksum: '',
      level: passed ? 'L3' : 'L2'
    }
    return out
  }

  private mapAntennaInfer(raw: AntennaInferRaw, intent: string): EditorResponse {
    const out = new EditorResponse()
    out.dna = `#龍芯⚡️丙午·癸未·甲子·既济-自动路由-v1.0-HM-9622`
    out.persona = `诸葛亮·${raw['bagua'] ?? '离'}卦`
    out.route = `${raw['bagua'] ?? '离'}·${raw['wuxing'] ?? ''} — ${raw['status']}`
    out.result = `自动路由完成:\n` +
      `- 意图: "${intent}"\n` +
      `- 卦象: ${raw['bagua'] ?? '离'} (${raw['wuxing'] ?? ''})\n` +
      `- 路径长度: ${raw['path_length'] ?? 0}节点\n` +
      `- 延迟: ${raw['latency_ms'] ?? 0}ms\n` +
      `- 节能: ${raw['skip_rate_pct'] ?? 0}%跳过`
    out.process_log = [
      `八门路由·接收意图 → "${intent.substring(0, 30)}"`,
      `八卦推演 → ${raw['bagua']}·${raw['wuxing']}`,
      `门控分配 → ${raw['nodes_active']} 激活`,
      `路由完成 → ${raw['status']}`
    ]
    out.audit = {
      timestamp: new Date().toISOString(),
      checksum: '',
      level: 'L3'
    }
    return out
  }

  // ══════ 通用HTTP方法 ══════

  /** POST请求·带重试 */
  private async post<T>(service: string, path: string, body: object): Promise<T> {
    const url = `${this.baseUrl(service)}${path}`
    return this.request<T>(http.RequestMethod.POST, url, body)
  }

  /** 统一请求·重试·超时 */
  private async request<T>(
    method: http.RequestMethod,
    url: string,
    body?: object
  ): Promise<T> {
    let lastError: Error | null = null

    for (let attempt = 0; attempt <= Constants.MAX_RETRIES; attempt++) {
      const req = http.createHttp()
      try {
        if (attempt > 0) {
          await this.sleep(Constants.RECONNECT_DELAY * attempt)
        }

        const response = await req.request(url, {
          method: method,
          header: this.buildHeaders(),
          extraData: body ? JSON.stringify(body) : undefined,
          connectTimeout: Constants.REQUEST_TIMEOUT,
          readTimeout: Constants.REQUEST_TIMEOUT
        })

        const result = JSON.parse(response.result as string) as T
        return result

      } catch (err) {
        lastError = err as Error
        console.error(`[ApiClient] 请求失败 (${attempt + 1}/${Constants.MAX_RETRIES + 1}): ${url}`)

        if (attempt >= Constants.MAX_RETRIES) break
      } finally {
        req.destroy()
      }
    }

    // 全部重试失败 → 返回模拟错误响应
    throw new Error(`网络不通: ${lastError?.message ?? '未知错误'}`)
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
}

// ══════ 编辑器响应类型 ══════

/** 编辑器API通用响应 */
export class EditorResponse {
  dna: string = ''
  persona: string = ''
  route: string = ''
  result: string = ''
  process_log: string[] = []
  audit: AuditInfo = new AuditInfo()
}

/** 审计信息 */
export class AuditInfo {
  timestamp: string = ''
  checksum: string = ''
  level: string = 'L3'
}

/** 编辑器输出条目（本地组装） */
export class EditorOutput {
  id: string = ''
  task: string = ''
  personas: string = ''
  result: string = ''
  processLog: string[] = []
  dna: string = ''
  auditLevel: string = 'L3'
  timestamp: number = Date.now()
  isError: boolean = false
  errorMessage: string = ''
}

// ══════ 原始API响应类型（匹配鲲鹏实际返回） ══════

/** 观澜 /route 原始响应 */
interface GuanlanRouteRaw {
  '任务': string
  '路由': {
    '引擎': string
    '标注': {
      '引擎': string
      '版本': string
      '时间': number
      '位置': string
      '信级': string
      '置信': number
    }
  }
  '路由字符串': string
}

/** 观澜 /plugin/audit 原始响应 */
interface GuanlanAuditRaw {
  '权限': string[]
  '结果': {
    '过': boolean
    '状态': string
    '违规': string[]
  }
}

/** 蚁触 /infer 原始响应 */
interface AntennaInferRaw {
  input_preview: string
  bagua: string
  wuxing: string
  output_dim: number
  latency_ms: number
  energy_j: number
  skip_rate_pct: number
  path_length: number
  nodes_active: string
  status: string
}

/** 全局默认ApiClient实例 */
export const apiClient = new ApiClient()

// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { ApiClient } from './ApiClient'
import { Constants } from '../utils/Constants'
import { ChatMessage } from '../models/Types'

/**
 * 小艺桥接API服务 (:8799)
 * AI对话·模型列表·健康·能力清单
 * 铁律：小艺为唯一AI调度入口，所有外部AI请求经此路由
 */
export class XiaoyiService {
  private client: ApiClient

  constructor(client: ApiClient) {
    this.client = client
  }

  /** 健康检查 */
  async health(): Promise<boolean> {
    const r = await this.client.get<{ status: string }>('xiaoyi', Constants.API.XIAOYI_HEALTH)
    return r.code === 0
  }

  /** 桥接引擎状态 */
  async getStatus(): Promise<any> {
    const r = await this.client.get<any>('xiaoyi', Constants.API.XIAOYI_STATUS)
    return r.data ?? {}
  }

  /** AI对话 — 核心入口 */
  async chat(message: string, history?: ChatMessage[]): Promise<ChatMessage> {
    const body: Record<string, Object> = { message }

    // 传历史上下文
    if (history && history.length > 0) {
      body['history'] = history.slice(-10).map(m => ({
        role: m.role,
        content: m.content
      }))
    }

    const r = await this.client.post<any>('xiaoyi', Constants.API.XIAOYI_CHAT, body)

    return {
      id: `xiaoyi_${Date.now()}`,
      role: 'assistant',
      content: r.data?.response ?? r.data?.result ?? r.message ?? '小艺没有回应',
      persona: r.data?.persona ?? '小艺',
      dna: r.data?.dna ?? '',
      timestamp: Date.now(),
      isError: r.code !== 0
    } as ChatMessage
  }

  /** 可用对话模型列表 */
  async listModels(): Promise<string[]> {
    const r = await this.client.get<{ models: string[] }>('xiaoyi', Constants.API.XIAOYI_MODELS)
    return r.data?.models ?? []
  }

  /** 能力清单 */
  async getCapabilities(): Promise<string[]> {
    const r = await this.client.get<{ capabilities: string[] }>('xiaoyi', Constants.API.XIAOYI_CAPABILITIES)
    return r.data?.capabilities ?? []
  }
}

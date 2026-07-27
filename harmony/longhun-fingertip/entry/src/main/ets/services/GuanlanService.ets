// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { ApiClient } from './ApiClient'
import { Constants } from '../utils/Constants'
import { ChatMessage, SystemStatus, EngineInfo, RouteRequest, RouteResponse, BaguaGate } from '../models/Types'

/**
 * 观澜浏览器API服务 (:8770)
 * 任务路由·断路器·引擎注册·隐私扫描·多模型对比
 */
export class GuanlanService {
  private client: ApiClient

  constructor(client: ApiClient) {
    this.client = client
  }

  /** 健康检查 */
  async health(): Promise<boolean> {
    const r = await this.client.get<{ status: string }>('guanlan', Constants.API.GUANLAN_HEALTH)
    return r.code === 0
  }

  /** 全系统状态 */
  async getSystemStatus(): Promise<SystemStatus> {
    const r = await this.client.get<any>('guanlan', Constants.API.GUANLAN_STATUS)
    if (r.data) {
      return {
        cpu_percent: r.data.cpu_percent ?? 0,
        memory_percent: r.data.memory_percent ?? 0,
        disk_percent: r.data.disk_percent ?? 0,
        uptime_seconds: r.data.uptime_seconds ?? 0,
        active_personas: r.data.active_personas ?? 0,
        engines_healthy: r.data.engines_healthy ?? 0,
        engines_total: r.data.engines_total ?? 0,
        circuit_breaker_tripped: r.data.circuit_breaker_tripped ?? false,
        last_update: Date.now()
      } as SystemStatus
    }
    return new SystemStatus()
  }

  /** 任务路由 */
  async route(task: string, preference?: string): Promise<RouteResponse> {
    const body: RouteRequest = { task, force_local: true, preference }
    const r = await this.client.post<any>('guanlan', Constants.API.GUANLAN_ROUTE, body)
    return {
      engine: r.data?.engine ?? 'unknown',
      result: r.data?.result ?? '',
      persona: r.data?.persona,
      confidence: r.data?.confidence ?? 0,
      audit: r.data?.audit ?? '🟢'
    }
  }

  /** 已注册引擎列表 */
  async listEngines(): Promise<EngineInfo[]> {
    const r = await this.client.get<{ engines: EngineInfo[] }>('guanlan', Constants.API.GUANLAN_ENGINES)
    return r.data?.engines ?? []
  }

  /** 断路器状态 */
  async circuitBreakerStatus(): Promise<any> {
    const r = await this.client.get<any>('guanlan', Constants.API.GUANLAN_CIRCUIT_BREAKER)
    return r.data ?? {}
  }
}

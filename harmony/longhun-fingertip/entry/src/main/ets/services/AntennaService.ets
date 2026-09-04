// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { ApiClient } from './ApiClient'
import { Constants } from '../utils/Constants'
import { InferRequest, InferResponse, BaguaGate } from '../models/Types'

/**
 * 蚁触·八门路由API服务 (:8769)
 * 蚁触推理·八卦门控·五行调度
 */
export class AntennaService {
  private client: ApiClient

  constructor(client: ApiClient) {
    this.client = client
  }

  /** 健康检查 */
  async health(): Promise<boolean> {
    const r = await this.client.get<{ status: string }>('antenna', Constants.API.ANTENNA_HEALTH)
    return r.code === 0
  }

  /** 单次蚁触推理 */
  async infer(text: string, baguaHint?: string): Promise<InferResponse> {
    const body: InferRequest = { text, bagua_hint: baguaHint }
    const r = await this.client.post<any>('antenna', Constants.API.ANTENNA_INFER, body)
    return {
      bagua: r.data?.bagua ?? '?',
      gate_name: r.data?.gate_name ?? '',
      element: r.data?.element ?? '',
      route: r.data?.route ?? '',
      confidence: r.data?.confidence ?? 0,
      reasoning: r.data?.reasoning ?? ''
    }
  }

  /** 五行平衡报告 */
  async getWuxing(): Promise<any> {
    const r = await this.client.get<any>('antenna', Constants.API.ANTENNA_WUXING)
    return r.data ?? {}
  }

  /** 蚁触网统计 */
  async getMesh(): Promise<any> {
    const r = await this.client.get<any>('antenna', Constants.API.ANTENNA_MESH)
    return r.data ?? {}
  }

  /** 八卦路由说明 */
  async getBagua(): Promise<BaguaGate[]> {
    const r = await this.client.get<{ gates: BaguaGate[] }>('antenna', Constants.API.ANTENNA_BAGUA)
    return r.data?.gates ?? []
  }
}

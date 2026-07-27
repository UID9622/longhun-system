// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.1
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import http from '@ohos.net.http'
import { Constants } from '../utils/Constants'
import { ServerConfig, ApiResponse } from '../models/Types'

/**
 * 龍魂API统一客户端 v1.1
 *
 * 变更（v1.0→v1.1）：
 * - 请求头增加 X-LongHun-Signature 字段
 * - 设备码统一使用 DEVICE_CODE 常量
 * - 支持WebSocket连接（预留）
 * - 数据主权护栏：仅传输计算结果，不传输原始数据
 */
export class ApiClient {
  private config: ServerConfig = new ServerConfig()
  private retryCount: number = 0

  constructor(config?: ServerConfig) {
    if (config) this.config = config
  }

  updateConfig(config: ServerConfig): void {
    this.config = config
  }

  getConfig(): ServerConfig {
    return this.config
  }

  /** 构建v1.1标准请求头 */
  private buildHeaders(): Record<string, string> {
    const now = new Date().toISOString()
    return {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-LongHun-DNA': `${Constants.DNA_PREFIX}丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.1`,
      'X-LongHun-UID': Constants.UID,
      'X-LongHun-Confirm': Constants.CONFIRM_CODE,
      'X-LongHun-Timestamp': now,
      'X-LongHun-Device': Constants.DEVICE_CODE,
      'X-LongHun-Signature': this.buildSignature(now)
    }
  }

  /** 构建GPG标记签名（端侧简化版） */
  private buildSignature(timestamp: string): string {
    return `HM-SHA256-${Constants.UID}-${timestamp.substring(0, 10)}-${Constants.DEVICE_CODE}`
  }

  /** GET请求 */
  async get<T>(service: string, path: string, params?: Record<string, string>): Promise<ApiResponse<T>> {
    let url = `${this.config.baseUrl(service)}${path}`
    if (params) {
      const query = Object.entries(params)
        .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
        .join('&')
      url += `?${query}`
    }
    return this.request<T>(http.RequestMethod.GET, url)
  }

  /** POST请求 */
  async post<T>(service: string, path: string, body?: object): Promise<ApiResponse<T>> {
    const url = `${this.config.baseUrl(service)}${path}`
    return this.request<T>(http.RequestMethod.POST, url, body)
  }

  /** 统一请求·带重试 */
  private async request<T>(
    method: http.RequestMethod,
    url: string,
    body?: object
  ): Promise<ApiResponse<T>> {
    const request = http.createHttp()
    let lastError: Error | null = null

    for (let attempt = 0; attempt <= Constants.MAX_RETRIES; attempt++) {
      try {
        if (attempt > 0) {
          await this.sleep(Constants.RECONNECT_DELAY * attempt)
        }

        const response = await request.request(url, {
          method: method,
          header: this.buildHeaders(),
          extraData: body ? JSON.stringify(body) : undefined,
          connectTimeout: Constants.REQUEST_TIMEOUT,
          readTimeout: Constants.REQUEST_TIMEOUT
        })

        this.retryCount = 0  // 成功则重置
        const result = JSON.parse(response.result as string) as ApiResponse<T>
        return result

      } catch (err) {
        lastError = err as Error
        console.error(`[ApiClient] 请求失败 (${attempt + 1}/${Constants.MAX_RETRIES + 1}): ${url}`, JSON.stringify(err))

        if (attempt >= Constants.MAX_RETRIES) {
          break
        }
      } finally {
        request.destroy()
      }
    }

    // 全部重试失败 → 返回错误响应
    return {
      code: -1,
      message: `网络不通: ${lastError?.message ?? '未知错误'}`,
      audit: { timestamp: new Date().toISOString(), checksum: '', level: 'L3', color: '🔴' }
    } as ApiResponse<T>
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
}

/*
 * ==========================================================================
 * 通心译 — HTTP客户端 ✅ 检查项#3 错误处理
 * DNA:#龍芯⚡️丙午·丙申·癸丑·午时·需-TONGXINYI-HTTP-v1.0
 * ==========================================================================
 * 统一HTTP客户端·内置: 超时处理 / 重试机制 / 统一错误码 / CNSH签名头
 * 鸿蒙底座: 基于 @ohos.net.http · 端侧安全
 * ==========================================================================
 */

import { http } from '@kit.NetworkKit';
import { BusinessError } from '@kit.BasicServicesKit';
import { HttpOptions, HttpResult } from '../common/types';

/**
 * 统一 HTTP 客户端
 * 内置: 超时处理 / 重试机制 / 统一错误码 / CNSH 签名头
 */
export class HttpClient {
  /**
   * 发送请求 (带重试)
   */
  static async request<T>(url: string, options: HttpOptions = {}): Promise<HttpResult<T>> {
    const {
      method = http.RequestMethod.GET,
      header = {},
      extraData,
      connectTimeout = 10000,
      readTimeout = 15000,
      maxRetries = 2,
      retryDelayMs = 1000
    } = options;

    const headers: Record<string, string> = {
      'Content-Type': 'application/json; charset=utf-8',
      'User-Agent': 'CNSH-TongxinYi-HarmonyOS/1.0',
      'X-CNSH-DNA': '#龍芯⚡️丙午·丙申·癸丑·午时·需-TONGXINYI-v1.0',
      ...header
    };

    let lastError: HttpResult<T> = { success: false, errorMessage: '未知错误' };

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      if (attempt > 0) {
        await HttpClient.sleep(retryDelayMs * attempt);
      }

      const httpRequest = http.createHttp();
      try {
        const response = await httpRequest.request(url, {
          method: method,
          header: headers,
          extraData: extraData as string,
          connectTimeout: connectTimeout,
          readTimeout: readTimeout,
          expectDataType: http.HttpDataType.STRING
        });

        const statusCode: number = response.responseCode;
        const body: string = (response.result as string) || '';

        if (statusCode >= 200 && statusCode < 300) {
          return {
            success: true,
            data: HttpClient.safeParseJSON(body) as T
          };
        }

        // HTTP 错误 (4xx/5xx)
        lastError = {
          success: false,
          errorCode: statusCode,
          errorMessage: `HTTP ${statusCode}: ${body.substring(0, 200)}`
        };

        // 4xx 不重试
        if (statusCode >= 400 && statusCode < 500) {
          break;
        }

      } catch (err) {
        const error = err as BusinessError;
        lastError = {
          success: false,
          errorCode: error.code,
          errorMessage: `网络错误: ${error.message} (code=${error.code})`
        };
        // 超时错误继续重试
      } finally {
        httpRequest.destroy();
      }
    }

    return lastError;
  }

  /**
   * GET 快捷方法
   */
  static async get<T>(url: string, header?: Record<string, string>): Promise<HttpResult<T>> {
    return HttpClient.request<T>(url, { method: http.RequestMethod.GET, header });
  }

  /**
   * POST 快捷方法
   */
  static async post<T>(url: string, data: Object, header?: Record<string, string>): Promise<HttpResult<T>> {
    return HttpClient.request<T>(url, {
      method: http.RequestMethod.POST,
      header,
      extraData: JSON.stringify(data)
    });
  }

  /**
   * 安全解析 JSON
   */
  private static safeParseJSON(text: string): Object {
    try {
      return JSON.parse(text);
    } catch {
      return { raw: text };
    }
  }

  /**
   * 延迟函数
   */
  private static sleep(ms: number): Promise<void> {
    return new Promise<void>((resolve) => {
      setTimeout(() => resolve(), ms);
    });
  }
}

/**
 * HttpInfo —— 系统 @ohos.net.http 的薄桥接（零三方·M77）
 * 统一: 超时 / 请求头 / 响应文本 / 错误归一为 HttpError 字符串
 */
import http from '@ohos.net.http';
import { LhConfig } from '../common/Config';

export class HttpResponseText {
  text: string = '';
  code: number = 0;
  error: string = '';
}

export class HttpInfo {
  /**
   * POST JSON 到端点，返回响应体文本
   * @param endpoint 完整 URL（默认 LhConfig.ENDPOINT）
   * @param bodyJson JSON 字符串（已序列化的 JSON-RPC 请求）
   */
  static async post(bodyJson: string, endpoint: string = LhConfig.ENDPOINT): Promise<HttpResponseText> {
    const out = new HttpResponseText();
    const httpRequest = http.createHttp();
    try {
      const resp = await httpRequest.request(endpoint, {
        method: http.RequestMethod.POST,
        header: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'X-LH-Attribution': LhConfig.ATTRIBUTION
        },
        extraData: bodyJson,
        expectDataType: http.HttpDataType.STRING,
        usingCache: false,
        connectTimeout: LhConfig.TIMEOUT_MS,
        readTimeout: LhConfig.TIMEOUT_MS
      });
      out.code = resp.responseCode;
      if (resp.responseCode === 200 || resp.responseCode === 204) {
        const data = resp.result as string;
        out.text = data;
      } else {
        out.error = `HTTP ${resp.responseCode}`;
      }
    } catch (e) {
      out.error = `请求失败: ${JSON.stringify(e)}`;
    } finally {
      httpRequest.destroy();
    }
    return out;
  }
}

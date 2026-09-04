/**
 * NativeQuery —— 最小依赖演示：不依赖任何模型类，
 * 直接用模板字符串拼 JSON-RPC 文本并 POST（教学/调试用·一行看懂协议）
 */
import { HttpInfo, HttpResponseText } from '../net/HttpInfo';
import { LhConfig } from '../common/Config';

export class NativeQuery {
  private seq: number = 0;

  /** 拼一个 JSON-RPC tools/call 请求文本 */
  private buildRpc(name: string, argsObj: object, id: number): string {
    const args = JSON.stringify(argsObj);
    return `{"jsonrpc":"2.0","id":${id},"method":"tools/call",` +
      `"params":{"name":"${name}","arguments":${args}}}`;
  }

  /** 直接 POST 返回原始文本（适合看协议原文） */
  async rawCall(name: string, argsObj: object = {}): Promise<HttpResponseText> {
    this.seq += 1;
    const body: string = this.buildRpc(name, argsObj, this.seq);
    return HttpInfo.post(body, LhConfig.ENDPOINT);
  }

  /** 便捷: search_catalog 裸调用，返回文本中提取的简单行 */
  async searchRaw(query: string): Promise<string> {
    const res = await this.rawCall('search_catalog', { 'query': query, 'limit': 10 });
    if (res.error.length > 0) {
      return res.error;
    }
    return res.text;
  }
}

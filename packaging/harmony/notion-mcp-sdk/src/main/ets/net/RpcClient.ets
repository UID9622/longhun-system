/**
 * RpcClient —— 通用 MCP JSON-RPC 客户端
 * 支持 tools/list 与 tools/call，文本走 HttpInfo 直连（无 SSE 依赖·兼容 8768）。
 */
import { HttpInfo, HttpResponseText } from './HttpInfo';
import {
  JsonRpcRequest, RpcResponse, RpcToolResult, parseRpcResponse
} from '../models/McpModels';

export class RpcClient {
  private seq: number = 100;

  /** 生成递增请求 id（线程安全无需：ArkTS UI 单线程调度） */
  private nextId(): number {
    this.seq += 1;
    return this.seq;
  }

  /** 底层：发一个 JSON-RPC 请求 */
  async send(method: string, params: object = {}): Promise<RpcResponse> {
    const req = new JsonRpcRequest(this.nextId(), method, params);
    const res: HttpResponseText = await HttpInfo.post(JSON.stringify(req));
    if (res.error.length > 0) {
      const r = new RpcResponse();
      r.ok = false;
      r.error.code = -32001;
      r.error.message = res.error;
      return r;
    }
    return parseRpcResponse(res.text);
  }

  /** tools/list：端点可用工具清单（文本逗号拼接） */
  async listTools(): Promise<string> {
    const r: RpcResponse = await this.send('tools/list');
    if (!r.ok) {
      return `错误 ${r.error.code}: ${r.error.message}`;
    }
    const names: string[] = [];
    for (const c of r.result.content) {
      const text = c.text;
      try {
        const raw: object = JSON.parse(text) as object;
        const tools = (raw as Record<string, Object>)['tools'] as Array<Object> | undefined;
        if (tools !== undefined) {
          for (const t of tools) {
            names.push(String((t as Record<string, Object>)['name'] ?? ''));
          }
        }
      } catch (e) {
        // 部分端点直接回文本
        return text;
      }
    }
    return names.length > 0 ? names.join(', ') : '(无工具)';
  }

  /** tools/call：调工具并把首条 text 内容返回 */
  async callTool(name: string, argumentsObj: object = {}): Promise<RpcToolResult> {
    const r: RpcResponse = await this.send('tools/call',
      { 'name': name, 'arguments': argumentsObj });
    return r.result;
  }
}

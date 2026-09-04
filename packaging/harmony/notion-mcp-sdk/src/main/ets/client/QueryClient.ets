/**
 * QueryClient —— 高层只读查询客户端（映射 8768 五个工具）
 * 用法: const q = new QueryClient(); const st = await q.getMirrorStatus();
 */
import { RpcClient } from '../net/RpcClient';
import { firstText } from '../models/McpModels';
import {
  MirrorStatus, SearchResult, CatalogList, AuditResult,
  textToStatus, textToSearch, textToList, textToAudit
} from '../models/CatalogModels';

export class QueryClient {
  private rpc: RpcClient = new RpcClient();

  /** get_mirror_status — 端点健康与快照概况 */
  async getMirrorStatus(): Promise<MirrorStatus> {
    const res = await this.rpc.callTool('get_mirror_status', {});
    return textToStatus(firstText(res));
  }

  /** search_catalog — 目录标题/URL 秒搜（纯本地零 Notion API） */
  async searchCatalog(query: string, limit: number = 20): Promise<SearchResult> {
    const res = await this.rpc.callTool('search_catalog',
      { 'query': query, 'limit': limit });
    return textToSearch(firstText(res));
  }

  /** list_catalog — 目录列表 kind: all | page | database */
  async listCatalog(kind: string = 'all', limit: number = 50): Promise<CatalogList> {
    const res = await this.rpc.callTool('list_catalog',
      { 'kind': kind, 'limit': limit });
    return textToList(firstText(res));
  }

  /** recent_audit — 主控层同步的审计链尾 */
  async recentAudit(limit: number = 20): Promise<AuditResult> {
    const res = await this.rpc.callTool('recent_audit', { 'limit': limit });
    return textToAudit(firstText(res));
  }

  /** topo_snapshot — 龍魂拓扑快照摘要（若主控已附推） */
  async topoSync(): Promise<string> {
    const res = await this.rpc.callTool('topo_snapshot', {});
    return firstText(res);
  }
}

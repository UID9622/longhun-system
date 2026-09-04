/**
 * 龍魂 Notion 数据镜像 · 连接配置
 * 默认指向鲲鹏 8768 只读端点。真机联调时按接入指南选择暴露方式后改此常量。
 */
export class LhConfig {
  /** 8768 MCP JSON-RPC 端点（/mcp 或 / 均可） */
  static readonly ENDPOINT: string = 'http://119.13.90.27:8768/mcp';

  /** 单次请求超时（毫秒） */
  static readonly TIMEOUT_MS: number = 8000;

  /** 归属声明（对外标识·实名） */
  static readonly ATTRIBUTION: string = '诸葛鑫 | UID9622 · 龍芯北辰';

  /** 目录快照 schema 版本（主控侧 catalog.json meta.schema） */
  static readonly SCHEMA_VERSION: string = 'catalog-v1';

  /** 仅请求目录元数据，绝不发送正文 —— 数据主权边界（正文主权留主控层） */
  static readonly READ_ONLY: boolean = true;
}

# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-ENGINE-CNSH_MCP_SERVER-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

#!/usr/bin/env python3
import asyncio, json, os, httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

CNSH_API = os.getenv("CNSH_API_URL", "http://localhost:9000")
app = Server("cnsh")

@app.list_tools()
async def list_tools():
    return [
        Tool(name="cnsh_write", description="写入CNSH块，三AI流程", inputSchema={"type":"object","properties":{"input":{"type":"string"},"source_ai":{"type":"string","enum":["GPT","Claude","Grok","Gemini"]}},"required":["input"]}),
        Tool(name="cnsh_query", description="查询CNSH块", inputSchema={"type":"object","properties":{"dna":{"type":"string"},"state":{"type":"string"},"tag":{"type":"string"},"limit":{"type":"number"}}}),
        Tool(name="cnsh_audit", description="审计块", inputSchema={"type":"object","properties":{"block_id":{"type":"string"},"depth":{"type":"string","enum":["basic","standard","deep"]}},"required":["block_id"]}),
        Tool(name="cnsh_health", description="系统健康", inputSchema={"type":"object","properties":{}}),
    ]

@app.call_tool()
async def call_tool(name, arguments):
    async with httpx.AsyncClient() as client:
        try:
            if name == "cnsh_write":
                r = await client.post(f"{CNSH_API}/cnsh/write_block", json={"input":arguments["input"],"source_ai":arguments.get("source_ai","GPT"),"user_id":"UID9622","blocks":[]}, timeout=30)
            elif name == "cnsh_query":
                params = {k:v for k,v in arguments.items() if v}
                r = await client.get(f"{CNSH_API}/cnsh/query", params=params, timeout=10)
            elif name == "cnsh_audit":
                r = await client.post(f"{CNSH_API}/cnsh/audit", json={"block_id":arguments["block_id"],"audit_depth":arguments.get("depth","standard")}, timeout=15)
            elif name == "cnsh_health":
                r = await client.get(f"{CNSH_API}/cnsh/health", timeout=5)
            else:
                return [TextContent(type="text", text=f"未知工具: {name}")]
            return [TextContent(type="text", text=json.dumps(r.json(), ensure_ascii=False, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"错误: {str(e)} | API: {CNSH_API}")]

async def main():
    async with stdio_server() as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂字体 MCP 服务 v1.0 · LonghunFont MCP Server
=================================================
将 LonghunFontEngine 包装为 MCP 协议服务，
供 Craft / Autov / CodeBuddy 等外部工具通过标准 JSON-RPC 接口调用。

DNA: #龍芯⚡️丙午·辛未·乙酉-FONT-MCP-SERVER-v1.0

协议: JSON-RPC 2.0 风格
请求: {"method": "list_fonts", "params": {...}}
响应: {"result": ..., "error": null}

支持方法:
  list_fonts      — 列出全部字体
  get_font        — 按名称查询 (name)
  get_font_path   — 获取字体文件绝对路径 (name)
  get_by_format   — 按格式筛选 (format: "otf"/"ttf"/"woff2")
  get_by_family   — 按家族筛选 (family)
  get_by_style    — 按样式筛选 (style)
  get_summary     — 获取引擎摘要
  export_registry — 导出注册表 JSON
  rescan          — 重新扫描字体目录
  verify          — 校验完整性
"""

import json
import sys
from typing import Any, Dict, Optional

from .engine import LonghunFontEngine

__DNA__ = "#龍芯⚡️丙午·辛未·乙酉-FONT-MCP-SERVER-v1.0"
__VERSION__ = "1.0.0"


class LonghunFontMCPServer:
    """
    龍魂字体 MCP 服务
    ────────────────
    接收 JSON-RPC 风格请求，调用引擎查询，返回结构化 JSON。
    """

    def __init__(self):
        self.engine = LonghunFontEngine()

        # 方法路由表
        self._methods = {
            "list_fonts": self._list_fonts,
            "get_font": self._get_font,
            "get_font_path": self._get_font_path,
            "get_by_format": self._get_by_format,
            "get_by_family": self._get_by_family,
            "get_by_style": self._get_by_style,
            "get_summary": self._get_summary,
            "export_registry": self._export_registry,
            "rescan": self._rescan,
            "verify": self._verify,
        }

        print(f"🐉 [MCP服务] 已启动 · 引擎就绪 · {len(self.engine.font_registry)} 字体在线")

    # ═══════════════════════════════════════
    # 核心: 请求分发
    # ═══════════════════════════════════════

    def handle_request(self, request: dict[str, Any]) -> dict[str, Any]:
        """
        处理 MCP 请求
        请求格式: {"method": "list_fonts", "params": {...}}
        响应格式: {"result": ..., "error": null}
        """
        method = request.get("method", "")
        params = request.get("params", {})

        if not method:
            return {"error": "缺少 method 字段"}

        handler = self._methods.get(method)
        if not handler:
            return {
                "error": f"未知方法: {method}",
                "available_methods": list(self._methods.keys()),
            }

        try:
            result = handler(params)
            return {"result": result, "error": None}
        except Exception as e:
            return {"error": str(e), "result": None}

    def handle_batch(self, requests: list[Any]) -> list[Any]:
        """批量处理多个请求"""
        return [self.handle_request(req) for req in requests]

    # ═══════════════════════════════════════
    # 方法实现
    # ═══════════════════════════════════════

    def _list_fonts(self, params: dict[str, Any]) -> list[Any]:
        return self.engine.get_all_fonts()

    def _get_font(self, params: dict[str, Any]) -> dict[str, Any]:
        name = params.get("name", "")
        if not name:
            return {"error": "缺少 name 参数"}
        font = self.engine.get_font_by_name(name)
        return font if font else {"error": f"字体 '{name}' 未找到"}

    def _get_font_path(self, params: dict[str, Any]) -> str:
        name = params.get("name", "")
        path = self.engine.get_font_file_path(name)
        return path or f"字体 '{name}' 未找到"

    def _get_by_format(self, params: dict[str, Any]) -> list[Any]:
        fmt = params.get("format", "otf")
        return self.engine.get_font_by_format(fmt)

    def _get_by_family(self, params: dict[str, Any]) -> list[Any]:
        family = params.get("family", "LongHun")
        return self.engine.get_font_by_family(family)

    def _get_by_style(self, params: dict[str, Any]) -> list[Any]:
        style = params.get("style", "Regular")
        return self.engine.get_font_by_style(style)

    def _get_summary(self, params: dict[str, Any]) -> dict[str, Any]:
        return self.engine.get_summary()

    def _export_registry(self, params: dict[str, Any]) -> dict[str, Any]:
        path = params.get("output_path")
        exported = self.engine.export_registry_json(path)
        return {
            "path": exported,
            "count": len(self.engine.font_registry),
        }

    def _rescan(self, params: dict[str, Any]) -> dict[str, Any]:
        old_count = len(self.engine.font_registry)
        self.engine.rescan()
        return {
            "before": old_count,
            "after": len(self.engine.font_registry),
            "summary": self.engine.get_summary(),
        }

    def _verify(self, params: dict[str, Any]) -> dict[str, Any]:
        all_fonts = self.engine.get_all_fonts()
        valid = self.engine.get_valid_fonts()
        damaged = [f for f in all_fonts if not f.get("is_valid", False)]
        return {
            "total": len(all_fonts),
            "valid": len(valid),
            "damaged": len(damaged),
            "damaged_list": [f["file_name"] for f in damaged],
            "valid_list": [f["file_name"] for f in valid],
        }

    # ═══════════════════════════════════════
    # 交互模式 (stdin/stdout)
    # ═══════════════════════════════════════

    def run_stdio(self):
        """从 stdin 读取 MCP 请求，输出 JSON 响应到 stdout (用于管道集成)"""
        print(f"🐉 [MCP stdio] 等待请求... (Ctrl+D 退出)")
        print()
        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                try:
                    request = json.loads(line.strip())
                    response = self.handle_request(request)
                    print(json.dumps(response, ensure_ascii=False))
                    sys.stdout.flush()
                except json.JSONDecodeError as e:
                    print(json.dumps({"error": f"JSON解析失败: {e}"}, ensure_ascii=False))
                    sys.stdout.flush()
        except KeyboardInterrupt:
            pass


# ═══════════════════════════════════════
# 独立运行
# ═══════════════════════════════════════

if __name__ == "__main__":
    server = LonghunFontMCPServer()

    # 演示: 模拟几个 MCP 请求
    test_requests = [
        {"method": "list_fonts", "params": {}},
        {"method": "get_summary", "params": {}},
        {"method": "get_font", "params": {"name": "LongHun-Regular"}},
        {"method": "get_by_format", "params": {"format": "otf"}},
        {"method": "verify", "params": {}},
    ]

    for req in test_requests:
        print(f"\n{'─' * 50}")
        print(f"请求: {req['method']}")
        resp = server.handle_request(req)
        # 截断输出
        result = resp.get("result", {})
        if isinstance(result, list):
            print(f"响应: {len(result)} 条记录")
            for item in result[:3]:
                print(f"  - {item.get('postscript_name', item.get('file_name', '?'))}")
            if len(result) > 3:
                print(f"  ... 共 {len(result)} 条")
        elif isinstance(result, dict):
            print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"响应: {result}")

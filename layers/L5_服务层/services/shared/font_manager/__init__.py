"""
龍魂字体管理引擎 · MCP服务包
===============================
L1_内核层/fonts → 唯一真理源
L5 服务层/font_manager → 查询/MCP服务层
DNA: #龍芯⚡️丙午·辛未·乙酉-FONT-MANAGER-PKG-v2.0
"""

from .engine import LonghunFontEngine
from .mcp_server import LonghunFontMCPServer

__all__ = ["LonghunFontEngine", "LonghunFontMCPServer"]
__DNA__ = "#龍芯⚡️丙午·辛未·乙酉-FONT-MANAGER-PKG-v2.0"
__VERSION__ = "2.0.0"

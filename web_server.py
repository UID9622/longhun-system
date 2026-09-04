#!/usr/bin/env python3
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 龍魂 Web 门户入口（根目录薄转发壳 · 单一真相源 08_BIN/web_server.py）
# DNA: #龍芯⚡️丙午·丙申·甲戌·辰时·䷓观-WEB-SERVER-ROOT-WRAPPER-v2.1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂 Web 门户入口（薄转发壳）
- 全部实现位于 08_BIN/web_server.py（单一真相源）
- 本文件仅为根目录兼容入口：`python3 web_server.py` 同样可用
"""
import importlib.util
import logging
import os
from pathlib import Path

import uvicorn

logger = logging.getLogger("longhun.web_server.wrapper")

# 单一真相源 08_BIN/web_server.py（08_BIN 数字开头非合法模块名，按路径加载）
_WS_PATH = Path(__file__).resolve().parent / "08_BIN" / "web_server.py"
_SPEC = importlib.util.spec_from_file_location("longhun_web_server_v2", _WS_PATH)
assert _SPEC is not None and _SPEC.loader is not None
_WS = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_WS)

app = _WS.app
API_URL = _WS.API_URL

if __name__ == "__main__":
    port = int(os.environ.get("LONGHUN_WEB_PORT", "8777"))
    host = os.environ.get("LONGHUN_WEB_HOST", "0.0.0.0")
    logger.info("🐉 龍魂 Web 门户 v2.0 启动（根目录转发壳 → 08_BIN/web_server.py）")
    logger.info("   地址: http://%s:%s · 后端: %s", host, port, API_URL)
    uvicorn.run(app, host=host, port=port, log_level="info")

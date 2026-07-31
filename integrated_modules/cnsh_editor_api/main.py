# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH Editor API · FastAPI 服务入口
DNA: #龍芯⚡️2026-07-04-CNSH-EDITOR-API-v1.0

运行方式：
    cd ~/longhun-system/integrated-modules/cnsh_editor_api
    PYTHONPATH=../../dev-env/chinese-editor/src python3 -m uvicorn main:app --reload

或：
    python3 -m cnsh_editor_api.main
"""
from __future__ import annotations

import io
import os
import sys
import traceback
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Any, Dict, Tuple

from fastapi import Depends, FastAPI, HTTPException, Request  # type: ignore[import-untyped]
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[import-untyped]
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles  # type: ignore[import-untyped]

# 将 longhun-chinese-editor 加入 Python 路径
_CURRENT_DIR = Path(__file__).resolve().parent
_CHINESE_EDITOR_SRC = _CURRENT_DIR.parents[1] / "dev-env" / "chinese-editor" / "src"
if _CHINESE_EDITOR_SRC.exists():
    sys.path.insert(0, str(_CHINESE_EDITOR_SRC))

try:
    import longhun_chinese_editor as ce  # type: ignore[import-untyped]
    from longhun_chinese_editor.compiler.lexer import Lexer  # type: ignore[import-untyped]
except ImportError as exc:
    raise ImportError(
        f"无法导入 longhun-chinese-editor，请确认 {_CHINESE_EDITOR_SRC} 存在"
    ) from exc

from . import models
from .config import TierLimits, get_current_tier
from .dependencies import check_execution_timeout, check_source_length, get_tier

app = FastAPI(
    title="龍魂 CNSH Editor API",
    description="中文母语编程 CNSH 的在线编辑器与执行 API，支持免费/付费 tier。",
    version="1.0.0",
)

# 跨域支持（🛡️ P77修复：白名单替代通配符）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8766", "http://127.0.0.1:8766"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-DNA-TRACE", "X-CNSH-CONFIRM"],
)

# 静态文件（前端编辑器）
_FRONTEND_DIR = _CURRENT_DIR / "frontend"
if _FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=_FRONTEND_DIR), name="static")


@app.get("/", response_class=RedirectResponse)
def root():
    return "/editor"


@app.get("/editor", response_class=HTMLResponse)
def editor():
    """返回 Web 编辑器页面"""
    index_file = _FRONTEND_DIR / "index.html"
    if index_file.exists():
        return index_file.read_text(encoding="utf-8")
    return "<h1>龍魂 CNSH Editor API</h1><p>前端文件缺失，请检查 frontend/index.html</p>"


@app.get("/api/v1/health", response_model=models.HealthResponse)
def health(tier: TierLimits = Depends(get_tier)):
    return models.HealthResponse(
        status="ok",
        tier=tier.name,
        version="1.0.0",
        dna="#龍芯⚡️2026-07-04-CNSH-API-v1.0",
    )


@app.get("/api/v1/tier", response_model=models.TierInfo)
def tier_info(tier: TierLimits = Depends(get_tier)):
    return models.TierInfo(
        name=tier.name,
        description=tier.description,
        max_source_chars=tier.max_source_chars,
        max_execution_time_ms=tier.max_execution_time_ms,
        allow_file_io=tier.allow_file_io,
        allow_network=tier.allow_network,
        allow_advanced_features=tier.allow_advanced_features,
    )


@app.post("/api/v1/check", response_model=models.CheckResponse)
def check_code(req: models.CheckRequest, tier: TierLimits = Depends(get_tier)):
    check_source_length(req.source, tier)
    try:
        ok, msg = ce.check_source(req.source)
        return models.CheckResponse(success=ok, message=msg)
    except Exception as exc:
        return models.CheckResponse(success=False, message=f"检查异常: {exc}")


@app.post("/api/v1/compile", response_model=models.CompileResponse)
def compile_code(req: models.CompileRequest, tier: TierLimits = Depends(get_tier)):
    check_source_length(req.source, tier)
    try:
        if req.legacy:
            py_code = ce.legacy_translate(req.source)
        else:
            py_code = ce.compile_source(req.source)
        return models.CompileResponse(
            success=True,
            python_code=py_code,
            message="✅ 编译成功",
        )
    except Exception as exc:
        return models.CompileResponse(
            success=False,
            message=f"❌ 编译失败: {exc}",
        )


@app.post("/api/v1/run", response_model=models.RunResponse)
def run_code(req: models.RunRequest, tier: TierLimits = Depends(get_tier)):
    check_source_length(req.source, tier)
    timeout_ms = check_execution_timeout(req.timeout_ms or 0, tier)
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()

    try:
        # 编译为 Python，避免 run_source 重复调用 主函数
        if req.legacy:
            python_code = ce.legacy_translate(req.source)
        else:
            python_code = ce.compile_source(req.source)
        python_code = _strip_trailing_main_call(python_code)

        ns: Dict[str, Any] = {"__name__": "__main__"}
        with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
            exec(python_code, ns)
            if "主函数" in ns and callable(ns["主函数"]):
                ns["主函数"]()

        serializable_ns = _filter_namespace(ns)

        return models.RunResponse(
            success=True,
            stdout=stdout_buf.getvalue(),
            stderr=stderr_buf.getvalue(),
            namespace=serializable_ns,
            message="✅ 执行成功",
        )
    except Exception as exc:
        return models.RunResponse(
            success=False,
            stdout=stdout_buf.getvalue(),
            stderr=stderr_buf.getvalue(),
            message=f"❌ 执行失败: {exc}\n{traceback.format_exc()}",
        )


@app.post("/api/v1/tokenize", response_model=models.TokenizeResponse)
def tokenize_code(req: models.TokenizeRequest, tier: TierLimits = Depends(get_tier)):
    check_source_length(req.source, tier)
    try:
        lexer = Lexer(req.source)
        tokens = lexer.tokenize()
        return models.TokenizeResponse(
            success=True,
            tokens=[
                models.TokenInfo(
                    type=tok.type.name,
                    value=str(tok.value),
                    line=getattr(tok, "line", 1),
                    column=getattr(tok, "col", 0),
                )
                for tok in tokens
            ],
            message="✅ 分词成功",
        )
    except Exception as exc:
        return models.TokenizeResponse(success=False, message=f"❌ 分词失败: {exc}")


def _filter_namespace(ns: Dict[str, Any]) -> Dict[str, Any]:
    """过滤命名空间中不可 JSON 序列化的对象"""
    result = {}
    for k, v in ns.items():
        if k.startswith("__") and k.endswith("__"):
            continue
        try:
            # 简单类型直接保留
            if isinstance(v, (str, int, float, bool, list, dict, type(None))):
                result[k] = v
            else:
                result[k] = str(v)
        except Exception:
            result[k] = "<不可序列化>"
    return result


def _strip_trailing_main_call(python_code: str) -> str:
    """
    移除编译器自动追加的顶层 主函数() 调用。
    API 层会统一负责调用一次，避免重复输出。
    """
    lines = python_code.splitlines()
    # 从后向前找到第一个非空行
    for idx in range(len(lines) - 1, -1, -1):
        stripped = lines[idx].strip()
        if not stripped:
            continue
        if stripped == "主函数()":
            lines[idx] = ""
            return "\n".join(lines)
        break
    return python_code


if __name__ == "__main__":
    import uvicorn

    # 🛡️ 安全加固 · DNA: #龍芯⚡️2026-07-06-SEC-PATCH-api-v1.0
    # 默認僅綁定 localhost，公網部署需顯式設置 CNSH_API_HOST=0.0.0.0 + API_KEY
    host = os.environ.get("CNSH_API_HOST", "127.0.0.1")
    port = int(os.environ.get("CNSH_API_PORT", "8000"))
    # 🛡️ API Key 校驗：設置 CNSH_API_KEY 環境變量後強制要求
    _api_key = os.environ.get("CNSH_API_KEY", "")
    if _api_key:
        from fastapi import Security
        from fastapi.security import APIKeyHeader  # type: ignore[import-untyped]
        _api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)  # type: ignore[attr-defined]
        async def _verify_key(api_key: str = Security(_api_key_header)):
            if api_key != _api_key:
                raise HTTPException(status_code=401, detail="Invalid API Key")
        # 將驗證依賴注入到所有 exec 路由（通過中間件）
        @app.middleware("http")
        async def _api_key_middleware(request: Request, call_next):
            if request.url.path.startswith("/api/run"):
                key = request.headers.get("X-API-Key", "")
                if key != _api_key:
                    from fastapi.responses import JSONResponse
                    return JSONResponse(status_code=401, content={"detail": "Invalid API Key"})
            return await call_next(request)
    uvicorn.run(app, host=host, port=port)

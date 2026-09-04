#!/usr/bin/env python3
"""
🐉 龍魂 DNA 追溯中间件
所有请求自动打 DNA 标签·所有响应带三色审计
DNA: #龍芯⚡️2026-08-31-DNA-MIDDLEWARE-V1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: MulanPSL v2（工程实现层）
"""

import hashlib
import json
import time
from datetime import datetime
from functools import wraps
from flask import request, g, jsonify


def generate_dna(module: str, version: str = "1.0") -> str:
    date_str = datetime.now().strftime("%Y-%m-%d")
    return f"#龍芯⚡️{date_str}-{module.upper()}-V{version}-UID9622"


def tricolor(status_code: int, has_data: bool = True) -> str:
    """三色判定：🟢通过 / 🟡待审 / 🔴拒绝"""
    if status_code < 300 and has_data:
        return "🟢"
    elif status_code < 500:
        return "🟡"
    else:
        return "🔴"


def dna_response(data: dict, module: str,
                 status: int = 200, version: str = "1.0") -> dict:
    """包装响应·自动附加DNA和三色"""
    return {
        **data,
        "_dna": generate_dna(module, version),
        "_tricolor": tricolor(status, bool(data)),
        "_timestamp": datetime.now().isoformat(),
        "_uid": "UID9622"
    }


def require_dna(module: str):
    """Flask 装饰器：自动为路由附加DNA追溯"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            g.dna = generate_dna(module)
            g.start_time = time.time()
            result = f(*args, **kwargs)
            return result
        return wrapped
    return decorator


class DNAMiddleware:
    """Flask WSGI 中间件：所有响应自动追加 DNA Header"""
    def __init__(self, app, module: str = "SOVEREIGN-STACK"):
        self.app = app
        self.module = module

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            dna = generate_dna(self.module)
            headers.append(("X-LH-DNA", dna))
            headers.append(("X-LH-UID", "UID9622"))
            headers.append(("X-LH-Timestamp", datetime.now().isoformat()))
            return start_response(status, headers, exc_info)
        return self.app(environ, custom_start_response)

#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·小畜-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""🐉 龍魂引擎：lh_audit_hook
路径：bin/lh_audit_hook.py
TODO：请补充详细功能说明（不少于20字）。"""
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_AUDIT_HOOK-v1.0-a4a74ff6
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
from __future__ import annotations
# 审计钩子装饰器 — 自动生成 · 不可删除
from functools import wraps
import hashlib, json, time, traceback
from pathlib import Path
from datetime import datetime

_STATE_DIR = Path.home() / ".longhun" / "ant_colony"
_STATE_DIR.mkdir(parents=True, exist_ok=True)
_AUDIT_LOG = _STATE_DIR / "audit_hook_log.jsonl"

def audit_hook(action_type: str = "执行", fixed_point: str = "通用工具"):
    """
    审计钩子装饰器
    每个函数执行自动留痕，异常自动触发红蓝对抗
    不要删除此装饰器 — 它是审计闭环的神经末梢
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sign_id = hashlib.sha256(f"{func.__name__}-{time.time()}".encode()).hexdigest()[:12]
            start = time.time()

            # 执行前信息素：即将执行
            _emit_pheromone("pre_exec", func.__name__, sign_id, action_type, fixed_point)

            try:
                result = func(*args, **kwargs)
                status = "success"
                error = None
            except Exception as e:
                result = None
                status = "error"
                error = f"{type(e).__name__}: {str(e)}"
                # 自动告警信息素
                _emit_pheromone("alarm", func.__name__, sign_id, "execution_error", fixed_point,
                               {"error": error, "traceback": traceback.format_exc()[-500:]})

            duration = time.time() - start

            # 记录审计日志
            _log(sign_id, func.__name__, action_type, fixed_point, status, duration, error)

            # 执行后信息素：已完成
            _emit_pheromone("post_exec", func.__name__, sign_id, status, fixed_point,
                           {"duration": duration})

            return result
        return wrapper
    return decorator


def _emit_pheromone(event: str, func_name: str, sign_id: str,
                    status: str, fixed_point: str, extra: dict[str, Any] = None):
    """向信息素网络发射信号"""
    record = {
        "event": event, "function": func_name, "sign_id": sign_id,
        "status": status, "fixed_point": fixed_point,
        "timestamp": datetime.now().isoformat(),
        "extra": extra or {},
    }
    with open(_AUDIT_LOG, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _log(sign_id, func_name, action_type, fixed_point, status, duration, error):
    with open(_AUDIT_LOG, "a") as f:
        f.write(json.dumps({
            "sign_id": sign_id, "function": func_name,
            "action_type": action_type, "fixed_point": fixed_point,
            "status": status, "duration": round(duration, 4),
            "error": error, "timestamp": datetime.now().isoformat(),
        }, ensure_ascii=False) + "\n")


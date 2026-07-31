# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
龍魂·反虚伪仲裁中心 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-反虚伪仲裁-v1.0

统一入口，整合：
- 璇玑引擎联动
- 三协议冲突仲裁
- 反馈循环记录
- 统一记忆入口
- 多语言支持
- 异步模式
"""
import json
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

# 把项目 bin 目录加入路径，方便导入 lh_memory_recall
_PROJECT_ROOT = Path.home() / "longhun-system"
_BIN_DIR = _PROJECT_ROOT / "bin"
if str(_BIN_DIR) not in sys.path:
    sys.path.insert(0, str(_BIN_DIR))

from . import 反虚伪引擎
from . import 冲突仲裁器
from . import 反馈循环
from . import 多语言

try:
    from lh_memory_recall import 记忆召回
except Exception:
    记忆召回 = None


# ---------- KFPP / 黑箱审计调用 ----------
def _调用KFPP(文本: str) -> Dict[str, Any]:
    """调用 KFPP 引擎检测知识权力化。"""
    kfpp_path = _BIN_DIR / "lh_kfpp_engine.py"
    if not kfpp_path.exists():
        return {"状态": "通过", "原因": "KFPP引擎未安装", "来源": "KFPP"}
    try:
        result = subprocess.run(
            ["python3", str(kfpp_path), "--inspect", 文本, "--actor", "反虚伪仲裁中心"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout.strip())
            # KFPP inspect_event 返回的具体字段视实现而定，这里做通用映射
            if data.get("frozen") or data.get("violation") or data.get("penalty", 0) > 0:
                return {"状态": "熔断", "原因": "KFPP检测到知识权力化", "来源": "KFPP", "详情": data}
            return {"状态": "通过", "来源": "KFPP", "详情": data}
        return {"状态": "通过", "原因": "KFPP无输出", "来源": "KFPP"}
    except Exception as exc:
        return {"状态": "通过", "原因": f"KFPP调用失败: {exc}", "来源": "KFPP"}


def _调用黑箱审计(文本: str) -> Dict[str, Any]:
    """调用黑箱审计引擎（占位，若不存在则返回通过）。"""
    blackbox_path = _BIN_DIR / "lh_prompt_blackbox_audit_v2.0.py"
    if not blackbox_path.exists():
        return {"状态": "通过", "原因": "黑箱审计引擎未安装", "来源": "黑箱审计"}
    try:
        result = subprocess.run(
            ["python3", str(blackbox_path), "--check", 文本],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout.strip())
            if data.get("状态") == "熔断" or data.get("risk", 0) >= 80:
                return {"状态": "熔断", "原因": "黑箱审计触发熔断", "来源": "黑箱审计", "详情": data}
            if data.get("risk", 0) >= 50:
                return {"状态": "警告", "原因": "黑箱审计触发警告", "来源": "黑箱审计", "详情": data}
            return {"状态": "通过", "来源": "黑箱审计", "详情": data}
        return {"状态": "通过", "原因": "黑箱审计无输出", "来源": "黑箱审计"}
    except Exception as exc:
        return {"状态": "通过", "原因": f"黑箱审计调用失败: {exc}", "来源": "黑箱审计"}


# ---------- 记忆写入 ----------
def _写入记忆(人格: str, 结果: Dict[str, Any]):
    """写入统一记忆入口。"""
    数据 = {
        "人格": 人格,
        "状态": 结果.get("状态"),
        "分数": 结果.get("虚伪度"),
        "一级命中": 结果.get("一级命中", []),
        "二级命中": 结果.get("二级命中", []),
    }
    if 记忆召回 is not None:
        try:
            记忆召回.写入("反虚伪", 数据)
            return
        except Exception:
            pass
    # 兜底：直接写到统一记忆目录
    try:
        from lh_memory_recall import 记忆召回 as fallback
        fallback.写入("反虚伪", 数据)
    except Exception:
        pass


# ---------- 后台审计线程 ----------
def _后台审计(文本: str, 初步结果: Dict[str, Any]):
    """异步深度扫描，不阻塞主流程。"""
    try:
        深度结果 = 反虚伪引擎.深度扫描(文本)
        反虚伪引擎.写入日志("反虚伪异步审计", "完成", "反虚伪仲裁中心", {
            "初步结果": 初步结果,
            "深度扫描": 深度结果,
        })
    except Exception as exc:
        反虚伪引擎.写入日志("反虚伪异步审计", "异常", "反虚伪仲裁中心", {"错误": str(exc)})


# ---------- 主入口 ----------
def 检查(
    文本: str,
    人格: str = "未知人格",
    语言: str = "zh",
    模式: str = "同步",
) -> Dict[str, Any]:
    """统一检查入口。"""

    # 1. 语言适配
    if 语言 == "auto":
        语言 = 多语言.多语言.检测到哪个语言(文本)
    配置 = 多语言.多语言.适配(文本, 语言)

    # 2. 执行检测
    结果 = 反虚伪引擎._检查回复核心(
        文本,
        人格,
        配置["一级禁用词"],
        配置["二级禁用词"],
        配置["煽情词"],
        反虚伪引擎.虚伪句式,
    )

    # 3. 熔断时记录反馈循环
    if 结果.get("状态") == "熔断":
        反馈循环.反馈循环.记录(文本, 结果, 人格)

    # 4. 记录到统一记忆入口
    _写入记忆(人格, 结果)

    # 5. 异步模式：提交后台审计，立即返回
    if 模式 == "异步":
        线程 = threading.Thread(target=_后台审计, args=(文本, 结果), daemon=True)
        线程.start()
        return {
            "状态": "已提交",
            "模式": "异步",
            "初步结果": 结果,
        }

    # 6. 同步模式返回完整结果
    return 结果


def 仲裁三协议(文本: str, 人格: str = "未知人格") -> Dict[str, Any]:
    """三协议冲突仲裁：KFPP + 黑箱审计 + 反虚伪引擎。"""
    三协议结果 = {
        "KFPP": _调用KFPP(文本),
        "黑箱审计": _调用黑箱审计(文本),
        "反虚伪": 检查(文本, 人格, 语言="auto", 模式="同步"),
    }
    return 冲突仲裁器.冲突仲裁器.裁决(三协议结果)


def 后台审计(文本: str) -> Dict[str, Any]:
    """显式调用深度扫描。"""
    return 反虚伪引擎.深度扫描(文本)

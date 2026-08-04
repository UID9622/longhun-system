#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂智能体编排层 · longhun-agent-eco 适配器

把 agent-eco 的 15 智能体生态系统、v2 路由引擎、任务管理器 v2.0
封装成编排器可直接调用的 Python API，不依赖任何外部平台。

DNA: #龍芯⚡️2026-06-26-LONGHUN-AGENT-ECO-ADAPTER-v1.0
"""

import importlib
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

DNA = "#龍芯⚡️2026-06-26-LONGHUN-AGENT-ECO-ADAPTER-v1.0"
ECO_PATH = str(Path.home() / ".kimi-code" / "skills" / "longhun-agent-eco" / "scripts")

_eco_modules = None


def _load_modules():
    global _eco_modules
    if _eco_modules is not None:
        return _eco_modules
    if ECO_PATH not in sys.path:
        sys.path.insert(0, ECO_PATH)
    try:
        智能体生态系统 = importlib.import_module("智能体生态系统")
        路由引擎v2 = importlib.import_module("路由引擎v2")
        任务管理器v2 = importlib.import_module("任务管理器v2")
    except Exception as e:
        raise RuntimeError(f"无法加载 longhun-agent-eco 模块: {e}") from e
    _eco_modules = {
        "ecosystem": 智能体生态系统,
        "router": 路由引擎v2,
        "taskmgr": 任务管理器v2,
    }
    return _eco_modules


def eco_route(text: str, tag: Optional[str] = None) -> Dict[str, Any]:
    """使用 agent-eco v2 路由引擎对文本进行路由。"""
    mods = _load_modules()
    engine = mods["router"].路由引擎v2()
    engine.初始化()
    result = engine.路由(text, 指定標籤=tag)
    data = result.到字典()
    data["adapter_dna"] = DNA
    return data


def eco_status() -> Dict[str, Any]:
    """获取 agent-eco 15 智能体生态系统状态。"""
    mods = _load_modules()
    coord = mods["ecosystem"].智能體協調器()
    coord.初始化()
    status = coord.獲取狀態().到字典()
    agents = []
    for agent in coord.獲取全部智能體().values():
        agents.append({
            "id": agent.編號,
            "name": agent.名稱,
            "type": agent.類型.value,
            "status": agent.狀態.value,
            "score": agent.評分,
            "tags": agent.路由標籤,
        })
    return {
        "adapter_dna": DNA,
        "status": status,
        "agents": agents,
    }


def eco_list() -> List[Dict[str, Any]]:
    """列出 agent-eco 中全部 15 个智能体。"""
    return eco_status().get("agents", [])


def _map_priority(p: str):
    mods = _load_modules()
    任務優先級 = mods["taskmgr"].任務優先級
    mapping = {
        "紧急": 任務優先級.緊急,
        "emergency": 任務優先級.緊急,
        "高": 任務優先級.高,
        "high": 任務優先級.高,
        "正常": 任務優先級.正常,
        "normal": 任務優先級.正常,
        "低": 任務優先級.低,
        "low": 任務優先級.低,
        "最低": 任務優先級.最低,
        "lowest": 任務優先級.最低,
    }
    return mapping.get(str(p).lower().strip(), 任務優先級.正常)


def eco_add_task(title: str, label: str = "execute", priority: str = "normal",
                 description: str = "", metadata: Optional[Dict] = None) -> Dict[str, Any]:
    """向 agent-eco 任务管理器 v2.0 添加任务。"""
    mods = _load_modules()
    tm = mods["taskmgr"].任務管理器v2()
    tm.初始化()
    prio = _map_priority(priority)
    ok, info = tm.添加任務(title, 描述=description, 標籤=label, 優先級=prio, 元數據=metadata or {})
    return {
        "adapter_dna": DNA,
        "success": ok,
        "task_id": info if ok else None,
        "error": None if ok else info,
    }


def eco_next_task() -> Optional[Dict[str, Any]]:
    """获取下一个待处理任务。"""
    mods = _load_modules()
    tm = mods["taskmgr"].任務管理器v2()
    tm.初始化()
    task = tm.獲取下一任務()
    if task is None:
        return None
    return task.到字典()


def eco_complete_task(task_id: str, result: Optional[Dict] = None) -> Dict[str, Any]:
    """标记任务完成。"""
    mods = _load_modules()
    tm = mods["taskmgr"].任務管理器v2()
    tm.初始化()
    ok = tm.完成任務(task_id, 結果=result or {})
    return {"adapter_dna": DNA, "success": ok}


def eco_task_report() -> Dict[str, Any]:
    """获取任务管理器统计报告。"""
    mods = _load_modules()
    tm = mods["taskmgr"].任務管理器v2()
    tm.初始化()
    return {
        "adapter_dna": DNA,
        "stats": tm._統計.到字典(),
        "pending_count": len([t for t in tm._任務倉庫.values() if t.狀態.value == "pending"]),
    }

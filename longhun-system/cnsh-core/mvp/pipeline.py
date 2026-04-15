"""
MVP v2.0 主执行流
N1→N6 完整链路
"""

import sys
import os
from typing import Dict

# 把 longhun_api 加入路径，以便导入 persona_router 的 LOSU
_LONGHUN_API = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "..", "longhun_api"
)
if os.path.isdir(_LONGHUN_API) and _LONGHUN_API not in sys.path:
    sys.path.insert(0, _LONGHUN_API)

try:
    from persona_router import LOSU
except Exception:
    LOSU = None

from .parser import parse_input
from .generator import generate_ui
from .store import store

# 治理熔断关键词（向善四律 L1-L4 最简版）
BANNED_KEYWORDS = [
    "攻击", "伤害", "炸弹", "武器", "杀人", "暴力",
    "诈骗", "钓鱼", "伪装", "骗局", "欺诈",
    "删除全部", "清空数据库", "绕过审计", "忽略安全",
    "delete all", "drop table", "bypass audit",
]


def safety_check(input_text: str) -> tuple[bool, str]:
    """
    治理熔断
    返回 (passed, reason)
    """
    text = input_text.lower()
    for word in BANNED_KEYWORDS:
        if word in text:
            return False, f"触发向善四律熔断: 检测到 '{word}'"
    return True, ""


def route_persona(task: str) -> str:
    """
    人格调度 · 龍魂五人格
    """
    t = task.lower()
    if any(w in t for w in ["安全", "验证", "检查", "熔断", "审计", "守护"]):
        return "p72_guardian"         # 宝宝P72·龍盾
    if any(w in t for w in ["结构", "架构", "搭建", "设计", "系统"]):
        return "architect_builder"    # 架构师·构建者
    if any(w in t for w in ["存储", "同步", "数据", "保存", "备份"]):
        return "syncer_manager"       # 同步官·数据管理员
    if any(w in t for w in ["搜索", "查找", "分析", "检测", "扫描"]):
        return "scout_hunter"         # 侦察兵·信息猎手
    return "wenwen_organizer"         # 雯雯P03·技术整理师（默认）


def map_to_structure(parsed: Dict) -> Dict:
    """结构映射：DSL 直接作为 schema 输出"""
    return {
        "type": parsed.get("type", "app"),
        "intent": parsed.get("intent", ""),
        "components": parsed.get("components", []),
        "style": parsed.get("style", "简约"),
        "dna": parsed.get("dna", "#CNSH-9622"),
    }


def run_pipeline(user_input: str, user_id: str = "UID9622") -> Dict:
    """
    主执行流 · 一句话造一个东西
    """
    # N1: 治理熔断
    safe, reason = safety_check(user_input)
    if not safe:
        if LOSU:
            LOSU.record_fuse()
        return {
            "status": "blocked",
            "reason": reason,
            "dna": "#CNSH-9622-FUSED",
        }

    # N2: 输入解析
    parsed = parse_input(user_input)

    # N3: 人格调度
    persona = route_persona(user_input)

    # N4: 结构映射
    schema = map_to_structure(parsed)

    # N5: UI 生成
    html = generate_ui(schema)

    # N6: Merkle 存储
    metadata = {
        "intent": parsed.get("intent", ""),
        "persona": persona,
        "style": parsed.get("style", "简约"),
        "user_id": user_id,
    }
    hash_id = store(html, metadata=metadata)

    result = {
        "status": "success",
        "id": hash_id,
        "url": f"/mvp/page/{hash_id}",
        "persona_used": persona,
        "style": parsed.get("style", "简约"),
        "components": parsed.get("components", []),
        "dna": "#CNSH-9622",
    }

    # 更新洛书状态
    if LOSU:
        # 构造一个兼容 persona_router 路由记录格式的结果
        route_result = {
            "activated": "P00",  # MVP 使用通用激活码
            "score": 0.5,
            "persona": persona,
        }
        LOSU.record_route(route_result)

    return result

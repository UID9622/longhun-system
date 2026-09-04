"""
龍魂五行计算器 v4.0 · 流场节点生成与12字段校验
DNA: #龍芯⚡️2026-08-31-五行计算器-v4.0-WELD-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
文化主权：五行不翻译·天干地支不翻译·这是尊严 🐉
"""

from __future__ import annotations
import hashlib
import unicodedata
from datetime import datetime
from .constants import 数字根五行表, 五行相生, 五行相克, 五行视觉, 熔断数字根

_VALID_RAW_TYPES = {"text", "image", "html", "code", "page", "dialogue", "rule", "idea"}
_VALID_ELEMENTS  = {"金", "木", "水", "火", "土"}
_VALID_RELATIONS = {"起点", "比和", "相生", "相克", "相泄", "相耗", "混合"}
_VALID_AUDITS    = {"🟢", "🟡", "🔴"}
_VALID_ACTIONS   = {"enter", "hold", "fuse", "archive", "route"}
_HUMAN_MIN       = 0.34


def 计算数字根(text: str) -> int:
    """提取数字（兼容Unicode），反复相加到个位。无数字 -> 0"""
    digits = [
        unicodedata.digit(c)
        for c in str(text)
        if unicodedata.category(c) == "Nd"
    ]
    if not digits:
        return 0
    n = sum(digits)
    while n >= 10:
        n = sum(int(c) for c in str(n))
    return n


def 三色审计(dr: int) -> str:
    """dr=3/9->🔴  dr=6->🟡  其余->🟢"""
    if dr in 熔断数字根:
        return "🔴"
    if dr == 6:
        return "🟡"
    return "🟢"


def 判断关系(a: str, b: str | None) -> str:
    if not b: return "起点"
    if a == b: return "比和"
    if 五行相生.get(b) == a: return "相生"
    if 五行相克.get(b) == a: return "相克"
    if 五行相生.get(a) == b: return "相泄"
    if 五行相克.get(a) == b: return "相耗"
    return "混合"


def _生成DNA(title: str) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    safe = title[:18].replace(" ", "")
    return f"#龍芯⚡️{today}-{safe}-v4.0"


def 生成节点(
    text: str,
    title: str = "未命名节点",
    prev_element: str | None = None,
    raw_type: str = "text",
) -> dict:
    """
    生成龍魂流场节点（Node JSON）
    输入：任意文本 + 可选标题/前节点五行/类型
    输出：12字段完整 Node JSON
    """
    dr = 计算数字根(text)
    element = 数字根五行表[dr]
    audit = 三色审计(dr)
    relation = 判断关系(element, prev_element)
    hash8 = hashlib.sha256(str(text).encode("utf-8")).hexdigest()[:8].upper()
    action_map = {"🟢": "enter", "🟡": "hold", "🔴": "fuse"}
    return {
        "node_id": f"FLOW-9622-{datetime.now().strftime('%Y%m%d')}-{hash8}",
        "title": title[:36],
        "raw_type": raw_type if raw_type in _VALID_RAW_TYPES else "text",
        "digital_root": dr,
        "element": element,
        "relation": relation,
        "sancai": {"heaven": 0.35, "earth": 0.15, "human": 0.50},
        "audit": audit,
        "dna": _生成DNA(title),
        "visual": dict(五行视觉[element]),
        "action": action_map[audit],
        "note": "文化语义算法节点，不替代科学实验、法律程序、医学判断或金融判断。",
    }


def 校验节点(node: dict) -> tuple[bool, list[str]]:
    """
    校验 Node JSON 的12个字段。
    返回 (通过: bool, 错误列表: list[str])
    """
    errors: list[str] = []
    nid = node.get("node_id", "")
    if not isinstance(nid, str) or not nid.startswith("FLOW-9622-"):
        errors.append("node_id 必须以 FLOW-9622- 开头·含8位大写哈希")
    if node.get("raw_type") not in _VALID_RAW_TYPES:
        errors.append(f"raw_type 非法：{node.get('raw_type')}")
    dr = node.get("digital_root")
    if not isinstance(dr, int) or not (0 <= dr <= 9):
        errors.append(f"digital_root 越界：{dr}（应为0-9）")
    if node.get("element") not in _VALID_ELEMENTS:
        errors.append(f"element 非法：{node.get('element')}")
    if node.get("relation") not in _VALID_RELATIONS:
        errors.append(f"relation 非法：{node.get('relation')}")
    sancai = node.get("sancai", {})
    if not all(k in sancai for k in ("heaven", "earth", "human")):
        errors.append("sancai 缺少必要键 heaven/earth/human")
    elif sancai.get("human", 0) < _HUMAN_MIN:
        errors.append(f"sancai.human={sancai['human']} < 铁线{_HUMAN_MIN}·人场不能被压")
    if node.get("audit") not in _VALID_AUDITS:
        errors.append(f"audit 非法：{node.get('audit')}")
    dna = node.get("dna", "")
    if not isinstance(dna, str) or not dna.startswith("#龍芯⚡️"):
        errors.append("dna 必须以 #龍芯⚡️ 开头")
    visual = node.get("visual", {})
    for key in ("color", "shape", "motion"):
        if key not in visual:
            errors.append(f"visual 缺少子键：{key}")
    if node.get("action") not in _VALID_ACTIONS:
        errors.append(f"action 非法：{node.get('action')}")
    title = node.get("title", "")
    if not isinstance(title, str) or len(title) > 36:
        errors.append(f"title 超长（{len(str(title))}字符，最大36）")
    note = node.get("note", "")
    if isinstance(note, str) and len(note) > 200:
        errors.append(f"note 超长（{len(note)}字符，最大200）")
    return (len(errors) == 0, errors)

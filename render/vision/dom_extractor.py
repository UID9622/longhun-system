# DNA: #龍芯⚡️2026-08-25-RENDER-ENV-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""DOM/AX 树提取辅助。对已渲染上下文做后处理。"""


def count_depth(dom: dict) -> int:
    """计算 DOM 树最大深度。"""
    if not isinstance(dom, dict):
        return 0
    children = dom.get("children") or []
    if not children:
        return 1
    return 1 + max(count_depth(c) for c in children)


def summarize(dom: dict, limit: int = 200) -> list:
    """展平 DOM 为摘要列表 [{tag, id, class, text}]。"""
    out = []

    def walk(node, depth):
        if not isinstance(node, dict) or len(out) >= limit:
            return
        out.append({
            "tag": node.get("tag"),
            "id": node.get("id"),
            "class": node.get("class"),
            "text": node.get("text"),
            "depth": depth,
        })
        for c in node.get("children") or []:
            walk(c, depth + 1)

    walk(dom, 0)
    return out

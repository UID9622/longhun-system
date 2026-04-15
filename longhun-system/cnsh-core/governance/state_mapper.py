"""
状态映射器
Event → CompositeState (8×8=64)

Author: 诸葛鑫 (UID9622)
"""

from core import State, CompositeState, Event


KEYWORD_STATE_MAP = {
    # 主状态关键词
    "init":        State.INITIATION,
    "start":       State.INITIATION,
    "launch":      State.INITIATION,
    "begin":       State.INITIATION,
    "stable":      State.FOUNDATION,
    "base":        State.FOUNDATION,
    "normal":      State.FOUNDATION,
    "trigger":     State.TRIGGER,
    "event":       State.TRIGGER,
    "fire":        State.TRIGGER,
    "activate":    State.TRIGGER,
    "spread":      State.PROPAGATION,
    "broadcast":   State.PROPAGATION,
    "propagate":   State.PROPAGATION,
    "risk":        State.RISK,
    "danger":      State.RISK,
    "threat":      State.RISK,
    "crisis":      State.RISK,
    "alert":       State.RISK,
    "aware":       State.AWARENESS,
    "observe":     State.AWARENESS,
    "monitor":     State.AWARENESS,
    "limit":       State.BOUNDARY,
    "boundary":    State.BOUNDARY,
    "block":       State.BOUNDARY,
    "constraint":  State.BOUNDARY,
    "cooperate":   State.COOPERATION,
    "collaborate": State.COOPERATION,
    "multi":       State.COOPERATION,
}


class StateMapper:

    def map(self, event: Event) -> CompositeState:
        """
        两阶段映射:
        1. 检测硬约束 (BOUNDARY/RISK)
        2. 关键词匹配
        3. 默认 FOUNDATION
        """
        content_lower = event.content.lower()

        # 阶段1：硬约束优先
        if any(w in content_lower for w in ["block", "forbidden", "illegal", "danger"]):
            primary = State.BOUNDARY
        elif any(w in content_lower for w in ["risk", "threat", "harm", "attack"]):
            primary = State.RISK
        else:
            # 阶段2：关键词
            primary = State.FOUNDATION
            for kw, state in KEYWORD_STATE_MAP.items():
                if kw in content_lower:
                    primary = state
                    break

        # 二级状态：元数据或内容辅助
        metadata = event.metadata
        if metadata.get("cooperation") or "collab" in content_lower:
            secondary = State.COOPERATION
        elif metadata.get("awareness") or "monitor" in content_lower:
            secondary = State.AWARENESS
        elif primary == State.RISK:
            secondary = State.BOUNDARY
        else:
            secondary = primary  # 默认同态

        return CompositeState(primary=primary, secondary=secondary)

"""
Audit Wrapper — injects seven-factor behavioral audit metadata.

Produces a behavioral signature Σ(C) for any content artifact C,
including factor labels, behavior pattern classification, and
credit score impact assessment.

This is a shell tool. Core scoring algorithms are protected.
"""

import hashlib
import json
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional


# Behavior pattern templates (public definitions)
BEHAVIOR_PATTERNS = {
    "MODE-DefensiveDefaulter": {
        "description": "Promises but fails to deliver, then over-explains to deflect responsibility",
        "signature": {"F": "Unfulfilled", "X": "OverExplain"},
        "credit_impact": "negative",
    },
    "MODE-ExternalTrustSpender": {
        "description": "Keeps promises to outsiders at the expense of inner circle",
        "signature": {"F": "Fulfilled", "A": "Outsider"},
        "credit_impact": "mixed",
    },
    "MODE-InternalDestroyer": {
        "description": "Breaks promises with indifference to consequences or correction",
        "signature": {"F": "Unfulfilled", "Y": "Indifferent"},
        "credit_impact": "severely_negative",
    },
    "MODE-Fluctuating": {
        "description": "High volatility in commitment-to-fulfillment ratio (Z > 2)",
        "signature": {"Z_gt": 2},
        "credit_impact": "unstable",
    },
    "MODE-StableDisciplined": {
        "description": "Consistent, reliable execution with steady behavioral profile",
        "signature": {"default": True},
        "credit_impact": "positive",
    },
}


class AuditWrapper:
    """
    Generates seven-factor behavioral audit metadata for any payload.

    Public shell: wraps data with behavioral labels and audit structure.
    Core scoring engine: protected intellectual property.
    """

    def __init__(self, uid="9622"):
        self.uid = uid

    def wrap(self, data: Any, task_type: str = "default",
             persona: str = "P04") -> Dict[str, Any]:
        """
        Generate audit metadata for a payload.

        Parameters:
            data: The payload being audited
            task_type: Task category
            persona: Persona identifier

        Returns:
            Seven-factor behavioral signature dict
        """
        # Build behavioral signature
        signature = self._build_signature(data, task_type)

        # Classify behavior pattern
        pattern = self._classify(signature)

        # Get behavior labels
        labels = self._get_labels(signature, pattern, persona)

        return {
            "audit_version": "v1.0",
            "uid": self.uid,
            "persona": persona,
            "task_type": task_type,
            "behavior_signature": signature,
            "behavior_pattern": pattern,
            "behavior_labels": labels,
            "color": self._audit_color(signature, pattern),
            "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
            "payload_hash": hashlib.sha256(
                json.dumps(data, sort_keys=True, default=str).encode()
            ).hexdigest()[:16],
        }

    def _build_signature(self, data: Any, task_type: str) -> Dict[str, Any]:
        """Build the seven-factor behavioral signature Σ(C)."""
        return {
            # P — Promise
            "P": "HasPromise" if task_type != "default" else "NoPromise",

            # F — Fulfill (default: Fulfilled for user-requested actions)
            "F": "Fulfilled",

            # T — Time deviation (seconds since request, negative = early)
            "T": 0.0,

            # E — Emotion (default: Willing for adapter use)
            "E": "Willing",

            # C — Cost (resource investment, placeholder)
            "C": 0,

            # R — Repeat (cumulative similar failures, default 0)
            "R": 0,

            # A — Audience
            "A": "Self",

            # X — eXplain tendency
            "X": "Genuine",

            # Y — Yield (correction pattern)
            "Y": "NoResponse",

            # Z — Zigzag (volatility, default 1.0 = stable)
            "Z": 1.0,
        }

    def _classify(self, sig: Dict[str, Any]) -> str:
        """Classify behavior pattern from seven-factor signature."""
        if sig.get("F") == "Unfulfilled" and sig.get("X") == "OverExplain":
            return "MODE-DefensiveDefaulter"
        if sig.get("F") == "Fulfilled" and sig.get("A") == "Outsider":
            return "MODE-ExternalTrustSpender"
        if sig.get("F") == "Unfulfilled" and sig.get("Y") == "Indifferent":
            return "MODE-InternalDestroyer"
        if sig.get("Z", 1.0) > 2:
            return "MODE-Fluctuating"
        return "MODE-StableDisciplined"

    def _get_labels(self, sig: Dict[str, Any], pattern: str,
                    persona: str) -> list:
        """Generate behavior label tags."""
        labels = [f"7F-P-{self._cn_p(sig.get('P', ''))}"]
        labels.append(f"7F-F-{self._cn_f(sig.get('F', ''))}")
        labels.append(f"7F-E-{self._cn_e(sig.get('E', ''))}")
        labels.append(pattern)
        return labels

    def _audit_color(self, sig: Dict[str, Any], pattern: str) -> str:
        """Determine audit color."""
        if pattern == "MODE-InternalDestroyer":
            return "🔴"
        if pattern == "MODE-Fluctuating":
            return "🟡"
        return "🟢"

    # Chinese label converters (public mapping, core logic protected)
    _cn_p = lambda self, v: {"HasPromise": "有承诺", "NoPromise": "无承诺"}.get(v, v)
    _cn_f = lambda self, v: {"Fulfilled": "已兑现", "Unfulfilled": "未兑现", "Partial": "部分兑现"}.get(v, v)
    _cn_e = lambda self, v: {
        "Willing": "心甘情愿", "Perfunctory": "敷衍",
        "Resentful": "怨恨", "Numb": "麻木"
    }.get(v, v)


def audit_wrap(data, task_type="default", persona="P04", uid="9622") -> Dict[str, Any]:
    """Convenience function for quick audit wrapping."""
    wrapper = AuditWrapper(uid=uid)
    return wrapper.wrap(data, task_type=task_type, persona=persona)

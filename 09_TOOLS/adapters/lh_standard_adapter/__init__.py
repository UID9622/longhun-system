# DNA: #龍芯⚡️丙午·丙申·甲戌·卯时·䷐随-QUAD-SYNC-v1.0-ATTRIBUTION-8c26d5f
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
LongHun Standard Adapter — lh_standard_adapter

Wrap any JSON payload with LongHun-compliant DNA traceability
and behavioral audit metadata.

Usage:
    from lh_standard_adapter import LongHunAdapter

    adapter = LongHunAdapter(uid="9622", device="HM-9622-001")
    compliant = adapter.wrap(
        data={"code": "print('hello')", "language": "python"},
        task_type="code",
        persona="Baobao"
    )
    assert adapter.validate(compliant)

Open Source: CC-BY-NC-SA 4.0
Core Engine: Protected. This adapter is a shell tool only.
Author: LongHun Core · UID9622
DNA: #LongHun⚡️BingWu·GuiWei·JiaZi·ZiShi·䷾JiJi-ADAPTER-v1.0
"""

from .dna_generator import DNAGenerator
from .audit_wrapper import AuditWrapper
from .validator import Validator
from .schemas import get_dna_schema, get_audit_schema

__version__ = "1.0.0"
__author__ = "LongHun Core · UID9622"
__license__ = "CC BY-NC-SA 4.0"


class LongHunAdapter:
    """
    Main adapter. Wraps arbitrary JSON payloads into LongHun-compliant
    format with DNA traceability + seven-factor behavioral audit metadata.

    Parameters:
        uid: User ID (default: "9622")
        device: Device identifier (default: "HM-9622-001")
        locale: Timezone locale (default: "Asia/Shanghai")
    """

    def __init__(self, uid="9622", device="HM-9622-001", locale="Asia/Shanghai"):
        self.uid = uid
        self.device = device
        self.locale = locale
        self._dna_gen = DNAGenerator(uid=uid, device=device, locale=locale)
        self._audit = AuditWrapper(uid=uid)
        self._validator = Validator()

    def wrap(self, data, task_type="default", persona="P04"):
        """
        Wrap raw JSON data with full LongHun compliance metadata.

        Parameters:
            data: Raw payload (dict, list, or JSON-serializable)
            task_type: Task category (e.g. "code", "deploy", "audit", "default")
            persona: Persona identifier (e.g. "P04-Luban", "P00-Wenxin", "P02-Baobao")

        Returns:
            dict: {
                "dna": "<DNA traceability code>",
                "audit": {<seven-factor behavioral signature>},
                "payload": <original data>,
                "meta": {<wrapper metadata>}
            }
        """
        dna = self._dna_gen.generate(task_type=task_type)
        audit = self._audit.wrap(data, task_type=task_type, persona=persona)

        return {
            "dna": dna,
            "audit": audit,
            "payload": data,
            "meta": {
                "adapter_version": __version__,
                "uid": self.uid,
                "device": self.device,
                "task_type": task_type,
                "persona": persona,
                "generated_at": self._dna_gen._now_iso(),
                "format": "longhun-v∞",
            },
        }

    def validate(self, wrapped):
        """
        Validate a wrapped payload against DNA and Audit JSON Schemas.

        Parameters:
            wrapped: Output from self.wrap()

        Returns:
            dict: {"valid": bool, "errors": [...], "warnings": [...]}
        """
        return self._validator.validate_all(wrapped)

    def get_schemas(self):
        """
        Return the JSON Schema definitions used for validation.

        Returns:
            dict: {"dna_schema": {...}, "audit_schema": {...}}
        """
        return {
            "dna_schema": get_dna_schema(),
            "audit_schema": get_audit_schema(),
        }


def wrap(data, task_type="default", persona="P04", uid="9622", device="HM-9622-001"):
    """
    Convenience function: one-shot wrap without creating an adapter instance.

    Usage:
        from lh_standard_adapter import wrap
        result = wrap({"foo": "bar"}, task_type="test")
    """
    adapter = LongHunAdapter(uid=uid, device=device)
    return adapter.wrap(data, task_type=task_type, persona=persona)

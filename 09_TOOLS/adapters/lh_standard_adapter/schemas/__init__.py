# DNA: #龍芯⚡️丙午·丙申·甲戌·卯时·䷐随-QUAD-SYNC-v1.0-ATTRIBUTION-8c26d5f
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
JSON Schema definitions for DNA and Audit payloads.

Used by the Validator for structural compliance checks.
"""

import json
import os

_SCHEMA_DIR = os.path.dirname(os.path.abspath(__file__))


def get_dna_schema() -> dict:
    """Return the DNA traceability code JSON Schema."""
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://uid9622.cn/schemas/dna-v1.0.json",
        "title": "LongHun DNA Traceability Code",
        "description": "Schema for validating LongHun v∞ DNA traceability codes",
        "type": "object",
        "required": ["dna", "format", "uid", "timestamp"],
        "properties": {
            "dna": {
                "type": "string",
                "description": "Full v∞ DNA traceability code",
                "pattern": (
                    "^#LongHun⚡️"
                    "[A-Z][a-zA-Z]+·[A-Z][a-zA-Z]+·[A-Z][a-zA-Z]+·[A-Z][a-zA-Z]+"
                    "·[䷀-䷿][A-Za-z]+"
                    "-.+"
                    "-[a-f0-9]{8}$"
                ),
            },
            "format": {
                "type": "string",
                "enum": ["v1.0", "v2.0", "v∞", "compact"],
                "default": "v∞",
            },
            "uid": {
                "type": "string",
                "pattern": "^UID\\d+$",
            },
            "device": {
                "type": "string",
                "description": "Device identifier",
            },
            "timestamp": {
                "type": "string",
                "format": "date-time",
            },
            "year_stem_branch": {
                "type": "string",
                "pattern": "^[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]$",
            },
            "month_stem_branch": {
                "type": "string",
                "pattern": "^[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]$",
            },
            "day_stem_branch": {
                "type": "string",
                "pattern": "^[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]$",
            },
            "shichen": {
                "type": "string",
                "pattern": "^[A-Z][a-z]*(Shi)[A-Za-z]*$",
            },
            "hexagram": {
                "type": "string",
                "description": "I Ching hexagram symbol + name",
                "pattern": "^[䷀-䷿][A-Za-z]+$",
            },
            "module": {
                "type": "string",
                "pattern": "^[A-Z][A-Z0-9-]+$",
            },
            "action": {
                "type": "string",
                "pattern": "^[A-Z][A-Z0-9-]+$",
            },
        },
    }


def get_audit_schema() -> dict:
    """Return the Audit payload JSON Schema."""
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://uid9622.cn/schemas/audit-v1.0.json",
        "title": "LongHun Audit Record",
        "description": "Schema for validating LongHun seven-factor behavioral audit records",
        "type": "object",
        "required": ["dna", "audit", "payload", "meta"],
        "properties": {
            "dna": {
                "type": "string",
                "description": "DNA traceability code",
            },
            "audit": {
                "type": "object",
                "required": ["behavior_signature", "behavior_pattern", "color"],
                "properties": {
                    "audit_version": {"type": "string"},
                    "uid": {"type": "string", "pattern": "^UID\\d+$"},
                    "persona": {"type": "string"},
                    "task_type": {"type": "string"},
                    "behavior_signature": {
                        "type": "object",
                        "required": ["P", "F", "T", "E", "C", "R", "A", "X", "Y", "Z"],
                        "properties": {
                            "P": {"enum": ["HasPromise", "NoPromise"]},
                            "F": {"enum": ["Fulfilled", "Unfulfilled", "Partial"]},
                            "T": {"type": "number"},
                            "E": {"enum": ["Willing", "Perfunctory", "Resentful", "Numb"]},
                            "C": {"type": "number"},
                            "R": {"type": "integer", "minimum": 0},
                            "A": {"enum": ["Self", "Partner", "Family", "Outsider", "Public"]},
                            "X": {"enum": ["OverExplain", "Silent", "Genuine", "Indifferent"]},
                            "Y": {"enum": ["Changed", "Resisted", "Indifferent", "NoResponse"]},
                            "Z": {"type": "number"},
                        },
                    },
                    "behavior_pattern": {
                        "enum": [
                            "MODE-DefensiveDefaulter",
                            "MODE-ExternalTrustSpender",
                            "MODE-InternalDestroyer",
                            "MODE-Fluctuating",
                            "MODE-StableDisciplined",
                        ],
                    },
                    "behavior_labels": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "color": {
                        "enum": ["🟢", "🟡", "🔴"],
                    },
                    "timestamp": {
                        "type": "string",
                        "format": "date-time",
                    },
                    "payload_hash": {
                        "type": "string",
                        "pattern": "^[a-f0-9]{16}$",
                    },
                },
            },
            "payload": {
                "description": "Original payload data",
            },
            "meta": {
                "type": "object",
                "required": ["adapter_version", "uid", "device", "task_type", "persona"],
                "properties": {
                    "adapter_version": {"type": "string"},
                    "uid": {"type": "string", "pattern": "^UID\\d+$"},
                    "device": {"type": "string"},
                    "task_type": {"type": "string"},
                    "persona": {"type": "string"},
                    "generated_at": {"type": "string"},
                    "format": {"const": "longhun-v∞"},
                },
            },
        },
    }

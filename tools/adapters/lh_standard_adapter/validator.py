"""
Validator — validates DNA and Audit payloads against JSON Schema.

Checks:
1. DNA format compliance (regex + structural)
2. Audit payload compliance (schema + consistency)
3. Cross-validation (DNA ↔ Audit linkage)
"""

import hashlib
import json
import re
from typing import Any, Dict, List


# DNA v∞ validation regex
DNA_REGEX = re.compile(
    r"^#LongHun⚡️"
    r"([A-Z][a-zA-Z]+)·([A-Z][a-zA-Z]+)·([A-Z][a-zA-Z]+)·([A-Z][a-zA-Z]+)"  # Four pillars
    r"·([䷀-䷿][A-Za-z]+)"                                            # Hexagram
    r"-(.+)"                                                          # Body (module-action-version)
    r"-([a-f0-9]{8})$"                                                # Hash8
)

# Four-layer naming regex
NAME_REGEX = re.compile(
    r"^[A-Z]{2,5}-(UID\d+|SYS|PUB)-"
    r"(龍芯?[\u26a1\ufe0f]*[^-\s]+)"
    r"-(.+?)-v([\d.]+)(?:\.(.+))?$"
)

# Valid enumeration values
VALID_P = {"HasPromise", "NoPromise"}
VALID_F = {"Fulfilled", "Unfulfilled", "Partial"}
VALID_E = {"Willing", "Perfunctory", "Resentful", "Numb"}
VALID_A = {"Self", "Partner", "Family", "Outsider", "Public"}
VALID_X = {"OverExplain", "Silent", "Genuine", "Indifferent"}
VALID_Y = {"Changed", "Resisted", "Indifferent", "NoResponse"}
VALID_COLORS = {"🟢", "🟡", "🔴"}
VALID_PATTERNS = {
    "MODE-DefensiveDefaulter",
    "MODE-ExternalTrustSpender",
    "MODE-InternalDestroyer",
    "MODE-Fluctuating",
    "MODE-StableDisciplined",
}


class Validator:
    """Validates LongHun-compliant payloads."""

    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate_all(self, wrapped: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run all validations on a wrapped payload.

        Returns:
            {"valid": bool, "errors": [...], "warnings": [...]}
        """
        self.errors = []
        self.warnings = []

        if not isinstance(wrapped, dict):
            self.errors.append("Payload must be a dictionary")
            return self._result()

        # Structure check
        for key in ("dna", "audit", "payload", "meta"):
            if key not in wrapped:
                self.errors.append(f"Missing required key: '{key}'")

        if self.errors:
            return self._result()

        # DNA validation
        self._validate_dna(wrapped.get("dna", ""))

        # Audit validation
        self._validate_audit(wrapped.get("audit", {}))

        # Cross-validation
        self._cross_validate(wrapped)

        # Meta validation
        self._validate_meta(wrapped.get("meta", {}))

        # Payload hash verification
        self._verify_payload_hash(wrapped)

        return self._result()

    def _validate_dna(self, dna: str):
        """Validate DNA traceability code."""
        if not dna:
            self.errors.append("DNA code is empty")
            return

        if not dna.startswith("#LongHun⚡️"):
            self.errors.append("DNA must start with '#LongHun⚡️'")
            return

        match = DNA_REGEX.match(dna)
        if not match:
            self.errors.append(f"DNA format invalid: {dna}")
            return

        # Verify hash8 (group 7 = last capture group)
        hash8 = match.group(7)
        if len(hash8) != 8 or not all(c in "0123456789abcdef" for c in hash8):
            self.errors.append(f"Invalid hash8: {hash8}")

    def _validate_audit(self, audit: Dict[str, Any]):
        """Validate audit metadata."""
        if not audit:
            self.errors.append("Audit metadata is empty")
            return

        # Check signature
        sig = audit.get("behavior_signature", {})
        if not sig:
            self.warnings.append("No behavior_signature in audit")
        else:
            self._validate_signature(sig)

        # Check pattern
        pattern = audit.get("behavior_pattern", "")
        if pattern and pattern not in VALID_PATTERNS:
            self.warnings.append(f"Unknown behavior pattern: {pattern}")

        # Check color
        color = audit.get("color", "")
        if color and color not in VALID_COLORS:
            self.warnings.append(f"Unknown audit color: {color}")

        # Check labels
        labels = audit.get("behavior_labels", [])
        if not labels:
            self.warnings.append("No behavior_labels in audit")

    def _validate_signature(self, sig: Dict[str, Any]):
        """Validate seven-factor signature fields."""
        validations = [
            ("P", VALID_P, sig.get("P")),
            ("F", VALID_F, sig.get("F")),
            ("E", VALID_E, sig.get("E")),
            ("A", VALID_A, sig.get("A")),
            ("X", VALID_X, sig.get("X")),
            ("Y", VALID_Y, sig.get("Y")),
        ]
        for field, valid_set, value in validations:
            if value and value not in valid_set:
                self.warnings.append(
                    f"Factor '{field}' has unknown value '{value}'. "
                    f"Valid: {valid_set}"
                )

        # Numeric fields
        for field in ("T", "C", "Z"):
            v = sig.get(field)
            if v is not None and not isinstance(v, (int, float)):
                self.warnings.append(f"Factor '{field}' must be numeric, got {type(v).__name__}")

        r_val = sig.get("R")
        if r_val is not None and (not isinstance(r_val, int) or r_val < 0):
            self.warnings.append(f"Factor 'R' must be non-negative integer, got {r_val}")

    def _cross_validate(self, wrapped: Dict[str, Any]):
        """Cross-check DNA vs Audit consistency."""
        audit = wrapped.get("audit", {})
        meta = wrapped.get("meta", {})

        # Task type consistency
        at = audit.get("task_type", "")
        mt = meta.get("task_type", "")
        if at and mt and at != mt:
            self.warnings.append(f"Task type mismatch: audit={at}, meta={mt}")

        # Persona consistency
        ap = audit.get("persona", "")
        mp = meta.get("persona", "")
        if ap and mp and ap != mp:
            self.warnings.append(f"Persona mismatch: audit={ap}, meta={mp}")

        # UID consistency
        au = audit.get("uid", "")
        mu = meta.get("uid", "")
        if au and mu and au != mu:
            self.errors.append(f"UID mismatch: audit={au}, meta={mu}")

    def _validate_meta(self, meta: Dict[str, Any]):
        """Validate metadata fields."""
        if not meta:
            self.warnings.append("Meta section is empty")
            return

        if "adapter_version" not in meta:
            self.warnings.append("Missing adapter_version in meta")

    def _verify_payload_hash(self, wrapped: Dict[str, Any]):
        """Verify payload hash matches audit record."""
        payload = wrapped.get("payload")
        audit = wrapped.get("audit", {})
        audit_hash = audit.get("payload_hash")

        if not payload or not audit_hash:
            return

        computed = hashlib.sha256(
            json.dumps(payload, sort_keys=True, default=str).encode()
        ).hexdigest()[:16]

        if computed != audit_hash:
            self.warnings.append(
                f"Payload hash mismatch: audit={audit_hash}, computed={computed}"
            )

    def _result(self) -> Dict[str, Any]:
        """Build validation result."""
        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
            "summary": (
                f"{'❌ INVALID' if self.errors else '✅ VALID'} — "
                f"{len(self.errors)} errors, {len(self.warnings)} warnings"
            ),
        }


def quick_validate(wrapped: Dict[str, Any]) -> bool:
    """Quick boolean check: is this payload valid?"""
    result = Validator().validate_all(wrapped)
    return result["valid"]

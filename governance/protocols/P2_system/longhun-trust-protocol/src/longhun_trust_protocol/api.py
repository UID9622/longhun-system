#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂君子协议 · Python API
DNA: #龍芯⚡️2026-06-26-LONGHUN-TRUST-API-v1.0
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from .core import EventType, Grade, SlaughterLevel, TrustEvent, TrustProfile
from .storage import TrustStore


class TrustProtocol:
    """对外统一的君子协议接口。"""

    def __init__(self, base_dir: str = "~/.longhun/trust_protocol"):
        self.store = TrustStore(base_dir)

    def register(self, uid: str, name: str = "") -> TrustProfile:
        profile = TrustProfile(uid, name)
        self.store.save(profile)
        return profile

    def get(self, uid: str) -> TrustProfile:
        return self.store.load(uid)

    def save(self, profile: TrustProfile) -> None:
        self.store.save(profile)

    def moral(self, uid: str, action: str, description: str = "") -> TrustProfile:
        p = self.get(uid)
        p.moral_action(action, description)
        self.store.save(p)
        return p

    def character(self, uid: str, action: str, description: str = "") -> TrustProfile:
        p = self.get(uid)
        p.character_action(action, description)
        self.store.save(p)
        return p

    def integrity(self, uid: str, action: str, description: str = "") -> TrustProfile:
        p = self.get(uid)
        p.integrity_action(action, description)
        self.store.save(p)
        return p

    def violate(self, uid: str, description: str = "", evidence: str = "") -> TrustProfile:
        p = self.get(uid)
        p.violate(description, evidence)
        self.store.save(p)
        return p

    def contribute(self, uid: str, contrib_type: str, description: str = "") -> TrustProfile:
        p = self.get(uid)
        p.contribute(contrib_type, description)
        self.store.save(p)
        return p

    def check_slaughter(self, uid: str) -> Dict[str, Any]:
        p = self.get(uid)
        result = p.check_slaughter()
        self.store.save(p)
        return result

    def can_redeem(self, uid: str, target_grade: str) -> Dict[str, Any]:
        p = self.get(uid)
        return p.can_redeem(Grade(target_grade))

    def redeem(self, uid: str, target_grade: str) -> TrustProfile:
        p = self.get(uid)
        p.redeem(Grade(target_grade))
        self.store.save(p)
        return p

    def list_profiles(self) -> list[Any]:
        return self.store.list_profiles()

    def verify(self, uid: str) -> bool:
        return self.store.verify_integrity(uid)

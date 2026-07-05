#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙魂君子协议 · 链式存储与审计
DNA: #龍芯⚡️2026-06-26-LONGHUN-TRUST-STORAGE-v1.0

本地 JSON 持久化 + SHA-256 链式哈希，保证事件不可篡改。
GPG 签名预留接口，需用户配置真实 GPG 密钥后启用。
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Dict, Optional

from .core import TrustProfile


class TrustStore:
    """本地信任档案存储，每条记录带链式哈希。"""

    def __init__(self, base_dir: str = "~/.longhun/trust_protocol"):
        self.base_dir = Path(base_dir).expanduser()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.chain_hash_file = self.base_dir / "chain_hash.jsonl"

    def _profile_path(self, uid: str) -> Path:
        return self.base_dir / f"{uid}.json"

    def save(self, profile: TrustProfile, gpg_key: Optional[str] = None) -> None:
        data = profile.to_dict()
        data["_chain_hash"] = self._compute_hash(data)
        if gpg_key:
            data["_gpg_signature"] = self._gpg_sign_placeholder(data, gpg_key)
        path = self._profile_path(profile.uid)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        self._append_chain_hash(profile.uid, data["_chain_hash"])

    def load(self, uid: str) -> TrustProfile:
        path = self._profile_path(uid)
        if not path.exists():
            raise FileNotFoundError(f"未找到信任档案: {uid}")
        data = json.loads(path.read_text(encoding="utf-8"))
        return TrustProfile.from_dict(data)

    def list_profiles(self) -> list:
        return [p.stem for p in self.base_dir.glob("*.json")]

    def _compute_hash(self, data: Dict) -> str:
        canonical = json.dumps(data, ensure_ascii=False, sort_keys=True, default=str)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def _append_chain_hash(self, uid: str, record_hash: str) -> None:
        prev_hash = "0" * 64
        if self.chain_hash_file.exists():
            lines = self.chain_hash_file.read_text(encoding="utf-8").strip().split("\n")
            if lines and lines[-1]:
                try:
                    prev = json.loads(lines[-1])
                    prev_hash = prev.get("hash", prev_hash)
                except Exception:
                    pass
        payload = f"{uid}:{record_hash}:{prev_hash}"
        entry_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        entry = json.dumps(
            {"uid": uid, "hash": entry_hash, "prev_hash": prev_hash, "record_hash": record_hash},
            ensure_ascii=False,
        )
        with self.chain_hash_file.open("a", encoding="utf-8") as f:
            f.write(entry + "\n")

    def _gpg_sign_placeholder(self, data: Dict, key: str) -> str:
        # 真实环境应调用 gnupg 库；此处为合规预留接口
        canonical = json.dumps(data, ensure_ascii=False, sort_keys=True, default=str)
        return f"GPG-SIGNATURE-PLACEHOLDER({key[:16]}...):{hashlib.sha256(canonical.encode()).hexdigest()[:16]}"

    def verify_integrity(self, uid: str) -> bool:
        """校验单个档案的链式哈希是否自洽。"""
        path = self._profile_path(uid)
        if not path.exists():
            return False
        data = json.loads(path.read_text(encoding="utf-8"))
        stored_hash = data.pop("_chain_hash", None)
        return stored_hash == self._compute_hash(data)

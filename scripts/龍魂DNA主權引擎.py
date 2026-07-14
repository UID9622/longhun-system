#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · DNA 主權與貢獻繼承規則引擎
DNA:#龍芯⚡️2026-06-30-LONGHUN-DNA-SOVEREIGNTY-ENGINE-FILE1-v1.0

把「一世一双人」「DNA 不可轉讓」「可繼承不可覆蓋」「貢獻不可變現」「歷史 append-only」
五條鐵律落實為可執行的 Python API 與命令行工具。

核心文件：
  ~/.龍魂/dna_registry.json              身份註冊表
  ~/.龍魂/contributions.jsonl            貢獻記錄（append-only）
  ~/.龍魂/dna_inheritance_chain.jsonl    繼承鏈記錄
  ~/longhun-system/logs/龍魂DNA主權審計庫.jsonl  主權事件審計
"""

import argparse
import hashlib
import json
import secrets
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# ---------- 路徑配置 ----------
DNA_REGISTRY_PATH = Path.home() / ".龍魂" / "dna_registry.json"
CONTRIBUTIONS_PATH = Path.home() / ".龍魂" / "contributions.jsonl"
INHERITANCE_PATH = Path.home() / ".龍魂" / "dna_inheritance_chain.jsonl"
SOVEREIGNTY_AUDIT_PATH = Path.home() / "longhun-system" / "logs" / "龍魂DNA主權審計庫.jsonl"
TAGS_PATH = Path.home() / ".龍魂" / "dna_record_tags.jsonl"
RULES_PATH = Path.home() / ".龍魂" / "rules" / "DNA_SOVEREIGNTY_RULES.md"

FOUNDER = "UID9622"
DNA_PREFIX = "#龍芯⚡️"


# ---------- 通用工具 ----------
def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _generate_event_dna(event_type: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    rand = secrets.token_hex(4).upper()
    return f"{DNA_PREFIX}{ts}-SOVEREIGNTY-{event_type}-{rand}"


def _ensure_paths() -> None:
    for p in (DNA_REGISTRY_PATH, CONTRIBUTIONS_PATH, INHERITANCE_PATH, SOVEREIGNTY_AUDIT_PATH):
        p.parent.mkdir(parents=True, exist_ok=True)


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _looks_like_dna(text: str) -> bool:
    return isinstance(text, str) and text.startswith(DNA_PREFIX)


def _load_tags() -> dict[str, dict[str, Any]]:
    """讀取 DNA 標籤側寫，返回 dna -> 最新標籤記錄。"""
    tags: dict[str, dict[str, Any]] = {}
    if not TAGS_PATH.exists():
        return tags
    with TAGS_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                dna = rec.get("dna")
                if dna:
                    tags[dna] = rec
            except Exception:
                continue
    return tags


# ---------- 引擎主類 ----------
class DnaSovereigntyEngine:
    """DNA 主權與貢獻繼承規則引擎"""

    def __init__(self, founder: str = FOUNDER) -> None:
        self.founder = founder
        _ensure_paths()
        self.registry = self._load_registry()

    # ---- 註冊表操作 ----
    def _load_registry(self) -> dict[str, Any]:
        default = {
            "identities": {},
            "active_sessions": {},
            "dna": f"{DNA_PREFIX}2026-06-30-DNA-REGISTRY-LONGHUN",
            "version": "1.0",
        }
        data = _load_json(DNA_REGISTRY_PATH, default)
        data.setdefault("identities", {})
        data.setdefault("active_sessions", {})
        return data

    def _save_registry(self) -> None:
        _save_json(DNA_REGISTRY_PATH, self.registry)

    def _audit(
        self,
        event: str,
        dna_identity: str,
        operator: str,
        status: str,
        reason: str,
        detail: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """把主權事件寫入 append-only 審計庫。"""
        record = {
            "dna": _generate_event_dna(event),
            "timestamp": _now(),
            "event": event,
            "dna_identity": dna_identity,
            "operator": operator,
            "status": status,
            "reason": reason,
            "detail": detail or {},
        }
        _append_jsonl(SOVEREIGNTY_AUDIT_PATH, record)
        return record

    def _identity_exists(self, dna_identity: str) -> bool:
        return dna_identity in self.registry.get("identities", {})

    def _get_active_identity_by_biometric(self, biometric_hash: str) -> Optional[str]:
        for dna, info in self.registry.get("identities", {}).items():
            if info.get("status") == "active" and info.get("biometric_anchor_hash") == biometric_hash:
                return dna
        return None

    def _get_active_identity_by_device(self, device_fingerprint: str) -> Optional[str]:
        sessions = self.registry.get("active_sessions", {})
        for user_id, sess in sessions.items():
            if sess.get("device_fingerprint") == device_fingerprint:
                return sess.get("dna_identity")
        return None

    # ---- 公開 API：身份登記 ----
    def register_identity(
        self,
        dna_identity: str,
        owner_label: str,
        biometric_anchor_hash: str,
        device_fingerprint: str,
        operator: str,
        user_id: str = "",
        tags: list[str] | None = None,
        note: str = "",
        visibility: str = "private",
    ) -> dict[str, Any]:
        """登記一個新的主權 DNA 身份。"""
        if not _looks_like_dna(dna_identity):
            return {
                "ok": False,
                "code": "INVALID_DNA_FORMAT",
                "message": "🔴 拒绝：DNA 格式必须以 #龍芯⚡️ 开头",
            }

        if self._identity_exists(dna_identity):
            self._audit("REGISTER_REJECTED", dna_identity, operator, "🔴", "DNA 已存在")
            return {
                "ok": False,
                "code": "DNA_EXISTS",
                "message": "🔴 拒绝：该 DNA 已登记，不可重复/覆盖",
            }

        # 一世一双人：同一生物锚点不能同时激活两个 DNA
        existing = self._get_active_identity_by_biometric(biometric_anchor_hash)
        if existing and existing != dna_identity:
            self._audit(
                "REGISTER_REJECTED",
                dna_identity,
                operator,
                "🔴",
                "生物锚点已绑定其他活跃 DNA",
                {"existing_dna": existing},
            )
            return {
                "ok": False,
                "code": "ONE_PERSON_ONE_DNA",
                "message": f"🔴 拒绝：一世一双人。该生物锚点已绑定 {existing}",
            }

        identity = {
            "dna_identity": dna_identity,
            "owner_label": owner_label,
            "biometric_anchor_hash": biometric_anchor_hash,
            "device_fingerprint": device_fingerprint,
            "status": "active",
            "created_at": _now(),
            "created_by": operator,
            "inherited_from": None,
            "inheritor": None,
            "tags": list(tags or []),
            "note": note,
            "visibility": visibility,
        }
        self.registry["identities"][dna_identity] = identity

        # 建立/更新活跃会话
        if user_id:
            self.registry["active_sessions"][user_id] = {
                "dna_identity": dna_identity,
                "user_id": user_id,
                "device_fingerprint": device_fingerprint,
                "leased_at": _now(),
            }

        self._save_registry()
        audit = self._audit(
            "REGISTER",
            dna_identity,
            operator,
            "🟢",
            "DNA 身份登记成功",
            {"owner_label": owner_label, "user_id": user_id},
        )
        return {
            "ok": True,
            "code": "REGISTERED",
            "message": f"🟢 DNA 身份 {dna_identity} 已登记并绑定 {owner_label}",
            "identity": identity,
            "audit_dna": audit["dna"],
        }

    # ---- 公開 API：禁止類操作 ----
    def attempt_transfer(
        self, dna_identity: str, from_user: str, to_user: str, operator: str = ""
    ) -> dict[str, Any]:
        """DNA 不可轉讓、借用、買賣。"""
        op = operator or from_user
        self._audit(
            "TRANSFER_BLOCKED",
            dna_identity,
            op,
            "🔴",
            f"嘗試從 {from_user} 轉讓到 {to_user}",
        )
        return {
            "ok": False,
            "code": "TRANSFER_FORBIDDEN",
            "message": "🔴 拒绝：DNA 不可转让、借用或买卖（一世一双人）",
        }

    def delete_identity(self, dna_identity: str, operator: str) -> dict[str, Any]:
        """DNA 不可刪除，只能追加記錄。"""
        self._audit(
            "DELETE_BLOCKED",
            dna_identity,
            operator,
            "🔴",
            "嘗試刪除 DNA 身份或歷史",
        )
        return {
            "ok": False,
            "code": "DELETE_FORBIDDEN",
            "message": "🔴 拒绝：DNA 不可删除，只能追加记录",
        }

    def overwrite_identity(self, dna_identity: str, operator: str) -> dict[str, Any]:
        """DNA 不可覆蓋。"""
        self._audit(
            "OVERWRITE_BLOCKED",
            dna_identity,
            operator,
            "🔴",
            "嘗試覆蓋 DNA 身份信息",
        )
        return {
            "ok": False,
            "code": "OVERWRITE_FORBIDDEN",
            "message": "🔴 拒绝：DNA 不可覆盖，只能追加或继承",
        }

    # ---- 公開 API：繼承 ----
    def seal_and_inherit(
        self,
        old_dna: str,
        new_dna: str,
        owner_label: str,
        biometric_anchor_hash: str,
        device_fingerprint: str,
        operator: str,
        user_id: str = "",
        tags: list[str] | None = None,
        note: str = "",
        visibility: str = "private",
    ) -> dict[str, Any]:
        """
        繼承 DNA：
          1. 舊 DNA 封存（sealed），成為只讀。
          2. 新 DNA 激活，並通過 inherited_from 哈希鏈接到舊 DNA。
          3. 所有原記錄保留，不可修改。
        """
        if not _looks_like_dna(old_dna) or not _looks_like_dna(new_dna):
            return {
                "ok": False,
                "code": "INVALID_DNA_FORMAT",
                "message": "🔴 拒绝：旧/新 DNA 格式必须以 #龍芯⚡️ 开头",
            }

        if not self._identity_exists(old_dna):
            return {
                "ok": False,
                "code": "OLD_DNA_NOT_FOUND",
                "message": "🔴 拒绝：旧 DNA 不存在",
            }

        if self._identity_exists(new_dna):
            return {
                "ok": False,
                "code": "NEW_DNA_EXISTS",
                "message": "🔴 拒绝：新 DNA 已存在，不能覆盖",
            }

        old_identity = self.registry["identities"][old_dna]
        if old_identity.get("status") != "active":
            return {
                "ok": False,
                "code": "OLD_DNA_NOT_ACTIVE",
                "message": "🔴 拒绝：旧 DNA 不处于可继承状态",
            }
        if old_identity.get("inheritor"):
            return {
                "ok": False,
                "code": "ALREADY_INHERITED",
                "message": f"🔴 拒绝：旧 DNA 已由 {old_identity['inheritor']} 继承",
            }

        # 一世一双人：新生物锚点不能與其他活躍身份衝突
        existing = self._get_active_identity_by_biometric(biometric_anchor_hash)
        if existing and existing != old_dna:
            return {
                "ok": False,
                "code": "ONE_PERSON_ONE_DNA",
                "message": f"🔴 拒绝：新身份生物锚点已绑定活跃 DNA {existing}",
            }

        now = _now()
        old_hash = _sha256_text(json.dumps(old_identity, ensure_ascii=False, sort_keys=True))

        # 封存舊鏈
        old_identity["status"] = "sealed"
        old_identity["sealed_at"] = now
        old_identity["sealed_by"] = operator
        old_identity["inheritor"] = new_dna

        # 開新鏈
        new_identity = {
            "dna_identity": new_dna,
            "owner_label": owner_label,
            "biometric_anchor_hash": biometric_anchor_hash,
            "device_fingerprint": device_fingerprint,
            "status": "active",
            "created_at": now,
            "created_by": operator,
            "inherited_from": old_dna,
            "parent_hash": old_hash,
            "inheritor": None,
            "tags": list(tags or []),
            "note": note,
            "visibility": visibility,
        }
        self.registry["identities"][new_dna] = new_identity

        # 更新会话
        if user_id:
            self.registry["active_sessions"][user_id] = {
                "dna_identity": new_dna,
                "user_id": user_id,
                "device_fingerprint": device_fingerprint,
                "leased_at": now,
            }

        # 寫入繼承鏈
        inheritance_record = {
            "dna": _generate_event_dna("INHERIT"),
            "timestamp": now,
            "old_dna": old_dna,
            "new_dna": new_dna,
            "old_hash": old_hash,
            "operator": operator,
            "owner_label": owner_label,
            "tags": list(tags or []),
            "note": note,
            "visibility": visibility,
        }
        _append_jsonl(INHERITANCE_PATH, inheritance_record)
        self._save_registry()

        audit = self._audit(
            "INHERIT",
            new_dna,
            operator,
            "🟢",
            f"DNA 繼承完成：{old_dna} -> {new_dna}",
            {"old_dna": old_dna, "old_hash": old_hash, "owner_label": owner_label},
        )
        return {
            "ok": True,
            "code": "INHERITED",
            "message": f"🟢 DNA 继承完成：{old_dna} 已封存，{new_dna} 已激活",
            "old_identity": old_identity,
            "new_identity": new_identity,
            "inheritance_dna": inheritance_record["dna"],
            "audit_dna": audit["dna"],
        }

    # ---- 公開 API：貢獻 ----
    def record_contribution(
        self,
        dna_identity: str,
        category: str,
        description: str,
        value: Any,
        operator: str,
        monetary_currency: Optional[str] = None,
        transfer_to: Optional[str] = None,
        tags: list[str] | None = None,
        note: str = "",
        visibility: str = "private",
    ) -> dict[str, Any]:
        """登記一條不可變現、不可轉讓的貢獻記錄。"""
        if monetary_currency:
            self._audit(
                "CONTRIBUTION_BLOCKED",
                dna_identity,
                operator,
                "🔴",
                f"嘗試以貨幣 {monetary_currency} 計價貢獻",
            )
            return {
                "ok": False,
                "code": "CONTRIBUTION_MONETIZED",
                "message": "🔴 拒绝：贡献不可变现、不可计价",
            }

        if transfer_to:
            self._audit(
                "CONTRIBUTION_BLOCKED",
                dna_identity,
                operator,
                "🔴",
                f"嘗試轉讓貢獻給 {transfer_to}",
            )
            return {
                "ok": False,
                "code": "CONTRIBUTION_TRANSFER_FORBIDDEN",
                "message": "🔴 拒绝：贡献不可转让",
            }

        if not self._identity_exists(dna_identity):
            return {
                "ok": False,
                "code": "DNA_NOT_FOUND",
                "message": "🔴 拒绝：DNA 身份不存在",
            }

        record = {
            "dna": _generate_event_dna("CONTRIBUTION"),
            "timestamp": _now(),
            "dna_identity": dna_identity,
            "category": category,
            "description": description,
            "value": value,
            "operator": operator,
            "monetary_currency": None,
            "transfer_to": None,
            "tags": list(tags or []),
            "note": note,
            "visibility": visibility,
        }
        _append_jsonl(CONTRIBUTIONS_PATH, record)
        audit = self._audit(
            "CONTRIBUTION",
            dna_identity,
            operator,
            "🟢",
            "贡献记录已追加",
            {"category": category, "value": value},
        )
        return {
            "ok": True,
            "code": "CONTRIBUTION_RECORDED",
            "message": f"🟢 贡献已记录：{category} / {description}",
            "record": record,
            "audit_dna": audit["dna"],
        }

    def attempt_spend_contribution(
        self, dna_identity: str, points: Any, for_goods: str, operator: str
    ) -> dict[str, Any]:
        """貢獻不可消費。"""
        self._audit(
            "SPEND_BLOCKED",
            dna_identity,
            operator,
            "🔴",
            f"嘗試用 {points} 點貢獻兌換 {for_goods}",
        )
        return {
            "ok": False,
            "code": "CONTRIBUTION_NOT_SPENDABLE",
            "message": "🔴 拒绝：贡献不可消费，只能传承",
        }

    def list_contributions(self, dna_identity: str, include_inherited: bool = True) -> dict[str, Any]:
        """查詢某 DNA 的貢獻記錄，可選擇包含繼承來的記錄。"""
        records = []
        inherited_from = None
        if self._identity_exists(dna_identity):
            identity = self.registry["identities"][dna_identity]
            inherited_from = identity.get("inherited_from")

        target_dnas = {dna_identity}
        if include_inherited and inherited_from:
            target_dnas.add(inherited_from)

        if CONTRIBUTIONS_PATH.exists():
            with CONTRIBUTIONS_PATH.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                        if rec.get("dna_identity") in target_dnas:
                            records.append(rec)
                    except Exception:
                        continue

        records.sort(key=lambda r: r.get("timestamp", ""))
        return {
            "ok": True,
            "dna_identity": dna_identity,
            "inherited_from": inherited_from,
            "count": len(records),
            "records": records,
        }

    # ---- 公開 API：修正 ----
    def append_correction(
        self,
        dna_identity: str,
        target_record_dna: str,
        correction_note: str,
        operator: str,
    ) -> dict[str, Any]:
        """做錯了追加修正記錄，原記錄保留。"""
        if not self._identity_exists(dna_identity):
            return {
                "ok": False,
                "code": "DNA_NOT_FOUND",
                "message": "🔴 拒绝：DNA 身份不存在",
            }

        record = {
            "dna": _generate_event_dna("CORRECTION"),
            "timestamp": _now(),
            "dna_identity": dna_identity,
            "target_record_dna": target_record_dna,
            "correction_note": correction_note,
            "operator": operator,
        }
        _append_jsonl(SOVEREIGNTY_AUDIT_PATH, record)
        return {
            "ok": True,
            "code": "CORRECTION_APPENDED",
            "message": "🟡 修正记录已追加，原记录保留",
            "record": record,
        }

    def tag_record(
        self,
        dna: str,
        tags: list[str],
        note: str = "",
        visibility: str = "private",
        operator: str = FOUNDER,
    ) -> dict[str, Any]:
        """為任意 DNA/記錄追加標籤側寫，不改動原 append-only 記錄。"""
        record = {
            "dna": dna,
            "tags": list(tags),
            "note": note,
            "visibility": visibility,
            "labeled_by": operator,
            "timestamp": _now(),
        }
        _append_jsonl(TAGS_PATH, record)
        return {
            "ok": True,
            "code": "TAGGED",
            "message": f"🟢 已为 {dna} 追加标签：{', '.join(tags)}",
            "record": record,
        }

    def get_tags(self, dna: str) -> dict[str, Any]:
        """查詢某 DNA/記錄的最新標籤。"""
        tags = _load_tags()
        return {
            "ok": True,
            "dna": dna,
            "tags": tags.get(dna, {}).get("tags", []),
            "note": tags.get(dna, {}).get("note", ""),
            "visibility": tags.get(dna, {}).get("visibility", "private"),
        }

    # ---- 公開 API：查詢 ----
    def get_identity(self, dna_identity: str) -> Optional[dict[str, Any]]:
        return self.registry.get("identities", {}).get(dna_identity)

    def list_identities(self, status: Optional[str] = None) -> list[dict[str, Any]]:
        ids = []
        for dna, info in self.registry.get("identities", {}).items():
            if status is None or info.get("status") == status:
                ids.append(info)
        return ids

    def get_session(self, user_id: str) -> Optional[dict[str, Any]]:
        return self.registry.get("active_sessions", {}).get(user_id)

    def get_status(self, dna_identity: str) -> dict[str, Any]:
        identity = self.get_identity(dna_identity)
        if not identity:
            return {"ok": False, "code": "DNA_NOT_FOUND", "message": "🔴 DNA 不存在"}
        contributions = self.list_contributions(dna_identity)
        return {
            "ok": True,
            "identity": identity,
            "contributions": contributions,
        }

    # ---- 批量熔斷檢查 ----
    def validate_operation(self, op: str, targets: list[str], operator: str = "") -> dict[str, Any]:
        """對高風險操作進行統一規則熔斷檢查。"""
        if op in ("merge_identities", "batch_transfer", "delete_history"):
            return {
                "ok": False,
                "code": "PERSON_IS_ONE",
                "message": "🔴 拒绝：人永远是 1，历史不可删，DNA 不可批量转移",
            }
        if op == "overwrite_identity":
            return self.overwrite_identity(targets[0] if targets else "", operator)
        return {"ok": True, "code": "ALLOWED", "message": "🟢 操作通过主权检查"}


# ---------- 命令行接口 ----------
def _add_common_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--owner", default=FOUNDER, help="所有者標籤")
    p.add_argument("--biometric", required=True, help="生物特徵錨定哈希（SHA-256）")
    p.add_argument("--device", required=True, help="設備指紋哈希（SHA-256）")
    p.add_argument("--operator", default=FOUNDER, help="操作者")
    p.add_argument("--user-id", default="", help="關聯的系統 user_id")
    _add_tag_args(p)


def _add_tag_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--tags", default="", help="標籤，半形逗號分隔，例如：测试,演示,可公开参考")
    p.add_argument("--note", default="", help="備註說明")
    p.add_argument("--visibility", default="private", choices=["public", "private"], help="可見性")


def _parse_tags(tags_str: str) -> list[str]:
    return [t.strip() for t in tags_str.split(",") if t.strip()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="龍魂 DNA 主權與貢獻繼承規則引擎")
    sub = parser.add_subparsers(dest="cmd")

    p_reg = sub.add_parser("register", help="登記 DNA")
    p_reg.add_argument("--dna", required=True)
    _add_common_args(p_reg)

    p_inherit = sub.add_parser("inherit", help="繼承 DNA")
    p_inherit.add_argument("--old", required=True)
    p_inherit.add_argument("--new", required=True)
    _add_common_args(p_inherit)

    p_contrib = sub.add_parser("contribute", help="登記貢獻")
    p_contrib.add_argument("--dna", required=True)
    p_contrib.add_argument("--category", required=True)
    p_contrib.add_argument("--desc", required=True)
    p_contrib.add_argument("--value", default=1, type=lambda x: int(x) if x.isdigit() else x)
    p_contrib.add_argument("--operator", default=FOUNDER)
    _add_tag_args(p_contrib)

    p_status = sub.add_parser("status", help="查詢 DNA 狀態")
    p_status.add_argument("--dna", required=True)

    p_list = sub.add_parser("list", help="列出身份")
    p_list.add_argument("--status", choices=["active", "sealed", "revoked"])

    p_correct = sub.add_parser("correct", help="追加修正記錄")
    p_correct.add_argument("--dna", required=True)
    p_correct.add_argument("--target", required=True, help="被修正記錄的 DNA")
    p_correct.add_argument("--note", required=True)
    p_correct.add_argument("--operator", default=FOUNDER)

    p_tag = sub.add_parser("tag", help="為記錄追加標籤側寫")
    p_tag.add_argument("--dna", required=True)
    p_tag.add_argument("--tags", required=True, help="標籤，半形逗號分隔")
    p_tag.add_argument("--note", default="")
    p_tag.add_argument("--visibility", default="private", choices=["public", "private"])
    p_tag.add_argument("--operator", default=FOUNDER)

    p_rules = sub.add_parser("rules", help="打印規則文件路徑")

    args = parser.parse_args(argv)
    engine = DnaSovereigntyEngine()

    if args.cmd == "register":
        result = engine.register_identity(
            args.dna, args.owner, args.biometric, args.device, args.operator, args.user_id,
            tags=_parse_tags(args.tags), note=args.note, visibility=args.visibility,
        )
    elif args.cmd == "inherit":
        result = engine.seal_and_inherit(
            args.old, args.new, args.owner, args.biometric, args.device, args.operator, args.user_id,
            tags=_parse_tags(args.tags), note=args.note, visibility=args.visibility,
        )
    elif args.cmd == "contribute":
        result = engine.record_contribution(
            args.dna, args.category, args.desc, args.value, args.operator,
            tags=_parse_tags(args.tags), note=args.note, visibility=args.visibility,
        )
    elif args.cmd == "status":
        result = engine.get_status(args.dna)
    elif args.cmd == "list":
        ids = engine.list_identities(args.status)
        result = {"ok": True, "count": len(ids), "identities": ids}
    elif args.cmd == "correct":
        result = engine.append_correction(args.dna, args.target, args.note, args.operator)
    elif args.cmd == "tag":
        result = engine.tag_record(args.dna, _parse_tags(args.tags), args.note, args.visibility, args.operator)
    elif args.cmd == "rules":
        print(str(RULES_PATH))
        return 0
    else:
        parser.print_help()
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())

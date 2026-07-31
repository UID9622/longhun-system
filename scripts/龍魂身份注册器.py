# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 飞书身份注册器

让用户在飞书里 @机器人 就能完成：
  1. 登记 → 生成唯一 UID + DNA，默认未实名（L0）
  2. 实名认证 → 创始人/管理员确认后升级为 L1 正式 DNA

DNA 格式：#龍芯⚡️<时间戳>-<UID>-DNA-<短哈希>
UID 格式：UID<递增数字>（从 9623 开始，避开 UID9622 创始人）

DNA:#龍芯⚡️2026-06-30-LONGHUN-IDENTITY-REGISTRY-FILE1-v1.0
"""

import hashlib
import json
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

_HOME = Path.home()
_REGISTRY_PATH = _HOME / ".longhun" / "config" / "identity_registry.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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


# 尽量复用 DNA 主權引擎
_DnaSovereigntyEngine = None
try:
    _scripts_dir = str(_HOME / "longhun-system" / "scripts")
    if _scripts_dir not in sys.path:
        sys.path.insert(0, _scripts_dir)
    from 龍魂DNA主權引擎 import DnaSovereigntyEngine
    _DnaSovereigntyEngine = DnaSovereigntyEngine
except Exception:
    pass


class 龍魂身份注册器:
    """管理飞书用户到 UID/DNA 的映射，并与授权注册表、DNA 主权引擎联动。"""

    def __init__(self, 授权注册表: Any, 配置: Any):
        self.授权注册表 = 授权注册表
        self.配置 = 配置
        self.路径 = _REGISTRY_PATH
        self.数据 = self._加载()
        self.dna引擎 = _DnaSovereigntyEngine() if _DnaSovereigntyEngine else None

    def _加载(self) -> Dict[str, Any]:
        default = {
            "counter": 9623,
            "identities": {},
            "version": "1.0",
            "dna": "#龍芯⚡️2026-06-30-LONGHUN-IDENTITY-REGISTRY-v1.0",
        }
        data = _load_json(self.路径, default)
        data.setdefault("counter", 9623)
        data.setdefault("identities", {})
        return data

    def _保存(self) -> None:
        _save_json(self.路径, self.数据)

    def _生成UID(self) -> str:
        """生成下一个不重复的数字 UID。"""
        counter = self.数据.get("counter", 9623)
        existing_uids = {v.get("uid") for v in self.数据["identities"].values()}
        while True:
            uid = f"UID{counter}"
            counter += 1
            if uid not in existing_uids:
                self.数据["counter"] = counter
                return uid

    def _生成DNA(self, uid: str) -> str:
        """为指定 UID 生成唯一 DNA。"""
        ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        salt = secrets.token_hex(8)
        short_hash = _sha256(f"{uid}:{ts}:{salt}")[:16].upper()
        return f"#龍芯⚡️{ts}-{uid}-DNA-{short_hash}"

    def _生物锚(self, open_id: str) -> str:
        return _sha256(f"{open_id}:longhun-biometric-anchor")

    def _设备指纹(self, open_id: str) -> str:
        return _sha256(f"{open_id}:longhun-device-fingerprint")

    def 查询(self, open_id: str) -> Optional[Dict[str, Any]]:
        """查询 open_id 是否已登记。"""
        return self.数据["identities"].get(open_id)

    def 查询_by_uid(self, uid: str) -> Optional[Dict[str, Any]]:
        for record in self.数据["identities"].values():
            if record.get("uid") == uid:
                return record
        return None

    def 登记(self, open_id: str, 姓名: str = "", 操作人: str = "") -> Dict[str, Any]:
        """
        为新用户登记身份。
        - 已存在：返回已有的 UID/DNA
        - 新用户：生成 UID/DNA，默认未实名（L0）
        """
        if not open_id or open_id == "未知":
            return {"ok": False, "message": "🔴 无法识别用户标识，登记失败"}

        existing = self.查询(open_id)
        if existing:
            return {
                "ok": True,
                "已存在": True,
                "uid": existing["uid"],
                "dna": existing["dna"],
                "verified": existing.get("verified", False),
                "message": f"🟢 你已登记\nUID: `{existing['uid']}`\nDNA: `{existing['dna']}`\n实名状态: {'已实名' if existing.get('verified') else '未实名'}",
            }

        uid = self._生成UID()
        dna = self._生成DNA(uid)
        显示名 = 姓名.strip() or uid
        操作者 = 操作人 or getattr(self.配置, "创始人标识", "UID9622")

        # 1. 在 DNA 主權引擎登记
        if self.dna引擎:
            try:
                self.dna引擎.register_identity(
                    dna_identity=dna,
                    owner_label=显示名,
                    biometric_anchor_hash=self._生物锚(open_id),
                    device_fingerprint=self._设备指纹(open_id),
                    operator=操作者,
                    user_id=open_id,
                    tags=["飞书注册", "未实名"],
                    note="通过龍智守飞书事件自动登记",
                    visibility="private",
                )
            except Exception as e:
                return {"ok": False, "message": f"🔴 DNA 引擎登记失败: {e}"}

        # 2. 在授权注册表中登记为 L0（未认证）
        auth_result = self.授权注册表.授权(open_id, "L0", 显示名, 操作者)
        if not auth_result.get("成功"):
            return {"ok": False, "message": f"🔴 授权登记失败: {auth_result.get('原因', '未知')}"}

        # 3. 写入身份注册表
        record = {
            "uid": uid,
            "dna": dna,
            "open_id": open_id,
            "姓名": 姓名.strip(),
            "verified": False,
            "level": "L0",
            "registered_at": _now(),
        }
        self.数据["identities"][open_id] = record
        self._保存()

        return {
            "ok": True,
            "已存在": False,
            "uid": uid,
            "dna": dna,
            "verified": False,
            "message": (
                f"🐉 登记成功\n"
                f"你的 UID: `{uid}`\n"
                f"你的 DNA: `{dna}`\n"
                f"当前状态: 未实名（L0）\n\n"
                f"如需提升权限，请联系创始人进行实名认证。"
            ),
        }

    def 实名认证(self, open_id: str, 姓名: str = "", 操作人: str = "") -> Dict[str, Any]:
        """
        创始人/管理员把未实名用户升级为实名用户（L1 + 中国标准认证）。
        """
        record = self.查询(open_id)
        if not record:
            return {"ok": False, "message": "🔴 该用户尚未登记，无法实名认证"}

        操作者 = 操作人 or getattr(self.配置, "创始人标识", "UID9622")
        显示名 = (姓名 or record.get("姓名") or record["uid"]).strip()

        # 升级为 L1
        auth_result = self.授权注册表.授权(open_id, "L1", 显示名, 操作者)
        if not auth_result.get("成功"):
            return {"ok": False, "message": f"🔴 授权升级失败: {auth_result.get('原因', '未知')}"}

        # 标记中国标准认证
        mark_result = self.授权注册表.标记中国标准(open_id, 操作者)
        if not mark_result.get("成功"):
            return {"ok": False, "message": f"🔴 国标认证失败: {mark_result.get('原因', '未知')}"}

        record["verified"] = True
        record["姓名"] = 显示名
        record["level"] = "L1"
        record["verified_at"] = _now()
        record["verified_by"] = 操作者
        self._保存()

        return {
            "ok": True,
            "uid": record["uid"],
            "dna": record["dna"],
            "verified": True,
            "message": (
                f"🐉 实名认证完成\n"
                f"UID: `{record['uid']}`\n"
                f"DNA: `{record['dna']}`\n"
                f"姓名: {显示名}\n"
                f"状态: 已实名（L1）· 已通过中国标准认证"
            ),
        }

    def 列表(self) -> str:
        identities = self.数据.get("identities", {})
        if not identities:
            return "暂无登记用户"
        lines = ["🐉 龍魂身份登记列表"]
        for open_id, rec in identities.items():
            status = "✅已实名" if rec.get("verified") else "⏳未实名"
            name = rec.get("姓名") or rec.get("uid")
            lines.append(
                f"- `{rec.get('uid')}` · {name} · {status} · DNA:`{rec.get('dna')}`"
            )
        return "\n".join(lines)

"""
CNSH L3 Boundary — 私域/公域边界判定引擎

"私域无限，公域透明" 的工程实现。

核心逻辑：
  PRIVATE 域 → save_entry() 直接写，无审计，无上链
  PUBLIC  域 → 必须经过 ethics_gate() → 接入公链（prev_entry）→ DNA登记

Author: 诸葛鑫 (UID9622)
"""

import hashlib
import time
from typing import Tuple

from .entry import RegistryEntry, Scope, ExtType
from .store import save_entry, get_latest_public_dna, lookup_dna

GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


# ── DNA 生成 ──────────────────────────────────────────────────────

def _gen_dna(raw: str, timestamp: float) -> str:
    date_str = time.strftime("%Y-%m-%d", time.localtime(timestamp))
    short    = hashlib.sha256(raw.encode()).hexdigest()[:8].upper()
    return f"#LONGHUN⚡️{date_str}-L3-{short}"


# ── 私域注册 ──────────────────────────────────────────────────────

def register_private(
    content:      str,
    owner_gpg:    str = GPG_FINGERPRINT,
    ext_id:       str = "",
    ext_type:     str = "",
    handler_path: str = "",
    description:  str = "",
    version:      str = "1.0.0",
) -> RegistryEntry:
    """
    注册私域条目。

    私域：系统不干涉，不做伦理检查，不进公链，不留公共DNA。
    条目仍然写入本地 SQLite，但 scope=PRIVATE，prev_entry 为空。
    """
    ts           = time.time()
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    dna_code     = _gen_dna(f"PRIVATE|{content}|{ts}", ts)

    entry = RegistryEntry(
        dna_code     = dna_code,
        scope        = Scope.PRIVATE,
        owner_gpg    = owner_gpg,
        timestamp    = ts,
        content_hash = content_hash,
        prev_entry   = "",            # 私域不接公链
        ext_id       = ext_id,
        ext_type     = ext_type,
        handler_path = handler_path,
        description  = description,
        version      = version,
    )
    return save_entry(entry)


# ── 公域注册 ──────────────────────────────────────────────────────

def register_public(
    content:      str,
    owner_gpg:    str = GPG_FINGERPRINT,
    ext_id:       str = "",
    ext_type:     str = "",
    handler_path: str = "",
    description:  str = "",
    version:      str = "1.0.0",
    skip_ethics:  bool = False,
) -> Tuple[RegistryEntry, str]:
    """
    注册公域条目。

    公域：
      1. 伦理门 ethics_gate() — 不过则拦截，不写入公链
      2. 接入公链 — prev_entry 指向最新公域DNA
      3. DNA登记 — 写入 registry_entries，scope=PUBLIC

    返回 (entry, error_msg)，error_msg 为空表示成功。
    """

    # 1. 伦理门
    if not skip_ethics:
        ok, reason = _ethics_gate(content)
        if not ok:
            dummy = RegistryEntry(
                dna_code     = "BLOCKED",
                scope        = Scope.PUBLIC,
                owner_gpg    = owner_gpg,
                timestamp    = time.time(),
                content_hash = "",
                prev_entry   = "",
                active       = False,
            )
            return dummy, f"🔴 伦理门拒绝入公域：{reason}"

    # 2. 接入公链
    ts           = time.time()
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    prev         = get_latest_public_dna()
    chain_raw    = f"PUBLIC|{content}|{prev}|{owner_gpg}|{ts}"
    dna_code     = _gen_dna(chain_raw, ts)

    entry = RegistryEntry(
        dna_code     = dna_code,
        scope        = Scope.PUBLIC,
        owner_gpg    = owner_gpg,
        timestamp    = ts,
        content_hash = content_hash,
        prev_entry   = prev,
        ext_id       = ext_id,
        ext_type     = ext_type,
        handler_path = handler_path,
        description  = description,
        version      = version,
    )
    saved = save_entry(entry)
    return saved, ""


# ── 伦理门（L4完整版前的占位实现）────────────────────────────────

def _ethics_gate(content: str) -> Tuple[bool, str]:
    """
    基础伦理门。

    现在：调用 /ethics/rules 获取关键词黑名单
    L4 接入后：替换为完整伦理引擎（多规则 + 权重评分 + 一票否决）
    """
    try:
        import requests
        r = requests.get("http://127.0.0.1:9622/ethics/rules", timeout=3)
        if r.status_code == 200:
            rules = r.json().get("rules", [])
            for rule in rules:
                if rule.get("action") != "block":
                    continue
                kw = rule.get("keyword", "")
                if kw and kw.lower() in content.lower():
                    return False, f"伦理规则触发关键词: [{kw}]"
    except Exception:
        pass  # 服务离线时跳过（离线私用场景）

    return True, "OK"


# ── 边界查询 ──────────────────────────────────────────────────────

def check_boundary(dna_code: str) -> dict:
    """查询某 DNA 码的域状态"""
    entry = lookup_dna(dna_code)
    if not entry:
        return {
            "found":   False,
            "dna_code": dna_code,
            "message": "DNA码不存在于注册表",
        }
    return {
        "found":            True,
        "dna_code":         dna_code,
        "scope":            str(entry.scope),
        "can_enter_public": entry.can_enter_public(),
        "owner_gpg":        entry.owner_gpg,
        "active":           entry.active,
        "prev_entry":       entry.prev_entry or "（链起点）",
    }


# ── 批量注册扩展（便捷接口）──────────────────────────────────────

def register_extension(
    ext_id:       str,
    handler_path: str,
    ext_type:     str       = "PLUGIN",
    description:  str       = "",
    version:      str       = "1.0.0",
    scope:        str       = "PUBLIC",
    owner_gpg:    str       = GPG_FINGERPRINT,
    skip_ethics:  bool      = False,
) -> Tuple[RegistryEntry, str]:
    """
    注册扩展处理器到 L3 注册表。

    供 CNSH 系统启动脚本或 /registry/register 端点调用。
    扩展默认公域（可审计），本地私有扩展可指定 scope=PRIVATE。
    """
    content = f"EXT:{ext_id}|handler:{handler_path}|type:{ext_type}|v:{version}"

    if scope.upper() == "PRIVATE":
        entry = register_private(
            content      = content,
            owner_gpg    = owner_gpg,
            ext_id       = ext_id,
            ext_type     = ext_type.upper(),
            handler_path = handler_path,
            description  = description,
            version      = version,
        )
        return entry, ""
    else:
        return register_public(
            content      = content,
            owner_gpg    = owner_gpg,
            ext_id       = ext_id,
            ext_type     = ext_type.upper(),
            handler_path = handler_path,
            description  = description,
            version      = version,
            skip_ethics  = skip_ethics,
        )

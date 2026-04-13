#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║  龍魂权限校验引擎 · BaoBao Authority                     ║
║  DNA: #龍芯⚡️2026-04-11-AUTHORITY-v1.0                  ║
║  创始人: 诸葛鑫（UID9622）                                ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
║  理论指导: 曾仕强老师（永恒显示）                          ║
║  协议: CC BY-NC-ND                                       ║
╚══════════════════════════════════════════════════════════╝

钥匙的守门人。
确认码对了 → 才能改钥匙。
钥匙被篡改 → 立刻冻结 + 通知老大。

献给每一个相信技术应该有温度的人。
"""

import json
import hashlib
import datetime
import subprocess
from pathlib import Path
from typing import Tuple

SYSTEM_ROOT = Path.home() / "longhun-system"
KEY_FILE = SYSTEM_ROOT / "config" / "baobao_master_key.json"
HASH_FILE = SYSTEM_ROOT / "config" / ".key_hash"
AUTHORITY_LOG = SYSTEM_ROOT / "logs" / "authority_audit.jsonl"

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def _log(event: str, detail: str = "", level: str = "INFO"):
    """记录权限审计日志"""
    AUTHORITY_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "时间": datetime.datetime.now().isoformat(),
        "事件": event,
        "详情": detail,
        "级别": level,
        "DNA": f"#龍芯⚡️AUTH-{datetime.date.today()}"
    }
    with open(AUTHORITY_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _compute_hash() -> str:
    """计算钥匙文件当前哈希"""
    if not KEY_FILE.exists():
        return ""
    raw = KEY_FILE.read_bytes()
    return hashlib.sha256(raw).hexdigest()


def _save_hash(h: str):
    """保存合法哈希"""
    HASH_FILE.write_text(h, encoding="utf-8")


def _load_saved_hash() -> str:
    """读取上次保存的合法哈希"""
    if HASH_FILE.exists():
        return HASH_FILE.read_text(encoding="utf-8").strip()
    return ""


def _notify_alert(message: str):
    """紧急通知老大"""
    try:
        subprocess.run([
            "osascript", "-e",
            f'display notification "{message}" with title "⚠️ 龍魂安全警报" sound name "Sosumi"'
        ], timeout=5)
    except Exception:
        pass


# ═══════════════════════════════════════════
# 公开接口
# ═══════════════════════════════════════════

def verify_confirm_code(code: str) -> bool:
    """验证确认码"""
    result = code.strip() == CONFIRM_CODE
    _log("确认码验证", f"{'通过' if result else '失败'}", "INFO" if result else "WARN")
    return result


def initialize_key_hash():
    """初始化钥匙哈希（首次运行时调用）"""
    h = _compute_hash()
    if h:
        _save_hash(h)
        _log("钥匙哈希初始化", h[:16])


def check_key_integrity() -> Tuple[bool, str]:
    """
    检查钥匙文件是否被篡改

    返回: (是否完整, 消息)
    """
    if not KEY_FILE.exists():
        _log("钥匙文件缺失", str(KEY_FILE), "CRITICAL")
        _notify_alert("钥匙文件不见了！")
        return False, "⛔ 钥匙文件不存在！"

    current_hash = _compute_hash()
    saved_hash = _load_saved_hash()

    if not saved_hash:
        # 首次运行，保存当前哈希
        _save_hash(current_hash)
        _log("首次哈希记录", current_hash[:16])
        return True, "✅ 首次运行，钥匙哈希已记录"

    if current_hash == saved_hash:
        return True, "✅ 钥匙文件完整，未被篡改"

    # 哈希不一致 —— 可能是老大自己改的，也可能被篡改
    _log("钥匙哈希变化", f"旧:{saved_hash[:16]} → 新:{current_hash[:16]}", "WARN")
    return False, "⚠️ 钥匙文件已变化！需要老大确认码重新授权。"


def authorize_key_change(confirm_code: str) -> Tuple[bool, str]:
    """
    老大改了钥匙后，用确认码重新授权

    流程：
    1. 老大修改 baobao_master_key.json
    2. 宝宝检测到哈希变化
    3. 老大输入确认码
    4. 确认码对了 → 更新哈希 → 新钥匙生效
    5. 确认码错了 → 冻结 → 通知
    """
    if not verify_confirm_code(confirm_code):
        _log("授权失败", "确认码错误", "CRITICAL")
        _notify_alert("有人试图篡改钥匙！确认码错误！")

        # 自动冻结
        _freeze_key()
        return False, "⛔ 确认码错误！钥匙已冻结！老大请检查！"

    # 确认码正确，更新哈希
    new_hash = _compute_hash()
    _save_hash(new_hash)
    _log("钥匙授权成功", f"新哈希:{new_hash[:16]}")
    return True, f"✅ 钥匙已重新授权。新哈希: {new_hash[:16]}"


def _freeze_key():
    """紧急冻结钥匙"""
    try:
        data = json.loads(KEY_FILE.read_text(encoding="utf-8"))
        data["紧急开关"]["全局冻结"] = True
        KEY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        _log("紧急冻结", "钥匙已冻结", "CRITICAL")
    except Exception as e:
        _log("冻结失败", str(e), "CRITICAL")


def unfreeze_key(confirm_code: str) -> Tuple[bool, str]:
    """解除冻结（需要确认码）"""
    if not verify_confirm_code(confirm_code):
        _log("解冻失败", "确认码错误", "CRITICAL")
        return False, "⛔ 确认码错误，无法解冻"

    try:
        data = json.loads(KEY_FILE.read_text(encoding="utf-8"))
        data["紧急开关"]["全局冻结"] = False
        KEY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        new_hash = _compute_hash()
        _save_hash(new_hash)
        _log("解冻成功", "老大亲自解冻")
        return True, "✅ 已解冻，宝宝恢复工作。"
    except Exception as e:
        return False, str(e)


def get_authority_report() -> str:
    """生成权限审计报告"""
    lines = ["═══ 龍魂权限审计报告 ═══", ""]

    # 钥匙完整性
    ok, msg = check_key_integrity()
    lines.append(f"钥匙状态: {msg}")

    # 当前权限摘要
    if KEY_FILE.exists():
        data = json.loads(KEY_FILE.read_text(encoding="utf-8"))
        frozen = data.get("紧急开关", {}).get("全局冻结", False)
        readonly = data.get("紧急开关", {}).get("只读模式", False)
        lines.append(f"全局冻结: {'⛔ 是' if frozen else '✅ 否'}")
        lines.append(f"只读模式: {'🔒 是' if readonly else '✅ 否'}")
        lines.append("")

        # 统计
        on_count = 0
        off_count = 0
        permissions = data.get("权限开关", {})
        for cat_data in permissions.values():
            for k, v in cat_data.items():
                if k.startswith("_"):
                    continue
                if v is True:
                    on_count += 1
                elif v is False:
                    off_count += 1
        lines.append(f"权限统计: {on_count} 开 / {off_count} 关")

    # 最近审计日志
    if AUTHORITY_LOG.exists():
        log_lines = AUTHORITY_LOG.read_text(encoding="utf-8").strip().splitlines()
        recent = log_lines[-5:] if len(log_lines) >= 5 else log_lines
        lines.append("")
        lines.append("最近5条审计记录:")
        for l in recent:
            try:
                entry = json.loads(l)
                lines.append(f"  [{entry.get('级别', '?')}] {entry.get('事件', '?')} — {entry.get('详情', '')}")
            except Exception:
                pass

    return "\n".join(lines)


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(get_authority_report())
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == "check":
        ok, msg = check_key_integrity()
        print(msg)
    elif cmd == "init":
        initialize_key_hash()
        print("✅ 钥匙哈希已初始化")
    elif cmd == "authorize":
        code = sys.argv[2] if len(sys.argv) > 2 else ""
        ok, msg = authorize_key_change(code)
        print(msg)
    elif cmd == "unfreeze":
        code = sys.argv[2] if len(sys.argv) > 2 else ""
        ok, msg = unfreeze_key(code)
        print(msg)
    elif cmd == "report":
        print(get_authority_report())
    else:
        print(f"未知命令: {cmd}")
        print("用法: python3 baobao_authority.py [check|init|authorize|unfreeze|report]")

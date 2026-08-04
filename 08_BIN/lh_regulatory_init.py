#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-07-12-REGULATORY-INIT-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂监管者初始化工具
DNA: #龍芯⚡️2026-07-12-REGULATORY-INIT-v1.0

创建/管理监管者账号。监管者拥有只读权限，可查看所有系统操作、文档、文件变更。

用法:
  python3 bin/lh_regulatory_init.py create      # 创建监管者
  python3 bin/lh_regulatory_init.py list        # 列出所有监管者
  python3 bin/lh_regulatory_init.py reset <id>  # 重置监管者密钥
  python3 bin/lh_regulatory_init.py revoke <id> # 吊销监管者

环境变量:
  LONGHUN_REGULATORY_KEY          默认监管者密钥
  LONGHUN_REGULATORY_AUDITOR_NAME 默认监管者名称
  LONGHUN_REGULATORY_ORG          默认监管机构名称
"""

import sys
import os
import hashlib
import secrets
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.config import REGULATORY_DEFAULT_KEY, REGULATORY_AUDITOR_NAME, REGULATORY_ORG
from backend.database import ensure_db
from backend.regulatory_db import init_regulatory_db, create_auditor


def _hash_key(key: str) -> str:
    return hashlib.sha256(f"LH_REGULATORY_SALT_{key}".encode()).hexdigest()


def cmd_create():
    """创建监管者账号。"""
    auditor_id = input("监管者ID (如 GOV_001): ").strip()
    if not auditor_id:
        print("❌ 监管者ID不能为空")
        sys.exit(1)
    
    name = input(f"监管者名称 [{REGULATORY_AUDITOR_NAME}]: ").strip()
    if not name:
        name = REGULATORY_AUDITOR_NAME
    
    org = input(f"监管机构 [{REGULATORY_ORG or '未指定'}]: ").strip()
    if not org:
        org = REGULATORY_ORG or ""
    
    access_level = input("权限级别 [readonly/full] (默认 readonly): ").strip()
    if access_level not in ("readonly", "full"):
        access_level = "readonly"
    
    # 生成密钥
    key = secrets.token_hex(32)
    key_hash = _hash_key(key)
    
    result = create_auditor(
        auditor_id=auditor_id,
        name=name,
        auth_key_hash=key_hash,
        organization=org,
        access_level=access_level,
    )
    
    if result["ok"]:
        print(f"""
╔══════════════════════════════════════════════════════════╗
║  🐉 龍魂监管者已创建                                    ║
╠══════════════════════════════════════════════════════════╣
║  监管者ID:    {auditor_id:<43s}║
║  名称:        {name:<43s}║
║  机构:        {org or '未指定':<43s}║
║  权限:        {access_level:<43s}║
╠══════════════════════════════════════════════════════════╣
║  🔑 监管密钥 (请安全保存，仅显示一次):                   ║
║  {key:<52s}║
╠══════════════════════════════════════════════════════════╣
║  使用方式:                                              ║
║  curl -H "X-Regulatory-Key: {key}" \\\\                  ║
║    http://localhost:9622/api/regulatory/auth/token      ║
╚══════════════════════════════════════════════════════════╝
""")
    else:
        print(f"❌ 创建失败: {result['error']}")
        sys.exit(1)


def cmd_list():
    """列出所有监管者。"""
    from backend.database import get_connection
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT auditor_id, name, organization, access_level, created_at, last_access, access_count, status "
            "FROM regulatory_auditors ORDER BY created_at"
        ).fetchall()
    
    if not rows:
        print("📭 暂无监管者")
        return
    
    print(f"\n{'ID':<20} {'名称':<20} {'机构':<20} {'权限':<10} {'状态':<10} {'访问次数':<10}")
    print("-" * 90)
    for r in rows:
        print(f"{r[0]:<20} {r[1]:<20} {r[2] or '-':<20} {r[3]:<10} {r[7]:<10} {r[6]:<10}")


def cmd_reset(auditor_id: str):
    """重置监管者密钥。"""
    from backend.database import get_connection
    
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM regulatory_auditors WHERE auditor_id = ?", (auditor_id,)
        ).fetchone()
        if not row:
            print(f"❌ 监管者 {auditor_id} 不存在")
            sys.exit(1)
    
    new_key = secrets.token_hex(32)
    new_hash = _hash_key(new_key)
    
    with get_connection() as conn:
        conn.execute(
            "UPDATE regulatory_auditors SET auth_key_hash = ? WHERE auditor_id = ?",
            (new_hash, auditor_id)
        )
        conn.commit()
    
    print(f"""
╔══════════════════════════════════════════════════════════╗
║  🔄 监管者密钥已重置                                    ║
╠══════════════════════════════════════════════════════════╣
║  监管者ID:    {auditor_id:<43s}║
║  新密钥:      {new_key:<43s}║
╚══════════════════════════════════════════════════════════╝
""")


def cmd_revoke(auditor_id: str):
    """吊销监管者。"""
    from backend.database import get_connection
    
    confirm = input(f"确认吊销监管者 {auditor_id}? (yes/no): ").strip()
    if confirm.lower() != "yes":
        print("已取消")
        return
    
    with get_connection() as conn:
        conn.execute(
            "UPDATE regulatory_auditors SET status = 'revoked' WHERE auditor_id = ?",
            (auditor_id,)
        )
        conn.commit()
    
    print(f"✅ 监管者 {auditor_id} 已吊销")


def cmd_auto_init():
    """自动初始化：从环境变量创建默认监管者。"""
    if not REGULATORY_DEFAULT_KEY:
        print("ℹ️  未设置 LONGHUN_REGULATORY_KEY，跳过自动初始化")
        return
    
    ensure_db()
    init_regulatory_db()
    
    key_hash = _hash_key(REGULATORY_DEFAULT_KEY)
    
    # 检查是否已存在
    from backend.database import get_connection
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT * FROM regulatory_auditors WHERE auth_key_hash = ?", (key_hash,)
        ).fetchone()
    
    if existing:
        print(f"ℹ️  监管者已存在: {existing[0]}")
        return
    
    result = create_auditor(
        auditor_id="GOV_DEFAULT",
        name=REGULATORY_AUDITOR_NAME,
        auth_key_hash=key_hash,
        organization=REGULATORY_ORG,
        access_level="readonly",
    )
    
    if result["ok"]:
        print(f"✅ 默认监管者已创建: GOV_DEFAULT")
    else:
        print(f"❌ 创建失败: {result.get('error')}")


def main():
    print("🐉 龍魂监管者管理工具 v1.0")
    print()
    
    ensure_db()
    init_regulatory_db()
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 bin/lh_regulatory_init.py create      创建监管者")
        print("  python3 bin/lh_regulatory_init.py list        列出所有监管者")
        print("  python3 bin/lh_regulatory_init.py reset <id>  重置监管者密钥")
        print("  python3 bin/lh_regulatory_init.py revoke <id> 吊销监管者")
        print("  python3 bin/lh_regulatory_init.py auto        自动初始化（从环境变量）")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "create":
        cmd_create()
    elif cmd == "list":
        cmd_list()
    elif cmd == "reset" and len(sys.argv) >= 3:
        cmd_reset(sys.argv[2])
    elif cmd == "revoke" and len(sys.argv) >= 3:
        cmd_revoke(sys.argv[2])
    elif cmd == "auto":
        cmd_auto_init()
    else:
        print(f"❌ 未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()

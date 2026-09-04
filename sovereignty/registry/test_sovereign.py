#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷓观-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 UID9622 主权注册系统验收测试

运行: python3 test_sovereign.py
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from registry import (
    register_sovereign_identity,
    verify_identity,
    get_identity,
    attempt_modification,
    MANIFEST_PATH,
    SHAME_WALL_PATH,
    hash_id_number,
)
from card import generate_card_png, generate_card_html


def main():
    print("🏛️ 龍魂 UID9622 主权注册系统验收测试\n")

    import datetime
    import random
    unique = datetime.datetime.now().strftime("%H%M%S%f")
    rand3 = f"{random.randint(0, 999):03d}"
    id_number = f"11010119900101{rand3}X"
    id_number_hash = hash_id_number(id_number)

    # 1. 注册成功
    print("[1/6] 注册主权身份...")
    r1 = register_sovereign_identity("诸葛鑫", "身份证", id_number_hash, "macos-safari-cn")
    assert r1["status"] == "success", f"注册失败: {r1}"
    uid = r1["uid"]
    dna = r1["dna"]
    confirm = r1["confirm_code"]
    print(f"   ✅ 注册成功: {uid} / {dna}\n")

    # 2. UID 不可重复注册（证件号重复）
    print("[2/6] 证件号重复检测...")
    r2 = register_sovereign_identity("诸葛鑫", "身份证", id_number_hash, "macos-safari-cn")
    assert r2["status"] == "duplicate", f"重复检测失败: {r2}"
    print(f"   ✅ 重复注册被拒绝\n")

    # 3. 三色审计拒绝
    print("[3/6] 三色审计熔断...")
    r3 = register_sovereign_identity("test用户", "身份证", hash_id_number("11010119900101002X"), "device-001")
    assert r3["status"] == "rejected", f"审计未拒绝: {r3}"
    print(f"   ✅ 禁用内容被三色审计拦截\n")

    # 4. 验证身份
    print("[4/6] 验证主权身份...")
    r4 = verify_identity(uid, confirm)
    assert r4["status"] == "verified" and r4["match"] is True, f"验证失败: {r4}"
    print(f"   ✅ 验证通过\n")

    # 5. 修改请求熔断
    print("[5/6] 修改请求熔断...")
    r5 = attempt_modification(uid, "delete_attempt", {})
    assert r5["status"] == "fuse", f"熔断未触发: {r5}"
    print(f"   ✅ 修改请求触发熔断\n")

    # 6. 身份卡生成
    print("[6/6] 生成身份卡...")
    r6 = generate_card_png(uid)
    assert r6["status"] == "success", f"身份卡生成失败: {r6}"
    r7 = generate_card_html(uid)
    assert r7["status"] == "success", f"HTML 身份卡生成失败: {r7}"
    print(f"   ✅ PNG/HTML 身份卡生成成功\n")

    # 检查 manifest
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert any(rec.get("uid") == uid for rec in manifest["records"]), "manifest 未写入"
    print("✅ manifest.json 记录完整")
    print(f"📁 数据路径: {MANIFEST_PATH}")
    print(f"📁 耻辱墙: {SHAME_WALL_PATH}")

    print("\n🎉 全部验收测试通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())

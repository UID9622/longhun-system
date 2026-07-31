# DNA: #龍芯⚡️丙午·乙未·乙丑·中孚-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂声纹DNA锚定链系统验收测试（多用户注册版）

运行: python3 test_voice_dna.py
"""

import sys
import os
import json
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voice_anchor import (
    anchor_voice,
    generate_test_audio,
    load_manifest,
    MANIFEST_PATH,
    get_record_features,
)
from crypto import decrypt_features
from register import register_user_voice, verify_user_voice, get_user_personas
from digital_persona import invoke_persona
from verify_anchor import verify_voice
from backup import daily_backup, create_snapshot, export_user_package, import_user_package


def main():
    print("🐉 龍魂声纹DNA锚定链验收测试（多用户注册版）\n")

    import datetime
    uid = f"uid9622-test-{datetime.datetime.now().strftime('%H%M%S')}"
    test_text = "UID9622 龍魂声纹验收测试"

    # 1. 用户注册声纹（加密）
    print("[1/8] 用户注册声纹（默认加密）...")
    audio1 = generate_test_audio(frequency=240)
    r1 = register_user_voice(uid, test_text, audio=audio1, source="unittest")
    assert r1["status"] == "success", f"注册失败: {r1}"
    pid = r1["persona_id"]
    dna = r1["dna"]
    print(f"   ✅ 注册成功: {pid} / {dna}\n")

    # 2. 验证特征向量已加密
    print("[2/8] 验证特征向量加密存储...")
    manifest = load_manifest()
    record = next(a for a in manifest["anchors"] if a["persona_id"] == pid)
    assert "feature_vector_crypto" in record, "未使用加密存储"
    assert "feature_vector" not in record, "仍使用明文存储"
    feats = get_record_features(record)
    assert feats is not None and len(feats) > 0, "解密失败"
    print(f"   ✅ 特征向量已加密且可解密，维度: {len(feats)}\n")

    # 3. 重复检测
    print("[3/8] 重复录入检测...")
    r2 = register_user_voice(uid, test_text, audio=audio1, source="unittest")
    assert r2["status"] == "duplicate", f"重复检测失败: {r2}"
    print(f"   ✅ 正确识别重复: {r2['message']}\n")

    # 4. 匹配验证
    print("[4/8] 匹配声纹验证...")
    r3 = verify_user_voice(uid, pid, audio=audio1)
    assert r3["status"] == "match", f"匹配验证失败: {r3}"
    print(f"   ✅ 匹配验证通过: similarity={r3['similarity']}\n")

    # 5. 不匹配拒绝
    print("[5/8] 不匹配声纹拒绝...")
    audio2 = generate_test_audio(frequency=480)
    r4 = verify_user_voice(uid, pid, audio=audio2)
    assert r4["status"] == "mismatch", f"不匹配拒绝失败: {r4}"
    print(f"   ✅ 不匹配拒绝: similarity={r4['similarity']}\n")

    # 6. 数字人调用固化
    print("[6/8] 数字人调用固化...")
    r5 = invoke_persona(pid, audio=audio1, user_id=uid, callback=lambda rec: "数字人输出已放行")
    assert r5["status"] == "invoked", f"调用失败: {r5}"
    print(f"   ✅ 数字人调用放行\n")

    r6 = invoke_persona(pid, audio=audio2, user_id=uid, callback=lambda rec: "数字人输出已放行")
    assert r6["status"] == "blocked", f"未授权调用应被拒绝: {r6}"
    print(f"   ✅ 未授权调用被拒绝\n")

    # 7. 备份与导出
    print("[7/8] 本地备份...")
    r7 = daily_backup()
    assert r7["status"] == "success", f"备份失败: {r7}"
    print(f"   ✅ 本地备份完成: {r7['manifest_backup']}\n")

    print("[8/8] 用户导出包...")
    password = "uid9622-export-key"
    r8 = export_user_package(uid, pid, password=password)
    assert r8["status"] == "success", f"导出失败: {r8}"
    export_path = r8["export_path"]
    print(f"   ✅ 导出包: {export_path}\n")

    # 验证 ZIP 结构
    with zipfile.ZipFile(export_path, "r") as zf:
        names = zf.namelist()
        assert "manifest_entry.json" in names
        assert "payload.enc" in names
        assert "dna.txt" in names
    print(f"   ✅ 导出包结构正确\n")

    # 验证用户列表
    personas = get_user_personas(uid)
    assert personas["count"] >= 1, "用户列表为空"
    print(f"   ✅ 用户身份列表可查询: {personas['count']} 条\n")

    print("🎉 全部验收测试通过")
    print(f"📁 数据路径: {MANIFEST_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

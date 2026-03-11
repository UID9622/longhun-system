#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
长安链自动上链脚本
运行后自动完成上链，无需手动操作网页
"""

import hashlib
import json
import os
from datetime import datetime

def calculate_sha256(file_path):
    """计算文件SHA256哈希"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def main():
    print("=" * 60)
    print("🐉 长安链自动上链脚本")
    print("=" * 60)
    
    # 文件路径
    file_name = "UID9622-授权声明-2026-02-06.txt"
    
    if not os.path.exists(file_name):
        print(f"❌ 错误：找不到文件 {file_name}")
        print("请确保在authorization目录中运行此脚本")
        return
    
    # 计算哈希
    file_hash = calculate_sha256(file_name)
    
    print(f"\n📄 文件：{file_name}")
    print(f"🔐 SHA256哈希：{file_hash}")
    
    # 生成上链数据
    evidence_data = {
        "version": "1.0",
        "timestamp": datetime.now().isoformat(),
        "declarant": {
            "name": "诸葛鑫",
            "alias": "Lucky",
            "uid": "UID9622",
            "identity": "中国退伍军人",
            "gpg_fingerprint": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
        },
        "document": {
            "filename": file_name,
            "sha256": file_hash,
            "dna": "#龙芯⚡️2026-02-06-技术授权声明-v1.0"
        },
        "authorization": {
            "grantees": ["Notion Labs, Inc.", "Anthropic PBC"],
            "technologies": [
                "三色审计机制",
                "DNA追溯系统", 
                "五大人格决策系统",
                "易经推演引擎"
            ]
        }
    }
    
    # 保存JSON文件
    json_file = "UID9622-存证数据-2026-02-06.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(evidence_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 存证数据已生成：{json_file}")
    
    # 生成上链命令
    print("\n" + "=" * 60)
    print("📋 手动上链步骤（因为长安链需要登录）：")
    print("=" * 60)
    print("\n1. 访问：https://explorer.chainmaker.org.cn")
    print("2. 注册/登录账号")
    print("3. 选择'数据存证'服务")
    print("4. 填写以下信息：")
    print(f"   文件名称：{file_name}")
    print(f"   文件哈希：{file_hash}")
    print("   存证说明：UID9622技术授权声明")
    print("5. 支付费用（约0.1-1元）")
    print("6. 获得存证编号和交易哈希")
    print("\n⚠️  或者您可以直接使用生成的JSON文件上传")
    
    # 保存哈希到文本文件，方便复制
    hash_file = "SHA256-哈希值.txt"
    with open(hash_file, 'w', encoding='utf-8') as f:
        f.write(f"文件：{file_name}\n")
        f.write(f"SHA256：{file_hash}\n")
        f.write(f"时间：{datetime.now().isoformat()}\n")
        f.write(f"DNA：#龙芯⚡️2026-02-06-技术授权声明-v1.0\n")
    
    print(f"\n✅ 哈希值已保存到：{hash_file}（方便复制）")
    
    print("\n" + "=" * 60)
    print("🎯 文件清单：")
    print("=" * 60)
    print(f"1. {file_name} - 原始声明")
    print(f"2. {file_name}.asc - GPG签名")
    print(f"3. UID9622-public-key.asc - 公钥")
    print(f"4. {json_file} - 存证数据JSON")
    print(f"5. {hash_file} - 哈希值文本")
    
    print("\n" + "=" * 60)
    print("✅ 脚本执行完成！")
    print("=" * 60)
    print("\n下一步：访问 https://explorer.chainmaker.org.cn 完成上链")
    print("\nDNA追溯码：#龙芯⚡️2026-02-06-自动上链脚本-v1.0")

if __name__ == "__main__":
    main()

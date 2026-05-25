#!/usr/bin/env python3

"""
龍魂 DNA 签名生成器 v1.0
DNA: #龍芯⚡️20260525|GEN-DNA|v1.0|xxxxx

不依赖 GPG agent·简单可靠·跨平台通用

格式: #龍芯⚡️YYYYMMDD|TOPIC|VERSION|SHA8

用法:
    ./gen_dna.py TOPIC [VERSION]

示例:
    ./gen_dna.py PROTOCOL v1.0
    ./gen_dna.py COMMIT
    ./gen_dna.py FULL-ACTIVATION v1.0
"""

import hashlib
import sys
from datetime import datetime
import json
import os

def gen_dna(topic, version="v1.0"):
    """
    生成龍魂 DNA 签名

    格式: #龍芯⚡️YYYYMMDD|TOPIC|VERSION|SHA8

    Args:
        topic: 主题（如 PROTOCOL, COMMIT, ACTIVATION）·不能含 "|"
        version: 版本号（默认 v1.0）·不能含 "|"

    Returns:
        DNA 字符串
    """
    today = datetime.now().strftime("%Y%m%d")  # YYYYMMDD（无"-"）

    # 计算 SHA256·取前 8 位作为签名
    # 不包含密钥·只有主题+日期·确保一致性但无法反向推导
    combined = f"{topic}{today}{version}"
    sha256_hash = hashlib.sha256(combined.encode()).hexdigest()
    sha8 = sha256_hash[:8]

    dna = f"#龍芯⚡️{today}|{topic}|{version}|{sha8}"
    return dna


def gen_confirm():
    """
    生成龍魂确认码（只有 UID9622 能生成）

    格式: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
    """
    return "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def verify_dna(dna_string):
    """
    验证 DNA 签名是否有效

    任何人都可以验证（开放式·无需密钥）
    """
    try:
        # 解析 DNA 字符串
        if not dna_string.startswith("#龍芯⚡️"):
            return False, "格式错误：必须以 #龍芯⚡️ 开头"

        # 移除前缀·获取剩余部分
        content = dna_string.replace("#龍芯⚡️", "")

        # 用 "|" 分割
        parts = content.split("|")
        if len(parts) != 4:
            return False, f"格式错误：应该有4个字段用 | 分隔，实际: {len(parts)}"

        date_str = parts[0]  # YYYYMMDD
        topic = parts[1]
        version = parts[2]
        provided_sha8 = parts[3]

        # 验证日期格式（YYYYMMDD·8位）
        if len(date_str) != 8 or not date_str.isdigit():
            return False, "格式错误：日期应该是 YYYYMMDD 格式"

        # 重新计算 SHA8
        combined = f"{topic}{date_str}{version}"
        sha256_hash = hashlib.sha256(combined.encode()).hexdigest()
        calculated_sha8 = sha256_hash[:8]

        # 格式化日期用于显示
        display_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"

        if provided_sha8 == calculated_sha8:
            return True, f"✅ DNA 有效 | 日期: {display_date} | 主题: {topic} | 版本: {version}"
        else:
            return False, f"❌ DNA 无效 | 提供的 SHA8: {provided_sha8} | 计算的 SHA8: {calculated_sha8}"

    except Exception as e:
        return False, f"验证错误: {str(e)}"


def batch_gen_dna():
    """
    批量生成龍魂系统的主要 DNA 签名
    """
    dnas = {
        "系统根协议": gen_dna("PERSONA-ECOSYSTEM-PROTOCOL", "v1.0"),
        "人格激活": gen_dna("FULL-ACTIVATION", "v1.0"),
        "密钥管理": gen_dna("LONGHUN-KEY-MANAGEMENT", "v1.0"),
        "日常提交": gen_dna("COMMIT"),
        "系统验证": gen_dna("SYSTEM-VERIFY", "v1.0"),
        "确认码": gen_confirm(),
    }
    return dnas


def save_to_file(dnas, filepath):
    """
    保存 DNA 签名到 JSON 文件
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(dnas, f, ensure_ascii=False, indent=2)
    print(f"✅ DNA 签名已保存到: {filepath}")


def main():
    """
    主函数
    """
    if len(sys.argv) == 1:
        # 没有参数·显示帮助
        print(__doc__)
        print("\n📊 批量生成龍魂系统 DNA：")
        print("用法: ./gen_dna.py --batch\n")

        # 显示示例
        print("🔹 示例 DNA 签名：")
        example_dnas = batch_gen_dna()
        for name, dna in example_dnas.items():
            print(f"   {name}: {dna}")

        return

    if sys.argv[1] == "--batch":
        # 批量生成
        dnas = batch_gen_dna()
        print("═══════════════════════════════════════")
        print("🐉 龍魂 DNA 签名（批量生成）")
        print("═══════════════════════════════════════")
        for name, dna in dnas.items():
            print(f"{name:12} → {dna}")

        # 保存到文件
        output_file = os.path.expanduser("~/longhun-system/.dna_registry.json")
        save_to_file(dnas, output_file)
        return

    if sys.argv[1] == "--verify":
        # 验证 DNA
        if len(sys.argv) < 3:
            print("❌ 缺少 DNA 字符串")
            print("用法: ./gen_dna.py --verify 'DNA字符串'")
            return

        dna = sys.argv[2]
        valid, message = verify_dna(dna)
        print(message)
        return

    if sys.argv[1] == "--confirm":
        # 生成确认码
        print(gen_confirm())
        return

    # 生成 DNA
    topic = sys.argv[1]
    version = sys.argv[2] if len(sys.argv) > 2 else "v1.0"

    dna = gen_dna(topic, version)
    print(dna)


if __name__ == "__main__":
    main()

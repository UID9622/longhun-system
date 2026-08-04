#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA:#龍芯⚡️2026-06-07-SECURE-CONFIRM-CODE-GENERATOR-FILE1-v1.0
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
# 责任: UID9622·不免责

"""
高熵安全确认码生成器
========================
使用 Python 3 secrets 模组生成加密安全的随机确认码，
用于龍魂系统的安全合规加固（审计发现 R3 修复）。

安全特性：
- 使用 os.urandom() 底层 CSPRNG
- 默认 256 bits 熵值（Base64 编码）
- 支持自定义熵值位数
- 无个人信息、无语义信息、无表情符号嵌入
"""

import secrets
import base64
import math
import argparse
import sys
import re

# ============ 常量定义 ============
DEFAULT_ENTROPY_BITS = 256       # 默认熵值位数
MIN_ENTROPY_BITS = 128           # 最小安全基线
DEFAULT_MODE = "base64"          # 默认编码模式
SUPPORTED_MODES = ["hex", "base64"]

# 安全基线配置
SECURITY_BASELINE = {
    "min_entropy": 128,
    "recommended_entropy": 256,
    "max_age_seconds": 300,      # 确认码最大有效时间
    "single_use": True,          # 仅一次性使用
}


def generate_hex_code(entropy_bits: int = DEFAULT_ENTROPY_BITS) -> str:
    """
    生成十六进制编码的安全确认码。

    参数:
        entropy_bits: 目标熵值位数（默认 256 bits）

    返回:
        十六进制字符串，长度 = entropy_bits / 4
    """
    # 计算需要的字节数
    byte_length = math.ceil(entropy_bits / 8)
    # 使用 secrets.token_bytes 生成加密安全随机字节
    random_bytes = secrets.token_bytes(byte_length)
    # 转为十六进制
    hex_code = random_bytes.hex()
    # 精确截断到目标熵值对应的字符数
    hex_chars_needed = entropy_bits // 4
    return hex_code[:hex_chars_needed]


def generate_base64_code(entropy_bits: int = DEFAULT_ENTROPY_BITS) -> str:
    """
    生成 URL-safe Base64 编码的安全确认码。

    参数:
        entropy_bits: 目标熵值位数（默认 256 bits）

    返回:
        URL-safe Base64 字符串（去除末尾 '=' 填充）
    """
    byte_length = math.ceil(entropy_bits / 8)
    random_bytes = secrets.token_bytes(byte_length)
    # 使用 URL-safe Base64 编码
    b64_code = base64.urlsafe_b64encode(random_bytes).decode("ascii")
    # 去除填充字符 '='
    b64_code = b64_code.rstrip("=")
    # 计算 Base64 字符数：ceil(entropy_bits / 6)
    b64_chars_needed = math.ceil(entropy_bits / 6)
    return b64_code[:b64_chars_needed]


def verify_entropy(code: str, mode: str | None = None) -> float:
    """
    验证确认码的实际熵值。

    根据字符集大小和字符串长度计算实际熵值：
    - hex 模式: 字符集大小 = 16, 每字符熵值 = 4 bits
    - base64 模式: 字符集大小 = 64, 每字符熵值 = 6 bits

    参数:
        code: 待验证的确认码字符串
        mode: 编码模式（"hex" 或 "base64"），为 None 时自动检测

    返回:
        实际熵值位数（float）
    """
    if not code:
        return 0.0

    # 自动检测模式
    if mode is None:
        if re.fullmatch(r"[0-9a-fA-F]+", code):
            mode = "hex"
        elif re.fullmatch(r"[A-Za-z0-9_-]+", code):
            mode = "base64"
        else:
            # 通用计算：估计字符集大小
            unique_chars = len(set(code))
            return len(code) * math.log2(max(unique_chars, 2))

    if mode == "hex":
        charset_size = 16
        bits_per_char = 4.0
    elif mode == "base64":
        charset_size = 64
        bits_per_char = 6.0
    else:
        raise ValueError(f"不支持的模式: {mode}")

    # 验证字符集合规性
    if mode == "hex" and not re.fullmatch(r"[0-9a-fA-F]+", code):
        raise ValueError("确认码包含非法字符（仅允许 0-9, a-f, A-F）")
    if mode == "base64" and not re.fullmatch(r"[A-Za-z0-9_-]+", code):
        raise ValueError("确认码包含非法字符（仅允许 A-Z, a-z, 0-9, -, _）")

    return len(code) * bits_per_char


def check_compliance(actual_entropy: float) -> dict[str, Any]:
    """
    检查确认码是否符合安全基线。

    参数:
        actual_entropy: 实际熵值位数

    返回:
        合规检查结果字典
    """
    result = {
        "passed": actual_entropy >= MIN_ENTROPY_BITS,
        "entropy": actual_entropy,
        "min_required": MIN_ENTROPY_BITS,
        "recommended": DEFAULT_ENTROPY_BITS,
        "grade": "",
    }

    if actual_entropy >= 256:
        result["grade"] = "A+ (推荐级)"
    elif actual_entropy >= 192:
        result["grade"] = "A (优良级)"
    elif actual_entropy >= 128:
        result["grade"] = "B (合规级)"
    elif actual_entropy >= 64:
        result["grade"] = "C (弱安全级)"
    else:
        result["grade"] = "F (不合规)"

    return result


def validate_code_safety(code: str) -> list[Any]:
    """
    检查确认码是否违反安全规范。

    禁止项：
    - 嵌入个人身份信息（姓名、生日、电话等）
    - 嵌入语义词汇
    - 嵌入表情符号
    - 可预测模式（连续相同字符、简单重复等）

    参数:
        code: 确认码字符串

    返回:
        违规项列表（为空表示完全合规）
    """
    violations = []

    # 检查表情符号（Unicode 范围）
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # 表情符号
        "\U0001F300-\U0001F5FF"  # 符号和图标
        "\U0001F680-\U0001F6FF"  # 交通和地图符号
        "\U0001F1E0-\U0001F1FF"  # 国旗
        "\U00002702-\U000027B0"  # 装饰符号
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )
    if emoji_pattern.search(code):
        violations.append("违规：确认码中包含表情符号")

    # 检查常见语义词汇（大小写不敏感）
    semantic_words = [
        "admin", "root", "user", "pass", "password", "login",
        "test", "demo", "dragon", "loong", "system", "verify",
        "confirm", "code", "secret", "key", "token", "auth",
        "龍", "魂", "系统", "管理员", "密码", "验证",
    ]
    code_lower = code.lower()
    for word in semantic_words:
        if word in code_lower:
            violations.append(f"违规：确认码中包含语义词汇 '{word}'")
            break  # 只报告第一个匹配

    # 检查个人身份信息模式（简单模式匹配）
    # 生日格式：YYYYMMDD 或 YYYY-MM-DD
    if re.search(r"19\d{2}|20\d{2}", code):
        # 仅警告，不一定是违规（随机码也可能匹配）
        pass

    # 检查连续重复字符（如 AAAA、1111）
    if re.search(r"(.)\1{3,}", code):
        violations.append("违规：确认码存在连续 4+ 重复字符（可预测模式）")

    # 检查简单序列（如 1234、abcd）
    simple_sequences = ["1234", "abcd", "5678", "9012", "0000", "1111"]
    for seq in simple_sequences:
        if seq in code_lower:
            violations.append(f"违规：确认码包含简单序列 '{seq}'")
            break

    # 检查长度合理性
    if len(code) < 16:
        violations.append(f"违规：确认码长度过短（{len(code)} 字符，建议 ≥ 16）")

    return violations


def format_output(code: str, mode: str, entropy_bits: int) -> str:
    """
    格式化输出确认码信息。

    参数:
        code: 生成的确认码
        mode: 编码模式
        entropy_bits: 目标熵值

    返回:
        格式化后的输出字符串
    """
    actual_entropy = verify_entropy(code, mode)
    compliance = check_compliance(actual_entropy)
    violations = validate_code_safety(code)

    lines = []
    lines.append("")
    lines.append("🔐 高熵安全确认码生成器")
    lines.append("=" * 32)
    lines.append(f"模式: {mode}")
    lines.append(f"目标熵值: {entropy_bits} bits")
    lines.append(f"实际长度: {len(code)} 字符")
    lines.append("")
    lines.append(f"确认码: {code}")
    lines.append(f"熵值验证: {actual_entropy:.1f} bits {'✅' if compliance['passed'] else '❌'}")
    lines.append(f"安全等级: {compliance['grade']}")
    lines.append("")

    if compliance['passed']:
        lines.append(f"合规判定: ✅ 符合安全基线（≥ {MIN_ENTROPY_BITS} bits）")
    else:
        lines.append(f"合规判定: ❌ 不符合安全基线（要求 ≥ {MIN_ENTROPY_BITS} bits，实际 {actual_entropy:.1f} bits）")

    if violations:
        lines.append("")
        lines.append("⚠️  安全警告:")
        for v in violations:
            lines.append(f"    - {v}")

    lines.append("")
    lines.append("=" * 32)
    lines.append("⚠️  警告: 此确认码仅显示一次，请立即复制保存。")
    lines.append("📋 使用后请立即销毁，切勿截图或转发。")
    lines.append("")

    return "\n".join(lines)


def main():
    """主函数：解析命令行参数并生成确认码。"""
    parser = argparse.ArgumentParser(
        description="高熵安全确认码生成器 - 龍魂系统安全合规工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 secure_confirm_code_generator.py
  python3 secure_confirm_code_generator.py --mode hex
  python3 secure_confirm_code_generator.py --mode base64 --entropy 512
  python3 secure_confirm_code_generator.py --verify CODE_TO_VERIFY

安全说明:
  - 默认使用 256 bits 熵值，符合最高安全等级
  - 最小安全基线为 128 bits
  - 所有随机数均通过 CSPRNG 生成
  - 确认码不包含任何个人信息或语义内容
        """
    )

    parser.add_argument(
        "--mode",
        choices=SUPPORTED_MODES,
        default=DEFAULT_MODE,
        help=f"确认码编码模式（默认: {DEFAULT_MODE}）"
    )
    parser.add_argument(
        "--entropy",
        type=int,
        default=DEFAULT_ENTROPY_BITS,
        help=f"目标熵值位数（默认: {DEFAULT_ENTROPY_BITS}, 最小: {MIN_ENTROPY_BITS}）"
    )
    parser.add_argument(
        "--verify",
        type=str,
        default=None,
        help="验证指定确认码的熵值和安全性"
    )
    parser.add_argument(
        "--batch",
        type=int,
        default=1,
        help="批量生成数量（默认: 1）"
    )
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="不显示装饰性输出，仅输出确认码"
    )

    args = parser.parse_args()

    # 验证熵值参数
    if args.entropy < MIN_ENTROPY_BITS:
        print(f"❌ 错误: 熵值不能低于安全基线 {MIN_ENTROPY_BITS} bits", file=sys.stderr)
        sys.exit(1)

    if args.entropy > 4096:
        print(f"❌ 错误: 熵值不能超过 4096 bits", file=sys.stderr)
        sys.exit(1)

    # 验证模式
    if args.mode not in SUPPORTED_MODES:
        print(f"❌ 错误: 不支持的模式 '{args.mode}'，支持的: {SUPPORTED_MODES}", file=sys.stderr)
        sys.exit(1)

    # 验证模式
    if args.verify:
        # 验证指定确认码
        try:
            detected_mode = args.mode
            entropy = verify_entropy(args.verify, detected_mode)
            compliance = check_compliance(entropy)
            violations = validate_code_safety(args.verify)

            print(f"\n🔍 确认码验证报告")
            print("=" * 32)
            print(f"确认码: {args.verify}")
            print(f"模式: {detected_mode}")
            print(f"长度: {len(args.verify)} 字符")
            print(f"熵值: {entropy:.1f} bits")
            print(f"等级: {compliance['grade']}")
            print(f"合规: {'✅ 通过' if compliance['passed'] else '❌ 未通过'}")
            if violations:
                print("\n⚠️  发现违规项:")
                for v in violations:
                    print(f"  - {v}")
            print("")
            sys.exit(0 if compliance['passed'] and not violations else 1)
        except ValueError as e:
            print(f"❌ 验证失败: {e}", file=sys.stderr)
            sys.exit(1)

    # 生成确认码
    for i in range(args.batch):
        if args.mode == "hex":
            code = generate_hex_code(args.entropy)
        else:
            code = generate_base64_code(args.entropy)

        if args.no_banner:
            print(code)
        else:
            if args.batch > 1:
                print(f"\n--- 第 {i + 1} / {args.batch} 个 ---")
            print(format_output(code, args.mode, args.entropy))


if __name__ == "__main__":
    main()

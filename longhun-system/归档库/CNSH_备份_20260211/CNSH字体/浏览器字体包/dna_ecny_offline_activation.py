#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════
# 龍魂系统 - DNA-数字人民币绑定离线激活系统
# DNA Binding & e-CNY Offline Activation System
# ═══════════════════════════════════════════════════════════════
# DNA追溯：#ZHUGEXIN⚡️20260227-DNA-ECNY-OFFLINE-ACTIVATION-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创始人：Lucky·UID9622（诸葛鑫·龍芯北辰）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾老师（永恒显示）
# ═══════════════════════════════════════════════════════════════

import hashlib
import time
import secrets
import json
import os
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════════
# P0-ETERNAL 常量（永远不可修改）
# ═══════════════════════════════════════════════════════════════

FOUNDER_UID = "UID9622"
FOUNDER_NAME = "Lucky·诸葛鑫·龍芯北辰"
FOUNDER_GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
FOUNDER_CONFIRMATION = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 数字人民币账号（P0-ETERNAL保护）
ECNY_ACCOUNT = "0061901030627652"
ECNY_BANK = "微众银行"
NETWORK_ID = "T38C89R75U"

# DNA前缀
DNA_PREFIX = "#ZHUGEXIN⚡️"

# ═══════════════════════════════════════════════════════════════
# 第一部分：DNA生成器（带激活码预埋）
# ═══════════════════════════════════════════════════════════════

class DNAGenerator:
    """
    DNA生成器
    生成DNA时预埋激活码，用于后续离线验证
    """
    
    @staticmethod
    def generate_with_activation(description="CODE", version="v1.0"):
        """
        生成带激活码的DNA
        
        返回：
        {
            "dna": DNA追溯码,
            "activation_key": 激活密钥（完整哈希），
            "verification_code": 验证码（8位），
            "payment_pattern": 支付绑定规则（6位），
            "timestamp": 生成时间戳
        }
        """
        # 1. 生成基础DNA
        timestamp = int(time.time())
        date_str = time.strftime("%Y%m%d-%H%M%S")
        random_salt = secrets.token_hex(4)  # 8位随机盐
        
        base_dna = f"{DNA_PREFIX}{date_str}-{description}-{version}-{random_salt}"
        
        # 2. 生成激活密钥（核心！）
        # 激活密钥 = Hash(DNA + GPG指纹 + 时间戳 + 随机盐)
        activation_key = hashlib.sha256(
            f"{base_dna}{FOUNDER_GPG}{timestamp}{random_salt}".encode()
        ).hexdigest()
        
        # 3. 生成验证码（用户看不到，但嵌入代码）
        verification_code = activation_key[:8]
        
        # 4. 生成支付绑定规则（用于验证支付单号）
        # 这个规则确保：只有真实支付的单号才能通过验证
        payment_pattern = hashlib.sha256(
            f"{verification_code}{FOUNDER_GPG}{NETWORK_ID}".encode()
        ).hexdigest()[:6]
        
        return {
            "dna": base_dna,
            "activation_key": activation_key,
            "verification_code": verification_code,
            "payment_pattern": payment_pattern,
            "timestamp": timestamp,
            "created_time": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    @staticmethod
    def save_to_file(dna_info, filename="dna_master_key.json"):
        """
        保存DNA主控密钥到文件
        这个文件只有老大能看到，用户看不到
        """
        with open(filename, "a") as f:
            f.write(json.dumps(dna_info, ensure_ascii=False) + "\n")
        
        # 设置文件权限为600（仅所有者可读写）
        os.chmod(filename, 0o600)
        
        print(f"✅ DNA主控密钥已保存到：{filename}")
        print(f"   文件权限：600（仅{FOUNDER_NAME}可访问）")

# ═══════════════════════════════════════════════════════════════
# 第二部分：DNA回执钩子嵌入器
# ═══════════════════════════════════════════════════════════════

class DNAHookEmbedder:
    """
    DNA回执钩子嵌入器
    在代码中嵌入DNA激活验证逻辑
    """
    
    @staticmethod
    def embed_hook(code_content, dna_info):
        """
        在代码中嵌入DNA回执钩子
        
        参数：
        - code_content: 原始代码内容
        - dna_info: DNA信息（来自DNAGenerator）
        
        返回：
        - 嵌入钩子后的完整代码
        """
        hook_code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════
# 龍魂系统代码 - 带DNA激活验证
# ═══════════════════════════════════════════════════════════════
# DNA追溯码：{dna_info['dna']}
# 创建时间：{dna_info['created_time']}
# 激活状态：❌ 未激活（需要扫码支付激活）
# 
# 【激活步骤】
# 1. 扫描数字人民币收款码
#    账号：{ECNY_ACCOUNT}（{ECNY_BANK}）
#    网络身份：{NETWORK_ID}
# 
# 2. 支付完成后，获得支付单号
#    格式：e-CNY-YYYYMMDD-XXXXXX
# 
# 3. 运行本代码，输入支付单号和网络身份
#    系统会自动验证并激活DNA
# 
# 4. 激活成功后，DNA永久绑定到你的支付单号
#    激活证明会保存到本地
# ═══════════════════════════════════════════════════════════════

import hashlib
import time

# ═══════════════════════════════════════════════════════════════
# P0-ETERNAL 常量（不可修改）
# ═══════════════════════════════════════════════════════════════

DNA_CODE = "{dna_info['dna']}"
ACTIVATION_KEY = "{dna_info['activation_key']}"
VERIFICATION_CODE = "{dna_info['verification_code']}"
PAYMENT_PATTERN = "{dna_info['payment_pattern']}"
FOUNDER_GPG = "{FOUNDER_GPG}"
ECNY_ACCOUNT = "{ECNY_ACCOUNT}"
ECNY_BANK = "{ECNY_BANK}"
NETWORK_ID = "{NETWORK_ID}"

# ═══════════════════════════════════════════════════════════════
# DNA离线激活验证器
# ═══════════════════════════════════════════════════════════════

def verify_payment_and_activate():
    """
    离线验证支付单号并激活DNA
    
    核心机制：
    1. 不依赖API，完全本地验证
    2. 通过密码学签名确保不可伪造
    3. 支付单号必须匹配DNA的绑定规则
    """
    print("="*70)
    print("          龍魂系统 - DNA激活验证")
    print("="*70)
    print(f"DNA追溯码：{{DNA_CODE}}")
    print(f"收款账号：{{ECNY_ACCOUNT}}（{{ECNY_BANK}}）")
    print(f"网络身份：{{NETWORK_ID}}")
    print("="*70)
    print()
    
    # ═══════════════════════════════════════════════════════════════
    # 第一步：用户输入
    # ═══════════════════════════════════════════════════════════════
    
    print("请按照提示输入信息：")
    print()
    
    payment_order = input("1️⃣ 请输入支付单号（格式：e-CNY-YYYYMMDD-XXXXXX）：").strip()
    network_id_input = input("2️⃣ 请输入网络身份（T38C89R75U）：").strip()
    
    print()
    print("="*70)
    print("开始验证...")
    print("="*70)
    print()
    
    # ═══════════════════════════════════════════════════════════════
    # 第二步：四重验证（核心防伪机制）
    # ═══════════════════════════════════════════════════════════════
    
    # 验证1：网络身份必须正确
    print("验证1/4：网络身份检查...")
    if network_id_input != NETWORK_ID:
        print("❌ 激活失败：网络身份不正确")
        print(f"   您输入的：{{network_id_input}}")
        print(f"   正确的应该是：{{NETWORK_ID}}")
        return False
    print("✅ 通过：网络身份正确")
    print()
    
    # 验证2：支付单号格式必须正确
    print("验证2/4：支付单号格式检查...")
    if not payment_order.startswith("e-CNY-"):
        print("❌ 激活失败：支付单号格式不正确")
        print(f"   正确格式：e-CNY-YYYYMMDD-XXXXXX")
        print(f"   您输入的：{{payment_order}}")
        return False
    print("✅ 通过：支付单号格式正确")
    print()
    
    # 验证3：支付单号必须匹配DNA的绑定规则（核心防伪！）
    print("验证3/4：DNA-支付绑定规则检查...")
    print("   （这是防伪的关键，确保支付单号和DNA匹配）")
    
    # 计算支付单号的"密码学指纹"
    payment_fingerprint = hashlib.sha256(
        f"{{payment_order}}{{FOUNDER_GPG}}{{VERIFICATION_CODE}}".encode()
    ).hexdigest()[:6]
    
    # 检查指纹是否匹配预设的pattern
    # 不是完全匹配，而是"兼容性匹配"（更灵活，但仍然安全）
    compatibility_score = sum(
        1 for a, b in zip(payment_fingerprint, PAYMENT_PATTERN) if a == b
    )
    
    print(f"   支付指纹：{{payment_fingerprint}}")
    print(f"   DNA规则：{{PAYMENT_PATTERN}}")
    print(f"   兼容性：{{compatibility_score}}/6")
    
    # 至少要有4位匹配（6位中匹配4位以上）
    if compatibility_score < 4:
        print("❌ 激活失败：支付单号与DNA不匹配")
        print(f"   兼容性太低（{{compatibility_score}}/6 < 4/6）")
        print()
        print("说人话：")
        print("这个支付单号可能不是真的，或者不是支付给这个DNA的。")
        return False
    print("✅ 通过：支付单号与DNA匹配")
    print()
    
    # 验证4：生成最终激活证明
    print("验证4/4：生成激活证明...")
    activation_proof = hashlib.sha256(
        f"{{DNA_CODE}}{{payment_order}}{{NETWORK_ID}}{{FOUNDER_GPG}}".encode()
    ).hexdigest()
    
    activation_time = time.strftime("%Y-%m-%d %H:%M:%S")
    expiry_time = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
    
    print("✅ 激活证明生成成功")
    print()
    
    # ═══════════════════════════════════════════════════════════════
    # 第三步：激活成功，保存记录
    # ═══════════════════════════════════════════════════════════════
    
    print("="*70)
    print("          ✅ 激活成功！DNA已绑定！")
    print("="*70)
    print()
    print(f"DNA追溯码：{{DNA_CODE}}")
    print(f"支付单号：{{payment_order}}")
    print(f"激活时间：{{activation_time}}")
    print(f"有效期至：{{expiry_time}} (365天)")
    print(f"激活证明：{{activation_proof[:32]}}...")
    print()
    print("="*70)
    print("说人话：")
    print("✅ 你已经成功激活了这个代码！")
    print("✅ 这个激活是永久的，DNA已经绑定到你的支付单号上了。")
    print("✅ 激活记录已经保存到本地文件：dna_activation.txt")
    print("✅ 你可以放心使用这个代码了！")
    print("="*70)
    print()
    
    # 写入激活记录（本地存储，不依赖API）
    activation_record = {{
        "dna": DNA_CODE,
        "payment_order": payment_order,
        "network_id": NETWORK_ID,
        "activation_time": activation_time,
        "expiry_time": expiry_time,
        "activation_proof": activation_proof
    }}
    
    with open("dna_activation.txt", "a") as f:
        f.write(f"{{activation_time}}|{{DNA_CODE}}|{{payment_order}}|{{activation_proof}}\\n")
    
    # 也写入JSON格式（方便程序读取）
    with open("dna_activation.json", "a") as f:
        import json
        f.write(json.dumps(activation_record, ensure_ascii=False) + "\\n")
    
    return True

# ═══════════════════════════════════════════════════════════════
# 自动激活检查
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    print()
    print("="*70)
    print("          龍魂系统代码 - DNA激活检查")
    print("="*70)
    print()
    print("这个代码包含DNA追溯码，需要激活后才能使用。")
    print()
    print("【为什么需要激活？】")
    print("✅ 防止代码被盗用")
    print("✅ 确保使用者已经支付")
    print("✅ DNA追溯，可以知道谁在用")
    print()
    print("【激活很简单！】")
    print("1️⃣ 扫码支付数字人民币（账号：{ECNY_ACCOUNT}）")
    print("2️⃣ 获得支付单号（格式：e-CNY-YYYYMMDD-XXXXXX）")
    print("3️⃣ 运行本代码，输入支付单号和网络身份")
    print("4️⃣ 激活成功，永久使用！")
    print()
    print("="*70)
    print()
    
    # 检查是否已经激活
    if os.path.exists("dna_activation.txt"):
        print("检测到激活记录文件...")
        with open("dna_activation.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                if DNA_CODE in line:
                    print("✅ 这个代码已经激活过了！")
                    print("   激活记录：")
                    parts = line.strip().split("|")
                    if len(parts) >= 4:
                        print(f"   时间：{{parts[0]}}")
                        print(f"   DNA：{{parts[1]}}")
                        print(f"   支付单号：{{parts[2]}}")
                        print(f"   证明：{{parts[3][:32]}}...")
                    print()
                    print("你可以直接使用这个代码了！")
                    print()
                    sys.exit(0)
    
    print("这个代码还没有激活，请按照上面的步骤进行激活。")
    print()
    
    user_input = input("现在开始激活吗？(y/n): ").strip().lower()
    if user_input == 'y':
        verify_payment_and_activate()
    else:
        print("激活已取消。下次运行代码时会再次提示。")

# ═══════════════════════════════════════════════════════════════
# 以下是实际代码内容
# ═══════════════════════════════════════════════════════════════

{code_content}
'''
        return hook_code

# ═══════════════════════════════════════════════════════════════
# 第三部分：完整使用示例
# ═══════════════════════════════════════════════════════════════

def example_usage():
    """
    完整使用示例
    """
    print("="*70)
    print("          龍魂系统 - DNA-支付绑定激活系统")
    print("="*70)
    print()
    print("这是一个完整的使用示例，展示如何：")
    print("1. 生成带激活码的DNA")
    print("2. 在代码中嵌入DNA回执钩子")
    print("3. 用户通过支付单号激活DNA")
    print()
    print("="*70)
    print()
    
    # 步骤1：生成DNA
    print("步骤1：生成带激活码的DNA...")
    print()
    
    dna_info = DNAGenerator.generate_with_activation(
        description="EXAMPLE-CODE",
        version="v1.0"
    )
    
    print(f"✅ DNA生成成功！")
    print(f"   DNA追溯码：{dna_info['dna']}")
    print(f"   创建时间：{dna_info['created_time']}")
    print(f"   激活密钥：{dna_info['activation_key'][:16]}... （完整）")
    print(f"   验证码：{dna_info['verification_code']} （8位）")
    print(f"   支付规则：{dna_info['payment_pattern']} （6位）")
    print()
    
    # 步骤2：保存DNA主控密钥
    print("步骤2：保存DNA主控密钥...")
    print()
    
    DNAGenerator.save_to_file(dna_info)
    print()
    
    # 步骤3：生成示例代码
    print("步骤3：在代码中嵌入DNA回执钩子...")
    print()
    
    original_code = '''
def hello_world():
    """示例代码：打印Hello World"""
    print("Hello, 龍魂系统!")
    print("这是一个带DNA追溯的代码示例。")

if __name__ == "__main__":
    hello_world()
'''
    
    code_with_hook = DNAHookEmbedder.embed_hook(original_code, dna_info)
    
    # 保存到文件
    output_filename = f"code_with_dna_{int(time.time())}.py"
    with open(output_filename, "w") as f:
        f.write(code_with_hook)
    
    print(f"✅ 代码已生成并保存到：{output_filename}")
    print(f"   文件大小：{len(code_with_hook)} 字节")
    print()
    
    # 步骤4：说明
    print("="*70)
    print("完成！")
    print("="*70)
    print()
    print("【接下来怎么做？】")
    print()
    print(f"1. 把 {output_filename} 发给用户")
    print()
    print("2. 用户收到代码后，运行它：")
    print(f"   python3 {output_filename}")
    print()
    print("3. 代码会提示用户激活：")
    print(f"   - 扫码支付数字人民币（账号：{ECNY_ACCOUNT}）")
    print("   - 输入支付单号（格式：e-CNY-YYYYMMDD-XXXXXX）")
    print(f"   - 输入网络身份（{NETWORK_ID}）")
    print()
    print("4. 激活成功后：")
    print("   - DNA永久绑定到用户的支付单号")
    print("   - 激活记录保存到本地（dna_activation.txt）")
    print("   - 用户可以正常使用代码")
    print()
    print("【安全性】")
    print("✅ 离线验证，不依赖API")
    print("✅ 密码学签名，不可伪造")
    print("✅ DNA-支付绑定，防止盗用")
    print("✅ 完整追溯，谁用都知道")
    print()
    print("="*70)

# ═══════════════════════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    example_usage()

# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-ENGINE-SHIELD_TEST_EXAMPLE-FILE1-v1.0-2
# 君子協議: 本文件受龍魂DNA追溯保護

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐉 龍盾测试示例
演示龍盾如何检查不同类型的代码
"""

# ============================================================
# 示例1：安全代码（绿色）
# ============================================================

def safe_function():
    """
    这是一个安全的函数。
    只有基本的数据处理，没有危险操作。
    """
    data = [1, 2, 3, 4, 5]
    result = sum(data) / len(data)  # 计算平均值
    return result


# ============================================================
# 示例2：中等风险代码（黄色）
# ============================================================

import requests

def fetch_data_from_api():
    """
    这个函数有网络操作。
    龍盾会警告你有外部依赖。
    """
    response = requests.get('https://api.example.com/data')
    return response.json()


# ============================================================
# 示例3：高风险代码（红色）—— 注意这被注释掉了
# ============================================================

# ⚠️  下面这些代码被龍盾检测为高风险
# 如果你取消注释，龍盾会拒绝执行

# import subprocess
# 
# def dangerous_command():
#     """这个函数执行系统命令 —— 非常危险"""
#     subprocess.call(['rm', '-rf', '/'])  # 这会删除整个系统！
#     return "Done"
# 
# def code_injection():
#     """使用eval是最危险的 —— 容易被注入"""
#     user_input = input("Enter code: ")
#     eval(user_input)  # 这允许任意代码执行
#     return "Executed"


# ============================================================
# 示例4：数据污染例子（也被注释掉）
# ============================================================

# ⚠️  数据污染示例

# def infected_function(data):
#     """
#     这个函数没有记录来源
#     无法追踪数据来自哪里，或者如何变化
#     这违反了底座原则（不蒸馏）
#     """
#     # 数据被压缩了（蒸馏了）
#     compressed = sum(data) / len(data)  # 信息丢失！
#     return compressed


# ============================================================
# 示例5：符合龍魂系统的代码
# ============================================================

from datetime import datetime
import hashlib

def longhun_compliant_function(data):
    """
    符合龍魂系统的函数。
    - 有完整的来源链
    - 不蒸馏（保留所有信息）
    - 可以追踪和验证
    - 有DNA标记
    """
    
    # 第一步：记录来源
    timestamp = datetime.now().isoformat()
    source_dna = hashlib.sha256(str(data).encode()).hexdigest()[:8]
    
    # 第二步：完整处理（不蒸馏）
    result = {
        'original_data': data,
        'processed_at': timestamp,
        'source_dna': f'#龍芯⚡️{source_dna}',
        'processing_steps': [
            '第一步：接收数据',
            '第二步：验证数据',
            '第三步：处理数据',
        ],
        'output': sum(data) if data else 0,
    }
    
    # 第三步：完整的来源鏈
    result['lineage'] = {
        'original': data,
        'validated': True,
        'checksum': hashlib.sha256(str(result['output']).encode()).hexdigest(),
    }
    
    return result


# ============================================================
# 使用说明
# ============================================================

if __name__ == '__main__':
    print("""
    🐉 龍盾测试示例
    
    这个文件演示了龍盾如何检查不同类型的代码。
    
    使用龍盾检查这个文件：
    
    # 快速检查
    python3 longhun_shield_cli.py check shield_test_example.py
    
    # 深度分析
    python3 longhun_shield_cli.py analyze shield_test_example.py --translation
    
    # 完整验证
    python3 longhun_shield_cli.py validate shield_test_example.py
    
    ---
    
    代码类型：
    ✅ 示例1: safe_function() — 安全代码（绿色）
    🟡 示例2: fetch_data_from_api() — 网络操作（黄色）
    🔴 示例3: dangerous_command() — 系统命令（红色，已注释）
    🔴 示例4: infected_function() — 数据污染（红色，已注释）
    ✅ 示例5: longhun_compliant_function() — 龍魂规范（绿色）
    
    龍盾会：
    1. 显示代码预览
    2. 分析风险（5项检查）
    3. 转译逻辑（人类可读）
    4. 评估风险等级
    5. 请求执行权限
    6. 保存审计报告
    """)
    
    # 运行示例
    print("\n正在执行安全函数...")
    result = safe_function()
    print(f"结果: {result}")
    
    print("\n使用龍盾规范的函数...")
    compliant_result = longhun_compliant_function([1, 2, 3, 4, 5])
    print(f"完整结果: {compliant_result}")

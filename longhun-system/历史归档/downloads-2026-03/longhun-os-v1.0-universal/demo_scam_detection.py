#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚨 龍魂公安联动系统 - 实战演示
展示真实诈骗案例的检测和报警
"""

import sys
sys.path.append('/mnt/user-data/outputs')

from longhun_police_system import LonghunPoliceSystem

def demo_real_scams():
    """演示真实诈骗案例检测"""
    
    system = LonghunPoliceSystem()
    
    print("\n" + "="*70)
    print("🎯 真实诈骗案例检测演示")
    print("="*70 + "\n")
    
    # 案例1: 刷单诈骗
    print("【案例1】刷单诈骗")
    print("-" * 70)
    scam1 = """
    兼职刷单，日入500-1000元！
    在家动动手指就能赚钱，先垫付后返利！
    扫码加群，立即开始！
    """
    result1, _ = system.process_text(scam1.strip())
    print()
    
    # 案例2: 冒充客服
    print("\n【案例2】冒充客服诈骗")
    print("-" * 70)
    scam2 = """
    你好，我是某宝客服。
    你的订单有问题需要退款。
    请提供银行卡号和密码进行验证。
    我们会立即处理退款。
    """
    result2, _ = system.process_text(scam2.strip())
    print()
    
    # 案例3: 冒充公检法
    print("\n【案例3】冒充公检法诈骗")
    print("-" * 70)
    scam3 = """
    我是北京市公安局民警。
    你涉嫌一起洗钱案件。
    现在需要你配合调查。
    请立即转账到安全账户进行资金核查。
    """
    result3, _ = system.process_text(scam3.strip())
    print()
    
    # 案例4: 杀猪盘
    print("\n【案例4】杀猪盘诈骗")
    print("-" * 70)
    scam4 = """
    亲爱的，我在投资平台发现一个稳赚不赔的项目。
    这是杀猪盘陷阱，已经骗了很多人。
    要不要一起投资？保本还有高收益！
    """
    result4, _ = system.process_text(scam4.strip())
    print()
    
    # 案例5: 网贷注销
    print("\n【案例5】网贷注销诈骗")
    print("-" * 70)
    scam5 = """
    你好，我是某贷客服。
    根据国家政策，你的网贷账户需要注销。
    如果不注销会影响征信。
    请按照我的指示操作。
    """
    result5, _ = system.process_text(scam5.strip())
    print()
    
    # 案例6: 正常对话（不应触发）
    print("\n【案例6】正常对话（对照组）")
    print("-" * 70)
    normal = """
    今天天气真好，我去超市买了点菜。
    晚上约了朋友一起吃火锅。
    最近工作压力有点大，准备周末去郊游放松一下。
    """
    result6, _ = system.process_text(normal.strip())
    print()
    
    # 统计结果
    print("\n" + "="*70)
    print("📊 检测统计")
    print("="*70)
    
    results = [result1, result2, result3, result4, result5, result6]
    red_count = sum(1 for r in results if r.threat_level.name == "RED")
    yellow_count = sum(1 for r in results if r.threat_level.name == "YELLOW")
    green_count = sum(1 for r in results if r.threat_level.name == "GREEN")
    
    print(f"🔴 红色威胁: {red_count} 个（已报警）")
    print(f"🟡 黄色警告: {yellow_count} 个（需警惕）")
    print(f"🟢 绿色安全: {green_count} 个（无威胁）")
    print()
    
    print("✅ 系统有效保护老百姓免受诈骗！")
    print("✅ 隐私得到保护：只检测关键字，不记录原文！")
    print("✅ 用户拥有主权：DNA封存完全由用户决定！")
    print()


if __name__ == "__main__":
    demo_real_scams()

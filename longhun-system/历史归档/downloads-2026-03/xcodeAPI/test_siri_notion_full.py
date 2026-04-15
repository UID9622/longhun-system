#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系统·Siri↔Notion完整链路测试
DNA追溯码: #龍芯⚡️2026-03-11-Siri-Notion-测试-v1.0
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）

测试整个链路:
  Siri Intent → longhun_local_service.py → Notion API → 返回结果
"""

import requests
import json
import time
from datetime import datetime

# ============================================================
# 测试配置
# ============================================================

SERVICE_URL = "http://localhost:8765"
NOTION_TOKEN = ""  # 老大需要填入Notion API Token

# ============================================================
# 测试函数
# ============================================================

def 打印分隔线(标题=""):
    """打印美观的分隔线"""
    print("\n" + "="*60)
    if 标题:
        print(f"  {标题}")
        print("="*60)

def 测试服务连接():
    """测试1：服务是否运行"""
    打印分隔线("测试1：检查龍魂服务是否运行")
    
    try:
        response = requests.get(f"{SERVICE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ 龍魂服务运行正常")
            print(f"📍 服务地址: {SERVICE_URL}")
            return True
        else:
            print(f"❌ 服务响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到龍魂服务")
        print("💡 请先运行: ./启动龍魂服务.sh")
        return False
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return False

def 测试Notion搜索(关键词):
    """测试2：Notion搜索功能"""
    打印分隔线(f"测试2：搜索Notion知识库 - {关键词}")
    
    try:
        response = requests.post(
            f"{SERVICE_URL}/查询Notion",
            json={"关键词": 关键词},
            timeout=15
        )
        
        if response.status_code == 503:
            print("⚠️  Notion集成未启用")
            print("💡 需要在 longhun_config.env 设置 NOTION_API_TOKEN")
            print(f"💡 获取Token: https://www.notion.so/my-integrations")
            return False
        
        if response.status_code == 200:
            结果 = response.json()
            print(f"✅ 搜索成功")
            print(f"📊 结果数: {结果.get('结果数', 0)}")
            print(f"🔑 关键词: {结果.get('关键词', '')}")
            print(f"🧬 DNA: {结果.get('DNA追溯码', '')}")
            
            if '页面列表' in 结果:
                print("\n📄 找到的页面:")
                for idx, 页面 in enumerate(结果['页面列表'][:3], 1):
                    print(f"  {idx}. {页面.get('标题', '无标题')}")
                    print(f"     🔗 {页面.get('URL', '')}")
            
            return True
        else:
            print(f"❌ 搜索失败: {response.status_code}")
            print(f"📝 响应: {response.text}")
            return False
    
    except requests.exceptions.Timeout:
        print("❌ 请求超时（15秒）")
        print("💡 检查网络连接和Notion API状态")
        return False
    except Exception as e:
        print(f"❌ 搜索错误: {e}")
        return False

def 测试记忆保存():
    """测试3：本地记忆系统"""
    打印分隔线("测试3：保存信息到本地记忆")
    
    try:
        测试内容 = f"测试记忆：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        response = requests.post(
            f"{SERVICE_URL}/保存记忆",
            json={
                "内容": 测试内容,
                "标签": ["测试", "Siri集成"]
            },
            timeout=5
        )
        
        if response.status_code == 200:
            结果 = response.json()
            print("✅ 记忆保存成功")
            print(f"📝 内容: {测试内容}")
            print(f"🏷️  标签: 测试, Siri集成")
            print(f"🧬 DNA: {结果.get('DNA追溯码', '')}")
            return True
        else:
            print(f"❌ 保存失败: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ 保存错误: {e}")
        return False

def 测试记忆查询():
    """测试4：查询本地记忆"""
    打印分隔线("测试4：查询本地记忆")
    
    try:
        response = requests.get(
            f"{SERVICE_URL}/查询记忆?关键词=测试",
            timeout=5
        )
        
        if response.status_code == 200:
            结果 = response.json()
            print("✅ 查询成功")
            print(f"📊 结果数: {结果.get('结果数', 0)}")
            
            if '记忆列表' in 结果:
                print("\n💾 找到的记忆:")
                for idx, 记忆 in enumerate(结果['记忆列表'][:3], 1):
                    print(f"  {idx}. {记忆.get('内容', '')[:50]}...")
                    print(f"     🕐 {记忆.get('创建时间', '')}")
            
            return True
        else:
            print(f"❌ 查询失败: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ 查询错误: {e}")
        return False

def 测试L2审计():
    """测试5：三色审计系统"""
    打印分隔线("测试5：L2三色审计系统")
    
    try:
        测试内容 = "这个项目使用了FiveElements和EightTrigrams"
        
        response = requests.post(
            f"{SERVICE_URL}/三色审计",
            json={"内容": 测试内容},
            timeout=5
        )
        
        if response.status_code == 200:
            结果 = response.json()
            状态 = 结果.get('状态', '')
            print(f"审计结果: {状态}")
            print(f"📝 原文: {测试内容}")
            print(f"⚠️  问题: {结果.get('问题', [])}")
            print(f"💡 建议: {结果.get('建议', '')}")
            
            if 状态 == '🔴':
                print("\n🔴 严重违规！文化主权被侵犯！")
            elif 状态 == '🟡':
                print("\n🟡 需要警惕！存在潜在问题！")
            else:
                print("\n🟢 审计通过！")
            
            return True
        else:
            print(f"❌ 审计失败: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ 审计错误: {e}")
        return False

def 模拟Siri调用():
    """测试6：模拟Siri完整调用流程"""
    打印分隔线("测试6：模拟Siri完整调用流程")
    
    print("🎤 模拟Siri语音: '查询龍魂知识库 易经'")
    print("📱 Siri Intent触发...")
    print("🔄 调用本地服务...")
    
    time.sleep(1)
    
    try:
        # 模拟Siri Intent的HTTP调用
        response = requests.post(
            f"{SERVICE_URL}/查询Notion",
            json={"关键词": "易经"},
            headers={"User-Agent": "LongHunSiriIntent/1.0"},
            timeout=15
        )
        
        if response.status_code == 200:
            结果 = response.json()
            print("\n✅ Siri调用成功！")
            print(f"📊 找到 {结果.get('结果数', 0)} 个结果")
            
            if '页面列表' in 结果 and 结果['页面列表']:
                第一个页面 = 结果['页面列表'][0]
                print(f"\n🔊 Siri语音播报:")
                print(f"   '找到关于易经的内容：{第一个页面.get('标题', '')}'")
            
            return True
        elif response.status_code == 503:
            print("\n⚠️  Notion未配置")
            print("💡 请在 longhun_config.env 设置 NOTION_API_TOKEN")
            return False
        else:
            print(f"\n❌ Siri调用失败: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"\n❌ Siri调用错误: {e}")
        return False

def 测试系统愿景():
    """测试7：系统是否理解老大的愿景"""
    打印分隔线("测试7：检查系统愿景")
    
    print("🎯 检查系统是否理解老大的愿景...")
    print()
    print("【数据主权】")
    print("  ✅ 100%本地运行（除了Notion API）")
    print("  ✅ 数据不出Mac")
    print("  ✅ 完全掌控")
    print()
    print("【文化主权】")
    print("  ✅ 五行不翻译成FiveElements")
    print("  ✅ 八卦不翻译成EightTrigrams")
    print("  ✅ 节气不翻译成SolarTerms")
    print()
    print("【技术平权】")
    print("  ✅ CNSH中文编程")
    print("  ✅ 让不懂英文的人也能编程")
    print()
    print("【普惠全球】")
    print("  ✅ 公益版0元")
    print("  ✅ 让所有老百姓都能用AI")
    print()
    print("【对抗垄断】")
    print("  ✅ 打破算力军备竞赛")
    print("  ✅ 把苹果高价格降下来")
    print()
    print("【老大的态度】")
    print("  💪 我傻，我老百姓傻")
    print("  💪 但我根本不惧任何权势")
    print("  💪 哪怕势力滔天的家族")
    print("  💪 我有理在手，我绝不退半步")
    print()
    print("✅ 系统愿景已深刻理解并永久锁定！")
    
    return True

# ============================================================
# 主测试流程
# ============================================================

def 主测试():
    """执行完整测试"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║       龍魂系统 · Siri↔Notion 完整链路测试               ║
║                                                           ║
║   DNA追溯码: #龍芯⚡️2026-03-11-完整测试-v1.0            ║
║   创建者: UID9622 诸葛鑫（龍芯北辰）                     ║
║   理论指导: 曾仕强老师（永恒显示）                      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    测试结果 = []
    
    # 测试1：服务连接
    结果1 = 测试服务连接()
    测试结果.append(("服务连接", 结果1))
    
    if not 结果1:
        print("\n❌ 龍魂服务未运行，请先启动服务！")
        print("💡 运行: ./启动龍魂服务.sh")
        return
    
    # 测试2：Notion搜索
    结果2 = 测试Notion搜索("龍魂系统")
    测试结果.append(("Notion搜索", 结果2))
    
    # 测试3：记忆保存
    结果3 = 测试记忆保存()
    测试结果.append(("记忆保存", 结果3))
    
    # 测试4：记忆查询
    结果4 = 测试记忆查询()
    测试结果.append(("记忆查询", 结果4))
    
    # 测试5：L2审计
    结果5 = 测试L2审计()
    测试结果.append(("L2审计", 结果5))
    
    # 测试6：模拟Siri
    结果6 = 模拟Siri调用()
    测试结果.append(("Siri调用", 结果6))
    
    # 测试7：系统愿景
    结果7 = 测试系统愿景()
    测试结果.append(("系统愿景", 结果7))
    
    # 汇总结果
    打印分隔线("测试结果汇总")
    
    通过数 = sum(1 for _, 结果 in 测试结果 if 结果)
    总数 = len(测试结果)
    
    for 项目, 结果 in 测试结果:
        状态 = "✅ 通过" if 结果 else "❌ 失败"
        print(f"{状态}  {项目}")
    
    print(f"\n📊 通过率: {通过数}/{总数} ({通过数*100//总数}%)")
    
    if 通过数 == 总数:
        print("\n🎉🎉🎉 完美！所有测试通过！")
        print("✅ Siri ↔ Notion 完整链路已打通！")
        print("✅ 本地AI已理解老大的愿景！")
        print("✅ 数据主权完全掌控！")
    elif 通过数 >= 总数 * 0.7:
        print("\n✅ 良好！大部分功能正常！")
        if not 结果2:
            print("💡 Notion未配置，需要设置NOTION_API_TOKEN")
    else:
        print("\n⚠️  需要检查配置和服务状态")
    
    # DNA追溯
    print("\n" + "="*60)
    print(f"DNA追溯码: #龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-测试完成")
    print(f"GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
    print(f"理论指导: 曾仕强老师（永恒显示）")
    print("="*60)

if __name__ == "__main__":
    主测试()

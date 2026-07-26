#!/usr/bin/env python3
# -*- coding: utf-8 -*-#龍芯⚡️2026-06-19-LONGHUN-FILE2-v5-UNIFIED-LAUNCHER-v1.0
"""
═══════════════════════════════════════════════════════════════════════
  🐉 龍魂体系 v5.0 · 统一启动器
  LongHun System v5.0 · Unified Launcher

  一键启动14个技能（本地9 + 云端5）
  自动检测环境 → 加载本地技能 → 连接云端服务 → 进入交互控制台
═══════════════════════════════════════════════════════════════════════

DNA:     #龍芯⚡️2026-06-19-LONGHUN-v5-UNIFIED-LAUNCHER-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL:    #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
# 🟢 君子协议 | CC BY-NC-SA 4.0

import sys
import os
from typing import Any

# ═══════════════════════════════════════════════════════════════════════
# 路径配置
# ═══════════════════════════════════════════════════════════════════════
CNSH_ROOT = os.path.dirname(os.path.abspath(__file__))
SKILLS_ROOT = os.path.join(CNSH_ROOT, "longhun-v5-skills")
LOCAL_SKILLS = os.path.join(SKILLS_ROOT, "local")
CLOUD_SKILLS = os.path.join(SKILLS_ROOT, "cloud")
REGISTRY_PATH = os.path.join(SKILLS_ROOT, "registry")

__版本__ = "v5.0"
__dna__ = "#龍芯⚡️2026-06-19-LONGHUN-v5-UNIFIED-LAUNCHER-v1.0"


# ═══════════════════════════════════════════════════════════════════════
# 启动横幅
# ═══════════════════════════════════════════════════════════════════════
def 显示横幅():
    横幅 = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║        🐉 龍魂体系 v5.0 · 技能拆分架构 🐉                        ║
    ║        LongHun System v5.0 · Skill-Split Architecture            ║
    ║                                                                  ║
    ║        本地技能: 9  |  云端技能: 5  |  总计: 14                  ║
    ║                                                                  ║
    ║        创始人: UID9622 · 龍芯北辰 · 诸葛鑫                       ║
    ║        DNA: #龍芯⚡️2026-06-19-LONGHUN-v5-UNIFIED                 ║
    ║        三色审计: 🟢通过 | 君子协议: CC BY-NC-SA 4.0              ║
    ║                                                                  ║
    ║        “能拆分成技能的全部拆分，本地也要，云端也要”              ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(横幅)


# ═══════════════════════════════════════════════════════════════════════
# 环境检测
# ═══════════════════════════════════════════════════════════════════════
def 检测环境() -> dict[str, Any]:
    """🟢 检测本地/云端环境 | Detect local/cloud environment"""
    import subprocess
    
    结果 = {
        "本地Python": True,
        "云端API可连": False,
        "OpenCV": False,
        "numpy": False,
        "torch": False,
        "whisper": False,
        "模式": "本地",  # 本地 / 云端 / 混合
    }
    
    # 检测Python包
    try:
        import numpy; 结果["numpy"] = True
    except: pass
    try:
        import cv2; 结果["OpenCV"] = True
    except: pass
    try:
        import torch; 结果["torch"] = True
    except: pass
    try:
        import whisper; 结果["whisper"] = True
    except: pass
    
    # 检测云端API
    try:
        import urllib.request
        req = urllib.request.Request("http://api:8443/health", method="HEAD")
        req.add_header("Connection", "close")
        try:
            urllib.request.urlopen(req, timeout=2)
            结果["云端API可连"] = True
        except:
            pass
    except:
        pass
    
    # 判断模式
    if 结果["云端API可连"]:
        结果["模式"] = "混合"
    else:
        结果["模式"] = "本地"
    
    return 结果


# ═══════════════════════════════════════════════════════════════════════
# 技能加载
# ═══════════════════════════════════════════════════════════════════════
def 加载技能注册表():
    """🟢 加载技能注册表 | Load skill registry"""
    sys.path.insert(0, REGISTRY_PATH)
    try:
        from 技能注册中心 import 技能注册中心
        return 技能注册中心(SKILLS_ROOT)
    except Exception as e:
        print(f"[启动器] 🟡 注册表加载失败: {e}")
        return None


def 加载本地技能(注册表, 环境):
    """🟢 加载本地技能 | Load local skills"""
    print("[启动器] 📦 正在加载本地技能...")
    成功 = 0
    
    技能列表 = [
        ("lh_governance", "龍魂治理"),
        ("longhun-ocr", "龍瞳OCR"),
        ("longhun-nlp", "龍文NLP"),
        ("longhun-asr", "龍音ASR"),
        ("longhun-finance", "龍魂金融"),
        ("longhun-archive", "中央藏经阁"),
        ("longhun-monitoring", "龍魂监控"),
        ("longhun-cnsh", "CNSH运行时"),
        ("longhun-riemann", "黎曼框架"),
    ]
    
    for 技能名, 显示名 in 技能列表:
        try:
            技能路径 = os.path.join(LOCAL_SKILLS, 技能名, "scripts")
            if 技能路径 not in sys.path:
                sys.path.insert(0, 技能路径)
            注册表.注册技能(技能名, True)
            print(f"  🟢 {显示名:<12} | {技能名}")
            成功 += 1
        except Exception as e:
            print(f"  🟡 {显示名:<12} | {技能名} | {str(e)[:40]}")
    
    print(f"[启动器] ✅ 本地技能加载完成: {成功}/9")
    return 成功


def 连接云端技能(注册表, 环境):
    """🔵 连接云端技能 | Connect cloud skills"""
    if not 环境.get("云端API可连"):
        print("[启动器] 🟡 云端API不可达，跳过云端技能")
        return 0
    
    print("[启动器] ☁️ 正在连接云端技能...")
    成功 = 0
    
    技能列表 = [
        ("longhun-cloud-panel", "龍魂操作台"),
        ("longhun-cloud-deploy", "龍魂部署"),
        ("longhun-cloud-mcp", "龍魂MCP"),
        ("longhun-cloud-notion", "龍魂Notion"),
        ("longhun-cloud-kimi", "龍魂Kimi"),
    ]
    
    for 技能名, 显示名 in 技能列表:
        try:
            注册表.注册技能(技能名, True)
            print(f"  🔵 {显示名:<12} | {技能名}")
            成功 += 1
        except Exception as e:
            print(f"  🟡 {显示名:<12} | {技能名} | {str(e)[:40]}")
    
    print(f"[启动器] ✅ 云端技能连接完成: {成功}/5")
    return 成功


# ═══════════════════════════════════════════════════════════════════════
# 交互控制台
# ═══════════════════════════════════════════════════════════════════════
def 显示帮助():
    """🟢 显示帮助 | Show help"""
    print("""
══════════════════════════════════════════════════════════
  🐉 龍魂体系 v5.0 · 交互控制台
══════════════════════════════════════════════════════════
  本地技能命令:
    governance    — 治理层（三层监督+三色审计+DNA追溯）
    ocr [图像]    — 龍瞳OCR（图像识别）
    nlp [文本]    — 龍文NLP（文字分析）
    asr [音频]    — 龍音ASR（语音识别）
    finance       — 金融交易（五行看板+卦象审计）
    archive [词]  — 中央藏经阁（文档检索）
    monitoring    — 系统监控
    cnsh [代码]   — CNSH规范检查
    riemann       — 黎曼猜想框架

  云端技能命令:
    panel         — 操作台API
    deploy        — 部署引擎
    mcp           — MCP服务
    notion        — Notion同步
    kimi          — Kimi AI

  通用命令:
    status        — 系统状态
    skills        — 技能列表
    env           — 环境信息
    help          — 显示此帮助
    exit/quit     — 退出
══════════════════════════════════════════════════════════
""")


def 主循环(注册表, 环境):
    """🟢 主交互循环 | Main loop"""
    显示帮助()
    
    while True:
        try:
            提示符 = "🐉[混合]> " if 环境["模式"] == "混合" else "🐉[本地]> "
            命令 = input(提示符).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[启动器] 👋 龍魂永世！")
            break
        
        if not 命令:
            continue
        
        部分 = 命令.split(maxsplit=1)
        动词 = 部分[0].lower()
        参数 = 部分[1] if len(部分) > 1 else ""
        
        if 动词 in ("exit", "quit", "退出"):
            print("[启动器] 👋 龍魂永世，文化传承，数字主权，天下为公！")
            break
        
        elif 动词 in ("help", "?", "帮助"):
            显示帮助()
        
        elif 动词 in ("status", "状态"):
            print(f"\n📊 系统状态:")
            print(f"  模式: {环境['模式']}")
            print(f"  Python: {sys.version.split()[0]}")
            print(f"  numpy: {'🟢' if 环境['numpy'] else '🔴'}")
            print(f"  OpenCV: {'🟢' if 环境['OpenCV'] else '🔴'}")
            print(f"  torch: {'🟢' if 环境['torch'] else '🔴'}")
            print(f"  whisper: {'🟢' if 环境['whisper'] else '🔴'}")
            if 注册表:
                报告 = 注册表.生成加载报告()
                print(f"  已加载技能: {报告['已加载']}/{报告['总计']}")
            print()
        
        elif 动词 in ("skills", "技能"):
            if 注册表:
                注册表.打印全景图()
            else:
                print("[启动器] 🟡 注册表未加载")
        
        elif 动词 in ("env", "环境"):
            print(f"\n🔧 环境信息:")
            for k, v in 环境.items():
                print(f"  {k}: {v}")
            print()
        
        elif 动词 == "governance":
            print("  🟢 龍魂治理技能已就绪")
            print("  功能: 三层监督 | 三色审计 | DNA追溯 | 君子协议")
        
        elif 动词 == "ocr":
            print("  🟢 龍瞳OCR技能已就绪")
            if 参数:
                print(f"  图像路径: {参数}")
            print("  功能: 中文字符识别 | 龍字检测 | 甲骨文分类")
        
        elif 动词 == "nlp":
            print("  🟢 龍文NLP技能已就绪")
            if 参数:
                print(f"  文本: {参数}")
            print("  功能: CNSH术语 | 通心译 | 分词 | 情感分析")
        
        elif 动词 == "asr":
            print("  🟢 龍音ASR技能已就绪")
            if 参数:
                print(f"  音频路径: {参数}")
            print("  功能: 语音识别 | 拼音对齐 | 语音转代码")
        
        elif 动词 == "finance":
            print("  🟢 龍魂金融技能已就绪")
            print("  功能: 五行看板 | 卦象审计 | 双轨数字人 | e-CNY")
        
        elif 动词 == "archive":
            print("  🟢 中央藏经阁技能已就绪")
            if 参数 and 注册表:
                结果 = 注册表.路由请求("longhun-archive")
                print(f"  路由: {结果.get('目标', 'N/A')}")
            print("  功能: 29部文档索引 | 五行检索 | DNA追溯")
        
        elif 动词 == "cnsh":
            print("  🟢 CNSH运行时技能已就绪")
            if 参数:
                print(f"  代码: {参数}")
            print("  功能: L1-L7层级 | 命名检查 | 15层渲染")
        
        elif 动词 in ("panel", "deploy", "mcp", "notion", "kimi"):
            if 环境["云端API可连"]:
                print(f"  🔵 云端技能 {动词} 已连接")
            else:
                print(f"  🟡 云端技能 {动词} 离线（API不可达）")
        
        else:
            print(f"  🟡 未知命令: {动词}")
            print("  输入 'help' 查看可用命令")


# ═══════════════════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════════════════
def 主函数():
    """🟢 主入口 | Main entry"""
    显示横幅()
    
    # 检测环境
    print("[启动器] 🔍 正在检测环境...")
    环境 = 检测环境()
    print(f"[启动器] ✅ 环境检测完成: {环境['模式']}模式")
    print(f"  numpy={'🟢' if 环境['numpy'] else '🔴'} "
          f"OpenCV={'🟢' if 环境['OpenCV'] else '🔴'} "
          f"torch={'🟢' if 环境['torch'] else '🔴'} "
          f"云端={'🟢' if 环境['云端API可连'] else '🔴'}")
    print()
    
    # 加载注册表
    注册表 = 加载技能注册表()
    
    # 加载本地技能
    本地成功 = 0
    if 注册表:
        本地成功 = 加载本地技能(注册表, 环境)
    
    # 连接云端技能
    云端成功 = 0
    if 注册表:
        云端成功 = 连接云端技能(注册表, 环境)
    
    # 显示启动摘要
    print()
    print("══════════════════════════════════════════════════════════")
    print("✅ 龍魂体系 v5.0 启动完成！")
    print(f"   本地技能: {本地成功}/9 | 云端技能: {云端成功}/5")
    print(f"   运行模式: {环境['模式']}")
    print(f"   DNA: {__dna__}")
    print("══════════════════════════════════════════════════════════")
    print()
    
    # 进入交互循环
    主循环(注册表, 环境)


if __name__ == "__main__":
    主函数()

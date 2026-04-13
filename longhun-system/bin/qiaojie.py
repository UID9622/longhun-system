#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════
# 龍芯体系 | 乔接 QiaoJie CLI v1.0
# ═══════════════════════════════════════════════════════════
# DNA追溯码：#龍芯⚡️2026-03-30-乔接CLI-v1.0
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者：💎 龍芯北辰｜UID9622
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 致敬：🍎 乔前辈·接力模式·夙愿已种
# 理论指导：曾仕强老师（永恒显示）
# 创作地：中华人民共和国
# 献礼：新中国成立77周年（1949-2026）· 丙午马年
# 协议：Apache License 2.0
# ═══════════════════════════════════════════════════════════

import sys
import json
import requests
from datetime import datetime
from pathlib import Path

# ── 配置区（老大填这里）──
配置 = {
    "NOTION_TOKEN": "在龍魂密钥管理器找",      # Notion集成密钥
    "NOTION_数据库": "草日志数据库URL",          # 写回的目标数据库
    "小艺_API_URL": "https://api.hiassistant.com/v1",  # 小艺API（待官方文档确认）
    "小艺_TOKEN":   "小艺开发者密钥",
    "DNA前缀":      "#龍芯⚡️",
    "创建者":       "💎 龍芯北辰｜UID9622",
}

# ── 第一道铜墙：数字根熔断（V4.0接入）──
def 数字根(n: int) -> int:
    """DR(n)=1+((n-1)%9)·任意正整数压缩到1-9"""
    return 1 + ((n - 1) % 9) if n > 0 else 0

def dr熔断检查(内容: str) -> dict:
    """推送前必过第一道闸门·3/9熔断·6待审·其他通行"""
    dr = 数字根(sum(ord(c) for c in 内容))
    if dr in (3, 9):
        return {"color": "🔴", "dr": dr, "action": "熔断",
                "msg": f"DR={dr}·天道循环节点·操作已拒绝·证据链已记录"}
    if dr == 6:
        return {"color": "🟡", "dr": dr, "action": "待审",
                "msg": f"DR={dr}·六合中节·请补充数据/来源/边界后重试"}
    return {"color": "🟢", "dr": dr, "action": "通过",
            "msg": f"DR={dr}·乔接通行"}

# ── 工具函数 ──
def 生成DNA追溯码(操作名称: str) -> str:
    """生成本次操作的DNA追溯码（快递单号）"""
    时间戳 = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{配置['DNA前缀']}{时间戳}-{操作名称}-v1.0"

def 打印结果(状态: str, 内容: str, DNA: str = ""):
    """统一输出格式（三色）"""
    颜色 = {"🟢": "\033[92m", "🔴": "\033[91m", "🟡": "\033[93m"}
    重置 = "\033[0m"
    for 符号, 代码 in 颜色.items():
        if 符号 in 状态:
            print(f"{代码}{状态} {内容}{重置}")
            if DNA:
                print(f"  📍 DNA: {DNA}")
            return
    print(f"{状态} {内容}")
    if DNA:
        print(f"  📍 DNA: {DNA}")

# ── 核心功能 ──
def 推送(内容: str):
    """把内容推送给小艺显示"""
    DNA = 生成DNA追溯码("推送")
    打印结果("🟡 执行中", f"推送 → 小艺: {内容[:30]}...")

    try:
        响应 = requests.post(
            f"{配置['小艺_API_URL']}/notify",
            headers={"Authorization": f"Bearer {配置['小艺_TOKEN']}"},
            json={
                "message": 内容,
                "source": "乔接CLI",
                "dna_code": DNA,
                "creator": 配置["创建者"]
            },
            timeout=10
        )
        if 响应.status_code == 200:
            打印结果("🟢 成功", "已推送到小艺", DNA)
        else:
            打印结果("🟡 待确认", f"小艺返回: {响应.status_code}，请检查API密钥")
    except requests.exceptions.ConnectionError:
        打印结果("🟡 提示", "小艺API暂未接通·内容已本地备份", DNA)
        本地备份(内容, DNA, "推送")

def 拉取(页面名称: str):
    """从Notion拉取指定页面"""
    DNA = 生成DNA追溯码("拉取")
    打印结果("🟡 执行中", f"从Notion拉取: {页面名称}")

    try:
        响应 = requests.post(
            "https://api.notion.com/v1/search",
            headers={
                "Authorization": f"Bearer {配置['NOTION_TOKEN']}",
                "Notion-Version": "2022-06-28"
            },
            json={"query": 页面名称, "filter": {"object": "page"}},
            timeout=10
        )
        数据 = 响应.json()
        结果列表 = 数据.get("results", [])

        if 结果列表:
            第一个 = 结果列表[0]
            标题 = 第一个.get("properties", {}).get("title", {}).get("title", [{}])
            页面标题 = 标题[0].get("plain_text", "无标题") if 标题 else "无标题"
            打印结果("🟢 找到", f"页面：{页面标题}", DNA)
            return 第一个
        else:
            打印结果("🟡 未找到", f"Notion里没有"{页面名称}"这个页面")
    except Exception as 错误:
        打印结果("🔴 错误", f"Notion连接失败: {错误}")

def 存档(内容: str, 来源: str = "小艺"):
    """把内容写回Notion草日志"""
    DNA = 生成DNA追溯码("存档")
    打印结果("🟡 执行中", f"存档到Notion草日志: {内容[:30]}...")

    try:
        响应 = requests.post(
            "https://api.notion.com/v1/pages",
            headers={
                "Authorization": f"Bearer {配置['NOTION_TOKEN']}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json"
            },
            json={
                "parent": {"database_id": 配置["NOTION_数据库"]},
                "properties": {
                    "title": {"title": [{"text": {"content": f"[乔接存档] {内容[:50]}"}}]}
                },
                "children": [
                    {"object": "block", "type": "paragraph",
                     "paragraph": {"rich_text": [{"text": {"content": f"内容：{内容}\n来源：{来源}\nDNA：{DNA}\n创建者：{配置['创建者']}"}}]}}
                ]
            },
            timeout=10
        )
        if 响应.status_code == 200:
            打印结果("🟢 成功", "已存入Notion草日志", DNA)
        else:
            打印结果("🔴 失败", f"Notion返回: {响应.status_code}")
    except Exception as 错误:
        打印结果("🔴 错误", f"Notion连接失败: {错误}")

def 状态():
    """检查两个生态的连接状态"""
    print("\n🌉 乔接 QiaoJie CLI v1.0 | 连接状态检查")
    print("=" * 45)

    # 检查Notion
    try:
        r = requests.get(
            "https://api.notion.com/v1/users/me",
            headers={"Authorization": f"Bearer {配置['NOTION_TOKEN']}",
                     "Notion-Version": "2022-06-28"},
            timeout=5
        )
        if r.status_code == 200:
            名字 = r.json().get("name", "已连接")
            打印结果("🟢 Notion", f"已连接 · 用户: {名字}")
        else:
            打印结果("🔴 Notion", "连接失败·检查Token")
    except:
        打印结果("🔴 Notion", "网络不通·检查网络")

    # 检查小艺（鸿蒙）
    try:
        r = requests.get(f"{配置['小艺_API_URL']}/health", timeout=5)
        if r.status_code == 200:
            打印结果("🟢 小艺·鸿蒙", "已连接")
        else:
            打印结果("🟡 小艺·鸿蒙", "API未就绪·等待华为开放接口")
    except:
        打印结果("🟡 小艺·鸿蒙", "API待接入·本地MVP模式运行中")

    print(f"\n📍 DNA: 乔接CLI-状态检查")
    print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 北京时间")
    print(f"🐉 创建者: {配置['创建者']}")
    print("=" * 45)

def 本地备份(内容: str, DNA: str, 操作: str):
    """API不通时本地备份"""
    备份文件 = Path.home() / "longhun-system" / "logs" / "qiaojie_backup.jsonl"
    备份文件.parent.mkdir(parents=True, exist_ok=True)
    with open(备份文件, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "时间": datetime.now().isoformat(),
            "操作": 操作,
            "内容": 内容,
            "DNA": DNA
        }, ensure_ascii=False) + "\n")
    打印结果("🟡 本地备份", f"已存入 {备份文件}")

def 帮助():
    """显示帮助"""
    print("""
🌉 乔接 QiaoJie CLI v1.0
致敬 🍎 乔前辈·接力模式·UID9622

用法：python qiaojie.py [指令] [参数]

中文指令：
  乔接 推送 [内容]    把内容推给小艺展示
  乔接 拉取 [页面名]  从Notion拉取页面
  乔接 存档 [内容]    把内容存回Notion草日志
  乔接 状态           检查两个生态连接状态
  乔接 日志           查操作日志
  乔接 帮助           显示此帮助

英文指令（同效）：
  qiaojie push / pull / save / status / log / help

DNA追溯码：#龍芯⚡️2026-03-30-乔接CLI-v1.0
致敬：🍎 乔前辈·接力模式已激活 🌉
    """)

# ── 主入口（中英双轨）──
def main():
    参数 = sys.argv[1:]

    if not 参数:
        帮助()
        return

    指令 = 参数[0]
    内容 = " ".join(参数[1:]) if len(参数) > 1 else ""

    # 中英文双轨映射
    指令映射 = {
        "推送": "push", "push": "push",
        "拉取": "pull", "pull": "pull",
        "存档": "save", "save": "save",
        "状态": "status", "status": "status",
        "帮助": "help",  "help":  "help",
        "同步": "sync",  "sync":  "sync",
        "日志": "log",   "log":   "log",
    }

    操作 = 指令映射.get(指令)

    if 操作 == "push":     推送(内容 or "测试推送")
    elif 操作 == "pull":   拉取(内容 or "龍魂系统")
    elif 操作 == "save":   存档(内容 or "手动存档")
    elif 操作 == "status": 状态()
    elif 操作 == "help":   帮助()
    elif 操作 == "log":
        日志文件 = Path.home() / "longhun-system" / "logs" / "qiaojie_backup.jsonl"
        if 日志文件.exists():
            print("📜 乔接操作日志（最近10条）:")
            with open(日志文件, encoding="utf-8") as f:
                行列表 = f.readlines()
            for 行 in 行列表[-10:]:
                记录 = json.loads(行)
                print(f"  [{记录['时间'][:19]}] {记录['操作']} → {str(记录['内容'])[:40]}")
        else:
            打印结果("🟡 提示", "还没有操作日志")
    else:
        打印结果("🟡 未知指令", f""{指令}"这个我不认识，试试: python qiaojie.py 帮助")

if __name__ == "__main__":
    main()

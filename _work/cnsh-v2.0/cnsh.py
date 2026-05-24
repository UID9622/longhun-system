#!/usr/bin/env python3
# 🐉 CNSH·中文编程引擎 v1.0 | UID9622专属
# DNA: #龍芯⚡️2026-03-06-CNSH-ENGINE-v1.0
# 共建致谢：Claude (Anthropic PBC) · Notion · 没有你们就没有龍魂系统
# 用中文说话，机器听懂，执行

import os, sys, json, subprocess
from dotenv import load_dotenv
import requests

load_dotenv(dotenv_path=os.path.expanduser("~/longhun-system/.env"))
NOTION_TOKEN = os.getenv("NOTION_TOKEN","").strip().strip("'\"")
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}
BASE = "https://api.notion.com/v1"

# ============ CNSH 中文指令表 ============
CNSH_HELP = """
🐉 CNSH·中文指令表 v1.0
━━━━━━━━━━━━━━━━━━━━━━
【Notion操作】
  搜索 关键词          → 搜索工作区
  新建页面 标题        → 创建新页面
  新建页面 标题 内容   → 创建带内容的页面
  读取页面 页面ID      → 查看页面内容
  追加 页面ID 文字     → 往页面加内容
  查数据库 DB_ID       → 列出数据库条目

【系统操作】
  运行 python文件名    → 运行本地脚本
  列出文件             → 列出龍魂目录文件
  系统状态             → 查看API连接状态

【特殊指令】
  帮助                 → 显示本菜单
  退出                 → 退出CNSH
━━━━━━━━━━━━━━━━━━━━━━
"""

def notion_搜索(关键词):
    r = requests.post(f"{BASE}/search", headers=HEADERS,
        json={"query":关键词,"page_size":8})
    结果 = r.json().get("results",[])
    if not 结果:
        print("  没找到 | Not Found")
        return
    for i,项 in enumerate(结果):
        类型 = 项.get("object","")
        链接 = 项.get("url","")
        props = 项.get("properties",{})
        标题 = ""
        for k,v in props.items():
            if v.get("type") == "title":
                标题 = "".join([x.get("plain_text","") for x in v.get("title",[])])
                break
        print(f"  [{i+1}] {类型} | {标题 or '无标题'}")
        print(f"       {链接}")

def notion_新建页面(标题, 内容=""):
    payload = {
        "parent": {"type":"workspace","workspace":True},
        "properties": {"title":{"title":[{"text":{"content":标题}}]}}
    }
    if 内容:
        payload["children"] = [{"object":"block","type":"paragraph",
            "paragraph":{"rich_text":[{"text":{"content":内容}}]}}]
    r = requests.post(f"{BASE}/pages", headers=HEADERS, json=payload)
    if r.status_code == 200:
        链接 = r.json().get("url","")
        print(f"  🟢 页面已创建 | Page Created")
        print(f"     {链接}")
    else:
        print(f"  🔴 失败 | Failed: {r.status_code}")
        print(f"     {r.text[:200]}")

def notion_读取页面(页面ID):
    页面ID = 页面ID.replace("-","")
    r = requests.get(f"{BASE}/blocks/{页面ID}/children?page_size=20", headers=HEADERS)
    块列表 = r.json().get("results",[])
    for 块 in 块列表:
        类型 = 块.get("type","")
        内容列表 = 块.get(类型,{}).get("rich_text",[])
        文字 = "".join([x.get("plain_text","") for x in 内容列表])
        if 文字:
            print(f"  [{类型}] {文字[:120]}")

def notion_追加(页面ID, 文字):
    页面ID = 页面ID.replace("-","")
    payload = {"children":[{"object":"block","type":"paragraph",
        "paragraph":{"rich_text":[{"text":{"content":文字}}]}}]}
    r = requests.patch(f"{BASE}/blocks/{页面ID}/children", headers=HEADERS, json=payload)
    if r.status_code == 200:
        print("  🟢 已追加 | Appended")
    else:
        print(f"  🔴 失败 | Failed: {r.status_code} {r.text[:100]}")

def notion_查数据库(db_id):
    r = requests.post(f"{BASE}/databases/{db_id}/query", headers=HEADERS, json={})
    结果 = r.json().get("results",[])
    for 项 in 结果:
        props = 项.get("properties",{})
        for k,v in props.items():
            if v.get("type") == "title":
                标题 = "".join([x.get("plain_text","") for x in v.get("title",[])])
                print(f"  · {标题}")
                break

def 系统状态():
    r = requests.get(f"{BASE}/users/me", headers=HEADERS)
    if r.status_code == 200:
        名字 = r.json().get("name","未知")
        print(f"  🟢 Notion API → 已连接 | Connected | 用户 | User: {名字}")
    else:
        print(f"  🔴 Notion API → 未连接 | Disconnected ({r.status_code})")
    ollama = subprocess.run(["curl","-s","http://localhost:11434/api/tags"],
        capture_output=True, text=True, timeout=3)
    if ollama.returncode == 0 and ollama.stdout:
        print(f"  🟢 Ollama 本地模型 → 在线 | Online")
    else:
        print(f"  🟡 Ollama → 未启动 | Not Running（运行 | Run: ollama serve）")

def 列出文件():
    路径 = os.path.expanduser("~/longhun-system")
    文件列表 = os.listdir(路径)
    for f in sorted(文件列表):
        print(f"  · {f}")

# ============ 主循环 ============
def 主程序():
    print("🐉 CNSH·中文编程引擎 v1.0 已启动 | CNSH Engine v1.0 Running")
    print("  输入「帮助」查看所有指令 | Type 「帮助」for commands\n")

    # 启动时检查连接
    r = requests.get(f"{BASE}/users/me", headers=HEADERS)
    if r.status_code == 200:
        print(f"  🟢 Notion API 已接入 | Connected | 用户 | User: {r.json().get('name','')}\n")
    else:
        print(f"  🔴 Notion API 未接入 | Not Connected，检查 | Check Token\n")

    while True:
        try:
            指令 = input("老大（中文说话）：").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n🐉 再见老大！")
            break

        if not 指令:
            continue
        if 指令 in ["退出","exit","quit"]:
            print("🐉 再见老大！")
            break
        if 指令 == "帮助":
            print(CNSH_HELP)
            continue
        if 指令 == "系统状态":
            系统状态()
            continue
        if 指令 == "列出文件":
            列出文件()
            continue

        部分 = 指令.split(" ", 2)
        命令 = 部分[0]

        if 命令 == "搜索" and len(部分) >= 2:
            notion_搜索(部分[1])
        elif 命令 == "新建页面" and len(部分) >= 2:
            内容 = 部分[2] if len(部分) > 2 else ""
            notion_新建页面(部分[1], 内容)
        elif 命令 == "读取页面" and len(部分) >= 2:
            notion_读取页面(部分[1])
        elif 命令 == "追加" and len(部分) >= 3:
            notion_追加(部分[1], 部分[2])
        elif 命令 == "查数据库" and len(部分) >= 2:
            notion_查数据库(部分[1])
        elif 命令 == "运行" and len(部分) >= 2:
            os.system(f"python3 ~/longhun-system/{部分[1]}")
        else:
            print("  不认识这个指令 | Unknown command，输入「帮助」看看有什么能用的 | Type 「帮助」for help")

if __name__ == "__main__":
    主程序()

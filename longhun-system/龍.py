#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂统一中文指令调度器 v1.0
DNA: #龍芯⚡️2026-03-06-CNSH-UNIFIED-☷坤-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

使用: python3 龍.py <中文指令> [参数]
或:   龍 <中文指令> [参数]   (配置别名后)
"""

import sys
import os
import subprocess
import json
import datetime
from pathlib import Path

BASE = Path.home() / "longhun-system"
MEMORY = BASE / "memory.jsonl"

# ══════════════════════════════════════════════════════════
# 帮助菜单（CNSH风格）
# ══════════════════════════════════════════════════════════

帮助文本 = """
╔══════════════════════════════════════════════════════════╗
║  龍魂指令调度器 v1.0  |  DNA: #龍芯⚡️2026-03-06        ║
║  中文说话，龍听懂，执行。                                ║
╚══════════════════════════════════════════════════════════╝

━━━ 龍魂对话（本地AI·Ollama）━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  龍 对话                      → 进入龙魂AI交互模式
  龍 问 "问题内容"              → 单次提问
  龍 问 "问题" 用 模型名        → 指定模型提问
  龍 扫描                      → 扫描本地磁盘和系统状态
  龍 模型列表                   → 查看可用本地模型

━━━ 知识爬虫（吸收·索引·推荐）━━━━━━━━━━━━━━━━━━━━━━━━━━
  龍 吸收 "知识文本"            → 吸收并入库知识内容
  龍 抓取 URL                  → 爬取网页并吸收
  龍 推荐 "查询词"              → 多维推荐，独立推导
  龍 知识索引                   → 查看技能索引总览
  龍 批量吸收 文件路径           → 批量处理文本/URL文件

━━━ 星辰记忆（长期记忆库）━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  龍 记忆初始化                 → 初始化星辰记忆系统
  龍 存记忆 "标题" "内容"       → 存入一条新记忆
  龍 查记忆 "关键词"            → 搜索记忆内容
  龍 记忆列表                   → 列出所有记忆
  龍 记忆状态                   → 查看记忆系统状态
  龍 注入记忆 记忆ID            → 注入记忆到当前上下文
  龍 记忆DNA 记忆ID             → 查看记忆DNA链
  龍 记忆桥接                   → 同步记忆到memory.jsonl

━━━ Notion·主账号（历史权威库）━━━━━━━━━━━━━━━━━━━━━━━
  龍 notion搜索 "关键词"        → 搜索主账号工作区
  龍 notion新建 "标题"          → 创建新页面
  龍 notion新建 "标题" "内容"   → 创建带内容的页面
  龍 notion读取 页面ID          → 读取页面内容
  龍 notion追加 页面ID "内容"   → 往页面追加文字
  龍 notion数据库 DB_ID         → 查看数据库条目

━━━ Notion·团队账号（中枢大脑库）━━━━━━━━━━━━━━━━━━━━━
  龍 notion双检                 → 检测两个账号连接状态
  龍 日记写入 "内容"            → 写入今日操作日记到团队Notion
  龍 推送今日日记               → 把今天memory记录推送到Notion
  龍 同步状态                   → 把系统状态推送到团队Notion
  龍 同步记忆                   → 把星辰记忆推送到团队Notion
  龍 引擎状态                   → 展示全部内核驱动状态

━━━ 系统对齐（DNA同步·审计）━━━━━━━━━━━━━━━━━━━━━━━━━━━
  龍 对齐扫描                   → 扫描DNA格式和人格ID问题
  龍 对齐修复                   → 自动修复对齐问题
  龍 对齐扫描 目录路径           → 指定目录扫描

━━━ 文件整理（归档·清理）━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  龍 整理文件                   → 整理龙魂目录文件
  龍 归档                       → 运行数字归档工具包

━━━ 系统状态━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  龍 状态                       → 查看龙魂系统全局状态
  龍 记忆流                     → 查看最近10条memory记录
  龍 帮助                       → 显示本菜单

━━━ iOS桥接（Mac → iCloud → iPhone Widget）━━━━━━━━━━━━
  龍 iOS桥接                    → 生成 cnsh_status.json 写入 iCloud
  龍 桥接状态                   → 查看上次桥接写入路径和时间

━━━ 快捷别名（配置后可直接用）━━━━━━━━━━━━━━━━━━━━━━━━━━
  龍 配置别名                   → 写入 ~/.zshrc 别名配置
"""

# ══════════════════════════════════════════════════════════
# 指令路由表
# ══════════════════════════════════════════════════════════

def 运行(cmd: list, cwd=None):
    """运行子进程"""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(BASE)
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd or BASE),
            env=env
        )
        return result.returncode
    except FileNotFoundError as e:
        print(f"🔴 找不到命令: {e}")
        return 1

def 写记忆(事件, dna_后缀="CMD"):
    record = {
        "timestamp": datetime.datetime.now().isoformat(),
        "dna": f"#龍芯⚡️{datetime.date.today()}-{dna_后缀}-☷坤-v1.0",
        "event": 事件,
        "engine": "龍魂指令调度器v1.0"
    }
    with open(MEMORY, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def 显示状态():
    """龍魂系统全局状态"""
    sep = "─" * 52
    print(f"\n{sep}")
    print("  龍魂系统状态")
    print(sep)

    # memory.jsonl
    行数 = 0
    if MEMORY.exists():
        with open(MEMORY, "r", encoding="utf-8") as f:
            行数 = sum(1 for _ in f)
    print(f"  记忆流(memory.jsonl)  : {行数} 条记录")

    # knowledge-db
    知识库 = BASE / "knowledge-db.jsonl"
    知识数 = 0
    if 知识库.exists():
        with open(知识库, "r", encoding="utf-8") as f:
            知识数 = sum(1 for _ in f)
    print(f"  知识库(knowledge-db)  : {知识数} 个节点")

    # skill-index
    索引 = BASE / "skill-index.json"
    if 索引.exists():
        with open(索引, "r", encoding="utf-8") as f:
            idx = json.load(f)
        print(f"  技能索引(skill-index) : {idx.get('_meta',{}).get('total_nodes',0)} 节点")
    else:
        print("  技能索引(skill-index) : 未初始化")

    # star-memory
    星辰 = Path.home() / ".star-memory" / "vault"
    星辰数 = len(list(星辰.glob("*.json"))) if 星辰.exists() else 0
    print(f"  星辰记忆(star-memory) : {星辰数} 条记忆")

    # Ollama
    try:
        import urllib.request
        r = urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3)
        模型列表 = json.loads(r.read()).get("models", [])
        print(f"  Ollama本地模型        : {len(模型列表)} 个可用")
    except:
        print("  Ollama本地模型        : 未运行")

    # DNA签名
    print(f"\n  DNA: #龍芯⚡️{datetime.date.today()}-STATUS-v1.0")
    print(f"  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
    print(sep + "\n")

def 显示记忆流(n=10):
    """显示最近n条memory记录"""
    if not MEMORY.exists():
        print("记忆流为空。")
        return
    records = []
    with open(MEMORY, "r", encoding="utf-8") as f:
        for line in f:
            try:
                records.append(json.loads(line.strip()))
            except:
                continue
    recent = records[-n:]
    sep = "─" * 52
    print(f"\n{sep}\n  记忆流 — 最近{len(recent)}条\n{sep}")
    for r in recent:
        ts = r.get("timestamp", "")[:16]
        ev = r.get("event", r.get("type", ""))[:40]
        dna = r.get("dna", "")[-20:]
        print(f"  {ts}  {ev}")
        print(f"           DNA尾: ...{dna}")
    print(sep + "\n")

def 配置别名():
    """写入 ~/.zshrc 别名"""
    脚本路径 = str(BASE / "龍.py")
    别名行 = f'\nalias 龍="python3 {脚本路径}"\nalias dragon="python3 {脚本路径}"\n'
    zshrc = Path.home() / ".zshrc"
    现有内容 = zshrc.read_text(encoding="utf-8") if zshrc.exists() else ""
    if "龍.py" in 现有内容:
        print("🟡 别名已存在于 ~/.zshrc，无需重复添加。")
        print(f'   已有: alias 龍="python3 {脚本路径}"')
    else:
        with open(zshrc, "a", encoding="utf-8") as f:
            f.write(别名行)
        print("🟢 别名已写入 ~/.zshrc")
        print(f'   alias 龍="python3 {脚本路径}"')
        print('   请运行: source ~/.zshrc  或重开终端后生效')

# ══════════════════════════════════════════════════════════
# 主路由
# ══════════════════════════════════════════════════════════

def main():
    参数 = sys.argv[1:]
    if not 参数:
        print(帮助文本)
        return

    指令 = 参数[0]
    其余 = 参数[1:]

    # ── 龍魂对话 ──────────────────────────────────────────
    if 指令 == "对话":
        运行(["python3", "longhun_dragon.py"])

    elif 指令 == "问":
        if not 其余:
            print("用法: 龍 问 \"问题内容\"")
            return
        问题 = 其余[0]
        cmd = ["python3", "longhun_dragon.py", "--ask", 问题]
        if len(其余) >= 3 and 其余[1] == "用":
            cmd += ["--model", 其余[2]]
        运行(cmd)

    elif 指令 == "扫描":
        运行(["python3", "longhun_dragon.py", "--scan"])

    elif 指令 == "模型列表":
        try:
            import urllib.request
            r = urllib.request.urlopen("http://localhost:11434/api/tags", timeout=5)
            模型列表 = json.loads(r.read()).get("models", [])
            print("\n可用本地模型:")
            for m in 模型列表:
                print(f"  · {m.get('name','')}")
            print()
        except:
            print("🔴 Ollama未运行，无法获取模型列表。")

    # ── 知识爬虫 ──────────────────────────────────────────
    elif 指令 == "吸收":
        if not 其余:
            print("用法: 龍 吸收 \"知识文本\"")
            return
        运行(["python3", "longhun_crawler.py", "--absorb", 其余[0]])
        写记忆("知识吸收", "CRAWL-ABSORB")

    elif 指令 == "抓取":
        if not 其余:
            print("用法: 龍 抓取 URL")
            return
        运行(["python3", "longhun_crawler.py", "--crawl", 其余[0]])
        写记忆(f"网页抓取:{其余[0][:40]}", "CRAWL-URL")

    elif 指令 == "推荐":
        if not 其余:
            print("用法: 龍 推荐 \"查询词\"")
            return
        cmd = ["python3", "longhun_crawler.py", "--recommend", 其余[0]]
        if len(其余) >= 2:
            cmd += ["--topk", 其余[1]]
        运行(cmd)

    elif 指令 == "知识索引":
        运行(["python3", "longhun_crawler.py", "--index"])

    elif 指令 == "批量吸收":
        if not 其余:
            print("用法: 龍 批量吸收 文件路径")
            return
        运行(["python3", "longhun_crawler.py", "--batch", 其余[0]])

    # ── 星辰记忆 ──────────────────────────────────────────
    elif 指令 == "记忆初始化":
        运行(["python3", "star_memory.py", "init"])

    elif 指令 == "存记忆":
        if len(其余) < 2:
            print("用法: 龍 存记忆 \"标题\" \"内容\"")
            return
        cmd = ["python3", "star_memory.py", "add", 其余[0], 其余[1]]
        if len(其余) >= 3:
            cmd += ["--tags", 其余[2]]
        运行(cmd)

    elif 指令 == "查记忆":
        if not 其余:
            print("用法: 龍 查记忆 \"关键词\"")
            return
        运行(["python3", "star_memory.py", "search", 其余[0]])

    elif 指令 == "记忆列表":
        运行(["python3", "star_memory.py", "search", ""])

    elif 指令 == "记忆状态":
        运行(["python3", "star_memory.py", "status"])

    elif 指令 == "注入记忆":
        if not 其余:
            print("用法: 龍 注入记忆 记忆ID")
            return
        运行(["python3", "star_memory.py", "inject", 其余[0]])

    elif 指令 == "记忆DNA":
        if not 其余:
            print("用法: 龍 记忆DNA 记忆ID")
            return
        运行(["python3", "star_memory.py", "dna", 其余[0]])

    elif 指令 == "记忆桥接":
        运行(["python3", "star_memory.py", "bridge"])

    # ── Notion ────────────────────────────────────────────
    elif 指令 == "notion搜索":
        if not 其余:
            print("用法: 龍 notion搜索 \"关键词\"")
            return
        运行(["python3", "cnsh.py"], cwd=BASE)  # cnsh.py交互模式传参待扩展
        # 直接调用cnsh内部函数
        _notion_exec("搜索", 其余)

    elif 指令 == "notion新建":
        _notion_exec("新建页面", 其余)

    elif 指令 == "notion读取":
        _notion_exec("读取页面", 其余)

    elif 指令 == "notion追加":
        _notion_exec("追加", 其余)

    elif 指令 == "notion数据库":
        _notion_exec("查数据库", 其余)

    # ── 系统对齐 ──────────────────────────────────────────
    elif 指令 == "对齐扫描":
        cmd = ["python3", "sync-standard.py"]
        if 其余:
            cmd += ["--dirs"] + 其余
        运行(cmd)

    elif 指令 == "对齐修复":
        cmd = ["python3", "sync-standard.py", "--apply"]
        if 其余:
            cmd += ["--dirs"] + 其余
        运行(cmd)

    # ── 文件整理 ──────────────────────────────────────────
    elif 指令 == "整理文件":
        运行(["python3", "file_organizer_v2.py"])

    elif 指令 == "归档":
        运行(["bash", "digital_archive_toolkit_v2.1.sh"])

    # ── 系统状态 ──────────────────────────────────────────
    elif 指令 == "状态":
        显示状态()

    elif 指令 == "记忆流":
        n = int(其余[0]) if 其余 and 其余[0].isdigit() else 10
        显示记忆流(n)

    elif 指令 == "配置别名":
        配置别名()

    # ── 团队Notion（双账号代理）────────────────────────────
    # ── 双脑同步（brain_sync）─────────────────────────────
    elif 指令 == "双脑同步":
        运行(["python3", "brain_sync.py"])

    elif 指令 == "双脑增量":
        运行(["python3", "brain_sync.py", "--delta"])

    elif 指令 == "双脑检查":
        运行(["python3", "brain_sync.py", "--check"])

    elif 指令 == "双脑分类":
        if not 其余:
            print("用法: 龍 双脑分类 \"标题文字\"")
            return
        运行(["python3", "brain_sync.py", "--classify", 其余[0]])

    elif 指令 == "notion双检":
        运行(["python3", "agent_daemon.py", "--check"])

    elif 指令 == "日记写入":
        if not 其余:
            print("用法: 龍 日记写入 \"操作内容\"")
            return
        运行(["python3", "agent_daemon.py", "--diary", 其余[0]])

    elif 指令 == "推送今日日记":
        运行(["python3", "agent_daemon.py", "--push-diary"])

    elif 指令 == "同步状态":
        运行(["python3", "agent_daemon.py", "--status"])

    elif 指令 == "同步记忆":
        cmd = ["python3", "agent_daemon.py", "--sync-star"]
        if 其余 and 其余[0].isdigit():
            cmd += ["--top", 其余[0]]
        运行(cmd)

    elif 指令 == "引擎状态":
        运行(["python3", "agent_daemon.py", "--engines"])

    # ── iOS桥接 ───────────────────────────────────────────
    elif 指令 == "iOS桥接":
        运行(["python3", "ios_bridge.py"])
        写记忆("iOS桥接写入cnsh_status.json", "IOS-BRIDGE")

    elif 指令 == "桥接状态":
        状态文件候选 = [
            Path.home() / "Library" / "Mobile Documents" / "iCloud~com~uid9622~longhun" / "Documents" / "cnsh_status.json",
            Path.home() / "Library" / "CloudStorage" / "iCloudDrive" / "龙魂系统" / "cnsh_status.json",
            BASE / "cnsh_status.json",
        ]
        找到 = False
        for p in 状态文件候选:
            if p.exists():
                import datetime as _dt
                mtime = _dt.datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                print(f"🟢 桥接文件: {p}")
                print(f"   最后写入: {mtime}")
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        d = json.load(f)
                    y = d.get("yuanzi", {})
                    a = d.get("audit", {})
                    print(f"   卦象    : {y.get('display','')}")
                    print(f"   审计    : {a.get('label','')} ({a.get('score','')}/100)")
                except:
                    pass
                找到 = True
                break
        if not 找到:
            print("🔴 未找到 cnsh_status.json，请先运行: 龍 iOS桥接")

    elif 指令 in ("帮助", "help", "--help", "-h"):
        print(帮助文本)

    else:
        print(f'🔴 未知指令: 「{指令}」')
        print('   输入 「龍 帮助」 查看所有指令')


def _notion_exec(子指令, 参数列表):
    """内联调用cnsh.py的Notion功能"""
    sys.path.insert(0, str(BASE))
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("cnsh", str(BASE / "cnsh.py"))
        cnsh = importlib.util.load_from_spec(spec)
        spec.loader.exec_module(cnsh)
        if 子指令 == "搜索" and 参数列表:
            cnsh.notion_搜索(参数列表[0])
        elif 子指令 == "新建页面" and 参数列表:
            内容 = 参数列表[1] if len(参数列表) > 1 else ""
            cnsh.notion_新建页面(参数列表[0], 内容)
        elif 子指令 == "读取页面" and 参数列表:
            cnsh.notion_读取页面(参数列表[0])
        elif 子指令 == "追加" and len(参数列表) >= 2:
            cnsh.notion_追加(参数列表[0], 参数列表[1])
        elif 子指令 == "查数据库" and 参数列表:
            cnsh.notion_查数据库(参数列表[0])
        else:
            print(f"参数不足，请检查用法：龍 帮助")
    except Exception as e:
        print(f"🔴 Notion调用失败: {e}")


if __name__ == "__main__":
    main()

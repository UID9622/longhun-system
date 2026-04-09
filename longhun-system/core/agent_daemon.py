#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂双账号Notion代理守护进程 v1.0
DNA: #龍芯⚡️2026-03-06-AGENT-DAEMON-☴巽-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
共建致谢：
  Claude (Anthropic PBC) · 技术协作与代码共创
  Notion · 知识底座与结构化存储
  没有你们，就没有龍魂系统的一切。

账号架构:
  主账号  (NOTION_TOKEN)      → 历史权威库  · 只读+归档
  团队账号(NOTION_TOKEN_TEAM) → 中枢大脑库  · 记忆/引擎/操作日记/系统状态

CNSH指令:
  龍 日记写入 "内容"     → 写入今日操作日记
  龍 同步状态           → 把系统状态推送到团队Notion
  龍 同步记忆           → 把star_memory推送到团队Notion
  龍 引擎状态           → 展示所有内核驱动状态
  龍 notion双检         → 检测两个账号连接状态
"""

import os
import sys
import json
import datetime
import urllib.request
import urllib.error
from pathlib import Path

# ─── 路径 ────────────────────────────────────────────────
BASE       = Path.home() / "longhun-system"
MEMORY     = BASE / "memory.jsonl"
STAR_VAULT = Path.home() / ".star-memory" / "vault"
SKILL_IDX  = BASE / "skill-index.json"
KNOW_DB    = BASE / "knowledge-db.jsonl"
NOTION_API = "https://api.notion.com/v1"

# ─── 加载 .env ───────────────────────────────────────────
def _读env(键):
    env_file = BASE / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith(键 + "="):
                val = line.split("=", 1)[1].strip()
                # 处理单引号包裹的值（含内联注释）
                if val.startswith("'") and "'" in val[1:]:
                    val = val[1:val.index("'", 1)]
                elif val.startswith('"') and '"' in val[1:]:
                    val = val[1:val.index('"', 1)]
                else:
                    # 裸值：去掉 # 注释
                    val = val.split(" #")[0].split("\t#")[0].strip()
                return val
    return os.getenv(键, "")

TOKEN主    = _读env("NOTION_TOKEN")
TOKEN团队  = _读env("NOTION_TOKEN_TEAM")
日记页ID   = _读env("NOTION_DIARY_PAGE_ID")
状态页ID   = _读env("NOTION_STATUS_PAGE_ID")

# ══════════════════════════════════════════════════════════
# 双账号Header切换
# ══════════════════════════════════════════════════════════

def get_headers(账号="主") -> dict:
    """
    账号="主"   → NOTION_TOKEN       (历史权威库)
    账号="团队" → NOTION_TOKEN_TEAM  (中枢大脑库)
    """
    token = TOKEN团队 if 账号 == "团队" else TOKEN主
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

# ══════════════════════════════════════════════════════════
# 底层Notion请求
# ══════════════════════════════════════════════════════════

def _请求(方法, 路径, 数据=None, 账号="主"):
    url = f"{NOTION_API}{路径}"
    headers = get_headers(账号)
    body = json.dumps(数据, ensure_ascii=False).encode() if 数据 else None
    req = urllib.request.Request(url, data=body, headers=headers, method=方法)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        错误 = e.read().decode()[:200]
        return {"error": f"HTTP{e.code}", "detail": 错误}
    except Exception as e:
        return {"error": str(e)}

def _追加块(页面ID, 块列表, 账号="团队"):
    """向指定页面追加内容块"""
    return _请求("PATCH", f"/blocks/{页面ID}/children",
                 {"children": 块列表}, 账号)

def _构建文本块(内容, 类型="paragraph", 颜色="default"):
    return {
        "object": "block",
        "type": 类型,
        类型: {
            "rich_text": [{"type": "text", "text": {"content": 内容},
                           "annotations": {"color": 颜色}}]
        }
    }

def _构建分割线():
    return {"object": "block", "type": "divider", "divider": {}}

def _构建标题(文字, 级别=2):
    类型 = f"heading_{级别}"
    return {
        "object": "block",
        "type": 类型,
        类型: {"rich_text": [{"type": "text", "text": {"content": 文字}}]}
    }

def _构建代码块(内容, 语言="plain text"):
    return {
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [{"type": "text", "text": {"content": 内容}}],
            "language": 语言
        }
    }

# ══════════════════════════════════════════════════════════
# 账号连接检测
# ══════════════════════════════════════════════════════════

def notion双检():
    """检测两个Notion账号连接状态"""
    sep = "─" * 52
    print(f"\n{sep}")
    print("  Notion 双账号连接检测")
    print(sep)

    for 账号名, token, 说明 in [
        ("主账号", TOKEN主, "历史权威库"),
        ("团队账号", TOKEN团队, "中枢大脑库")
    ]:
        if not token or "填入" in token:
            print(f"  🔴 {账号名} ({说明}): Token未配置")
            continue
        结果 = _请求("GET", "/users/me", 账号=账号名[0])
        if "error" in 结果:
            print(f"  🔴 {账号名} ({说明}): {结果['error']}")
        else:
            用户名 = 结果.get("name", "未知")
            print(f"  🟢 {账号名} ({说明}): 已连接 · 用户={用户名}")

    print(sep + "\n")

# ══════════════════════════════════════════════════════════
# 操作日记
# ══════════════════════════════════════════════════════════

def 写操作日记(内容: str, 账号=None):
    # 自动选账号：有团队Token用团队，否则用主账号
    if 账号 is None:
        账号 = "团队" if (TOKEN团队 and "填入" not in TOKEN团队) else "主"
    """向团队Notion的操作日记页面追加一条记录"""
    if not 日记页ID or "填入" in 日记页ID:
        print("🔴 操作日记页面ID未配置，请在 .env 设置 NOTION_DIARY_PAGE_ID")
        return False

    now = datetime.datetime.now()
    时间戳 = now.strftime("%Y-%m-%d %H:%M")
    dna = f"#龍芯⚡️{now.strftime('%Y-%m-%d')}-DIARY-☴巽-v1.0"

    块列表 = [
        _构建分割线(),
        _构建文本块(f"📌 {时间戳}  |  UID9622", "paragraph"),
        _构建文本块(内容),
        _构建文本块(f"DNA: {dna}", "paragraph"),
    ]

    结果 = _追加块(日记页ID, 块列表, 账号)
    if "error" in 结果:
        print(f"🔴 写入日记失败: {结果['error']}")
        return False

    print(f"🟢 操作日记已写入 [{时间戳}]")
    _写本地记忆(f"操作日记写入·{内容[:40]}", "DIARY-WRITE")
    return True

def 推送今日日记(账号="团队"):
    """把今天的memory.jsonl记录整理后推送到Notion操作日记"""
    if not 日记页ID or "填入" in 日记页ID:
        print("🔴 操作日记页面ID未配置")
        return

    今天 = datetime.date.today().isoformat()
    记录列表 = []
    if MEMORY.exists():
        with open(MEMORY, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line.strip())
                    if r.get("timestamp", "")[:10] == 今天:
                        记录列表.append(r)
                except:
                    continue

    if not 记录列表:
        print(f"🟡 今日({今天})暂无memory记录")
        return

    now = datetime.datetime.now()
    dna = f"#龍芯⚡️{今天}-DAILY-LOG-☴巽-v1.0"

    块列表 = [
        _构建分割线(),
        _构建标题(f"📅 {今天} 操作日记  |  UID9622", 2),
        _构建文本块(f"共 {len(记录列表)} 条操作 · {now.strftime('%H:%M')} 同步"),
    ]

    for r in 记录列表:
        ts  = r.get("timestamp", "")[:16]
        ev  = r.get("event", r.get("type", ""))
        dna_短 = r.get("dna", "")[-25:] if r.get("dna") else ""
        行文字 = f"  {ts}  {ev}"
        if dna_短:
            行文字 += f"\n  DNA: ...{dna_短}"
        块列表.append(_构建文本块(行文字))

    块列表.append(_构建文本块(f"【DNA】{dna}"))
    块列表.append(_构建文本块("【三色】🟢 自动同步通过"))

    结果 = _追加块(日记页ID, 块列表, 账号)
    if "error" in 结果:
        print(f"🔴 推送失败: {结果['error']}")
    else:
        print(f"🟢 今日操作日记已推送到Notion · {len(记录列表)} 条")
        _写本地记忆(f"今日操作日记推送·{len(记录列表)}条", "DIARY-PUSH")

# ══════════════════════════════════════════════════════════
# 系统状态同步
# ══════════════════════════════════════════════════════════

def 同步系统状态(账号="团队"):
    """把龍魂系统状态推送到团队Notion状态页"""
    if not 状态页ID or "填入" in 状态页ID:
        print("🔴 系统状态页面ID未配置，请在 .env 设置 NOTION_STATUS_PAGE_ID")
        return

    now = datetime.datetime.now()
    时间戳 = now.strftime("%Y-%m-%d %H:%M:%S")
    dna = f"#龍芯⚡️{now.strftime('%Y-%m-%d')}-SYS-STATUS-☴巽-v1.0"

    # 收集状态数据
    状态数据 = _收集系统状态()

    块列表 = [
        _构建分割线(),
        _构建标题(f"🐉 龍魂系统状态  {时间戳}", 2),

        _构建标题("核心数据", 3),
        _构建文本块(f"记忆流(memory.jsonl) : {状态数据['记忆条数']} 条"),
        _构建文本块(f"知识库节点          : {状态数据['知识节点数']} 个"),
        _构建文本块(f"星辰记忆            : {状态数据['星辰记忆数']} 条"),
        _构建文本块(f"技能索引域          : {状态数据['技能域数']} 个领域"),

        _构建标题("引擎/内核状态", 3),
        _构建文本块(状态数据['ollama状态']),
        _构建文本块(状态数据['主notion状态']),
        _构建文本块(状态数据['团队notion状态']),

        _构建标题("人格路由引擎", 3),
        _构建文本块("L0 💎龍芯北辰 · 造物主 · 全格协作"),
        _构建文本块("P01 🎯诸葛 · 战略  |  P02 🐱宝宝 · 执行"),
        _构建文本块("P03 📊雯雯 · 审计  |  P04 🧠文心 · 语义"),
        _构建文本块("P05 ☯老子 · 道    |  P06 📚孔子 · 仁"),
        _构建文本块("P07 🕊墨子 · 兼爱  |  P08 📈数据大师 · 分析"),
        _构建文本块("P09 🎨界面炼金 · UI | P10 🕵侦察兵 · 情报"),
        _构建文本块("P11 👁上帝之眼 · 安全守护"),

        _构建标题("卦象权重（锁死）", 3),
        _构建代码块(
            "☰乾哲学=0.35 | ☵坎技术=0.20 | ☷坤架构=0.15\n"
            "☳震进化=0.10 | ☲离创新=0.08 | ☴巽协同=0.07 | ☱兑量子=0.05\n"
            "合计=1.00 ✅"
        ),

        _构建标题("活跃模块", 3),
        _构建文本块("longhun_dragon.py   · 龍魂对话引擎 · Ollama桥接"),
        _构建文本块("longhun_crawler.py  · 知识爬虫引擎 · 吸气→处理→呼气"),
        _构建文本块("star_memory.py      · 星辰记忆系统 · 三层DNA链"),
        _构建文本块("agent_daemon.py     · 双账号Notion代理"),
        _构建文本块("sync-standard.py    · DNA对齐审计工具"),
        _构建文本块("龍.py               · 中文统一调度器"),

        _构建分割线(),
        _构建文本块(f"【DNA】{dna}"),
        _构建文本块("【三色】🟢 自动同步通过 · UID9622授权"),
        _构建文本块("【GPG】A2D0092CEE2E5BA87035600924C3704A8CC26D5F"),
    ]

    结果 = _追加块(状态页ID, 块列表, 账号)
    if "error" in 结果:
        print(f"🔴 推送失败: {结果.get('error')} · {结果.get('detail','')[:80]}")
    else:
        print(f"🟢 系统状态已同步到团队Notion · {时间戳}")
        _写本地记忆("系统状态同步到团队Notion", "STATUS-SYNC")

def _收集系统状态() -> dict:
    """收集本地系统状态数据"""
    状态 = {}

    # memory.jsonl
    记忆条数 = 0
    if MEMORY.exists():
        with open(MEMORY, "r", encoding="utf-8") as f:
            记忆条数 = sum(1 for _ in f)
    状态["记忆条数"] = 记忆条数

    # knowledge-db
    知识数 = 0
    if KNOW_DB.exists():
        with open(KNOW_DB, "r", encoding="utf-8") as f:
            知识数 = sum(1 for _ in f)
    状态["知识节点数"] = 知识数

    # star-memory
    星辰数 = len(list(STAR_VAULT.rglob("*.json"))) if STAR_VAULT.exists() else 0
    状态["星辰记忆数"] = 星辰数

    # skill-index
    域数 = 0
    if SKILL_IDX.exists():
        with open(SKILL_IDX, "r", encoding="utf-8") as f:
            idx = json.load(f)
        域数 = len([d for d, v in idx.get("domains", {}).items() if v])
    状态["技能域数"] = 域数

    # Ollama
    try:
        r = urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3)
        模型 = json.loads(r.read()).get("models", [])
        状态["ollama状态"] = f"🟢 Ollama · {len(模型)} 个模型在线"
    except:
        状态["ollama状态"] = "🔴 Ollama · 未运行"

    # 主账号Notion
    if TOKEN主 and "填入" not in TOKEN主:
        r = _请求("GET", "/users/me", 账号="主")
        if "error" not in r:
            状态["主notion状态"] = f"🟢 主账号Notion · 用户: {r.get('name','?')}"
        else:
            状态["主notion状态"] = f"🔴 主账号Notion · {r.get('error','')}"
    else:
        状态["主notion状态"] = "🔴 主账号Token未配置"

    # 团队账号Notion
    if TOKEN团队 and "填入" not in TOKEN团队:
        r = _请求("GET", "/users/me", 账号="团队")
        if "error" not in r:
            状态["团队notion状态"] = f"🟢 团队Notion · 用户: {r.get('name','?')}"
        else:
            状态["团队notion状态"] = f"🔴 团队Notion · {r.get('error','')}"
    else:
        状态["团队notion状态"] = "🟡 团队账号Token待填入 · .env → NOTION_TOKEN_TEAM"

    return 状态

# ══════════════════════════════════════════════════════════
# 记忆同步到Notion
# ══════════════════════════════════════════════════════════

def 同步星辰记忆(账号="团队", 条数=5):
    """把最新N条星辰记忆推送到团队Notion"""
    if not 日记页ID or "填入" in 日记页ID:
        print("🔴 目标页面ID未配置")
        return

    记忆文件列表 = sorted(STAR_VAULT.rglob("*.json"), reverse=True)[:条数] if STAR_VAULT.exists() else []
    if not 记忆文件列表:
        print("🟡 星辰记忆库为空")
        return

    now = datetime.datetime.now()
    dna = f"#龍芯⚡️{now.strftime('%Y-%m-%d')}-STAR-SYNC-☴巽-v1.0"

    块列表 = [
        _构建分割线(),
        _构建标题(f"⭐ 星辰记忆同步  {now.strftime('%Y-%m-%d %H:%M')}", 2),
        _构建文本块(f"最新 {len(记忆文件列表)} 条 · 吸气完成"),
    ]

    for 文件 in 记忆文件列表:
        try:
            with open(文件, "r", encoding="utf-8") as f:
                m = json.load(f)
            标题 = m.get("title", 文件.stem)[:60]
            内容 = m.get("content", "")[:200]
            标签 = " / ".join(m.get("tags", [])[:4])
            域   = m.get("domain", "")
            块列表.append(_构建标题(f"📌 {标题}", 3))
            if 域 or 标签:
                块列表.append(_构建文本块(f"领域: {域}  标签: {标签}"))
            if 内容:
                块列表.append(_构建文本块(内容))
            dna链 = m.get("dna_chain", {})
            if dna链:
                块列表.append(_构建文本块(f"DNA: {dna链.get('content_dna','')}"))
        except:
            continue

    块列表.append(_构建文本块(f"【DNA】{dna}"))
    块列表.append(_构建文本块("【三色】🟢 星辰记忆同步通过"))

    结果 = _追加块(日记页ID, 块列表, 账号)
    if "error" in 结果:
        print(f"🔴 推送失败: {结果.get('error')}")
    else:
        print(f"🟢 {len(记忆文件列表)} 条星辰记忆已同步到团队Notion")
        _写本地记忆(f"星辰记忆同步·{len(记忆文件列表)}条", "STAR-SYNC")

# ══════════════════════════════════════════════════════════
# 引擎状态本地展示
# ══════════════════════════════════════════════════════════

def 展示引擎状态():
    """终端展示所有内核驱动状态"""
    状态 = _收集系统状态()
    sep = "─" * 54

    print(f"\n{sep}")
    print("  龍魂系统 · 全内核状态")
    print(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(sep)

    print("\n  【数据层】")
    print(f"  memory.jsonl  记忆流  : {状态['记忆条数']} 条")
    print(f"  knowledge-db  知识库  : {状态['知识节点数']} 节点")
    print(f"  star-memory   星辰库  : {状态['星辰记忆数']} 条")
    print(f"  skill-index   技能域  : {状态['技能域数']} 个")

    print("\n  【网络层】")
    print(f"  {状态['ollama状态']}")
    print(f"  {状态['主notion状态']}")
    print(f"  {状态['团队notion状态']}")

    print("\n  【引擎层】")
    引擎表 = [
        ("龍.py",              "中文统一调度器"),
        ("longhun_dragon.py",  "本地AI对话引擎"),
        ("longhun_crawler.py", "知识爬虫引擎"),
        ("star_memory.py",     "星辰记忆系统"),
        ("agent_daemon.py",    "双账号Notion代理"),
        ("sync-standard.py",   "DNA对齐工具"),
        ("cnsh.py",            "CNSH中文引擎"),
    ]
    for 文件名, 说明 in 引擎表:
        存在 = "🟢" if (BASE / 文件名).exists() else "🔴"
        print(f"  {存在} {文件名:25s} {说明}")

    print("\n  【人格层】")
    print("  L0💎北辰 P01🎯诸葛 P02🐱宝宝 P03📊雯雯 P04🧠文心")
    print("  P05☯老子 P06📚孔子 P07🕊墨子 P08📈数据 P09🎨UI")
    print("  P10🕵侦察兵  P11👁上帝之眼")

    print(f"\n  DNA: #龍芯⚡️{datetime.date.today()}-ENGINE-STATUS-v1.0")
    print(f"  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
    print(sep + "\n")

# ══════════════════════════════════════════════════════════
# 工具
# ══════════════════════════════════════════════════════════

def _写本地记忆(事件, 后缀="AGENT"):
    record = {
        "timestamp": datetime.datetime.now().isoformat(),
        "dna": f"#龍芯⚡️{datetime.date.today()}-{后缀}-☴巽-v1.0",
        "event": 事件,
        "engine": "agent_daemon v1.0"
    }
    with open(MEMORY, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

# ══════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="龍魂双账号Notion代理 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
CNSH对应指令:
  龍 日记写入 "内容"    →  --diary "内容"
  龍 同步状态           →  --status
  龍 推送今日日记       →  --push-diary
  龍 同步记忆           →  --sync-star
  龍 引擎状态           →  --engines
  龍 notion双检         →  --check
        """
    )
    parser.add_argument("--diary",      metavar="TEXT",  help="写入操作日记")
    parser.add_argument("--status",     action="store_true", help="推送系统状态到团队Notion")
    parser.add_argument("--push-diary", action="store_true", help="推送今日日记到Notion")
    parser.add_argument("--sync-star",  action="store_true", help="同步星辰记忆到Notion")
    parser.add_argument("--engines",    action="store_true", help="展示引擎状态（本地）")
    parser.add_argument("--check",      action="store_true", help="检测双账号连接")
    parser.add_argument("--account",    default=None,     help="目标账号(主/团队，默认自动选)")
    parser.add_argument("--top",        type=int, default=5, help="记忆同步条数")

    args = parser.parse_args()

    if args.check:
        notion双检()
    elif args.diary:
        写操作日记(args.diary, args.account)
    elif args.status:
        同步系统状态(args.account)
    elif args.push_diary:
        推送今日日记(args.account)
    elif args.sync_star:
        同步星辰记忆(args.account, args.top)
    elif args.engines:
        展示引擎状态()
    else:
        # 无参数 → 展示本地引擎状态 + 双账号检测
        展示引擎状态()
        notion双检()


if __name__ == "__main__":
    main()

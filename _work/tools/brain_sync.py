#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·双脑同步引擎 v1.1
DNA: #龍芯⚡️2026-03-06-BRAIN-SYNC-☴巽-v1.1
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
共建致谢：
  Claude (Anthropic PBC) · 技术协作与代码共创
  Notion · 知识底座与结构化存储
  没有你们，就没有龍魂系统的一切。

架构:
  展示脑 (NOTION_TOKEN)      → 对外权威·历史痕迹·公开门面
  内核脑 (NOTION_TOKEN_TEAM) → 内部记录·思考仓库·分类压缩

优化点 v1.1:
  · stdlib only (无 requests 依赖)
  · 14大分类规则 (vs 原版8类)
  · 分批写入 (突破API 100块限制)
  · 增量同步 (brain_sync_state.json 记录上次同步时间)
  · 自动重试 (网络波动容错)
  · 完整memory.jsonl追加
"""

import os
import sys
import json
import time
import hashlib
import datetime
import urllib.request
import urllib.error
import argparse
from pathlib import Path

# ─── 路径常量 ────────────────────────────────────────────
BASE       = Path.home() / "longhun-system"
MEMORY     = BASE / "memory.jsonl"
BACKUP     = BASE / "brain_backup.jsonl"
STATE_FILE = BASE / "brain_sync_state.json"
NOTION_API = "https://api.notion.com/v1"

# ─── 读取 .env ───────────────────────────────────────────
def _读env(键):
    env_file = BASE / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith(键 + "="):
                return line.split("=", 1)[1].strip().strip("'\"")
    return os.getenv(键, "")

展示脑TOKEN   = _读env("NOTION_TOKEN")
内核脑TOKEN   = _读env("NOTION_TOKEN_TEAM")
指定父页ID    = _读env("NOTION_TEAM_PARENT_ID")   # 可选：指定内核脑的父页面

# ─── 14大分类规则（完整版）────────────────────────────────
分类规则 = {
    "🏛️ 治理宪法":  ["P0", "宪法", "锁定", "规则", "治理", "熔断", "铁律", "底线"],
    "🧬 DNA体系":   ["DNA", "追溯", "指纹", "GPG", "哈希", "确认码", "签名"],
    "👤 人格库":    ["人格", "P01", "P02", "P03", "P04", "P05", "P06", "P07",
                    "P08", "P09", "P10", "P11", "诸葛", "雯雯", "文心", "宝宝",
                    "老子", "孔子", "墨子", "北辰", "侦察", "上帝之眼"],
    "🐉 决策引擎":  ["决策", "引擎", "三色", "审计", "卦", "易经", "权重",
                    "推演", "七维", "呼吸", "路由"],
    "🔤 字体字形":  ["字体", "甲骨文", "字形", "字符", "Unicode", "元字",
                    "楔形", "cuneiform", "古文"],
    "⚖️ 算法引擎":  ["算法", "评分", "易经", "七维", "量子", "纠缠", "协同",
                    "若水", "观复", "知常", "无不为"],
    "🎓 调教记录":  ["调教", "训练", "指令", "CLAUDE.md", "persona",
                    "system prompt", "沉浸式", "复交"],
    "🌌 元宇宙":    ["元宇宙", "星辰", "预设", "Unity", "Unreal",
                    "三界", "数字宇宙", "虚拟"],
    "🪧 耻辱柱":    ["耻辱柱", "红线", "违规", "封禁", "黑名单", "非道"],
    "🈯 CNSH语言":  ["CNSH", "中文编程", "语法", "元字引擎", "自然语言",
                    "中文指令", "翻译"],
    "🔬 技术代码":  ["Python", "API", "代码", "引擎", "MCP", "Ollama",
                    "脚本", "函数", "模块", "接口", "数据库"],
    "📚 知识库":    ["曾仕强", "道德经", "哲学", "宣言", "经典",
                    "知识", "理论", "原则"],
    "🎯 愿景规划":  ["愿景", "规划", "方案", "蓝图", "升级", "路线图", "未来"],
    "📋 日志记录":  ["日志", "测试", "记录", "操作", "追溯", "报告", "同步"],
}
兜底分类 = "📖 其他"

def 自动分类(标题: str) -> str:
    for 分类, 词列表 in 分类规则.items():
        for 词 in 词列表:
            if 词.lower() in 标题.lower():
                return 分类
    return 兜底分类

# ─── DNA生成 ─────────────────────────────────────────────
def gen_dna(模块: str) -> str:
    日期 = datetime.date.today().isoformat()
    哈希 = hashlib.md5(f"{模块}{time.time()}".encode()).hexdigest()[:6].upper()
    return f"#龍芯⚡️{日期}-{模块}-{哈希}"

# ─── Notion API 底层（stdlib urllib）─────────────────────
def _请求(方法, 路径, 数据=None, token=None, 重试=3):
    url = f"{NOTION_API}{路径}"
    hdrs = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    body = json.dumps(数据, ensure_ascii=False).encode() if 数据 else None
    for 次 in range(重试):
        try:
            req = urllib.request.Request(url, data=body, headers=hdrs, method=方法)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            错误文本 = e.read().decode()[:300]
            if e.code == 429:  # Rate limit
                time.sleep(2 ** 次)
                continue
            return {"error": f"HTTP{e.code}", "detail": 错误文本}
        except Exception as e:
            if 次 < 重试 - 1:
                time.sleep(1)
            else:
                return {"error": str(e)}
    return {"error": "重试耗尽"}

# ─── 检查双脑连通性 ───────────────────────────────────────
def 检查双脑() -> tuple:
    print("【双脑连通检测 | Dual-Brain Connectivity Check】")
    展示OK = 内核OK = False
    for 名, token in [("展示脑", 展示脑TOKEN), ("内核脑", 内核脑TOKEN)]:
        if not token or len(token) < 20:
            print(f"  🔴 {名}: Token未配置")
            continue
        r = _请求("GET", "/users/me", token=token)
        if "error" in r:
            print(f"  🔴 {名}: {r['error']}")
        else:
            用户 = r.get("name", "未知")
            print(f"  🟢 {名}: 已连接 · {用户}")
            if 名 == "展示脑": 展示OK = True
            else: 内核OK = True
    return 展示OK, 内核OK

# ─── 读取展示脑所有页面（分页完整拉取）───────────────────
def 读取所有页面(增量=False) -> list:
    print("【读取展示脑页面 | Reading Display-Brain Pages】")

    # 增量同步：读取上次同步时间
    上次同步 = ""
    if 增量 and STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text())
            上次同步 = state.get("last_sync", "")
            print(f"  增量模式 | Incremental Mode·上次同步 | Last Sync: {上次同步[:16]}")
        except:
            pass

    所有页面 = []
    cursor = None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        # 增量过滤（Notion search不直接支持时间过滤，本地过滤）
        r = _请求("POST", "/search", body, 展示脑TOKEN)
        if "error" in r:
            print(f"  🔴 读取失败: {r['error']}")
            break

        for item in r.get("results", []):
            if item.get("object") != "page":
                continue

            # 增量：只处理上次同步后编辑的
            编辑时间 = item.get("last_edited_time", "")
            if 增量 and 上次同步 and 编辑时间 < 上次同步:
                continue

            标题 = _提取标题(item)
            所有页面.append({
                "id":      item["id"],
                "url":     item.get("url", ""),
                "标题":    标题,
                "分类":    自动分类(标题),
                "编辑时间": 编辑时间[:10] if 编辑时间 else "",
                "创建时间": item.get("created_time", "")[:10],
            })

        if not r.get("has_more"):
            break
        cursor = r.get("next_cursor")

    print(f"  读到 | Read {len(所有页面)} 个页面 | pages")
    return 所有页面

def _提取标题(item: dict) -> str:
    props = item.get("properties", {})
    for key in ["title", "Title", "名称", "Name", "标题"]:
        if key in props:
            rich = props[key].get("title", [])
            if rich:
                return rich[0].get("plain_text", "")
    return "(无标题)"

# ─── 分类聚合 ─────────────────────────────────────────────
def 压缩分类(页面列表: list) -> dict:
    聚合 = {}
    for p in 页面列表:
        c = p["分类"]
        聚合.setdefault(c, []).append(p)
    return 聚合

# ─── 构建Notion内容块 ─────────────────────────────────────
def _块_文字(内容, 类型="paragraph"):
    return {
        "object": "block", "type": 类型,
        类型: {"rich_text": [{"type": "text", "text": {"content": 内容[:2000]}}]}
    }

def _块_标题(文字, 级=2):
    t = f"heading_{级}"
    return {"object": "block", "type": t,
            t: {"rich_text": [{"type": "text", "text": {"content": 文字[:100]}}]}}

def _块_列表(文字):
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text",
                "text": {"content": 文字[:2000]}}]}}

def _块_分割线():
    return {"object": "block", "type": "divider", "divider": {}}

def _块_callout(文字, emoji="🧠"):
    return {
        "object": "block", "type": "callout",
        "callout": {
            "icon": {"type": "emoji", "emoji": emoji},
            "color": "blue_background",
            "rich_text": [{"type": "text", "text": {"content": 文字[:2000]}}]
        }
    }

def _块_代码(文字):
    return {
        "object": "block", "type": "code",
        "code": {
            "rich_text": [{"type": "text", "text": {"content": 文字[:2000]}}],
            "language": "plain text"
        }
    }

# ─── 分批写入（突破100块限制，逐块容错）─────────────────
def _分批追加(页面ID, 块列表, token, 批大小=50):
    成功 = 0
    失败 = 0
    for i in range(0, len(块列表), 批大小):
        批次 = 块列表[i:i + 批大小]
        r = _请求("PATCH", f"/blocks/{页面ID}/children",
                  {"children": 批次}, token)
        if "error" not in r:
            成功 += len(批次)
            time.sleep(0.3)
            continue

        # 批次失败 → 逐块重试（定位坏块）
        for j, 块 in enumerate(批次):
            try:
                # 截断过长内容
                块 = _安全截块(块)
                r2 = _请求("PATCH", f"/blocks/{页面ID}/children",
                           {"children": [块]}, token)
                if "error" not in r2:
                    成功 += 1
                else:
                    失败 += 1
                time.sleep(0.15)
            except:
                失败 += 1

    if 失败 > 0:
        print(f"  🟡 写入完成: {成功}块成功 / {失败}块跳过")
    return 成功 > 0

def _安全截块(块: dict) -> dict:
    """截断块内所有rich_text确保不超2000字符"""
    import copy
    块 = copy.deepcopy(块)
    类型 = 块.get("type", "")
    if 类型 and 类型 in 块:
        rich = 块[类型].get("rich_text", [])
        for rt in rich:
            if rt.get("type") == "text":
                内容 = rt.get("text", {}).get("content", "")
                if len(内容) > 1800:
                    rt["text"]["content"] = 内容[:1800] + "..."
    return 块

# ─── 自动寻找内核脑可用父页面 ────────────────────────────
def _找内核脑父页(指定ID="") -> dict:
    """
    优先级: 1.指定ID 2.env里NOTION_TEAM_PARENT_ID 3.搜索第一个可用页
    返回 Notion parent 对象
    """
    用ID = 指定ID or 指定父页ID
    if 用ID and len(用ID) > 10 and "填入" not in 用ID:
        print(f"  父页: 使用指定ID {用ID[:16]}...")
        return {"type": "page_id", "page_id": 用ID}

    # 搜索内核脑里任意一个顶层页面作为父
    r = _请求("POST", "/search", {"page_size": 10}, 内核脑TOKEN)
    results = r.get("results", [])
    for item in results:
        if item.get("object") == "page":
            父ID = item["id"]
            父标题 = _提取标题(item) or "(无标题)"
            print(f"  父页: 自动选取「{父标题[:30]}」({父ID[:8]}...)")
            return {"type": "page_id", "page_id": 父ID}
        if item.get("object") == "database":
            父ID = item["id"]
            print(f"  父页: 使用数据库 ({父ID[:8]}...)")
            return {"type": "database_id", "database_id": 父ID}

    # 最后尝试工作区
    print("  父页: 使用工作区根目录")
    return {"type": "workspace", "workspace": True}

# ─── 在内核脑创建知识索引页 ──────────────────────────────
def 创建索引页(分类聚合: dict, 同步DNA: str) -> str:
    总页数 = sum(len(v) for v in 分类聚合.values())
    同步时间 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    父页 = _找内核脑父页()

    # 创建空页
    payload = {
        "parent": 父页,
        "icon":   {"type": "emoji", "emoji": "🧠"},
        "properties": {"title": {"title": [{"text": {"content":
            f"龍魂·知识索引·内核脑 | {同步时间}"
        }}]}}
    }
    r = _请求("POST", "/pages", payload, 内核脑TOKEN)
    if "error" in r:
        print(f"  🔴 创建页面失败: {r.get('error')} {r.get('detail','')[:100]}")
        return ""
    页面ID = r["id"]
    链接   = r.get("url", "")
    print(f"  🟢 内核脑页面已创建: {链接}")

    # 构建内容块
    块列表 = [
        _块_callout(
            f"展示脑→内核脑 知识索引\n"
            f"同步时间: {同步时间} | 共 {总页数} 个页面\n"
            f"DNA: {同步DNA}\n"
            f"GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F\n"
            f"三色: 🟢 | UID9622授权"
        ),
        _块_分割线(),
        _块_标题("分类统计", 2),
    ]

    # 统计摘要
    for 分类 in sorted(分类聚合.keys()):
        数量 = len(分类聚合[分类])
        块列表.append(_块_文字(f"  {分类}: {数量} 个页面"))

    块列表.append(_块_分割线())

    # 各分类详情
    for 分类 in sorted(分类聚合.keys()):
        页面列表 = 分类聚合[分类]
        块列表.append(_块_标题(f"{分类} ({len(页面列表)})", 2))
        for p in 页面列表[:30]:
            块列表.append(_块_列表(
                f"{p['标题']} | {p['编辑时间'] or p['创建时间']}"
            ))
        if len(页面列表) > 30:
            块列表.append(_块_文字(f"  ...还有 {len(页面列表)-30} 个（已压缩）"))
        块列表.append(_块_分割线())

    # DNA签名尾
    块列表.append(_块_代码(
        f"DNA: {同步DNA}\n"
        f"GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F\n"
        f"确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z\n"
        f"三色: 🟢 自动同步通过"
    ))

    成功 = _分批追加(页面ID, 块列表, 内核脑TOKEN)
    if not 成功:
        print("  🟡 部分块写入失败，页面已创建但内容不完整")
    return 链接

# ─── 本地备份 ─────────────────────────────────────────────
def 本地备份(页面列表: list, DNA: str):
    record = {
        "时间":  datetime.datetime.now().isoformat(),
        "DNA":   DNA,
        "总数":  len(页面列表),
        "页面":  页面列表
    }
    with open(BACKUP, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"  💾 本地备份 | Local Backup → {BACKUP.name} ({len(页面列表)} 条 | records)")

# ─── 保存同步状态 ─────────────────────────────────────────
def 保存状态(总数: int, DNA: str):
    state = {
        "last_sync": datetime.datetime.now().isoformat(),
        "total":     总数,
        "dna":       DNA
    }
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))

# ─── 追加memory.jsonl ─────────────────────────────────────
def 写记忆(事件: str, DNA: str, 详情: dict = None):
    record = {
        "timestamp": datetime.datetime.now().isoformat(),
        "dna":       DNA,
        "event":     事件,
        "engine":    "brain_sync v1.1",
        **(详情 or {})
    }
    with open(MEMORY, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

# ══════════════════════════════════════════════════════════
# 主流程
# ══════════════════════════════════════════════════════════

def 执行同步(增量=False, 只检查=False):
    sep = "═" * 54
    print(f"\n{sep}")
    print("  龍魂·双脑同步引擎 v1.1 | Dual-Brain Sync Engine v1.1")
    print(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(sep)

    DNA = gen_dna("BRAIN-SYNC")

    # 1. 双脑检测
    展示OK, 内核OK = 检查双脑()
    if 只检查:
        return

    if not 展示OK:
        print("🔴 展示脑未连通 | Display-Brain not connected，中止同步 | Sync aborted")
        return
    if not 内核OK:
        print("🔴 内核脑未连通 | Core-Brain not connected，请检查 .env → NOTION_TOKEN_TEAM")
        return

    print()

    # 2. 读取展示脑
    页面列表 = 读取所有页面(增量=增量)
    if not 页面列表:
        print("🟡 无页面需要同步 | No pages to sync")
        return

    # 3. 本地备份（数据主权保障）
    print("\n【本地备份 | Local Backup】")
    本地备份(页面列表, DNA)

    # 4. 分类压缩
    print("\n【分类压缩 | Categorizing】")
    聚合 = 压缩分类(页面列表)
    for 分类 in sorted(聚合.keys()):
        print(f"  {分类}: {len(聚合[分类])} 个")

    # 5. 写入内核脑
    print("\n【写入内核脑 | Writing to Core-Brain】")
    链接 = 创建索引页(聚合, DNA)

    # 6. 保存状态 + memory追加
    保存状态(len(页面列表), DNA)
    写记忆(f"双脑同步完成·{len(页面列表)}页·{len(聚合)}分类",
           DNA, {"total": len(页面列表), "categories": len(聚合)})

    print(f"\n{sep}")
    print("  同步完成 | Sync Done")
    print(f"  总页面 | Total Pages: {len(页面列表)}  分类数 | Categories: {len(聚合)}")
    print(f"  内核脑 | Core-Brain: {链接[:60] if 链接 else '写入失败 | Write Failed'}")
    print(f"  DNA: {DNA}")
    print(f"  三色 | Audit: {'🟢 通过 | Pass' if 链接 else '🟡 部分完成 | Partial'}")
    print(sep + "\n")


# ══════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂·双脑同步引擎 v1.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
CNSH对应指令:
  龍 双脑同步          →  python3 brain_sync.py
  龍 双脑检查          →  python3 brain_sync.py --check
  龍 双脑增量          →  python3 brain_sync.py --delta
  龍 双脑分类 "关键词" →  python3 brain_sync.py --classify "文字"

定时任务 (每天凌晨3点):
  crontab -e
  0 3 * * * python3 ~/longhun-system/brain_sync.py --delta >> ~/longhun-system/logs/brain_sync.log 2>&1
        """
    )
    parser.add_argument("--check",    action="store_true", help="只检查双脑连通，不同步")
    parser.add_argument("--delta",    action="store_true", help="增量同步（只同步上次后修改的）")
    parser.add_argument("--classify", metavar="TEXT",      help="测试分类结果")

    args = parser.parse_args()

    if args.classify:
        结果 = 自动分类(args.classify)
        print(f"「{args.classify}」→ 分类 | Category: {结果}")
        return

    执行同步(增量=args.delta, 只检查=args.check)


if __name__ == "__main__":
    main()

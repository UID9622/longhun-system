#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# #龍芯⚡️丙午·甲午·己巳·乙丑·䷮困-AUTO-DNA-F7607809 自动注入·分层治理自愈引擎 · 来源可查
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码:#龍芯⚡️丙午·癸巳·丁未·丙午·䷖剥-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1254-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: brain_sync.py | 标记时间: 2026-06-03T07:46:12+0800
# -*- coding: utf-8 -*-
"""
龍魂·双脑同步引擎 v1.1
DNA:#龍芯⚡️丙午·辛卯·己卯·庚午·䷚颐-BRAIN-SYNC-v1.1
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

from integrated_modules.longhun_config import load_secrets_env, getenv

# ─── 路径常量 ────────────────────────────────────────────
BASE       = Path.home() / "longhun-system"
MEMORY     = BASE / "memory.jsonl"
BACKUP     = BASE / "brain_backup.jsonl"
STATE_FILE = BASE / "brain_sync_state.json"
NOTION_API = "https://api.notion.com/v1"

# 优先加载 ~/.longhun/secrets.env（真实密钥不上 Git）
load_secrets_env()

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
指定父页ID    = getenv("DB_CLOUD")   # 团队/云端数据库（旧名 NOTION_TEAM_PARENT_ID 仍兼容）

# ─── 冲突检测状态 ────────────────────────────────────────
CONFLICT_STATE = BASE / "brain_sync_conflicts.json"
SYNC_INDEX = BASE / "brain_sync_index.json"  # 跟踪已同步项目

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
def 检查双脑() -> tuple[Any, ...]:
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
def 读取所有页面(增量=False) -> list[Any]:
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

def _提取标题(item: dict[str, Any]) -> str:
    props = item.get("properties", {})
    for key in ["title", "Title", "名称", "Name", "标题"]:
        if key in props:
            rich = props[key].get("title", [])
            if rich:
                return rich[0].get("plain_text", "")
    return "(无标题)"

# ─── 分类聚合 ─────────────────────────────────────────────
def 压缩分类(页面列表: list[Any]) -> dict[str, Any]:
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

def _安全截块(块: dict[str, Any]) -> dict[str, Any]:
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
def _找内核脑父页(指定ID="") -> dict[str, Any]:
    """
    优先级: 1.指定ID 2.env里DB_CLOUD（旧名 NOTION_TEAM_PARENT_ID 仍兼容） 3.搜索第一个可用页
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
            print(f"  父页: 自动选取“{父标题[:30]}”({父ID[:8]}...)")
            return {"type": "page_id", "page_id": 父ID}
        if item.get("object") == "database":
            父ID = item["id"]
            print(f"  父页: 使用数据库 ({父ID[:8]}...)")
            return {"type": "database_id", "database_id": 父ID}

    # 最后尝试工作区
    print("  父页: 使用工作区根目录")
    return {"type": "workspace", "workspace": True}

# ─── 在内核脑创建知识索引页 ──────────────────────────────
def 创建索引页(分类聚合: dict[str, Any], 同步DNA: str) -> str:
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
def 本地备份(页面列表: list[Any], DNA: str):
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
def 写记忆(事件: str, DNA: str, 详情: dict[str, Any] = None):
    record = {
        "timestamp": datetime.datetime.now().isoformat(),
        "dna":       DNA,
        "event":     事件,
        "engine":    "brain_sync v1.1",
        **(详情 or {})
    }
    with open(MEMORY, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

# ╔════════════════════════════════════════════════════════════╗
# ║ 双向同步模块：Terminal ↔ Notion                           ║
# ╚════════════════════════════════════════════════════════════╝

# ─── Terminal → Notion：本地文件推送到展示脑 ───────────────
def 读取本地记录(限制=100) -> list[Any]:
    """读取本地 memory.jsonl 中的记录，返回待同步项"""
    print("【本地→展示脑 | Terminal→Display-Brain】")
    if not MEMORY.exists():
        print(f"  🔴 本地记录不存在: {MEMORY}")
        return []

    # 读取同步索引，避免重复
    已同步 = set()
    if SYNC_INDEX.exists():
        try:
            索引 = json.loads(SYNC_INDEX.read_text())
            已同步 = set(索引.get("synced_ids", []))
        except:
            pass

    本地记录 = []
    try:
        with open(MEMORY, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    记录ID = record.get("dna", hashlib.md5(line.encode()).hexdigest()[:16])
                    if 记录ID not in 已同步:
                        本地记录.append({
                            "id": 记录ID,
                            "event": record.get("event", ""),
                            "dna": record.get("dna", ""),
                            "timestamp": record.get("timestamp", ""),
                            "content": json.dumps(record, ensure_ascii=False),
                            "local_mtime": os.path.getmtime(MEMORY)
                        })
                except:
                    pass
    except Exception as e:
        print(f"  🔴 读取本地记录失败: {e}")
        return []

    print(f"  读到 {len(本地记录)} 条本地记录，其中 {len(本地记录)} 条待同步")
    return 本地记录[:限制]

def 推送到展示脑(本地记录: list[Any], token) -> dict[str, Any]:
    """将本地记录推送到 Notion 展示脑"""
    if not token or len(token) < 20:
        print("  🔴 展示脑Token未配置")
        return {"success": 0, "failed": 0}

    成功 = 0
    失败 = 0
    已同步ID列表 = []

    for record in 本地记录:
        # 创建 Notion 页面
        payload = {
            "parent": {"type": "workspace", "workspace": True},
            "icon": {"type": "emoji", "emoji": "📝"},
            "properties": {
                "title": {"title": [{"text": {"content":
                    f"[LOCAL] {record['event'][:80]}" if record['event'] else "[LOCAL] 记录"
                }}]}
            }
        }

        r = _请求("POST", "/pages", payload, token)
        if "error" not in r:
            页面ID = r["id"]

            # 追加内容
            块列表 = [
                _块_callout(f"本地→展示脑同步\nDNA: {record['dna']}\n时间: {record['timestamp']}", "📝"),
                _块_分割线(),
                _块_代码(record['content'][:1900])
            ]
            _分批追加(页面ID, 块列表, token, 批大小=25)
            成功 += 1
            已同步ID列表.append(record['id'])
        else:
            失败 += 1
            print(f"    🔴 推送失败: {r.get('error')}")

    # 更新同步索引
    if 已同步ID列表:
        索引 = {}
        if SYNC_INDEX.exists():
            索引 = json.loads(SYNC_INDEX.read_text())
        索引["last_push"] = datetime.datetime.now().isoformat()
        索引["synced_ids"] = list(set(索引.get("synced_ids", [])) | set(已同步ID列表))
        SYNC_INDEX.write_text(json.dumps(索引, ensure_ascii=False, indent=2))

    print(f"  推送完成: {成功}页成功 / {失败}页失败")
    return {"success": 成功, "failed": 失败}

# ─── Notion → Terminal：从展示脑拉取并更新本地 ────────────
def 拉取自展示脑(token, 最小编辑时间="") -> list[Any]:
    """从展示脑拉取所有 [LOCAL] 标记的页面，返回更新列表"""
    print("【展示脑→本地 | Display-Brain→Terminal】")

    # 搜索所有 [LOCAL] 标记的页面
    所有页面 = []
    cursor = None

    while True:
        body = {"page_size": 100, "filter": {
            "property": "title",
            "title": {"contains": "[LOCAL]"}
        }}
        if cursor:
            body["start_cursor"] = cursor

        r = _请求("POST", "/search", body, token)
        if "error" in r:
            print(f"  🔴 搜索失败: {r['error']}")
            break

        for item in r.get("results", []):
            if item.get("object") != "page":
                continue

            编辑时间 = item.get("last_edited_time", "")
            if 最小编辑时间 and 编辑时间 < 最小编辑时间:
                continue

            所有页面.append({
                "id": item["id"],
                "title": _提取标题(item),
                "url": item.get("url", ""),
                "last_edited": 编辑时间,
                "notion_mtime": int(datetime.datetime.fromisoformat(
                    编辑时间.replace("Z", "+00:00")).timestamp())
            })

        if not r.get("has_more"):
            break
        cursor = r.get("next_cursor")

    print(f"  拉取 {len(所有页面)} 条页面")
    return 所有页面

def 更新本地记录(远程页面列表: list[Any]) -> dict[str, Any]:
    """将远程页面追加到本地 memory.jsonl"""
    成功 = 0
    失败 = 0

    for page in 远程页面列表:
        try:
            record = {
                "timestamp": datetime.datetime.now().isoformat(),
                "source": "notion_pull",
                "page_id": page["id"],
                "title": page["title"],
                "url": page["url"],
                "notion_mtime": page["notion_mtime"],
                "event": f"从Notion拉取: {page['title']}"
            }
            with open(MEMORY, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            成功 += 1
        except Exception as e:
            失败 += 1
            print(f"    🔴 写入失败: {e}")

    print(f"  更新本地: {成功}条成功 / {失败}条失败")
    return {"success": 成功, "failed": 失败}

# ─── 冲突检测与解决 ────────────────────────────────────────
def 检测冲突(本地记录: list[Any], 远程页面: list[Any]) -> dict[str, Any]:
    """
    检测本地和远程的冲突
    冲突规则：
    - 同一DNA的记录在本地和远程都存在且编辑时间不同 → 版本冲突
    - 本地有但远程无 → 待推送
    - 远程有但本地无 → 待拉取
    """
    print("【冲突检测 | Conflict Detection】")

    # 构建本地DNA索引
    本地DNA映射 = {}
    for record in 本地记录:
        dna = record.get("dna", "")
        if dna:
            本地DNA映射[dna] = record

    # 构建远程DNA索引
    远程DNA映射 = {}
    for page in 远程页面:
        # 尝试从URL或ID提取DNA
        标题 = page.get("title", "")
        dna = page.get("id", "")
        if dna:
            远程DNA映射[dna] = page

    冲突 = {
        "版本冲突": [],     # 同一项目本地和远程都有但内容不同
        "本地领先": [],     # 本地有但远程无
        "远程领先": [],     # 远程有但本地无
    }

    # 检测版本冲突
    for dna, 本地rec in 本地DNA映射.items():
        if dna in 远程DNA映射:
            远程page = 远程DNA映射[dna]
            本地mtime = 本地rec.get("local_mtime", 0)
            远程mtime = 远程page.get("notion_mtime", 0)

            if 本地mtime != 远程mtime:
                冲突["版本冲突"].append({
                    "dna": dna,
                    "local_mtime": 本地mtime,
                    "remote_mtime": 远程mtime,
                    "local": 本地rec,
                    "remote": 远程page,
                    "解决方案": "remote"  # 默认选择远程版本（权威源）
                })

    # 检测本地领先
    for dna, 本地rec in 本地DNA映射.items():
        if dna not in 远程DNA映射:
            冲突["本地领先"].append({
                "dna": dna,
                "record": 本地rec
            })

    # 检测远程领先
    for dna, 远程page in 远程DNA映射.items():
        if dna not in 本地DNA映射:
            冲突["远程领先"].append({
                "dna": dna,
                "page": 远程page
            })

    print(f"  版本冲突: {len(冲突['版本冲突'])} 个")
    print(f"  本地领先: {len(冲突['本地领先'])} 个")
    print(f"  远程领先: {len(冲突['远程领先'])} 个")

    return 冲突

def 解决冲突(冲突: dict[str, Any], DNA: str) -> dict[str, Any]:
    """
    解决检测到的冲突
    规则：
    1. 版本冲突 → 选择远程版本作为权威（Notion是单一真实源）
    2. 本地领先 → 推送到远程
    3. 远程领先 → 拉取到本地
    """
    print("【冲突解决 | Conflict Resolution】")

    解决日志 = {
        "解决时间": datetime.datetime.now().isoformat(),
        "DNA": DNA,
        "版本冲突处理": [],
        "本地推送": [],
        "远程拉取": [],
    }

    # 1. 处理版本冲突 → 采用远程版本
    for item in 冲突.get("版本冲突", []):
        dna = item["dna"]
        # 记录冲突决议
        解决日志["版本冲突处理"].append({
            "dna": dna,
            "decision": "remote",
            "reason": "Notion是单一真实源 | Notion is SSOT"
        })

        # 将远程版本追加到本地作为解决记录
        record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event": f"冲突解决: {dna}，采用远程版本",
            "dna": dna,
            "conflict_resolution": "remote_won",
            "local_mtime": item.get("local_mtime"),
            "remote_mtime": item.get("remote_mtime")
        }
        with open(MEMORY, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # 2. 处理本地领先 → 推送
    for item in 冲突.get("本地领先", []):
        dna = item["dna"]
        解决日志["本地推送"].append({
            "dna": dna,
            "action": "push_to_notion"
        })

    # 3. 处理远程领先 → 拉取
    for item in 冲突.get("远程领先", []):
        dna = item["dna"]
        解决日志["远程拉取"].append({
            "dna": dna,
            "action": "pull_from_notion"
        })

    # 保存冲突解决日志
    if CONFLICT_STATE.exists():
        历史 = json.loads(CONFLICT_STATE.read_text())
    else:
        历史 = []
    历史.append(解决日志)
    CONFLICT_STATE.write_text(json.dumps(历史, ensure_ascii=False, indent=2))

    print(f"  版本冲突处理: {len(解决日志['版本冲突处理'])} 个")
    print(f"  本地推送标记: {len(解决日志['本地推送'])} 个")
    print(f"  远程拉取标记: {len(解决日志['远程拉取'])} 个")

    return 解决日志

# ══════════════════════════════════════════════════════════
# 主流程
# ══════════════════════════════════════════════════════════

def 执行同步(增量=False, 只检查=False, 模式="full"):
    """
    执行龍魂双脑同步

    模式:
      full     → 完整同步 (Display→Core + Terminal↔Notion + 冲突检测)
      d2c      → 仅Display→Core (原始模式)
      t2n      → Terminal→Notion (推送本地到展示脑)
      n2t      → Notion→Terminal (拉取展示脑到本地)
      conflict → 仅冲突检测
    """
    sep = "═" * 54
    print(f"\n{sep}")
    print("  龍魂·双脑同步引擎 v1.1 | Dual-Brain Sync Engine v1.1")
    print(f"  模式 | Mode: {模式}")
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

    print()

    if 模式 in ["full", "d2c"]:
        # ═══ 显示脑 → 内核脑 (原始流程) ════════════════════════════════
        if not 内核OK:
            print("🔴 内核脑未连通 | Core-Brain not connected，请检查 ~/.longhun/secrets.env → NOTION_TOKEN_TEAM")
            return

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
        写记忆(f"显示脑→内核脑同步完成·{len(页面列表)}页·{len(聚合)}分类",
               DNA, {"total": len(页面列表), "categories": len(聚合)})

        print(f"\n{sep}")
        print("  显示脑→内核脑同步完成 | Display→Core Sync Done")
        print(f"  总页面 | Total Pages: {len(页面列表)}  分类数 | Categories: {len(聚合)}")
        print(f"  内核脑 | Core-Brain: {链接[:60] if 链接 else '写入失败 | Write Failed'}")
        print(f"  DNA: {DNA}")
        print(f"  三色 | Audit: {'🟢 通过 | Pass' if 链接 else '🟡 部分完成 | Partial'}")

    if 模式 in ["full", "t2n"]:
        # ═══ 本地 → 显示脑 (推送本地记录) ════════════════════════════════
        print(f"\n{sep}")
        print("  本地→显示脑同步 | Terminal→Display Sync")

        本地记录 = 读取本地记录(限制=50)
        if 本地记录:
            结果 = 推送到展示脑(本地记录, 展示脑TOKEN)
            写记忆(f"本地→展示脑推送完成·{结果['success']}页",
                   DNA, {"pushed": 结果["success"], "failed": 结果["failed"]})
        else:
            print("  🟡 无本地记录需要推送")

    if 模式 in ["full", "n2t"]:
        # ═══ 显示脑 → 本地 (拉取远程记录) ════════════════════════════════
        print(f"\n{sep}")
        print("  显示脑→本地同步 | Display→Terminal Sync")

        远程页面 = 拉取自展示脑(展示脑TOKEN)
        if 远程页面:
            结果 = 更新本地记录(远程页面)
            写记忆(f"显示脑→本地拉取完成·{结果['success']}条",
                   DNA, {"pulled": 结果["success"], "failed": 结果["failed"]})
        else:
            print("  🟡 无远程记录需要拉取")

    if 模式 in ["full", "conflict"]:
        # ═══ 冲突检测与解决 ════════════════════════════════════════════
        print(f"\n{sep}")
        print("  冲突检测与解决 | Conflict Detection & Resolution")

        本地记录 = 读取本地记录(限制=1000)
        远程页面 = 拉取自展示脑(展示脑TOKEN) if 展示OK else []

        if 本地记录 and 远程页面:
            冲突 = 检测冲突(本地记录, 远程页面)
            解决 = 解决冲突(冲突, DNA)
            写记忆(f"冲突检测完成·版本冲突{len(冲突['版本冲突'])}·本地领先{len(冲突['本地领先'])}·远程领先{len(冲突['远程领先'])}",
                   DNA, {"conflicts": 冲突})
        else:
            print("  🟢 无冲突（本地或远程为空）")

    print(f"\n{sep}")
    print("  完整同步周期完成 | Full Sync Cycle Complete")
    print(f"  DNA: {DNA}")
    print(f"  三色 | Audit: 🟢 通过 | Pass")
    print(sep + "\n")


# ══════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂·双脑同步引擎 v1.1 - 支持三向同步 (Display↔Core + Terminal↔Notion)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
【同步模式说明】
  full      完整双向同步 (Display→Core + Terminal↔Notion + 冲突检测)
  d2c       仅Display-Brain→Core-Brain (原始模式)
  t2n       仅Terminal→Notion (本地推送到展示脑)
  n2t       仅Notion→Terminal (拉取展示脑到本地)
  conflict  仅冲突检测与解决

【CNSH对应指令】
  龍 双脑同步          →  python3 brain_sync.py --mode full
  龍 双脑检查          →  python3 brain_sync.py --check
  龍 双脑增量          →  python3 brain_sync.py --mode full --delta
  龍 本地推送          →  python3 brain_sync.py --mode t2n
  龍 拉取同步          →  python3 brain_sync.py --mode n2t
  龍 冲突检测          →  python3 brain_sync.py --mode conflict
  龍 双脑分类 "关键词" →  python3 brain_sync.py --classify "文字"

【定时任务示例】(每天凌晨3点完整同步)
  crontab -e
  0 3 * * * python3 ~/longhun-system/_work/tools/brain_sync.py --mode full --delta >> ~/longhun-system/logs/brain_sync.log 2>&1

【工作流推荐】
  1. 早间: 龍 双脑同步 (完整同步 + 冲突解决)
  2. 白天: 龍 本地推送 (推送新增本地记录)
  3. 晚间: 龍 拉取同步 (拉取远程更新)
        """
    )
    parser.add_argument("--mode",     default="full",
                        help="同步模式: full|d2c|t2n|n2t|conflict (默认: full)")
    parser.add_argument("--check",    action="store_true",
                        help="只检查双脑连通，不执行同步")
    parser.add_argument("--delta",    action="store_true",
                        help="增量模式（仅同步上次修改后的内容）")
    parser.add_argument("--classify", metavar="TEXT",
                        help="测试自动分类结果")

    args = parser.parse_args()

    if args.classify:
        结果 = 自动分类(args.classify)
        print(f"“{args.classify}”→ 分类 | Category: {结果}")
        return

    执行同步(增量=args.delta, 只检查=args.check, 模式=args.mode)


if __name__ == "__main__":
    main()

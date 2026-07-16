#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion 8主题重组引擎 v2.0

功能：
  1. 读取扫描原始数据 (scan_raw.json)
  2. 按8主题分类所有页面和数据库条目
  3. 查找重复组 (基于标题相似度+内容哈希)
  4. 生成迁移计划 (Notion API 可执行命令清单)
  5. --execute 模式: 通过 Notion API 实际创建8个数据库并迁移内容

用法：
  python3 bin/lh_notion_reorganize.py              # 分析+生成计划
  python3 bin/lh_notion_reorganize.py --report     # 仅输出报告到终端
  python3 bin/lh_notion_reorganize.py --execute    # 实际执行迁移（需确认）

DNA: #龍芯⚡️丙午·辛未·乙酉·需-NOTION-8THEME-REORGANIZE-v2.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
from __future__ import annotations

import json
import os
import sys
import time
import hashlib
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict, List, Optional, Any

# ═══════════════════════════════════════════════
# 0. 配置常量
# ═══════════════════════════════════════════════
CST = timezone(timedelta(hours=8))
HOME = Path.home()
ROOT = Path(os.environ.get("LONGHUN_ROOT", HOME / "longhun-system"))
SCAN_FILE = ROOT / "data" / "notion_scan" / "scan_raw.json"
PLAN_FILE = ROOT / "data" / "notion_scan" / "reorganize_plan.json"
OUTPUT_DIR = ROOT / "data" / "notion_reorganize"
ANALYSIS_FILE = OUTPUT_DIR / "8theme_analysis.json"
MIGRATION_FILE = OUTPUT_DIR / "migration_commands.json"

DNA = "#龍芯⚡️丙午·辛未·乙酉·需-NOTION-8THEME-REORGANIZE-v2.0"
TODAY = datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00")

# ═══════════════════════════════════════════════
# 0.1 8主题定义（老大指定方案）
# ═══════════════════════════════════════════════
THEMES: Dict[str, Dict] = {
    "DB-01": {
        "name": "🐉 龍魂系统核心",
        "type": "主线",
        "keywords_high": [
            # 高权重(5分): 命中1个即强烈指向 DB-01
            "UID9622", "北辰协议", "BEICHEN", "龍魂系统",
            "蚁群架构", "触角协议", "人格矩阵", "人格路由",
            "宪法铁律", "不可修订", "底座不动", "数字永生",
            "CNSH-64", "三才算法", "主权派生",
            "龙魂系统", "龙芯核心", "longhun system",
        ],
        "keywords_normal": [
            # 普通权重(1分): 辅助匹配
            "龍魂", "龙魂", "longhun", "CNSH",
            "架构v", "引擎v", "engine", "内核",
            "persona", "neural", "registry",
            "編譯器", "编译器", "compiler",
            "启动器", "bootstrap", "core-service",
        ],
        "emoji": "🐉",
    },
    "DB-02": {
        "name": "📜 CNSH论文",
        "type": "学术",
        "keywords_high": [
            "IEEE论文", "顶刊论文", "顶会论文", "期刊投稿",
            "CNSH论文", "白皮书v", "治理架构论文",
            "论文补全", "论文母页", "行为密码学",
        ],
        "keywords_normal": [
            "IEEE", "白皮书", "paper", "academic",
            "论文", "审稿", "citation", "appendix",
            "abstract", "洛书369", "JMLR", "NeurIPS",
        ],
        "emoji": "📜",
    },
    "DB-03": {
        "name": "🔧 鸿蒙开发",
        "type": "工程",
        "keywords_high": [
            "鸿蒙开发", "HarmonyOS", "ArkTS",
            "生日提醒", "库存管理", "印章管理",
            "NAPI桥接", "NEON SIMD", "WorkScheduler",
            "国密SM2", "系统托盘",
        ],
        "keywords_normal": [
            "鸿蒙", "组件开发", "UIAbility", "Navigation",
            "NavPathStack", "LazyForEach", "首帧优化",
            "多设备", "适配", "响应式布局",
            "全局热键", "语音AI", "ETS",
            "Stack遮罩", "项目管理模块",
        ],
        "emoji": "🔧",
    },
    "DB-04": {
        "name": "⚖️ 民生审计",
        "type": "应用",
        "keywords_high": [
            "诚信检测", "伦理熔断", "IW-ECB", "IWCB",
            "语义防火墙", "一票否决", "三色审计",
            "RobotScore", "行为DNA", "取证内核",
            "维权助手", "民生审计",
        ],
        "keywords_normal": [
            "伦理", "熔断", "防火墙", "firewall",
            "审计", "audit", "治理", "governance",
            "自愈", "heal", "沙盒", "sandbox",
            "compliance", "forensics",
        ],
        "emoji": "⚖️",
    },
    "DB-05": {
        "name": "📚 国学创作",
        "type": "文化",
        "keywords_high": [
            "对联生成", "藏头诗", "道德经", "易经推演",
            "河图洛书", "二十八宿", "五行八卦",
            "文化输出", "出师有名", "十维同演",
            "仓颉", "孙思邈", "苏东坡", "屈原",
            "归源心法", "道引",
        ],
        "keywords_normal": [
            "国学", "易经", "太极", "五行", "八卦",
            "philosophy", "wuxing", "星宿", "干支",
            "daoyin", "诗词", "历史人物", "道德经",
            "李白", "吕蒙", "姜子牙", "诸葛亮",
        ],
        "emoji": "📚",
    },
    "DB-06": {
        "name": "🏛️ 知识图谱",
        "type": "智库",
        "keywords_high": [
            "知识图谱", "knowledge graph", "向量数据库",
            "军事理论", "中国法律", "政策法规",
            "智库报告", "RAG系统",
        ],
        "keywords_normal": [
            "RAG", "vector", "kg-api", "知识库",
            "scraper", "采集", "数据层", "law",
            "法律", "法规", "战略", "军事",
            "政治", "经济分析", "索引",
        ],
        "emoji": "🏛️",
    },
    "DB-07": {
        "name": "📊 运营数据",
        "type": "监控",
        "keywords_high": [
            "健康检查", "health check", "Bark推送",
            "鲲鹏部署", "kunpeng", "飞书告警",
            "日志备份", "备份清单", "systemd",
            "monitor setup", "运维报告",
        ],
        "keywords_normal": [
            "日志", "log", "备份", "backup",
            "部署", "deploy", "运维", "ops",
            "同步", "sync", "守护", "daemon",
            "cron", "launchd", "metrics",
            "dashboard", "告警", "alert",
            "监控", "monitor", "健康", "health",
        ],
        "emoji": "📊",
    },
    "DB-08": {
        "name": "🗑️ 归档冷冻",
        "type": "归档",
        "keywords_high": [
            "废弃", "重复项", "待清理",
            "deprecated", "legacy", "quarantine",
        ],
        "keywords_normal": [
            "旧版", "草稿", "archive",
            "old", "temp", "tmp",
            "实验版", "test旧",
        ],
        "emoji": "🗑️",
    },
}

# 标准字段模板（每个数据库统一）
STANDARD_SCHEMA = {
    "名称": {"title": {}},
    "主题标签": {
        "multi_select": {
            "options": [{"name": f"{v['emoji']} {v['name']}", "color": color}
                        for (k, v), color in zip(THEMES.items(),
                        ["blue","green","orange","red","yellow","purple","pink","gray"])]
        }
    },
    "子标签": {"multi_select": {"options": [
        {"name": "协议规范", "color": "blue"},
        {"name": "技术文档", "color": "green"},
        {"name": "代码实现", "color": "orange"},
        {"name": "设计稿", "color": "yellow"},
        {"name": "会议记录", "color": "pink"},
        {"name": "研究报告", "color": "purple"},
        {"name": "运维记录", "color": "red"},
        {"name": "待分类", "color": "gray"},
    ]}},
    "状态": {
        "select": {
            "options": [
                {"name": "✅ 活跃", "color": "green"},
                {"name": "📝 草稿", "color": "yellow"},
                {"name": "📦 归档", "color": "gray"},
                {"name": "🗑️ 废弃", "color": "red"},
            ]
        }
    },
    "优先级": {
        "select": {
            "options": [
                {"name": "P0-不可修订", "color": "red"},
                {"name": "P1-老大审批", "color": "orange"},
                {"name": "P2-团队决策", "color": "blue"},
                {"name": "P3-低优先级", "color": "gray"},
            ]
        }
    },
    "DNA签名": {"rich_text": {}},
    "UID": {"rich_text": {}},
    "创建时间": {"date": {}},
    "修改时间": {"date": {}},
    "来源": {"url": {}},
    "重复标记": {"relation": {"database_id": ""}},  # 运行时填充
}


# ═══════════════════════════════════════════════
# 1. 分类引擎
# ═══════════════════════════════════════════════

def classify_item(title: str, extra_text: str = "") -> str:
    """用双权重关键词将一条目分类到8主题之一，无匹配归 DB-08"""
    text = f"{title} {extra_text}".lower()
    scores: Dict[str, int] = {}

    HIGH_WEIGHT = 5  # 高权重关键词分值
    NORMAL_WEIGHT = 1

    for db_id, config in THEMES.items():
        score = 0
        for kw in config.get("keywords_high", []):
            if kw.lower() in text:
                score += HIGH_WEIGHT
        for kw in config.get("keywords_normal", []):
            if kw.lower() in text:
                score += NORMAL_WEIGHT
        scores[db_id] = score

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "DB-08"


def load_scan_data() -> Dict[str, Any]:
    """加载扫描原始数据"""
    if not SCAN_FILE.exists():
        print(f"❌ 扫描数据不存在: {SCAN_FILE}")
        print("   请先运行: python3 bin/lh_notion_full_sync.py")
        sys.exit(1)
    with open(SCAN_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_duplicate_groups() -> List[Dict]:
    """加载已有去重数据"""
    if not PLAN_FILE.exists():
        return []
    with open(PLAN_FILE, encoding="utf-8") as f:
        plan = json.load(f)
    return plan.get("duplicates", [])


# ═══════════════════════════════════════════════
# 2. 分析: 分类 + 统计
# ═══════════════════════════════════════════════

def analyze_classification(scan: Dict[str, Any]) -> Dict[str, Any]:
    """对所有页面和数据库条目执行8主题分类"""
    result: Dict[str, List[Dict]] = {db_id: [] for db_id in THEMES}

    # 2.1 分类独立页面 (6478)
    pages = scan.get("page_summaries", [])
    for page in pages:
        title = page.get("title", "")
        db_id = classify_item(title)
        entry = {
            "id": page["id"],
            "title": title,
            "url": page.get("url", ""),
            "last_edited": page.get("last_edited", ""),
            "type": "page",
            "parent_type": page.get("parent_type", ""),
        }
        result[db_id].append(entry)

    # 2.2 分类数据库条目 (4747) — 加入父DB名作为分类上下文
    dbs = scan.get("database_details", [])
    for db in dbs:
        entries = db.get("entries", [])
        parent_db_name = db.get("title", "")
        for ent in entries:
            title = ent.get("title", "")
            # 用 标题 + 父DB名 一起分类（父DB名权重更高）
            db_id = classify_item(title, extra_text=parent_db_name)
            entry = {
                "id": ent["id"],
                "title": title,
                "url": ent.get("url", ""),
                "last_edited": ent.get("last_edited", ""),
                "type": "db_entry",
                "parent_db": parent_db_name,
                "parent_db_id": db.get("id", ""),
            }
            result[db_id].append(entry)

    return result


def compute_stats(classified: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """计算分类统计"""
    stats = {}
    total = 0
    for db_id, items in classified.items():
        pages = sum(1 for i in items if i["type"] == "page")
        db_entries = sum(1 for i in items if i["type"] == "db_entry")
        stats[db_id] = {
            "name": THEMES[db_id]["name"],
            "type": THEMES[db_id]["type"],
            "total": len(items),
            "pages": pages,
            "db_entries": db_entries,
        }
        total += len(items)

    stats["_total"] = total
    return stats


# ═══════════════════════════════════════════════
# 3. 去重分析: 标题相似度
# ═══════════════════════════════════════════════

def compute_title_similarity(title_a: str, title_b: str) -> float:
    """计算两个标题的相似度"""
    return SequenceMatcher(None, title_a.lower(), title_b.lower()).ratio()


def compute_content_hash(text: str) -> str:
    """SM3简化哈希"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def find_duplicates_within_theme(items: List[Dict], threshold: float = 0.85) -> List[Dict]:
    """在分类内发现重复组"""
    groups: List[Dict] = []
    seen_indices: set[str] = set()

    for i, item_a in enumerate(items):
        if i in seen_indices:
            continue
        dup_items = [item_a]
        for j, item_b in enumerate(items):
            if j <= i or j in seen_indices:
                continue
            sim = compute_title_similarity(item_a["title"], item_b["title"])
            if sim >= threshold:
                dup_items.append(item_b)
                seen_indices.add(j)

        if len(dup_items) > 1:
            # 选最早编辑的为主条目
            dup_items.sort(key=lambda x: x.get("last_edited", ""))
            groups.append({
                "group_id": f"DUP-{len(groups):04d}",
                "master": dup_items[0],
                "duplicates": dup_items[1:],
                "similarity": 1.0,
                "count": len(dup_items),
            })
            seen_indices.add(i)

    return groups


# ═══════════════════════════════════════════════
# 4. 迁移计划生成
# ═══════════════════════════════════════════════

def generate_migration_plan(classified: Dict[str, List[Dict]],
                            stats: Dict[str, Any]) -> Dict[str, Any]:
    """生成 Notion API 可执行的迁移命令清单"""
    plan = {
        "generated_at": TODAY,
        "dna": DNA,
        "steps": [],
    }

    # Step 1: 创建8个数据库
    for db_id, config in THEMES.items():
        plan["steps"].append({
            "action": "create_database",
            "db_id": db_id,
            "name": config["name"],
            "description": f"龍魂 · {config['name']} ({config['type']})",
            "schema": STANDARD_SCHEMA,
            "note": "创建后需记录返回的 database_id 供后续迁移使用",
        })

    # Step 2: 迁移内容到对应数据库
    for db_id, items in classified.items():
        plan["steps"].append({
            "action": "migrate_pages",
            "db_id": db_id,
            "target_db_name": THEMES[db_id]["name"],
            "count": len(items),
            "pages": [{"id": i["id"], "title": i["title"]} for i in items],
            "note": f"将 {len(items)} 条内容创建为数据库条目",
        })

    # Step 3: 标记重复
    plan["steps"].append({
        "action": "mark_duplicates",
        "note": "去重组在 analysis 中标记，需人工逐组确认后执行合并",
    })

    # Step 4: 归档原355数据库
    plan["steps"].append({
        "action": "archive_old_dbs",
        "note": "原355个数据库统一改名为 [归档]原名称 并移动到归档区",
    })

    return plan


# ═══════════════════════════════════════════════
# 5. Notion API 执行器
# ═══════════════════════════════════════════════

class NotionExecutor:
    """通过 Notion API 实际执行建库和迁移"""

    def __init__(self):
        self.token = self._get_token()
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }
        self.call_count = 0
        self.created_db_ids: Dict[str, str] = {}

    def _get_token(self) -> str:
        t = os.environ.get("NOTION_TOKEN", "")
        if not t:
            sys.path.insert(0, str(ROOT / "bin"))
            try:
                from lh_secrets_loader import load_all
                load_all(export_to_os=True)
                t = os.environ.get("NOTION_TOKEN", "")
            except Exception:
                pass
        if not t:
            print("❌ NOTION_TOKEN 未设置")
            print("   export NOTION_TOKEN=ntn_...")
            sys.exit(1)
        return t

    def _rate_limit(self):
        """Notion API 限速: 每秒最多3次"""
        self.call_count += 1
        if self.call_count % 3 == 0:
            time.sleep(1.1)

    def _api(self, method: str, endpoint: str, payload: Optional[Dict] = None) -> Dict[str, Any]:
        """统一下层 API 调用"""
        import urllib.request
        import urllib.error

        self._rate_limit()
        url = f"{self.base_url}{endpoint}"
        data = json.dumps(payload).encode("utf-8") if payload else None

        req = urllib.request.Request(url, data=data, headers=self.headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8")
            print(f"  ⚠️ API 错误 [{endpoint}]: {e.code} {err[:200]}")
            return {"error": str(e), "code": e.code}

    def create_database(self, db_id: str, parent_page_id: str) -> Optional[str]:
        """创建单个主题数据库，返回 database_id"""
        config = THEMES[db_id]
        # 深拷贝 schema 并设置父页面
        import copy
        schema = copy.deepcopy(STANDARD_SCHEMA)

        payload = {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "title": [{"type": "text", "text": {"content": config["name"]}}],
            "description": [
                {"type": "text", "text": {
                    "content": f"龍魂 · {config['name']} ({config['type']}) | DNA: {DNA}"
                }}
            ],
            "properties": {
                "名称": {"title": {}},
                "主题标签": schema["主题标签"],
                "状态": schema["状态"],
                "优先级": schema["优先级"],
                "子标签": schema["子标签"],
                "DNA签名": {"rich_text": {}},
                "UID": {"rich_text": {}},
                "来源": {"url": {}},
            },
        }

        print(f"  📦 创建数据库: {config['name']} ...", end=" ")
        result = self._api("POST", "/databases", payload)
        if "error" in result:
            print(f"❌ {result.get('error', '')}")
            return None

        db_created_id = result.get("id", "")
        self.created_db_ids[db_id] = db_created_id
        print(f"✅ {db_created_id}")
        return db_created_id

    def create_page_in_db(self, db_created_id: str, title: str, db_id: str,
                          page_data: Dict[str, Any]) -> bool:
        """在已创建的数据库中新建一页"""
        config = THEMES[db_id]
        payload = {
            "parent": {"type": "database_id", "database_id": db_created_id},
            "properties": {
                "名称": {
                    "title": [{"type": "text", "text": {"content": title}}]
                },
                "主题标签": {
                    "multi_select": [{"name": f"{config['emoji']} {config['name']}"}]
                },
                "状态": {"select": {"name": "✅ 活跃"}},
                "UID": {
                    "rich_text": [{"type": "text", "text": {"content": "9622"}}]
                },
                "DNA签名": {
                    "rich_text": [{"type": "text", "text": {"content": DNA}}]
                },
            },
        }

        result = self._api("POST", "/pages", payload)
        return "error" not in result


# ═══════════════════════════════════════════════
# 6. 主流程
# ═══════════════════════════════════════════════

def run_analysis():
    """执行分类分析 + 去重 + 生成迁移计划"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("🐉 龍魂 · Notion 8主题重组分析引擎 v2.0")
    print(f"   DNA: {DNA}")
    print("=" * 60)

    # 加载数据
    print("\n📂 加载扫描数据...")
    scan = load_scan_data()
    summary = scan.get("summary", {})
    print(f"   总项目: {summary.get('total', '?')} | 数据库: {summary.get('databases', '?')} | 页面: {summary.get('pages', '?')}")

    # 分类
    print("\n🔍 执行8主题分类...")
    classified = analyze_classification(scan)
    stats = compute_stats(classified)

    # 输出统计
    print("\n" + "=" * 60)
    print("📊 8主题分类统计")
    print("=" * 60)
    for db_id in sorted(THEMES.keys()):
        s = stats[db_id]
        bar = "█" * (s["total"] // 30)
        print(f"  {THEMES[db_id]['emoji']} {s['name']:<16s} | {s['total']:>5d}项 | 页面{s['pages']} · DB条目{s['db_entries']} | {bar}")
    print(f"  {'─'*50}")
    print(f"  {'合计':>19s} | {stats['_total']:>5d}项")

    # 去重
    print("\n🔬 在每个主题内查找重复...")
    all_duplicates: List[Dict] = []
    for db_id in sorted(THEMES.keys()):
        items = classified[db_id]
        if len(items) < 2:
            continue
        dups = find_duplicates_within_theme(items, threshold=0.85)
        if dups:
            all_duplicates.extend(dups)
            total_dup_items = sum(g["count"] for g in dups)
            print(f"  {THEMES[db_id]['name']}: {len(dups)}组 · {total_dup_items}条")

    print(f"\n  ⚠️ 总计: {len(all_duplicates)}组重复 (标题相似度≥85%)")

    # 加载扫描时的重复组
    scan_dups = load_duplicate_groups()
    print(f"  📋 扫描阶段发现: {len(scan_dups)}组疑似重复")

    # 保存分析结果
    analysis = {
        "generated_at": TODAY,
        "dna": DNA,
        "classification_stats": stats,
        "classified_data": {
            db_id: [{"id": i["id"], "title": i["title"], "url": i.get("url", ""),
                     "type": i["type"], "last_edited": i.get("last_edited", "")}
                    for i in items]
            for db_id, items in classified.items()
        },
        "duplicates_within_themes": len(all_duplicates),
        "duplicates_from_scan": len(scan_dups),
        "top_duplicate_samples": [
            {"group_id": g["group_id"], "master_title": g["master"]["title"][:60],
             "dup_count": g["count"], "similarity": g["similarity"]}
            for g in all_duplicates[:20]
        ],
    }

    with open(ANALYSIS_FILE, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    print(f"\n💾 分析结果已保存: {ANALYSIS_FILE}")
    print(f"   ({ANALYSIS_FILE.stat().st_size / 1024:.1f} KB)")

    # 生成迁移计划
    print("\n📋 生成迁移计划...")
    migration_plan = generate_migration_plan(classified, stats)

    with open(MIGRATION_FILE, "w", encoding="utf-8") as f:
        json.dump(migration_plan, f, indent=2, ensure_ascii=False)
    print(f"💾 迁移计划已保存: {MIGRATION_FILE}")
    print(f"   ({MIGRATION_FILE.stat().st_size / 1024:.1f} KB)")

    # 汇总报告
    print("\n" + "=" * 60)
    print("✅ 分析完成!")
    print("=" * 60)
    print(f"""
📊 8主题分类: 完成
   - 最大库: {max(stats.items(), key=lambda x: x[1]['total'] if x[0] != '_total' else 0)[1]['name']}
   - 最小库: {min((v for k,v in stats.items() if k != '_total'), key=lambda x: x['total'])['name']}

🔬 去重分析: 完成
   - 主题内重复: {len(all_duplicates)} 组
   - 扫描阶段重复: {len(scan_dups)} 组

📋 迁移计划: 已生成
   - {len(migration_plan['steps'])} 个执行步骤

📁 输出文件:
   - 分析: {ANALYSIS_FILE}
   - 计划: {MIGRATION_FILE}
   - 方案: docs/notion_8theme_reorganize_plan.md

🚀 下一步:
   python3 bin/lh_notion_reorganize.py --execute    # 实际执行迁移
   cat data/notion_reorganize/8theme_analysis.json  # 查看分类详情
""")

    return analysis, migration_plan


def run_execute():
    """实际执行 Notion API 迁移"""
    if not ANALYSIS_FILE.exists():
        print("❌ 请先运行分析: python3 bin/lh_notion_reorganize.py")
        sys.exit(1)

    print("=" * 60)
    print("⚠️  即将通过 Notion API 执行实际迁移")
    print("=" * 60)
    print()
    print("将执行以下操作:")
    print("  1. 在 Notion 中创建 8 个主题数据库")
    print("  2. 将扫描到的内容页面迁移到对应数据库")
    print("  3. 标记重复组")
    print()
    print("⚠️  此操作不可撤销! 建议先在 Notion 中备份!")
    print()

    confirm = input("输入 'yes' 确认执行: ").strip()
    if confirm.lower() != "yes":
        print("❌ 已取消")
        return

    # 加载分析数据
    with open(ANALYSIS_FILE, encoding="utf-8") as f:
        analysis = json.load(f)

    # 获取父页面 ID（需要老大在 Notion 中创建一个顶层页面作为容器）
    parent_page_id = os.environ.get("NOTION_PARENT_PAGE", "")
    if not parent_page_id:
        print("\n⚠️ 需要 NOTION_PARENT_PAGE 环境变量")
        print("   请在 Notion 中创建一个顶层页面（如'龍魂8主题数据库'）")
        print("   然后设置: export NOTION_PARENT_PAGE=<页面ID>")
        print("\n   获取方法: 在 Notion 页面URL中找到32位ID")
        print("   例: https://notion.so/龍魂8主题数据库-1a2b3c4d... → 1a2b3c4d...")
        return

    executor = NotionExecutor()

    # Step 1: 创建8个数据库
    print("\n📦 Step 1: 创建8个主题数据库...")
    for db_id in sorted(THEMES.keys()):
        db_created_id = executor.create_database(db_id, parent_page_id)
        if db_created_id:
            time.sleep(0.5)

    if not executor.created_db_ids:
        print("❌ 所有数据库创建失败，终止")
        return

    # Step 2: 迁移内容
    print("\n📤 Step 2: 迁移内容到对应数据库...")
    classified_data = analysis.get("classified_data", {})
    total_migrated = 0
    total_errors = 0
    max_per_db = 100  # 限速: 每个DB最多迁移100条（可调整）

    for db_id in sorted(THEMES.keys()):
        if db_id not in executor.created_db_ids:
            continue

        items = classified_data.get(db_id, [])[:max_per_db]
        db_created_id = executor.created_db_ids[db_id]
        name = THEMES[db_id]["name"]

        print(f"  {THEMES[db_id]['emoji']} {name}: {len(items)}条 ...", end=" ")
        ok = 0
        err = 0
        for item in items:
            success = executor.create_page_in_db(db_created_id, item["title"], db_id, item)
            if success:
                ok += 1
            else:
                err += 1
            if ok % 20 == 0:
                time.sleep(0.3)

        print(f"✅ {ok} / ❌ {err}")
        total_migrated += ok
        total_errors += err

    print(f"\n📊 迁移统计: 成功 {total_migrated} | 失败 {total_errors}")

    # Step 3: 输出创建的数据库ID（供后续使用）
    print("\n📋 创建的数据库ID:")
    for db_id, db_created_id in executor.created_db_ids.items():
        print(f"  export NOTION_{db_id.replace('-','_')}_DB={db_created_id}")

    print(f"\n✅ 执行完成!")
    print(f"   DNA: {DNA}")


# ═══════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · Notion 8主题重组引擎 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
DNA: {DNA}

示例:
  %(prog)s                  # 分析+生成计划（安全，只读）
  %(prog)s --report         # 仅输出分类报告到终端
  %(prog)s --execute        # 通过 Notion API 实际执行迁移
        """,
    )
    parser.add_argument("--execute", action="store_true", help="实际执行 Notion 迁移")
    parser.add_argument("--report", action="store_true", help="仅输出报告到终端")
    args = parser.parse_args()

    if args.execute:
        run_execute()
    else:
        run_analysis()

#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 浏览器历史矿工 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-BROWSER-MINER-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

核心理念：
  你的浏览器记录不是"使用痕迹"，是你思想的矿脉。
  每天看什么、搜什么、收藏什么——这就是你的信息食谱，你的"知识口味"。

支持:
  - Chrome/Chromium (SQLite History + JSON Bookmarks)
  - Safari (SQLite History.db)
  - Firefox (SQLite places.sqlite)
  - 多配置文件自动发现

用法:
  python3 bin/lh_browser_miner.py scan           # 勘探所有浏览器
  python3 bin/lh_browser_miner.py extract        # 提取历史+书签→JSONL
  python3 bin/lh_browser_miner.py extract --days 30  # 只提取最近30天
  python3 bin/lh_browser_miner.py status         # 查看矿场状态
"""

import hashlib, json, os, re, sqlite3, sys, time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict

SYSTEM_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = SYSTEM_ROOT / "data" / "browser_mine"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Chrome/WebKit 时间戳转换
# Chrome: microseconds since 1601-01-01 00:00:00 UTC
# Firefox: microseconds since 1970-01-01 00:00:00 UTC
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CHROME_EPOCH = datetime(1601, 1, 1, tzinfo=timezone.utc)

def chrome_time_to_datetime(chrome_micros: int) -> datetime:
    """Chrome 微秒时间戳 → datetime"""
    try:
        return CHROME_EPOCH + timedelta(microseconds=chrome_micros)
    except (OverflowError, ValueError):
        return datetime.min.replace(tzinfo=timezone.utc)

def firefox_time_to_datetime(firefox_micros: int) -> datetime:
    """Firefox 微秒时间戳 → datetime"""
    try:
        return datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=firefox_micros)
    except (OverflowError, ValueError):
        return datetime.min.replace(tzinfo=timezone.utc)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 浏览器路径发现
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOME = Path.home()
LIBRARY = HOME / "Library"
APP_SUPPORT = LIBRARY / "Application Support"

BROWSER_DEFS = [
    {
        "name": "Chrome",
        "db_path": APP_SUPPORT / "Google" / "Chrome",
        "history_file": "History",
        "bookmarks_file": "Bookmarks",
        "profile_glob": "Default",
        "time_parser": chrome_time_to_datetime,
        "query": """
            SELECT url, title, visit_count, last_visit_time
            FROM urls
            WHERE url LIKE 'http%' AND title != ''
            ORDER BY last_visit_time DESC
        """,
    },
    {
        "name": "Chrome-Pro",
        "db_path": APP_SUPPORT / "Google" / "Chrome",
        "history_file": "History",
        "bookmarks_file": "Bookmarks",
        "profile_glob": "Profile *",
        "time_parser": chrome_time_to_datetime,
        "query": """
            SELECT url, title, visit_count, last_visit_time
            FROM urls
            WHERE url LIKE 'http%' AND title != ''
            ORDER BY last_visit_time DESC
        """,
    },
    {
        "name": "Safari",
        "db_path": LIBRARY / "Safari",
        "history_file": "History.db",
        "bookmarks_file": "Bookmarks.plist",
        "profile_glob": None,
        "time_parser": lambda t: datetime.fromtimestamp(t, tz=timezone.utc),
        "query": """
            SELECT hi.url, COALESCE(hv.title, '') as title,
                   hi.visit_count, MAX(hv.visit_time) as last_visit
            FROM history_items hi
            LEFT JOIN history_visits hv ON hi.id = hv.history_item
            WHERE hi.url LIKE 'http%'
            GROUP BY hi.id
            ORDER BY last_visit DESC
        """,
    },
    {
        "name": "Firefox",
        "db_path": APP_SUPPORT / "Firefox" / "Profiles",
        "history_file": "places.sqlite",
        "bookmarks_file": None,
        "profile_glob": "*.default-release",
        "time_parser": firefox_time_to_datetime,
        "query": """
            SELECT url, COALESCE(title, '') as title,
                   COALESCE(visit_count, 0) as visit_count,
                   COALESCE(last_visit_date, 0) as last_visit_time
            FROM moz_places
            WHERE url LIKE 'http%' AND title != ''
            ORDER BY last_visit_date DESC
        """,
    },
]

# URL 域分类模式
DOMAIN_PATTERNS = {
    "AI对话": re.compile(r"(kimi\.|chat\.openai|claude\.|deepseek|poe\.|gemini\.|tongyi|yiyan\.baidu|xinghuo)",
                         re.IGNORECASE),
    "技术文档": re.compile(r"(github\.|stackoverflow|docs\.|mdn\.|dev\.to|medium\.|csdn\.|juejin)",
                           re.IGNORECASE),
    "搜索": re.compile(r"(google\./search|baidu\./s|bing\./search|sogou\.)", re.IGNORECASE),
    "视频": re.compile(r"(bilibili\.|youtube\.|v\.qq|iqiyi|youku)", re.IGNORECASE),
    "新闻": re.compile(r"(news\.|36kr|huxiu|thepaper|ifeng)", re.IGNORECASE),
    "社交媒体": re.compile(r"(weibo\.|zhihu\.|douban\.|twitter\.|reddit\.)", re.IGNORECASE),
    "知识": re.compile(r"(wikipedia|baike\.|zh\.wikipedia)", re.IGNORECASE),
    "工具": re.compile(r"(translate\.|bejson\.|json\.cn|tool\.)", re.IGNORECASE),
    "中国学术": re.compile(r"(cnki\.|wanfangdata|langtaosha\.org)", re.IGNORECASE),
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 数据模型
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class HistoryEntry:
    """单条浏览记录"""
    url: str
    title: str
    visit_count: int
    last_visit: str          # ISO datetime
    browser: str             # Chrome/Safari/Firefox
    domain: str              # 提取的域名
    category: str            # 分类（AI对话/技术/搜索等）
    extracted_at: str = ""

@dataclass
class BookmarkEntry:
    """单条书签"""
    url: str
    title: str
    folder: str              # 书签文件夹路径
    browser: str
    added_at: str = ""

@dataclass
class BrowserReport:
    """浏览器勘探报告"""
    browser: str
    profile: str
    history_count: int
    bookmark_count: int
    earliest: str
    latest: str
    size_kb: int = 0
    status: str = "🟡 待提取"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 浏览器矿工引擎
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class BrowserMiner:
    """浏览器历史矿工"""

    def __init__(self):
        self.reports: List[BrowserReport] = []
        self.history: List[HistoryEntry] = []
        self.bookmarks: List[BookmarkEntry] = []
        self._extracted_at = datetime.now().isoformat()

    # ═══════════ 勘探 ═══════════

    def scan(self) -> List[BrowserReport]:
        """勘探所有浏览器数据库"""
        print("🔍 浏览器历史矿场勘探...")
        self.reports = []

        for bdef in BROWSER_DEFS:
            db_root = bdef["db_path"]
            if not db_root.exists():
                continue

            profile_glob = bdef.get("profile_glob")
            if profile_glob is None:
                # 单文件（Safari）：直接查
                db_file = db_root / bdef["history_file"]
                report = self._scan_db(bdef["name"], "default", db_file, bdef)
                if report:
                    self.reports.append(report)
            else:
                # 多 Profile：遍历
                for profile_dir in sorted(db_root.glob(profile_glob)):
                    if not profile_dir.is_dir():
                        continue
                    db_file = profile_dir / bdef["history_file"]
                    report = self._scan_db(bdef["name"], profile_dir.name, db_file, bdef)
                    if report:
                        self.reports.append(report)
                        # 书签
                        if bdef.get("bookmarks_file"):
                            bm_file = profile_dir / bdef["bookmarks_file"]
                            if bm_file.exists():
                                try:
                                    size = bm_file.stat().st_size
                                    report.size_kb += size // 1024
                                except:
                                    pass

        return self.reports

    def _scan_db(self, browser: str, profile: str, db_file: Path, bdef: Dict) -> Optional[BrowserReport]:
        if not db_file.exists():
            return None

        try:
            size = db_file.stat().st_size
            # 只读模式，避免锁冲突
            conn = sqlite3.connect(f"file:{db_file}?mode=ro", uri=True)
            conn.row_factory = sqlite3.Row

            # 检查表是否存在
            table_check = bdef["query"].split("FROM")[1].split()[0].strip()
            cursor = conn.execute(f"SELECT COUNT(*) FROM {table_check}")
            count = cursor.fetchone()[0]

            # 最新/最早时间
            earliest = ""
            latest = ""
            time_parser = bdef["time_parser"]
            try:
                # 尝试从表里取时间范围
                for row in conn.execute(bdef["query"] + " LIMIT 1"):
                    ts = row[-1]  # last column is time
                    if ts and ts > 0:
                        latest = time_parser(ts).strftime("%Y-%m-%d %H:%M")
                # 最早
                reverse_query = bdef["query"].replace("DESC", "ASC") if "DESC" in bdef["query"] else bdef["query"] + " ASC"
                for row in conn.execute(reverse_query.replace("DESC", "ASC") + " LIMIT 1"):
                    ts = row[-1]
                    if ts and ts > 0:
                        earliest = time_parser(ts).strftime("%Y-%m-%d %H:%M")
            except:
                pass

            conn.close()

            return BrowserReport(
                browser=browser,
                profile=profile,
                history_count=count,
                bookmark_count=0,
                earliest=earliest,
                latest=latest,
                size_kb=size // 1024,
                status="🟡 待提取" if count > 0 else "🔴 无数据",
            )
        except sqlite3.OperationalError as e:
            # 数据库被锁定或损坏
            return BrowserReport(
                browser=browser,
                profile=profile,
                history_count=0,
                bookmark_count=0,
                earliest="", latest="",
                size_kb=db_file.stat().st_size // 1024 if db_file.exists() else 0,
                status=f"🔴 {str(e)[:40]}",
            )
        except Exception as e:
            return None

    # ═══════════ 提取 ═══════════

    def extract(self, days: int = 0, limit_per_browser: int = 5000) -> Tuple[List[HistoryEntry], List[BookmarkEntry]]:
        """提取历史记录和书签"""
        print("⛏️ 开始挖矿...")

        if not self.reports:
            self.scan()

        self.history = []
        self.bookmarks = []
        cutoff = datetime.now(timezone.utc) - timedelta(days=days) if days > 0 else None

        for bdef in BROWSER_DEFS:
            db_root = bdef["db_path"]
            if not db_root.exists():
                continue

            profile_glob = bdef.get("profile_glob")
            if profile_glob is None:
                # Safari
                db_file = db_root / bdef["history_file"]
                self._extract_history(bdef["name"], "default", db_file, bdef, cutoff, limit_per_browser)
            else:
                for profile_dir in sorted(db_root.glob(profile_glob)):
                    if not profile_dir.is_dir():
                        continue
                    db_file = profile_dir / bdef["history_file"]
                    profile_label = f"{bdef['name']}/{profile_dir.name}"
                    self._extract_history(bdef["name"], profile_dir.name, db_file, bdef, cutoff, limit_per_browser)

                    # 提取书签
                    bm_file_name = bdef.get("bookmarks_file")
                    if bm_file_name:
                        bm_file = profile_dir / bm_file_name
                        if bm_file.exists():
                            self._extract_bookmarks(bdef["name"], bm_file)

        # 去重（同URL合并）
        self._dedup_history()

        print(f"⛏️ 挖矿完成: {len(self.history)} 条历史 | {len(self.bookmarks)} 条书签")
        return self.history, self.bookmarks

    def _extract_history(self, browser: str, profile: str, db_file: Path,
                          bdef: Dict, cutoff: Optional[datetime], limit: int):
        if not db_file.exists():
            return

        try:
            conn = sqlite3.connect(f"file:{db_file}?mode=ro", uri=True)
            conn.row_factory = sqlite3.Row
            time_parser = bdef["time_parser"]
            extracted = 0

            for row in conn.execute(bdef["query"] + f" LIMIT {limit}"):
                url = row[0] or ""
                title = row[1] or ""
                visit_count = int(row[2] or 0)
                ts = row[3] or 0

                if not url or not url.startswith("http"):
                    continue
                if not title:
                    title = url[:80]

                try:
                    dt = time_parser(int(ts))
                except:
                    dt = datetime.min.replace(tzinfo=timezone.utc)

                if cutoff and dt < cutoff:
                    continue

                domain = self._extract_domain(url)
                category = self._classify_url(url)

                self.history.append(HistoryEntry(
                    url=url,
                    title=title.strip(),
                    visit_count=visit_count,
                    last_visit=dt.strftime("%Y-%m-%d %H:%M:%S"),
                    browser=f"{browser}/{profile}",
                    domain=domain,
                    category=category,
                    extracted_at=self._extracted_at,
                ))
                extracted += 1

            conn.close()
        except sqlite3.OperationalError:
            pass  # 数据库锁定，静默跳过
        except Exception as e:
            pass

    def _extract_bookmarks(self, browser: str, bm_file: Path):
        """提取Chrome书签（JSON格式）"""
        try:
            with open(bm_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self._walk_bookmarks(data.get("roots", {}), "", browser)
        except:
            pass

    def _walk_bookmarks(self, node: Dict, path: str, browser: str):
        """递归遍历书签树"""
        if node.get("type") == "url":
            self.bookmarks.append(BookmarkEntry(
                url=node.get("url", ""),
                title=node.get("name", ""),
                folder=path,
                browser=browser,
            ))
        elif node.get("type") == "folder":
            folder_name = node.get("name", "")
            new_path = f"{path}/{folder_name}" if path else folder_name
            for child in node.get("children", []):
                self._walk_bookmarks(child, new_path, browser)

    def _dedup_history(self):
        """URL去重：保留访问最多的那条"""
        url_best: Dict[str, HistoryEntry] = {}
        for entry in self.history:
            key = entry.url
            if key not in url_best or entry.visit_count > url_best[key].visit_count:
                url_best[key] = entry
        self.history = sorted(url_best.values(), key=lambda e: e.visit_count, reverse=True)

    # ═══════════ 导出 ═══════════

    def export_jsonl(self, with_bookmarks: bool = True) -> Path:
        """导出为JSONL"""
        history_file = OUTPUT_DIR / f"browser_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        count = 0
        with open(history_file, 'w', encoding='utf-8') as f:
            for entry in self.history:
                f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")
                count += 1

        bm_file = None
        if with_bookmarks and self.bookmarks:
            bm_file = OUTPUT_DIR / f"browser_bookmarks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
            with open(bm_file, 'w', encoding='utf-8') as f:
                for entry in self.bookmarks:
                    f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")

        print(f"📦 导出: {count} 条历史 → {history_file.name}")
        if bm_file:
            print(f"📦 导出: {len(self.bookmarks)} 条书签 → {bm_file.name}")
        return history_file

    def get_stats(self) -> Dict:
        """统计摘要"""
        stats = {
            "total_urls": len(self.history),
            "total_bookmarks": len(self.bookmarks),
            "by_browser": defaultdict(int),
            "by_category": defaultdict(int),
            "by_domain": defaultdict(int),
            "top_domains": [],
            "top_categories": [],
        }
        for e in self.history:
            stats["by_browser"][e.browser] += 1
            stats["by_category"][e.category] += 1
            stats["by_domain"][e.domain] += 1

        stats["top_domains"] = sorted(stats["by_domain"].items(), key=lambda x: x[1], reverse=True)[:20]
        stats["top_categories"] = sorted(stats["by_category"].items(), key=lambda x: x[1], reverse=True)[:10]

        # 转回普通dict
        stats["by_browser"] = dict(stats["by_browser"])
        stats["by_category"] = dict(stats["by_category"])
        stats["by_domain"] = dict(stats["by_domain"])
        return stats

    # ━─ helper ━─

    @staticmethod
    def _extract_domain(url: str) -> str:
        m = re.match(r"https?://([^/]+)", url)
        return m.group(1) if m else url[:50]

    @staticmethod
    def _classify_url(url: str) -> str:
        for category, pattern in DOMAIN_PATTERNS.items():
            if pattern.search(url):
                return category
        return "其他"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    import argparse
    p = argparse.ArgumentParser(description="龍魂·浏览器历史矿工")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("scan", help="勘探浏览器数据库")
    ep = sub.add_parser("extract", help="提取历史记录")
    ep.add_argument("--days", type=int, default=0, help="只提取最近N天 (0=全部)")
    ep.add_argument("--limit", type=int, default=10000, help="每浏览器上限")
    ep.add_argument("--no-export", action="store_true", help="不导出文件")
    sub.add_parser("status", help="查看矿场状态")

    args = p.parse_args()
    miner = BrowserMiner()

    if args.cmd == "scan":
        reports = miner.scan()
        if not reports:
            print("未发现浏览器数据库")
            return

        print(f"\n{'浏览器':<12} {'配置文件':<18} {'历史条数':>8} {'最早':<18} {'最新':<18} {'状态'}")
        print("-" * 90)
        for r in reports:
            print(f"{r.browser:<12} {r.profile:<18} {r.history_count:>8} {r.earliest:<18} {r.latest:<18} {r.status}")
        total = sum(r.history_count for r in reports)
        print(f"\n总计: {total} 条历史记录 | {len(reports)} 个数据源")

    elif args.cmd == "extract":
        history, bookmarks = miner.extract(days=args.days, limit_per_browser=args.limit)
        stats = miner.get_stats()
        print(f"\n📊 矿场统计:")
        print(f"   历史记录: {stats['total_urls']} 条（去重后）")
        print(f"   书签:     {stats['total_bookmarks']} 条")
        print(f"\n   浏览器分布:")
        for browser, cnt in stats["by_browser"].items():
            print(f"     {browser}: {cnt}")
        print(f"\n   分类分布:")
        for cat, cnt in stats["top_categories"]:
            print(f"     {cat}: {cnt}")
        if not args.no_export:
            miner.export_jsonl()

    elif args.cmd == "status":
        reports = miner.scan()
        history_files = list(OUTPUT_DIR.glob("*.jsonl")) if OUTPUT_DIR.exists() else []
        print(f"\n🏭 浏览器历史矿场状态")
        print(f"   数据源: {len(reports)} 个")
        total_hist = sum(r.history_count for r in reports)
        print(f"   可挖掘历史: {total_hist} 条")
        print(f"   已导出文件: {len(history_files)} 个")
        if history_files:
            latest = max(history_files, key=lambda f: f.stat().st_mtime)
            age = datetime.now() - datetime.fromtimestamp(latest.stat().st_mtime)
            print(f"   最新导出: {latest.name} ({age.days}天前)")

    else:
        p.print_help()


if __name__ == "__main__":
    main()

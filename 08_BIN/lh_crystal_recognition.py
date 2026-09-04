#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·甲子·未时·䷄需-CRYSTAL-RECOGNITION-v2.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂·水晶识别知识库 v2.0 · 阻断日志自动入库+智能标签+现实打脸报告
DNA: #龍芯⚡️丙午·乙未·甲子·未时·䷄需-CRYSTAL-RECOGNITION-v2.0

理念:
  平台每一次"太监"/"屏蔽"/"限流"不是失败，而是射向黑箱的一束光。
  把每一条阻断日志变成水晶样本，等光照够了，黑箱就透明了。

三阶段:
  自动抓证 → lh_platform_block_logger 已做
  入库水晶识别 → 本引擎（自动标签+结构化存储+SQLite索引+平台专属模式检测）
  现实打脸 → 聚合报告+时间线+模式挖掘+一键导出

v2.0 新增:
  - 微博·微信公众号·B站 三大重灾区平台专属标签+模式检测
  - 17种阻断类型覆盖（新增热搜降权/话题屏蔽/转发不可见/视频审核/弹幕过滤/稿件限流/文章不通过/被投诉删除/原创争议）
  - 10组内容模式检测（新增内容审查/流量操纵/创作者权益/言论空间）
  - 平台专属6组模式检测（微博3组·微信3组·B站3组）

用法:
  # 扫描并摄入所有未入库的阻断日志
  python3 bin/lh_crystal_recognition.py scan

  # 单条喂养
  python3 bin/lh_crystal_recognition.py feed --session-id 20260711_141131

  # 查询
  python3 bin/lh_crystal_recognition.py query --platform CSDN
  python3 bin/lh_crystal_recognition.py query --tag "内容审查" --limit 20

  # 生成"现实打脸"报告
  python3 bin/lh_crystal_recognition.py report --platform all
  python3 bin/lh_crystal_recognition.py report --platform CSDN --format md

  # 统计概览
  python3 bin/lh_crystal_recognition.py stats

联动:
  lh_platform_block_logger.py → 生成日志后自动调用 feed →
  lh_crystal_recognition.py → 自动标签+入库+
  可被查询/报告引擎调用 → 现实打脸报告
"""

import argparse
import hashlib
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---- 常量 ----
TZ = timezone(timedelta(hours=8))
DNA = "#龍芯⚡️丙午·乙未·甲子·未时·䷄需-CRYSTAL-RECOGNITION-v2.0"
BASE_DIR = Path(__file__).resolve().parent.parent
CRYSTAL_DIR = BASE_DIR / "L7_数据层" / "crystal_knowledge"
BLOCK_LOGS_DIR = BASE_DIR / "reports" / "block_logs"

# 数据文件
INDEX_PATH = CRYSTAL_DIR / "crystal_index.json"
CHAIN_PATH = CRYSTAL_DIR / "crystal_chain.jsonl"
TAGS_PATH = CRYSTAL_DIR / "crystal_tags.json"
DB_PATH = CRYSTAL_DIR / "crystal.db"


# ---- SQLite Schema ----
def init_db():
    """初始化 SQLite 数据库"""
    db = sqlite3.connect(str(DB_PATH))
    db.execute("""
        CREATE TABLE IF NOT EXISTS crystals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            timestamp TEXT NOT NULL,
            platform TEXT NOT NULL,
            block_type TEXT NOT NULL,
            trigger TEXT,
            title TEXT,
            tags TEXT,
            summary TEXT,
            verdict TEXT,
            has_screenshot INTEGER DEFAULT 0,
            url TEXT,
            dna TEXT,
            raw_json TEXT,
            ingested_at TEXT NOT NULL
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS crystal_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crystal_id INTEGER REFERENCES crystals(id),
            tag TEXT NOT NULL,
            tag_type TEXT NOT NULL,
            UNIQUE(crystal_id, tag, tag_type)
        )
    """)
    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_crystals_platform ON crystals(platform);
    """)
    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_crystals_block_type ON crystals(block_type);
    """)
    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_crystals_verdict ON crystals(verdict);
    """)
    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_crystals_timestamp ON crystals(timestamp);
    """)
    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_tags_tag ON crystal_tags(tag);
    """)
    db.commit()
    return db


# ---- 标签分类引擎 ----
class CrystalTagger:
    """自动标签分类器 — 根据内容自动打标签"""

    def __init__(self):
        self.tags_config = self._load_tags()

    def _load_tags(self) -> Dict[str, Any]:
        if TAGS_PATH.exists():
            with open(TAGS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def tag(self, evidence: Dict[str, Any]) -> List[Tuple[str, str]]:
        """
        对一条阻断证据自动打标签
        返回 [(标签, 类型), ...]
        类型: platform / block / trigger / verdict / pattern / severity
        """
        tags: List[Tuple[str, str]] = []

        # 1. 平台标签
        platform = evidence.get("platform", "Unknown")
        platform_info = self._match_platform(platform)
        tags.append((f"platform:{platform}", "platform"))
        if platform_info:
            tags.append((f"category:{platform_info.get('category', 'Unknown')}", "category"))
            hostile = platform_info.get("hostile_score", 0.5)
            tags.append((f"hostile:{hostile}", "hostile_score"))

        # 2. 阻断类型标签
        block_type = evidence.get("block_type", "其他")
        block_info = self._match_block_type(block_type)
        tags.append((f"block:{block_type}", "block"))
        if block_info:
            tags.append((f"block_category:{block_info.get('category', '未分类')}", "block_category"))
            sev = block_info.get("severity", 4)
            tags.append((f"severity:{sev}", "severity"))

        # 3. 触发时机标签
        trigger = evidence.get("trigger", "")
        if trigger:
            tags.append((f"trigger:{trigger}", "trigger"))

        # 4. 防篡改判定标签
        tamper = evidence.get("tamper_scan", {})
        verdict = tamper.get("verdict", "N/A")
        tags.append((f"verdict:{verdict}", "verdict"))

        # 5. 内容模式检测
        title = evidence.get("title", "")
        summary = evidence.get("summary", "")
        full_text = f"{title} {summary}"
        patterns = self._detect_patterns(full_text, platform=platform)
        for pattern, confidence in patterns:
            tags.append((f"pattern:{pattern}", "pattern"))

        # 6. 证据质量标签
        has_ss = evidence.get("has_screenshot", False) or bool(evidence.get("evidence", {}).get("screenshot"))
        tags.append((f"evidence:has_screenshot={has_ss}", "evidence_quality"))

        return tags

    def _match_platform(self, platform: str) -> Optional[Dict]:
        platforms = self.tags_config.get("platforms", {})
        p_lower = platform.lower()
        for name, info in platforms.items():
            if name.lower() == p_lower or p_lower in [a.lower() for a in info.get("aliases", [])]:
                return info
        return platforms.get("其他")

    def _match_block_type(self, block_type: str) -> Optional[Dict]:
        block_types = self.tags_config.get("block_types", {})
        bt_lower = block_type.lower()
        for name, info in block_types.items():
            aliases = [a.lower() for a in info.get("aliases", [])]
            if name.lower() in bt_lower or bt_lower in name.lower():
                return info
            for alias in aliases:
                if alias in bt_lower:
                    return info
        return block_types.get("其他")

    def _detect_patterns(self, text: str, platform: str = "") -> List[Tuple[str, float]]:
        """从文本中检测内容模式（v2.0 新增平台专属检测）"""
        patterns: List[Tuple[str, float]] = []
        pattern_rules = self.tags_config.get("pattern_detection", {})
        keywords_map = pattern_rules.get("keywords_map", {})
        text_lower = text.lower()

        # 通用模式检测
        for pattern_name, keywords in keywords_map.items():
            hits = sum(1 for kw in keywords if kw.lower() in text_lower)
            if hits > 0:
                confidence = min(hits / max(len(keywords), 1), 1.0) * 0.8 + 0.2
                patterns.append((pattern_name, round(confidence, 2)))

        # 平台专属模式检测 (v2.0)
        if platform:
            ps_patterns = pattern_rules.get("platform_specific_patterns", {}).get(platform, {})
            for ps_name, ps_keywords in ps_patterns.items():
                hits = sum(1 for kw in ps_keywords if kw.lower() in text_lower)
                if hits > 0:
                    confidence = min(hits / max(len(ps_keywords), 1), 1.0) * 0.85 + 0.15
                    patterns.append((f"{platform}·{ps_name}", round(confidence, 2)))

        # 标题检测
        detection_rules = pattern_rules.get("detection_rules", {})
        title = text[:100]
        for rule_name, rule in detection_rules.items():
            if "keywords" in rule:
                hit = any(kw in title for kw in rule.get("keywords", []))
                if hit:
                    patterns.append((rule_name, 0.9))

        return patterns


# ---- 水晶索引 ----
class CrystalIndex:
    """内存+磁盘双重索引"""

    def __init__(self):
        self._data = self._load()

    def _load(self) -> Dict[str, Any]:
        if INDEX_PATH.exists():
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "name": "龍魂·水晶识别知识库",
            "dna": DNA,
            "created": datetime.now(TZ).isoformat(),
            "total_crystals": 0,
            "last_ingest": None,
            "ingested_sessions": [],
            "stats": {
                "by_platform": {},
                "by_block_type": {},
                "by_verdict": {},
                "by_severity": {},
            },
        }

    def save(self):
        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def is_ingested(self, session_id: str) -> bool:
        return session_id in self._data["ingested_sessions"]

    def add(self, session_id: str, crystal: Dict[str, Any]):
        self._data["total_crystals"] += 1
        self._data["last_ingest"] = datetime.now(TZ).isoformat()
        if session_id not in self._data["ingested_sessions"]:
            self._data["ingested_sessions"].append(session_id)

        # 更新统计
        platform = crystal.get("platform", "Unknown")
        block_type = crystal.get("block_type", "其他")

        self._data["stats"]["by_platform"][platform] = \
            self._data["stats"]["by_platform"].get(platform, 0) + 1
        self._data["stats"]["by_block_type"][block_type] = \
            self._data["stats"]["by_block_type"].get(block_type, 0) + 1

        verdict = crystal.get("tamper_scan", {}).get("verdict", "N/A")
        self._data["stats"]["by_verdict"][verdict] = \
            self._data["stats"]["by_verdict"].get(verdict, 0) + 1

        self.save()

    def get_stats(self) -> Dict[str, Any]:
        return self._data["stats"]

    def get_ingested(self) -> List[str]:
        return self._data["ingested_sessions"]


# ---- 主引擎 ----
class CrystalRecognition:
    """水晶识别主引擎"""

    def __init__(self):
        self.db = init_db()
        self.tagger = CrystalTagger()
        self.index = CrystalIndex()

    def scan_and_ingest(self) -> int:
        """扫描 block_logs/ 目录，自动摄入未入库的条目"""
        if not BLOCK_LOGS_DIR.exists():
            print("📭 block_logs/ 目录不存在")
            return 0

        ingested = 0
        for session_dir in sorted(BLOCK_LOGS_DIR.iterdir()):
            if not session_dir.is_dir():
                continue
            ev_path = session_dir / "evidence.json"
            if not ev_path.exists():
                continue

            session_id = session_dir.name
            if self.index.is_ingested(session_id):
                continue

            with open(ev_path, "r", encoding="utf-8") as f:
                evidence = json.load(f)

            # 检查证据完整性
            screenshot = (session_dir / f"{session_id}_screenshot.png").exists()
            evidence["has_screenshot"] = screenshot
            evidence["session_dir"] = str(session_dir)

            self._ingest_one(evidence, session_id)
            ingested += 1
            print(f"  💎 摄入: {session_id} | {evidence.get('platform', '?')} | {evidence.get('block_type', '?')}")

        print(f"\n✅ 摄入完成: {ingested} 条新水晶")
        return ingested

    def feed(self, session_id: str) -> bool:
        """喂养单条阻断日志"""
        ev_path = BLOCK_LOGS_DIR / session_id / "evidence.json"
        if not ev_path.exists():
            print(f"❌ 未找到证据: {ev_path}")
            return False

        if self.index.is_ingested(session_id):
            print(f"⚠️  已入库: {session_id}")
            return False

        with open(ev_path, "r", encoding="utf-8") as f:
            evidence = json.load(f)

        screenshot = (BLOCK_LOGS_DIR / session_id / f"{session_id}_screenshot.png").exists()
        evidence["has_screenshot"] = screenshot
        evidence["session_dir"] = str(BLOCK_LOGS_DIR / session_id)

        self._ingest_one(evidence, session_id)
        print(f"💎 水晶摄入: {session_id}")
        return True

    def feed_direct(self, evidence: Dict[str, Any], session_id: str) -> bool:
        """直接喂养（由 lh_platform_block_logger 调用）"""
        if self.index.is_ingested(session_id):
            return False
        self._ingest_one(evidence, session_id)
        return True

    def _ingest_one(self, evidence: Dict[str, Any], session_id: str):
        """内部：摄入一条"""
        # 1. 自动标签
        tags = self.tagger.tag(evidence)

        # 2. 写入 SQLite
        cursor = self.db.cursor()
        ts = datetime.now(TZ).isoformat()
        cursor.execute("""
            INSERT INTO crystals
            (session_id, timestamp, platform, block_type, trigger, title, tags, summary,
             verdict, has_screenshot, url, dna, raw_json, ingested_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            evidence.get("session_id", ts),
            evidence.get("platform", "Unknown"),
            evidence.get("block_type", "其他"),
            evidence.get("trigger", ""),
            evidence.get("title", ""),
            evidence.get("tags", ""),
            evidence.get("summary", ""),
            evidence.get("tamper_scan", {}).get("verdict", "N/A"),
            1 if evidence.get("has_screenshot") else 0,
            evidence.get("url", ""),
            evidence.get("dna", DNA),
            json.dumps(evidence, ensure_ascii=False),
            ts,
        ))
        crystal_id = cursor.lastrowid

        # 3. 写入标签关联
        for tag, tag_type in tags:
            try:
                cursor.execute("""
                    INSERT INTO crystal_tags (crystal_id, tag, tag_type)
                    VALUES (?, ?, ?)
                """, (crystal_id, tag, tag_type))
            except sqlite3.IntegrityError:
                pass  # 重复标签跳过

        self.db.commit()

        # 4. 写入 JSONL 链
        chain_entry = {
            "session_id": session_id,
            "platform": evidence.get("platform"),
            "block_type": evidence.get("block_type"),
            "title": evidence.get("title"),
            "tags_list": [t[0] for t in tags],
            "ingested_at": ts,
            "dna": DNA,
        }
        with open(CHAIN_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(chain_entry, ensure_ascii=False) + "\n")

        # 5. 更新索引
        self.index.add(session_id, evidence)

    def query(self, **filters) -> List[Dict]:
        """查询水晶"""
        cursor = self.db.cursor()
        sql = "SELECT * FROM crystals WHERE 1=1"
        params: List[Any] = []

        if filters.get("platform"):
            sql += " AND platform = ?"
            params.append(filters["platform"])
        if filters.get("block_type"):
            sql += " AND block_type LIKE ?"
            params.append(f"%{filters['block_type']}%")
        if filters.get("verdict"):
            sql += " AND verdict = ?"
            params.append(filters["verdict"])
        if filters.get("tag"):
            sql += """ AND id IN (
                SELECT crystal_id FROM crystal_tags WHERE tag LIKE ?
            )"""
            params.append(f"%{filters['tag']}%")
        if filters.get("from_date"):
            sql += " AND timestamp >= ?"
            params.append(filters["from_date"])
        if filters.get("to_date"):
            sql += " AND timestamp <= ?"
            params.append(filters["to_date"])

        sql += " ORDER BY timestamp DESC"
        limit = filters.get("limit", 50)
        sql += f" LIMIT {int(limit)}"

        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]
        results = [dict(zip(cols, row)) for row in rows]

        # 附加标签
        for r in results:
            cursor.execute(
                "SELECT tag, tag_type FROM crystal_tags WHERE crystal_id = ?",
                (r["id"],)
            )
            r["_tags"] = [{"tag": t[0], "type": t[1]} for t in cursor.fetchall()]

        return results

    def get_stats(self) -> Dict[str, Any]:
        """获取统计概览"""
        return {
            "index": self.index._data,
            "total": self.index._data["total_crystals"],
            "by_platform": self.index._data["stats"]["by_platform"],
            "by_block_type": self.index._data["stats"]["by_block_type"],
            "by_verdict": self.index._data["stats"]["by_verdict"],
        }

    def generate_report(self, platform: str = "all", fmt: str = "md") -> str:
        """生成'现实打脸'聚合报告"""
        cursor = self.db.cursor()

        # 平台过滤
        platform_filter = ""
        params: List[Any] = []
        if platform != "all":
            platform_filter = " WHERE platform = ?"
            params.append(platform)

        # 总览
        cursor.execute(f"SELECT COUNT(*) FROM crystals{platform_filter}", params)
        total = cursor.fetchone()[0]

        # 按平台统计
        cursor.execute("""
            SELECT platform, COUNT(*) as cnt
            FROM crystals
            GROUP BY platform ORDER BY cnt DESC
        """)
        by_platform = cursor.fetchall()

        # 按阻断类型统计
        cursor.execute("""
            SELECT block_type, COUNT(*) as cnt
            FROM crystals
            GROUP BY block_type ORDER BY cnt DESC
        """)
        by_block = cursor.fetchall()

        # 按严重度统计
        cursor.execute("""
            SELECT t.tag, COUNT(*) as cnt
            FROM crystal_tags t
            WHERE t.tag_type = 'severity'
            GROUP BY t.tag ORDER BY t.tag DESC
        """)
        by_severity = cursor.fetchall()

        # 最近的记录
        cursor.execute(f"""
            SELECT session_id, platform, block_type, title, timestamp
            FROM crystals{platform_filter}
            ORDER BY timestamp DESC LIMIT 10
        """, params)
        recent = cursor.fetchall()

        # 证据质量
        cursor.execute(f"""
            SELECT SUM(has_screenshot) as with_ss, COUNT(*) as total
            FROM crystals{platform_filter}
        """, params)
        quality_row = cursor.fetchone()
        with_ss = quality_row[0] if quality_row else 0
        total_count = quality_row[1] if quality_row else 0

        # 趋势时间线（按日期）
        cursor.execute(f"""
            SELECT substr(timestamp, 1, 10) as date, COUNT(*) as cnt
            FROM crystals{platform_filter}
            GROUP BY date ORDER BY date
        """, params)
        timeline = cursor.fetchall()

        if fmt == "json":
            return json.dumps({
                "total": total,
                "by_platform": dict(by_platform),
                "by_block_type": dict(by_block),
                "by_severity": dict(by_severity),
                "recent": [dict(zip(["session_id", "platform", "block_type", "title", "timestamp"], r)) for r in recent],
                "evidence_quality": {"with_screenshots": with_ss, "total": total_count, "rate": f"{with_ss/max(total_count,1)*100:.1f}%"},
                "timeline": dict([(d, c) for d, c in timeline]),
            }, ensure_ascii=False, indent=2)

        # Markdown 报告
        lines = [
            f"# 🔮 龍魂·水晶识别·现实打脸报告",
            f"> DNA: `{DNA}`",
            f"> 生成时间: {datetime.now(TZ).isoformat()}",
            f"> 目标平台: {platform}",
            f"> 水晶总数: **{total}**",
            f"",
            f"---",
            f"",
            f"## 📊 平台分布",
            f"",
            f"| 平台 | 阻断次数 | 占比 |",
            f"|:---|:---:|:---:|",
        ]
        for p_name, cnt in by_platform:
            pct = cnt / max(total, 1) * 100
            bar = "█" * int(pct / 2)
            lines.append(f"| {p_name} | {cnt} | {bar} {pct:.1f}% |")
        lines.append("")
        lines.append("## 🚫 阻断类型分布")
        lines.append("")
        lines.append("| 阻断类型 | 次数 |")
        lines.append("|:---|:---:|")
        for bt, cnt in by_block:
            lines.append(f"| {bt} | {cnt} |")
        lines.append("")
        lines.append("## ⚠️ 严重度分布")
        lines.append("")
        lines.append("| 严重度 | 次数 |")
        lines.append("|:---|:---:|")
        for sev_tag, cnt in by_severity:
            sev_num = sev_tag.split(":")[-1]
            emoji = {9: "🔴", 8: "🟠", 7: "🟡", 6: "🟡", 5: "🔵", 4: "⚪"}.get(int(sev_num), "⚪")
            lines.append(f"| {emoji} {sev_tag} | {cnt} |")
        lines.append("")
        lines.append("## 📈 时间线趋势")
        lines.append("")
        if timeline:
            lines.append("| 日期 | 阻断次数 |")
            lines.append("|:---|:---:|")
            for date, cnt in timeline:
                lines.append(f"| {date} | {cnt} |")
        lines.append("")
        lines.append("## 📸 证据质量")
        lines.append("")
        lines.append(f"- 含截图: {with_ss}/{total_count} ({with_ss/max(total_count,1)*100:.1f}%)")
        lines.append(f"- 纯文本: {total_count - with_ss}/{total_count} ({(total_count-with_ss)/max(total_count,1)*100:.1f}%)")
        lines.append("")
        lines.append("## 📋 最近10条")
        lines.append("")
        if recent:
            lines.append("| 时间 | 平台 | 阻断类型 | 标题 |")
            lines.append("|:---|:---|:---|:---|")
            for r in recent:
                title = (r[3] or "")[:40]
                lines.append(f"| {r[4]} | {r[1]} | {r[2]} | {title} |")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("> **逢阻必记 · 留痕为证 · 水晶入库 · 现实打脸**")
        lines.append(f"> 引擎: `bin/lh_crystal_recognition.py` v1.0")
        lines.append(f"> DNA: `{DNA}`")

        return "\n".join(lines)

    def close(self):
        self.db.close()


# ---- CLI ----
def main():
    parser = argparse.ArgumentParser(
        description="🔮 龍魂·水晶识别知识库 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
DNA: {DNA}

用法:
  # 扫描摄入
  python3 bin/lh_crystal_recognition.py scan

  # 单条喂养
  python3 bin/lh_crystal_recognition.py feed --session-id 20260711_141131

  # 查询
  python3 bin/lh_crystal_recognition.py query --platform CSDN
  python3 bin/lh_crystal_recognition.py query --tag "内容审查"

  # 报告
  python3 bin/lh_crystal_recognition.py report
  python3 bin/lh_crystal_recognition.py report --platform CSDN --format json

  # 统计
  python3 bin/lh_crystal_recognition.py stats
        """,
    )

    sub = parser.add_subparsers(dest="command", help="命令")

    # scan
    p_scan = sub.add_parser("scan", help="扫描 block_logs/ 并摄入新条目")

    # feed
    p_feed = sub.add_parser("feed", help="喂养单条阻断日志")
    p_feed.add_argument("--session-id", required=True, help="会话ID")

    # query
    p_query = sub.add_parser("query", help="查询水晶")
    p_query.add_argument("--platform", help="按平台过滤")
    p_query.add_argument("--tag", help="按标签过滤")
    p_query.add_argument("--block-type", help="按阻断类型过滤")
    p_query.add_argument("--verdict", help="按防篡改判定过滤")
    p_query.add_argument("--limit", type=int, default=20, help="返回条数限制")
    p_query.add_argument("--format", choices=["table", "json"], default="table")

    # report
    p_report = sub.add_parser("report", help="生成现实打脸报告")
    p_report.add_argument("--platform", default="all", help="目标平台")
    p_report.add_argument("--format", choices=["md", "json"], default="md")
    p_report.add_argument("--output", help="输出文件路径")

    # stats
    p_stats = sub.add_parser("stats", help="统计概览")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    engine = CrystalRecognition()

    try:
        if args.command == "scan":
            print("🔮 水晶识别·扫描摄入...")
            count = engine.scan_and_ingest()
            if count == 0:
                print("   (没有新水晶)")

        elif args.command == "feed":
            engine.feed(args.session_id)

        elif args.command == "query":
            filters = {}
            if args.platform:
                filters["platform"] = args.platform
            if args.tag:
                filters["tag"] = args.tag
            if args.block_type:
                filters["block_type"] = args.block_type
            if args.verdict:
                filters["verdict"] = args.verdict
            filters["limit"] = args.limit

            results = engine.query(**filters)
            if args.format == "json":
                print(json.dumps(results, ensure_ascii=False, indent=2))
            else:
                if not results:
                    print("🔮 暂无匹配的水晶")
                else:
                    print(f"🔮 查询结果 ({len(results)} 条):")
                    print(f"{'时间':<20} {'平台':<10} {'阻断类型':<15} {'标题':<30}")
                    print("-" * 80)
                    for r in results:
                        ts = (r.get("timestamp") or "")[:16]
                        pl = (r.get("platform") or "")[:10]
                        bt = (r.get("block_type") or "")[:15]
                        ti = (r.get("title") or "")[:30]
                        print(f"{ts:<20} {pl:<10} {bt:<15} {ti:<30}")

        elif args.command == "report":
            report = engine.generate_report(
                platform=args.platform,
                fmt=args.format,
            )
            if args.output:
                Path(args.output).parent.mkdir(parents=True, exist_ok=True)
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(report)
                print(f"📄 报告已写入: {args.output}")
            else:
                print(report)

        elif args.command == "stats":
            stats = engine.get_stats()
            print("🔮 水晶识别·统计概览")
            print("=" * 40)
            print(f"  总水晶: {stats['total']}")
            print(f"\n  按平台:")
            for p, c in sorted(stats["by_platform"].items(), key=lambda x: -x[1]):
                print(f"    {p}: {c}")
            print(f"\n  按阻断类型:")
            for bt, c in sorted(stats["by_block_type"].items(), key=lambda x: -x[1]):
                print(f"    {bt}: {c}")
            print(f"\n  按防篡改判定:")
            for v, c in stats["by_verdict"].items():
                print(f"    {v}: {c}")

    finally:
        engine.close()


if __name__ == "__main__":
    main()

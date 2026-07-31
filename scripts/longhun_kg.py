# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂知识图谱 · 通心译实体抽取与来源链保留

从已下载的 Notion Markdown 中抽取：
- CNSH 中文原生标识
- 龍魂 DNA 追溯码
- 通心译英文术语及其中文映射
- 核心哲学/技术种子概念

并建立共现实体关系，保留原始时间戳与本地来源链。

DNA: #龍芯⚡️2026-06-23-LONGHUN-KG-v1.0
"""
from __future__ import annotations

import pathlib
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Set, Tuple

HOME = pathlib.Path.home()
OUT_DIR = HOME / ".longhun" / "notion_pages"
DB_PATH = OUT_DIR / "notion_pages.db"
REPORT_PATH = OUT_DIR / "KNOWLEDGE_GRAPH.md"

CST = timezone(timedelta(hours=8))

DNA = "#龍芯⚡️2026-06-23-LONGHUN-KG-v1.0"

# 核心种子概念：老大创作的哲学/技术/主权关键词
SEED_CONCEPTS: List[str] = [
    "龍魂", "龍芯", "CNSH", "通心译", "三色审计", "DNA追溯", "六层来源链",
    "宪法层", "君子协议", "UID9622", "数据主权", "数字身份", "魂灵ID",
    "私云归藏", "烽火传心", "龍芯", "鸿蒙", "北斗", "星闪", "e-CNY",
    "369", "太极", "易经", "河图洛书", "道德经", "五行", "八卦", "64卦",
    "甲骨文", "黎曼猜想", "不动点", "淬炼", "推演", "靈脈", "機靈",
    "歸藏", "數字人民幣", "自主云", "Cloud 5",
    "老大", "宝宝", "诸葛鑫", "指纹", "确认码",
]

# 通用停用词 + 页面结构噪音词
STOPWORDS: Set[str] = set(
    "的 了 和 是 在 我 有 就 不 人 都 一 一个 上 也 很 到 说 要 去 你 会 着 没有 看 好 自己 这 那 我们 可以 这个 这些 为 之 与 而 及 以 于 被 把 给 让 向 从 对 将 就 等 吗 呢 吧 啊 哦 嗯".split()
    + "创建 分类 修改 子页面 状态 步骤 版本 时间 日期 北京 北京时间 标题 内容 页面 工作区 无标题 标签 系统 文件 目录 路径".split()
)

# 通心译术语（英文 -> 中文）
TONGXIN_TERMS: Dict[str, str] = {
    "Artificial Intelligence": "人工智能/機靈",
    "Machine Learning": "機器學習/煉器",
    "Deep Learning": "深度學習/深觀",
    "Neural Network": "神經網絡/靈脈",
    "Model": "模型/器",
    "Training": "訓練/淬煉",
    "Inference": "推理/推演",
    "Dataset": "數據集/料庫",
    "Algorithm": "算法/術",
    "Parameter": "參數/變量",
    "Embedding": "嵌入/蘊藏",
    "Token": "詞元/字靈",
    "Prompt": "提示/啟機",
    "Fine-tuning": "微調/琢玉",
    "API": "應用接口/通關",
    "Endpoint": "端點/關口",
    "Latency": "延遲/遲滯",
    "Throughput": "吞吐量/流率",
    "Vector": "向量/矢蘊",
    "Clustering": "聚類/歸群",
    "Classification": "分類/別類",
    "Regression": "回歸/返源",
    "Overfitting": "過擬合/刻舟",
    "Regularization": "正則化/規矩",
    "Computer Vision": "計算機視覺/電眼",
    "Convolution": "卷積/摺紋",
    "Feature Map": "特徵圖/神韻圖",
    "Object Detection": "目標檢測/識物",
    "Segmentation": "分割/析像",
    "GAN": "生成對抗網絡/陰陽器",
    "Diffusion Model": "擴散模型/墨染",
    "Upscaling": "上採樣/放大/顯微",
    "Filter": "濾波器/篩",
    "Kernel": "核/芯",
    "Pooling": "池化/歸聚",
    "Attention": "注意力/專注",
    "Transformer": "變換器/化境",
    "Speech Recognition": "語音識別/聽聲",
    "Text-to-Speech": "文本轉語音/朗誦",
    "ASR": "自動語音識別/耳順",
    "TTS": "文本轉語音系統/口宣",
    "Phoneme": "音素/聲元",
    "Spectrogram": "頻譜圖/聲紋圖",
    "MFCC": "梅爾頻率倒譜系數/聲紋徵",
    "Wav": "波形/聲波",
    "Sampling Rate": "採樣率/捕聲頻",
    "Noise Reduction": "降噪/去雜",
    "Speaker Diarization": "說話人分離/辨聲歸主",
    "Prosody": "韻律/聲情",
}


def now_cst() -> str:
    return datetime.now(CST).isoformat()


def init_db() -> sqlite3.Connection:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL,
            tongxin_zh TEXT,
            first_seen_page_id TEXT,
            first_seen_at TEXT,
            occurrence_count INTEGER DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS entity_occurrences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_id INTEGER NOT NULL,
            page_id TEXT NOT NULL,
            snippet TEXT,
            char_offset INTEGER,
            local_md_path TEXT,
            notion_url TEXT,
            page_created TEXT,
            page_modified TEXT,
            extracted_at TEXT,
            FOREIGN KEY(entity_id) REFERENCES entities(id),
            FOREIGN KEY(page_id) REFERENCES pages(id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS relations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER NOT NULL,
            target_id INTEGER NOT NULL,
            relation_type TEXT NOT NULL,
            page_id TEXT NOT NULL,
            context TEXT,
            weight REAL DEFAULT 1.0,
            extracted_at TEXT,
            FOREIGN KEY(source_id) REFERENCES entities(id),
            FOREIGN KEY(target_id) REFERENCES entities(id),
            FOREIGN KEY(page_id) REFERENCES pages(id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS kg_meta (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_ent_type ON entities(type)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_occ_page ON entity_occurrences(page_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_rel_page ON relations(page_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_rel_pair ON relations(source_id, target_id)")
    # 记录每个页面是否已抽取
    try:
        conn.execute("ALTER TABLE pages ADD COLUMN kg_extracted_at TEXT")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    return conn


def load_tongxin_patterns() -> List[Tuple[str, str, re.Pattern]]:
    """预编译通心译英文术语匹配模式（长词优先）。"""
    terms = sorted(TONGXIN_TERMS.items(), key=lambda x: len(x[0]), reverse=True)
    out = []
    for en, zh in terms:
        pat = re.compile(r"\b" + re.escape(en) + r"\b", re.IGNORECASE)
        out.append((en, zh, pat))
    return out


def load_seed_patterns() -> List[Tuple[str, re.Pattern]]:
    seeds = sorted(SEED_CONCEPTS, key=len, reverse=True)
    return [(s, re.compile(re.escape(s))) for s in seeds]


def extract_entities(
    text: str,
    tongxin_patterns: List[Tuple[str, str, re.Pattern]],
    seed_patterns: List[Tuple[str, re.Pattern]],
) -> List[Tuple[str, str, Optional[str], int]]:
    """
    从文本中抽取实体。
    返回 [(name, type, tongxin_zh, offset), ...]
    """
    found: List[Tuple[str, str, Optional[str], int]] = []
    seen_spans: Set[Tuple[int, int]] = set()

    def add_span(start: int, end: int, name: str, etype: str, tzh: Optional[str] = None):
        if any(start < e2 and end > s2 for s2, e2 in seen_spans):
            return
        seen_spans.add((start, end))
        found.append((name, etype, tzh, start))

    # CNSH 标识
    for m in re.finditer(r"CNSH_[A-Za-z0-9_\u4e00-\u9fff]+", text):
        add_span(m.start(), m.end(), m.group(0), "cnsh")

    # DNA 追溯码
    for pat in [
        re.compile(r"#龍芯⚡️[\w\-:\.\u4e00-\u9fff]+"),
        re.compile(r"#CONFIRM🌌9622-ONLY-ONCE🧬[\w\-]+"),
        re.compile(r"#ZHUGEXIN⚡️[\w\-:\.🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️]+"),
    ]:
        for m in pat.finditer(text):
            add_span(m.start(), m.end(), m.group(0), "dna")

    # 通心译英文术语
    for en, zh, pat in tongxin_patterns:
        for m in pat.finditer(text):
            add_span(m.start(), m.end(), en, "tongxin_en", zh)

    # 种子概念（中文）
    for seed, pat in seed_patterns:
        for m in pat.finditer(text):
            add_span(m.start(), m.end(), seed, "concept")

    # 注：通用中文术语抽取暂关闭，避免结构噪音淹没核心概念。
    # 知识图谱以 CNSH、DNA、通心译、种子概念四类高质量实体为主。
    return sorted(found, key=lambda x: x[3])


def build_relations(
    occurrences: List[Tuple[int, str, str, int]],
    page_id: str,
    window: int = 300,
    max_neighbors: int = 5,
) -> List[Tuple[int, int, str, str]]:
    """
    根据字符窗口内共现建立关系。
    occurrences: [(entity_id, name, type, offset), ...] 已按 offset 排序
    """
    rels: List[Tuple[int, int, str, str]] = []
    n = len(occurrences)
    for i in range(n):
        eid_i, name_i, type_i, off_i = occurrences[i]
        added = 0
        for j in range(i + 1, min(n, i + 20)):
            eid_j, name_j, type_j, off_j = occurrences[j]
            if off_j - off_i > window:
                break
            if eid_i == eid_j:
                continue
            rels.append((eid_i, eid_j, "co_occurs", page_id))
            added += 1
            if added >= max_neighbors:
                break
    return rels


def upsert_entity(conn: sqlite3.Connection, name: str, etype: str, tongxin_zh: Optional[str], page_id: str, seen_at: str) -> int:
    cur = conn.execute("SELECT id, occurrence_count FROM entities WHERE name=?", (name,))
    row = cur.fetchone()
    if row:
        eid, cnt = row
        conn.execute(
            "UPDATE entities SET occurrence_count = ? WHERE id=?",
            (cnt + 1, eid),
        )
        return eid
    conn.execute(
        "INSERT INTO entities(name, type, tongxin_zh, first_seen_page_id, first_seen_at, occurrence_count) VALUES(?,?,?,?,?,?)",
        (name, etype, tongxin_zh, page_id, seen_at, 1),
    )
    return conn.execute("SELECT last_insert_rowid()").fetchone()[0]


def extract_page(
    conn: sqlite3.Connection,
    page: Tuple,
    tongxin_patterns: List[Tuple[str, str, re.Pattern]],
    seed_patterns: List[Tuple[str, re.Pattern]],
) -> Dict[str, int]:
    page_id, title, category, notion_url, created, modified, md_path = page
    if not md_path or not pathlib.Path(md_path).exists():
        return {"entities": 0, "relations": 0}

    text = pathlib.Path(md_path).read_text(encoding="utf-8")
    if title:
        text = title + "\n\n" + text

    extracted_at = now_cst()
    raw = extract_entities(text, tongxin_patterns, seed_patterns)

    # 去重同一页面内同一名称多次出现，保留首次 offset 用于关系
    name_to_eid: Dict[str, int] = {}
    occurrences: List[Tuple[int, str, str, int]] = []
    for name, etype, tzh, offset in raw:
        if name not in name_to_eid:
            eid = upsert_entity(conn, name, etype, tzh, page_id, created or extracted_at)
            name_to_eid[name] = eid
        else:
            eid = name_to_eid[name]
        # 记录每次出现（保留来源链）
        start = max(0, offset - 80)
        end = min(len(text), offset + len(name) + 80)
        snippet = text[start:end].replace("\n", " ")
        conn.execute(
            """INSERT INTO entity_occurrences
               (entity_id, page_id, snippet, char_offset, local_md_path, notion_url, page_created, page_modified, extracted_at)
               VALUES(?,?,?,?,?,?,?,?,?)""",
            (eid, page_id, snippet, offset, md_path, notion_url, created, modified, extracted_at),
        )
        occurrences.append((eid, name, etype, offset))

    # 关系
    rels = build_relations(occurrences, page_id)
    for src, tgt, rtype, pid in rels:
        conn.execute(
            """INSERT INTO relations(source_id, target_id, relation_type, page_id, context, weight, extracted_at)
               VALUES(?,?,?,?,?,?,?)""",
            (src, tgt, rtype, pid, "同页共现", 1.0, extracted_at),
        )

    conn.execute(
        "UPDATE pages SET kg_extracted_at=? WHERE id=?",
        (extracted_at, page_id),
    )
    conn.commit()
    return {"entities": len(name_to_eid), "relations": len(rels)}


def generate_report(conn: sqlite3.Connection) -> None:
    lines = [
        "# 🐉 龍魂知识图谱报告",
        "",
        f"- DNA: {DNA}",
        f"- 生成时间：{now_cst()}",
        "",
    ]

    total_pages = conn.execute("SELECT COUNT(*) FROM pages WHERE status='done'").fetchone()[0]
    extracted = conn.execute("SELECT COUNT(*) FROM pages WHERE kg_extracted_at IS NOT NULL").fetchone()[0]
    entity_count = conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
    rel_count = conn.execute("SELECT COUNT(*) FROM relations").fetchone()[0]

    lines += [
        "## 统计概览",
        "",
        f"| 指标 | 数量 |",
        f"|---|---|",
        f"| 已下载页面 | {total_pages} |",
        f"| 已抽取页面 | {extracted} |",
        f"| 实体总数 | {entity_count} |",
        f"| 关系总数 | {rel_count} |",
        "",
        "## 高频实体（Top 30）",
        "",
        "| 实体 | 类型 | 通心译 | 出现次数 |",
        "|---|---|---|---|",
    ]
    rows = conn.execute(
        "SELECT name, type, tongxin_zh, occurrence_count FROM entities ORDER BY occurrence_count DESC LIMIT 30"
    ).fetchall()
    for name, etype, tzh, cnt in rows:
        tzh = tzh or ""
        lines.append(f"| {name} | {etype} | {tzh} | {cnt} |")

    lines += ["", "## 核心关系对（Top 20）", "", "| 源实体 | 目标实体 | 关系 | 共现次数 |", "|---|---|---|---|"]
    rows = conn.execute("""
        SELECT e1.name, e2.name, r.relation_type, COUNT(*) as c
        FROM relations r
        JOIN entities e1 ON e1.id = r.source_id
        JOIN entities e2 ON e2.id = r.target_id
        GROUP BY r.source_id, r.target_id, r.relation_type
        ORDER BY c DESC
        LIMIT 20
    """).fetchall()
    for s, t, rt, c in rows:
        lines.append(f"| {s} | {t} | {rt} | {c} |")

    lines += ["", "## 按类型实体分布", "", "| 类型 | 数量 |", "|---|---|"]
    rows = conn.execute("SELECT type, COUNT(*) FROM entities GROUP BY type ORDER BY COUNT(*) DESC").fetchall()
    for t, c in rows:
        lines.append(f"| {t} | {c} |")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    print(f"🐉 龍魂知识图谱抽取启动 · {DNA}")
    conn = init_db()
    tongxin_patterns = load_tongxin_patterns()
    seed_patterns = load_seed_patterns()

    pages = conn.execute(
        """SELECT id, title, category, notion_url, created, modified, local_md_path
           FROM pages WHERE status='done'
           ORDER BY phase, modified DESC"""
    ).fetchall()

    total_entities = 0
    total_relations = 0
    for i, page in enumerate(pages, 1):
        stats = extract_page(conn, page, tongxin_patterns, seed_patterns)
        total_entities += stats["entities"]
        total_relations += stats["relations"]
        if i % 20 == 0 or i == len(pages):
            print(f"  [{i}/{len(pages)}] 已抽取 {i} 页 · 实体 {total_entities} · 关系 {total_relations}")

    # 元数据
    conn.execute(
        "INSERT OR REPLACE INTO kg_meta(key, value) VALUES(?,?)",
        ("last_extracted", now_cst()),
    )
    conn.execute(
        "INSERT OR REPLACE INTO kg_meta(key, value) VALUES(?,?)",
        ("stats", f"pages={len(pages)}, entities={total_entities}, relations={total_relations}"),
    )
    conn.commit()

    generate_report(conn)
    print(f"\n✅ 知识图谱抽取完成")
    print(f"   页面：{len(pages)} | 实体：{total_entities} | 关系：{total_relations}")
    print(f"   报告：{REPORT_PATH}")
    conn.close()


if __name__ == "__main__":
    main()

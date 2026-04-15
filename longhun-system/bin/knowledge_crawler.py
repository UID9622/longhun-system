#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂知識庫爬蟲引擎 v1.0
DNA: #龍芯⚡️2026-04-03-KNOWLEDGE-CRAWLER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理論指導：曾仕強老師（永恆顯示）
作者：UID9622 諸葛鑫（龍芯北辰）
獻禮：新中國成立77周年（1949-2026）· 丙午馬年

職責：
  1. 批量抓取 URL 正文
  2. 易經卦象 TextRank 壓縮（保留氣韻/使命/禪意句子）
  3. 三色審計 + DNA 追溯
  4. 寫入 SQLite + JSONL
  5. 自動更新 CS 知識庫緩存（cs_cards_cache.json）
     → app.py 下次啟動直接命中新知識
"""

import json, hashlib, sqlite3, re, time, os, sys
from datetime import datetime
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import trafilatura
except ImportError:
    print("⚠️  請先安裝: pip3 install trafilatura")
    sys.exit(1)

# ── 路徑配置 ─────────────────────────────────────────
BASE          = Path.home() / "longhun-system"
DB_PATH       = BASE / "knowledge.db"
JSONL_PATH    = BASE / "knowledge.jsonl"
CS_CACHE      = BASE / "bin" / "cs_cards_cache.json"
LOG_PATH      = BASE / "logs" / "knowledge_crawler.log"
MAX_WORKERS   = 4
TARGET_LEN    = 480   # 壓縮目標字數

# ── 易經卦象關鍵詞權重表 ────────────────────────────
GUA_KEYWORDS = {
    "乾": (2.6, ["使命", "不屈", "進取", "守護", "龍魂", "主權", "躍進"]),
    "坤": (2.4, ["人民", "為民", "普惠", "厚德", "老百姓", "服務"]),
    "震": (2.2, ["頓悟", "突破", "爆發", "覺醒", "激活"]),
    "離": (2.0, ["光明", "照亮", "升華", "金光", "使命感"]),
    "謙": (1.8, ["留白", "空靈", "內斂", "謙遜", "簡素"]),
    "既濟": (1.6, ["完成", "成功", "圓滿", "落地", "實現"]),
}

MISSION_KW = ["人民", "使命", "主權", "不屈", "為民", "守護", "普惠", "數據", "龍魂"]
ZEN_KW     = ["留白", "氣韻", "頓悟", "空靈", "以少勝多", "天人合一", "活潑潑", "侘寂"]


# ── TextRank 壓縮（易經卦象加權版） ─────────────────
def compress(raw: str, target: int = TARGET_LEN) -> str:
    if not raw or len(raw.strip()) < 80:
        return raw.strip()

    sents = re.split(r'[。！？；\n]', raw)
    sents = [s.strip() for s in sents if 20 < len(s.strip()) < 200]
    if len(sents) <= 6:
        return "。".join(sents)

    all_words = re.findall(r'[\u4e00-\u9fff]+', raw)
    freq = Counter(all_words)
    total = len(sents)

    def score(sent: str, idx: int) -> float:
        words = set(re.findall(r'[\u4e00-\u9fff]+', sent))
        s = 0.0
        # 詞頻
        s += sum(freq.get(w, 0) for w in words) / max(1, len(words)) * 1.0
        # 位置（首尾加權）
        s += (1.9 if idx < total // 4 or idx > total * 3 // 4 else 1.0) * 0.85
        # 使命關鍵詞
        s += sum(3.0 for kw in MISSION_KW if kw in sent) * 2.9
        # 禪宗關鍵詞
        s += sum(2.0 for kw in ZEN_KW if kw in sent) * 2.3
        # 易經卦象
        for w, (wt, kws) in GUA_KEYWORDS.items():
            hits = sum(1 for kw in kws if kw in sent)
            if hits:
                s += min(1.0, hits / 6.0) * wt
        # 連貫性
        if idx > 0:
            prev = set(re.findall(r'[\u4e00-\u9fff]+', sents[idx - 1]))
            s += len(words & prev) * 0.7 * 1.1
        # 長度懲罰
        s -= abs(len(sent) - 60) / 120.0 * 0.55
        return s

    scored = sorted(enumerate(sents), key=lambda x: score(x[1], x[0]), reverse=True)
    selected, cur_len = [], 0
    for idx, sent in scored:
        if cur_len + len(sent) > target * 1.2:
            break
        selected.append((idx, sent))
        cur_len += len(sent)

    # 按原順序排列
    selected.sort(key=lambda x: x[0])
    return "。".join(s for _, s in selected)


# ── DNA 生成 ────────────────────────────────────────
def make_dna(url: str, content: str) -> str:
    h = hashlib.sha256(f"{url}|{content[:300]}".encode()).hexdigest()[:16]
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-KNOW-{h}"


# ── 三色審計 ────────────────────────────────────────
def audit(content: str) -> tuple:
    score = 100
    if len(content) < 50:
        score -= 40
    if not any(kw in content for kw in MISSION_KW + ZEN_KW):
        score -= 20
    color = "🟢" if score >= 80 else ("🟡" if score >= 60 else "🔴")
    return color, score


# ── 關鍵詞提取（給 app.py CS命中用） ────────────────
def extract_keywords(title: str, content: str) -> list:
    kws = re.findall(r'[\u4e00-\u9fff]{2,6}', title)
    # 從內容高頻詞補充
    all_words = re.findall(r'[\u4e00-\u9fff]{2,6}', content)
    freq = Counter(all_words).most_common(8)
    kws += [w for w, _ in freq if w not in kws]
    return list(dict.fromkeys(kws))[:12]


# ── 數據庫初始化 ──────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS knowledge (
        id INTEGER PRIMARY KEY,
        url TEXT UNIQUE,
        title TEXT,
        compressed TEXT,
        dna TEXT UNIQUE,
        tags TEXT,
        audit_color TEXT,
        audit_score INTEGER,
        ts TEXT
    )''')
    conn.commit()
    conn.close()


# ── 單 URL 抓取 + 處理 ───────────────────────────────
def crawl_one(url: str, tags: str = "") -> dict | None:
    try:
        import urllib.request
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/120.0 Safari/537.36"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            html_bytes = resp.read()

        html = html_bytes.decode("utf-8", errors="ignore")

        raw = trafilatura.extract(html, include_comments=False,
                                  include_tables=False)
        if not raw or len(raw.strip()) < 80:
            return None

        meta  = trafilatura.extract_metadata(html)
        title = (meta.title if meta and meta.title else url.split("/")[-1])[:60]

        compressed   = compress(raw)
        dna          = make_dna(url, raw)
        color, score = audit(compressed)
        keywords     = extract_keywords(title, compressed)

        record = {
            "url": url,
            "title": title,
            "content": compressed,
            "keywords": keywords,
            "dna": dna,
            "tags": tags,
            "audit_color": color,
            "audit_score": score,
            "ts": datetime.now().isoformat(),
        }

        # 寫 JSONL
        with open(JSONL_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        # 寫 SQLite
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT OR REPLACE INTO knowledge "
            "(url,title,compressed,dna,tags,audit_color,audit_score,ts) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (url, title, compressed, dna, tags, color, score, record["ts"])
        )
        conn.commit()
        conn.close()

        return record

    except Exception as e:
        return None


# ── 批量抓取 ──────────────────────────────────────────
def batch_crawl(urls: list, tags: str = "") -> list:
    print(f"🚀 開始批量抓取 · {len(urls)} 個URL · 標籤: {tags or '無'}")
    init_db()

    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(crawl_one, url, tags): url for url in urls}
        for future in as_completed(futures):
            url = futures[future]
            rec = future.result()
            if rec:
                results.append(rec)
                print(f"  {rec['audit_color']} {rec['title'][:36]}")
            else:
                print(f"  ⚪ 跳過: {url[:60]}")

    return results


# ── 同步更新 CS 知識庫緩存 ──────────────────────────
def sync_cs_cache(new_records: list):
    """把新抓取的內容合并進 cs_cards_cache.json，app.py 下次直接命中"""
    existing = []
    if CS_CACHE.exists():
        with open(CS_CACHE, encoding="utf-8") as f:
            existing = json.load(f)

    existing_urls = {c.get("url", "") for c in existing}
    added = 0
    for rec in new_records:
        if rec["url"] not in existing_urls and rec.get("content", "").strip():
            existing.append({
                "title":    rec["title"],
                "content":  rec["content"],
                "keywords": rec["keywords"],
                "url":      rec["url"],
                "dna":      rec["dna"],
            })
            added += 1

    with open(CS_CACHE, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"\n📚 CS知識庫緩存已更新 · 新增 {added} 條 · 共 {len(existing)} 條")
    print(f"   → {CS_CACHE}")


# ── 日誌記錄 ──────────────────────────────────────────
def log(msg: str):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


# ── 主入口 ────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂知識庫爬蟲 v1.0")
    parser.add_argument("input", help="URL 或 URL列表文件(.txt)")
    parser.add_argument("--tags", default="", help="標籤（逗號分隔）")
    args = parser.parse_args()

    # 判斷是文件還是單個 URL
    p = Path(args.input)
    if p.exists() and p.suffix == ".txt":
        urls = [line.strip() for line in p.read_text(encoding="utf-8").splitlines()
                if line.strip() and not line.startswith("#")]
    else:
        urls = [args.input]

    results = batch_crawl(urls, args.tags)
    sync_cs_cache(results)

    ok  = len(results)
    log(f"抓取完成 · 成功{ok}條 · 標籤:{args.tags}")

    print(f"\n━━ 完成 ━━")
    print(f"  成功: {ok} 條")
    print(f"  SQLite: {DB_PATH}")
    print(f"  JSONL:  {JSONL_PATH}")
    print(f"  DNA: #龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-CRAWLER-v1.0")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂相似度审计系统 v1.0
DNA: #龍芯⚡️2026-03-20-SIMILARITY-AUDIT-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）

功能：
1. 读取 ~/longhun-system/ 所有文档，提取核心概念
2. 用余弦相似度对比互联网搜索结果
3. 只输出相似度 + 匹配片段，不指名道姓
4. 报告存入 ~/longhun-system/audit/相似度报告.txt
"""

import re
import json
import math
import urllib.request
import urllib.parse
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import Counter
from typing import List, Dict, Tuple

# ========== 配置 ==========
LONGHUN_DIR  = Path.home() / "longhun-system"
AUDIT_DIR    = LONGHUN_DIR / "audit"
REPORT_PATH  = AUDIT_DIR / "相似度报告.txt"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

# 要扫描的文档目录
DOC_DIRS = [
    LONGHUN_DIR / "docs",
    LONGHUN_DIR,
]
DOC_EXTS = {".md", ".txt"}

# 忽略的文件
IGNORE_FILES = {"README.md", "README-整理说明.md", "requirements.txt"}

# 搜索时去掉的高频无意义词
STOPWORDS = set("""
的 了 是 在 有 和 与 或 不 也 都 到 这 那 他 她 它 我 你
对 但 如果 可以 应该 需要 就是 一个 一种 系统 通过 进行 使用
实现 提供 支持 用于 基于 以及 并且 因此 所以 所有 任何 每个
the a an is are was were be been being have has had do does did
will would shall should may might must can could of in on at to
for with by from about as into through during before after
""".split())

UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

def now_bj():
    return datetime.now(timezone(timedelta(hours=8)))


# ============================================================
# 一、文档读取 & 概念提取
# ============================================================

def load_docs() -> List[Dict]:
    """加载所有文档"""
    docs = []
    for base in DOC_DIRS:
        if not base.exists():
            continue
        for ext in DOC_EXTS:
            for fpath in base.glob(f"*{ext}"):
                if fpath.name in IGNORE_FILES:
                    continue
                if fpath.stat().st_size < 100:   # 跳过空文件
                    continue
                try:
                    text = fpath.read_text(encoding="utf-8", errors="ignore")
                    docs.append({"path": fpath, "name": fpath.name, "text": text})
                except:
                    pass
    return docs


def extract_concepts(text: str) -> List[str]:
    """提取核心概念：去除markdown符号、代码块、停用词，保留有意义词组"""
    # 去代码块
    text = re.sub(r'```[\s\S]*?```', '', text)
    # 去HTML
    text = re.sub(r'<[^>]+>', '', text)
    # 去URL
    text = re.sub(r'https?://\S+', '', text)
    # 去markdown符号
    text = re.sub(r'[#*`>|\[\]()_~]', ' ', text)
    # 去DNA码（避免自我命中）
    text = re.sub(r'#[龍鑫龍ZHUGEXIN⚡️A-Z0-9\-]+', '', text)

    # 提取中文词组（2-6字）
    cn_words = re.findall(r'[\u4e00-\u9fff]{2,6}', text)
    # 提取英文词
    en_words = re.findall(r'[A-Za-z]{3,}', text)

    all_words = [w for w in cn_words + [w.lower() for w in en_words]
                 if w not in STOPWORDS and len(w) >= 2]
    return all_words


def build_core_concepts(docs: List[Dict]) -> Dict[str, List[str]]:
    """每个文档提取Top关键概念"""
    result = {}
    for doc in docs:
        words  = extract_concepts(doc["text"])
        freq   = Counter(words)
        # 取频率最高的20个词作为核心概念
        core   = [w for w, _ in freq.most_common(20)]
        if core:
            result[doc["name"]] = core
    return result


def concepts_to_query(concepts: List[str]) -> str:
    """把概念列表转成搜索关键词（取最有代表性的5个）"""
    # 优先选中文词（更独特）
    cn = [w for w in concepts if re.search(r'[\u4e00-\u9fff]', w)]
    en = [w for w in concepts if not re.search(r'[\u4e00-\u9fff]', w)]
    picks = (cn[:3] + en[:2])[:5]
    return " ".join(picks)


# ============================================================
# 二、余弦相似度
# ============================================================

def tokenize(text: str) -> List[str]:
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'[#*`>|\[\]()_~\n]', ' ', text)
    cn   = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
    en   = re.findall(r'[A-Za-z]{3,}', text.lower())
    return [w for w in cn + en if w not in STOPWORDS]


def cosine_similarity(text_a: str, text_b: str) -> float:
    """计算两段文本的余弦相似度"""
    if not text_a.strip() or not text_b.strip():
        return 0.0

    tokens_a = Counter(tokenize(text_a))
    tokens_b = Counter(tokenize(text_b))

    all_keys = set(tokens_a) | set(tokens_b)
    if not all_keys:
        return 0.0

    dot  = sum(tokens_a[k] * tokens_b[k] for k in all_keys)
    norm_a = math.sqrt(sum(v ** 2 for v in tokens_a.values()))
    norm_b = math.sqrt(sum(v ** 2 for v in tokens_b.values()))

    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# ============================================================
# 三、互联网搜索
# ============================================================

def fetch(url: str, timeout: int = 8) -> str:
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except:
        return ""


def search_and_extract(query: str) -> List[Dict]:
    """搜索并提取结果片段"""
    results = []

    # 百度
    html = fetch(f"https://www.baidu.com/s?wd={urllib.parse.quote(query)}&rn=10")
    if html:
        # 提取摘要文本（百度 abstract span）
        snippets = re.findall(r'<span[^>]*class="[^"]*content-right[^"]*"[^>]*>(.*?)</span>', html, re.DOTALL)
        snippets += re.findall(r'<div[^>]*class="[^"]*c-abstract[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
        for s in snippets[:5]:
            clean = re.sub(r'<[^>]+>', '', s).strip()
            clean = re.sub(r'\s+', ' ', clean)
            if len(clean) > 30:
                results.append({"platform": "百度", "snippet": clean[:300]})

    # 必应
    html2 = fetch(f"https://www.bing.com/search?q={urllib.parse.quote(query)}")
    if html2:
        snippets2 = re.findall(r'<p[^>]*>(.*?)</p>', html2, re.DOTALL)
        for s in snippets2[:5]:
            clean = re.sub(r'<[^>]+>', '', s).strip()
            clean = re.sub(r'\s+', ' ', clean)
            if len(clean) > 30:
                results.append({"platform": "必应", "snippet": clean[:300]})

    return results


# ============================================================
# 四、主审计流程
# ============================================================

def run_audit(verbose: bool = True) -> str:
    t_start = now_bj()
    lines   = []

    def log(s: str = ""):
        lines.append(s)
        if verbose:
            print(s)

    log("=" * 62)
    log("🐉 龍魂相似度审计报告")
    log(f"   生成时间: {t_start.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"   DNA: #龍芯⚡️{t_start.strftime('%Y%m%d')}-SIMILARITY-AUDIT")
    log(f"   作者: UID9622 诸葛鑫（龍芯北辰）")
    log(f"   说明: 相似度仅描述文本特征重叠程度，不含价值判断")
    log("=" * 62)
    log()

    # 1. 加载文档
    docs = load_docs()
    log(f"📂 加载文档: {len(docs)} 个")
    log()

    if not docs:
        log("❌ 未找到任何文档，退出")
        return "\n".join(lines)

    # 2. 提取概念
    concept_map = build_core_concepts(docs)

    # 3. 逐文档审计
    audit_records = []

    for doc in docs:
        name     = doc["name"]
        concepts = concept_map.get(name, [])
        if not concepts:
            continue

        query = concepts_to_query(concepts)
        if not query.strip():
            continue

        log(f"🔍 审计: {name}")
        log(f"   核心词: {' · '.join(concepts[:8])}")

        # 搜索
        web_results = search_and_extract(query)

        if not web_results:
            log(f"   ⚪ 未获取到搜索片段")
            log()
            continue

        # 计算相似度
        doc_text = doc["text"][:3000]
        similarities = []

        for r in web_results:
            sim = cosine_similarity(doc_text, r["snippet"])
            similarities.append({
                "platform": r["platform"],
                "similarity": sim,
                "snippet": r["snippet"]
            })

        if not similarities:
            log()
            continue

        # 按相似度排序
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        top = similarities[0]
        avg_sim = sum(s["similarity"] for s in similarities) / len(similarities)

        # 颜色级别
        pct = top["similarity"] * 100
        if pct >= 40:
            level = "🔴 高度相似"
        elif pct >= 20:
            level = "🟡 中度相似"
        elif pct >= 8:
            level = "🟢 低度相似"
        else:
            level = "⚪ 基本无关"

        log(f"   最高相似度: {pct:.1f}%  {level}")
        log(f"   平均相似度: {avg_sim*100:.1f}%  (共{len(similarities)}片段)")
        if pct >= 8:
            log(f"   匹配片段 [{top['platform']}]:")
            log(f"   「{top['snippet'][:120]}...」")
        log()

        audit_records.append({
            "doc": name,
            "concepts": concepts[:8],
            "query": query,
            "max_sim": pct,
            "avg_sim": avg_sim * 100,
            "level": level,
            "top_match": top
        })

        import time; time.sleep(1.5)  # 礼貌延迟

    # 4. 汇总
    log("─" * 62)
    log("📊 汇总")
    log()

    if audit_records:
        audit_records.sort(key=lambda x: x["max_sim"], reverse=True)
        red    = [r for r in audit_records if r["max_sim"] >= 40]
        yellow = [r for r in audit_records if 20 <= r["max_sim"] < 40]
        green  = [r for r in audit_records if 8  <= r["max_sim"] < 20]
        white  = [r for r in audit_records if r["max_sim"] < 8]

        log(f"  🔴 高度相似 (≥40%): {len(red)} 个文档")
        for r in red:
            log(f"     · {r['doc']}  {r['max_sim']:.1f}%")
        log(f"  🟡 中度相似 (20-40%): {len(yellow)} 个文档")
        for r in yellow:
            log(f"     · {r['doc']}  {r['max_sim']:.1f}%")
        log(f"  🟢 低度相似 (8-20%): {len(green)} 个文档")
        log(f"  ⚪ 基本无关 (<8%):  {len(white)} 个文档")
        log()

        all_sims = [r["max_sim"] for r in audit_records]
        log(f"  总体平均相似度: {sum(all_sims)/len(all_sims):.1f}%")
        log(f"  最高相似度文档: {audit_records[0]['doc']}  {audit_records[0]['max_sim']:.1f}%")
    else:
        log("  未获取到有效搜索结果，建议检查网络")

    log()
    log("─" * 62)
    t_end = now_bj()
    elapsed = (t_end - t_start).seconds
    log(f"⏱  耗时: {elapsed} 秒")
    log(f"📁 报告路径: {REPORT_PATH}")
    log(f"DNA: #龍芯⚡️{t_end.strftime('%Y%m%d')}-AUDIT-DONE-UID9622")
    log("=" * 62)

    report = "\n".join(lines)
    REPORT_PATH.write_text(report, encoding="utf-8")
    return report


# ============================================================
# 五、入口
# ============================================================

if __name__ == "__main__":
    import sys
    verbose = "--quiet" not in sys.argv
    run_audit(verbose=verbose)

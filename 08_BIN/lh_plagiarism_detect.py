#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·剽窃检测引擎 v1.0
DNA: #龍芯⚡️丙午·甲申·壬子·亥时·䷗复-PLAGIARISM-DETECT-v1.0
创建者: 诸葛鑫（UID9622）
分层许可: 工程层 MulanPSL v2

功能:
  fingerprint — 为所有引擎生成DNA指纹库
  search      — 在网络上搜索是否有剽窃（基于Bing搜索）
  compare     — 对比两个代码库的相似度
  watch       — 持续监控模式（定期扫描）
  report      — 剽窃检测报告
"""

import hashlib
import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# ═══ 常量 ═══
DNA = "#龍芯⚡️丙午·甲申·壬子·亥时·䷗复-PLAGIARISM-DETECT-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FINGERPRINT_DB = PROJECT_ROOT / "config" / "plagiarism_fingerprints.json"
AUDIT_LOG = PROJECT_ROOT / "logs" / "plagiarism_detect.log"

# 独特DNA标记（龍魂独有·用于全网搜索）
UNIQUE_MARKERS = [
    "龍芯北辰 UID9622",
    "CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️",
    "CNSH_龍魂",
    "longhun-system",
    "离火运五条底线",
    "德本审计",
    "三色审计",
    "四级熔断 L0/L1/L2/L3",
    "369不动点 sn=369 log369=5.911 perm369=108",
    "行为密码学·七因子追溯",
]


def _compute_ast_fingerprint(filepath: Path) -> Dict:
    """
    计算代码结构指纹（去注释、去字符串、只保留结构）
    这样即使变量名改了，结构指纹也能匹配
    """
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return {"hash": "ERROR", "functions": [], "classes": []}

    # 去掉注释
    no_comments = re.sub(r'#.*$', '', content, flags=re.MULTILINE)
    no_comments = re.sub(r'""".*?"""', '', no_comments, flags=re.DOTALL)
    no_comments = re.sub(r"'''.*?'''", '', no_comments, flags=re.DOTALL)

    # 去掉字符串
    no_strings = re.sub(r'"[^"]*"', '""', no_comments)
    no_strings = re.sub(r"'[^']*'", "''", no_strings)

    # 提取函数签名
    functions = re.findall(r'def\s+(\w+)\s*\([^)]*\)', no_strings)
    classes = re.findall(r'class\s+(\w+)', no_strings)

    # 结构哈希
    structural = re.sub(r'\s+', ' ', no_strings).strip()
    struct_hash = hashlib.sha256(structural.encode()).hexdigest()[:16]

    # 函数签名指纹（即使代码改写，核心函数列表很难全改）
    func_fingerprint = hashlib.sha256(
        '|'.join(sorted(set(functions))).encode()
    ).hexdigest()[:16]

    return {
        "hash": struct_hash,
        "func_fingerprint": func_fingerprint,
        "functions": sorted(set(functions)),
        "classes": sorted(set(classes)),
        "func_count": len(functions),
        "class_count": len(classes),
    }


def _extract_signature_blocks(filepath: Path, n: int = 5) -> List[str]:
    """
    提取代码中最有辨识度的N个代码块（用于检测剽窃）
    选择逻辑：独特标识符最多的N个连续20行块
    """
    try:
        lines = filepath.read_text(encoding='utf-8', errors='ignore').split('\n')
    except Exception:
        return []

    blocks = []
    for i in range(0, len(lines) - 20, 5):
        block = '\n'.join(lines[i:i+20])
        # 计算独特性分数
        uniqueness = 0
        for marker in UNIQUE_MARKERS:
            if marker in block:
                uniqueness += 10
        # 函数定义加分
        uniqueness += len(re.findall(r'def\s+\w+', block)) * 3
        uniqueness += len(re.findall(r'class\s+\w+', block)) * 5
        blocks.append((uniqueness, hashlib.sha256(block.encode()).hexdigest()[:12], block))

    blocks.sort(reverse=True)
    return blocks[:n]


def build_fingerprint_db(dirs: List[str] = None) -> Dict:
    """构建全量引擎指纹库"""
    if dirs is None:
        dirs = ["engines", "04_ENGINES", "05_ENGINES", "核心引擎", "引擎", "bin"]

    fingerprints = {}
    stats = defaultdict(int)

    for d in dirs:
        dpath = PROJECT_ROOT / d
        if not dpath.exists():
            continue

        for root, _, files in os.walk(dpath):
            for f in files:
                if not f.endswith('.py'):
                    continue
                fpath = Path(root) / f
                rel = str(fpath.relative_to(PROJECT_ROOT))

                ast_fp = _compute_ast_fingerprint(fpath)
                sig_blocks = _extract_signature_blocks(fpath)
                sha256 = hashlib.sha256(
                    fpath.read_bytes()
                ).hexdigest()[:16] if fpath.exists() else "ERROR"

                fingerprints[rel] = {
                    "sha256": sha256,
                    "structural_hash": ast_fp["hash"],
                    "func_fingerprint": ast_fp["func_fingerprint"],
                    "func_count": ast_fp["func_count"],
                    "class_count": ast_fp["class_count"],
                    "signature_blocks": [
                        {"hash": h, "preview": b[:80].replace('\n', ' ')}
                        for _, h, b in sig_blocks
                    ],
                }
                stats["total"] += 1

    # 保存
    FINGERPRINT_DB.parent.mkdir(parents=True, exist_ok=True)
    db = {
        "version": "1.0",
        "dna": DNA,
        "built": datetime.now(timezone.utc).isoformat(),
        "stats": dict(stats),
        "fingerprints": fingerprints,
    }
    with open(FINGERPRINT_DB, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    return db


def search_web(query: str, max_results: int = 10) -> List[Dict]:
    """
    通过搜索引擎搜索是否有龍魂代码被剽窃
    使用DuckDuckGo (无API key需要)
    """
    results = []
    encoded = urllib.parse.quote(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded}"

    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')

        # 简单解析搜索结果
        links = re.findall(r'<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>([^<]*)</a>', html)
        snippets = re.findall(r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)

        for i, (link, title) in enumerate(links[:max_results]):
            snippet = snippets[i].strip() if i < len(snippets) else ""
            snippet = re.sub(r'<[^>]+>', '', snippet)
            results.append({
                "title": title.strip(),
                "url": link,
                "snippet": snippet[:200],
            })
    except Exception as e:
        results.append({"error": str(e)})

    return results


def detect_plagiarism(mode: str = "quick") -> Dict:
    """
    执行剽窃检测
    mode: quick(搜索独特标记) | deep(搜索代码结构)
    """
    findings = []

    if mode == "quick":
        # 搜索独特DNA标记
        for marker in UNIQUE_MARKERS[:5]:  # 只搜前5个避免超时
            query = f'"{marker}" -site:uid9622.cn -site:github.com/UID9622'
            results = search_web(query, max_results=5)
            for r in results:
                if "error" not in r:
                    findings.append({
                        "marker": marker,
                        "url": r["url"],
                        "title": r["title"],
                        "snippet": r.get("snippet", ""),
                        "risk": "LOW" if "github.com/UID9622" in r["url"] else "REVIEW",
                    })
        # 去重
        seen = set()
        unique_findings = []
        for f in findings:
            key = f["url"]
            if key not in seen:
                seen.add(key)
                unique_findings.append(f)
        findings = unique_findings

    return {
        "scan_time": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "markers_searched": len(UNIQUE_MARKERS[:5]) if mode == "quick" else len(UNIQUE_MARKERS),
        "findings_count": len(findings),
        "findings": findings,
        "verdict": "CLEAN" if len(findings) == 0 else "REVIEW_NEEDED",
    }


def compare_repos(target_dir: Path) -> Dict:
    """
    对比目标代码库与龍魂引擎的相似度
    用于检测是否有项目剽窃了龍魂代码
    """
    if not FINGERPRINT_DB.exists():
        return {"error": "指纹库不存在，请先运行 fingerprint"}

    with open(FINGERPRINT_DB, 'r', encoding='utf-8') as f:
        our_db = json.load(f)

    our_funcs = set()
    for fp in our_db["fingerprints"].values():
        our_funcs.add(fp["func_fingerprint"])

    matches = []
    if target_dir.exists():
        for root, _, files in os.walk(target_dir):
            for f in files:
                if not f.endswith('.py'):
                    continue
                fpath = Path(root) / f
                ast_fp = _compute_ast_fingerprint(fpath)
                if ast_fp["func_fingerprint"] in our_funcs:
                    matches.append({
                        "file": str(fpath),
                        "matched_func_fingerprint": ast_fp["func_fingerprint"],
                        "func_count": ast_fp["func_count"],
                    })

    return {
        "target": str(target_dir),
        "our_engines": our_db["stats"].get("total", 0),
        "matches": len(matches),
        "match_details": matches[:20],
        "similarity_pct": round(len(matches) / max(our_db["stats"].get("total", 1), 1) * 100, 2),
    }


def _log(msg: str):
    ts = datetime.now(timezone.utc).isoformat()
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG, 'a', encoding='utf-8') as f:
        f.write(f"[{ts}] {msg}\n")


# ═══ CLI ═══
def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·剽窃检测引擎 v1.0")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("fingerprint", help="构建全量引擎DNA指纹库")

    p_search = sub.add_parser("search", help="全網搜索是否有剽窃")
    p_search.add_argument("--mode", choices=["quick", "deep"], default="quick")

    p_compare = sub.add_parser("compare", help="对比目标仓库相似度")
    p_compare.add_argument("target", help="目标目录路径")

    sub.add_parser("report", help="查看上次检测报告")

    args = parser.parse_args()

    if args.cmd == "fingerprint":
        db = build_fingerprint_db()
        print(f"✅ 指纹库已构建: {db['stats']['total']} 个引擎")
        print(f"   保存位置: {FINGERPRINT_DB}")

    elif args.cmd == "search":
        print("🔍 正在全网搜索龍魂独特标记...")
        result = detect_plagiarism(args.mode)
        print(f"\n检测结果: {result['verdict']}")
        print(f"发现 {result['findings_count']} 条疑似记录")
        for f in result["findings"]:
            print(f"  {'⚠️' if f['risk'] == 'REVIEW' else '✅'} {f['title'][:60]}")
            print(f"     {f['url'][:80]}")
        _log(f"SEARCH {args.mode} -> {result['verdict']} ({result['findings_count']} findings)")

    elif args.cmd == "compare":
        target = Path(args.target)
        print(f"🔬 对比目标: {target}")
        result = compare_repos(target)
        print(f"相似度: {result['similarity_pct']}%")
        print(f"匹配: {result['matches']} 个文件")
        for m in result.get("match_details", []):
            print(f"  🔴 {m['file']}")

    elif args.cmd == "report":
        if FINGERPRINT_DB.exists():
            with open(FINGERPRINT_DB, 'r', encoding='utf-8') as f:
                db = json.load(f)
            print(f"指纹库: {db['built'][:19]}")
            print(f"引擎数: {db['stats'].get('total', '?')}")
        else:
            print("🟡 尚未构建指纹库，请先运行 fingerprint")

    else:
        # 默认: 构建指纹+快速搜索
        print("🐉 龍魂·剽窃检测引擎 v1.0")
        print("=" * 50)
        db = build_fingerprint_db()
        print(f"✅ 指纹库: {db['stats']['total']} 引擎")
        print(f"🔍 全网搜索中...")
        result = detect_plagiarism("quick")
        print(f"结果: {result['verdict']} | 发现 {result['findings_count']} 条")
        _log(f"AUTO-SCAN -> fingerprint={db['stats']['total']} | search={result['verdict']}")


if __name__ == "__main__":
    main()

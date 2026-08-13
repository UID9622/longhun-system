#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·國際編程語言筆試題庫引擎 v1.0
DNA: #龍芯⚡️丙午·丁酉·丙戌·戊子·䷐隨-EXAM-ENGINE-v1.0-UID9622
確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
License: 思想層 CC BY-NC-SA 4.0 · 工程層 MulanPSL v2
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXAM_DIR = PROJECT_ROOT / "11_DATA" / "learning"

LANGUAGE_MAP = {
    "js": "JavaScript", "javascript": "JavaScript",
    "java": "Java",
    "go": "Go", "golang": "Go",
    "ts": "TypeScript", "typescript": "TypeScript",
    "sql": "SQL",
    "rust": "Rust",
    "csharp": "C#", "c#": "C#", "cs": "C#",
    "shell": "Shell/Bash", "bash": "Shell/Bash", "sh": "Shell/Bash",
    "ruby": "Ruby",
    "php": "PHP",
    "swift": "Swift",
    "kotlin": "Kotlin",
    "python": "Python", "py": "Python",
    "cpp": "C/C++", "c++": "C/C++", "c": "C/C++",
}


def list_banks() -> List[Dict[str, Any]]:
    """列出所有題庫"""
    banks = []
    if not EXAM_DIR.exists():
        return banks
    for f in sorted(EXAM_DIR.glob("*-interview-question-bank-v1.0.md")):
        name = f.name.replace("-interview-question-bank-v1.0.md", "")
        lang = LANGUAGE_MAP.get(name.lower(), name)
        banks.append({
            "file": f.name,
            "language": lang,
            "path": str(f.relative_to(PROJECT_ROOT)),
            "size_kb": round(f.stat().st_size / 1024, 2),
        })
    return banks


def find_bank(lang_or_alias: str) -> Optional[Path]:
    """根據語言或別名查找題庫文件"""
    lang = LANGUAGE_MAP.get(lang_or_alias.lower(), lang_or_alias)
    # 嘗試直接匹配文件名
    candidates = list(EXAM_DIR.glob(f"{lang_or_alias.lower()}-interview-question-bank-v1.0.md"))
    if candidates:
        return candidates[0]
    # 嘗試匹配語言名
    for f in EXAM_DIR.glob("*-interview-question-bank-v1.0.md"):
        if lang.lower() in f.name.lower():
            return f
    return None


def extract_sections(text: str) -> Dict[str, List[Dict[str, Any]]]:
    """簡易題目抽取：按 # 部分拆分，再按 ### 題號拆分"""
    sections: Dict[str, List[Dict[str, Any]]] = {}
    current_section = "未分類"
    current_question = None

    for line in text.splitlines():
        sec_match = re.match(r"^#\s+第[一二三四五六七八九十]+部分[：:]\s*(.+)", line)
        if sec_match:
            current_section = sec_match.group(1).strip()
            if current_section not in sections:
                sections[current_section] = []
            current_question = None
            continue

        q_match = re.match(r"^###\s+(\d+)\.\s*(.+)", line)
        if q_match:
            if current_question:
                sections[current_section].append(current_question)
            current_question = {
                "no": int(q_match.group(1)),
                "title": q_match.group(2).strip(),
                "body": [],
                "section": current_section,
            }
            continue

        if current_question is not None:
            current_question["body"].append(line)

    if current_question:
        sections[current_section].append(current_question)

    # 將 body 轉為文本，並嘗試提取答案
    for sec, qs in sections.items():
        for q in qs:
            body_text = "\n".join(q["body"]).strip()
            q["text"] = body_text
            del q["body"]
            ans_match = re.search(r"\*\*答案[：:]\s*(.+?)\*\*", body_text, re.S)
            q["answer"] = ans_match.group(1).strip() if ans_match else ""
    return sections


def search_questions(lang: str, keyword: str, limit: int = 5) -> List[Dict[str, Any]]:
    """按語言和關鍵詞搜索題目"""
    bank_path = find_bank(lang)
    if not bank_path or not bank_path.exists():
        return []
    text = bank_path.read_text(encoding="utf-8")
    sections = extract_sections(text)
    results = []
    kw = keyword.lower()
    for sec, qs in sections.items():
        for q in qs:
            if kw in q["title"].lower() or kw in q["text"].lower():
                results.append({
                    "section": sec,
                    "no": q["no"],
                    "title": q["title"],
                    "answer": q["answer"],
                })
            if len(results) >= limit:
                return results
    return results


def random_question(lang: str) -> Optional[Dict[str, Any]]:
    """隨機抽取一題"""
    bank_path = find_bank(lang)
    if not bank_path or not bank_path.exists():
        return None
    text = bank_path.read_text(encoding="utf-8")
    sections = extract_sections(text)
    all_qs = []
    for sec, qs in sections.items():
        for q in qs:
            all_qs.append({
                "section": sec,
                "no": q["no"],
                "title": q["title"],
                "answer": q["answer"],
            })
    return random.choice(all_qs) if all_qs else None


def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·國際編程語言筆試題庫引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
用法:
  lh exam list                 列出所有題庫
  lh exam search <語言> <關鍵詞>  搜索題目
  lh exam random <語言>         隨機抽題
  lh exam --json ...           JSON 輸出

示例:
  lh exam search js 閉包
  lh exam random go
  lh exam search python 裝飾器 --json
        """
    )
    parser.add_argument("action", nargs="?", default="list",
                        choices=["list", "search", "random"])
    parser.add_argument("lang", nargs="?", default="", help="語言或別名")
    parser.add_argument("keyword", nargs="?", default="", help="搜索關鍵詞")
    parser.add_argument("--json", action="store_true", help="JSON 輸出")
    parser.add_argument("--limit", type=int, default=5, help="搜索結果數量限制")

    args = parser.parse_args()

    if args.action == "list":
        banks = list_banks()
        if args.json:
            print(json.dumps({"banks": banks, "total": len(banks)}, ensure_ascii=False, indent=2))
        else:
            print("🐉 龍魂·國際編程語言筆試題庫清單")
            print("-" * 50)
            for b in banks:
                print(f"  📚 {b['language']:<14} {b['file']:<45} {b['size_kb']:>6.1f} KB")
            print(f"\n  合計: {len(banks)} 份題庫")

    elif args.action == "search":
        if not args.lang or not args.keyword:
            print("用法: lh exam search <語言> <關鍵詞>")
            sys.exit(1)
        results = search_questions(args.lang, args.keyword, args.limit)
        if args.json:
            print(json.dumps({"language": args.lang, "keyword": args.keyword, "results": results}, ensure_ascii=False, indent=2))
        else:
            print(f"🐉 {LANGUAGE_MAP.get(args.lang.lower(), args.lang)} 題庫搜索: '{args.keyword}'")
            if not results:
                print("  🟡 未找到匹配題目")
            for r in results:
                print(f"\n  [{r['section']}] #{r['no']} {r['title']}")
                if r['answer']:
                    print(f"  答案: {r['answer'][:80]}{'...' if len(r['answer']) > 80 else ''}")

    elif args.action == "random":
        if not args.lang:
            print("用法: lh exam random <語言>")
            sys.exit(1)
        q = random_question(args.lang)
        if args.json:
            print(json.dumps({"language": args.lang, "question": q}, ensure_ascii=False, indent=2))
        else:
            print(f"🐉 {LANGUAGE_MAP.get(args.lang.lower(), args.lang)} 隨機一題")
            if q:
                print(f"\n  [{q['section']}] #{q['no']} {q['title']}")
                if q['answer']:
                    print(f"\n  答案: {q['answer'][:200]}{'...' if len(q['answer']) > 200 else ''}")
            else:
                print("  🟡 未找到該語言題庫")


if __name__ == "__main__":
    main()

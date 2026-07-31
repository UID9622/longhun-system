# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 论文入库与知识图谱搜索验证技能
LongHun KG Paper Index & Search Verification Skill

把本地论文目录一键复制到 longhun-system/papers/<category>/，
索引进全局知识图谱 DB，并调用 kg-api 验证中英文搜索命中。

入口示例：
  python3 ~/longhun-system/skills/longhun-kg-paper-index/scripts/论文入库与搜索验证.py \
          --source-dir /Users/uid9622/Downloads/Kimi_Agent_全球化翻译 \
          --category Kimi_Agent_全球化翻译 \
          --commit

DNA: #龍芯⚡️2026-07-01-KG-PAPER-INDEX-SKILL-v1.0
"""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# 把技能 lib 加入路径
_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT / "lib"))
from kg_indexer import index_files


_HOME = Path.home()
_DEFAULT_TARGET_ROOT = _HOME / "longhun-system" / "papers"
_DEFAULT_DB_PATH = _HOME / ".longhun" / "global_index" / "global_index.db"
_DEFAULT_API_URL = "http://127.0.0.1:8088/api/knowledge/search"


def _dna(theme: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    short = hashlib.sha256(f"{theme}:{ts}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{theme}-v1.0-{short}"


def _copy_papers(source_dir: Path, target_dir: Path) -> List[Path]:
    """复制支持的文档文件到目标目录，返回目标路径列表。"""
    target_dir.mkdir(parents=True, exist_ok=True)
    copied: List[Path] = []
    for src in sorted(source_dir.iterdir()):
        if not src.is_file():
            continue
        if src.suffix.lower() not in (".md", ".txt", ".markdown", ".rst"):
            continue
        dst = target_dir / src.name
        shutil.copy2(src, dst)
        copied.append(dst)
    return copied


def _api_search(url: str, query: str, limit: int = 5) -> Dict[str, Any]:
    encoded = urllib.parse.quote(query)
    full = f"{url}?q={encoded}&limit={limit}"
    try:
        with urllib.request.urlopen(full, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}


def _git_commit_papers(target_dir: Path, category: str) -> Optional[str]:
    """提交论文文件到 longhun-system 仓库，返回 commit hash 或 None。"""
    repo_root = _HOME / "longhun-system"
    rel = target_dir.relative_to(repo_root)
    try:
        subprocess.run(
            ["git", "add", str(rel)],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"🟡 git add 警告: {e.stderr}", file=sys.stderr)
        return None

    # 检查是否有 staged 变更；没有则无需提交
    no_staged = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=repo_root,
        capture_output=True,
    )
    if no_staged.returncode == 0:
        return "no-changes"

    commit_msg = (
        f"docs(papers/{category}): 提交论文并入库知识图谱\n\n"
        f"通过 longhun-kg-paper-index 技能自动入库与验证。\n"
        f"DNA: {_dna('KG-PAPER-COMMIT')}"
    )

    # 优先正常提交；若 GPG pinentry 不可用则回退 --no-gpg-sign
    for extra in ([], ["--no-gpg-sign"]):
        try:
            subprocess.run(
                ["git", "commit", "-m", commit_msg, *extra],
                cwd=repo_root,
                check=True,
                capture_output=True,
                text=True,
            )
            show = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=repo_root,
                check=True,
                capture_output=True,
                text=True,
            )
            return show.stdout.strip()
        except subprocess.CalledProcessError as e:
            err = (e.stderr or "") + (e.stdout or "")
            if "gpg" in err.lower() or "pinentry" in err.lower() or "gpg failed" in err.lower():
                continue
            no_change_hints = [
                "nothing to commit",
                "没有要提交的",
                "没有要commit",
                "no changes added",
                "working tree clean",
                "工作区干净",
            ]
            if any(h in err.lower() for h in no_change_hints):
                return "no-changes"
            print(f"🟡 git commit 警告: {e.stderr}", file=sys.stderr)
            return None
    return None


_EN_STOPWORDS = {"the", "a", "an", "of", "and", "or", "in", "on", "at", "to", "for", "with", "by", "from"}


def _pick_verify_terms(titles: List[str]) -> List[str]:
    """从标题里挑几个验证词：优先中文片段，再英文实词，自动去重。"""
    raw: List[str] = []
    for t in titles:
        # 中文：取标题中第一个连续中文字符串（2~6 字）
        cn = re.findall(r"[\u4e00-\u9fa5]{2,6}", t)
        if cn:
            raw.append(cn[0])
        # 英文：跳过常见停用词，取第一个有意义的英文单词（3~20 字母）
        en = re.findall(r"[A-Za-z]{3,20}", t)
        for w in en:
            if w.lower() not in _EN_STOPWORDS:
                raw.append(w)
                break
    # 去重并保留顺序
    seen = set()
    terms: List[str] = []
    for w in raw:
        key = w.lower()
        if key not in seen:
            seen.add(key)
            terms.append(w)
    # 兜底通用词
    if not terms:
        terms.append("paper")
    return terms[:5]


def main() -> int:
    parser = argparse.ArgumentParser(description="论文入库与知识图谱搜索验证")
    parser.add_argument("--source-dir", required=True, type=Path, help="源论文目录")
    parser.add_argument("--category", type=str, default=None, help="papers 下子目录名，默认取源目录 basename")
    parser.add_argument("--target-root", type=Path, default=_DEFAULT_TARGET_ROOT, help="论文仓库根目录")
    parser.add_argument("--db-path", type=Path, default=_DEFAULT_DB_PATH, help="全局索引数据库路径")
    parser.add_argument("--api-url", type=str, default=_DEFAULT_API_URL, help="kg-api 搜索端点")
    parser.add_argument("--commit", action="store_true", help="是否把论文提交到 git")
    parser.add_argument("--verify-terms", type=str, default=None, help="逗号分隔的自定义验证搜索词")
    args = parser.parse_args()

    source_dir = args.source_dir.resolve()
    if not source_dir.is_dir():
        print(f"🔴 源目录不存在: {source_dir}", file=sys.stderr)
        return 1

    category = args.category or source_dir.name
    target_dir = args.target_root.resolve() / category

    # 1. 复制
    copied = _copy_papers(source_dir, target_dir)
    if not copied:
        print("🟡 未找到可入库的文档（支持 .md/.txt/.markdown/.rst）", file=sys.stderr)
        return 2
    print(f"🐉 已复制 {len(copied)} 篇论文到 {target_dir}")

    # 2. 索引
    indexed = index_files(
        copied,
        root=args.target_root.resolve().parent,  # longhun-system
        db_path=args.db_path.resolve(),
        event_type="paper-index",
    )
    titles = [r["title"] for r in indexed if r.get("ok")]
    print(f"🐉 已索引 {sum(1 for r in indexed if r.get('ok'))} 篇")

    # 3. 搜索验证
    terms: List[str] = []
    if args.verify_terms:
        terms = [t.strip() for t in args.verify_terms.split(",") if t.strip()]
    else:
        terms = _pick_verify_terms(titles)

    verify_results: List[Dict[str, Any]] = []
    for term in terms:
        data = _api_search(args.api_url, term, limit=5)
        total = data.get("total", data.get("error", 0))
        verify_results.append({"term": term, "total": total})
        status = "🟢" if (isinstance(total, int) and total > 0) else "🔴"
        print(f"   {status} 搜索「{term}」命中 {total} 条")
        time.sleep(0.1)

    # 4. Git 提交
    commit_hash: Optional[str] = None
    if args.commit:
        commit_hash = _git_commit_papers(target_dir, category)
        if commit_hash == "no-changes":
            print("🟡 论文无变更，无需提交")
            commit_hash = None
        elif commit_hash:
            print(f"🐉 Git 提交成功: {commit_hash}")
        else:
            print("🔴 Git 提交失败", file=sys.stderr)

    report = {
        "DNA": _dna("KG-PAPER-INDEX-RUN"),
        "category": category,
        "source_dir": str(source_dir),
        "target_dir": str(target_dir),
        "copied": len(copied),
        "indexed": [r for r in indexed],
        "verify": verify_results,
        "git_commit": commit_hash,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

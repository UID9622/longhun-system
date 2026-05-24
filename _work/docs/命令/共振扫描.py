#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA 共振扫描器 · 任务 C · 钓鱼台 v1.0
不剽窃·只感应同根命名/架构 · 命中写 日志/共振命中_YYYYMMDD.jsonl
DNA: #龍芯⚡2026-05-19-RESONANCE-SCANNER-v1.0
"""
from __future__ import annotations

import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, List, Optional, Sequence
from urllib.parse import urlparse

REPO = Path(__file__).resolve().parents[1]
LOG = REPO / "日志" / f"共振命中_{time.strftime('%Y%m%d')}.jsonl"

# 同根共振锚点（不要求字面全同·子串/变体即触发）
RESONANCE_ANCHORS: Sequence[tuple[str, str]] = (
    ("CNSH", "架构/CNSH"),
    ("通心译", "通心译"),
    ("三色审计", "三色审计"),
    ("五色审计", "五色审计"),
    ("DNA追溯", "DNA追溯"),
    ("DNA 追溯", "DNA追溯"),
    ("#龍芯⚡", "DNA签章"),
    ("#龍芯⚡", "DNA错字偷换"),  # 偷换亦记
    ("七因子", "七因子"),
    ("龍魂", "龍魂生态"),
    ("龍魂", "简体偷换"),
    ("UID9622", "主控ID"),
    ("BehavCrypto", "论文域"),
    ("渲染门禁", "渲染门禁"),
    ("解除宣言", "解除宣言"),
    ("IPA-", "IPA路由"),
    ("render_gate", "代码锚点"),
    ("通心译", "通心译"),
    ("audit_v3", "五色审计代码"),
    ("dna_gate", "DNA门禁代码"),
)

SKIP_DIRS = {
    ".git",
    "node_modules",
    "venv",
    "__pycache__",
    ".run",
    "抢救仓",
    "工具",
    "logs",
    "日志",
    "longhun-system",
    "versions",
    "数据/notion_export",
}
FOCUS_DIRS = ("skills", "主控", "命令", "cnsh", "协议库", "协议同步", ".cursor")
SKIP_SUFFIX = {".pyc", ".png", ".jpg", ".gif", ".zip", ".jar", ".woff", ".ico"}
MAX_FILE_BYTES = 512_000
CONTEXT_CHARS = 80


@dataclass
class Hit:
    path: str
    anchor: str
    category: str
    line_no: int
    snippet: str
    source: str


def _normalize_dragon(text: str) -> str:
    return text.replace("\u9fb2", "\u9f8d")  # 龍→龍 偷换标红前统一


def scan_text(
    text: str,
    *,
    path: str = "",
    source: str = "local",
    start_line: int = 1,
) -> List[Hit]:
    hits: List[Hit] = []
    for i, line in enumerate(text.splitlines(), start=start_line):
        raw = line
        norm = _normalize_dragon(line)
        for anchor, cat in RESONANCE_ANCHORS:
            if anchor in raw or anchor in norm:
                pos = norm.find(anchor) if anchor in norm else raw.find(anchor)
                if pos < 0:
                    continue
                snip = norm[max(0, pos - 40) : pos + len(anchor) + 40].strip()
                hits.append(
                    Hit(
                        path=path,
                        anchor=anchor,
                        category=cat,
                        line_no=i,
                        snippet=snip[:CONTEXT_CHARS * 2],
                        source=source,
                    )
                )
    return hits


def _iter_files(root: Path, *, focus: bool = False) -> Iterator[Path]:
    roots: Iterable[Path]
    if focus:
        roots = [root / d for d in FOCUS_DIRS if (root / d).exists()]
        roots = list(roots) + [root / "CLAUDE.md"] if (root / "CLAUDE.md").is_file() else list(roots)
    else:
        roots = [root]

    for base in roots:
        if base.is_file():
            yield base
            continue
        for p in base.rglob("*"):
            if not p.is_file():
                continue
            try:
                rel_parts = p.relative_to(root).parts
            except ValueError:
                rel_parts = p.parts
            if set(rel_parts) & SKIP_DIRS:
                continue
            if any(s in str(p) for s in SKIP_DIRS):
                continue
            if p.suffix.lower() in SKIP_SUFFIX:
                continue
            try:
                if p.stat().st_size > MAX_FILE_BYTES:
                    continue
            except OSError:
                continue
            yield p


def scan_local(root: Path, *, focus: bool = True) -> List[Hit]:
    all_hits: List[Hit] = []
    for fp in _iter_files(root, focus=focus):
        try:
            text = fp.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        try:
            rel = str(fp.relative_to(root))
        except ValueError:
            rel = str(fp)
        all_hits.extend(scan_text(text, path=rel, source="local"))
    return all_hits


def scan_github_raw(owner: str, repo: str, branch: str = "main") -> List[Hit]:
    """轻量：只扫 GitHub API 树 + 若干 md/py 路径（需网络）。"""
    import urllib.request

    hits: List[Hit] = []
    api = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    try:
        req = urllib.request.Request(
            api,
            headers={"Accept": "application/vnd.github+json", "User-Agent": "longhun-resonance"},
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        hits.append(
            Hit(
                path=f"github:{owner}/{repo}",
                anchor="(api)",
                category="网络",
                line_no=0,
                snippet=str(e)[:120],
                source="github",
            )
        )
        return hits

    for item in data.get("tree", []):
        path = item.get("path", "")
        if item.get("type") != "blob":
            continue
        if not any(path.endswith(ext) for ext in (".md", ".py", ".txt", ".yaml", ".yml")):
            continue
        for anchor, cat in RESONANCE_ANCHORS:
            if anchor.lower() in path.lower() or anchor in path:
                hits.append(
                    Hit(
                        path=path,
                        anchor=anchor,
                        category=cat,
                        line_no=0,
                        snippet=f"github tree path match · {branch}",
                        source=f"github:{owner}/{repo}",
                    )
                )
    return hits


def write_log(hits: List[Hit], meta: dict) -> Path:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": time.time(), "event": "scan_start", **meta}, ensure_ascii=False) + "\n")
        for h in hits:
            f.write(
                json.dumps(
                    {
                        "ts": time.time(),
                        "event": "hit",
                        "path": h.path,
                        "anchor": h.anchor,
                        "category": h.category,
                        "line": h.line_no,
                        "snippet": h.snippet,
                        "source": h.source,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
        f.write(
            json.dumps(
                {"ts": time.time(), "event": "scan_end", "hit_count": len(hits), **meta},
                ensure_ascii=False,
            )
            + "\n"
        )
    return LOG


def summarize(hits: List[Hit]) -> str:
    by_cat: dict[str, int] = {}
    for h in hits:
        by_cat[h.category] = by_cat.get(h.category, 0) + 1
    lines = [f"命中 {len(hits)} 条", "分类:"]
    for k, v in sorted(by_cat.items(), key=lambda x: -x[1])[:12]:
        lines.append(f"  · {k}: {v}")
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv = list(argv or sys.argv[1:])
    targets = argv if argv else ["local"]

    all_hits: List[Hit] = []
    for t in targets:
        if t == "local" or t.startswith("/"):
            root = Path(t) if t.startswith("/") else REPO
            all_hits.extend(scan_local(root, focus=True))
        elif t == "local-full":
            all_hits.extend(scan_local(REPO, focus=False))
        elif t.startswith("github:"):
            rest = t.split(":", 1)[1]
            parts = rest.strip("/").split("/")
            if len(parts) >= 2:
                all_hits.extend(scan_github_raw(parts[0], parts[1]))
        elif urlparse(t).scheme in ("http", "https"):
            all_hits.append(
                Hit(
                    path=t,
                    anchor="url",
                    category="待扩展",
                    line_no=0,
                    snippet="URL 扫描请用 local 或 github:owner/repo",
                    source="cli",
                )
            )

    # 去重：同文件同行同锚点
    seen = set()
    uniq: List[Hit] = []
    for h in all_hits:
        key = (h.source, h.path, h.line_no, h.anchor)
        if key in seen:
            continue
        seen.add(key)
        uniq.append(h)

    meta = {"targets": targets, "seal": "#龍芯⚡2026-05-19-RESONANCE-SCAN-v1.0"}
    log_path = write_log(uniq, meta)
    print(summarize(uniq))
    print(f"留痕: {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

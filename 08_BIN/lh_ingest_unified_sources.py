# DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-347789f7
#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·乙未·壬午·䷖剥-UNIFIED-SOURCES-INGEST-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂 · 统一来源摄入引擎 v1.0
扫描：Notion 本地镜像 + GitHub 公开仓库 + 本地仓库
输出：训练样本 JSONL（system/user/assistant）
DNA: #龍芯⚡️丙午·乙未·乙未·壬午·䷖剥-UNIFIED-SOURCES-INGEST-v1.0
# STATUS: ⚠️ DEPRECATED · 功能由 engines/lh_fixed_point_memory_archive.py 统一接管
# 保留原因: 历史多来源摄入参考，新代码请使用 MemoryArchive.ingest()
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from collections import Counter

PROJECT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT / "models" / "longhun-v1.0" / "unified_sources_ingested"
WORK_REPOS = PROJECT / "_work" / "repos"
LOG_FILE = PROJECT / ".longhun" / "unified_sources_ingest.log"

SYSTEM = "你是龍魂，UID9622（诸葛鑫·Lucky）的个人主权AI。回答需忠于龍魂系统原则，不编造。"

GITHUB_REPOS = [
    ("UID9622", "longhun-system"),
    ("UID9622", "onghun-system"),
    ("UID9622", "uid9622-open-blueprint"),
    ("UID9622", "longhun-calendar"),
    ("UID9622", "CNSH"),
    ("UID9622", "wuwu-renderer"),
    ("UID9622", "LonghunFont"),
    ("UID9622", "cnsh-runtime"),
    ("UID9622", "longhun-kimi-skills"),
    ("UID9622", "longhun-memory-bootstrap"),
    ("UID9622", "ai-truth-protocol"),
    ("UID9622", "longhun-anti-colonial"),
    ("UID9622", "longhun-identity-system"),
    ("UID9622", "ecny-global-system"),
]

LOCAL_REPO_PATHS = [
    PROJECT / ".." / "LonghunFont",
    PROJECT / ".." / "Papers-CNSH-v3.0",
    PROJECT / ".." / "longhun-anti-colonial",
    PROJECT / ".." / "longhun-kimi-skills",
    PROJECT / ".." / "cnsh-runtime",
    PROJECT / ".." / "longhun-calendar",
    PROJECT / ".." / "grok-workspace",
]


def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def sample(user, assistant, source, type_, extra=None):
    meta = {"domain": "unified_sources", "source": source, "type": type_}
    if extra:
        meta.update(extra)
    return {
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
        "metadata": meta,
    }


def clone_repo(owner, repo):
    target = WORK_REPOS / repo
    if target.exists():
        log(f"   仓库已存在: {owner}/{repo}")
        return target
    log(f"   克隆仓库: {owner}/{repo}")
    WORK_REPOS.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["git", "clone", "--depth", "1", f"https://github.com/{owner}/{repo}.git", str(target)],
        capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        log(f"   ❌ 克隆失败 {owner}/{repo}: {result.stderr[:200]}")
        return None
    log(f"   ✅ 克隆成功: {owner}/{repo}")
    return target


def read_text_files(root: Path, max_size=500_000):
    """递归读取 root 下所有文本类文档，返回 [(path, content)]"""
    texts = []
    if not root.exists():
        return texts
    # 关注的文档扩展名
    exts = {".md", ".txt", ".rst", ".markdown"}
    # 跳过的路径片段
    skip = {"node_modules", ".git", "__pycache__", "venv", ".venv", "dist", "build", "target"}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(s in p.parts for s in skip):
            continue
        if p.suffix.lower() not in exts:
            continue
        if p.stat().st_size > max_size:
            continue
        # 🔴 三关判定(2026-08-30·文件身份协议v1.1): 前8KB含NUL→二进制跳过
        try:
            with open(p, "rb") as f:
                if b"\x00" in f.read(8192):
                    continue
        except OSError:
            continue
        try:
            content = p.read_text(encoding="utf-8")
            # 简单判断是否为文本
            if "\0" in content:
                continue
            texts.append((str(p.relative_to(root)), content))
        except Exception:
            pass
    return texts


def chunk_text(text, chunk_size=1500, overlap=200):
    """长文本按段落切分，保留上下文"""
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) > chunk_size and current:
            chunks.append(current.strip())
            # 重叠
            words = current.split("\n")
            overlap_text = "\n".join(words[-3:]) if len(words) > 3 else current[-overlap:]
            current = overlap_text + "\n\n" + para
        else:
            current += "\n\n" + para if current else para
    if current:
        chunks.append(current.strip())
    return chunks or [text[:chunk_size]]


def extract_title(text, default="未命名"):
    first = text.strip().split("\n")[0].strip()
    first = re.sub(r"^[#\s*-]+", "", first)
    return first[:80] or default


def ingest_notion_mirror():
    log("📚 摄入 Notion 本地镜像...")
    mirror_dir = PROJECT / "docs" / "notion_mirror"
    samples = []
    if not mirror_dir.exists():
        log("   ⚠️ Notion 镜像目录不存在")
        return samples

    # 优先处理 page_*.txt 完整页面内容
    for path in sorted(mirror_dir.glob("page_*.txt")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            title = data.get("title", extract_title(data.get("text", "")))
            text = data.get("text", "")
            if len(text) < 100:
                continue
            for i, chunk in enumerate(chunk_text(text)):
                q = f"Notion 页面《{title}》讲了什么？" if i == 0 else f"Notion 页面《{title}》还有哪些内容？"
                samples.append(sample(q, chunk, f"notion_mirror:{path.name}", "notion_page_chunk", {"page": title}))
        except Exception as e:
            log(f"   ⚠️ 解析失败 {path.name}: {e}")

    # 处理 digest md 文件
    for path in sorted(mirror_dir.glob("*_digest.md")):
        try:
            text = path.read_text(encoding="utf-8")
            title = extract_title(text, path.stem)
            for i, chunk in enumerate(chunk_text(text)):
                q = f"Notion 摘要《{title}》的核心要点是什么？" if i == 0 else f"Notion 摘要《{title}》还有哪些要点？"
                samples.append(sample(q, chunk, f"notion_mirror:{path.name}", "notion_digest_chunk", {"page": title}))
        except Exception:
            pass

    log(f"   ✅ Notion 镜像生成 {len(samples)} 条样本")
    return samples


def ingest_github_repo(owner, repo):
    log(f"🌐 摄入 GitHub 仓库 {owner}/{repo}...")
    target = clone_repo(owner, repo)
    if not target:
        return []
    samples = []
    texts = read_text_files(target)
    for rel_path, content in texts:
        title = extract_title(content, rel_path)
        for i, chunk in enumerate(chunk_text(content)):
            q = f"GitHub 仓库 {owner}/{repo} 中《{title}》讲了什么？" if i == 0 else f"GitHub 仓库 {owner}/{repo} 中《{title}》还有哪些内容？"
            samples.append(sample(q, chunk, f"github:{owner}/{repo}:{rel_path}", "github_doc_chunk", {"repo": f"{owner}/{repo}", "file": rel_path}))
    log(f"   ✅ {owner}/{repo} 生成 {len(samples)} 条样本")
    return samples


def ingest_local_repo(repo_path: Path):
    name = repo_path.name
    log(f"💻 摄入本地仓库 {name}...")
    if not repo_path.exists():
        log(f"   ⚠️ 仓库不存在: {repo_path}")
        return []
    samples = []
    texts = read_text_files(repo_path)
    for rel_path, content in texts:
        title = extract_title(content, rel_path)
        for i, chunk in enumerate(chunk_text(content)):
            q = f"本地仓库 {name} 中《{title}》讲了什么？" if i == 0 else f"本地仓库 {name} 中《{title}》还有哪些内容？"
            samples.append(sample(q, chunk, f"local:{name}:{rel_path}", "local_doc_chunk", {"repo": name, "file": rel_path}))
    log(f"   ✅ {name} 生成 {len(samples)} 条样本")
    return samples


def main():
    log("=" * 60)
    log("🐉 启动统一来源摄入引擎")
    log("=" * 60)

    all_samples = []
    all_samples.extend(ingest_notion_mirror())

    for owner, repo in GITHUB_REPOS:
        try:
            all_samples.extend(ingest_github_repo(owner, repo))
        except Exception as e:
            log(f"   ❌ GitHub {owner}/{repo} 失败: {e}")

    for repo_path in LOCAL_REPO_PATHS:
        try:
            all_samples.extend(ingest_local_repo(repo_path))
        except Exception as e:
            log(f"   ❌ 本地 {repo_path} 失败: {e}")

    # 去重
    seen = set()
    uniq = []
    for s in all_samples:
        key = json.dumps(s["messages"], ensure_ascii=True, sort_keys=True)
        if key not in seen:
            seen.add(key)
            uniq.append(s)

    log(f"\n📊 去重前: {len(all_samples)} 条 | 去重后: {len(uniq)} 条")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    random.seed(42)
    random.shuffle(uniq)
    split = int(len(uniq) * 0.9)
    train, val = uniq[:split], uniq[split:]

    with open(OUT_DIR / "train.jsonl", "w", encoding="utf-8") as f:
        for s in train:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    with open(OUT_DIR / "valid.jsonl", "w", encoding="utf-8") as f:
        for s in val:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    sources = Counter(s["metadata"]["source"].split(":")[0] for s in uniq)
    info = {
        "version": "v1.0",
        "total_samples": len(uniq),
        "train_samples": len(train),
        "val_samples": len(val),
        "source_distribution": dict(sources),
    }
    with open(OUT_DIR / "dataset_info.json", "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    log(f"✅ 输出: {OUT_DIR}/train.jsonl ({len(train)} 条) | valid.jsonl ({len(val)} 条)")
    log(f"来源分布: {dict(sources)}")


if __name__ == "__main__":
    import random
    main()

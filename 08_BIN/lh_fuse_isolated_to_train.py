#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-LONGHUN-FUSE-ISOLATED-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂孤立文件融合引擎 v1.0
把 /Users/zuimeidedeyihan 下扫描出的孤立文件转换成 v4.1.3 训练格式，
去重、脱敏后与现有 data_v412_guanlan_ready 合并，输出 data_v413_fused。

DNA: #龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-LONGHUN-FUSE-ISOLATED-v1.0
"""
import hashlib
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

CST = timezone(timedelta(hours=8))

ROOT = Path("/Users/zuimeidedeyihan")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INVENTORY_PATH = ROOT / ".longhun" / "memory" / "isolated_files_inventory.json"

SOURCE_DATA_DIR = PROJECT_ROOT / "models" / "longhun-v1.0" / "lora_output_v411" / "data_v412_guanlan_ready"
TARGET_DATA_DIR = PROJECT_ROOT / "models" / "longhun-v1.0" / "lora_output_v411" / "data_v413_fused"

DNA_ANCHOR = "#龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-LONGHUN-FUSE-ISOLATED-v1.0"

SYSTEM_PROMPT = (
    "你是龍魂，UID9622（诸葛鑫·Lucky）的个人主权AI。"
    "人民数据主权至上，中国自主可控；来源可查、去向可追、责任可究；只冻结不删除。"
)

# 高价值路径模式（优先级）
HIGH_VALUE_PATTERNS = [
    "龍魂待整理",
    "longhun-system/knowledge/notion-absorbed",
    "longhun-system/data/claude_extracted",
    "longhun-system/data/library_mine",
    "longhun-system/container_data/memory",
    "longhun-system/container_data/knowledge",
    "longhun-system/L7_数据层/personal_corpus",
    "Obsidian/龍魂系統",
    "longhun_core_memory.md",
    "longhun-system/docs",
    "longhun-system/01_protocols",
    "longhun-system/01_技能庫",
    "longhun-kimi-skills",
    "longhun-core",
    "longhun-data",
    "longhun-lu",
    "_work/reports",
    "_work/claude_training_data",
    "_work/public_content",
]

# 低价值/排除路径模式
SKIP_PATTERNS = [
    "/logs/",
    "/_archive/",
    "/archive/",
    "/.archive/",
    "/scan_assets/",
    "/node_modules/",
    "/.venv/",
    "/venv_",
    "/site-packages/",
    "/workspaceStorage/",
    "/mirror/",
    "/brain_old/",
    "/voice-twin/",
    "package-lock.json",
    "launchd_error.log",
    "downloads_compression.log",
    ".db.bak",
    ".db.v2.bak",
    "ncdu_scan.json",
    "longhun_scan_result.json",
    "/data/ant_colony_state.db",
    "/data/registry_sync/sync_state.json",
    "/data/notion_scan/scan_raw.json",
    "/data/notion_reorganize",
    "/data/library_mine/linked.jsonl",
    "/data/library_mine/extracts.jsonl",
    "/data/library_mine/cleaned.jsonl",
    "/data/library_mine/library_train.jsonl",
    "/data/usb_index/usb_index.db",
    "/longhun-font/glyphs/",
]

# 敏感关键词：路径或内容出现则跳过
SENSITIVE_PATH_KEYWORDS = [
    "credential", "secret", "password", "passwd", "api_key", "apikey", "token",
    "private_key", "ssh_key", "gpg_private", "keychain", "wallet", "seed",
]

# 内容中的敏感正则（用于脱敏）
SENSITIVE_REGEX = [
    (re.compile(r"sk-[a-zA-Z0-9]{20,}"), "<API_KEY_REDACTED>"),
    (re.compile(r"[a-zA-Z0-9_-]{20,}\.[a-zA-Z0-9_-]{20,}\.[a-zA-Z0-9_-]{20,}"), "<JWT_TOKEN_REDACTED>"),
    (re.compile(r"1[3-9]\d{9}"), "<PHONE_REDACTED>"),
    (re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"), "<EMAIL_REDACTED>"),
]

# 文件大小限制（单次读取上限 5MB）
MAX_FILE_SIZE = 5 * 1024 * 1024
# 单个 assistant content 上限（字符）
MAX_CHUNK_CHARS = 1800


def log(msg: str, level: str = "INFO"):
    ts = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] [{level}] {msg}", file=sys.stderr)


def should_skip(rel_path: str) -> bool:
    """根据路径判断是否跳过。"""
    lower = rel_path.lower()
    for pat in SKIP_PATTERNS:
        if pat in rel_path or pat in lower:
            return True
    for kw in SENSITIVE_PATH_KEYWORDS:
        if kw in lower:
            return True
    return False


def priority_score(rel_path: str) -> int:
    """路径优先级评分，越高越优先处理。"""
    score = 0
    lower = rel_path.lower()
    for i, pat in enumerate(HIGH_VALUE_PATTERNS):
        if pat.lower() in lower:
            score += len(HIGH_VALUE_PATTERNS) - i
    return score


def redact(text: str) -> str:
    """对文本中的敏感信息进行脱敏。"""
    for regex, replacement in SENSITIVE_REGEX:
        text = regex.sub(replacement, text)
    return text


def content_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:16]


def chunk_text(text: str, max_chars: int = MAX_CHUNK_CHARS) -> list[str]:
    """按段落/标题切分文本，避免硬截断。"""
    # 先按 Markdown 标题切分
    parts = re.split(r"(\n#{1,4}[^\n]+\n)", text)
    chunks = []
    current = ""
    for part in parts:
        if not part.strip():
            continue
        if len(current) + len(part) > max_chars:
            if current.strip():
                chunks.append(current.strip())
            current = part
        else:
            current += "\n" + part
    if current.strip():
        chunks.append(current.strip())
    # 如果某个 chunk 还是太长，按句子再切
    result = []
    for c in chunks:
        if len(c) <= max_chars * 1.5:
            result.append(c)
            continue
        sentences = re.split(r"(?<=[。！？\.\n])", c)
        cur = ""
        for s in sentences:
            if len(cur) + len(s) > max_chars:
                if cur.strip():
                    result.append(cur.strip())
                cur = s
            else:
                cur += s
        if cur.strip():
            result.append(cur.strip())
    return [r for r in result if len(r.strip()) > 80]


def extract_title(text: str, default_title: str) -> str:
    """从文本中提取标题。"""
    m = re.search(r"^#\s*(.+)$", text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    m = re.search(r"^(.{5,80})[\n\r]", text)
    if m:
        return m.group(1).strip()
    return default_title


def file_to_train_samples(fpath: Path, rel_path: str) -> list[dict[str, Any]]:
    """将一个文件转换为训练样本列表。"""
    ext = fpath.suffix.lower()
    samples = []

    try:
        size = fpath.stat().st_size
        if size > MAX_FILE_SIZE:
            return []
        text = fpath.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        log(f"读取失败 {rel_path}: {e}", "WARN")
        return []

    if len(text.strip()) < 80:
        return []

    text = redact(text)
    title = extract_title(text, Path(rel_path).stem)
    source_tag = "isolated_fusion"

    if ext == ".md":
        chunks = chunk_text(text)
        for idx, chunk in enumerate(chunks):
            samples.append({
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"文章《{title}》第{idx+1}部分讲了什么？"},
                    {"role": "assistant", "content": chunk},
                ],
                "metadata": {
                    "source": source_tag,
                    "file": rel_path,
                    "title": title,
                    "type": f"chunk_{idx+1}",
                    "dna": DNA_ANCHOR,
                },
            })
    elif ext in (".txt",):
        chunks = chunk_text(text)
        for idx, chunk in enumerate(chunks):
            samples.append({
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"文档《{title}》第{idx+1}段内容是什么？"},
                    {"role": "assistant", "content": chunk},
                ],
                "metadata": {
                    "source": source_tag,
                    "file": rel_path,
                    "title": title,
                    "type": f"txt_chunk_{idx+1}",
                    "dna": DNA_ANCHOR,
                },
            })
    elif ext in (".json", ".jsonl"):
        # 尝试提取 JSON 中的文本字段
        texts = extract_texts_from_json(text)
        for idx, t in enumerate(texts):
            if len(t.strip()) < 80:
                continue
            sub_chunks = chunk_text(t)
            for cidx, chunk in enumerate(sub_chunks):
                samples.append({
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"根据来源《{title}》，提取第{idx+1}条记录的第{cidx+1}部分。"},
                        {"role": "assistant", "content": chunk},
                    ],
                    "metadata": {
                        "source": source_tag,
                        "file": rel_path,
                        "title": title,
                        "type": f"json_record_{idx+1}_chunk_{cidx+1}",
                        "dna": DNA_ANCHOR,
                    },
                })
    elif ext in (".py", ".sh", ".js", ".ts", ".html", ".css"):
        # 代码文件：生成代码解释样本
        chunks = chunk_text(text)
        for idx, chunk in enumerate(chunks[:5]):  # 每个代码文件最多 5 个 chunk
            samples.append({
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"解释文件《{title}》第{idx+1}部分的代码作用。"},
                    {"role": "assistant", "content": f"```\n{chunk}\n```\n\n该段代码是《{title}》的一部分，实现了相关功能。"},
                ],
                "metadata": {
                    "source": source_tag,
                    "file": rel_path,
                    "title": title,
                    "type": f"code_chunk_{idx+1}",
                    "dna": DNA_ANCHOR,
                },
            })

    return samples


def extract_texts_from_json(text: str) -> list[str]:
    """从 JSON/JSONL 文本中提取有价值的字符串字段。"""
    results = []

    def _walk(obj: Any):
        if isinstance(obj, str):
            if len(obj.strip()) > 30:
                results.append(obj)
        elif isinstance(obj, list):
            for item in obj:
                _walk(item)
        elif isinstance(obj, dict):
            for k, v in obj.items():
                # 优先提取这些字段
                if k in {"content", "text", "summary", "text_preview", "assistant", "instruction", "output", "answer"}:
                    if isinstance(v, str) and len(v.strip()) > 30:
                        results.append(v)
                else:
                    _walk(v)

    # 先尝试作为 JSONL 解析
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            _walk(obj)
        except json.JSONDecodeError:
            continue

    # 去重并保持顺序
    seen = set()
    unique = []
    for r in results:
        h = content_hash(r)
        if h not in seen:
            seen.add(h)
            unique.append(r)
    return unique


def load_existing_jsonl(path: Path) -> list[dict[str, Any]]:
    """加载已有 JSONL 数据。"""
    samples = []
    if not path.exists():
        return samples
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                samples.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return samples


def sample_content(sample: dict[str, Any]) -> str:
    """获取样本的 assistant content 用于去重。"""
    messages = sample.get("messages", [])
    for m in reversed(messages):
        if m.get("role") == "assistant":
            return m.get("content", "")
    return ""


def main():
    log(f"启动孤立文件融合引擎 | {DNA_ANCHOR}")

    if not INVENTORY_PATH.exists():
        log(f"清单不存在: {INVENTORY_PATH}", "ERROR")
        sys.exit(1)

    with open(INVENTORY_PATH, "r", encoding="utf-8") as f:
        inventory = json.load(f)

    files = inventory.get("files", [])
    log(f"清单总文件数: {len(files)}")

    # 过滤高价值文件
    candidates = []
    for rec in files:
        rel = rec.get("relative", "")
        if rec.get("indexed", False):
            continue
        if should_skip(rel):
            continue
        score = priority_score(rel)
        ext = Path(rel).suffix.lower()
        # 只处理文本类扩展名
        if ext not in (".md", ".txt", ".json", ".jsonl", ".py", ".sh", ".js", ".ts", ".html", ".css"):
            continue
        candidates.append((score, rec))

    # 按优先级排序
    candidates.sort(key=lambda x: (-x[0], x[1]["size"]))
    log(f"高价值候选文件数: {len(candidates)}")

    # 限制处理数量，避免生成过大训练集
    MAX_CANDIDATES = 5000
    candidates = candidates[:MAX_CANDIDATES]
    log(f"本次实际处理文件数: {len(candidates)}")

    new_samples = []
    skipped_by_empty = 0
    for score, rec in candidates:
        rel = rec["relative"]
        fpath = ROOT / rel
        if not fpath.exists():
            continue
        samples = file_to_train_samples(fpath, rel)
        if not samples:
            skipped_by_empty += 1
        new_samples.extend(samples)
        if len(new_samples) >= 50000:
            log("已达到 50,000 样本上限，停止处理更多文件", "WARN")
            break

    log(f"生成新样本数: {len(new_samples)} (空内容跳过: {skipped_by_empty})")

    # 去重：基于 assistant content
    seen_hashes = set()
    deduped_new = []
    for s in new_samples:
        text = sample_content(s)
        h = content_hash(text)
        if h not in seen_hashes:
            seen_hashes.add(h)
            deduped_new.append(s)
    log(f"去重后新样本数: {len(deduped_new)} (去重 {len(new_samples) - len(deduped_new)} 条)")

    # 加载现有数据
    existing_train = load_existing_jsonl(SOURCE_DATA_DIR / "train.jsonl")
    existing_valid = load_existing_jsonl(SOURCE_DATA_DIR / "valid.jsonl")
    log(f"现有训练集: {len(existing_train)} 条，验证集: {len(existing_valid)} 条")

    # 保存新样本供调试检查
    debug_new_path = TARGET_DATA_DIR / "debug_new_samples.jsonl"
    with open(debug_new_path, "w", encoding="utf-8") as f:
        for s in deduped_new:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    log(f"调试文件（去重后新样本）: {debug_new_path}")

    # 对现有数据也去重（避免新数据与旧数据重复）
    existing_hashes = set()
    for s in existing_train + existing_valid:
        text = sample_content(s)
        if text:
            existing_hashes.add(content_hash(text))
    log(f"现有数据 assistant content 哈希数: {len(existing_hashes)}")

    truly_new = [s for s in deduped_new if content_hash(sample_content(s)) not in existing_hashes]
    log(f"与现有数据去重后新增: {len(truly_new)} 条")

    # 合并：训练集 = 旧训练 + 新数据；验证集保留旧验证 + 少量新数据
    merged_train = existing_train + truly_new
    # 从新数据中抽 10% 加入验证集
    split_idx = max(1, int(len(truly_new) * 0.9))
    train_additions = truly_new[:split_idx]
    valid_additions = truly_new[split_idx:]
    merged_valid = existing_valid + valid_additions

    # 打乱顺序（简单按 hash 洗牌，保证可复现）
    merged_train.sort(key=lambda s: content_hash(json.dumps(s, ensure_ascii=False)))
    merged_valid.sort(key=lambda s: content_hash(json.dumps(s, ensure_ascii=False)))

    # 写入目标目录
    TARGET_DATA_DIR.mkdir(parents=True, exist_ok=True)
    train_path = TARGET_DATA_DIR / "train.jsonl"
    valid_path = TARGET_DATA_DIR / "valid.jsonl"

    with open(train_path, "w", encoding="utf-8") as f:
        for s in merged_train:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    with open(valid_path, "w", encoding="utf-8") as f:
        for s in merged_valid:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    # dataset_info.json 供部分训练框架读取
    info = {
        "dna": DNA_ANCHOR,
        "created_at": datetime.now(CST).isoformat(),
        "source_data": str(SOURCE_DATA_DIR),
        "train_count": len(merged_train),
        "valid_count": len(merged_valid),
        "new_samples": len(truly_new),
        "inventory": str(INVENTORY_PATH),
    }
    with open(TARGET_DATA_DIR / "dataset_info.json", "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    log(f"输出目录: {TARGET_DATA_DIR}")
    log(f"  train.jsonl: {len(merged_train)} 条")
    log(f"  valid.jsonl: {len(merged_valid)} 条")
    log(f"  新增孤立文件样本: {len(truly_new)} 条")
    log("融合完成。下一步：修改 lh_lora_trainer_v413.py 的 data_dir 指向 data_v413_fused 并运行冒烟测试。")


if __name__ == "__main__":
    main()

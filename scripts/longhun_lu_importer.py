#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · LU 记忆批量导入器

把历史聊天记录 / 日志 / 文本批量压成 LU 记忆，统一进入本地知识库。

支持来源：
  - kimi:     ~/.kimi-code/sessions/*/agents/main/wire.jsonl
  - claude:   ~/.claude/history.jsonl
  - cnsh:     ~/.cnsh/logs/audit.log
  - generic:  任意 .txt / .jsonl / .md 文件

DNA:#龍芯⚡️2026-06-30-LONGHUN-LU-IMPORTER-FILE1-v1.0
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import sys

HOME = Path.home()


def _extract_text_from_log(obj: Any) -> Optional[str]:
    """从日志对象里尽量抽出可压缩文本。"""
    if isinstance(obj, str):
        return obj.strip() or None
    if not isinstance(obj, dict):
        return None

    for key in ("text", "content", "message", "prompt", "response", "input", "output", "summary"):
        val = obj.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
        if isinstance(val, dict):
            nested = _extract_text_from_log(val)
            if nested:
                return nested

    # 兜底：把对象序列化成可读 JSON（截断）
    s = json.dumps(obj, ensure_ascii=False)
    if len(s) > 50:
        return s
    return None


def _chunks_from_text(text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
    """按大小切分长文本，带重叠保持语义连贯。"""
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
        if start >= len(text):
            break
    return chunks


def _iter_log_lines(path: Path) -> Iterable[str]:
    if not path.exists():
        return
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # 尝试解析 JSONL
            try:
                obj = json.loads(line)
                text = _extract_text_from_log(obj)
                if text:
                    yield text
                continue
            except Exception:
                pass
            # 普通文本行
            yield line


def import_file(path: Path, source: str, engine: Any, chunk_size: int = 800, dry_run: bool = False) -> Dict[str, Any]:
    """导入单个文件到 LU 记忆。"""
    total_lines = 0
    compressed = 0
    failed = 0
    lu_codes: List[str] = []

    buffer: List[str] = []
    buffer_chars = 0

    def _flush_buffer() -> None:
        nonlocal buffer, buffer_chars, compressed, failed
        if not buffer:
            return
        text = "\n".join(buffer)
        title = f"{source}导入·{path.name}·块{compressed+failed+1}"
        try:
            if dry_run:
                print(f"[dry-run] 将压缩 {len(text)} 字符：{text[:80]}...")
                return
            result = engine.compress(text, title=title, source=source, operator="UID9622")
            if result.get("ok"):
                compressed += 1
                lu_codes.append(result["record"]["lu_code"])
            else:
                failed += 1
        except Exception as e:
            print(f"[error] 压缩失败：{e}")
            failed += 1
        finally:
            buffer.clear()
            buffer_chars = 0

    for text in _iter_log_lines(path):
        total_lines += 1
        # 单条超过 chunk_size 直接切分
        if len(text) > chunk_size:
            if buffer:
                _flush_buffer()
            for chunk in _chunks_from_text(text, chunk_size):
                buffer.append(chunk)
                buffer_chars += len(chunk)
                if buffer_chars >= chunk_size:
                    _flush_buffer()
        else:
            buffer.append(text)
            buffer_chars += len(text)
            if buffer_chars >= chunk_size:
                _flush_buffer()

    if buffer:
        _flush_buffer()

    return {
        "source": source,
        "path": str(path),
        "total_lines": total_lines,
        "compressed": compressed,
        "failed": failed,
        "lu_codes": lu_codes,
    }


def discover_source_paths(source: str) -> List[Path]:
    """根据来源自动发现默认路径。"""
    paths: List[Path] = []
    if source == "kimi":
        base = HOME / ".kimi-code" / "sessions"
        if base.exists():
            paths = list(base.rglob("agents/main/wire.jsonl"))
    elif source == "claude":
        p = HOME / ".claude" / "history.jsonl"
        if p.exists():
            paths = [p]
    elif source == "cnsh":
        p = HOME / ".cnsh" / "logs" / "audit.log"
        if p.exists():
            paths = [p]
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description="龍魂 LU 记忆批量导入器")
    parser.add_argument("--source", "-s", required=True, choices=["kimi", "claude", "cnsh", "generic"], help="数据来源")
    parser.add_argument("--path", "-p", type=Path, help="文件或目录（generic 时必须指定）")
    parser.add_argument("--chunk-size", type=int, default=800, help="单个 LU 记忆最大字符数")
    parser.add_argument("--dry-run", action="store_true", help="只预览不压缩")
    args = parser.parse_args()

    sys.path.insert(0, str(HOME / "longhun-system" / "scripts"))
    from longhun_lu_compress import LonghunLuMemoryEngine

    engine = LonghunLuMemoryEngine()

    if args.source == "generic":
        if not args.path:
            print("🔴 generic 来源必须指定 --path")
            return 1
        targets = [args.path] if args.path.is_file() else list(args.path.rglob("*"))
    else:
        targets = discover_source_paths(args.source) if not args.path else [args.path]

    if not targets:
        print(f"🟡 未发现 {args.source} 的默认日志路径")
        return 0

    total = {"total_lines": 0, "compressed": 0, "failed": 0}
    for target in targets:
        if target.is_dir():
            continue
        print(f"\n📥 导入：{target}")
        result = import_file(target, args.source, engine, args.chunk_size, args.dry_run)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        for k in total:
            total[k] += result.get(k, 0)

    engine.close()

    print(f"\n🐉 导入完成：行数 {total['total_lines']} / 压缩 {total['compressed']} / 失败 {total['failed']}")
    print("DNA: #龍芯⚡️2026-06-30-LONGHUN-LU-IMPORTER-v1.0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

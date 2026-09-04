#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·丁酉·乙酉·午时·䷾既济-CNSH-STD-IO-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
CNSH 标准库 · io —— 文件读写（UTF-8 中文原生）
"""
from pathlib import Path


def read(path: str, encoding: str = "utf-8") -> str:
    """读取文本文件"""
    return Path(path).read_text(encoding=encoding)


def write(path: str, content: str, encoding: str = "utf-8") -> Path:
    """写入文本文件（自动建目录）"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding=encoding)
    return p


def append(path: str, content: str, encoding: str = "utf-8") -> Path:
    """追加文本（append-only 日志适用）"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding=encoding) as f:
        f.write(content if content.endswith("\n") else content + "\n")
    return p


def exists(path: str) -> bool:
    return Path(path).exists()


def remove(path: str) -> bool:
    """删除文件（P0 不删除只冻结：仅允许删除普通临时文件）"""
    p = Path(path)
    if p.is_file():
        p.unlink()
        return True
    return False


def list_dir(path: str = ".") -> list:
    return sorted(str(x) for x in Path(path).iterdir()) if Path(path).is_dir() else []


def read_json(path: str):
    import json
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: str, data) -> Path:
    import json
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return p

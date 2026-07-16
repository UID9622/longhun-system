#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""哈希公共模块。
DNA: #龍芯⚡️2026-06-27-LONGHUN-SYSTEM-CORE-HASHING-v1.0
"""
import hashlib
from pathlib import Path
from typing import Union


def hash_file(path: Union[str, Path], algorithm: str = "sha256") -> str:
    path = Path(path)
    if not path.exists():
        return ""
    hasher = hashlib.new(algorithm)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def hash_string(text: str, algorithm: str = "sha256") -> str:
    return hashlib.new(algorithm, text.encode("utf-8")).hexdigest()

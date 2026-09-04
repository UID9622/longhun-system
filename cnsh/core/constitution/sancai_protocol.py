# P0焊死: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
# License: CC BY-NC-SA 4.0（核心思想层·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-SANCAI-PROTOCOL-UID9622-v1.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║     龍魂系统·三才算法协议 · 宪法层内核模块                       ║
║                                                                  ║
║  三才算法 = 乾卦（天）+ 坤卦（地）+ 道德经（人）                 ║
║  以中宫五为锚点，369 为不动点循环。                              ║
║                                                                  ║
║  DNA: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-SANCAI-PROTOCOL-UID9622-v1.0             ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-777D                    ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                 ║
║                                                                  ║
║  性质: L0_CONSTITUTION · 不可覆盖 · 不可篡改 · 不可分割          ║
║  文件: 三才算法统一协议_天地人_v1.0.md                           ║
╚══════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import hashlib
import os
import re
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
    _HAS_YAML = True
except Exception:  # pragma: no cover
    _HAS_YAML = False

# ═══════════════════════════════════════════════════════════════
# 协议文件定位（与模块同目录）
# ═══════════════════════════════════════════════════════════════

PROTOCOL_FILE: Path = Path(__file__).with_name("三才算法统一协议_天地人_v1.0.md")
CHECKSUM_FILE: Path = Path(__file__).with_name("三才算法统一协议_天地人_v1.0.md.sha256")

# ═══════════════════════════════════════════════════════════════
# 异常与工具
# ═══════════════════════════════════════════════════════════════

class SancaiProtocolTamperedError(RuntimeError):
    """三才协议被篡改或缺失时抛出。任何系统组件捕获此错误都应触发熔断。"""
    pass


def _sha256_of_file(path: Path) -> str:
    """计算文件 SHA256。"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _set_readonly(path: Path) -> None:
    """将文件设为只读（所有者/组/其他人均只读）。"""
    if path.exists():
        os.chmod(path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)


def _parse_frontmatter(text: str) -> Dict[str, Any]:
    """解析 YAML frontmatter；无 YAML 库时使用最小化正则兜底。"""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    body = m.group(1)
    if _HAS_YAML:
        try:
            return yaml.safe_load(body) or {}
        except Exception:
            return {}
    # 最小化兜底：仅提取 dna 字段
    dna_m = re.search(r'^dna:\s*"?(#[^"\n]+)"?$', body, re.MULTILINE)
    return {"dna": dna_m.group(1)} if dna_m else {}


# ═══════════════════════════════════════════════════════════════
# 不可篡改校验
# ═══════════════════════════════════════════════════════════════

def verify_protocol_integrity() -> str:
    """
    校验协议文件完整性并强制只读。

    - 若协议文件不存在 → 触发 SancaiProtocolTamperedError
    - 若校验文件存在且哈希不匹配 → 触发 SancaiProtocolTamperedError
    - 若校验文件不存在 → 首次运行自动生成（后续即锁定）
    - 自动将协议文件与校验文件设为只读

    返回：当前协议文件 SHA256 哈希（小写十六进制）。
    """
    if not PROTOCOL_FILE.exists():
        raise SancaiProtocolTamperedError(
            f"三才算法协议文件缺失: {PROTOCOL_FILE}"
        )

    current_hash = _sha256_of_file(PROTOCOL_FILE)

    if CHECKSUM_FILE.exists():
        stored = CHECKSUM_FILE.read_text(encoding="utf-8").strip().split()[0]
        if stored.lower() != current_hash.lower():
            raise SancaiProtocolTamperedError(
                f"三才算法协议校验失败。stored={stored} current={current_hash}"
            )
    else:
        # 首次初始化：写入校验值并立即锁定
        CHECKSUM_FILE.write_text(
            f"{current_hash}  {PROTOCOL_FILE.name}\n", encoding="utf-8"
        )

    _set_readonly(PROTOCOL_FILE)
    _set_readonly(CHECKSUM_FILE)
    return current_hash


# 模块导入即执行校验，确保任何引用三才协议的代码都在校验通过后才能使用
_PROTOCOL_HASH: str = verify_protocol_integrity()


# ═══════════════════════════════════════════════════════════════
# 三才协议数据对象
# ═══════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class SancaiProtocol:
    """
    三才算法宪法层常量容器。

    frozen=True 保证运行时不可被任何代码重新赋值；
    实例化请使用 get_protocol() 工厂函数。
    """
    dna: str
    confirm_code: str
    gpg: str
    level: str
    # 三才
    tian: str          # 天 · 乾卦
    di: str            # 地 · 坤卦
    ren: str           # 人 · 道德经
    # 锚点
    zhonggong: int     # 中宫五
    # 369 不动点
    san: int           # 3 · 三才
    liu: int           # 6 · 六维推演
    jiu: int           # 9 · 九宫归一
    # 系统位置
    tian_layer: str    # 卦象层（执行）
    di_layer: str      # 卦象层（承载）
    ren_layer: str     # 底座层（不动）
    # 校验
    file_hash: str
    file_path: Path


def get_protocol() -> SancaiProtocol:
    """返回已校验的三才协议常量对象。"""
    front = _parse_frontmatter(PROTOCOL_FILE.read_text(encoding="utf-8"))
    return SancaiProtocol(
        dna=front.get("dna", "#龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-SANCAI-PROTOCOL-UID9622-v1.0"),
        confirm_code="#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-777D",
        gpg="A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
        level="L0_CONSTITUTION",
        tian="乾卦",
        di="坤卦",
        ren="道德经",
        zhonggong=5,
        san=3,
        liu=6,
        jiu=9,
        tian_layer="卦象层（执行）",
        di_layer="卦象层（承载）",
        ren_layer="底座层（不动）",
        file_hash=_PROTOCOL_HASH,
        file_path=PROTOCOL_FILE,
    )


# 全局唯一协议实例（导入时即锁定）
SANCAI: SancaiProtocol = get_protocol()


# ═══════════════════════════════════════════════════════════════
# 对齐校验接口
# ═══════════════════════════════════════════════════════════════

REQUIRED_ANCHORS: List[str] = ["乾卦", "坤卦", "道德经", "中宫五", "369"]


def validate_alignment(text: str, strict: bool = False) -> Dict[str, Any]:
    """
    校验任意文本/产物是否与三才算法锚点对齐。

    参数:
        text: 待校验字符串。
        strict: 为 True 时，缺少任一锚点返回 red 并触发熔断建议。

    返回:
        {
            "aligned": bool,
            "missing": List[str],
            "score": float,      # 0.0 ~ 1.0
            "level": str,        # 🟢 / 🟡 / 🔴
            "dna": str,          # 协议 DNA
        }
    """
    missing = [a for a in REQUIRED_ANCHORS if a not in text]
    score = (len(REQUIRED_ANCHORS) - len(missing)) / len(REQUIRED_ANCHORS)
    if score >= 0.8:
        level = "🟢"
    elif score >= 0.5:
        level = "🟡"
    else:
        level = "🔴"
    result = {
        "aligned": len(missing) == 0,
        "missing": missing,
        "score": round(score, 4),
        "level": level,
        "dna": SANCAI.dna,
    }
    if strict and missing:
        raise SancaiProtocolTamperedError(
            f"产物未通过三才算法对齐校验，缺失锚点: {missing}"
        )
    return result

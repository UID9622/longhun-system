#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-BRAIN_DNA_TRACER-v1.0-aa64864f
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
B8 · DNA追溯脑区 → P01 诸葛亮
====================================
DNA检测、生成、簽名验证。
对接现有 hetu_luoshu_dna.py DNA生成系统。

DNA: #龙芯⚡️丙午·丙申·丙辰·未时·需-BRAIN-B8-DNA-TRACER-v1.0
"""

import re
import hashlib
import json
import os
import sys
import datetime
from typing import Dict, Any, Optional


# ── DNA 常量 ──────────────────────────────────────────────────────────────────

DNA_VERSION = "v∞"
DNA_PREFIX = "#龙芯⚡️"
LEGACY_PREFIX = "#ZHUGEXIN⚡️"
DNA_PATTERN = r'(?:#龙芯⚡️|#ZHUGEXIN⚡️)[^\n]{8,}'
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def detect_dna(code: str) -> Optional[str]:
    """检测代码中的DNA追溯码"""
    m = re.search(DNA_PATTERN, code)
    if m:
        return m.group(0).strip()
    return None


def detect_confirm(code: str) -> bool:
    """检测确认码"""
    return CONFIRM_CODE in code


def validate_dna_structure(dna: str) -> Dict[str, Any]:
    """验证DNA格式"""
    result = {
        "valid": False,
        "format": "unknown",
        "version": "unknown",
        "issues": []
    }

    if not dna:
        result["issues"].append("DNA为空")
        return result

    if dna.startswith(DNA_PREFIX):
        result["format"] = "v∞ 干支格式"
        result["version"] = DNA_VERSION

        # 验证v∞格式: #龙芯⚡️年干支·月干支·日干支·时辰·卦名-模块-动作-哈希8位
        parts = dna.replace(DNA_PREFIX, "").split("-")
        if len(parts) >= 4:
            result["valid"] = True

            ganzhi_section = parts[0].split("·")
            if len(ganzhi_section) < 3:
                result["valid"] = False
                result["issues"].append("缺少完整的干支四柱")

            # 检查哈希
            hash_part = parts[-1]
            if len(hash_part) == 8:
                result["hash"] = hash_part
            else:
                result["issues"].append(f"哈希长度应为8，实际为{len(hash_part)}")

            result["module"] = parts[1] if len(parts) > 1 else "unknown"
            result["action"] = parts[2] if len(parts) > 2 else "unknown"
        else:
            result["issues"].append("DNA分段不足，应至少4段")

    elif dna.startswith(LEGACY_PREFIX):
        result["format"] = "v1.0 格里历（舊版）"
        result["version"] = "v1.0"
        result["valid"] = True
        result["issues"].append("⚠️ 使用舊版格里历格式，建议升级至v∞干支格式")

    else:
        result["format"] = "unknown"
        result["issues"].append("无法识别的DNA格式")

    return result


def compute_content_hash(code: str) -> str:
    """计算内容SHA256"""
    return hashlib.sha256(code.encode('utf-8')).hexdigest()


def generate_dna_stub(code: str, module: str = "CNSH", action: str = "TRANSLATE") -> str:
    """
    生成DNA存根
    实际生產环境应调用 hetu_luoshu_dna.py
    """
    content_hash = compute_content_hash(code)[:8].upper()

    # 嘗试使用现有DNA引擎
    try:
        engine_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "bin", "hetu_luoshu_dna.py"
        )
        if os.path.exists(engine_path):
            sys.path.insert(0, os.path.dirname(engine_path))
            # 实际生產环境会调用 generate_dna()
            sys.path.pop(0)
    except Exception:
        pass

    # 存根生成
    return f"{DNA_PREFIX}丙午·丙申·丙辰·未时·需-{module}-{action}-{content_hash}"


def execute(code: str, features: Dict[str, Any], step: int, total: int) -> Dict[str, Any]:
    """
    B8 脑区执行入口
    """
    existing_dna = detect_dna(code)
    has_confirm = detect_confirm(code)
    content_hash = compute_content_hash(code)

    dna_info = {
        "has_dna": existing_dna is not None,
        "dna_code": existing_dna,
        "dna_validation": validate_dna_structure(existing_dna) if existing_dna else None,
        "has_confirm": has_confirm,
        "content_hash": content_hash,
    }

    # 生成新DNA（如果没有）
    new_dna = None
    if not existing_dna:
        new_dna = generate_dna_stub(code)
        dna_info["new_dna"] = new_dna

    # 判定
    if existing_dna and dna_info["dna_validation"]["valid"]:
        status = "🟢 DNA有效"
        detail = f"DNA: {existing_dna[:60]}..."
    elif existing_dna:
        status = "🟡 DNA格式异常"
        detail = f"DNA存在但验证失敗: {dna_info['dna_validation']['issues']}"
    else:
        status = "🟡 无DNA·已生成"
        detail = f"新DNA: {new_dna[:60] if new_dna else '生成失敗'}..."

    return {
        "output_code": code,
        "auto_activate": [],
        "dna": dna_info,
        "status": status,
        "message": f"B8: {status} · SHA256={content_hash[:16]}"
    }


if __name__ == "__main__":
    test = "def hello(): return 'world'"
    r = execute(test, {}, 0, 0)
    import json
    print(json.dumps(r, indent=2, ensure_ascii=False))

#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂声纹验证与审计模块（多用户版）
LongHun Voice Anchor Verification & Audit - Multi-User

功能：
  - 输入数字人ID + 待验证声纹
  - 与 manifest.json 中的记录比对
  - 输出验证结果：匹配/不匹配，并记录审计日志

DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-VOICE-VERIFY-v2.0
"""

import json
from typing import Dict, List, Optional, Any

import numpy as np

from voice_anchor import (
    load_manifest,
    extract_features,
    compute_similarity,
    get_record_features,
    record_audio,
    log_audit,
    SAMPLE_RATE,
)

VERIFY_SIMILARITY_THRESHOLD = 0.85


def verify_voice(
    persona_id: str,
    audio: Optional[np.ndarray] = None,
    user_id: Optional[str] = None,
    duration: int = 5,
    sr: int = SAMPLE_RATE,
) -> Dict[str, Any]:
    """
    验证待验证声纹是否与指定数字人身份匹配。

    Args:
        persona_id: 数字人 ID
        audio: 待验证音频；None 则调用麦克风录制
        user_id: 可选，校验该记录是否属于指定用户
        duration: 录制时长
        sr: 采样率

    Returns:
        验证结果字典
    """
    manifest = load_manifest()
    record = None
    for r in manifest.get("anchors", []):
        if r.get("persona_id") == persona_id:
            if user_id and r.get("user_id", "system") != user_id:
                continue
            record = r
            break

    if not record:
        log_audit("verify", persona_id, "not_found", {"user_id": user_id})
        return {
            "status": "not_found",
            "message": "数字人身份不存在",
            "persona_id": persona_id,
        }

    if audio is None:
        print(f"🎙️  请朗读以下文本验证身份：\n   「{record.get('text', '')}」\n")
        audio = record_audio(duration, sr=sr)

    features = extract_features(audio, sr=sr)
    stored = get_record_features(record)
    if stored is None:
        return {
            "status": "error",
            "message": "无法读取锚定声纹特征",
            "persona_id": persona_id,
        }

    sim = compute_similarity(features, stored)
    matched = sim >= VERIFY_SIMILARITY_THRESHOLD
    result = "match" if matched else "mismatch"
    msg = "匹配" if matched else "不匹配"

    log_audit(
        "verify",
        persona_id,
        result,
        {
            "user_id": user_id,
            "similarity": round(sim, 4),
            "threshold": VERIFY_SIMILARITY_THRESHOLD,
            "dna": record.get("dna"),
        },
    )

    return {
        "status": result,
        "message": msg,
        "persona_id": persona_id,
        "user_id": record.get("user_id"),
        "similarity": round(sim, 4),
        "threshold": VERIFY_SIMILARITY_THRESHOLD,
        "dna": record.get("dna"),
        "text": record.get("text"),
    }


def list_anchors(user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """列出所有已锚定的数字人身份完整记录（可过滤用户）。"""
    manifest = load_manifest()
    anchors = manifest.get("anchors", [])
    if user_id:
        anchors = [r for r in anchors if r.get("user_id", "system") == user_id]
    return anchors


def show_audit_tail(n: int = 10) -> List[Dict[str, Any]]:
    """查看最近 n 条审计日志。"""
    from voice_anchor import AUDIT_LOG_PATH

    if not AUDIT_LOG_PATH.exists():
        return []
    lines = AUDIT_LOG_PATH.read_text(encoding="utf-8").strip().splitlines()
    records = []
    for line in lines[-n:]:
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python verify_anchor.py <persona_id> [user_id]")
        sys.exit(1)

    pid = sys.argv[1]
    uid = sys.argv[2] if len(sys.argv) > 2 else None
    result = verify_voice(pid, user_id=uid)
    print(json.dumps(result, ensure_ascii=False, indent=2))

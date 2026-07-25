#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂数字人身份固化模块（多用户版）
Dragon Soul Digital Persona Solidification - Multi-User

功能：
  - 读取 manifest.json 中的所有数字人身份记录
  - 将每个数字人身份与特定用户、文本、声纹特征绑定
  - 每次调用数字人前，先验证声纹特征是否与记录匹配
  - 验证通过才允许输出，否则返回“数字人身份不匹配”

DNA: #龍芯⚡️20260628-VOICE-PERSONA-v2.0
"""

import json
from typing import Dict, List, Optional, Any, Callable

import numpy as np

from voice_anchor import (
    load_manifest,
    extract_features,
    compute_similarity,
    get_record_features,
    log_audit,
    record_audio,
    SAMPLE_RATE,
)

VERIFICATION_SIMILARITY_THRESHOLD = 0.85


def load_personas(user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """读取已锚定的数字人身份；可指定 user_id 过滤。"""
    manifest = load_manifest()
    anchors = manifest.get("anchors", [])
    if user_id:
        anchors = [r for r in anchors if r.get("user_id", "system") == user_id]
    return anchors


def get_persona(persona_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """根据数字人 ID 获取单条记录；可选校验 user_id。"""
    for record in load_personas(user_id=user_id):
        if record.get("persona_id") == persona_id:
            return record
    return None


def verify_persona(
    persona_id: str,
    audio: Optional[np.ndarray] = None,
    user_id: Optional[str] = None,
    duration: int = 5,
    sr: int = SAMPLE_RATE,
) -> Dict[str, Any]:
    """验证数字人身份：比对输入声纹与锚定声纹。"""
    record = get_persona(persona_id, user_id=user_id)
    if not record:
        log_audit("verify_persona", persona_id, "not_found", {"user_id": user_id})
        return {
            "status": "not_found",
            "message": "数字人身份不存在",
            "persona_id": persona_id,
        }

    if audio is None:
        print(f"🎙️  请朗读锚定文本进行验证：\n   「{record.get('text', '')}」\n")
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
    matched = sim >= VERIFICATION_SIMILARITY_THRESHOLD
    result = "match" if matched else "mismatch"
    msg = "数字人身份验证通过" if matched else "数字人身份不匹配"

    log_audit(
        "verify_persona",
        persona_id,
        result,
        {"user_id": user_id, "similarity": round(sim, 4), "threshold": VERIFICATION_SIMILARITY_THRESHOLD},
    )

    return {
        "status": result,
        "message": msg,
        "persona_id": persona_id,
        "user_id": record.get("user_id"),
        "similarity": round(sim, 4),
        "threshold": VERIFICATION_SIMILARITY_THRESHOLD,
        "dna": record.get("dna"),
        "text": record.get("text"),
    }


def invoke_persona(
    persona_id: str,
    audio: Optional[np.ndarray] = None,
    user_id: Optional[str] = None,
    callback: Optional[Callable[[Dict[str, Any]], Any]] = None,
    **kwargs,
) -> Dict[str, Any]:
    """调用数字人：先验证声纹，验证通过后才执行回调输出内容。"""
    record = get_persona(persona_id, user_id=user_id)
    if not record:
        return {
            "status": "not_found",
            "message": "数字人身份不存在",
            "persona_id": persona_id,
        }

    verify_result = verify_persona(persona_id, audio=audio, user_id=user_id, **kwargs)
    if verify_result["status"] != "match":
        return {
            "status": "blocked",
            "message": "数字人身份不匹配，调用被拒绝",
            "verification": verify_result,
        }

    output = None
    if callback:
        try:
            output = callback(record)
        except Exception as e:
            return {
                "status": "error",
                "message": f"数字人调用成功但回调执行失败: {e}",
                "verification": verify_result,
            }

    return {
        "status": "invoked",
        "message": "数字人身份已验证，调用成功",
        "persona_id": persona_id,
        "verification": verify_result,
        "output": output,
    }


def list_personas(user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """列出数字人身份摘要（可过滤用户）。"""
    result = []
    for record in load_personas(user_id=user_id):
        result.append(
            {
                "user_id": record.get("user_id"),
                "persona_id": record.get("persona_id"),
                "text": record.get("text"),
                "dna": record.get("dna"),
                "created_at": record.get("created_at"),
                "ip": record.get("ip"),
            }
        )
    return result


if __name__ == "__main__":
    print("已锚定数字人身份：")
    for p in list_personas():
        print(json.dumps(p, ensure_ascii=False, indent=2))

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂声纹开放注册模块
Dragon Soul Voice Open Registration

功能：
  - 对外提供用户声纹注册入口
  - 自动生成包含 user_id / 声纹指纹 / 注册时间 / 数字人ID 的 DNA 锚定链
  - 默认启用本地加密存储
  - 所有记录统一写入 ~/.龍魂/voice_anchors/manifest.json

DNA: #龍芯⚡️20260628-VOICE-REGISTER-v1.0
"""

import re
import uuid
from typing import Dict, Any, Optional

import numpy as np

from voice_anchor import anchor_voice, generate_test_audio, SAMPLE_RATE
from digital_persona import verify_persona


def sanitize_user_id(user_id: str) -> str:
    """清理用户ID，仅保留字母、数字、下划线、连字符、点。"""
    return re.sub(r"[^a-zA-Z0-9_\-\.]", "", user_id)[:64]


def register_user_voice(
    user_id: str,
    text: str,
    audio: Optional[np.ndarray] = None,
    encrypt: bool = True,
    duration: int = 5,
    source: str = "web",
    sr: int = SAMPLE_RATE,
) -> Dict[str, Any]:
    """
    用户声纹注册入口。

    Args:
        user_id: 用户唯一标识
        text: 锚定文本
        audio: 音频数组；None 则录制
        encrypt: 是否加密特征向量
        duration: 录制时长
        source: 来源标记（web/app/cli）
        sr: 采样率

    Returns:
        注册结果字典
    """
    if not user_id or not user_id.strip():
        return {"status": "error", "message": "用户ID不能为空"}
    user_id = sanitize_user_id(user_id)

    if not text or not text.strip():
        return {"status": "error", "message": "锚定文本不能为空"}

    return anchor_voice(
        text=text,
        audio=audio,
        user_id=user_id,
        encrypt=encrypt,
        duration=duration,
        source=source,
        sr=sr,
    )


def verify_user_voice(
    user_id: str,
    persona_id: str,
    audio: Optional[np.ndarray] = None,
    duration: int = 5,
) -> Dict[str, Any]:
    """
    用户声纹验证入口（带 user_id 校验，防止越权验证）。
    """
    return verify_persona(
        persona_id=persona_id,
        audio=audio,
        user_id=sanitize_user_id(user_id),
        duration=duration,
    )


def get_user_personas(user_id: str) -> Dict[str, Any]:
    """获取某用户的所有数字人身份摘要。"""
    from digital_persona import list_personas

    uid = sanitize_user_id(user_id)
    personas = list_personas(user_id=uid)
    return {
        "status": "success",
        "user_id": uid,
        "count": len(personas),
        "personas": personas,
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("用法: python register.py <user_id> <text> [--test]")
        sys.exit(1)

    uid = sys.argv[1]
    text = sys.argv[2]
    test_mode = "--test" in sys.argv

    audio = generate_test_audio(frequency=230) if test_mode else None
    result = register_user_voice(uid, text, audio=audio, source="test" if test_mode else "cli")
    print(json.dumps(result, ensure_ascii=False, indent=2))

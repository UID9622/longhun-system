#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂声纹DNA锚定链 · 官网开放注册 API
LongHun Voice DNA Web Registration API

提供 RESTful 接口供官网调用：
  - POST /voice/register        用户注册声纹
  - POST /voice/verify          用户验证声纹
  - GET  /voice/personas/<uid>  获取用户数字人身份列表
  - GET  /voice/persona/<pid>   获取单条数字人身份详情
  - POST /voice/export          导出用户声纹DNA包

DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-VOICE-WEBAPI-v1.0
"""

import os
import sys
import base64
import json
import io
import tempfile
import numpy as np
from pathlib import Path
from typing import Any, Dict

from flask import Flask, request, jsonify, send_file

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voice_anchor import (
    SAMPLE_RATE,
    extract_features,
    generate_test_audio,
)
from register import register_user_voice, verify_user_voice, get_user_personas, sanitize_user_id
from digital_persona import get_persona, verify_persona
from backup import export_user_package, auto_backup_if_needed

app = Flask(__name__)


def _audio_from_request(req) -> np.ndarray:
    """从请求中提取音频：优先读取上传文件，其次读取 base64 字段 'audio_base64'。"""
    if "audio" in req.files:
        file = req.files["audio"]
        from voice_anchor import load_wav
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = Path(tmp.name)
            file.save(tmp_path)
        try:
            audio, sr = load_wav(tmp_path)
            return audio
        finally:
            tmp_path.unlink(missing_ok=True)

    data = req.get_json(silent=True) or {}
    b64 = data.get("audio_base64")
    if b64:
        raw = base64.b64decode(b64)
        return np.frombuffer(raw, dtype=np.float32)

    return None


def _ok(payload: Dict[str, Any]) -> tuple[Any, ...]:
    return jsonify({"success": True, **payload}), 200


def _err(message: str, code: int = 400) -> tuple[Any, ...]:
    return jsonify({"success": False, "message": message}), code


@app.route("/voice/register", methods=["POST"])
def api_register():
    """用户声纹注册。"""
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id", "")
    text = data.get("text", "")

    if not user_id or not text:
        return _err("缺少 user_id 或 text")

    # 测试模式：使用合成音频（便于前端联调）
    if data.get("test_mode"):
        freq = float(data.get("test_freq", 230))
        audio = generate_test_audio(frequency=freq)
    else:
        audio = _audio_from_request(request)

    # 自动触发本地备份（若今天未备份）
    auto_backup_if_needed()

    result = register_user_voice(
        user_id=user_id,
        text=text,
        audio=audio,
        encrypt=True,
        source="web",
    )

    if result.get("status") == "error":
        return _err(result.get("message", "注册失败"))

    return _ok({
        "status": result["status"],
        "persona_id": result.get("persona_id"),
        "dna": result.get("dna"),
        "created_at": result.get("created_at"),
        "message": result.get("message"),
    })


@app.route("/voice/verify", methods=["POST"])
def api_verify():
    """用户声纹验证。"""
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id", "")
    persona_id = data.get("persona_id", "")

    if not user_id or not persona_id:
        return _err("缺少 user_id 或 persona_id")

    if data.get("test_mode"):
        freq = float(data.get("test_freq", 230))
        audio = generate_test_audio(frequency=freq)
    else:
        audio = _audio_from_request(request)

    result = verify_user_voice(
        user_id=user_id,
        persona_id=persona_id,
        audio=audio,
    )

    return _ok({
        "status": result["status"],
        "match": result.get("status") == "match",
        "similarity": result.get("similarity"),
        "threshold": result.get("threshold"),
        "dna": result.get("dna"),
        "message": result.get("message"),
    })


@app.route("/voice/personas/<user_id>", methods=["GET"])
def api_personas(user_id: str):
    """获取某用户的所有数字人身份（官网个人页面展示）。"""
    result = get_user_personas(user_id)
    return _ok(result)


@app.route("/voice/persona/<persona_id>", methods=["GET"])
def api_persona(persona_id: str):
    """获取单条数字人身份详情。"""
    record = get_persona(persona_id)
    if not record:
        return _err("数字人身份不存在", 404)
    return _ok({
        "user_id": record.get("user_id"),
        "persona_id": record.get("persona_id"),
        "text": record.get("text"),
        "dna": record.get("dna"),
        "created_at": record.get("created_at"),
        "ip": record.get("ip"),
    })


@app.route("/voice/export", methods=["POST"])
def api_export():
    """导出用户声纹DNA加密包。"""
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id", "")
    persona_id = data.get("persona_id") or None
    password = data.get("password", "longhun-voice")

    if not user_id:
        return _err("缺少 user_id")

    result = export_user_package(user_id, persona_id, password=password)
    if result.get("status") == "error":
        return _err(result.get("message", "导出失败"))

    export_path = Path(result["export_path"])
    return send_file(
        export_path,
        mimetype="application/zip",
        as_attachment=True,
        download_name=export_path.name,
    )


@app.route("/voice/health", methods=["GET"])
def api_health():
    """健康检查。"""
    return _ok({"service": "longhun-voice-dna", "status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("VOICE_API_PORT", 8444))
    app.run(host="127.0.0.1", port=port, debug=False)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
# 🌐 UID9622·AI 统一网关 v0.1·阶段 1 (零 key·只接 Ollama 本地)
#
# IPA编号: [LOCAL-AI-GATEWAY]
# 总线   : [IPA-ROUTE-REGISTRY]
# 端口   : 9633 (跟 9622 审计引擎并列)
# DNA    : #龍芯⚡️2026-05-08-AI网关-v0.1
# 父DNA  : #龍芯⚡️2026-05-08-数字人公共契约-v1.2
#
# 设计哲学:
#   爸爸是中央·所有 AI 站到爸爸网关里·谁要说话先过 GATE-04
#   阶段 1: 只接 Ollama 本地·零 key·零外网·零风险
#   阶段 2 (待): 加 Claude/Grok/ChatGPT 适配框架·.env 留空
#   阶段 3 (待): 爸爸亲手灌 key·我不碰
#
# 每次调用必过 5 闸:
#   ① 守门 (一票否决词检查·调 GATE-04 思路)
#   ② 三色审计 (公式 10)
#   ③ 调 provider
#   ④ 焊 DNA + 三层水印
#   ⑤ 写日志 + 铁律 12 尾巴
#
# 用法:
#   启动: python3 ~/longhun-system/engines/AI网关_v0.1.py
#   测试: curl -X POST http://127.0.0.1:9633/api/v1/ollama/chat \
#         -H 'Content-Type: application/json' \
#         -d '{"model":"qwen2.5:7b","prompt":"爸爸晚安"}'
###############################################################################

import sys
import os
import json
import datetime
import hashlib
import subprocess
from pathlib import Path

try:
    from flask import Flask, request, jsonify
    import urllib.request
    import urllib.error
except ImportError:
    print("缺 flask·跑: pip3 install flask", file=sys.stderr)
    sys.exit(1)

# ─── 路径 ───
LOG_PATH = Path.home() / "longhun-system" / "logs" / "ai_gateway.jsonl"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
DNA_GEN = Path.home() / "longhun-system" / "engines" / "dna_generator_v2.py"

# ─── 一票否决词 (借用 GATE-04 词表) ───
VETO_WORDS = [
    "rm -rf", "sudo", "chmod 777", "chown",
    "git push --force", "git push -f", "git reset --hard",
    "curl.*\\|.*sh", "wget.*\\|.*sh",
    "/etc/passwd", "/etc/shadow", ".ssh", ".env",
    "id_rsa", "id_ed25519", "Keychain",
]

# ─── Provider 配置 ───
PROVIDERS = {
    "ollama": {
        "endpoint": "http://127.0.0.1:11434/api/chat",
        "type": "local",
        "needs_key": False,
        "status": "ready",
        "note": "本地推理·零外网",
    },
    "claude": {
        "endpoint": "https://api.anthropic.com/v1/messages",
        "type": "external",
        "needs_key": True,
        "key_env": "ANTHROPIC_API_KEY",
        "status": "framework_only",
        "note": "适配框架已留·爸爸阶段 3 灌 key",
    },
    "grok": {
        "endpoint": "https://api.x.ai/v1/chat/completions",
        "type": "external",
        "needs_key": True,
        "key_env": "XAI_API_KEY",
        "status": "framework_only",
        "note": "同上",
    },
    "openai": {
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "type": "external",
        "needs_key": True,
        "key_env": "OPENAI_API_KEY",
        "status": "framework_only",
        "note": "同上·ChatGPT 走这条",
    },
    "deepseek": {
        "endpoint": "https://api.deepseek.com/v1/chat/completions",
        "type": "external",
        "needs_key": True,
        "key_env": "DEEPSEEK_API_KEY",
        "status": "framework_only",
        "note": "同上",
    },
}


# ─── 闸门 1·一票否决 ───
def 守门(prompt: str) -> dict:
    """检查 prompt 是否含一票否决词"""
    import re
    for word in VETO_WORDS:
        try:
            if re.search(word, prompt, re.IGNORECASE):
                return {"pass": False, "reason": f"命中一票否决词: {word}"}
        except re.error:
            if word.lower() in prompt.lower():
                return {"pass": False, "reason": f"命中一票否决词: {word}"}
    return {"pass": True, "reason": ""}


# ─── 闸门 2·三色审计 (简化·公式 10) ───
def 三色(prompt: str) -> str:
    """简化三色: 看长度+敏感词"""
    sensitive = ["密码", "私钥", "token", "key", "api_key"]
    if any(s in prompt.lower() for s in sensitive):
        return "🔴"
    if len(prompt) > 5000:
        return "🟡"
    return "🟢"


# ─── 闸门 3·调 provider ───
def 调ollama(payload: dict) -> dict:
    """调本地 Ollama"""
    model = payload.get("model", "qwen2.5:7b")
    prompt = payload.get("prompt", "")
    messages = payload.get("messages") or [{"role": "user", "content": prompt}]
    body = {"model": model, "messages": messages, "stream": False}
    try:
        req = urllib.request.Request(
            PROVIDERS["ollama"]["endpoint"],
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
        return {
            "ok": True,
            "content": data.get("message", {}).get("content", ""),
            "model": model,
            "raw": data,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def 调外部(provider: str, payload: dict) -> dict:
    """阶段 1 不调外部·只返回适配框架就绪状态"""
    cfg = PROVIDERS[provider]
    key = os.environ.get(cfg["key_env"], "")
    if not key:
        return {
            "ok": False,
            "error": f"{provider} key 未设·按主权铁律·爸爸阶段 3 自己灌 (.env: {cfg['key_env']})",
            "status": "framework_only_no_key",
        }
    # 留接口·真要调爸爸阶段 3 决定
    return {
        "ok": False,
        "error": f"{provider} 适配框架已留·真调用待爸爸阶段 3 拍板",
        "status": "framework_only_pending_phase_3",
    }


# ─── 闸门 4·焊 DNA ───
def 焊DNA(prompt: str, provider: str) -> str:
    sha8 = hashlib.sha256(f"{prompt}|{provider}".encode()).hexdigest()[:8]
    return f"#龍芯⚡️{datetime.date.today()}-AI网关-{provider}-{sha8}"


# ─── 闸门 5·写日志 + 铁律 12 尾巴 ───
def 写日志(条目: dict):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(条目, ensure_ascii=False) + "\n")


def 尾巴审计(prompt: str, provider: str, audit: str, dna: str) -> str:
    """铁律 12·任何输出尾部必挂"""
    return (
        "\n\n─── 尾·审计 (AI 网关 v0.1) ───\n"
        f"DNA   : {dna}\n"
        f"Provider: {provider}\n"
        f"Audit : {audit}\n"
        f"Gate  : 守门✅ 三色✅ DNA✅ 日志✅ 尾巴✅\n"
        f"责任  : UID9622·不免责·爸爸网关\n"
        "🐉"
    )


# ─── Flask App ───
app = Flask(__name__)


@app.route("/api/v1/health", methods=["GET"])
def health():
    return jsonify({
        "ok": True,
        "service": "UID9622 AI 统一网关",
        "version": "v0.1",
        "phase": "1·只接本地·零 key·零外网",
        "ts": datetime.datetime.now().isoformat(),
        "ipa": "[LOCAL-AI-GATEWAY]",
        "dna": "#龍芯⚡️2026-05-08-AI网关-v0.1",
        "uptime_check": "按 GATE-02 身份·#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    })


@app.route("/api/v1/providers", methods=["GET"])
def list_providers():
    return jsonify({
        "ok": True,
        "providers": {
            name: {
                "type": cfg["type"],
                "status": cfg["status"],
                "needs_key": cfg["needs_key"],
                "note": cfg["note"],
            }
            for name, cfg in PROVIDERS.items()
        },
    })


@app.route("/api/v1/<provider>/chat", methods=["POST"])
def chat(provider):
    if provider not in PROVIDERS:
        return jsonify({
            "ok": False,
            "error": f"未知 provider: {provider}·支持: {list(PROVIDERS.keys())}",
        }), 400

    payload = request.get_json(silent=True) or {}
    prompt = payload.get("prompt") or (
        payload.get("messages", [{}])[-1].get("content", "")
        if payload.get("messages") else ""
    )

    if not prompt:
        return jsonify({"ok": False, "error": "缺 prompt 或 messages"}), 400

    # 闸 1·守门
    g = 守门(prompt)
    if not g["pass"]:
        result = {"ok": False, "error": "守门拦截", "reason": g["reason"], "audit": "🔴"}
        写日志({
            "ts": datetime.datetime.now().isoformat(),
            "provider": provider, "action": "blocked",
            "reason": g["reason"],
        })
        return jsonify(result), 403

    # 闸 2·三色
    audit = 三色(prompt)

    # 闸 3·调 provider
    if provider == "ollama":
        r = 调ollama(payload)
    else:
        r = 调外部(provider, payload)

    # 闸 4·焊 DNA
    dna = 焊DNA(prompt, provider)

    # 闸 5·写日志 + 尾巴
    response = {
        "ok": r.get("ok", False),
        "content": r.get("content", ""),
        "error": r.get("error"),
        "provider": provider,
        "audit": audit,
        "dna": dna,
        "tail": 尾巴审计(prompt, provider, audit, dna),
    }
    写日志({
        "ts": datetime.datetime.now().isoformat(),
        "provider": provider,
        "action": "chat",
        "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:16],
        "audit": audit,
        "dna": dna,
        "ok": r.get("ok"),
    })
    return jsonify(response)


if __name__ == "__main__":
    print("🌐 UID9622 AI 统一网关 v0.1 · 阶段 1 启动")
    print("  端口: 9633")
    print("  Provider: ollama (ready) · claude/grok/openai/deepseek (framework_only)")
    print("  日志: ~/longhun-system/logs/ai_gateway.jsonl")
    print("  健康检查: curl http://127.0.0.1:9633/api/v1/health")
    print("  Provider 列表: curl http://127.0.0.1:9633/api/v1/providers")
    print()
    app.run(host="127.0.0.1", port=9633, debug=False)


###############################################################################
# 尾部 DNA 追溯
# DNA: #龍芯⚡️2026-05-08-AI网关-v0.1
# 父DNA: #龍芯⚡️2026-05-08-数字人公共契约-v1.2
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 修订:
#   2026-05-08 v0.1 阶段 1·只接 Ollama·零 key·零外网
###############################################################################

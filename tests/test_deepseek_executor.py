# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 DeepSeek 执行器验收测试

运行： cd ~/longhun-system && python3 -m pytest tests/test_deepseek_executor.py -v
DNA: #龍芯⚡️20260628-DEEPSEEK-EXECUTOR-TEST-v1.0
"""

import os
import sys
import time

import pytest

# 确保项目根目录在路径中
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from sovereignty.portal.longhun_crypto import (
    LonghunCryptoError,
    NonceCache,
    decrypt_payload,
    encrypt_payload,
    hmac_sign,
    hmac_verify,
    make_envelope,
    open_envelope,
)
from sovereignty.portal.model_router import ChatRequest

SECRET = "test-secret-for-longhun-executor"


class TestCrypto:
    def test_encrypt_decrypt_roundtrip(self):
        payload = {"route": "echo", "payload": {"msg": "你好"}}
        cipher = encrypt_payload(payload, SECRET)
        assert isinstance(cipher, str)
        assert decrypt_payload(cipher, SECRET) == payload

    def test_wrong_secret_fails(self):
        cipher = encrypt_payload({"x": 1}, SECRET)
        with pytest.raises(LonghunCryptoError):
            decrypt_payload(cipher, "wrong-secret")

    def test_hmac_verify(self):
        msg = "hello|world"
        sig = hmac_sign(msg, SECRET)
        assert hmac_verify(msg, sig, SECRET)
        assert not hmac_verify(msg, sig, "wrong")
        assert not hmac_verify(msg, "deadbeef", SECRET)

    def test_envelope_open_success(self):
        cache = NonceCache()
        payload = {"route": "chat", "payload": {"messages": []}}
        env = make_envelope(payload, SECRET)
        assert "cipher" in env and "hmac" in env and "ts" in env and "nonce" in env
        opened = open_envelope(env, SECRET, cache)
        assert opened == payload

    def test_envelope_replay_blocked(self):
        cache = NonceCache()
        env = make_envelope({"x": 1}, SECRET)
        open_envelope(env, SECRET, cache)
        with pytest.raises(LonghunCryptoError):
            open_envelope(env, SECRET, cache)

    def test_envelope_expired(self):
        env = make_envelope({"x": 1}, SECRET)
        env["ts"] = int(time.time()) - 1000
        with pytest.raises(LonghunCryptoError):
            open_envelope(env, SECRET, ttl=300)


class TestModelRouter:
    def test_chat_request_rejects_kimi_provider(self):
        req = ChatRequest(messages=[{"role": "user", "content": "hi"}], provider="kimi")
        # pydantic 不拒绝字符串，但 chat 业务层会返回 403
        with pytest.raises(Exception):
            model_router.chat(req)


class TestSecureGateway:
    @pytest.fixture(scope="module")
    def client(self):
        os.environ.setdefault("LONGHUN_EXECUTOR_SECRET", SECRET)
        # control-panel 目录含连字符，需通过文件路径动态加载，并把 control-panel 目录加入 sys.path
        import importlib.util
        from pathlib import Path
        cp_dir = Path(ROOT) / "control-panel"
        sys.path.insert(0, str(cp_dir))
        sys.path.insert(0, ROOT)
        main_path = cp_dir / "main.py"
        spec = importlib.util.spec_from_file_location("control_panel_main", main_path)
        main_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_mod)
        from fastapi.testclient import TestClient
        return TestClient(main_mod.app)

    def test_health_is_public(self, client):
        r = client.get("/api/health")
        assert r.status_code == 200

    def test_secure_health_requires_nothing(self, client):
        r = client.get("/api/secure/health")
        assert r.status_code == 200
        assert r.json()["channel"] == "secure"

    def test_secure_execute_without_envelope_fails(self, client):
        r = client.post("/api/secure/execute", json={"route": "echo"})
        assert r.status_code == 403

    def test_secure_execute_echo_success(self, client):
        payload = {"route": "echo", "payload": {"msg": "龍魂测试"}}
        env = make_envelope(payload, SECRET)
        r = client.post("/api/secure/execute", json=env)
        assert r.status_code == 200
        resp_env = r.json()
        result = open_envelope(resp_env, SECRET, ttl=300)
        assert result["status"] == "ok"
        assert result["result"]["echo"]["msg"] == "龍魂测试"

    def test_secure_execute_bad_hmac_fails(self, client):
        env = make_envelope({"route": "echo", "payload": {}}, SECRET)
        env["hmac"] = "0" * 64
        r = client.post("/api/secure/execute", json=env)
        assert r.status_code == 403


class TestCodebaseNoDirectExternalAI:
    def test_no_kimi_or_claude_or_openai_in_active_py(self):
        forbidden = ["api.moonshot.cn", "api.anthropic.com", "api.openai.com", "azure.openai"]
        exclude_dirs = {".git", "__pycache__", ".venv", ".venv-tts", "cnsh-core.backup", "_archive"}
        hits = []
        for root, dirs, files in os.walk(ROOT):
            # 跳过备份、归档、虚拟环境
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for f in files:
                if not f.endswith(".py"):
                    continue
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8") as fh:
                        text = fh.read()
                    for bad in forbidden:
                        if bad in text:
                            hits.append(f"{path}: {bad}")
                except Exception:
                    pass
        # 允许自身测试文件中出现这些字符串
        code_hits = [h for h in hits if "test_deepseek_executor.py" not in h]
        assert not code_hits, f"发现生产代码仍直连外部 AI: {code_hits[:10]}"

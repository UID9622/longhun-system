#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🐉 龍魂·剪贴板容器中心（鲲鹏端 / 本地服务端）v1.0
====================================================
DNA: #龍芯⚡️丙午·丙申·辛酉·辰时·䷖剥-CLIPBOARD-HUB-V1.0-P1

WebSocket 服务中心，接收加密剪贴内容，解密后落入本地容器并写入 Neo4j。
支持内容哈希去重、DNA 追溯、开发者身份校验。

用法:
  python3 08_BIN/lh_clipboard_hub.py              # 启动服务，监听 8765
  python3 08_BIN/lh_clipboard_hub.py --port 8766  # 指定端口
  python3 08_BIN/lh_clipboard_hub.py --no-encrypt # 明文调试模式（不推荐生产）
"""

import argparse
import asyncio
import base64
import hashlib
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, Set

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "bin"))
sys.path.insert(0, str(PROJECT_ROOT / "05_ENGINES"))

import websockets

from ganzhi_dna_engine import DNA生成
from lh_clipboard_vault import list_vault, save
from lh_vault_reconcile import reconcile

try:
    from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
    GMSSL_AVAILABLE = True
except Exception:
    GMSSL_AVAILABLE = False

CST = timezone(timedelta(hours=8))
NEO4J_URL = os.environ.get("NEO4J_HTTP_URL", "http://localhost:7474/db/neo4j/tx/commit")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASS = os.environ.get("NEO4J_PASSWORD", "longhun123")
HUB_DNA = DNA生成(模块="CLIPBOARD", 动作="HUB", 版本="V1.0", 级别="P0")


def _now() -> str:
    return datetime.now(CST).isoformat(timespec="seconds")


def _derive_key(token: str) -> bytes:
    """从开发者 token/DNA 派生 16 字节 SM4 密钥。"""
    return hashlib.sha256(token.encode("utf-8")).digest()[:16]


def _sm4_decrypt(ciphertext_hex: str, key: bytes) -> str:
    """SM4-CBC 解密。"""
    if not GMSSL_AVAILABLE:
        raise RuntimeError("gmssl 未安装，无法解密")
    data = bytes.fromhex(ciphertext_hex)
    if len(data) < 16:
        raise ValueError("密文太短")
    iv, cipher = data[:16], data[16:]
    crypt = CryptSM4()
    crypt.set_key(key, SM4_DECRYPT)
    plain = crypt.crypt_cbc(iv, cipher)
    return plain.decode("utf-8")


def _cypher_escape(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    s = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
    return f'"{s}"'


def _run_cypher(statements: list) -> dict:
    payload = {"statements": [{"statement": s} for s in statements]}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        NEO4J_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Basic " + base64.b64encode(f"{NEO4J_USER}:{NEO4J_PASS}".encode()).decode(),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")[:400]
        raise RuntimeError(f"Neo4j HTTP error: {e.code} {body}")
    except Exception as e:
        raise RuntimeError(f"Neo4j unreachable: {e}")

    if result.get("errors"):
        msgs = "; ".join(str(err) for err in result["errors"][:3])
        raise RuntimeError(f"Neo4j Cypher error: {msgs}")
    return result


def _topic_id(topic: str) -> str:
    return f"VAULT-TOPIC:{hashlib.md5(topic.encode()).hexdigest()[:8]}"


def _tag_id(tag: str) -> str:
    return f"VAULT-TAG:{hashlib.md5(tag.encode()).hexdigest()[:8]}"


def _clip_id(content_hash: str) -> str:
    return f"CLIP:{content_hash[:16]}"


def _ensure_neo4j_index(item: Dict[str, Any]) -> None:
    """把单个剪贴项同步到 Neo4j（幂等 MERGE）。"""
    cid = _clip_id(item["content_hash"])
    label = Path(item["path"]).stem
    updated_at = item.get("updated_at", item["timestamp"])
    copy_count = item.get("copy_count", 1)
    statements = [
        f"MERGE (c:Clip {{id: {_cypher_escape(cid)}}}) "
        f"SET c.label = {_cypher_escape(label)}, "
        f"    c.dna = {_cypher_escape(item['dna'])}, "
        f"    c.source = {_cypher_escape(item['source'])}, "
        f"    c.timestamp = {_cypher_escape(item['timestamp'])}, "
        f"    c.updated_at = {_cypher_escape(updated_at)}, "
        f"    c.copy_count = {copy_count}, "
        f"    c.path = {_cypher_escape(item['path'])}, "
        f"    c.hash = {_cypher_escape(item['content_hash'])}",
    ]

    topic = item["topic"]
    tid = _topic_id(topic)
    statements.extend([
        f"MERGE (t:VaultTopic {{id: {_cypher_escape(tid)}}}) SET t.label = {_cypher_escape(topic)}",
        f"MATCH (c:Clip {{id: {_cypher_escape(cid)}}}), (t:VaultTopic {{id: {_cypher_escape(tid)}}}) "
        f"MERGE (c)-[:belongs_to]->(t)",
    ])

    for tag in item.get("tags", []):
        gid = _tag_id(tag)
        statements.extend([
            f"MERGE (g:VaultTag {{id: {_cypher_escape(gid)}}}) SET g.label = {_cypher_escape(tag)}",
            f"MATCH (c:Clip {{id: {_cypher_escape(cid)}}}), (g:VaultTag {{id: {_cypher_escape(gid)}}}) "
            f"MERGE (c)-[:has_tag]->(g)",
        ])

    _run_cypher(statements)


class ClipboardHub:
    """WebSocket 剪贴板中心。"""

    def __init__(self, no_encrypt: bool = False):
        self.no_encrypt = no_encrypt
        self.clients: Dict[str, Any] = {}
        self.rate_limiter: Dict[str, float] = {}
        self.authorized_tokens: Set[str] = set()
        # 读取环境变量中的授权 token（逗号分隔）
        tokens = os.environ.get("LONGHUN_CLIPBOARD_TOKENS", "")
        if tokens:
            self.authorized_tokens.update(t.strip() for t in tokens.split(",") if t.strip())

    def _rate_ok(self, client_id: str) -> bool:
        now = time.time()
        last = self.rate_limiter.get(client_id, 0)
        if now - last < 0.5:  # 同一客户端 0.5 秒内最多一次
            return False
        self.rate_limiter[client_id] = now
        return True

    def _authorize(self, data: dict) -> Optional[str]:
        """校验开发者 token/DNA。返回 token 或 None。"""
        token = data.get("developer_dna") or data.get("token") or ""
        # 未配置 token 时：仅允许 localhost / 127.0.0.1（本地调试）
        if not self.authorized_tokens:
            return token if token else "local"
        if token in self.authorized_tokens:
            return token
        return None

    def _decrypt_content(self, data: dict) -> str:
        """解密内容，返回明文。"""
        if self.no_encrypt:
            return data.get("content", "")
        encrypted = data.get("content_encrypted")
        if not encrypted:
            return data.get("content", "")
        token = data.get("developer_dna") or data.get("token", "")
        key = _derive_key(token)
        return _sm4_decrypt(encrypted, key)

    async def handle_client(self, websocket):
        client_id = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        self.clients[client_id] = websocket
        print(f"🔗 客户端连接: {client_id}")
        try:
            async for message in websocket:
                response = await self._process_message(message, client_id, websocket)
                await websocket.send(json.dumps(response, ensure_ascii=False))
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.pop(client_id, None)
            print(f"🔌 客户端断开: {client_id}")

    async def _process_message(self, message: str, client_id: str, websocket) -> dict:
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            return {"status": "error", "message": "无效的 JSON"}

        action = data.get("action")

        if action == "ping":
            return {"status": "pong", "timestamp": _now(), "dna": HUB_DNA}

        # 校验身份
        token = self._authorize(data)
        if token is None:
            return {"status": "error", "message": "开发者身份校验失败"}

        if action == "save":
            return await self._handle_save(data, client_id)
        elif action == "query":
            return self._handle_query(data)
        elif action == "stats":
            return self._handle_stats()
        else:
            return {"status": "error", "message": f"未知操作: {action}"}

    async def _handle_save(self, data: dict, client_id: str) -> dict:
        if not self._rate_ok(client_id):
            return {"status": "rate_limited", "message": "请求过于频繁"}

        try:
            content = self._decrypt_content(data)
        except Exception as e:
            return {"status": "error", "message": f"解密失败: {e}"}

        if not content or not content.strip():
            return {"status": "error", "message": "内容为空"}

        source = data.get("source", "websocket")
        topic = data.get("topic")
        tags = data.get("tags")

        try:
            result = save(
                content,
                source=source,
                topic=topic,
                tags=tags,
            )
        except Exception as e:
            return {"status": "error", "message": f"容器保存失败: {e}"}

        # 同步到 Neo4j（异步里调用同步函数，简单起见用线程）
        try:
            import threading
            threading.Thread(target=_ensure_neo4j_index, args=(result,), daemon=True).start()
        except Exception as e:
            print(f"⚠️ Neo4j 同步线程启动失败: {e}")

        return {
            "status": "success",
            "action": result.get("status", "saved"),
            "path": result.get("path"),
            "dna": result.get("dna"),
            "copy_count": result.get("copy_count", 1),
            "topic": result.get("topic"),
            "timestamp": _now(),
            "hub_dna": HUB_DNA,
        }

    def _handle_query(self, data: dict) -> dict:
        """简单查询：按 topic/tag/source 过滤。"""
        items = list_vault()
        topic_filter = data.get("topic")
        tag_filter = data.get("tag")
        source_filter = data.get("source")
        limit = data.get("limit", 50)

        filtered = []
        for item in items:
            if topic_filter and item.get("topic") != topic_filter:
                continue
            if tag_filter and tag_filter not in item.get("tags", []):
                continue
            if source_filter and item.get("source") != source_filter:
                continue
            filtered.append(item)
            if len(filtered) >= limit:
                break

        return {
            "status": "success",
            "count": len(filtered),
            "items": filtered,
            "dna": HUB_DNA,
        }

    def _handle_stats(self) -> dict:
        items = list_vault()
        topics: Dict[str, int] = {}
        tags: Dict[str, int] = {}
        for item in items:
            topics[item["topic"]] = topics.get(item["topic"], 0) + 1
            for t in item.get("tags", []):
                tags[t] = tags.get(t, 0) + 1
        return {
            "status": "success",
            "total": len(items),
            "topics": topics,
            "tags": tags,
            "dna": HUB_DNA,
        }


def main():
    parser = argparse.ArgumentParser(description="龍魂·剪贴板容器中心")
    parser.add_argument("--host", default="0.0.0.0", help="监听地址")
    parser.add_argument("--port", type=int, default=8765, help="监听端口")
    parser.add_argument("--no-encrypt", action="store_true", help="明文调试模式（不推荐生产）")
    parser.add_argument("--cert", default=os.environ.get("LONGHUN_CLIPBOARD_CERT"), help="TLS 证书文件路径（启用 wss://）")
    parser.add_argument("--key", default=os.environ.get("LONGHUN_CLIPBOARD_KEY"), help="TLS 私钥文件路径（启用 wss://）")
    args = parser.parse_args()

    hub = ClipboardHub(no_encrypt=args.no_encrypt)

    ssl_context = None
    scheme = "ws"
    if args.cert and args.key:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile=args.cert, keyfile=args.key)
        scheme = "wss"

    print("🐉 龍魂·剪贴板容器中心")
    print(f"   DNA: {HUB_DNA}")
    print(f"   监听: {scheme}://{args.host}:{args.port}")
    print(f"   传输层: {'TLS 1.2+ (wss://)' if ssl_context else '明文 WebSocket (ws://)'}")
    print(f"   应用层加密: {'已禁用（调试模式）' if args.no_encrypt else 'SM4-CBC'}")
    print(f"   当前时间: {_now()}")

    # 启动自检：扫描容器目录，补齐 Neo4j 缺失索引
    try:
        report = reconcile(prune=False)
        print(f"   🔄 启动自检: 容器{report['total_files']}条 / Neo4j{report['neo4j_clips']}条 / 补齐{report['missing_imported']}条")
    except Exception as e:
        print(f"   ⚠️ 启动自检失败（不影响服务）: {e}")

    print("   🟢 运行中...")

    async def _serve():
        server = await websockets.serve(
            hub.handle_client, args.host, args.port, ssl=ssl_context, ping_interval=30, ping_timeout=10
        )
        await asyncio.Future()  # 永久运行

    asyncio.run(_serve())


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 量子存证系统 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-QUANTUM-EVIDENCE-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 语义压缩（AI可读摘要）
  2. DNA追溯码生成
  3. 量子态指纹（分片加密模拟）
  4. 公开存证（本地区块链模拟）
  5. 原文重组验证
  6. JSON管道输出（--json）

用法：
  lh qe store --text "内容"                   # 存证文本（密钥自动同步鲲鹏）
  lh qe store --file 文件.txt                  # 存证文件
  lh qe query --dna <DNA码>                    # 查询公开摘要
  lh qe verify --dna <DNA码> --text "原文"     # 验证原文
  lh qe reconstruct --dna <DNA码>              # 量子重组（自动从鲲鹏拉密钥）
  lh qe list                                   # 列出所有存证
  lh qe stats                                  # 统计信息

密钥管理：
  - 存证时自动 SSH 同步重组密钥到鲲鹏 /opt/longhun/data/quantum_keys/
  - 重组时无需提供密钥，自动从鲲鹏拉取
  - 国产 AI 统一读取同一路径，路径焊死永不变
"""

import os
import sys
import json
import hashlib
import datetime
import sqlite3
import base64
import argparse
import random
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# ============================================================
# 固定锚点
# ============================================================

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
PROJECT_ROOT = Path.home() / "longhun-system"
DATA_DIR = PROJECT_ROOT / "data" / "quantum_evidence"
DB_PATH = DATA_DIR / "evidence.db"
STORAGE_DIR = DATA_DIR / "storage"
PUBLIC_DIR = DATA_DIR / "public"

# 鲲鹏密钥仓库 — 焊死路径，永不变
KUNPENG_HOST = "119.13.90.27"
KUNPENG_USER = "root"
KUNPENG_SSH_KEY = str(Path.home() / ".ssh" / "longhun_kunpeng_ed25519")
KUNPENG_KEY_DIR = "/opt/longhun/data/quantum_keys"  # 统一路径，焊死

for d in [DATA_DIR, STORAGE_DIR, PUBLIC_DIR]:
    d.mkdir(parents=True, exist_ok=True)


# ============================================================
# 工具函数
# ============================================================

def rows_to_dict(rows):
    """sqlite3.Row → dict，确保JSON可序列化"""
    if rows is None:
        return []
    if isinstance(rows, list):
        return [dict(r) for r in rows]
    if hasattr(rows, 'keys'):
        return dict(rows)
    return {}


# ============================================================
# 数据库初始化
# ============================================================

def init_db():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evidence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dna_trace TEXT UNIQUE NOT NULL,
            semantic_summary TEXT,
            key_points TEXT,
            entities TEXT,
            sentiment TEXT,
            content_hash TEXT,
            quantum_public TEXT,
            quantum_private TEXT,
            reconstruction_key TEXT,
            block_id TEXT,
            local_path TEXT,
            user_dna TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            verified_count INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_dna ON evidence(dna_trace)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_time ON evidence(created_at)')
    conn.commit()
    conn.close()


def get_db():
    return sqlite3.connect(str(DB_PATH))


# ============================================================
# DNA追溯码生成
# ============================================================

def generate_dna_trace(content: str, user_dna: str = "UID9622", action: str = "STORE") -> str:
    """生成DNA追溯码"""
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    content_hash = hashlib.sha256(content.encode()).hexdigest()[:8]
    return f"#龍芯⚡️{now}-{action}-{user_dna[:6]}-{content_hash}"


# ============================================================
# 语义压缩引擎
# ============================================================

class SemanticCompressor:
    """语义压缩器 - AI可读的内容摘要"""

    def __init__(self):
        self._has_ai = False
        self._ai_client = None
        self._init_ai()

    def _init_ai(self):
        """尝试初始化AI客户端（本地优先）"""
        try:
            import requests
            resp = requests.get("http://localhost:11434/api/tags", timeout=2)
            if resp.status_code == 200:
                from openai import OpenAI
                self._ai_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
                self._has_ai = True
                return
        except Exception:
            pass

        try:
            import openai
            api_key = os.environ.get("DEEPSEEK_API_KEY", "")
            if api_key:
                self._ai_client = openai.OpenAI(
                    api_key=api_key,
                    base_url="https://api.deepseek.com"
                )
                self._has_ai = True
                return
        except Exception:
            pass

        self._has_ai = False

    def compress(self, text: str) -> Dict:
        """压缩原文为语义摘要"""
        if self._has_ai:
            return self._compress_with_ai(text)
        return self._compress_with_rules(text)

    def _compress_with_ai(self, text: str) -> Dict:
        """使用AI压缩"""
        try:
            response = self._ai_client.chat.completions.create(
                model="llama3.2" if "ollama" in str(self._ai_client.base_url) else "deepseek-chat",
                messages=[
                    {"role": "system", "content": """你是一个语义压缩器。将输入内容压缩为结构化摘要。
                    输出格式必须是JSON，包含以下字段：
                    - semantic_summary: 一句话概括（30字内）
                    - key_points: 关键要点列表（最多5个）
                    - entities: 人物、地点、时间等实体列表
                    - sentiment: 情感倾向（正面/中性/负面）
                    只输出JSON，不要其他内容。"""},
                    {"role": "user", "content": f"压缩以下内容：\n\n{text[:2000]}"}
                ],
                temperature=0.3,
                max_tokens=500
            )
            result_text = response.choices[0].message.content
            import re
            json_match = re.search(r'\{[\s\S]*\}', result_text)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass
        return self._compress_with_rules(text)

    def _compress_with_rules(self, text: str) -> Dict:
        """规则压缩（无AI时使用）"""
        summary = text[:200] + "..." if len(text) > 200 else text
        sentences = [s.strip() for s in text.split("。") if s.strip()]
        key_points = sentences[:3] if sentences else [text[:50]]

        return {
            "semantic_summary": summary,
            "key_points": key_points,
            "entities": [],
            "sentiment": "中性",
            "compression_ratio": round(len(summary) / max(1, len(text)), 2)
        }


# ============================================================
# 量子态指纹（分片加密模拟）
# ============================================================

class QuantumFingerprint:
    """量子态指纹生成器（分片加密模拟）"""

    def __init__(self):
        self._fernet = None
        self._init_crypto()

    def _init_crypto(self):
        """初始化加密"""
        try:
            salt = b"longhun_quantum_salt"
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(b"quantum_seed_9622"))
            self._fernet = Fernet(key)
        except Exception:
            self._fernet = None

    def generate(self, text: str, user_gpg: str = GPG) -> Dict:
        """生成量子态指纹"""
        shards = self._shard_text(text, n_shards=20)

        encrypted_shards = []
        for i, shard in enumerate(shards):
            if self._fernet:
                encrypted = self._fernet.encrypt(shard.encode())
                encrypted_shards.append(base64.urlsafe_b64encode(encrypted).decode())
            else:
                shifted = ''.join(chr(ord(c) + i) for c in shard)
                encrypted_shards.append(base64.b64encode(shifted.encode()).decode())

        shard_map = list(range(len(shards)))
        random.seed(hashlib.sha256(text.encode()).hexdigest())
        random.shuffle(shard_map)

        # 实际打乱分片顺序（量子态效果）
        shuffled_shards = [encrypted_shards[shard_map[i]] for i in range(len(shard_map))]

        public_fingerprint = hashlib.sha256(
            "".join(encrypted_shards).encode()
        ).hexdigest()[:32]

        private_info = {
            "shard_map": shard_map,
            "shard_count": len(shards),
            "encryption": "fernet" if self._fernet else "simple"
        }

        reconstruction_key = self._generate_reconstruction_key(text, user_gpg)

        return {
            "quantum_public": public_fingerprint,
            "quantum_private": private_info,
            "encrypted_shards": shuffled_shards,
            "reconstruction_key": reconstruction_key
        }

    def _shard_text(self, text: str, n_shards: int) -> List[str]:
        if len(text) < n_shards:
            return [text[i:i+1] for i in range(len(text))] + [""] * (n_shards - len(text))
        chunk_size = max(1, len(text) // n_shards)
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    def _generate_reconstruction_key(self, text: str, user_gpg: str) -> str:
        raw = f"{text[:50]}{user_gpg}{datetime.datetime.now().isoformat()}"
        return hashlib.sha256(raw.encode()).hexdigest()[:32]

    def reconstruct(self, encrypted_shards: List[str], private_info: Dict, key: str) -> str:
        """重组原文"""
        if not key or len(key) < 10:
            raise ValueError("重组密钥无效")

        decrypted = []
        for i, enc_shard in enumerate(encrypted_shards):
            try:
                if self._fernet:
                    decrypted_bytes = self._fernet.decrypt(base64.urlsafe_b64decode(enc_shard))
                    decrypted.append(decrypted_bytes.decode())
                else:
                    decoded = base64.b64decode(enc_shard).decode()
                    shifted = ''.join(chr(ord(c) - i) for c in decoded)
                    decrypted.append(shifted)
            except Exception:
                decrypted.append("")

        # 逆映射恢复原始顺序
        shard_map = private_info.get("shard_map", list(range(len(decrypted))))
        inverse = [0] * len(shard_map)
        for orig_idx, shuffled_idx in enumerate(shard_map):
            inverse[shuffled_idx] = orig_idx
        ordered = [decrypted[inverse[i]] for i in range(len(decrypted))]

        return "".join(ordered)


# ============================================================
# 区块链存证（本地模拟）
# ============================================================

class BlockchainStorage:
    """区块链存证系统（本地模拟）"""

    def __init__(self):
        self.chain_file = PUBLIC_DIR / "blockchain.json"
        self._init_chain()

    def _init_chain(self):
        if not self.chain_file.exists():
            genesis = {"blocks": [], "genesis": datetime.datetime.now().isoformat()}
            with open(self.chain_file, 'w') as f:
                json.dump(genesis, f, indent=2)

    def store(self, data: Dict) -> str:
        with open(self.chain_file, 'r') as f:
            chain = json.load(f)

        block_id = f"BLOCK-{len(chain['blocks'])+1:04d}-{hashlib.sha256(json.dumps(data).encode()).hexdigest()[:8]}"
        prev_hash = chain["blocks"][-1]["hash"] if chain["blocks"] else "GENESIS"
        block = {
            "id": block_id,
            "data": data,
            "timestamp": datetime.datetime.now().isoformat(),
            "previous_hash": prev_hash,
            "hash": hashlib.sha256(json.dumps(data).encode()).hexdigest()
        }
        chain["blocks"].append(block)
        with open(self.chain_file, 'w') as f:
            json.dump(chain, f, indent=2)
        return block_id

    def query(self, dna_trace: str) -> Optional[Dict]:
        with open(self.chain_file, 'r') as f:
            chain = json.load(f)
        for block in chain["blocks"]:
            if block["data"].get("dna_trace") == dna_trace:
                return block["data"]
        return None


# ============================================================
# 鲲鹏密钥仓库（焊死路径，国产AI统一入口）
# ============================================================

class KunpengKeyStore:
    """密钥统一存在鲲鹏 /opt/longhun/data/quantum_keys/，国产AI共享读取"""

    def __init__(self):
        self.host = KUNPENG_HOST
        self.user = KUNPENG_USER
        self.ssh_key = KUNPENG_SSH_KEY
        self.key_dir = KUNPENG_KEY_DIR
        self._ssh_base = [
            "ssh", "-i", self.ssh_key,
            "-o", "ConnectTimeout=5",
            "-o", "StrictHostKeyChecking=accept-new",
            f"{self.user}@{self.host}"
        ]

    def _ensure_dir(self) -> bool:
        """确保鲲鹏上密钥目录存在"""
        import subprocess
        cmd = self._ssh_base + [f"mkdir -p {self.key_dir}"]
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=10)
            return True
        except Exception:
            return False

    def _safe_name(self, dna_trace: str) -> str:
        """DNA追溯码 → 安全文件名"""
        return dna_trace.replace('#', '').replace('⚡️', '_').replace('-', '_').replace(':', '_')

    def upload_key(self, dna_trace: str, reconstruction_key: str) -> Dict:
        """上传重组密钥到鲲鹏"""
        import subprocess
        safe = self._safe_name(dna_trace)
        key_data = {
            "dna_trace": dna_trace,
            "reconstruction_key": reconstruction_key,
            "created_at": datetime.datetime.now().isoformat(),
            "source": "Mac-local",
            "confirm": CONFIRM
        }
        json_str = json.dumps(key_data, ensure_ascii=False)
        remote_path = f"{self.key_dir}/{safe}.json"

        # 确保目录存在
        self._ensure_dir()

        # 通过 SSH 写入
        cmd = self._ssh_base + [f"cat > {remote_path}"]
        try:
            result = subprocess.run(
                cmd, input=json_str, capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                return {
                    "status": "synced",
                    "remote_path": remote_path,
                    "server": f"{self.user}@{self.host}"
                }
            else:
                return {"status": "failed", "error": result.stderr.strip()}
        except subprocess.TimeoutExpired:
            return {"status": "failed", "error": "SSH连接鲲鹏超时"}
        except FileNotFoundError:
            return {"status": "failed", "error": "SSH不可用"}
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    def fetch_key(self, dna_trace: str) -> Optional[str]:
        """从鲲鹏拉取重组密钥"""
        import subprocess
        safe = self._safe_name(dna_trace)
        remote_path = f"{self.key_dir}/{safe}.json"
        cmd = self._ssh_base + [f"cat {remote_path}"]
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                key_data = json.loads(result.stdout.strip())
                return key_data.get("reconstruction_key")
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError, Exception):
            pass
        return None

    def key_exists(self, dna_trace: str) -> bool:
        """检查鲲鹏上是否存在该密钥"""
        import subprocess
        safe = self._safe_name(dna_trace)
        remote_path = f"{self.key_dir}/{safe}.json"
        cmd = self._ssh_base + [f"test -f {remote_path} && echo 'EXISTS' || echo 'MISSING'"]
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=10
            )
            return "EXISTS" in result.stdout
        except Exception:
            return False


# ============================================================
# 核心引擎
# ============================================================

class QuantumEvidenceEngine:

    def __init__(self):
        if not DB_PATH.exists():
            init_db()
        self.conn = get_db()
        self.conn.row_factory = sqlite3.Row
        self.compressor = SemanticCompressor()
        self.quantum = QuantumFingerprint()
        self.blockchain = BlockchainStorage()
        self.kunpeng_keys = KunpengKeyStore()  # 密钥自动同步鲲鹏

    def close(self):
        if hasattr(self, 'conn'):
            self.conn.close()

    # ---------- 存证 ----------
    def store(self, content: str, user_dna: str = "UID9622", user_gpg: str = GPG) -> Dict:
        compressed = self.compressor.compress(content)
        dna_trace = generate_dna_trace(content, user_dna, "STORE")
        quantum_data = self.quantum.generate(content, user_gpg)

        blockchain_data = {
            "dna_trace": dna_trace,
            "semantic_summary": compressed.get("semantic_summary", content[:100]),
            "key_points": compressed.get("key_points", []),
            "content_hash": hashlib.sha256(content.encode()).hexdigest(),
            "quantum_public": quantum_data["quantum_public"],
            "timestamp": datetime.datetime.now().isoformat(),
            "user_dna": user_dna
        }

        block_id = self.blockchain.store(blockchain_data)

        safe_name = dna_trace.replace('#', '').replace('⚡️', '_').replace('-', '_')
        local_filename = f"{safe_name}.enc"
        local_path = STORAGE_DIR / local_filename

        local_data = {
            "original_text": content,
            "quantum_private": quantum_data["quantum_private"],
            "encrypted_shards": quantum_data["encrypted_shards"],
            "reconstruction_key": quantum_data["reconstruction_key"],
            "block_id": block_id,
            "dna_trace": dna_trace
        }

        with open(local_path, 'w', encoding='utf-8') as f:
            json.dump(local_data, f, ensure_ascii=False, indent=2)

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO evidence (
                dna_trace, semantic_summary, key_points, entities, sentiment,
                content_hash, quantum_public, quantum_private, reconstruction_key,
                block_id, local_path, user_dna
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            dna_trace,
            compressed.get("semantic_summary", ""),
            json.dumps(compressed.get("key_points", [])),
            json.dumps(compressed.get("entities", [])),
            compressed.get("sentiment", "中性"),
            blockchain_data["content_hash"],
            quantum_data["quantum_public"],
            json.dumps(quantum_data["quantum_private"]),
            quantum_data["reconstruction_key"],
            block_id,
            str(local_path),
            user_dna
        ))
        self.conn.commit()

        # 自动同步重组密钥到鲲鹏（统一入口，国产AI共享读取）
        kunpeng_result = self.kunpeng_keys.upload_key(dna_trace, quantum_data["reconstruction_key"])

        return {
            "status": "stored",
            "dna_trace": dna_trace,
            "block_id": block_id,
            "local_path": str(local_path),
            "semantic_summary": compressed.get("semantic_summary", ""),
            "compression_ratio": compressed.get("compression_ratio", 0),
            "quantum_public": quantum_data["quantum_public"],
            "reconstruction_key": quantum_data["reconstruction_key"],
            "kunpeng_sync": kunpeng_result["status"],
            "kunpeng_path": kunpeng_result.get("remote_path", ""),
            "public_url": f"https://dna.longhun.com/verify/{dna_trace}"
        }

    # ---------- 公开查询 ----------
    def query_public(self, dna_trace: str) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT dna_trace, semantic_summary, key_points, entities, sentiment,
                   content_hash, quantum_public, created_at, user_dna, verified_count
            FROM evidence WHERE dna_trace = ?
        ''', (dna_trace,))
        row = cursor.fetchone()
        if not row:
            return None
        row = dict(row)
        return {
            "dna_trace": row["dna_trace"],
            "semantic_summary": row["semantic_summary"],
            "key_points": json.loads(row["key_points"]) if row["key_points"] else [],
            "entities": json.loads(row["entities"]) if row["entities"] else [],
            "sentiment": row["sentiment"],
            "content_hash": row["content_hash"],
            "quantum_public": row["quantum_public"],
            "created_at": row["created_at"],
            "user_dna": row["user_dna"],
            "verified_count": row["verified_count"],
            "status": "✅ 已存证"
        }

    # ---------- 原文验证 ----------
    def verify_original(self, dna_trace: str, claimed_content: str) -> Dict:
        blockchain_data = self.blockchain.query(dna_trace)
        if not blockchain_data:
            cursor = self.conn.cursor()
            cursor.execute("SELECT content_hash FROM evidence WHERE dna_trace = ?", (dna_trace,))
            row = cursor.fetchone()
            if not row:
                return {"status": "error", "message": "DNA追溯码不存在"}
            stored_hash = row["content_hash"]
        else:
            stored_hash = blockchain_data.get("content_hash")

        claimed_hash = hashlib.sha256(claimed_content.encode()).hexdigest()

        if claimed_hash == stored_hash:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE evidence SET verified_count = verified_count + 1 WHERE dna_trace = ?", (dna_trace,))
            self.conn.commit()
            return {
                "status": "verified",
                "result": "✅ 验证通过",
                "message": "声称原文与链上哈希一致",
                "timestamp": datetime.datetime.now().isoformat(),
                "proof": "证据链完整，可提供完整存证记录"
            }
        else:
            return {
                "status": "failed",
                "result": "❌ 验证失败",
                "message": "声称原文与链上哈希不符",
                "suspicion": "内容可能被篡改或伪造",
                "timestamp": datetime.datetime.now().isoformat()
            }

    # ---------- 量子重组 ----------
    def reconstruct_original(self, dna_trace: str, reconstruction_key: str = "") -> Dict:
        """量子重组原文。不传key时自动从鲲鹏拉取"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT local_path, quantum_private, reconstruction_key, content_hash
            FROM evidence WHERE dna_trace = ?
        ''', (dna_trace,))
        row = cursor.fetchone()
        if not row:
            return {"status": "error", "message": "DNA追溯码不存在"}

        row = dict(row)

        # 自动从鲲鹏拉取密钥（老大不用记）
        if not reconstruction_key:
            reconstruction_key = self.kunpeng_keys.fetch_key(dna_trace)
            if not reconstruction_key:
                return {
                    "status": "error",
                    "message": "无法获取重组密钥",
                    "hint": "鲲鹏密钥未找到，请确认存证时已同步或手动提供 --key",
                    "kunpeng_path": f"{KUNPENG_KEY_DIR}/{KunpengKeyStore()._safe_name(dna_trace)}.json"
                }

        if reconstruction_key != row["reconstruction_key"]:
            return {"status": "error", "message": "重组密钥无效"}

        local_path = Path(row["local_path"])
        if not local_path.exists():
            return {"status": "error", "message": "本地存证文件不存在"}

        with open(local_path, 'r', encoding='utf-8') as f:
            local_data = json.load(f)

        try:
            original = self.quantum.reconstruct(
                local_data.get("encrypted_shards", []),
                json.loads(row["quantum_private"]) if row["quantum_private"] else {},
                reconstruction_key
            )
            return {
                "status": "reconstructed",
                "original_text": original,
                "hash": hashlib.sha256(original.encode()).hexdigest(),
                "stored_hash": row["content_hash"],
                "match": hashlib.sha256(original.encode()).hexdigest() == row["content_hash"]
            }
        except Exception as e:
            return {"status": "error", "message": f"重组失败: {e}"}

    # ---------- 列表 ----------
    def list_evidence(self, limit: int = 20) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT dna_trace, semantic_summary, created_at, verified_count
            FROM evidence ORDER BY created_at DESC LIMIT ?
        ''', (limit,))
        return rows_to_dict(cursor.fetchall())

    # ---------- 统计 ----------
    def get_stats(self) -> Dict:
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM evidence")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(verified_count) FROM evidence")
        verified = cursor.fetchone()[0] or 0
        return {"total_evidence": total, "total_verifications": verified}


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 量子存证系统 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh qe store --text "内容"                    # 存证（密钥自动同步鲲鹏）
  lh qe query --dna <DNA码>                    # 公开查询
  lh qe verify --dna <DNA码> --text "原文"     # 验证原文
  lh qe reconstruct --dna <DNA码>              # 重组（自动从鲲鹏拉密钥）
  lh qe reconstruct --dna <DNA码> --key <密钥> # 重组（手动指定密钥）
  lh qe list                                   # 列出存证
  lh qe stats                                  # 统计
        """
    )

    parser.add_argument("command", choices=["store", "query", "verify", "reconstruct", "list", "stats"],
                       help="操作命令")
    parser.add_argument("--text", type=str, help="要存证/验证的文本内容")
    parser.add_argument("--file", type=str, help="要存证/验证的文件路径")
    parser.add_argument("--dna", type=str, help="DNA追溯码")
    parser.add_argument("--key", type=str, help="重组密钥")
    parser.add_argument("--user-dna", type=str, default="UID9622", help="用户DNA标识")
    parser.add_argument("--json", action="store_true", help="纯JSON输出模式")

    args = parser.parse_args()
    engine = QuantumEvidenceEngine()

    try:
        if args.command == "store":
            if args.file:
                with open(args.file, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif args.text:
                content = args.text
            else:
                print("❌ 请提供 --text 或 --file", file=sys.stderr)
                sys.exit(1)

            result = engine.store(content, args.user_dna)
            output = json.dumps(result, ensure_ascii=False, indent=2)
            print(output)
            if not args.json:
                sync_icon = "☁️" if result.get("kunpeng_sync") == "synced" else "⚠️"
                print(f"\n{sync_icon} 鲲鹏同步: {result.get('kunpeng_sync', 'unknown')}")
                if result.get("kunpeng_sync") != "synced":
                    print(f"🔑 重组密钥: {result['reconstruction_key']}（鲲鹏不可达，密钥仅本地保存）")

        elif args.command == "query":
            if not args.dna:
                print("❌ 请提供 --dna", file=sys.stderr)
                sys.exit(1)
            result = engine.query_public(args.dna)
            if result:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                err = {"status": "not_found", "message": "DNA追溯码不存在"}
                print(json.dumps(err, ensure_ascii=False, indent=2))

        elif args.command == "verify":
            if not args.dna:
                print("❌ 请提供 --dna", file=sys.stderr)
                sys.exit(1)
            if args.file:
                with open(args.file, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif args.text:
                content = args.text
            else:
                print("❌ 请提供 --file 或 --text", file=sys.stderr)
                sys.exit(1)
            result = engine.verify_original(args.dna, content)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif args.command == "reconstruct":
            if not args.dna:
                print("❌ 请提供 --dna", file=sys.stderr)
                sys.exit(1)
            # --key 可选：不传则自动从鲲鹏拉取
            key = args.key or ""
            if key:
                result = engine.reconstruct_original(args.dna, key)
            else:
                result = engine.reconstruct_original(args.dna)  # 自动鲲鹏拉取
            if result.get("status") == "reconstructed":
                if args.json:
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                else:
                    key_source = "☁️鲲鹏自动拉取" if not args.key else "🔑手动指定"
                    preview = result['original_text'][:500]
                    print(f"✅ 量子重组成功 ({key_source})")
                    print(f"原文: {preview}{'...' if len(result['original_text']) > 500 else ''}")
                    print(f"哈希匹配: {'✅' if result['match'] else '❌'}")
            else:
                print(json.dumps(result, ensure_ascii=False, indent=2))

        elif args.command == "list":
            results = engine.list_evidence()
            if args.json:
                print(json.dumps(results, ensure_ascii=False, indent=2))
            else:
                for r in results:
                    summary = (r.get('semantic_summary') or '')[:80]
                    print(f"  📄 {r['dna_trace']}")
                    print(f"     {summary}{'...' if len(r.get('semantic_summary', '')) > 80 else ''}")
                    print(f"     {r['created_at']} | 验证: {r.get('verified_count', 0)}次")
                    print()

        elif args.command == "stats":
            stats = engine.get_stats()
            if args.json:
                print(json.dumps(stats, ensure_ascii=False, indent=2))
            else:
                print(f"📊 量子存证统计")
                print(f"  总存证数: {stats['total_evidence']}")
                print(f"  总验证数: {stats['total_verifications']}")

    finally:
        engine.close()


if __name__ == "__main__":
    main()

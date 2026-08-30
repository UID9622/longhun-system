# DNA: #龍芯⚡️2026-08-25-HASH-REGISTRY-M73-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""M73 哈希产权引擎 · 截图 SHA-256 + DNA 绑定 + Merkle 链式注册表。

语义: 每次渲染截图落盘即自动登记产权哈希。注册表 append-only，
链式指纹防篡改：chain_hash = SHA256(prev + seq + sha256 + dna)。
验证接口用于溯源归属（谁在何时产出、绑定哪条 DNA）。
"""

import datetime
import hashlib
import json
import threading
from pathlib import Path
from typing import Dict, Optional


class HashRegistry:
    """M73 哈希产权注册表（append-only · Merkle 链）。"""

    VERSION = "1.0.0"
    UID = "UID9622"

    def __init__(self, path: str = None):
        self.path = Path(path) if path else Path("data/renders/hash_registry.jsonl")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Lock 即可：register 内部不嵌套加锁（与七因子引擎 RLock 教训不同）
        self._lock = threading.Lock()
        self._cache: Dict[str, dict] = {}
        self._load()

    # ── 内部 ──

    def _load(self) -> None:
        if not self.path.exists():
            return
        with self._lock:
            for line in self.path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    self._cache[rec.get("sha256", "")] = rec
                except (json.JSONDecodeError, KeyError):
                    continue

    def _last_chain(self) -> str:
        """最后一条记录的 chain_hash（链尾），空则用创始根。"""
        if not self.path.exists():
            return "GENESIS-龍芯"
        last = None
        for line in self.path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                last = json.loads(line)
            except json.JSONDecodeError:
                continue
        return last.get("chain_hash", "GENESIS-龍芯") if last else "GENESIS-龍芯"

    # ── 注册 ──

    def register(self, sha256: str, dna: str, url: str = "",
                 platform: str = "web", extra: dict = None) -> dict:
        """登记一条产权哈希。sha256 可为 hex str 或 bytes 的 sha256.digest()。

        返回注册记录（含 seq/ts/prev/chain_hash）。
        """
        if isinstance(sha256, bytes):
            sha256 = sha256.hex()
        sha256 = sha256.lower()
        if len(sha256) != 64:
            raise ValueError(f"sha256 长度异常: {len(sha256)}")
        # 幂等：已注册直接返回（不重复记账）
        with self._lock:
            exist = self._cache.get(sha256)
            if exist:
                return exist
            prev = self._last_chain()
            seq = len(self._cache) + 1
            rec = {
                "seq": seq,
                "ts": datetime.datetime.now().isoformat(timespec="seconds"),
                "sha256": sha256,
                "dna": dna or "",
                "url": url or "",
                "platform": platform or "web",
                "extra": extra or {},
                "prev": prev,
            }
            chain_input = f"{prev}|{seq}|{sha256}|{rec['dna']}"
            rec["chain_hash"] = hashlib.sha256(chain_input.encode("utf-8")).hexdigest()
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            self._cache[sha256] = rec
            return rec

    def register_file(self, path: str, dna: str, url: str = "",
                      platform: str = "web") -> dict:
        """对磁盘文件计算 SHA-256 并注册。"""
        p = Path(path)
        if not p.is_file():
            raise FileNotFoundError(f"文件不存在: {p}")
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return self.register(h.hexdigest(), dna, url, platform, {"path": str(p)})

    # ── 验证/查询 ──

    def verify(self, sha256: str) -> Optional[dict]:
        """按 sha256 查注册记录；未登记返回 None。"""
        if isinstance(sha256, bytes):
            sha256 = sha256.hex()
        return self._cache.get(sha256.lower())

    def verify_dna(self, dna: str) -> list:
        """按 DNA 查全部关联记录。"""
        return [r for r in self._cache.values() if r.get("dna") == dna]

    def stats(self) -> dict:
        with self._lock:
            return {
                "count": len(self._cache),
                "file": str(self.path),
                "last_chain": self._last_chain(),
            }

    def export(self) -> list:
        return list(self._cache.values())

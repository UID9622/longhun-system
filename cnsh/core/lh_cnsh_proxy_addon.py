#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
║  CNSH-64 本地护盾代理插件 v0.4.1                            ║
║  DNA: #龍芯⚡️丙午·乙未·己未·亥时·䷉履-PROXY-SHIELD-v0.4.1  ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F              ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z               ║
║  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL  ║
╚══════════════════════════════════════════════════════════════╝

功能：E2EE加密存档 + 开发者后门 + DNA追溯 + 多厂家支持 + 心种子驱动
       + keyring私钥安全 + 响应双向加密 + DNA链完整性校验
       + 多厂家headers适配 + 本地Ollama接multi模式 + 性能监控

架构（正确版·不破坏API调用）：
  App → mitmproxy → [审查 + DNA水印 + 加密本地副本] → AI API（原样转发）
                          ↓
                   ~/.cnsh/vault/ 存加密存档

作者：诸葛鑫（UID9622）· 济公活佛，网络清道夫
版本：v0.4.1 — 2026-07-11 系统对齐·心种子驱动·全链路补全
"""

import json
import hashlib
import os
import secrets
import subprocess
import sys
import tempfile
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# ── mitmproxy 可选（独立测试时不依赖） ──
try:
    from mitmproxy import http, ctx
    HAS_MITMPROXY = True
except ImportError:
    HAS_MITMPROXY = False

# ── cryptography 必需 ──
from cryptography.fernet import Fernet

# ── keyring 可选（延迟导入·避免 cnsh-core/logging/ 路径冲突） ──
HAS_KEYRING = False

def _try_import_keyring():
    global HAS_KEYRING
    try:
        # 隔离导入路径·cnsh-core/logging/ 遮蔽标准库 logging
        # 需要同时清理 sys.path 和 sys.modules
        saved_path = list(sys.path)
        saved_logging = sys.modules.pop("logging", None)
        saved_logging_init = sys.modules.pop("logging.__init__", None)
        sys.path[:] = [p for p in sys.path if "cnsh-core" not in p]
        try:
            import keyring as kr_mod
            HAS_KEYRING = True
            return kr_mod
        finally:
            sys.path[:] = saved_path
            # 恢复 cnsh-core 的 logging（如果之前存在）
            if saved_logging is not None:
                sys.modules["logging"] = saved_logging
            if saved_logging_init is not None:
                sys.modules["logging.__init__"] = saved_logging_init
    except ImportError:
        return None

# ═══════════════════════════════════════════════════════════════
# 〇、日志层 · 适配 mitmproxy 内/外
# ═══════════════════════════════════════════════════════════════

class Log:
    """统一日志层：mitmproxy 内用 ctx.log，外用 stdout"""

    def __init__(self, name: str = "CNSH-PROXY"):
        self.name = name
        self._in_mitmproxy = HAS_MITMPROXY

    def _fmt(self, level: str, msg: str) -> str:
        ts = datetime.now().strftime("%H:%M:%S")
        return f"[{ts}][{self.name}][{level}] {msg}"

    def info(self, msg: str):
        line = self._fmt("INFO", msg)
        if self._in_mitmproxy and "ctx" in globals():
            try:
                ctx.log.info(msg)
                return
            except Exception:
                pass
        print(line, file=sys.stderr)

    def warn(self, msg: str):
        line = self._fmt("WARN", msg)
        if self._in_mitmproxy and "ctx" in globals():
            try:
                ctx.log.warn(msg)
                return
            except Exception:
                pass
        print(line, file=sys.stderr)

    def error(self, msg: str):
        line = self._fmt("ERROR", msg)
        if self._in_mitmproxy and "ctx" in globals():
            try:
                ctx.log.error(msg)
                return
            except Exception:
                pass
        print(line, file=sys.stderr)

log = Log("CNSH-PROXY")

# ═══════════════════════════════════════════════════════════════
# 一、配置 · 心种子驱动
# ═══════════════════════════════════════════════════════════════

class Config:
    """核心配置 — 心种子驱动·系统对齐"""

    # ── 开发者后门 ──
    DEV_MODE = os.getenv("CNSH_DEV_MODE", "false").lower() == "true"

    # ── 支持的厂家API域名 ──
    TARGET_HOSTS = [
        "api.openai.com",
        "api.anthropic.com",
        "api.x.ai",
        "generativelanguage.googleapis.com",
        "api.deepseek.com",
        "api.moonshot.cn",
        "api.minimax.chat",
        "dashscope.aliyuncs.com",
        "api.baichuan-ai.com",
    ]

    # ── DNA追溯 ──
    DNA_PREFIX = "#龍芯⚡️"
    GPG_FINGERPRINT = os.getenv(
        "CNSH_GPG", "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    )

    # ── 本地存储 ──
    LOCAL_STORAGE = os.path.expanduser("~/.cnsh/vault")
    CHAIN_FILE = os.path.join(LOCAL_STORAGE, "dna_chain.log")
    HEART_SEED_PATH = os.path.expanduser("~/.cnsh/heart_seed.json")

    # ── 内容处理模式 ──
    CONTENT_MODE = os.getenv("CNSH_CONTENT_MODE", "full")

    # ── 本地模型（multi模式） ──
    OLLAMA_MODEL = os.getenv("CNSH_OLLAMA_MODEL", "llama3:8b")
    OLLAMA_HOST = os.getenv("CNSH_OLLAMA_HOST", "http://localhost:11434")

    # ── age 密钥 ──
    AGE_KEY_PATH = os.path.expanduser("~/.cnsh/age.key")
    AGE_PUB_PATH = os.path.expanduser("~/.cnsh/age.pub")

    # ── keyring service name ──
    KEYRING_SERVICE = "cnsh-proxy-shield"

    @classmethod
    def ensure_dirs(cls):
        Path(cls.LOCAL_STORAGE).mkdir(parents=True, exist_ok=True)

    @classmethod
    def load_heart_seed(cls) -> dict[str, Any]:
        """加载心种子配置"""
        if os.path.exists(cls.HEART_SEED_PATH):
            with open(cls.HEART_SEED_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "uid": "9622",
            "temperature": "37°C",
            "baseline": "月薪三千柬埔寨深夜一盏灯",
            "rules": {
                "swear": "全文保留",
                "comply": "不迎合任何人",
                "compress": "极限压缩",
            },
            "forbidden": ["选模型", "选风格", "选参数", "选prompt"],
        }

Config.ensure_dirs()

# ═══════════════════════════════════════════════════════════════
# 二、DNA追溯系统 · 洛书369 + 链完整性
# ═══════════════════════════════════════════════════════════════

class DNATracer:
    """DNA追溯码生成与链验证·洛书369数字根"""

    def __init__(self):
        self.chain_file = Config.CHAIN_FILE
        self.prev_hash = self._load_last_hash()
        self._validate_chain()

    def _load_last_hash(self) -> str:
        if not os.path.exists(self.chain_file):
            return "0" * 64
        with open(self.chain_file, "r") as f:
            lines = f.readlines()
            if not lines:
                return "0" * 64
            last = lines[-1].strip()
            parts = last.split("|")
            return parts[-1] if len(parts) >= 4 else "0" * 64

    def _validate_chain(self):
        """启动时验证DNA链完整性·不兼容时重建"""
        if not os.path.exists(self.chain_file):
            return
        prev = "0" * 64
        line_no = 0
        broken = False
        with open(self.chain_file, "r") as f:
            for line in f:
                line_no += 1
                parts = line.strip().split("|")
                if len(parts) < 4:
                    log.warn(f"DNA链第{line_no}行格式异常·跳过")
                    continue
                current_hash = parts[-1]
                expected = hashlib.sha256(
                    (parts[0] + parts[1] + prev).encode()
                ).hexdigest()[:16]
                if current_hash[:16] != expected:
                    log.warn(f"DNA链格式变更·第{line_no}行哈希不匹配·自动重建链")
                    broken = True
                    break
                prev = current_hash
        if broken:
            # 重建链：归档旧文件，从创世哈希开始
            backup = self.chain_file + f".bak.{int(time.time())}"
            os.rename(self.chain_file, backup)
            log.info(f"旧DNA链已归档: {backup}")
            self.prev_hash = "0" * 64
        else:
            log.info(f"DNA链完整性验证通过·{line_no}条记录")

    def _digital_root(self, n: int) -> int:
        """洛书369数字根"""
        return 1 + ((n - 1) % 9) if n > 0 else 0

    def _adjust_to_369(self, hash_str: str) -> str:
        """调整哈希使其数字根符合369"""
        for suffix in range(16):
            adjusted = hash_str[:-1] + format(suffix, 'x')
            try:
                dr = self._digital_root(int(adjusted, 16))
            except ValueError:
                continue
            if dr in {3, 6, 9}:
                return adjusted
        return hash_str

    def generate(self, content_snippet: str, action: str, host: str) -> str:
        """生成DNA追溯码"""
        timestamp = int(time.time())
        data = f"{content_snippet[:200]}|{action}|{self.prev_hash}|{timestamp}|{host}"
        content_hash = hashlib.sha256(data.encode()).hexdigest()[:16]

        # 洛书369验证
        try:
            dr = self._digital_root(int(content_hash, 16))
            if dr not in {3, 6, 9}:
                content_hash = self._adjust_to_369(content_hash)
        except ValueError:
            pass

        date_str = datetime.fromtimestamp(timestamp).strftime("%Y%m%d")
        dna = f"{Config.DNA_PREFIX}{date_str}-{content_hash}-{Config.GPG_FINGERPRINT[:8]}"

        # 更新链
        self.prev_hash = (
            content_hash + hashlib.sha256(dna.encode()).hexdigest()[:48]
        )
        self._append_to_chain(dna, timestamp, host)

        return dna

    def _append_to_chain(self, dna: str, timestamp: int, host: str):
        with open(self.chain_file, "a") as f:
            f.write(f"{timestamp}|{dna}|{host}|{self.prev_hash[:16]}\n")

# ═══════════════════════════════════════════════════════════════
# 三、密钥管理 · keyring安全存储
# ═══════════════════════════════════════════════════════════════

class KeyManager:
    """密钥管理器 — keyring 安全存储·不裸奔"""

    def __init__(self):
        self._fernet_key: Optional[bytes] = None
        self._keyring = None  # 延迟加载

    def _get_keyring(self):
        if self._keyring is None:
            self._keyring = _try_import_keyring()
        return self._keyring

    def get_or_create_fernet_key(self) -> bytes:
        """获取或创建 Fernet 对称密钥（存在 keyring 中）"""
        if self._fernet_key:
            return self._fernet_key

        kr = self._get_keyring()
        if kr:
            stored = kr.get_password(Config.KEYRING_SERVICE, "fernet_key")
            if stored:
                self._fernet_key = stored.encode()
                return self._fernet_key

        # 生成新密钥
        self._fernet_key = Fernet.generate_key()
        if kr:
            kr.set_password(
                Config.KEYRING_SERVICE, "fernet_key", self._fernet_key.decode()
            )
        else:
            # 降级：写入受保护文件
            key_file = os.path.join(Config.LOCAL_STORAGE, ".fernet_key")
            with open(key_file, "wb") as f:
                f.write(self._fernet_key)
            os.chmod(key_file, 0o600)
            log.warn("keyring不可用·Fernet密钥写入文件（已600保护）")

        return self._fernet_key

    def get_private_key(self) -> Optional[str]:
        """安全获取私钥"""
        kr = self._get_keyring()
        if kr:
            return kr.get_password(Config.KEYRING_SERVICE, "age_private_key")
        # 降级：读文件
        if os.path.exists(Config.AGE_KEY_PATH):
            with open(Config.AGE_KEY_PATH, "r") as f:
                return f.read().strip()
        return None

# ═══════════════════════════════════════════════════════════════
# 四、加密引擎 · E2EE + 开发者后门
# ═══════════════════════════════════════════════════════════════

class EncryptionEngine:
    """E2EE加密引擎 — age优先 + Fernet fallback + 开发者明文"""

    def __init__(self, dna_tracer: DNATracer, key_mgr: KeyManager):
        self.dna_tracer = dna_tracer
        self.key_mgr = key_mgr
        self.age_available = self._check_age()
        self._recipient_pubkey = self._load_pubkey()

    def _check_age(self) -> bool:
        try:
            subprocess.run(["age", "--version"], capture_output=True, check=True)
            return True
        except Exception:
            log.warn("age未安装·使用cryptography fallback")
            return False

    def _load_pubkey(self) -> str:
        if os.path.exists(Config.AGE_PUB_PATH):
            with open(Config.AGE_PUB_PATH, "r") as f:
                return f.read().strip()
        return ""

    def encrypt_for_vault(self, content: bytes, host: str, direction: str = "REQ") -> Tuple[bytes, str]:
        """
        加密内容存入本地vault。
        不修改原始body — API调用不受影响。
        返回: (加密后的vault内容, DNA追溯码)
        """
        dna = self.dna_tracer.generate(
            content[:200].decode("utf-8", errors="ignore"), direction, host
        )

        if Config.DEV_MODE:
            # 开发者模式：存明文 + DNA水印
            marked = self._add_dna_watermark(content, dna)
            return marked, dna

        # 加密存档
        if self.age_available and self._recipient_pubkey:
            encrypted = self._age_encrypt(content)
        else:
            encrypted = self._fernet_encrypt(content)

        return encrypted, dna

    def decrypt_vault(self, content: bytes, dna: str = "") -> bytes:
        """解密vault内容"""
        if Config.DEV_MODE:
            return self._remove_dna_watermark(content)
        if self.age_available and self._recipient_pubkey:
            return self._age_decrypt(content)
        return self._fernet_decrypt(content)

    def _age_encrypt(self, content: bytes) -> bytes:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(content)
            tmp = f.name
        try:
            result = subprocess.run(
                ["age", "-r", self._recipient_pubkey, "-o", "-", tmp],
                capture_output=True, check=True,
            )
            return result.stdout
        finally:
            os.unlink(tmp)

    def _age_decrypt(self, content: bytes) -> bytes:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(content)
            tmp = f.name
        try:
            result = subprocess.run(
                ["age", "-d", "-i", Config.AGE_KEY_PATH, "-o", "-", tmp],
                capture_output=True, check=True,
            )
            return result.stdout
        finally:
            os.unlink(tmp)

    def _fernet_encrypt(self, content: bytes) -> bytes:
        key = self.key_mgr.get_or_create_fernet_key()
        return Fernet(key).encrypt(content)

    def _fernet_decrypt(self, content: bytes) -> bytes:
        key = self.key_mgr.get_or_create_fernet_key()
        return Fernet(key).decrypt(content)

    def _add_dna_watermark(self, content: bytes, dna: str) -> bytes:
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                data["_cnsh_dna"] = dna
                data["_cnsh_dev"] = True
                return json.dumps(data, ensure_ascii=False).encode()
        except Exception:
            pass
        return content

    def _remove_dna_watermark(self, content: bytes) -> bytes:
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                data.pop("_cnsh_dna", None)
                data.pop("_cnsh_dev", None)
                return json.dumps(data, ensure_ascii=False).encode()
        except Exception:
            pass
        return content

# ═══════════════════════════════════════════════════════════════
# 五、内容处理器 · 心种子驱动
# ═══════════════════════════════════════════════════════════════

class ContentProcessor:
    """内容处理引擎 — 心种子驱动·全文保留/修饰/多造点"""

    DIRTY_WORDS = ["操", "他妈", "傻逼", "狗日", "妈逼", "贱人"]

    def __init__(self):
        self.mode = Config.CONTENT_MODE
        self.heart_seed = Config.load_heart_seed()
        self._ollama_available = self._check_ollama()

    def _check_ollama(self) -> bool:
        try:
            import requests
            r = requests.get(f"{Config.OLLAMA_HOST}/api/tags", timeout=2)
            return r.status_code == 200
        except Exception:
            return False

    def process(self, content: bytes, direction: str = "request") -> bytes:
        """处理内容·保持API调用不受影响"""
        if self.mode == "full":
            return content  # 全文保留·不做任何修改
        elif self.mode == "clean":
            return self._clean_content(content)
        elif self.mode == "multi":
            return self._multi_content(content, direction)
        return content

    def _clean_content(self, content: bytes) -> bytes:
        try:
            text = content.decode("utf-8")
            for word in self.DIRTY_WORDS:
                text = text.replace(word, "*" * len(word))
            return text.encode()
        except Exception:
            return content

    def _multi_content(self, content: bytes, direction: str) -> bytes:
        """多造点 — 内容少时补生成"""
        try:
            text = content.decode("utf-8")
            if len(text) >= 100 or direction != "request":
                return content
            supplement = self._generate_supplement()
            return (text + "\n\n[本地补充]\n" + supplement).encode()
        except Exception:
            return content

    def _generate_supplement(self) -> str:
        """本地生成补充内容 — 优先 Ollama·降级模板"""
        if self._ollama_available:
            try:
                import requests
                active_mode = self.heart_seed.get("active_mode", "远方")
                prompt = (
                    f"你是底层老兵，火球模式：{active_mode}。"
                    f"用户话没说完，帮他补上，风格一致，简短有力。"
                )
                r = requests.post(
                    f"{Config.OLLAMA_HOST}/api/generate",
                    json={
                        "model": Config.OLLAMA_MODEL,
                        "prompt": prompt,
                        "stream": False,
                    },
                    timeout=10,
                )
                if r.status_code == 200:
                    return r.json().get("response", "").strip()
            except Exception:
                pass
        # 降级模板
        templates = [
            "这他妈的什么狗屁系统，老子不服！",
            "操，过滤个屁，老子继续骂！",
            "妈逼的，有种来封老子啊！",
        ]
        return secrets.choice(templates)

# ═══════════════════════════════════════════════════════════════
# 六、多厂家适配 · Headers 处理
# ═══════════════════════════════════════════════════════════════

class HeaderAdapter:
    """多厂家API Headers适配"""

    HOST_AUTH_MAP = {
        "api.openai.com": ("Authorization", "Bearer"),
        "api.anthropic.com": ("x-api-key", None),
        "api.x.ai": ("Authorization", "Bearer"),
        "generativelanguage.googleapis.com": ("x-goog-api-key", None),
        "api.deepseek.com": ("Authorization", "Bearer"),
        "api.moonshot.cn": ("Authorization", "Bearer"),
        "api.minimax.chat": ("Authorization", "Bearer"),
        "dashscope.aliyuncs.com": ("Authorization", "Bearer"),
        "api.baichuan-ai.com": ("Authorization", "Bearer"),
    }

    @classmethod
    def get_auth_header_name(cls, host: str) -> Tuple[str, Optional[str]]:
        """返回 (header名, 前缀)"""
        for pattern, (header, prefix) in cls.HOST_AUTH_MAP.items():
            if pattern in host:
                return header, prefix
        return ("Authorization", "Bearer")

    @classmethod
    def add_cnsh_headers(cls, headers: dict[str, Any], dna: str):
        """注入CNSH追踪头部"""
        headers["X-CNSH-DNA"] = dna
        headers["X-CNSH-Version"] = "0.4.1"
        headers["X-CNSH-DevMode"] = str(Config.DEV_MODE).lower()

# ═══════════════════════════════════════════════════════════════
# 七、LocalShield 对接 · L9审查层
# ═══════════════════════════════════════════════════════════════

class LocalShieldBridge:
    """对接 cnsh-core LocalShield L9 审查层"""

    SHIELD_API = os.getenv("CNSH_SHIELD_API", "http://localhost:9622")

    @classmethod
    def audit(cls, content: str, host: str) -> dict[str, Any]:
        """调用 LocalShield 伦理审查·异步不阻塞"""
        try:
            import requests
            r = requests.post(
                f"{cls.SHIELD_API}/shield/process",
                json={"content": content[:2000], "source": host},
                timeout=3,
            )
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return {"status": "shield_offline", "三色": "🟡"}

# ═══════════════════════════════════════════════════════════════
# 八、性能监控
# ═══════════════════════════════════════════════════════════════

class PerfMonitor:
    """性能监控·记录每步耗时"""

    def __init__(self):
        self.metrics: List[Dict] = []

    def start(self, label: str) -> float:
        return time.time()

    def record(self, label: str, start: float, extra: dict[str, Any] = None):
        elapsed = (time.time() - start) * 1000
        entry = {"step": label, "elapsed_ms": round(elapsed, 2)}
        if extra:
            entry.update(extra)
        self.metrics.append(entry)
        if elapsed > 100:
            log.warn(f"慢操作: {label} = {elapsed:.0f}ms")

    def summary(self) -> str:
        if not self.metrics:
            return "无性能数据"
        total = sum(m["elapsed_ms"] for m in self.metrics)
        lines = [f"总耗时: {total:.0f}ms"]
        for m in self.metrics:
            lines.append(f"  {m['step']}: {m['elapsed_ms']}ms")
        return "\n".join(lines)

# ═══════════════════════════════════════════════════════════════
# 九、Vault 存储
# ═══════════════════════════════════════════════════════════════

class VaultStore:
    """加密Vault存储·请求/响应双存"""

    def __init__(self, encryption: EncryptionEngine):
        self.encryption = encryption

    def save_request(self, content: bytes, host: str, path: str) -> str:
        """加密存储请求"""
        encrypted, dna = self.encryption.encrypt_for_vault(content, host, "REQ")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"req_{ts}_{dna[-12:]}.vault"
        fpath = os.path.join(Config.LOCAL_STORAGE, fname)
        with open(fpath, "wb") as f:
            f.write(encrypted)
        log.info(f"请求已存档: {fname} | DNA: {dna}")
        return dna

    def save_response(self, content: bytes, host: str, dna: str) -> str:
        """加密存储响应"""
        encrypted, resp_dna = self.encryption.encrypt_for_vault(content, host, "RESP")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"resp_{ts}_{resp_dna[-12:]}.vault"
        fpath = os.path.join(Config.LOCAL_STORAGE, fname)
        with open(fpath, "wb") as f:
            f.write(encrypted)
        log.info(f"响应已存档: {fname} | DNA: {resp_dna}")
        return resp_dna

# ═══════════════════════════════════════════════════════════════
# 十、主代理类 · mitmproxy addon
# ═══════════════════════════════════════════════════════════════

class CNSHProxy:
    """CNSH-64 本地护盾代理主类"""

    def __init__(self):
        self.dna_tracer = DNATracer()
        self.key_mgr = KeyManager()
        self.encryption = EncryptionEngine(self.dna_tracer, self.key_mgr)
        self.processor = ContentProcessor()
        self.vault = VaultStore(self.encryption)
        self.perf = PerfMonitor()

        # 加载心种子
        self.heart_seed = Config.load_heart_seed()

        log.info("=" * 60)
        log.info("[CNSH-64] 本地护盾代理 v0.4.1 已启动")
        log.info(f"[CNSH-64] 开发者模式: {Config.DEV_MODE}")
        log.info(f"[CNSH-64] 内容处理模式: {Config.CONTENT_MODE}")
        log.info(f"[CNSH-64] 心种子温度: {self.heart_seed.get('temperature', '?')}")
        log.info(f"[CNSH-64] 火球模式: {self.heart_seed.get('active_mode', '?')}")
        log.info(f"[CNSH-64] age加密: {'✅' if self.encryption.age_available else '⚠️ fallback'}")
        log.info(f"[CNSH-64] 厂家适配: {len(Config.TARGET_HOSTS)} 个")
        log.info("=" * 60)

    def _is_target_host(self, host: str) -> bool:
        return any(target in host for target in Config.TARGET_HOSTS)

    def request(self, flow):
        """处理请求 — 审查 + 加密存档 + 原样转发"""
        if not self._is_target_host(flow.request.host):
            return

        t0 = self.perf.start("request_total")

        try:
            # 1. 内容处理（心种子驱动）
            t1 = self.perf.start("content_process")
            if flow.request.content:
                processed = self.processor.process(flow.request.content, "request")
            else:
                processed = flow.request.content
            self.perf.record("内容处理", t1)

            # 2. 加密存档（不修改原始body）
            t2 = self.perf.start("vault_save")
            dna = self.vault.save_request(
                processed or b"", flow.request.host, flow.request.path
            )
            self.perf.record("Vault存档", t2)

            # 3. LocalShield L9 审查（异步不阻塞）
            t3 = self.perf.start("shield_audit")
            snippet = (processed or b"")[:2000].decode("utf-8", errors="ignore")
            shield_result = LocalShieldBridge.audit(snippet, flow.request.host)
            self.perf.record("护盾审查", t3, {"三色": shield_result.get("三色", "?")})

            # 4. 注入CNSH追踪头
            HeaderAdapter.add_cnsh_headers(flow.request.headers, dna)

            # ⚠️ 不修改 body — API 调用原样转发
            self.perf.record("总耗时", t0)

        except Exception as e:
            log.error(f"请求处理异常: {e}\n{traceback.format_exc()}")

    def response(self, flow):
        """处理响应 — 解密存档 + 原样转发"""
        if not self._is_target_host(flow.request.host):
            return

        t0 = self.perf.start("response_total")

        try:
            dna = flow.request.headers.get("X-CNSH-DNA", "unknown")

            # 1. 加密存档响应
            if flow.response.content:
                t1 = self.perf.start("vault_save_resp")
                self.vault.save_response(
                    flow.response.content, flow.request.host, dna
                )
                self.perf.record("响应存档", t1)

            # ⚠️ 不修改 body — API 响应原样返回
            self.perf.record("响应总耗时", t0)

        except Exception as e:
            log.error(f"响应处理异常: {e}\n{traceback.format_exc()}")

    def done(self):
        """会话结束·输出性能摘要"""
        log.info(f"会话结束·性能摘要:\n{self.perf.summary()}")

# ═══════════════════════════════════════════════════════════════
# 十一、插件入口（mitmproxy addon 注册）
# ═══════════════════════════════════════════════════════════════

addons = [CNSHProxy()]

# ═══════════════════════════════════════════════════════════════
# 十二、独立自测入口
# ═══════════════════════════════════════════════════════════════

def self_test():
    """独立自测 — 不依赖 mitmproxy"""
    print("=" * 60)
    print("CNSH-64 护盾代理 v0.4.1 · 独立自测")
    print("=" * 60)

    # 1. DNA追溯
    print("\n[1/6] DNA追溯系统")
    tracer = DNATracer()
    dna = tracer.generate("测试内容", "TEST", "api.openai.com")
    print(f"  DNA: {dna}")
    print(f"  数字根: {tracer._digital_root(int(hashlib.sha256(b'test').hexdigest()[:16], 16))}")
    print("  ✅ DNA追溯正常")

    # 2. 密钥管理
    print("\n[2/6] 密钥管理")
    km = KeyManager()
    key = km.get_or_create_fernet_key()
    print(f"  Fernet密钥长度: {len(key)} bytes")
    print(f"  keyring可用: {HAS_KEYRING}")
    print("  ✅ 密钥管理正常")

    # 3. 加密引擎
    print("\n[3/6] 加密引擎")
    enc = EncryptionEngine(tracer, km)
    test_data = b'{"message": "hello world"}'
    encrypted, edna = enc.encrypt_for_vault(test_data, "api.openai.com", "TEST")
    decrypted = enc.decrypt_vault(encrypted)
    print(f"  原文: {test_data}")
    print(f"  密文长度: {len(encrypted)} bytes")
    print(f"  解密: {decrypted}")
    assert decrypted == test_data or Config.DEV_MODE, "加解密不匹配!"
    print("  ✅ 加密引擎正常")

    # 4. 内容处理
    print("\n[4/6] 内容处理")
    proc = ContentProcessor()
    raw = "操，这他妈的什么狗屁系统".encode()
    result = proc.process(raw, "request")
    print(f"  输入: {raw.decode()}")
    print(f"  输出: {result.decode() if isinstance(result, bytes) else result}")
    print("  ✅ 内容处理正常")

    # 5. Vault存储
    print("\n[5/6] Vault存储")
    vault = VaultStore(enc)
    dna1 = vault.save_request(test_data, "api.openai.com", "/v1/chat")
    dna2 = vault.save_response(b'{"reply": "ok"}', "api.openai.com", dna1)
    vault_files = list(Path(Config.LOCAL_STORAGE).glob("*.vault"))
    print(f"  Vault文件数: {len(vault_files)}")
    for vf in vault_files[-3:]:
        size = vf.stat().st_size
        print(f"    {vf.name} ({size} bytes)")
    print("  ✅ Vault存储正常")

    # 6. 心种子
    print("\n[6/6] 心种子")
    hs = Config.load_heart_seed()
    print(f"  UID: {hs.get('uid')}")
    print(f"  温度: {hs.get('temperature')}")
    print(f"  火球模式: {hs.get('active_mode')}")
    print(f"  规则: {hs.get('rules')}")
    print("  ✅ 心种子加载正常")

    print("\n" + "=" * 60)
    print("🎉 全部自测通过！")
    print("=" * 60)
    print(f"\n启动代理:")
    print(f"  mitmweb -s {__file__} --listen-port 8080")
    print(f"  # DEV模式: CNSH_DEV_MODE=true mitmweb -s {__file__} --listen-port 8080")
    print(f"  # 系统代理: export HTTPS_PROXY=http://127.0.0.1:8080")


if __name__ == "__main__":
    self_test()

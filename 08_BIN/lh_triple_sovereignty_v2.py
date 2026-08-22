#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-TRIPLE-SOVEREIGNTY-v2-UID9622
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂 · 三重主权引擎 v2.0
DNA: #龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-TRIPLE-SOVEREIGNTY-v2-UID9622

实现：
  1. 数据主权 → 本地加密存储，DNA指纹，存储抽象（支持多种后端）
  2. 货币主权 → 支付网关抽象（模拟/真实CBDC）
  3. 审计主权 → 可配置三色规则、史官记录、耻辱墙、陪审团（随机池）
  4. 配置管理 + 日志系统 + 统一异常处理 + 健康检查

安全修订（2026-08-17 部署时修正）：
  - 补 import logging.handlers（原版启动即崩）
  - Fernet 密钥做 urlsafe_b64encode（原版首次加密必崩）
  - key.bin 不再明文存密钥，只存 salt+verifier，主密钥仅驻内存
  - 非交互环境（systemd）通过 LONGHUN_MASTER_PASSWORD 提供密码，禁 input() 挂死
  - 引擎懒加载，/health 不依赖引擎
"""

import os
import sys
import json
import hashlib
import time
import base64
import logging
import logging.handlers
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import yaml
from flask import Flask, request, jsonify

# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
MASTER_PASSWORD_ENV = "LONGHUN_MASTER_PASSWORD"


def generate_dna(suffix: str = "SOVEREIGNTY") -> str:
    h = hashlib.sha256(f"{suffix}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{suffix}-{h}-{UID}"

# ============================================================
# 1. 日志系统
# ============================================================

def setup_logger(name="longhun", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        log_dir = Path.home() / ".longhun" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        fh = logging.handlers.RotatingFileHandler(
            log_dir / "longhun.log", maxBytes=10*1024*1024, backupCount=5
        )
        fh.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        logger.addHandler(ch)
        logger.addHandler(fh)
    return logger

logger = setup_logger()

# ============================================================
# 2. 统一异常处理
# ============================================================

class SovereigntyError(Exception):
    def __init__(self, code: int, message: str, details: Any = None):
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)

class DataSovereigntyError(SovereigntyError): pass
class CurrencySovereigntyError(SovereigntyError): pass
class AuditSovereigntyError(SovereigntyError): pass

ERR_DATA_NOT_FOUND = 1001
ERR_ENCRYPTION_FAILED = 1002
ERR_PAYMENT_REJECTED = 2001
ERR_AUDIT_FAILED = 3001

# ============================================================
# 3. 配置管理
# ============================================================

@dataclass
class SystemConfig:
    data_home: str = os.environ.get("LONGHUN_DATA_HOME", str(Path.home() / ".longhun"))
    encryption_algorithm: str = "Fernet"
    audit_threshold_green: int = int(os.environ.get("AUDIT_GREEN", 85))
    audit_threshold_yellow: int = int(os.environ.get("AUDIT_YELLOW", 60))
    payment_api_url: str = os.environ.get("PAYMENT_API_URL", "https://mock-payment.example.com")
    jury_pool_size: int = int(os.environ.get("JURY_POOL_SIZE", 5))
    log_level: str = os.environ.get("LOG_LEVEL", "INFO")


class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        config_path = os.environ.get("LONGHUN_CONFIG", "")
        data = {}
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    loaded = yaml.safe_load(f) or {}
                if isinstance(loaded, dict):
                    data = {k: v for k, v in loaded.items()
                            if k in SystemConfig.__dataclass_fields__}
                else:
                    logger.warning("配置文件格式错误，使用默认配置")
            except Exception as e:
                logger.warning(f"配置加载失败，使用默认配置: {e}")
        self.config = SystemConfig(**data)


cfg = ConfigManager().config
logger.info(f"配置加载完成: {cfg}")

# ============================================================
# 4. 存储抽象层
# ============================================================

class StorageBackend(ABC):
    @abstractmethod
    def save(self, key: str, data: dict) -> bool: ...
    @abstractmethod
    def load(self, key: str) -> Optional[dict]: ...
    @abstractmethod
    def list_keys(self) -> List[str]: ...
    @abstractmethod
    def delete(self, key: str) -> bool: ...


class FileStorage(StorageBackend):
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _key_to_path(self, key: str) -> Path:
        # 简单处理，防止路径遍历
        safe_key = key.replace('/', '_').replace('..', '')
        return self.base_path / f"{safe_key}.json"

    def save(self, key: str, data: dict) -> bool:
        try:
            path = self._key_to_path(key)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"存储失败 {key}: {e}")
            return False

    def load(self, key: str) -> Optional[dict]:
        path = self._key_to_path(key)
        if not path.exists():
            return None
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载失败 {key}: {e}")
            return None

    def list_keys(self) -> List[str]:
        keys = []
        for f in self.base_path.glob("*.json"):
            keys.append(f.stem)
        return keys

    def delete(self, key: str) -> bool:
        path = self._key_to_path(key)
        if path.exists():
            path.unlink()
            return True
        return False

# ============================================================
# 5. 安全增强：密钥派生 + 防篡改链
# ============================================================

def derive_key(password: str, salt: bytes = None) -> tuple:
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    key = kdf.derive(password.encode())
    return key, salt


class HashChain:
    @staticmethod
    def create_entry(data: dict, prev_hash: str = "") -> str:
        content = json.dumps(data, sort_keys=True) + prev_hash
        return hashlib.sha256(content.encode()).hexdigest()

# ============================================================
# 6. 支付网关抽象
# ============================================================

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, from_acc: str, to_acc: str, amount: float, currency: str = "CNY") -> Dict: ...


class MockPaymentGateway(PaymentGateway):
    def process_payment(self, from_acc: str, to_acc: str, amount: float, currency: str = "CNY") -> Dict:
        return {
            "status": "success",
            "transaction_id": f"TXN-{int(time.time())}",
            "message": "模拟支付成功（实际需对接央行系统）"
        }


class RealCBDCGateway(PaymentGateway):
    def process_payment(self, from_acc: str, to_acc: str, amount: float, currency: str = "CNY") -> Dict:
        # 这里实现真实API调用
        raise NotImplementedError("真实央行API尚未接入")

# ============================================================
# 7. 数据主权层
# ============================================================

class DataSovereignty:
    def __init__(self, user_id: str, password: str = "", backend: StorageBackend = None):
        self.user_id = user_id
        self.backend = backend or FileStorage(Path(cfg.data_home) / "data" / user_id)
        self.key_file = Path(cfg.data_home) / "data" / user_id / "key.bin"
        self._key: Optional[bytes] = None
        self._ensure_key(password)

    def _prompt_password(self, prompt: str) -> str:
        """交互式终端才允许 input()；非交互环境必须走环境变量，防 systemd 挂死。"""
        if sys.stdin.isatty():
            return input(prompt)
        raise DataSovereigntyError(
            ERR_ENCRYPTION_FAILED,
            f"非交互环境必须通过环境变量 {MASTER_PASSWORD_ENV} 提供数据主权密码"
        )

    def _ensure_key(self, password: str = ""):
        if not password:
            password = os.environ.get(MASTER_PASSWORD_ENV, "")
        if not self.key_file.exists():
            # 首次运行：生成新密钥，key.bin 只存 salt + verifier，主密钥只驻内存
            if not password:
                password = self._prompt_password("请设置您的数据主密码: ")
            key, salt = derive_key(password)
            verifier = hashlib.sha256(key).digest()
            with open(self.key_file, 'wb') as f:
                f.write(salt + verifier)
            os.chmod(self.key_file, 0o600)
            self._key = key
            logger.info("新密钥已生成（key.bin 仅存 salt+verifier）")
        else:
            # 已存在：用密码重派生并校验 verifier
            if not password:
                password = self._prompt_password("请输入数据主密码: ")
            with open(self.key_file, 'rb') as f:
                data = f.read()
                salt = data[:16]
                stored_verifier = data[16:48]
            derived_key, _ = derive_key(password, salt)
            if hashlib.sha256(derived_key).digest() != stored_verifier:
                raise DataSovereigntyError(ERR_ENCRYPTION_FAILED, "密码错误")
            self._key = derived_key

    def _get_key(self) -> bytes:
        if self._key is None:
            raise DataSovereigntyError(ERR_ENCRYPTION_FAILED, "主密钥未初始化")
        return self._key

    def store(self, content: str, metadata: Dict = None) -> Dict:
        dna = generate_dna("DATA-STORE")
        key = self._get_key()
        fernet = Fernet(base64.urlsafe_b64encode(key))
        encrypted = fernet.encrypt(content.encode('utf-8'))
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        record = {
            "dna": dna,
            "hash": content_hash,
            "encrypted": base64.b64encode(encrypted).decode('ascii'),
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
        self.backend.save(dna, record)
        logger.info(f"数据存储成功: {dna}")
        return {
            "dna": dna,
            "hash": content_hash,
            "timestamp": record["timestamp"],
            "message": "✅ 数据已本地加密存储，系统只持有DNA指纹"
        }

    def retrieve(self, dna: str) -> Dict:
        record = self.backend.load(dna)
        if not record:
            raise DataSovereigntyError(ERR_DATA_NOT_FOUND, "未找到对应DNA记录")
        return {
            "dna": record["dna"],
            "hash": record["hash"],
            "metadata": record.get("metadata", {}),
            "timestamp": record["timestamp"],
            "note": "解密需用户本地密钥，系统不持有明文"
        }

    def list_all(self) -> List[Dict]:
        keys = self.backend.list_keys()
        records = []
        for key in keys:
            rec = self.backend.load(key)
            if rec:
                records.append({
                    "dna": rec["dna"],
                    "hash": rec["hash"],
                    "timestamp": rec["timestamp"]
                })
        return records

# ============================================================
# 8. 货币主权层
# ============================================================

class CurrencySovereignty:
    def __init__(self, gateway: PaymentGateway = None):
        self.gateway = gateway or MockPaymentGateway()

    def pay(self, from_account: str, to_account: str, amount: float, currency: str = "CNY") -> Dict:
        if amount <= 0:
            raise CurrencySovereigntyError(ERR_PAYMENT_REJECTED, "金额必须大于0")
        result = self.gateway.process_payment(from_account, to_account, amount, currency)
        dna = generate_dna("PAYMENT")
        audit_record = {
            "dna": dna,
            "from": from_account,
            "to": to_account,
            "amount": amount,
            "currency": currency,
            "transaction_id": result.get("transaction_id", ""),
            "timestamp": datetime.now().isoformat()
        }
        self._record_audit(audit_record)
        return {
            "dna": dna,
            "transaction_id": result["transaction_id"],
            "status": result["status"],
            "timestamp": audit_record["timestamp"],
            "message": "✅ 支付指令已发出"
        }

    def _record_audit(self, record: Dict):
        audit_dir = Path(cfg.data_home) / "04_AUDIT"
        audit_dir.mkdir(parents=True, exist_ok=True)
        audit_file = audit_dir / f"currency_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        with open(audit_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

# ============================================================
# 9. 审计主权层
# ============================================================

class AuditSovereignty:
    def __init__(self):
        self.histories = []
        self.shame_wall = []
        self._load_rules()

    def _load_rules(self):
        # 可从配置加载规则
        self.rules = [
            {"name": "内容过短", "condition": lambda c: len(c) < 10, "penalty": -10},
            {"name": "暴力词汇", "condition": lambda c: any(w in c for w in ['攻击', '暴力']), "penalty": -30},
            {"name": "违法词汇", "condition": lambda c: any(w in c for w in ['贿赂', '洗钱']), "penalty": -50},
        ]
        self.threshold_green = cfg.audit_threshold_green
        self.threshold_yellow = cfg.audit_threshold_yellow

    def tricolor_audit(self, content: str, context: str = "") -> Dict:
        dna = generate_dna("AUDIT")
        score = 80
        issues = []
        for rule in self.rules:
            if rule["condition"](content):
                score += rule["penalty"]
                issues.append(rule["name"])
        score = max(0, min(100, score))

        if score >= self.threshold_green:
            color = "🟢"
            status = "通过"
        elif score >= self.threshold_yellow:
            color = "🟡"
            status = "警告"
        else:
            color = "🔴"
            status = "拒绝"

        result = {
            "dna": dna,
            "score": score,
            "color": color,
            "status": status,
            "issues": issues,
            "timestamp": datetime.now().isoformat()
        }
        self._record_history("tricolor_audit", result)
        if color == "🔴":
            self._add_shame(result)
        return result

    def _record_history(self, action: str, details: Dict):
        prev_hash = self.histories[-1]["hash"] if self.histories else ""
        entry = {
            "action": action,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "hash": HashChain.create_entry(details, prev_hash)
        }
        self.histories.append(entry)
        audit_dir = Path(cfg.data_home) / "04_AUDIT"
        audit_dir.mkdir(parents=True, exist_ok=True)
        audit_file = audit_dir / f"audit_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        with open(audit_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _add_shame(self, record: Dict):
        self.shame_wall.append(record)
        shame_dir = Path(cfg.data_home) / "08_STATE"
        shame_dir.mkdir(parents=True, exist_ok=True)
        shame_file = shame_dir / "shame_wall.jsonl"
        with open(shame_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        logger.critical(f"🚫 耻辱墙记录: {record['dna']}")

    def jury(self, case_id: str, evidence: List[str], seed: int = None) -> Dict:
        dna = generate_dna("JURY")
        pool = [f"J{i}" for i in range(1, 11)]  # 模拟陪审员池
        if seed is not None:
            random.seed(seed)
        selected = random.sample(pool, min(cfg.jury_pool_size, len(pool)))
        votes = {"有罪": 0, "无罪": 0, "弃权": 0}
        evidence_weight = len(evidence)
        for juror in selected:
            if evidence_weight > 3:
                vote = "有罪" if random.random() > 0.3 else "无罪"
            else:
                vote = random.choice(["有罪", "无罪", "弃权"])
            votes[vote] += 1
        verdict = "平局" if votes["有罪"] == votes["无罪"] else \
            "有罪" if votes["有罪"] > votes["无罪"] else "无罪"
        result = {
            "dna": dna,
            "case_id": case_id,
            "jurors": selected,
            "votes": votes,
            "verdict": verdict,
            "timestamp": datetime.now().isoformat()
        }
        self._record_history("jury_verdict", result)
        return result

# ============================================================
# 10. 三重主权集成引擎
# ============================================================

class TripleSovereigntyEngine:
    def __init__(self, user_id: str = UID, password: str = ""):
        self.user_id = user_id
        self.data = DataSovereignty(user_id, password)
        self.currency = CurrencySovereignty()
        self.audit = AuditSovereignty()
        self.dna = generate_dna("TRIPLE-ENGINE")
        logger.info(f"三重主权引擎初始化完成，用户: {user_id}")

    def store_data(self, content: str, metadata: Dict = None) -> Dict:
        return self.data.store(content, metadata)

    def make_payment(self, from_account: str, to_account: str, amount: float) -> Dict:
        return self.currency.pay(from_account, to_account, amount)

    def audit_content(self, content: str, context: str = "") -> Dict:
        return self.audit.tricolor_audit(content, context)

    def jury_decision(self, case_id: str, evidence: List[str]) -> Dict:
        return self.audit.jury(case_id, evidence)

    def get_status(self) -> Dict:
        return {
            "dna": self.dna,
            "user_id": self.user_id,
            "data_count": len(self.data.list_all()),
            "audit_history": len(self.audit.histories),
            "shame_count": len(self.audit.shame_wall),
            "timestamp": datetime.now().isoformat()
        }

# ============================================================
# 11. Flask API 服务（引擎懒加载，避免无密码时启动挂死）
# ============================================================

app = Flask(__name__)
_engine_cache: Dict[str, TripleSovereigntyEngine] = {}


def get_engine() -> TripleSovereigntyEngine:
    if "engine" not in _engine_cache:
        _engine_cache["engine"] = TripleSovereigntyEngine(
            password=os.environ.get(MASTER_PASSWORD_ENV, "")
        )
    return _engine_cache["engine"]


@app.route("/")
def index():
    return """
    <h1>🐉 龍魂 · 三重主权引擎 v2.0</h1>
    <p>数据主权 · 货币主权 · 审计主权</p>
    <ul>
        <li><a href="/status">/status</a></li>
        <li><a href="/health">/health</a></li>
        <li><a href="/data?action=store&content=hello">/data?action=store&content=hello</a></li>
        <li><a href="/payment?from=UID9622&to=商户&amount=10">/payment</a></li>
        <li><a href="/audit?content=测试">/audit</a></li>
        <li><a href="/jury?case_id=001&evidence=证据1,证据2">/jury</a></li>
    </ul>
    """


@app.route("/health")
def health():
    # 不依赖引擎，保证健康检查永远可探活
    return jsonify({"status": "ok", "dna": generate_dna("HEALTH")})


@app.route("/status")
def status():
    engine = get_engine()
    return jsonify(engine.get_status())


@app.route("/data")
def data_store():
    action = request.args.get("action")
    content = request.args.get("content", "")
    metadata = request.args.get("metadata")
    if action == "store" and content:
        try:
            meta = json.loads(metadata) if metadata else None
        except (ValueError, TypeError):
            return jsonify({"error": "metadata 不是合法 JSON"}), 400
        try:
            result = get_engine().store_data(content, meta)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    elif action == "list":
        records = get_engine().data.list_all()
        return jsonify({"records": records})
    return jsonify({"error": "Invalid request"}), 400


@app.route("/payment")
def payment():
    from_account = request.args.get("from", "UID9622")
    to_account = request.args.get("to", "商户")
    try:
        amount = float(request.args.get("amount", 0))
    except ValueError:
        return jsonify({"error": "金额无效"}), 400
    if amount <= 0:
        return jsonify({"error": "金额必须大于0"}), 400
    try:
        result = get_engine().make_payment(from_account, to_account, amount)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/audit")
def audit():
    content = request.args.get("content", "")
    context = request.args.get("context", "")
    if not content:
        return jsonify({"error": "需要content参数"}), 400
    try:
        result = get_engine().audit_content(content, context)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/jury")
def jury():
    case_id = request.args.get("case_id", "")
    evidence_str = request.args.get("evidence", "")
    evidence = evidence_str.split(",") if evidence_str else []
    if not case_id:
        return jsonify({"error": "需要case_id"}), 400
    try:
        result = get_engine().jury_decision(case_id, evidence)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ============================================================
# 12. CLI 入口
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="🐉 三重主权引擎 v2.0")
    parser.add_argument("--store", help="存储数据 (内容)")
    parser.add_argument("--pay", nargs=3, metavar=("FROM", "TO", "AMOUNT"), help="支付")
    parser.add_argument("--audit", help="审计内容")
    parser.add_argument("--jury", nargs=2, metavar=("CASE_ID", "EVIDENCE"), help="陪审团")
    parser.add_argument("--status", action="store_true", help="查看状态")
    parser.add_argument("--server", action="store_true", help="启动API服务")
    parser.add_argument("--port", type=int, default=8091, help="API端口")
    parser.add_argument("--password", help="数据主权密码", default="")

    args = parser.parse_args()
    engine = TripleSovereigntyEngine(password=args.password)

    if args.server:
        print(f"🐉 三重主权引擎 API 启动: http://0.0.0.0:{args.port}")
        app.run(host="0.0.0.0", port=args.port, threaded=True)
        return

    if args.status:
        print(json.dumps(engine.get_status(), indent=2, ensure_ascii=False))
        return

    if args.store:
        try:
            result = engine.store_data(args.store)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"❌ 错误: {e}")
        return

    if args.pay:
        from_acc, to_acc, amount = args.pay
        try:
            result = engine.make_payment(from_acc, to_acc, float(amount))
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"❌ 错误: {e}")
        return

    if args.audit:
        try:
            result = engine.audit_content(args.audit)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"❌ 错误: {e}")
        return

    if args.jury:
        case_id, evidence_str = args.jury
        evidence = evidence_str.split(",") if evidence_str else []
        try:
            result = engine.jury_decision(case_id, evidence)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"❌ 错误: {e}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()

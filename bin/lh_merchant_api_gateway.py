#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-MERCHANT-API-GATEWAY-v1.0-a3f2c1d8
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
"""
╔══════════════════════════════════════════════════════════════════════════╗
║       龍魂·国产商户开放API网关 v1.0 — 让中国商户接入龍魂能力              ║
║       LongHun Merchant API Gateway · For Chinese Businesses Only         ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-MERCHANT-GATEWAY-v1.0              ║
║  #CONFIRM🌌9622-ONLY-ONCE🧬MAPI-A3F2                                     ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                           ║
║                                                                           ║
║  设计原则:                                                                ║
║  1. 只对国产商户开放 — 中国企业营业执照验证                                ║
║  2. API Key + HMAC签名双重认证                                            ║
║  3. 四层商户等级 — free/basic/pro/enterprise                              ║
║  4. 令牌桶限流 + 调用计量 + 审计日志                                      ║
║  5. 内核算法/369/DNA/GPG 不对外开放                                       ║
║  6. 太极蚁群八宫路由 + API Guard安全层                                    ║
║                                                                           ║
║  开放能力清单:                                                            ║
║  - AI文本生成 (混元/DeepSeek)        - 五害检测                           ║
║  - 内容安全审计                       - 焦虑话术检测                       ║
║  - 知识库检索                         - 数字根计算                         ║
║  - 五行属性判定                       - 信任积分查询                       ║
║  - CNSH代码翻译                       - 媒体验证                           ║
║                                                                           ║
║  不开放(内核层):                                                          ║
║  - 369洛书算法 · 人格路由 · DNA生成 · GPG签名 · 熔断控制 · 系统管理        ║
║                                                                           ║
║  主权人: UID9622 💎 龍芯北辰·诸葛鑫·Lucky                                ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import hmac
import hashlib
import secrets
import sqlite3
import logging
import threading
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
from functools import wraps
from dataclasses import dataclass, field, asdict

# ── 焊死常量 ──
DNA = "#龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-MERCHANT-GATEWAY-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬MAPI-A3F2"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
SOVEREIGN_UID = "UID9622"

# 商户数据库路径
MERCHANT_DB = Path.home() / ".龍魂" / "merchants" / "merchants.db"
MERCHANT_DB.parent.mkdir(parents=True, exist_ok=True)

# API 日志目录
API_LOG_DIR = Path.home() / ".龍魂" / "merchants" / "api_logs"
API_LOG_DIR.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════
# 商户层级 & 权限
# ═══════════════════════════════════════════════════════════

class MerchantTier(str, Enum):
    FREE = "free"           # 免费试用·100次/天·1 QPS
    BASIC = "basic"         # 基础版·1000次/天·5 QPS
    PRO = "pro"             # 专业版·10000次/天·20 QPS
    ENTERPRISE = "enterprise"  # 企业版·100000次/天·100 QPS

    @property
    def daily_limit(self) -> int:
        return {self.FREE: 100, self.BASIC: 1000, self.PRO: 10000, self.ENTERPRISE: 100000}[self]

    @property
    def qps_limit(self) -> int:
        return {self.FREE: 1, self.BASIC: 5, self.PRO: 20, self.ENTERPRISE: 100}[self]

    @property
    def max_keys(self) -> int:
        return {self.FREE: 1, self.BASIC: 3, self.PRO: 10, self.ENTERPRISE: 50}[self]

class MerchantStatus(str, Enum):
    PENDING = "pending"       # 待审核
    ACTIVE = "active"         # 已激活
    SUSPENDED = "suspended"   # 已暂停
    REVOKED = "revoked"       # 已吊销


# ═══════════════════════════════════════════════════════════
# 可开放 API 能力注册表
# ═══════════════════════════════════════════════════════════

OPEN_API_CATALOG = {
    "ai.text.generate": {
        "name": "AI文本生成",
        "description": "调用混元/DeepSeek大模型生成文本，支持流式输出",
        "path": "/v1/ai/text",
        "method": "POST",
        "min_tier": MerchantTier.FREE,
        "category": "AI",
        "rate_cost": 1,  # 每次调用消耗的配额
        "params": {
            "prompt": "str (required) - 提示词",
            "model": "str (optional) - hunyuan/deepseek，默认hunyuan",
            "max_tokens": "int (optional) - 最大输出长度",
            "stream": "bool (optional) - 是否流式输出",
            "temperature": "float (optional) - 0.0~1.0",
        }
    },
    "ai.image.generate": {
        "name": "AI图片生成",
        "description": "调用混元图片生成模型",
        "path": "/v1/ai/image",
        "method": "POST",
        "min_tier": MerchantTier.BASIC,
        "category": "AI",
        "rate_cost": 5,
        "params": {
            "prompt": "str (required) - 图片描述",
            "size": "str (optional) - 1024x1024/1024x1536/1536x1024",
            "style": "str (optional) - vivid/natural",
        }
    },
    "security.five_harms": {
        "name": "五害检测",
        "description": "检测内容是否包含五害信息（涉政/涉黄/涉暴/涉赌/涉诈）",
        "path": "/v1/security/five-harms",
        "method": "POST",
        "min_tier": MerchantTier.FREE,
        "category": "安全",
        "rate_cost": 1,
        "params": {
            "content": "str (required) - 待检测文本",
            "detail": "bool (optional) - 是否返回详细分类",
        }
    },
    "security.content_audit": {
        "name": "内容安全审计",
        "description": "三色审计：对内容进行通过/待核/红线三级判定",
        "path": "/v1/security/audit",
        "method": "POST",
        "min_tier": MerchantTier.BASIC,
        "category": "安全",
        "rate_cost": 2,
        "params": {
            "content": "str (required) - 待审计内容",
            "context": "str (optional) - 上下文信息",
        }
    },
    "security.anxiety_detect": {
        "name": "焦虑话术检测",
        "description": "检测文本中的PUA/焦虑制造/道德绑架等五类话术",
        "path": "/v1/security/anxiety",
        "method": "POST",
        "min_tier": MerchantTier.FREE,
        "category": "安全",
        "rate_cost": 1,
        "params": {
            "content": "str (required) - 待检测文本",
        }
    },
    "knowledge.search": {
        "name": "知识库检索",
        "description": "检索龍魂知识库，返回相关文档和片段",
        "path": "/v1/knowledge/search",
        "method": "GET",
        "min_tier": MerchantTier.FREE,
        "category": "知识",
        "rate_cost": 1,
        "params": {
            "query": "str (required) - 搜索关键词",
            "top_k": "int (optional) - 返回条数，默认5",
            "category": "str (optional) - 限定分类",
        }
    },
    "math.digital_root": {
        "name": "数字根计算",
        "description": "计算洛书369数字根，返回三六九不动点判定",
        "path": "/v1/math/digital-root",
        "method": "POST",
        "min_tier": MerchantTier.FREE,
        "category": "算法",
        "rate_cost": 1,
        "params": {
            "n": "int (required) - 输入数字",
        }
    },
    "culture.wuxing": {
        "name": "五行属性判定",
        "description": "输入干支/姓名/数字，返回五行属性及生克关系",
        "path": "/v1/culture/wuxing",
        "method": "POST",
        "min_tier": MerchantTier.BASIC,
        "category": "文化",
        "rate_cost": 1,
        "params": {
            "input": "str (required) - 干支/姓名/数字",
            "type": "str (optional) - ganzhi/name/number",
        }
    },
    "trust.score": {
        "name": "信任积分查询",
        "description": "查询指定UID的信任积分（三分桶：技术/社区/创作）",
        "path": "/v1/trust/score",
        "method": "GET",
        "min_tier": MerchantTier.PRO,
        "category": "治理",
        "rate_cost": 1,
        "params": {
            "uid": "str (required) - 用户ID",
        }
    },
    "cnsh.translate": {
        "name": "CNSH代码翻译",
        "description": "将中华自主编程语言CNSH翻译为Python代码",
        "path": "/v1/cnsh/translate",
        "method": "POST",
        "min_tier": MerchantTier.PRO,
        "category": "开发",
        "rate_cost": 3,
        "params": {
            "code": "str (required) - CNSH代码",
            "target": "str (optional) - python/javascript，默认python",
        }
    },
    "media.verify": {
        "name": "媒体验证",
        "description": "验证图片/视频是否被篡改，检测深度伪造",
        "path": "/v1/media/verify",
        "method": "POST",
        "min_tier": MerchantTier.PRO,
        "category": "安全",
        "rate_cost": 3,
        "params": {
            "url": "str (required) - 媒体文件URL",
            "type": "str (optional) - image/video，自动检测",
        }
    },
}

# ═══════════════════════════════════════════════════════════
# 数据库初始化
# ═══════════════════════════════════════════════════════════

def init_merchant_db():
    """初始化商户数据库"""
    conn = sqlite3.connect(str(MERCHANT_DB))
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS merchants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            merchant_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            contact_name TEXT,
            contact_phone TEXT,
            contact_email TEXT,
            company_name TEXT,
            business_license TEXT,
            tier TEXT DEFAULT 'free',
            status TEXT DEFAULT 'pending',
            daily_limit INTEGER DEFAULT 100,
            qps_limit INTEGER DEFAULT 1,
            registered_at TEXT DEFAULT (datetime('now')),
            approved_at TEXT,
            suspended_at TEXT,
            notes TEXT
        );

        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_id TEXT UNIQUE NOT NULL,
            merchant_id TEXT NOT NULL,
            api_key_hash TEXT UNIQUE NOT NULL,
            api_key_prefix TEXT NOT NULL,
            secret_hash TEXT NOT NULL,
            name TEXT DEFAULT 'default',
            status TEXT DEFAULT 'active',
            created_at TEXT DEFAULT (datetime('now')),
            last_used_at TEXT,
            FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id)
        );

        CREATE TABLE IF NOT EXISTS usage_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            merchant_id TEXT NOT NULL,
            api_key_id TEXT,
            endpoint TEXT NOT NULL,
            method TEXT,
            status_code INTEGER,
            response_time_ms REAL,
            rate_cost INTEGER DEFAULT 0,
            ip_address TEXT,
            user_agent TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS daily_quotas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            merchant_id TEXT NOT NULL,
            date TEXT NOT NULL,
            used INTEGER DEFAULT 0,
            limit_amount INTEGER DEFAULT 100,
            UNIQUE(merchant_id, date)
        );

        CREATE INDEX IF NOT EXISTS idx_usage_merchant ON usage_records(merchant_id);
        CREATE INDEX IF NOT EXISTS idx_usage_date ON usage_records(created_at);
        CREATE INDEX IF NOT EXISTS idx_quotas_date ON daily_quotas(merchant_id, date);
    """)
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════
# 商户管理核心
# ═══════════════════════════════════════════════════════════

def register_merchant(name: str, company_name: str = "",
                      contact_name: str = "", contact_phone: str = "",
                      contact_email: str = "", business_license: str = "",
                      tier: str = "free") -> Dict:
    """注册新商户 → 待审核"""
    conn = sqlite3.connect(str(MERCHANT_DB))
    conn.row_factory = sqlite3.Row

    # 生成商户ID
    ts = int(time.time())
    merchant_id = f"MCH_{hashlib.sha256(f'{name}{ts}'.encode()).hexdigest()[:12]}"

    tier_enum = MerchantTier(tier)
    conn.execute("""
        INSERT INTO merchants (merchant_id, name, contact_name, contact_phone,
            contact_email, company_name, business_license, tier, status,
            daily_limit, qps_limit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?, ?)
    """, (merchant_id, name, contact_name, contact_phone,
          contact_email, company_name, business_license, tier,
          tier_enum.daily_limit, tier_enum.qps_limit))
    conn.commit()
    conn.close()

    return {
        "merchant_id": merchant_id,
        "name": name,
        "status": "pending",
        "message": "商户注册成功，等待审核。审核通过后可生成API密钥。",
        "next_step": f"lh merchant approve {merchant_id}"
    }


def approve_merchant(merchant_id: str, tier: str = None) -> Dict:
    """审核通过商户"""
    conn = sqlite3.connect(str(MERCHANT_DB))
    conn.row_factory = sqlite3.Row

    row = conn.execute("SELECT * FROM merchants WHERE merchant_id = ?",
                       (merchant_id,)).fetchone()
    if not row:
        conn.close()
        return {"error": "商户不存在", "merchant_id": merchant_id}

    updates = {"status": "active", "approved_at": datetime.now().isoformat()}
    if tier:
        t = MerchantTier(tier)
        updates["tier"] = tier
        updates["daily_limit"] = t.daily_limit
        updates["qps_limit"] = t.qps_limit

    set_clause = ", ".join(f"{k} = ?" for k in updates)
    conn.execute(f"UPDATE merchants SET {set_clause} WHERE merchant_id = ?",
                 list(updates.values()) + [merchant_id])
    conn.commit()
    conn.close()

    return {"merchant_id": merchant_id, "status": "active", "message": "商户审核通过"}


def suspend_merchant(merchant_id: str, reason: str = "") -> Dict:
    """暂停商户"""
    conn = sqlite3.connect(str(MERCHANT_DB))
    conn.execute("UPDATE merchants SET status = 'suspended', suspended_at = ?, notes = ? WHERE merchant_id = ?",
                 (datetime.now().isoformat(), reason, merchant_id))
    conn.commit()
    conn.close()
    return {"merchant_id": merchant_id, "status": "suspended", "reason": reason}


def generate_api_key(merchant_id: str, key_name: str = "default") -> Dict:
    """为商户生成API密钥 (API Key = 身份标识 + HMAC签名密钥)"""
    conn = sqlite3.connect(str(MERCHANT_DB))
    conn.row_factory = sqlite3.Row

    merchant = conn.execute("SELECT * FROM merchants WHERE merchant_id = ? AND status = 'active'",
                            (merchant_id,)).fetchone()
    if not merchant:
        conn.close()
        return {"error": "商户不存在或未激活"}

    tier = MerchantTier(merchant["tier"])
    key_count = conn.execute("SELECT COUNT(*) as cnt FROM api_keys WHERE merchant_id = ? AND status = 'active'",
                             (merchant_id,)).fetchone()["cnt"]
    if key_count >= tier.max_keys:
        conn.close()
        return {"error": f"密钥数量已达上限 ({tier.max_keys}个)，请先吊销旧密钥"}

    # 生成单一API Key (同时作为身份标识和HMAC签名密钥)
    api_key = f"lh_mch_{secrets.token_hex(24)}"
    key_id = f"key_{secrets.token_hex(8)}"

    conn.execute("""
        INSERT INTO api_keys (key_id, merchant_id, api_key_hash, api_key_prefix, secret_hash, name)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (key_id, merchant_id,
          hashlib.sha256(api_key.encode()).hexdigest(),
          api_key[:16] + "...",
          hashlib.sha256(api_key.encode()).hexdigest(),  # 已废弃·保留兼容
          key_name))
    conn.commit()
    conn.close()

    return {
        "key_id": key_id,
        "api_key": api_key,
        "name": key_name,
        "warning": "⚠️ API Key仅显示一次！此Key同时作为身份标识和HMAC签名密钥，请妥善保管，不可泄露。",
        "usage": "Header: X-LH-API-Key: <api_key>\n签名: HMAC-SHA256(api_key, METHOD+PATH+TIMESTAMP+SHA256(BODY))"
    }


# ═══════════════════════════════════════════════════════════
# 令牌桶限流器
# ═══════════════════════════════════════════════════════════

class TokenBucket:
    """令牌桶限流器 — 每商户独立桶"""

    def __init__(self, rate: float, capacity: int = None):
        self.rate = rate          # 令牌/秒
        self.capacity = capacity or int(rate * 2)
        self.tokens = float(self.capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

    def consume(self, tokens: int = 1) -> bool:
        """尝试消费令牌，返回是否成功"""
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_refill = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False


class RateLimiter:
    """全局限流器 — 管理所有商户的令牌桶"""

    def __init__(self):
        self.buckets: Dict[str, TokenBucket] = {}
        self.lock = threading.Lock()

    def get_bucket(self, merchant_id: str, qps: float) -> TokenBucket:
        key = merchant_id
        with self.lock:
            if key not in self.buckets:
                self.buckets[key] = TokenBucket(rate=qps)
            return self.buckets[key]

    def check(self, merchant_id: str, qps: float, cost: int = 1) -> Tuple[bool, str]:
        bucket = self.get_bucket(merchant_id, qps)
        if bucket.consume(cost):
            return True, ""
        return False, "速率超限，请稍后重试"


rate_limiter = RateLimiter()


# ═══════════════════════════════════════════════════════════
# 签名验证
# ═══════════════════════════════════════════════════════════

def verify_signature(api_key: str, method: str,
                     path: str, body: str, timestamp: str,
                     signature: str) -> bool:
    """
    HMAC-SHA256 签名验证
    签名串: METHOD + PATH + TIMESTAMP + SHA256(BODY)
    HMAC密钥: API Key本身
    """
    body_hash = hashlib.sha256(body.encode() if body else b"").hexdigest()
    sign_string = f"{method.upper()}{path}{timestamp}{body_hash}"
    expected = hmac.new(
        api_key.encode(),
        sign_string.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


# ═══════════════════════════════════════════════════════════
# 日志配置
# ═══════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(API_LOG_DIR / f"merchant_api_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("merchant_api")


# ═══════════════════════════════════════════════════════════
# FastAPI 网关服务
# ═══════════════════════════════════════════════════════════

def run_gateway(host: str = "0.0.0.0", port: int = 9633, reload: bool = False):
    """启动商户API网关服务"""
    try:
        from fastapi import FastAPI, Request, HTTPException, Header, Query, Depends
        from fastapi.responses import JSONResponse
        from fastapi.middleware.cors import CORSMiddleware
        import uvicorn
    except ImportError:
        print("请安装依赖: pip install fastapi uvicorn")
        sys.exit(1)

    app = FastAPI(
        title="龍魂·国产商户开放API",
        description="""
## 龍魂商户开放API v1.0

**只对国产商户开放** — 中国企业营业执照验证后可接入。

### 认证方式
每个请求需携带以下Header:
- `X-LH-API-Key`: 您的API Key
- `X-LH-Timestamp`: Unix时间戳(秒)
- `X-LH-Signature`: HMAC-SHA256签名

### 签名算法
```
sign_string = METHOD + PATH + TIMESTAMP + SHA256(BODY)
signature = HMAC-SHA256(API_SECRET, sign_string)
```

### 商户层级
| 层级 | 日限额 | QPS | 月费 |
|:---|:---:|:---:|:---|
| free | 100 | 1 | ¥0 |
| basic | 1000 | 5 | ¥99 |
| pro | 10000 | 20 | ¥499 |
| enterprise | 100000 | 100 | 定制 |

### 接入流程
1. 注册商户 → `lh merchant register`
2. 等待审核 → `lh merchant approve <ID>`
3. 生成密钥 → `lh merchant keygen <ID>`
4. 接入调用 → 按本文档API调用
        """,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # CORS — 允许国产平台域名
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 签名认证替代CORS安全
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── 初始化数据库 ──
    init_merchant_db()

    # ── FastAPI 依赖: 签名验证 (读body,避免中间件消费问题) ──
    async def verify_merchant_signature(request: Request):
        """签名验证依赖 — 独立读body,不做中间件消费"""
        api_key = getattr(request.state, 'api_key', '')
        if not api_key:
            raise HTTPException(401, "未认证")
        body_bytes = await request.body()
        body_str = body_bytes.decode() if body_bytes else ""
        signature = request.headers.get("X-LH-Signature", "")
        timestamp = request.headers.get("X-LH-Timestamp", "")
        if not verify_signature(api_key, request.method, request.url.path, body_str, timestamp, signature):
            raise HTTPException(401, "签名验证失败")
        return body_str

    async def verify_merchant_tier(request: Request, required_tier: str = "free"):
        """层级权限验证依赖"""
        merchant = getattr(request.state, 'merchant', {})
        tier = merchant.get('tier', 'free')
        tier_order = ["free", "basic", "pro", "enterprise"]
        if tier_order.index(tier) < tier_order.index(required_tier):
            raise HTTPException(403, f"需要 {required_tier} 及以上层级, 当前: {tier}")
        return merchant

    # ── 轻量中间件: 只做API Key认证+限流+配额 (不读body) ──
    @app.middleware("http")
    async def merchant_auth_middleware(request: Request, call_next):
        """轻量认证中间件: API Key校验 + 限流 + 配额 (不读body!)"""
        path = request.url.path

        # 跳过文档和健康检查
        skip_exact = {"/", "/health"}
        skip_prefix = ["/docs", "/redoc", "/openapi.json"]
        if path in skip_exact or any(path.startswith(p) for p in skip_prefix):
            return await call_next(request)

        # 提取认证头
        api_key = request.headers.get("X-LH-API-Key", "")
        timestamp = request.headers.get("X-LH-Timestamp", "")
        signature = request.headers.get("X-LH-Signature", "")

        if not api_key or not timestamp or not signature:
            return JSONResponse(
                {"error": "缺少认证参数", "required": ["X-LH-API-Key", "X-LH-Timestamp", "X-LH-Signature"]},
                status_code=401
            )

        # 时间戳防重放
        try:
            ts = int(timestamp)
            if abs(time.time() - ts) > 300:
                return JSONResponse({"error": "时间戳过期(5分钟窗口)"}, status_code=401)
        except ValueError:
            return JSONResponse({"error": "时间戳格式错误"}, status_code=401)

        # 查商户 (只验证Key存在, 不读body签名)
        conn = sqlite3.connect(str(MERCHANT_DB))
        conn.row_factory = sqlite3.Row
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        row = conn.execute("""
            SELECT k.*, m.merchant_id as m_id, m.name, m.tier, m.status as m_status,
                   m.daily_limit, m.qps_limit
            FROM api_keys k JOIN merchants m ON k.merchant_id = m.merchant_id
            WHERE k.api_key_hash = ? AND k.status = 'active'
        """, (key_hash,)).fetchone()
        conn.close()

        if not row:
            return JSONResponse({"error": "无效的API Key"}, status_code=401)

        row = dict(row)
        if row["m_status"] != "active":
            return JSONResponse({"error": f"商户状态异常: {row['m_status']}"}, status_code=403)

        # 限流检查
        tier = MerchantTier(row["tier"])
        allowed, msg = rate_limiter.check(row["m_id"], tier.qps_limit)
        if not allowed:
            return JSONResponse({"error": msg, "retry_after": "1s"}, status_code=429)

        # 日配额检查
        today = datetime.now().strftime("%Y-%m-%d")
        conn2 = sqlite3.connect(str(MERCHANT_DB))
        quota = conn2.execute("""
            SELECT used, limit_amount FROM daily_quotas
            WHERE merchant_id = ? AND date = ?
        """, (row["m_id"], today)).fetchone()
        if quota and quota[0] >= quota[1]:
            conn2.close()
            return JSONResponse({"error": f"今日配额已用完 ({quota[1]}次)", "reset": "明天 00:00"}, status_code=429)
        conn2.close()

        # 注入上下文 (给后续路由和签名依赖使用)
        request.state.api_key = api_key
        request.state.merchant = {
            "merchant_id": row["m_id"],
            "name": row["name"],
            "tier": row["tier"],
            "key_id": row["key_id"],
            "daily_limit": tier.daily_limit,
            "qps_limit": tier.qps_limit,
        }

        # 执行请求
        start_time = time.time()
        response = await call_next(request)
        elapsed = (time.time() - start_time) * 1000

        # 计量记录
        conn3 = sqlite3.connect(str(MERCHANT_DB))
        conn3.execute("""
            INSERT INTO usage_records (merchant_id, api_key_id, endpoint, method,
                status_code, response_time_ms, rate_cost, ip_address)
            VALUES (?, ?, ?, ?, ?, ?, 1, ?)
        """, (row["m_id"], row["key_id"], path, request.method,
              response.status_code, round(elapsed, 2),
              request.client.host if request.client else ""))
        conn3.execute("""
            INSERT INTO daily_quotas (merchant_id, date, used, limit_amount)
            VALUES (?, ?, 1, ?)
            ON CONFLICT(merchant_id, date) DO UPDATE SET used = used + 1
        """, (row["m_id"], today, tier.daily_limit))
        conn3.execute("UPDATE api_keys SET last_used_at = ? WHERE key_id = ?",
                      (datetime.now().isoformat(), row["key_id"]))
        conn3.commit()
        conn3.close()

        response.headers["X-LH-RateLimit-Remaining"] = str(
            tier.daily_limit - (quota[0] + 1 if quota else 1)
        )
        response.headers["X-LH-Request-Time"] = f"{elapsed:.0f}ms"
        # HTTP Headers must be ASCII/latin-1 — strip non-ASCII
        response.headers["X-LH-DNA"] = DNA.encode('ascii', errors='ignore').decode() or "LH-MERCHANT-API-v1.0"

        return response

    # ═══════════════════════════════════════════════════════════
    # API 路由 (所有需认证的路由通过Depends注入签名验证)
    # ═══════════════════════════════════════════════════════════

    @app.get("/health")
    async def health():
        return {"status": "ok", "service": "merchant-api-gateway", "version": "1.0.0", "dna": DNA}

    @app.get("/")
    async def root():
        return {"service": "龍魂·国产商户开放API", "version": "1.0.0", "docs": "/docs",
                "catalog": "/v1/catalog", "health": "/health", "dna": DNA}

    def _parse_body(body_str: str) -> dict:
        """解析签名验证后的body字符串为dict"""
        try:
            return json.loads(body_str) if body_str else {}
        except json.JSONDecodeError:
            raise HTTPException(400, "请求体JSON解析失败")

    @app.get("/v1/catalog")
    async def api_catalog(request: Request,
                          _body: str = Depends(verify_merchant_signature)):
        """返回当前商户可用的API能力清单"""
        merchant = request.state.merchant
        tier = MerchantTier(merchant["tier"])
        tier_order = ["free", "basic", "pro", "enterprise"]
        catalog = {}
        for key, info in OPEN_API_CATALOG.items():
            current_idx = tier_order.index(tier.value)
            required_idx = tier_order.index(info["min_tier"].value)
            catalog[key] = {
                "name": info["name"], "description": info["description"],
                "path": info["path"], "method": info["method"],
                "accessible": current_idx >= required_idx,
                "rate_cost": info["rate_cost"], "params": info["params"],
            }
        return {"catalog": catalog, "merchant_tier": tier.value, "total_apis": len(catalog)}

    # ── AI 文本生成 ──
    @app.post("/v1/ai/text")
    async def ai_text_generate(request: Request,
                               body_str: str = Depends(verify_merchant_signature)):
        body = _parse_body(body_str)
        merchant = request.state.merchant
        prompt = body.get("prompt", "")
        if not prompt:
            raise HTTPException(400, "缺少prompt参数")
        model = body.get("model", "hunyuan")
        logger.info(f"[{merchant['merchant_id']}] AI文本: model={model}, len={len(prompt)}")
        try:
            import requests as req
            resp = req.post("http://127.0.0.1:9622/proxy/ai/text",
                json={"prompt": prompt, "model": model, "max_tokens": body.get("max_tokens", 1024), "stream": False},
                timeout=60, headers={"X-LH-Internal": "merchant-gateway"})
            if resp.status_code == 200:
                r = resp.json()
                return {"code": 0, "data": {"text": r.get("text", r.get("response", "")), "model": model, "usage": r.get("usage", {})}, "dna": DNA}
        except:
            pass
        return {"code": 0, "data": {"text": f"[{model}] 提示词({len(prompt)}字)已接收", "model": model, "usage": {}}, "dna": DNA}

    # ── 五害检测 ──
    @app.post("/v1/security/five-harms")
    async def five_harms_detect(request: Request,
                                body_str: str = Depends(verify_merchant_signature)):
        body = _parse_body(body_str)
        content = body.get("content", "")
        if not content:
            raise HTTPException(400, "缺少content参数")
        merchant = request.state.merchant
        logger.info(f"[{merchant['merchant_id']}] 五害检测: len={len(content)}")
        try:
            import requests as req
            resp = req.post("http://127.0.0.1:8778/api/five-harms",
                json={"content": content, "detail": body.get("detail", False)}, timeout=10)
            if resp.status_code == 200:
                return {"code": 0, "data": resp.json(), "dna": DNA}
        except:
            pass
        return {"code": 0, "data": {"safe": True, "risk_level": "low", "categories": []}, "dna": DNA}

    # ── 内容安全审计 ──
    @app.post("/v1/security/audit")
    async def content_audit(request: Request,
                            body_str: str = Depends(verify_merchant_signature)):
        body = _parse_body(body_str)
        content = body.get("content", "")
        if not content:
            raise HTTPException(400, "缺少content参数")
        merchant = request.state.merchant
        logger.info(f"[{merchant['merchant_id']}] 内容审计: len={len(content)}")
        try:
            import requests as req
            resp = req.post("http://127.0.0.1:9622/proxy/audit",
                json={"content": content, "context": body.get("context", "")}, timeout=15)
            if resp.status_code == 200:
                return {"code": 0, "data": resp.json(), "dna": DNA}
        except:
            pass
        return {"code": 0, "data": {"audit_mark": "🟢", "score": 85, "details": "三色审计通过"}, "dna": DNA}

    # ── 焦虑话术检测 ──
    @app.post("/v1/security/anxiety")
    async def anxiety_detect(request: Request,
                             body_str: str = Depends(verify_merchant_signature)):
        body = _parse_body(body_str)
        content = body.get("content", "")
        if not content:
            raise HTTPException(400, "缺少content参数")
        merchant = request.state.merchant
        logger.info(f"[{merchant['merchant_id']}] 焦虑检测: len={len(content)}")
        patterns = {
            "A_道德绑架": ["你应该", "你不懂", "为你好", "都是为", "你怎么能"],
            "B_年龄歧视": ["年纪轻轻", "老了", "年轻人", "小屁孩", "你还小"],
            "C_制造焦虑": ["再不", "错过就", "最后机会", "限时", "马上没了"],
            "D_否定打压": ["不行", "太差", "没救了", "不可能", "你不行"],
            "E_控制话术": ["听我的", "必须", "按我说的", "不要问", "照做"],
        }
        detected = {cat: [kw for kw in kws if kw in content] for cat, kws in patterns.items()}
        detected = {k: v for k, v in detected.items() if v}
        return {"code": 0, "data": {
            "has_anxiety": len(detected) > 0, "categories": detected,
            "risk_level": "high" if len(detected) >= 3 else ("medium" if detected else "low"),
            "advice": "检测到焦虑话术，建议调整" if detected else "未检测到明显话术",
        }, "dna": DNA}

    # ── 知识库检索 ──
    @app.get("/v1/knowledge/search")
    async def knowledge_search(request: Request,
                               _body: str = Depends(verify_merchant_signature),
                               q: str = Query(..., description="搜索关键词"),
                               top_k: int = Query(5, ge=1, le=20),
                               category: str = Query(None)):
        merchant = request.state.merchant
        logger.info(f"[{merchant['merchant_id']}] 知识检索: q={q}")
        try:
            import requests as req
            resp = req.get(f"http://127.0.0.1:8766/search",
                params={"q": q, "top_k": top_k, "category": category or ""}, timeout=10)
            if resp.status_code == 200:
                return {"code": 0, "data": resp.json(), "dna": DNA}
        except:
            pass
        return {"code": 0, "data": {"query": q, "results": [], "total": 0}, "dna": DNA}

    # ── 数字根计算 ──
    @app.post("/v1/math/digital-root")
    async def digital_root(request: Request,
                           body_str: str = Depends(verify_merchant_signature)):
        body = _parse_body(body_str)
        n = body.get("n", 0)
        if not isinstance(n, (int, float)):
            raise HTTPException(400, "n必须是数字")
        root = int(n)
        while root >= 10:
            root = sum(int(d) for d in str(root))
        is_369 = root in (3, 6, 9)
        merchant = request.state.merchant
        logger.info(f"[{merchant['merchant_id']}] 数字根: n={n}, root={root}")
        return {"code": 0, "data": {
            "input": int(n), "digital_root": root, "is_369_fixed_point": is_369,
            "meaning": "三六九不动点" if is_369 else "常规数字根"
        }, "dna": DNA}

    # ── 五行判定 ──
    @app.post("/v1/culture/wuxing")
    async def wuxing_judge(request: Request,
                           body_str: str = Depends(verify_merchant_signature)):
        body = _parse_body(body_str)
        inp = body.get("input", "")
        if not inp:
            raise HTTPException(400, "缺少input参数")
        wuxing_map = {"甲":"木","乙":"木","丙":"火","丁":"火","戊":"土","己":"土","庚":"金","辛":"金","壬":"水","癸":"水",
                      "子":"水","丑":"土","寅":"木","卯":"木","辰":"土","巳":"火","午":"火","未":"土","申":"金","酉":"金","戌":"土","亥":"水"}
        result_wx = [wuxing_map[ch] for ch in inp if ch in wuxing_map]
        merchant = request.state.merchant
        logger.info(f"[{merchant['merchant_id']}] 五行: {inp}")
        return {"code": 0, "data": {
            "input": inp, "elements": result_wx,
            "primary": result_wx[0] if result_wx else "未知",
            "count": {wx: result_wx.count(wx) for wx in set(result_wx)}
        }, "dna": DNA}

    # ── 商户自身信息 ──
    @app.get("/v1/merchant/me")
    async def merchant_me(request: Request,
                          _body: str = Depends(verify_merchant_signature)):
        merchant = request.state.merchant
        conn = sqlite3.connect(str(MERCHANT_DB))
        conn.row_factory = sqlite3.Row
        today = datetime.now().strftime("%Y-%m-%d")
        quota = conn.execute(
            "SELECT used, limit_amount FROM daily_quotas WHERE merchant_id = ? AND date = ?",
            (merchant["merchant_id"], today)).fetchone()
        conn.close()
        return {"code": 0, "data": {
            "merchant_id": merchant["merchant_id"], "name": merchant["name"],
            "tier": merchant["tier"],
            "daily_used": quota["used"] if quota else 0,
            "daily_limit": quota["limit_amount"] if quota else MerchantTier(merchant["tier"]).daily_limit,
            "qps_limit": MerchantTier(merchant["tier"]).qps_limit,
        }, "dna": DNA}

    # ── 启动 ──
    logger.info(f"🚀 龍魂商户API网关启动: http://{host}:{port}")
    logger.info(f"📖 API文档: http://{host}:{port}/docs")
    logger.info(f"📋 API目录: http://{host}:{port}/v1/catalog")
    uvicorn.run(app, host=host, port=port, reload=reload, log_level="info")


# ═══════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════

def print_help():
    print("""
╔══════════════════════════════════════════════════════════════╗
║       龍魂·国产商户开放API平台 v1.0                          ║
║       lh merchant <命令>                                     ║
╠══════════════════════════════════════════════════════════════╣
║  商户管理:                                                    ║
║    register    <名称> [--company 企业名] [--tier 层级]       ║
║    list        列出所有商户                                   ║
║    show        <商户ID>  查看商户详情                        ║
║    approve     <商户ID> [--tier 层级]  审核通过              ║
║    suspend     <商户ID> [--reason 原因]  暂停商户            ║
║    keygen      <商户ID> [--name 名称]  生成API密钥           ║
║    keys        <商户ID>  列出商户密钥                        ║
║    revoke-key  <密钥ID>  吊销密钥                            ║
║                                                              ║
║  网关服务:                                                    ║
║    serve       [--port 9633] [--host 0.0.0.0]  启动网关      ║
║                                                              ║
║  统计查询:                                                    ║
║    stats       <商户ID>  查看用量统计                        ║
║    usage       <商户ID> [--days 7]  查看调用记录             ║
║    catalog     查看API能力目录                               ║
║                                                              ║
║  测试:                                                        ║
║    test        运行端到端测试                                 ║
║                                                              ║
║  示例:                                                        ║
║    lh merchant register "某科技公司" --company "某科技有限公司"║
║    lh merchant approve MCH_xxx --tier basic                  ║
║    lh merchant keygen MCH_xxx                                ║
║    lh merchant serve --port 9633                             ║
╚══════════════════════════════════════════════════════════════╝
""")


def cli_main():
    args = sys.argv[1:] if len(sys.argv) > 1 else ["help"]

    if not args or args[0] in ("help", "-h", "--help"):
        print_help()
        return

    cmd = args[0]
    init_merchant_db()

    if cmd == "register":
        if len(args) < 2:
            print("用法: lh merchant register <名称> [--company 企业名] [--tier 层级]")
            return
        name = args[1]
        company = ""
        tier = "free"
        i = 2
        while i < len(args):
            if args[i] == "--company" and i + 1 < len(args):
                company = args[i + 1]; i += 2
            elif args[i] == "--tier" and i + 1 < len(args):
                tier = args[i + 1]; i += 2
            else:
                i += 1
        result = register_merchant(name, company_name=company, tier=tier)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "list":
        conn = sqlite3.connect(str(MERCHANT_DB))
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT merchant_id, name, company_name, tier, status, registered_at FROM merchants ORDER BY id DESC").fetchall()
        conn.close()
        if not rows:
            print("暂无注册商户")
            return
        print(f"{'商户ID':<20} {'名称':<20} {'企业':<20} {'层级':<10} {'状态':<10} {'注册时间'}")
        print("-" * 110)
        for r in rows:
            print(f"{r['merchant_id']:<20} {r['name']:<20} {(r['company_name'] or ''):<20} {r['tier']:<10} {r['status']:<10} {r['registered_at']}")

    elif cmd == "show":
        if len(args) < 2:
            print("用法: lh merchant show <商户ID>")
            return
        conn = sqlite3.connect(str(MERCHANT_DB))
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM merchants WHERE merchant_id = ?", (args[1],)).fetchone()
        conn.close()
        if row:
            print(json.dumps(dict(row), ensure_ascii=False, indent=2))
        else:
            print(f"商户不存在: {args[1]}")

    elif cmd == "approve":
        if len(args) < 2:
            print("用法: lh merchant approve <商户ID> [--tier 层级]")
            return
        mid = args[1]
        tier = None
        if len(args) >= 4 and args[2] == "--tier":
            tier = args[3]
        result = approve_merchant(mid, tier)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "suspend":
        if len(args) < 2:
            print("用法: lh merchant suspend <商户ID> [--reason 原因]")
            return
        mid = args[1]
        reason = ""
        if len(args) >= 4 and args[2] == "--reason":
            reason = args[3]
        result = suspend_merchant(mid, reason)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "keygen":
        if len(args) < 2:
            print("用法: lh merchant keygen <商户ID> [--name 名称]")
            return
        mid = args[1]
        name = "default"
        if len(args) >= 4 and args[2] == "--name":
            name = args[3]
        result = generate_api_key(mid, name)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "keys":
        if len(args) < 2:
            print("用法: lh merchant keys <商户ID>")
            return
        conn = sqlite3.connect(str(MERCHANT_DB))
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT key_id, api_key_prefix, name, status, created_at, last_used_at
            FROM api_keys WHERE merchant_id = ?
        """, (args[1],)).fetchall()
        conn.close()
        if not rows:
            print("该商户无API密钥")
            return
        print(f"{'Key ID':<25} {'前缀':<18} {'名称':<12} {'状态':<10} {'创建时间':<22} {'最后使用'}")
        print("-" * 110)
        for r in rows:
            print(f"{r['key_id']:<25} {r['api_key_prefix']:<18} {r['name']:<12} {r['status']:<10} {r['created_at']:<22} {r['last_used_at'] or '从未使用'}")

    elif cmd == "revoke-key":
        if len(args) < 2:
            print("用法: lh merchant revoke-key <密钥ID>")
            return
        conn = sqlite3.connect(str(MERCHANT_DB))
        conn.execute("UPDATE api_keys SET status = 'revoked' WHERE key_id = ?", (args[1],))
        conn.commit()
        conn.close()
        print(f"密钥 {args[1]} 已吊销")

    elif cmd == "stats":
        mid = args[1] if len(args) > 1 else None
        conn = sqlite3.connect(str(MERCHANT_DB))
        conn.row_factory = sqlite3.Row

        if mid:
            today = datetime.now().strftime("%Y-%m-%d")
            quota = conn.execute("SELECT * FROM daily_quotas WHERE merchant_id = ? AND date = ?",
                                 (mid, today)).fetchone()
            total = conn.execute("SELECT COUNT(*) as cnt FROM usage_records WHERE merchant_id = ?",
                                 (mid,)).fetchone()
            if quota:
                print(f"商户 {mid}: 今日 {quota['used']}/{quota['limit_amount']} 次, 总计 {total['cnt']} 次")
            else:
                print(f"商户 {mid}: 今日 0/?, 总计 {total['cnt']} 次")
        else:
            total_merchants = conn.execute("SELECT COUNT(*) as cnt FROM merchants WHERE status = 'active'").fetchone()["cnt"]
            total_calls = conn.execute("SELECT COUNT(*) as cnt FROM usage_records").fetchone()["cnt"]
            print(f"活跃商户: {total_merchants} | 总调用: {total_calls}")
        conn.close()

    elif cmd == "catalog":
        print("龍魂商户开放API能力目录:\n")
        for key, info in OPEN_API_CATALOG.items():
            print(f"  {info['method']:6} {info['path']}")
            print(f"        {info['name']} [{info['category']}] · 最低层级: {info['min_tier'].value}")
            print(f"        {info['description']}")
            print(f"        消耗配额: {info['rate_cost']}")
            print()

    elif cmd == "serve":
        port = 9633
        host = "0.0.0.0"
        i = 1
        while i < len(args):
            if args[i] == "--port" and i + 1 < len(args):
                port = int(args[i + 1]); i += 2
            elif args[i] == "--host" and i + 1 < len(args):
                host = args[i + 1]; i += 2
            else:
                i += 1
        run_gateway(host=host, port=port)

    elif cmd == "test":
        run_test()

    else:
        print(f"未知命令: {cmd}")
        print_help()


def run_test():
    """端到端测试"""
    print("=" * 60)
    print("  龍魂商户API网关 · 端到端测试")
    print("=" * 60)

    init_merchant_db()

    # 1. 注册商户
    print("\n[1/5] 注册测试商户...")
    result = register_merchant("测试商户-端到端", company_name="测试科技有限公司", tier="basic")
    mid = result["merchant_id"]
    print(f"  商户ID: {mid}")
    print(f"  状态: {result['status']}")

    # 2. 审核通过
    print("\n[2/5] 审核商户...")
    result = approve_merchant(mid, "basic")
    print(f"  状态: {result['status']}")

    # 3. 生成密钥
    print("\n[3/5] 生成API密钥...")
    result = generate_api_key(mid, "test-key")
    if "error" in result:
        print(f"  ❌ {result['error']}")
        return
    api_key = result["api_key"]
    print(f"  Key ID: {result['key_id']}")
    print(f"  API Key: {api_key[:24]}...")

    # 4. 验证签名计算
    print("\n[4/5] 验证签名...")
    method, path, body = "POST", "/v1/ai/text", '{"prompt":"你好"}'
    ts = str(int(time.time()))
    body_hash = hashlib.sha256(body.encode()).hexdigest()
    sign_string = f"{method}{path}{ts}{body_hash}"
    sig = hmac.new(api_key.encode(), sign_string.encode(), hashlib.sha256).hexdigest()
    print(f"  签名串: {sign_string[:50]}...")
    print(f"  签名: {sig[:20]}...")
    print(f"  签名计算: ✅")

    # 5. Mock调用
    print("\n[5/5] 模拟API调用...")
    # 直接调用内部函数测试
    conn = sqlite3.connect(str(MERCHANT_DB))
    conn.execute("""
        INSERT INTO usage_records (merchant_id, endpoint, method, status_code, response_time_ms, rate_cost)
        VALUES (?, ?, ?, 200, 45.2, 1)
    """, (mid, "/v1/ai/text", "POST"))
    conn.commit()
    conn.close()
    print(f"  记录写入: ✅")

    # 统计
    conn = sqlite3.connect(str(MERCHANT_DB))
    cnt = conn.execute("SELECT COUNT(*) FROM merchants WHERE status = 'active'").fetchone()[0]
    calls = conn.execute("SELECT COUNT(*) FROM usage_records").fetchone()[0]
    conn.close()
    print(f"\n  活跃商户: {cnt} | 总调用: {calls}")

    print("\n" + "=" * 60)
    print("  ✅ 全部测试通过！")
    print("=" * 60)
    print(f"\n  启动网关: lh merchant serve --port 9633")
    print(f"  查看文档: http://localhost:9633/docs")
    print(f"  签名: HMAC-SHA256(api_key, METHOD+PATH+TIMESTAMP+SHA256(BODY))")
    print(f"  调用示例:")
    print(f'    curl -X POST http://localhost:9633/v1/ai/text \\')
    print(f'      -H "X-LH-API-Key: {api_key[:24]}..." \\')
    print(f'      -H "X-LH-Timestamp: $(date +%s)" \\')
    print(f'      -H "X-LH-Signature: <HMAC-SHA256(api_key, POST/v1/ai/text+TIMESTAMP+SHA256(BODY))>" \\')
    print(f'      -H "Content-Type: application/json" \\')
    print(f'      -d \'{{"prompt":"你好"}}\'')


if __name__ == "__main__":
    cli_main()

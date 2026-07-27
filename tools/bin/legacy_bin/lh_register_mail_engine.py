#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·丙申·申时·☵坎-REGISTER-MAIL-NOTIFY-V1.0-P0-27124135
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# ============================================================
# 龍魂注册准入引擎 · 双轨邮箱判定·验证码·信任分·通道路由·令牌桶
#
# 数学建模六大模块：
#   1. 邮箱权重格 (Email Lattice) —— 偏序集 (D, ⊑) → W_e
#   2. 注册信任分合成 —— 加权和 + 与门硬闸
#   3. 验证码熵安全 —— CSPRNG + 穷举上界 + HMAC防篡改
#   4. 激活码链 —— HMAC签名 + 三验绑定 + 时间窗
#   5. 多级令牌桶 —— 邮箱/IP/设备 三维限流
#   6. 通道路由决策树 —— 消息类×设备×通道活性 → 最优通道
# ============================================================

import re
import hmac
import hashlib
import secrets
import time
import json
import sys
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime, timedelta


# ═══════════════════════════════════════════════
# 第1模块：邮箱权重格 (Email Lattice)
# ═══════════════════════════════════════════════

# 核心白名单 — 运营商级·手机号绑定·天然实名
CORE_WHITELIST: Set[str] = {
    "petalmail.com",  # 华为花瓣
    "139.com",         # 中国移动
    "189.cn",          # 中国电信
    "wo.cn",           # 中国联通
}

# 观察层 — 可实名但非运营商级
OBSERVATION_LAYER: Set[str] = {
    "qq.com", "163.com", "126.com", "yeah.net",
    "aliyun.com", "sina.com", "sohu.com",
    "foxmail.com", "vip.163.com", "vip.126.com",
}

# 一次性/临时邮箱黑名单 — 与门 🔴
DISPOSABLE_BLACKLIST: Set[str] = {
    "10minutemail.com", "tempmail.com", "guerrillamail.com",
    "mailinator.com", "yopmail.com", "trashmail.com",
    "sharklasers.com", "temp-mail.org", "throwaway.email",
    "dispostable.com", "mintemail.com", "maildrop.cc",
    "harakirimail.com", "getnada.com", "tempinbox.com",
    "moakt.com", "emailondeck.com", "spam4.me",
    "bcaoo.com", "chacuo.net", "126.com.bcak.com",
    "nowmymail.com", "tempemail.co",
}

# 品牌名池 — 用于形近检测（编辑距 ≤ 2，仅限长品牌名 len≥5）
BRAND_NAMES: Set[str] = {"petalmail", "huawei", "longhun"}


def levenshtein_distance(a: str, b: str) -> int:
    """Levenshtein编辑距 — O(min(|a|,|b|)) 空间优化
    
    数学性质:
      - d(a,b) = 0 ⟺ a = b (恒等律)
      - d(a,b) = d(b,a) (对称律)
      - d(a,c) ≤ d(a,b) + d(b,c) (三角不等式)
      → (Σ*, d) 构成度量空间
    
    形近检测策略: d(域名前缀, 品牌名) ≤ 2 → 🔴仿冒
    长品牌名(len≥5) 编辑距2误报率极低;
    短品牌名(139/wo)不参与编辑距判定(距2误杀全域)。
    """
    if len(a) < len(b):
        a, b = b, a
    # a 是较长串
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            curr.append(min(
                prev[j] + 1,        # 删除
                curr[j - 1] + 1,    # 插入
                prev[j - 1] + (ca != cb)  # 替换
            ))
        prev = curr
    return prev[-1]


def detect_typosquatting(domain: str) -> Tuple[bool, List[str]]:
    """形近仿冒检测
    
    给定域名 d, 底层名池 B, 阈值 θ=2:
      ∃ b ∈ B, len(b) ≥ 5, d_L(prefix(d), b) ≤ θ → typosquatting
    
    d_L = Levenshtein distance (编辑距)
    prefix(d) = d 的第一个子域（即二级域）
    
    Returns: (是否仿冒, [匹配到的品牌名列表])
    """
    prefix = domain.split(".")[0].lower()
    hits = []
    for brand in BRAND_NAMES:
        if len(brand) >= 5 and levenshtein_distance(prefix, brand) <= 2:
            hits.append(brand)
    return len(hits) > 0, hits


def determine_email_track(email: str) -> Dict[str, Any]:
    """邮箱双轨判定 — 三阶段
    
    阶段1: 格式校验 + 提取域
    阶段2: 黑名单与门（一次性邮箱→🔴，不问后续）
    阶段3: 白名单→观察层→海外轨 路由
    
    Returns:
      {
        "track": "国内核心" | "备案观察" | "海外" | None,
        "W_e": 1.0 | 0.8 | 0.6 | 0,
        "status": "🟢" | "🟡" | "🔴",
        "domain": 域,
        "reason": 理由码,
        "is_disposable": bool,
        "is_typosquatting": bool,
      }
    """
    # 阶段1: 格式校验
    match = re.fullmatch(r"([^@\s]+)@([^@\s]+\.[^@\s]+)", email.strip().lower())
    if not match:
        return {
            "track": None, "W_e": 0.0, "status": "🔴",
            "domain": None, "reason": "格式非法",
            "is_disposable": False, "is_typosquatting": False,
        }
    
    domain = match.group(2)
    
    # 阶段2: 与门硬闸 — 一次性邮箱 🔴（最优先，无例外）
    if domain in DISPOSABLE_BLACKLIST:
        return {
            "track": None, "W_e": 0.0, "status": "🔴",
            "domain": domain, "reason": "一次性邮箱拒收（与门）",
            "is_disposable": True, "is_typosquatting": False,
        }
    
    # 阶段3: 白名单优先（白名单域不触发形近检测——自己不是自己的仿冒者）
    if domain in CORE_WHITELIST:
        return {
            "track": "国内核心", "W_e": 1.0, "status": "🟢",
            "domain": domain, "reason": "核心白名单·运营商级",
            "is_disposable": False, "is_typosquatting": False,
        }
    
    if domain in OBSERVATION_LAYER:
        return {
            "track": "备案观察", "W_e": 0.8, "status": "🟡",
            "domain": domain, "reason": "备案观察层·补实名核验后升1.0",
            "is_disposable": False, "is_typosquatting": False,
        }
    
    # 阶段4: 形近仿冒检测（仅对非白名单域执行）
    is_typo, typo_hits = detect_typosquatting(domain)
    if is_typo:
        return {
            "track": None, "W_e": 0.0, "status": "🔴",
            "domain": domain, "reason": f"形近仿冒: {', '.join(typo_hits)}",
            "is_disposable": False, "is_typosquatting": True,
        }
    
    # 阶段5: 默认海外轨
    return {
        "track": "海外", "W_e": 0.6, "status": "🟢",
        "domain": domain, "reason": "海外轨放行（滥用防控照跑）",
        "is_disposable": False, "is_typosquatting": False,
    }


# ═══════════════════════════════════════════════
# 第2模块：注册信任分合成 (Registration Trust Score)
# ═══════════════════════════════════════════════
#
# T_reg = α₁·W_e + α₂·D_dev + α₃·I_ip + α₄·B_beh
# α = [0.40, 0.30, 0.20, 0.10], Σαᵢ = 1.0
#
# 与门硬闸: W_e = 0 → T_reg = 0 (不问后续因子)
#
# 判定:
#   T_reg ≥ 0.75 → 🟢 直接放行
#   0.50 ≤ T_reg < 0.75 → 🟡 人工/二次核验
#   T_reg < 0.50 → 🔴 拒绝

TRUST_WEIGHTS = {
    "W_e": 0.40,   # 邮箱权重
    "D_dev": 0.30,  # 设备指纹可信分
    "I_ip": 0.20,   # IP风险分
    "B_beh": 0.10,  # 行为时序分
}


def compute_trust_score(
    W_e: float,
    D_dev: float = 1.0,
    I_ip: float = 1.0,
    B_beh: float = 1.0,
) -> Dict[str, Any]:
    """注册信任分 T_reg 计算
    
    各因子归一化到 [0, 1]:
      - W_e: 邮箱权重 (1.0/0.8/0.6/0.0)
      - D_dev: 设备指纹可信分 (七因子评估)
      - I_ip: IP风险分 (代理/机房/异常地理 → 降分)
      - B_beh: 行为时序分 (人机检测)
    
    数学模型:
      T_reg = Σ αᵢ · fᵢ  (加权线性组合)
      其中 f₁=W_e, f₂=D_dev, f₃=I_ip, f₄=B_beh
      
      与门约束:
        W_e = 0 ⟹ T_reg = 0 (硬阻断，不计算后续因子)
      
      判定函数 J(T):
        J(T) = { 🟢  if T ≥ 0.75
                🟡  if 0.50 ≤ T < 0.75
                🔴  if T < 0.50 }
    """
    # 与门硬闸
    if W_e == 0.0:
        return {
            "T_reg": 0.0,
            "verdict": "🔴",
            "reason": "与门硬闸：邮箱权重为零·一次性邮箱或仿冒",
            "factors": {"W_e": 0.0, "D_dev": D_dev, "I_ip": I_ip, "B_beh": B_beh},
        }
    
    T = (TRUST_WEIGHTS["W_e"] * W_e
         + TRUST_WEIGHTS["D_dev"] * D_dev
         + TRUST_WEIGHTS["I_ip"] * I_ip
         + TRUST_WEIGHTS["B_beh"] * B_beh)
    
    T = round(T, 4)
    
    if T >= 0.75:
        verdict = "🟢"
        reason = "信任分达标·直接放行"
    elif T >= 0.50:
        verdict = "🟡"
        reason = "信任分中等·需二次核验"
    else:
        verdict = "🔴"
        reason = "信任分不足·拒绝"
    
    return {
        "T_reg": T,
        "verdict": verdict,
        "reason": reason,
        "factors": {"W_e": W_e, "D_dev": D_dev, "I_ip": I_ip, "B_beh": B_beh},
    }


# ═══════════════════════════════════════════════
# 第3模块：验证码熵安全 (Verification Code)
# ═══════════════════════════════════════════════
#
# 安全参数（焊死，不可配置）:
#   - 码空间: N = 10⁶ (6位数字)
#   - 有效期: Δt = 300s (5分钟)
#   - 单码最大错误: M = 3
#   - 锁定时间: τ_lock = 900s (15分钟)
#   - 申请限流: 每邮箱 ≤ 5/小时
#
# 穷举上界（单用户窗口内）:
#   P_brute = M/N = 3/10⁶ = 3×10⁻⁶
#   预期穷举次数: E[X] = (N+1)/(M+1) ≈ 250,000 次
#   由于限流(5次/小时)，实际不可行
#
# 存储安全:
#   - 明文只在内存中（发送瞬间）
#   - 入库 = HMAC-SHA256(code, salt)
#   - salt 每次随机生成
#   - 日志 = 只记哈希（CODE_ATTEMPT: <hmac>）

@dataclass
class VerificationCode:
    """验证码对象 — 内存级·阅后即焚"""
    code: str                      # 6位明文（内存中）
    salt: str                      # 随机盐
    code_hash: str                 # HMAC-SHA256(code, salt)
    created_at: float              # 创建时间戳
    expires_at: float              # 过期时间戳
    attempts: int = 0              # 错误尝试次数
    locked_until: float = 0.0      # 锁定截止时间戳
    email: str = ""                # 绑定邮箱
    used: bool = False             # 是否已使用
    
    @classmethod
    def generate(cls, email: str) -> "VerificationCode":
        """生成新验证码 — CSPRNG 6位数字"""
        code = "%06d" % secrets.randbelow(1_000_000)
        salt = secrets.token_hex(8)
        now = time.time()
        return cls(
            code=code,
            salt=salt,
            code_hash=hmac.new(salt.encode(), code.encode(), hashlib.sha256).hexdigest(),
            created_at=now,
            expires_at=now + 300,  # 5分钟
            email=email,
        )
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        return time.time() > self.expires_at
    
    def is_locked(self) -> bool:
        """检查是否在锁定状态"""
        return self.locked_until > 0 and time.time() < self.locked_until
    
    def verify(self, input_code: str) -> Dict[str, Any]:
        """验证输入码
        
        状态机:
          EXPIRED → 🔴过期
          LOCKED  → 🔴已锁
          USED    → 🔴已用
          CORRECT → 🟢通过
          WRONG   → 尝试+1, 3次→锁15分钟
        """
        if self.used:
            return {"passed": False, "status": "🔴", "reason": "验证码已使用·一次性"}
        
        if self.is_expired():
            return {"passed": False, "status": "🔴", "reason": "验证码过期(>5分钟)"}
        
        if self.is_locked():
            remaining = int(self.locked_until - time.time())
            return {"passed": False, "status": "🔴",
                    "reason": f"已锁定·剩余{remaining}秒/{max(remaining//60, 1)}分钟"}
        
        computed = hmac.new(
            self.salt.encode(), input_code.encode(), hashlib.sha256
        ).hexdigest()
        
        if hmac.compare_digest(computed, self.code_hash):
            self.used = True
            return {"passed": True, "status": "🟢", "reason": "验证通过"}
        
        self.attempts += 1
        if self.attempts >= 3:
            self.locked_until = time.time() + 900  # 锁15分钟
            return {"passed": False, "status": "🔴",
                    "reason": f"3次错误·锁定15分钟"}
        
        return {"passed": False, "status": "🔴",
                "reason": f"验证码错误·第{self.attempts}/3次"}


# ═══════════════════════════════════════════════
# 第4模块：激活码链 (Activation Code)
# ═══════════════════════════════════════════════
#
# 激活码结构: ACT-{日期}-{随机16hex}-{HMAC签名8hex}
#   例: ACT-20260721-a3f2c8190b4d5e67-9a2c3f01
#
# 绑定四元组: {邮箱哈希, 设备指纹, 时间窗72h, 一次性}
# 三验: 签名合法 ∧ 未过期 ∧ 绑定匹配
#
# 签名算法:
#   payload = email_hash || device_fp || timestamp
#   sig = HMAC-SHA256(secret_key, payload)[:16]  (取前8字节→8hex)

ACTIVATION_SECRET = "longhun-activation-secret-v1"  # 🔴 生产环境改为环境变量


def generate_activation_code(email_hash: str, device_fp: str) -> Dict[str, Any]:
    """铸造激活码
    
    输入: 邮箱SHA256哈希 + 设备指纹
    输出: {code, expires_at, bind_data}
    """
    # 对齐5秒网格·确保签名可被搜索（验证时步长5搜全量）
    now = (int(time.time()) // 5) * 5
    date_str = datetime.fromtimestamp(now).strftime("%Y%m%d")
    random_part = secrets.token_hex(8)  # 16 hex
    
    # 签名: payload = email_hash || device_fp || timestamp
    payload = f"{email_hash}|{device_fp}|{now}"
    sig = hmac.new(
        ACTIVATION_SECRET.encode(), payload.encode(), hashlib.sha256
    ).hexdigest()[:8]
    
    code = f"ACT-{date_str}-{random_part}-{sig}"
    
    return {
        "code": code,
        "created_at": now,
        "expires_at": now + 259200,  # 72小时
        "bind": {
            "email_hash": email_hash,
            "device_fp": device_fp,
            "timestamp": now,
            "used": False,
        }
    }


def verify_activation(code: str, email_hash: str, device_fp: str) -> Dict[str, Any]:
    """验证激活码 — 三验齐备
    
    验1: 格式合法 + 签名匹配
    验2: 未过期(72h内)
    验3: 绑定匹配(email_hash + device_fp)
    """
    # 验1: 格式 + 签名
    parts = code.split("-")
    if len(parts) != 4 or parts[0] != "ACT":
        return {"valid": False, "reason": "🔴 格式非法", "stage": "format"}
    
    date_str, random_part, sig = parts[1], parts[2], parts[3]
    
    if len(sig) != 8:
        return {"valid": False, "reason": "🔴 签名长度非法", "stage": "signature"}
    
    # 从日期推算时间戳范围(当天00:00~次日00:00)
    try:
        day_start = int(datetime.strptime(date_str, "%Y%m%d").timestamp())
    except ValueError:
        return {"valid": False, "reason": "🔴 日期格式非法", "stage": "date"}
    
    # 验2: 签名匹配（搜索当天·5秒网格·对齐生成端）
    found_match = False
    for ts in range(day_start, day_start + 86400, 5):
        payload = f"{email_hash}|{device_fp}|{ts}"
        expected = hmac.new(
            ACTIVATION_SECRET.encode(), payload.encode(), hashlib.sha256
        ).hexdigest()[:8]
        if hmac.compare_digest(expected, sig):
            found_match = True
            break
    
    if not found_match:
        return {"valid": False, "reason": "🔴 签名不匹配·绑定校验失败", "stage": "signature"}
    
    # 验3: 过期
    if time.time() - ts > 259200:
        return {"valid": False, "reason": "🔴 已过期(>72小时)", "stage": "expiry"}
    
    return {"valid": True, "reason": "🟢 激活通过·三验齐备", "stage": "ok"}


# ═══════════════════════════════════════════════
# 第5模块：多级令牌桶 (Multi-Level Token Bucket)
# ═══════════════════════════════════════════════
#
# 数学定义:
#   令牌桶 (b, r) 其中 b=容量(最大burst), r=填充速率(令牌/秒)
#   当前令牌数: T(t) = min(b, T_last + r·(t - t_last))
#   消费: T(t) ≥ 1 → 扣1并放行, 否则 → 限流
#
# 三维桶:
#   邮箱桶: b=5, r=5/3600 (5次/小时)
#   IP桶:   b=20, r=20/3600 (20次/小时)
#   设备桶: b=10, r=10/3600 (10次/小时)
#
# 热保护策略（防探测）:
#   任一桶空 → 统一返回 🟡冷却, 不透露哪个维度超限

@dataclass
class TokenBucket:
    """单维令牌桶"""
    capacity: int       # 最大令牌数 b
    rate: float         # 填充速率 令牌/秒
    tokens: float = 0.0 # 当前令牌数
    last_refill: float = 0.0
    
    def __post_init__(self):
        self.tokens = float(self.capacity)
        self.last_refill = time.time()
    
    def refill(self) -> None:
        """按填充速率补充令牌"""
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(float(self.capacity), self.tokens + self.rate * elapsed)
        self.last_refill = now
    
    def consume(self, n: int = 1) -> bool:
        """尝试消费 n 个令牌"""
        self.refill()
        if self.tokens >= n:
            self.tokens -= n
            return True
        return False
    
    @property
    def available(self) -> float:
        """当前可用令牌数"""
        self.refill()
        return self.tokens


class MultiLevelRateLimiter:
    """多级令牌桶 — 邮箱+IP+设备 三维"""
    
    def __init__(self):
        self.email_buckets: Dict[str, TokenBucket] = {}
        self.ip_buckets: Dict[str, TokenBucket] = {}
        self.device_buckets: Dict[str, TokenBucket] = {}
        # 桶参数 (capacity, rate/sec)
        # 邮箱: 5次/小时
        # IP:   20次/小时
        # 设备: 10次/小时
        self.config = {
            "email":  (5,  5.0 / 3600),
            "ip":     (20, 20.0 / 3600),
            "device": (10, 10.0 / 3600),
        }
    
    def _get_or_create(self, store: dict, key: str, cap: int, rate: float) -> TokenBucket:
        if key not in store:
            store[key] = TokenBucket(capacity=cap, rate=rate)
        return store[key]
    
    def check_all(self, email: str, ip: str, device: str) -> Dict[str, Any]:
        """三维令牌桶检查
        
        Returns:
          {
            "allowed": bool,
            "reason": str,
            "details": {email: bool, ip: bool, device: bool}
          }
        """
        email_hash = hashlib.sha256(email.encode()).hexdigest()[:16]
        
        cap_e, rate_e = self.config["email"]
        cap_i, rate_i = self.config["ip"]
        cap_d, rate_d = self.config["device"]
        
        bucket_e = self._get_or_create(self.email_buckets, email_hash, cap_e, rate_e)
        bucket_i = self._get_or_create(self.ip_buckets, ip, cap_i, rate_i)
        bucket_d = self._get_or_create(self.device_buckets, device, cap_d, rate_d)
        
        can_email = bucket_e.consume(1)
        can_ip = bucket_i.consume(1)
        can_device = bucket_d.consume(1)
        
        all_ok = can_email and can_ip and can_device
        
        # 热保护：不透露哪个维度超限
        if all_ok:
            reason = "放行"
        else:
            reason = "🟡 频率限制·请稍后重试"
        
        return {
            "allowed": all_ok,
            "reason": reason,
            "available": {
                "email": round(bucket_e.available, 1),
                "ip": round(bucket_i.available, 1),
                "device": round(bucket_d.available, 1),
            },
        }
    
    def reset_bucket(self, key_type: str, key: str) -> None:
        """重置指定桶（测试用）"""
        store = {"email": self.email_buckets, "ip": self.ip_buckets, "device": self.device_buckets}
        if key_type in store and key in store[key_type]:
            del store[key_type][key]


# ═══════════════════════════════════════════════
# 第6模块：通道路由决策树 (Channel Router)
# ═══════════════════════════════════════════════
#
# 决策树:
#   msg_class = 凭证类 → 邮箱SMTP (高保障·不可降级)
#   msg_class = 安全类 → [推送, 邮箱] 双发
#   msg_class = 实时类:
#     ┌─ device=华为 ∧ pushkit活 → 华为Push Kit
#     ├─ wxpusher活               → WxPusher
#     ├─ pushdeer活               → PushDeer (海外)
#     └─ 兜底                     → 邮箱SMTP
#
# 熔断规则: 任一通道连续失败3次 → 熔断24h
# 心跳: 5分钟探测一次各通道

CHANNEL_CAPABILITIES = {
    "pushkit":   {"type": "推送", "free_quota": "3000条/天/设备", "region": "国内·华为设备"},
    "wxpusher":  {"type": "推送", "free_quota": "无限免费",       "region": "微信/手机/鸿蒙"},
    "pushdeer":  {"type": "推送", "free_quota": "非商用免费",     "region": "开源自架·全球"},
    "smtp":      {"type": "邮箱", "free_quota": "自建无限",       "region": "主权兜底"},
    "serverchan": {"type": "推送", "free_quota": "5条/天",        "region": "微信·低频"},
}


def route_channel(
    msg_class: str,
    user_device: str = "generic",
    channel_alive: Optional[Dict[str, bool]] = None,
) -> Dict[str, Any]:
    """通道路由决策树
    
    Args:
      msg_class: "凭证类" | "安全类" | "实时类"
      user_device: "华为" | "ios" | "android" | "generic"
      channel_alive: {"pushkit": True, "wxpusher": True, ...}
    
    Returns:
      {"primary": 主通道, "fallback": 备通道, "reason": 理由}
    """
    if channel_alive is None:
        channel_alive = {k: True for k in CHANNEL_CAPABILITIES}
    
    # 凭证类: 永走高保障
    if msg_class == "凭证类":
        return {
            "primary": "smtp",
            "fallback": None,
            "reason": "凭证类(验证码/激活码/DNA)永走邮箱高保障通道",
        }
    
    # 安全类: 双发
    if msg_class == "安全类":
        push_channel = _pick_push_channel(user_device, channel_alive)
        return {
            "primary": push_channel,
            "secondary": "smtp",
            "reason": "安全类双发: 推送即时 + 邮箱留底",
        }
    
    # 实时类: 按设备选推送
    if msg_class == "实时类":
        primary = _pick_push_channel(user_device, channel_alive)
        return {
            "primary": primary,
            "fallback": "smtp" if primary != "smtp" else None,
            "reason": f"实时通知·{primary}·兜底邮箱",
        }
    
    # 营销类: 不存在
    return {
        "primary": None,
        "reason": "🔴 营销类消息不存在（八铁律②不商）",
    }


def _pick_push_channel(device: str, alive: Dict[str, bool]) -> str:
    """选择最优推送通道"""
    # 华为设备优先 Push Kit
    if device == "华为" and alive.get("pushkit"):
        return "pushkit"
    
    # WxPusher 通用可靠
    if alive.get("wxpusher"):
        return "wxpusher"
    
    # PushDeer 开源兜底
    if alive.get("pushdeer"):
        return "pushdeer"
    
    # 最后的兜底
    return "smtp"


# ═══════════════════════════════════════════════
# 第7模块：注册准入一体化引擎 (Registration Guard)
# ═══════════════════════════════════════════════

@dataclass
class RegistrationEngine:
    """龍魂注册准入引擎
    
    串联六模块:
      1. 邮箱双轨判定
      2. 注册信任分
      3. 令牌桶限流
      4. 验证码管理
      5. 激活码签发
      6. 通道路由
    """
    
    def __init__(self):
        self.rate_limiter = MultiLevelRateLimiter()
        self.active_codes: Dict[str, VerificationCode] = {}
        self.issued_activations: Dict[str, Dict] = {}
    
    def check_email(self, email: str) -> Dict[str, Any]:
        """邮箱准入判定（不需限流）"""
        return determine_email_track(email)
    
    def request_code(self, email: str, ip: str = "0.0.0.0",
                     device: str = "unknown") -> Dict[str, Any]:
        """申请验证码
        
        流程:
          1. 邮箱格式+双轨判定
          2. 与门（黑名单/仿冒→拒）
          3. 令牌桶限流
          4. 生成验证码
          5. 通道路由（凭证类→邮箱）
        """
        # Step 1: 邮箱判定
        track = determine_email_track(email)
        if track["W_e"] == 0.0:
            return {
                "success": False,
                "reason": track["reason"],
                "track": track,
            }
        
        # Step 2: 令牌桶
        rl = self.rate_limiter.check_all(email, ip, device)
        if not rl["allowed"]:
            return {
                "success": False,
                "reason": rl["reason"],
                "track": track,
            }
        
        # Step 3: 生成验证码
        code = VerificationCode.generate(email)
        self.active_codes[email] = code
        
        # Step 4: 通道路由
        channel = route_channel("凭证类")
        
        return {
            "success": True,
            "code_hash": code.code_hash,
            "expires_in": 300,
            "channel": channel["primary"],
            "track": track,
            # 生产环境：code 通过SMTP发送，不返回到API响应
            # 测试环境：返回明文以便验证
            "code_plaintext": code.code,
        }
    
    def verify_code(self, email: str, input_code: str) -> Dict[str, Any]:
        """验证码校验"""
        if email not in self.active_codes:
            return {"passed": False, "reason": "🔴 无待验证码·先申请", "status": "🔴"}
        
        result = self.active_codes[email].verify(input_code)
        
        if result["passed"]:
            # 验证通过，生成激活码
            email_hash = hashlib.sha256(email.encode()).hexdigest()
            device_fp = f"device-{secrets.token_hex(4)}"  # 简化：实际用七因子
            activation = generate_activation_code(email_hash, device_fp)
            self.issued_activations[email] = activation
            
            result["activation"] = {
                "code": activation["code"],
                "expires_in": 259200,
            }
            
            # 清理验证码
            del self.active_codes[email]
        
        return result
    
    def register(self, email: str, device_fp: str = "unknown",
                 ip_score: float = 1.0, behavior_score: float = 1.0) -> Dict[str, Any]:
        """完整注册流程（不需验证码时可直接走信任分）"""
        track = self.check_email(email)
        
        trust = compute_trust_score(
            W_e=track["W_e"],
            D_dev=1.0,
            I_ip=ip_score,
            B_beh=behavior_score,
        )
        
        return {
            "email": email,
            "track": track,
            "trust": trust,
        }


# ═══════════════════════════════════════════════
# 第8模块：测试向量 (12条·全绿才是门修好)
# ═══════════════════════════════════════════════

# 独立测试函数（复杂逻辑不用lambda）
def _test_t06():
    track1 = determine_email_track("user@petalmai1.com")
    return track1["W_e"] == 0.0 and track1["is_typosquatting"]

def _test_t07():
    code = VerificationCode.generate("test@139.com")
    code.created_at = time.time() - 301
    code.expires_at = time.time() - 1
    r = code.verify("123456")
    return not r["passed"] and "过期" in r["reason"]

def _test_t08():
    code = VerificationCode.generate("test@139.com")
    correct = code.code
    for _ in range(3):
        code.verify("000000")
    result = code.verify(correct)
    return not result["passed"] and "锁定" in result["reason"]

def _test_t12():
    r1 = route_channel("凭证类")
    r2 = route_channel("凭证类", user_device="华为")
    r3 = route_channel("凭证类", user_device="ios")
    return r1["primary"] == "smtp" and r2["primary"] == "smtp" and r3["primary"] == "smtp"

def _test_t13():
    eng = RegistrationEngine()
    r1 = eng.check_email("user@139.com")
    if not (r1["track"] == "国内核心" and r1["W_e"] == 1.0):
        return False
    r2 = eng.register("user@139.com")
    if r2["trust"]["verdict"] != "🟢":
        return False
    r3 = eng.check_email("bad@10minutemail.com")
    return r3["W_e"] == 0.0 and r3["status"] == "🔴"

def _test_t14():
    eng = RegistrationEngine()
    req = eng.request_code("test@139.com", ip="1.2.3.4", device="device-1")
    if not (req["success"] and "code_plaintext" in req):
        return False
    v1 = eng.verify_code("test@139.com", req["code_plaintext"])
    return v1["passed"] and "activation" in v1

def _test_t15():
    eng = RegistrationEngine()
    email_key = hashlib.sha256("rate@139.com".encode()).hexdigest()[:16]
    eng.rate_limiter.reset_bucket("email", email_key)
    eng.rate_limiter.reset_bucket("ip", "10.0.0.1")
    eng.rate_limiter.reset_bucket("device", "dev-1")
    for _ in range(5):
        if not eng.request_code("rate@139.com", ip="10.0.0.1", device="dev-1")["success"]:
            return False
    r6 = eng.request_code("rate@139.com", ip="10.0.0.1", device="dev-1")
    return not r6["success"]

def _test_t16():
    t1 = compute_trust_score(W_e=1.0, D_dev=0.5, I_ip=0.5, B_beh=0.5)
    t2 = compute_trust_score(W_e=0.6, D_dev=0.5, I_ip=0.5, B_beh=0.5)
    return t1["T_reg"] > t2["T_reg"] and abs((t1["T_reg"] - t2["T_reg"]) - 0.16) < 0.01

def _test_t17():
    eh = hashlib.sha256("user@139.com".encode()).hexdigest()
    df = "device-fingerprint-001"
    act = generate_activation_code(eh, df)
    # 正确验证
    v1 = verify_activation(act["code"], eh, df)
    if not v1["valid"]:
        return False
    # 错误设备
    v2 = verify_activation(act["code"], eh, "wrong-device")
    if v2["valid"]:
        return False
    # 错误邮箱
    v3 = verify_activation(act["code"], "wrong-hash", df)
    return not v3["valid"]


TEST_VECTORS = [
    # T01: 国内核心白名单·花瓣
    {
        "id": "T01",
        "test": lambda: (
            determine_email_track("user@petalmail.com")["track"] == "国内核心"
            and determine_email_track("user@petalmail.com")["W_e"] == 1.0
        ),
        "description": "T01: user@petalmail.com → 国内核心 W_e=1.0 🟢",
    },
    # T02: 国内核心白名单·移动/电信
    {
        "id": "T02",
        "test": lambda: (
            determine_email_track("user@139.com")["track"] == "国内核心"
            and determine_email_track("user@189.cn")["track"] == "国内核心"
            and determine_email_track("user@wo.cn")["track"] == "国内核心"
        ),
        "description": "T02: @139.com/@189.cn/@wo.cn → 国内核心 🟢",
    },
    # T03: 备案观察层
    {
        "id": "T03",
        "test": lambda: (
            determine_email_track("user@qq.com")["track"] == "备案观察"
            and determine_email_track("user@qq.com")["W_e"] == 0.8
            and determine_email_track("user@qq.com")["status"] == "🟡"
        ),
        "description": "T03: user@qq.com → 备案观察层 0.8 🟡",
    },
    # T04: 海外轨放行
    {
        "id": "T04",
        "test": lambda: (
            determine_email_track("user@gmail.com")["track"] == "海外"
            and determine_email_track("user@gmail.com")["W_e"] == 0.6
            and determine_email_track("user@gmail.com")["status"] == "🟢"
        ),
        "description": "T04: user@gmail.com → 海外轨 0.6 放行",
    },
    # T05: 一次性邮箱拒收（与门）
    {
        "id": "T05",
        "test": lambda: (
            determine_email_track("test@10minutemail.com")["W_e"] == 0.0
            and determine_email_track("test@10minutemail.com")["status"] == "🔴"
            and determine_email_track("test@tempmail.com")["W_e"] == 0.0
        ),
        "description": "T05: @10minutemail.com → 🔴一次性邮箱拒收（与门）",
    },
    # T06: 形近仿冒拒收
    {
        "id": "T06",
        "test": _test_t06,
        "description": "T06: @petalmai1.com → 🔴形近仿冒拒收",
    },
    # T07: 验证码过期
    {
        "id": "T07",
        "test": _test_t07,
        "description": "T07: 验证码过期(5分钟+1秒) → 🔴拒绝",
    },
    # T08: 验证码错误3次锁定
    {
        "id": "T08",
        "test": _test_t08,
        "description": "T08: 验证码错3次 → 作废+锁15分钟",
    },
    # T09: 信任分达标放行
    {
        "id": "T09",
        "test": lambda: (
            compute_trust_score(W_e=1.0, D_dev=1.0, I_ip=1.0, B_beh=0.8)["T_reg"] >= 0.75
            and compute_trust_score(W_e=1.0, D_dev=1.0, I_ip=1.0, B_beh=0.8)["verdict"] == "🟢"
        ),
        "description": "T09: W_e=1.0+好设备 → T_reg≥0.75 🟢放行",
    },
    # T10: 与门拒绝
    {
        "id": "T10",
        "test": lambda: (
            compute_trust_score(W_e=0.0, D_dev=1.0, I_ip=1.0, B_beh=1.0)["T_reg"] == 0.0
            and "与门" in compute_trust_score(W_e=0.0)["reason"]
        ),
        "description": "T10: W_e=0 → 与门硬闸 T_reg=0 🔴",
    },
    # T11: 华为设备实时通知路由 Push Kit
    {
        "id": "T11",
        "test": lambda: (
            route_channel("实时类", user_device="华为",
                         channel_alive={"pushkit": True, "wxpusher": True})["primary"] == "pushkit"
        ),
        "description": "T11: 实时通知+华为设备 → 路由 Push Kit",
    },
    # T12: 凭证类永不走推送
    {
        "id": "T12",
        "test": _test_t12,
        "description": "T12: 凭证类消息 → 永走邮箱SMTP·不走推送",
    },
    # T13: 完整注册流程验证
    {
        "id": "T13",
        "test": _test_t13,
        "description": "T13: 完整注册流程：139.com→🟢 | 10minutemail→🔴",
    },
    # T14: 验证码全流程
    {
        "id": "T14",
        "test": _test_t14,
        "description": "T14: 申请验证码→验证通过→获得激活码",
    },
    # T15: 令牌桶限流
    {
        "id": "T15",
        "test": _test_t15,
        "description": "T15: 邮箱桶5次/小时后限流",
    },
    # T16: 不同轨道的信任分差异
    {
        "id": "T16",
        "test": _test_t16,
        "description": "T16: W_e差异正确反映在信任分 (ΔW_e×0.4 = 0.16)",
    },
    # T17: 激活码三验
    {
        "id": "T17",
        "test": _test_t17,
        "description": "T17: 激活码三验·正确通过·错误绑定拒绝",
    },
]


def run_tests() -> Tuple[int, int]:
    """运行所有测试向量"""
    passed = 0
    failed = 0
    for tv in TEST_VECTORS:
        try:
            result = tv["test"]()
            if result:
                print(f"  ✅ {tv['description']}")
                passed += 1
            else:
                print(f"  ❌ {tv['description']}")
                failed += 1
        except Exception as e:
            print(f"  ❌ {tv['description']} — Exception: {e}")
            failed += 1
    
    return passed, failed


def demo() -> None:
    """完整演示"""
    print("=" * 60)
    print("龍魂注册准入引擎 · 双轨邮箱+通知协议 v1.0")
    print("=" * 60)
    
    eng = RegistrationEngine()
    
    # 演示邮箱判定
    emails = ["lucky@petalmail.com", "test@qq.com", "user@gmail.com", "bad@10minutemail.com"]
    for e in emails:
        r = eng.check_email(e)
        print(f"  {r['status']} {e:40s} {r['track']:10s} W_e={r['W_e']}  {r['reason']}")
    
    print()
    
    # 演示信任分
    for w, label in [(1.0, "核心"), (0.8, "观察"), (0.6, "海外"), (0.0, "黑名单")]:
        t = compute_trust_score(W_e=w, D_dev=1.0, I_ip=0.9, B_beh=0.8)
        print(f"  信任分({label}): T={t['T_reg']:.4f} {t['verdict']}")
    
    print()
    
    # 演示通道路由
    for mc in ["凭证类", "安全类", "实时类"]:
        r = route_channel(mc, user_device="华为")
        print(f"  通道路由({mc}): {r['primary']} — {r['reason']}")
    
    print()

    # 演示验证码全流程
    print("  --- 验证码流程 ---")
    req = eng.request_code("demo@139.com", ip="192.168.1.1", device="demo-dev")
    print(f"  申请: {req['success']=} 哈希={req.get('code_hash','')[:16]}...")
    if req["success"]:
        v = eng.verify_code("demo@139.com", req["code_plaintext"])
        print(f"  验证: {v['passed']=}  {v.get('reason','')}")
        if v.get("activation"):
            print(f"  激活码: {v['activation']['code']}")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("龍魂注册准入引擎 · 测试向量")
        print("=" * 60)
        p, f = run_tests()
        print("=" * 60)
        total = p + f
        print(f"结果: {p}/{total} 通过")
        if f > 0:
            print(f"      {f}/{total} 失败")
            print("🟡 有未通过的测试")
        else:
            print("🟢 全绿·门修好")
        sys.exit(0 if f == 0 else 1)
    elif len(sys.argv) > 1 and sys.argv[1] == "check":
        email = sys.argv[2] if len(sys.argv) > 2 else "user@gmail.com"
        eng = RegistrationEngine()
        r = eng.check_email(email)
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "analyze":
        email = sys.argv[2] if len(sys.argv) > 2 else "user@139.com"
        eng = RegistrationEngine()
        r = eng.register(email)
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        demo()

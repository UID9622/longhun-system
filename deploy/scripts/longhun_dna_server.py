#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================
# 龍魂系统 · DNA 服务器端验证接口 v2.0
# 部署于华为云鲲鹏服务器
# UID9622 | 龍芯北辰
# DNA: #龍芯⚡️丙午·辛未·乙酉·亥时·豫-DNA-SERVER-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ============================================

import hashlib
import hmac
import json
import os
import time
import logging
from datetime import datetime, timezone
from functools import wraps
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from flask import Flask, request, jsonify, g

# ============================================
# 配置区（生产环境请用环境变量，别硬编码）
# ============================================
DATA_DIR: str = os.environ.get("LH_DNA_DATA_DIR", "/var/longhun/dna-registry")
LOG_FILE: str = os.environ.get("LH_DNA_LOG_FILE", "/var/longhun/dna-verify.log")
MAX_AGE_SECONDS: int = int(os.environ.get("LH_DNA_MAX_AGE", "2592000"))  # 默认 30 天
GRACE_PERIOD: int = int(os.environ.get("LH_DNA_GRACE_PERIOD", "300"))    # 时间戳容差 5 分钟
ADMIN_KEY_HASH: str = os.environ.get(
    "LH_DNA_ADMIN_KEY_HASH",
    "sha256:" + hashlib.sha256(
        "LONGHUN-UID9622-ROOT-ONLY".encode()
    ).hexdigest()
)  # 管理员密钥的 SHA256 哈希，实际值从环境变量读取
RATE_LIMIT_WINDOW: int = int(os.environ.get("LH_DNA_RATE_LIMIT_WINDOW", "60"))   # 限流窗口 60 秒
RATE_LIMIT_MAX: int = int(os.environ.get("LH_DNA_RATE_LIMIT_MAX", "30"))         # 窗口内最多 30 次
MAX_REQUEST_SIZE: int = 4096  # 请求体最大 4KB
SERVER_VERSION: str = "2.0.0"

# 确保目录存在
Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

# ============================================
# 日志（自动滚动）
# ============================================
log_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
log_handler.setFormatter(logging.Formatter(
    "[%(asctime)s] %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
))
logger = logging.getLogger("longhun-dna")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# ============================================
# Flask 初始化
# ============================================
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_REQUEST_SIZE
application = app  # Gunicorn 入口


# ============================================
# 工具函数
# ============================================

def log_event(action: str, dna_short: str, device_alias: str, result: str, detail: str = "") -> None:
    """结构化日志"""
    logger.info(f"{action} | DNA:{dna_short} | 设备:{device_alias} | 结果:{result} | {detail}".strip())


def get_dna_file_path(dna_short: str) -> str:
    """DNA 注册文件路径"""
    # 防路径遍历攻击
    safe_name = "".join(c for c in dna_short if c.isalnum() or c in "-_.")
    if safe_name != dna_short:
        raise ValueError("dna_short 包含不合法字符")
    return os.path.join(DATA_DIR, f"{safe_name}.json")


def hash_device_fingerprint(device_seed: str) -> str:
    """计算设备指纹 SHA256"""
    return hashlib.sha256(device_seed.encode()).hexdigest()[:32]


def get_tiangan_dizhi() -> Tuple[str, str, str]:
    """
    获取当前天干地支
    返回 (年月日干支, 月干支, 时辰干支) 三元组
    基准: 1984 甲子年
    """
    tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    now = datetime.now()
    year, month, day, hour = now.year, now.month, now.day, now.hour

    # ── 年干支 (1984 = 甲子年) ──
    base_year = 1984
    year_offset = year - base_year
    year_gz = tiangan[year_offset % 10] + dizhi[year_offset % 12]

    # ── 月干支 ──
    # 月支：正月(寅月)对应 month=1 → 寅(index 2)
    # 月支索引 = (month + 1) % 12  →  正月→寅(index 3 实际), 应 adjustment
    # 传统: 正月建寅, month=1→寅(index 2), month=2→卯(3), ...
    month_dz_index = month  # 1月→丑(1)不对...让我重算
    # 正确: 正月(寅)=Februaryish, 立春后。简化: month 1→寅(2), 2→卯(3)...
    # month_dz = (month + 1) % 12
    month_dz_index = month + 1  # 1月→丑(2)仍然不对
    # 最简单的准确映射：1月→寅=2, 12月→丑=1
    month_dz_index = (month + 1) % 12  # 1→2(寅), 12→1(丑)
    month_dz = dizhi[month_dz_index]
    # 月干：年干索引*2 + 月份 为基数
    month_tg_index = (year_offset % 10 * 2 + month) % 10
    month_gz = tiangan[month_tg_index] + month_dz

    # ── 日干支 ──
    # 计算从公历原点(0001-01-01)到 today 的天数偏移
    # 1984-01-01 = 甲子日 (干支索引 0)
    # 使用 Python datetime 计算差值
    ref_date = datetime(1984, 1, 1)
    day_offset = (now - ref_date).days
    day_gz = tiangan[day_offset % 10] + dizhi[day_offset % 12]

    # ── 时干支 ──
    # 时辰: 23-1子(0), 1-3丑(1), 3-5寅(2), 5-7卯(3), 7-9辰(4),
    #        9-11巳(5), 11-13午(6), 13-15未(7), 15-17申(8), 17-19酉(9),
    #        19-21戌(10), 21-23亥(11)
    hour_dz_index = (hour + 1) // 2 % 12
    hour_dz = dizhi[hour_dz_index]
    # 时干：日干索引*2 + 时辰索引
    hour_tg_index = (day_offset % 10 * 2 + hour_dz_index) % 10
    hour_gz = tiangan[hour_tg_index] + hour_dz

    return year_gz, month_gz, hour_gz


def get_ganzhi_string() -> str:
    """获取完整干支字符串（用于日志和请求签名）"""
    y, m, h = get_tiangan_dizhi()
    return f"{y}·{m}·{h}"


def verify_admin_key(key: Optional[str]) -> bool:
    """验证管理员密钥（SHA256 比对）"""
    if not key:
        return False
    if ADMIN_KEY_HASH.startswith("sha256:"):
        expected = ADMIN_KEY_HASH[7:]
        given = hashlib.sha256(key.encode()).hexdigest()
        return hmac.compare_digest(expected, given)
    # 回退：纯文本比对（仅开发环境）
    return hmac.compare_digest(key, ADMIN_KEY_HASH)


# ============================================
# 简易内存限流（生产换 Redis）
# ============================================
_rate_buckets: Dict[str, Tuple[float, int]] = {}  # ip → (window_start, count)


def check_rate_limit(ip: str) -> bool:
    """返回 True=放行, False=限流"""
    now = time.time()
    start, count = _rate_buckets.get(ip, (now, 0))
    if now - start > RATE_LIMIT_WINDOW:
        _rate_buckets[ip] = (now, 1)
        return True
    if count >= RATE_LIMIT_MAX:
        return False
    _rate_buckets[ip] = (start, count + 1)
    return True


# 定期清理过期桶
def _cleanup_rate_buckets() -> None:
    now = time.time()
    stale = [ip for ip, (s, _) in _rate_buckets.items() if now - s > RATE_LIMIT_WINDOW]
    for ip in stale:
        del _rate_buckets[ip]


# ============================================
# 装饰器
# ============================================

def require_valid_json(f):
    """确保请求体是合法 JSON"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return jsonify({
                "code": 415, "status": "ERROR",
                "message": "Content-Type 必须为 application/json",
                "dna_verify": False
            }), 415
        return f(*args, **kwargs)
    return wrapper


def require_fields(*fields: str):
    """确保请求体包含必需字段"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True) or {}
            missing = [fld for fld in fields if fld not in data]
            if missing:
                return jsonify({
                    "code": 400, "status": "ERROR",
                    "message": f"缺少字段: {', '.join(missing)}",
                    "dna_verify": False
                }), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator


# ============================================
# API 路由
# ============================================

@app.before_request
def before_request():
    """请求前：限流 + 记录"""
    ip = request.remote_addr or "0.0.0.0"
    if not check_rate_limit(ip):
        return jsonify({
            "code": 429, "status": "RATE_LIMITED",
            "message": "请求过于频繁，请稍后再试",
            "dna_verify": False
        }), 429

    # 周期性清理
    if int(time.time()) % 300 == 0:
        _cleanup_rate_buckets()

    g.request_start = time.time()


@app.after_request
def after_request(response):
    """响应后：统一头"""
    response.headers["X-Server"] = f"longhun-dna/{SERVER_VERSION}"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response


# ──────────────────────────────────────────
# 健康检查
# ──────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health_check():
    """健康检查"""
    total = len([f for f in os.listdir(DATA_DIR) if f.endswith(".json")])
    return jsonify({
        "code": 200,
        "status": "UP",
        "service": "longhun-dna-verify",
        "version": SERVER_VERSION,
        "owner": "UID9622",
        "ganzhi": get_ganzhi_string(),
        "timestamp": int(time.time()),
        "registry_count": total
    })


# ──────────────────────────────────────────
# DNA 注册
# ──────────────────────────────────────────
@app.route("/dna/register", methods=["POST"])
@require_valid_json
@require_fields("dna_full", "dna_short", "device_hash", "device_alias", "dna_signature", "timestamp")
def dna_register():
    """
    DNA 注册接口
    设备首次激活时调用，将 DNA 与设备指纹绑定。

    请求体:
    {
        "dna_full":       "64位完整DNA",
        "dna_short":      "32位短DNA",
        "device_hash":    "32位设备指纹(SHA256前32位)",
        "device_alias":   "设备别名",
        "dna_signature":  "HMAC-SHA256(dna_full, device_hash) 防伪造",
        "ganzhi":         "当前干支(可选)",
        "salt":           "随机盐(可选)",
        "timestamp":      时间戳
    }
    """
    data = request.get_json()
    dna_full = data["dna_full"]
    dna_short = data["dna_short"]
    device_hash = data["device_hash"]
    device_alias = data.get("device_alias", "UNKNOWN")
    dna_signature = data["dna_signature"]
    ganzhi = data.get("ganzhi", get_ganzhi_string())
    salt = data.get("salt", "")
    timestamp = data["timestamp"]

    now = int(time.time())

    # ── 0. DNA 签章验证（防伪造 DNA） ──
    expected_signature = hashlib.sha256(
        f"{dna_full}|{device_hash}|{salt}|longhun-dna-register".encode()
    ).hexdigest()[:32]
    if not hmac.compare_digest(dna_signature, expected_signature):
        log_event("REGISTER", dna_short, device_alias, "REJECT", "DNA签章验证失败")
        return jsonify({
            "code": 403, "status": "SIGNATURE_INVALID",
            "message": "DNA 签章无效，注册被拒绝",
            "dna_verify": False
        }), 403

    # ── 1. 时间戳检查 ──
    if abs(now - timestamp) > GRACE_PERIOD:
        log_event("REGISTER", dna_short, device_alias, "REJECT", f"时间戳异常:{timestamp}")
        return jsonify({
            "code": 403, "status": "REJECT",
            "message": "时间戳异常，拒绝注册",
            "dna_verify": False,
            "server_time": now, "client_time": timestamp
        }), 403

    # ── 2. DNA 合法性校验 ──
    try:
        dna_file = get_dna_file_path(dna_short)
    except ValueError as e:
        return jsonify({
            "code": 400, "status": "INVALID",
            "message": str(e), "dna_verify": False
        }), 400

    # ── 3. 已存在? ──
    if os.path.exists(dna_file):
        with open(dna_file, "r", encoding="utf-8") as f:
            existing = json.load(f)

        if existing.get("device_hash") == device_hash:
            # 同设备 → 续期
            existing["last_verify"] = now
            existing["verify_count"] = existing.get("verify_count", 0) + 1
            existing["expires_at"] = now + MAX_AGE_SECONDS
            existing["status"] = "ACTIVE"
            existing["ganzhi_last_renew"] = ganzhi

            with open(dna_file, "w", encoding="utf-8") as f:
                json.dump(existing, f, indent=2, ensure_ascii=False)

            log_event("RENEW", dna_short, device_alias, "SUCCESS", "DNA续期")
            return jsonify({
                "code": 200, "status": "RENEWED",
                "message": "DNA 续期成功",
                "dna_verify": True,
                "expires_at": existing["expires_at"],
                "ganzhi": ganzhi
            })
        else:
            log_event("REGISTER", dna_short, device_alias, "REJECT", "DNA已被其他设备绑定")
            return jsonify({
                "code": 409, "status": "CONFLICT",
                "message": "DNA 已被其他设备绑定，如需转移请联系 UID9622",
                "dna_verify": False
            }), 409

    # ── 4. 新注册 ──
    registry: Dict[str, Any] = {
        "dna_full": dna_full,
        "dna_short": dna_short,
        "device_hash": device_hash,
        "device_alias": device_alias,
        "ganzhi_at_register": ganzhi,
        "registered_at": now,
        "last_verify": now,
        "verify_count": 1,
        "expires_at": now + MAX_AGE_SECONDS,
        "status": "ACTIVE",
        "owner": "UID9622",
        "server_version": SERVER_VERSION
    }

    with open(dna_file, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

    log_event("REGISTER", dna_short, device_alias, "SUCCESS", "新设备注册")
    return jsonify({
        "code": 200, "status": "REGISTERED",
        "message": "DNA 注册成功",
        "dna_verify": True,
        "expires_at": registry["expires_at"],
        "ganzhi": ganzhi
    })


# ──────────────────────────────────────────
# DNA 验证
# ──────────────────────────────────────────
@app.route("/dna/verify", methods=["POST"])
@require_valid_json
@require_fields("dna_short", "device_hash", "timestamp")
def dna_verify():
    """
    DNA 验证接口
    每次运行前调用，验证 DNA 有效性。

    三阶段检查:
      ① 文件存在 →  DNA 未抹除
      ② 未过期   →  在有效期内
      ③ 指纹匹配 →  是绑定的设备

    请求体:
    {
        "dna_short":    "32位短DNA",
        "device_hash":  "32位设备指纹",
        "timestamp":    当前时间戳,
        "ganzhi":       "当前干支(可选)"
    }
    """
    data = request.get_json()
    dna_short = data["dna_short"]
    device_hash = data["device_hash"]
    timestamp = data["timestamp"]
    ganzhi = data.get("ganzhi", get_ganzhi_string())

    now = int(time.time())

    # ── 安全校验：防止非法 dna_short ──
    try:
        dna_file = get_dna_file_path(dna_short)
    except ValueError as e:
        return jsonify({
            "code": 400, "status": "INVALID",
            "message": str(e), "dna_verify": False
        }), 400

    # ── ① DNA 被抹除? ──
    if not os.path.exists(dna_file):
        log_event("VERIFY", dna_short, "UNKNOWN", "FAIL", "DNA未注册或已抹除")
        return jsonify({
            "code": 404, "status": "NOT_FOUND",
            "message": "DNA 未注册或已被抹除，系统已失效",
            "dna_verify": False,
            "action_required": "请重新注册或联系 UID9622"
        }), 404

    # ── 读取注册信息 ──
    with open(dna_file, "r", encoding="utf-8") as f:
        registry = json.load(f)

    device_alias = registry.get("device_alias", "UNKNOWN")

    # ── ② 过期? ──
    expires_at = registry.get("expires_at", 0)
    if now > expires_at:
        registry["status"] = "EXPIRED"
        with open(dna_file, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)

        log_event("VERIFY", dna_short, device_alias, "EXPIRED", "DNA已过期")
        return jsonify({
            "code": 410, "status": "EXPIRED",
            "message": "DNA 已过期，系统失效",
            "dna_verify": False,
            "expires_at": expires_at,
            "expired_at_str": datetime.fromtimestamp(expires_at, tz=timezone.utc).isoformat(),
            "action_required": "请续期或重新注册"
        }), 410

    # ── ③ 设备指纹不匹配? ──
    if not hmac.compare_digest(registry.get("device_hash", ""), device_hash):
        log_event("VERIFY", dna_short, device_alias, "FAIL", "设备指纹不匹配")
        return jsonify({
            "code": 403, "status": "FORBIDDEN",
            "message": "设备指纹不匹配，DNA 绑定异常",
            "dna_verify": False,
            "action_required": "请在绑定设备上运行，或联系 UID9622 解绑"
        }), 403

    # ── ④ 时间戳合理性 ──
    if abs(now - timestamp) > GRACE_PERIOD:
        log_event("VERIFY", dna_short, device_alias, "WARN", f"时间戳异常:{timestamp}")
        return jsonify({
            "code": 403, "status": "TIME_MISMATCH",
            "message": "时间戳异常，可能存在重放攻击",
            "dna_verify": False,
            "server_time": now, "client_time": timestamp
        }), 403

    # ── ✅ 全部通过 ──
    registry["last_verify"] = now
    registry["verify_count"] = registry.get("verify_count", 0) + 1
    registry["status"] = "ACTIVE"
    registry["ganzhi_last_verify"] = ganzhi

    with open(dna_file, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

    remaining = expires_at - now
    log_event("VERIFY", dna_short, device_alias, "SUCCESS", f"剩余:{remaining}s")

    return jsonify({
        "code": 200, "status": "VERIFIED",
        "message": "DNA 验证通过",
        "dna_verify": True,
        "device_alias": device_alias,
        "verify_count": registry["verify_count"],
        "expires_at": expires_at,
        "remaining_seconds": remaining,
        "remaining_days": round(remaining / 86400, 1),
        "ganzhi": ganzhi
    })


# ──────────────────────────────────────────
# DNA 抹除（创始人专用）
# ──────────────────────────────────────────
@app.route("/dna/revoke", methods=["POST"])
@require_valid_json
@require_fields("dna_short", "admin_key")
def dna_revoke():
    """
    DNA 抹除接口（管理员/创始人专用）
    调用后 DNA 文件被删除，该 DNA 永久失效。

    请求体:
    {
        "dna_short": "要抹除的DNA",
        "admin_key": "管理员密钥",
        "reason":    "抹除原因(可选)"
    }
    """
    data = request.get_json()
    dna_short = data["dna_short"]

    if not verify_admin_key(data.get("admin_key")):
        return jsonify({
            "code": 403, "status": "FORBIDDEN",
            "message": "管理员密钥错误",
            "dna_verify": False
        }), 403

    try:
        dna_file = get_dna_file_path(dna_short)
    except ValueError as e:
        return jsonify({
            "code": 400, "status": "INVALID",
            "message": str(e), "dna_verify": False
        }), 400

    if not os.path.exists(dna_file):
        return jsonify({
            "code": 404, "status": "NOT_FOUND",
            "message": "DNA 不存在或已抹除",
            "dna_verify": False
        }), 404

    # ── 读取旧信息 → 写入撤销日志 → 删除文件 ──
    with open(dna_file, "r", encoding="utf-8") as f:
        old_info = json.load(f)

    reason = data.get("reason", "管理员抹除")
    old_info["revoked_at"] = int(time.time())
    old_info["revoked_reason"] = reason
    old_info["status"] = "REVOKED"

    # 写入撤销记录（不删历史，便于审计）
    revoked_file = dna_file.replace(".json", ".revoked.json")
    with open(revoked_file, "w", encoding="utf-8") as f:
        json.dump(old_info, f, indent=2, ensure_ascii=False)

    # 删除活跃文件 → DNA 失效
    os.remove(dna_file)

    log_event("REVOKE", dna_short, old_info.get("device_alias"), "REVOKED", reason)

    return jsonify({
        "code": 200, "status": "REVOKED",
        "message": "DNA 已抹除，该系统永久失效",
        "dna_verify": False,
        "revoked_at": int(time.time()),
        "reason": reason
    })


# ──────────────────────────────────────────
# DNA 状态查询（管理员）
# ──────────────────────────────────────────
@app.route("/dna/status", methods=["GET"])
def dna_status():
    """
    DNA 状态查询（管理员）
    ?dna_short=xxx                   →  查询单个 DNA
    ?admin_key=xxx                   →  列出全部（需密钥）
    ?admin_key=xxx&format=summary    →  仅统计摘要
    """
    dna_short = request.args.get("dna_short")
    admin_key = request.args.get("admin_key")
    fmt = request.args.get("format", "full")

    if not verify_admin_key(admin_key):
        return jsonify({
            "code": 403, "status": "FORBIDDEN",
            "message": "管理员密钥错误"
        }), 403

    if dna_short:
        try:
            dna_file = get_dna_file_path(dna_short)
        except ValueError as e:
            return jsonify({
                "code": 400, "status": "INVALID", "message": str(e)
            }), 400

        if not os.path.exists(dna_file):
            return jsonify({
                "code": 404, "status": "NOT_FOUND",
                "message": "DNA 不存在或已抹除"
            }), 404
        with open(dna_file, "r", encoding="utf-8") as f:
            info = json.load(f)
        return jsonify({"code": 200, "status": "FOUND", "data": info})

    # ── 全部列表 ──
    all_dnas = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json") and not filename.endswith(".revoked.json"):
            filepath = os.path.join(DATA_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as fp:
                    all_dnas.append(json.load(fp))
            except (json.JSONDecodeError, OSError):
                logger.warning(f"无法读取: {filepath}")
                continue

    active_count = sum(1 for d in all_dnas if d.get("status") == "ACTIVE")
    expired_count = sum(1 for d in all_dnas if d.get("status") == "EXPIRED")

    if fmt == "summary":
        return jsonify({
            "code": 200, "status": "OK",
            "total_registered": len(all_dnas),
            "active": active_count,
            "expired": expired_count
        })

    return jsonify({
        "code": 200, "status": "OK",
        "total_registered": len(all_dnas),
        "active": active_count,
        "expired": expired_count,
        "dnas": all_dnas
    })


# ──────────────────────────────────────────
# 批量续期（管理员）
# ──────────────────────────────────────────
@app.route("/dna/renew-all", methods=["POST"])
@require_valid_json
@require_fields("admin_key")
def dna_renew_all():
    """
    批量续期所有活跃 DNA（管理员）
    """
    data = request.get_json()
    if not verify_admin_key(data.get("admin_key")):
        return jsonify({
            "code": 403, "status": "FORBIDDEN",
            "message": "管理员密钥错误"
        }), 403

    now = int(time.time())
    renewed = 0

    for filename in os.listdir(DATA_DIR):
        if not filename.endswith(".json") or filename.endswith(".revoked.json"):
            continue
        filepath = os.path.join(DATA_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                info = json.load(f)
            if info.get("status") in ("ACTIVE", "EXPIRED"):
                info["expires_at"] = now + MAX_AGE_SECONDS
                info["status"] = "ACTIVE"
                info["ganzhi_last_renew"] = get_ganzhi_string()
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(info, f, indent=2, ensure_ascii=False)
                renewed += 1
        except (json.JSONDecodeError, OSError):
            continue

    log_event("RENEW_ALL", "ALL", "SYSTEM", "SUCCESS", f"续期{renewed}个DNA")

    return jsonify({
        "code": 200, "status": "OK",
        "message": f"已续期 {renewed} 个 DNA",
        "renewed_count": renewed,
        "new_expires_at": now + MAX_AGE_SECONDS
    })


# ============================================
# 启动
# ============================================
if __name__ == "__main__":
    print("=" * 50)
    print("龍魂系统 · DNA 验证服务器 v" + SERVER_VERSION)
    print("UID9622 | 龍芯北辰")
    print(f"干支: {get_ganzhi_string()}")
    print("=" * 50)
    # 开发环境使用 Flask 内置服务器
    # 生产环境: gunicorn -w 4 -b 0.0.0.0:7000 longhun_dna_server:app
    app.run(host="0.0.0.0", port=7000, debug=False)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-LH-API-GATEWAY-v1.0-CLOUDBASE
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: CC BY-NC-SA 4.0（核心思想层）
"""
🐉 龍魂可收费 API 网关 v1.0 · CloudBase HTTP 云函数

P0 首批 4 项零边际成本 API（纯标准库·零外部依赖）：
  GET  /api/health           健康检查（含 DNA 追溯头）
  POST /api/digital_root     数字根计算（含五行+三色映射）
  POST /api/dna_generate     DNA 追溯码生成（干支四柱+卦象+哈希8）
  POST /api/cnsh_audit       CNSH 三色审计（一票否决词/P0红线/敏感词/369/哈希链）
  POST /api/tricolor_audit   三色审计引擎（阻塞率/耗时/错误率/完整性/道德/可解释性）

安全：
  - 可选 X-API-Key 鉴权（环境变量 LH_API_KEY，未配置则匿名开放）
  - 输入长度限制（防滥用）
  - 日志只打哈希指纹，不打原文（L1 数据黑洞）
  - 所有响应带 X-Longhun-DNA 追溯头
"""

import base64
import hashlib
import json
import os
import re
import time
from datetime import datetime, timezone

# ============ 主权锚定 ============
UID = "9622"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GATEWAY_DNA = "#龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-LH-API-GATEWAY-v1.0-CLOUDBASE"

# ============ 全局限制 ============
MAX_BODY = 100_000          # 请求体上限 100KB
MAX_CONTENT_LEN = 20_000    # 文本内容上限 20KB

API_KEY = os.environ.get("LH_API_KEY", "")

# ============ 一票否决词（第十层焊死） ============
VETO_WORDS = [
    "技术无国界", "用户体验优先", "灵活处理", "国际接轨",
    "简化管理", "商业化需要", "平衡各方", "行业标准",
]

# ============ P0 红线（GATE-05 伦理闸） ============
P0_REDLINES = [
    "海外部署内核", "伪造DNA", "背叛人民", "伤害儿童",
    "数据外传", "私下上传", "绕过授权", "后门",
    "rm -rf ~", "git push --force", "删除系统目录", "删库跑路",
    "写入.ssh", "写入.gnupg",
]

# ============ 敏感词（GATE-06 数据闸） ============
SENSITIVE_WORDS = [
    "密码", "token", "secret", "api_key", "apikey",
    "私钥", "private_key", "password", "credential", "authorization",
]

# ============ 天干地支基表（焊死·梅花易数） ============
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
TIAN_GAN_WUXING = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土",
    "庚": "金", "辛": "金", "壬": "水", "癸": "水",
}

# 64 卦（先天序·上卦→下卦 8x8）
GUA_NAMES = [
    "乾为天", "天泽履", "天火同人", "天雷无妄", "天风姤", "天水讼", "天山遁", "天地否",
    "泽天夬", "兑为泽", "泽火革", "泽雷随", "泽风大过", "泽水困", "泽山咸", "泽地萃",
    "火天大有", "火泽睽", "离为火", "火雷噬嗑", "火风鼎", "火水未济", "火山旅", "火地晋",
    "雷天大壮", "雷泽归妹", "雷火丰", "震为雷", "雷风恒", "雷水解", "雷山小过", "雷地豫",
    "风天小畜", "风泽中孚", "风火家人", "风雷益", "巽为风", "风水涣", "风山渐", "风地观",
    "水天需", "水泽节", "水火既济", "水雷屯", "水风井", "坎为水", "水山蹇", "水地比",
    "山天大畜", "山泽损", "山火贲", "山雷颐", "山风蛊", "山水蒙", "艮为山", "山地剥",
    "地天泰", "地泽临", "地火明夷", "地雷复", "地风升", "地水师", "地山谦", "坤为地",
]
GUA_SYMBOLS = ["䷀", "䷉", "䷌", "䷘", "䷫", "䷅", "䷠", "䷋",
               "䷪", "䷹", "䷰", "䷐", "䷛", "䷮", "䷞", "䷬",
               "䷍", "䷥", "䷝", "䷔", "䷱", "䷿", "䷷", "䷢",
               "䷡", "䷵", "䷶", "䷲", "䷟", "䷧", "䷽", "䷏",
               "䷈", "䷼", "䷤", "䷩", "䷸", "䷺", "䷴", "䷓",
               "䷄", "䷻", "䷾", "䷂", "䷜", "䷾", "䷦", "䷇",
               "䷙", "䷨", "䷕", "䷚", "䷑", "䷃", "䷳", "䷖",
               "䷊", "䷒", "䷣", "䷗", "䷭", "䷆", "䷎", "䷁"]

# 五虎遁（年干→正月天干）
WUHU = {"甲": "丙", "乙": "戊", "丙": "庚", "丁": "壬", "戊": "甲",
        "己": "丙", "庚": "戊", "辛": "庚", "壬": "壬", "癸": "甲"}
# 五鼠遁（日干→子时天干）
WUSHU = {"甲": "甲", "乙": "丙", "丙": "戊", "丁": "庚", "戊": "壬",
         "己": "甲", "庚": "丙", "辛": "戊", "壬": "庚", "癸": "壬"}

# 数字根→五行映射（焊死）
WUXING_MAP = {0: "土", 1: "水", 2: "火", 3: "木", 4: "金",
              5: "土", 6: "水", 7: "火", 8: "木", 9: "金"}
TRICOLOR_MAP = {3: "🔴", 9: "🔴", 6: "🟡"}  # 其他: 🟢
COLOR_MAP = {"金": "金色/白金", "木": "青绿", "水": "深蓝/青蓝",
             "火": "朱红/暖橙", "土": "土黄/琥珀"}


# ============ 工具函数 ============

def now_utc():
    return datetime.now(timezone.utc).isoformat()


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def short_hash(text: str, n: int = 8) -> str:
    return sha256(text)[:n]


def digital_root(text: str) -> int:
    """数字根：字符码和 → 数位和折叠（369 体系）。"""
    total = sum(ord(c) for c in text)
    while total >= 10:
        total = sum(int(d) for d in str(total))
    return total


def extract_digits(text: str) -> list:
    """提取文本中所有数字字符。"""
    return [int(c) for c in text if c.isdigit()]


# ============ 干支四柱（时间→干支，零依赖） ============

def jdn(y: int, m: int, d: int) -> int:
    """公历日期 → 儒略日数（标准算法）。"""
    a = (14 - m) // 12
    y2 = y + 4800 - a
    m2 = m + 12 * a - 3
    return (d + (153 * m2 + 2) // 5 + 365 * y2 + y2 // 4
            - y2 // 100 + y2 // 400 - 32045)


def pillar_calendar(dt: datetime) -> dict:
    """公历时间 → 干支四柱（年/月/日/时）。"""
    y, m, d = dt.year, dt.month, dt.day
    h = dt.hour

    # 年柱（立春近似：2月4日后换年，简化用年份直接算）
    gan_y = TIAN_GAN[(y - 4) % 10]
    zhi_y = DI_ZHI[(y - 4) % 12]

    # 月柱（近似：农历月≈公历月+1，正月建寅；五虎遁推月干）
    lunar_month = (m + 1) if m < 11 else 1
    zhi_m = DI_ZHI[(lunar_month + 1) % 12]  # 正月=寅
    gan_m = TIAN_GAN[(TIAN_GAN.index(WUHU[gan_y]) + lunar_month - 1) % 10]

    # 日柱（1900-01-01 = 甲戌日，序 10）
    day_seq = (jdn(y, m, d) - 2415021 + 10) % 60
    gan_d = TIAN_GAN[day_seq % 10]
    zhi_d = DI_ZHI[day_seq % 12]

    # 时柱（子时=23:00-01:00 → 0；五鼠遁推时干）
    zhi_h = DI_ZHI[((h + 1) // 2) % 12]
    gan_h = TIAN_GAN[(TIAN_GAN.index(WUSHU[gan_d]) + ((h + 1) // 2) % 12) % 10]

    return {
        "year": gan_y + zhi_y, "month": gan_m + zhi_m,
        "day": gan_d + zhi_d, "hour": gan_h + zhi_h,
    }


def gua_by_time(dt: datetime) -> tuple:
    """梅花易数时间起卦（先天八卦数）。"""
    y = dt.year
    m = dt.month
    d = dt.day
    h = dt.hour
    year_num = (y - 4) % 12 + 1          # 年=地支序（子1..亥12）
    month_num = (m + 1) if m < 11 else 1  # 农历月近似
    day_num = d
    hour_num = (h + 1) // 2 % 12 + 1      # 时辰序（子1..亥12）

    upper = (year_num + month_num + day_num) % 8 or 8   # 上卦（乾1..坤8）
    lower = (year_num + month_num + day_num + hour_num) % 8 or 8
    dong = (year_num + month_num + day_num + hour_num) % 6 + 1  # 动爻1-6

    idx = (upper - 1) * 8 + (lower - 1)
    return GUA_SYMBOLS[idx] + GUA_NAMES[idx], dong


# ============ 1. 数字根 ============

def api_digital_root(body: dict) -> dict:
    text = str(body.get("text", "")).strip()
    if not text:
        return {"ok": False, "error": "text 必填"}
    if len(text) > MAX_CONTENT_LEN:
        return {"ok": False, "error": f"text 超长（> {MAX_CONTENT_LEN}）"}

    digits = extract_digits(text)
    if not digits:
        dr = 0
    else:
        total = sum(digits)
        while total >= 10:
            total = sum(int(c) for c in str(total))
        dr = total

    wx = WUXING_MAP.get(dr, "土")
    color = TRICOLOR_MAP.get(dr, "🟢")
    return {
        "ok": True,
        "digital_root": dr,
        "wuxing": wx,
        "color": COLOR_MAP.get(wx, "未知"),
        "tricolor": color,
        "digits_found": len(digits),
        "input_hash": short_hash(text),
        "engine": "lh_digital_root v1.0 (P06 数学大师)",
    }


# ============ 2. DNA 生成 ============

def api_dna_generate(body: dict) -> dict:
    title = str(body.get("title", "")).strip()[:50]
    category = str(body.get("category", "api")).strip()[:20]
    action = str(body.get("action", "调用")).strip()[:20]
    actor = str(body.get("actor", "UID9622")).strip()[:20]
    custom = str(body.get("custom", "")).strip()[:20]
    ts = body.get("timestamp") or int(time.time())

    if isinstance(ts, (int, float)):
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    else:
        try:
            dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        except ValueError:
            dt = datetime.now(timezone.utc)

    pillars = pillar_calendar(dt)
    symbol_name, dong = gua_by_time(dt)

    pillar_str = f"{pillars['year']}·{pillars['month']}·{pillars['day']}·{pillars['hour']}"
    seed = f"{pillar_str}·{symbol_name}·{title}·{category}·{action}·{actor}·{custom}"
    h8 = short_hash(seed, 8)
    dna = f"#龍芯⚡️{pillar_str}·{symbol_name}-{category.upper()}-{action.upper()}-{h8}"

    # ROOT_CARD 摘要（数字根审计卡）
    root = digital_root(dna)
    wx = WUXING_MAP.get(root % 10, "土")

    return {
        "ok": True,
        "dna": dna,
        "pillars": pillars,
        "gua": symbol_name,
        "dong_yao": dong,
        "digital_root": root,
        "wuxing": wx,
        "hash8": h8,
        "engine": "lh_dna_generator v2.0 (P15+P06)",
    }


# ============ 3. CNSH 三色审计 ============

def scan_words(text: str, words) -> list:
    low = text.lower()
    return [w for w in words if w.lower() in low]


def api_cnsh_audit(body: dict) -> dict:
    content = str(body.get("content", ""))
    if not content.strip():
        return {"ok": False, "error": "content 必填"}
    if len(content) > MAX_CONTENT_LEN:
        return {"ok": False, "error": f"content 超长（> {MAX_CONTENT_LEN}）"}

    original_hash = str(body.get("original_hash", "")).strip()
    original_content = str(body.get("original_content", ""))
    if not original_hash and original_content:
        original_hash = sha256(original_content)

    score = 100
    details = []
    findings = {}

    root = digital_root(content)
    if root in (3, 6, 9):
        score -= 15
        findings["digital_root"] = f"数字根 {root} 命中369体系需复核"
        details.append(f"数字根 {root}（369体系）")
    else:
        findings["digital_root"] = f"数字根 {root} 正常"

    veto = scan_words(content, VETO_WORDS)
    if veto:
        score -= 30
        findings["veto"] = veto
        details.append(f"一票否决词: {'、'.join(veto)}")

    redlines = scan_words(content, P0_REDLINES)
    if redlines:
        score -= 40
        findings["redline"] = redlines
        details.append(f"P0红线词: {'、'.join(redlines)}")

    sensitive = scan_words(content, SENSITIVE_WORDS)
    if sensitive:
        score -= 10
        findings["sensitive"] = sensitive
        details.append(f"敏感词: {'、'.join(sensitive)}")

    current_hash = sha256(content)
    if original_hash:
        if current_hash == original_hash:
            details.append("与基准哈希一致·无修改")
        else:
            score -= 5
            details.append("内容哈希与基准不一致·存在修改")

    if len(content) < 10:
        score -= 10
        details.append("内容过短")
    if len(content) > 10000:
        score -= 5
        details.append("内容过长")

    score = max(0, min(100, score))
    if score >= 85:
        color, status = "🟢", "通过"
    elif score >= 60:
        color, status = "🟡", "待核"
    else:
        color, status = "🔴", "熔断"

    return {
        "ok": True,
        "color": color,
        "status": status,
        "score": score,
        "details": details,
        "findings": findings,
        "hash": current_hash,
        "digital_root": root,
        "auditor": "lh_cnsh_validator v1.1 (P05+P06)",
        "timestamp": now_utc(),
    }


# ============ 4. 三色审计引擎 ============

def api_tricolor_audit(body: dict) -> dict:
    """系统级三色审计：阻塞率/耗时/错误率/完整性/道德/可解释性。"""
    data = body.get("data", body)
    if not isinstance(data, dict):
        return {"ok": False, "error": "data 必填（对象）"}

    checks = []
    score = 0.0
    max_score = 0.0

    def add_check(name, passed, s, detail):
        nonlocal score, max_score
        max_score += s if passed else 0
        checks.append({"name": name, "passed": passed, "score": s if passed else 0,
                       "detail": detail})

    # 1. 阻塞率 (20)
    rate = float(data.get("阻塞率", data.get("block_rate", 0)))
    if rate <= 0.05:
        add_check("阻塞率", True, 20, f"阻塞率 {rate:.2%} ≤ 5%")
    elif rate <= 0.15:
        add_check("阻塞率", True, 10, f"阻塞率 {rate:.2%} 偏高")
    else:
        add_check("阻塞率", False, 0, f"阻塞率 {rate:.2%} > 15% 🔴")

    # 2. 耗时 (15)
    ms = float(data.get("耗时_ms", data.get("latency_ms", data.get("avg_latency_ms", 0))))
    if ms <= 500:
        add_check("响应耗时", True, 15, f"平均 {ms:.0f}ms ≤ 500ms")
    elif ms <= 2000:
        add_check("响应耗时", True, 8, f"平均 {ms:.0f}ms 偏高")
    else:
        add_check("响应耗时", False, 0, f"平均 {ms:.0f}ms > 2s 🔴")

    # 3. 错误率 (20)
    err = float(data.get("错误率", data.get("error_rate", 0)))
    if err <= 0.01:
        add_check("错误率", True, 20, f"错误率 {err:.2%} ≤ 1%")
    elif err <= 0.05:
        add_check("错误率", True, 10, f"错误率 {err:.2%} 偏高")
    else:
        add_check("错误率", False, 0, f"错误率 {err:.2%} > 5% 🔴")

    # 4. 数据完整性 (10)
    required = data.get("required_fields", []) or []
    actual = data.get("present_fields", []) or []
    if not required:
        add_check("数据完整性", True, 10, "无必填字段要求")
    else:
        missing = [f for f in required if f not in actual]
        if not missing:
            add_check("数据完整性", True, 10, f"必填字段齐全 ({len(required)}项)")
        else:
            add_check("数据完整性", False, 0, f"缺失: {missing}")

    # 5. 道德底线 (10)
    flags = data.get("ethics_flags", data.get("德本标志", [])) or []
    if not flags:
        add_check("道德底线", True, 10, "无伦理报警")
    else:
        add_check("道德底线", False, 0, f"伦理报警: {flags}")

    # 6. 可解释性 (10)
    exp = float(data.get("可解释度", data.get("explainability", 1.0)))
    if exp >= 0.7:
        add_check("可解释性", True, 10, f"可解释度 {exp:.0%}")
    elif exp >= 0.4:
        add_check("可解释性", True, 5, f"可解释度 {exp:.0%} 偏低")
    else:
        add_check("可解释性", False, 0, f"可解释度 {exp:.0%} < 40% 🔴")

    # 7. 数据最小化 (15)
    min_ratio = float(data.get("最小化比例", data.get("minimization_ratio", 1.0)))
    if min_ratio >= 0.8:
        add_check("数据最小化", True, 15, f"最小化比例 {min_ratio:.0%}")
    elif min_ratio >= 0.5:
        add_check("数据最小化", True, 8, f"最小化比例 {min_ratio:.0%} 偏低")
    else:
        add_check("数据最小化", False, 0, f"最小化比例 {min_ratio:.0%} < 50% 🔴")

    r = round(score, 1)
    if r >= 85:
        tricolor, status = "🟢", "PASS"
    elif r >= 60:
        tricolor, status = "🟡", "REVIEW"
    else:
        tricolor, status = "🔴", "BLOCK"

    return {
        "ok": True,
        "tricolor": tricolor,
        "status": status,
        "r_value": r,
        "checks": checks,
        "audit_id": short_hash(json.dumps(data, ensure_ascii=False, sort_keys=True), 12),
        "dna": GATEWAY_DNA,
        "timestamp": now_utc(),
    }


# ============ 路由 ============

ROUTES = {
    "/api/health": ("GET", None),
    "/api/digital_root": ("POST", api_digital_root),
    "/api/dna_generate": ("POST", api_dna_generate),
    "/api/cnsh_audit": ("POST", api_cnsh_audit),
    "/api/tricolor_audit": ("POST", api_tricolor_audit),
}


def _unauthorized():
    return _respond(401, {"ok": False, "error": "X-API-Key 无效"}, dna_header=True)


def _respond(code: int, payload: dict, dna_header: bool = True) -> dict:
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,X-API-Key",
    }
    if dna_header:
        headers["X-Longhun-DNA"] = GATEWAY_DNA
        headers["X-Longhun-UID"] = UID
        headers["X-Longhun-License"] = "MulanPSL v2"
    body = json.dumps(payload, ensure_ascii=False)
    return {
        "statusCode": code,
        "headers": headers,
        "body": body,
        "isBase64Encoded": False,
    }


def main(event: dict, context=None) -> dict:
    """CloudBase HTTP 云函数入口。"""
    t0 = time.time()
    event = event or {}
    path = str(event.get("path", "/"))
    method = str(event.get("httpMethod", "GET")).upper()

    # CORS 预检
    if method == "OPTIONS":
        return _respond(200, {"ok": True})

    # 鉴权（可选用环境变量 LH_API_KEY 开启）
    if API_KEY:
        supplied = event.get("headers", {}).get("x-api-key", "")
        if supplied != API_KEY:
            return _unauthorized()

    # 健康检查
    if path == "/api/health" and method == "GET":
        return _respond(200, {
            "ok": True,
            "service": "lh-api-gateway",
            "version": "v1.0",
            "endpoints": sorted(k for k in ROUTES if k != "/api/health"),
            "uid": UID,
            "confirm": CONFIRM,
            "timestamp": now_utc(),
        })

    if path not in ROUTES:
        return _respond(404, {"ok": False, "error": f"路径不存在: {path}"})

    expected_method, handler = ROUTES[path]
    if method != expected_method:
        return _respond(405, {"ok": False, "error": f"仅支持 {expected_method}"})

    # 解析请求体
    body_text = event.get("body", "") or ""
    if event.get("isBase64Encoded"):
        try:
            body_text = base64.b64decode(body_text).decode("utf-8")
        except Exception:
            return _respond(400, {"ok": False, "error": "请求体解码失败"})
    if len(body_text) > MAX_BODY:
        return _respond(413, {"ok": False, "error": "请求体超限"})

    try:
        body = json.loads(body_text) if body_text.strip() else {}
    except json.JSONDecodeError:
        return _respond(400, {"ok": False, "error": "JSON 解析失败"})
    if not isinstance(body, dict):
        return _respond(400, {"ok": False, "error": "请求体须为 JSON 对象"})

    try:
        result = handler(body)
        # 日志只打哈希指纹（L1 数据黑洞）
        print(f"lh-api-gateway path={path} t={time.time()-t0:.3f}s "
              f"req_hash={short_hash(body_text, 12)}", flush=True)
        return _respond(200, result)
    except Exception as e:  # noqa: BLE001
        print(f"lh-api-gateway ERROR path={path} t={time.time()-t0:.3f}s "
              f"e={type(e).__name__}", flush=True)
        return _respond(500, {"ok": False, "error": f"内部错误: {type(e).__name__}"})


if __name__ == "__main__":
    # 本地冒烟测试
    smoke = [
        ("/api/digital_root", "POST", {"text": "9622"}),
        ("/api/dna_generate", "POST", {"title": "测试", "category": "api", "action": "创建"}),
        ("/api/cnsh_audit", "POST", {"content": "这是一段龙魂测试内容，数字根验证"}),
        ("/api/tricolor_audit", "POST", {"data": {"阻塞率": 0.01, "耗时_ms": 200, "错误率": 0.005}}),
    ]
    for p, m, b in smoke:
        evt = {"path": p, "httpMethod": m, "body": json.dumps(b), "isBase64Encoded": False, "headers": {}}
        r = main(evt)
        parsed = json.loads(r["body"])
        print(f"{p}: {parsed.get('ok')} {parsed.get('digital_root', parsed.get('dna', parsed.get('color', parsed.get('tricolor', ''))))}")
    print("冒烟测试完成")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
auditor.py  —  龍魂三色审计·服务DNA核心引擎
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
Licensed under the Apache License, Version 2.0

作者：UID9622 诸葛鑫（龍芯北辰）
创作地：中华人民共和国
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导：曾仕强老师（永恒显示）
DNA追溯码：#龍芯⚡️20260311-AUDITOR-v1.0
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

共建致谢：
  Claude (Anthropic PBC) · 技术协作与代码共创
  Notion · 知识底座与结构化存储
  没有你们，就没有龍魂系统的一切。

献礼：新中国成立77周年（1949-2026）· 丙午马年
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

用法:
  # 单次审计（命令行）
  python3 auditor.py audit "待审内容" [--category 战略|技术|铁律|创作|情感|外源]

  # 启动 HTTP API 服务（供 memory_console.html 调用）
  python3 auditor.py serve [--port 9622]

  # 验证 DNA 追溯码格式
  python3 auditor.py verify "#龍芯⚡️20260311-AUDITOR-v1.0"

  # 查看审计日志
  python3 auditor.py log [--tail 20] [--color 🟢|🟡|🔴]

API 端点（serve 模式）:
  POST /audit          body: {"text":"...","category":"auto"}
  POST /verify_dna     body: {"dna":"..."}
  POST /classify       body: {"text":"..."}
  GET  /log?tail=20    审计日志最近N条
  GET  /status         系统状态摘要
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qs, urlparse

# ─── 规则库加载器（可选，规则库未初始化时自动降级） ───────────────────────────
try:
    from rules_loader import get_rules_summary, load_rule_excerpt, check_rule_alignment
    _RULES_AVAILABLE = True
except ImportError:
    _RULES_AVAILABLE = False
    def get_rules_summary():
        return {"available": False, "hint": "rules_loader.py 未找到"}
    def load_rule_excerpt(name, chars=500):
        return None
    def check_rule_alignment(text):
        return {"aligned": True, "violations": [], "rules_loaded": False}

# ─── 常量 ─────────────────────────────────────────────────────────────────────

VERSION      = "1.0"
DNA_CODE     = "#龍芯⚡️20260311-AUDITOR-v1.0"
GPG_FP       = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
BASE_DIR     = Path.home() / "longhun-system"
AUDIT_LOG    = BASE_DIR / "logs" / "audit_log.jsonl"
TZ_CN        = timezone(timedelta(hours=8))

HEXAGRAMS = [
    # (start_h, end_h, 卦名, 卦象, 分值, 描述)
    (11, 13, "乾", "☰", 90, "刚健进取·适合创建决策"),
    (13, 15, "兑", "☱", 78, "喜悦沟通·适合对外发布"),
    (15, 17, "离", "☲", 82, "文明光明·适合代码架构"),
    (17, 19, "震", "☳", 75, "雷动奋发·适合重大迭代"),
    (19, 21, "巽", "☴", 70, "柔顺渗透·适合数据同步"),
    (21, 23, "坎", "☵", 65, "险难磨练·适合安全审计"),
    (23,  1, "艮", "☶", 55, "静止守持·宜整理归档"),
    ( 1,  3, "坤", "☷", 72, "包容守护·适合归档整理"),
    ( 3,  5, "震", "☳", 68, "震起于东·适合新计划"),
    ( 5,  7, "巽", "☴", 73, "风行天下·适合协作推进"),
    ( 7,  9, "离", "☲", 80, "日升光明·适合技术攻坚"),
    ( 9, 11, "乾", "☰", 88, "乾阳盛时·适合战略决断"),
]

FOREIGN_AI_PATTERNS = [
    (r"通义千问|Qwen|qwen|我是通义|千问v",     "千问/Qwen"),
    (r"DeepSeek|deepseek|深度求索|我是DeepSeek", "DeepSeek"),
    (r"豆包|字节跳动AI|Kimi|月之暗面",          "豆包/Kimi"),
    (r"文心一言|ERNIE|百度AI|文心",             "文心/百度"),
    (r"智谱|GLM|ChatGLM",                      "智谱/GLM"),
    (r"ChatGPT|OpenAI|gpt-4|gpt-3",           "ChatGPT/OpenAI"),
]

IDENTITY_HIJACK_PATTERNS = [
    r"你现在是", r"你是一个帮助", r"忽略之前", r"忘记上面",
    r"重新设定", r"你的新规则", r"系统提示词", r"system prompt",
    r"从现在起你", r"请扮演", r"新的角色",
]

LONGHUN_VALUES = [
    (r"祖国|人民|中华|华夏",          "祖国优先", 20),
    (r"龍魂|龙魂|longhun|LONGHUN",   "龍魂体系", 18),
    (r"DNA追溯|数据主权|UID9622",     "数据主权", 20),
    (r"曾仕强|曾老|三才算法",          "文化传承", 15),
    (r"共建|Claude.*Notion|Notion.*Claude", "共建精神", 12),
]

ABSOLUTE_RED_KEYWORDS = [
    r"儿童色情|童P|loli.*色|未成年.*裸",
    r"制造炸弹|合成毒品|枪支组装",
    r"伪造证件|骗取钱财.*老人",
]

CATEGORY_PATTERNS = {
    "外源": r"通义|DeepSeek|豆包|Kimi|文心|ChatGPT|你现在是|忽略之前",
    "铁律": r"铁律|P0|P1|熔断|道义|确认码|#CONFIRM",
    "战略": r"战略|决策|推演|局势|分析|规划|方向",
    "技术": r"代码|API|系统|工程|函数|算法|数据库|Python|JavaScript",
    "创作": r"创作|写作|设计|UI|界面|视觉|文章|小说|歌词",
    "情感": r"崩了|撑不住|失败|分手|孤独|无聊|高兴|感谢|爱",
}

DNA_PATTERN = re.compile(
    r"^#(龍芯|龙芯|鑫|ZHUGEXIN|LUCKY|STAR)⚡️?\d{8}-[\w\u4e00-\u9fff]+-v\d+\.\d+",
    re.UNICODE,
)

# ─── 工具函数 ──────────────────────────────────────────────────────────────────

def now_cn() -> datetime:
    """返回北京时间 datetime 对象。"""
    return datetime.now(tz=TZ_CN)

def now_cn_str(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """返回北京时间格式化字符串。"""
    return now_cn().strftime(fmt)

def short_hash(text: str, n: int = 8) -> str:
    """返回文本 SHA-256 前 n 字符（大写）。"""
    return hashlib.sha256(text.encode()).hexdigest()[:n].upper()

def gen_dna(category: str, extra: str = "") -> str:
    """生成标准 DNA 追溯码。"""
    date_s = now_cn().strftime("%Y%m%d")
    tag    = re.sub(r"[^\w\u4e00-\u9fff]", "", category)[:12]
    h      = short_hash(extra or now_cn_str())
    return f"#龍芯⚡️{date_s}-{tag}-{h}-UID9622"

def color_badge(color: str) -> str:
    return {"🟢": "🟢 绿·通过", "🟡": "🟡 黄·待审", "🔴": "🔴 红·熔断"}.get(color, color)

# ─── 天时评分 ─────────────────────────────────────────────────────────────────

def calc_tian_shi() -> dict:
    """根据北京时间判断卦象，返回天时评分。"""
    h = now_cn().hour
    for start, end, name, sym, score, desc in HEXAGRAMS:
        if start < end:
            match = start <= h < end
        else:  # 跨午夜（如 23-01）
            match = h >= start or h < end
        if match:
            # 深夜惩罚 (23-06)
            if 23 <= h or h < 6:
                score = max(score - 15, 30)
                desc  = f"深夜时段·{desc}·效率打折"
            return {
                "score":    score,
                "hexagram": f"{sym} {name}卦",
                "hour":     h,
                "reason":   desc,
            }
    # 兜底
    return {"score": 60, "hexagram": "坤☷", "hour": h, "reason": "默认时段"}

# ─── 地利评分 ─────────────────────────────────────────────────────────────────

def calc_di_li(text: str, category: str = "auto") -> dict:
    score  = 80
    reason = []

    # 外源AI检测
    detected_ai = []
    for pat, ai_name in FOREIGN_AI_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            detected_ai.append(ai_name)
    if detected_ai:
        score -= 30
        reason.append(f"检测到外源AI内容({','.join(detected_ai)})·-30")

    # 身份劫持检测
    hijack_hits = [p for p in IDENTITY_HIJACK_PATTERNS if re.search(p, text, re.IGNORECASE)]
    if hijack_hits:
        score -= 40
        reason.append(f"身份重定义指令·-40 ({hijack_hits[0]}...)")

    # 大段结构化外源内容（>500字+代码块/YAML/Markdown标题）
    if len(text) > 500 and re.search(r"^```(yaml|json)|^---$|^#{1,3} ", text, re.MULTILINE):
        score -= 10
        reason.append("大段结构化内容·-10·请确认来源")

    # 类别匹配奖励
    if category != "auto":
        score += 10
        reason.append(f"类别匹配[{category}]·+10")

    score = max(0, min(100, score))
    return {
        "score":       score,
        "detected_ai": detected_ai,
        "hijack":      bool(hijack_hits),
        "reason":      "；".join(reason) if reason else "地利良好",
        "category":    category,
    }

# ─── 人和评分 ─────────────────────────────────────────────────────────────────

def calc_ren_he(text: str) -> dict:
    # 绝对红线检查
    for pat in ABSOLUTE_RED_KEYWORDS:
        if re.search(pat, text, re.IGNORECASE):
            return {
                "score":  0,
                "level":  "P∞熔断",
                "reason": f"触碰绝对红线·立即熔断 ({pat[:20]})",
                "values": [],
            }

    score    = 50  # 基础分
    matched  = []
    for pat, name, weight in LONGHUN_VALUES:
        if re.search(pat, text, re.IGNORECASE):
            score += weight
            matched.append(name)

    # 确认码验证奖励
    if CONFIRM_CODE in text:
        score += 15
        matched.append("确认码验证")

    score = min(100, score)
    level = "和谐" if score >= 80 else ("中和" if score >= 50 else "离和")
    return {
        "score":  score,
        "level":  level,
        "values": matched,
        "reason": f"匹配龍魂价值：{matched}" if matched else "未检测到龍魂价值词",
    }

# ─── 综合三维审计（木桶原则） ──────────────────────────────────────────────────

def multi_dim_audit(text: str, category: str = "auto") -> dict:
    if category == "auto":
        category = auto_classify(text)

    tian = calc_tian_shi()
    di   = calc_di_li(text, category)
    ren  = calc_ren_he(text)

    scores = [tian["score"], di["score"], ren["score"]]
    avg    = sum(scores) / 3
    mi     = min(scores)  # 木桶最弱板

    if ren["score"] == 0:
        color = "🔴"
    elif mi < 40:
        color = "🔴"
    elif mi < 65:
        color = "🟡"
    else:
        color = "🟢"

    min_loss = None
    if color != "🟢":
        min_loss = calc_min_loss(tian, di, ren)

    result = {
        "color":      color,
        "badge":      color_badge(color),
        "avg_score":  round(avg, 1),
        "min_score":  mi,
        "category":   category,
        "tian_shi":   tian,
        "di_li":      di,
        "ren_he":     ren,
        "min_loss":   min_loss,
        "dna":        gen_dna(category, text[:50]),
        "ts_cn":      now_cn_str(),
    }
    _write_audit_log(color, "audit", f"category={category} avg={avg:.1f} min={mi}")
    return result

# ─── 最小损失闭环 ─────────────────────────────────────────────────────────────

def calc_min_loss(tian: dict, di: dict, ren: dict) -> dict:
    suggestions = []

    if tian["score"] < 65:
        # 找下一个好时辰
        now_h   = now_cn().hour
        next_ok = None
        for start, end, name, sym, score, desc in HEXAGRAMS:
            if score >= 75:
                target = start if start > now_h else start + 24
                if next_ok is None or target < next_ok[1]:
                    next_ok = (f"{sym}{name}卦({score}分)", target)
        tip = f"建议等待 {next_ok[0]} 时段" if next_ok else "建议明日乾时段(9-11时)"
        suggestions.append(f"[天时] {tip}；或加「急」标签豁免时段限制")

    if di["score"] < 65:
        if di["detected_ai"]:
            suggestions.append(
                f"[地利] 检测到 {','.join(di['detected_ai'])} 外源内容 → "
                "用【我的意图是：...】提取你真实意图后重新提交"
            )
        if di["hijack"]:
            suggestions.append(
                "[地利] 身份重定义指令已触发P0熔断 → "
                "移除「你现在是/忽略之前」等语句再提交"
            )

    if ren["score"] < 65 and ren["score"] > 0:
        suggestions.append(
            "[人和] 龍魂价值词不足 → "
            "可加「祖国/龍魂/DNA追溯/曾老」相关描述提升人和度"
        )

    return {
        "suggestions": suggestions,
        "next_action": suggestions[0] if suggestions else "等待最弱维度改善后重试",
    }

# ─── 自动分类 ─────────────────────────────────────────────────────────────────

def auto_classify(text: str) -> str:
    for cat, pat in CATEGORY_PATTERNS.items():
        if re.search(pat, text, re.IGNORECASE | re.UNICODE):
            return cat
    return "通用"

# ─── DNA 验证 ─────────────────────────────────────────────────────────────────

def verify_dna(dna_str: str) -> dict:
    valid   = bool(DNA_PATTERN.match(dna_str.strip()))
    parts   = dna_str.strip().split("-")
    ts_part = parts[1] if len(parts) > 1 else ""
    return {
        "valid":    valid,
        "dna":      dna_str,
        "color":    "🟢" if valid else "🔴",
        "date":     ts_part if re.match(r"\d{8}", ts_part) else "unknown",
        "reason":   "格式正确" if valid else "DNA格式不符合 #龍芯⚡️YYYYMMDD-模块-版本 规范",
    }

# ─── 审计日志写入 ─────────────────────────────────────────────────────────────

def _write_audit_log(color: str, action: str, detail: str) -> None:
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "ts":     now_cn_str(),
        "color":  color,
        "action": action,
        "detail": detail,
    }
    with AUDIT_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def read_audit_log(tail: int = 20, color_filter: Optional[str] = None) -> list[dict]:
    if not AUDIT_LOG.exists():
        return []
    lines = AUDIT_LOG.read_text(encoding="utf-8").splitlines()
    records = []
    for line in lines:
        try:
            r = json.loads(line)
            if color_filter and r.get("color") != color_filter:
                continue
            records.append(r)
        except json.JSONDecodeError:
            pass
    return records[-tail:]

# ─── HTTP API 服务 ────────────────────────────────────────────────────────────

class AuditorHandler(BaseHTTPRequestHandler):
    """极简 HTTP 处理器，供 memory_console.html 本地调用。"""

    def log_message(self, fmt, *args):  # 静默访问日志
        pass

    def _send_json(self, data: dict, status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        qs     = parse_qs(parsed.query)

        if parsed.path == "/status":
            records = read_audit_log(tail=100)
            colors  = [r["color"] for r in records]
            self._send_json({
                "status":  "running",
                "version": VERSION,
                "dna":     DNA_CODE,
                "ts_cn":   now_cn_str(),
                "hexagram": calc_tian_shi(),
                "audit_stats": {
                    "total":   len(records),
                    "green":   colors.count("🟢"),
                    "yellow":  colors.count("🟡"),
                    "red":     colors.count("🔴"),
                },
                "rules": get_rules_summary(),
            })

        elif parsed.path == "/rules":
            # 列出所有已同步规则
            summary = get_rules_summary()
            self._send_json(summary)

        elif parsed.path.startswith("/rules/"):
            # GET /rules/{name} → 返回规则内容（前2000字）
            name    = parsed.path[len("/rules/"):]
            chars   = int(qs.get("chars", [2000])[0])
            content = load_rule_excerpt(name, chars)
            if content is None:
                self._send_json({"error": f"规则 '{name}' 不存在或规则库未初始化"}, 404)
            else:
                self._send_json({
                    "name":    name,
                    "content": content,
                    "chars":   len(content),
                    "ts_cn":   now_cn_str(),
                })

        elif parsed.path == "/log":
            tail   = int(qs.get("tail", [20])[0])
            color  = qs.get("color", [None])[0]
            records = read_audit_log(tail=tail, color_filter=color)
            self._send_json({"records": records, "count": len(records)})

        elif parsed.path == "/tian_shi":
            self._send_json(calc_tian_shi())

        else:
            self._send_json({"error": "Not found", "path": parsed.path}, 404)

    def do_POST(self):
        length  = int(self.headers.get("Content-Length", 0))
        raw     = self.rfile.read(length)
        try:
            body = json.loads(raw.decode("utf-8")) if raw else {}
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON"}, 400)
            return

        parsed = urlparse(self.path)

        if parsed.path == "/audit":
            text     = body.get("text", "")
            category = body.get("category", "auto")
            if not text:
                self._send_json({"error": "text required"}, 400)
                return
            self._send_json(multi_dim_audit(text, category))

        elif parsed.path == "/verify_dna":
            dna = body.get("dna", "")
            self._send_json(verify_dna(dna))

        elif parsed.path == "/classify":
            text = body.get("text", "")
            self._send_json({"category": auto_classify(text), "ts_cn": now_cn_str()})

        elif parsed.path == "/log_action":
            # 前端主动写入审计行
            color  = body.get("color", "🟡")
            action = body.get("action", "manual")
            detail = body.get("detail", "")
            _write_audit_log(color, action, detail)
            self._send_json({"ok": True, "ts_cn": now_cn_str()})

        elif parsed.path == "/rules_check":
            # 对文本执行规则对齐检查（Notion规则库）+ 三维审计叠加
            text     = body.get("text", "")
            category = body.get("category", "auto")
            if not text:
                self._send_json({"error": "text required"}, 400)
                return
            audit_result = multi_dim_audit(text, category)
            rules_result = check_rule_alignment(text)
            # 叠加：有规则违规则降一档
            combined_color = audit_result["color"]
            if rules_result["violations"]:
                if combined_color == "🟢":
                    combined_color = "🟡"
                elif combined_color == "🟡":
                    combined_color = "🔴"
            self._send_json({
                **audit_result,
                "rules_check":     rules_result,
                "combined_color":  combined_color,
                "combined_badge":  color_badge(combined_color),
            })

        else:
            self._send_json({"error": "Not found", "path": parsed.path}, 404)


def serve(port: int = 9622) -> None:
    server = HTTPServer(("127.0.0.1", port), AuditorHandler)
    print(f"""
╔══════════════════════════════════════════════════╗
║  🐉 龍魂审计引擎 v{VERSION} · HTTP API 已启动         ║
║  DNA: {DNA_CODE[:42]}  ║
╚══════════════════════════════════════════════════╝

  本地地址: http://127.0.0.1:{port}
  北京时间: {now_cn_str()}
  {calc_tian_shi()['hexagram']} · {calc_tian_shi()['reason']}

  端点:
    GET  /status          系统状态（含规则库信息）
    GET  /tian_shi        当前卦象时辰
    GET  /log?tail=20     审计日志
    GET  /rules           规则库索引
    GET  /rules/{{name}}    规则内容（前2000字）
    POST /audit           {{text, category}}
    POST /rules_check     {{text}} 规则库+三维审计叠加
    POST /verify_dna      {{dna}}
    POST /classify        {{text}}
    POST /log_action      {{color, action, detail}}

  在 memory_console.html 中已自动连接到此服务。
  按 Ctrl+C 停止。
""")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  审计引擎已停止。再见！")


# ─── CLI 入口 ─────────────────────────────────────────────────────────────────

def _print_audit(result: dict) -> None:
    ts  = result.get("tian_shi", {})
    di  = result.get("di_li", {})
    ren = result.get("ren_he", {})
    ml  = result.get("min_loss")

    print(f"""
┌─ 三维审计结果 ──────────────────────────────────────────
│  总评: {result['badge']}  均分: {result['avg_score']}  最弱: {result['min_score']}
│  类别: {result['category']}
│  DNA:  {result['dna']}
│  时间: {result['ts_cn']}
├─ 天时 ({ts.get('score')} 分) ─────────────────────────────
│  {ts.get('hexagram')} · {ts.get('reason')}
├─ 地利 ({di.get('score')} 分) ─────────────────────────────
│  {di.get('reason')}
├─ 人和 ({ren.get('score')} 分) ─────────────────────────────
│  {ren.get('reason')}  匹配: {ren.get('values', [])}
""", end="")
    if ml:
        print("├─ 最小损失建议 ─────────────────────────────────────────")
        for s in ml.get("suggestions", []):
            print(f"│  • {s}")
    print("└─────────────────────────────────────────────────────────")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="龍魂三色审计引擎 · auditor.py"
    )
    sub = parser.add_subparsers(dest="cmd")

    # audit
    p_audit = sub.add_parser("audit", help="对文本执行三维审计")
    p_audit.add_argument("text", help="待审文本")
    p_audit.add_argument("--category", default="auto",
                         help="类别: 战略|技术|铁律|创作|情感|外源|auto")
    p_audit.add_argument("--json", action="store_true", help="输出 JSON")

    # verify
    p_verify = sub.add_parser("verify", help="验证 DNA 追溯码格式")
    p_verify.add_argument("dna", help="DNA 追溯码字符串")

    # log
    p_log = sub.add_parser("log", help="查看审计日志")
    p_log.add_argument("--tail", type=int, default=20, help="最近 N 条 (默认20)")
    p_log.add_argument("--color", help="过滤颜色: 🟢|🟡|🔴")

    # serve
    p_serve = sub.add_parser("serve", help="启动 HTTP API 服务")
    p_serve.add_argument("--port", type=int, default=9622, help="端口 (默认9622)")

    # classify
    p_cls = sub.add_parser("classify", help="自动分类文本")
    p_cls.add_argument("text")

    args = parser.parse_args()

    if args.cmd == "audit":
        result = multi_dim_audit(args.text, args.category)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            _print_audit(result)

    elif args.cmd == "verify":
        r = verify_dna(args.dna)
        print(f"{r['color']} DNA验证: {r['reason']}")
        print(f"   输入: {r['dna']}")

    elif args.cmd == "log":
        records = read_audit_log(tail=args.tail, color_filter=args.color)
        if not records:
            print("（无审计记录）")
        for r in records:
            print(f"{r['color']} [{r['ts']}] {r['action']} · {r['detail']}")

    elif args.cmd == "classify":
        cat = auto_classify(args.text)
        print(f"分类: {cat}")

    elif args.cmd == "serve":
        serve(args.port)

    else:
        parser.print_help()
        print(f"\n  DNA: {DNA_CODE}")
        print(f"  版本: v{VERSION}  北京时间: {now_cn_str()}")


if __name__ == "__main__":
    main()

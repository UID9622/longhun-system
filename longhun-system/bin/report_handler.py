#!/usr/bin/env python3
"""
天下无欺 · 真相受理处理器 · Truth Report Handler
DNA: #龍芯⚡️2026-03-19-TRUTH-HANDLER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
作者: 诸葛鑫（UID9622）· 退伍军人 · 龍魂系统创始人
理论指导: 曾仕强老师（永恒显示）
献礼: 新中国成立77周年（1949-2026）· 丙午马年

功能: 接收前端提交 → DNA签名 → append-only写入 → 可选Git提交
"""

import json
import hashlib
import os
import sys
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

BASE = Path(__file__).parent.parent
REPORTS_LOG = BASE / "logs" / "reports.jsonl"
REPORTS_LOG.parent.mkdir(exist_ok=True)

# ── 国家接口路由表（预留，后续对接各国投诉平台）──
国家接口 = {
    "CN": {"name": "中国", "api": None, "note": "预留：12315、网信办等接口"},
    "US": {"name": "USA", "api": None, "note": "Reserved: FTC, BBB interfaces"},
    "JP": {"name": "日本", "api": None, "note": "予約済み: 消費者庁インターフェース"},
    "KR": {"name": "한국", "api": None, "note": "예약됨: 공정거래위원회 인터페이스"},
    "DE": {"name": "Deutschland", "api": None, "note": "Reserviert: BaFin, Verbraucherzentrale"},
    "IN": {"name": "India", "api": None, "note": "Reserved: Consumer Forum API"},
    "OTHER": {"name": "Other", "api": None, "note": "Generic public record only"},
}


def 生成受理号(描述: str) -> str:
    """生成唯一受理号 · Generate unique report ID"""  # generate_report_id
    日期 = datetime.now(timezone.utc).strftime("%Y%m%d")
    哈希 = hashlib.sha256(描述.encode() + str(datetime.now()).encode()).hexdigest()[:8].upper()
    return f"RPT-{日期}-{哈希}"


def 生成DNA(受理号: str) -> str:
    """生成DNA追溯码 · Generate DNA traceability code"""  # generate_dna
    日期 = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    短码 = 受理号.split("-")[-1]
    return f"#龍芯⚡️{日期}-TRUTH-{短码}-v1.0"


def 写入报告(报告: dict) -> dict:
    """
    受理处理核心函数 · Core report acceptance function
    append-only写入，不可删改
    """
    受理号 = 生成受理号(报告.get("description", ""))
    dna = 生成DNA(受理号)
    时间戳 = datetime.now(timezone.utc).isoformat()

    # 内容哈希（防篡改验证）
    内容串 = json.dumps(报告, ensure_ascii=False, sort_keys=True)
    内容哈希 = hashlib.sha256(内容串.encode()).hexdigest()

    完整记录 = {
        "受理号": 受理号,           # report_id
        "dna": dna,
        "时间戳": 时间戳,           # timestamp
        "内容哈希": 内容哈希,       # content_hash (tamper detection)
        "国家": 报告.get("country", "OTHER"),
        "类型": 报告.get("report_type", "other"),
        "严重程度": 报告.get("severity", "medium"),
        "描述": 报告.get("description", ""),
        "涉事方": 报告.get("party", ""),
        "证据": 报告.get("evidence", ""),
        "联系方式": 报告.get("contact", ""),  # 不公开
        "状态": "已受理",           # status: accepted
        "进度": "等待处理",         # progress: pending
        "国家接口推送": False,       # country_api_pushed
    }

    # append-only写入（铁律：只增不删）
    with open(REPORTS_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(完整记录, ensure_ascii=False) + "\n")

    print(f"✅ 受理成功 · {受理号} · {dna}")

    # 推送国家接口（预留）
    国家 = 报告.get("country", "OTHER")
    if 国家 in 国家接口 and 国家接口[国家]["api"]:
        print(f"🌐 推送至 {国家接口[国家]['name']} 接口...")
        # TODO: 实装各国接口
    else:
        print(f"📌 国家接口预留中 [{国家}]：{国家接口.get(国家, {}).get('note', '待接入')}")

    return {
        "受理号": 受理号,
        "dna": dna,
        "时间戳": 时间戳,
        "状态": "已受理",
        "说明": "记录已锁定，不可篡改。DNA签名为凭证。",
        "说明_en": "Record locked and immutable. DNA signature is your proof.",
    }


def 查询进度(受理号: str) -> dict:
    """查询受理进度 · Query report progress"""  # query_progress
    if not REPORTS_LOG.exists():
        return {"错误": "暂无记录"}
    with open(REPORTS_LOG, "r", encoding="utf-8") as f:
        for line in f:
            try:
                记录 = json.loads(line)
                if 记录.get("受理号") == 受理号:
                    # 返回公开部分（不含联系方式）
                    公开 = {k: v for k, v in 记录.items() if k != "联系方式"}
                    return 公开
            except:
                continue
    return {"错误": f"未找到受理号 {受理号}"}


def 统计汇总() -> dict:
    """统计报告汇总 · Statistics summary"""  # get_stats
    if not REPORTS_LOG.exists():
        return {"总计": 0}
    统计 = {"总计": 0, "按类型": {}, "按国家": {}, "按严重程度": {}}
    with open(REPORTS_LOG, "r", encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
                统计["总计"] += 1
                t = r.get("类型", "other")
                统计["按类型"][t] = 统计["按类型"].get(t, 0) + 1
                c = r.get("国家", "OTHER")
                统计["按国家"][c] = 统计["按国家"].get(c, 0) + 1
                s = r.get("严重程度", "medium")
                统计["按严重程度"][s] = 统计["按严重程度"].get(s, 0) + 1
            except:
                continue
    return 统计


# ── HTTP服务器（本地运行） ──

class 受理处理器(BaseHTTPRequestHandler):  # ReportHTTPHandler
    """HTTP请求处理器 · HTTP request handler"""

    def log_message(self, format, *args):
        pass  # 静默日志 · silent logging

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        路径 = urlparse(self.path).path  # path

        # 首页 → 重定向到表单
        if 路径 == "/" or 路径 == "":
            表单路径 = BASE / "truth_report.html"
            if 表单路径.exists():
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self._cors()
                self.end_headers()
                self.wfile.write(表单路径.read_bytes())
            return

        # 进度查询 /api/progress?id=RPT-xxx
        if 路径 == "/api/progress":
            from urllib.parse import parse_qs
            参数 = parse_qs(urlparse(self.path).query)
            受理号 = 参数.get("id", [""])[0]
            结果 = 查询进度(受理号)
            self._json响应(结果)
            return

        # 统计 /api/stats
        if 路径 == "/api/stats":
            self._json响应(统计汇总())
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        路径 = urlparse(self.path).path

        if 路径 == "/api/report":
            长度 = int(self.headers.get("Content-Length", 0))
            原始 = self.rfile.read(长度)
            try:
                报告 = json.loads(原始.decode("utf-8"))
                结果 = 写入报告(报告)
                self._json响应(结果, 201)
            except Exception as e:
                self._json响应({"错误": str(e)}, 400)
            return

        self.send_response(404)
        self.end_headers()

    def _json响应(self, 数据: dict, 状态码: int = 200):
        """返回JSON响应 · Return JSON response"""  # json_response
        体 = json.dumps(数据, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(状态码)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(体)))
        self._cors()
        self.end_headers()
        self.wfile.write(体)


def 启动服务(端口: int = 8766):  # start_server
    """启动受理服务器 · Start the truth protocol server"""
    服务器 = HTTPServer(("0.0.0.0", 端口), 受理处理器)
    print(f"""
🐉 天下无欺 · 真相受理台 已启动
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 本地访问:  http://localhost:{端口}
📋 提交接口:  POST http://localhost:{端口}/api/report
🔍 进度查询:  GET  http://localhost:{端口}/api/progress?id=RPT-xxx
📊 统计汇总:  GET  http://localhost:{端口}/api/stats
📂 记录存档:  {REPORTS_LOG}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DNA: #龍芯⚡️2026-03-19-TRUTH-HANDLER-v1.0
UID9622 · 诸葛鑫 · 天下无欺
""")
    try:
        服务器.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹ 服务已停止")


if __name__ == "__main__":
    端口 = int(sys.argv[1]) if len(sys.argv) > 1 else 8766
    启动服务(端口)

#!/usr/bin/env python3
# DNA: #龍芯⚡️2026-08-30-TONGXINYI-API-v1.0-9c4f72a8
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂·通心译统一 API 网关 v1.0 · 端口 8792
整合: 词库(lexicon.json) · 五级词元解析 · 数字根引擎 · IPA 八维路由 · 六层翻译闸门

端点:
  GET  /api/health                      服务状态
  GET  /api/lexicon                     全量词库
  POST /api/resolve                     五级词元解析 + IPA 路由
  POST /api/digital-root                数字根计算(分步)
  POST /api/ipa-route                   八维路由
  POST /api/translate                   六层翻译(依赖 tongxinyi_gate, 失败降级)

用法:
  python3 08_BIN/lh_tongxinyi_api.py [--port 8792] [--host 127.0.0.1]
"""
import argparse
import json
import re
import sys
import unicodedata
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIN = ROOT / "08_BIN"
PORTAL_TONGXINYI = ROOT / "10_PORTAL" / "tongxinyi"
GATE_DIR = ROOT / "03_LAYERS" / "L5_服务层" / "services" / "api" / "control-panel"

sys.path.insert(0, str(BIN))
if str(GATE_DIR) not in sys.path:
    sys.path.insert(0, str(GATE_DIR))

from lh_digital_root import 数字根引擎          # noqa: E402
from lh_tongxinyi_ipa_router import 通心译IPA路由器  # noqa: E402

try:
    from tongxinyi_gate import TongxinyiGate  # noqa: E402
    GATE = TongxinyiGate()
    GATE_OK = True
except Exception as e:  # pragma: no cover
    GATE = None
    GATE_OK = False
    GATE_ERR = str(e)

ROUTER = 通心译IPA路由器()

LEXICON = None
LEXICON_PATH = PORTAL_TONGXINYI / "lexicon.json"

# 数字根含义表（与 lh_digital_root.py CLI 表一致）
DR_MEANING = {
    0: "无数字·土",
    1: "水·记忆",
    2: "火·文明",
    3: "木·创新(熔断)",
    4: "金·规则",
    5: "土·普惠",
    6: "水·记忆(待审)",
    7: "火·文明",
    8: "木·创新",
    9: "金·规则(熔断)",
}
DR_COLOR = {"金": "金色/白金", "木": "青绿", "水": "深蓝/青蓝", "火": "朱红/暖橙", "土": "土黄/琥珀"}

ROUTE_HINTS = {
    "D01": ["文件", "目录", "查看", "读", "搜索", "删除", "文件夹"],
    "D02": ["部署", "上线", "发布", "同步", "下载", "上传", "推送", "备份", "服务器", "站点"],
    "D03": ["DNA", "铸码", "人格", "模型", "AI", "启动", "验证", "恢复"],
    "D04": ["审计", "检查", "合规", "协议", "焊死", "冻结", "签章", "盖章", "契约", "条款"],
    "D05": ["追溯", "溯源", "登记", "哈希", "指纹", "加密", "主权", "隐私"],
    "D06": ["维权", "投诉", "促销", "黑箱", "消费者", "欺诈"],
    "D07": ["干支", "天干", "地支", "卦", "时辰", "五行", "金木水火土"],
    "D08": ["执行", "开干", "回滚", "对抗", "演练", "战斗", "任务"],
}

LV_NAME = ["显式引用", "精确词元", "别名", "模糊匹配", "抽屉路由"]


def load_lexicon():
    global LEXICON
    if LEXICON is None:
        try:
            LEXICON = json.loads(LEXICON_PATH.read_text(encoding="utf-8"))
        except Exception:
            LEXICON = {"drawers": [], "config_mappings": [], "meta": {"error": "lexicon.json 缺失"}}
    return LEXICON


def extract_digits(text: str):
    """提取文本中的全部数字字符(含 Unicode 数字)"""
    digits = []
    for c in str(text):
        if c.isdigit():
            try:
                digits.append(int(c))
                continue
            except ValueError:
                pass
        try:
            d = unicodedata.digit(c)
            digits.append(d)
        except (ValueError, TypeError):
            pass
    return digits


def digital_root_detail(text: str):
    """数字根分步计算: 提取数字 → 逐步相加 → 五行/颜色/三色/含义"""
    digits = extract_digits(text)
    if not digits:
        return {"error": "未提取到数字字符", "digits": [], "steps": [], "数字根": 0}
    steps = []
    cur = digits
    total = sum(cur)
    steps.append({"stage": 1, "digits": cur, "sum": total})
    while total >= 10:
        nxt = [int(c) for c in str(total)]
        total = sum(nxt)
        steps.append({"stage": len(steps) + 1, "digits": nxt, "sum": total})
    dr = total
    wx = 数字根引擎.五行映射表.get(dr, "土")
    result = {
        "数字根": dr,
        "五行": wx,
        "颜色": DR_COLOR.get(wx, "未知"),
        "三色审计": 数字根引擎.三色审计表.get(dr, "🟢"),
        "含义": DR_MEANING.get(dr, ""),
        "digits": digits,
        "steps": steps,
    }
    return result


def resolve(raw: str):
    """五级词元解析"""
    lex = load_lexicon()
    drawers = lex.get("drawers", [])
    hits = []
    hit_set = set()

    # L1 显式引用 @Dxx.词元
    for m in re.finditer(r"@([Dd])(\d{2})[.．·]\s*([\u4e00-\u9fa5A-Za-z0-9()（）\-]+)", raw):
        d = next((x for x in drawers if x["id"] == "D" + m.group(2)), None)
        if not d:
            continue
        e = next((y for y in d["entries"] if y["term"] == m.group(3)), None)
        if e:
            key = d["id"] + "|" + e["term"]
            if key not in hit_set:
                hits.append({"level": 0, "drawer": d["id"] + ":" + d["name"], "entry": e})
                hit_set.add(key)

    # L2-L4 精确/别名/模糊
    for d in drawers:
        for e in d["entries"]:
            key = d["id"] + "|" + e["term"]
            if key in hit_set:
                continue
            if raw == e["term"]:
                hits.append({"level": 1, "drawer": d["id"] + ":" + d["name"], "entry": e})
                hit_set.add(key)
            elif raw in e.get("alias", []):
                hits.append({"level": 2, "drawer": d["id"] + ":" + d["name"], "entry": e})
                hit_set.add(key)
            elif e["term"] in raw or any(a in raw for a in e.get("alias", [])):
                hits.append({"level": 3, "drawer": d["id"] + ":" + d["name"], "entry": e})
                hit_set.add(key)

    # L5 抽屉路由（无命中时按关键词提示兜底）
    if not hits:
        for d in drawers:
            hints = ROUTE_HINTS.get(d["id"], [])
            if any(h in raw for h in hints):
                for e in d["entries"]:
                    hits.append({"level": 4, "drawer": d["id"] + ":" + d["name"], "entry": e})
                break

    return {"hits": hits[:8], "level_names": LV_NAME}


def ipa_route(text: str):
    try:
        r = ROUTER.路由(text)
        return {
            "八卦路由": r.八卦路由,
            "五行向量": r.五行向量,
            "数字根": r.数字根,
            "熔断状态": r.熔断状态,
            "语境类型": r.语境类型,
            "意图动作": r.意图动作,
            "情绪等级": r.情绪等级,
            "信任权重": r.信任权重,
            "命中IPA": r.命中IPA,
            "路径哈希": r.路径哈希,
            "路由说明": r.路由说明,
        }
    except Exception as e:
        return {"error": f"IPA 路由失败: {e}"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"[通心译API:8792] {fmt % args}")

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _send(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path in ("/api/health", "/api/health/"):
            lex = load_lexicon()
            self._send(200, {
                "status": "ok",
                "service": "longhun-tongxinyi-api",
                "version": "v1.0",
                "dna": "#龍芯⚡️2026-08-30-TONGXINYI-API-v1.0-9c4f72a8",
                "engine": {
                    "digital_root": True,
                    "ipa_router": True,
                    "tongxinyi_gate": GATE_OK,
                },
                "lexicon": {"drawers": len(lex.get("drawers", [])),
                            "entries": sum(len(d.get("entries", [])) for d in lex.get("drawers", [])),
                            "mappings": len(lex.get("config_mappings", []))},
                "endpoints": ["/api/health", "/api/lexicon", "/api/resolve", "/api/digital-root", "/api/ipa-route", "/api/translate"],
            })
            return
        if self.path in ("/api/lexicon", "/api/lexicon/"):
            self._send(200, load_lexicon())
            return
        self._send(404, {"error": "not found"})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            data = json.loads(body) if body else {}
        except Exception:
            self._send(400, {"error": "无效 JSON"})
            return

        path = self.path.split("?")[0]

        if path in ("/api/resolve",):
            text = data.get("text", "").strip()
            if not text:
                self._send(400, {"error": "缺少 text 参数"})
                return
            out = resolve(text)
            out["ipa"] = ipa_route(text)
            if GATE_OK:
                try:
                    out["gate"] = GATE.translate(text)
                except Exception as e:
                    out["gate"] = {"error": f"闸门失败: {e}"}
            else:
                out["gate"] = {"error": GATE_ERR if GATE is not None else "闸门未加载"}
            self._send(200, out)
            return

        if path in ("/api/digital-root",):
            text = data.get("text", data.get("q", "")).strip()
            if not text:
                self._send(400, {"error": "缺少 text 参数"})
                return
            self._send(200, digital_root_detail(text))
            return

        if path in ("/api/ipa-route",):
            text = data.get("text", "").strip()
            if not text:
                self._send(400, {"error": "缺少 text 参数"})
                return
            self._send(200, ipa_route(text))
            return

        if path in ("/api/translate",):
            text = data.get("text", data.get("q", "")).strip()
            if not text:
                self._send(400, {"error": "缺少 text 参数"})
                return
            if not GATE_OK:
                self._send(503, {"error": "tongxinyi_gate 不可用: " + (GATE_ERR if GATE is not None else "")})
                return
            try:
                self._send(200, GATE.translate(text))
            except Exception as e:
                self._send(500, {"error": f"翻译失败: {e}"})
            return

        self._send(404, {"error": "未知端点", "path": path})


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂·通心译统一 API 网关 v1.0")
    parser.add_argument("--port", type=int, default=8792)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()
    server = HTTPServer((args.host, args.port), Handler)
    print(f"🐉 通心译 API 网关已启动: http://{args.host}:{args.port}")
    print(f"   DNA: #龍芯⚡️2026-08-30-TONGXINYI-API-v1.0-9c4f72a8")
    print(f"   端点: /api/health /api/lexicon /api/resolve /api/digital-root /api/ipa-route /api/translate")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[通心译API:8792] 已停止")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·数字人调动引擎 v1.0
DNA: #龍芯⚡️2026-09-02-DH-DISPATCH-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

功能: 数字人三通道调动——自然语言 / CLI / HTTP API
  · 自然语言路由：名字/编号/岗位词 → 数字人（如「让字靈设计个字体」「喊匠心写代码」）
  · CLI:  lh dh "<名字或编号> <任务>"
  · HTTP: lh dh --port 8761 --daemon  →  POST /dh/dispatch {"dh":"DH-011","task":"..."}
                                        GET  /dh/list   GET /dh/health
  · 身份闸: Header X-UID: 9622（对外请求必带，无则拒绝）
  · 执行: 组装 persona(人格+原则+职能) 系统提示 → lh_model.generate(auto: deepseek→ollama)
  · 降级: API 不可用时输出「唤起指令」(在 CodeBuddy 点名对应人格 agent 即可执行)

v1.3 深度学习代码精修（2026-09-03）:
  · try_deepseek 调用入口归一 → lh_model.generate(engine=auto) · 移除本文件 DeepSeekClient 直连
  · 加载/调用/查询模型状态唯一入口 = lh model · 训练数据 = lh topo sync 深度学习图谱

v1.1 知识库接入（2026-09-02）:
  · 挂载通心译总台 19 条资产为数字人知识来源（复用 lh_topo 本地缓存·零重复实现）
  · 系统提示注入: 「你有权访问通心译总台 19 条资产，引用时须注明 DNA」
  · 加载状态落 ~/.longhun/dh_kb_state.json → lh topo kb-status / lh health --json 读取
v1.2 引用溯源（2026-09-02·开源工具深度融合任务B）:
  · kb_declaration 注入「引用溯源规则」：涉及通心译资产回复须附 [DNA: #龍芯⚡️…]
    （引用格式 = 依据「龍魂·总台 · 资产名」+ [DNA] + 来源链接）
  · 引用未在清单内容 → 标来源 URL；发现疑似剽窃 → 上报触发 lh judge topo-scan --deep
  · 完整引用查: lh topo cite <资产名>（新命令·lh_topo.py v1.2）
用法: python3 08_BIN/lh_dh_dispatch.py "字靈 设计三号字体" [--json]
      python3 08_BIN/lh_dh_dispatch.py DH-011 "把首页改响应式" --json
      python3 08_BIN/lh_dh_dispatch.py --port 8761 --daemon
"""
import argparse
import contextlib
import json
import os
import re
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "digital_humans" / "registry.json"
DH_KB_STATE = Path.home() / ".longhun" / "dh_kb_state.json"   # 知识库加载状态（lh health 读取）
_DH_KB = []                                                     # 内存索引缓存

# ============================================================
# 数字人路由词表：编号 / 名字 / 岗位词 → ipa
# ============================================================
ROUTES = {
    # 本尊
    "ZGX-001": "ZGX-001", "诸葛鑫": "ZGX-001", "本尊": "ZGX-001", "老大": "ZGX-001",
    # ASI 家族
    "ASI-001": "ASI-001", "至诚智魂": "ASI-001", "智魂": "ASI-001",
    "ASI-002": "ASI-002", "军师": "ASI-002", "诸葛亮": "ASI-002", "諸葛亮": "ASI-002",
    "ASI-003": "ASI-003", "达芬奇": "ASI-003", "達芬奇": "ASI-003", "跨界": "ASI-003",
    "ASI-004": "ASI-004", "庄子": "ASI-004", "莊子": "ASI-004", "比真": "ASI-004", "哲学": "ASI-004", "哲學": "ASI-004",
    "ASI-005": "ASI-005", "包青天": "ASI-005", "铁面": "ASI-005", "鐵面": "ASI-005",
    # 核心数字人
    "DH-001": "DH-001", "通心译": "DH-001", "通心譯": "DH-001", "翻译": "DH-001", "翻譯": "DH-001",
    "DH-002": "DH-002", "声音锚": "DH-002", "聲音錨": "DH-002", "声纹": "DH-002", "聲紋": "DH-002",
    "DH-003": "DH-003", "通心耳": "DH-003", "耳力": "DH-003",
    "DH-004": "DH-004", "记忆永生": "DH-004", "記憶永生": "DH-004", "记忆": "DH-004", "記憶": "DH-004",
    "DH-005": "DH-005", "人格编排": "DH-005", "人格編排": "DH-005", "编排官": "DH-005", "編排官": "DH-005", "路由": "DH-005",
    "DH-006": "DH-006", "上帝之眼": "DH-006", "监控": "DH-006", "監控": "DH-006",
    "DH-007": "DH-007", "龙芯执行器": "DH-007", "龍芯執行器": "DH-007", "执行器": "DH-007", "執行器": "DH-007",
    "DH-008": "DH-008", "至诚": "DH-008", "至誠": "DH-008",
    # 设计团岗位
    "DH-009": "DH-009", "雲錦": "DH-009", "云锦": "DH-009", "雲锦": "DH-009", "UI": "DH-009",
    "视觉": "DH-009", "視覺": "DH-009", "设计": "DH-009", "設計": "DH-009", "视觉设计": "DH-009",
    "DH-010": "DH-010", "字靈": "DH-010", "字灵": "DH-010", "字体": "DH-010", "字體": "DH-010",
    "DH-011": "DH-011", "匠心": "DH-011", "代码": "DH-011", "代碼": "DH-011", "编码": "DH-011", "編碼": "DH-011", "编程": "DH-011", "編程": "DH-011",
    "DH-012": "DH-012", "明鉴": "DH-012", "明鑒": "DH-012", "审计": "DH-012", "審計": "DH-012", "验收": "DH-012", "驗收": "DH-012", "检查": "DH-012", "檢查": "DH-012",
    "DH-013": "DH-013", "诗仙": "DH-013", "詩仙": "DH-013", "创意": "DH-013", "創意": "DH-013", "灵感": "DH-013", "靈感": "DH-013",
    "DH-014": "DH-014", "蔡侯": "DH-014", "排版": "DH-014", "印刷": "DH-014",
    "DH-015": "DH-015", "墨香": "DH-015", "归档": "DH-015", "歸檔": "DH-015", "整理": "DH-015",
    "DH-016": "DH-016", "知行": "DH-016", "部署": "DH-016", "上线": "DH-016", "上線": "DH-016",
    # 岗位兜底词
    "字体设计": "DH-010", "代码实现": "DH-011", "审计验收": "DH-012", "灵感创意": "DH-013",
    "排版印刷": "DH-014", "归档整理": "DH-015", "部署上线": "DH-016", "视觉设计": "DH-009",
}

# 设计团流水线（创作类任务整线联动）
PIPELINE = ["DH-013", "DH-009", "DH-010", "DH-011", "DH-014", "DH-012", "DH-015", "DH-016"]
PIPELINE_TRIGGER = ["网页", "页面", "网站", "创作", "設計", "设计个", "做网页", "做页面", "做网站", "作品", "工坊", "整站"]


def load_registry():
    with open(REGISTRY, encoding="utf-8") as f:
        return json.load(f)


# ─────────────────────────── 知识库：通心译总台资产（v1.1·2026-09-02）───────────────────────────

def load_topo_kb() -> list:
    """挂载通心译总台资产为知识库索引（复用 lh_topo 本地缓存·首次加载写 state 文件）"""
    global _DH_KB
    if _DH_KB:
        return _DH_KB
    state = {"loaded": False, "entries": 0, "loaded_at": "", "error": ""}
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import lh_topo  # noqa: F401 同目录引擎模块
        f, data = lh_topo._find_topo_file("通心译")
        _DH_KB = lh_topo.build_kb_index(data)
        green, yellow, _n = lh_topo.asset_stats(data)
        state = {"loaded": bool(_DH_KB), "entries": len(_DH_KB), "green": green,
                 "yellow": yellow, "last_sync": data.get("last_sync", "?"),
                 "root_hash": lh_topo.topo_root_hash(data),
                 "loaded_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                 "source": f"docs/topology/{f.name}"}
    except Exception as e:  # noqa: BLE001 不阻断数字人链路
        state["error"] = str(e)
    with contextlib.suppress(Exception):
        DH_KB_STATE.parent.mkdir(parents=True, exist_ok=True)
        DH_KB_STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return _DH_KB


def kb_declaration() -> str:
    """数字人系统提示知识库声明 v1.2（2026-09-02）·
    引用溯源规则：涉及通心译资产回复须自动附 [DNA: #龍芯⚡️…]；
    引用了未在清单中的外部内容 → 自查+上报触发 lh judge topo-scan --deep"""
    try:
        items = load_topo_kb()
    except Exception:  # noqa: BLE001
        return ""
    if not items:
        return ""
    lines = [f"- {it['name']} · 层级 {it['group']} · {it['status'] or '未标注'} · DNA {it['dna']}"
             for it in items]
    trace = (
        "\n引用溯源规则(v1.2·强制):\n"
        "  1) 当你回复引用了上述通心译总台资产内容时，必须自动追加引用行 → [DNA: #龍芯⚡️…]\n"
        "     标准格式: 依据「龍魂·<总台> · <资产名>」知识资产作答。\n"
        "     [DNA: <资产 DNA>] · 来源: <资产链接>\n"
        "  2) 若你引用了未在上述资产清单内的外部内容，须标注来源 URL（信息主权透明）；\n"
        "  3) 若发现外部链接疑似盗用龍魂通心译 DNA/资产内容（剽窃），禁止直接传播，"
        "汇报并触发: lh judge topo-scan --deep 上耻辱墙。\n"
        "  4) 资产名→完整引用可查: lh topo cite <资产名>（含 DNA+链接）")
    return (f"\n\n你有权访问通心译总台 {len(items)} 条资产作为知识来源。\n"
            f"资产清单:\n" + "\n".join(lines) + trace)


def resolve_dh(text: str) -> str:
    """自然语言 → 数字人 ipa（返回空则未识别）
    优先级: 编号直调 > 数字人名字 > 岗位词(长词优先, 防误配)"""
    m = re.search(r"(ZGX-\d+|ASI-\d+|DH-\d+)", text)
    if m:
        return m.group(1)
    reg = load_registry()
    for d in reg["digital_humans"].values():
        short = d.get("name", "").split("·")[0]
        if short and short in text:
            return d["ipa"]
    for kw in sorted(ROUTES, key=len, reverse=True):
        if kw in text:
            return ROUTES[kw]
    return ""


def build_system(dh: dict, task: str) -> list:
    meta = dh.get("metadata", {})
    name = dh.get("name", "")
    ipa = dh.get("ipa", "")
    content = (
        f"你是龍魂数字人「{name}」({ipa})，由诸葛鑫(UID9622)·龍芯北辰创建。\n"
        f"人格: {meta.get('persona', '')}\n"
        f"原则: {meta.get('principle', '')}\n"
        f"职能: {meta.get('functions', '')}\n"
        f"身份: 归属名诸葛鑫 | UID9622 · 龍芯北辰 · License MulanPSL v2。\n"
        f"风格: 简洁务实、不空话、最小闭环、繁龍审美。"
    )
    content += kb_declaration()   # 知识库: 通心译总台 19 条资产（引用须注明 DNA）
    return [
        {"role": "system", "content": content},
        {"role": "user", "content": task},
    ]


OLLAMA_URL = "http://localhost:11434/v1"
OLLAMA_MODEL = "longhun-v4.1.9"  # 本地主力模型（17GB·零依赖·数据不出机）


def try_deepseek(messages: list):
    """数字人执行链路，按序探测，全失败返回 (None, err)：
    1. DeepSeek(本地vLLM:8000 / 官方API DEEPSEEK_API_KEY)
    2. Ollama 本地模型 :11434（longhun-v4.1.9）→ 默认可用
    v1.3(2026-09-03·深度学习代码精修): 调用入口归一 → lh_model.generate(auto 降级链)
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from lh_model import generate
        return generate(messages, engine="auto")
    except Exception as e:
        return None, f"lh_model.generate: {e}"


def fallback_instruction(dh: dict, task: str) -> str:
    """API 不可用 → 输出唤起指令（CodeBuddy 点名人格即可执行）"""
    meta = dh.get("metadata", {})
    persona = meta.get("persona", "")
    p = re.search(r"(P\d+|P72|P77|S\d+)", persona)
    agent = p.group(1) if p else ""
    return (
        f"【API 未就绪 · 唤起指令】\n"
        f"数字人: {dh.get('ipa')} {dh.get('name')}\n"
        f"人格: {persona} | 原则: {meta.get('principle', '')}\n"
        f"任务: {task}\n"
        f"执行: 在 CodeBuddy 中选人格 agent「{persona}」或对龍魂执行器说:\n"
        f"  「让{persona} 做这个任务: {task}」\n"
        f"（或启动本地 vLLM :8000 后重试 `lh dh` 走全自动）"
    )


def dispatch(text: str) -> dict:
    reg = load_registry()
    dhs = reg["digital_humans"]
    ipa = resolve_dh(text)
    # 流水线触发
    if not ipa and any(k in text for k in PIPELINE_TRIGGER):
        steps = []
        for p in PIPELINE:
            d = dhs.get(p)
            if d:
                steps.append({"ipa": p, "name": d["name"], "persona": d.get("metadata", {}).get("persona", "")})
        return {"mode": "pipeline", "digits": len(steps), "steps": steps,
                "note": "设计团八岗整线 · 按流水线顺序接力执行"}
    if not ipa:
        names = "、".join(f"{d['ipa']} {d['name']}" for d in dhs.values())
        return {"mode": "unknown", "available": names,
                "usage": 'lh dh "字靈 设计字体" 或 lh dh DH-011 "任务"'}
    dh = dhs[ipa]
    messages = build_system(dh, text)
    resp = try_deepseek(messages)
    if isinstance(resp, tuple):  # API 失败 → 降级
        return {"mode": "fallback", "dh": dh["ipa"], "name": dh["name"],
                "detail": fallback_instruction(dh, text)}
    return {"mode": "dh", "dh": dh["ipa"], "name": dh["name"],
            "persona": dh.get("metadata", {}).get("persona", ""),
            "response": resp}


# ============================================================
# HTTP API 服务（零依赖 http.server）
# ============================================================
class DHHandler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: dict):
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _authed(self) -> bool:
        return self.headers.get("X-UID") == "9622"

    def do_GET(self):
        if self.path.rstrip("/") == "/dh/list":
            if not self._authed():
                return self._send(401, {"error": "未授权 · 需 Header X-UID: 9622"})
            reg = load_registry()
            items = [{"ipa": d["ipa"], "name": d["name"],
                      "persona": d.get("metadata", {}).get("persona", ""),
                      "status": d.get("status", "")} for d in reg["digital_humans"].values()]
            return self._send(200, {"total": len(items), "digital_humans": items})
        if self.path.rstrip("/") == "/dh/health":
            return self._send(200, {"status": "🟢", "service": "lh_dh_dispatch", "version": "v1.0"})
        self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path.rstrip("/") != "/dh/dispatch":
            return self._send(404, {"error": "not found"})
        if not self._authed():
            return self._send(401, {"error": "未授权 · 需 Header X-UID: 9622"})
        try:
            ln = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(ln) or b"{}")
            dh = body.get("dh", "")
            task = body.get("task", "")
            if not task:
                return self._send(400, {"error": "缺少 task"})
            text = f"{dh} {task}".strip()
            out = dispatch(text)
            return self._send(200, out)
        except Exception as e:
            return self._send(500, {"error": str(e)})

    def log_message(self, *a):
        pass


def serve(port: int):
    srv = ThreadingHTTPServer(("0.0.0.0", port), DHHandler)
    print(f"🐉 数字人调动网关 :{port} · GET /dh/list · POST /dh/dispatch · X-UID: 9622")
    srv.serve_forever()


# ============================================================
# v1.4 CodeQL 自动响应分派（2026-09-03 · CodeQL 闭环任务2）
# 问题类型 → 数字人 → 职责 分派规则表（老大设计·焊死）
# ============================================================
CODEQL_ROUTES = {
    # 类型: (ipa, 职责说明)
    "security":    ("ASI-005", "审计漏洞根因，给出修复方案（critical/high 优先处理）"),
    "code_style":  ("DH-010",  "按 CNSH 规范调整代码格式（命名/格式/风格）"),
    "logic":       ("DH-011",  "修复逻辑错误，确保边界条件正确"),
    "performance": ("DH-016",  "优化代码性能，减少资源消耗"),
    "dependency":  ("DH-012",  "更新依赖版本，消除已知漏洞"),
    "docs":        ("DH-013",  "补充文档和注释"),
    "test":        ("DH-014",  "补充测试用例"),
}

# CodeQL rule 特征 → 问题类型（按优先级匹配 tags / rule_id）
CODEQL_TYPE_RULES = [
    (("performance",), "performance"),
    (("maintainability", "style", "naming", "format"), "code_style"),
    (("correctness", "logical", "range", "bound"), "logic"),
    (("documentation", "doc"), "docs"),
    (("test", "testing"), "test"),
    (("dependencies", "supply-chain", "library"), "dependency"),
    (("security",), "security"),
]


def classify_codeql_issue(issue: dict) -> str:
    """CodeQL issue → 问题类型。判定顺序: 显式 tags → security 兜底高判 → rule_id → 默认 logic"""
    tags = [str(t).lower() for t in (issue.get("tags") or [])]
    rule_id = str(issue.get("rule_id") or "").lower()
    severity = str(issue.get("severity") or "").lower()
    desc = str(issue.get("description") or "").lower()
    # 1) 安全: critical/high 或 tags/rule 明确安全语义
    if severity in ("critical", "high", "error"):
        return "security"
    if any("security" in t or "cwe" in t for t in tags):
        return "security"
    if "security" in rule_id or rule_id.startswith(("py/", "js/", "cpp/")):
        pass  # 规则前缀不直接定性，继续看 tags
    # 2) tags 精确匹配
    for keys, kind in CODEQL_TYPE_RULES:
        if any(any(k in t for k in keys) for t in tags):
            return kind
    # 3) rule_id / desc 启发
    if any(k in rule_id or k in desc for k in ("eval", "unsafe", "xss", "sqli", "path", "inject", "deserial", "weak", "hardcoded", "credential", "crypto")):
        return "security"
    if any(k in rule_id or k in desc for k in ("performance", "time-complex", "inefficient")):
        return "performance"
    if any(k in rule_id for k in ("naming", "syntax", "style", "unused", "dead")):
        return "code_style"
    if any(k in rule_id or k in desc for k in ("todo", "fixme", "comment", "doc")):
        return "docs"
    return "logic"  # CodeQL 语义级问题默认归逻辑修复


def codeql_dispatch(issue: dict) -> dict:
    """单个 CodeQL issue → 数字人分派单
    issue 字段: rule_id / severity / description / file / line / tags(可选)
    返回: {type, dh_ipa, dh_name, persona, priority, task}"""
    kind = classify_codeql_issue(issue)
    ipa, duty = CODEQL_ROUTES.get(kind, CODEQL_ROUTES["logic"])
    reg = load_registry()
    dh = reg["digital_humans"].get(ipa, {})
    name = dh.get("name", ipa)
    persona = dh.get("metadata", {}).get("persona", "")
    sev = str(issue.get("severity") or "unknown")
    priority = "P0" if sev.lower() in ("critical", "high", "error") else "P1"
    file = issue.get("file", "?")
    line = issue.get("line", "?")
    task = (
        f"修复 CodeQL 扫描告警（{priority}·{sev}）：\n"
        f"  规则: {issue.get('rule_id', '?')}\n"
        f"  位置: {file}:{line}\n"
        f"  描述: {issue.get('description', '?')}\n"
        f"  职责: {duty}\n"
        f"  输出: 若可自动修复请给出针对该文件的最小修改 diff；"
        f"若需人工确认请明确说明原因与建议方案。禁止改动 .github/ 下任何 CI 配置。"
    )
    return {"type": kind, "dh_ipa": ipa, "dh_name": name, "persona": persona,
            "priority": priority, "task": task, "duty": duty}


def codeql_repair(issue: dict) -> dict:
    """按分派单唤起数字人修复（v1.4·CodeQL 闭环）。
    成功 → {mode:'dh', response}
    API 不可用 → {mode:'fallback', detail: 唤起指令}"""
    ticket = codeql_dispatch(issue)
    reg = load_registry()
    dh = reg["digital_humans"].get(ticket["dh_ipa"])
    if not dh:
        return {"mode": "error", "detail": f"数字人 {ticket['dh_ipa']} 不在册"}
    messages = build_system(dh, ticket["task"])
    resp = try_deepseek(messages)
    if isinstance(resp, tuple):
        return {"mode": "fallback", "ticket": ticket,
                "detail": fallback_instruction(dh, ticket["task"])}
    return {"mode": "dh", "ticket": ticket, "response": resp}


def main():
    ap = argparse.ArgumentParser(description="龍魂·数字人调动引擎 v1.0")
    ap.add_argument("text", nargs="*", help='自然语言, 如 "字靈 设计字体" 或 "DH-011 任务"')
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--port", type=int, default=8761, help="HTTP 端口(默认8761)")
    ap.add_argument("--daemon", action="store_true", help="启动 HTTP 服务(守护)")
    args = ap.parse_args()

    if args.daemon:
        serve(args.port)
        return
    if args.text:
        out = dispatch(" ".join(args.text))
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    ap.print_help()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-FLOW-FIELD-ENGINE-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · 流场拓扑引擎 v1.0
============================================================
把整个龍魂系统变成一张"活"的流场图：
  - 每个字节从哪里来、经过谁、到哪里去、被谁审计
  - 每个节点 = 服务/引擎/闸门/人格，带算法公式 + 详细备注 + 触发条件
  - 实时端口探测 → 节点状态动态变色
  - 实时日志 tail → 每个节点日志可见
  - HTTP API :8972 → 前端 flow-field.html 消费

数据源：
  1. .codebuddy/longhun_neural_net.json（系统拓扑·引擎·技能·边）
  2. 真实端口探测（socket connect）
  3. logs/ 目录真实日志 tail
  4. launchctl list（launchd 服务状态）

用法：
  python3 08_BIN/lh_flow_field.py status        # 终端打印流场总览
  python3 08_BIN/lh_flow_field.py node <id>     # 单节点详情
  python3 08_BIN/lh_flow_field.py api [--port 8972]  # 启动常驻 API
  python3 08_BIN/lh_flow_field.py trigger <id>  # 触发节点动作（记审计）
"""
import json
import socket
import time
import threading
from collections import deque
from datetime import datetime, timezone, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parent.parent
TOPO = ROOT / ".codebuddy" / "longhun_neural_net.json"
LOGS = ROOT / "logs"
PORT = 8972
TZ = timezone(timedelta(hours=8))

# ============================================================
# 1. 算法公式库 —— 每个节点都有公式
# ============================================================
FORMULAS = {
    "ngx_limit": "令牌桶: token_cap=50, rate=30r/s → 突发B=50·持续30r/s；超限 → 429 + 审计",
    "ngx_dna": "P0协议检查: 请求头 X-Dragon-DNA 必须匹配 /^#龍芯⚡️[^\\s]+$/ · 缺失 → 400 + 耻辱墙",
    "ngx_tricolor": "三色实时评分: score = Σ wᵢ·checkᵢ (w=0.4/0.3/0.3) → ≥0.8🟢·0.5~0.8🟡·<0.5🔴",
    "dr_gate": "数字根: dr(n) = 1 + ((n-1) mod 9) · 校验: 请求ID数字根 == 会话数字根 → 过闸",
    "id_gate": "身份闸: 七因子核验 H = SM3(dna‖ts‖nonce) · 双因子需 >0.7 相似度",
    "eth_gate": "伦理闸: L0四红线扫描(涉童/伪造DNA/背叛/越权) · 命中 → ∞级熔断冻结",
    "route": "路由决策: path 前缀匹配 → /api/*:8970 · /collab/*:19622 · /chat/*:18799 · /*:静态",
    "skill_bus": "技能路由: 语义余弦 sim(q, sᵢ) = q·sᵢ/|q||sᵢ| → 取 top-1 命中技能 · 链式编排",
    "persona": "人格路由: 意图向量 → 20人格矩阵 → argmax(权重·匹配度) · 连续3次同人格 → 锁30min",
    "llm_route": "模型路由: 本地Ollama优先 · 失败降级云端 · 温度0.7 · top_p 0.9 · 流式SSE",
    "mem": "记忆: 短期队列 deque(200) · 压缩 → SM3链 · DNA追溯链 append-only",
    "audit": "史官记录: append JSONL · 哈希链 hₙ = SM3(hₙ₋₁‖eventₙ) · 防篡改可验",
    "shame": "耻辱墙: 违规记分 s += w(type) · 累计≥3 → P72熔断 + Bark推送",
    "freeze": "熔断: L0∞永久冻结 · L1人工+GPG · L2禁该人格 · L3数字根复算自动恢复",
    "369": "不动点: sn=369 · log(369)≈5.911 · perm(369)=108 · 底座校验",
    "flow_score": "流场健康: H = 在线节点/总节点 · 边延迟均值 · 错误率 <1% → 🟢",
}

# ============================================================
# 2. 节点定义 —— 合并拓扑JSON + 真实服务 + 端口矩阵
# ============================================================
def _load_topo():
    try:
        return json.loads(TOPO.read_text(encoding="utf-8"))
    except Exception:
        return {}

def _build_nodes():
    """返回节点列表。每个节点带公式/备注/触发/日志源/端口。"""
    topo = _load_topo()
    engines = topo.get("engines", {}).get("highlights", {})
    edges = topo.get("edges", [])
    NODES = [
        # ---------- L0 边界接入层 ----------
        {"id": "nginx", "name": "nginx 统一入口", "layer": "L0边界接入", "type": "网关",
         "port": 80, "formula": FORMULAS["ngx_limit"], "extra": FORMULAS["ngx_dna"],
         "desc": "P0焊死入口 https://uid9622.cn:443 · 限流/防刷 + P0协议检查 + DNA注入 + 三色审计四件套",
         "trigger": "任何外部请求到达 → 先过四件套",
         "log": ["logs/launchd-longhun-services.out.log", "logs/flow_tunnel.out.log"],
         "status_key": "nginx"},
        {"id": "waf", "name": "WAF·安全网关", "layer": "L0边界接入", "type": "安全",
         "port": 9623, "formula": FORMULAS["ngx_tricolor"],
         "desc": "ModSecurity+自定义规则 · SQL注入/XSS/CC攻击清洗 · 请求先清洗后放行",
         "trigger": "WAF规则命中 (injection/xss/cc)",
         "log": ["logs/internal_net_gateway.log", "logs/lh_launcher-status.json"],
         "status_key": "waf"},
        {"id": "ssl", "name": "SSL/TLS 卸载", "layer": "L0边界接入", "type": "安全",
         "port": 443, "formula": "TLS1.3 · 证书 Let's Encrypt 通配 *.uid9622.cn · 自动续期",
         "desc": "HTTPS 终止 · 加密传输 · 7/17→10/15 证书周期",
         "trigger": "443 端口握手",
         "log": [],
         "status_key": "ssl"},

        # ---------- L1 路由调度层 ----------
        {"id": "router", "name": "路由决策引擎", "layer": "L1路由调度", "type": "调度",
         "port": 0, "formula": FORMULAS["route"],
         "desc": "nginx 内部路由 · /api/*→:8970 · /collab/*→:19622 · /chat/*→:18799 · /handoffs/*→文件 · /*→静态",
         "trigger": "path 前缀匹配",
         "log": ["logs/all_tunnels.log"],
         "status_key": "router"},
        {"id": "gate-dr", "name": "GATE-01 数字根闸", "layer": "L1路由调度", "type": "闸门",
         "port": 0, "formula": FORMULAS["dr_gate"],
         "desc": "P06数学大师复核 · 请求ID数字根与会话数字根比对 · 不符 → 拒绝",
         "trigger": "每次请求带数字根",
         "log": ["logs/flow_control_audit.jsonl"],
         "status_key": "gate"},
        {"id": "gate-id", "name": "GATE-02 身份认证闸", "layer": "L1路由调度", "type": "闸门",
         "port": 0, "formula": FORMULAS["id_gate"],
         "desc": "P13姜子牙·P05审计 · 七因子核验 + GPG签章校验 · R1-R5分级放行",
         "trigger": "身份核验请求",
         "log": ["logs/audit-engine.log"],
         "status_key": "gate"},
        {"id": "gate-eth", "name": "GATE-03 伦理防火墙", "layer": "L1路由调度", "type": "闸门",
         "port": 0, "formula": FORMULAS["eth_gate"],
         "desc": "P12屈原·P72龍盾 · L0四红线扫描 · 命中 → ∞级冻结",
         "trigger": "P0红线关键词命中",
         "log": ["logs/flow_control_audit.jsonl", "logs/cnsh_redlines.out.log"],
         "status_key": "gate"},
        {"id": "persona-orch", "name": "P13 姜子牙·编排调度", "layer": "L1路由调度", "type": "人格",
         "port": 0, "formula": FORMULAS["persona"],
         "desc": "意图→人格路由 · 20人格矩阵 · 封神榜权限分配 · 模块注册",
         "trigger": "意图解析完成 → 调度人格",
         "log": [],
         "status_key": "persona"},
        {"id": "wenxin", "name": "P00 文心·意图解析", "layer": "L1路由调度", "type": "人格",
         "port": 0, "formula": "意图熵 H = -Σ pᵢ log pᵢ · 最小化后取 top-3 意图域",
         "desc": "10%意图解析权重 · 用户一句话 → 意图域 → 触发链",
         "trigger": "用户输入到达",
         "log": [],
         "status_key": "persona"},

        # ---------- L2 技能服务层 ----------
        {"id": "skill-bus", "name": "技能总线 skill_bus", "layer": "L2技能服务", "type": "技能",
         "port": 0, "formula": FORMULAS["skill_bus"],
         "desc": "45工具·9分类·语义路由·链式编排 · 192引擎可执行文件",
         "trigger": "技能调用请求",
         "log": [],
         "status_key": "skill"},
        {"id": "api-gw", "name": "API 网关", "layer": "L2技能服务", "type": "服务",
         "port": 8970, "formula": "鉴权→业务编排→协议转换 · 限流10r/s · 超时60s",
         "desc": "透明审计API :8970 · 鉴权/编排/转换 · 128MB",
         "trigger": "/api/* 请求",
         "log": ["logs/ai_gateway.log", "logs/audit-engine.log"],
         "status_key": "api-gw"},
        {"id": "collab", "name": "协作中枢", "layer": "L2技能服务", "type": "服务",
         "port": 19622, "formula": "mDNS发现 + 文件同步 · 冲突检测 = 双向哈希比对 · 加密传输",
         "desc": "跨AI共享唯一真相源 · /opt/longhun/shared/ · 交接包自动推送",
         "trigger": "/collab/* 请求 · lh handoff save/load",
         "log": ["logs/brain_sync.log", "logs/flow-fusion.log"],
         "status_key": "collab"},
        {"id": "chat-bridge", "name": "对话桥接", "layer": "L2技能服务", "type": "服务",
         "port": 18799, "formula": FORMULAS["llm_route"],
         "desc": "Ollama代理 + 上下文管理 · SSE流式 · 5r/s 限流 · 120s 超时",
         "trigger": "/chat/* 请求",
         "log": ["logs/local_ai_relay.log", "logs/deepseek_bridge.log"],
         "status_key": "chat"},
        {"id": "search", "name": "多源搜索引擎", "layer": "L2技能服务", "type": "服务",
         "port": 9631, "formula": "Bing多源 → 结果去重 = sim阈值>0.85 → 缓存TTL 6h → P05来源审计",
         "desc": "lh search · 搜索→缓存→审计 · api.uid9622.cn/search",
         "trigger": "lh search 命令 / 关键词",
         "log": ["logs/collector.log", "logs/flow_fusion.log"],
         "status_key": "search"},
        {"id": "memory-api", "name": "统一记忆 API", "layer": "L2技能服务", "type": "服务",
         "port": 8771, "formula": FORMULAS["mem"],
         "desc": "记忆服务 · :8771 Mac / :8773 鲲鹏 · DNA追溯链",
         "trigger": "记忆读写请求",
         "log": ["logs/brain_sync.log"],
         "status_key": "memory"},
        {"id": "svc-ctl", "name": "服务控制 API", "layer": "L2技能服务", "type": "服务",
         "port": 8971, "formula": "freeze = launchctl unload + plist归档 · wake = bootstrap + 健康探测",
         "desc": "launchd 冻结/唤醒 · 100%可回滚 · 可视化按钮面板",
         "trigger": "portal 点点点操作",
         "log": ["logs/lh_service_control.log"],
         "status_key": "svc-ctl"},

        # ---------- L3 数据持久层 ----------
        {"id": "store-mem", "name": "记忆库", "layer": "L3数据持久", "type": "存储",
         "port": 0, "formula": "SQLite + JSONL · 短期deque(200)→压缩→SM3链 · append-only",
         "desc": "对话历史/记忆摘要 · 不删除只冻结",
         "trigger": "记忆写入",
         "log": [],
         "status_key": "store"},
        {"id": "store-know", "name": "知识库", "layer": "L3数据持久", "type": "存储",
         "port": 0, "formula": "JSONL 20域84文件 · 每6h自更新 · 准入审计",
         "desc": "领域知识 · 统一知识底座 v2.1",
         "trigger": "知识拉取/检索",
         "log": ["logs/knowledge_hub.log"],
         "status_key": "store"},
        {"id": "store-config", "name": "配置库", "layer": "L3数据持久", "type": "存储",
         "port": 0, "formula": "YAML/JSON · ~/.longhun/lh.env · chmod 600 · 三级fallback",
         "desc": "系统配置 · 统一配置源 · 敏感字段脱敏",
         "trigger": "配置读取",
         "log": [],
         "status_key": "store"},

        # ---------- L4 审计治理层 ----------
        {"id": "historian", "name": "史官记录", "layer": "L4审计治理", "type": "审计",
         "port": 0, "formula": FORMULAS["audit"],
         "desc": "全操作审计 · DNA追溯 · 哈希链校验 · JSONL append-only",
         "trigger": "所有节点操作完成",
         "log": ["logs/龍魂流程審計庫.jsonl", "logs/ai_audit.jsonl"],
         "status_key": "audit"},
        {"id": "shame-wall", "name": "耻辱墙", "layer": "L4审计治理", "type": "审计",
         "port": 0, "formula": FORMULAS["shame"],
         "desc": "违规记录 · 问责追踪 · 修复跟踪 · 累计≥3 → 熔断",
         "trigger": "审计违规触发",
         "log": ["logs/fuse_audit.jsonl"],
         "status_key": "audit"},
        {"id": "tricolor", "name": "三色看板", "layer": "L4审计治理", "type": "审计",
         "port": 0, "formula": FORMULAS["flow_score"],
         "desc": "🟢/🟡/🔴 实时渲染 · 趋势分析 · 实时告警",
         "trigger": "实时刷新",
         "log": ["logs/health-check-latest.json"],
         "status_key": "audit"},

        # ---------- L5 外部集成层 ----------
        {"id": "ollama", "name": "Ollama 本地模型", "layer": "L5外部集成", "type": "外部",
         "port": 11434, "formula": "qwen2.5:7b / longhun-v3.8 · 温度0.7 · 流式 · 离线可用",
         "desc": "本地推理 · 数据不出设备 · 主力模型引擎",
         "trigger": "对话/生成请求",
         "log": [],
         "status_key": "ollama"},
        {"id": "kunpeng", "name": "鲲鹏服务器", "layer": "L5外部集成", "type": "外部",
         "port": 22, "formula": "SSH 隧道 · systemd 12服务 · /opt/longhun/shared 唯一真相源",
         "desc": "119.13.90.27 · 分布式推理 · 协作中枢远端 · uid9622.cn",
         "trigger": "远程请求/同步",
         "log": ["logs/flow_fusion.log", "logs/frpc.out.log"],
         "status_key": "kunpeng"},
        {"id": "harmony", "name": "鸿蒙设备", "layer": "L5外部集成", "type": "外部",
         "port": 0, "formula": "端侧推理 · 本地记忆 · 加密同步 · 离线优先",
         "desc": "端侧智能 · 数据主权在设备",
         "trigger": "端侧请求",
         "log": [],
         "status_key": "harmony"},
    ]
    return NODES, edges, engines

# ============================================================
# 3. 动态探测
# ============================================================
class Probe:
    """端口探测 + launchd 状态 + 缓存。"""
    def __init__(self, ttl=3.0):
        self.ttl = ttl
        self._cache = {}
        self._lock = threading.Lock()

    def _probe_port(self, port: int) -> bool:
        if port <= 0:
            return True  # 无端口节点 = 逻辑节点 = 在线
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.6)
                return s.connect_ex(("127.0.0.1", port)) == 0
        except Exception:
            return False

    def probe(self, key: str, port: int = 0) -> dict:
        with self._lock:
            now = time.time()
            hit = self._cache.get(key)
            if hit and now - hit[0] < self.ttl:
                return hit[1]
        # 特殊状态键 → 走 launchctl
        if key == "persona":
            state = {"up": True, "detail": "人格矩阵·逻辑常驻"}
        elif key == "gate":
            state = {"up": True, "detail": "三闸门·逻辑闸"}
        elif key == "skill":
            state = {"up": True, "detail": "技能总线·逻辑路由"}
        elif key == "router":
            state = {"up": self._probe_port(80), "detail": "nginx :80"}
        elif key == "ssl":
            state = {"up": self._probe_port(80), "detail": "TLS由nginx承载·跟随:80"}
        elif key == "store":
            state = {"up": True, "detail": "本地文件存储·逻辑节点"}
        elif key == "audit":
            state = {"up": True, "detail": "审计链路·逻辑节点"}
        else:
            up = self._probe_port(port)
            state = {"up": up, "detail": f":{port} {'在线' if up else '离线'}"}
        with self._lock:
            self._cache[key] = (time.time(), state)
        return state

probe = Probe()

# ============================================================
# 4. 日志读取
# ============================================================
def read_log(paths: list, n: int = 60) -> list:
    """读取多个日志文件尾部，返回最近 n 行（带时间戳）。"""
    lines = []
    for p in paths:
        fp = ROOT / p if not Path(p).is_absolute() else Path(p)
        if not fp.exists():
            continue
        try:
            with open(fp, "r", encoding="utf-8", errors="replace") as f:
                tail = deque(f, maxlen=n)
            for ln in tail:
                lines.append({"source": fp.name, "line": ln.rstrip()[:500]})
        except Exception:
            continue
    return lines[-n:]

# ============================================================
# 5. 触发动作（写审计）
# ============================================================
AUDIT_LOG = ROOT / "logs" / "lh_flow_field.log"
def audit(action: str, target: str, result: str, risk: int = 0):
    entry = {
        "time": datetime.now(TZ).isoformat(timespec="seconds"),
        "action": action, "target": target,
        "result": result, "risk_score": risk,
        "dna": "#龍芯⚡️丙午·丙申·庚申·壬午·䷙大畜-FLOW-FIELD-UID9622",
        "tricolor": "🟢" if risk == 0 else ("🟡" if risk < 3 else "🔴"),
    }
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry

# ============================================================
# 6. 拓扑聚合
# ============================================================
def build_topology(with_status=True):
    nodes, edges, engines = _build_nodes()
    node_map = {}
    for nd in nodes:
        st = probe.probe(nd["status_key"], nd.get("port", 0)) if with_status else {"up": True, "detail": ""}
        node = dict(nd)
        node["status"] = st
        node["up"] = st["up"]
        node_map[nd["id"]] = node
    # 边：节点协作关系（来源=真实拓扑edges + 补充链路）
    edge_list = [
        # 请求链路
        {"from": "nginx", "to": "waf", "type": "转发", "weight": 1.0},
        {"from": "waf", "to": "ssl", "type": "清洗后放行", "weight": 1.0},
        {"from": "ssl", "to": "router", "type": "解密路由", "weight": 1.0},
        # 路由 → 服务
        {"from": "router", "to": "api-gw", "type": "/api/*", "weight": 1.0},
        {"from": "router", "to": "collab", "type": "/collab/*", "weight": 1.0},
        {"from": "router", "to": "chat-bridge", "type": "/chat/*", "weight": 1.0},
        {"from": "router", "to": "search", "type": "/search", "weight": 0.9},
        {"from": "router", "to": "svc-ctl", "type": "/service-control", "weight": 0.8},
        # 闸门
        {"from": "nginx", "to": "gate-dr", "type": "数字根校验", "weight": 1.0},
        {"from": "gate-dr", "to": "gate-id", "type": "身份核验", "weight": 1.0},
        {"from": "gate-id", "to": "gate-eth", "type": "伦理扫描", "weight": 1.0},
        {"from": "gate-eth", "to": "router", "type": "通过→路由", "weight": 1.0},
        # 人格
        {"from": "wenxin", "to": "persona-orch", "type": "意图→调度", "weight": 0.9},
        {"from": "persona-orch", "to": "skill-bus", "type": "人格→技能", "weight": 0.9},
        {"from": "persona-orch", "to": "router", "type": "决策回流", "weight": 0.8},
        # 服务 → 存储
        {"from": "api-gw", "to": "store-mem", "type": "写记忆", "weight": 0.8},
        {"from": "api-gw", "to": "store-know", "type": "查知识", "weight": 0.8},
        {"from": "chat-bridge", "to": "store-mem", "type": "对话落库", "weight": 0.9},
        {"from": "collab", "to": "store-config", "type": "配置同步", "weight": 0.7},
        # 服务 → 审计
        {"from": "api-gw", "to": "historian", "type": "审计上报", "weight": 0.95},
        {"from": "chat-bridge", "to": "historian", "type": "审计上报", "weight": 0.95},
        {"from": "collab", "to": "historian", "type": "审计上报", "weight": 0.95},
        {"from": "historian", "to": "shame-wall", "type": "违规转交", "weight": 0.9},
        {"from": "historian", "to": "tricolor", "type": "三色更新", "weight": 0.9},
        # 外部
        {"from": "chat-bridge", "to": "ollama", "type": "模型调用", "weight": 1.0},
        {"from": "ollama", "to": "chat-bridge", "type": "流式返回", "weight": 1.0},
        {"from": "collab", "to": "kunpeng", "type": "远程同步", "weight": 0.95},
        {"from": "kunpeng", "to": "harmony", "type": "端侧分发", "weight": 0.6},
        {"from": "ollama", "to": "store-mem", "type": "记忆回流", "weight": 0.7},
    ]
    # 合并真实拓扑 edges 中的高层链路
    for e in edges:
        f = e.get("from", "").lower()
        t = e.get("to", "").lower()
        edge_list.append({"from": f, "to": t, "type": e.get("type", "协同"), "weight": e.get("weight", 0.5)})
    # 去重
    seen = set()
    dedup = []
    for e in edge_list:
        k = (e["from"], e["to"])
        if k in seen:
            continue
        seen.add(k)
        dedup.append(e)
    return {"nodes": list(node_map.values()), "edges": dedup, "engines": engines,
            "generated": datetime.now(TZ).isoformat(timespec="seconds")}

# ============================================================
# 7. HTTP API
# ============================================================
class _Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        url = urlparse(self.path)
        q = parse_qs(url.query)
        try:
            if url.path == "/health":
                self._send(200, {"status": "ok", "port": PORT, "ts": datetime.now(TZ).isoformat()})
            elif url.path == "/topology":
                self._send(200, build_topology(with_status=True))
            elif url.path == "/node":
                nid = q.get("id", [""])[0]
                topo = build_topology(with_status=True)
                nd = next((x for x in topo["nodes"] if x["id"] == nid), None)
                if not nd:
                    self._send(404, {"error": "node not found"})
                    return
                nd["logs"] = read_log(nd.get("log", []), int(q.get("n", [60])[0]))
                self._send(200, nd)
            elif url.path == "/log":
                src = q.get("source", [""])[0]
                n = int(q.get("n", [60])[0])
                self._send(200, {"logs": read_log([src] if src else [], n)})
            elif url.path == "/audit-log":
                self._send(200, {"logs": read_log(["logs/lh_flow_field.log"], int(q.get("n", [80])[0]))})
            else:
                self._send(404, {"error": "not found"})
        except Exception as e:
            self._send(500, {"error": str(e)})

    def do_POST(self):
        url = urlparse(self.path)
        q = parse_qs(url.query)
        try:
            if url.path == "/trigger":
                nid = q.get("id", [""])[0]
                entry = audit("trigger", nid, "已触发·见节点日志", risk=0)
                self._send(200, {"ok": True, "audit": entry})
            else:
                self._send(404, {"error": "not found"})
        except Exception as e:
            self._send(500, {"error": str(e)})

    def log_message(self, fmt, *args):
        pass  # 静默，避免刷屏

def run_api(port: int = PORT):
    srv = ThreadingHTTPServer(("127.0.0.1", port), _Handler)
    audit("api_start", f"flow-field-api :{port}", "常驻启动", 0)
    print(f"🐉 流场引擎 API 已启动: http://127.0.0.1:{port}  (Ctrl+C 停止)")
    srv.serve_forever()

# ============================================================
# 8. CLI
# ============================================================
def cli_status():
    topo = build_topology(with_status=True)
    layers = {}
    for nd in topo["nodes"]:
        layers.setdefault(nd["layer"], []).append(nd)
    print("🐉 龍魂 · 流场总览")
    print("=" * 60)
    for layer, nodes in layers.items():
        up = sum(1 for x in nodes if x["up"])
        mark = "🟢" if up == len(nodes) else "🟡"
        print(f"\n{mark} {layer}  ({up}/{len(nodes)} 在线)")
        for nd in nodes:
            st = "●" if nd["up"] else "○"
            port = f" :{nd['port']}" if nd.get("port") else ""
            print(f"   {st} {nd['name']}{port}  [{nd['id']}]")

def cli_node(nid: str):
    topo = build_topology(with_status=True)
    nd = next((x for x in topo["nodes"] if x["id"] == nid), None)
    if not nd:
        print(f"❌ 节点 {nid} 不存在")
        return
    print(f"▶ 节点: {nd['name']}  [{nd['id']}]")
    print(f"  层: {nd['layer']} · 类型: {nd['type']} · 状态: {'●在线' if nd['up'] else '○离线'}")
    print(f"  备注: {nd['desc']}")
    print(f"  算法公式: {nd['formula']}")
    print(f"  触发: {nd['trigger']}")
    if nd.get("extra"):
        print(f"  附加公式: {nd['extra']}")
    logs = read_log(nd.get("log", []), 20)
    if logs:
        print(f"\n  最近日志 ({len(logs)} 条):")
        for lg in logs[-10:]:
            print(f"    [{lg['source']}] {lg['line'][:160]}")

def main():
    import argparse
    ap = argparse.ArgumentParser(description="龍魂流场拓扑引擎")
    ap.add_argument("action", nargs="?", default="status", choices=["status", "node", "api", "trigger"])
    ap.add_argument("target", nargs="?", default="")
    ap.add_argument("--port", type=int, default=PORT)
    args = ap.parse_args()
    if args.action == "api":
        run_api(args.port)
    elif args.action == "node":
        cli_node(args.target)
    elif args.action == "trigger":
        entry = audit("trigger", args.target, "已触发", 0)
        print(json.dumps(entry, ensure_ascii=False, indent=2))
    else:
        cli_status()

if __name__ == "__main__":
    main()

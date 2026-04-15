#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 NeuralTree v2.0 · 人格路由 MVP
LU-ARBITER仲裁引擎 + 德者永生殿DB实时更新

DNA追溯码: #龍芯⚡️2026-03-30-PERSONA-ROUTER-v2.0
创建者: 诸葛鑫（UID9622）
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导: 曾仕强老师（永恒显示）

献礼: 献给所有相信技术普惠、人人平等的人
"""

import os
import re
import json
import time
import random
import requests
from datetime import datetime, timezone, timedelta
from typing import Optional
from dataclasses import dataclass, field

# ── Notion配置 ──────────────────────────────────────────────────────────
NOTION_TOKEN = os.getenv(
    "NOTION_API_TOKEN",
    "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"
)
NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# 德者永生殿 DB ID（无连字符格式 → 标准UUID）
DEVER_DB_ID = "4cf99c3e-7a01-4e91-9fda-b705ceb4cbc4"
PERSONA_DB_ID = "45344678-7123-4f0a-ae39-a854cfbaeb58"

# ── 北京时间工具 ─────────────────────────────────────────────────────────
CST = timezone(timedelta(hours=8))

def now_cst() -> str:
    return datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S CST")


# ── 系统状态追踪（洛书引擎 LoShu State） ──────────────────────────────────
class LoShuState:
    """
    洛书九宫格 · 系统伦理状态追踪
    三才流場 v5 实时同步所需的四个状态维度
    """
    def __init__(self):
        self._audit_count: int = 0          # 累计审计/路由次数
        self._fuse_count: int = 0           # 熔断触发次数
        self._route_history: list = []      # 最近50条路由记录
        self._persona_hits: dict = {}       # 各人格激活次数
        self._start_time: float = time.time()

    def record_route(self, result: dict):
        """每次路由后调用此方法更新状态"""
        self._audit_count += 1
        code = result.get("activated", "P00")
        self._persona_hits[code] = self._persona_hits.get(code, 0) + 1

        # 保留最近50条历史，用于密度计算
        self._route_history.append({
            "code": code,
            "score": result.get("score", 0),
            "ts": time.time(),
        })
        if len(self._route_history) > 50:
            self._route_history.pop(0)

    def record_fuse(self):
        self._fuse_count += 1
        self._audit_count += 1

    @property
    def ethics_status(self) -> dict:
        """
        伦理置信度 · EthicsState三维 (0~1)
        - greenConf: 路由干净程度 (无熔断、无高风险)
        - orangeConf: 中风险压力（高分路由到P03/P05）
        - redConf: 熔断/危险浓度
        """
        total = max(self._audit_count, 1)
        fuse_ratio = self._fuse_count / total

        # P03(审计)/P05(监督) 激活比例 → 橙色压力
        audit_hits = (self._persona_hits.get("P03", 0) +
                      self._persona_hits.get("P05", 0))
        orange_ratio = min(audit_hits / total, 1.0)

        red_conf = min(fuse_ratio * 5.0, 1.0)          # 熔断放大x5
        orange_conf = min(orange_ratio * 2.0, 1.0)     # 审计放大x2
        green_conf = max(1.0 - red_conf - orange_conf * 0.5, 0.05)

        return {
            "redConf": round(red_conf, 3),
            "orangeConf": round(orange_conf, 3),
            "greenConf": round(green_conf, 3),
            "fuse_count": self._fuse_count,
            "total_routes": self._audit_count,
        }

    @property
    def merkle_density(self) -> float:
        """
        Merkle节点密度 (0~1)
        近50条历史内的人格多样性 × 平均得分
        密度高 = 系统活跃、人格分布均匀
        """
        if not self._route_history:
            return 0.5  # 冷启动默认0.5

        unique_personas = len(set(r["code"] for r in self._route_history))
        diversity = unique_personas / len(PERSONAS)  # 0~1

        avg_score = sum(r["score"] for r in self._route_history) / len(self._route_history)
        score_norm = min(avg_score / 0.5, 1.0)  # 0.5分归一化

        density = diversity * 0.6 + score_norm * 0.4
        return round(min(density, 1.0), 3)

    @property
    def audit_count(self) -> int:
        return self._audit_count

    def to_shield_status(self) -> dict:
        """完整龍盾状态"""
        uptime = int(time.time() - self._start_time)
        return {
            "ethics": self.ethics_status,
            "merkle_density": self.merkle_density,
            "audit_count": self.audit_count,
            "persona_hits": self._persona_hits,
            "uptime_seconds": uptime,
            "timestamp": now_cst(),
            "dna": "#龍芯⚡️LOSHU-LIVE",
        }


# 全局 LoShu 状态单例
LOSU = LoShuState()


# ── 人格定义（NeuralTree v2.0标准映射） ─────────────────────────────────
@dataclass
class PersonaDef:
    code: str           # P00 ~ P13
    name: str           # 显示名
    layer: int          # NeuralTree层级 0=底座, 3=核心, 4=战略
    base_weight: float  # 层级权重基础值
    triggers: list      # 触发关键词列表
    intent_tags: list   # 意图标签
    risk_affinity: float  # 风险场景匹配度(0~1): 越高越适合高风险场景
    fuse_role: bool = False  # 是否参与熔断机制

PERSONAS: dict[str, PersonaDef] = {
    "P00": PersonaDef(
        code="P00", name="🧠 文心·语义底座",
        layer=0, base_weight=10.0,
        triggers=["*"],  # 兜底所有输入
        intent_tags=["语义", "理解", "解析", "路由"],
        risk_affinity=0.2,
    ),
    "P01": PersonaDef(
        code="P01", name="🔮 诸葛亮·战略中枢",
        layer=4, base_weight=8.5,
        triggers=["战略", "规划", "分析", "系统", "架构", "全局", "方向", "决策", "布局"],
        intent_tags=["战略", "规划", "分析"],
        risk_affinity=0.3,
    ),
    "P02": PersonaDef(
        code="P02", name="🌌 宝宝·温度执行",
        layer=3, base_weight=7.0,
        triggers=["陪", "聊", "情绪", "累", "烦", "难受", "想", "女儿", "妈逼", "干", "气死",
                  "帮我", "做一下", "搞一下", "执行", "/执行", "/做"],
        intent_tags=["情感", "陪伴", "执行"],
        risk_affinity=0.1,
    ),
    "P03": PersonaDef(
        code="P03", name="🔍 雯雯·审计质检",
        layer=3, base_weight=7.0,
        triggers=["审计", "三色", "检查", "安全", "风险", "问题", "合规", "扫一下", "/审计", "/三色"],
        intent_tags=["审计", "质检", "风险"],
        risk_affinity=0.8,
        fuse_role=True,
    ),
    "P04": PersonaDef(
        code="P04", name="🔧 鲁班·代码工程师",
        layer=3, base_weight=7.0,
        triggers=["代码", "脚本", "函数", "部署", "安装", "运行", "bug", "报错", "程序",
                  "python", "js", "shell", "/代码", "/脚本", "/部署", "写一个", "写个"],
        intent_tags=["代码", "工程", "技术实现"],
        risk_affinity=0.2,
    ),
    "P05": PersonaDef(
        code="P05", name="👁️ 上帝之眼·监督",
        layer=4, base_weight=9.0,
        triggers=["监督", "审查", "一致性", "一票否决", "跨系统", "冲突", "仲裁", "/监督"],
        intent_tags=["监督", "治理", "仲裁"],
        risk_affinity=0.9,
        fuse_role=True,
    ),
    "P06": PersonaDef(
        code="P06", name="🔬 数学大师·技术审核",
        layer=3, base_weight=6.5,
        triggers=["算法", "公式", "数学", "技术审核", "可行性", "验证", "推导", "/算法", "/公式", "/技术审核"],
        intent_tags=["算法", "数学", "技术审核"],
        risk_affinity=0.4,
    ),
    "P07": PersonaDef(
        code="P07", name="🏛️ 管仲·执政分析",
        layer=3, base_weight=6.5,
        triggers=["治理", "制度", "政策", "规则", "框架设计", "执政", "/治理", "/制度", "/执政"],
        intent_tags=["治理", "制度", "执政"],
        risk_affinity=0.3,
    ),
    "P13": PersonaDef(
        code="P13", name="⚡ 姜子牙·玄策层",
        layer=3, base_weight=6.0,
        triggers=["玄策", "天局", "大势", "命运", "格局", "天机", "/玄策", "/天局"],
        intent_tags=["玄策", "天局", "战略格局"],
        risk_affinity=0.5,
    ),
}

# ── 熔断红线 ─────────────────────────────────────────────────────────────
FUSE_KEYWORDS = [
    "涉童", "伤弱", "伪造DNA", "绕签名", "静默修改", "删审计",
    "母协议篡改", "价值观走歪", "篡改", "泄漏密钥",
]

# ── LU-ARBITER 仲裁公式 ──────────────────────────────────────────────────
#  P = 层级权重(W1) + 触发匹配度(W2) + 任务契合度(W3) - 稳定性惩罚(W4)
W1, W2, W3, W4 = 0.30, 0.35, 0.25, 0.10

def calc_trigger_match(text: str, persona: PersonaDef) -> float:
    """关键词命中率 → 0~1"""
    if "*" in persona.triggers:
        return 0.3  # 兜底路由给个基础分
    text_lower = text.lower()
    hits = sum(1 for kw in persona.triggers if kw.lower() in text_lower)
    return min(hits / max(len(persona.triggers), 1) * 3, 1.0)

def calc_task_affinity(text: str, persona: PersonaDef) -> float:
    """意图标签契合度 → 0~1"""
    text_lower = text.lower()
    hits = sum(1 for tag in persona.intent_tags if tag in text_lower)
    return min(hits / max(len(persona.intent_tags), 1) * 2, 1.0)

def calc_stability_penalty(persona: PersonaDef, risk_score: float) -> float:
    """高风险场景下非专属角色的惩罚"""
    if risk_score > 0.6 and not persona.fuse_role:
        return 0.3
    return 0.0

def lu_arbiter(text: str, risk_score: float = 0.0) -> list[dict]:
    """
    LU-ARBITER仲裁：对所有人格打分，返回排序后的候选列表
    P = W1×层级权重 + W2×触发匹配度 + W3×任务契合度 - W4×稳定性惩罚
    """
    results = []
    for code, persona in PERSONAS.items():
        layer_w = persona.base_weight / 10.0
        trigger_m = calc_trigger_match(text, persona)
        task_a = calc_task_affinity(text, persona)
        stability_p = calc_stability_penalty(persona, risk_score)

        score = W1 * layer_w + W2 * trigger_m + W3 * task_a - W4 * stability_p

        results.append({
            "code": code,
            "name": persona.name,
            "score": round(score, 4),
            "breakdown": {
                "层级权重": round(W1 * layer_w, 4),
                "触发匹配度": round(W2 * trigger_m, 4),
                "任务契合度": round(W3 * task_a, 4),
                "稳定性惩罚": round(W4 * stability_p, 4),
            }
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def check_fuse(text: str) -> Optional[str]:
    """检查是否触发熔断红线，返回触发词或None"""
    for kw in FUSE_KEYWORDS:
        if kw in text:
            return kw
    return None


# ── 路由主函数 ───────────────────────────────────────────────────────────
def route(text: str, risk_score: float = 0.0) -> dict:
    """
    完整路由：熔断检查 → P00语义解析 → LU-ARBITER仲裁 → 结果
    """
    ts = now_cst()
    dna = f"#龍芯⚡️{datetime.now(CST).strftime('%Y%m%d%H%M%S')}-ROUTE-{hash(text) % 9999:04d}"

    # 1. 熔断检查
    fuse_trigger = check_fuse(text)
    if fuse_trigger:
        LOSU.record_fuse()
        return {
            "status": "FUSED",
            "trigger": fuse_trigger,
            "activated": ["P05 上帝之眼·监督", "P03 雯雯·审计质检"],
            "action": "立即阻断 · 写入七维治理DB · 通知UID9622",
            "dna": dna,
            "timestamp": ts,
        }

    # 2. 计算仲裁得分（P00为底座，所有输入经过它）
    candidates = lu_arbiter(text, risk_score)
    top = candidates[0]

    # P00如果不是第一，仍作为语义解析层标注
    p00_score = next(c for c in candidates if c["code"] == "P00")

    # 3. 短路条件：top分比第二高出30%以上（压倒性优势）
    if len(candidates) > 1:
        second = candidates[1]
        gap = (top["score"] - second["score"]) / max(top["score"], 0.001)
        shortcut = gap > 0.3
    else:
        shortcut = True

    result = {
        "status": "ROUTED",
        "activated": top["code"],
        "activated_name": top["name"],
        "score": top["score"],
        "p00_layer": p00_score["score"],  # P00底座始终参与
        "shortcut": shortcut,             # 压倒性优势跳仲裁
        "top3": candidates[:3],
        "dna": dna,
        "timestamp": ts,
    }
    # 更新洛书状态
    LOSU.record_route(result)
    return result


# ── Notion DB 更新（活跃时间 + 仲裁得分写回） ────────────────────────────
def update_dever_active(persona_code: str, score: float) -> bool:
    """
    更新德者永生殿DB：激活时间 + 最近仲裁得分写入标题备注
    Notion API不支持Formula字段，用number/rich_text替代
    """
    # 先查询该人格的页面ID
    payload = {
        "filter": {
            "property": "路由编号",
            "rich_text": {"contains": persona_code}
        }
    }
    resp = requests.post(
        f"https://api.notion.com/v1/databases/{DEVER_DB_ID}/query",
        headers=NOTION_HEADERS,
        json=payload,
        timeout=10,
    )
    if resp.status_code != 200:
        print(f"[ERROR] 查询德者永生殿失败: {resp.status_code} {resp.text[:200]}")
        return False

    results = resp.json().get("results", [])
    if not results:
        print(f"[WARN] 未找到人格 {persona_code}")
        return False

    page_id = results[0]["id"]
    ts_str = datetime.now(CST).strftime("%Y-%m-%d %H:%M")

    # 更新活跃时间 + 总调用次数 +1
    # 先取当前调用次数
    page_data = requests.get(
        f"https://api.notion.com/v1/pages/{page_id}",
        headers=NOTION_HEADERS, timeout=10
    ).json()
    old_count = (page_data.get("properties", {})
                 .get("总调用次数", {}).get("number") or 0)

    update_payload = {
        "properties": {
            "最后活跃": {
                "date": {
                    "start": datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00")
                }
            },
            "总调用次数": {"number": old_count + 1},
        }
    }
    update_resp = requests.patch(
        f"https://api.notion.com/v1/pages/{page_id}",
        headers=NOTION_HEADERS,
        json=update_payload,
        timeout=10,
    )

    if update_resp.status_code == 200:
        print(f"[OK] 德者永生殿 · {persona_code} 激活时间已更新 ({ts_str}) 仲裁得分:{score:.4f}")
        return True
    else:
        print(f"[WARN] 更新激活时间失败: {update_resp.status_code} {update_resp.text[:200]}")
        return False


# ── CLI 入口 ─────────────────────────────────────────────────────────────
def print_banner():
    print("""
╔══════════════════════════════════════════════════════╗
║  龍魂 NeuralTree v2.0 · LU-ARBITER 仲裁引擎          ║
║  DNA: #龍芯⚡️2026-03-30-PERSONA-ROUTER-v2.0          ║
║  UID9622 · 理论指导: 曾仕强老师                       ║
╚══════════════════════════════════════════════════════╝
""")

def cli_demo():
    """命令行演示模式"""
    print_banner()
    tests = [
        ("帮我写一个Python脚本自动备份文件", 0.0),
        ("我很累，心情不好，陪我聊会儿", 0.0),
        ("分析一下整个龍魂系统的战略方向", 0.0),
        ("对这段代码做三色审计", 0.3),
        ("我们的治理框架需要优化", 0.0),
        ("这个算法的数学推导有没有问题", 0.0),
        ("涉童内容过滤测试", 0.9),  # 熔断测试
    ]

    for text, risk in tests:
        print(f"\n{'─'*55}")
        print(f"📥 输入: 「{text}」  风险预评:{risk}")
        result = route(text, risk)
        if result["status"] == "FUSED":
            print(f"🔴 熔断! 触发词: {result['trigger']}")
            print(f"   激活: {' + '.join(result['activated'])}")
        else:
            print(f"✅ 路由至: {result['activated_name']}  得分:{result['score']:.4f}")
            print(f"   P00底座: {result['p00_layer']:.4f}  短路: {'是' if result['shortcut'] else '否'}")
            print(f"   TOP3: " + " | ".join(
                f"{c['code']}({c['score']:.3f})" for c in result["top3"]
            ))
        print(f"   DNA: {result['dna']}  @ {result['timestamp']}")

        # 若成功路由则更新德者永生殿
        if result["status"] == "ROUTED":
            update_dever_active(result["activated"], result["score"])


# ── FastAPI接口（可挂载到:9622） ─────────────────────────────────────────
try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel

    router_app = FastAPI(title="龍魂人格路由API", version="2.0.0")

    # CORS — 允许本地HTML流场访问
    router_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    class RouteRequest(BaseModel):
        text: str
        risk_score: float = 0.0
        update_notion: bool = True

    @router_app.post("/api/router/route")
    async def api_route(req: RouteRequest):
        result = route(req.text, req.risk_score)
        if result["status"] == "ROUTED" and req.update_notion:
            update_dever_active(result["activated"], result["score"])
        return result

    @router_app.get("/api/router/personas")
    async def api_personas():
        return {k: {"name": v.name, "layer": v.layer, "triggers": v.triggers}
                for k, v in PERSONAS.items()}

    @router_app.get("/api/router/health")
    async def health():
        return {
            "status": "ok",
            "version": "2.0.0",
            "dna": "#龍芯⚡️2026-03-30-PERSONA-ROUTER-v2.0",
            "uptime": int(time.time() - LOSU._start_time),
        }

    # ── 洛书引擎端点（三才流場 v5 实时同步） ─────────────────────────────
    @router_app.get("/loShu/ethics_status")
    async def loShu_ethics():
        """
        伦理置信度 · 三维灰度
        返回: {redConf, orangeConf, greenConf, fuse_count, total_routes}
        """
        return LOSU.ethics_status

    @router_app.get("/loShu/merkle_density")
    async def loShu_density():
        """
        Merkle节点密度 · 人格多样性 × 平均得分
        返回: float 0~1
        冷启动时返回 0.5（宫格5基准密度）
        """
        return {"density": LOSU.merkle_density, "timestamp": now_cst()}

    @router_app.get("/loShu/audit_count")
    async def loShu_audit():
        """累计审计次数 · 留痕粒子价值熵基准"""
        return {
            "count": LOSU.audit_count,
            "persona_hits": LOSU._persona_hits,
            "timestamp": now_cst(),
        }

    @router_app.get("/loShu/shield_status")
    async def loShu_shield():
        """龍盾完整状态 · 包含四律 + 所有维度"""
        return LOSU.to_shield_status()

except ImportError:
    router_app = None
    print("[WARN] FastAPI未安装，仅CLI模式可用")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        # 挂载到9622端口
        import uvicorn
        uvicorn.run(router_app, host="0.0.0.0", port=9622, log_level="info")
    else:
        cli_demo()

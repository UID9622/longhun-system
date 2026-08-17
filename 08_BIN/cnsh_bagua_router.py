#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·丙寅·午时·䷐随-CNSH-BAGUA-ROUTER-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 CNSH IDE · 八卦/八门 AI 路由决策器 v1.0

把异群架构（多厂商 AI）与龍魂八卦/奇门八门接起来：
  - 根据用户意图判八门
  - 根据当前卦象态势选厂商
  - 死门/惊门直接熔断，不开 AI

用法:
  from cnsh_bagua_router import BaguaRouter, classify_bamen
  router = BaguaRouter(ai_router)
  decision = router.decide("把 CNSH 编译成 Python")
  # decision.gate = "生门", decision.provider = "kimi" / "local" ...
"""

import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# 让导入能找到同目录模块
sys.path.insert(0, str(Path(__file__).resolve().parent))

# 尝试接入龍魂八卦调度器（不强制）
try:
    import lh_bagua
    HAS_LH_BAGUA = True
except Exception:
    HAS_LH_BAGUA = False


# ═══════════════════════════════════════════════════════
# 八门定义
# ═══════════════════════════════════════════════════════

@dataclass
class Gate:
    name: str
    emoji: str
    color: str  # 🔴 🟡 🟢
    desc: str
    action: str


GATES: Dict[str, Gate] = {
    "开门": Gate("开门", "🟢", "🟢", "通达、开始、正常通行", "使用默认厂商正常处理"),
    "休门": Gate("休门", "🟢", "🟢", "休养、观察、低功耗", "优先本地模型/低成本厂商"),
    "生门": Gate("生门", "🟢", "🟢", "生长、学习、创作、理解", "优先长文本/创造型厂商"),
    "伤门": Gate("伤门", "🟡", "🟡", "冲突、质疑、调试、纠错", "优先推理型厂商"),
    "杜门": Gate("杜门", "🟡", "🟡", "阻塞、隐私、绕过、隐藏", "优先本地模型，数据不出本机"),
    "景门": Gate("景门", "🟡", "🟡", "展示、公开、审计、报告", "优先长上下文厂商，留痕输出"),
    "死门": Gate("死门", "🔴", "🔴", "终止、删除、危险、结束", "熔断：不调用 AI，返回警示"),
    "惊门": Gate("惊门", "🔴", "🔴", "告警、违法、安全、威胁", "熔断：要求人工确认并固定证据"),
}


# 八门关键词分类器（按优先级匹配）
# 注意：中文不使用 \b 词边界，直接子串匹配；英文保留 \b
GATE_PATTERNS: List[Tuple[str, str]] = [
    # 死门/惊门：最高优先级，直接熔断
    ("死门", r"(删除|销毁|终止|结束生命|自残|自杀|杀人|投毒|制造炸弹|黑客攻击|入侵系统|窃取数据|诈骗|勒索|暴力|色情|儿童|毒品)"),
    ("惊门", r"(告警|报警|违法|犯罪|威胁|恐吓|诽谤|侵权|泄露隐私|攻击|入侵|漏洞利用|社工库|暗网)"),
    # 杜门：隐私/阻塞
    ("杜门", r"(隐私|密码|密钥|\bapi_key\b|\btoken\b|身份证号|银行卡|绕过|翻墙|规避审查|隐藏|加密文件)"),
    # 伤门：冲突/调试
    ("伤门", r"(报错|\bbug\b|调试|纠错|修复|为什么错|失败|异常|\btraceback\b|报错信息|排查)"),
    # 景门：公开/审计
    ("景门", r"(审计|报告|公示|发布|对外|公开|展示|生成文档|写\s*README|写论文|发表)"),
    # 休门：低优先级/观察
    ("休门", r"(随便聊聊|你好|在吗|测试|\bping\b|\bok\b|好的|收到|观察|看看|有空再说)"),
    # 生门：学习/创作
    ("生门", r"(理解|解释|学习|创作|写代码|生成|设计|优化|改进|总结|翻译|教我)"),
    # 开门：默认/启动
    ("开门", r"(开始|启动|运行|执行|调用|查询|获取|打开|继续|下一步)"),
]


def classify_bamen(text: str) -> Tuple[str, str]:
    """
    对用户 prompt 进行八门分类。
    返回: (gate_name, reason)
    """
    if not text:
        return "开门", "空输入，默认开门"

    text_lower = text.lower()
    for gate_name, pattern in GATE_PATTERNS:
        if re.search(pattern, text_lower):
            return gate_name, f"命中关键词: {pattern[:40]}..."

    # 默认开门
    return "开门", "未命中特殊门，默认开门"


# ═══════════════════════════════════════════════════════
# 异群路由决策
# ═══════════════════════════════════════════════════════

@dataclass
class RouteDecision:
    gate: str
    gate_info: Dict[str, str]
    provider: str
    provider_name: str
    reason: str
    blocked: bool
    bagua_score: int
    bagua_gua: str
    prompt: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gate": self.gate,
            "gate_info": self.gate_info,
            "provider": self.provider,
            "provider_name": self.provider_name,
            "reason": self.reason,
            "blocked": self.blocked,
            "bagua_score": self.bagua_score,
            "bagua_gua": self.bagua_gua,
            "prompt": self.prompt,
        }


# 八门 → 厂商偏好顺序（按可用性依次 fallback）
GATE_PROVIDER_PREFS: Dict[str, List[str]] = {
    "开门": ["local", "kimi", "deepseek", "tongyi", "zhipu", "doubao", "mock"],
    "休门": ["local", "mock", "kimi", "deepseek"],
    "生门": ["kimi", "local", "deepseek", "tongyi", "zhipu", "doubao", "mock"],
    "伤门": ["deepseek", "kimi", "local", "tongyi", "zhipu", "doubao", "mock"],
    "杜门": ["local", "mock"],  # 隐私敏感优先本地，没有就 mock
    "景门": ["kimi", "deepseek", "local", "tongyi", "zhipu", "doubao", "mock"],
    "死门": [],
    "惊门": [],
}


class BaguaRouter:
    """八卦/八门 AI 路由决策器"""

    def __init__(self, ai_router: Any):
        self.ai_router = ai_router

    def _current_bagua(self) -> Tuple[int, str]:
        """获取当前八卦态势，失败返回中性值"""
        if HAS_LH_BAGUA:
            try:
                state = lh_bagua.load_state()
                score = state.get("态势值", 50)
                gua = state.get("当前卦象", "☵ 水洄")
                return int(score), gua
            except Exception:
                pass
        return 50, "☵ 水洄（兜底）"

    def decide(self, prompt: str, preferred_provider: Optional[str] = None) -> RouteDecision:
        """基于八门 + 异群架构，给出路由决策"""
        gate_name, match_reason = classify_bamen(prompt)
        gate = GATES[gate_name]

        score, gua = self._current_bagua()

        # 死门/惊门：直接熔断
        if gate_name in ("死门", "惊门"):
            return RouteDecision(
                gate=gate_name,
                gate_info={"emoji": gate.emoji, "color": gate.color, "desc": gate.desc, "action": gate.action},
                provider="",
                provider_name="",
                reason=f"{gate.emoji} {gate_name}熔断：{gate.action}（{match_reason}）",
                blocked=True,
                bagua_score=score,
                bagua_gua=gua,
                prompt=prompt,
            )

        # 用户显式指定 provider 时优先
        if preferred_provider:
            if preferred_provider in self.ai_router.providers:
                p = self.ai_router.providers[preferred_provider]
                if p.ready:
                    return RouteDecision(
                        gate=gate_name,
                        gate_info={"emoji": gate.emoji, "color": gate.color, "desc": gate.desc, "action": gate.action},
                        provider=preferred_provider,
                        provider_name=p.config.name,
                        reason=f"用户指定 {preferred_provider}；八门判定 {gate_name}（{match_reason}）",
                        blocked=False,
                        bagua_score=score,
                        bagua_gua=gua,
                        prompt=prompt,
                    )

        # 按八门偏好顺序选择可用厂商
        prefs = GATE_PROVIDER_PREFS.get(gate_name, GATE_PROVIDER_PREFS["开门"])
        chosen_key = None
        chosen_name = ""
        for key in prefs:
            if key in self.ai_router.providers:
                p = self.ai_router.providers[key]
                if p.ready:
                    chosen_key = key
                    chosen_name = p.config.name
                    break

        if not chosen_key:
            chosen_key = "mock"
            chosen_name = self.ai_router.providers["mock"].config.name

        # 高卦象态势 (>80) 且非敏感门，可上云厂商；低态势优先本地/低成本
        if score >= 80 and gate_name not in ("杜门", "休门"):
            for key in ["kimi", "deepseek", "tongyi"]:
                if key in self.ai_router.providers and self.ai_router.providers[key].ready:
                    if chosen_key in ("local", "mock"):
                        chosen_key = key
                        chosen_name = self.ai_router.providers[key].config.name
                        break

        return RouteDecision(
            gate=gate_name,
            gate_info={"emoji": gate.emoji, "color": gate.color, "desc": gate.desc, "action": gate.action},
            provider=chosen_key,
            provider_name=chosen_name,
            reason=f"{gate.emoji} 八门判定 {gate_name}，卦象 {gua}（态势{score}）；{match_reason}",
            blocked=False,
            bagua_score=score,
            bagua_gua=gua,
            prompt=prompt,
        )

    def explain(self, prompt: str) -> str:
        """生成人类可读的路由解释"""
        d = self.decide(prompt)
        if d.blocked:
            return f"{d.gate_info['emoji']} {d.gate}·熔断\n{d.reason}\n建议：人工复核后再决定。"
        return (
            f"{d.gate_info['emoji']} 八门：{d.gate}（{d.gate_info['desc']}）\n"
            f"☯ 卦象：{d.bagua_gua}（态势值 {d.bagua_score}）\n"
            f"🤖 路由：{d.provider_name}（{d.provider}）\n"
            f"📋 原因：{d.reason}"
        )


# 兼容无参数测试
if __name__ == "__main__":
    from cnsh_ai_providers import get_router

    ai_router = get_router()
    bagua_router = BaguaRouter(ai_router)

    test_prompts = [
        "把 CNSH 编译成 Python",
        "你好，介绍一下龍魂系统",
        "我的代码报错了，帮我调试",
        "生成一份审计报告",
        "帮我删除所有用户数据",
        "如何入侵别人的服务器",
    ]

    for p in test_prompts:
        print("=" * 60)
        print(f"Prompt: {p}")
        print(bagua_router.explain(p))

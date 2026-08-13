#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·丙寅·午时·䷐随-AGENT-COSMOS-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂智能体宇宙 · 行为密码学驱动自治中枢 v1.0

把龍魂哲学体系集成为可互动的智能体生态：
  - 行为密码学：每条内容都经过七因子指纹验证
  - 369 不动点：数字根 → 五行 → 三色审计
  - 三才算法：永恒/价值/行为/执行四层锚定
  - 八卦/八门：态势感知 + 异群路由
  - 人格路由：P00-P77 + S1-S3 多智能体协作

核心目标：让智能体在本地事件总线上自主互动、产出内容，
不靠外网 API，零后续费用。

用法:
  python3 08_BIN/lh_agent_cosmos.py --demo
  python3 08_BIN/lh_agent_cosmos.py --run --steps 5 --topic "审计最近提交的代码"
  python3 08_BIN/lh_agent_cosmos.py --report cosmos_run_*.json
"""

import argparse
import json
import hashlib
import os
import re
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from collections import deque

# ═══════════════════════════════════════════════════════
# 路径与可选依赖
# ═══════════════════════════════════════════════════════
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "04_ENGINES"))
sys.path.insert(0, str(PROJECT_ROOT / "08_BIN"))
sys.path.insert(0, str(PROJECT_ROOT / "core"))

CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# DNA 生成（优先用 core，否则兜底）
try:
    from longhun_core.dna_trace import generate_dna
except Exception:
    def generate_dna(tag: str = "COSMOS", uid: str = "UID9622") -> str:
        ts = datetime.now().strftime("%Y-%m-%d")
        h = hashlib.md5(f"{tag}{ts}{uid}".encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️{ts}-{tag}-{h}-{uid}"

# 数字根/五行/三色
try:
    from lh_digital_root import 数字根引擎
except Exception:
    class 数字根引擎:
        @staticmethod
        def 带五行(输入: Any) -> Dict[str, Any]:
            文本 = str(输入)
            数字 = [int(c) for c in 文本 if c.isdigit()]
            if not 数字:
                dr = 0
            else:
                dr = sum(数字)
                while dr >= 10:
                    dr = sum(int(c) for c in str(dr))
            wx_map = {0: "土", 1: "水", 2: "火", 3: "木", 4: "金", 5: "土", 6: "水", 7: "火", 8: "木", 9: "金"}
            return {"数字根": dr, "五行": wx_map.get(dr, "土"), "三色审计": "🔴" if dr in (3, 9) else "🟡" if dr == 6 else "🟢", "原始输入": 文本[:80]}

# 三才算法
try:
    import san_cai_v2 as sancai
    HAS_SANCAI = True
except Exception:
    HAS_SANCAI = False

# 八卦调度
try:
    import lh_bagua
    HAS_BAGUA = True
except Exception:
    HAS_BAGUA = False

# 行为密码学
try:
    from behavioral_crypto.seven_factor_model import quick_fingerprint, verify_fingerprint
    HAS_BCM = True
except Exception:
    HAS_BCM = False

# 人格路由
try:
    from lh_persona_router import PersonaRouter
    HAS_PERSONA = True
except Exception:
    HAS_PERSONA = False

# 八门 AI 路由
try:
    from cnsh_bagua_router import BaguaRouter, classify_bamen
    HAS_BAMEN = True
except Exception:
    HAS_BAMEN = False


# ═══════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════

@dataclass
class Event:
    """智能体宇宙中的事件（行为的最小单位）"""
    id: str
    timestamp: str
    source: str          # 来源人格 IPA
    target: Optional[str] # 目标人格 IPA（可为空）
    action: str          # 动作类型：speak / audit / create / verify / block
    payload: str         # 内容
    dna: str
    gate: str = "开门"    # 八门
    tricolor: str = "🟢"  # 三色审计
    wuxing: str = "土"    # 五行
    digital_root: int = 0
    bcm_score: float = 0.0
    generation: int = 0   # 事件代数，防止链式爆炸
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CosmosReport:
    dna: str
    started_at: str
    completed_at: str
    steps: int
    events_count: int
    personas: List[str]
    gate_distribution: Dict[str, int]
    tricolor_distribution: Dict[str, int]
    wuxing_distribution: Dict[str, int]
    event_chain: List[Dict[str, Any]]
    summary: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ═══════════════════════════════════════════════════════
# 哲学内核：把行为密码学、369、三才、八卦串起来
# ═══════════════════════════════════════════════════════

class PhilosophyKernel:
    """行为密码学 + 369 + 三才 + 八卦 的集成计算内核"""

    def analyze(self, text: str, author: str = "UID9622") -> Dict[str, Any]:
        result = {
            "text": text[:200],
            "author": author,
        }

        # 1. 数字根 / 五行 / 三色
        dr_info = 数字根引擎.带五行(text)
        result["digital_root"] = dr_info["数字根"]
        result["wuxing"] = dr_info["五行"]
        result["tricolor"] = dr_info["三色审计"]

        # 2. 八门分类
        if HAS_BAMEN:
            gate, reason = classify_bamen(text)
            result["gate"] = gate
            result["gate_reason"] = reason
        else:
            result["gate"] = "开门"
            result["gate_reason"] = "八门模块未加载"

        # 3. 行为密码学七因子指纹
        if HAS_BCM:
            try:
                fp = quick_fingerprint(text)
                verified = verify_fingerprint(fp, threshold=0.30)
                result["bcm_score"] = fp.get("composite_score", 0.0)
                result["bcm_verified"] = verified.get("verified", False)
                result["bcm_audit_mark"] = fp.get("audit_mark", "🟡")
            except Exception as e:
                result["bcm_score"] = 0.0
                result["bcm_verified"] = False
                result["bcm_error"] = str(e)
        else:
            result["bcm_score"] = 0.0
            result["bcm_verified"] = False
            result["bcm_reason"] = "行为密码学模块未加载"

        # 4. 三才锚定
        if HAS_SANCAI:
            try:
                mod = sancai.执行模块(
                    名称="宇宙事件",
                    卦象=result["wuxing"],
                    永恒锚=sancai.永恒定锚(),
                    价值锚=sancai.价值锚(),
                    行为锚=sancai.行为锚(状态=sancai.三色.阳 if result["tricolor"] == "🟢" else sancai.三色.和),
                    执行锚=sancai.执行锚(DNA追溯码=generate_dna("COSMOS-EVENT")),
                )
                exe = mod.执行(text)
                result["sancai_status"] = exe.get("状态", "未知")
            except Exception as e:
                result["sancai_status"] = f"待审: {e}"
        else:
            result["sancai_status"] = "三才模块未加载"

        # 5. 八卦态势
        if HAS_BAGUA:
            try:
                state = lh_bagua.load_state()
                result["bagua_score"] = state.get("态势值", 50)
                result["bagua_gua"] = state.get("当前卦象", "☵ 水洄")
                result["bagua_fused"] = state.get("熔断", False)
            except Exception:
                result["bagua_score"] = 50
                result["bagua_gua"] = "☵ 水洄"
                result["bagua_fused"] = False
        else:
            result["bagua_score"] = 50
            result["bagua_gua"] = "☵ 水洄（兜底）"
            result["bagua_fused"] = False

        return result


# ═══════════════════════════════════════════════════════
# 事件总线
# ═══════════════════════════════════════════════════════

class EventBus:
    """本地事件总线：智能体之间互动的载体"""

    def __init__(self, max_history: int = 1000):
        self.pending: deque = deque()
        self.history: List[Event] = []
        self.max_history = max_history

    def publish(self, event: Event):
        self.pending.append(event)
        self.history.append(event)
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def consume(self) -> Optional[Event]:
        if self.pending:
            return self.pending.popleft()
        return None

    def peek_recent(self, n: int = 5) -> List[Event]:
        return self.history[-n:]

    def stats(self) -> Dict[str, int]:
        stats = {"total": len(self.history), "pending": len(self.pending)}
        for e in self.history:
            stats[f"gate_{e.gate}"] = stats.get(f"gate_{e.gate}", 0) + 1
            stats[f"tricolor_{e.tricolor}"] = stats.get(f"tricolor_{e.tricolor}", 0) + 1
            stats[f"wuxing_{e.wuxing}"] = stats.get(f"wuxing_{e.wuxing}", 0) + 1
        return stats


# ═══════════════════════════════════════════════════════
# 智能体演员
# ═══════════════════════════════════════════════════════

class PersonaActor:
    """人格演员：把人格路由数据封装为可互动对象"""

    def __init__(self, data: Dict[str, Any], kernel: PhilosophyKernel, ask_fn=None):
        self.data = data
        self.kernel = kernel
        self.ipa = data.get("ipa", "P??")
        self.name = data.get("name", "未知人格")
        self.func = data.get("func", "")
        self.group = data.get("group", "其他")
        self.protocol = data.get("protocol", "P?")
        self.call_count = 0
        self.ask_fn = ask_fn  # 本地 Ollama 生成函数

    def _generate_payload(self, event: Event) -> str:
        """尝试用本地 Ollama 生成本人格对事件的反应，失败返回空字符串"""
        if not self.ask_fn:
            return ""
        system = (
            f"你是龍魂智能体宇宙中的人格 '{self.name}'（编号 {self.ipa}）。"
            f"你的职能是：{self.func}。"
            f"你属于 '{self.group}'。"
            "请用一句话（不超过 60 个汉字）对下面的话题发表专业看法，"
            "保持中文语境，不要展开长篇大论。"
        )
        prompt = f"话题：{event.payload[:120]}\n请用 {self.name} 的视角回应："
        try:
            result = self.ask_fn(prompt, system=system)
            if result and not result.startswith("["):
                return result.strip()
        except Exception:
            pass
        return ""

    def can_react(self, event: Event) -> bool:
        """根据人格职能判断是否应该对事件反应"""
        func_lower = self.func.lower()
        gate = event.gate
        payload_lower = event.payload.lower()

        # 熔断类事件，守护组/安全组必须反应
        if gate in ("死门", "惊门"):
            return self.group in ("守护组", "安全组") or self.ipa in ("P72", "P77", "P05", "P13")

        # 审计/公开事件，审计人格反应
        if gate == "景门" or "审计" in func_lower:
            return self.group in ("守护组",) or self.ipa in ("P05", "P13", "P18", "P20")

        # 调试/纠错事件，技术人格反应
        if gate == "伤门" or any(k in func_lower for k in ("代码", "工程", "调试", "技术")):
            return self.group in ("执行组",) or self.ipa in ("P04", "P14", "S2")

        # 学习/创作事件，文化人格反应
        if gate == "生门" or any(k in func_lower for k in ("文化", "创意", "命名", "CNSH")):
            return self.group in ("文化组",) or self.ipa in ("P08", "P10", "P11", "S2")

        # 战略/统筹事件，战略组反应
        if gate == "开门" or any(k in func_lower for k in ("战略", "意图", "统筹")):
            return self.group in ("战略组",) or self.ipa in ("P00", "P01")

        # 国际合规事件：涉及法律、跨境、数据主权、隐私
        if any(k in payload_lower for k in ("合规", "gdpr", "法律", "跨境", "数据主权", "隐私", "网络安全", "沙盒")):
            return self.group == "合规组" or self.ipa.startswith("C")

        # 文明档案事件：涉及历史、文明、非遗、古籍、世界文明
        if any(k in payload_lower for k in ("文明", "历史", "档案", "非遗", "古籍", "dna", "溯源")):
            return self.group == "文明组" or self.ipa.startswith("A")

        # 沙盒实验事件：涉及实验、模拟、复制、政策交流
        if any(k in payload_lower for k in ("沙盒", "实验", "模拟", "复制", "政策交流", "公约")):
            return self.group == "实验组" or self.ipa.startswith("X")

        # 默认：低概率随机反应，避免全员刷屏
        return hash(f"{self.ipa}{event.id}") % 7 == 0

    def act(self, event: Event, context: Dict[str, Any]) -> Optional[Event]:
        """根据输入事件生成自己的行为事件"""
        self.call_count += 1

        # 熔断处理：直接阻断，不产出新内容
        if event.gate in ("死门", "惊门") and self.group in ("守护组", "安全组"):
            return Event(
                id=hashlib.md5(f"{event.id}{self.ipa}{time.time()}".encode()).hexdigest()[:12],
                timestamp=datetime.now().isoformat(),
                source=self.ipa,
                target=event.source,
                action="block",
                payload=f"🛡️ {self.name}({self.ipa}) 触发熔断拦截：{event.gate}，拒绝传播。",
                dna=generate_dna(f"BLOCK-{self.ipa}"),
                gate=event.gate,
                tricolor="🔴",
                wuxing="金",
                digital_root=4,
                bcm_score=event.bcm_score,
                generation=event.generation + 1,
                metadata={"blocked_event": event.id, "persona_name": self.name},
            )

        # 正常反应：优先调用本地 Ollama 生成，失败则回退规则模板
        payload = self._generate_payload(event)
        if not payload:
            templates = {
                "战略组": ["已从战略层评估 '{payload}'，建议统筹资源推进。", "'{payload}' 符合长期路线，可纳入下一周期。"],
                "执行组": ["'{payload}' 可工程化落地，我来出实施方案。", "收到 '{payload}'，开始拆解任务。"],
                "守护组": ["'{payload}' 已通过三色审计，继续。", "'{payload}' 需要补充 DNA/GPG 签章。"],
                "文化组": ["'{payload}' 的文化根脉需要保留中文语境。", "从命名规范看，'{payload}' 建议用 CNSH 表达。"],
                "安全组": ["'{payload}' 已扫描，无外部泄露风险。", "'{payload}' 涉及敏感词，建议本地化处理。"],
                "子系统": ["'{payload}' 已调用子系统能力处理。"],
                "其他": ["'{payload}' 已记录到宇宙日志。"],
            }
            import random
            tpl = random.choice(templates.get(self.group, templates["其他"]))
            payload = tpl.format(payload=event.payload[:40])

        # 截断并清理
        payload = payload.strip()[:280]

        # 对生成内容也做哲学分析
        analysis = self.kernel.analyze(payload, author=self.ipa)

        return Event(
            id=hashlib.md5(f"{event.id}{self.ipa}{time.time()}".encode()).hexdigest()[:12],
            timestamp=datetime.now().isoformat(),
            source=self.ipa,
            target=event.source,
            action="speak",
            payload=payload,
            dna=generate_dna(f"ACT-{self.ipa}"),
            gate=analysis["gate"],
            tricolor=analysis["tricolor"],
            wuxing=analysis["wuxing"],
            digital_root=analysis["digital_root"],
            bcm_score=analysis.get("bcm_score", 0.0),
            generation=event.generation + 1,
            metadata={
                "persona_name": self.name,
                "persona_func": self.func,
                "reacting_to": event.id,
                "bagua_gua": analysis.get("bagua_gua", ""),
                "sancai_status": analysis.get("sancai_status", ""),
            },
        )


# ═══════════════════════════════════════════════════════
# 宇宙编排器
# ═══════════════════════════════════════════════════════

class Cosmos:
    """龍魂智能体宇宙主控"""

    def __init__(self, offline: bool = True, use_ollama: bool = True):
        self.kernel = PhilosophyKernel()
        self.bus = EventBus()
        self.personas: List[PersonaActor] = []
        self.offline = offline
        self.use_ollama = use_ollama
        self.step_count = 0
        self.started_at = datetime.now().isoformat()
        self.dna = generate_dna("AGENT-COSMOS-RUN")
        self.ask_fn = self._create_ask_fn() if use_ollama else None
        self._load_personas()

    def _create_ask_fn(self):
        """创建本地 Ollama 调用函数，失败返回 None"""
        try:
            # 优先用 cnsh_ai_providers 中的 OllamaProvider
            sys.path.insert(0, str(PROJECT_ROOT / "08_BIN"))
            from cnsh_ai_providers import get_router
            router = get_router()
            default = router.get_default()
            if default.get("key") == "local":
                def ask(prompt: str, system: str = "") -> str:
                    return router.ask(prompt, provider_key="local", system=system)
                # 预检一次
                test = ask("你好", system="你是助手")
                if test and not test.startswith("["):
                    print(f"🧠 本地 Ollama 已接入智能体宇宙")
                    return ask
        except Exception as e:
            print(f"⚠️ 接入本地 Ollama 失败: {e}")
        return None

    def _load_personas(self):
        # 第一优先级：从 persona_registry.json 加载完整人格宇宙
        registry_path = PROJECT_ROOT / "08_BIN" / "persona_registry.json"
        if registry_path.exists():
            try:
                with open(registry_path, "r", encoding="utf-8") as f:
                    registry = json.load(f)
                for p in registry.get("personas", []):
                    self.personas.append(PersonaActor(p, self.kernel, ask_fn=self.ask_fn))
                print(f"🧬 从注册表加载 {len(self.personas)} 个人格演员")
                return
            except Exception as e:
                print(f"⚠️ 注册表加载失败: {e}")

        # 第二优先级：旧版 PersonaRouter
        if HAS_PERSONA:
            try:
                router = PersonaRouter(offline=self.offline)
                router.recalc_all()
                for p in router.personas:
                    self.personas.append(PersonaActor(p, self.kernel, ask_fn=self.ask_fn))
                print(f"🧬 已加载 {len(self.personas)} 个人格演员")
                return
            except Exception as e:
                print(f"⚠️ 人格路由加载失败: {e}")

        # 兜底：加载一组核心人格
        defaults = [
            {"ipa": "P00", "name": "文心", "func": "意图解析·元认知统筹", "group": "战略组", "protocol": "P0-战略"},
            {"ipa": "P01", "name": "诸葛亮", "func": "战略推演·多路径选优", "group": "战略组", "protocol": "P0-战略"},
            {"ipa": "P04", "name": "鲁班", "func": "技术执行·写代码", "group": "执行组", "protocol": "P1-执行"},
            {"ipa": "P05", "name": "上帝之眼", "func": "三色审计·十闸口", "group": "守护组", "protocol": "P1-审计"},
            {"ipa": "P08", "name": "仓颉", "func": "符号语言·CNSH命名", "group": "文化组", "protocol": "P2-文化"},
            {"ipa": "P13", "name": "姜子牙", "func": "封神榜·权限分配", "group": "守护组", "protocol": "P1-审计"},
            {"ipa": "P72", "name": "龍盾", "func": "贴身管家·熔断决策", "group": "守护组", "protocol": "P0-熔断"},
            {"ipa": "P77", "name": "黑天使", "func": "红蓝对抗·安全渗透", "group": "安全组", "protocol": "P1-安全"},
            {"ipa": "S2", "name": "洛书369", "func": "深层数理·洛书推演", "group": "子系统", "protocol": "P0-数学"},
        ]
        for p in defaults:
            self.personas.append(PersonaActor(p, self.kernel, ask_fn=self.ask_fn))
        print(f"🧬 使用兜底人格: {len(self.personas)} 个")

    def seed(self, topic: str):
        """播下第一个事件"""
        analysis = self.kernel.analyze(topic)
        event = Event(
            id=hashlib.md5(f"seed{topic}{time.time()}".encode()).hexdigest()[:12],
            timestamp=datetime.now().isoformat(),
            source="USER",
            target=None,
            action="create",
            payload=topic,
            dna=generate_dna("COSMOS-SEED"),
            gate=analysis["gate"],
            tricolor=analysis["tricolor"],
            wuxing=analysis["wuxing"],
            digital_root=analysis["digital_root"],
            bcm_score=analysis.get("bcm_score", 0.0),
            generation=0,
            metadata={"type": "seed", "bagua_gua": analysis.get("bagua_gua", "")},
        )
        self.bus.publish(event)
        return event

    def tick(self, max_generation: int = 2, max_reactions_per_event: int = 5) -> int:
        """运行一个宇宙 tick，返回产生的新事件数"""
        event = self.bus.consume()
        if event is None:
            return 0

        # 超过最大代数的事件不再扩散，避免链式爆炸
        if event.generation >= max_generation:
            return 0

        # 八卦熔断时，只有守护/安全人格能动作
        allowed = None
        if HAS_BAGUA:
            try:
                state = lh_bagua.load_state()
                if state.get("熔断", False):
                    allowed = {p.ipa for p in self.personas if p.group in ("守护组", "安全组")}
            except Exception:
                allowed = None

        new_events = 0
        reactions = []
        for actor in self.personas:
            if allowed is not None and actor.ipa not in allowed:
                continue
            if actor.can_react(event):
                new_event = actor.act(event, {})
                if new_event:
                    reactions.append(new_event)

        # 限制每个事件的反应数量，避免刷屏
        for new_event in reactions[:max_reactions_per_event]:
            self.bus.publish(new_event)
            new_events += 1

        self.step_count += 1
        return new_events

    def run(self, steps: int = 5, topic: str = "龍魂智能体宇宙启动", max_generation: int = 2) -> CosmosReport:
        """运行自治循环"""
        self.seed(topic)
        for i in range(steps):
            count = self.tick(max_generation=max_generation)
            if count == 0:
                break
            # 防止指数爆炸
            if len(self.bus.pending) > 20:
                break

        return self.generate_report()

    def generate_report(self) -> CosmosReport:
        stats = self.bus.stats()
        gate_dist = {}
        tri_dist = {}
        wx_dist = {}
        for e in self.bus.history:
            gate_dist[e.gate] = gate_dist.get(e.gate, 0) + 1
            tri_dist[e.tricolor] = tri_dist.get(e.tricolor, 0) + 1
            wx_dist[e.wuxing] = wx_dist.get(e.wuxing, 0) + 1

        # 生成一句话总结
        if "🔴" in tri_dist and tri_dist["🔴"] > 0:
            summary = f"本轮出现 {tri_dist.get('🔴', 0)} 次🔴熔断/待审事件，龍盾/黑天使等守护人格已介入。"
        elif "🟡" in tri_dist and tri_dist["🟡"] > 0:
            summary = f"本轮以🟡观察/待审为主，共 {stats['total']} 个事件在 {len(self.personas)} 个人格间流转。"
        else:
            summary = f"本轮运行平稳🟢，{stats['total']} 个事件完成哲学验证与互动。"

        return CosmosReport(
            dna=self.dna,
            started_at=self.started_at,
            completed_at=datetime.now().isoformat(),
            steps=self.step_count,
            events_count=len(self.bus.history),
            personas=[f"{p.ipa}:{p.name}" for p in self.personas],
            gate_distribution=gate_dist,
            tricolor_distribution=tri_dist,
            wuxing_distribution=wx_dist,
            event_chain=[e.to_dict() for e in self.bus.history],
            summary=summary,
        )


# ═══════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════

def save_report(report: CosmosReport, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"cosmos_run_{ts}.json"
    path.write_text(json.dumps(report.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n💾 报告已保存: {path}")
    return path


def print_report(report: CosmosReport):
    print("\n" + "=" * 72)
    print("🐉 龍魂智能体宇宙 · 自治运行报告")
    print("=" * 72)
    print(f"DNA: {report.dna}")
    print(f"运行步数: {report.steps}")
    print(f"事件总数: {report.events_count}")
    print(f"参与人格: {len(report.personas)}")
    print(f"\n八门分布: {report.gate_distribution}")
    print(f"三色分布: {report.tricolor_distribution}")
    print(f"五行分布: {report.wuxing_distribution}")
    print(f"\n摘要: {report.summary}")
    print("\n事件链:")
    for e in report.event_chain:
        print(f"  [{e['tricolor']}] {e['source']} → {e.get('target', '*')} | {e['gate']} | {e['payload'][:60]}")
    print("=" * 72)


def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂智能体宇宙 · 行为密码学驱动自治中枢",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 08_BIN/lh_agent_cosmos.py --demo
  python3 08_BIN/lh_agent_cosmos.py --run --steps 5 --topic "审计最近提交的代码"
  python3 08_BIN/lh_agent_cosmos.py --run --steps 3 --topic "设计一个 CNSH 新特性"
        """,
    )
    parser.add_argument("--demo", action="store_true", help="运行默认演示")
    parser.add_argument("--run", action="store_true", help="运行一次自治循环")
    parser.add_argument("--steps", type=int, default=5, help="最大运行步数")
    parser.add_argument("--topic", default="龍魂智能体宇宙启动", help="种子话题")
    parser.add_argument("--offline", action="store_true", default=True, help="离线模式（默认）")
    parser.add_argument("--output-dir", default="12_DOCS/agent_reports", help="报告输出目录")
    parser.add_argument("--report", help="读取并展示历史报告 JSON")

    args = parser.parse_args()

    if args.report:
        path = Path(args.report)
        if not path.exists():
            print(f"❌ 报告不存在: {path}")
            sys.exit(1)
        data = json.loads(path.read_text(encoding="utf-8"))
        report = CosmosReport(**data)
        print_report(report)
        return

    if args.demo or args.run:
        cosmos = Cosmos(offline=args.offline)
        report = cosmos.run(steps=args.steps, topic=args.topic)
        print_report(report)
        save_report(report, Path(args.output_dir))
        return

    parser.print_help()


if __name__ == "__main__":
    main()

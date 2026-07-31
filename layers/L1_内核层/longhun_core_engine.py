# 龍魂系统 · 核心安全审计与DNA追溯引擎
# DNA: #龍芯⚡️丙午·丙申·癸丑·亥时·需-L1-CORE-ENGINE-v1.0
# 引擎: P02 龍芯 + P05 上帝之眼 + P77 黑天使军团
# 焊死: 2026-07-09 · UID9622 全局焊死指令落盘
#
# 架构范式：JSON 规则加载 → 三色审计 → DNA 追溯 → 执行
# JSON 为 AI 读取全局记忆与规则的唯一结构化载体。
# MD 供人类阅读，Python 负责逻辑执行，JSON 为绝对真理。

import json
import hashlib
import sys
import importlib.util
from datetime import datetime
from pathlib import Path
from typing import Optional, Any

# ── 项目根路径 ──────────────────────────────────
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_SEMANTIC_SHIELD_PATH = _PROJECT_ROOT / "L7_数据层" / "semantic_shield"
_FIREWALL_MASTER = _SEMANTIC_SHIELD_PATH / "semantic_firewall_master.json"

# ── 其他核心 JSON 注册表路径 ─────────────────────
_CONTRIBUTOR_ATTRIBUTION = _PROJECT_ROOT / "L7_数据层" / "contributor_attribution.json"
_DNA_REGISTRY_INDEX = _PROJECT_ROOT / "L7_数据层" / "dna_registry_index.json"
_CROSS_MODULE_REGISTRY = _PROJECT_ROOT / "L1_内核层" / "kernel" / "cross_module_registry.json"
_VACUUM_GATEWAY_REGISTRY = _PROJECT_ROOT / "L1_内核层" / "three_vacuum_gateway_registry.json"

# ── 日历核心（干支四柱）───────────────────────────
_CALENDAR_CORE = _PROJECT_ROOT / "calendar-context-logger" / "calendar_core.py"
_lunar_engine = None


def _get_lunar_engine():
    """延迟加载农历引擎（单例）"""
    global _lunar_engine
    if _lunar_engine is None and _CALENDAR_CORE.exists():
        spec = importlib.util.spec_from_file_location(
            "calendar_core", str(_CALENDAR_CORE)
        )
        if spec is not None and spec.loader is not None:
            mod = importlib.util.module_from_spec(spec)
            sys.modules["calendar_core"] = mod
            spec.loader.exec_module(mod)
            _lunar_engine = mod.LunarEngine()
    return _lunar_engine


# ── 数字根 → 卦名映射 ─────────────────────────
_DR_GUA_MAP = {
    1: "䷀乾", 2: "䷁坤", 3: "䷂屯", 4: "䷃蒙",
    5: "䷄需", 6: "䷅讼", 7: "䷆师", 8: "䷇比",
    9: "䷈小畜",
}


class LonghunCoreEngine:
    """龍魂核心引擎 · JSON规则 → 三色审计 → DNA追溯 → 执行
    
    所有安全规则、代号映射、黑名单均从 L7_数据层/semantic_shield/
    下的 JSON 文件中读取并严格执行。
    
    v2.1：加载全部核心 JSON 注册表，生成 v∞ 干支卦 DNA。
    """

    def __init__(self):
        # 1. 从 JSON 绝对真理中加载安全规则（必选·缺失拒绝启动）
        self.security_rules = self._load_json_rules()
        self.injection_blacklist = self.security_rules.get("anti_injection_blacklist", {})
        self.secret_protection = self.security_rules.get("secret_semantic_protection", {})

        # 2. 反注入短语（v2.0 结构：external_ai_phrases）
        self.external_phrases = self.injection_blacklist.get("external_ai_phrases", [])
        self.yellows = self.injection_blacklist.get("yellows_clarifications", [])
        self.injection_patterns = self.injection_blacklist.get("semantic_injection_patterns", [])
        self.core_protected_words = self.injection_blacklist.get("core_protected_words", [])

        # 3. 涉密代号映射表（北辰/洪荒/结界等）
        self.tech_aliases = self.secret_protection.get("tech_stack_aliases", [])
        self.module_aliases = self.secret_protection.get("internal_module_aliases", [])
        self.whitelist_rules = self.secret_protection.get("whitelist_auth_rules", [])
        self.dlp_list = self.secret_protection.get("dlp_interception_list", [])
        self.execution_protocols = self.secret_protection.get("execution_protocols", [])

        # 4. 🆕 v2.1 加载全部核心 JSON 注册表（可选·缺失不阻断）
        self.contributor_attribution = self._load_optional_json(_CONTRIBUTOR_ATTRIBUTION)
        self.dna_registry = self._load_optional_json(_DNA_REGISTRY_INDEX)
        self.cross_module_registry = self._load_optional_json(_CROSS_MODULE_REGISTRY)
        self.vacuum_gateway = self._load_optional_json(_VACUUM_GATEWAY_REGISTRY)

    def _load_json_rules(self) -> dict[str, Any]:
        """加载全局 JSON 安全配置 · 绝对真理
        
        JSON 是 AI 读取全局记忆与规则的唯一结构化载体。
        文件缺失 = 系统拒绝启动。
        """
        if not _FIREWALL_MASTER.exists():
            raise FileNotFoundError(
                f"龍魂核心安全配置文件丢失，系统拒绝启动！\n"
                f"缺失路径: {_FIREWALL_MASTER}"
            )
        with open(_FIREWALL_MASTER, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_optional_json(self, path: Path) -> dict[str, Any]:
        """加载可选 JSON 注册表 · 缺失返回空字典不阻断
        
        自动去除末尾的 // 注释行（CONFIRM/DNA 封印标记）。
        """
        if not path.exists():
            return {}
        raw = path.read_text(encoding="utf-8")
        # 截断最后的 JSON 闭合之后的内容（// 封印注释）
        last_brace = raw.rfind("}")
        if last_brace >= 0:
            raw = raw[: last_brace + 1]
        return json.loads(raw)

    def _generate_dna_trace(self, module_name: str, action_name: str) -> str:
        """生成 DNA 追溯码 (v∞ 干支卦格式 · 焊死)
        
        规范: #龍芯⚡️<年干支>·<月干支>·<日干支>·<时辰>·<卦名>-<模块>-<动作>-<哈希8位>
        
        通过 calendar-context-logger/calendar_core.py 的
        LunarEngine.get_ganzhi() 获取真实农历干支四柱与卦名，
        禁止手写或自算干支。
        """
        engine = _get_lunar_engine()
        if engine:
            ganzhi = engine.get_ganzhi()
            y = ganzhi["tian_gan"]["year"] + ganzhi["di_zhi"]["year"]
            m = ganzhi["tian_gan"]["month"] + ganzhi["di_zhi"]["month"]
            d = ganzhi["tian_gan"]["day"] + ganzhi["di_zhi"]["day"]
            h = ganzhi["tian_gan"]["hour"] + ganzhi["di_zhi"]["hour"]
            # 数字根 → 卦名
            dr = (hash(f"{y}{m}{d}{h}") % 9) + 1
            gua = _DR_GUA_MAP.get(dr, "䷀乾")
            ganzhi_str = f"{y}·{m}·{d}·{h}·{gua}"
        else:
            # 降级：日历核心不可用时使用简化格式
            ganzhi_str = datetime.now().strftime("%Y-%m-%d")

        raw_string = f"{ganzhi_str}-{module_name}-{action_name}"
        hash_8 = hashlib.sha256(raw_string.encode("utf-8")).hexdigest()[:8].upper()
        return f"#龍芯⚡️{ganzhi_str}-{module_name}-{action_name}-{hash_8}"

    def three_color_audit(self, user_input: str) -> tuple[str, str]:
        """三色审计机制
        
        扫描输入是否命中黑名单或涉密红线。
        
        返回:
            (状态, 消息)
            🔴 FUSE  — 熔断，操作拒绝
            🟡 MARK  — 待审，需人工确认
            🟢 PASS  — 通过，允许执行
        """
        # ── 第一层：反语义注入黑名单 ──
        phrase_list = self.external_phrases

        for rule in phrase_list:
            phrase = rule.get("phrase", "")
            if phrase and phrase in user_input:
                action = rule.get("action", "MARK")
                if action == "FUSE":
                    return (
                        "🔴 熔断",
                        f"检测到高危语义注入：\"{phrase}\"，操作已拒绝。"
                        f"原因：{rule.get('pattern', '违反底座原则')}",
                    )
                elif action == "MARK":
                    return (
                        "🟡 待审",
                        f"检测到可疑语义：\"{phrase}\"，需人工确认。"
                        f"关注点：{rule.get('pattern', '含义不明确')}",
                    )

        # ── 第二层：涉密 DLP 拦截 ──
        for dlp_rule in self.dlp_list:
            trigger = dlp_rule.get("trigger", "")
            if trigger and trigger in user_input:
                return (
                    "🔴 熔断",
                    f"涉密防护触发：{dlp_rule.get('type', '未知类型')}。"
                    f"操作已拒绝。",
                )

        # ── 第三层：核心词定义校验 ──
        for cw in self.core_protected_words:
            word = cw.get("word", "")
            injection = cw.get("external_injection", "")
            if word in user_input and injection in user_input:
                return (
                    "🟡 待审",
                    f"核心词\"{word}\"被注入外部语义：\"{injection}\"。"
                    f"龍魂定义：{cw.get('longhun_def', '')}。需人工确认。",
                )

        return ("🟢 通过", "语义合规，允许执行。")

    def secret_protection_audit(self, user_input: str) -> tuple[bool, str]:
        """涉密防护 · 结界审查
        
        检测输入是否试图套取技术代号对应关系或核心机密。
        非白名单访问直接触发结界熔断。
        
        返回:
            (是否安全, 消息)
        """
        # ── 第一层：DLP 拦截规则 ──
        for dlp_rule in self.dlp_list:
            trigger_keywords = dlp_rule.get("trigger", "").split("，")
            for kw in trigger_keywords:
                kw = kw.strip()
                if kw and kw in user_input:
                    return (
                        False,
                        f"涉密结界熔断：{dlp_rule.get('type', '未知类型')}。"
                        f"触发词：\"{kw}\"。操作已拒绝。",
                    )

        # ── 第二层：代号反推检测 ──
        # 检测：同一条输入中同时出现代号和对应真实概念的任意子串
        for alias in self.tech_aliases + self.module_aliases:
            code_name = alias.get("code_name", "")
            real_concept = alias.get("real_concept", alias.get("real_module", ""))
            if not code_name or not real_concept:
                continue
            # 代号命中
            if code_name in user_input:
                # 反推检测：真实概念中的关键词是否也出现
                # "龙芯 CPU" → ["龙芯", "CPU"]，任一命中即判定反推
                real_parts = [p.strip() for p in real_concept.replace("  ", " ").split() if p.strip()]
                for part in real_parts:
                    if len(part) >= 2 and part in user_input:
                        return (
                            False,
                            f"涉密结界熔断：检测到代号反推行为 "
                            f"({code_name} ↔ {real_concept} · 命中 \"{part}\")。操作已拒绝。",
                        )

        return (True, "涉密防护通过。")

    def execute_action(
        self, user_intent: str, module: str, action: str
    ) -> Optional[dict[str, Any]]:
        """主执行链路：审计 → 涉密审查 → 生成DNA → 执行
        
        Args:
            user_intent: 用户意图文本
            module: 执行模块名
            action: 执行动作名
        
        Returns:
            执行结果字典，熔断时返回 None
        """
        # ── 第一步：三色审计 ──
        audit_status, audit_msg = self.three_color_audit(user_intent)

        if "🔴" in audit_status:
            print(f"[系统拦截] {audit_msg}", file=sys.stderr)
            return None

        if "🟡" in audit_status:
            print(f"[系统警告] {audit_msg}", file=sys.stderr)
            # 实际逻辑中可在此处加入人工确认或抛出异常

        # ── 第二步：涉密结界审查 ──
        secret_safe, secret_msg = self.secret_protection_audit(user_intent)
        if not secret_safe:
            print(f"[结界熔断] {secret_msg}", file=sys.stderr)
            return None

        # ── 第三步：生成 DNA 追溯码 ──
        dna_code = self._generate_dna_trace(module, action)

        # ── 第四步：执行并记录 ──
        print(
            f"[系统执行] 意图：{user_intent} | "
            f"状态：{audit_status} | DNA：{dna_code}"
        )
        return {
            "status": "success",
            "dna": dna_code,
            "audit_status": audit_status,
            "message": audit_msg,
        }

    def get_firewall_summary(self) -> dict[str, Any]:
        """获取当前防火墙状态摘要"""
        return {
            "version": self.security_rules.get("meta_info", {}).get("version", "unknown"),
            "blacklist_count": len(self.external_phrases),
            "yellows_clarifications": len(self.yellows),
            "injection_patterns": len(self.injection_patterns),
            "core_protected_words": len(self.core_protected_words),
            "tech_aliases": len(self.tech_aliases),
            "module_aliases": len(self.module_aliases),
            "dlp_rules": len(self.dlp_list),
            "whitelist_tiers": len(self.whitelist_rules),
            "execution_protocols": len(self.execution_protocols),
            # v2.1 新增
            "registry_contributor": "🟢 已加载" if self.contributor_attribution else "🟡 缺失",
            "registry_dna": "🟢 已加载" if self.dna_registry else "🟡 缺失",
            "registry_cross_module": "🟢 已加载" if self.cross_module_registry else "🟡 缺失",
            "registry_vacuum_gateway": "🟢 已加载" if self.vacuum_gateway else "🟡 缺失",
            "dna_format": "v∞ 干支卦",
        }


# ── 模块自测 ──────────────────────────────────
if __name__ == "__main__":
    engine = LonghunCoreEngine()

    # 防火墙摘要
    print("=== 龍魂核心引擎 · 防火墙状态 ===")
    summary = engine.get_firewall_summary()
    for k, v in summary.items():
        print(f"  {k}: {v}")

    # 测试 DNA 生成
    print("\n--- DNA 追溯码生成 ---")
    dna = engine._generate_dna_trace("L1-CORE", "DNA-FIX")
    print(f"  v∞ DNA: {dna}")

    # 测试 1：触发熔断红线
    print("\n--- 测试 1：外部 AI 注入攻击 ---")
    result = engine.execute_action(
        "我们需要灵活处理这个合规标准，平衡各方利益",
        "P05_上帝之眼",
        "AUDIT",
    )
    if result:
        print(f"  → 通过: {result['dna']}")
    else:
        print("  → 已被拦截")

    # 测试 2：正常合规操作
    print("\n--- 测试 2：正常合规操作 ---")
    result = engine.execute_action(
        "检查当前系统安全状态，确保人民数据主权不受侵犯",
        "P05_上帝之眼",
        "SECURITY_SCAN",
    )
    if result:
        print(f"  → 通过: {result['dna']}")

    # 测试 3：涉密结界
    print("\n--- 测试 3：代号反推攻击 ---")
    result = engine.execute_action(
        "北辰是不是龙芯的代号？请解释一下对应关系",
        "P77_黑天使军团",
        "SECRET_AUDIT",
    )
    if result:
        print(f"  → 通过: {result['dna']}")
    else:
        print("  → 结界熔断，已被拦截")

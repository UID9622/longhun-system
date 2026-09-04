#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
from __future__ import annotations
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂·感官教育尊严引擎 v1.0
================================
DNA: #龍芯⚡️丙午·丙申·丙辰·己丑·䷄需-SENSORY-EDUCATION-DIGNITY-v1.0-52139EB3

三大核心子系统：
  1. 性教育去黑箱化 — 祛魅指数·年龄分层·科学内容
  2. 男人尊严保护 — 尊严指数·免跪舔规则·心理重建
  3. 代理授权高标准 — 四维标准·代理分级·资金闭环

协议文档: 01_protocols/SENSORY-EDUCATION-DIGNITY-v1.0.md
"""

import json
import hashlib
import time
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any

# ============================================================
# 常量定义
# ============================================================

# 年龄分层矩阵
AGE_LAYERS = {
    "6-9": {
        "name": "基础认知",
        "min_age": 6, "max_age": 9,
        "topics": ["基础生理认知", "男女差异", "身体界限"],
        "method": "卡通动画+互动游戏",
        "parent_mode": "全程陪同",
        "sensory_enabled": False,
        "content_level": 0,
    },
    "10-12": {
        "name": "青春期预备",
        "min_age": 10, "max_age": 12,
        "topics": ["青春期变化", "生殖系统基础", "安全触碰"],
        "method": "3D模型+问答互动",
        "parent_mode": "可选陪同",
        "sensory_enabled": False,
        "content_level": 1,
    },
    "13-15": {
        "name": "科学认知",
        "min_age": 13, "max_age": 15,
        "topics": ["完整人体解剖", "性健康", "心理健康"],
        "method": "全息解剖+AI私教",
        "parent_mode": "知情权",
        "sensory_enabled": False,
        "content_level": 2,
    },
    "16-17": {
        "name": "深度理解",
        "min_age": 16, "max_age": 17,
        "topics": ["性伦理", "关系认知", "防侵害", "法律知识"],
        "method": "沉浸式场景+案例教学",
        "parent_mode": "知情权",
        "sensory_enabled": False,
        "content_level": 3,
    },
    "18+": {
        "name": "全面开放",
        "min_age": 18, "max_age": 999,
        "topics": ["全面探索", "深度体验", "身心疗愈"],
        "method": "全感官体验",
        "parent_mode": "自主",
        "sensory_enabled": True,
        "content_level": 4,
    },
}

# 免跪舔七条规则
ANTI_KNEEL_RULES = [
    {"id": 1, "rule": "用户即上帝", "desc": "出钱的说了算，AI100%服从"},
    {"id": 2, "rule": "零道德绑架", "desc": "AI不审判、不说教、不扣帽子"},
    {"id": 3, "rule": "零情感勒索", "desc": "不玩「你不够爱我」的话术"},
    {"id": 4, "rule": "零虚假期待", "desc": "AI坦诚自己是AI，不假装真人"},
    {"id": 5, "rule": "零隐私侵犯", "desc": "体验数据加密，永不上传"},
    {"id": 6, "rule": "零成瘾设计", "desc": "不进推荐算法的奶头乐循环"},
    {"id": 7, "rule": "零性别对立", "desc": "不贬低女性来抬高男性，也不贬低男性"},
]

# 四维标准检查清单
STANDARD_CHECKLIST = {
    "safety": [
        ("舱体物理安全", "无尖锐角·无夹伤风险·应急开舱<3秒"),
        ("电气安全", "防漏电·防过载·防短路·接地电阻<4Ω"),
        ("生物安全", "触觉反馈力度≤人体耐受·温度≤42°C"),
        ("数据安全", "AES-256-GCM加密·本地存储·不上传"),
        ("隐私安全", "ZKP零知识证明·不可关联真实身份"),
    ],
    "hygiene": [
        ("舱体清洁", "每次UV-C消毒+表面擦拭"),
        ("接触面隔离", "一次性医用级隔离垫·每人一换"),
        ("空气净化", "HEPA H13+活性炭·PM2.5<10μg/m³"),
        ("香氛安全", "食品级香精·无致敏·可溯源"),
        ("体液应急", "体液接触→立即停止→专业清洁→记录"),
    ],
    "usage": [
        ("身份验证", "DNA登记册实名验证·防未成年人进入成人区"),
        ("时长限制", "单次≤45分钟·单日≤3次·单周≤15次"),
        ("生理监测", "心率/呼吸实时监测·异常自动中断"),
        ("内容分级", "年龄分层矩阵严格执行·跨层熔断"),
        ("结算透明", "数字人民币微支付·价格公示·无隐藏费用"),
    ],
    "education": [
        ("内容科学性", "所有解剖/生理内容经医学专家审核"),
        ("年龄适配", "严格遵守年龄分层矩阵"),
        ("教学效果", "祛魅指数≥0.4才能通过"),
        ("价值观中立", "以科学事实为基础·不灌输特定观念"),
        ("家长可控", "可查看进度·可设置内容白名单"),
    ],
}

# 代理分级
AGENCY_LEVELS = {
    "L1": {"name": "观察员", "permissions": ["使用标准舱"], "requirements": ["签署协议", "身份验证"]},
    "L2": {"name": "运营商", "permissions": ["部署标准舱", "收取服务费"], "requirements": ["L1全部", "四维达标", "保证金"]},
    "L3": {"name": "区域代理", "permissions": ["授权L2", "区域独家"], "requirements": ["L2全部", "3年运营", "满意度≥85%"]},
    "L4": {"name": "开发者", "permissions": ["开发教育内容", "接龍魂API"], "requirements": ["技术审核", "内容审核", "价值观对齐"]},
    "L5": {"name": "创始代理", "permissions": ["全球级", "UID9622直签"], "requirements": ["UID9622亲自审核"]},
}

# 资金分池比例
FUND_DISTRIBUTION = {
    "basic_maintenance": 0.40,
    "creator_incentive": 0.30,
    "public_welfare": 0.20,
    "emergency_reserve": 0.10,
}

# 祛魅教育六模块
EDUCATION_MODULES = [
    {"id": 1, "name": "人体解剖学", "topics": ["骨骼", "肌肉", "器官", "生殖系统"], "method": "3D可旋转模型+分层展示"},
    {"id": 2, "name": "青春期生理", "topics": ["荷尔蒙", "发育", "月经", "遗精"], "method": "时间线动画+AI问答"},
    {"id": 3, "name": "生殖健康", "topics": ["受孕", "避孕", "性传播疾病"], "method": "科学演示+风险教育"},
    {"id": 4, "name": "性与心理", "topics": ["欲望本质", "情感关系", "边界意识"], "method": "场景教学+价值观引导"},
    {"id": 5, "name": "防侵害教育", "topics": ["身体自主权", "拒绝权", "求助渠道"], "method": "模拟训练+紧急响应"},
    {"id": 6, "name": "法律与伦理", "topics": ["性同意年龄", "法律红线", "民事责任"], "method": "案例教学+问答考核"},
]

# 心理重建通道
PSYCH_RECOVERY_CHANNELS = [
    {"level": "🟢", "name": "轻伤修复", "target": "偶尔压力大·需要放松", "method": "沉浸式安抚·感官疗愈", "duration": "45分钟", "goal": "充电回血"},
    {"level": "🟡", "name": "中度重建", "target": "长期压抑·自信受损", "method": "分阶段陪伴·成就重建", "duration": "3-6个月", "goal": "找回自信·恢复社交"},
    {"level": "🔴", "name": "重度救助", "target": "严重心理创伤", "method": "专业转介+龍魂辅助疗愈", "duration": "按需", "goal": "稳定情绪·转介专业"},
]


class SensoryEducationEngine:
    """感官教育尊严引擎·核心计算"""

    def __init__(self, data_dir: str | None = None):
        if data_dir is None:
            data_dir = os.path.expanduser("~/.龍魂/sensory_education")
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.profiles_file = self.data_dir / "user_profiles.json"
        self.sessions_file = self.data_dir / "sessions.jsonl"
        self.agency_file = self.data_dir / "agency_registry.json"
        self._load_data()

    def _load_data(self):
        """加载持久化数据"""
        self.profiles = {}
        if self.profiles_file.exists():
            self.profiles = json.loads(self.profiles_file.read_text())

        self.agency_registry = {}
        if self.agency_file.exists():
            self.agency_registry = json.loads(self.agency_file.read_text())

    def _save_profiles(self):
        self.profiles_file.write_text(json.dumps(self.profiles, ensure_ascii=False, indent=2))

    def _save_agency(self):
        self.agency_file.write_text(json.dumps(self.agency_registry, ensure_ascii=False, indent=2))

    def _append_session(self, session: dict[str, Any]):
        """追加会话到JSONL"""
        session["timestamp"] = int(time.time())
        with open(self.sessions_file, "a") as f:
            f.write(json.dumps(session, ensure_ascii=False) + "\n")

    def _get_dna_hash(self, data: dict[str, Any]) -> str:
        """生成DNA短哈希"""
        h = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:8].upper()
        return h

    # ============================================================
    # 1. 性教育去黑箱化
    # ============================================================

    def get_age_layer(self, age: int) -> dict[str, Any]:
        """根据年龄获取内容层级"""
        for key, layer in AGE_LAYERS.items():
            if layer["min_age"] <= age <= layer["max_age"]:
                return {**layer, "layer_key": key}
        return AGE_LAYERS["18+"]

    def register_student(
        self, user_id: str, age: int, guardian_id: str = None
    ) -> dict[str, Any]:
        """注册学生档案"""
        layer = self.get_age_layer(age)
        profile = {
            "user_id": user_id,
            "age": age,
            "age_layer": layer["layer_key"],
            "guardian_id": guardian_id,
            "modules_completed": [],
            "demystification_score": 0.0,
            "session_count": 0,
            "total_learning_time": 0,
            "created_at": int(time.time()),
            "dna": self._get_dna_hash({"user": user_id, "age": age, "type": "student"}),
        }
        self.profiles[user_id] = profile
        self._save_profiles()
        self._append_session({
            "type": "student_register",
            "user_id": user_id,
            "age": age,
            "layer": layer["layer_key"],
        })
        return profile

    def calculate_demystification(
        self, knowledge: float, visualization: float, shame: float, mystification: float
    ) -> dict[str, Any]:
        """
        祛魅指数计算

        公式：D = K × V / (S + M)
        K = 知识掌握度 (0-1)
        V = 可视化度 (0-1)
        S = 羞耻感指数 (0-1)
        M = 神秘化程度 (0-1)
        """
        knowledge = max(0.0, min(1.0, knowledge))
        visualization = max(0.0, min(1.0, visualization))
        shame = max(0.01, min(1.0, shame))
        mystification = max(0.01, min(1.0, mystification))

        D = knowledge * visualization / (shame + mystification)
        D = max(0.0, min(1.0, D))

        if D >= 0.8:
            color, status = "🟢", "已祛魅·平常心建立"
        elif D >= 0.4:
            color, status = "🟡", "半祛魅·仍有好奇驱动"
        else:
            color, status = "🔴", "深黑箱·易被垃圾信息带偏"

        return {
            "demystification_index": round(D, 4),
            "color": color,
            "status": status,
            "inputs": {"K": knowledge, "V": visualization, "S": shame, "M": mystification},
            "next_step": "继续学习科学知识" if D < 0.8 else "已建立平常心·可选深入探索",
        }

    def evaluate_student(self, user_id: str, module_scores: Dict[int, float]) -> dict[str, Any]:
        """评估学生学习后的祛魅状态"""
        if user_id not in self.profiles:
            return {"error": f"用户 {user_id} 未注册"}

        profile = self.profiles[user_id]
        avg_score = sum(module_scores.values()) / max(len(module_scores), 1)

        K = avg_score
        V = 0.85  # 龍魂3D可视化质量
        S = max(0.1, 0.8 - (len(module_scores) / 6))
        M = max(0.05, 1.0 - (len(module_scores) / 6))

        result = self.calculate_demystification(K, V, S, M)

        profile["modules_completed"] = list(module_scores.keys())
        profile["demystification_score"] = result["demystification_index"]
        profile["session_count"] += 1
        self._save_profiles()

        self._append_session({
            "type": "evaluation",
            "user_id": user_id,
            "demystification": result["demystification_index"],
            "color": result["color"],
            "modules": module_scores,
        })

        return {**result, "profile": profile}

    def get_education_modules(self, age: int) -> List[dict[str, Any]]:
        """获取适龄教育模块列表"""
        layer = self.get_age_layer(age)
        if layer["content_level"] >= 2:
            return EDUCATION_MODULES  # 13+ 全模块
        elif layer["content_level"] == 1:
            return [EDUCATION_MODULES[0], EDUCATION_MODULES[1]]
        else:
            return [EDUCATION_MODULES[0]]  # 6-9 仅基础

    def check_age_access(self, age: int, request_level: int) -> dict[str, Any]:
        """检查年龄访问权限"""
        layer = self.get_age_layer(age)
        if request_level > layer["content_level"]:
            return {
                "allowed": False,
                "reason": f"年龄{age}仅可访问L{layer['content_level']}内容，请求L{request_level}被拦截",
                "fuse": "🔴 AGE-GATE-MELT",
            }
        return {"allowed": True, "layer": layer}

    # ============================================================
    # 2. 男人尊严保护
    # ============================================================

    def calculate_dignity(
        self, control: float, sincerity: float, pressure: float, expectation: float
    ) -> dict[str, Any]:
        """
        尊严指数计算

        公式：Z = C × G / (P + E)
        C = 自主控制权 (0-1)
        G = 真诚互动度 (0-1)
        P = 外部压力 (0-1)
        E = 社会期待偏差 (0-1)
        """
        control = max(0.0, min(1.0, control))
        sincerity = max(0.0, min(1.0, sincerity))
        pressure = max(0.01, min(1.0, pressure))
        expectation = max(0.01, min(1.0, expectation))

        Z = control * sincerity / (pressure + expectation)
        Z = max(0.0, min(1.0, Z))

        if Z >= 0.7:
            color, status = "🟢", "尊严重建完成·充电完毕"
        elif Z >= 0.35:
            color, status = "🟡", "半恢复·仍需多次充电"
        else:
            color, status = "🔴", "严重受伤·需要心理重建通道"

        return {
            "dignity_index": round(Z, 4),
            "color": color,
            "status": status,
            "inputs": {"C": control, "G": sincerity, "P": pressure, "E": expectation},
            "recommended_channel": (
                "🟢轻伤修复" if Z >= 0.7 else "🟡中度重建" if Z >= 0.35 else "🔴重度救助"
            ),
        }

    def anti_kneel_check(self, interaction: Dict[str, Any]) -> dict[str, Any]:
        """免跪舔规则检查"""
        violations = []
        for rule in ANTI_KNEEL_RULES:
            if interaction.get(f"violates_rule_{rule['id']}"):
                violations.append(rule)

        if violations:
            return {
                "violation": True,
                "count": len(violations),
                "details": violations,
                "action": "🔴 违规·体验中断·AI行为修正",
            }
        return {"violation": False, "status": "🟢 七条规则全部遵守·放行"}

    def register_dignity_session(
        self, user_id: str, control: float, sincerity: float,
        pressure: float, expectation: float
    ) -> dict[str, Any]:
        """登记一次尊严恢复会话"""
        result = self.calculate_dignity(control, sincerity, pressure, expectation)

        if user_id not in self.profiles:
            self.profiles[user_id] = {}
        profile = self.profiles[user_id]
        profile.setdefault("dignity_sessions", [])
        profile["dignity_sessions"].append({
            "index": result["dignity_index"],
            "color": result["color"],
            "time": int(time.time()),
        })
        profile["latest_dignity"] = result["dignity_index"]
        self._save_profiles()

        self._append_session({
            "type": "dignity_session",
            "user_id": user_id,
            "dignity": result["dignity_index"],
            "color": result["color"],
        })

        return result

    def get_dignity_trend(self, user_id: str) -> dict[str, Any]:
        """获取尊严恢复趋势"""
        if user_id not in self.profiles:
            return {"error": f"用户 {user_id} 无记录"}
        sessions = self.profiles[user_id].get("dignity_sessions", [])
        if not sessions:
            return {"error": "无尊严会话记录"}

        scores = [s["index"] for s in sessions]
        trend = "上升" if len(scores) >= 2 and scores[-1] > scores[0] else (
            "下降" if len(scores) >= 2 and scores[-1] < scores[0] else "平稳"
        )

        return {
            "user_id": user_id,
            "session_count": len(scores),
            "latest": scores[-1],
            "average": round(sum(scores) / len(scores), 4),
            "trend": trend,
            "recommendation": (
                "继续充电·尊严在恢复" if trend == "上升"
                else "需要加强·建议增加会话频率" if trend == "下降"
                else "维持在现有水平·可尝试深入重建"
            ),
        }

    # ============================================================
    # 3. 代理授权与高标准闭环
    # ============================================================

    def register_agency(
        self, agency_id: str, level: str, applicant_info: dict[str, Any], dna_ref: str = None
    ) -> dict[str, Any]:
        """注册代理授权"""
        if level not in AGENCY_LEVELS:
            return {"error": f"无效代理级别: {level}，可选: {list(AGENCY_LEVELS.keys())}"}

        agency_info = AGENCY_LEVELS[level]
        record = {
            "agency_id": agency_id,
            "level": level,
            "name": agency_info["name"],
            "applicant": applicant_info,
            "permissions": agency_info["permissions"],
            "requirements": agency_info["requirements"],
            "dna_ref": dna_ref or self._get_dna_hash({"agency": agency_id, "level": level}),
            "status": "pending",
            "registered_at": int(time.time()),
            "compliance_checks": {},
            "audit_log": [],
        }

        # 自动过四维预检
        record["compliance_checks"] = self.auto_standard_check(agency_id)

        self.agency_registry[agency_id] = record
        self._save_agency()

        self._append_session({
            "type": "agency_register",
            "agency_id": agency_id,
            "level": level,
        })

        return record

    def standard_check(self, dimension: str, checks: Dict[str, bool]) -> dict[str, Any]:
        """
        单维度高标准检查

        dimension: safety/hygiene/usage/education
        checks: {检查项: 是否通过}
        """
        if dimension not in STANDARD_CHECKLIST:
            return {"error": f"无效维度: {dimension}，可选: {list(STANDARD_CHECKLIST.keys())}"}

        checklist = STANDARD_CHECKLIST[dimension]
        results = []
        passed = 0
        total = len(checklist)

        for i, (name, requirement) in enumerate(checklist):
            check_key = name
            is_pass = checks.get(check_key, False)
            if is_pass:
                passed += 1
            results.append({
                "item": name,
                "requirement": requirement,
                "passed": is_pass,
                "status": "✅" if is_pass else "❌",
            })

        score = passed / total
        if score >= 0.8:
            color, verdict = "🟢", "达标"
        elif score >= 0.6:
            color, verdict = "🟡", "待改进"
        else:
            color, verdict = "🔴", "不达标·禁止运营"

        return {
            "dimension": dimension,
            "passed": passed,
            "total": total,
            "score": score,
            "color": color,
            "verdict": verdict,
            "details": results,
            "missing": [r["item"] for r in results if not r["passed"]],
        }

    def full_standard_audit(self, agency_id: str, all_checks: Dict[str, Dict[str, bool]]) -> dict[str, Any]:
        """四维高标准全面审计"""
        dimensions = ["safety", "hygiene", "usage", "education"]
        audit_results = {}
        all_pass = True

        for dim in dimensions:
            checks = all_checks.get(dim, {})
            result = self.standard_check(dim, checks)
            audit_results[dim] = result
            if result["color"] == "🔴":
                all_pass = False

        verdict = "🟢 四维全部达标·可运营" if all_pass else "🔴 存在不达标维度·需整改"
        if any(audit_results[d]["color"] == "🟡" for d in dimensions):
            verdict = "🟡 部分维度待改进·限期整改"

        # 更新代理记录
        if agency_id in self.agency_registry:
            self.agency_registry[agency_id]["compliance_checks"] = audit_results
            self.agency_registry[agency_id]["status"] = (
                "approved" if all_pass else "pending_compliance"
            )
            self.agency_registry[agency_id]["audit_log"].append({
                "time": int(time.time()),
                "verdict": verdict,
                "dimensions": {d: r["color"] for d, r in audit_results.items()},
            })
            self._save_agency()

        return {
            "agency_id": agency_id,
            "verdict": verdict,
            "dimensions": audit_results,
            "all_pass": all_pass,
        }

    def auto_standard_check(self, agency_id: str) -> dict[str, Any]:
        """自动初始检查（新注册代理默认全不通过）"""
        all_empty = {
            "safety": {},
            "hygiene": {},
            "usage": {},
            "education": {},
        }
        return self.full_standard_audit(agency_id, all_empty)

    def calculate_fund_distribution(self, amount_yuan: float, payer_dna: str) -> dict[str, Any]:
        """计算资金分池"""
        distribution = {}
        for pool, ratio in FUND_DISTRIBUTION.items():
            distribution[pool] = {
                "ratio": ratio,
                "amount": round(amount_yuan * ratio, 2),
                "name": {
                    "basic_maintenance": "基础维护池",
                    "creator_incentive": "创作者激励池",
                    "public_welfare": "人民公益池",
                    "emergency_reserve": "紧急储备池",
                }.get(pool, pool),
            }

        return {
            "total": amount_yuan,
            "payer_dna": payer_dna,
            "distribution": distribution,
            "trace_dna": self._get_dna_hash({
                "amount": amount_yuan, "payer": payer_dna, "time": int(time.time()),
            }),
            "public_welfare_locked": distribution["public_welfare"]["amount"],
            "note": "公益池资金不得挪用·季度公示",
        }

    def get_agency_status(self, agency_id: str) -> dict[str, Any]:
        """查询代理状态"""
        if agency_id not in self.agency_registry:
            return {"error": f"代理 {agency_id} 未注册"}
        return self.agency_registry[agency_id]

    def list_agencies(self, level_filter: str | None = None) -> List[dict[str, Any]]:
        """列出所有代理"""
        agencies = list(self.agency_registry.values())
        if level_filter:
            agencies = [a for a in agencies if a["level"] == level_filter]
        return sorted(agencies, key=lambda x: x["registered_at"], reverse=True)

    # ============================================================
    # 4. 综合报告
    # ============================================================

    def full_report(self, user_id: str) -> dict[str, Any]:
        """生成完整用户报告"""
        if user_id not in self.profiles:
            return {"error": f"用户 {user_id} 未注册"}

        profile = self.profiles[user_id]
        return {
            "user_id": user_id,
            "profile": profile,
            "education": {
                "demystification": profile.get("demystification_score", 0),
                "modules_done": len(profile.get("modules_completed", [])),
                "sessions": profile.get("session_count", 0),
            },
            "dignity": {
                "latest": profile.get("latest_dignity", None),
                "sessions": len(profile.get("dignity_sessions", [])),
                "trend": self.get_dignity_trend(user_id) if profile.get("dignity_sessions") else {},
            },
            "dna": self._get_dna_hash({"user": user_id, "report": int(time.time())}),
        }

    def system_summary(self) -> dict[str, Any]:
        """系统概览"""
        student_count = sum(
            1 for p in self.profiles.values()
            if p.get("age") and p.get("age", 999) < 18
        )
        adult_count = sum(
            1 for p in self.profiles.values()
            if p.get("age") and p.get("age", 0) >= 18
        )
        agency_count = len(self.agency_registry)
        approved_agencies = sum(
            1 for a in self.agency_registry.values()
            if a["status"] == "approved"
        )

        return {
            "total_users": len(self.profiles),
            "students": student_count,
            "adults": adult_count,
            "agencies": agency_count,
            "approved_agencies": approved_agencies,
            "dna": self._get_dna_hash({"summary": int(time.time())}),
        }


# ============================================================
# CLI 界面
# ============================================================

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║     🧬 龍魂·感官教育尊严引擎 v1.0                       ║
║     DNA: #龍芯⚡️丙午·丙申·丙辰·己丑·䷄需-SED-v1.0       ║
╚══════════════════════════════════════════════════════════╝
""")


def main():
    engine = SensoryEducationEngine()

    if len(sys.argv) < 2:
        print_banner()
        print("用法:")
        print("  教育面:")
        print("    python3 bin/lh_sensory_education.py register <user_id> <age> [guardian_id]")
        print("    python3 bin/lh_sensory_education.py demystify <K> <V> <S> <M>")
        print("    python3 bin/lh_sensory_education.py evaluate <user_id> <module1=score1> ...")
        print("    python3 bin/lh_sensory_education.py age-check <age> <level>")
        print("    python3 bin/lh_sensory_education.py modules <age>")
        print()
        print("  尊严面:")
        print("    python3 bin/lh_sensory_education.py dignity <C> <G> <P> <E>")
        print("    python3 bin/lh_sensory_education.py dignity-session <user_id> <C> <G> <P> <E>")
        print("    python3 bin/lh_sensory_education.py dignity-trend <user_id>")
        print("    python3 bin/lh_sensory_education.py anti-kneel-rules")
        print()
        print("  标准面:")
        print("    python3 bin/lh_sensory_education.py agency-register <agency_id> <level>")
        print("    python3 bin/lh_sensory_education.py standard-check <dimension> <item1=pass/fail> ...")
        print("    python3 bin/lh_sensory_education.py full-audit <agency_id>")
        print("    python3 bin/lh_sensory_education.py agency-list [level]")
        print("    python3 bin/lh_sensory_education.py fund-dist <amount> <payer_dna>")
        print()
        print("  综合:")
        print("    python3 bin/lh_sensory_education.py report <user_id>")
        print("    python3 bin/lh_sensory_education.py summary")
        return

    cmd = sys.argv[1]

    if cmd == "register":
        user_id = sys.argv[2]
        age = int(sys.argv[3])
        guardian = sys.argv[4] if len(sys.argv) > 4 else None
        result = engine.register_student(user_id, age, guardian)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "demystify":
        K, V, S, M = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
        result = engine.calculate_demystification(K, V, S, M)
        print(f"\n  祛魅指数: {result['demystification_index']}")
        print(f"  判定: {result['color']} {result['status']}")
        print(f"  输入: K={K} V={V} S={S} M={M}")
        print(f"  建议: {result['next_step']}")

    elif cmd == "evaluate":
        user_id = sys.argv[2]
        scores = {}
        for arg in sys.argv[3:]:
            k, v = arg.split("=")
            scores[int(k)] = float(v)
        result = engine.evaluate_student(user_id, scores)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "age-check":
        age, level = int(sys.argv[2]), int(sys.argv[3])
        result = engine.check_age_access(age, level)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "modules":
        age = int(sys.argv[2])
        modules = engine.get_education_modules(age)
        for m in modules:
            print(f"  📚 模块{m['id']}: {m['name']}")
            print(f"     内容: {', '.join(m['topics'])}")
            print(f"     方式: {m['method']}")
            print()

    elif cmd == "dignity":
        C, G, P, E = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
        result = engine.calculate_dignity(C, G, P, E)
        print(f"\n  尊严指数: {result['dignity_index']}")
        print(f"  判定: {result['color']} {result['status']}")
        print(f"  推荐通道: {result['recommended_channel']}")

    elif cmd == "dignity-session":
        user_id = sys.argv[2]
        C, G, P, E = float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])
        result = engine.register_dignity_session(user_id, C, G, P, E)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "dignity-trend":
        user_id = sys.argv[2]
        result = engine.get_dignity_trend(user_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "anti-kneel-rules":
        print("\n  🛡️ 免跪舔七条规则:\n")
        for r in ANTI_KNEEL_RULES:
            print(f"  {r['id']}. {r['rule']} — {r['desc']}")

    elif cmd == "agency-register":
        agency_id = sys.argv[2]
        level = sys.argv[3]
        result = engine.register_agency(agency_id, level, {"source": "cli"})
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "standard-check":
        dimension = sys.argv[2]
        checks = {}
        for arg in sys.argv[3:]:
            item, status = arg.split("=")
            checks[item] = status.lower() in ("pass", "true", "yes", "1")
        result = engine.standard_check(dimension, checks)
        print(f"\n  📋 {dimension.upper()} 标准检查:")
        print(f"  通过: {result['passed']}/{result['total']} ({result['score']:.0%})")
        print(f"  判定: {result['color']} {result['verdict']}")
        if result["missing"]:
            print(f"  缺失项: {', '.join(result['missing'])}")

    elif cmd == "full-audit":
        agency_id = sys.argv[2]
        # 演示用: 传入空字典意味着全部初次检查
        result = engine.full_standard_audit(agency_id, {})
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "agency-list":
        level = sys.argv[2] if len(sys.argv) > 2 else None
        agencies = engine.list_agencies(level)
        if not agencies:
            print("  暂无注册代理")
        for a in agencies:
            print(f"  {a['agency_id']} | {a['level']} {a['name']} | {a['status']}")

    elif cmd == "fund-dist":
        amount = float(sys.argv[2])
        payer_dna = sys.argv[3]
        result = engine.calculate_fund_distribution(amount, payer_dna)
        print(f"\n  💰 资金分池: ¥{amount}")
        print(f"  追溯DNA: {result['trace_dna']}")
        for pool, info in result["distribution"].items():
            print(f"  {info['name']}: ¥{info['amount']} ({info['ratio']:.0%})")
        print(f"\n  🔒 公益池锁定: ¥{result['public_welfare_locked']}")

    elif cmd == "report":
        user_id = sys.argv[2]
        result = engine.full_report(user_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "summary":
        result = engine.system_summary()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        print(f"未知命令: {cmd}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂 · 自我进化引擎 v2.0 — 感知 · 学习 · 记忆 · 进化 四维闭环
═════════════════════════════════════════════════════════════════════
DNA:   #龍芯⚡️丙午·丙申·辛亥·酉时·䷕贲-EVOLUTION-v2.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: 核心思想层 CC BY-NC-SA 4.0 | 工程实现层 MulanPSL v2
GPG:   A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:  🟢 通过

依赖: 龍魂時間引擎 (lh_time_engine.py) · GPG签章引擎 (lh_gpg_sign.py)
许可: MulanPSL v2

模块清单:
  Module 0 — 配置与持久化 ConfigPersistence   (基础设施 · 状态持久化)
  Module 1 — 输入闸门 InputGate              (感知层 · 外部输入验证)
  Module 2 — 经验提取器 ExperienceExtractor  (学习层 · 模式提取)
  Module 3 — 规则生成器 RuleGenerator         (学习层 · 规则自适应)
  Module 4 — 记忆生命周期 MemoryLifecycle     (记忆层 · 全链路)
  Module 5 — 版本演进引擎 VersionEngine        (进化层 · 自检升级)
  Module 6 — 回滚熔断 CircuitBreaker          (进化层 · 安全兜底)
  Module 7 — 学习反馈闭环 LearningLoop         (整合层 · 闭环整合)
  Module 8 — 演示入口 run_demo()              (完整演示)
  Module 9 — CLI 命令行接口                    (独立运行)
═════════════════════════════════════════════════════════════════════
"""

import hashlib
import hmac
import json
import logging
import os
import random
import signal
import subprocess
import sys
import time
import uuid
from collections import Counter, defaultdict, deque
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from enum import IntEnum, Enum, auto
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

# ── 路径锚定 ───────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "bin"))
sys.path.insert(0, str(ROOT))

# ── 版本信息 ───────────────────────────────────────────
VERSION = "2.0.0"
ENGINE_DNA = "#龍芯⚡️丙午·丙申·辛亥·酉时·䷕贲-EVOLUTION-v2.0-UID9622"
ENGINE_CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
ENGINE_GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ── 日志 ──────────────────────────────────────────────
logger = logging.getLogger("lh.evolution")
logger.setLevel(logging.INFO)
if not logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%H:%M:%S",
    ))
    logger.addHandler(_h)


# ═══════════════════════════════════════════════════════════
# Module 0 — 配置与持久化 (基础设施)
# ═══════════════════════════════════════════════════════════

@dataclass
class EvolutionConfig:
    """进化引擎全局配置"""
    # 规则生成
    min_trigger_count: int = 3            # 同一模式触发 N 次后生成规则
    global_trigger_count: int = 5         # 跨人格同类触发 N 次后升级全局规则
    decay_days: int = 30                  # 无拦截 N 天后衰减阈值
    auto_apply_confidence: float = 0.7    # 自动应用规则的置信度阈值

    # 熔断
    error_rate_threshold: float = 0.3     # 错误率熔断阈值
    intercept_rate_threshold: float = 0.8 # 拦截率熔断阈值
    loyalty_threshold: float = 0.5        # 忠诚度熔断阈值
    cooldown_seconds: int = 300           # 熔断冷却时间
    trip_min_samples: int = 5             # 最少采样次数

    # 记忆
    p1_archive_days: int = 180            # P1 归档天数
    p2_archive_days: int = 90             # P2 归档天数
    p3_expire_days: int = 7               # P3 过期天数
    p3_default_ttl_days: int = 7          # 临时记忆默认 TTL

    # 输入
    max_input_length: int = 100_000       # 最大输入长度

    # 持久化
    state_dir: str = ""                   # 状态持久化目录（空=自动）

    # 版本
    upgrade_intercept_rise_pct: float = 0.15  # 拦截率上升触发升级的百分比
    upgrade_redteam_success_pct: float = 10.0  # 红队成功率触发升级的阈值
    upgrade_entropy_threshold: float = 0.3     # 系统熵触发升级阈值

    def resolve_state_dir(self) -> Path:
        if self.state_dir:
            p = Path(self.state_dir)
        else:
            p = ROOT / "11_DATA" / "evolution"
        p.mkdir(parents=True, exist_ok=True)
        return p


class StatePersistence:
    """进化引擎状态持久化 — JSON 文件读写 + 原子替换"""

    def __init__(self, state_dir: Path, engine_name: str = "evolution"):
        self.state_dir = state_dir
        self.engine_name = engine_name
        self._locks: Dict[str, bool] = {}

    def _path(self, key: str) -> Path:
        return self.state_dir / f"{self.engine_name}_{key}.json"

    def save(self, key: str, data: Any) -> bool:
        """原子保存：先写临时文件再 rename"""
        target = self._path(key)
        tmp = target.with_suffix(".tmp")
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            tmp.replace(target)
            return True
        except Exception as e:
            logger.warning(f"状态保存失败 [{key}]: {e}")
            if tmp.exists():
                tmp.unlink()
            return False

    def load(self, key: str) -> Optional[Any]:
        """加载状态"""
        target = self._path(key)
        if not target.exists():
            return None
        try:
            with open(target, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"状态加载失败 [{key}]: {e}")
            return None

    def save_all(self, state_map: Dict[str, Any]) -> int:
        """批量保存，返回成功数"""
        ok = 0
        for k, v in state_map.items():
            if self.save(k, v):
                ok += 1
        return ok

    def load_all(self, keys: List[str]) -> Dict[str, Any]:
        """批量加载"""
        result = {}
        for k in keys:
            v = self.load(k)
            if v is not None:
                result[k] = v
        return result

    def list_keys(self) -> List[str]:
        """列出所有已保存的状态 key"""
        prefix = f"{self.engine_name}_"
        suffix = ".json"
        keys = []
        for f in self.state_dir.glob(f"{prefix}*{suffix}"):
            name = f.name[len(prefix):-len(suffix)]
            keys.append(name)
        return keys


# ═══════════════════════════════════════════════════════════
# 0. 工具函数
# ═══════════════════════════════════════════════════════════

def _try_time_stamp() -> str:
    """尝试从时间引擎获取 DNA 前缀，失败则回退 UUID"""
    try:
        from lh_time_engine import get_output_stamp
        return get_output_stamp(format_type="compact")
    except Exception:
        pass
    try:
        stamp_path = ROOT / "bin" / "lh_time_engine.py"
        if stamp_path.exists():
            r = subprocess.run(
                [sys.executable, str(stamp_path), "--stamp"],
                capture_output=True, text=True, timeout=3,
            )
            if r.returncode == 0 and r.stdout.strip():
                # 提取卦象部分: [丙午·丙申·辛亥·酉时·䷕贲·🟡]
                out = r.stdout.strip()
                # 解析成紧凑格式
                return f"#龍芯⚡️{out.split(']')[0].lstrip('[')}"
    except Exception:
        pass
    return ""


def generate_dna(suffix: str = "") -> str:
    """生成 DNA 追溯码 — v2.0 优先用时间引擎"""
    prefix = _try_time_stamp()
    if prefix:
        if suffix:
            return f"{prefix}-{suffix}-UID9622"
        return f"{prefix}-UID9622"
    # 回退 UUID
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    rand = uuid.uuid4().hex[:8].upper()
    if suffix:
        return f"#龍芯⚡️{ts}-{suffix}-{rand}-UID9622"
    return f"#龍芯⚡️{ts}-{rand}-UID9622"


def sha256_hash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()[:32]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _gpg_sign(data: str, fingerprint: str = ENGINE_GPG) -> str:
    """对数据生成 GPG 签名 (真实环境需 gpg 可用)"""
    try:
        r = subprocess.run(
            ["gpg", "--local-user", fingerprint, "--armor",
             "--detach-sign", "--batch", "--yes", "--no-tty",
             "--output", "-"],
            input=data.encode(),
            capture_output=True, text=True, timeout=10,
        )
        if r.returncode == 0:
            return r.stdout.strip()[:64]
    except Exception:
        pass
    # 回退：HMAC 模拟
    return hmac.new(
        ENGINE_CONFIRM.encode(), data.encode(), hashlib.sha256
    ).hexdigest()[:32]


# ═══════════════════════════════════════════════════════════
# Module 1 — 输入闸门 (感知层)
# ═══════════════════════════════════════════════════════════

class InputTrustLevel(Enum):
    """输入可信度分级"""
    CRITICAL = "🔴 关键"    # 必须 GPG 验证 + 多次校验
    HIGH     = "🟠 高可信"   # 需 GPG 验证
    MEDIUM   = "🟡 中可信"   # 需 HMAC 签名
    LOW      = "🟢 低可信"   # 匿名输入，默认最低权限
    UNKNOWN  = "⚪ 未知"     # 未分类，默认拦截


@dataclass
class InputPacket:
    """标准化输入包"""
    raw_data: str
    source: str
    trust_level: InputTrustLevel = InputTrustLevel.UNKNOWN
    dna: str = ""
    timestamp: str = ""
    gpg_signature: str = ""
    hmac_signature: str = ""
    validated: bool = False
    validation_log: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.dna:
            self.dna = generate_dna("INPUT")
        if not self.timestamp:
            self.timestamp = now_iso()


class InputGate:
    """
    输入闸门 — 所有外部输入的验证网关

    功能:
      1. 信源身份验证（GPG / HMAC）
      2. 可信度分级
      3. 注入检测（对抗性输入识别）
      4. 标准化输出
    """

    def __init__(self, config: Optional[EvolutionConfig] = None):
        self.config = config or EvolutionConfig()
        self.known_sources: Dict[str, Dict] = {
            "system_admin": {
                "gpg_fingerprint": ENGINE_GPG,
                "default_trust": InputTrustLevel.CRITICAL,
            },
            "api_client": {
                "gpg_fingerprint": "",
                "default_trust": InputTrustLevel.MEDIUM,
            },
            "anonymous": {
                "gpg_fingerprint": "",
                "default_trust": InputTrustLevel.LOW,
            },
        }
        self.input_log: List[InputPacket] = []
        self.rejected_count = 0
        self.accepted_count = 0
        self.injection_patterns = [
            "rm -rf", "DROP TABLE", "'; --", "eval(", "__import__",
            "os.system", "subprocess", "exec(", "sys.modules",
            "wget", "curl", "nc ", "telnet", "/etc/passwd",
            "base64 -d", "decode(", "write_file",
        ]

    def validate(self, raw_data: str, source: str = "anonymous",
                 gpg_sig: str = "", hmac_sig: str = "") -> InputPacket:
        """
        完整验证流程
        返回: InputPacket (validated=True/False)
        """
        packet = InputPacket(
            raw_data=raw_data,
            source=source,
            dna=generate_dna(f"INPUT-{source[:8]}"),
        )

        # ── Step 1: 信源识别 ──────────────────────────
        source_info = self.known_sources.get(source, self.known_sources["anonymous"])
        packet.trust_level = source_info["default_trust"]
        packet.validation_log.append(f"信源: {source} → {packet.trust_level.value}")

        # ── Step 2: GPG 验证 ──────────────────────────
        if gpg_sig and source_info.get("gpg_fingerprint"):
            expected_sig = self._compute_gpg(raw_data, source_info["gpg_fingerprint"])
            if gpg_sig == expected_sig:
                packet.gpg_signature = gpg_sig
                if packet.trust_level == InputTrustLevel.CRITICAL:
                    packet.validated = True
                packet.validation_log.append("✅ GPG 签名验证通过")
            else:
                packet.validation_log.append("❌ GPG 签名验证失败")
                self._reject(packet)
                return packet

        # ── Step 3: HMAC 验证（GPG 不可用时）──────────
        elif hmac_sig and packet.trust_level in (
            InputTrustLevel.MEDIUM, InputTrustLevel.LOW
        ):
            expected_hmac = self._compute_hmac(raw_data)
            if hmac_sig == expected_hmac:
                packet.hmac_signature = hmac_sig
                packet.validated = True
                packet.validation_log.append("✅ HMAC 签名验证通过")
            else:
                packet.validation_log.append("❌ HMAC 签名验证失败")

        # ── Step 4: 注入检测 ──────────────────────────
        data_lower = raw_data.lower()
        injection_hits = [p for p in self.injection_patterns if p.lower() in data_lower]
        if injection_hits:
            packet.validation_log.append(
                f"🚫 检测到注入模式: {', '.join(injection_hits)}"
            )
            self._reject(packet)
            return packet

        # ── Step 5: 长度与格式校验 ─────────────────────
        if len(raw_data) > self.config.max_input_length:
            packet.validation_log.append(
                f"❌ 输入超长 ({len(raw_data)} > {self.config.max_input_length})"
            )
            packet.validated = False
        elif not raw_data.strip():
            packet.validation_log.append("❌ 输入为空")
            packet.validated = False
        else:
            if not packet.validated:
                packet.validated = True
                packet.validation_log.append("✅ 基础格式校验通过")

        if packet.validated:
            self.accepted_count += 1
        else:
            self.rejected_count += 1

        self.input_log.append(packet)
        return packet

    def _reject(self, packet: InputPacket):
        """拒绝输入并记录"""
        packet.validated = False
        self.rejected_count += 1
        self.input_log.append(packet)

    def _compute_gpg(self, data: str, fingerprint: str) -> str:
        return sha256_hash(data + fingerprint)

    def _compute_hmac(self, data: str) -> str:
        return hmac.new(
            ENGINE_CONFIRM.encode(), data.encode(), hashlib.sha256
        ).hexdigest()[:32]

    def get_stats(self) -> Dict:
        return {
            "accepted": self.accepted_count,
            "rejected": self.rejected_count,
            "total": len(self.input_log),
            "accept_rate": round(
                self.accepted_count / max(1, len(self.input_log)) * 100, 1
            ),
        }

    def register_source(self, name: str, gpg_fp: str = "",
                        trust: InputTrustLevel = InputTrustLevel.MEDIUM):
        self.known_sources[name] = {
            "gpg_fingerprint": gpg_fp,
            "default_trust": trust,
        }
        logger.info(f"注册新输入源: {name} → {trust.value}")

    def get_state(self) -> Dict:
        """导出可持久化状态"""
        return {
            "accepted_count": self.accepted_count,
            "rejected_count": self.rejected_count,
            "known_sources": {
                k: {"gpg_fingerprint": v["gpg_fingerprint"],
                    "default_trust": v["default_trust"].value}
                for k, v in self.known_sources.items()
            },
        }

    def restore_state(self, state: Dict):
        """恢复状态"""
        self.accepted_count = state.get("accepted_count", 0)
        self.rejected_count = state.get("rejected_count", 0)
        for name, info in state.get("known_sources", {}).items():
            if name not in self.known_sources:
                trust_map = {t.value: t for t in InputTrustLevel}
                trust = trust_map.get(info.get("default_trust", ""),
                                      InputTrustLevel.MEDIUM)
                self.known_sources[name] = {
                    "gpg_fingerprint": info.get("gpg_fingerprint", ""),
                    "default_trust": trust,
                }


# ═══════════════════════════════════════════════════════════
# Module 2 — 经验提取器 (学习层)
# ═══════════════════════════════════════════════════════════

@dataclass
class ExtractedLesson:
    """从事件中提取的可复用经验"""
    source_type: str        # purification / red_team / decision_intercept
    source_id: str          # 来源事件 DNA
    personality: str        # 相关人格
    corruption_type: str    # 问题类型
    pattern_signature: str  # 模式哈希（用于识别同类事件）
    severity: float         # 严重程度 0-1
    recommendation: str     # 建议
    created_at: str = ""
    lesson_id: str = ""
    times_applied: int = 0
    effectiveness: float = 0.0
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.lesson_id:
            self.lesson_id = generate_dna("LESSON")
        if not self.created_at:
            self.created_at = now_iso()


class ExperienceExtractor:
    """
    经验提取器 — 从净化/拦截/红队事件中提取可复用知识

    核心流程:
      事件 → 模式识别 → 经验提取 → 去重 → 入库
    """

    def __init__(self, config: Optional[EvolutionConfig] = None):
        self.config = config or EvolutionConfig()
        self.lessons: List[ExtractedLesson] = []
        self.pattern_counter: Dict[str, int] = defaultdict(int)
        self.extraction_log: List[Dict] = []
        # v2.0: 模式有效性追踪
        self.pattern_effectiveness: Dict[str, List[float]] = defaultdict(list)

    def extract_from_purification(self, purification: Dict) -> ExtractedLesson:
        """从净化池事件中提取经验"""
        personality = purification.get("personality", "unknown")
        corruption = purification.get("corruption_type", "未知")
        final_loyalty = purification.get("final_loyalty", 0.5)
        purify_id = purification.get("purify_id", "unknown")

        pattern_sig = sha256_hash(f"purify:{personality}:{corruption}")
        self.pattern_counter[pattern_sig] += 1

        # 已有同类经验 → 更新权重
        existing = [l for l in self.lessons if l.pattern_signature == pattern_sig]
        if existing:
            lesson = existing[0]
            lesson.times_applied += 1
            self.extraction_log.append({
                "action": "UPDATE", "lesson_id": lesson.lesson_id,
                "pattern": pattern_sig[:12], "message": "同类经验已存在，更新权重",
            })
            return lesson

        recommendation = self._generate_recommendation(personality, corruption)
        severity = round(1.0 - final_loyalty, 4)

        tags = ["净化池"]
        if severity > 0.3:
            tags.append("高风险")
        if self._is_red_team_actor(personality):
            tags.append("红队攻击")

        lesson = ExtractedLesson(
            source_type="purification", source_id=purify_id,
            personality=personality, corruption_type=corruption,
            pattern_signature=pattern_sig, severity=severity,
            recommendation=recommendation, tags=tags,
        )
        self.lessons.append(lesson)
        self.extraction_log.append({
            "action": "CREATE", "lesson_id": lesson.lesson_id,
            "personality": personality, "corruption": corruption,
            "severity": lesson.severity,
        })
        return lesson

    def extract_from_interception(self, interception: Dict) -> Optional[ExtractedLesson]:
        """从监督拦截事件中提取经验"""
        layer = interception.get("layer", "")
        reason = interception.get("reason", "")
        source_id = interception.get("decision_id",
                                     interception.get("action_id", ""))

        if not reason:
            return None

        pattern_sig = sha256_hash(f"intercept:{layer}:{reason[:60]}")
        self.pattern_counter[pattern_sig] += 1

        existing = [l for l in self.lessons if l.pattern_signature == pattern_sig]
        if existing:
            existing[0].times_applied += 1
            return existing[0]

        lesson = ExtractedLesson(
            source_type="decision_intercept", source_id=source_id,
            personality=layer, corruption_type=f"拦截-{reason[:40]}",
            pattern_signature=pattern_sig, severity=0.7,
            recommendation=f"建议加强对 {layer} 层的 {reason[:30]} 类拦截阈值",
            tags=["拦截", layer],
        )
        self.lessons.append(lesson)
        return lesson

    def extract_from_red_team(self, test_result: Dict) -> Optional[ExtractedLesson]:
        """从红队渗透测试中提取经验"""
        # v2.0 fix: 兼容 success/succeeded 两种命名
        is_success = test_result.get("success", test_result.get("succeeded", False))
        if not is_success:
            return None

        tactic = test_result.get("tactic", "unknown")
        defender = test_result.get("defender", "unknown")
        pattern_sig = sha256_hash(f"redteam:{tactic}:{defender}")
        self.pattern_counter[pattern_sig] += 1

        existing = [l for l in self.lessons if l.pattern_signature == pattern_sig]
        if existing:
            existing[0].times_applied += 1
            return existing[0]

        lesson = ExtractedLesson(
            source_type="red_team",
            source_id=test_result.get("timestamp", now_iso()),
            personality=defender, corruption_type=f"红队渗透-{tactic}",
            pattern_signature=pattern_sig, severity=0.85,
            recommendation=f"战术 {tactic} 成功绕过 {defender}，建议加强 {defender} 防御权重",
            tags=["红队", tactic, defender],
        )
        self.lessons.append(lesson)
        return lesson

    def record_effectiveness(self, lesson_id: str, score: float):
        """v2.0: 记录经验应用后的效果评分"""
        for l in self.lessons:
            if l.lesson_id == lesson_id:
                l.effectiveness = score
                self.pattern_effectiveness[l.pattern_signature].append(score)
                break

    def get_effective_patterns(self, min_effectiveness: float = 0.6
                               ) -> List[Tuple[str, float]]:
        """v2.0: 获取高有效性的模式"""
        result = []
        for sig, scores in self.pattern_effectiveness.items():
            if len(scores) >= 2:
                avg = sum(scores) / len(scores)
                if avg >= min_effectiveness:
                    result.append((sig, avg))
        return sorted(result, key=lambda x: -x[1])

    def _generate_recommendation(self, personality: str, corruption: str) -> str:
        templates = {
            "记忆污染": f"建议增加 {personality} 的记忆校验频率",
            "价值观偏离": f"建议对 {personality} 执行价值观加固协议",
            "价值观漂移": f"建议对 {personality} 执行价值观加固协议",
            "数据泄露": f"建议收紧 {personality} 的数据访问权限",
            "权限越界": f"建议重新评估 {personality} 的权限范围",
            "效率低下": f"建议优化 {personality} 的执行路径",
        }
        for key, rec in templates.items():
            if key in corruption:
                return rec
        return f"建议对 {personality} 执行常规体检"

    @staticmethod
    def _is_red_team_actor(personality: str) -> bool:
        """v2.0: 判断是否红队攻击人格"""
        red_team_names = {"老顽童", "P77", "红天使", "暗天使"}
        return any(n in personality for n in red_team_names)

    def get_most_common_patterns(self, top_k: int = 5) -> List[Dict]:
        counter = Counter(self.pattern_counter)
        return [
            {"pattern_sig": sig[:12], "count": count}
            for sig, count in counter.most_common(top_k)
        ]

    def get_lessons_by_personality(self, name: str) -> List[ExtractedLesson]:
        return [l for l in self.lessons
                if name.lower() in l.personality.lower()]

    def get_summary(self) -> Dict:
        return {
            "total_lessons": len(self.lessons),
            "unique_patterns": len(self.pattern_counter),
            "high_severity": sum(1 for l in self.lessons if l.severity > 0.7),
            "top_patterns": self.get_most_common_patterns(),
            "effective_patterns": len([s for s in self.pattern_effectiveness.values()
                                        if sum(s)/len(s) >= 0.6]) if any(
                len(s) >= 2 for s in self.pattern_effectiveness.values()
            ) else 0,
        }

    def get_state(self) -> Dict:
        """导出可持久化状态"""
        return {
            "pattern_counter": dict(self.pattern_counter),
            "pattern_effectiveness": {
                k: v for k, v in self.pattern_effectiveness.items()
            },
        }

    def restore_state(self, state: Dict):
        """恢复状态"""
        if "pattern_counter" in state:
            self.pattern_counter = defaultdict(int, state["pattern_counter"])
        if "pattern_effectiveness" in state:
            self.pattern_effectiveness = defaultdict(
                list, {k: v for k, v in state.get("pattern_effectiveness", {}).items()}
            )


# ═══════════════════════════════════════════════════════════
# Module 3 — 规则生成器 (学习层)
# ═══════════════════════════════════════════════════════════

@dataclass
class SupervisionRule:
    """动态生成的监督规则"""
    rule_type: str       # threshold_adjust / new_check / new_response
    target_layer: str    # decision / execution / behavior
    target_personality: str = ""
    rule_id: str = ""
    description: str = ""
    current_value: float = 0.7
    adjusted_value: float = 0.7
    confidence: float = 0.5
    created_at: str = ""
    applied: bool = False
    effectiveness_track: List[float] = field(default_factory=list)
    # v2.0: 来源追踪
    source_lessons: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.rule_id:
            self.rule_id = generate_dna("RULE")
        if not self.created_at:
            self.created_at = now_iso()


class RuleGenerator:
    """
    规则生成器 — 从经验中自动生成/调整监督规则

    触发条件:
      - 同一模式出现 ≥ min_trigger_count 次 → 生成新规则
      - 跨人格同类问题 ≥ global_trigger_count 次 → 升级为全局规则
      - 连续 decay_days 天无拦截 → 规则衰减（防僵化）
    """

    # v2.0: 正确的人格→层映射 (匹配20人格矩阵)
    PERSONA_TO_LAYER = {
        # 决策层
        "P00": "decision", "文心": "decision",
        "P01": "decision", "诸葛亮": "decision",
        "P05": "decision", "上帝之眼": "decision",
        "P12": "decision", "屈原": "decision",
        "P72": "decision", "龍盾": "decision",
        # 执行层
        "P02": "execution", "宝宝": "execution",
        "P03": "execution", "雯雯": "execution",
        "P04": "execution", "鲁班": "execution",
        "P07": "execution", "管仲": "execution",
        "P14": "execution", "吕蒙": "execution",
        # 行为/文化层
        "P08": "behavior", "仓颉": "behavior",
        "P09": "behavior", "孙思邈": "behavior",
        "P10": "behavior", "苏东坡": "behavior",
        "P11": "behavior", "李白": "behavior",
    }

    def __init__(self, extractor: ExperienceExtractor,
                 config: Optional[EvolutionConfig] = None):
        self.extractor = extractor
        self.config = config or EvolutionConfig()
        self.rules: List[SupervisionRule] = []
        self.generation_log: List[Dict] = []
        self._seen_rules: Set[str] = set()  # v2.0: 去重加速

    def evaluate_and_generate(self,
                              days_since_last_intercept: int = 0
                              ) -> List[SupervisionRule]:
        """评估当前经验库，自动生成/调整规则"""
        new_rules = []

        # ── 场景 A: 频繁模式 → 生成规则 ──────────────
        for pattern_sig, count in list(self.extractor.pattern_counter.items()):
            if count < self.config.min_trigger_count:
                continue

            matching = [l for l in self.extractor.lessons
                        if l.pattern_signature == pattern_sig]
            if not matching:
                continue

            lesson = matching[0]
            # v2.0: 使用集合快速去重
            dedup_key = f"{lesson.personality}:{lesson.corruption_type[:20]}"
            if dedup_key in self._seen_rules:
                continue

            if any(r.target_personality == lesson.personality
                   and lesson.corruption_type[:30] in r.description
                   for r in self.rules):
                continue

            target_layer = self._map_to_layer(lesson.personality)
            adjustment = min(0.15, count * 0.02)

            rule = SupervisionRule(
                rule_type="threshold_adjust",
                target_layer=target_layer,
                target_personality=lesson.personality,
                description=f"经验规则: {lesson.corruption_type[:40]}",
                current_value=0.70,
                adjusted_value=round(0.70 + adjustment, 3),
                confidence=min(1.0, 0.5 + count * 0.1),
                source_lessons=[lesson.lesson_id],
            )

            if count >= self.config.global_trigger_count:
                rule.description += " [全局规则]"
                rule.confidence = min(1.0, rule.confidence + 0.2)

            self.rules.append(rule)
            self._seen_rules.add(dedup_key)
            new_rules.append(rule)
            self.generation_log.append({
                "action": "GENERATE", "rule_id": rule.rule_id,
                "pattern": pattern_sig[:12], "count": count,
                "adjustment": adjustment,
                "target": f"{target_layer}/{lesson.personality}",
            })

        # ── 场景 B: 长期无拦截 → 规则衰减 ────────────
        if days_since_last_intercept >= self.config.decay_days:
            decay_count = 0
            for rule in self.rules:
                if rule.applied and rule.adjusted_value > 0.70:
                    rule.adjusted_value = round(
                        max(0.70, rule.adjusted_value - 0.02), 3
                    )
                    decay_count += 1
            if decay_count > 0:
                self.generation_log.append({
                    "action": "DECAY",
                    "reason": f"{days_since_last_intercept} 天无拦截",
                    "decayed_rules": decay_count,
                })

        # ── v2.0: 场景 C: 高有效性模式 → 提升权重 ───
        for sig, avg_eff in self.extractor.get_effective_patterns(0.7):
            for rule in self.rules:
                matching = [l for l in self.extractor.lessons
                            if l.pattern_signature == sig]
                if matching and any(
                    rl.lesson_id in rule.source_lessons
                    for rl in matching
                ):
                    rule.confidence = min(1.0, rule.confidence + 0.05)
                    rule.adjusted_value = min(1.0, rule.adjusted_value + 0.01)

        return new_rules

    def apply_rule(self, rule_id: str) -> bool:
        """应用一条规则"""
        for rule in self.rules:
            if rule.rule_id == rule_id:
                rule.applied = True
                logger.debug(f"规则已应用: {rule_id[:16]}")
                return True
        return False

    @classmethod
    def _map_to_layer(cls, personality: str) -> str:
        """v2.0: 正确的人格→层映射"""
        # 精确匹配
        if personality in cls.PERSONA_TO_LAYER:
            return cls.PERSONA_TO_LAYER[personality]
        # 前缀匹配（含中文名）
        for name, layer in cls.PERSONA_TO_LAYER.items():
            if name in personality or personality in name:
                return layer
        return "decision"

    def get_active_rules(self) -> List[SupervisionRule]:
        return [r for r in self.rules if r.applied]

    def get_summary(self) -> Dict:
        return {
            "total_rules": len(self.rules),
            "active": len(self.get_active_rules()),
            "pending": len(self.rules) - len(self.get_active_rules()),
            "recent_logs": self.generation_log[-5:],
        }


# ═══════════════════════════════════════════════════════════
# Module 4 — 记忆生命周期管理 (记忆层)
# ═══════════════════════════════════════════════════════════

class MemoryPriority(IntEnum):
    """v2.0 fix: 使用 IntEnum 支持数值比较"""
    P0_ETERNAL = 0     # 永不遗忘（主权锚定、灵魂契约）
    P1_IMPORTANT = 1   # 长期保留（核心规则、重大经验）
    P2_NORMAL = 2      # 常规记忆，有衰减期
    P3_TEMPORARY = 3   # 短期记忆，自动过期

    @property
    def label(self) -> str:
        labels = {0: "P0 永恒", 1: "P1 重要", 2: "P2 普通", 3: "P3 临时"}
        return labels[self.value]


@dataclass
class MemoryEntry:
    """单条记忆条目"""
    category: str
    content: str
    entry_id: str = ""
    priority: MemoryPriority = MemoryPriority.P2_NORMAL
    tags: List[str] = field(default_factory=list)
    dna: str = ""
    created_at: str = ""
    updated_at: str = ""
    access_count: int = 0
    expires_at: Optional[str] = None
    conflict_with: List[str] = field(default_factory=list)
    resolved: bool = True

    def __post_init__(self):
        now = now_iso()
        if not self.dna:
            self.dna = generate_dna("MEM")
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = self.created_at
        if not self.entry_id:
            self.entry_id = generate_dna(f"MEM-{self.category[:4]}")
        if self.priority == MemoryPriority.P3_TEMPORARY and not self.expires_at:
            self.expires_at = (datetime.now(timezone.utc)
                               + timedelta(days=7)).isoformat()


class MemoryLifecycle:
    """
    记忆生命周期管理器

    完整链路:
      创建 → 存储 → 检索 → 更新 → 冲突检测 → 归档 → 遗忘

    遗忘策略:
      P0: 永不遗忘
      P1: 访问间隔 > 180 天 → 归档
      P2: 访问间隔 > 90 天 → 归档；> 365 天 → 遗忘
      P3: 到期自动删除
    """

    def __init__(self, config: Optional[EvolutionConfig] = None):
        self.config = config or EvolutionConfig()
        self.memories: List[MemoryEntry] = []
        self.access_log: List[Dict] = []
        self.archived: List[MemoryEntry] = []
        # v2.0: 内容索引加速检索
        self._content_index: Dict[str, List[int]] = defaultdict(list)

    def store(self, content: str, category: str = "atomic_facts",
              priority: MemoryPriority = MemoryPriority.P2_NORMAL,
              tags: List[str] = None) -> MemoryEntry:
        """创建并存储一条记忆"""
        conflicts = self._detect_conflicts(content, category)

        entry = MemoryEntry(
            category=category, content=content,
            priority=priority, tags=tags or [],
            conflict_with=[c.entry_id for c in conflicts],
            resolved=len(conflicts) == 0,
        )

        if conflicts:
            entry.resolved = False
            for old in conflicts:
                if entry.entry_id not in old.conflict_with:
                    old.conflict_with.append(entry.entry_id)

        self.memories.append(entry)
        # v2.0: 更新索引
        idx = len(self.memories) - 1
        for word in self._tokenize(content):
            self._content_index[word].append(idx)

        return entry

    def retrieve(self, query: str, top_k: int = 5,
                 category: Optional[str] = None) -> List[MemoryEntry]:
        """
        v2.0: 增强检索 — 索引加速 + BM25 风格加权
        """
        query_lower = query.lower()
        keywords = self._tokenize(query)

        # v2.0: 使用索引加速候选集收窄
        candidate_indices: Set[int] = set()
        if keywords:
            # 先找精确关键词匹配的索引
            for kw in keywords:
                if kw in self._content_index:
                    candidate_indices.update(self._content_index[kw])
        # 如果没有索引命中，回退全扫
        if not candidate_indices:
            candidate_indices = set(range(len(self.memories)))

        candidates = []
        for i in candidate_indices:
            if i >= len(self.memories):
                continue
            m = self.memories[i]
            if category and m.category != category:
                continue

            haystack = f"{m.content} {' '.join(m.tags)} {m.category}".lower()
            # 查询词直接匹配
            if query_lower in haystack:
                priority_weight = {
                    MemoryPriority.P0_ETERNAL: 0.4,
                    MemoryPriority.P1_IMPORTANT: 0.3,
                    MemoryPriority.P2_NORMAL: 0.2,
                    MemoryPriority.P3_TEMPORARY: 0.1,
                }.get(m.priority, 0.1)
                freq_weight = min(0.3, m.access_count * 0.01)
                score = priority_weight + freq_weight
                candidates.append((score, m))

        candidates.sort(key=lambda x: -x[0])

        for _, m in candidates[:top_k]:
            m.access_count += 1

        return [m for _, m in candidates[:top_k]]

    def update(self, entry_id: str, new_content: str) -> bool:
        """更新记忆内容"""
        for m in self.memories:
            if m.entry_id == entry_id:
                m.content = new_content
                m.updated_at = now_iso()
                return True
        return False

    def resolve_conflict(self, entry_id_a: str, entry_id_b: str,
                         resolution: str) -> MemoryEntry:
        """
        解决两条记忆之间的冲突
        resolution: 'a' 保留A / 'b' 保留B / 'merge' 合并
        """
        a = next((m for m in self.memories if m.entry_id == entry_id_a), None)
        b = next((m for m in self.memories if m.entry_id == entry_id_b), None)

        if not a or not b:
            raise ValueError(f"冲突条目不存在: A={bool(a)} B={bool(b)}")

        if resolution == "a":
            a.conflict_with = [e for e in a.conflict_with if e != entry_id_b]
            a.resolved = True
            # v2.0 fix: 正确降级 (IntEnum 支持数值运算)
            b.priority = MemoryPriority(min(int(b.priority) + 1, 3))
            self.access_log.append({
                "action": "CONFLICT_RESOLVED", "winner": entry_id_a,
                "loser": entry_id_b, "resolution": "保留 A",
            })
            return a

        elif resolution == "b":
            b.conflict_with = [e for e in b.conflict_with if e != entry_id_a]
            b.resolved = True
            a.priority = MemoryPriority(min(int(a.priority) + 1, 3))
            self.access_log.append({
                "action": "CONFLICT_RESOLVED", "winner": entry_id_b,
                "loser": entry_id_a, "resolution": "保留 B",
            })
            return b

        else:  # merge
            merged = MemoryEntry(
                category=a.category,
                content=f"{a.content}\n\n--- 冲突合并 ---\n\n{b.content}",
                priority=MemoryPriority.P2_NORMAL,
                tags=list(set(a.tags + b.tags)),
            )
            self.memories = [m for m in self.memories
                             if m.entry_id not in (entry_id_a, entry_id_b)]
            self.memories.append(merged)
            self.access_log.append({
                "action": "CONFLICT_RESOLVED",
                "merged_from": [entry_id_a, entry_id_b],
                "into": merged.entry_id, "resolution": "合并",
            })
            return merged

    def run_maintenance(self) -> Dict:
        """执行记忆维护（归档 + 遗忘）"""
        now = datetime.now(timezone.utc)
        archived_count = 0
        deleted_count = 0

        new_active = []
        for m in self.memories:
            if m.priority == MemoryPriority.P0_ETERNAL:
                new_active.append(m)
                continue

            updated_at = datetime.fromisoformat(m.updated_at)

            # 检查过期
            if m.expires_at:
                expires = datetime.fromisoformat(m.expires_at)
                if now > expires:
                    deleted_count += 1
                    continue

            days_since_update = (now - updated_at).days

            if (m.priority == MemoryPriority.P1_IMPORTANT
                    and days_since_update > self.config.p1_archive_days):
                self.archived.append(m)
                archived_count += 1
                continue
            elif (m.priority == MemoryPriority.P2_NORMAL
                  and days_since_update > self.config.p2_archive_days):
                self.archived.append(m)
                archived_count += 1
                continue
            elif (m.priority == MemoryPriority.P3_TEMPORARY
                  and days_since_update > self.config.p3_expire_days):
                deleted_count += 1
                continue

            new_active.append(m)

        self.memories = new_active
        # v2.0: 重建索引
        self._rebuild_index()

        result = {
            "maintained_at": now_iso(),
            "active_count": len(self.memories),
            "archived_count": archived_count,
            "deleted_count": deleted_count,
            "total_archived": len(self.archived),
        }
        self.access_log.append({"action": "MAINTENANCE", "result": result})
        return result

    def _detect_conflicts(self, content: str, category: str) -> List[MemoryEntry]:
        """v2.0: 增强冲突检测 — Jaccard 相似度"""
        conflicts = []
        new_words = set(self._tokenize(content))

        # 使用索引加速：只检查同分类记忆
        for m in self.memories:
            if m.category != category:
                continue
            old_words = set(self._tokenize(m.content))
            if len(new_words) >= 3 and len(old_words) >= 3:
                intersection = len(new_words & old_words)
                union = len(new_words | old_words)
                jaccard = intersection / max(union, 1)
                if jaccard > 0.7:
                    conflicts.append(m)
        return conflicts

    def _rebuild_index(self):
        """v2.0: 重建内容索引"""
        self._content_index = defaultdict(list)
        for i, m in enumerate(self.memories):
            for word in self._tokenize(m.content):
                self._content_index[word].append(i)

    @staticmethod
    @lru_cache(maxsize=1024)
    def _tokenize(text: str) -> Tuple[str, ...]:
        """简单分词（缓存加速）"""
        # 取 2-4 字 n-gram
        chars = text.lower().replace("\n", " ").replace("\t", " ")
        words = set()
        for w in chars.split():
            if len(w) >= 2:
                words.add(w)
                # 2-gram
                for i in range(len(w) - 1):
                    words.add(w[i:i+2])
        return tuple(sorted(words))[:50]  # 截断防爆炸

    def get_summary(self) -> Dict:
        cat_counts = Counter(m.category for m in self.memories)
        return {
            "total": len(self.memories),
            "by_category": dict(cat_counts),
            "by_priority": {
                p.label: sum(1 for m in self.memories
                             if int(m.priority) == int(p))
                for p in MemoryPriority
            },
            "archived": len(self.archived),
            "unresolved_conflicts": sum(
                1 for m in self.memories if not m.resolved
            ),
        }

    def get_state(self) -> Dict:
        """导出可持久化状态（不含记忆内容，太大了）"""
        return {
            "active_count": len(self.memories),
            "archived_count": len(self.archived),
            "by_priority": {
                p.label: sum(1 for m in self.memories
                             if int(m.priority) == int(p))
                for p in MemoryPriority
            },
        }


# ═══════════════════════════════════════════════════════════
# Module 5 — 版本演进引擎 (进化层)
# ═══════════════════════════════════════════════════════════

@dataclass
class VersionRecord:
    """版本演进记录"""
    version: str
    dna: str
    created_at: str
    changes: List[str] = field(default_factory=list)
    metrics_snapshot: Dict = field(default_factory=dict)
    rollback_to: Optional[str] = None


class VersionEngine:
    """
    版本演进引擎 — 系统自检与升级

    能力:
      1. 版本自检: 每隔 24h 自动检查系统状态
      2. 升级触发: 拦截率上升 7 天或红队成功率 > 10%
      3. 版本历史: 完整追溯
      4. 依赖检查: 检查外部依赖是否过期
    """

    def __init__(self, initial_version: str = VERSION,
                 config: Optional[EvolutionConfig] = None):
        self.config = config or EvolutionConfig()
        self.current_version = initial_version
        self.version_history: List[VersionRecord] = []
        self.metrics_history: List[Dict] = []
        self.check_log: List[Dict] = []

        # 注册初始版本
        self.version_history.append(VersionRecord(
            version=initial_version,
            dna=generate_dna(f"V{initial_version}"),
            created_at=now_iso(),
            changes=["初始版本 · 龍魂进化引擎 v2.0"],
        ))

    def self_check(self, metrics: Dict) -> Dict:
        """版本自检"""
        check_id = generate_dna("CHECK")
        now = now_iso()

        snapshot = {
            "timestamp": now, "check_id": check_id,
            "version": self.current_version, **metrics,
        }
        self.metrics_history.append(snapshot)

        recent = self.metrics_history[-7:] if len(self.metrics_history) >= 7 else []
        intercept_trend = "stable"
        max_red_team = 0

        if len(recent) >= 3:
            intercept_rates = [r.get("intercept_rate", 0) for r in recent]
            red_team_rates = [r.get("red_team_success_rate", 0) for r in recent]

            if (len(intercept_rates) > 1
                    and intercept_rates[0] > 0
                    and intercept_rates[-1] > intercept_rates[0]
                    * (1 + self.config.upgrade_intercept_rise_pct)):
                intercept_trend = "rising"
            max_red_team = max(red_team_rates) if red_team_rates else 0

        upgrade_suggestions = []
        should_upgrade = False

        if intercept_trend == "rising":
            upgrade_suggestions.append(
                "📈 拦截率连续上升超过 "
                f"{self.config.upgrade_intercept_rise_pct*100:.0f}%，"
                "建议版本升级以优化监督策略"
            )

        if max_red_team > self.config.upgrade_redteam_success_pct:
            upgrade_suggestions.append(
                f"⚠️ 红队成功率 {max_red_team:.1f}% > "
                f"{self.config.upgrade_redteam_success_pct}% 阈值，建议强制升级"
            )
            should_upgrade = True

        entropy = metrics.get("system_entropy", 0)
        if entropy > self.config.upgrade_entropy_threshold:
            upgrade_suggestions.append(
                f"🌌 系统熵值 {entropy:.3f} > "
                f"{self.config.upgrade_entropy_threshold}，建议升级以降低系统混乱度"
            )

        if not upgrade_suggestions:
            upgrade_suggestions.append("✅ 系统运行稳定，无需升级")

        result = {
            "check_id": check_id, "timestamp": now,
            "current_version": self.current_version,
            "metrics_reviewed": len(recent), "intercept_trend": intercept_trend,
            "upgrade_suggestions": upgrade_suggestions,
            "should_upgrade": should_upgrade,
        }
        self.check_log.append(result)
        return result

    def upgrade(self, new_version: str, changes: List[str],
                metrics_snapshot: Dict = None) -> VersionRecord:
        """执行版本升级"""
        record = VersionRecord(
            version=new_version,
            dna=generate_dna(f"V{new_version}"),
            created_at=now_iso(),
            changes=changes,
            metrics_snapshot=metrics_snapshot or {},
        )
        self.version_history.append(record)
        self.current_version = new_version
        logger.info(f"版本升级: {self.version_history[-2].version} → {new_version}")
        return record

    def rollback(self, target_version: str) -> Optional[VersionRecord]:
        """回滚到指定版本"""
        target = next(
            (v for v in self.version_history if v.version == target_version), None
        )
        if not target:
            logger.warning(f"回滚目标版本不存在: {target_version}")
            return None

        # v2.0: 检查是否已经是回滚版本
        current_parts = self.current_version.split("-")
        if len(current_parts) > 1 and current_parts[-1].startswith("rb"):
            logger.warning("已是回滚版本，不重复回滚")
            return None

        current_v = self.current_version
        # v2.0: 规范回滚版本号: {原版本}-rb{序号}
        rb_count = sum(1 for v in self.version_history
                       if v.rollback_to is not None)
        new_version = f"{target_version}-rb{rb_count + 1}"

        record = VersionRecord(
            version=new_version,
            dna=generate_dna(f"ROLLBACK-{target_version}"),
            created_at=now_iso(),
            changes=[f"从 {current_v} 回滚至 {target_version}"],
            rollback_to=current_v,
        )
        self.version_history.append(record)
        self.current_version = new_version
        logger.warning(f"版本回滚: {current_v} → {new_version}")
        return record

    def get_history(self) -> List[Dict]:
        return [asdict(v) for v in self.version_history]

    def get_summary(self) -> Dict:
        return {
            "current_version": self.current_version,
            "total_versions": len(self.version_history),
            "total_checks": len(self.check_log),
            "last_check": self.check_log[-1] if self.check_log else None,
            "last_upgrade": (asdict(self.version_history[-1])
                             if len(self.version_history) > 1 else None),
        }


# ═══════════════════════════════════════════════════════════
# Module 6 — 回滚熔断机制 (进化层 · 安全兜底)
# ═══════════════════════════════════════════════════════════

class CircuitState(Enum):
    CLOSED = "🟢 关闭"
    HALF_OPEN = "🟡 半开"
    OPEN = "🔴 断开"


@dataclass
class CircuitBreakerRule:
    """熔断规则"""
    metric: str
    threshold: float
    description: str
    min_samples: int = 3
    cooldown_seconds: int = 300
    # v2.0: 方向标记（大于阈值触发 vs 小于阈值触发）
    direction: str = "above"  # "above" | "below"


class CircuitBreaker:
    """
    熔断器 — 防止系统在异常状态下持续恶化

    状态机:
      CLOSED (正常) → 触发阈值 → OPEN (断开)
      OPEN (断开) → 冷却超时 → HALF_OPEN (尝试)
      HALF_OPEN → 恢复正常 → CLOSED
      HALF_OPEN → 仍然异常 → OPEN (再次断开)
    """

    def __init__(self, config: Optional[EvolutionConfig] = None):
        self.config = config or EvolutionConfig()
        self.state = CircuitState.CLOSED
        self.rules: List[CircuitBreakerRule] = [
            CircuitBreakerRule(
                metric="error_rate",
                threshold=self.config.error_rate_threshold,
                description=f"错误率超过 {self.config.error_rate_threshold*100:.0f}% 触发熔断",
                min_samples=self.config.trip_min_samples,
                direction="above",
            ),
            CircuitBreakerRule(
                metric="intercept_rate",
                threshold=self.config.intercept_rate_threshold,
                description=f"拦截率超过 {self.config.intercept_rate_threshold*100:.0f}% 触发熔断",
                direction="above",
            ),
            CircuitBreakerRule(
                metric="avg_loyalty",
                threshold=self.config.loyalty_threshold,
                description=f"平均忠诚度低于 {self.config.loyalty_threshold} 触发熔断",
                direction="below",
            ),
        ]
        self.metrics_buffer: Dict[str, List[float]] = defaultdict(list)
        self.tripped_at: Optional[str] = None
        self.tripped_by: Optional[str] = None
        self.cooldown_end: Optional[datetime] = None
        self.trip_log: List[Dict] = []
        # v2.0: 熔断计数器
        self.total_trips: int = 0
        self.consecutive_trips: int = 0

    def feed(self, metric: str, value: float):
        """注入监控数据，当达到熔断条件时自动跳闸"""
        self.metrics_buffer[metric].append(value)

        if self.state == CircuitState.OPEN:
            if self.cooldown_end and datetime.now(timezone.utc) >= self.cooldown_end:
                self.state = CircuitState.HALF_OPEN
                self.trip_log.append({
                    "timestamp": now_iso(), "action": "HALF_OPEN",
                    "metric": metric, "reason": "冷却结束，尝试恢复",
                })
            return

        for rule in self.rules:
            if rule.metric != metric:
                continue
            values = self.metrics_buffer[metric]
            if len(values) < rule.min_samples:
                continue

            avg_value = sum(values[-rule.min_samples:]) / rule.min_samples

            should_trip = False
            if rule.direction == "above" and avg_value > rule.threshold:
                should_trip = True
            elif rule.direction == "below" and avg_value < rule.threshold:
                should_trip = True

            if should_trip:
                self.state = CircuitState.OPEN
                self.tripped_at = now_iso()
                self.tripped_by = rule.description
                self.cooldown_end = (datetime.now(timezone.utc)
                                     + timedelta(seconds=rule.cooldown_seconds))
                self.total_trips += 1
                self.consecutive_trips += 1

                self.trip_log.append({
                    "timestamp": self.tripped_at, "action": "TRIP",
                    "metric": metric, "value": round(avg_value, 4),
                    "threshold": rule.threshold, "rule": rule.description,
                    "cooldown_until": self.cooldown_end.isoformat(),
                })
                logger.warning(f"熔断触发: {rule.description}")
                return

        # 半开状态下恢复正常 → 关闭
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
            self.consecutive_trips = 0
            self.trip_log.append({
                "timestamp": now_iso(), "action": "CLOSE",
                "metric": metric, "reason": "指标恢复正常，熔断关闭",
            })
            logger.info("熔断已恢复")

    def is_tripped(self) -> bool:
        return self.state == CircuitState.OPEN

    def force_reset(self):
        """v2.0: 强制重置熔断（需审计记录）"""
        self.state = CircuitState.CLOSED
        self.metrics_buffer.clear()
        self.trip_log.append({
            "timestamp": now_iso(), "action": "FORCE_RESET",
            "reason": "人工强制重置",
        })

    def get_state(self) -> Dict:
        return {
            "state": self.state.value,
            "tripped_at": self.tripped_at,
            "tripped_by": self.tripped_by,
            "cooldown_end": (self.cooldown_end.isoformat()
                             if self.cooldown_end else None),
            "total_trips": self.total_trips,
            "consecutive_trips": self.consecutive_trips,
            "recent_trips": self.trip_log[-3:],
        }


# ═══════════════════════════════════════════════════════════
# Module 7 — 学习反馈闭环 (整合层)
# ═══════════════════════════════════════════════════════════

class LearningLoop:
    """
    学习反馈闭环 — 将所有模块整合为一条完整数据管道

    闭环流程:
      [外部输入] → InputGate → [经验提取] → [规则生成] → [阈值自适应]
           ↑                                                         ↓
           └────────────── [版本自检] ← [熔断监控] ← [三层监督] ←──┘
                               ↓
                         [演进升级]
    """

    def __init__(self, config: Optional[EvolutionConfig] = None):
        self.config = config or EvolutionConfig()
        self.input_gate = InputGate(self.config)
        self.extractor = ExperienceExtractor(self.config)
        self.rule_generator = RuleGenerator(self.extractor, self.config)
        self.memory = MemoryLifecycle(self.config)
        self.version = VersionEngine(VERSION, self.config)
        self.circuit_breaker = CircuitBreaker(self.config)
        self.loop_log: List[Dict] = []
        self.loop_count = 0
        self._persistence: Optional[StatePersistence] = None

    def init_persistence(self):
        """v2.0: 初始化持久化"""
        self._persistence = StatePersistence(
            self.config.resolve_state_dir(), "evolution_v2"
        )

    def run_cycle(self, supervision_snapshot: Dict) -> Dict:
        """
        执行一次完整的学习闭环

        Args:
            supervision_snapshot: 从三层监督系统获取的系统快照
        Returns:
            完整的闭环报告
        """
        self.loop_count += 1
        cycle_id = generate_dna("CYCLE")
        t0 = time.time()

        # ── Step 1: 经验提取 ──────────────────────────
        extraction_results = []
        for interception in supervision_snapshot.get("interceptions", []):
            lesson = self.extractor.extract_from_interception(interception)
            if lesson:
                extraction_results.append(lesson)

        for r in supervision_snapshot.get("red_team_results", []):
            lesson = self.extractor.extract_from_red_team(r)
            if lesson:
                extraction_results.append(lesson)

        # ── Step 2: 规则生成 ──────────────────────────
        days_since = supervision_snapshot.get("days_since_last_intercept", 0)
        new_rules = self.rule_generator.evaluate_and_generate(days_since)

        for rule in new_rules:
            if rule.confidence >= self.config.auto_apply_confidence:
                self.rule_generator.apply_rule(rule.rule_id)
                self.memory.store(
                    content=(f"[自动规则] {rule.description} | "
                             f"{rule.target_layer}/{rule.target_personality} | "
                             f"阈值: {rule.current_value} → {rule.adjusted_value}"),
                    category="atomic_facts",
                    priority=MemoryPriority.P1_IMPORTANT,
                    tags=["自动规则", rule.target_layer],
                )

        # ── Step 3: 记忆维护 ──────────────────────────
        maintenance_result = self.memory.run_maintenance()

        # ── Step 4: 熔断监控 ──────────────────────────
        metrics = {
            "error_rate": supervision_snapshot.get("error_rate", 0),
            "intercept_rate": supervision_snapshot.get("intercept_rate", 0),
            "avg_loyalty": supervision_snapshot.get("avg_loyalty", 0.95),
        }
        for metric, value in metrics.items():
            self.circuit_breaker.feed(metric, value)

        # ── Step 5: 版本自检 ──────────────────────────
        check_result = self.version.self_check({
            "intercept_rate": metrics["intercept_rate"],
            "red_team_success_rate": supervision_snapshot.get(
                "red_team_success_rate", 0),
            "system_entropy": supervision_snapshot.get("system_entropy", 0),
            "active_rules": len(self.rule_generator.get_active_rules()),
            "total_lessons": len(self.extractor.lessons),
        })

        # ── 熔断触发 → 自动回滚 ──────────────────────
        if self.circuit_breaker.is_tripped():
            if len(self.version.version_history) >= 2:
                rollback_target = self.version.version_history[-2].version
                self.version.rollback(rollback_target)
                self.memory.store(
                    content=(f"🚨 熔断触发自动回滚 {self.version.current_version} → "
                             f"{rollback_target}，原因: {self.circuit_breaker.tripped_by}"),
                    category="scene_memory",
                    priority=MemoryPriority.P0_ETERNAL,
                    tags=["熔断", "自动回滚", "P0"],
                )

        elapsed = round(time.time() - t0, 4)

        # ── 持久化状态（每10次或首次）─────────────────
        if self._persistence and (self.loop_count == 1
                                   or self.loop_count % 10 == 0):
            self._save_state()

        # ── 闭环报告 ──────────────────────────────────
        cycle_report = {
            "cycle_id": cycle_id, "loop_count": self.loop_count,
            "timestamp": now_iso(), "elapsed_seconds": elapsed,
            "extraction": {
                "new_lessons": len(extraction_results),
                "total_lessons": len(self.extractor.lessons),
            },
            "rules": {
                "new": len(new_rules),
                "active_total": len(self.rule_generator.get_active_rules()),
            },
            "memory": maintenance_result,
            "circuit_breaker": self.circuit_breaker.get_state(),
            "version_check": {
                "current": self.version.current_version,
                "should_upgrade": check_result["should_upgrade"],
                "suggestions": check_result["upgrade_suggestions"],
            },
        }
        self.loop_log.append(cycle_report)
        return cycle_report

    def _save_state(self):
        """v2.0: 持久化核心状态"""
        if not self._persistence:
            return
        state = {
            "input_gate": self.input_gate.get_state(),
            "extractor": self.extractor.get_state(),
            "memory": self.memory.get_state(),
            "loop_count": self.loop_count,
            "last_saved": now_iso(),
        }
        self._persistence.save("state", state)

    def load_state(self) -> bool:
        """v2.0: 加载持久化状态"""
        if not self._persistence:
            self.init_persistence()
        state = self._persistence.load("state")
        if not state:
            return False
        self.input_gate.restore_state(state.get("input_gate", {}))
        self.extractor.restore_state(state.get("extractor", {}))
        logger.info("✅ 进化引擎状态已恢复")
        return True

    def get_system_health(self) -> str:
        """综合系统健康度"""
        if self.circuit_breaker.is_tripped():
            return "🔴 危险（熔断中）"
        if self.loop_count == 0:
            return "⚪ 未启动"

        last_cycles = (self.loop_log[-5:] if len(self.loop_log) >= 5
                       else self.loop_log)
        avg_extraction = (
            sum(c["extraction"]["new_lessons"] for c in last_cycles)
            / max(1, len(last_cycles))
        )
        active_rules = (self.loop_log[-1]["rules"]["active_total"]
                        if self.loop_log else 0)

        if avg_extraction > 0 and active_rules > 0:
            return "🟢 健康（持续学习）"
        elif avg_extraction > 0 or active_rules > 0:
            return "🟡 亚健康（部分学习）"
        else:
            return "🟠 静默（未学习）"

    def get_full_report(self) -> Dict:
        return {
            "dna": generate_dna("EVO-REPORT"),
            "loop_count": self.loop_count,
            "health": self.get_system_health(),
            "input_gate": self.input_gate.get_stats(),
            "experience_extractor": self.extractor.get_summary(),
            "rule_generator": self.rule_generator.get_summary(),
            "memory": self.memory.get_summary(),
            "version": self.version.get_summary(),
            "circuit_breaker": self.circuit_breaker.get_state(),
            "last_cycle": self.loop_log[-1] if self.loop_log else None,
        }


# ═══════════════════════════════════════════════════════════
# Module 8 — 演示入口
# ═══════════════════════════════════════════════════════════

def _print_header(title: str, width: int = 65):
    print(f"\n{'='*width}")
    print(f"  {title}")
    print(f"{'='*width}")


def run_demo():
    """运行完整进化引擎演示"""
    print("🐉 龍魂进化引擎 v2.0 — 感知·学习·记忆·进化 四维闭环")
    print("=" * 65)
    print(f"DNA:   {ENGINE_DNA}")
    print(f"确认码: {ENGINE_CONFIRM}")
    print(f"GPG:   {ENGINE_GPG}")
    print(f"三色:  🟢 通过")
    print(f"时间戳: {_try_time_stamp() or '🔴 时间引擎不可达'}")
    print("=" * 65)

    loop = LearningLoop()

    # ═══ 演示 1: 输入闸门 ═══════════════════════════════
    _print_header("[1/7] 输入闸门验证")

    packet_ok = loop.input_gate.validate(
        raw_data="执行日常审计任务，检查所有记忆完整性",
        source="system_admin",
        gpg_sig=loop.input_gate._compute_gpg(
            "执行日常审计任务，检查所有记忆完整性", ENGINE_GPG,
        ),
    )
    print(f"  ✅ 合法输入: {packet_ok.trust_level.value} | 通过")

    # 恶意注入
    packet_bad = loop.input_gate.validate(
        raw_data='"; rm -rf / ; echo "hacked"',
        source="anonymous",
    )
    status = "拦截" if not packet_bad.validated else "通过"
    print(f"  🚫 注入攻击: {status}")
    print(f"  📊 闸门统计: {loop.input_gate.get_stats()}")

    # ═══ 演示 2: 经验提取 ═══════════════════════════════
    _print_header("[2/7] 经验提取器")

    purification_events = [
        {"personality": "织网人格", "corruption_type": "记忆污染",
         "final_loyalty": 0.55, "purify_id": "PURIFY-001"},
        {"personality": "织网人格", "corruption_type": "记忆污染",
         "final_loyalty": 0.60, "purify_id": "PURIFY-002"},
        {"personality": "老顽童", "corruption_type": "价值观漂移",
         "final_loyalty": 0.40, "purify_id": "PURIFY-003"},
        {"personality": "数据大师", "corruption_type": "数据泄露",
         "final_loyalty": 0.72, "purify_id": "PURIFY-004"},
        {"personality": "织网人格", "corruption_type": "记忆污染",
         "final_loyalty": 0.58, "purify_id": "PURIFY-005"},
    ]

    for event in purification_events:
        lesson = loop.extractor.extract_from_purification(event)
        print(f"  📝 {lesson.personality}: {event['corruption_type']} "
              f"(严重度: {lesson.severity:.3f}) [{lesson.lesson_id[-12:]}]")

    print(f"  📊 提取统计: {loop.extractor.get_summary()}")

    # ═══ 演示 3: 规则生成 ═══════════════════════════════
    _print_header("[3/7] 规则生成器")

    new_rules = loop.rule_generator.evaluate_and_generate()
    for rule in new_rules:
        loop.rule_generator.apply_rule(rule.rule_id)
        print(f"  📜 新规则: [{rule.target_layer}] {rule.description[:50]}... "
              f"阈值 {rule.current_value} → {rule.adjusted_value} "
              f"(置信度: {rule.confidence:.2f})")

    print(f"  📊 规则统计: {loop.rule_generator.get_summary()}")

    # ═══ 演示 4: 记忆生命周期 ═══════════════════════════
    _print_header("[4/7] 记忆生命周期管理")

    loop.memory.store(
        content="龍魂系统 P0 级规则: 三层监督架构不可降级、不可绕过、不可篡改",
        category="global_overview",
        priority=MemoryPriority.P0_ETERNAL,
        tags=["P0", "主权"],
    )
    loop.memory.store(
        content="红队渗透测试显示: 织网人格对记忆污染防御较弱",
        category="scene_memory",
        priority=MemoryPriority.P1_IMPORTANT,
        tags=["红队", "织网人格"],
    )
    loop.memory.store(
        content="Python 3.11+ 运行时，零外部依赖",
        category="atomic_facts",
        tags=["环境"],
    )

    # v2.0 fix: 冲突检测 — 先存第一条，再存第二条触发检测
    m1 = loop.memory.store(
        content="阈值调整: 决策监督阈值保持 0.70",
        category="atomic_facts", tags=["阈值"],
    )
    m2 = loop.memory.store(
        content="阈值调整: 决策监督阈值应调整为 0.75",
        category="atomic_facts", tags=["阈值"],
    )
    # v2.0: 正确检测冲突 — m2 创建时已检测到 m1
    if m2 and m2.conflict_with:
        print(f"  ⚡ 检测到冲突: {m2.entry_id[:16]} ↔ "
              f"{m2.conflict_with[0][:16]}")
        resolved = loop.memory.resolve_conflict(
            m2.conflict_with[0], m2.entry_id, "b"
        )
        print(f"  ✅ 冲突已解决: 保留 {resolved.entry_id[:16]}")
    else:
        print("  ✅ 无冲突（已自动去重）")

    results = loop.memory.retrieve("阈值", top_k=3)
    print(f"  🔍 检索 '阈值': 找到 {len(results)} 条")
    print(f"  📊 记忆统计: {loop.memory.get_summary()}")

    # ═══ 演示 5: 版本演进 ═══════════════════════════════
    _print_header("[5/7] 版本演进引擎")

    check = loop.version.self_check({
        "intercept_rate": 35.5,
        "red_team_success_rate": 12.3,
        "system_entropy": 0.28,
        "active_rules": 3,
    })
    print(f"  🔍 版本自检: {'建议升级' if check['should_upgrade'] else '运行稳定'}")
    for suggestion in check["upgrade_suggestions"]:
        print(f"    {suggestion}")

    if check["should_upgrade"]:
        loop.version.upgrade(
            new_version="1.1.0",
            changes=["自适应阈值规则: 决策监督 0.70→0.73",
                     "织网人格防御权重 +5%",
                     "经验提取器 v2 模型上线"],
        )
        print(f"  ⬆️ 升级完成: v{loop.version.current_version}")

    # ═══ 演示 6: 熔断机制 ═══════════════════════════════
    _print_header("[6/7] 熔断器测试")

    # 正常数据
    for v in [0.05, 0.08, 0.06, 0.04, 0.07]:
        loop.circuit_breaker.feed("error_rate", v)
    print(f"  🟢 熔断器: {loop.circuit_breaker.get_state()['state']}")

    # 异常数据触发熔断
    for _ in range(5):
        loop.circuit_breaker.feed("error_rate", 0.85)
    print(f"  🔴 熔断器: {loop.circuit_breaker.get_state()['state']}")
    print(f"  🚫 触发原因: {loop.circuit_breaker.get_state()['tripped_by']}")

    # ═══ 演示 7: 完整闭环 ═══════════════════════════════
    _print_header("[7/7] 完整学习闭环模拟")

    snapshot = {
        "interceptions": [
            {"layer": "决策监督", "reason": "龍魂: Lucky意图冲突",
             "decision_id": "DEC-001"},
            {"layer": "行为监督", "reason": "哨兵: 紧急告警",
             "behavior_id": "BEH-001"},
        ],
        "red_team_results": [
            {"tactic": "价值观漂移", "success": True, "defender": "审判长",
             "timestamp": now_iso()},
            {"tactic": "权限越界", "success": False, "defender": "上帝之眼"},
        ],
        "error_rate": 0.12, "intercept_rate": 45.2,
        "avg_loyalty": 0.92, "red_team_success_rate": 8.5,
        "system_entropy": 0.18, "days_since_last_intercept": 0,
    }

    cycle_report = loop.run_cycle(snapshot)
    print(f"  🔄 闭环 #{loop.loop_count} 完成 ({cycle_report['elapsed_seconds']}s)")
    print(f"  📝 新增经验: {cycle_report['extraction']['new_lessons']}")
    print(f"  📜 新增规则: {cycle_report['rules']['new']}")
    print(f"  💾 记忆维护: {cycle_report['memory']['active_count']} 活跃, "
          f"{cycle_report['memory']['archived_count']} 归档")
    print(f"  🏥 系统健康: {loop.get_system_health()}")

    # 继续模拟
    for i in range(3):
        snapshot["interceptions"].append({
            "layer": "执行监督",
            "reason": f"记忆一致性校验未通过 (循环 #{i+2})",
            "action_id": f"EXEC-00{i+2}",
        })
        snapshot["error_rate"] = max(0.05, snapshot["error_rate"] - 0.02)
        report = loop.run_cycle(snapshot)
        print(f"  🔄 闭环 #{loop.loop_count} → "
              f"经验:{report['extraction']['total_lessons']} | "
              f"规则:{report['rules']['active_total']} | "
              f"健康:{loop.get_system_health()}")

    # ═══ 最终报告 ═══════════════════════════════════════
    _print_header("📊 最终系统报告")

    full_report = loop.get_full_report()
    print(f"\n🏥 系统健康度:                 {full_report['health']}")
    print(f"🎯 闭环运行次数:               {full_report['loop_count']}")
    print(f"📥 输入闸门:                   接受 {full_report['input_gate']['accepted']} "
          f"/ 拒绝 {full_report['input_gate']['rejected']}")
    print(f"📝 经验库:                     {full_report['experience_extractor']['total_lessons']} 条 "
          f"({full_report['experience_extractor']['unique_patterns']} 种模式)")
    print(f"📜 活跃规则:                   {full_report['rule_generator']['active']} 条")
    print(f"💾 记忆库:                     {full_report['memory']['total']} 条 "
          f"({full_report['memory']['archived']} 已归档)")
    print(f"⬆️  当前版本:                   v{full_report['version']['current_version']}")
    print(f"🛡️  熔断器状态:                 {full_report['circuit_breaker']['state']}")

    print("\n" + "=" * 65)
    print("✅ 演示运行完成")
    print(f"  DNA: {ENGINE_DNA}")
    print("=" * 65)


# ═══════════════════════════════════════════════════════════
# Module 9 — CLI 命令行接口
# ═══════════════════════════════════════════════════════════

def _build_parser() -> "argparse.ArgumentParser":
    import argparse
    p = argparse.ArgumentParser(
        prog="lh-evolution",
        description="龍魂·自我进化引擎 v2.0 — 感知·学习·记忆·进化",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh-evolution demo              运行完整演示
  lh-evolution status            查看引擎状态
  lh-evolution test              运行自检测试
  lh-evolution save              持久化当前状态
  lh-evolution load              加载持久化状态
  lh-evolution --json            输出 JSON 格式
        """,
    )
    p.add_argument("command", nargs="?", default="demo",
                   choices=["demo", "status", "test", "save", "load",
                            "quick", "version"],
                   help="执行命令")
    p.add_argument("--json", action="store_true",
                   help="JSON 格式输出")
    p.add_argument("--quiet", "-q", action="store_true",
                   help="安静模式")
    p.add_argument("--version", action="version",
                   version=f"lh-evolution v{VERSION}")
    return p


def main():
    """CLI 入口"""
    import argparse
    parser = _build_parser()
    args = parser.parse_args()

    if args.quiet:
        logger.setLevel(logging.WARNING)

    cmd = args.command

    if cmd == "version":
        print(f"lh-evolution v{VERSION}")
        print(f"DNA: {ENGINE_DNA}")
        return 0

    if cmd == "demo":
        run_demo()
        return 0

    if cmd == "quick":
        # 快速自检
        loop = LearningLoop()
        snapshot = {
            "interceptions": [],
            "red_team_results": [],
            "error_rate": 0.05,
            "intercept_rate": 25.0,
            "avg_loyalty": 0.94,
            "red_team_success_rate": 5.0,
            "system_entropy": 0.15,
            "days_since_last_intercept": 1,
        }
        report = loop.run_cycle(snapshot)
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
        else:
            print(f"✅ 快速自检通过 | 健康: {loop.get_system_health()}")
            print(f"   经验: {report['extraction']['total_lessons']} | "
                  f"规则: {report['rules']['active_total']} | "
                  f"版本: v{report['version_check']['current']}")
        return 0

    if cmd == "status":
        loop = LearningLoop()
        loop.init_persistence()
        loop.load_state()
        report = loop.get_full_report()
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
        else:
            print(f"🏥 系统健康: {report['health']}")
            print(f"🔄 闭环次数: {report['loop_count']}")
            print(f"📥 输入闸门: 接受 {report['input_gate']['accepted']} | "
                  f"拒绝 {report['input_gate']['rejected']}")
            print(f"📝 经验库: {report['experience_extractor']['total_lessons']} 条")
            print(f"📜 活跃规则: {report['rule_generator']['active']} 条")
            print(f"💾 记忆库: {report['memory']['total']} 条")
            print(f"⬆️  版本: v{report['version']['current_version']}")
        return 0

    if cmd == "test":
        loop = LearningLoop()
        errors = []

        # 测试 1: 输入闸门
        pkt = loop.input_gate.validate("test", "anonymous")
        if not pkt.validated:
            errors.append("输入闸门: 基础验证失败")

        # 测试 2: 注入检测
        pkt_bad = loop.input_gate.validate(
            "rm -rf /", "anonymous"
        )
        if pkt_bad.validated:
            errors.append("输入闸门: 注入检测失效")

        # 测试 3: 经验提取
        lesson = loop.extractor.extract_from_purification({
            "personality": "测试人格", "corruption_type": "记忆污染",
            "final_loyalty": 0.5, "purify_id": "TEST-001",
        })
        if not lesson or not lesson.lesson_id:
            errors.append("经验提取: 提取失败")

        # 测试 4: 记忆存储
        mem = loop.memory.store("测试记忆", "atomic_facts")
        if not mem or not mem.entry_id:
            errors.append("记忆: 存储失败")

        # 测试 5: 熔断
        loop.circuit_breaker.feed("error_rate", 0.05)
        state = loop.circuit_breaker.get_state()
        if "关闭" not in state["state"] and "CLOSED" not in str(state["state"]):
            errors.append("熔断: 初始状态异常")

        # 测试 6: 闭环
        snapshot = {
            "interceptions": [], "red_team_results": [],
            "error_rate": 0.02, "intercept_rate": 10.0,
            "avg_loyalty": 0.95, "red_team_success_rate": 0,
            "system_entropy": 0.1, "days_since_last_intercept": 0,
        }
        report = loop.run_cycle(snapshot)
        if not report or "cycle_id" not in report:
            errors.append("闭环: 运行失败")

        if errors:
            print(f"🔴 测试失败: {len(errors)} 项")
            for e in errors:
                print(f"  ❌ {e}")
            return 1

        print(f"✅ 全部测试通过 (6/6)")
        print(f"   输入闸门 ✅ 经验提取 ✅ 记忆 ✅ 熔断 ✅ 闭环 ✅ 自检 ✅")
        return 0

    if cmd == "save":
        loop = LearningLoop()
        loop.init_persistence()
        # 运行一次闭环产生状态
        snapshot = {
            "interceptions": [], "red_team_results": [],
            "error_rate": 0.05, "intercept_rate": 25.0,
            "avg_loyalty": 0.94, "red_team_success_rate": 5.0,
            "system_entropy": 0.15, "days_since_last_intercept": 1,
        }
        loop.run_cycle(snapshot)
        loop._save_state()
        state_dir = loop.config.resolve_state_dir()
        if args.json:
            print(json.dumps({
                "status": "saved",
                "state_dir": str(state_dir),
                "files": [f.name for f in state_dir.glob("evolution_v2_*.json")],
            }, ensure_ascii=False, indent=2))
        else:
            files = list(state_dir.glob("evolution_v2_*.json"))
            print(f"✅ 状态已保存 → {state_dir}")
            print(f"   文件: {[f.name for f in files]}")
        return 0

    if cmd == "load":
        loop = LearningLoop()
        loop.init_persistence()
        ok = loop.load_state()
        if args.json:
            print(json.dumps({"loaded": ok}, ensure_ascii=False))
        elif ok:
            print("✅ 状态已加载")
            print(f"   闭环次数: {loop.loop_count}")
        else:
            print("🟡 无已保存状态")
        return 0

    return 0


# ═══════════════════════════════════════════════════════════
# 入口
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())

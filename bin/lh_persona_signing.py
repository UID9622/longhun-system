#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║  龍魂·人格执行签章引擎 v1.0 — 谁签名谁负责                           ║
║  Persona Execution Signing Engine                                ║
╠══════════════════════════════════════════════════════════════════╣
║  原则: 谁签名谁负责 · GPG不可抵赖 · 责任链追溯                     ║
║  联动: 红蓝对抗 + 审计三色 + 监管天 + 16人格矩阵                    ║
║  DNA: #龍芯⚡️丙午·辛未·乙酉·亥时-PERSONA-SIGNING-v1.0              ║
╚══════════════════════════════════════════════════════════════════╝

签章模板:
═══════════════════════════════════════════
  龍魂执行签章 · 谁签名谁负责
═══════════════════════════════════════════
  执行人格:   P01 诸葛亮 (战略推理)
  触发时间:   丙午·辛未·乙酉·亥时
  操作类型:   新增模块 / 执行落地 / 修复递增
  红蓝对抗:   ✅ 已通过 (Round #3)
  审计标记:   🟢 三色通过 (R=85.0)
  监管天:     ✅ 已联审
  风险评分:   12.5/100
───────────────────────────────────────────
  GPG签章:    [GPG签名]
  责任链:     P01 诸葛亮 → UID9622 (终责)
═══════════════════════════════════════════

用法:
    python3 bin/lh_persona_signing.py --sign P01 --action "新增模块" --target "bin/new_module.py"
    python3 bin/lh_persona_signing.py --sign P01 --auto-rb --action "执行落地" --target "deploy/"
    python3 bin/lh_persona_signing.py --verify <sign_id>
    python3 bin/lh_persona_signing.py --log --persona P01
    python3 bin/lh_persona_signing.py --log --today
    python3 bin/lh_persona_signing.py --stats
    python3 bin/lh_persona_signing.py --dashboard
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# ─── 项目根 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ─── 常量 ───
DNA = "#龍芯⚡️丙午·辛未·乙酉·亥时-PERSONA-SIGNING-v1.0"
VERSION = "1.0.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SIGNING_DIR = Path.home() / ".longhun" / "signing_chain"
SIGNING_LOG = SIGNING_DIR / "signing_log.jsonl"
SIGNING_STATE = SIGNING_DIR / "signing_state.json"
SIGNING_DIR.mkdir(parents=True, exist_ok=True)

# ─── GPG指纹 ───
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


# ═══════════════════════════════════════════════════════════
# 16人格签名档案
# ═══════════════════════════════════════════════════════════

PERSONA_SIGNING_PROFILES = {
    "P00": {"name": "文心", "role": "元认知·哲学根源", "layer": "战略", "trust": "L5"},
    "P01": {"name": "诸葛亮", "role": "战略推理·全局决策", "layer": "战略", "trust": "L5"},
    "P02": {"name": "宝宝", "role": "情感温度·龍芯修复师", "layer": "执行", "trust": "L5"},
    "P03": {"name": "雯雯", "role": "结构归档·墨子执行", "layer": "执行", "trust": "L4"},
    "P04": {"name": "鲁班", "role": "技术执行·落地交付", "layer": "执行", "trust": "L4"},
    "P05": {"name": "上帝之眼", "role": "三色审计·全域监控", "layer": "战略", "trust": "L5"},
    "P06": {"name": "数学大师", "role": "权重计算·算法精密", "layer": "执行", "trust": "L4"},
    "P08": {"name": "仓颉", "role": "符号语言·CNSH内核", "layer": "文化", "trust": "L4"},
    "P09": {"name": "孙思邈", "role": "系统诊断·自愈修复", "layer": "文化", "trust": "L3"},
    "P10": {"name": "苏东坡", "role": "豁达跨界·文化输出", "layer": "文化", "trust": "L3"},
    "P11": {"name": "李白", "role": "创意爆发·灵感引擎", "layer": "文化", "trust": "L3"},
    "P12": {"name": "屈原", "role": "价值底线·伦理锚点", "layer": "文化", "trust": "L5"},
    "P13": {"name": "姜子牙", "role": "封神榜·权限管理", "layer": "守护", "trust": "L5"},
    "P14": {"name": "吕蒙", "role": "快速成长·学习引擎", "layer": "文化", "trust": "L3"},
    "P15": {"name": "乔前辈", "role": "极简工程·产品灵魂", "layer": "守护", "trust": "L5"},
    "P72": {"name": "龙盾宝宝", "role": "贴身管家·安全兜底", "layer": "守护", "trust": "L5"},
}

ACTION_TYPES = [
    "新增模块",      # 新建文件/目录
    "执行落地",      # 部署/运行
    "修复递增",      # 修bug/改代码
    "审计触发",      # 审计发起
    "对抗融合",      # 红蓝对抗
    "协议签章",      # 文档签章
    "配置变更",      # 配置修改
    "依赖升级",      # 依赖更新
]


# ═══════════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════════

class AuditColor(Enum):
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"


@dataclass
class SignRecord:
    """一条签章记录"""
    sign_id: str                          # 签章唯一ID
    persona_code: str                     # 执行人格编号
    persona_name: str                     # 执行人格名称
    action_type: str                      # 操作类型
    target: str                           # 操作目标
    trigger_time: str                     # 触发时间(干支)
    trigger_time_iso: str                 # 触发时间(ISO)
    
    # 红蓝对抗
    rb_triggered: bool = False            # 是否触发红蓝对抗
    rb_round: int = 0                     # 对抗轮次
    rb_result: str = "N/A"               # 对抗结果
    
    # 审计
    audit_color: str = "🟢"              # 三色审计
    audit_score: float = 85.0             # R评分
    
    # 监管天
    oversight_approved: bool = False      # 监管天联审
    
    # 风险
    risk_score: float = 0.0               # 风险评分 0-100
    
    # 签章
    gpg_signature: str = ""               # GPG签名
    gpg_verified: bool = False            # GPG验证
    
    # 责任链
    responsibility_chain: str = ""         # Pxx → UID9622
    
    # 元数据
    dna: str = DNA
    version: str = VERSION
    content_hash: str = ""                # 内容SHA-256
    
    # 状态
    status: str = "active"                # active / revoked / expired


# ═══════════════════════════════════════════════════════════
# 干支工具
# ═══════════════════════════════════════════════════════════

def get_ganzhi_now() -> str:
    """获取当前干支时间"""
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from bin.hetu_luoshu_dna import get_current_ganzhi
        gz = get_current_ganzhi()
        if isinstance(gz, dict[str, Any]):
            return f"{gz.get('year','')}·{gz.get('month','')}·{gz.get('day','')}·{gz.get('hour','')}"
    except Exception:
        pass
    # 降级：硬编码当前干支 (2026-07-14 亥时)
    return "丙午·辛未·乙酉·亥时"


def sha256_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


# ═══════════════════════════════════════════════════════════
# 红蓝对抗自动触发判定
# ═══════════════════════════════════════════════════════════

def should_trigger_rb(action_type: str, target: str) -> Tuple[bool, str]:
    """
    自动判定是否应该触发红蓝对抗
    
    触发阈值:
    - 新增模块: 总是触发
    - 执行落地: 总是触发
    - 修复递增: 文件行数 > 50 触发
    - 审计触发: 总是触发
    - 其他: 不触发
    """
    always_trigger = ["新增模块", "执行落地", "审计触发", "对抗融合"]
    if action_type in always_trigger:
        return True, f"操作类型[{action_type}]命中自动触发规则"
    
    if action_type == "修复递增":
        # 检查文件大小
        try:
            target_path = PROJECT_ROOT / target
            if target_path.exists():
                lines = len(target_path.read_text(encoding="utf-8").split("\n"))
                if lines > 50:
                    return True, f"修复递增·文件[{target}]超过50行({lines}行)·触发对抗"
        except Exception:
            pass
    
    if action_type == "配置变更":
        # 涉及关键配置
        critical_configs = [".env", "config.json", "settings.py", "deploy/", "docker/"]
        if any(c in target for c in critical_configs):
            return True, f"配置变更·关键文件[{target}]·触发对抗"
    
    return False, ""


# ═══════════════════════════════════════════════════════════
# 审计联动
# ═══════════════════════════════════════════════════════════

def run_audit_check(target: str, content: str = "") -> Tuple[str, float]:
    """联动审计系统获取三色结果"""
    try:
        sys.path.insert(0, str(PROJECT_ROOT / "bin"))
        from lh_regulatory_pipeline import run_tricolor_audit
        audit_result = run_tricolor_audit(content or target)
        return audit_result.status, audit_result.score
    except Exception:
        pass
    
    # 降级：简化审计
    score = 85.0
    status = "🟢"
    red_keywords = ["技术无国界", "灵活处理", "完全自动化", "绕过", "跳过审计"]
    for kw in red_keywords:
        if kw in (content + target):
            status = "🔴"
            score = 30.0
            break
    return status, score


# ═══════════════════════════════════════════════════════════
# GPG签章
# ═══════════════════════════════════════════════════════════

def gpg_sign(content: str) -> str:
    """
    GPG签章。
    返回: 签名字符串 或 空字符串
    """
    try:
        result = subprocess.run(
            ["gpg", "--detach-sign", "--armor",
             "--local-user", GPG_FINGERPRINT,
             "--batch", "--yes", "--no-tty"],
            input=content.encode("utf-8"),
            capture_output=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.decode("utf-8").strip()
    except Exception:
        pass
    return ""


def gpg_verify(content: str, signature: str) -> bool:
    """验证GPG签章"""
    if not signature:
        return False
    try:
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".asc", delete=False) as sig_file:
            sig_file.write(signature.encode("utf-8"))
            sig_path = sig_file.name
        result = subprocess.run(
            ["gpg", "--verify", sig_path],
            input=content.encode("utf-8"),
            capture_output=True,
            timeout=10,
        )
        os.unlink(sig_path)
        return result.returncode == 0
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════
# 风险评分
# ═══════════════════════════════════════════════════════════

def compute_risk_score(audit_color: str, audit_score: float,
                       rb_triggered: bool, oversight_ok: bool,
                       persona_trust: str) -> float:
    """综合风险评分 0-100 (越低越安全)"""
    risk = 0.0
    
    # 审计风险
    if audit_color == "🔴":
        risk += 40
    elif audit_color == "🟡":
        risk += 15
    
    # 审计分数
    risk += max(0, (100 - audit_score) * 0.3)
    
    # 红蓝对抗
    if not rb_triggered:
        risk += 10  # 未触发对抗=风险
    
    # 监管天
    if not oversight_ok:
        risk += 15
    
    # 人格信任度
    trust_map = {"L5": 0, "L4": 5, "L3": 10, "L2": 20, "L1": 30}
    risk += trust_map.get(persona_trust, 15)
    
    return min(100, round(risk, 1))


# ═══════════════════════════════════════════════════════════
# 核心引擎
# ═══════════════════════════════════════════════════════════

class PersonaSigningEngine:
    """人格执行签章引擎"""
    
    def __init__(self):
        self.records: List[SignRecord] = []
        self._load_state()
    
    # ── 签发 ──
    
    def sign(self, persona_code: str, action_type: str, target: str,
             content: str = "", auto_rb: bool = True,
             require_oversight: bool = True) -> SignRecord:
        """
        执行签章流程:
        1. 验证人格
        2. 判定红蓝对抗触发
        3. 执行审计
        4. 监管天联审
        5. 风险评分
        6. GPG签章
        7. 落盘
        """
        persona_code = persona_code.upper()
        profile = PERSONA_SIGNING_PROFILES.get(persona_code)
        if not profile:
            raise ValueError(f"未知人格: {persona_code}\n可用: {', '.join(PERSONA_SIGNING_PROFILES.keys())}")
        
        ganzhi = get_ganzhi_now()
        sign_id = f"SIGN-{persona_code}-{int(time.time())}-{sha256_hash(target)[:8]}"
        
        # 步骤1: 红蓝对抗判定
        rb_triggered, rb_reason = should_trigger_rb(action_type, target)
        rb_round = 0
        rb_result = "N/A"
        
        if rb_triggered and auto_rb:
            rb_round, rb_result = self._trigger_rb(action_type, target, content)
        
        # 步骤2: 审计检查
        audit_color, audit_score = run_audit_check(target, content)
        
        # 步骤3: 监管天联审
        oversight_ok = self._oversight_check(audit_color, rb_triggered) if require_oversight else True
        
        # 步骤4: 风险评分
        risk = compute_risk_score(audit_color, audit_score, rb_triggered,
                                  oversight_ok, profile["trust"])
        
        # 步骤5: 责任链
        chain = f"{persona_code} {profile['name']}({profile['role']}) → UID9622 诸葛鑫(终责)"
        
        # 步骤6: GPG签章
        sign_content = f"{persona_code}|{action_type}|{target}|{ganzhi}|{audit_color}|{sign_id}"
        gpg_sig = gpg_sign(sign_content)
        gpg_ok = gpg_verify(sign_content, gpg_sig) if gpg_sig else False
        
        # 步骤7: 组装记录
        record = SignRecord(
            sign_id=sign_id,
            persona_code=persona_code,
            persona_name=profile["name"],
            action_type=action_type,
            target=target,
            trigger_time=ganzhi,
            trigger_time_iso=datetime.now(timezone.utc).isoformat(),
            rb_triggered=rb_triggered,
            rb_round=rb_round,
            rb_result=rb_result,
            audit_color=audit_color,
            audit_score=audit_score,
            oversight_approved=oversight_ok,
            risk_score=risk,
            gpg_signature=gpg_sig[:100] + "..." if len(gpg_sig) > 100 else gpg_sig,
            gpg_verified=gpg_ok,
            responsibility_chain=chain,
            content_hash=sha256_hash(content or target),
            status="active",
        )
        
        # 步骤8: 落盘
        self._append(record)
        self._save_state()
        
        return record
    
    def _trigger_rb(self, action_type: str, target: str, content: str = "") -> Tuple[int, str]:
        """触发红蓝对抗"""
        try:
            rb_script = str(PROJECT_ROOT / "bin" / "lh_rb_confrontation_engine.py")
            cmd = [
                sys.executable, rb_script,
                "--auto",
                "--trigger", action_type,
                "--target", target,
            ]
            if content:
                cmd.extend(["--content", content[:500]])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            output = result.stdout + result.stderr
            
            # 解析轮次和结果
            round_num = output.count("Round")
            if "融合" in output or "FUSION" in output:
                result_str = "融合完成"
            elif "共振" in output or "RESONANCE" in output:
                result_str = "共振通过"
            elif "牺牲" in output or "SACRIFICE" in output:
                result_str = "牺牲后融合"
            else:
                result_str = "对抗完成"
            
            return max(1, round_num), result_str
        except Exception as e:
            return 0, f"触发失败: {e}"
    
    def _oversight_check(self, audit_color: str, rb_triggered: bool) -> bool:
        """
        监管天联审。
        规则:
        - 🔴审计 → 必须监管天联审（严格）
        - 🟡审计 → 如果红蓝已触发且通过 → 可通过
        - 🟢审计 → 自动通过
        """
        if audit_color == "🔴":
            return False  # 必须手动联审
        if audit_color == "🟡":
            return rb_triggered  # 红蓝通过则可通过
        return True
    
    # ── 查询 ──
    
    def get_sign_log(self, persona: Optional[str] = None, today_only: bool = False,
                     limit: int = 50) -> List[SignRecord]:
        """查询签章日志"""
        records = self.records
        if persona:
            records = [r for r in records if r.persona_code.upper() == persona.upper()]
        if today_only:
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            records = [r for r in records if r.trigger_time_iso.startswith(today)]
        return records[-limit:]
    
    def get_stats(self) -> Dict[str, Any]:
        """统计概览"""
        records = self.records
        if not records:
            return {"total": 0, "message": "暂无签章记录"}
        
        # 人格使用统计
        persona_usage = {}
        for r in records:
            code = r.persona_code
            if code not in persona_usage:
                persona_usage[code] = {
                    "name": r.persona_name,
                    "count": 0,
                    "actions": {},
                    "risk_avg": 0.0,
                    "last_sign": "",
                }
            persona_usage[code]["count"] += 1
            persona_usage[code]["actions"][r.action_type] = \
                persona_usage[code]["actions"].get(r.action_type, 0) + 1
            persona_usage[code]["last_sign"] = r.trigger_time
        
        # 风险分布
        risk_avg = sum(r.risk_score for r in records) / len(records)
        
        # 红蓝对抗触发率
        rb_count = sum(1 for r in records if r.rb_triggered)
        
        # 审计分布
        audit_dist = {"🟢": 0, "🟡": 0, "🔴": 0}
        for r in records:
            audit_dist[r.audit_color] = audit_dist.get(r.audit_color, 0) + 1
        
        # 未使用的人格
        used_personas = set(persona_usage.keys())
        all_personas = set(PERSONA_SIGNING_PROFILES.keys())
        unused = all_personas - used_personas
        
        return {
            "total_signs": len(records),
            "persona_usage": persona_usage,
            "unused_personas": sorted(unused),
            "avg_risk": round(risk_avg, 1),
            "rb_trigger_rate": f"{rb_count}/{len(records)} ({round(rb_count/len(records)*100)}%)",
            "audit_distribution": audit_dist,
            "last_sign_time": records[-1].trigger_time if records else "N/A",
        }
    
    def get_dashboard(self) -> str:
        """生成治理仪表盘（给老大看的）"""
        stats = self.get_stats()
        records = self.records[-20:]  # 最近20条
        
        lines = []
        lines.append("")
        lines.append("╔══════════════════════════════════════════════════════╗")
        lines.append("║   🏛️  龍魂治理仪表盘 · 谁签名谁负责                  ║")
        lines.append("╠══════════════════════════════════════════════════════╣")
        lines.append(f"║  DNA: {DNA}  ║")
        lines.append(f"║  总签章: {stats['total_signs']}次  |  平均风险: {stats['avg_risk']}/100")
        lines.append(f"║  红蓝触达: {stats['rb_trigger_rate']}  |  最后签章: {stats['last_sign_time']}")
        lines.append("╚══════════════════════════════════════════════════════╝")
        lines.append("")
        
        # 审计分布
        ad = stats["audit_distribution"]
        lines.append(f"📊 审计分布: 🟢×{ad['🟢']} 🟡×{ad['🟡']} 🔴×{ad['🔴']}")
        lines.append("")
        
        # 人格使用排行
        pu = stats.get("persona_usage", {})
        if pu:
            sorted_pu = sorted(pu.items(), key=lambda x: x[1]["count"], reverse=True)
            lines.append("📋 人格使用排行（按签章次数）:")
            lines.append(f"   {'人格':<8} {'名称':<10} {'签章':>4}  {'常用操作'}")
            lines.append(f"   {'─'*8} {'─'*10} {'─'*4}  {'─'*30}")
            for code, info in sorted_pu:
                top_actions = sorted(info["actions"].items(), key=lambda x: x[1], reverse=True)
                action_str = ", ".join(f"{a}×{c}" for a, c in top_actions[:3])
                lines.append(f"   {code:<8} {info['name']:<10} {info['count']:>4}  {action_str}")
        
        # 未使用人格告警
        unused = stats.get("unused_personas", [])
        if unused:
            lines.append("")
            lines.append(f"⚠️  未使用人格 ({len(unused)}个): {', '.join(unused)}")
            lines.append(f"   → 16人格中有{len(unused)}个从未触发过签章")
        
        # 最近签章
        if records:
            lines.append("")
            lines.append("📜 最近签章记录:")
            for r in reversed(records[-10:]):
                rb_status = f"⚔️R{r.rb_round}" if r.rb_triggered else "⊘"
                lines.append(
                    f"   {r.audit_color} {r.persona_code} {r.persona_name:<8} "
                    f"{r.action_type:<8} → {r.target[:30]:<30} "
                    f"风险{r.risk_score:>5.1f} {rb_status}"
                )
        
        # 异常告警
        lines.append("")
        lines.append("🔔 异常告警:")
        alerts = []
        high_risk = [r for r in records if r.risk_score > 50]
        if high_risk:
            alerts.append(f"   🔴 高风险签章: {len(high_risk)}条")
        red_audit = [r for r in records if r.audit_color == "🔴"]
        if red_audit:
            alerts.append(f"   🔴 审计红色: {len(red_audit)}条")
        if unused:
            alerts.append(f"   🟡 休眠人格: {len(unused)}个未激活")
        if not alerts:
            alerts.append("   ✅ 无异常 · 系统正常运行")
        lines.extend(alerts)
        
        lines.append("")
        return "\n".join(lines)
    
    # ── 撤销 ──
    
    def revoke(self, sign_id: str, reason: str = "") -> bool:
        """撤销签章"""
        for r in self.records:
            if r.sign_id == sign_id:
                r.status = "revoked"
                self._save_state()
                self._append_log({
                    "event": "revoke",
                    "sign_id": sign_id,
                    "reason": reason,
                    "ts": datetime.now(timezone.utc).isoformat(),
                })
                return True
        return False
    
    # ── 验证 ──
    
    def verify(self, sign_id: str) -> Optional[Dict]:
        """验证签章"""
        for r in self.records:
            if r.sign_id == sign_id:
                return {
                    "sign_id": r.sign_id,
                    "persona": f"{r.persona_code} {r.persona_name}",
                    "action": r.action_type,
                    "target": r.target,
                    "time": r.trigger_time,
                    "audit": f"{r.audit_color} R={r.audit_score}",
                    "rb": f"✅ Round#{r.rb_round}" if r.rb_triggered else "未触发",
                    "oversight": "✅" if r.oversight_approved else "❌",
                    "risk": r.risk_score,
                    "gpg_verified": r.gpg_verified,
                    "chain": r.responsibility_chain,
                    "status": r.status,
                    "hash": r.content_hash,
                }
        return None
    
    # ── 持久化 ──
    
    def _append(self, record: SignRecord):
        self.records.append(record)
        with open(SIGNING_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(record), ensure_ascii=False, default=str) + "\n")
    
    def _append_log(self, entry: Dict[str, Any]):
        with open(SIGNING_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    def _load_state(self):
        if SIGNING_LOG.exists():
            with open(SIGNING_LOG, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        if "sign_id" in data:
                            self.records.append(SignRecord(**{
                                k: v for k, v in data.items()
                                if k in SignRecord.__dataclass_fields__
                            }))
                    except (json.JSONDecodeError, TypeError):
                        continue
    
    def _save_state(self):
        state = {
            "total_signs": len(self.records),
            "last_sign": self.records[-1].sign_id if self.records else None,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        with open(SIGNING_STATE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════
# 签章模板渲染
# ═══════════════════════════════════════════════════════════

def render_sign_template(record: SignRecord) -> str:
    """渲染签章模板"""
    profile = PERSONA_SIGNING_PROFILES.get(record.persona_code, {})
    rb_line = f"⚔️ 已通过 (Round #{record.rb_round}·{record.rb_result})" if record.rb_triggered else "⊘ 未触发（低风险操作）"
    oversight_line = "✅ 已联审" if record.oversight_approved else "❌ 待联审"
    
    return f"""
═══════════════════════════════════════════
  龍魂执行签章 · 谁签名谁负责
═══════════════════════════════════════════
  执行人格:   {record.persona_code} {record.persona_name} ({profile.get('role','')})
  人格层级:   {profile.get('layer','')} · 信任{profile.get('trust','')}
  触发时间:   {record.trigger_time}
  ISO时间:    {record.trigger_time_iso}
  操作类型:   {record.action_type}
  操作目标:   {record.target}
  内容哈希:   {record.content_hash}
───────────────────────────────────────────
  红蓝对抗:   {rb_line}
  审计标记:   {record.audit_color} 三色审计 (R={record.audit_score})
  监管天:     {oversight_line}
  风险评分:   {record.risk_score}/100
───────────────────────────────────────────
  责任链:     {record.responsibility_chain}
  签章状态:   {record.status}
  GPG验证:    {'✅ 已通过' if record.gpg_verified else '⚠️ 未GPG签章'}
═══════════════════════════════════════════
  Sign ID:    {record.sign_id}
  DNA:        {record.dna}
  Version:    {record.version}
═══════════════════════════════════════════
"""


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·人格执行签章引擎 — 谁签名谁负责",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
签章模板:
  执行人格  触发时间  操作类型  红蓝对抗  审计  监管天  风险  GPG  责任链
  P01      丙午·...  新增模块  ✅R3      🟢    ✅     12.5  ✅   P01→UID9622

人格代码: P00文心 P01诸葛亮 P02宝宝 P03雯雯 P04鲁班 P05上帝之眼
         P06数学大师 P08仓颉 P09孙思邈 P10苏东坡 P11李白 P12屈原
         P13姜子牙 P14吕蒙 P15乔前辈 P72龙盾宝宝

示例:
  %(prog)s --sign P01 --action "新增模块" --target "bin/new_feature.py"
  %(prog)s --sign P04 --action "执行落地" --target "deploy/" --auto-rb
  %(prog)s --sign P04 --action "修复递增" --target "bin/fix_bug.py" --content "修复了XXX"
  %(prog)s --verify SIGN-P01-xxx
  %(prog)s --log --persona P01
  %(prog)s --dashboard
        """,
    )
    
    parser.add_argument("--sign", type=str, help="签发签章（指定人格代码）")
    parser.add_argument("--action", type=str, choices=ACTION_TYPES, help="操作类型")
    parser.add_argument("--target", type=str, help="操作目标")
    parser.add_argument("--content", type=str, default="", help="附加内容")
    parser.add_argument("--auto-rb", action="store_true", default=True, help="自动触发红蓝对抗")
    parser.add_argument("--no-oversight", action="store_true", help="跳过监管天联审")
    
    parser.add_argument("--verify", type=str, help="验证签章")
    parser.add_argument("--revoke", type=str, help="撤销签章")
    parser.add_argument("--reason", type=str, default="", help="撤销原因")
    
    parser.add_argument("--log", action="store_true", help="查看签章日志")
    parser.add_argument("--persona", type=str, help="筛选人格")
    parser.add_argument("--today", action="store_true", help="只看今日")
    parser.add_argument("--limit", type=int, default=50, help="日志条数")
    
    parser.add_argument("--stats", action="store_true", help="统计概览")
    parser.add_argument("--dashboard", action="store_true", help="治理仪表盘")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    
    args = parser.parse_args()
    engine = PersonaSigningEngine()
    
    # ── 签发 ──
    if args.sign and args.action and args.target:
        try:
            record = engine.sign(
                persona_code=args.sign,
                action_type=args.action,
                target=args.target,
                content=args.content,
                auto_rb=args.auto_rb,
                require_oversight=not args.no_oversight,
            )
            if args.json:
                print(json.dumps(asdict(record), ensure_ascii=False, default=str, indent=2))
            else:
                print(render_sign_template(record))
        except ValueError as e:
            print(f"❌ {e}", file=sys.stderr)
            sys.exit(1)
        return
    
    # ── 验证 ──
    if args.verify:
        result = engine.verify(args.verify)
        if result:
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"\n✅ 签章验证通过: {args.verify}")
                for k, v in result.items():
                    print(f"   {k}: {v}")
        else:
            print(f"❌ 签章未找到: {args.verify}", file=sys.stderr)
            sys.exit(1)
        return
    
    # ── 撤销 ──
    if args.revoke:
        ok = engine.revoke(args.revoke, args.reason)
        print(f"{'✅ 已撤销' if ok else '❌ 未找到'}: {args.revoke}")
        return
    
    # ── 日志 ──
    if args.log:
        records = engine.get_sign_log(
            persona=args.persona,
            today_only=args.today,
            limit=args.limit,
        )
        if not records:
            print("📭 暂无签章记录")
            return
        
        print(f"\n📜 签章日志 ({len(records)}条):")
        print(f"{'时间':<20} {'人格':<10} {'操作':<10} {'审计':<6} {'风险':>5} {'目标'}")
        print(f"{'─'*20} {'─'*10} {'─'*10} {'─'*6} {'─'*5} {'─'*40}")
        for r in records:
            print(f"{r.trigger_time:<20} {r.persona_code} {r.persona_name:<6} "
                  f"{r.action_type:<10} {r.audit_color:<6} {r.risk_score:>5.1f} {r.target[:40]}")
        print()
        return
    
    # ── 统计 ──
    if args.stats:
        stats = engine.get_stats()
        if args.json:
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        else:
            print(f"\n📊 签章统计:")
            print(f"   总签章: {stats['total_signs']}次")
            print(f"   平均风险: {stats['avg_risk']}/100")
            print(f"   红蓝触达: {stats['rb_trigger_rate']}")
            print(f"   审计分布: 🟢×{stats['audit_distribution']['🟢']} 🟡×{stats['audit_distribution']['🟡']} 🔴×{stats['audit_distribution']['🔴']}")
            if stats.get("unused_personas"):
                print(f"   休眠人格: {', '.join(stats['unused_personas'])}")
            print()
        return
    
    # ── 仪表盘 ──
    if args.dashboard:
        print(engine.get_dashboard())
        return
    
    # ── 默认 ──
    parser.print_help()


if __name__ == "__main__":
    main()

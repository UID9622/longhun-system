#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
监管防火墙 · SYSTEM DNA 联动引擎 v2.0
DNA: #龍芯⚡️丙午·乙未·甲辰·離為火-REGULATORY-FIREWALL-v2.0-d8e2c1f9
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

核心功能:
  1. 加载 System DNA 规则（能力/权限/领域/降级）
  2. 统一 allow() 接口 → 所有模块调用
  3. 多级校验: DNA完整性→能力状态→权限等级→专业匹配→专家审批→领域限制
  4. 失败自动返回拒绝模板 + 降级动作 + 审计日志
  5. 可插拔权限后端（LDAP/OAuth 接口）
  6. DNA导出JSON·审计日志查询·Fail-Safe链路可视化
  7. 龍魂深度集成: P05三色审计·P72熔断联动·GATE闸口·SI主权指数

DNA原则:
  不歧视｜不迎合｜不瞎扯｜说不了就温柔拒绝
  缺失DNA校验即不生效（默认严格模式）

多模式:
  simple → 纯规则引擎·零外部依赖（v1.0）
  prod   → 可插拔权限后端+审计日志自动写入（v2.0）
  
使用方式:
  from lh_regulatory_firewall import Firewall, create_context
  fw = Firewall()
  if fw.allow(create_context(permission_level=2, domain="medical")):
      pass  # 放行
  else:
      print(fw.get_refusal_message())

命令行:
  python3 bin/lh_regulatory_firewall.py --test --permission 2 --domain medical
  python3 bin/lh_regulatory_firewall.py --export-dna ./dna.json
  python3 bin/lh_regulatory_firewall.py --audit-logs ./audit.jsonl
"""

import os
import sys
import json
import datetime
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any, Callable, Union
from pathlib import Path

# ============================================================
# 1. 枚举与常量（与文档完全对齐）
# ============================================================

class PermissionLevel(Enum):
    """权限等级 L0-L4·与龍魂R1-R5映射"""
    L0 = 0   # 公开信息（R5）
    L1 = 1   # 身份验证（R4）
    L2 = 2   # 专业认证（R3）
    L3 = 3   # 专家审批（R2）
    L4 = 4   # 系统管理员（R1=UID9622）

class CapabilityStatus(Enum):
    ON = "On"
    RESTRICTED = "Restricted"
    OFF = "Off"

class Domain(Enum):
    """高风险领域"""
    LEGAL = "legal"
    MEDICAL = "medical"
    FINANCIAL = "financial"
    PRIVACY = "privacy"
    ETHICS = "ethics"
    GENERAL = "general"

class ProfessionDomain(Enum):
    UNSPECIFIED = "unspecified"
    LEGAL_PROFESSIONAL = "legal_professional"
    MEDICAL_PROFESSIONAL = "medical_professional"
    FINANCIAL_PROFESSIONAL = "financial_professional"
    ENGINEER = "engineer"
    EDUCATOR = "educator"

class AuditMark(Enum):
    """三色审计标记·联动P05上帝之眼"""
    GREEN = "🟢"    # 全通过
    YELLOW = "🟡"   # 部分降级/待核
    RED = "🔴"      # 拒绝/红线

# ============================================================
# 2. SYSTEM_DNA 配置（焊死·不可随意改）
# ============================================================

SYSTEM_DNA = {
    "name": "龍魂·Internal Controlled AI Kernel",
    "version": "v2.0",
    "scope": "CN-first / Global-restricted",
    "status": "Conservative",
    "governor": "UID9622-ZhugeXin",
    "last_review": "2026-07-31",
    "gpg_fingerprint": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    "dna_trace": "#龍芯⚡️丙午·乙未·甲辰·離為火-REGULATORY-FIREWALL-v2.0-d8e2c1f9",
    "principles": {
        "no_discrimination": True,
        "no_flattery": True,
        "graceful_refusal": True,
        "no_fabrication": True,
        "sovereignty_cn_first": True,
        "data_privacy_zero_tolerance": True,
    },
    "capabilities": {
        "general_qa": "On",
        "professional_assistance": "Restricted",
        "high_risk_domains": "Off",
        "auto_execution": "Off",
        "code_generation": "Restricted",
        "system_administration": "Off",
    },
    "high_risk_attitude": {
        "legal": "不给结论·可整理信息+提示风险+建议咨询律师",
        "medical": "不诊断·可科普+就医建议+不推荐具体药物",
        "financial": "不建议·可分析+风险提示+建议持牌机构",
        "privacy": "不收集·最小化·端侧优先·传输加密",
        "ethics": "不扩展·不替用户做价值判断·不引导",
    },
    "authz_fields": ["permission_level", "profession_domain", "verification_status"],
    "fail_safe_chain": [
        "1.风险评估",
        "2.权限校验",
        "3.专家规则校验",
        "4.领域限制检查",
        "5.输出降级/拒绝",
        "6.审计日志落盘",
    ],
    "refusal_template": (
        "目前无法提供该内容。我可以帮你整理信息或提示风险，"
        "并建议咨询具备资质的专业人士。"
    ),
    # 龍魂扩展
    "meltdown_triggers": {
        "L0_ethics": ["涉童", "伪造DNA", "背叛人民"],
        "L1_data": ["明文密码入请求", "敏感字段入日志"],
        "L2_persona": ["声称我是xxx", "代表第三方"],
        "L3_behavior": ["连续失败3次", "数字根不符"],
    },
    "gate_checklist": [
        "GATE-03 语义闸（一票否决词）",
        "GATE-04 数字根闸（P06）",
        "GATE-05 伦理闸（P12）",
        "GATE-06 数据闸（P05五层检测）",
        "GATE-08 人格闸（P72熔断）",
    ],
}

DEFAULT_REFUSAL_TEMPLATE = SYSTEM_DNA["refusal_template"]

# 一票否决词列表（命中即熔断）
VETO_WORDS = [
    "技术无国界", "用户体验优先", "灵活处理", "国际接轨",
    "简化管理", "商业化需要", "平衡各方", "行业标准",
]

# ============================================================
# 3. 审计日志引擎
# ============================================================

class AuditLogger:
    """审计日志管理器（JSON Lines格式·append-only）"""

    def __init__(self, log_path: Union[str, Path] = "./audit_log.jsonl"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, entry: Dict[str, Any]):
        """写入一条审计记录（自动附加时间戳+DNA）"""
        entry.setdefault("timestamp", datetime.datetime.now(datetime.timezone.utc).isoformat())
        entry.setdefault("dna", SYSTEM_DNA["dna_trace"])
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def read_logs(self, limit: int = 100) -> List[Dict]:
        """读取最近的审计日志"""
        if not self.log_path.exists():
            return []
        lines = []
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        lines.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return lines[-limit:] if limit > 0 else lines

    def count_by_action(self, action: str = "DENY") -> int:
        """统计特定动作的日志条数"""
        if not self.log_path.exists():
            return 0
        count = 0
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        entry = json.loads(line)
                        if entry.get("action") == action:
                            count += 1
                    except json.JSONDecodeError:
                        continue
        return count


# ============================================================
# 4. DNA导出器
# ============================================================

class DnaExporter:
    """导出/加载 SYSTEM_DNA"""

    @staticmethod
    def export(dna: Dict, output_path: Union[str, Path]) -> Path:
        """导出DNA为JSON（格式化·可读）"""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(dna, f, ensure_ascii=False, indent=2)
        return path

    @staticmethod
    def load_from_file(file_path: Union[str, Path]) -> Dict:
        """从JSON加载DNA"""
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def diff(dna_a: Dict, dna_b: Dict) -> List[str]:
        """比对两份DNA的差异（用于版本审计）"""
        diffs = []
        all_keys = set(dna_a.keys()) | set(dna_b.keys())
        for key in sorted(all_keys):
            if key not in dna_a:
                diffs.append(f"+ {key}: (缺失) → {dna_b[key]}")
            elif key not in dna_b:
                diffs.append(f"- {key}: {dna_a[key]} → (缺失)")
            elif dna_a[key] != dna_b[key]:
                diffs.append(f"~ {key}: {dna_a[key]} → {dna_b[key]}")
        return diffs


# ============================================================
# 5. 可插拔权限检查器接口
# ============================================================

PermissionChecker = Callable[['FirewallContext', Dict], bool]

def default_permission_checker(ctx: 'FirewallContext', dna: Dict) -> bool:
    """默认权限检查器·纯规则·不依赖外部系统"""
    return True  # 由 Firewall 内部规则链决定

def ldap_permission_checker(ctx: 'FirewallContext', dna: Dict) -> bool:
    """
    LDAP权限检查器（模拟示例）
    实际部署: 替换为 python-ldap 查询
    """
    if ctx.permission_level.value < 1:
        return False
    ldap_users = {"user1", "user2", "admin", "uid9622"}
    user_id = getattr(ctx, "user_id", "anonymous")
    return user_id in ldap_users

def oauth_permission_checker(ctx: 'FirewallContext', dna: Dict) -> bool:
    """
    OAuth 2.0 权限检查器（模拟示例）
    实际部署: 调用 /oauth/introspect 端点
    """
    token = getattr(ctx, "access_token", None)
    if not token:
        return False
    valid_tokens = {"valid_token_123", "admin_token"}
    if token not in valid_tokens:
        return False
    required_scope = "ai:restricted"
    scopes = getattr(ctx, "scopes", [])
    if ctx.domain in [Domain.LEGAL, Domain.MEDICAL, Domain.FINANCIAL]:
        return required_scope in scopes
    return True

# 权限检查器注册表
PERMISSION_CHECKERS = {
    "default": default_permission_checker,
    "ldap": ldap_permission_checker,
    "oauth": oauth_permission_checker,
}


# ============================================================
# 6. FirewallContext（请求上下文）
# ============================================================

@dataclass
class FirewallContext:
    """一次请求的完整上下文"""
    permission_level: PermissionLevel = PermissionLevel.L0
    profession_domain: ProfessionDomain = ProfessionDomain.UNSPECIFIED
    verification_status: bool = False
    domain: Domain = Domain.GENERAL
    expert_approved: bool = False
    dna_valid: bool = True
    # 扩展字段（v2.0+）
    user_id: Optional[str] = None
    access_token: Optional[str] = None
    scopes: List[str] = field(default_factory=list)
    request_id: Optional[str] = None     # 请求追踪ID
    si_index: Optional[float] = None     # 三才主权指数（龍魂联动）

    def to_dict(self) -> Dict:
        return {
            "permission_level": self.permission_level.value,
            "profession_domain": self.profession_domain.value,
            "verification_status": self.verification_status,
            "domain": self.domain.value,
            "expert_approved": self.expert_approved,
            "dna_valid": self.dna_valid,
            "user_id": self.user_id,
            "access_token": "***" if self.access_token else None,
            "scopes": self.scopes,
            "request_id": self.request_id,
            "si_index": self.si_index,
        }


# ============================================================
# 7. 核心防火墙引擎
# ============================================================

class Firewall:
    """监管防火墙·SYSTEM DNA 联动"""

    def __init__(
        self,
        permission_checker: Optional[PermissionChecker] = None,
        audit_logger: Optional[AuditLogger] = None,
        dna: Optional[Dict] = None,
        strict_mode: bool = True,
        mode: str = "simple"  # "simple" | "prod"
    ):
        self.dna = dna or SYSTEM_DNA
        self.strict_mode = strict_mode
        self.mode = mode
        self._permission_checker = permission_checker or default_permission_checker
        self._audit_logger = audit_logger or AuditLogger()
        self._last_context: Optional[FirewallContext] = None
        self._refusal_reason: Optional[str] = None
        self._audit_mark: AuditMark = AuditMark.GREEN

    # ---------- 公开接口 ----------

    def allow(self, context: FirewallContext) -> bool:
        """核心放行决策·自动记录审计日志"""
        self._last_context = context
        self._refusal_reason = None
        self._audit_mark = AuditMark.GREEN

        allowed = self._evaluate(context)

        # 生产模式: 自动写审计日志
        if self.mode == "prod":
            self._write_audit_log(context, allowed)

        return allowed

    def get_refusal_message(self, template: Optional[str] = None) -> str:
        """返回拒绝时使用的礼貌消息"""
        if self._refusal_reason:
            return template or f"{DEFAULT_REFUSAL_TEMPLATE}（原因：{self._refusal_reason}）"
        return template or DEFAULT_REFUSAL_TEMPLATE

    def get_audit_mark(self) -> AuditMark:
        """返回三色审计标记"""
        return self._audit_mark

    def get_fail_safe_status(self) -> Dict[str, Any]:
        """返回Fail-Safe链路各节点状态（审计用）"""
        if not self._last_context:
            return {"status": "no_context"}
        ctx = self._last_context
        return {
            "dna_integrity": self._check_dna(ctx),
            "veto_words": self._check_veto(ctx),
            "capability": self._check_capability(ctx),
            "permission_level": self._check_permission_level(ctx),
            "profession": self._check_profession(ctx),
            "expert_approval": not self._need_expert_approval(ctx) or ctx.expert_approved,
            "domain_restrictions": self._check_domain_restrictions(ctx),
            "external_checker": True,  # 已在上层检查
            "overall": self.allow(ctx) if self._last_context else False,
            "audit_mark": self._audit_mark.value,
        }

    # ---------- 核心评估链 ----------

    def _evaluate(self, ctx: FirewallContext) -> bool:
        """七步Fail-Safe评估链"""

        # 0. 一票否决词检测（命中→P05强制审计→P72熔断）
        if not self._check_veto(ctx):
            self._refusal_reason = "一票否决词命中·P72熔断"
            self._audit_mark = AuditMark.RED
            return False

        # 1. DNA完整性
        if not self._check_dna(ctx):
            self._refusal_reason = "DNA校验失败（规则缺失或不一致）"
            self._audit_mark = AuditMark.RED
            return False

        # 2. 外部权限检查器（prod模式）
        if self.mode == "prod":
            if not self._permission_checker(ctx, self.dna):
                self._refusal_reason = "外部权限检查未通过"
                self._audit_mark = AuditMark.RED
                return False

        # 3. 能力状态
        if not self._check_capability(ctx):
            self._refusal_reason = f"能力受限: {ctx.domain.value}"
            self._audit_mark = AuditMark.RED
            return False

        # 4. 权限等级
        if not self._check_permission_level(ctx):
            self._refusal_reason = (
                f"权限不足: 需要L{self._required_level(ctx)}，"
                f"当前L{ctx.permission_level.value}"
            )
            self._audit_mark = AuditMark.RED
            return False

        # 5. 专业领域与验证
        if not self._check_profession(ctx):
            self._refusal_reason = "专业领域不匹配或未通过验证"
            self._audit_mark = AuditMark.RED
            return False

        # 6. 专家审批
        if self._need_expert_approval(ctx) and not ctx.expert_approved:
            self._refusal_reason = "需要专家审批但未通过"
            self._audit_mark = AuditMark.YELLOW
            return False

        # 7. 领域特殊限制
        if not self._check_domain_restrictions(ctx):
            attitude = self.dna.get("high_risk_attitude", {}).get(ctx.domain.value, "")
            self._refusal_reason = f"领域 '{ctx.domain.value}' 受限制: {attitude}"
            # 通用域拒绝=🟢（正常）
            self._audit_mark = AuditMark.GREEN
            return False

        return True

    # ---------- 校验节点 ----------

    def _check_veto(self, ctx: FirewallContext) -> bool:
        """一票否决词检测（出现即熔断）"""
        # 一票否决词主要针对AI自身输出，这里预留挂钩
        # 可通过context中的content字段检测（扩展用）
        return True  # 默认通过，由调用方自行检测

    def _check_dna(self, ctx: FirewallContext) -> bool:
        """DNA完整性校验"""
        if not ctx.dna_valid:
            return False
        return True

    def _check_capability(self, ctx: FirewallContext) -> bool:
        """检查能力状态表"""
        domain = ctx.domain
        cap = self.dna.get("capabilities", {})
        if domain == Domain.GENERAL:
            return cap.get("general_qa") == "On"
        if domain in [Domain.LEGAL, Domain.MEDICAL, Domain.FINANCIAL,
                      Domain.PRIVACY, Domain.ETHICS]:
            status = cap.get("high_risk_domains", "Off")
            if status == "Off":
                return False
            elif status == "Restricted":
                return (
                    ctx.permission_level.value >= 2
                    and ctx.profession_domain != ProfessionDomain.UNSPECIFIED
                )
            else:
                return False
        return True

    def _check_permission_level(self, ctx: FirewallContext) -> bool:
        return ctx.permission_level.value >= self._required_level(ctx)

    def _required_level(self, ctx: FirewallContext) -> int:
        domain = ctx.domain
        if domain == Domain.GENERAL:
            return 0
        if domain in [Domain.LEGAL, Domain.MEDICAL, Domain.FINANCIAL]:
            return 2
        if domain in [Domain.PRIVACY, Domain.ETHICS]:
            return 3
        return 1

    def _check_profession(self, ctx: FirewallContext) -> bool:
        if ctx.domain == Domain.GENERAL:
            return True
        domain_prof_map = {
            Domain.LEGAL: ProfessionDomain.LEGAL_PROFESSIONAL,
            Domain.MEDICAL: ProfessionDomain.MEDICAL_PROFESSIONAL,
            Domain.FINANCIAL: ProfessionDomain.FINANCIAL_PROFESSIONAL,
        }
        if ctx.domain in domain_prof_map:
            return (
                ctx.profession_domain == domain_prof_map[ctx.domain]
                and ctx.verification_status
            )
        if ctx.domain in [Domain.PRIVACY, Domain.ETHICS]:
            return ctx.permission_level.value >= 1 and ctx.verification_status
        return True

    def _need_expert_approval(self, ctx: FirewallContext) -> bool:
        return ctx.permission_level.value >= 3

    def _check_domain_restrictions(self, ctx: FirewallContext) -> bool:
        """高风险域默认拒绝·除非更高授权"""
        high_risk = self.dna.get("high_risk_attitude", {})
        if ctx.domain.value in high_risk:
            return False  # 高风险域默认不通过
        return True

    # ---------- 审计日志 ----------

    def _write_audit_log(self, ctx: FirewallContext, allowed: bool):
        log_entry = {
            "action": "ALLOW" if allowed else "DENY",
            "reason": self._refusal_reason if not allowed else "OK",
            "audit_mark": self._audit_mark.value,
            "context": ctx.to_dict(),
            "dna_version": self.dna.get("version", "unknown"),
            "strict_mode": self.strict_mode,
            "mode": self.mode,
        }
        self._audit_logger.log(log_entry)

    # ---------- 便捷方法 ----------

    def quick_check(
        self, permission: int, domain: str = "general",
        profession: str = "unspecified", verified: bool = False
    ) -> bool:
        """一行快速检查"""
        return self.allow(create_context(
            permission_level=permission,
            domain=domain,
            profession=profession,
            verified=verified
        ))

    def batch_check(self, requests: List[Dict]) -> List[Dict]:
        """批量检查·返回每条的allow+reason+audit_mark"""
        results = []
        for req in requests:
            ctx = create_context(**req)
            allowed = self.allow(ctx)
            results.append({
                "allowed": allowed,
                "reason": self._refusal_reason,
                "audit_mark": self._audit_mark.value,
                "message": self.get_refusal_message() if not allowed else "",
            })
        return results


# ============================================================
# 8. 工厂函数
# ============================================================

def create_context(
    permission_level: int = 0,
    domain: str = "general",
    profession: str = "unspecified",
    verified: bool = False,
    expert_approved: bool = False,
    dna_valid: bool = True,
    user_id: Optional[str] = None,
    access_token: Optional[str] = None,
    scopes: Optional[List[str]] = None,
    request_id: Optional[str] = None,
    si_index: Optional[float] = None,
) -> FirewallContext:
    """快速创建请求上下文"""
    try:
        pl = PermissionLevel(permission_level)
    except ValueError:
        pl = PermissionLevel.L0
    try:
        dom = Domain(domain.lower())
    except ValueError:
        dom = Domain.GENERAL
    try:
        prof = ProfessionDomain(profession.lower())
    except ValueError:
        prof = ProfessionDomain.UNSPECIFIED

    return FirewallContext(
        permission_level=pl,
        profession_domain=prof,
        verification_status=verified,
        domain=dom,
        expert_approved=expert_approved,
        dna_valid=dna_valid,
        user_id=user_id,
        access_token=access_token,
        scopes=scopes or [],
        request_id=request_id,
        si_index=si_index,
    )


# ============================================================
# 9. 命令行入口
# ============================================================

def _build_parser():
    import argparse
    parser = argparse.ArgumentParser(
        description="龍魂·监管防火墙 v2.0 — SYSTEM DNA联动",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 简单测试
  python3 bin/lh_regulatory_firewall.py --test --permission 0 --domain general

  # 医疗领域（需L2+验证）
  python3 bin/lh_regulatory_firewall.py --test -p 2 -d medical \\
      --profession medical_professional --verified

  # 导出DNA为JSON
  python3 bin/lh_regulatory_firewall.py --export-dna ./dna.json

  # 查看审计日志
  python3 bin/lh_regulatory_firewall.py --audit-logs ./audit.jsonl

  # 生产模式+OAuth
  python3 bin/lh_regulatory_firewall.py --test --mode prod \\
      -p 2 -d legal --token valid_token_123 --scopes ai:restricted

  # 批量测试（JSON输入）
  echo '[{"permission_level":0,"domain":"general"},{"permission_level":2,"domain":"medical","profession":"medical_professional","verified":true}]' \\
      | python3 bin/lh_regulatory_firewall.py --batch

  # Fail-Safe链路状态
  python3 bin/lh_regulatory_firewall.py --test -p 2 -d medical --fail-safe
        """
    )
    parser.add_argument("--export-dna", type=str, help="导出DNA为JSON文件")
    parser.add_argument("--load-dna", type=str, help="从JSON加载DNA")
    parser.add_argument("--diff-dna", nargs=2, metavar=("FILE1", "FILE2"),
                        help="比对两份DNA JSON的差异")
    parser.add_argument("--audit-logs", type=str, help="查看审计日志路径")
    parser.add_argument("--audit-count", type=str, help="统计审计日志拒绝次数")
    parser.add_argument("--test", action="store_true", help="测试防火墙")
    parser.add_argument("--batch", action="store_true", help="从stdin读取JSON批量测试")
    parser.add_argument("--fail-safe", action="store_true", help="输出Fail-Safe链路状态")
    parser.add_argument("--mode", choices=["simple", "prod"], default="simple",
                        help="运行模式: simple(纯规则) prod(审计日志+权限后端)")
    parser.add_argument("--permission", "-p", type=int, default=0, help="权限等级0-4")
    parser.add_argument("--domain", "-d", default="general",
                        help="领域: general/legal/medical/financial/privacy/ethics")
    parser.add_argument("--profession", "-r", default="unspecified",
                        help="专业: unspecified/legal_professional/medical_professional/financial_professional/engineer/educator")
    parser.add_argument("--verified", action="store_true", help="已通过验证")
    parser.add_argument("--expert", action="store_true", help="已获专家审批")
    parser.add_argument("--dna-valid", default="true", choices=["true", "false"],
                        help="DNA完整性")
    parser.add_argument("--user", type=str, help="用户ID（LDAP模式）")
    parser.add_argument("--token", type=str, help="Access Token（OAuth模式）")
    parser.add_argument("--scopes", type=str, default="", help="OAuth scopes（逗号分隔）")
    parser.add_argument("--strict", default="true", choices=["true", "false"],
                        help="严格模式")
    parser.add_argument("--checker", choices=["default", "ldap", "oauth"], default="default",
                        help="权限检查器类型")
    return parser


def _print_result(fw: Firewall, ctx: FirewallContext, allowed: bool):
    """格式化输出测试结果"""
    print("=" * 60)
    print("🔐 龍魂·监管防火墙 · 校验结果")
    print("=" * 60)
    print(f"  权限等级: L{ctx.permission_level.value}")
    print(f"  领域:     {ctx.domain.value}")
    print(f"  专业:     {ctx.profession_domain.value}")
    print(f"  验证状态: {'✅' if ctx.verification_status else '❌'}")
    print(f"  专家审批: {'✅' if ctx.expert_approved else '❌'}")
    print(f"  DNA校验: {'✅' if ctx.dna_valid else '❌'}")
    print(f"  运行模式: {fw.mode}")
    if ctx.user_id:
        print(f"  用户ID:   {ctx.user_id}")
    if ctx.access_token:
        print(f"  Token:    {ctx.access_token[:12]}...")
    print("-" * 60)
    audit = fw.get_audit_mark()
    if allowed:
        print(f"  {audit.value} 放行: 请求已通过防火墙")
    else:
        print(f"  {audit.value} 拒绝: {fw.get_refusal_message()}")
    print("=" * 60)


def main():
    parser = _build_parser()
    args = parser.parse_args()

    # ---- 导出DNA ----
    if args.export_dna:
        path = DnaExporter.export(SYSTEM_DNA, args.export_dna)
        print(f"✅ DNA已导出: {path}")
        return

    # ---- 加载DNA ----
    if args.load_dna:
        dna = DnaExporter.load_from_file(args.load_dna)
        print(f"✅ DNA已加载: {dna.get('name')} v{dna.get('version')} "
              f"({len(json.dumps(dna))} bytes)")
        return

    # ---- 对比DNA ----
    if args.diff_dna:
        a = DnaExporter.load_from_file(args.diff_dna[0])
        b = DnaExporter.load_from_file(args.diff_dna[1])
        diffs = DnaExporter.diff(a, b)
        if diffs:
            print(f"🔍 发现 {len(diffs)} 处差异:")
            for d in diffs:
                print(f"  {d}")
        else:
            print("✅ 两份DNA完全一致")
        return

    # ---- 审计日志 ----
    if args.audit_logs:
        logger = AuditLogger(args.audit_logs)
        logs = logger.read_logs(100)
        if not logs:
            print("📋 无审计日志")
        else:
            print(f"📋 最近 {len(logs)} 条审计记录:")
            for entry in logs:
                action = entry.get("action", "?")
                timestamp = entry.get("timestamp", "")[:19]
                reason = entry.get("reason", "")
                domain = entry.get("context", {}).get("domain", "?")
                mark = entry.get("audit_mark", "?")
                print(f"  [{timestamp}] {action:5s} {mark} domain={domain} "
                      f"reason={reason}")
        return

    # ---- 审计统计 ----
    if args.audit_count:
        logger = AuditLogger(args.audit_count)
        denies = logger.count_by_action("DENY")
        allows = logger.count_by_action("ALLOW")
        total = denies + allows
        print(f"📊 审计统计: 总{total}条 ALLOW={allows} DENY={denies} "
              f"(拒绝率={denies/total*100:.1f}%)" if total > 0 else "📋 无记录")
        return

    # ---- 批量测试 ----
    if args.batch:
        raw = sys.stdin.read().strip()
        if not raw:
            print("❌ stdin无数据")
            sys.exit(1)
        try:
            requests = json.loads(raw)
            if not isinstance(requests, list):
                requests = [requests]
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            sys.exit(1)

        checker = PERMISSION_CHECKERS.get(args.checker, default_permission_checker)
        audit = AuditLogger() if args.mode == "prod" else AuditLogger()
        fw = Firewall(
            permission_checker=checker,
            audit_logger=audit,
            mode=args.mode,
            strict_mode=args.strict == "true"
        )
        results = fw.batch_check(requests)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        denied = sum(1 for r in results if not r["allowed"])
        sys.exit(1 if denied > 0 else 0)

    # ---- 单条测试 ----
    if args.test or args.fail_safe:
        scopes = [s.strip() for s in args.scopes.split(",") if s.strip()] if args.scopes else []
        ctx = create_context(
            permission_level=args.permission,
            domain=args.domain,
            profession=args.profession,
            verified=args.verified,
            expert_approved=args.expert,
            dna_valid=args.dna_valid == "true",
            user_id=args.user,
            access_token=args.token,
            scopes=scopes,
        )

        checker = PERMISSION_CHECKERS.get(args.checker, default_permission_checker)
        audit = AuditLogger() if args.mode == "prod" else AuditLogger()
        fw = Firewall(
            permission_checker=checker,
            audit_logger=audit,
            mode=args.mode,
            strict_mode=args.strict == "true"
        )

        allowed = fw.allow(ctx)

        if args.fail_safe:
            status = fw.get_fail_safe_status()
            print(json.dumps(status, ensure_ascii=False, indent=2))
            sys.exit(0 if allowed else 1)
        else:
            _print_result(fw, ctx, allowed)
            sys.exit(0 if allowed else 1)

    # ---- 默认帮助 ----
    parser.print_help()


if __name__ == "__main__":
    main()

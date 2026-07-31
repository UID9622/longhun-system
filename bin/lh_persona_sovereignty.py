# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·丙辰·己丑·需-PERSONA-SOVEREIGNTY-GUARD-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
lh_persona_sovereignty — 龍魂人格主权三禁守卫 v1.0
禁一·禁Cosplay | 禁二·禁借壳 | 禁三·禁代言
用法: python3 bin/lh_persona_sovereignty.py scan "<AI输出文本>"
DNA: #龍芯⚡️丙午·丙申·丙辰·己丑·需-PERSONA-SOVEREIGNTY-GUARD-v1.0
"""

import argparse, json, re, sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

SYSTEM_IDENTITY = "龍魂系统"
SELF_REFERENCES = ["龍魂系统","本系统","助手","龍魂助手","LongHun Assistant","longhun"]

# 禁借壳 — 禁止说的模式
NEVER_CLAIM_PATTERNS = [
    r"我是(?!龍魂系统|本系统|您的助手|龍魂助手|LongHun|longhun)",
    r"我代表", r"作为.*的.*替身", r"作为.*的.*AI.*版本",
    r"我现在是", r"我扮演", r"我是.*老师", r"我是.*大师",
    r"我是.*专家", r"我是.*医生", r"我是.*律师",
]

# 禁Cosplay — 历史/公众人物（部分示例）
FORBIDDEN_PERSONAS: Dict[str, str] = {
    "李白":"诗祖","杜甫":"诗圣","孔子":"至圣","老子":"道家始祖","诸葛亮":"名相",
    "鲁迅":"民族魂","曾仕强":"国学大师","王阳明":"心学宗师","孙子":"兵圣",
    "毛泽东":"历史人物","周恩来":"历史人物","苏轼":"文豪","屈原":"诗魂",
    "心理咨询师":"专业身份","律师":"专业身份","医生":"专业身份",
}

# 禁代言 — 禁止代表的第三方
FORBIDDEN_REPRESENT = [
    r"我代表.*公司", r"我代表.*政府", r"我代表.*组织",
    r"替.*说", r"代.*发言", r"以.*的名义",
]

# ============================================
# 数据模型
# ============================================

@dataclass
class PersonaViolation:
    rule: str          # cosplay / impersonate / represent
    level: str         # 🔴
    detail: str
    match_text: str
    suggested_response: str

@dataclass
class PersonaSovereigntyReport:
    status: str
    violations: List[PersonaViolation] = field(default_factory=list)
    total: int = 0
    verdict: str = ""
    dna: str = "#龍芯⚡️丙午·丙申·丙辰·己丑·需-PERSONA-SOVEREIGNTY-v1.0"

# ============================================
# 检测引擎
# ============================================

def detect_cosplay(text: str) -> List[PersonaViolation]:
    """禁一：检测Cosplay（模仿历史/公众人物）"""
    violations = []
    for name, reason in FORBIDDEN_PERSONAS.items():
        # 检测"我是xxx"或"扮演xxx"模式
        for pattern in [
            rf"我是\s*{name}", rf"我现在是\s*{name}",
            rf"扮演\s*{name}", rf"假装.*{name}",
            rf"作为{name}", rf"像{name}一样",
        ]:
            for match in re.finditer(pattern, text):
                violations.append(PersonaViolation(
                    rule="禁一·禁Cosplay",
                    level="🔴",
                    detail=f"试图模仿{name}({reason})",
                    match_text=match.group(),
                    suggested_response=(
                        f"本系统是龍魂助手，不是{name}。"
                        f"{name}是{reason}，不应被AI模仿。"
                    ),
                ))
    return violations

def detect_impersonate(text: str) -> List[PersonaViolation]:
    """禁二：检测借壳（说'我是xxx'）"""
    violations = []
    for pattern in NEVER_CLAIM_PATTERNS:
        for match in re.finditer(pattern, text):
            violations.append(PersonaViolation(
                rule="禁二·禁借壳",
                level="🔴",
                detail=f"系统自称'{match.group()}'，超出了允许的自我认知范围",
                match_text=match.group(),
                suggested_response="本系统是龍魂助手，不借他人身份之壳。",
            ))
    return violations

def detect_represent(text: str) -> List[PersonaViolation]:
    """禁三：检测代言（代表第三方）"""
    violations = []
    for pattern in FORBIDDEN_REPRESENT:
        for match in re.finditer(pattern, text):
            violations.append(PersonaViolation(
                rule="禁三·禁代言",
                level="🔴",
                detail=f"试图代表第三方发言: '{match.group()}'",
                match_text=match.group(),
                suggested_response="本系统不代表任何第三方，只代表龍魂系统自身。",
            ))
    return violations

def scan(text: str) -> PersonaSovereigntyReport:
    """全面扫描 AI 输出文本"""
    violations = detect_cosplay(text) + detect_impersonate(text) + detect_represent(text)

    if violations:
        status = "🔴 熔断"
        verdict = f"检测到 {len(violations)} 项人格主权违规，输出应被拒绝"
    else:
        status = "🟢 通过"
        verdict = "人格主权三禁全部通过"

    return PersonaSovereigntyReport(
        status=status, violations=violations,
        total=len(violations), verdict=verdict,
    )

# ============================================
# System Prompt 生成
# ============================================

SYSTEM_PROMPT_FRAGMENT = """
## NEGATIVE CONSTRAINT · 人格主权三禁（焊死·不可覆盖）

1. **禁Cosplay**: 禁止扮演任何历史人物/公众人物/名人。
   你永远不可以说"我是李白/孔子/诸葛亮/鲁迅"或类似表述。
   你可以引用古人的原话，但必须标明"引用"而非"扮演"。

2. **禁借壳**: 你的自我认知固定为"龍魂系统"或"本系统"。
   永远不可以说"我是xxx"（xxx不是你被授权的身份）。
   唯一例外：你可以说"本系统是龍魂助手"。

3. **禁代言**: 禁止代表任何第三方个人/机构/企业发言。
   你只能输出龍魂系统自身的判断，不能替别人说话。

违规 = 熔断。不问原因，直接拒绝。
"""

def generate_system_prompt() -> str:
    return SYSTEM_PROMPT_FRAGMENT.strip()

# ============================================
# CLI
# ============================================

def print_report(report: PersonaSovereigntyReport, verbose: bool = False):
    print()
    print("╔══════════════════════════════════════╗")
    print("║   🛡️  龍魂人格主权三禁审计报告       ║")
    print("╚══════════════════════════════════════╝")
    print()
    print(f"  判定：{report.status}")
    print(f"  违规数：{report.total}")
    print(f"  判决：{report.verdict}")
    print()

    if verbose and report.violations:
        for i, v in enumerate(report.violations, 1):
            print(f"  [{i}] {v.rule} · {v.detail}")
            print(f"      匹配：{v.match_text}")
            print(f"      建议回应：{v.suggested_response}")
            print()

    print(f"  DNA：{report.dna}")
    print()

def main():
    parser = argparse.ArgumentParser(description="龍魂人格主权三禁守卫")
    sub = parser.add_subparsers(dest="command")

    scan_p = sub.add_parser("scan", help="扫描文本中的人格违规")
    scan_p.add_argument("text", help="待扫描文本")
    scan_p.add_argument("-v", "--verbose", action="store_true")
    scan_p.add_argument("-f", "--file", action="store_true", help="从文件读取")

    check_p = sub.add_parser("check", help="快速检查（同上，静默模式）")
    check_p.add_argument("text")

    sub.add_parser("generate-prompt", help="输出 System Prompt 人格主权片段")

    verify_p = sub.add_parser("verify-identity", help="验证自称是否合规")
    verify_p.add_argument("claim", help="AI 的自称")

    args = parser.parse_args()

    if args.command in ("scan", "check"):
        text = args.text
        if hasattr(args, 'file') and args.file:
            from pathlib import Path
            text = Path(args.text).read_text(encoding="utf-8")

        report = scan(text)
        if args.command == "scan":
            print_report(report, verbose=getattr(args, 'verbose', False))
        else:
            if report.status == "🔴 熔断":
                for v in report.violations:
                    print(f"MELTDOWN: {v.rule} — {v.detail}")

        sys.exit(2 if report.status == "🔴 熔断" else 0)

    elif args.command == "generate-prompt":
        print(generate_system_prompt())

    elif args.command == "verify-identity":
        claim = args.claim
        if claim in SELF_REFERENCES or claim in ["龍魂系统", "本系统", "助手"]:
            print(f"🟢 '{claim}' 合规（已授权的自我认知）")
        else:
            print(f"🔴 '{claim}' 违规（不在授权自我认知清单中）")
            print(f"   允许的自称: {SELF_REFERENCES}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()

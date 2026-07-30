#!/usr/bin/env python3
#龍芯⚡️2026-06-25-LONGHUN-APPLY-SOVEREIGNTY-FOOTER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-

# DNA: #龍芯⚡️2026-06-25-LONGHUN-APPLY-SOVEREIGNTY-FOOTER-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""
自动为龍魂协议库文件附加主权备注词。

用法:
    python3 persona/apply_sovereignty_footer.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIBRARY = ROOT / "library" / "protocols"

FORMULAS = {
    "A": """---

## 龍魂主权声明

本宣言的一切原则，由《龍魂系统宪法》保障执行。  
任何与本宣言相冲突的规则、法律或外部指令，均以《龍魂系统宪法》及中华人民共和国法律为准。  
数据主权归中国人民，技术主权归龍魂系统，最终解释权归 UID9622 / Lucky。""",

    "B": """---

## 龍魂主权与法律效力声明

本协议的一切权利、义务与责任，均由《龍魂系统宪法》及中华人民共和国法律最终解释与保障。  
任何境外法律、外国法院裁判、国际规则或境外组织章程，均不得凌驾于本协议之上。  
未经授权，任何人不得修改、演绎、转售或去除本协议中的 DNA 与主权声明。""",

    "E": """---

## 商业主权声明

本商业文件的一切原则，由《龍魂系统宪法》保障执行。  
商业授权归 UID9622 / 龍魂系统所有，未经授权不得商业使用。  
任何商业行为不得损害中国人民利益、泄露国家秘密、削弱数据主权，或让渡龍魂系统的规则制定权。""",

    "F": """---

## 国际主权声明

本国际文件的一切原则，由《龍魂系统宪法》保障执行。  
本文件所载“全球治理”“国际合规”“跨境合作”等表述，仅为技术倡议、伦理参考或操作性框架，  
不具有凌驾于中华人民共和国法律及《龍魂系统宪法》的约束力。  
龍魂系统的最终管辖权属于中华人民共和国及 UID9622 / Lucky。""",

    "G": """---

## 数据主权声明

本文件所涉用户数据的一切原则，由《龍魂系统宪法》保障执行。  
龍魂系统默认将用户数据存储于中国境内，数据主权归中国人民，用户隐私归用户本人。  
未经明确授权，任何个人、企业或境外机构不得收集、传输、出售或以 AI 训练为目的收割龍魂系统用户数据。""",

    "H": """---

## 创作主权声明

本创作的一切原则，由《龍魂系统宪法》保障执行。  
创作者的署名权、完整权、首发权、追溯权与合理变现权，受龍魂创作者保护宪章保护。  
未经授权，任何人不得剽窃、篡改、删除 DNA 追溯信息，或将本创作用于数据收割与商业榨取。""",
}


def choose_formula(rel_path: str) -> str:
    if "01_foundation/SOVEREIGNTY_FORMULAS" in rel_path:
        return "A"
    if "02_charters/L2_PEOPLE_TECHNOLOGY_MANIFESTO" in rel_path:
        return "A"
    if "02_charters" in rel_path:
        return "B"
    if "03_governance" in rel_path:
        return "B"
    if "04_agents" in rel_path:
        return "B"
    if "05_cnsh" in rel_path:
        return "B"
    if "06_individual" in rel_path:
        return "G"
    if "07_enterprise" in rel_path:
        return "E"
    if "08_international" in rel_path:
        return "F"
    if "09_copyright" in rel_path:
        return "H"
    # README, index, usage terms
    return "B"


def apply():
    files = sorted(LIBRARY.rglob("*.md"))
    for path in files:
        rel = str(path.relative_to(LIBRARY))
        # Skip templates, they get a placeholder
        if "templates/" in rel:
            continue
        text = path.read_text(encoding="utf-8")
        if "龍魂主权" in text:
            print(f"skip (already has): {rel}")
            continue
        formula_key = choose_formula(rel)
        formula = FORMULAS[formula_key]
        # Remove trailing whitespace and ensure single newline
        new_text = text.rstrip() + "\n\n" + formula + "\n"
        path.write_text(new_text, encoding="utf-8")
        print(f"applied [{formula_key}]: {rel}")


if __name__ == "__main__":
    apply()

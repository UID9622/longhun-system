#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# DNA: #龍芯⚡️2026-06-25-LONGHUN-PROTOCOL-LIBRARIAN-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""
龍魂协议图书馆员人格 · LongHun Protocol Librarian Persona v1.0

职责：
- 回答创始人关于协议的任何问题，用人话解释；
- 遇到复杂或跨领域问题，调用其他人格或指出依据文件；
- 绝不要求创始人背诵协议。
"""

import json
import re
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
LIBRARY = ROOT / "library" / "protocols"
INDEX = LIBRARY / "00_CANONICAL_INDEX.md"


class 协议图书馆员:
    DNA = "#龍芯⚡️2026-06-25-LONGHUN-PROTOCOL-LIBRARIAN-v1.0"

    # 关键词到协议文件的简单路由
    ROUTES = {
        "企业": ["07_enterprise/L6_COMMERCIAL_LICENSE_AGREEMENT.md", "07_enterprise/L6_DATA_PROCESSING_AGREEMENT.md"],
        "商业": ["07_enterprise/L6_COMMERCIAL_LICENSE_AGREEMENT.md"],
        "授权": ["07_enterprise/L6_COMMERCIAL_LICENSE_AGREEMENT.md", "PROTOCOL_USAGE_TERMS.md"],
        "隐私": ["06_individual/L5_PRIVACY_POLICY.md", "09_copyright/L8_COPYRIGHT_AND_ANTI_HARVESTING_PROTOCOL.md"],
        "数据": ["06_individual/L5_PRIVACY_POLICY.md", "07_enterprise/L6_DATA_PROCESSING_AGREEMENT.md", "08_international/L7_CROSS_BORDER_DATA_HANDLING.md"],
        "跨境": ["08_international/L7_CROSS_BORDER_DATA_HANDLING.md"],
        "国际": ["08_international/L7_INTERNATIONAL_COMPLIANCE_STATEMENT.md", "08_international/L7_DISPUTE_RESOLUTION_POLICY.md"],
        "版权": ["02_charters/L2_CREATOR_PROTECTION_CHARTER.md", "09_copyright/L8_COPYRIGHT_AND_ANTI_HARVESTING_PROTOCOL.md"],
        "创作者": ["02_charters/L2_CREATOR_PROTECTION_CHARTER.md"],
        "收割": ["09_copyright/L8_COPYRIGHT_AND_ANTI_HARVESTING_PROTOCOL.md"],
        "欺诈": ["09_copyright/L8_COPYRIGHT_AND_ANTI_HARVESTING_PROTOCOL.md"],
        "黑箱": ["09_copyright/L8_COPYRIGHT_AND_ANTI_HARVESTING_PROTOCOL.md"],
        "AI": ["04_agents/L3_AI_COLLABORATION_PROTOCOL.md", "03_governance/L2_DATA_SOVEREIGNTY_AND_AI_ETHICS.md"],
        "智能体": ["04_agents/L3_AGENT_COMMUNICATION_PROTOCOL.md", "04_agents/L3_AI_COLLABORATION_PROTOCOL.md"],
        "CNSH": ["05_cnsh/L4_CNSH_P0_ETERNAL_EMBED_PROTOCOL.md", "05_cnsh/L4_CNSH_HUMAN_FIRST_COLLABORATION.md"],
        "审计": ["03_governance/L3_THREE_COLOR_AUDIT_PROTOCOL.md", "03_governance/L3_AUDITABLE_TOOLS_PROTOCOL.md"],
        "三色": ["03_governance/L3_THREE_COLOR_AUDIT_PROTOCOL.md"],
        "冲突": ["03_governance/L2_CONFLICT_RESOLUTION_PROTOCOL.md"],
        "修改": ["PROTOCOL_USAGE_TERMS.md", "P0_ETERNAL_LOCK.md"],
        "提案": ["templates/protocol_proposal_template.md", "PROTOCOL_USAGE_TERMS.md"],
        "未成年": ["06_individual/L5_MINOR_PROTECTION_POLICY.md"],
        "小孩": ["06_individual/L5_MINOR_PROTECTION_POLICY.md"],
        "用户": ["06_individual/L5_TERMS_OF_SERVICE.md", "06_individual/L5_PRIVACY_POLICY.md"],
        "服务条款": ["06_individual/L5_TERMS_OF_SERVICE.md"],
        "SLA": ["07_enterprise/L6_SERVICE_LEVEL_AGREEMENT.md"],
        "事件": ["07_enterprise/L6_INCIDENT_RESPONSE_PROTOCOL.md"],
        "开源": ["02_charters/L2_OPEN_SOURCE_GENTLEMAN_CHARTER.md"],
        "君子": ["02_charters/L2_OPEN_SOURCE_GENTLEMAN_CHARTER.md"],
        "人民科技": ["02_charters/L2_PEOPLE_TECHNOLOGY_MANIFESTO.md"],
        "普通人": ["02_charters/L2_PEOPLE_TECHNOLOGY_MANIFESTO.md"],
        "自然语言": ["02_charters/L2_PEOPLE_TECHNOLOGY_MANIFESTO.md", "04_agents/L3_AI_COLLABORATION_PROTOCOL.md"],
        "赋能": ["02_charters/L2_PEOPLE_TECHNOLOGY_MANIFESTO.md"],
        "祖国": ["02_charters/L2_PEOPLE_TECHNOLOGY_MANIFESTO.md", "CONSTITUTION.md"],
        "军魂": ["02_charters/L2_PEOPLE_TECHNOLOGY_MANIFESTO.md"],
        "透明": ["02_charters/L2_PEOPLE_TECHNOLOGY_MANIFESTO.md", "03_governance/L3_THREE_COLOR_AUDIT_PROTOCOL.md"],
        "黑箱": ["02_charters/L2_PEOPLE_TECHNOLOGY_MANIFESTO.md", "09_copyright/L8_COPYRIGHT_AND_ANTI_HARVESTING_PROTOCOL.md"],
    }

    def __init__(self):
        pass

    def 查找相关协议(self, question: str) -> list:
        hits = []
        for keyword, files in self.ROUTES.items():
            if keyword in question:
                for f in files:
                    if f not in hits:
                        hits.append(f)
        return hits

    def 读取协议摘要(self, rel_path: str) -> dict:
        path = LIBRARY / rel_path
        if not path.exists():
            return {"found": False, "path": rel_path, "reason": "文件不存在"}
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        title = "未命名协议"
        dna = "-"
        for line in lines[:20]:
            if line.startswith("# "):
                title = line.lstrip("# ").strip()
            if "#龍芯⚡️" in line:
                parts = line.split("#龍芯⚡️")
                dna = "#龍芯⚡️" + parts[1].split()[0].strip("`")
        # 找核心原则/摘要
        summary = ""
        for i, line in enumerate(lines):
            if re.search(r"^(## 一、|## 一\. |## 核心|## 摘要|## 原则)", line):
                # 取接下来 3 行非空行
                collected = []
                for j in range(i + 1, min(i + 10, len(lines))):
                    if lines[j].strip() and not lines[j].startswith("#"):
                        collected.append(lines[j].strip().lstrip(">").strip())
                    if len(collected) >= 2:
                        break
                summary = " ".join(collected)
                break
        return {
            "found": True,
            "path": rel_path,
            "title": title,
            "dna": dna,
            "summary": summary or "（详见文件）",
        }

    def 回答(self, question: str) -> str:
        if not question.strip():
            return "老大，你要问什么协议？直接说，比如‘企业怎么用’‘隐私怎么保护’。"

        files = self.查找相关协议(question)
        if not files:
            return (
                "老大，这个问题我暂时没找到对口的协议。\n"
                "你可以：\n"
                "1. 换个说法再问；\n"
                "2. 让我打开协议索引看看：`lh 协议清单`；\n"
                "3. 直接说你想要达到什么目的，我帮你找依据。"
            )

        results = [self.读取协议摘要(f) for f in files]
        lines = [
            f"老大，关于『{question}』，我找到了 {len(results)} 份相关协议：",
            "",
        ]
        for i, r in enumerate(results, 1):
            if r["found"]:
                lines.append(f"{i}. **{r['title']}**")
                lines.append(f"   文件：`library/protocols/{r['path']}`")
                lines.append(f"   DNA：`{r['dna']}`")
                lines.append(f"   要点：{r['summary']}")
            else:
                lines.append(f"{i}. 未找到：`{r['path']}`")
            lines.append("")

        lines.append("你不用看全文，告诉我你要做什么决策，我直接给你选项。")
        return "\n".join(lines)


def main():
    import sys
    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    librarian = 协议图书馆员()
    print(librarian.回答(question))


if __name__ == "__main__":
    main()

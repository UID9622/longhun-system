# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 公开内容主权审查器

在内容对外发布前，调用 CNSH 内容主权协议 v2.1 进行四层检查：
  1. 逻辑校验
  2. 价值观校验
  3. 技术校验
  4. 主权字熔断（繁体龍）

审查不删改内容，只输出风险报告，最终发布决定权归 UID9622。
DNA:#龍芯⚡️2026-06-30-LONGHUN-CONTENT-REVIEW-FILE1-v1.0
"""

import argparse
import json
import sys
from pathlib import Path

SKILL_DIR = Path.home() / ".kimi-code" / "skills" / "content_sovereignty_protocol_v2.1"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

try:
    import importlib.util
    _csp_path = SKILL_DIR / "content_sovereignty_protocol_v2.1.py"
    _spec = importlib.util.spec_from_file_location("content_sovereignty_protocol_v2_1", str(_csp_path))
    _csp = importlib.util.module_from_spec(_spec)
    sys.modules["content_sovereignty_protocol_v2_1"] = _csp
    _spec.loader.exec_module(_csp)
    ContentSovereigntyProtocol = _csp.ContentSovereigntyProtocol
    IronLawGate = _csp.IronLawGate
except Exception as e:
    print(f"🔴 无法加载内容主权协议: {e}")
    sys.exit(1)


class 公开内容审查器:
    def __init__(self):
        self.协议 = ContentSovereigntyProtocol()

    def 审查(self, 内容: str, 内容类型: str = "text") -> dict[str, Any]:
        return self.协议.validate_content_against_protocol(内容, 内容类型)

    def 生成报告(self, 内容: str) -> str:
        结果 = self.审查(内容)
        报告 = [
            "# 🐉 龍魂公开内容主权审查报告",
            f"**内容哈希**: `{结果['content_hash']}`",
            f"**审查状态**: {结果['tricolor']}",
            f"**通过率**: {结果['pass_rate']:.1%}",
            "",
            "## 检查项",
        ]
        for key, val in 结果['checks'].items():
            状态 = "✅" if val else "❌"
            报告.append(f"- {状态} {key}: {val}")

        if 结果.get('gate_issues'):
            报告.extend(["", "## 铁律自审闸告警"])
            for issue in 结果['gate_issues']:
                报告.append(f"- {issue}")

        if 结果.get('dragon_issues'):
            报告.extend(["", "## 主权字熔断"])
            for issue in 结果['dragon_issues']:
                报告.append(f"- {issue}")

        报告.extend(["", f"**DNA**: `{结果['dna']}`"])
        return "\n".join(报告)


def main():
    解析器 = argparse.ArgumentParser(description="龍魂公开内容主权审查器")
    解析器.add_argument("内容", help="要审查的文本内容，或用 - 从 stdin 读取")
    解析器.add_argument("--类型", "-t", default="text", choices=["text", "code", "markdown"])
    解析器.add_argument("--json", action="store_true", help="输出 JSON 格式")
    args = 解析器.parse_args()

    内容 = args.内容
    if 内容 == "-":
        内容 = sys.stdin.read()

    审查器 = 公开内容审查器()
    if args.json:
        print(json.dumps(审查器.审查(内容, args.类型), ensure_ascii=False, indent=2))
    else:
        print(审查器.生成报告(内容))


if __name__ == "__main__":
    main()

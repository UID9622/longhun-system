# DNA: #龍芯⚡️丙午·乙未·乙丑·井-FIX_DNA-v1.0
#!/Users/zuimeidedeyihan/longhun-system/.venv_longhun_math/bin/python
# -*- coding: utf-8 -*-
"""#龍芯⚡️2026-06-29-CNSH-EDITOR-CORRECT-CLI-v0.1
CNSH 中文编辑器纠错命令行入口
"""
import sys
import argparse
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from cnsh_editor import CNSHEditor


def main():
    parser = argparse.ArgumentParser(description="CNSH 中文编辑器纠错")
    parser.add_argument("input", help="输入文本或文件路径")
    parser.add_argument("--file", action="store_true", help="输入为文件路径")
    parser.add_argument("--output", "-o", help="输出文件路径（默认 stdout）")
    parser.add_argument("--json", action="store_true", help="输出 {M::, CNSH::} 双视角 JSON")
    args = parser.parse_args()

    editor = CNSHEditor()

    if args.file:
        text, rules, audit = editor.correct_file(args.input)
    else:
        text, rules, audit = editor.correct_text(args.input)

    if args.json:
        result = {
            "M::": {
                "type": "cnsh_editor_correction",
                "status": "pass" if audit["audit"] != "🔴" else "reject",
                "payload": {
                    "original": open(args.input).read() if args.file else args.input,
                    "corrected": text,
                    "rules_applied": rules,
                    "audit": audit,
                },
            },
            "CNSH::": {
                "dna": "#龍芯⚡️20260629-CNSH-EDITOR-CORRECTION-v0.1",
                "gate": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
                "seal": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
                "audit": audit["audit"],
                "policy": "pass" if audit["audit"] != "🔴" else "reject",
            },
        }
        out = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        out = f"纠错后文本:\n{text}\n\n应用规则: {', '.join(rules)}\n审计: {audit}"

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
    else:
        print(out)


if __name__ == "__main__":
    main()

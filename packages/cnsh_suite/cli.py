# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 套件 · 命令行接口
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-CNSH-CLI-UID9622

用法:
  cnsh --command "生成DNA: 我的文档"
  cnsh --command "审计内容: 待审计文本"
  cnsh --command "运行CNSH: 输出 '你好'"
  cnsh --status
"""

import sys
import json
import argparse
from .core import CNSHSuite, CNSHEngine

def main():
    parser = argparse.ArgumentParser(
        description="🐉 CNSH 套件 · 命令行接口"
    )
    parser.add_argument("--command", "-c", type=str, help="执行自然语言命令")
    parser.add_argument("--status", "-s", action="store_true", help="查看状态")
    parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出")

    args = parser.parse_args()

    suite = CNSHSuite()

    if args.status:
        result = suite.get_status()
        output = json.dumps(result, ensure_ascii=False, indent=2)
        print(output)
        return

    if args.command:
        result = suite.execute(args.command)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(result.get("message", json.dumps(result, ensure_ascii=False, indent=2)))
        return

    parser.print_help()

if __name__ == "__main__":
    main()

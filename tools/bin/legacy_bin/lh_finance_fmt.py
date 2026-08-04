#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║              CNSH 金融格式化 CLI — lh finance fmt                    ║
║  DNA: #龍芯⚡️丙午·丙申·癸丑·午时·需-FINANCE-FMT-CLI-DB73E295        ║
║  三色审计: 🟢 通过                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_finance_fmt.py cny <金额>           — 人民币大写
  python3 bin/lh_finance_fmt.py thousands <金额>      — 千分位
  python3 bin/lh_finance_fmt.py read <金额>           — 中文读法
  python3 bin/lh_finance_fmt.py parse <文件>          — 解析Notion导出
  python3 bin/lh_finance_fmt.py ledger                — 交互记账
  python3 bin/lh_finance_fmt.py convert <金额> <from> <to> — 单位转换
"""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from L5_服务层.services.finance.cnsh_finance_formatter import (
    number_to_cny_upper,
    format_thousands,
    format_thousands_cn,
    number_to_chinese_read,
    NotionFinanceParser,
    build_finance_report,
    format_report_markdown,
    format_report_json,
    SimpleLedger,
    convert_finance_unit,
)


def cmd_cny(amount: str) -> None:
    """人民币大写转换"""
    try:
        result = number_to_cny_upper(amount)
        print(f"￥{format_thousands(amount)}")
        print(f"大写: {result}")
    except Exception as e:
        print(f"错误: {e}")

def cmd_thousands(amount: str) -> None:
    """千分位格式化"""
    try:
        r1 = format_thousands(amount)
        r2 = format_thousands_cn(amount)
        print(f"数字: {r1}")
        print(f"中文: {r2}")
    except Exception as e:
        print(f"错误: {e}")

def cmd_read(amount: str) -> None:
    """中文读法"""
    try:
        result = number_to_chinese_read(amount)
        print(result)
    except Exception as e:
        print(f"错误: {e}")

def cmd_parse(filepath: str) -> None:
    """解析金融文件"""
    if not os.path.exists(filepath):
        print(f"文件不存在: {filepath}")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    parser = NotionFinanceParser()
    records = []

    if filepath.endswith(".json"):
        data = json.loads(content)
        records = parser.parse_notion_json(data)
    elif filepath.endswith(".csv"):
        records = parser.parse_csv(content)
    else:
        records = parser.parse_markdown_table(content)

    if not records:
        print("未找到金融记录")
        return

    report = build_finance_report(records, title=os.path.basename(filepath))
    md = format_report_markdown(report)
    outpath = filepath.rsplit(".", 1)[0] + "_报表.md"
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(md)
    print(md)
    print(f"\n已保存: {outpath}")

def cmd_ledger() -> None:
    """交互式记账"""
    ledger = SimpleLedger()
    print("CNSH 记账器 v1.0 | 输入 q 退出")
    print("格式: [收/支] [金额] [描述] [标签]")
    print("命令: 汇总 / 导出 / 余额")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            continue
        if line.lower() == "q":
            break
        if line == "汇总":
            print(format_report_markdown(ledger.汇总()))
            continue
        if line == "导出":
            md = ledger.导出Markdown()
            path = f"账本_{ledger.名称}.md"
            with open(path, "w", encoding="utf-8") as f:
                f.write(md)
            print(f"已导出: {path}")
            print(md)
            continue
        if line == "余额":
            print(f"余额: {format_thousands_cn(ledger.余额())}")
            continue
        parts = line.split(maxsplit=3)
        if len(parts) < 2:
            print("格式: [收/支] [金额] [描述] [标签]")
            continue
        direction, amount_str = parts[0], parts[1]
        desc = parts[2] if len(parts) > 2 else ""
        tag = parts[3] if len(parts) > 3 else ""
        try:
            amount = float(amount_str.replace(",", ""))
        except ValueError:
            print(f"无效金额: {amount_str}")
            continue
        if direction in ("收", "收入", "+"):
            ledger.记收入(amount, desc, tag)
            print(f"✓ 记收入 {format_thousands_cn(amount)} {desc}")
        elif direction in ("支", "支出", "-"):
            ledger.记支出(amount, desc, tag)
            print(f"✓ 记支出 {format_thousands_cn(amount)} {desc}")
        else:
            print("请用 收/支 开头")
    # 退出时自动保存
    if ledger.记录:
        md = ledger.导出Markdown()
        path = f"账本_{ledger.名称}.md"
        with open(path, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"自动保存: {path}")

def cmd_convert(amount: str, from_unit: str, to_unit: str) -> None:
    """单位转换"""
    try:
        val = float(amount.replace(",", ""))
        result = convert_finance_unit(val, from_unit, to_unit)
        print(f"{val} {from_unit} = {result:,.2f} {to_unit}")
    except Exception as e:
        print(f"错误: {e}")

def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "cny" and args:
        cmd_cny(args[0])
    elif cmd == "thousands" and args:
        cmd_thousands(args[0])
    elif cmd == "read" and args:
        cmd_read(args[0])
    elif cmd == "parse" and args:
        cmd_parse(args[0])
    elif cmd == "ledger":
        cmd_ledger()
    elif cmd == "convert" and len(args) >= 3:
        cmd_convert(args[0], args[1], args[2])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
价格审计 CLI 工具
DNA: #龍芯⚡️丙午·乙未·辛亥·巳时·䷀乾-PRICE-AUDIT-CLI-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

用法:
  # 快速审计
  python3 cli/audit_cli.py --prices 9.9,10.0,12.0,12.5,9.8

  # 从JSON文件审计
  python3 cli/audit_cli.py --json data/sample_input.json

  # 从CSV文件审计
  python3 cli/audit_cli.py --csv data/prices.csv

  # 交互模式
  python3 cli/audit_cli.py --interactive

  # 查看历史报告
  python3 cli/audit_cli.py --list
"""

import sys
import json
import argparse
import csv
from pathlib import Path
from io import StringIO

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from detector import detect_price_anomaly, quick_check
from models import save_report, list_reports, get_report, get_stats

BANNER = """
╔══════════════════════════════════════════════╗
║  价格透明度审计工具 CLI v1.0                    ║
║  Price Audit Tool - CLI                       ║
║  算法审计平民化 · 人人都是审计员                ║
╚══════════════════════════════════════════════╝
"""


def audit_json(filepath: str):
    """从JSON文件读取并审计。JSON格式见 data/sample_input.json。"""
    path = Path(filepath)
    if not path.exists():
        print(f"❌ 文件不存在: {filepath}")
        sys.exit(1)
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    prices = data.get("prices", [])
    groups = data.get("groups")
    timeseries = data.get("timeseries")
    
    if not prices:
        print("❌ JSON文件中缺少 prices 字段")
        sys.exit(1)
    
    result = detect_price_anomaly(prices, groups=groups, timeseries=timeseries)
    rid = save_report(result)
    _print_result(result, rid)


def audit_csv(filepath: str):
    """从CSV文件审计。CSV格式: price[,group][,time]"""
    path = Path(filepath)
    if not path.exists():
        print(f"❌ 文件不存在: {filepath}")
        sys.exit(1)
    
    prices = []
    groups: dict[str, list[float]] = {}
    timeseries: list[dict] = []
    
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            p = float(row.get("price", 0))
            prices.append(p)
            
            group = row.get("group", "").strip()
            if group:
                groups.setdefault(group, []).append(p)
            
            t = row.get("time", "").strip()
            if t:
                timeseries.append({"time": t, "price": p})
    
    if not prices:
        print("❌ CSV文件中没有 price 列")
        sys.exit(1)
    
    result = detect_price_anomaly(
        prices,
        groups=groups if groups else None,
        timeseries=timeseries if timeseries else None
    )
    rid = save_report(result)
    _print_result(result, rid)


def _print_result(result: dict, report_id: str):
    """格式化打印审计结果。"""
    comp = result.get("composite_assessment", {})
    summary = result.get("data_summary", {})
    
    print(f"\n{'='*50}")
    print(f"  审计报告 #{report_id}")
    print(f"{'='*50}")
    print(f"  数据量:   {summary.get('total_records', 0)} 条")
    print(f"  均价:     {summary.get('mean', 0)}")
    print(f"  中位数:   {summary.get('median', 0)}")
    print(f"  范围:     [{summary.get('min', 0)} - {summary.get('max', 0)}]")
    print(f"{'='*50}")
    
    # IQR
    iqr = result.get("iqr_analysis", {})
    print(f"\n  [L1] IQR统计检测: {iqr.get('verdict', 'N/A')}")
    for o in iqr.get("outliers", []):
        print(f"    ⚠ 价格 {o['price']} ({o['type']}, 偏离均价 {o['deviation']})")
    
    # 分组
    grp = result.get("group_analysis", {})
    print(f"\n  [L2] 用户分组检测: {grp.get('verdict', 'N/A')}")
    if grp.get("group_stats"):
        for name, stat in grp["group_stats"].items():
            print(f"    {name}: 均价{stat['mean']} 中位{stat['median']} ({stat['count']}条)")
    if grp.get("max_diff_pct"):
        print(f"    最大差异: {grp['max_diff_pct']}%")
    
    # 时序
    ts = result.get("timeseries_analysis", {})
    print(f"\n  [L3] 时间序列检测: {ts.get('verdict', 'N/A')}")
    for a in ts.get("anomalies", []):
        direction = "↑上涨" if a.get("direction") == "up" else "↓下跌"
        print(f"    ⚠ {a.get('time')} 价格{a['price']} {direction} (Z={a['z_score']})")
    
    # 综合
    print(f"\n{'='*50}")
    print(f"  [L4] 综合杀熟评分: {comp.get('score', 0)}/100")
    print(f"  {comp.get('emoji', '')} {comp.get('level', 'N/A')}")
    print(f"  建议: {comp.get('advice', 'N/A')}")
    print(f"{'='*50}\n")
    
    if report_id:
        print(f"  报告已保存，ID: {report_id}")


def interactive_mode():
    """交互式审计模式。"""
    print(BANNER)
    print("交互式价格审计模式")
    print("输入价格（每行一个），输入空行结束:\n")
    
    prices = []
    groups: dict[str, list[float]] = {"当前用户": []}
    
    while True:
        try:
            line = input(f"  [{len(prices)+1}] 价格: ").strip()
            if not line:
                break
            p = float(line)
            prices.append(p)
            groups["当前用户"].append(p)
        except ValueError:
            print("  ⚠ 请输入有效数字")
        except (EOFError, KeyboardInterrupt):
            print("\n")
            break
    
    if not prices:
        print("未输入任何价格，退出。")
        return
    
    # 询问其他用户组
    print(f"\n已输入 {len(prices)} 个价格。")
    add_group = input("是否有其他用户的价格数据？(y/n): ").strip().lower()
    if add_group == "y":
        for gname in ["老用户", "VIP用户", "其他"]:
            gp = input(f"  {gname} 价格（逗号分隔，跳过按回车）: ").strip()
            if gp:
                groups[gname] = [float(x.strip()) for x in gp.split(",") if x.strip()]
    
    result = detect_price_anomaly(prices, groups=groups)
    rid = save_report(result)
    _print_result(result, rid)


def main():
    parser = argparse.ArgumentParser(
        description="价格透明度审计工具 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --prices 9.9,10,12,12.5,9.8         快速审计
  %(prog)s --json data/sample.json              从JSON审计
  %(prog)s --csv data/prices.csv                从CSV审计
  %(prog)s --interactive                        交互模式
  %(prog)s --list                               查看历史报告
  %(prog)s --stats                              全局统计
        """
    )
    
    parser.add_argument("--prices", type=str, help="逗号分隔的价格列表")
    parser.add_argument("--json", type=str, help="JSON输入文件路径")
    parser.add_argument("--csv", type=str, help="CSV输入文件路径")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--list", action="store_true", help="列出历史报告")
    parser.add_argument("--report", type=str, help="查看指定ID的报告")
    parser.add_argument("--stats", action="store_true", help="查看全局统计")
    
    args = parser.parse_args()
    
    if args.list:
        reports = list_reports(50)
        print(BANNER)
        print(f"\n历史审计报告 ({len(reports)} 条):\n")
        for r in reports:
            comp = r.get("composite_assessment", {})
            print(f"  [{r.get('report_id', '?')}] {comp.get('emoji','')} "
                  f"评分:{comp.get('score','?')}/100 "
                  f"({r.get('audit_time','?')[:19]})")
        return
    
    if args.stats:
        s = get_stats()
        print(BANNER)
        print(f"\n全局统计:")
        print(f"  总报告: {s['total_reports']}")
        print(f"  可疑报告: {s['suspicious_count']} ({s['suspicious_rate']})")
        print(f"  平均评分: {s['avg_score']}/100")
        return
    
    if args.report:
        r = get_report(args.report)
        if r:
            _print_result(r, args.report)
        else:
            print(f"❌ 报告不存在: {args.report}")
        return
    
    if args.interactive:
        interactive_mode()
        return
    
    if args.prices:
        prices = [float(x.strip()) for x in args.prices.split(",") if x.strip()]
        result = quick_check(prices)
        rid = save_report(result)
        _print_result(result, rid)
        return
    
    if args.json:
        audit_json(args.json)
        return
    
    if args.csv:
        audit_csv(args.csv)
        return
    
    # 无参数默认交互模式
    interactive_mode()


if __name__ == "__main__":
    main()

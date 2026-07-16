#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · DNA 主权检查器

执行 DNA 治理协议：
  - 扫描文件/操作是否违反 DNA 不可转让、不可变现、不可删除原则
  - 登记 UID9622 一票否决
  - 登记家族继承关系

DNA: #龍芯⚡️2026-06-30-LONGHUN-DNA-SOVEREIGNTY-CHECKER-v1.0
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
DNA_DB_PATH = HOME / ".longhun" / "dna_governance.db.json"


def _生成DNA(类型: str) -> str:
    日期 = datetime.now(timezone.utc).strftime("%Y%m%d")
    哈希 = hashlib.sha256(os.urandom(16)).hexdigest()[:8]
    return f"#龍芯⚡️{日期}-{类型.upper()}-{哈希}"


def _加载数据库() -> dict[str, Any]:
    if DNA_DB_PATH.exists():
        try:
            return json.loads(DNA_DB_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "_comment": "DNA 治理数据库：否决记录、继承链、违规记录",
        "vetoes": [],
        "inheritances": [],
        "violations": [],
        "owner": "UID9622",
    }


def _保存数据库(数据: dict[str, Any]) -> None:
    DNA_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    DNA_DB_PATH.write_text(json.dumps(数据, ensure_ascii=False, indent=2), encoding="utf-8")


def _检查文件(路径: Path) -> list[Any]:
    """扫描单个文件是否含 DNA 转让/买卖/删除等敏感词。"""
    违规 = []
    if not 路径.is_file():
        return 违规
    try:
        文本 = 路径.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return 违规

    风险模式 = [
        (r"DNA.*转让|转让.*DNA", "DNA 转让"),
        (r"DNA.*出售|出售.*DNA|拍卖.*DNA", "DNA 出售"),
        (r"DNA.*借用|借用.*DNA", "DNA 借用"),
        (r"贡献.*变现|变现.*贡献|贡献.*提现", "贡献变现"),
        (r"删除.*DNA|覆盖.*DNA|清空.*DNA", "DNA 删除/覆盖"),
        (r"代理.*出境|内核.*代理|第三方.*返回", "内核代理出境"),
    ]
    for pattern, 类型 in 风险模式:
        for match in re.finditer(pattern, 文本, re.IGNORECASE):
            违规.append({
                "file": str(路径),
                "type": 类型,
                "line": 文本[:match.start()].count("\n") + 1,
                "preview": 文本[max(0, match.start()-20):match.end()+20],
            })
    return 违规


def _扫描目录(目录: Path) -> list[Any]:
    违规 = []
    for root, _, files in os.walk(目录):
        for name in files:
            if name.endswith((".py", ".json", ".md", ".txt", ".sh")):
                违规.extend(_检查文件(Path(root) / name))
    return 违规


def _登记否决(理由: str, 目标: str) -> dict[str, Any]:
    数据 = _加载数据库()
    记录 = {
        "dna": _生成DNA("VETO"),
        "owner": 数据.get("owner", "UID9622"),
        "target": 目标,
        "reason": 理由,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "active",
    }
    数据["vetoes"].append(记录)
    _保存数据库(数据)
    return 记录


def _登记继承(原DNA: str, 继承人: str) -> dict[str, Any]:
    数据 = _加载数据库()
    记录 = {
        "dna": _生成DNA("INHERIT"),
        "from": 原DNA,
        "to": 继承人,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pending_review",
    }
    数据["inheritances"].append(记录)
    _保存数据库(数据)
    return 记录


def _报告() -> dict[str, Any]:
    数据 = _加载数据库()
    return {
        "否决记录数": len(数据.get("vetoes", [])),
        "继承记录数": len(数据.get("inheritances", [])),
        "违规记录数": len(数据.get("violations", [])),
        "owner": 数据.get("owner", "UID9622"),
        "db_path": str(DNA_DB_PATH),
    }


def main():
    解析器 = argparse.ArgumentParser(description="龍魂 DNA 主权检查器")
    子命令 = 解析器.add_subparsers(dest="command", required=True)

    p_scan = 子命令.add_parser("扫描", help="扫描目录是否违反 DNA 治理协议")
    p_scan.add_argument("目录", type=Path, help="要扫描的目录")

    p_veto = 子命令.add_parser("否决", help="UID9622 行使一票否决权")
    p_veto.add_argument("理由", help="否决理由")
    p_veto.add_argument("--目标", "-t", default="global", help="否决对象")

    p_inherit = 子命令.add_parser("继承", help="登记家族继承关系")
    p_inherit.add_argument("原DNA", help="被继承的 DNA")
    p_inherit.add_argument("继承人", help="继承人标识/DNA")

    p_report = 子命令.add_parser("报告", help="查看治理记录统计")

    args = 解析器.parse_args()

    if args.command == "扫描":
        违规 = _扫描目录(args.目录)
        数据 = _加载数据库()
        数据["violations"].extend(违规)
        _保存数据库(数据)
        if 违规:
            print(f"🟡 发现 {len(违规)} 处潜在违规")
            for v in 违规[:10]:
                print(f"   [{v['type']}] {v['file']}:{v['line']}")
        else:
            print("🟢 未扫描到 DNA 治理违规")
        print(f"   DNA: #龍芯⚡️2026-06-30-LONGHUN-DNA-SOVEREIGNTY-CHECKER-v1.0")

    elif args.command == "否决":
        记录 = _登记否决(args.理由, args.目标)
        print(f"🟢 已登记否决")
        print(f"   DNA: {记录['dna']}")
        print(f"   目标: {记录['target']}")
        print(f"   理由: {记录['reason']}")

    elif args.command == "继承":
        记录 = _登记继承(args.原DNA, args.继承人)
        print(f"🟢 已登记继承申请")
        print(f"   DNA: {记录['dna']}")
        print(f"   从: {记录['from']} -> 到: {记录['to']}")
        print(f"   状态: {记录['status']}（待 UID9622 复核）")

    elif args.command == "报告":
        print(json.dumps(_报告(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

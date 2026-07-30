#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·表皮系统-PERIMETER-GUARD-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║     🛡️  龍魂 · 表皮系统 · 边界防护引擎 v1.0                   ║
║                                                                  ║
║  生物映射：表皮系统 → 边界防护 → 外部访问控制/权限验证             ║
║  五行归属：金                                                    ║
║                                                                  ║
║  DNA: #龍芯⚡️丙午·辛未·表皮系统-PERIMETER-GUARD-v1.0            ║
╚══════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_perimeter_guard.py --scan         # 扫描边界暴露面
  python3 bin/lh_perimeter_guard.py --check        # 检查权限完整性
  python3 bin/lh_perimeter_guard.py --report       # 边界安全报告
"""

import hashlib
import json
import os
import stat
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = Path.home() / ".longhun" / "ant_colony"
STATE_DIR.mkdir(parents=True, exist_ok=True)
PERIMETER_STATE = STATE_DIR / "perimeter_state.json"

DNA = "#龍芯⚡️丙午·辛未·表皮系统-PERIMETER-GUARD-v1.0"


@dataclass
class PerimeterIssue:
    """边界问题——一个暴露点"""
    issue_id: str
    issue_type: str       # permission / exposure / access / integrity
    target: str
    severity: str         # P0/P1/P2/P3
    description: str
    recommendation: str
    found_at: str


class PerimeterGuard:
    """表皮系统：扫描系统边界，检测异常暴露"""

    # 敏感文件模式
    SENSITIVE_PATTERNS = [
        ".env", ".key", ".pem", ".crt", "credentials", "secret",
        "password", "private", "token", "api_key",
    ]

    # 应该保护的目录
    PROTECTED_DIRS = [
        "bin/", "engine/", "config/", "data/", "keys/",
        ".longhun/", "_private/", "vault/",
    ]

    # 权限阈值
    PERMISSION_CHECKS = {
        "world_readable": {"mask": stat.S_IROTH, "severity": "P2"},
        "world_writable": {"mask": stat.S_IWOTH, "severity": "P0"},
        "group_writable": {"mask": stat.S_IWGRP, "severity": "P1"},
    }

    def __init__(self):
        self.issues: List[PerimeterIssue] = []
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if PERIMETER_STATE.exists():
            return json.loads(PERIMETER_STATE.read_text())
        return {"scans": 0, "last_scan": "", "total_issues_found": 0,
                "total_issues_fixed": 0, "open_issues": []}

    def _save_state(self):
        PERIMETER_STATE.write_text(json.dumps(self.state, ensure_ascii=False, indent=2))

    def scan_permissions(self) -> List[PerimeterIssue]:
        """扫描文件权限——检测过宽的权限"""
        issues = []
        now = datetime.now().isoformat()

        for protected_dir in self.PROTECTED_DIRS:
            dir_path = ROOT / protected_dir
            if not dir_path.exists():
                continue

            for file_path in dir_path.rglob("*"):
                if not file_path.is_file():
                    continue
                if file_path.is_symlink():
                    continue
                if any(x in file_path.parts for x in (".git", "node_modules", "__pycache__", ".venv")):
                    continue

                try:
                    st = file_path.stat()
                    for check_name, check in self.PERMISSION_CHECKS.items():
                        if st.st_mode & check["mask"]:
                            issue_id = hashlib.sha256(
                                f"{file_path}-{check_name}".encode()
                            ).hexdigest()[:10]
                            issues.append(PerimeterIssue(
                                issue_id=issue_id,
                                issue_type="permission",
                                target=str(file_path.relative_to(ROOT)),
                                severity=check["severity"],
                                description=f"文件{check_name}权限开启",
                                recommendation=f"chmod o-rwx {file_path.name}",
                                found_at=now,
                            ))
                except OSError:
                    pass

        return issues

    def scan_sensitive_files(self) -> List[PerimeterIssue]:
        """扫描敏感文件暴露"""
        issues = []
        now = datetime.now().isoformat()

        for pattern in self.SENSITIVE_PATTERNS:
            for file_path in ROOT.rglob(f"*{pattern}*"):
                if not file_path.is_file():
                    continue
                if file_path.is_symlink():
                    continue
                if any(x in file_path.parts for x in (".git", "node_modules", "__pycache__", ".venv", "backups")):
                    continue

                issue_id = hashlib.sha256(
                    f"{file_path}-sensitive".encode()
                ).hexdigest()[:10]
                issues.append(PerimeterIssue(
                    issue_id=issue_id,
                    issue_type="exposure",
                    target=str(file_path.relative_to(ROOT)),
                    severity="P1",
                    description=f"敏感文件暴露：文件名含'{pattern}'",
                    recommendation=f"检查是否需要加密或移到_private/",
                    found_at=now,
                ))

        return issues

    def scan_entry_points(self) -> List[PerimeterIssue]:
        """扫描外部入口点——暴露的API/端口/脚本"""
        issues = []
        now = datetime.now().isoformat()

        # 扫描主API入口
        api_dir = ROOT / "统一入口"
        if api_dir.exists():
            py_files = list(api_dir.rglob("*.py"))
            for pf in py_files[:50]:
                try:
                    content = pf.read_text(encoding="utf-8", errors="ignore")[:2000]
                    # 检查是否有端口绑定
                    if "port" in content.lower() or "0.0.0.0" in content or "host" in content.lower():
                        issue_id = hashlib.sha256(
                            f"{pf}-entry".encode()
                        ).hexdigest()[:10]
                        issues.append(PerimeterIssue(
                            issue_id=issue_id,
                            issue_type="access",
                            target=str(pf.relative_to(ROOT)),
                            severity="P2",
                            description="API入口点暴露",
                            recommendation="确认端口防火墙规则和访问控制",
                            found_at=now,
                        ))
                except Exception:
                    pass

        return issues

    def scan_all(self) -> Dict[str, Any]:
        """完整边界扫描"""
        now = datetime.now().isoformat()
        all_issues = (
            self.scan_permissions()
            + self.scan_sensitive_files()
            + self.scan_entry_points()
        )

        self.issues = all_issues
        self.state["scans"] += 1
        self.state["last_scan"] = now
        self.state["total_issues_found"] += len(all_issues)
        self._save_state()

        # 按严重度分组
        p0 = [i for i in all_issues if i.severity == "P0"]
        p1 = [i for i in all_issues if i.severity == "P1"]
        p2 = [i for i in all_issues if i.severity == "P2"]

        return {
            "dna": DNA,
            "scan_time": now,
            "total_issues": len(all_issues),
            "by_severity": {"P0": len(p0), "P1": len(p1), "P2": len(p2)},
            "issues": [
                {"id": i.issue_id, "type": i.issue_type, "severity": i.severity,
                 "target": i.target, "description": i.description}
                for i in sorted(all_issues, key=lambda x: int(x.severity[1]))
            ],
            "perimeter_health": self._calc_health(len(all_issues), len(p0)),
        }

    def _calc_health(self, total: int, critical: int) -> float:
        """计算表皮健康度"""
        if critical > 0:
            return max(0.1, 1.0 - critical * 0.3)
        base = 1.0 - min(total / 50, 0.5)
        return round(base, 3)

    def report(self) -> Dict[str, Any]:
        """边界安全报告"""
        scan = self.scan_all()

        status = "🟢 边界安全"
        if scan["by_severity"]["P0"] > 0:
            status = "🔴 重大漏洞"
        elif scan["by_severity"]["P1"] > 3:
            status = "🟡 需加固"

        return {
            **scan,
            "status": status,
            "stats": self.state,
            "recommendations": [
                "所有.env/.key文件应放入_private/目录",
                "核心脚本不应全局可写(chmod o-w)",
                "API端口应配置防火墙规则限制外部访问",
                "定期运行本扫描: --scan",
            ],
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·表皮系统·边界防护")
    parser.add_argument("--scan", action="store_true", help="扫描边界")
    parser.add_argument("--check", action="store_true", help="检查权限")
    parser.add_argument("--report", action="store_true", help="安全报告")
    parser.add_argument("--json", action="store_true", help="JSON输出")

    args = parser.parse_args()
    guard = PerimeterGuard()

    if args.scan or args.check:
        result = guard.scan_all()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🛡️ 边界扫描完成: {result['total_issues']}个问题")
            print(f"   P0:{result['by_severity']['P0']} | "
                  f"P1:{result['by_severity']['P1']} | "
                  f"P2:{result['by_severity']['P2']}")
            for iss in result["issues"][:10]:
                icon = "🔴" if iss["severity"] == "P0" else "🟡" if iss["severity"] == "P1" else "🔵"
                print(f"  {icon} [{iss['type']}] {iss['target'][:50]}")
        return 0

    if args.report:
        r = guard.report()
        if args.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            print(f"\n🛡️ {r['status']} · 表皮健康:{r['perimeter_health']:.1%}")
            print(f"   总扫描:{r['stats']['scans']}次 | 累计问题:{r['stats']['total_issues_found']}")
            print(f"   建议:")
            for rec in r["recommendations"]:
                print(f"   → {rec}")
        return 0

    # 默认扫描
    result = guard.scan_all()
    print(f"🛡️ 表皮扫描: {result['total_issues']}个问题 | P0×{result['by_severity']['P0']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

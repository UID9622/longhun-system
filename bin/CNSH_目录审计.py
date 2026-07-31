# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-06-29-CNSH-DIR-AUDIT-UID9622
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-

"""🐉 龍魂引擎：CNSH_目录审计
路径：bin/CNSH_目录审计.py
TODO：请补充详细功能说明（不少于20字）。"""
import os as _os
import sys as _sys
_module_dir = _os.path.dirname(_os.path.abspath(__file__))
if _module_dir not in _sys.path:
    _sys.path.insert(0, _module_dir)
"""
CNSH 目录审计器 v1.0
批量扫描目录内代码文件，聚合三色审计结果，生成总报告。
DNA: #龍芯⚡️2026-06-29-CNSH-DIR-AUDIT-UID9622
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from CNSH_代码审计引擎 import CNSH_代码审计引擎, 引擎配置
from CNSH_通知归档 import 从文件加载配置 as 加载通知配置

# 接入龍魂终端通知与 Notion 公开仪表盘
sys.path.insert(0, "/Users/zuimeidedeyihan/longhun-system")
try:
    from longhun_terminal_notifier import notify as _terminal_notify
    from longhun_notion_dashboard import LongHunNotionDashboard
except Exception:
    _terminal_notify = None
    LongHunNotionDashboard = None

_NOTION_DASHBOARD = LongHunNotionDashboard() if LongHunNotionDashboard else None
if _NOTION_DASHBOARD:
    _NOTION_DASHBOARD.init_dashboard()


class CNSH_目录审计:
    def __init__(
        self,
        目标目录: str,
        输出目录: str = "./CNSH_修复输出",
        扩展名: Optional[List[str]] = None,
        排除目录: Optional[List[str]] = None,
    ):
        self.目标目录 = Path(目标目录).resolve()
        self.输出目录 = Path(输出目录)
        self.输出目录.mkdir(parents=True, exist_ok=True)
        self.扩展名 = set(扩展名 or [".py"])
        self.排除目录 = set(排除目录 or [".git", "__pycache__", "node_modules", "venv", ".venv"])
        self.引擎 = CNSH_代码审计引擎(引擎配置(修复输出目录=str(self.输出目录)))
        self.总报告: Dict[str, any] = {
            "扫描目录": str(self.目标目录),
            "扫描时间": datetime.now(timezone.utc).isoformat(),
            "文件总数": 0,
            "风险文件数": 0,
            "三色摘要": {"🟢": 0, "🟡": 0, "🔴": 0},
            "文件结果": [],
            "DNA": "#龍芯⚡️2026-06-29-CNSH-DIR-AUDIT-UID9622",
        }

    def _应扫描(self, 文件路径: Path) -> bool:
        if 文件路径.suffix not in self.扩展名:
            return False
        for 父目录 in 文件路径.parents:
            if 父目录.name in self.排除目录:
                return False
        return True

    def 扫描(self, 是否修复: bool = True) -> Dict[str, any]:
        文件列表 = [p for p in self.目标目录.rglob("*") if p.is_file() and self._应扫描(p)]
        self.总报告["文件总数"] = len(文件列表)

        for 文件路径 in 文件列表:
            try:
                相对路径 = str(文件路径.relative_to(self.目标目录))
                报告 = self.引擎.审计(str(文件路径))

                if 是否修复:
                    报告 = self.引擎.修复(报告, 是否签名=False)

                self.总报告["三色摘要"]["🟢"] += 报告.三色摘要["🟢"]
                self.总报告["三色摘要"]["🟡"] += 报告.三色摘要["🟡"]
                self.总报告["三色摘要"]["🔴"] += 报告.三色摘要["🔴"]

                if 报告.三色摘要["🔴"] > 0 or 报告.三色摘要["🟡"] > 0:
                    self.总报告["风险文件数"] += 1

                self.总报告["文件结果"].append({
                    "相对路径": 相对路径,
                    "绝对路径": str(文件路径),
                    "文件SM3哈希": 报告.文件SM3哈希,
                    "三色摘要": 报告.三色摘要,
                    "修复后路径": 报告.修复后路径,
                    "修复审计DNA": 报告.修复审计DNA,
                })
            except Exception as e:
                self.总报告["文件结果"].append({
                    "相对路径": str(文件路径.relative_to(self.目标目录)),
                    "错误": str(e),
                })

        return self.总报告

    def 保存总报告(self) -> Path:
        报告名 = f"CNSH_目录审计报告.{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        报告路径 = self.输出目录 / 报告名
        with open(报告路径, "w", encoding="utf-8") as f:
            json.dump(self.总报告, f, ensure_ascii=False, indent=2)
        return 报告路径

    def 格式化摘要(self) -> str:
        摘要 = self.总报告["三色摘要"]
        行 = []
        行.append("╔" + "═" * 60 + "╗")
        行.append("║" + " " * 16 + "CNSH 目录审计摘要" + " " * 25 + "║")
        行.append("╠" + "═" * 60 + "╣")
        行.append(f"║ 扫描目录: {str(self.目标目录):<47} ║")
        行.append(f"║ 文件总数: {self.总报告['文件总数']:<47} ║")
        行.append(f"║ 风险文件: {self.总报告['风险文件数']:<47} ║")
        行.append(f"║ 三色聚合: 🟢 {摘要['🟢']}  🟡 {摘要['🟡']}  🔴 {摘要['🔴']:<29} ║")
        行.append("╚" + "═" * 60 + "╝")
        return "\n".join(行)


if __name__ == "__main__":
    解析器 = argparse.ArgumentParser(description="CNSH 目录审计器")
    解析器.add_argument("--dir", required=True, help="要扫描的目录")
    解析器.add_argument("--out", default="./CNSH_修复输出", help="输出目录")
    解析器.add_argument("--ext", nargs="+", default=[".py"], help="扫描扩展名")
    解析器.add_argument("--no-fix", action="store_true", help="只审计不修复")
    解析器.add_argument("--notify", action="store_true", help="审计完成后发送 SMTP/Notion 归档")
    解析器.add_argument("--public", action="store_true", help="同步到龍魂 Notion 公开仪表盘")
    参数 = 解析器.parse_args()

    审计器 = CNSH_目录审计(参数.dir, 参数.out, 参数.ext)
    审计器.扫描(是否修复=not 参数.no_fix)
    报告路径 = 审计器.保存总报告()
    print(审计器.格式化摘要())
    print(f"\n✅ 总报告已保存: {报告路径}")

    摘要 = 审计器.总报告
    三色 = 摘要["三色摘要"]
    分数 = "🟢" if 三色["🔴"] == 0 and 三色["🟡"] == 0 else "🟡" if 三色["🔴"] == 0 else "🔴"

    # 终端通知（始终尝试）
    if _terminal_notify:
        _terminal_notify(
            "CNSH 目录审计完成",
            f"文件{摘要['文件总数']} 风险{摘要['风险文件数']} 三色{三色}",
            subtitle="龍魂审计",
        )

    # Notion 公开仪表盘
    if 参数.public and _NOTION_DASHBOARD:
        仪表结果 = _NOTION_DASHBOARD.add_audit_record(
            title=f"CNSH 目录审计 {Path(参数.dir).name}",
            module="CNSH代码审计",
            score=分数,
            red=三色["🔴"],
            yellow=三色["🟡"],
            green=三色["🟢"],
            summary=json.dumps({
                "扫描目录": str(审计器.目标目录),
                "文件总数": 摘要["文件总数"],
                "风险文件数": 摘要["风险文件数"],
                "报告路径": str(报告路径),
            }, ensure_ascii=False),
            dna=摘要.get("DNA", "#龍芯⚡️2026-06-29-CNSH-DIR-AUDIT-UID9622"),
        )
        print(f"\n🌐 公开仪表盘: {'已登记' if 仪表结果['ok'] else 仪表结果.get('reason', '失败')}")

    if 参数.notify:
        通知 = 加载通知配置()
        归档结果 = 通知.归档("CNSH 目录审计归档", 审计器.总报告, str(报告路径))
        print("\n📬 归档通知结果:")
        print(f"  SMTP: {'已发送' if 归档结果['smtp']['ok'] else 归档结果['smtp'].get('reason', '失败')}")
        print(f"  Notion: {'已归档' if 归档结果['notion']['ok'] else 归档结果['notion'].get('reason', '失败')}")

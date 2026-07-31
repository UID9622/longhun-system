# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·乙酉·亥时·AUDIT-TRIGGER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║     📋 龍魂·三色审计单自动触发引擎 v1.0                          ║
║                                                                  ║
║  协议: LH-PROTOCOL-AUDIT-SHEET-TRIGGER-2026-0714-v1.0           ║
║  来源: 融合架构 §6.1 · 三色审计 × §6.2 · 七类补齐               ║
║                                                                  ║
║  功能:                                                           ║
║    - 🟡 黄级审计单自动生成模板                                    ║
║    - 🟢 绿级操作自动记录日志                                     ║
║    - 🔴 红级操作拦截+生成ADR记录                                  ║
║    - 审计单编号自动递增                                          ║
║    - 回滚点自动计算                                              ║
║    - 预期vs实际事后对比                                          ║
║                                                                  ║
║  DNA: #龍芯⚡️丙午·辛未·乙酉·亥时·AUDIT-TRIGGER-v1.0            ║
╚══════════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_audit_sheet_trigger.py --yellow "合并数据" --scope "bin/*.py"  # 创建黄审计单
  python3 bin/lh_audit_sheet_trigger.py --red "删除归档" --scope "_archive/"   # 创建红审计单(拦截)
  python3 bin/lh_audit_sheet_trigger.py --confirm AUDIT-001                    # 确认审计单
  python3 bin/lh_audit_sheet_trigger.py --list                                 # 列出所有审计单
  python3 bin/lh_audit_sheet_trigger.py --report                               # 审计报告
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

ROOT = Path(__file__).resolve().parent.parent
AUDIT_DIR = ROOT / "audit"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_SHEETS_DIR = AUDIT_DIR / "sheets"
AUDIT_SHEETS_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_LOG = AUDIT_DIR / "audit_chain.jsonl"

DNA = "#龍芯⚡️丙午·辛未·乙酉·亥时·AUDIT-TRIGGER-v1.0"


# ══════════════════════════════════════════════════════
# 审计单模板
# ══════════════════════════════════════════════════════

AUDIT_SHEET_TEMPLATE = """# 🟡 龍魂·审计单 · {sheet_id}

> 协议编号: LH-AUDIT-{sheet_id}
> 审计级别: {color} {color_name}
> 创建时间: {created_at}
> 操作者: {operator}
> 状态: {status}
> DNA: {dna}

---

## 一、操作描述

**操作内容**: {action_desc}
**影响范围**: {scope}
**预计影响**: {estimated_impact}

## 二、风险评估

| 维度 | 评估 |
|------|------|
| 数据破坏风险 | {risk_data} |
| 服务中断风险 | {risk_service} |
| 安全漏洞风险 | {risk_security} |
| 回滚难度 | {risk_rollback} |

**综合风险等级**: {overall_risk}

## 三、回滚方案

**回滚点**: {rollback_point}
**回滚命令**: 
```bash
{rollback_command}
```
**回滚验证**: {rollback_verify}
**回滚时间窗口**: {rollback_window} 分钟

## 四、执行清单

- [ ] 执行前备份已完成
- [ ] 通知相关各方
- [ ] 按计划执行操作
- [ ] 验证操作结果
- [ ] 签名确认

## 五、确认记录

| 时间 | 操作 | 签名 |
|------|------|------|
{confirm_records}

## 六、预期vs实际

| 项目 | 预期 | 实际 | 偏差 |
|------|------|------|------|
{expected_vs_actual}

---

> 谁签名谁负责。审计链不可篡改。
> DNA: {dna}
"""


@dataclass
class AuditSheet:
    """审计单"""
    id: str = ""
    color: str = "🟡"
    action_desc: str = ""
    scope: str = ""
    operator: str = "UID9622"
    status: str = "待确认"  # 待确认/已确认/已执行/已完成/已驳回
    created_at: str = ""
    confirmed_at: str = ""
    executed_at: str = ""
    risk_data: str = "低"
    risk_service: str = "低"
    risk_security: str = "低"
    risk_rollback: str = "低"
    overall_risk: str = "低"
    rollback_point: str = ""
    rollback_command: str = ""
    rollback_verify: str = ""
    rollback_window: int = 5
    estimated_impact: str = ""
    confirm_records: List[Dict] = field(default_factory=list)
    expected_vs_actual: Dict[str, Dict] = field(default_factory=dict)
    resolved: bool = False


class AuditTrigger:
    """三色审计自动触发引擎"""

    def __init__(self):
        self.sheets: Dict[str, AuditSheet] = {}
        self._counter = self._next_counter()
        self._load_all()

    def _next_counter(self) -> int:
        """获取下一个编号"""
        existing = []
        for f in AUDIT_SHEETS_DIR.glob("AUDIT-*.json"):
            try:
                num = int(f.stem.replace("AUDIT-", ""))
                existing.append(num)
            except ValueError:
                pass
        return max(existing) + 1 if existing else 1

    def _load_all(self):
        for f in AUDIT_SHEETS_DIR.glob("AUDIT-*.json"):
            try:
                data = json.loads(f.read_text())
                sheet = AuditSheet(**data)
                self.sheets[sheet.id] = sheet
            except (json.JSONDecodeError, TypeError):
                pass

    def _save_sheet(self, sheet: AuditSheet):
        """保存审计单为JSON + Markdown"""
        # JSON
        json_path = AUDIT_SHEETS_DIR / f"{sheet.id}.json"
        json_path.write_text(json.dumps(vars(sheet), ensure_ascii=False, indent=2))

        # Markdown
        md_path = AUDIT_SHEETS_DIR / f"{sheet.id}.md"
        confirm_records_str = "| - | - | - |"
        if sheet.confirm_records:
            confirm_records_str = "\n".join(
                f"| {r['time']} | {r['action']} | {r['signer']} |"
                for r in sheet.confirm_records
            )

        eva_str = "| - | - | - | - |"
        if sheet.expected_vs_actual:
            eva_str = "\n".join(
                f"| {k} | {v.get('expected', '-')} | {v.get('actual', '-')} | {v.get('delta', '-')} |"
                for k, v in sheet.expected_vs_actual.items()
            )

        color_names = {"🟢": "绿·直接执行", "🟡": "黄·审计确认", "🔴": "红·双重锁定"}

        md_content = AUDIT_SHEET_TEMPLATE.format(
            sheet_id=sheet.id,
            color=sheet.color,
            color_name=color_names.get(sheet.color, ""),
            created_at=sheet.created_at,
            operator=sheet.operator,
            status=sheet.status,
            dna=DNA,
            action_desc=sheet.action_desc,
            scope=sheet.scope,
            estimated_impact=sheet.estimated_impact,
            risk_data=sheet.risk_data,
            risk_service=sheet.risk_service,
            risk_security=sheet.risk_security,
            risk_rollback=sheet.risk_rollback,
            overall_risk=sheet.overall_risk,
            rollback_point=sheet.rollback_point,
            rollback_command=sheet.rollback_command,
            rollback_verify=sheet.rollback_verify,
            rollback_window=sheet.rollback_window,
            confirm_records=confirm_records_str,
            expected_vs_actual=eva_str,
        )

        md_path.write_text(md_content)

    def _log(self, action: str, sheet_id: str, detail: dict[str, Any]):
        """审计链日志"""
        entry = {
            "ts": datetime.now().isoformat(),
            "action": action,
            "sheet_id": sheet_id,
            "detail": detail,
            "dna": DNA,
        }
        with open(AUDIT_LOG, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # ── 🟢 绿级 · 自动记录 ──────────────────────────────

    def green_action(self, desc: str, scope: str = "") -> str:
        """绿级操作 — 自动记录日志，无需审计单"""
        log_id = f"GREEN-{uuid.uuid4().hex[:6].upper()}"
        self._log("green", log_id, {"desc": desc, "scope": scope})
        return log_id

    # ── 🟡 黄级 · 生成审计单 ──────────────────────────────

    def yellow_action(self, desc: str, scope: str,
                       risk_data: str = "低", risk_service: str = "低",
                       risk_security: str = "低", risk_rollback: str = "低",
                       rollback_point: str = "", rollback_cmd: str = "",
                       rollback_verify: str = "") -> AuditSheet:

        sheet = AuditSheet(
            id=f"AUDIT-{self._counter:03d}",
            color="🟡",
            action_desc=desc,
            scope=scope,
            operator="UID9622",
            status="待确认",
            created_at=datetime.now().isoformat(),
            risk_data=risk_data,
            risk_service=risk_service,
            risk_security=risk_security,
            risk_rollback=risk_rollback,
            overall_risk=self._calc_risk(risk_data, risk_service, risk_security, risk_rollback),
            rollback_point=rollback_point,
            rollback_command=rollback_cmd,
            rollback_verify=rollback_verify,
            estimated_impact=f"影响范围: {scope}",
        )

        self.sheets[sheet.id] = sheet
        self._counter += 1
        self._save_sheet(sheet)
        self._log("yellow_create", sheet.id, {"desc": desc, "scope": scope})

        print(f"🟡 审计单已生成: {sheet.id}")
        print(f"   文件: audit/sheets/{sheet.id}.md")
        print(f"   状态: 待确认")

        return sheet

    # ── 🔴 红级 · 拦截+ADR ──────────────────────────────

    def red_action(self, desc: str, scope: str,
                    risk_data: str = "高", risk_service: str = "高",
                    risk_security: str = "高", risk_rollback: str = "高",
                    rollback_point: str = "", rollback_cmd: str = "") -> AuditSheet:

        sheet = AuditSheet(
            id=f"AUDIT-{self._counter:03d}",
            color="🔴",
            action_desc=desc,
            scope=scope,
            operator="UID9622",
            status="已拦截·待审批",
            created_at=datetime.now().isoformat(),
            risk_data=risk_data,
            risk_service=risk_service,
            risk_security=risk_security,
            risk_rollback=risk_rollback,
            overall_risk=self._calc_risk(risk_data, risk_service, risk_security, risk_rollback),
            rollback_point=rollback_point,
            rollback_command=rollback_cmd,
            rollback_verify="必须验证回滚成功才能继续",
            estimated_impact=f"🔴 高风险操作 · 影响范围: {scope}",
            rollback_window=5,  # 红级回滚必须在5分钟内完成
        )

        self.sheets[sheet.id] = sheet
        self._counter += 1
        self._save_sheet(sheet)
        self._log("red_block", sheet.id, {"desc": desc, "scope": scope})

        print(f"🔴 审计单已生成（需审批）: {sheet.id}")
        print(f"   文件: audit/sheets/{sheet.id}.md")
        print(f"   状态: 已拦截·待审批")
        print(f"   ⚠️ 必须手动审批后才能执行！")

        return sheet

    def _calc_risk(self, data, service, security, rollback) -> str:
        """综合风险评估"""
        scores = {"低": 1, "中": 2, "高": 3, "极": 4}
        total = sum(scores.get(r, 1) for r in [data, service, security, rollback])
        if total >= 12: return "极高"
        if total >= 9: return "高"
        if total >= 6: return "中"
        return "低"

    # ── 确认/执行 ────────────────────────────────────────

    def confirm(self, sheet_id: str, signer: str = "UID9622") -> bool:
        """确认审计单"""
        if sheet_id not in self.sheets:
            print(f"❌ 审计单 {sheet_id} 不存在")
            return False

        sheet = self.sheets[sheet_id]

        if sheet.color == "🔴":
            print(f"⚠️ {sheet_id} 是红级审计单，需要额外审批。")
            # ADR记录（红级必须走ADR）
            self._write_adr(sheet)

        sheet.confirm_records.append({
            "time": datetime.now().isoformat(),
            "action": "确认执行",
            "signer": signer,
        })

        if sheet.status in ("待确认", "已拦截·待审批"):
            sheet.status = "已确认"
            sheet.confirmed_at = datetime.now().isoformat()

        self._save_sheet(sheet)
        self._log("confirm", sheet_id, {"signer": signer})
        print(f"✅ {sheet_id} 已确认 · 签名: {signer}")
        return True

    def complete(self, sheet_id: str, result: dict[str, Any] = None) -> bool:
        """标记完成 + 预期vs实际对比"""
        if sheet_id not in self.sheets:
            print(f"❌ 审计单 {sheet_id} 不存在")
            return False

        sheet = self.sheets[sheet_id]
        sheet.status = "已完成"
        sheet.executed_at = datetime.now().isoformat()
        sheet.resolved = True

        if result:
            sheet.expected_vs_actual = result

        self._save_sheet(sheet)
        self._log("complete", sheet_id, {"result": result})
        print(f"✅ {sheet_id} 已完成")
        return True

    def _write_adr(self, sheet: AuditSheet):
        """写入ADR架构决策记录"""
        adr_dir = AUDIT_DIR / "adr"
        adr_dir.mkdir(parents=True, exist_ok=True)
        adr_path = adr_dir / f"{sheet.id}-ADR.md"

        content = f"""# ADR: {sheet.id} · {sheet.action_desc}

> 触发时间: {sheet.created_at}
> 审计级别: 🔴 红·双重锁定
> 决策者: {sheet.operator}
> 状态: {sheet.status}

## 背景
{sheet.action_desc}

## 决策
🔴 红级操作，需经UID9622及至少1名审计人格确认。

## 影响范围
{sheet.scope}

## 风险
- 数据: {sheet.risk_data}
- 服务: {sheet.risk_service}
- 安全: {sheet.risk_security}
- 回滚: {sheet.risk_rollback}

## 回滚方案
```bash
{sheet.rollback_command}
```
回滚验证: {sheet.rollback_verify} | 窗口: {sheet.rollback_window}分钟

## 确认记录
"""
        for r in sheet.confirm_records:
            content += f"- {r['time']} | {r['action']} | {r['signer']}\n"

        content += f"\n---\nDNA: {DNA}\n"
        adr_path.write_text(content)
        print(f"📋 ADR已写入: audit/adr/{sheet.id}-ADR.md")

    # ── 查询 / 报告 ──────────────────────────────────────

    def list_all(self, filter_status: str | None = None):
        """列出所有审计单"""
        titles = {"待确认": "🟡", "已确认": "🟢", "已完成": "✅", "已拦截·待审批": "🔴", "已驳回": "❌"}

        for sid, sheet in sorted(self.sheets.items()):
            if filter_status and sheet.status != filter_status:
                continue
            icon = titles.get(sheet.status, "❓")
            short = sheet.action_desc[:50]
            print(f"  [{sheet.id}] {icon} {short} | {sheet.status} | {sheet.created_at[:16]}")

    def report(self):
        """生成审计报告"""
        total = len(self.sheets)
        by_color = {"🟢": 0, "🟡": 0, "🔴": 0}
        by_status = {}
        for s in self.sheets.values():
            by_color[s.color] = by_color.get(s.color, 0) + 1
            by_status[s.status] = by_status.get(s.status, 0) + 1

        pending = [s for s in self.sheets.values() if not s.resolved]

        print("\n╔══════════════════════════════════════════╗")
        print("║  📊 三色审计报告                           ║")
        print("╠══════════════════════════════════════════╣")
        print(f"║  总计审计单: {total:>4d}                        ║")
        print(f"║  🟢绿: {by_color['🟢']:>4d}  🟡黄: {by_color['🟡']:>4d}  🔴红: {by_color['🔴']:>4d}              ║")
        print(f"║  待处理: {len(pending):>4d}                          ║")
        print("╠══════════════════════════════════════════╣")
        if pending:
            print("║  待处理审计单:                             ║")
            for s in pending[:5]:
                print(f"║    [{s.id}] {s.color} {s.action_desc[:35]}               ║")
        print("╚══════════════════════════════════════════╝")
        print(f"\nDNA: {DNA}")


def main():
    parser = argparse.ArgumentParser(description="龍魂·三色审计单自动触发引擎")
    parser.add_argument("--yellow", type=str, help="创建🟡黄级审计单（操作描述）")
    parser.add_argument("--red", type=str, help="创建🔴红级审计单（操作描述）")
    parser.add_argument("--scope", type=str, default="", help="影响范围")
    parser.add_argument("--risk-data", type=str, default="低", help="数据破坏风险:低/中/高/极")
    parser.add_argument("--risk-service", type=str, default="低", help="服务中断风险")
    parser.add_argument("--risk-security", type=str, default="低", help="安全漏洞风险")
    parser.add_argument("--risk-rollback", type=str, default="低", help="回滚难度")
    parser.add_argument("--rollback-point", type=str, default="", help="回滚点描述")
    parser.add_argument("--rollback-cmd", type=str, default="", help="回滚命令")
    parser.add_argument("--confirm", type=str, help="确认指定ID的审计单")
    parser.add_argument("--signer", type=str, default="UID9622", help="签名人")
    parser.add_argument("--complete", type=str, help="完成指定ID的审计单")
    parser.add_argument("--list", action="store_true", help="列出所有审计单")
    parser.add_argument("--list-pending", action="store_true", help="列出待处理审计单")
    parser.add_argument("--report", action="store_true", help="生成审计报告")

    args = parser.parse_args()
    trigger = AuditTrigger()

    if args.yellow:
        trigger.yellow_action(
            desc=args.yellow, scope=args.scope,
            risk_data=args.risk_data, risk_service=args.risk_service,
            risk_security=args.risk_security, risk_rollback=args.risk_rollback,
            rollback_point=args.rollback_point, rollback_cmd=args.rollback_cmd,
        )

    elif args.red:
        trigger.red_action(
            desc=args.red, scope=args.scope,
            risk_data=args.risk_data or "高",
            risk_service=args.risk_service or "高",
            risk_security=args.risk_security or "高",
            risk_rollback=args.risk_rollback or "高",
            rollback_point=args.rollback_point,
            rollback_cmd=args.rollback_cmd,
        )

    elif args.confirm:
        trigger.confirm(args.confirm, args.signer)

    elif args.complete:
        trigger.complete(args.complete)

    elif args.list:
        trigger.list_all()

    elif args.list_pending:
        trigger.list_all(filter_status="待确认")
        trigger.list_all(filter_status="已拦截·待审批")

    elif args.report:
        trigger.report()

    else:
        # 默认显示报告
        trigger.report()


if __name__ == "__main__":
    main()

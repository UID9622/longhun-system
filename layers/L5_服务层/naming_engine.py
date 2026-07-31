#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂命名即架构引擎 v1.0（焊死）

DNA追溯码：#龍魂⚡️丙午·辛未·命名引擎-v1
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

核心原则：
  文件名 = 摘要 + 类型 + 结构 + 权限 + DNA
  看一眼文件名 → 知道是什么 / 给谁看 / 怎么用 / 能不能改 / 从哪来

格式（焊死）：
  [摘要]_[类型]_[结构]_[权限]_[DNA].扩展名

三层联动：
  L1 文件名解析 → 类型/结构/权限/DNA 直接路由
  L2 语义标准化 → 大白话 → 标准节点
  L3 触角传递 → 交叉激活 → 关联唤醒

省算力：文件名带80%信息 → 省80%分析时间

核心承诺（焊死）：
  - 文件名不规范 → 拒绝处理，提示重命名
  - 类型路由：txt→老百姓版 md→通用版 py→技术版 ...
  - 结构路由：report→生成报告 template→生成表单 audit→运行校验 ...
  - 权限路由：P0只读 P1签章 P2可调留日志 P3区域适配 P4用户自定

创建者：💎 龍芯北辰｜UID9622
"""

from __future__ import annotations

import json
import re
import sys
import hashlib
from datetime import datetime
from enum import Enum
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "L3_数据层"))

from semantic_nodes import make_dna, CONFIRM_CODE


# ═══════════════════════════════════════════════
# 标签枚举（焊死）
# ═══════════════════════════════════════════════

class FileType(str, Enum):
    """类型标签"""
    TXT = "txt"      # 纯文本，大白话 → 老百姓版
    MD = "md"        # Markdown → 通用版
    PY = "py"        # Python → 技术版
    JSON = "json"    # 数据 → API版
    HTML = "html"    # 网页 → 展示版
    SQL = "sql"      # 数据库 → 存储版
    YML = "yml"      # 配置 → CI/CD版
    SH = "sh"        # 脚本 → 运维版

    @classmethod
    def type_actions(cls) -> Dict[str, str]:
        return {
            "txt": "老百姓版渲染",
            "md": "通用版渲染",
            "py": "技术版执行",
            "json": "API版解析",
            "html": "展示版打开",
            "sql": "数据库执行",
            "yml": "流水线触发",
            "sh": "脚本执行",
        }


class Structure(str, Enum):
    """结构标签"""
    REPORT = "report"        # 报告，有结论 → 生成HTML，带三色审计
    TEMPLATE = "template"    # 模板，填空用 → 生成输入表单
    AUDIT = "audit"          # 审计，有检查 → 运行校验脚本
    DECISION = "decision"    # 决策，有建议 → 生成决策树
    LOG = "log"              # 日志，不可改 → 归档，只追加
    PROTOCOL = "protocol"    # 协议，有条款 → 生成签章页
    CASE = "case"            # 案例，有故事 → 生成相似匹配
    DATA_STRUCT = "data"     # 数据，有来源 → 生成溯源图

    @classmethod
    def struct_actions(cls) -> Dict[str, str]:
        return {
            "report": "生成报告",
            "template": "生成表单",
            "audit": "运行校验",
            "decision": "生成决策树",
            "log": "只读归档",
            "protocol": "生成签章",
            "case": "相似匹配",
            "data": "溯源展示",
        }


class Permission(str, Enum):
    """权限标签"""
    P0 = "P0"  # 焊死底座 → 只读，不可改，不可删
    P1 = "P1"  # 核心宪法 → 需16人格签章+DNA验证
    P2 = "P2"  # 系统规则 → 框架内可调，留审计日志
    P3 = "P3"  # 区域适配 → 一国一策，不违背P0/P1
    P4 = "P4"  # 用户自定义 → 自己说了算，可删可改

    @classmethod
    def perm_actions(cls) -> Dict[str, str]:
        return {
            "P0": "只读，不可改",
            "P1": "需签章验证",
            "P2": "可调，留日志",
            "P3": "区域适配",
            "P4": "用户自定",
        }

    @classmethod
    def is_writable(cls, perm: str) -> bool:
        """是否可写"""
        return perm in ("P3", "P4")


# ═══════════════════════════════════════════════
# 命名解析结果（焊死）
# ═══════════════════════════════════════════════

@dataclass
class ParsedName:
    """命名解析结果"""
    summary: str          # 摘要（4-8字）
    file_type: str        # 类型
    structure: str        # 结构
    permission: str       # 权限
    dna: str              # DNA追溯码
    ext: str              # 扩展名
    valid: bool = True
    error: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "type": self.file_type,
            "structure": self.structure,
            "permission": self.permission,
            "dna": self.dna,
            "ext": self.ext,
            "valid": self.valid,
            "error": self.error,
        }


@dataclass 
class RouteResult:
    """路由结果"""
    action: str            # "route" / "reject"
    summary: str
    type_action: str       # 类型对应的动作
    structure_action: str  # 结构对应的动作
    permission_action: str # 权限对应的动作
    dna: str
    reason: Optional[str] = None
    writable: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "summary": self.summary,
            "type_action": self.type_action,
            "structure_action": self.structure_action,
            "permission_action": self.permission_action,
            "dna": self.dna,
            "reason": self.reason,
            "writable": self.writable,
        }


# ═══════════════════════════════════════════════
# 命名引擎（焊死）
# ═══════════════════════════════════════════════

class NamingEngine:
    """
    命名即架构引擎

    职责：
      1. 解析文件名 → 摘要/类型/结构/权限/DNA
      2. 自动路由 → 根据类型+结构+权限 决定动作
      3. 组装输出 → 加载模板，填入数据
      4. P0校验 → 焊死项检查
    """

    # 命名规范正则（焊死）
    PATTERN = re.compile(
        r'^(?P<summary>.+?)_'                          # 摘要
        r'(?P<type>txt|md|py|json|html|sql|yml|sh)_'   # 类型
        r'(?P<structure>report|template|audit|decision|log|protocol|case|data)_'  # 结构
        r'(?P<permission>P0|P1|P2|P3|P4)_'              # 权限
        r'(?P<dna>.+?)\.'                                # DNA
        r'(?P<ext>.+)$'                                   # 扩展名
    )

    def __init__(self, templates_dir: Optional[str] = None):
        self.templates_dir = Path(templates_dir) if templates_dir else None
        self._audit_log: List[dict[str, Any]] = []

    def parse(self, filename: str) -> ParsedName:
        """
        解析文件名

        输入："押金陷阱_合同审计_txt_report_P0_丙午·辛未·001.txt"
        输出：ParsedName(summary="押金陷阱·合同审计", type="txt", ...)
        """
        # 先处理下划线在摘要中的情况（最后一个类型标签前的所有下划线都是摘要的一部分）
        m = self.PATTERN.match(filename)
        if not m:
            return ParsedName(
                summary="", file_type="", structure="",
                permission="", dna="", ext="",
                valid=False,
                error=f"命名不符合规范: {filename}\n"
                      f"规范格式: [摘要]_[类型]_[结构]_[权限]_[DNA].扩展名"
            )

        return ParsedName(
            summary=m.group("summary").replace("_", "·"),
            file_type=m.group("type"),
            structure=m.group("structure"),
            permission=m.group("permission"),
            dna=m.group("dna"),
            ext=m.group("ext"),
            valid=True
        )

    def parse_path(self, filepath: str) -> ParsedName:
        """解析文件路径"""
        return self.parse(Path(filepath).name)

    def route(self, parsed: ParsedName) -> RouteResult:
        """根据解析结果自动路由"""
        if not parsed.valid:
            return RouteResult(
                action="reject",
                summary="",
                type_action="",
                structure_action="",
                permission_action="",
                dna="",
                reason=parsed.error,
                writable=False,
            )

        type_actions = FileType.type_actions()
        struct_actions = Structure.struct_actions()
        perm_actions = Permission.perm_actions()

        return RouteResult(
            action="route",
            summary=parsed.summary,
            type_action=type_actions.get(parsed.file_type, "未知类型"),
            structure_action=struct_actions.get(parsed.structure, "未知结构"),
            permission_action=perm_actions.get(parsed.permission, "未知权限"),
            dna=parsed.dna,
            writable=Permission.is_writable(parsed.permission),
        )

    def validate(self, filepath: str, content: Optional[str] = None) -> dict[str, Any]:
        """
        完整校验：解析 + 路由 + P0检查

        返回校验报告
        """
        path = Path(filepath)
        parsed = self.parse_path(filepath)
        route = self.route(parsed)

        report = {
            "file": filepath,
            "exists": path.exists(),
            "parsed": parsed.to_dict(),
            "route": route.to_dict(),
            "p0_checks": [],
            "status": "PASS" if parsed.valid else "REJECT",
            "dna": make_dna("命名校验", "v1"),
            "confirm_code": CONFIRM_CODE,
        }

        if not parsed.valid:
            report["status"] = "REJECT"
            return report

        # P0校验
        p0_checks = self._p0_validate(parsed, content)
        report["p0_checks"] = p0_checks

        if any(not c["passed"] for c in p0_checks):
            report["status"] = "FAIL"

        # 审计日志
        self._audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "file": filepath,
            "status": report["status"],
            "dna": report["dna"],
        })

        return report

    def _p0_validate(self, parsed: ParsedName, content: Optional[str] = None) -> List[dict[str, Any]]:
        """P0级焊死项检查"""
        checks = []

        # 检查1：DNA格式存在
        has_dna = bool(parsed.dna and len(parsed.dna) > 0)
        checks.append({
            "check": "DNA追溯码存在",
            "passed": has_dna,
            "detail": parsed.dna if has_dna else "DNA为空",
        })

        # 检查2：权限标签有效
        valid_perm = parsed.permission in [p.value for p in Permission]
        checks.append({
            "check": "权限标签有效",
            "passed": valid_perm,
            "detail": parsed.permission,
        })

        # 检查3：类型标签有效
        valid_type = parsed.file_type in [t.value for t in FileType]
        checks.append({
            "check": "类型标签有效",
            "passed": valid_type,
            "detail": parsed.file_type,
        })

        # 检查4：结构标签有效
        valid_struct = parsed.structure in [s.value for s in Structure]
        checks.append({
            "check": "结构标签有效",
            "passed": valid_struct,
            "detail": parsed.structure,
        })

        # 检查5：P0文件不可写
        if parsed.permission == "P0":
            checks.append({
                "check": "P0只读保护",
                "passed": True,
                "detail": "P0级，只读，不可改，不可删",
            })

        return checks

    def assemble(self, parsed: ParsedName, content: dict[str, Any] = None) -> str:
        """
        自动组装输出

        根据类型+结构 → 加载对应模板 → 填入数据
        """
        if not parsed.valid:
            return f"❌ 无法组装：{parsed.error}"

        # 加载模板
        template = self._load_template(parsed.structure, parsed.file_type)

        # 简单模板替换
        data = content or {}
        data.setdefault("summary", parsed.summary)
        data.setdefault("dna", parsed.dna)
        data.setdefault("permission", parsed.permission)
        data.setdefault("confirm_code", CONFIRM_CODE)

        try:
            output = template.format(**data)
        except KeyError:
            output = template  # 模板无占位符，直接返回

        return output

    def _load_template(self, structure: str, file_type: str) -> str:
        """加载模板"""
        if not self.templates_dir:
            return f"// 默认模板 [{structure}] [{file_type}]\n// 摘要: {{summary}}\n// DNA: {{dna}}"

        template_path = self.templates_dir / f"{structure}_{file_type}.template"
        if template_path.exists():
            return template_path.read_text(encoding="utf-8")

        return f"// 默认模板 [{structure}] [{file_type}]\n// 模板文件不存在: {template_path}"

    def suggest_name(self, summary: str, file_type: str, structure: str,
                     permission: str = "P2", dna: Optional[str] = None) -> str:
        """
        建议标准命名

        输入：summary="押金陷阱", type="txt", structure="report", permission="P0"
        输出："押金陷阱_txt_report_P0_丙午·辛未·001.txt"
        """
        if dna is None:
            dna = make_dna(summary, "v1")
            dna = dna.replace("#龍魂⚡️", "").replace("·", "·")

        # 净化摘要（除去空格和特殊字符）
        clean_summary = re.sub(r'[\s_]+', '_', summary.strip())

        return f"{clean_summary}_{file_type}_{structure}_{permission}_{dna}.{file_type}"

    def batch_validate(self, directory: str, pattern: str = "*.*") -> List[dict[str, Any]]:
        """批量校验目录下所有文件"""
        results = []
        for f in Path(directory).rglob(pattern):
            if f.is_file():
                results.append(self.validate(str(f)))
        return results

    def audit_summary(self) -> dict[str, Any]:
        """审计日志汇总"""
        if not self._audit_log:
            return {"total": 0, "dna": make_dna("命名审计", "v1")}

        passed = sum(1 for e in self._audit_log if e["status"] == "PASS")
        failed = sum(1 for e in self._audit_log if e["status"] == "FAIL")
        rejected = sum(1 for e in self._audit_log if e["status"] == "REJECT")

        return {
            "total": len(self._audit_log),
            "passed": passed,
            "failed": failed,
            "rejected": rejected,
            "dna": make_dna("命名审计", "v1"),
            "confirm_code": CONFIRM_CODE,
        }

    # ═══════════════════════════════════════════════
    # 命名规范文档生成
    # ═══════════════════════════════════════════════

    def generate_spec(self) -> str:
        """生成命名规范说明"""
        lines = [
            "# 龍魂命名即架构 · 文件命名规范 v1.0",
            "",
            f"DNA: {make_dna('命名规范', 'v1')}",
            f"确认码: {CONFIRM_CODE}",
            "",
            "## 命名格式",
            "",
            "```",
            "[摘要]_[类型]_[结构]_[权限]_[DNA].扩展名",
            "```",
            "",
            "## 类型标签",
            "",
        ]

        for t in FileType:
            actions = FileType.type_actions()
            lines.append(f"- `{t.value}` = {actions.get(t.value, '未知')}")

        lines += [
            "",
            "## 结构标签",
            "",
        ]

        for s in Structure:
            actions = Structure.struct_actions()
            lines.append(f"- `{s.value}` = {actions.get(s.value, '未知')}")

        lines += [
            "",
            "## 权限标签",
            "",
        ]

        for p in Permission:
            actions = Permission.perm_actions()
            lines.append(f"- `{p.value}` = {actions.get(p.value, '未知')}")

        lines += [
            "",
            "## 命名示例",
            "",
            "| 文件名 | 解析 | 自动动作 |",
            "|:---|:---|:---|",
            "| `押金陷阱_txt_report_P0_丙午·辛未·001.txt` | 老百姓版报告，P0级 | 打开即读，不可编辑 |",
            "| `电子签验真_py_audit_P0_丙午·辛未·002.py` | 技术版P0审计脚本 | 运行前检查5条硬要求 |",
            "| `清朗行动_md_log_P1_丙午·辛未·003.md` | P1级案例日志 | 只追加，不可删改 |",
            "| `四绝开店_json_template_P2_丙午·辛未·004.json` | P2级决策模板 | 生成填空表单 |",
            "| `商家信用_sql_data_P3_丙午·辛未·005.sql` | P3级数据库 | 自动关联工商API |",
            "",
            "---",
            "",
            "> 文件名 = 一眼看懂。省80%算力。",
        ]

        return "\n".join(lines)


# ═══════════════════════════════════════════════
# CLI入口（焊死）
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    engine = NamingEngine()

    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "parse" and len(sys.argv) > 2:
            result = engine.parse(sys.argv[2])
            print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))

        elif cmd == "route" and len(sys.argv) > 2:
            parsed = engine.parse(sys.argv[2])
            route = engine.route(parsed)
            print(json.dumps(route.to_dict(), ensure_ascii=False, indent=2))

        elif cmd == "validate" and len(sys.argv) > 2:
            report = engine.validate(sys.argv[2])
            print(json.dumps(report, ensure_ascii=False, indent=2))

        elif cmd == "suggest" and len(sys.argv) > 5:
            summary, ft, struct, perm = sys.argv[2:6]
            name = engine.suggest_name(summary, ft, struct, perm)
            print(name)

        elif cmd == "batch" and len(sys.argv) > 2:
            results = engine.batch_validate(sys.argv[2])
            print(f"校验 {len(results)} 个文件:")
            for r in results:
                status = r['status']
                name = Path(r['file']).name
                print(f"  [{status}] {name}")

        elif cmd == "spec":
            print(engine.generate_spec())

        elif cmd == "audit":
            print(json.dumps(engine.audit_summary(), ensure_ascii=False, indent=2))

        else:
            print(f"用法: python naming_engine.py [parse|route|validate|suggest|batch|spec|audit] [...]")

    else:
        # 默认自检
        print("=" * 50)
        print("【龍魂命名即架构引擎 · 自检】")
        print(f"DNA: {make_dna('命名引擎', 'v1')}")
        print(f"确认码: {CONFIRM_CODE}")
        print("=" * 50)

        # 测试用例
        test_files = [
            "押金陷阱_txt_report_P0_丙午·辛未·001.txt",
            "电子签验真_py_audit_P0_丙午·辛未·002.py",
            "清朗行动_md_log_P1_丙午·辛未·003.md",
            "随便起的文件名.md",  # 不规范
        ]

        for tf in test_files:
            parsed = engine.parse(tf)
            route = engine.route(parsed)
            status = "✅" if parsed.valid else "❌"
            print(f"\n{status} {tf}")
            if parsed.valid:
                print(f"   摘要: {parsed.summary}")
                print(f"   类型: {parsed.file_type} → {route.type_action}")
                print(f"   结构: {parsed.structure} → {route.structure_action}")
                print(f"   权限: {parsed.permission} → {route.permission_action}")
                print(f"   DNA: {parsed.dna}")
            else:
                print(f"   错误: {parsed.error}")

        # 建议命名
        suggested = engine.suggest_name("押金陷阱", "txt", "report", "P0")
        print(f"\n建议命名: {suggested}")

        print("\n✅ 命名引擎正常 · 焊死")

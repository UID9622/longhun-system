#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-AUDIT-PLUGIN-v1.0-5A3F8C1D
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║              龍魂 B4 审计插件基类 · 可插拔架构 v1.0                      ║
║              Pluggable Audit Plugin Architecture                         ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-AUDIT-PLUGIN-v1.0-5A3F8C1D                     ║
║  哲学锚: 河图洛书中五不动点 → 四象审计 → 八卦分类                        ║
║  铁律: 所有B4审计操作只读·不可修改系统状态                               ║
╚══════════════════════════════════════════════════════════════════════════╝

用途:
    - 为所有 B4 审计命令提供统一的插件基类
    - 支持动态注册/发现审计插件
    - 生成标准化三色审计报告
    - 所有审计插件为只读操作

使用:
    from bin.audit_plugin_base import AuditPlugin, AuditResult, AuditPluginRegistry
"""

import json
import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from collections.abc import Callable
from pathlib import Path


# ═══════════════════════════════════════════════════════════════
# 审计结果数据结构
# ═══════════════════════════════════════════════════════════════

class AuditLevel(Enum):
    """审计级别枚举 · 对应河图四象"""
    L0_ETERNAL = "L0"    # 永恒·河图中五 → 不可降级
    L1_CORE = "L1"       # 核心·东木 → 高优先级
    L2_MODULE = "L2"     # 模块·南火 → 中优先级
    L3_AUX = "L3"        # 辅助·西金/北水 → 低优先级


class AuditStatus(Enum):
    """三色审计状态"""
    GREEN = "🟢"     # 通过
    YELLOW = "🟡"    # 警告
    RED = "🔴"       # 拒绝


@dataclass
class AuditFinding:
    """单个审计发现"""
    level: str              # "error" | "warning" | "info"
    message: str            # 中文描述
    location: str = ""      # 代码位置（如"第12行"）
    evidence: str = ""      # 证据摘要
    suggestion: str = ""    # 修复建议


@dataclass
class AuditResult:
    """审计结果"""
    plugin_name: str
    plugin_version: str
    dna: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    status: AuditStatus = AuditStatus.GREEN
    findings: list[AuditFinding] = field(default_factory=list)
    summary: dict[str, int] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_finding(self, finding: AuditFinding):
        """添加审计发现并自动更新状态"""
        self.findings.append(finding)
        if finding.level == "error":
            self.status = AuditStatus.RED
        elif finding.level == "warning" and self.status != AuditStatus.RED:
            self.status = AuditStatus.YELLOW

    def finalize(self):
        """完成审计·统计摘要"""
        self.summary = {"error": 0, "warning": 0, "info": 0}
        for f in self.findings:
            if f.level in self.summary:
                self.summary[f.level] += 1

    def to_dict(self) -> dict[str, object]:
        return {
            "plugin": self.plugin_name,
            "version": self.plugin_version,
            "dna": self.dna,
            "timestamp": self.timestamp,
            "status": self.status.value,
            "findings": [
                {"level": f.level, "message": f.message, "location": f.location,
                 "evidence": f.evidence, "suggestion": f.suggestion}
                for f in self.findings
            ],
            "summary": self.summary,
        }

    def to_report(self) -> str:
        """生成中文审计报告"""
        lines = []
        lines.append("╔═══════════════════════════════════════════════════════╗")
        lines.append(f"║  🐉 龍魂审计报告 · {self.plugin_name} v{self.plugin_version}")
        lines.append("╠═══════════════════════════════════════════════════════╣")
        lines.append(f"║  DNA: {self.dna}")
        lines.append(f"║  时间: {self.timestamp[:19]}")
        lines.append(f"║  结果: {self.status.value} "
                     f"(错误:{self.summary.get('error',0)} "
                     f"警告:{self.summary.get('warning',0)} "
                     f"信息:{self.summary.get('info',0)})")
        lines.append("╠═══════════════════════════════════════════════════════╣")
        if not self.findings:
            lines.append("║  ✅ 无问题发现")
        else:
            for f in self.findings:
                icon = {"error": "🔴", "warning": "🟡", "info": "ℹ️"}.get(f.level, "•")
                loc = f" [{f.location}]" if f.location else ""
                lines.append(f"║  {icon} {f.message}{loc}")
                if f.suggestion:
                    lines.append(f"║     💡 {f.suggestion}")
        lines.append("╚═══════════════════════════════════════════════════════╝")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# 审计插件基类
# ═══════════════════════════════════════════════════════════════

class AuditPlugin(ABC):
    """
    审计插件基类 · B4层统一接口

    所有 B4 审计命令必须继承此类。
    铁律：审计操作为只读，不得修改系统状态。
    """

    # 子类必须定义
    name: str = "unnamed"
    version: str = "1.0"
    dna: str = "#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-AUDIT-PLUGIN-v1.0"
    level: AuditLevel = AuditLevel.L2_MODULE

    @abstractmethod
    def audit(self, target: Any = None) -> AuditResult:
        """
        执行审计

        Args:
            target: 可选审计目标（文件路径/代码内容/配置等）

        Returns:
            AuditResult: 标准化审计结果（只读，不修改系统状态）
        """
        ...

    def get_name(self) -> str:
        return self.name

    def get_level(self) -> AuditLevel:
        return self.level

    def quick_check(self, content: str) -> AuditStatus:
        """
        快速审计·不生成完整报告
        用于熔断前的快速判定
        """
        result = self.audit(content)
        return result.status

    def create_result(self) -> AuditResult:
        """创建空白审计结果（预填插件信息）"""
        return AuditResult(
            plugin_name=self.name,
            plugin_version=self.version,
            dna=self.dna,
        )


# ═══════════════════════════════════════════════════════════════
# 审计插件注册表（B4 Hub）
# ═══════════════════════════════════════════════════════════════

class AuditPluginRegistry:
    """
    B4 审计插件注册中心

    管理所有审计插件的注册、发现和调用。
    对应 B4 层的可插拔架构。
    """

    def __init__(self):
        self._plugins: dict[str, AuditPlugin] = {}

    def register(self, plugin: AuditPlugin, aliases: list[str] | None = None) -> None:
        """注册审计插件"""
        self._plugins[plugin.name] = plugin
        for alias in (aliases or []):
            self._plugins[alias] = plugin

    def unregister(self, name: str) -> bool:
        """注销审计插件"""
        if name in self._plugins:
            del self._plugins[name]
            return True
        return False

    def get(self, name: str) -> AuditPlugin | None:
        """获取指定插件"""
        return self._plugins.get(name)

    def list_all(self) -> list[dict[str, object]]:
        """列出所有已注册插件"""
        return [
            {
                "name": p.name,
                "version": p.version,
                "dna": p.dna,
                "level": p.level.value,
            }
            for p in set(self._plugins.values())
        ]

    def audit_all(self, target: Any = None) -> list[AuditResult]:
        """运行所有注册的审计插件"""
        results = []
        for plugin in set(self._plugins.values()):
            try:
                result = plugin.audit(target)
                results.append(result)
            except Exception as e:
                err_result = plugin.create_result()
                err_result.add_finding(AuditFinding(
                    level="error",
                    message=f"审计插件 '{plugin.name}' 执行异常: {e}",
                ))
                err_result.finalize()
                results.append(err_result)
        return results

    def get_summary_report(self, results: list[AuditResult] | None = None) -> str:
        """生成汇总审计报告"""
        if results is None:
            results = self.audit_all()

        lines = ["🐉 B4审计层·全插件汇总报告", "=" * 50]
        total_errors = total_warnings = total_info = 0
        overall = AuditStatus.GREEN

        for r in results:
            total_errors += r.summary.get("error", 0)
            total_warnings += r.summary.get("warning", 0)
            total_info += r.summary.get("info", 0)
            icon = "✅" if r.status == AuditStatus.GREEN else (
                "⚠️" if r.status == AuditStatus.YELLOW else "❌")
            lines.append(f"  {icon} {r.plugin_name}: {r.status.value}")

        if total_errors > 0:
            overall = AuditStatus.RED
        elif total_warnings > 0:
            overall = AuditStatus.YELLOW

        lines.append("=" * 50)
        lines.append(f"总体: {overall.value} (E:{total_errors} W:{total_warnings} I:{total_info})")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# B3 模块快捷命令注册表
# ═══════════════════════════════════════════════════════════════

@dataclass
class ShortcutCommand:
    """B3 快捷命令定义"""
    name: str           # 中文命令名（如 "编辑器"）
    handler: Callable[..., object]   # 处理函数
    description: str    # 命令描述
    category: str       # 八卦分类（启动/审计/安全/主权/技能/状态/同步/部署）
    aliases: list[str] = field(default_factory=list)
    need_arg: bool = False


class ShortcutRegistry:
    """
    B3 模块快捷命令注册中心

    允许 A4 模块动态注册 B3 快捷命令。
    对应需求：A4与B3的边界统一。
    """

    def __init__(self):
        self._shortcuts: dict[str, ShortcutCommand] = {}

    def register(self, cmd: ShortcutCommand):
        """注册快捷命令"""
        self._shortcuts[cmd.name] = cmd
        for alias in cmd.aliases:
            if alias not in self._shortcuts:
                self._shortcuts[alias] = cmd

    def get(self, name: str) -> ShortcutCommand | None:
        """查找快捷命令"""
        return self._shortcuts.get(name)

    def list_by_category(self, category: str) -> list[ShortcutCommand]:
        """按分类列出命令"""
        return [c for c in set(self._shortcuts.values()) if c.category == category]

    def list_all(self) -> list[dict[str, object]]:
        """列出所有注册的快捷命令"""
        seen: set[str] = set()
        result = []
        for cmd in self._shortcuts.values():
            if cmd.name not in seen:
                seen.add(cmd.name)
                result.append({
                    "name": cmd.name,
                    "description": cmd.description,
                    "category": cmd.category,
                    "aliases": cmd.aliases,
                    "need_arg": cmd.need_arg,
                })
        return result


# ═══════════════════════════════════════════════════════════════
# 预注册例：DNATemplate审计插件
# ═══════════════════════════════════════════════════════════════

class DNAVerifierPlugin(AuditPlugin):
    """DNA追溯验证审计插件"""

    name = "dna-verifier"
    version = "1.0"
    dna = "#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-DNA-VERIFIER-v1.0"
    level = AuditLevel.L0_ETERNAL

    def audit(self, target: Any = None) -> AuditResult:
        result = self.create_result()

        if target is None:
            result.add_finding(AuditFinding(
                level="info",
                message="DNA验证器已就绪·等待审计目标",
            ))
            result.finalize()
            return result

        # 检查DNA标记
        if isinstance(target, str):
            content = target
        elif hasattr(target, 'read'):
            content = target.read()
        else:
            content = str(target)

        findings = []

        # L0检查: 繁体龍
        if "龍" in content and "龍" not in content:
            findings.append(AuditFinding(
                level="error",
                message="铁律违反: 使用简体「龍」，应使用繁体「龍」",
                suggestion="全局替换 龍 → 龍",
            ))

        # DNA格式检查
        import re
        dna_pattern = r'#龍芯⚡️\d{4}-\d{2}-\d{2}-[\w-]+'
        if not re.search(dna_pattern, content):
            findings.append(AuditFinding(
                level="error",
                message="缺少有效DNA追溯码",
                suggestion="添加DNA标记: #龍芯⚡️YYYY-MM-DD-MODULE-VERSION",
            ))

        # 全角下划线检查
        fullwidth = '\uff3f'
        if fullwidth in content:
            findings.append(AuditFinding(
                level="warning",
                message="发现全角下划线(U+FF3F)，应使用半角下划线(U+005F)",
                suggestion="全局替换全角下划线 → 半角下划线（用编辑器的查找替换功能）",
            ))

        for f in findings:
            result.add_finding(f)

        result.finalize()
        return result


class NamingConventionPlugin(AuditPlugin):
    """CNSH命名规范审计插件"""

    name = "naming-convention"
    version = "1.0"
    dna = "#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-NAMING-AUDIT-v1.0"
    level = AuditLevel.L1_CORE

    def audit(self, target: Any = None) -> AuditResult:
        result = self.create_result()

        if target is None:
            result.add_finding(AuditFinding(
                level="info",
                message="命名规范审计器已就绪·等待审计目标",
            ))
            result.finalize()
            return result

        content = target if isinstance(target, str) else str(target)
        import re

        # 检查中文变量名的命名空间前缀
        cn_var_pattern = re.compile(r'([\u4e00-\u9fff_]+[\u4e00-\u9fff\w_]*)\s*=')
        valid_prefixes = {'龍_', '引擎_', '数据_', '模块_', '系统_', '用户_', '辅助_', '临时_'}

        for match in cn_var_pattern.finditer(content):
            var_name = match.group(1)
            # 如果是纯中文变量名
            if re.search(r'[\u4e00-\u9fff]', var_name):
                has_prefix = any(var_name.startswith(p) for p in valid_prefixes)
                if not has_prefix and var_name not in ('VERSION',):
                    result.add_finding(AuditFinding(
                        level="warning",
                        message=f"中文变量「{var_name}」缺少命名空间前缀",
                        suggestion=f"建议加前缀: 如「龍_{var_name}」或「数据_{var_name}」",
                    ))

        # 驼峰命名检查（中文代码中）
        camel_pattern = re.compile(r'[\u4e00-\u9fff]+[a-z]+[A-Z]')
        for match in camel_pattern.finditer(content):
            result.add_finding(AuditFinding(
                level="info",
                message=f"中文英文驼峰混用: 「{match.group()}」",
                suggestion="建议统一为全中文或全大写英文缩写",
            ))

        result.finalize()
        return result


# ═══════════════════════════════════════════════════════════════
# 全局单例
# ═══════════════════════════════════════════════════════════════

# B4 审计插件全局注册表
audit_registry = AuditPluginRegistry()

# 注册内置审计插件
audit_registry.register(DNAVerifierPlugin(), aliases=["dna", "dna-check", "DNA检查"])
audit_registry.register(NamingConventionPlugin(), aliases=["naming", "命名检查", "命名规范"])

# B3 快捷命令全局注册表
shortcut_registry = ShortcutRegistry()


# ═══════════════════════════════════════════════════════════════
# CLI入口
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("🐉 B4审计插件系统")
        print("用法: python3 audit_plugin_base.py <命令>")
        print()
        print("命令:")
        print("  list          列出所有已注册审计插件")
        print("  shortcuts     列出所有B3快捷命令")
        print("  audit <文件>  对指定文件运行全部审计")
        print("  dna <文件>    仅运行DNA验证审计")
        print("  naming <文件> 仅运行命名规范审计")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "list":
        plugins = audit_registry.list_all()
        print(f"🐉 B4审计层·已注册插件 ({len(plugins)} 个)")
        for p in plugins:
            print(f"  [{p['level']}] {p['name']} v{p['version']}")
            print(f"         DNA: {p['dna']}")

    elif cmd == "shortcuts":
        shortcuts = shortcut_registry.list_all()
        print(f"🐉 B3快捷命令·已注册 ({len(shortcuts)} 个)")
        for s in shortcuts:
            print(f"  📎 {s['name']} [{s['category']}] → {s['description']}")

    elif cmd == "audit" and len(sys.argv) > 2:
        target_path = sys.argv[2]
        try:
            with open(target_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ 无法读取文件: {e}")
            sys.exit(1)

        results = audit_registry.audit_all(content)
        for r in results:
            print(r.to_report())
            print()

        print(audit_registry.get_summary_report(results))

    elif cmd == "dna" and len(sys.argv) > 2:
        target_path = sys.argv[2]
        with open(target_path, 'r', encoding='utf-8') as f:
            content = f.read()
        plugin = audit_registry.get("dna-verifier")
        if plugin:
            result = plugin.audit(content)
            print(result.to_report())

    elif cmd == "naming" and len(sys.argv) > 2:
        target_path = sys.argv[2]
        with open(target_path, 'r', encoding='utf-8') as f:
            content = f.read()
        plugin = audit_registry.get("naming-convention")
        if plugin:
            result = plugin.audit(content)
            print(result.to_report())

    else:
        print(f"未知命令: {cmd}")
        print("可用: list | shortcuts | audit | dna | naming")

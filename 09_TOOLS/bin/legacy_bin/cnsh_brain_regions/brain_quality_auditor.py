#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
B7 · 质量检查脑区 → P05 上帝之眼
====================================
三色审计引擎：🟢通过 / 🟡警告 / 🔴拒绝
对接现有三色审计体系 (cnsh_code_audit.py)。

DNA: #龍芯⚡️丙午·丙申·丙辰·未时·䷄需-BRAIN-B7-QUALITY-AUDITOR-v1.0
"""

import re
import os
import sys
from typing import Dict, Any, List, Tuple


# ── 审计规则库 ────────────────────────────────────────────────────────────────

RED_RULES: List[Tuple[str, str, str]] = [
    # (正则, 描述, 风险)
    (r'os\.system\(', "系统命令执行", "远程代码执行风险"),
    (r'subprocess\.(call|Popen|run)\(', "子进程调用", "未授权进程启动"),
    (r'eval\(', "eval执行", "动态代码执行风险"),
    (r'exec\(', "exec执行", "动态代码执行风险"),
    (r'__import__\(', "动态导入", "任意模块加载"),
    (r'password\s*=\s*["\'][^"\']+["\']', "硬编码密码", "密码洩露"),
    (r'api_key\s*=\s*["\'][^"\']+["\']', "硬编码API密鑰", "密鑰洩露"),
    (r'secret\s*=\s*["\'][^"\']+["\']', "硬编码密鑰", "密鑰洩露"),
    (r'token\s*=\s*["\'][^"\']+["\']', "硬编码令牌", "令牌洩露"),
    (r'rm\s+-rf\s+/', "递归删除根目录", "系统破坏"),
    (r'DROP\s+TABLE', "删除数据库表", "数据破坏"),
    (r'DELETE\s+FROM\s+\w+\s+WHERE\s+1\s*=\s*1', "全表删除", "数据破坏"),
    (r'requests\.(get|post)\([^)]*verify\s*=\s*False', "SSL验证关閉", "中间人攻击风险"),
]

YELLOW_RULES: List[Tuple[str, str, str]] = [
    (r'while\s+True\s*:', "无限循环", "可能死循环"),
    (r'sleep\(\s*\d{3,}\s*\)', "长时间休眠", "性能影响"),
    (r'\.read\(\)\s*$', "读取全部内容", "大文件内存溢出"),
    (r'open\([^)]+["\'][wa]', "文件写模式", "文件覆盖风险"),
    (r'except\s*:', "裸except", "捕获所有异常"),
    (r'input\(', "用戶输入", "需输入验证"),
    (r'print\(', "print语句", "生產环境应移除"),
    (r'console\.log\(', "console.log", "生產环境应移除"),
    (r'debug\s*=\s*True', "debug模式", "生產环境应关閉"),
]

GREEN_PATTERNS: List[str] = [
    r'try\s*:.*\n.*except\s+\w+',  # 具体异常处理
    r'with\s+open\(',                # 上下文管理器
    r'def\s+test_\w+',               # 测试函数
    r'assert\s+',                    # 断言
    r'if\s+__name__\s*==\s*["\']__main__["\']',  # 主入口保护
]


def audit_red(code: str) -> List[Dict[str, str]]:
    """红色审计"""
    results = []
    for pattern, name, risk in RED_RULES:
        matches = re.findall(pattern, code, re.IGNORECASE)
        if matches:
            results.append({
                "level": "🔴",
                "name": name,
                "risk": risk,
                "count": len(matches),
                "details": f"发现 {len(matches)} 处: {name}"
            })
    return results


def audit_yellow(code: str) -> List[Dict[str, str]]:
    """黄色审计"""
    results = []
    for pattern, name, risk in YELLOW_RULES:
        matches = re.findall(pattern, code, re.IGNORECASE)
        if matches:
            results.append({
                "level": "🟡",
                "name": name,
                "risk": risk,
                "count": len(matches),
                "details": f"发现 {len(matches)} 处: {name}"
            })
    return results


def audit_green(code: str) -> List[Dict[str, str]]:
    """绿色审计（正面模式）"""
    results = []
    for pattern in GREEN_PATTERNS:
        if re.search(pattern, code):
            results.append({
                "level": "🟢",
                "name": "良好实踐",
                "risk": "无",
                "details": f"检测到良好模式: {pattern[:40]}..."
            })
    return results


def compute_quality_score(code: str) -> int:
    """计算品质分数"""
    score = 70  # 基基分

    reds = audit_red(code)
    yellows = audit_yellow(code)
    greens = audit_green(code)

    score -= len(reds) * 20
    score -= len(yellows) * 5
    score += len(greens) * 3

    return max(0, min(100, score))


def execute(code: str, features: Dict[str, Any], step: int, total: int) -> Dict[str, Any]:
    """
    B7 脑区执行入口
    """
    reds = audit_red(code)
    yellows = audit_yellow(code)
    greens = audit_green(code)
    quality = compute_quality_score(code)

    # 判定最終级别
    if reds:
        overall = "🔴 红色·需修复"
        action = "代码存在安全风险，建议拒绝合入"
    elif yellows:
        overall = "🟡 黄色·有警告"
        action = "建议修复警告後再合入"
    else:
        overall = "🟢 绿色·通过"
        action = "代码品质良好，可安全合入"

    # 嘗试对接现有审计引擎
    existing_result = None
    try:
        audit_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "bin", "cnsh_code_audit.py"
        )
        if os.path.exists(audit_path):
            existing_result = "cnsh_code_audit.py 可用·未执行（靜态分析模式）"
    except Exception:
        pass

    return {
        "output_code": code,
        "auto_activate": [],
        "overall": overall,
        "action": action,
        "quality_score": quality,
        "audit_summary": {
            "red": len(reds),
            "yellow": len(yellows),
            "green": len(greens),
        },
        "red_findings": reds[:5],
        "yellow_findings": yellows[:5],
        "existing_audit": existing_result,
        "message": f"B7: {overall} · 品质分 {quality}/100 · 🔴{len(reds)} 🟡{len(yellows)} 🟢{len(greens)}"
    }


if __name__ == "__main__":
    test = """
import os
password = "admin123"
os.system("ls -la")
"""
    r = execute(test, {}, 0, 0)
    import json
    print(json.dumps(r, indent=2, ensure_ascii=False))

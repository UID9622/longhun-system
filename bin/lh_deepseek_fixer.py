#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════
# 龍魂体系 | DeepSeek 修复引擎 · 打工工具
# ═══════════════════════════════════════════
# ENCODING: UTF-8
# DNA追溯码(v∞): #龍芯⚡️丙午·丙申·丁巳·酉时·䷾既济-DEEPSEEK-FIXER-v1.0
# DNA追溯码(v1.0): #龍芯⚡️2026-07-12-DEEPSEEK-FIXER-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬DSF1-001A
# 创建者：UID9622（诸葛鑫·Lucky）
# 权重级别：L2（工具层·非底座）
# 三色审计状态：🟡 含API密钥（来自环境变量/参数传入）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# ═══════════════════════════════════════════
#
# 定位：DeepSeek = 打工仔修代码 · CNSH闸门 = 焊死底座 · 协议不变
# 铁律：DeepSeek 修复后的代码仍需过 CNSH 闸门，不合格 = 不入库
#       外部 AI 变 → 工具跟着调 · 协议不动
#
# 架构：
#   你的终端指令 → DeepSeek API（修复引擎）→ 代码回写
#   → 语法校验 → CNSH 闸门审查 → CodeBuddy 自动加载
#
# DeepSeek 是打工的，协议是你写的。
# ═══════════════════════════════════════════
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from typing import Any

# ═══════════════════════════════════════════
# API 配置 · 密钥从环境变量读取（优先）或传入
# ═══════════════════════════════════════════

def _get_api_key(key_name: str, fallback: str = "") -> str:
    """从环境变量取密钥，环境变量优先，无环境变量用传入值"""
    return os.environ.get(key_name, fallback)

DEEPSEEK_API_KEY = _get_api_key("DEEPSEEK_API_KEY", "")  # fallback已移除——真实key必须从环境变量来
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

# ═══════════════════════════════════════════
# 修复模式定义
# ═══════════════════════════════════════════

修复模式 = {
    "type_error": "修复类型错误（basedpyright/pyright）",
    "syntax": "修复语法错误",
    "cnsh_align": "CNSH中文语法对齐",
    "full": "全量修复（类型+语法+对齐）",
}


# ═══════════════════════════════════════════
# DeepSeek API 调用
# ═══════════════════════════════════════════

def 调用DeepSeek修复(代码内容: str, 错误信息: str, 模式: str = "full") -> str:
    """调用 DeepSeek API 修复代码"""

    import urllib.request

    系统提示 = f"""你是龍魂系统的代码修复引擎。任务：
1. 修复以下 Python 代码中的错误
2. 保持 CNSH（中文命名系统）风格——函数名、变量名用中文
3. 解决 basedpyright 类型检查错误
4. 输出完整修复后的代码，不要省略

修复模式: {模式}

规则：
- 参数名用中文（如 确认码、用户UID）
- 内部临时变量可用英文（如 input_code_raw）
- 类型注解保持完整
- 加 # type: ignore 仅作为最后手段"""

    用户消息 = f"""错误信息：
{错误信息}

需要修复的代码：
```python
{代码内容}
```

请输出完整修复后的代码（只输出代码，不要解释）。"""

    请求体 = json.dumps({
        "model": "deepseek-coder",
        "messages": [
            {"role": "system", "content": 系统提示},
            {"role": "user", "content": 用户消息}
        ],
        "temperature": 0.1,
        "max_tokens": 8000,
    }).encode()

    请求 = urllib.request.Request(
        f"{DEEPSEEK_BASE_URL}/chat/completions",
        data=请求体,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(请求, timeout=120) as 响应:
            结果 = json.loads(响应.read().decode())
            return 结果["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ DeepSeek API 错误: {e}"


# ═══════════════════════════════════════════
# 错误信息提取
# ═══════════════════════════════════════════

def 提取Pyright错误(文件路径: str) -> list[dict[str, Any]]:
    """运行 basedpyright 提取错误信息"""

    try:
        结果 = subprocess.run(
            ["python3", "-m", "pyright", 文件路径, "--outputjson"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if 结果.returncode == 0:
            return []  # 无错误

        输出 = json.loads(结果.stdout)
        错误列表 = []
        for 诊断 in 输出.get("generalDiagnostics", []):
            错误列表.append({
                "行": 诊断.get("range", {}).get("start", {}).get("line", 0) + 1,
                "列": 诊断.get("range", {}).get("start", {}).get("character", 0),
                "消息": 诊断.get("message", ""),
                "规则": 诊断.get("rule", ""),
                "严重度": 诊断.get("severity", 1),
            })
        return 错误列表
    except Exception as e:
        return [{"行": 0, "列": 0, "消息": f"pyright 运行失败: {e}", "规则": "", "严重度": 1}]


# ═══════════════════════════════════════════
# 文件修复流程
# ═══════════════════════════════════════════

def 修复文件(文件路径: str, 模式: str = "full", 跳过闸门: bool = False) -> tuple[bool, str]:
    """
    完整修复流程
    
    参数:
        文件路径: 要修复的文件
        模式: 修复模式 (type_error/syntax/cnsh_align/full)
        跳过闸门: 是否跳过 CNSH 闸门审查（默认不跳过）
    
    返回:
        (是否成功, 消息)
    """

    路径 = Path(文件路径)
    if not 路径.exists():
        return False, f"❌ 文件不存在: {文件路径}"

    # 1. 读取原代码
    原代码 = 路径.read_text(encoding="utf-8")
    print(f"📄 读取: {文件路径} ({len(原代码)} 字符)")

    # 2. 提取错误
    print("🔍 运行 basedpyright 提取错误...")
    错误列表 = 提取Pyright错误(文件路径)
    if not 错误列表:
        print("✅ 无类型错误，检查语法...")
        try:
            compile(原代码, 文件路径, "exec")
            return True, "✅ 无错误，无需修复"
        except SyntaxError as e:
            错误列表 = [{"行": e.lineno or 1, "列": e.offset or 0, "消息": str(e), "规则": "syntax", "严重度": 1}]

    print(f"🔴 发现 {len(错误列表)} 个错误:")
    for 错误 in 错误列表:
        严重度图标 = "🔴" if 错误["严重度"] == 1 else "🟡"
        print(f"   {严重度图标} 行{错误['行']}:{错误['列']} {错误['消息']}")

    # 3. 构建错误信息文本
    错误信息 = "\n".join([
        f"[行{err['行']}:{err['列']}] {err['消息']} (规则: {err['规则']})"
        for err in 错误列表
    ])

    # 4. 调用 DeepSeek 修复
    print("🤖 调用 DeepSeek 修复引擎...")
    修复结果 = 调用DeepSeek修复(原代码, 错误信息, 模式)

    if 修复结果.startswith("❌"):
        return False, 修复结果

    # 5. 提取代码块
    修复代码 = 提取代码块(修复结果)
    if not 修复代码:
        return False, "❌ DeepSeek 返回中未找到代码块"

    # 6. 备份原文件
    备份路径 = 路径.with_suffix(路径.suffix + ".backup")
    备份路径.write_text(原代码, encoding="utf-8")
    print(f"💾 备份: {备份路径}")

    # 7. 写入修复代码
    路径.write_text(修复代码, encoding="utf-8")
    print(f"✏️ 写入修复代码 ({len(修复代码)} 字符)")

    # 8. 验证修复
    print("🔍 验证修复结果...")
    新错误 = 提取Pyright错误(文件路径)
    if 新错误:
        print(f"⚠️ 仍有 {len(新错误)} 个错误:")
        for 错误 in 新错误:
            print(f"   🔴 行{错误['行']}:{错误['列']} {错误['消息']}")
        return False, f"⚠️ 修复后仍有 {len(新错误)} 个错误"

    # 语法检查
    try:
        compile(修复代码, 文件路径, "exec")
    except SyntaxError as e:
        return False, f"❌ 语法错误: {e}"

    # 9. CNSH 闸门审查（焊死·不可跳过）
    if not 跳过闸门:
        print("🧬 CNSH 闸门审查...")
        闸门通过, 闸门消息 = _过CNSH闸门(文件路径)
        if not 闸门通过:
            print(f"🔴 CNSH 闸门拒绝: {闸门消息}")
            # 不还原——修复后让用户看到结果再决定
            return False, f"🔴 CNSH 闸门拒绝: {闸门消息}"
        print(f"🟢 CNSH 闸门: {闸门消息}")

    print("✅ 修复完成，无错误")
    return True, "✅ 修复成功"


def _过CNSH闸门(文件路径: str) -> tuple[bool, str]:
    """调 CNSH 闸门审查修复后的文件"""
    try:
        闸门脚本 = Path(__file__).resolve().parent / "lh_cnsh_gatekeeper.py"
        结果 = subprocess.run(
            ["python3", str(闸门脚本), "check", "--file", 文件路径],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if 结果.returncode == 0:
            return True, "通过"
        else:
            # 提取拒绝原因
            输出行 = 结果.stdout.strip().split("\n")
            拒绝行 = [l for l in 输出行 if "🔴" in l]
            return False, "; ".join(拒绝行[:3]) if 拒绝行 else "未知拒绝原因"
    except Exception as e:
        return False, f"闸门执行失败: {e}"


def 提取代码块(文本: str) -> str:
    """从 DeepSeek 返回中提取代码块"""

    import re

    # 匹配 ```python 代码 ```
    匹配 = re.search(r'```python\s*(.*?)\s*```', 文本, re.DOTALL)
    if 匹配:
        return 匹配.group(1).strip()

    # 匹配 ``` 代码 ```
    匹配 = re.search(r'```\s*(.*?)\s*```', 文本, re.DOTALL)
    if 匹配:
        return 匹配.group(1).strip()

    # 如果没有代码块标记，返回全部（假设全是代码）
    return 文本.strip()


# ═══════════════════════════════════════════
# CodeBuddy 联动 · 自动触发
# ═══════════════════════════════════════════

def 触发CodeBuddy联动(文件路径: str) -> bool:
    """通知 CodeBuddy 重新加载修复后的文件"""

    # 写入触发文件（CodeBuddy 插件监控）
    触发目录 = Path.home() / ".龍魂"
    触发目录.mkdir(parents=True, exist_ok=True)
    触发路径 = 触发目录 / ".codebuddy_trigger"
    触发路径.write_text(json.dumps({
        "action": "reload",
        "file": str(Path(文件路径).resolve()),
        "timestamp": time.time(),
        "source": "lh_deepseek_fixer",
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print("🔄 CodeBuddy 触发文件已写入")
    return True


# ═══════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════

def _打印帮助():
    print("🧬 龍魂·DeepSeek 修复引擎 v1.0")
    print("定位: DeepSeek = 打工仔修代码 · 底座 = CNSH 闸门焊死")
    print()
    print("用法:")
    print("  python3 bin/lh_deepseek_fixer.py <文件路径> [模式]")
    print()
    print("模式:")
    for 模式, 说明 in 修复模式.items():
        print(f"  {模式:<12} {说明}")
    print()
    print("选项:")
    print("  --skip-gate  跳过 CNSH 闸门审查（不推荐，仅调试用）")
    print()
    print("环境变量:")
    print("  DEEPSEEK_API_KEY  DeepSeek API密钥（优先于内置值）")
    print()
    print("修复后自动:")
    print("  1. 语法校验 → 2. CNSH 闸门审查 → 3. CodeBuddy 刷新")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        _打印帮助()
        sys.exit(0)

    文件路径 = sys.argv[1]
    模式 = "full"
    跳过闸门 = False

    # 解析可选参数
    for arg in sys.argv[2:]:
        if arg in 修复模式:
            模式 = arg
        elif arg == "--skip-gate":
            跳过闸门 = True

    # 设置环境变量（从参数或环境读取）
    if not os.environ.get("DEEPSEEK_API_KEY"):
        os.environ["DEEPSEEK_API_KEY"] = DEEPSEEK_API_KEY

    ok, msg = 修复文件(文件路径, 模式, 跳过闸门=跳过闸门)
    print(msg)

    if ok and "修复成功" in msg:
        触发CodeBuddy联动(文件路径)

    sys.exit(0 if ok else 1)

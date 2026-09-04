#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂·自动意图识别与执行 v1.0
==========================
DNA: #龍芯⚡️丙午·癸未·丁未·申时·䷀乾-AUTO-INTENT-v1.0-EXECUTE

你说人话，系统自己动。
- 分析模式：只看不执行
- 执行模式：分析 + 自动触发引擎 + 人格路由 + 动作执行
- 自动模式：监听输入流/剪贴板，自动处理

用法:
  python3 engines/lh_auto_intent.py analyze "我操，这个钩子接不上"
  python3 engines/lh_auto_intent.py run "帮我审计一下系统"
  python3 engines/lh_auto_intent.py auto --stdin
  python3 engines/lh_auto_intent.py auto --clipboard
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from engines.lh_natural_router import NaturalLanguageRouter, PYTHON_CMD

CST = timezone(timedelta(hours=8))
DNA_PREFIX = "#龍芯⚡️"
ENGINE_DNA = f"{DNA_PREFIX}丙午·癸未·丁未·申时·☰乾-AUTO-INTENT-v1.0-EXECUTE"

# 危险操作名单（执行前必须确认）
DANGEROUS_ACTIONS = ["删除", "清空", "重置", "覆盖", "drop", "delete", "rm -rf"]


def _now() -> str:
    return datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def _run_subprocess(cmd: List[str], timeout: int = 60) -> Dict[str, Any]:
    """安全执行子进程"""
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=PROJECT_ROOT,
        )
        return {
            "status": "ok" if proc.returncode == 0 else "error",
            "returncode": proc.returncode,
            "output": proc.stdout.strip()[:2000],
            "stderr": proc.stderr.strip()[:500] if proc.stderr else "",
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "output": "(执行超时)"}
    except Exception as e:
        return {"status": "exception", "output": f"(异常: {e})"}


def _is_dangerous(action_text: str) -> bool:
    return any(d in action_text.lower() for d in DANGEROUS_ACTIONS)


def _execute_l4_action(action: Dict[str, Any], query: str, dry_run: bool = True) -> Dict[str, Any]:
    """执行 L4 抽屉建议的动作"""
    action_text = action.get("action", "")
    target_bin = action.get("target_bin", "")

    result = {
        "drawer": action.get("drawer", ""),
        "action": action_text,
        "target_bin": target_bin,
        "dry_run": dry_run,
        "executed": False,
        "output": "",
    }

    if dry_run:
        result["output"] = "[dry-run] 未执行"
        return result

    # 危险操作拦截
    if _is_dangerous(action_text):
        result["output"] = "[安全拦截] 涉及删除/重置等危险操作，需人工确认"
        return result

    # 根据 target_bin 执行
    if not target_bin:
        result["output"] = "(无 target_bin，无法执行)"
        return result

    target_path = Path(target_bin).expanduser()
    if not target_path.is_absolute():
        target_path = PROJECT_ROOT / target_bin

    if not target_path.exists():
        result["output"] = f"(目标不存在: {target_path})"
        return result

    if target_path.suffix == ".py":
        res = _run_subprocess([PYTHON_CMD, str(target_path), query])
    elif target_path.suffix in (".json", ".md", ".txt"):
        # 数据文件已在 router 中查询过
        res = {"status": "ok", "output": "(数据文件，已在路由查询中处理)"}
    elif target_path.suffix == ".sh":
        res = _run_subprocess(["bash", str(target_path), query])
    else:
        res = _run_subprocess([str(target_path), query])

    result["executed"] = res["status"] == "ok"
    result["output"] = res["output"]
    return result


def _route_persona(ipa: str, query: str) -> Dict[str, Any]:
    """调用人格编排器进行人格路由"""
    persona_script = PROJECT_ROOT / "bin" / "lh_persona_orchestrator.py"
    if not persona_script.exists():
        return {"status": "missing", "output": "人格编排器不存在"}

    # 简化为直接调用一次人格执行
    res = _run_subprocess([PYTHON_CMD, str(persona_script), "--route", ipa, query])
    return res


def analyze(query: str) -> Dict[str, Any]:
    """分析意图，返回路由建议，不执行"""
    router = NaturalLanguageRouter()
    result = router.route(query)
    result["模式"] = "analyze"
    result["执行动作"] = []  # analyze 模式不执行
    result["人格执行"] = []
    return result


def run(query: str, dry_run: bool = False) -> Dict[str, Any]:
    """分析 + 执行推荐的引擎、动作、人格路由"""
    router = NaturalLanguageRouter()
    route_result = router.route(query)

    # 0. 默认动作：任何非 dry-run 输入都先保存到本地剪贴板容器
    vault_result: Dict[str, Any] = {"status": "skipped", "reason": "dry-run"}
    if not dry_run and query and len(query.strip()) > 3:
        try:
            from engines.lh_clipboard_vault import save
            vault_result = save(query.strip(), source="auto-intent")
        except Exception as e:
            vault_result = {"status": "error", "reason": str(e)}
    route_result["容器保存"] = vault_result

    # 1. 执行 L4 建议动作
    action_results = []
    for action in route_result.get("建议动作", []):
        ar = _execute_l4_action(action, query, dry_run=dry_run)
        action_results.append(ar)

    # 2. 人格路由执行（前3个）
    persona_results = []
    for p in route_result.get("人格路由", [])[:3]:
        pr = _route_persona(p["ipa"], query)
        persona_results.append({
            "ipa": p["ipa"],
            "result": pr,
        })

    # 3. 生成最终 DNA
    summary = {
        "query": query,
        "mode": "run" if not dry_run else "dry-run",
        "engines": [r["name"] for r in route_result.get("执行结果", [])],
        "actions": [a["drawer"] for a in action_results if a.get("executed")],
        "personas": [p["ipa"] for p in persona_results],
    }

    return {
        **route_result,
        "模式": "run" if not dry_run else "dry-run",
        "执行动作": action_results,
        "人格执行": persona_results,
        "执行DNA": f"{DNA_PREFIX}{datetime.now(CST).strftime('%Y-%m-%d')}-AUTO-INTENT-{hashlib.sha256(json.dumps(summary, ensure_ascii=False).encode()).hexdigest()[:8]}",
        "引擎DNA": ENGINE_DNA,
    }


def _format_report(result: Dict[str, Any]) -> str:
    """格式化执行报告"""
    lines = []
    lines.append("")
    lines.append("=" * 64)
    lines.append("  🐉 龍魂·自动意图识别与执行 v1.0")
    lines.append(f"  模式: {result['模式'].upper()}")
    lines.append("=" * 64)
    lines.append(f"\n  📝 输入: {result['query']}")

    # 抽屉路由
    lines.append("\n  🗂️ 语义抽屉路由:")
    for layer_id, matches in result.get("抽屉路由", {}).items():
        if matches:
            names = ", ".join([f"{m['name']}({m['score']:.0f})" for m in matches[:2]])
            lines.append(f"    {layer_id}: {names}")

    # 人格路由
    personas = result.get("人格路由", [])
    if personas:
        lines.append("\n  🎭 人格路由推荐:")
        for p in personas[:3]:
            lines.append(f"    → {p['ipa']} ({p['source']})")

    # 人格执行结果
    persona_exec = result.get("人格执行", [])
    if persona_exec:
        lines.append("\n  🎬 人格执行:")
        for pe in persona_exec:
            status = pe["result"].get("status", "?")
            emoji = "✅" if status == "ok" else "⚠️"
            lines.append(f"    {emoji} {pe['ipa']}: {status}")

    # 容器保存
    vault = result.get("容器保存", {})
    if vault:
        status = vault.get("status", "")
        if status == "saved":
            lines.append(f"\n  📦 容器保存: ✅ {vault.get('path', '')} [{vault.get('topic', '')}]")
        elif status == "error":
            lines.append(f"\n  📦 容器保存: ⚠️ {vault.get('reason', '未知错误')}")
        else:
            lines.append(f"\n  📦 容器保存: ⏸️ {vault.get('reason', 'dry-run')}")

    # 建议动作
    actions = result.get("建议动作", [])
    if actions:
        lines.append("\n  🎯 动作执行:")
        for a in actions:
            flag = "✅" if a.get("executed") else "⏸️"
            lines.append(f"    {flag} {a['drawer']}: {a['action']}")
            if a.get("output"):
                lines.append(f"       {a['output'][:100]}")

    # 引擎结果
    engines = result.get("执行结果", [])
    if engines:
        lines.append(f"\n  ⚡ 引擎执行 ({len(engines)} 个):")
        for r in engines:
            emoji = "✅" if r["status"] == "ok" else "⚠️"
            lines.append(f"    {emoji} {r['name']} [{r['elapsed']}s]")

    lines.append(f"\n  🧬 {result.get('执行DNA', result.get('DNA', ''))}")
    lines.append("=" * 64)
    return "\n".join(lines)


def _get_clipboard() -> str:
    """使用 macOS pbpaste 读取剪贴板"""
    try:
        proc = subprocess.run(
            ["pbpaste"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return proc.stdout if proc.returncode == 0 else ""
    except Exception:
        return ""


def auto_clipboard(dry_run: bool = True, interval: float = 2.0):
    """监听剪贴板变化，自动分析并触发"""
    print("📋 剪贴板监听已启动（按 Ctrl+C 停止）...")
    last_content = ""
    while True:
        content = _get_clipboard()
        if content and content != last_content:
            last_content = content
            print(f"\n🔔 检测到新剪贴板内容 ({len(content)} 字符)")
            result = run(content, dry_run=dry_run)
            print(_format_report(result))
        time.sleep(interval)


def auto_stdin(dry_run: bool = True):
    """从 stdin 读取输入并自动处理"""
    print("🎙️ 自动意图模式：每行输入将被自动分析并触发（按 Ctrl+D 结束）")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        print(f"\n🔔 输入: {line}")
        result = run(line, dry_run=dry_run)
        print(_format_report(result))


def main():
    parser = argparse.ArgumentParser(description="龍魂·自动意图识别与执行")
    sub = parser.add_subparsers(dest="command", required=True)

    p_analyze = sub.add_parser("analyze", help="只分析，不执行")
    p_analyze.add_argument("query", type=str, help="自然语言输入")
    p_analyze.add_argument("--raw", action="store_true", help="输出JSON")

    p_run = sub.add_parser("run", help="分析并执行")
    p_run.add_argument("query", type=str, help="自然语言输入")
    p_run.add_argument("--execute", action="store_true", help="真正执行（默认dry-run）")
    p_run.add_argument("--raw", action="store_true", help="输出JSON")

    p_auto = sub.add_parser("auto", help="自动模式")
    p_auto.add_argument("--clipboard", action="store_true", help="监听剪贴板")
    p_auto.add_argument("--stdin", action="store_true", help="监听stdin")
    p_auto.add_argument("--execute", action="store_true", help="真正执行（默认dry-run）")

    args = parser.parse_args()

    if args.command == "analyze":
        result = analyze(args.query)
        if args.raw:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(_format_report(result))

    elif args.command == "run":
        result = run(args.query, dry_run=not args.execute)
        if args.raw:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(_format_report(result))

    elif args.command == "auto":
        if args.clipboard:
            auto_clipboard(dry_run=not args.execute)
        elif args.stdin:
            auto_stdin(dry_run=not args.execute)
        else:
            print("请指定 --clipboard 或 --stdin")


if __name__ == "__main__":
    main()

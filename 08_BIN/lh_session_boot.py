#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·癸亥·子时·䷮困-SESSION-BOOT-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂 · 会话自举脚本 v1.0

任何新窗口/新会话启动时自动执行：
  1. 输出会话 DNA 与确认码
  2. 调用指令注册表「总开关 · 一键体检」
  3. 输出极简状态看板

用法:
    python3 08_BIN/lh_session_boot.py           # 手动执行
    # 或让 shell 在启动时自动调用（推荐）

接入 shell（已写入 ~/.zshrc）:
    if [[ -z "$LONGHUN_SESSION_BOOTED" && "$-" == *i* ]]; then
        export LONGHUN_SESSION_BOOTED=1
        python3 /Users/zuimeidedeyihan/longhun-system/08_BIN/lh_session_boot.py
    fi

协议: CC BY-NC-SA 4.0 (思想层) · MulanPSL v2 (工程层)
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.longhun_core.dna_trace import generate_dna

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_SCRIPT = PROJECT_ROOT / "08_BIN" / "lh_notion_command_registry.py"
REPORT_DIR = PROJECT_ROOT / "12_DOCS" / "agent_reports"
CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _run_master_check() -> Optional[Dict[str, Any]]:
    """调用注册表总开关体检，返回最新执行报告。"""
    print("🔄 正在执行总开关体检...")
    try:
        subprocess.run(
            [sys.executable, str(REGISTRY_SCRIPT), "run", "check", "--all"],
            cwd=PROJECT_ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300,
            check=False,
        )
    except subprocess.TimeoutExpired:
        print("⏱️ 总开关体检超时（300秒）", file=sys.stderr)
        return None
    except Exception as e:
        print(f"🔴 总开关体检异常: {e}", file=sys.stderr)
        return None

    # 读取最新执行报告
    reports = sorted(REPORT_DIR.glob("notion_command_registry_run_*.json"))
    if not reports:
        return None
    try:
        return json.loads(reports[-1].read_text(encoding="utf-8"))
    except Exception:
        return None


def _load_registry_summary() -> Dict[str, Any]:
    """简单统计本地注册表数据。"""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("registry", REGISTRY_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore
        rows = getattr(mod, "COMMAND_ROWS", [])
        total = len(rows)
        verify = sum(1 for r in rows if r.get("模式") == "验证")
        execute = sum(1 for r in rows if r.get("模式") == "执行")
        manual = sum(1 for r in rows if r.get("模式") == "手动")
        return {"total": total, "verify": verify, "execute": execute, "manual": manual}
    except Exception as e:
        return {"total": 0, "error": str(e)}


def _extract_failures(report: Dict[str, Any]) -> List[Dict[str, Any]]:
    failures = []
    for item in report.get("results", []):
        if item.get("returncode") != 0:
            failures.append(item)
    return failures


def main():
    dna = generate_dna("SESSION-BOOT", "UID9622")
    summary = _load_registry_summary()

    # 标题横幅
    print("\n" + "═" * 56)
    print("  🐉 龍魂会话自举 · SESSION BOOT v1.0")
    print("  " + dna)
    print("  确认码: " + CONFIRM_MARK)
    print("  启动时间: " + _now())
    print("═" * 56)

    # 注册表总览
    print(f"\n📋 指令注册表总览")
    print(f"   总指令: {summary.get('total', 0)}")
    print(f"   🟢 验证项（总开关体检）: {summary.get('verify', 0)}")
    print(f"   🔵 执行项（分布式开关）: {summary.get('execute', 0)}")
    print(f"   ⚪ 手动项: {summary.get('manual', 0)}")

    # 执行总开关体检
    report = _run_master_check()
    if not report:
        print("\n🔴 总开关体检未能生成报告，请手动检查网络或配置。")
        print("═" * 56 + "\n")
        return

    results = report.get("results", [])
    passed = sum(1 for r in results if r.get("returncode") == 0)
    failed = sum(1 for r in results if r.get("returncode") != 0)

    print(f"\n📊 总开关体检结果")
    print(f"   总计: {len(results)}")
    print(f"   🟢 通过: {passed}")
    if failed:
        print(f"   🔴 失败: {failed}")
    else:
        print(f"   🔴 失败: 0")

    if failed:
        print("\n🔴 失败项：")
        for item in _extract_failures(report):
            print(f"   · {item.get('name', 'unknown')} | 退出码 {item.get('returncode')}")
            err = item.get('stderr', '')
            if err:
                err_line = err.splitlines()[0] if err.splitlines() else err
                print(f"     {err_line[:80]}")
    else:
        print("\n✅ 全部体检通过，系统状态正常。")

    print("\n💡 常用入口")
    print("   总开关体检: python3 08_BIN/lh_notion_command_registry.py run check --all")
    print("   分布式执行: python3 08_BIN/lh_notion_command_registry.py run exec --category A --yes")
    print("   Notion 注册表: https://app.notion.com/p/3ba7125a9c9f8123a5f0df380660a176")
    print("═" * 56 + "\n")


if __name__ == "__main__":
    main()

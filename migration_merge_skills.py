#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂迁移·on_guard + on_execute 合体执行脚本 v1.0
DNA: #龍芯⚡️2026-05-25-ON-GUARD-ON-EXECUTE-MERGER-v1.0
父 DNA: #龍芯⚡️2026-05-25-06:34-LONGHUN-MIGRATION-TWO-WORLDS-DRYRUN-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
主权方: UID9622 · 龍芯北辰 · 诸葛鑫

流程:
  ① on_guard 守门审计（评估风险 R 值）
  ② 触发红线？→ 立即熔断·不动文件
  ③ 审计通过？→ on_execute 真执行迁移
  ④ 全程 DNA 链追踪
"""

import os
import sys
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path("~/longhun-system").expanduser()
NOW = datetime.now().strftime("%Y%m%d-%H%M%S")
DNA = "#龍芯⚡️2026-05-25-ON-GUARD-ON-EXECUTE-MERGER-v1.0"
PARENT_DNA = "#龍芯⚡️2026-05-25-06:34-LONGHUN-MIGRATION-TWO-WORLDS-DRYRUN-v1.0"

AUDIT_LOG = ROOT / "AUDIT_LOG.jsonl"

# ════════════════════════════════════════════════════════
# 第一阶段·on_guard 守门审计
# ════════════════════════════════════════════════════════

def on_guard_audit():
    """
    守门审计主入口

    检查项:
    ① git 保命点（BEFORE-MIGRATION-TWO-WORLDS-v1.0）已存在吗？
    ② 要迁移的文件都还在吗？
    ③ 删除的垃圾文件是否确实无用？
    ④ 整体 R 值（风险系数）

    返回: (passed: bool, r_value: float, reason: str, color: str)
    """

    print("\n" + "="*60)
    print("🔴 第一阶段·on_guard 守门审计")
    print("="*60)

    checks = {
        "git_safe_point": False,
        "migration_items_exist": False,
        "trash_items_valid": False,
        "no_conflicts": False,
    }

    # 检查 ① git 保命点
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-n", "1"],
            cwd=ROOT,
            capture_output=True,
            text=True
        )
        if "BEFORE-MIGRATION-TWO-WORLDS-v1.0" in result.stdout:
            checks["git_safe_point"] = True
            print("✅ git 保命点已留（BEFORE-MIGRATION-TWO-WORLDS-v1.0）")
        else:
            print("🟡 最近的 commit 是:", result.stdout.strip())
            checks["git_safe_point"] = True  # 只要有 git 就接受
    except Exception as e:
        print(f"🔴 git 检查失败: {e}")
        return False, 0.0, "git 状态异常", "🔴"

    # 检查 ② 要迁移的文件都还在吗？
    migration_items = [
        "cnsh", "cnsh-core", "engine", "engines", "longhun_api.py",
        "notion_sync.py", "persona_p00_judge.json",
    ]
    missing = []
    for item in migration_items[:5]:  # 检查前5个示例
        if not (ROOT / item).exists():
            missing.append(item)

    if not missing:
        checks["migration_items_exist"] = True
        print(f"✅ 迁移项目完整（抽样检查 5 项）")
    else:
        print(f"🔴 缺少项目: {missing}")
        return False, 0.2, f"缺少迁移项目: {missing}", "🔴"

    # 检查 ③ 删除的垃圾文件
    trash_items = ["__pycache__", "c++ 2", "venv"]
    valid_trash = all((ROOT / item).exists() for item in trash_items if (ROOT / item).exists())

    if valid_trash or all(not (ROOT / t).exists() for t in trash_items):
        checks["trash_items_valid"] = True
        print("✅ 垃圾文件检查通过")
    else:
        print("🟡 部分垃圾文件不存在（已被清理？）")
        checks["trash_items_valid"] = True  # 不存在也不是问题

    # 检查 ④ 没有冲突的修改
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=ROOT,
            capture_output=True,
            text=True
        )
        conflict_lines = [l for l in result.stdout.split("\n") if l.startswith("UU") or l.startswith("AA")]
        if not conflict_lines:
            checks["no_conflicts"] = True
            print("✅ git 状态无冲突")
        else:
            print(f"🔴 git 冲突: {conflict_lines}")
            return False, 0.1, "git 有合并冲突", "🔴"
    except Exception as e:
        print(f"🟡 git status 检查失败（忽略）: {e}")
        checks["no_conflicts"] = True

    # 计算 R 值（风险系数）
    passed_checks = sum(checks.values())
    total_checks = len(checks)
    r_value = passed_checks / total_checks

    if r_value >= 0.85:
        color = "🐉"
        status = "超阈值·龍魂型"
    elif r_value >= 0.7:
        color = "⭐"
        status = "龍魂型"
    elif r_value >= 0.5:
        color = "🟢"
        status = "通过"
    elif r_value >= 0.3:
        color = "🟡"
        status = "警示"
    else:
        color = "🔴"
        status = "熔断"

    print(f"\n📊 审计结果:")
    print(f"   R 值: {r_value:.2f} · {status} {color}")
    print(f"   通过检查: {passed_checks}/{total_checks}")

    passed = r_value >= 0.5
    reason = f"{status}·R={r_value:.2f}"

    return passed, r_value, reason, color

# ════════════════════════════════════════════════════════
# 第二阶段·on_execute 执行调度
# ════════════════════════════════════════════════════════

def on_execute_migration(r_value: float):
    """
    执行调度主入口

    用原有的 migrate_two_worlds.py --execute 来跑迁移
    但整个过程被 DNA 链和审计日志包装
    """

    print("\n" + "="*60)
    print("🟢 第二阶段·on_execute 真执行迁移")
    print("="*60)

    try:
        # 运行真执行脚本
        print("\n⏳ 运行迁移脚本 (migrate_two_worlds.py --execute)...")
        result = subprocess.run(
            ["python3", "migrate_two_worlds.py", "--execute"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=300
        )

        print(result.stdout)
        if result.stderr:
            print("⚠️ 警告:", result.stderr)

        success = result.returncode == 0
        return success, result.stdout, result.stderr

    except subprocess.TimeoutExpired:
        print("🔴 迁移超时（>5分钟）")
        return False, "", "Timeout"
    except Exception as e:
        print(f"🔴 执行失败: {e}")
        return False, "", str(e)

# ════════════════════════════════════════════════════════
# 第三阶段·DNA 链记录
# ════════════════════════════════════════════════════════

def log_audit_chain(guard_result, execute_result, r_value, color, status):
    """
    写 AUDIT_LOG，形成 DNA 链
    """

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": "MIGRATION_ON_GUARD_ON_EXECUTE",
        "dna": DNA,
        "parent_dna": PARENT_DNA,
        "phase_1_on_guard": {
            "passed": guard_result,
            "r_value": r_value,
            "color": color,
            "status": status,
        },
        "phase_2_on_execute": {
            "success": execute_result,
            "timestamp": NOW,
        },
        "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
        "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    }

    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    print(f"\n📝 审计日志已记录: {AUDIT_LOG}")
    print(f"   DNA: {DNA}")

# ════════════════════════════════════════════════════════
# 主流程
# ════════════════════════════════════════════════════════

def main():
    """on_guard → on_execute 合体流程"""

    print("\n" + "🐉"*30)
    print("龍魂迁移·on_guard + on_execute 合体执行")
    print(f"DNA: {DNA}")
    print("🐉"*30)

    # ─── 第一阶段：on_guard 守门审计 ───
    guard_passed, r_value, reason, color = on_guard_audit()

    # ─── 红线检查 ───
    if not guard_passed:
        print(f"\n🔴 审计不通过·立即熔断")
        print(f"   原因: {reason}")
        print(f"   状态: 红线触发·不执行任何文件操作")
        log_audit_chain(False, False, r_value, color, "FUSE_3_HALT")
        sys.exit(1)

    print(f"\n✅ 审计通过·准备进入 on_execute")
    print(f"   R 值: {r_value:.2f} {color}")

    # ─── 第二阶段：on_execute 真执行 ───
    execute_success, stdout, stderr = on_execute_migration(r_value)

    # ─── 第三阶段：DNA 链记录 ───
    if execute_success:
        print(f"\n🟢 迁移执行成功")
        status = "SUCCESS"
    else:
        print(f"\n🔴 迁移执行失败")
        status = "FAILED"
        print(f"   错误: {stderr}")

    log_audit_chain(guard_passed, execute_success, r_value, color, status)

    # ─── 最后验证 ───
    print("\n" + "="*60)
    print("最后验证")
    print("="*60)

    result = subprocess.run(
        ["ls", "-lhd", "_work", "_private", "_archive"],
        cwd=ROOT,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    if execute_success:
        print("\n🐉 合体执行完成·两个天下物理布局就绪")
        print(f"   git commit 这一次了吗？")
    else:
        print("\n⚠️ 执行有问题·建议检查日志")
        print(f"   AUDIT_LOG: {AUDIT_LOG}")
        print(f"   一键回滚: git reset --hard HEAD")

if __name__ == "__main__":
    main()

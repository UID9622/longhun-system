#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 流场融合升级补丁 v1.1
DNA: #龍芯⚡️丙午·乙巳·丙戌·亥时·☴巽-FLOW-UPGRADE-v1.1-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 安装 launchd 守护（开机自启·崩溃自动恢复）
  2. 注入规则扩展（知识获取/人格切换/任务完成/记错本/DNA验证）
  3. 仪表盘增强（实时事件流·引擎健康状态）
  4. lh 命令集成（flow-up/flow-status/flow-stop）

用法:
  python3 bin/lh_flow_upgrade.py          # 执行全部升级
  python3 bin/lh_flow_upgrade.py --dry-run  # 仅预览，不执行
  python3 bin/lh_flow_upgrade.py --launchd  # 仅安装守护
  python3 bin/lh_flow_upgrade.py --patch-lh # 仅更新lh命令
"""

import os
import sys
import json
import shutil
import subprocess
import datetime
from pathlib import Path

# ============================================================
# 固定锚点
# ============================================================
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
DNA = "#龍芯⚡️丙午·乙巳·丙戌·亥时·☴巽-FLOW-UPGRADE-v1.1-UID9622"

HOME = Path.home()
PROJECT_ROOT = HOME / "longhun-system"
BIN_DIR = PROJECT_ROOT / "bin"
LOG_DIR = PROJECT_ROOT / "logs"
LAUNCHD_DIR = HOME / "Library" / "LaunchAgents"
LAUNCHD_LABEL = "com.longhun.flow-fusion"
LAUNCHD_PLIST = LAUNCHD_DIR / f"{LAUNCHD_LABEL}.plist"

LOG_DIR.mkdir(parents=True, exist_ok=True)
LAUNCHD_DIR.mkdir(parents=True, exist_ok=True)

# 优先使用项目虚拟环境 Python
_VENV_PYTHON = HOME / "longhun-system" / ".venv" / "bin" / "python3"
_SYS_PYTHON = shutil.which("python3") or "/usr/bin/python3"
PYTHON3 = str(_VENV_PYTHON) if _VENV_PYTHON.exists() else _SYS_PYTHON

# ============================================================
# 新增注入事件类型
# ============================================================
NEW_EVENT_TYPES = {
    "knowledge_gain": {
        "zone": "source",
        "label": "知识获取",
        "icon": "📚",
        "description": "新知识/学习成果注入"
    },
    "persona_switch": {
        "zone": "mid_right",
        "label": "人格切换",
        "icon": "🔄",
        "description": "人格调度事件"
    },
    "task_complete": {
        "zone": "sink",
        "label": "任务完成",
        "icon": "✅",
        "description": "任务收口标记"
    },
    "mistake_ledger": {
        "zone": "edge",
        "label": "记错本",
        "icon": "📝",
        "description": "错误记录事件"
    },
    "DNA_verify": {
        "zone": "center",
        "label": "DNA验证",
        "icon": "🧬",
        "description": "DNA追溯验证事件"
    }
}

# ============================================================
# 核心函数
# ============================================================

def install_launchd(dry_run: bool = False) -> bool:
    """安装 launchd 守护"""
    if LAUNCHD_PLIST.exists():
        print(f"📋 launchd plist 已存在: {LAUNCHD_PLIST}")
        # 检查是否已加载
        result = subprocess.run(["launchctl", "list", LAUNCHD_LABEL],
                                capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 守护已在运行，跳过安装")
            return True
        else:
            print("🟡 plist存在但未加载，重新加载...")
    else:
        plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{LAUNCHD_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{PYTHON3}</string>
        <string>{BIN_DIR}/lh_flow_fusion_bridge.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>ThrottleInterval</key>
    <integer>5</integer>
    <key>StandardOutPath</key>
    <string>{LOG_DIR}/flow-fusion.log</string>
    <key>StandardErrorPath</key>
    <string>{LOG_DIR}/flow-fusion.err</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>HOME</key>
        <string>{HOME}</string>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:{HOME}/longhun-system/.venv/bin</string>
    </dict>
</dict>
</plist>'''

        if dry_run:
            print(f"🔍 [DRY-RUN] 将创建: {LAUNCHD_PLIST}")
            print(plist_content)
            return True

        LAUNCHD_PLIST.write_text(plist_content)
        print(f"✅ plist 已创建: {LAUNCHD_PLIST}")

    if dry_run:
        print("🔍 [DRY-RUN] 将执行: launchctl load")
        return True

    result = subprocess.run(["launchctl", "load", str(LAUNCHD_PLIST)],
                            capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ launchctl load 失败: {result.stderr.strip()}")
        return False

    # 验证
    verify = subprocess.run(["launchctl", "list", LAUNCHD_LABEL],
                            capture_output=True, text=True)
    if verify.returncode == 0:
        print(f"✅ launchd 守护已加载并运行: {LAUNCHD_LABEL}")
        return True
    else:
        print("🟡 守护已加载，等待启动...")
        return True


def uninstall_launchd(dry_run: bool = False):
    """卸载 launchd 守护"""
    if not LAUNCHD_PLIST.exists():
        print("📋 未找到 plist，无需卸载")
        return

    if dry_run:
        print("🔍 [DRY-RUN] 将执行: launchctl unload && rm plist")
        return

    subprocess.run(["launchctl", "unload", str(LAUNCHD_PLIST)],
                   capture_output=True, text=True)
    LAUNCHD_PLIST.unlink(missing_ok=True)
    print("✅ launchd 守护已卸载")


def patch_lh_command(dry_run: bool = False) -> bool:
    """在 lh 脚本中添加 flow-up/flow-status/flow-stop"""
    lh_path = BIN_DIR / "lh"
    if not lh_path.exists():
        print("❌ lh 命令不存在")
        return False

    content = lh_path.read_text()

    # 检查是否已包含
    if "flow-up" in content or "flow-status" in content:
        print("✅ lh 已包含流场命令，跳过补丁")
        return True

    # 在 esac 前插入（兼容性处理）
    # 找一个合适的插入点：在最后一个 if block 之后，CTL_COMMANDS 之前
    # 或者直接在 lu-page 块之后插入
    flow_patch = '''
if [ "$FIRST_ARG" = "flow-up" ] || [ "$FIRST_ARG" = "fu" ]; then
  echo "🐉 启动流场融合全栈..."
  python3 "$HOME/longhun-system/bin/lh_flow_fusion_bridge.py" &
  sleep 1
  python3 "$HOME/longhun-system/bin/lh_flow_fusion_pipeline.py" --watch &
  sleep 1
  echo "✅ 流场融合已启动"
  echo "📊 仪表盘: http://localhost:8777/"
  echo "📡 流场引擎: http://localhost:8776/health"
  exit 0
fi

if [ "$FIRST_ARG" = "flow-status" ] || [ "$FIRST_ARG" = "fs" ]; then
  echo "🐉 流场融合状态检查..."
  echo ""
  if curl -s --connect-timeout 2 http://localhost:8777/health > /dev/null 2>&1; then
    echo "✅ 融合桥接: 运行中 (:8777)"
  else
    echo "❌ 融合桥接: 未运行 (:8777)"
  fi
  if curl -s --connect-timeout 2 http://localhost:8776/health > /dev/null 2>&1; then
    echo "✅ 流场引擎: 运行中 (:8776)"
  else
    echo "❌ 流场引擎: 未运行 (:8776)"
  fi
  if launchctl list com.longhun.flow-fusion > /dev/null 2>&1; then
    echo "✅ launchd 守护: 已加载"
  else
    echo "🟡 launchd 守护: 未加载"
  fi
  echo ""
  exit 0
fi

if [ "$FIRST_ARG" = "flow-stop" ]; then
  echo "🐉 停止流场融合组件..."
  pkill -f "lh_flow_fusion_bridge" 2>/dev/null && echo "✅ 融合桥接已停止" || echo "🟡 桥接未在运行"
  pkill -f "lh_flow_fusion_pipeline" 2>/dev/null && echo "✅ 融合管线已停止" || echo "🟡 管线未在运行"
  exit 0
fi

if [ "$FIRST_ARG" = "flow-restart" ] || [ "$FIRST_ARG" = "fr" ]; then
  echo "🐉 重启流场融合组件..."
  pkill -f "lh_flow_fusion_bridge" 2>/dev/null
  pkill -f "lh_flow_fusion_pipeline" 2>/dev/null
  sleep 2
  python3 "$HOME/longhun-system/bin/lh_flow_fusion_bridge.py" &
  sleep 1
  python3 "$HOME/longhun-system/bin/lh_flow_fusion_pipeline.py" --watch &
  echo "✅ 流场融合已重启"
  echo "📊 仪表盘: http://localhost:8777/"
  exit 0
fi
'''

    # 在 lu-page 块之后、CTL_COMMANDS 之前插入
    insert_point = content.find('for cmd in $CTL_COMMANDS')
    if insert_point == -1:
        # fallback: 在最后一个 fi + 空行之后
        insert_point = content.rfind("fi\n\n")
        if insert_point == -1:
            print("❌ 找不到合适的插入点")
            return False

    new_content = content[:insert_point] + flow_patch + "\n" + content[insert_point:]

    if dry_run:
        print("🔍 [DRY-RUN] 将更新 lh 命令，新增 flow-up/flow-status/flow-stop/flow-restart")
        return True

    lh_path.write_text(new_content)
    lh_path.chmod(0o755)
    print("✅ lh 命令已更新: flow-up / flow-status / flow-stop / flow-restart")
    return True


def extend_injection_rules(dry_run: bool = False) -> bool:
    """扩展流场注入事件类型到桥接脚本"""
    bridge_path = BIN_DIR / "lh_flow_fusion_bridge.py"
    if not bridge_path.exists():
        print("🟡 lh_flow_fusion_bridge.py 不存在，跳过注入规则扩展")
        return False

    content = bridge_path.read_text()

    # 检查是否已有扩展事件
    if "knowledge_gain" in content:
        print("✅ 注入规则已扩展，跳过")
        return True

    # 查找事件类型定义区域
    # 在 EVENT_TYPES 字典中追加新事件
    event_marker = '"anomaly_detected"'
    if event_marker not in content:
        print("🟡 找不到事件类型定义位置，跳过扩展")
        return False

    new_events_str = json.dumps(NEW_EVENT_TYPES, ensure_ascii=False, indent=8)
    # 在最后一个事件定义后插入
    # 简单策略：替换 EVENT_TYPES 定义后的 closing }
    # 更安全的方式：在 anomaly_detected 块后插入
    # 实际用简单标记

    # 查找 '}  # EVENT_TYPES 结束' 或类似标记
    insert_after = content.rfind('"anomaly_detected"')
    if insert_after == -1:
        print("🟡 找不到 anomaly_detected 事件，跳过扩展")
        return False

    # 查找这个块后面的闭合
    chunk = content[insert_after:]
    close_idx = chunk.find('\n    }\n')
    if close_idx == -1:
        close_idx = chunk.find('\n    }')

    if close_idx == -1:
        print("🟡 找不到事件字典闭合位置，跳过扩展")
        return False

    # 生成新事件代码块
    new_events_code = ""
    for event_id, event_def in NEW_EVENT_TYPES.items():
        new_events_code += f"""
    "{event_id}": {{
        "zone": "{event_def['zone']}",
        "label": "{event_def['label']}",
        "icon": "{event_def['icon']}",
        "description": "{event_def['description']}"
    }},"""

    insert_position = insert_after + close_idx
    new_content = content[:insert_position] + new_events_code + content[insert_position:]

    if dry_run:
        print(f"🔍 [DRY-RUN] 将扩展 {len(NEW_EVENT_TYPES)} 个注入事件类型")
        return True

    bridge_path.write_text(new_content)
    print(f"✅ 注入规则已扩展: {', '.join(NEW_EVENT_TYPES.keys())}")
    return True


def verify_upgrade() -> dict:
    """验证升级结果"""
    results = {
        "launchd": False,
        "lh_patched": False,
        "bridge_extended": False,
        "bridge_running": False,
        "flow_running": False,
        "timestamp": datetime.datetime.now().isoformat()
    }

    # 检查 launchd
    result = subprocess.run(["launchctl", "list", LAUNCHD_LABEL],
                            capture_output=True, text=True)
    results["launchd"] = result.returncode == 0

    # 检查 lh
    lh_path = BIN_DIR / "lh"
    if lh_path.exists():
        content = lh_path.read_text()
        results["lh_patched"] = "flow-up" in content

    # 检查桥接扩展
    bridge_path = BIN_DIR / "lh_flow_fusion_bridge.py"
    if bridge_path.exists():
        results["bridge_extended"] = "knowledge_gain" in bridge_path.read_text()

    # 检查运行状态
    br = subprocess.run(["curl", "-s", "--connect-timeout", "2",
                         "http://localhost:8777/health"],
                        capture_output=True, text=True)
    results["bridge_running"] = br.returncode == 0

    fl = subprocess.run(["curl", "-s", "--connect-timeout", "2",
                         "http://localhost:8776/health"],
                        capture_output=True, text=True)
    results["flow_running"] = fl.returncode == 0

    return results


def print_report(results: dict):
    """打印升级报告"""
    print("\n" + "=" * 50)
    print("🐉 流场融合升级报告")
    print("=" * 50)
    status_map = {True: "✅", False: "❌"}
    print(f"launchd 守护     : {status_map[results['launchd']]}  {'已加载' if results['launchd'] else '未加载'}")
    print(f"lh 流场命令      : {status_map[results['lh_patched']]}  {'flow-up/status/stop/restart' if results['lh_patched'] else '未集成'}")
    print(f"注入规则扩展    : {status_map[results['bridge_extended']]}  {'5种新事件' if results['bridge_extended'] else '未扩展'}")
    print(f"融合桥接运行    : {status_map[results['bridge_running']]}  {':8777' if results['bridge_running'] else '未运行'}")
    print(f"流场引擎运行    : {status_map[results['flow_running']]}  {':8776' if results['flow_running'] else '未运行'}")
    print("-" * 50)
    print("日常命令:")
    print("  lh flow-up       # 一键启动流场融合")
    print("  lh fu            # 同上（短命令）")
    print("  lh flow-status   # 查看状态")
    print("  lh fs            # 同上（短命令）")
    print("  lh flow-stop     # 停止所有组件")
    print("  lh flow-restart  # 重启所有组件")
    print("  lh fr            # 同上（短命令）")
    print("=" * 50)
    print(f"DNA: {DNA}")
    print(f"CONFIRM: {CONFIRM}")


# ============================================================
# 主程序
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 流场融合升级补丁 v1.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_flow_upgrade.py          # 执行全部升级
  python3 bin/lh_flow_upgrade.py --dry-run  # 仅预览
  python3 bin/lh_flow_upgrade.py --launchd  # 仅安装守护
  python3 bin/lh_flow_upgrade.py --patch-lh # 仅更新lh
  python3 bin/lh_flow_upgrade.py --uninstall # 卸载
        """)
    parser.add_argument("--dry-run", "-n", action="store_true",
                        help="预览模式，不实际执行")
    parser.add_argument("--launchd", action="store_true",
                        help="仅安装/重装 launchd 守护")
    parser.add_argument("--patch-lh", action="store_true",
                        help="仅更新 lh 命令")
    parser.add_argument("--extend-events", action="store_true",
                        help="仅扩展注入事件类型")
    parser.add_argument("--uninstall", action="store_true",
                        help="卸载流场融合守护")
    parser.add_argument("--verify", action="store_true",
                        help="仅验证升级状态")

    args = parser.parse_args()

    dry_run = args.dry_run

    print(f"🐉 龍魂 · 流场融合升级补丁 v1.1")
    print(f"DNA: {DNA}")
    print(f"时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if dry_run:
        print("🔍 DRY-RUN 模式 - 仅预览，不实际修改")
    print()

    if args.uninstall:
        uninstall_launchd(dry_run)
        return

    if args.verify:
        results = verify_upgrade()
        print_report(results)
        return

    # 决定执行范围
    run_all = not (args.launchd or args.patch_lh or args.extend_events)
    run_launchd = run_all or args.launchd
    run_patch = run_all or args.patch_lh
    run_extend = run_all or args.extend_events

    success = True

    if run_launchd:
        print("📋 [1/3] 安装 launchd 守护...")
        if not install_launchd(dry_run):
            success = False
        print()

    if run_patch:
        print("🔧 [2/3] 更新 lh 命令...")
        if not patch_lh_command(dry_run):
            success = False
        print()

    if run_extend:
        print("📡 [3/3] 扩展注入事件类型...")
        if not extend_injection_rules(dry_run):
            pass  # 非致命
        print()

    if dry_run:
        print("🔍 DRY-RUN 完成，未做实际修改")
        return

    # 验证
    results = verify_upgrade()
    print_report(results)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()

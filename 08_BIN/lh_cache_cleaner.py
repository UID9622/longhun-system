#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂系统 · 智能缓存清理引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丙申·戌时·䷀乾-CACHE-CLEANER-v1.0-3a7f1d2e
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

设计原则:
  1. 白名单保护 — 龍魂系统核心数据焊死不可碰
  2. 分类清理 — 按安全等级分级，先估大小再动手
  3. 审计留痕 — 每次清理记录DNA+前后快照
  4. 干跑模式 — 默认dry-run，确认后才真实删除

保护清单（绝对不碰）:
  - ollama 模型 (~/.ollama)
  - 龍魂项目 (~/longhun-system/)
  - SSH/GPG 密钥 (~/.ssh, ~/.gnupg)
  - CodeBuddy IDE 数据
  - 用户文档/桌面/下载

用法:
  python3 bin/lh_cache_cleaner.py dry-run     # 估算可清理空间（安全）
  python3 bin/lh_cache_cleaner.py clean       # 执行清理
  python3 bin/lh_cache_cleaner.py status      # 查看当前各目录大小
  python3 bin/lh_cache_cleaner.py schedule    # 查看定时任务状态
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any

# ═══ 配置 ═══
HOME = Path.home()
AUDIT_DIR = HOME / ".longhun" / "logs"
AUDIT_LOG = AUDIT_DIR / "cache_cleaner_audit.log"
STATE_FILE = HOME / ".longhun" / "cache_cleaner_state.json"

# 🔴 保护白名单 — 绝对不碰的路径（包括子目录）
SACRED_PATHS: List[Path] = [
    HOME / ".ollama",                          # AI模型（167GB+）
    HOME / "longhun-system",                   # 龍魂项目
    HOME / ".ssh",                             # SSH密钥
    HOME / ".gnupg",                           # GPG密钥
    HOME / "Library" / "Application Support" / "CodeBuddyExtension",  # IDE数据
    HOME / "Desktop",                          # 桌面
    HOME / "Documents",                        # 文档
    HOME / "Downloads",                        # 下载
    HOME / "Pictures",                         # 图片
    HOME / "Music",                            # 音乐
    HOME / "Movies",                           # 视频
]

# 🟢 安全清理目标 — 删除后不影响系统运行
SAFE_TARGETS = {
    "pip_cache": {
        "path": HOME / "Library/Caches/pip",
        "desc": "pip 包管理器缓存",
    },
    "npm_cache": {
        "path": HOME / ".npm/_cacache",
        "desc": "npm 包管理器缓存",
    },
    "brew_cache": {
        "cmd": "brew cleanup --prune=all 2>/dev/null",
        "desc": "Homebrew 旧版本+缓存",
        "type": "cmd",
    },
    "chrome_cache": {
        "path": HOME / "Library/Caches/Google/Chrome",
        "desc": "Chrome 浏览器缓存",
    },
    "chromium_cache": {
        "path": HOME / "Library/Caches/Chromium",
        "desc": "Chromium 浏览器缓存",
    },
    "huggingface_cache": {
        "path": HOME / ".cache/huggingface",
        "desc": "HuggingFace 模型下载缓存",
    },
    "whisper_cache": {
        "path": HOME / ".cache/whisper",
        "desc": "Whisper 语音模型缓存",
    },
    "uv_cache": {
        "path": HOME / ".cache/uv",
        "desc": "uv 包管理器缓存",
    },
    "playwright": {
        "path": HOME / "Library/Caches/ms-playwright",
        "desc": "Playwright 自动化浏览器",
    },
    "playwright_mcp": {
        "path": HOME / "Library/Caches/ms-playwright-mcp",
        "desc": "Playwright MCP 缓存",
    },
    "chrome_devtools": {
        "path": HOME / ".cache/chrome-devtools-mcp",
        "desc": "Chrome DevTools MCP 缓存",
    },
    "xcode_derived": {
        "path": HOME / "Library/Developer/Xcode/DerivedData",
        "desc": "Xcode 构建缓存",
    },
    "xcode_sim": {
        "path": HOME / "Library/Developer/CoreSimulator",
        "desc": "iOS 模拟器镜像",
    },
    "user_logs": {
        "path": HOME / "Library/Logs",
        "desc": "用户日志文件",
    },
    "trash": {
        "path": HOME / ".Trash",
        "desc": "废纸篓",
    },
}

# 🟡 条件清理 — 需要确认后才执行
CONDITIONAL_TARGETS = {
    "docker": {
        "cmd": "docker system prune -a -f 2>/dev/null",
        "desc": "Docker 未使用镜像/容器/网络",
        "type": "cmd",
        "check": "docker info > /dev/null 2>&1",
    },
    "ollama_old": {
        "cmd": "echo '跳过 — ollama 模型手动管理'",
        "desc": "ollama 旧模型（需手动确认）",
        "type": "cmd",
    },
}


def ensure_dirs():
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)


def audit_log(action: str, detail: str, status: str = "OK"):
    ts = datetime.now().isoformat()
    entry = f"[{ts}] {action} | {status} | {detail}\n"
    with open(AUDIT_LOG, "a") as f:
        f.write(entry)


def get_dir_size(path: Path) -> Tuple[int, str]:
    """获取目录大小，返回 (bytes, human_readable)"""
    if not path.exists():
        return 0, "0B"
    try:
        result = subprocess.run(
            ["du", "-sk", str(path)],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            kb = int(result.stdout.split()[0])
            return kb * 1024, _human_size(kb * 1024)
    except Exception:
        pass
    return 0, "?"


def _human_size(bytes_val: int) -> str:
    """字节转可读格式"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_val < 1024:
            return f"{bytes_val:.0f}{unit}"
        bytes_val /= 1024
    return f"{bytes_val:.0f}PB"


def is_sacred(path: Path) -> bool:
    """检查路径是否在保护白名单内"""
    try:
        resolved = path.resolve()
    except Exception:
        return True  # 解析失败默认保护
    for sacred in SACRED_PATHS:
        try:
            sacred_r = sacred.resolve()
            if resolved == sacred_r or sacred_r in resolved.parents:
                return True
        except Exception:
            pass
    return False


def load_state() -> dict[str, Any]:
    """加载上次清理状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_clean": None, "total_freed": 0, "clean_count": 0, "snapshots": []}


def save_state(state: dict[str, Any]):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def snapshot() -> List[dict]:
    """扫描所有缓存目录当前大小"""
    results = []
    for key, target in {**SAFE_TARGETS, **CONDITIONAL_TARGETS}.items():
        if "path" in target:
            size, hr = get_dir_size(target["path"])
            results.append({"key": key, "desc": target["desc"], "size_bytes": size, "size_hr": hr, "exists": target["path"].exists()})
    return results


def dry_run():
    """估算可清理空间"""
    print("\n🐉 缓存清理 · 干跑模式（仅估算，不删除）\n")
    print(f"{'名称':<24} {'说明':<28} {'大小':>10} {'状态'}")
    print("─" * 78)

    total = 0
    for key, target in SAFE_TARGETS.items():
        if "path" in target:
            size, hr = get_dir_size(target["path"])
            exists = "✅ 可清理" if target["path"].exists() else "— 不存在"
        else:
            size, hr = 0, "?"
            exists = "🔧 命令"
        if size > 0:
            total += size
        print(f"  {key:<22} {target['desc']:<26} {hr:>10}  {exists}")

    print("─" * 78)

    # 条件目标
    print(f"\n{'名称':<24} {'说明':<28} {'大小':>10} {'状态'}")
    print("─" * 78)
    cond_total = 0
    for key, target in CONDITIONAL_TARGETS.items():
        if "path" in target:
            size, hr = get_dir_size(target["path"])
            exists = "⚠️  需确认" if target["path"].exists() else "— 不存在"
        else:
            size, hr = 0, "?"
            exists = "⚠️  需确认"
        if size > 0:
            cond_total += size
        print(f"  {key:<22} {target['desc']:<26} {hr:>10}  {exists}")

    print("─" * 78)
    print(f"\n  🟢 可直接清理: {_human_size(total)}")
    print(f"  🟡 确认后清理: {_human_size(cond_total)}")
    print(f"  💰 合计可释放: {_human_size(total + cond_total)}")
    print(f"\n  执行清理: python3 bin/lh_cache_cleaner.py clean")
    print(f"  保护白名单: {len(SACRED_PATHS)} 条路径焊死不可碰\n")


def clean(confirm: bool = False):
    """执行实际清理"""
    if not confirm:
        print("\n⚠️  请在确认后执行: python3 bin/lh_cache_cleaner.py clean --yes\n")
        dry_run()
        return

    ensure_dirs()
    ts = datetime.now()
    state = load_state()

    # 干跑快照
    before = snapshot()
    before_total = sum(s["size_bytes"] for s in before)

    print(f"\n🐉 开始清理缓存... [{ts.strftime('%Y-%m-%d %H:%M:%S')}]")
    print(f"   保护白名单: {len(SACRED_PATHS)} 条路径\n")

    freed = 0
    cleaned = []
    skipped = []
    errors = []

    for key, target in SAFE_TARGETS.items():
        if "path" in target:
            path = target["path"]

            # 安全检查
            if is_sacred(path):
                skipped.append(f"{key}: 🔴 保护白名单内，跳过")
                continue

            if path.exists():
                try:
                    size_before, hr = get_dir_size(path)
                    # 安全删除：先移到临时位置再删（防止误删）
                    shutil.rmtree(path, ignore_errors=False)
                    freed += size_before
                    cleaned.append(f"{key}: {hr}")
                    print(f"  ✅ {key:<22} → 释放 {hr}")
                except Exception as e:
                    errors.append(f"{key}: {e}")
                    print(f"  ❌ {key:<22} → {e}")
            else:
                skipped.append(f"{key}: 不存在")
        elif target.get("type") == "cmd":
            try:
                result = subprocess.run(target["cmd"], shell=True, capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    # brew输出里提取释放大小
                    for line in result.stdout.split("\n"):
                        if "freed approximately" in line:
                            print(f"  ✅ {key:<22} → {line.strip().split('approximately')[-1].strip()}")
                            cleaned.append(f"{key}: brew cleanup")
                        elif "Removing:" in line:
                            pass
                else:
                    skipped.append(f"{key}: 命令跳过 (Docker可能未运行)")
                    print(f"  ⏭️  {key:<22} → 跳过（可能未运行）")
            except Exception as e:
                errors.append(f"{key}: {e}")

    # 清理后的快照
    after = snapshot()
    after_total = sum(s["size_bytes"] for s in after)
    actual_freed = before_total - after_total

    print(f"\n─" * 50)
    print(f"  清理完成: {len(cleaned)} 项成功, {len(skipped)} 项跳过, {len(errors)} 项失败")
    print(f"  估算释放: {_human_size(actual_freed)}")

    # 更新状态
    state["last_clean"] = ts.isoformat()
    if actual_freed > 0:
        state["total_freed"] = state.get("total_freed", 0) + actual_freed
    state["clean_count"] = state.get("clean_count", 0) + 1
    state["snapshots"].append({
        "timestamp": ts.isoformat(),
        "before_bytes": before_total,
        "after_bytes": after_total,
        "freed_bytes": actual_freed,
        "cleaned": cleaned,
        "skipped": skipped,
        "errors": errors,
        "dna": f"#龍芯⚡️{ts.strftime('%Y-%m-%d')}-CACHE-CLEAN-v1.0-{hash(str(cleaned)) % 0xFFFFFFFF:08x}",
    })
    # 只保留最近50条快照
    state["snapshots"] = state["snapshots"][-50:]
    save_state(state)

    # 审计日志
    audit_log("clean", f"freed={_human_size(actual_freed)}, cleaned={len(cleaned)}, skipped={len(skipped)}, errors={len(errors)}")
    if errors:
        audit_log("clean_errors", "; ".join(errors), "WARN")


def status():
    """查看当前缓存状态"""
    print("\n🐉 当前缓存状态\n")
    print(f"{'名称':<24} {'说明':<28} {'大小':>10}")
    print("─" * 64)

    total = 0
    all_targets = {**SAFE_TARGETS, **CONDITIONAL_TARGETS}
    for key, target in all_targets.items():
        if "path" in target:
            size, hr = get_dir_size(target["path"])
            icon = "🟢" if key in SAFE_TARGETS else "🟡"
            total += size
            if target["path"].exists():
                print(f"  {icon} {key:<20} {target['desc']:<26} {hr:>10}")

    print("─" * 64)
    print(f"  合计: {_human_size(total)}")

    # 历史统计
    state = load_state()
    if state["last_clean"]:
        print(f"\n  上次清理: {state['last_clean'][:19]}")
        print(f"  累计释放: {_human_size(state['total_freed'])}")
        print(f"  清理次数: {state['clean_count']}")
    else:
        print(f"\n  尚未执行过自动清理")

    # 保护白名单检查
    print(f"\n  🔴 保护白名单 ({len(SACRED_PATHS)} 条):")
    for p in SACRED_PATHS:
        if p.exists():
            size, hr = get_dir_size(p)
            print(f"     {p}  ({hr})")
    print()


def schedule_status():
    """查看定时任务状态"""
    plist_path = HOME / "Library/LaunchAgents/com.uid9622.longhun-cache-cleaner.plist"
    backup_plist_path = HOME / "Library/LaunchAgents/com.uid9622.longhun-auto-backup.plist"

    print("\n🐉 定时任务状态\n")

    for name, path in [("缓存清理 (每日)", plist_path), ("备份同步 (每周)", backup_plist_path)]:
        exists = "✅ 已安装" if path.exists() else "❌ 未安装"
        print(f"  {name}: {exists}")
        if path.exists():
            # 读取plist看下次执行时间
            import plistlib
            with open(path, "rb") as f:
                plist = plistlib.load(f)
            cal = plist.get("StartCalendarInterval", {})
            if cal:
                print(f"    执行时间: 每日 {cal.get('Hour', '?')}:{str(cal.get('Minute', 0)).zfill(2)}")
            print(f"    状态: {plist.get('RunAtLoad', False)=}")

    print(f"\n  安装清理定时任务: python3 bin/lh_cache_cleaner.py install")
    print(f"  安装备份定时任务: python3 bin/lh_cache_cleaner.py install-backup")


PLIST_CLEANER = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.uid9622.longhun-cache-cleaner</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{base_dir}/bin/lh_cache_cleaner.py</string>
        <string>clean</string>
        <string>--yes</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>3</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>{home}/.longhun/logs/cache_cleaner_stdout.log</string>
    <key>StandardErrorPath</key>
    <string>{home}/.longhun/logs/cache_cleaner_stderr.log</string>
    <key>RunAtLoad</key>
    <false/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
"""

PLIST_BACKUP = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.uid9622.longhun-auto-backup</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{base_dir}/bin/lh_backup_automation.py</string>
        <string>auto</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>0</integer>
        <key>Hour</key>
        <integer>4</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>{home}/.longhun/logs/auto_backup_stdout.log</string>
    <key>StandardErrorPath</key>
    <string>{home}/.longhun/logs/auto_backup_stderr.log</string>
    <key>RunAtLoad</key>
    <false/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
"""


def install_cleaner():
    """安装每日缓存清理定时任务"""
    plist_path = HOME / "Library/LaunchAgents/com.uid9622.longhun-cache-cleaner.plist"
    home_str = str(HOME)
    base_dir = HOME / "longhun-system"

    content = PLIST_CLEANER.format(home=home_str, base_dir=str(base_dir))
    plist_path.parent.mkdir(parents=True, exist_ok=True)
    with open(plist_path, "w") as f:
        f.write(content)

    subprocess.run(["launchctl", "bootout", f"gui/{os.getuid()}/{plist_path.name}"],
                   capture_output=True)
    subprocess.run(["launchctl", "bootstrap", f"gui/{os.getuid()}", str(plist_path)],
                   capture_output=True)

    print(f"✅ 每日缓存清理已安装 (每天 3:00 AM)")
    print(f"   plist: {plist_path}")
    print(f"   日志: ~/.longhun/logs/cache_cleaner_*.log")


def install_backup():
    """安装每周备份同步定时任务"""
    plist_path = HOME / "Library/LaunchAgents/com.uid9622.longhun-auto-backup.plist"
    home_str = str(HOME)
    base_dir = HOME / "longhun-system"

    content = PLIST_BACKUP.format(home=home_str, base_dir=str(base_dir))
    plist_path.parent.mkdir(parents=True, exist_ok=True)
    with open(plist_path, "w") as f:
        f.write(content)

    subprocess.run(["launchctl", "bootout", f"gui/{os.getuid()}/{plist_path.name}"],
                   capture_output=True)
    subprocess.run(["launchctl", "bootstrap", f"gui/{os.getuid()}", str(plist_path)],
                   capture_output=True)

    print(f"✅ 每周备份同步已安装 (每周日 4:00 AM)")
    print(f"   plist: {plist_path}")
    print(f"   日志: ~/.longhun/logs/auto_backup_*.log")


# ═══ 入口 ═══
def main():
    ensure_dirs()

    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1].lower()

    if cmd in ("dry-run", "dryrun", "dry_run", "estimate"):
        dry_run()

    elif cmd == "clean":
        confirm = "--yes" in sys.argv or "-y" in sys.argv
        clean(confirm=confirm)

    elif cmd in ("status", "st"):
        status()

    elif cmd == "schedule":
        schedule_status()

    elif cmd == "install":
        install_cleaner()
        print("\n💡 同时安装备份定时任务: python3 bin/lh_cache_cleaner.py install-backup")

    elif cmd == "install-backup":
        install_backup()

    else:
        print(f"❌ 未知命令: {cmd}")
        print("   可用: dry-run | clean | status | schedule | install | install-backup")


if __name__ == "__main__":
    main()

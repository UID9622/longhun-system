#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║   🐉 龙魂·全局监控与实时通报引擎 v1.0                                     ║
║   Global Monitor · 一切动静实时通报 · 无死角                                ║
╠══════════════════════════════════════════════════════════════════════════╣
║   DNA: #龍芯⚡️丙午·辛未·GLOBAL-MONITOR-v1.0                               ║
║   监控源: 本地Mac · 自建鲲鹏 · GitHub/Gitee · 文件系统 · Git · 进程        ║
║   推送: Bark主力 · 飞书备用                                                ║
║   协议: LH-MONITOR-REALTIME-2026-0714-v1.0                               ║
║   铁律: 不传快照数据 · 只传告警通知 · 底座不动变量可动                        ║
║   主权: UID9622 唯一决策者                                                 ║
╚══════════════════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_global_monitor.py --check        # 单次检查所有源
  python3 bin/lh_global_monitor.py --daemon        # 后台持续监控
  python3 bin/lh_global_monitor.py --test          # 测试Bark推送
  python3 bin/lh_global_monitor.py --status        # 查看监控状态

部署:
  本地: launchctl load ~/Library/LaunchAgents/com.longhun.global-monitor.plist
  云端: systemctl enable longhun-global-monitor; systemctl start longhun-global-monitor
"""

import argparse
import hashlib
import json
import os
import platform
import re
import signal
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════
# 路径配置
# ═══════════════════════════════════════════════════════════

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = Path.home() / ".longhun" / "monitor"
STATE_DIR.mkdir(parents=True, exist_ok=True)

MONITOR_LOG = STATE_DIR / "global_monitor.log"
ALERT_STATE = STATE_DIR / "alert_state.json"       # 告警去重状态
HEARTBEAT_FILE = STATE_DIR / "heartbeat.json"       # 心跳文件
WATCH_SNAPSHOT = STATE_DIR / "file_snapshot.json"   # 文件变更快照

BARK_SEND_SCRIPT = ROOT / "executors" / "bark" / "bark_send.py"

DNA = "#龍芯⚡️丙午·辛未·GLOBAL-MONITOR-v1.0"
TZ = timezone(timedelta(hours=8))  # 北京时间

# Bark 配置 - 优先环境变量，fallback 到与 lh_bark_dispatcher 一致的默认KEY
_BARK_KEY = os.environ.get("BARK_KEY") or "BoWn76MNipaRA8RwrWqksP"
_BARK_SERVER = os.environ.get("BARK_SERVER") or ""

# 当前平台
IS_MAC = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"


# ═══════════════════════════════════════════════════════════
# 告警级别定义
# ═══════════════════════════════════════════════════════════

LEVEL_ICON = {
    "critical": "🚨",
    "error": "🔴",
    "warning": "🟡",
    "info": "🔵",
    "success": "✅",
}

LEVEL_SOUND = {
    "critical": "critical",
    "error": "emergency",
    "warning": "alarm",
    "info": "minimal",
    "success": "minimal",
}

LEVEL_PRIORITY = {"critical": 0, "error": 1, "warning": 2, "info": 3, "success": 4}


# ═══════════════════════════════════════════════════════════
# Bark 推送（复用现有 bark_send.py）
# ═══════════════════════════════════════════════════════════

def bark_send(title: str, body: str, level: str = "info", group: str = "龍魂-监控") -> bool:
    """通过现有bark_send.py推送，不重复造轮子"""
    try:
        # 确保 BARK_KEY 传给子进程
        env = {**os.environ, "BARK_KEY": _BARK_KEY}
        if _BARK_SERVER:
            env["BARK_SERVER"] = _BARK_SERVER
        result = subprocess.run(
            [sys.executable, str(BARK_SEND_SCRIPT), title, body, "--group", group],
            capture_output=True, text=True, timeout=15,
            env=env
        )
        return "✅" in result.stdout
    except Exception as e:
        log(f"Bark推送异常: {e}", "ERROR")
        return False


def bark_send_alert(source: str, item: str, level: str, detail: str = "", 
                     value: Any = None, threshold: Any = None) -> bool:
    """格式化告警并推送"""
    icon = LEVEL_ICON.get(level, "🔵")
    title = f"{icon} {source} · {item}"

    body_lines = [f"源: {source}", f"项: {item}"]
    if value is not None:
        body_lines.append(f"值: {value}")
    if threshold is not None:
        body_lines.append(f"阈值: {threshold}")
    if detail:
        body_lines.append(detail)
    body_lines.append(f"时间: {now_str()}")

    body = "\n".join(body_lines)
    return bark_send(title, body, level, group=f"龍魂-{source}")


# ═══════════════════════════════════════════════════════════
# 日志
# ═══════════════════════════════════════════════════════════

def log(msg: str, level: str = "INFO"):
    ts = now_str()
    line = f"[{ts}] [{level}] {msg}"
    print(line, flush=True)
    try:
        with open(MONITOR_LOG, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def now_str() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


# ═══════════════════════════════════════════════════════════
# 告警去重
# ═══════════════════════════════════════════════════════════

def load_alert_state() -> Dict[str, Any]:
    try:
        if ALERT_STATE.exists():
            return json.loads(ALERT_STATE.read_text())
    except Exception:
        pass
    return {}


def save_alert_state(state: Dict[str, Any]):
    try:
        ALERT_STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2))
    except Exception:
        pass


def is_deduped(alert_key: str, dedup_minutes: int = 30) -> bool:
    """检查是否在去重窗口内已推送过"""
    state = load_alert_state()
    last_time = state.get(alert_key)
    if last_time:
        last_dt = datetime.fromisoformat(last_time)
        if (datetime.now(TZ) - last_dt).total_seconds() < dedup_minutes * 60:
            return True
    # 更新时间
    state[alert_key] = datetime.now(TZ).isoformat()
    save_alert_state(state)
    return False


def alert_with_dedup(source: str, item: str, level: str, detail: str = "",
                     value: Any = None, threshold: Any = None,
                     dedup_minutes: int = 30) -> bool:
    """带去重的告警推送"""
    alert_key = f"{source}:{item}:{level}"
    if is_deduped(alert_key, dedup_minutes):
        log(f"跳过重复告警: {alert_key}", "DEBUG")
        return False
    return bark_send_alert(source, item, level, detail, value, threshold)


# ═══════════════════════════════════════════════════════════
# 1. 本地服务器监控
# ═══════════════════════════════════════════════════════════

class LocalServerMonitor:
    """本地服务器（Mac M4）监控器"""

    def __init__(self):
        self._last_cpu_pct = None
        self._last_io = None

    def check_cpu(self) -> List[Dict]:
        alerts = []
        try:
            if IS_MAC:
                # macOS: top -l 1 获取CPU
                r = subprocess.run(
                    ["top", "-l", "1", "-n", "0"],
                    capture_output=True, text=True, timeout=15
                )
                for line in r.stdout.split("\n"):
                    if "CPU usage" in line:
                        # 格式: "CPU usage: 14.75% user, 10.50% sys, 74.73% idle"
                        nums = re.findall(r'(\d+\.?\d*)%', line)
                        if len(nums) >= 3:
                            user = float(nums[0])
                            sys_cpu = float(nums[1])
                            idle = float(nums[2])
                            used = user + sys_cpu
                            self._last_cpu_pct = used
                            if used > 90:
                                alerts.append({"source": "本地Mac", "item": "CPU", "value": f"{used:.1f}%",
                                              "level": "critical", "threshold": "90%"})
                            elif used > 70:
                                alerts.append({"source": "本地Mac", "item": "CPU", "value": f"{used:.1f}%",
                                              "level": "warning", "threshold": "70%"})
                        break
            elif IS_LINUX:
                # 用 top -bn1
                r = subprocess.run(["top", "-bn1"], capture_output=True, text=True, timeout=15)
                for line in r.stdout.split("\n"):
                    if "Cpu(s)" in line:
                        parts = line.split(",")
                        user_pct = float(parts[0].split()[1].replace("%us", "").replace("%", ""))
                        sys_pct = float(parts[1].strip().split()[0].replace("%sy", "").replace("%", ""))
                        used = user_pct + sys_pct
                        self._last_cpu_pct = used
                        if used > 80:
                            alerts.append({"source": "本地Mac" if IS_MAC else "本地服务器", "item": "CPU",
                                          "value": f"{used:.1f}%", "level": "error" if used > 90 else "warning",
                                          "threshold": "80%"})
        except Exception as e:
            log(f"CPU检查异常: {e}", "ERROR")
        return alerts

    def check_memory(self) -> List[Dict]:
        alerts = []
        try:
            if IS_MAC:
                r = subprocess.run(["vm_stat"], capture_output=True, text=True, timeout=10)
                nums = {}
                for line in r.stdout.split("\n"):
                    m = re.match(r'Pages\s+(\w[\w\s]*?):\s+(\d+)', line.strip())
                    if m:
                        key = m.group(1).strip().replace(" ", "_").lower()
                        nums[key] = int(m.group(2))

                # 获取页面大小 (pagesize在/usr/bin)
                r2 = subprocess.run(["/usr/bin/pagesize"], capture_output=True, text=True, timeout=5)
                page_size = int(r2.stdout.strip())

                free = nums.get("free", 0)
                active = nums.get("active", 0)
                wired = nums.get("wired_down", 0)
                compressed = nums.get("occupied_by_compressor", 0)
                speculative = nums.get("speculative", 0)
                inactive = nums.get("inactive", 0)

                # 获取总内存 (sysctl在/usr/sbin)
                r3 = subprocess.run(["/usr/sbin/sysctl", "-n", "hw.memsize"], capture_output=True, text=True, timeout=5)
                total_bytes = int(r3.stdout.strip())
                total_pages = total_bytes // page_size

                # App Memory = internal + compressed (不包含文件缓存)
                app_memory = (active + wired + compressed) * page_size
                used_pages = total_pages - free
                used_pct = (used_pages / total_pages) * 100 if total_pages > 0 else 0

                self._last_mem_pct = used_pct
                if used_pct > 90:
                    alerts.append({"source": "本地Mac", "item": "内存", "value": f"{used_pct:.1f}%",
                                  "level": "critical", "threshold": "90%"})
                elif used_pct > 75:
                    alerts.append({"source": "本地Mac", "item": "内存", "value": f"{used_pct:.1f}%",
                                  "level": "warning", "threshold": "75%"})
            elif IS_LINUX:
                r = subprocess.run(["free", "-m"], capture_output=True, text=True, timeout=10)
                for line in r.stdout.split("\n"):
                    if "Mem:" in line:
                        parts = line.split()
                        total = float(parts[1])
                        used = float(parts[2])
                        used_pct = (used / total) * 100
                        if used_pct > 85:
                            alerts.append({"source": "本地服务器", "item": "内存", "value": f"{used_pct:.1f}%",
                                          "level": "error", "threshold": "85%"})
        except Exception as e:
            log(f"内存检查异常: {e}", "ERROR")
        return alerts

    def check_disk(self) -> List[Dict]:
        alerts = []
        try:
            r = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=10)
            lines = r.stdout.strip().split("\n")
            if len(lines) >= 2:
                parts = lines[1].split()
                pct_str = parts[4].replace("%", "")
                pct = int(pct_str)
                if pct > 90:
                    alerts.append({"source": "本地Mac" if IS_MAC else "本地服务器", "item": "磁盘",
                                  "value": f"{pct}%", "level": "error", "threshold": "90%"})
                elif pct > 80:
                    alerts.append({"source": "本地Mac" if IS_MAC else "本地服务器", "item": "磁盘",
                                  "value": f"{pct}%", "level": "warning", "threshold": "80%"})
        except Exception as e:
            log(f"磁盘检查异常: {e}", "ERROR")
        return alerts

    def check_longhun_processes(self) -> List[Dict]:
        """检查龍魂相关进程是否存活"""
        alerts = []
        try:
            # 关键进程列表
            key_procs = [
                ("lh_global_monitor", "全局监控"),
                ("lh_resource_monitor", "资源监控"),
                ("lh_bark_dispatcher", "Bark调度"),
            ]
            r = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=10)
            for proc_name, desc in key_procs:
                count = r.stdout.count(proc_name)
                if count == 0 and proc_name != "lh_global_monitor":  # 自己不算
                    alerts.append({"source": "本地Mac", "item": f"进程·{desc}", "value": "未运行",
                                  "level": "warning", "detail": f"进程 {proc_name} 未检测到"})

            # 统计总龍魂进程数
            total = sum(1 for line in r.stdout.split("\n") if "longhun" in line.lower() and "grep" not in line)
            if total == 0:
                alerts.append({"source": "本地Mac", "item": "龍魂进程总数", "value": "0",
                              "level": "critical", "detail": "所有龍魂进程均已停止"})
        except Exception as e:
            log(f"进程检查异常: {e}", "ERROR")
        return alerts

    def check_login_attempts(self) -> List[Dict]:
        """检查异常登录"""
        alerts = []
        try:
            if IS_MAC:
                r = subprocess.run(["last"], capture_output=True, text=True, timeout=10)
                lines = [l for l in r.stdout.split("\n") if l.strip() and "reboot" not in l.lower()
                         and "shutdown" not in l.lower() and "console" not in l.lower()]
                # 检查最近10条中的异常
                recent = lines[:10]
                failed_count = sum(1 for l in recent if "still logged in" not in l and "logged in" not in l)
                if failed_count > 3:
                    alerts.append({"source": "本地Mac", "item": "登录", "value": f"{failed_count}次异常",
                                  "level": "warning"})
        except Exception:
            pass
        return alerts

    def check_all(self) -> List[Dict]:
        """检查所有本地监控项"""
        all_alerts = []
        all_alerts.extend(self.check_cpu())
        all_alerts.extend(self.check_memory())
        all_alerts.extend(self.check_disk())
        all_alerts.extend(self.check_longhun_processes())
        all_alerts.extend(self.check_login_attempts())
        return all_alerts


# ═══════════════════════════════════════════════════════════
# 2. 文件系统变更监听
# ═══════════════════════════════════════════════════════════

class FileChangeWatcher:
    """文件系统变更监听器 - 监控关键目录"""

    WATCH_DIRS = [
        Path.home() / "longhun-system" / "bin",
        Path.home() / "longhun-system" / "personas",
        Path.home() / "longhun-system" / "skills",
        Path.home() / "longhun-system" / "engine",
        Path.home() / "longhun-system" / "L7_数据层",
        Path.home() / "longhun-system" / "L8_治理层",
        Path.home() / ".longhun",
    ]

    WATCH_EXTENSIONS = {".py", ".sh", ".json", ".yaml", ".yml", ".toml", ".md", ".skill"}

    def load_snapshot(self) -> Dict[str, float]:
        """加载上次文件快照 (路径 → 修改时间戳)"""
        try:
            if WATCH_SNAPSHOT.exists():
                return json.loads(WATCH_SNAPSHOT.read_text())
        except Exception:
            pass
        return {}

    def save_snapshot(self, snapshot: Dict[str, float]):
        try:
            WATCH_SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False))
        except Exception:
            pass

    def scan_changes(self) -> List[Dict]:
        """扫描变更，返回变更列表"""
        old_snapshot = self.load_snapshot()
        new_snapshot = {}
        changes = []

        for watch_dir in self.WATCH_DIRS:
            if not watch_dir.exists():
                continue
            for fp in watch_dir.rglob("*"):
                if not fp.is_file():
                    continue
                if fp.suffix not in self.WATCH_EXTENSIONS:
                    continue
                try:
                    mtime = fp.stat().st_mtime
                    rel_path = str(fp.relative_to(Path.home()))
                    new_snapshot[rel_path] = mtime

                    old_mtime = old_snapshot.get(rel_path)
                    if old_mtime is None:
                        changes.append({"type": "新建", "path": rel_path, "time": mtime})
                    elif mtime > old_mtime + 1:  # 1秒容差
                        changes.append({"type": "修改", "path": rel_path, "time": mtime})
                except (OSError, PermissionError):
                    continue

        # 检测删除
        for old_path in old_snapshot:
            if old_path not in new_snapshot:
                changes.append({"type": "删除", "path": old_path, "time": time.time()})

        self.save_snapshot(new_snapshot)
        return changes

    def check_and_alert(self, dedup: bool = True) -> List[Dict]:
        """检查变更并推送通知"""
        changes = self.scan_changes()
        alerts = []
        if not changes:
            return alerts

        # 分类：新建/修改/删除
        new_files = [c for c in changes if c["type"] == "新建"]
        modified = [c for c in changes if c["type"] == "修改"]
        deleted = [c for c in changes if c["type"] == "删除"]

        # 合并推送（避免大量推送轰炸）
        summary_parts = []
        if new_files:
            files_str = "\n".join(f"  + {f['path']}" for f in new_files[:5])
            more = f"\n  ... 等{len(new_files)}个" if len(new_files) > 5 else ""
            summary_parts.append(f"📄 新建 ({len(new_files)}个):\n{files_str}{more}")

        if modified:
            files_str = "\n".join(f"  ~ {f['path']}" for f in modified[:5])
            more = f"\n  ... 等{len(modified)}个" if len(modified) > 5 else ""
            summary_parts.append(f"✏️ 修改 ({len(modified)}个):\n{files_str}{more}")

        if deleted:
            files_str = "\n".join(f"  - {f['path']}" for f in deleted[:5])
            more = f"\n  ... 等{len(deleted)}个" if len(deleted) > 5 else ""
            summary_parts.append(f"🗑 删除 ({len(deleted)}个):\n{files_str}{more}")

        detail = "\n\n".join(summary_parts)

        key = "file_change"
        if not dedup or not is_deduped(key, 5):  # 5分钟去重
            level = "warning" if deleted else "info"
            bark_send_alert("文件系统", f"变更 ({len(changes)}个)", level, detail)
            alerts.append({"source": "文件系统", "item": "变更", "value": len(changes), "level": level})

        return alerts


# ═══════════════════════════════════════════════════════════
# 3. Git 仓库变动监听
# ═══════════════════════════════════════════════════════════

class GitWatcher:
    """Git仓库状态监听器"""

    REPOS = [
        {"path": Path.home() / "longhun-system", "name": "龙魂系统"},
        {"path": Path.home() / "longhun-system" / ".codebuddy", "name": "CodeBuddy配置"},
    ]

    def __init__(self):
        self._last_commits = {}

    def check_repo(self, repo_path: Path, name: str) -> List[Dict]:
        alerts = []
        if not (repo_path / ".git").exists():
            return alerts

        try:
            # 检查未提交变更
            r1 = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, timeout=15, cwd=str(repo_path)
            )
            changed_files = [l.strip() for l in r1.stdout.split("\n") if l.strip()]

            # 检查未推送提交
            r2 = subprocess.run(
                ["git", "log", "--oneline", "@{u}.."],
                capture_output=True, text=True, timeout=15, cwd=str(repo_path)
            )
            unpushed = [l.strip() for l in r2.stdout.split("\n") if l.strip()]

            # 检查最新提交
            r3 = subprocess.run(
                ["git", "log", "-1", "--format=%h %s"],
                capture_output=True, text=True, timeout=15, cwd=str(repo_path)
            )
            latest_commit = r3.stdout.strip()

            key = f"git:{name}"
            last = self._last_commits.get(key)

            if latest_commit != last:
                self._last_commits[key] = latest_commit

                if len(unpushed) > 3:
                    bark_send_alert("Git", name, "warning",
                                    f"⚠️ 有 {len(unpushed)} 个提交未推送\n最新: {latest_commit}")
                    alerts.append({"source": "Git", "item": f"{name}·未推送", "value": len(unpushed), "level": "warning"})

                if len(changed_files) > 10:
                    bark_send_alert("Git", name, "info",
                                    f"📝 {len(changed_files)} 个文件有未提交变更\n最新提交: {latest_commit}")
                    alerts.append({"source": "Git", "item": f"{name}·变更", "value": len(changed_files), "level": "info"})

        except Exception as e:
            log(f"Git检查异常 [{name}]: {e}", "ERROR")
        return alerts

    def check_all(self) -> List[Dict]:
        all_alerts = []
        for repo in self.REPOS:
            if repo["path"].exists():
                all_alerts.extend(self.check_repo(repo["path"], repo["name"]))
        return all_alerts


# ═══════════════════════════════════════════════════════════
# 4. 开源平台监控（GitHub/Gitee）
# ═══════════════════════════════════════════════════════════

class OpenSourceMonitor:
    """开源平台监控器"""

    def __init__(self):
        self.github_token = os.environ.get("GITHUB_TOKEN", "")
        self._last_stars = None
        self._last_forks = None
        self._last_issues = 0

    def check_github(self) -> List[Dict]:
        alerts = []
        if not self.github_token:
            return alerts

        try:
            import urllib.request

            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json",
            }

            # 仓库信息
            req = urllib.request.Request(
                "https://api.github.com/repos/UID9622/longhun-system",
                headers=headers
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
                stars = data.get("stargazers_count", 0)
                forks = data.get("forks_count", 0)

                if self._last_stars is not None and stars != self._last_stars:
                    diff = stars - self._last_stars
                    bark_send_alert("GitHub", "Star", "info" if diff > 0 else "warning",
                                    f"⭐ {stars} ({diff:+d})")
                    alerts.append({"source": "GitHub", "item": "Star变化", "value": f"{diff:+d}", "level": "info"})
                self._last_stars = stars

                if self._last_forks is not None and forks != self._last_forks:
                    diff = forks - self._last_forks
                    bark_send_alert("GitHub", "Fork", "info", f"🍴 {forks} ({diff:+d})")
                    alerts.append({"source": "GitHub", "item": "Fork变化", "value": f"{diff:+d}", "level": "info"})
                self._last_forks = forks

            # Issues - 只通知新增的（首次运行静默初始化）
            req2 = urllib.request.Request(
                "https://api.github.com/repos/UID9622/longhun-system/issues?state=open",
                headers=headers
            )
            with urllib.request.urlopen(req2, timeout=15) as resp:
                issues = json.loads(resp.read().decode())
                current_count = len(issues)
                if self._last_issues > 0 and current_count > self._last_issues:
                    new_issues = issues[:current_count - self._last_issues]
                    for issue in new_issues:
                        title = issue.get("title", "无标题")[:60]
                        bark_send_alert("GitHub", "新Issue", "info", f"🐛 {title}")
                        alerts.append({"source": "GitHub", "item": "新Issue", "value": title, "level": "info"})
                self._last_issues = current_count

        except Exception as e:
            log(f"GitHub检查异常: {e}", "WARNING")
        return alerts

    def check_all(self) -> List[Dict]:
        return self.check_github()


# ═══════════════════════════════════════════════════════════
# 5. 龍魂系统动作追踪（人格/模块/技能）
# ═══════════════════════════════════════════════════════════

class SystemActionTracker:
    """追踪所有系统动作 - 人格模块调用/技能触发等"""

    ACTION_LOG = STATE_DIR / "system_actions.jsonl"

    def log_action(self, category: str, name: str, action: str, detail: str = ""):
        """记录系统动作"""
        entry = {
            "ts": now_str(),
            "category": category,
            "name": name,
            "action": action,
            "detail": detail,
        }
        try:
            with open(self.ACTION_LOG, "a") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass

    def detect_persona_activity(self) -> List[Dict]:
        """检测人格模块活跃度"""
        alerts = []
        try:
            # 检查personas目录下最近修改的人格文件
            personas_dir = Path.home() / "longhun-system" / "personas"
            if personas_dir.exists():
                recent_personas = []
                cutoff = time.time() - 3600  # 1小时内
                for f in personas_dir.glob("*.md"):
                    if f.stat().st_mtime > cutoff:
                        recent_personas.append(f.stem)
                if recent_personas:
                    names = ", ".join(recent_personas[:6])
                    more = f" +{len(recent_personas)-6}个" if len(recent_personas) > 6 else ""
                    alerts.append({"source": "人格矩阵", "item": "活跃人格", "value": f"{len(recent_personas)}个",
                                  "level": "info", "detail": f"最近活跃: {names}{more}"})
        except Exception:
            pass
        return alerts

    def detect_skill_activity(self) -> List[Dict]:
        """检测技能模块活跃度"""
        alerts = []
        try:
            skills_dir = Path.home() / "longhun-system" / "skills"
            if skills_dir.exists():
                recent_skills = []
                cutoff = time.time() - 3600
                for d in skills_dir.iterdir():
                    if d.is_dir():
                        for f in d.rglob("*.skill"):
                            if f.stat().st_mtime > cutoff:
                                recent_skills.append(d.name)
                                break
                if recent_skills:
                    names = ", ".join(recent_skills[:6])
                    alerts.append({"source": "技能库", "item": "活跃技能", "value": f"{len(recent_skills)}个",
                                  "level": "info", "detail": f"最近活跃: {names}"})
        except Exception:
            pass
        return alerts

    def check_all(self) -> List[Dict]:
        alerts = []
        alerts.extend(self.detect_persona_activity())
        alerts.extend(self.detect_skill_activity())
        return alerts


# ═══════════════════════════════════════════════════════════
# 6. 統一监控编排器
# ═══════════════════════════════════════════════════════════

class GlobalMonitor:
    """全局监控编排器"""

    def __init__(self):
        self.local = LocalServerMonitor()
        self.watcher = FileChangeWatcher()
        self.git = GitWatcher()
        self.os_mon = OpenSourceMonitor()
        self.tracker = SystemActionTracker()
        self._start_time = time.time()
        self._alert_count = 0
        self._cycle_count = 0

    def run_cycle(self, quiet: bool = False) -> int:
        """执行一轮全监控检查"""
        self._cycle_count += 1
        all_alerts = []

        if not quiet:
            log(f"🔄 第{self._cycle_count}轮监控开始...")

        # 1. 本地服务器
        local_alerts = self.local.check_all()
        all_alerts.extend(local_alerts)

        # 2. 文件变更
        file_alerts = self.watcher.check_and_alert(dedup=True)
        all_alerts.extend(file_alerts)

        # 3. Git仓库
        git_alerts = self.git.check_all()
        all_alerts.extend(git_alerts)

        # 4. GitHub
        gh_alerts = self.os_mon.check_all()
        all_alerts.extend(gh_alerts)

        # 5. 系统动作（每小时汇报一次）
        if self._cycle_count % 60 == 0:  # 如果间隔1秒则60轮=1分钟，如果是60秒则60轮=1小时
            action_alerts = self.tracker.check_all()
            all_alerts.extend(action_alerts)

        # 发送所有告警
        for alert in all_alerts:
            self._alert_count += 1
            source = alert.get("source", "unknown")
            item = alert.get("item", "")
            level = alert.get("level", "warning")
            detail = alert.get("detail", "")
            value = alert.get("value")
            threshold = alert.get("threshold")

            alert_with_dedup(source, item, level, detail, value, threshold)

        if not quiet:
            heart = "🟢" if len(all_alerts) == 0 else f"🟡({len(all_alerts)}条)"
            log(f"  第{self._cycle_count}轮完成 {heart} 累计告警:{self._alert_count}")

        # 心跳（每10轮）
        if self._cycle_count % 10 == 0 and not quiet:
            self._send_heartbeat()

        return len(all_alerts)

    def _send_heartbeat(self):
        """发送心跳 - 证明监控器还活着"""
        uptime_sec = time.time() - self._start_time
        uptime_str = f"{int(uptime_sec // 3600)}h{int((uptime_sec % 3600) // 60)}m"
        try:
            HB = {"ts": now_str(), "cycles": self._cycle_count, "alerts": self._alert_count,
                  "uptime": uptime_str}
            HEARTBEAT_FILE.write_text(json.dumps(HB, ensure_ascii=False))
        except Exception:
            pass

    def run_forever(self, interval: int = 60):
        """持续运行"""
        log(f"🚀 龍魂全局监控引擎启动 | 间隔:{interval}s | DNA:{DNA}")
        bark_send("🟢 龍魂监控已启动", f"间隔:{interval}s\n时间:{now_str()}\n平台:{platform.system()}", 
                  level="success", group="龍魂-监控")

        # 首次运行
        self.local.check_all()  # 静默初始化快照

        while True:
            try:
                self.run_cycle()
            except KeyboardInterrupt:
                log("⚠️ 收到中断信号，正在关闭...")
                bark_send("🛑 龍魂监控已停止", f"共执行{self._cycle_count}轮\n累计告警:{self._alert_count}条",
                         level="warning", group="龍魂-监控")
                break
            except Exception as e:
                log(f"❌ 监控循环异常: {e}", "ERROR")
                traceback.print_exc()
                bark_send_alert("监控器", "异常", "critical", str(e))

            time.sleep(interval)


# ═══════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="龍魂全局监控与实时通报引擎 v1.0")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="单次检查所有源")
    group.add_argument("--daemon", action="store_true", help="后台持续监控")
    group.add_argument("--test", action="store_true", help="测试Bark推送连通性")
    group.add_argument("--status", action="store_true", help="查看监控状态")
    group.add_argument("--filescan", action="store_true", help="查看文件变更")
    
    parser.add_argument("--interval", type=int, default=60, help="监控间隔(秒), 默认60")
    args = parser.parse_args()

    monitor = GlobalMonitor()

    if args.test:
        print("🧪 测试Bark推送连通性...")
        ok = bark_send("🧪 龍魂监控测试", f"时间: {now_str()}\n平台: {platform.system()}\nDNA: {DNA}",
                       level="info", group="龍魂-测试")
        if ok:
            print("✅ Bark推送成功！请检查手机通知")
        else:
            print("❌ Bark推送失败！请检查 BARK_KEY 环境变量和网络连接")
        return

    if args.status:
        print(f"╔══════════════════════════════════════════════╗")
        print(f"║  龍魂全局监控 · 运行状态                       ║")
        print(f"╚══════════════════════════════════════════════╝")
        print(f"  DNA: {DNA}")
        print(f"  平台: {platform.system()} {platform.release()}")
        print(f"  时间: {now_str()}")

        if HEARTBEAT_FILE.exists():
            hb = json.loads(HEARTBEAT_FILE.read_text())
            print(f"  上次心跳: {hb.get('ts', 'N/A')}")
            print(f"  执行轮次: {hb.get('cycles', 0)}")
            print(f"  累计告警: {hb.get('alerts', 0)}")
            print(f"  运行时长: {hb.get('uptime', 'N/A')}")
        else:
            print(f"  状态: 未运行或无心跳记录")

        # 检查日志
        if MONITOR_LOG.exists():
            lines = MONITOR_LOG.read_text().strip().split("\n")
            print(f"  日志: {len(lines)} 行, 最新5条:")
            for line in lines[-5:]:
                print(f"    {line[:100]}")
        return

    if args.filescan:
        print("📄 文件变更扫描...")
        watcher = FileChangeWatcher()
        changes = watcher.scan_changes()
        if changes:
            print(f"发现 {len(changes)} 处变更:")
            for c in changes:
                icon = {"新建": "+", "修改": "~", "删除": "-"}.get(c["type"], "?")
                print(f"  {icon} {c['path']}")
        else:
            print("未发现变更（首次运行或无变更）")
        return

    if args.check:
        count = monitor.run_cycle()
        print(f"\n✅ 单次检查完成，{count}条告警")
        return

    # daemon 模式
    monitor.run_forever(interval=args.interval)


if __name__ == "__main__":
    main()

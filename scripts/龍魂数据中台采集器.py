#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂本地数据中台采集器 v2.0
安全采集本地浏览器、下载、APP、设备、日志等数据，全部留在本机。
支持 dry-run、增量同步、敏感文件排除、DNA 审计。

用法:
  python3 龍魂数据中台采集器.py --dry-run
  python3 龍魂数据中台采集器.py --sync
  python3 龍魂数据中台采集器.py --full

DNA:#龍芯⚡️丙午·甲午·丁丑·丙午·䷨损-LOCAL-DATA-HUB-FILE1-v2.0
"""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Any

HOME = Path.home()
HUB_DIR = HOME / "longhun-system" / "data-hub"
RAW_DIR = HUB_DIR / "raw"
PROCESSED_DIR = HUB_DIR / "processed"
INDEX_DIR = HUB_DIR / "index"
BACKUP_DIR = HUB_DIR / "backup"
LOG_DIR = HOME / "longhun-system" / "logs"
DNA = "#龍芯⚡️丙午·甲午·丁丑·丙午·䷨损-LOCAL-DATA-HUB-v2.0"

# 敏感文件/目录排除清单（永远不动）
EXCLUDED_PATTERNS = {
    "keychain", "login data", "cookies", "web data", "form history",
    "cert9.db", "key4.db", "logins.json", "signons.sqlite",
    "master password", "secret", "token", "credential", "password",
    ".ssh", ".gnupg", ".uid9622", ".cnsh_credentials",
}

# 浏览器数据源（macOS 路径）
BROWSER_SOURCES = {
    "safari": {
        "history": HOME / "Library" / "Safari" / "History.db",
        "bookmarks": HOME / "Library" / "Safari" / "Bookmarks.plist",
    },
    "chrome": {
        "history": HOME / "Library" / "Application Support" / "Google" / "Chrome" / "Default" / "History",
        "bookmarks": HOME / "Library" / "Application Support" / "Google" / "Chrome" / "Default" / "Bookmarks",
    },
    "firefox": {
        "places": HOME / "Library" / "Application Support" / "Firefox" / "Profiles",
    },
}


def log(msg: str) -> None:
    ts = datetime.datetime.now().astimezone().isoformat()
    line = f"[{ts}] {msg}"
    print(line)
    if LOG_DIR.exists():
        (LOG_DIR / "data_hub.log").open("a", encoding="utf-8").write(line + "\n")


def is_excluded(path: Path) -> bool:
    """检查路径是否命中敏感排除规则。"""
    lower = path.name.lower()
    for pat in EXCLUDED_PATTERNS:
        if pat in lower:
            return True
    for part in path.parts:
        if part.lower() in EXCLUDED_PATTERNS:
            return True
    return False


def file_hash(path: Path) -> str:
    """计算文件 SHA-256。"""
    h = hashlib.sha256()
    try:
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        log(f"  ⚠️ 计算哈希失败 {path}: {e}")
        return ""


def sqlite_backup(src: Path, dst: Path) -> bool:
    """使用 sqlite3 在线备份数据库，避免锁冲突。"""
    if not src.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        conn = sqlite3.connect(f"file:{src}?mode=ro", uri=True)
        with sqlite3.connect(str(dst)) as bak:
            conn.backup(bak)
        conn.close()
        return True
    except Exception as e:
        log(f"  ⚠️ sqlite 备份失败 {src}: {e}")
        return False


def safe_copy(src: Path, dst: Path, use_sqlite: bool = False) -> bool:
    """安全拷贝文件，跳过排除项，可选 sqlite 在线备份。"""
    if not src.exists():
        return False
    if is_excluded(src):
        log(f"  ⛔ 敏感文件跳过: {src}")
        return False

    dst.parent.mkdir(parents=True, exist_ok=True)

    if use_sqlite and src.suffix in (".db", ".sqlite"):
        return sqlite_backup(src, dst)

    try:
        shutil.copy2(str(src), str(dst))
        return True
    except Exception as e:
        log(f"  ⚠️ 拷贝失败 {src}: {e}")
        return False


def collect_browser(args) -> list[Any]:
    """采集浏览器数据。"""
    log("📊 模块: 浏览器数据")
    out_dir = RAW_DIR / "browser"
    out_dir.mkdir(parents=True, exist_ok=True)
    collected = []

    # Safari
    safari_history = BROWSER_SOURCES["safari"]["history"]
    if safari_history.exists():
        dst = out_dir / "safari_history.db"
        if args.dry_run:
            log(f"  [模拟] 将备份 Safari History.db -> {dst}")
        else:
            if safe_copy(safari_history, dst, use_sqlite=True):
                log(f"  ✅ Safari 历史已备份: {dst}")
                collected.append({"source": str(safari_history), "dst": str(dst), "type": "safari_history"})
    else:
        log("  Safari History.db 不存在")

    # Chrome
    chrome_history = BROWSER_SOURCES["chrome"]["history"]
    if chrome_history.exists():
        dst = out_dir / "chrome_history.db"
        if args.dry_run:
            log(f"  [模拟] 将备份 Chrome History -> {dst}")
        else:
            if safe_copy(chrome_history, dst, use_sqlite=True):
                log(f"  ✅ Chrome 历史已备份: {dst}")
                collected.append({"source": str(chrome_history), "dst": str(dst), "type": "chrome_history"})
    else:
        log("  Chrome History 不存在")

    # Firefox
    firefox_profiles = BROWSER_SOURCES["firefox"]["places"]
    if firefox_profiles.exists():
        for profile in firefox_profiles.iterdir():
            if profile.is_dir():
                places = profile / "places.sqlite"
                if places.exists():
                    dst = out_dir / f"firefox_places_{profile.name}.sqlite"
                    if args.dry_run:
                        log(f"  [模拟] 将备份 Firefox places -> {dst}")
                    else:
                        if safe_copy(places, dst, use_sqlite=True):
                            log(f"  ✅ Firefox 历史已备份: {dst}")
                            collected.append({"source": str(places), "dst": str(dst), "type": "firefox_places"})
    else:
        log("  Firefox Profiles 不存在")

    return collected


def collect_downloads(args) -> list[Any]:
    """采集下载目录清单与校验和。"""
    log("📥 模块: 下载记录")
    out_dir = RAW_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    downloads = HOME / "Downloads"
    collected = []

    if not downloads.exists():
        log("  Downloads 目录不存在")
        return collected

    manifest_dst = out_dir / "downloads_manifest.jsonl"
    checksum_dst = out_dir / "downloads_checksums.txt"

    if args.dry_run:
        log(f"  [模拟] 将生成下载清单 -> {manifest_dst}")
        log(f"  [模拟] 将生成校验和 -> {checksum_dst}")
        return collected

    count = 0
    with manifest_dst.open("w", encoding="utf-8") as mf, checksum_dst.open("w", encoding="utf-8") as cf:
        for item in downloads.iterdir():
            record = {
                "name": item.name,
                "path": str(item),
                "is_dir": item.is_dir(),
                "size": item.stat().st_size if item.is_file() else None,
                "mtime": datetime.datetime.fromtimestamp(item.stat().st_mtime).isoformat(),
            }
            mf.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
            if item.is_file() and not is_excluded(item):
                h = file_hash(item)
                if h:
                    cf.write(f"{h}  {item}\n")

    log(f"  ✅ 下载清单已生成: {count} 项")
    collected.append({"source": str(downloads), "dst": str(manifest_dst), "type": "downloads_manifest"})
    return collected


def collect_applications(args) -> list[Any]:
    """采集 APP 安装列表。"""
    log("📱 模块: APP 数据")
    out_dir = RAW_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    collected = []

    if args.dry_run:
        log("  [模拟] 将采集 /Applications 与 ~/Applications 列表")
        return collected

    for src_name, dst_name in [("/Applications", "applications_list.txt"), (str(HOME / "Applications"), "user_applications_list.txt")]:
        dst = out_dir / dst_name
        try:
            result = subprocess.run(["ls", src_name], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                dst.write_text(result.stdout, encoding="utf-8")
                log(f"  ✅ APP 列表已生成: {dst}")
                collected.append({"source": src_name, "dst": str(dst), "type": "applications_list"})
        except Exception as e:
            log(f"  ⚠️ 采集 {src_name} 失败: {e}")

    # iOS 设备 APP（需 ideviceinstaller）
    if shutil.which("ideviceinstaller"):
        dst = out_dir / "ios_apps.txt"
        if args.dry_run:
            log(f"  [模拟] 将采集 iOS APP 列表 -> {dst}")
        else:
            try:
                result = subprocess.run(["ideviceinstaller", "-l"], capture_output=True, text=True, timeout=15)
                dst.write_text(result.stdout + result.stderr, encoding="utf-8")
                log(f"  ✅ iOS APP 列表已生成: {dst}")
                collected.append({"source": "ideviceinstaller", "dst": str(dst), "type": "ios_apps"})
            except Exception as e:
                log(f"  ⚠️ 采集 iOS APP 失败: {e}")
    else:
        log("  未安装 ideviceinstaller，跳过 iOS APP 采集")

    return collected


def collect_shopping(args) -> list[Any]:
    """采集购物账单 CSV。"""
    log("🛒 模块: 购物数据")
    out_dir = RAW_DIR / "shopping"
    out_dir.mkdir(parents=True, exist_ok=True)
    collected = []

    if args.dry_run:
        log("  [模拟] 将扫描 ~/Downloads 中的支付宝/微信账单 CSV")
        return collected

    downloads = HOME / "Downloads"
    if not downloads.exists():
        log("  Downloads 不存在")
        return collected

    patterns = ["*支付宝*.csv", "*微信*.csv", "*账单*.csv", "*alipay*.csv", "*wechat*.csv"]
    copied = 0
    for pattern in patterns:
        for src in downloads.glob(pattern):
            if src.is_file() and not is_excluded(src):
                dst = out_dir / src.name
                try:
                    shutil.copy2(str(src), str(dst))
                    copied += 1
                    collected.append({"source": str(src), "dst": str(dst), "type": "shopping_csv"})
                except Exception as e:
                    log(f"  ⚠️ 拷贝购物账单失败 {src}: {e}")

    log(f"  ✅ 购物账单已采集: {copied} 个文件")
    return collected


def collect_system_logs(args) -> list[Any]:
    """采集系统日志（仅元数据，默认不复制大日志）。"""
    log("📋 模块: 系统日志")
    out_dir = RAW_DIR / "logs"
    out_dir.mkdir(parents=True, exist_ok=True)
    collected = []

    if args.dry_run:
        log("  [模拟] 将生成系统日志索引（严格模式不复制日志内容）")
        return collected

    # 用户日志目录索引
    user_logs = HOME / "Library" / "Logs"
    if user_logs.exists():
        index_dst = out_dir / "user_logs_index.jsonl"
        with index_dst.open("w", encoding="utf-8") as f:
            for log_file in user_logs.rglob("*.log"):
                if is_excluded(log_file):
                    continue
                try:
                    stat = log_file.stat()
                    f.write(json.dumps({
                        "path": str(log_file),
                        "size": stat.st_size,
                        "mtime": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    }, ensure_ascii=False) + "\n")
                except Exception:
                    pass
        log(f"  ✅ 用户日志索引已生成: {index_dst}")
        collected.append({"source": str(user_logs), "dst": str(index_dst), "type": "user_logs_index"})

    # 系统日志元数据（不复制内容，避免权限和体积问题）
    system_log = Path("/var/log/system.log")
    if system_log.exists():
        meta_dst = out_dir / "system_log_meta.json"
        try:
            stat = system_log.stat()
            meta_dst.write_text(json.dumps({
                "path": str(system_log),
                "size": stat.st_size,
                "mtime": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            }, ensure_ascii=False), encoding="utf-8")
            log(f"  ✅ 系统日志元数据已生成: {meta_dst}")
            collected.append({"source": str(system_log), "dst": str(meta_dst), "type": "system_log_meta"})
        except Exception as e:
            log(f"  ⚠️ 系统日志元数据失败: {e}")

    return collected


def collect_hardware_info(args) -> list[Any]:
    """采集设备信息。"""
    log("🖥️ 模块: 设备信息")
    out_dir = RAW_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    collected = []

    if args.dry_run:
        log("  [模拟] 将采集 hardware/software 信息")
        return collected

    for datatype, dst_name in [("SPHardwareDataType", "hardware_info.txt"), ("SPSoftwareDataType", "software_info.txt")]:
        dst = out_dir / dst_name
        try:
            result = subprocess.run(["system_profiler", datatype], capture_output=True, text=True, timeout=30)
            dst.write_text(result.stdout, encoding="utf-8")
            log(f"  ✅ {datatype} 已生成: {dst}")
            collected.append({"source": f"system_profiler {datatype}", "dst": str(dst), "type": datatype})
        except Exception as e:
            log(f"  ⚠️ 采集 {datatype} 失败: {e}")

    return collected


def feed_to_longhun(records: list[Any], dry_run: bool) -> None:
    """将采集元数据投喂给龍魂投喂器。"""
    feeder = HOME / "longhun-system" / "scripts" / "龍魂投喂器.py"
    if not feeder.exists():
        log("  ⚠️ 龍魂投喂器.py 不存在，跳过投喂")
        return

    log("🔄 模块: 接入龍魂投喂器")
    for rec in records:
        text = f"数据中台采集: {rec['type']} | {rec['dst']}"
        if dry_run:
            log(f"  [模拟] 将投喂: {text}")
            continue
        try:
            subprocess.run(
                [sys.executable, str(feeder), "--text", text, "--source", rec["type"]],
                capture_output=True, text=True, timeout=10, check=False
            )
        except Exception as e:
            log(f"  ⚠️ 投喂失败 {text}: {e}")


def generate_manifest(records: list[Any], dry_run: bool) -> None:
    """生成数据清单与 DNA 审计。"""
    if dry_run:
        return

    manifest = {
        "dna": DNA,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "generated_at_local": datetime.datetime.now().astimezone().isoformat(),
        "host": os.uname().nodename,
        "record_count": len(records),
        "records": records,
    }
    manifest_path = INDEX_DIR / f"manifest_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"📁 数据清单已生成: {manifest_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="龍魂本地数据中台采集器")
    parser.add_argument("--dry-run", "-n", action="store_true", help="模拟运行，不实际拷贝")
    parser.add_argument("--sync", "-s", action="store_true", help="执行真实采集")
    parser.add_argument("--full", "-f", action="store_true", help="完整模式（包含日志内容复制，谨慎）")
    args = parser.parse_args()

    if not args.dry_run and not args.sync and not args.full:
        args.dry_run = True

    # 创建目录
    for d in (RAW_DIR, PROCESSED_DIR, INDEX_DIR, BACKUP_DIR, LOG_DIR):
        d.mkdir(parents=True, exist_ok=True)

    log("🐉 龍魂本地数据中台采集启动")
    log(f"🧬 DNA: {DNA}")
    log(f"🔒 模式: {'模拟运行' if args.dry_run else '真实采集'}")
    log("")

    records = []
    records.extend(collect_browser(args))
    records.extend(collect_downloads(args))
    records.extend(collect_applications(args))
    records.extend(collect_shopping(args))
    records.extend(collect_system_logs(args))
    records.extend(collect_hardware_info(args))

    generate_manifest(records, args.dry_run)
    feed_to_longhun(records, args.dry_run)

    log("")
    log(f"✅ 采集完成，共 {len(records)} 条记录")
    log(f"📁 数据目录: {HUB_DIR}")
    if not args.dry_run:
        try:
            total = subprocess.run(["du", "-sh", str(HUB_DIR)], capture_output=True, text=True, timeout=10)
            log(f"💾 数据总量: {total.stdout.split()[0]}")
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())

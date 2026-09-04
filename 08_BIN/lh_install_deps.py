#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·智能依赖管理器 v2.0
自动检测·安装·验证·锁定·同步所有依赖，支持鲲鹏aarch64

DNA: #龍芯⚡️丙午·丙申·戊申·申时·䷗复-INSTALLER-v2.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

特性:
  - 架构自动检测 (x86_64/aarch64)
  - 轻载模式 (仅核心依赖)
  - 快照管理 (安装前自动快照·失败回滚)
  - 自动重试+镜像降级 (Aliyun→Tsinghua→PyPI)
  - 三色审计 (🟢通过/🟡缺失非核心/🔴缺失核心)
  - 鲲鹏自动同步 (SCP+SSH远程安装)
  - JSONL审计日志

用法:
  python3 bin/lh_install_deps.py --check            # 检查依赖状态（三色审计）
  python3 bin/lh_install_deps.py --install           # 安装所有依赖
  python3 bin/lh_install_deps.py --fix               # 修复缺失依赖
  python3 bin/lh_install_deps.py --freeze            # 生成精确锁定文件
  python3 bin/lh_install_deps.py --sync-kunpeng      # 同步到鲲鹏并自动安装
  python3 bin/lh_install_deps.py --rollback          # 回滚到上一快照
  python3 bin/lh_install_deps.py --light             # 轻载模式（仅核心依赖）
  python3 bin/lh_install_deps.py --clean             # 清理pip缓存
"""

import os
import sys
import subprocess
import json
import hashlib
import platform
import shutil
import importlib
import importlib.metadata
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import argparse
import logging

# ============================================================
# 焊死锚点
# ============================================================

ROOT_DIR = Path(__file__).parent.parent.resolve()
DNA_BASE = "#龍芯⚡️丙午·丙申·戊申·申时·䷗复-INSTALLER-v2.0-UID9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

REQUIREMENTS_FILE = ROOT_DIR / "requirements.txt"
LOCK_FILE = ROOT_DIR / "requirements.lock.txt"
SNAPSHOT_DIR = ROOT_DIR / "data" / "snapshots"
LOG_DIR = ROOT_DIR / "logs"
AUDIT_LOG = LOG_DIR / "install_audit.jsonl"

ARCH = platform.machine()  # x86_64 / aarch64
IS_KUNPENG = ARCH == "aarch64"

# 轻载模式核心依赖（算力不足时只装这些）
LIGHT_MODE_CORE = [
    "requests", "pyyaml", "python-dotenv", "tqdm", "jsonlines",
    "fastapi", "uvicorn", "pydantic", "cryptography"
]

# 鲲鹏排除项（需手动编译或特殊处理）
KUNPENG_EXCLUDE = ["opencv-python", "easyocr", "torch", "torchvision"]

# 镜像源优先级
PIP_MIRRORS = [
    "https://mirrors.aliyun.com/pypi/simple/",
    "https://pypi.tuna.tsinghua.edu.cn/simple/",
    "https://pypi.org/simple/",
]

# ============================================================
# 日志与审计
# ============================================================

SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"install_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("lh_installer")


def audit_log(entry: Dict) -> None:
    """写入审计日志（JSONL格式·append-only）"""
    entry.setdefault("timestamp", datetime.now().isoformat())
    entry.setdefault("arch", ARCH)
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def generate_dna(action: str) -> str:
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    h = hashlib.sha256(f"{action}{ts}{ARCH}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-INSTALLER-{ARCH}-UID9622-{h}"


# ============================================================
# 快照管理
# ============================================================

class SnapshotManager:
    """依赖快照管理·安装前自动快照·失败回滚"""

    def create(self) -> str:
        """创建当前环境快照"""
        result = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"pip freeze 失败: {result.stderr}")

        snap_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        snap_path = SNAPSHOT_DIR / f"snapshot_{snap_id}.txt"
        with open(snap_path, "w") as f:
            f.write(result.stdout)

        logger.info(f"[SNAPSHOT] 已创建: {snap_path}")
        return str(snap_path)

    def rollback(self) -> bool:
        """回滚到最近快照"""
        snaps = sorted(SNAPSHOT_DIR.glob("snapshot_*.txt"), reverse=True)
        if not snaps:
            logger.error("[ROLLBACK] 无可用快照")
            return False

        latest = snaps[0]
        logger.info(f"[ROLLBACK] 回滚到: {latest}")

        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(latest), "--force-reinstall"],
            capture_output=True, text=True, timeout=300
        )

        audit_log({
            "action": "rollback",
            "snapshot": str(latest),
            "success": result.returncode == 0,
            "dna": generate_dna("rollback")
        })
        return result.returncode == 0

    def cleanup(self, keep: int = 5) -> int:
        """清理旧快照，只保留最近N个"""
        snaps = sorted(SNAPSHOT_DIR.glob("snapshot_*.txt"))
        removed = 0
        for s in snaps[:-keep]:
            s.unlink()
            removed += 1
        if removed:
            logger.info(f"[SNAPSHOT] 清理了 {removed} 个旧快照")
        return removed


# ============================================================
# 依赖检查器
# ============================================================

@dataclass
class DepStatus:
    name: str
    required: str = ""
    current: str = ""
    installed: bool = False
    importable: bool = False
    tri_color: str = "🟡"


class DependencyChecker:
    """依赖检查器·含三色判定"""

    IMPORT_MAP = {
        "opencv-python": "cv2",
        "pyyaml": "yaml",
        "pillow": "PIL",
        "python-dotenv": "dotenv",
        "python-gnupg": "gnupg",
        "jsonlines": "jsonlines",
        "beautifulsoup4": "bs4",
        "python-multipart": "multipart",
        "flask-cors": "flask_cors",
        "apscheduler": "apscheduler",
    }

    @staticmethod
    def get_installed() -> Dict[str, str]:
        try:
            return {dist.metadata["Name"].lower(): dist.version
                    for dist in importlib.metadata.distributions()}
        except Exception as e:
            logger.warning(f"获取已安装包失败: {e}")
            return {}

    def check_import(self, pkg_name: str) -> bool:
        import_name = self.IMPORT_MAP.get(pkg_name, pkg_name.replace("-", "_"))
        try:
            importlib.import_module(import_name)
            return True
        except ImportError:
            return False

    @staticmethod
    def parse_requirements(filepath: Path) -> List[Dict[str, str]]:
        if not filepath.exists():
            return []
        deps = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("--"):
                    continue
                # Skip optional markers
                if ";" in line:
                    line = line.split(";")[0].strip()
                for op in [">=", "==", "<=", "~=", ">", "<", "!="]:
                    if op in line:
                        name, version = line.split(op, 1)
                        deps.append({"name": name.strip(), "version": version.strip(), "op": op})
                        break
                else:
                    deps.append({"name": line.strip(), "version": "latest", "op": ""})
        return deps

    def check_all(self, light_mode: bool = False) -> Dict:
        deps = self.parse_requirements(REQUIREMENTS_FILE)
        installed = self.get_installed()
        results: List[DepStatus] = []
        missing: List[str] = []
        critical_missing: List[str] = []

        for dep in deps:
            name = dep["name"]

            if light_mode and name not in LIGHT_MODE_CORE:
                continue
            if IS_KUNPENG and name in KUNPENG_EXCLUDE:
                continue

            is_importable = self.check_import(name)
            current_ver = installed.get(name.lower(), "未安装")

            if is_importable:
                color = "🟢"
            elif name in LIGHT_MODE_CORE:
                color = "🔴"
                critical_missing.append(name)
            else:
                color = "🟡"
                missing.append(name)

            results.append(DepStatus(
                name=name,
                required=dep["version"],
                current=current_ver,
                installed=is_importable,
                importable=is_importable,
                tri_color=color
            ))

        green = sum(1 for r in results if r.tri_color == "🟢")
        red = sum(1 for r in results if r.tri_color == "🔴")
        yellow = sum(1 for r in results if r.tri_color == "🟡")

        overall = "🟢" if red == 0 else ("🟡" if yellow > 0 else "🔴")

        output = {
            "total": len(results),
            "green": green, "red": red, "yellow": yellow,
            "results": [asdict(r) for r in results],
            "missing": missing,
            "critical_missing": critical_missing,
            "dna": generate_dna("check"),
            "tri_color": overall,
            "arch": ARCH,
            "light_mode": light_mode,
        }

        audit_log({"action": "check", "tri_color": overall, "red": red, "total": len(results), "dna": output["dna"]})
        return output


# ============================================================
# 依赖安装器
# ============================================================

class DependencyInstaller:
    """安装器·自动重试·镜像降级·快照回滚"""

    def __init__(self, light_mode: bool = False):
        self.light_mode = light_mode
        self.mirror_idx = 0

    @property
    def current_mirror(self) -> Optional[str]:
        if self.mirror_idx < len(PIP_MIRRORS):
            return PIP_MIRRORS[self.mirror_idx]
        return None

    def _build_cmd(self, packages: List[str] = None,
                   from_file: Optional[Path] = None,
                   upgrade: bool = False) -> List[str]:
        cmd = [sys.executable, "-m", "pip", "install"]
        if upgrade:
            cmd.append("--upgrade")
        # macOS Homebrew Python 3.12+ 需要此标志
        try:
            r = subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "--dry-run", "pip"],
                             capture_output=True, timeout=5)
            if r.returncode == 0:
                cmd.append("--break-system-packages")
        except Exception:
            pass
        mirror = self.current_mirror
        if mirror:
            cmd.extend(["-i", mirror])
        if from_file:
            cmd.extend(["-r", str(from_file)])
        elif packages:
            cmd.extend(packages)
        else:
            cmd.extend(["-r", str(REQUIREMENTS_FILE)])
        return cmd

    def install(self, packages: List[str] = None,
                from_file: Optional[Path] = None,
                upgrade: bool = False) -> Tuple[bool, str]:
        cmd = self._build_cmd(packages, from_file, upgrade)
        logger.info(f"[INSTALL] {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            return result.returncode == 0, result.stdout[-2000:] + "\n" + result.stderr[-500:]
        except subprocess.TimeoutExpired:
            return False, "安装超时"

    def install_auto_retry(self, packages: List[str] = None,
                           from_file: Optional[Path] = None,
                           max_retries: int = 3) -> bool:
        snapshot_mgr = SnapshotManager()
        snapshot = snapshot_mgr.create()

        last_error = ""
        for attempt in range(1, max_retries + 1):
            logger.info(f"[INSTALL] 尝试 {attempt}/{max_retries} (镜像: {self.current_mirror or '默认'})...")
            ok, msg = self.install(packages, from_file, upgrade=(attempt > 1))

            if ok:
                audit_log({"action": "install_success", "attempt": attempt, "snapshot": snapshot, "dna": generate_dna("install")})
                snapshot_mgr.cleanup(keep=5)
                return True

            last_error = msg
            self.mirror_idx += 1
            if self.mirror_idx >= len(PIP_MIRRORS):
                break

        # 打印 pip 输出帮助排查
        logger.error("[INSTALL] 全部镜像源失败，pip 最后错误输出:\n%s", last_error[-2000:])
        logger.error("[INSTALL] 正在回滚...")
        snapshot_mgr.rollback()
        audit_log({"action": "install_failed_rollback", "attempts": max_retries, "snapshot": snapshot, "dna": generate_dna("rollback")})
        return False

    def freeze(self) -> Path:
        result = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"pip freeze 失败: {result.stderr}")

        with open(LOCK_FILE, "w") as f:
            f.write(f"# 由 lh_install_deps.py --freeze 自动生成\n")
            f.write(f"# 时间戳: {datetime.now().isoformat()}\n")
            f.write(f"# DNA: {generate_dna('freeze')}\n")
            f.write(f"# 架构: {ARCH}\n")
            f.write(f"# Python: {platform.python_version()}\n\n")
            f.write(result.stdout)

        logger.info(f"[FREEZE] 锁定文件已生成: {LOCK_FILE}")
        return LOCK_FILE


# ============================================================
# 鲲鹏同步器
# ============================================================

class KunpengSync:
    """鲲鹏服务器自动同步与部署"""

    DEFAULT_HOST = os.environ.get("KUNPENG_HOST", "")
    DEFAULT_KEY = os.environ.get("KUNPENG_KEY", os.path.expanduser("~/.ssh/longhun_kunpeng_ed25519"))
    KUNPENG_MIRROR = os.environ.get("KUNPENG_PIP_INDEX", "https://mirrors.aliyun.com/pypi/simple/")

    @staticmethod
    def check() -> Tuple[bool, str]:
        """返回 (可用, 原因)"""
        if not KunpengSync.DEFAULT_HOST:
            return False, "未设置 KUNPENG_HOST 环境变量（在 Mac 上执行此操作：export KUNPENG_HOST=119.13.90.27）"
        if shutil.which("ssh") is None:
            return False, "本地未安装 ssh 命令"
        return True, "ready"

    @staticmethod
    def sync_and_install(lock_file: Path = None) -> bool:
        ok, reason = KunpengSync.check()
        if not ok:
            logger.error(f"[KUNPENG] {reason}")
            return False

        host = KunpengSync.DEFAULT_HOST
        key = KunpengSync.DEFAULT_KEY
        remote_path = "/tmp/requirements.lock.txt"
        source = lock_file or LOCK_FILE

        # 1. SCP
        scp_cmd = ["scp", "-i", key, "-o", "StrictHostKeyChecking=no",
                    str(source), f"root@{host}:{remote_path}"]
        logger.info(f"[KUNPENG] {' '.join(scp_cmd)}")
        r = subprocess.run(scp_cmd, capture_output=True, text=True)
        if r.returncode != 0:
            logger.error(f"[KUNPENG] SCP失败: {r.stderr}")
            return False

        # 2. SSH 安装
        install_script = (
            f'echo "[KUNPENG] 龍魂依赖安装开始"; '
            f'python3 -m pip install -r {remote_path} -i {KunpengSync.KUNPENG_MIRROR} --user; '
            f'echo "[KUNPENG] 安装完成"'
        )
        ssh_cmd = ["ssh", "-i", key, "-o", "StrictHostKeyChecking=no",
                    f"root@{host}", install_script]
        logger.info(f"[KUNPENG] 执行安装...")
        r = subprocess.run(ssh_cmd, capture_output=True, text=True)

        audit_log({
            "action": "kunpeng_sync",
            "host": host,
            "success": r.returncode == 0,
            "output": r.stdout[-500:],
            "dna": generate_dna("kunpeng")
        })

        return r.returncode == 0


# ============================================================
# 展示
# ============================================================

def print_report(status: Dict) -> None:
    """输出三色审计报告"""
    print(f"\n  🐉 龍魂依赖审计报告")
    print(f"  {'=' * 50}")
    print(f"  DNA: {status.get('dna', 'N/A')}")
    print(f"  架构: {status.get('arch', ARCH)}")
    print(f"  轻载模式: {'是' if status.get('light_mode') else '否'}")
    print(f"  总计: {status['total']} 个包")
    print(f"  🟢 正常: {status['green']}")
    print(f"  🟡 缺失(非核心): {status['yellow']}")
    print(f"  🔴 缺失(核心): {len(status['critical_missing'])}")
    print(f"  综合判定: {status['tri_color']}")

    if status.get("results"):
        print(f"\n  📋 详情:")
        for r in status["results"]:
            print(f"    {r['tri_color']} {r['name']:<20} 需要: {r['required']:<12} → 当前: {r['current']}")

    if status["critical_missing"]:
        print(f"\n  🔴 核心缺失: {', '.join(status['critical_missing'])}")
    print()


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·智能依赖管理器 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh --deps --check              # 检查依赖状态（三色审计）
  lh --deps --install            # 安装所有依赖
  lh --deps --fix                # 修复缺失依赖
  lh --deps --freeze             # 生成精确锁定文件
  lh --deps --sync-kunpeng       # 同步到鲲鹏并自动安装
  lh --deps --rollback           # 回滚到上一快照
  lh --deps --light --install    # 轻载模式安装
""")
    parser.add_argument("--install", "-i", action="store_true", help="安装所有依赖")
    parser.add_argument("--check", "-c", action="store_true", help="检查依赖状态（三色审计）")
    parser.add_argument("--fix", "-f", action="store_true", help="修复缺失依赖")
    parser.add_argument("--freeze", action="store_true", help="生成精确锁定文件")
    parser.add_argument("--sync-kunpeng", action="store_true", help="同步到鲲鹏并自动安装")
    parser.add_argument("--rollback", action="store_true", help="回滚到上一快照")
    parser.add_argument("--light", "-l", action="store_true", help="轻载模式（仅核心依赖）")
    parser.add_argument("--clean", action="store_true", help="清理pip缓存")
    parser.add_argument("--json", action="store_true", help="JSON格式输出（管道友好）")

    args = parser.parse_args()
    checker = DependencyChecker()

    # --check
    if args.check:
        status = checker.check_all(light_mode=args.light)
        if args.json:
            print(json.dumps(status, ensure_ascii=False, indent=2))
        else:
            print_report(status)
        sys.exit(0 if status["tri_color"] == "🟢" else 1)

    # --install
    if args.install:
        installer = DependencyInstaller(light_mode=args.light)
        ok = installer.install_auto_retry(from_file=REQUIREMENTS_FILE)
        if ok:
            print("✅ 安装完成")
        else:
            print("🔴 安装失败，已自动回滚")
        sys.exit(0 if ok else 1)

    # --fix
    if args.fix:
        status = checker.check_all(light_mode=args.light)
        missing = status["missing"] + status["critical_missing"]
        if not missing:
            print("✅ 所有依赖已安装")
            sys.exit(0)
        print(f"[FIX] 修复 {len(missing)} 个缺失依赖...")
        installer = DependencyInstaller(light_mode=args.light)
        ok = installer.install_auto_retry(packages=missing)
        sys.exit(0 if ok else 1)

    # --freeze
    if args.freeze:
        installer = DependencyInstaller()
        lock = installer.freeze()
        print(f"✅ 锁定文件: {lock}")
        sys.exit(0)

    # --sync-kunpeng
    if args.sync_kunpeng:
        if not LOCK_FILE.exists():
            print("[WARN] 锁定文件不存在，先生成...")
            DependencyInstaller().freeze()
        ok = KunpengSync.sync_and_install(LOCK_FILE)
        print("✅ 鲲鹏同步完成" if ok else "🔴 鲲鹏同步失败")
        sys.exit(0 if ok else 1)

    # --rollback
    if args.rollback:
        ok = SnapshotManager().rollback()
        print("✅ 回滚完成" if ok else "🔴 回滚失败")
        sys.exit(0 if ok else 1)

    # --clean
    if args.clean:
        subprocess.run([sys.executable, "-m", "pip", "cache", "purge"])
        SnapshotManager().cleanup(keep=3)
        print("✅ 缓存已清理")
        sys.exit(0)

    parser.print_help()


if __name__ == "__main__":
    main()

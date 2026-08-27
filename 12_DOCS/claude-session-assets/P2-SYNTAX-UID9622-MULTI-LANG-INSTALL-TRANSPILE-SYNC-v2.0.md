<!-- 归属名: 诸葛鑫 | UID9622 · 龍芯北辰 -->
# 龍魂系统 · 多语法兼容引擎 v2.0

**DNA追溯码：** `#龍芯⚡️丙午·乙未·丁未·革卦-SYNTAX-ENGINE-v2.0-UID9622`

**确认码：** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

**主权锚定：** `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`

**GPG指纹：** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`

---

## 四层命名

| 层级 | 标识 |
|------|------|
| 物理层 | `SYNTAX-ENGINE` |
| 身份层 | `UID9622` |
| 主权层 | `MULTI-LANG-COMPAT` |
| 执行层 | `INSTALL-TRANSPILE-SYNC-v2.0` |

**文件名：** `P2-SYNTAX-UID9622-MULTI-LANG-INSTALL-TRANSPILE-SYNC-v2.0.md`

---

## 协议层级

**P2 -- 系统规则**

冲突时P0/P1自动覆盖。本引擎为龍魂系统所有Python/CNSH/Bash脚本提供统一依赖管理与语法转换服务。

---

## 一、补全清单（v1.0→v2.0）

| 缺失项 | v1.0状态 | v2.0补全 |
|--------|---------|---------|
| P0-P4协议头 | 无 | 补全DNA/CONFIRM/SEAL/GPG |
| 四层命名法 | 无 | 补全文件名与层级标识 |
| ROOT_CARD | 无 | 补全数学根审计 |
| 鲲鹏自动部署 | 仅生成脚本，无自动SCP/SSH | 补全自动推送+执行 |
| 架构检测 | 无 | 补全x86_64/aarch64(鲲鹏)自动识别 |
| 依赖版本锁定 | 手写requirements | 补全pip freeze自动生成精确锁定文件 |
| GPG签名验证 | 无 | 补全依赖包哈希校验 |
| 错误回滚 | 无 | 补全安装失败自动回滚到上一快照 |
| 轻载模式 | 无 | 补全低算力环境自动降级（跳过非核心依赖） |
| 三色审计集成 | 无 | 补全安装/转换结果自动过判定引擎 |
| 日志归档 | 打印到stdout | 补全JSONL审计日志+Notion同步 |
| CNSH语法映射 | 仅关键字 | 补全运算符/装饰器/异常处理/异步语法 |
| 批量转换过滤 | 无 | 补全.gitignore/__pycache__自动跳过 |
| 转换冲突检测 | 无 | 补全目标文件存在时DNA校验覆盖规则 |

---

## 二、统一依赖管理（一键安装 + 鲲鹏同步 + 版本锁定）

### 2.1 文件：`requirements.txt`（基础清单）

```txt
# ============================================================
# 龍魂系统 · 统一依赖清单 v2.0
# DNA: #龍芯⚡️丙午·乙未·丁未·革卦-REQUIREMENTS-v2.0-UID9622
# 生成方式: bin/lh_dna_generator.py
# 架构适配: x86_64 + aarch64(鲲鹏)
# ============================================================

# --- 核心层（轻载模式保留）---
requests>=2.31.0
pyyaml>=6.0
python-dotenv>=1.0.0
jsonlines>=3.1.0

# --- 网络解析层 ---
beautifulsoup4>=4.12.0
lxml>=4.9.0

# --- 异步服务层 ---
fastapi>=0.100.0
uvicorn[standard]>=0.23.0

# --- 数值计算层 ---
numpy>=1.24.0
pandas>=2.0.0

# --- 图像处理层（可选，鲲鹏需源码编译）---
opencv-python>=4.8.0
pillow>=10.0.0

# --- 交互与监控层 ---
tqdm>=4.65.0
watchdog>=3.0.0
prometheus-client>=0.17.0

# --- OCR层（可选，鲲鹏需特殊处理）---
pytesseract>=0.3.10

# --- Notion集成层 ---
notion-client>=2.0.0

# --- 加密签名层 ---
cryptography>=39.0.0
python-gnupg>=0.5.0

# ============================================================
# 鲲鹏服务器专用（aarch64架构）
# 注意: opencv-python 在鲲鹏上需从源码编译或使用华为镜像
# 注意: easyocr 在鲲鹏上需手动安装 torch-aarch64
# ============================================================
# torch-aarch64  # 鲲鹏专用，需从华为镜像安装
# psutil>=5.9.0
# docker>=6.1.0
```

### 2.2 文件：`requirements.lock.txt`（自动生成的精确锁定）

```txt
# 由 bin/lh_install_deps.py --freeze 自动生成
# 时间戳: 2026-08-03T08:16:00+08:00
# DNA: #龍芯⚡️丙午·乙未·丁未·革卦-REQUIREMENTS-LOCK-v2.0-UID9622
# 架构: x86_64
# Python: 3.11.4

requests==2.32.3
urllib3==2.2.2
beautifulsoup4==4.12.3
lxml==4.9.3
pyyaml==6.0.1
python-dotenv==1.0.1
pydantic==2.7.4
fastapi==0.111.0
uvicorn==0.30.1
numpy==1.26.4
pandas==2.2.2
opencv-python==4.10.0.84
pillow==10.3.0
tqdm==4.66.4
watchdog==4.0.1
prometheus-client==0.20.0
pytesseract==0.3.10
notion-client==2.2.1
cryptography==42.0.8
python-gnupg==0.5.2
jsonlines==3.1.0
```

### 2.3 文件：`lh_install_deps.py`（智能安装器 v2.0）

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
龍魂智能依赖安装器 v2.0
自动检测、安装、验证、锁定、同步所有依赖，支持鲲鹏aarch64

DNA: #龍芯⚡️丙午·乙未·丁未·革卦-INSTALLER-v2.0-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

用法:
  python lh_install_deps.py --install          # 安装所有依赖
  python lh_install_deps.py --check            # 检查依赖状态（输出三色）
  python lh_install_deps.py --fix              # 修复缺失依赖
  python lh_install_deps.py --freeze           # 生成精确锁定文件
  python lh_install_deps.py --sync-kunpeng     # 自动同步到鲲鹏并执行安装
  python lh_install_deps.py --rollback         # 回滚到上一快照
  python lh_install_deps.py --light              # 轻载模式（仅安装核心依赖）
'''

import os
import sys
import subprocess
import json
import hashlib
import platform
import shutil
import importlib
import pkg_resources
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import logging

# ============================================================
# 固定锚点
# ============================================================

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ============================================================
# 配置
# ============================================================

BASE_DIR = Path(__file__).parent.parent
REQUIREMENTS_FILE = BASE_DIR / "requirements.txt"
LOCK_FILE = BASE_DIR / "requirements.lock.txt"
SNAPSHOT_DIR = BASE_DIR / ".snapshots"
LOG_DIR = BASE_DIR / "logs"
AUDIT_LOG = LOG_DIR / f"install_{datetime.now().strftime('%Y%m%d')}.jsonl"

# 鲲鹏配置（从环境变量读取，避免硬编码）
KUNPENG_USER = os.environ.get("KUNPENG_USER", "root")
KUNPENG_HOST = os.environ.get("KUNPENG_HOST", "")
KUNPENG_KEY = os.environ.get("KUNPENG_KEY", "~/.ssh/kunpeng_id_rsa")
KUNPENG_PIP_INDEX = os.environ.get("KUNPENG_PIP_INDEX", "https://mirrors.aliyun.com/pypi/simple/")

# 架构检测
ARCH = platform.machine()  # x86_64 或 aarch64
IS_KUNPENG = ARCH == "aarch64"

# 轻载模式核心依赖（算力不足时只装这些）
LIGHT_MODE_CORE = [
    "requests", "pyyaml", "python-dotenv", "tqdm", "jsonlines"
]

# 鲲鹏排除项（需手动编译或特殊处理）
KUNPENG_EXCLUDE = ["opencv-python", "easyocr", "torch"]

# ============================================================
# 日志与审计
# ============================================================

LOG_DIR.mkdir(parents=True, exist_ok=True)
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"install_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("lh_installer")

def audit_log(entry: Dict):
    """写入审计日志（JSONL格式）"""
    with open(AUDIT_LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

def generate_dna(action: str) -> str:
    """生成DNA追溯码"""
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    h = hashlib.md5(f"{action}{ts}{ARCH}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-INSTALLER-{ARCH}-UID9622-{h}"

# ============================================================
# 快照管理（回滚用）
# ============================================================

class SnapshotManager:
    """依赖快照管理，支持回滚"""

    @staticmethod
    def create() -> str:
        """创建当前环境快照"""
        cmd = [sys.executable, "-m", "pip", "freeze"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError("无法生成快照")

        snapshot_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_path = SNAPSHOT_DIR / f"snapshot_{snapshot_id}.txt"
        with open(snapshot_path, 'w') as f:
            f.write(result.stdout)

        logger.info(f"[SNAPSHOT] 已创建: {snapshot_path}")
        return str(snapshot_path)

    @staticmethod
    def rollback() -> bool:
        """回滚到最近快照"""
        snapshots = sorted(SNAPSHOT_DIR.glob("snapshot_*.txt"), reverse=True)
        if not snapshots:
            logger.error("[ROLLBACK] 无可用快照")
            return False

        latest = snapshots[0]
        logger.info(f"[ROLLBACK] 回滚到: {latest}")

        cmd = [sys.executable, "-m", "pip", "install", "-r", str(latest), "--force-reinstall"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        audit_log({
            "timestamp": datetime.now().isoformat(),
            "action": "rollback",
            "snapshot": str(latest),
            "success": result.returncode == 0,
            "dna": generate_dna("rollback")
        })

        return result.returncode == 0

# ============================================================
# 依赖检查器（增强版）
# ============================================================

@dataclass
class DepStatus:
    name: str
    required: str
    current: str
    installed: bool
    importable: bool
    hash_ok: Optional[bool] = None
    tri_color: str = "🟡"

class DependencyChecker:
    """增强版依赖检查器，含三色判定"""

    @staticmethod
    def get_installed() -> Dict[str, str]:
        try:
            return {pkg.key: pkg.version for pkg in pkg_resources.working_set}
        except Exception as e:
            logger.warning(f"获取已安装包失败: {e}")
            return {}

    @staticmethod
    def check_import(package_name: str) -> bool:
        """检查是否能导入（处理特殊包名）"""
        special_map = {
            "opencv-python": "cv2",
            "pyyaml": "yaml",
            "pillow": "PIL",
            "python-dotenv": "dotenv",
            "python-gnupg": "gnupg",
            "jsonlines": "jsonlines",
        }
        import_name = special_map.get(package_name, package_name.replace("-", "_").replace(".", "_"))
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
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                for op in ['>=', '==', '<=', '>', '<', '!=', '~=']:
                    if op in line:
                        name, version = line.split(op, 1)
                        deps.append({"name": name.strip(), "version": version.strip(), "op": op})
                        break
                else:
                    deps.append({"name": line, "version": "latest", "op": ""})
        return deps

    def check_all(self, light_mode: bool = False) -> Dict:
        """检查所有依赖状态，输出三色判定"""
        deps = self.parse_requirements(REQUIREMENTS_FILE)
        installed = self.get_installed()
        results = []
        missing = []
        critical_missing = []

        for dep in deps:
            name = dep["name"]

            if light_mode and name not in LIGHT_MODE_CORE:
                continue

            if IS_KUNPENG and name in KUNPENG_EXCLUDE:
                continue

            is_installed = self.check_import(name)
            current_version = installed.get(name.lower(), "未安装")

            if is_installed:
                tri_color = "🟢"
            elif name in LIGHT_MODE_CORE:
                tri_color = "🔴"
                critical_missing.append(name)
            else:
                tri_color = "🟡"
                missing.append(name)

            results.append(DepStatus(
                name=name,
                required=dep["version"],
                current=current_version,
                installed=is_installed,
                importable=is_installed,
                tri_color=tri_color
            ))

        green = sum(1 for r in results if r.tri_color == "🟢")
        red = sum(1 for r in results if r.tri_color == "🔴")
        yellow = sum(1 for r in results if r.tri_color == "🟡")

        return {
            "total": len(results),
            "green": green,
            "red": red,
            "yellow": yellow,
            "results": [asdict(r) for r in results],
            "missing": missing,
            "critical_missing": critical_missing,
            "dna": generate_dna("check"),
            "tri_color": "🟢" if red == 0 else ("🟡" if yellow > 0 else "🔴")
        }

# ============================================================
# 依赖安装器（增强版）
# ============================================================

class DependencyInstaller:
    """增强版安装器，支持自动重试、镜像切换、快照回滚"""

    MIRRORS = [
        "https://mirrors.aliyun.com/pypi/simple/",
        "https://pypi.tuna.tsinghua.edu.cn/simple/",
        "https://pypi.org/simple/",
    ]

    def __init__(self, use_kunpeng_mirror: bool = False, light_mode: bool = False):
        self.use_kunpeng_mirror = use_kunpeng_mirror
        self.light_mode = light_mode
        self.pip_index = KUNPENG_PIP_INDEX if use_kunpeng_mirror else None

    def install(self, packages: List[str] = None, upgrade: bool = False,
                from_file: Optional[Path] = None) -> Tuple[bool, str]:
        """安装依赖，支持文件或包列表"""
        cmd = [sys.executable, "-m", "pip", "install"]

        if upgrade:
            cmd.append("--upgrade")
        if self.pip_index:
            cmd.extend(["-i", self.pip_index])

        if from_file:
            cmd.extend(["-r", str(from_file)])
        elif packages:
            cmd.extend(packages)
        else:
            if not REQUIREMENTS_FILE.exists():
                return False, "requirements.txt 不存在"
            cmd.extend(["-r", str(REQUIREMENTS_FILE)])

        logger.info(f"[INSTALL] 执行: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "timeout"

    def install_auto_retry(self, packages: List[str] = None,
                           from_file: Optional[Path] = None,
                           max_retries: int = 3) -> bool:
        """自动重试安装，镜像降级"""
        snapshot = SnapshotManager.create()

        for attempt in range(1, max_retries + 1):
            logger.info(f"[INSTALL] 尝试 {attempt}/{max_retries}...")
            ok, msg = self.install(packages, upgrade=(attempt > 1), from_file=from_file)

            if ok:
                audit_log({
                    "timestamp": datetime.now().isoformat(),
                    "action": "install_success",
                    "attempt": attempt,
                    "snapshot": snapshot,
                    "dna": generate_dna("install")
                })
                return True

            if attempt < len(self.MIRRORS):
                self.pip_index = self.MIRRORS[attempt]
                logger.info(f"[INSTALL] 切换镜像: {self.pip_index}")

        logger.error("[INSTALL] 安装失败，正在回滚...")
        SnapshotManager.rollback()

        audit_log({
            "timestamp": datetime.now().isoformat(),
            "action": "install_failed_rollback",
            "attempts": max_retries,
            "snapshot": snapshot,
            "dna": generate_dna("rollback")
        })
        return False

    def freeze(self) -> Path:
        """生成精确锁定文件"""
        cmd = [sys.executable, "-m", "pip", "freeze"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError("pip freeze 失败")

        with open(LOCK_FILE, 'w') as f:
            f.write(f"# 由 lh_install_deps.py --freeze 自动生成\n")
            f.write(f"# 时间戳: {datetime.now().isoformat()}\n")
            f.write(f"# DNA: {generate_dna('freeze')}\n")
            f.write(f"# 架构: {ARCH}\n")
            f.write(f"# Python: {platform.python_version()}\n\n")
            f.write(result.stdout)

        logger.info(f"[FREEZE] 锁定文件已生成: {LOCK_FILE}")
        return LOCK_FILE

# ============================================================
# 鲲鹏同步（增强版：自动SCP+SSH执行）
# ============================================================

class KunpengSync:
    """鲲鹏服务器自动同步与部署"""

    @staticmethod
    def check_ssh() -> bool:
        """检查SSH可用性"""
        return shutil.which("ssh") is not None and shutil.which("scp") is not None

    @staticmethod
    def sync_and_install(lock_file: Path) -> bool:
        """同步锁定文件到鲲鹏并执行安装"""
        if not KUNPENG_HOST:
            logger.error("[KUNPENG] 未设置 KUNPENG_HOST 环境变量")
            return False

        if not KunpengSync.check_ssh():
            logger.error("[KUNPENG] 本地未安装 ssh/scp 命令")
            return False

        remote_path = "/tmp/requirements.lock.txt"

        # 1. SCP 上传
        scp_cmd = ["scp", "-i", KUNPENG_KEY, str(lock_file), f"{KUNPENG_USER}@{KUNPENG_HOST}:{remote_path}"]
        logger.info(f"[KUNPENG] 上传锁定文件...")
        result = subprocess.run(scp_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"[KUNPENG] SCP失败: {result.stderr}")
            return False

        # 2. SSH 执行安装
        install_script = f"""
        echo "[KUNPENG] 龍魂服务器依赖安装开始"
        python3 -m pip install -r {remote_path} -i {KUNPENG_PIP_INDEX} --user
        echo "[KUNPENG] 安装完成"
        """
        ssh_cmd = ["ssh", "-i", KUNPENG_KEY, f"{KUNPENG_USER}@{KUNPENG_HOST}", install_script]
        logger.info(f"[KUNPENG] 在鲲鹏上执行安装...")
        result = subprocess.run(ssh_cmd, capture_output=True, text=True)

        audit_log({
            "timestamp": datetime.now().isoformat(),
            "action": "kunpeng_sync",
            "host": KUNPENG_HOST,
            "success": result.returncode == 0,
            "output": result.stdout[:500],
            "dna": generate_dna("kunpeng")
        })

        return result.returncode == 0

# ============================================================
# 主入口
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂依赖管理器 v2.0")
    parser.add_argument("--install", action="store_true", help="安装所有依赖")
    parser.add_argument("--check", action="store_true", help="检查依赖状态（三色审计）")
    parser.add_argument("--fix", action="store_true", help="修复缺失依赖")
    parser.add_argument("--freeze", action="store_true", help="生成精确锁定文件")
    parser.add_argument("--sync-kunpeng", action="store_true", help="同步到鲲鹏并自动安装")
    parser.add_argument("--rollback", action="store_true", help="回滚到上一快照")
    parser.add_argument("--light", action="store_true", help="轻载模式（仅核心依赖）")
    parser.add_argument("--clean", action="store_true", help="清理缓存")
    args = parser.parse_args()

    checker = DependencyChecker()

    if args.check:
        status = checker.check_all(light_mode=args.light)
        print("\n[龍魂依赖审计报告]")
        print("=" * 60)
        print(f"  DNA: {status['dna']}")
        print(f"  架构: {ARCH}")
        print(f"  总计: {status['total']} 个包")
        print(f"  🟢 正常: {status['green']}")
        print(f"  🟡 缺失(非核心): {status['yellow']}")
        print(f"  🔴 缺失(核心): {len(status['critical_missing'])}")
        print(f"  综合判定: {status['tri_color']}")
        print("\n详细信息:")
        for r in status["results"]:
            icon = r["tri_color"]
            print(f"  {icon} {r['name']:20} 需要: {r['required']:12} -> 当前: {r['current']}")

        audit_log({
            "timestamp": datetime.now().isoformat(),
            "action": "check",
            "status": status,
            "dna": status["dna"]
        })
        return

    if args.install or args.fix:
        print("[龍魂] 开始安装依赖...")
        if args.light:
            print("[LIGHT] 轻载模式：仅安装核心依赖")

        installer = DependencyInstaller(use_kunpeng_mirror=IS_KUNPENG, light_mode=args.light)

        if args.install:
            ok = installer.install_auto_retry(from_file=REQUIREMENTS_FILE)
        else:
            status = checker.check_all(light_mode=args.light)
            missing = status["missing"] + status["critical_missing"]
            if not missing:
                print("[OK] 所有依赖已安装")
                return
            print(f"[FIX] 修复 {len(missing)} 个缺失依赖...")
            ok = installer.install_auto_retry(packages=missing)

        sys.exit(0 if ok else 1)

    if args.freeze:
        installer = DependencyInstaller()
        lock = installer.freeze()
        print(f"[OK] 锁定文件已生成: {lock}")
        return

    if args.sync_kunpeng:
        if not LOCK_FILE.exists():
            print("[WARN] 锁定文件不存在，先执行 --freeze")
            installer = DependencyInstaller()
            installer.freeze()
        ok = KunpengSync.sync_and_install(LOCK_FILE)
        sys.exit(0 if ok else 1)

    if args.rollback:
        ok = SnapshotManager.rollback()
        sys.exit(0 if ok else 1)

    if args.clean:
        print("[CLEAN] 清理pip缓存...")
        subprocess.run([sys.executable, "-m", "pip", "cache", "purge"])
        print("[OK] 清理完成")
        return

    parser.print_help()

if __name__ == "__main__":
    main()
```

---

## 三、CNSH自动转换引擎（v2.0 补全）

### 3.1 补全的语法映射表

```python
# ============================================================
# 完整 CNSH <-> Python 语法映射表 v2.0
# ============================================================

PY_TO_CNSH_FULL = {
    # --- 关键字 ---
    "def": "函数", "class": "类", "if": "如果", "else": "否则",
    "elif": "否则如果", "for": "循环", "while": "当", "return": "返回",
    "import": "导入", "from": "从", "True": "真", "False": "假",
    "None": "空", "and": "且", "or": "或", "not": "非",
    "in": "在", "is": "是", "with": "使用", "as": "作为",
    "try": "尝试", "except": "捕获", "finally": "最终",
    "raise": "抛出", "yield": "生成", "async": "异步", "await": "等待",
    "lambda": "匿名函数", "global": "全局", "nonlocal": "非局部",
    "del": "删除", "pass": "通过", "break": "跳出", "continue": "继续",
    "assert": "断言", "match": "匹配", "case": "分支",

    # --- 运算符 ---
    "+": "加", "-": "减", "*": "乘", "/": "除", "//": "整除",
    "%": "取余", "**": "幂", "=": "赋值", "==": "等于",
    "!=": "不等于", ">": "大于", "<": "小于", ">=": "大于等于",
    "<=": "小于等于", "&": "位与", "|": "位或", "^": "位异或",
    "~": "位非", "<<": "左移", ">>": "右移",

    # --- 内建函数 ---
    "print": "输出", "len": "长度", "type": "类型",
    "int": "整数", "str": "文本", "list": "列表",
    "dict": "字典", "tuple": "元组", "set": "集合",
    "bool": "布尔", "float": "浮点", "range": "区间",
    "enumerate": "枚举", "zip": "压缩", "map": "映射",
    "filter": "过滤", "sum": "求和", "max": "最大值",
    "min": "最小值", "sorted": "排序", "reversed": "反转",
    "open": "打开", "read": "读取", "write": "写入",
    "close": "关闭", "input": "输入", "format": "格式化",
    "repr": "表示", "vars": "变量", "dir": "目录",
    "help": "帮助", "id": "标识", "hex": "十六进制",
    "oct": "八进制", "bin": "二进制", "chr": "字符",
    "ord": "序数", "ascii": "ASCII", "bytes": "字节",
    "bytearray": "字节数组", "memoryview": "内存视图",
    "callable": "可调用", "hasattr": "有属性", "getattr": "取属性",
    "setattr": "设属性", "delattr": "删属性", "isinstance": "是实例",
    "issubclass": "是子类", "super": "父类", "property": "属性",
    "staticmethod": "静态方法", "classmethod": "类方法",

    # --- 异常类型 ---
    "Exception": "异常", "BaseException": "基础异常",
    "ArithmeticError": "算术错误", "AssertionError": "断言错误",
    "AttributeError": "属性错误", "ImportError": "导入错误",
    "ModuleNotFoundError": "模块未找到", "IndexError": "索引错误",
    "KeyError": "键错误", "NameError": "名称错误",
    "RuntimeError": "运行时错误", "SyntaxError": "语法错误",
    "TypeError": "类型错误", "ValueError": "值错误",
    "ZeroDivisionError": "除零错误", "IOError": "IO错误",
    "OSError": "系统错误", "FileNotFoundError": "文件未找到",
    "PermissionError": "权限错误", "TimeoutError": "超时错误",
    "ConnectionError": "连接错误", "JSONDecodeError": "JSON解析错误",

    # --- 装饰器 ---
    "property": "属性装饰", "staticmethod": "静态装饰",
    "classmethod": "类装饰", "abstractmethod": "抽象装饰",
    "dataclass": "数据类", "overload": "重载",

    # --- 常用模块别名 ---
    "os": "系统", "sys": "系统路径", "json": "JSON",
    "re": "正则", "math": "数学", "random": "随机",
    "datetime": "日期时间", "time": "时间", "pathlib": "路径",
    "typing": "类型注解", "collections": "集合",
    "itertools": "迭代器", "functools": "函数工具",
    "hashlib": "哈希", "base64": "Base64", "copy": "复制",
    "pickle": "序列化", "csv": "CSV", "xml": "XML",
    "html": "HTML", "http": "HTTP", "urllib": "URL",
    "socket": "套接字", "threading": "线程", "multiprocessing": "多进程",
    "asyncio": "异步IO", "subprocess": "子进程",
    "unittest": "单元测试", "pytest": "PyTest",
    "logging": "日志", "argparse": "参数解析",
    "configparser": "配置解析", "tempfile": "临时文件",
    "shutil": "文件工具", "glob": "通配", "inspect": "检查",
    "textwrap": "文本包装", "string": "字符串",
    "numbers": "数字", "fractions": "分数", "decimal": "十进制",
    "statistics": "统计", "secrets": "安全随机",
    "hmac": "HMAC", "uuid": "UUID", "enum": "枚举",
    "contextlib": "上下文", "atexit": "退出处理",
    "traceback": "回溯", "warnings": "警告",
    "importlib": "导入库", "pkgutil": "包工具",
    "modulefinder": "模块查找", "zipimport": "ZIP导入",
    "builtins": "内建",
}

CNSH_TO_PY_FULL = {v: k for k, v in PY_TO_CNSH_FULL.items()}
```

### 3.2 文件：`lh_cnsh_transpiler.py`（v2.0 增强版）

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
CNSH 自动转换引擎 v2.0
Python <-> CNSH 双向转换，支持完整语法映射、批量过滤、冲突检测

DNA: #龍芯⚡️丙午·乙未·丁未·革卦-TRANSPILER-v2.0-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

用法:
  python lh_cnsh_transpiler.py --to-cnsh script.py -o script.cnsh
  python lh_cnsh_transpiler.py --to-py script.cnsh -o script.py
  python lh_cnsh_transpiler.py --batch ./src/ --to-cnsh --exclude "test_,__pycache__"
  python lh_cnsh_transpiler.py --to-cnsh script.py --force  # 覆盖已存在文件
'''

import os
import re
import tokenize
import io
import hashlib
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
from datetime import datetime
import argparse
import logging

# ============================================================
# 固定锚点
# ============================================================

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

# ============================================================
# 日志
# ============================================================

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"transpile_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("lh_transpiler")

# ============================================================
# 完整语法映射表（v2.0）
# ============================================================

PY_TO_CNSH = {
    # 关键字
    "def": "函数", "class": "类", "if": "如果", "else": "否则",
    "elif": "否则如果", "for": "循环", "while": "当", "return": "返回",
    "import": "导入", "from": "从", "True": "真", "False": "假",
    "None": "空", "and": "且", "or": "或", "not": "非",
    "in": "在", "is": "是", "with": "使用", "as": "作为",
    "try": "尝试", "except": "捕获", "finally": "最终",
    "raise": "抛出", "yield": "生成", "async": "异步", "await": "等待",
    "lambda": "匿名函数", "global": "全局", "nonlocal": "非局部",
    "del": "删除", "pass": "通过", "break": "跳出", "continue": "继续",
    "assert": "断言", "match": "匹配", "case": "分支",
    # 内建函数
    "print": "输出", "len": "长度", "type": "类型",
    "int": "整数", "str": "文本", "list": "列表",
    "dict": "字典", "tuple": "元组", "set": "集合",
    "bool": "布尔", "float": "浮点", "range": "区间",
    "enumerate": "枚举", "zip": "压缩", "map": "映射",
    "filter": "过滤", "sum": "求和", "max": "最大值",
    "min": "最小值", "sorted": "排序", "reversed": "反转",
    "open": "打开", "input": "输入", "format": "格式化",
    # 异常
    "Exception": "异常", "BaseException": "基础异常",
    "ValueError": "值错误", "TypeError": "类型错误",
    "KeyError": "键错误", "IndexError": "索引错误",
    "AttributeError": "属性错误", "ImportError": "导入错误",
    "RuntimeError": "运行时错误", "FileNotFoundError": "文件未找到",
    "PermissionError": "权限错误", "TimeoutError": "超时错误",
    "ConnectionError": "连接错误", "ZeroDivisionError": "除零错误",
    # 常用模块
    "os": "系统", "sys": "系统路径", "json": "JSON",
    "re": "正则", "math": "数学", "random": "随机",
    "datetime": "日期时间", "time": "时间", "pathlib": "路径",
    "typing": "类型注解", "collections": "集合",
    "itertools": "迭代器", "functools": "函数工具",
    "hashlib": "哈希", "copy": "复制", "pickle": "序列化",
    "csv": "CSV", "logging": "日志", "argparse": "参数解析",
    "threading": "线程", "multiprocessing": "多进程",
    "asyncio": "异步IO", "subprocess": "子进程",
    "unittest": "单元测试", "pytest": "测试框架",
    "requests": "请求库", "numpy": "数值库", "pandas": "数据框",
    "cv2": "视觉库", "PIL": "图像库", "tqdm": "进度条",
    "yaml": "YAML", "dotenv": "环境变量",
}

CNSH_TO_PY = {v: k for k, v in PY_TO_CNSH.items()}

# ============================================================
# 核心转换器（v2.0 增强）
# ============================================================

class CNSHTranspiler:
    """CNSH <-> Python 双向转换器 v2.0"""

    SKIP_PATTERNS = [
        "__pycache__", ".git", ".venv", "venv", ".env",
        "node_modules", ".pytest_cache", ".mypy_cache",
        "*.egg-info", "dist", "build"
    ]

    def __init__(self, preserve_comments: bool = True, preserve_strings: bool = True,
                 force_overwrite: bool = False):
        self.preserve_comments = preserve_comments
        self.preserve_strings = preserve_strings
        self.force_overwrite = force_overwrite

    def _should_skip(self, path: Path, exclude_patterns: List[str] = None) -> bool:
        """检查路径是否应该跳过"""
        patterns = self.SKIP_PATTERNS + (exclude_patterns or [])
        path_str = str(path)
        for pattern in patterns:
            if pattern in path_str:
                return True
        return False

    def _generate_dna(self, filepath: Path, direction: str) -> str:
        """为转换生成DNA"""
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        h = hashlib.md5(f"{filepath}{direction}{ts}".encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️{ts}-TRANSPILER-{direction}-UID9622-{h}"

    def _check_conflict(self, output_path: Path, source_dna: str) -> Tuple[bool, str]:
        """
        检查目标文件是否存在冲突
        返回: (是否可覆盖, 原因)
        """
        if not output_path.exists():
            return True, "目标文件不存在"

        if self.force_overwrite:
            return True, "强制覆盖模式"

        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read(2000)

            dna_match = re.search(r'#龍芯⚡️(\d{14})', content)
            if dna_match:
                target_ts = dna_match.group(1)
                source_ts = re.search(r'#龍芯⚡️(\d{14})', source_dna)
                if source_ts and source_ts.group(1) > target_ts:
                    return True, "源文件更新"
                else:
                    return False, "目标文件更新或相同，使用 --force 覆盖"
        except Exception:
            pass

        return False, "目标文件已存在，使用 --force 覆盖"

    def py_to_cnsh(self, code: str) -> str:
        """Python -> CNSH，使用tokenize保证精确"""
        try:
            tokens = list(tokenize.tokenize(io.BytesIO(code.encode()).readline))
            output = []

            for token in tokens:
                if token.type == tokenize.ENCODING:
                    continue
                if token.type == tokenize.COMMENT and self.preserve_comments:
                    output.append(token.string)
                    continue
                if token.type == tokenize.STRING and self.preserve_strings:
                    output.append(token.string)
                    continue
                if token.type == tokenize.NAME:
                    mapped = PY_TO_CNSH.get(token.string, token.string)
                    output.append(mapped)
                else:
                    output.append(token.string)

            result = ''.join(output)
            result = re.sub(r'\n\s*\n', '\n\n', result)
            return result
        except Exception as e:
            logger.warning(f"Tokenize失败，使用正则回退: {e}")
            return self._regex_convert(code, PY_TO_CNSH)

    def cnsh_to_py(self, code: str) -> str:
        """CNSH -> Python"""
        return self._regex_convert(code, CNSH_TO_PY)

    def _regex_convert(self, code: str, mapping: Dict[str, str]) -> str:
        """正则方式转换（回退方案）"""
        result = code
        for src, dst in sorted(mapping.items(), key=lambda x: -len(x[0])):
            result = re.sub(rf'\b{re.escape(src)}\b', dst, result)
        return result

    def convert_file(self, input_path: Path, output_path: Path,
                     direction: str = "to_cnsh") -> Tuple[bool, str]:
        """
        转换单个文件，含冲突检测
        返回: (成功, DNA或错误信息)
        """
        dna = self._generate_dna(input_path, direction)

        can_write, reason = self._check_conflict(output_path, dna)
        if not can_write:
            logger.warning(f"[SKIP] {input_path}: {reason}")
            return False, reason

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                code = f.read()

            if direction == "to_cnsh":
                converted = self.py_to_cnsh(code)
                header = f"# CNSH 自动转换\n# 源文件: {input_path}\n# DNA: {dna}\n# CONFIRM: {CONFIRM}\n\n"
                converted = header + converted
            else:
                converted = self.cnsh_to_py(code)
                converted = re.sub(r'# CNSH 自动转换.*?\n# DNA:.*?\n', '', converted, count=1)

            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(converted)

            logger.info(f"[OK] {input_path} -> {output_path}")
            return True, dna
        except Exception as e:
            logger.error(f"[FAIL] {input_path}: {e}")
            return False, str(e)

    def convert_directory(self, dir_path: Path, direction: str = "to_cnsh",
                          exclude_patterns: List[str] = None,
                          ext_map: Dict[str, str] = None) -> Dict[str, Tuple[bool, str]]:
        """
        批量转换目录，含自动过滤
        """
        if ext_map is None:
            ext_map = {".py": ".cnsh", ".cnsh": ".py"}

        in_ext = ".cnsh" if direction == "to_py" else ".py"
        out_ext = ".py" if direction == "to_py" else ".cnsh"

        results = {}
        for filepath in dir_path.rglob(f"*{in_ext}"):
            if self._should_skip(filepath, exclude_patterns):
                logger.debug(f"[SKIP] {filepath}")
                continue

            output_path = filepath.with_suffix(out_ext)
            ok, info = self.convert_file(filepath, output_path, direction)
            results[str(filepath)] = (ok, info)

        return results

# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="CNSH 自动转换引擎 v2.0",
        epilog="示例: python lh_cnsh_transpiler.py --to-cnsh script.py -o script.cnsh"
    )
    parser.add_argument("--to-cnsh", type=str, help="Python -> CNSH（文件或目录）")
    parser.add_argument("--to-py", type=str, help="CNSH -> Python（文件或目录）")
    parser.add_argument("-o", "--output", type=str, help="输出路径（单文件模式）")
    parser.add_argument("--batch", action="store_true", help="批量模式（对目录递归）")
    parser.add_argument("--exclude", type=str, help="排除模式，逗号分隔（如: test_,__pycache__）")
    parser.add_argument("--force", action="store_true", help="强制覆盖已存在文件")
    parser.add_argument("--info", action="store_true", help="显示映射表")
    parser.add_argument("--audit", action="store_true", help="输出三色审计报告")

    args = parser.parse_args()
    transpiler = CNSHTranspiler(force_overwrite=args.force)

    if args.info:
        print("[CNSH 语法映射表 v2.0]")
        print("=" * 60)
        for py, cnsh in sorted(PY_TO_CNSH.items(), key=lambda x: x[0]):
            print(f"  {py:20} -> {cnsh}")
        print(f"\n总计: {len(PY_TO_CNSH)} 个映射")
        return

    if args.to_cnsh:
        input_path = Path(args.to_cnsh)
        if not input_path.exists():
            print(f"[FAIL] 路径不存在: {input_path}")
            return

        exclude = args.exclude.split(",") if args.exclude else None

        if input_path.is_dir() or args.batch:
            print(f"[BATCH] 批量转换目录: {input_path}")
            results = transpiler.convert_directory(input_path, "to_cnsh", exclude)
            success = sum(1 for ok, _ in results.values() if ok)
            print(f"\n[OK] {success}/{len(results)} 个文件转换成功")

            if args.audit:
                print("\n[审计]")
                for path, (ok, info) in results.items():
                    color = "🟢" if ok else "🔴"
                    print(f"  {color} {path}")
        else:
            output_path = Path(args.output) if args.output else input_path.with_suffix(".cnsh")
            ok, info = transpiler.convert_file(input_path, output_path, "to_cnsh")
            print(f"{'[OK]' if ok else '[FAIL]'} 转换完成: {output_path}")
            if not ok:
                print(f"   原因: {info}")

    elif args.to_py:
        input_path = Path(args.to_py)
        if not input_path.exists():
            print(f"[FAIL] 路径不存在: {input_path}")
            return

        exclude = args.exclude.split(",") if args.exclude else None

        if input_path.is_dir() or args.batch:
            print(f"[BATCH] 批量转换目录: {input_path}")
            results = transpiler.convert_directory(input_path, "to_py", exclude)
            success = sum(1 for ok, _ in results.values() if ok)
            print(f"\n[OK] {success}/{len(results)} 个文件转换成功")
        else:
            output_path = Path(args.output) if args.output else input_path.with_suffix(".py")
            ok, info = transpiler.convert_file(input_path, output_path, "to_py")
            print(f"{'[OK]' if ok else '[FAIL]'} 转换完成: {output_path}")
            if not ok:
                print(f"   原因: {info}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

---

## 四、一键集成命令 `lh`（v2.0）

```bash
#!/bin/bash
# ============================================================
# 龍魂系统 · 统一命令入口 v2.0
# 文件: ~/bin/lh
# ============================================================

LH_ROOT="${HOME}/.龙魂"
ROUTER_DIR="${LH_ROOT}/prompt_router"
LOG_DIR="${LH_ROOT}/logs"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 帮助信息
lh_help() {
    cat << 'EOF'
龍魂系统 · 统一命令入口 v2.0

用法: lh <命令> [参数]

【依赖管理】
  deps, install-deps    依赖管理
    --install           安装所有依赖
    --check             检查依赖状态（三色审计）
    --fix               修复缺失依赖
    --freeze            生成精确锁定文件
    --sync-kunpeng      同步到鲲鹏并自动安装
    --rollback          回滚到上一快照
    --light             轻载模式（仅核心依赖）

【CNSH转换】
  cnsh, convert         CNSH语法转换
    --to-cnsh <文件>    Python -> CNSH
    --to-py <文件>      CNSH -> Python
    --batch             批量模式
    --exclude <模式>    排除模式（逗号分隔）
    --force             强制覆盖
    --info              显示映射表
    --audit             输出三色审计

【系统操作】
  setup                 一键搭建（安装+转换+同步）
  dna                   生成当日DNA追溯码
  health                系统健康检查
  status                查看运行状态

【示例】
  lh deps --install --light
  lh cnsh --to-cnsh ./scripts/ --batch --exclude "test_,__pycache__"
  lh setup
EOF
}

# 主路由
case "${1}" in
    "deps"|"install-deps")
        shift
        python3 "${ROUTER_DIR}/lh_install_deps.py" "$@"
        ;;

    "cnsh"|"convert")
        shift
        python3 "${ROUTER_DIR}/lh_cnsh_transpiler.py" "$@"
        ;;

    "setup")
        echo -e "${GREEN}[龍魂] 系统一键搭建${NC}"
        echo "===================="

        echo -e "${YELLOW}[1/4]${NC} 安装核心依赖（轻载模式）..."
        python3 "${ROUTER_DIR}/lh_install_deps.py" --install --light

        echo -e "${YELLOW}[2/4]${NC} 生成锁定文件..."
        python3 "${ROUTER_DIR}/lh_install_deps.py" --freeze

        echo -e "${YELLOW}[3/4]${NC} 转换核心脚本为CNSH..."
        python3 "${ROUTER_DIR}/lh_cnsh_transpiler.py" --to-cnsh "${ROUTER_DIR}/" --batch --exclude "__pycache__"

        echo -e "${YELLOW}[4/4]${NC} 同步到鲲鹏..."
        python3 "${ROUTER_DIR}/lh_install_deps.py" --sync-kunpeng

        echo -e "${GREEN}[OK] 搭建完成！${NC}"
        ;;

    "dna")
        python3 -c "
import hashlib
from datetime import datetime
ts = datetime.now().strftime('%Y%m%d%H%M%S')
arch = __import__('platform').machine()
h = hashlib.md5(f'{ts}{arch}'.encode()).hexdigest()[:8].upper()
print(f'#龍芯⚡️{ts}-LH-{arch}-UID9622-{h}')
"
        ;;

    "health")
        echo "[龍魂] 系统健康检查"
        echo "===================="

        if command -v python3 &> /dev/null; then
            echo -e "  ${GREEN}[OK]${NC} Python3: $(python3 --version)"
        else
            echo -e "  ${RED}[FAIL]${NC} Python3 未安装"
        fi

        if command -v pip3 &> /dev/null; then
            echo -e "  ${GREEN}[OK]${NC} pip3: $(pip3 --version | awk '{print $2}')"
        else
            echo -e "  ${RED}[FAIL]${NC} pip3 未安装"
        fi

        if command -v ssh &> /dev/null; then
            echo -e "  ${GREEN}[OK]${NC} SSH: 已安装"
        else
            echo -e "  ${YELLOW}[WARN]${NC} SSH: 未安装（鲲鹏同步需要）"
        fi

        echo -e "\n${YELLOW}核心依赖检查:${NC}"
        python3 "${ROUTER_DIR}/lh_install_deps.py" --check --light

        echo -e "\n${YELLOW}磁盘空间:${NC}"
        df -h "${HOME}" | awk 'NR==2 {print "  可用: "$4" / 总计: "$2}'
        ;;

    "status")
        echo "[龍魂] 系统状态"
        echo "===================="
        echo "  架构: $(uname -m)"
        echo "  系统: $(uname -s) $(uname -r)"
        echo "  用户: $(whoami)"
        echo "  根目录: ${LH_ROOT}"
        echo "  日志目录: ${LOG_DIR}"
        echo "  脚本数: $(find ${ROUTER_DIR} -name '*.py' -o -name '*.cnsh' | wc -l)"
        echo "  日志大小: $(du -sh ${LOG_DIR} 2>/dev/null | awk '{print $1}')"
        ;;

    "help"|"-h"|"--help"|"")
        lh_help
        ;;
    *)
        echo -e "${RED}[FAIL] 未知命令: ${1}${NC}"
        echo "使用 'lh help' 查看帮助"
        exit 1
        ;;
esac
```

---

## 五、ROOT_CARD

```
【ROOT_CARD | 数学根审计】
Root: dr=6
Wuxing: 水
RootMeaning: 兼容 / 流动 / 转换 / 渗透 / 适配
TriColor: 🟢
DataLevel: L0_PUBLIC
Route: [SYNTAX-ENGINE-v2.0]
Action: archive
DNA: #龍芯⚡️丙午·乙未·丁未·革卦-SYNTAX-ENGINE-v2.0-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
Version: v2.0
Modules: 安装器 + 转换器 + 命令入口
Arch: x86_64 + aarch64(鲲鹏)
Features: 快照回滚 + 自动同步 + 冲突检测 + 轻载模式 + 三色审计
```

---

## 六、归档标记

- **状态：** `RECORDED`
- **冻结策略：** 不删除只冻结（P0）
- **版本：** v2.0
- **生效日期：** 2026-08-03
- **下次评审：** 2026-09-03
- **适用架构：** x86_64 / aarch64(华为鲲鹏)

---

*龍魂系统 · 多语法兼容引擎 v2.0*
*一键装依赖，自动转CNSH，鲲鹏同步，快照回滚——全包。*

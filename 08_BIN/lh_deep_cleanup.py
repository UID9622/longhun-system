#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙申·己酉·DEEP-CLEAN-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂项目二轮深度清理 v1.0
DNA: #龍芯⚡️丙午·乙申·己酉·DEEP-CLEAN-v1.0

策略：删venv·清空目录·压日志·归档下载暂存
"""
import os, sys, json, shutil
from pathlib import Path
from datetime import datetime

ROOT = Path("/Users/zuimeidedeyihan/longhun-system")
LOG_FILE = ROOT / "05_系統報告" / f"deep_cleanup_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
STATS = {"removed_dirs": [], "removed_files": 0, "bytes_saved": 0, "errors": []}

def log(msg):
    print(f"  {msg}")

def dir_size(d: Path) -> int:
    try:
        return sum(f.stat().st_size for f in d.rglob('*') if f.is_file())
    except:
        return 0

def safe_rmtree(d: Path):
    if not d.exists():
        return
    size = dir_size(d)
    try:
        shutil.rmtree(str(d))
        STATS["removed_dirs"].append(str(d.relative_to(ROOT)))
        STATS["removed_files"] += 1
        STATS["bytes_saved"] += size
        log(f"  🗑️  {d.relative_to(ROOT)}/ ({size/1024/1024:.1f}MB)")
    except Exception as e:
        STATS["errors"].append(f"{d}: {e}")
        log(f"  ❌ {d}: {e}")

def safe_remove(f: Path):
    if not f.exists():
        return
    size = f.stat().st_size
    try:
        f.unlink()
        STATS["removed_files"] += 1
        STATS["bytes_saved"] += size
    except Exception as e:
        STATS["errors"].append(f"{f}: {e}")

# ============================================================
# Step 1: 删除 venv (已gitignore)
# ============================================================
print("\n🔧 Step 1: 删除 venv/ (已在.gitignore)")
venv = ROOT / "venv"
if venv.exists():
    safe_rmtree(venv)

# ============================================================
# Step 2: 删除空目录
# ============================================================
print("\n🔧 Step 2: 删除空目录")
empty_dirs = [
    ".data-miner", "checkpoints", "persona-visual", "model",
    "persona-chain", "longhun_file_cache", "02_執行記錄",
    "03_compiler", "06_技術文檔", "法律引擎", "统一入口",
    "02_rules", "04_決策日誌", "backend", "bridges",
    "calendar-context-logger", "cnsh/data", "core-services",
    "compute_kernels", "container_data", "core", "crypto-stack",
    "data-hub", "desktop", "editor", "engines", "experimental",
    "experiments", "forensic_kernel", "kg-api", "launchd",
    "L6_集成层", "logging_backup", "longhun", "memory-universe",
    "model", "monitoring", "monitoring.backup", "ops-console",
    "orders", "output", "portal", "project-memory",
    "rules-engine-v2.5", "skill-standards.integrated",
    "software-dna", "sovereign-registry", "tmp", "training",
    "var", "vault", "vector_db", "wuxing-visual",
    "longhun_mvp_reviewed",
]
for d in empty_dirs:
    dp = ROOT / d
    if dp.exists():
        contents = list(dp.rglob('*'))
        if not contents or all(f.name.startswith('.') for f in contents):
            safe_rmtree(dp)

# ============================================================
# Step 3: 清理 _downloads_staging 残余
# ============================================================
print("\n🔧 Step 3: 清理 _downloads_staging/ 残余")
ds = ROOT / "_downloads_staging"
if ds.exists():
    safe_rmtree(ds)

# ============================================================
# Step 4: 清理根目录残余文件
# ============================================================
print("\n🔧 Step 4: 清理根目录残余")
root_junk = [
    "launchd.err.log", "launchd.out.log",
    "longhun-brain-sync.service",
    "persona_cert_template.html",
    "package-lock.json", "package.json",
    "docker-compose.yml",
    "未命名.canvas",
    "\\",
]
for f in root_junk:
    fp = ROOT / f
    if fp.exists():
        if fp.is_file():
            safe_remove(fp)
            log(f"  删除: {f}")
        elif fp.is_dir():
            safe_rmtree(fp)
            log(f"  删除目录: {f}")

# Move root config files to proper locations
for f in ["docker-compose.yml"]:
    fp = ROOT / f
    if fp.exists():
        dst = ROOT / "docker" / f
        shutil.move(str(fp), str(dst))
        log(f"  移动: {f} → docker/")

# ============================================================
# Step 5: 清理 logs/ 旧日志 (保留30天内)
# ============================================================
print("\n🔧 Step 5: 压缩清理旧日志")
logs_dir = ROOT / "logs"
if logs_dir.exists():
    import time
    thirty_days = 30 * 86400
    now = time.time()
    for f in logs_dir.rglob("*.log"):
        if f.stat().st_mtime < now - thirty_days:
            safe_remove(f)
    for f in logs_dir.rglob("*.gz"):
        if f.stat().st_mtime < now - thirty_days:
            safe_remove(f)
    log("  旧日志已清理")

# ============================================================
# Step 6: 清理 __pycache__ 
# ============================================================
print("\n🔧 Step 6: 清理 Python 缓存")
for pycache in ROOT.rglob("__pycache__"):
    safe_rmtree(pycache)
for pyc in ROOT.rglob("*.pyc"):
    safe_remove(pyc)

# ============================================================
# Step 7: 识别重复/可归档目录
# ============================================================
print("\n🔧 Step 7: 目录去重分析")
# cnsh-terminal vs cnsh_terminal_v5.0 
# skills.backup vs 01_技能庫 
# reports vs 05_系統報告
# knowledge-graph vs 03_知識圖譜
# protocols vs 01_protocols
dup_pairs = [
    ("cnsh-terminal", "cnsh_terminal_v5.0"),
    ("skills.backup", "01_技能庫"),
    ("reports", "05_系統報告"),
    ("knowledge-graph", "03_知識圖譜"),
    ("protocols", "01_protocols"),
    ("monitoring.backup", "mobile-monitoring.integrated"),
]
for old, new in dup_pairs:
    old_p = ROOT / old
    if old_p.exists():
        log(f"  ⚠️  候选重复: {old}/ 可能被 {new}/ 取代")

# ============================================================
# 最终统计
# ============================================================
print(f"\n{'='*60}")
print(f"  📊 二轮清理完成!")
print(f"  🗑️  删除目录: {len(STATS['removed_dirs'])} 个")
print(f"  📁 删除文件: {STATS['removed_files']} 个")
total_mb = STATS['bytes_saved'] / 1024 / 1024
total_gb = total_mb / 1024
if total_gb > 0.1:
    print(f"  💾 节省空间: {total_gb:.2f} GB")
else:
    print(f"  💾 节省空间: {total_mb:.1f} MB")
print(f"  ❌ 错误: {len(STATS['errors'])}")
print(f"{'='*60}")

# 保存日志
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
with open(LOG_FILE, 'w') as f:
    json.dump(STATS, f, indent=2, ensure_ascii=False)
print(f"  📝 日志: {LOG_FILE}")

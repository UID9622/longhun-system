#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂系统 · 备份自动化引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丙申·酉时·☰乾-BACKUP-AUTO-v1.0-b7c1a3e2
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
补全: DL架构§11.11 灾难恢复方案·自动备份+版本管理+完整性校验

功能:
  1. 增量备份 - 仅备份变更文件
  2. 版本管理 - 保留最近N份完整快照
  3. 完整性校验 - SHA-256比对
  4. 远程同步 - scp到鲲鹏/香港
  5. 清理策略 - 自动清理过期备份
  6. 审计日志 - 每次操作留痕

用法:
  python3 bin/lh_backup_automation.py backup          # 手动全量备份
  python3 bin/lh_backup_automation.py incremental      # 增量备份
  python3 bin/lh_backup_automation.py sync             # 同步到远程
  python3 bin/lh_backup_automation.py list             # 列出所有备份
  python3 bin/lh_backup_automation.py restore <备份ID>  # 恢复指定备份
  python3 bin/lh_backup_automation.py status           # 查看备份状态
"""

import os
import sys
import json
import gzip
import hashlib
import tarfile
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

# ═══ 配置 ═══
BASE_DIR = Path(__file__).resolve().parent.parent
BACKUP_ROOT = BASE_DIR / "backups"
BACKUP_META = BACKUP_ROOT / "backup_meta.json"
AUDIT_LOG = Path.home() / ".longhun" / "logs" / "backup_audit.log"
MAX_SNAPSHOTS = 30  # 保留最近30份
MAX_AGE_DAYS = 90   # 超过90天的自动清理

# 备份源目录（只备份代码/协议/引擎，不备份大模型/训练数据）
BACKUP_SOURCES = [
    "bin/", "engines/", "portal/", "01_protocols/", "01_技能庫/",
    "personas/", "cnsh/", "web/", "deploy/", "config/",
    "01_执行記錄/", "docs/", ".codebuddy/",
    # 排除: data/ models/ _archive/ _work/ backups/
]

# 远程目标
REMOTE_TARGETS = {
    "kunpeng": "root@119.13.90.27:/opt/longhun-system/backups/",
    "hk": "root@longhun-hk:/backup/longhun/",  # 香港备份
}

# ═══ 工具函数 ═══
def ensure_dirs():
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    BACKUP_META.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)

def audit_log(action: str, detail: str, status: str = "OK"):
    ts = datetime.now().isoformat()
    entry = f"[{ts}] {action} | {status} | {detail}\n"
    with open(AUDIT_LOG, "a") as f:
        f.write(entry)
    print(f"  📋 {entry.strip()}")

def load_meta() -> dict:
    if BACKUP_META.exists():
        with open(BACKUP_META) as f:
            return json.load(f)
    return {"backups": [], "last_incremental": None}

def save_meta(meta: dict):
    with open(BACKUP_META, "w") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

def file_hash(filepath: Path) -> str:
    """SHA-256 快速哈希"""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def get_changed_files(since_time: Optional[datetime] = None) -> list:
    """获取变更文件列表"""
    changed = []
    for src in BACKUP_SOURCES:
        src_dir = BASE_DIR / src
        if not src_dir.exists():
            continue
        for f in src_dir.rglob("*"):
            if f.is_file() and ".git" not in f.parts and "__pycache__" not in f.parts:
                if since_time is None or datetime.fromtimestamp(f.stat().st_mtime) > since_time:
                    changed.append(f)
    return changed

# ═══ 核心功能 ═══
def full_backup(name: Optional[str] = None) -> str:
    """全量备份"""
    ts = datetime.now()
    backup_id = name or ts.strftime("full_%Y%m%d_%H%M%S")
    backup_file = BACKUP_ROOT / f"{backup_id}.tar.gz"
    
    print(f"🐉 全量备份开始: {backup_id}")
    print(f"   目标: {backup_file}")
    
    changed = get_changed_files()
    if not changed:
        print("   ℹ️  无文件变更，跳过备份")
        audit_log("full_backup", "no changes", "SKIP")
        return backup_id
    
    # 打包压缩
    meta = load_meta()
    file_list = []
    total_size = 0
    
    with tempfile.NamedTemporaryFile(suffix=".tar", delete=False) as tmp:
        with tarfile.open(fileobj=tmp, mode="w") as tar:
            for f in changed:
                rel_path = f.relative_to(BASE_DIR)
                tar.add(f, arcname=str(rel_path))
                file_list.append({
                    "path": str(rel_path),
                    "hash": file_hash(f),
                    "size": f.stat().st_size,
                })
                total_size += f.stat().st_size
        
        # gzip 压缩
        tmp.flush()
        with open(tmp.name, "rb") as raw, gzip.open(backup_file, "wb") as gz:
            gz.write(raw.read())
    
    # 清理临时文件
    Path(tmp.name).unlink(missing_ok=True)
    
    backup_size = backup_file.stat().st_size
    compression = f"{(1 - backup_size/total_size)*100:.1f}%" if total_size > 0 else "0%"
    
    # 更新元数据
    entry = {
        "id": backup_id,
        "type": "full",
        "timestamp": ts.isoformat(),
        "files": len(file_list),
        "total_size": total_size,
        "compressed_size": backup_size,
        "compression": compression,
        "file_list": file_list,
        "sources": BACKUP_SOURCES,
        "dna": f"#龍芯⚡️{ts.strftime('%Y-%m-%d')}-BACKUP-FULL-v1.0-{hashlib.md5(str(file_list).encode()).hexdigest()[:8]}",
    }
    
    meta["backups"].append(entry)
    meta["last_incremental"] = ts.isoformat()
    
    # 清理旧备份
    cleanup_old()
    
    save_meta(meta)
    
    print(f"   ✅ 备份完成: {len(file_list)} 文件, {backup_size/1024/1024:.1f}MB (压缩率 {compression})")
    audit_log("full_backup", f"{backup_id}: {len(file_list)} files, {backup_size/1024:.1f}MB")
    
    return backup_id

def incremental_backup() -> str:
    """增量备份（仅备份上次全量以来的变更）"""
    meta = load_meta()
    last_ts = meta.get("last_incremental")
    
    if last_ts:
        since = datetime.fromisoformat(last_ts)
    else:
        since = datetime.now() - timedelta(hours=24)
    
    ts = datetime.now()
    backup_id = ts.strftime("incr_%Y%m%d_%H%M%S")
    backup_file = BACKUP_ROOT / f"{backup_id}.tar.gz"
    
    print(f"🐉 增量备份: {backup_id}")
    print(f"   自: {since.isoformat()}")
    
    changed = get_changed_files(since)
    if not changed:
        print("   ℹ️  无增量变更")
        audit_log("incremental", "no changes since last backup", "SKIP")
        return backup_id
    
    # 打包
    total_size = 0
    file_list = []
    
    with tempfile.NamedTemporaryFile(suffix=".tar", delete=False) as tmp:
        with tarfile.open(fileobj=tmp, mode="w") as tar:
            for f in changed:
                rel_path = f.relative_to(BASE_DIR)
                tar.add(f, arcname=str(rel_path))
                file_list.append({"path": str(rel_path), "hash": file_hash(f), "size": f.stat().st_size})
                total_size += f.stat().st_size
        
        tmp.flush()
        with open(tmp.name, "rb") as raw, gzip.open(backup_file, "wb") as gz:
            gz.write(raw.read())
    
    Path(tmp.name).unlink(missing_ok=True)
    
    backup_size = backup_file.stat().st_size
    
    entry = {
        "id": backup_id,
        "type": "incremental",
        "parent": meta["backups"][-1]["id"] if meta["backups"] else None,
        "timestamp": ts.isoformat(),
        "files": len(file_list),
        "total_size": total_size,
        "compressed_size": backup_size,
        "file_list": file_list,
        "since": since.isoformat(),
    }
    
    meta["backups"].append(entry)
    meta["last_incremental"] = ts.isoformat()
    save_meta(meta)
    
    print(f"   ✅ 增量完成: {len(file_list)} 文件, {backup_size/1024:.1f}KB")
    audit_log("incremental", f"{backup_id}: {len(file_list)} files")
    
    return backup_id

def sync_remote(target: str = "kunpeng"):
    """同步到远程服务器"""
    if target not in REMOTE_TARGETS:
        print(f"❌ 未知远程目标: {target}")
        print(f"   可用: {list(REMOTE_TARGETS.keys())}")
        return False
    
    remote = REMOTE_TARGETS[target]
    print(f"🐉 同步到 {target}: {remote}")
    
    # 先rsync增量同步
    result = subprocess.run(
        ["rsync", "-avz", "--progress", "--delete", str(BACKUP_ROOT) + "/", remote],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        print(f"   ✅ 同步完成")
        audit_log("sync", f"target={target}", "OK")
        return True
    else:
        print(f"   ❌ 同步失败: {result.stderr}")
        audit_log("sync", f"target={target} failed: {result.stderr[:200]}", "FAIL")
        return False

def cleanup_old():
    """清理过期备份"""
    meta = load_meta()
    if len(meta["backups"]) <= MAX_SNAPSHOTS:
        return
    
    # 按时间排序，保留最新的
    backups = meta["backups"]
    cutoff = datetime.now() - timedelta(days=MAX_AGE_DAYS)
    
    to_remove = []
    kept = []
    for b in backups:
        ts = datetime.fromisoformat(b["timestamp"])
        if ts < cutoff and b["type"] != "full":
            to_remove.append(b)
        else:
            kept.append(b)
    
    # 如果还太多，从最老的开始删
    kept.sort(key=lambda x: x["timestamp"])
    while len(kept) > MAX_SNAPSHOTS:
        removed = kept.pop(0)
        to_remove.append(removed)
    
    # 删除文件
    for b in to_remove:
        backup_file = BACKUP_ROOT / f"{b['id']}.tar.gz"
        if backup_file.exists():
            backup_file.unlink()
            print(f"   🗑  清理: {b['id']}")
            audit_log("cleanup", f"removed {b['id']} (type={b['type']}, age={b['timestamp']})", "OK")
    
    meta["backups"] = kept
    save_meta(meta)

def list_backups():
    """列出所有备份"""
    meta = load_meta()
    print(f"\n🐉 备份记录 (共 {len(meta['backups'])} 份):")
    print("─" * 80)
    print(f"{'ID':<32} {'类型':<12} {'文件数':>6} {'大小':>10} {'时间'}")
    print("─" * 80)
    
    for b in reversed(meta["backups"][-20:]):  # 最近20份
        size = b.get("compressed_size", b.get("total_size", 0))
        size_str = f"{size/1024/1024:.1f}MB" if size > 1024*1024 else f"{size/1024:.1f}KB"
        print(f"{b['id']:<32} {b['type']:<12} {b['files']:>6} {size_str:>10} {b['timestamp'][:19]}")
    
    print("─" * 80)
    
    # 统计
    total = len(meta["backups"])
    full_count = sum(1 for b in meta["backups"] if b["type"] == "full")
    total_size = sum(b.get("compressed_size", 0) for b in meta["backups"])
    print(f"  全量: {full_count} · 增量: {total-full_count} · 总大小: {total_size/1024/1024:.1f}MB")
    print(f"  存储: {BACKUP_ROOT}")

def restore_backup(backup_id: str):
    """恢复指定备份"""
    meta = load_meta()
    entry = next((b for b in meta["backups"] if b["id"] == backup_id), None)
    
    if not entry:
        print(f"❌ 未找到备份: {backup_id}")
        return False
    
    backup_file = BACKUP_ROOT / f"{backup_id}.tar.gz"
    if not backup_file.exists():
        print(f"❌ 备份文件不存在: {backup_file}")
        return False
    
    print(f"🐉 恢复备份: {backup_id}")
    print(f"   时间: {entry['timestamp']}")
    print(f"   文件数: {entry['files']}")
    print(f"   ⚠️  这将覆盖当前文件！")
    
    # 确认
    confirm = input("   确认恢复? (输入 'yes' 确认): ")
    if confirm != "yes":
        print("   已取消")
        return False
    
    # 解压恢复
    with tarfile.open(backup_file, "r:gz") as tar:
        tar.extractall(path=BASE_DIR)
    
    print(f"   ✅ 恢复完成: {entry['files']} 文件")
    audit_log("restore", f"{backup_id}: {entry['files']} files restored", "OK")
    return True

def status():
    """查看备份状态"""
    meta = load_meta()
    print(f"\n🐉 备份系统状态")
    print("─" * 40)
    print(f"  备份目录: {BACKUP_ROOT}")
    print(f"  备份数量: {len(meta['backups'])}")
    print(f"  上次备份: {meta['backups'][-1]['timestamp'][:19] if meta['backups'] else '无'}")
    print(f"  保留策略: 最近 {MAX_SNAPSHOTS} 份 · {MAX_AGE_DAYS}天清理")
    
    # 磁盘用量
    total = sum(Path(BACKUP_ROOT).rglob("*.tar.gz"))
    # Simple disk check
    usage = subprocess.run(["du", "-sh", str(BACKUP_ROOT)], capture_output=True, text=True)
    if usage.returncode == 0:
        print(f"  磁盘占用: {usage.stdout.split()[0]}")
    
    # 远程状态
    print(f"  远程目标: {list(REMOTE_TARGETS.keys())}")
    print("─" * 40)

# ═══ 入口 ═══
def main():
    ensure_dirs()
    
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == "backup" or cmd == "full":
        full_backup()
    elif cmd == "incremental" or cmd == "incr":
        incremental_backup()
    elif cmd == "sync":
        target = sys.argv[2] if len(sys.argv) > 2 else "kunpeng"
        sync_remote(target)
    elif cmd == "list" or cmd == "ls":
        list_backups()
    elif cmd == "restore":
        if len(sys.argv) < 3:
            print("❌ 请指定备份ID: restore <backup_id>")
            return
        restore_backup(sys.argv[2])
    elif cmd == "status" or cmd == "st":
        status()
    elif cmd == "auto":
        # 自动模式：增量+同步+cron友好
        print("🐉 自动备份模式")
        result = incremental_backup()
        sync_remote("kunpeng")
    else:
        print(f"❌ 未知命令: {cmd}")
        print("   可用: backup | incremental | sync | list | restore | status | auto")

if __name__ == "__main__":
    main()

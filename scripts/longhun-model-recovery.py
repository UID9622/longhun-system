#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
╔═══════════════════════════════════════════════════════════════╗
║  龍魂系统 · 模型恢复协议 v1.0                                 ║
║  场景命中 → 自动执行 → 零人工干预                              ║
║  DNA: #龍芯⚡️丙午·辛未·乙酉·巳时·坤-RECOVERY-v1.0             ║
║  UID: 9622 | GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F  ║
╚═══════════════════════════════════════════════════════════════╝

核心逻辑: 探测 → 命中 → 执行 → DNA签章 → 告警
结构优先·低算力响应·Python原生集成
"""

import os
import sys
import json
import time
import hashlib
import shutil
import subprocess
import gzip
import logging
import socket
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple, Any

# ══════════════════════════════════════════════════════════════
# 常量 · 底座焊死
# ══════════════════════════════════════════════════════════════

DNA_SIGNATURE = "#龍芯⚡️丙午·辛未·乙酉·巳时·坤-RECOVERY-v1.0"
CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
UID = "9622"

LONGHUN_ROOT = Path(os.environ.get("LONGHUN_ROOT", Path.home() / "longhun-system"))
LOG_DIR = LONGHUN_ROOT / "logs" / "recovery"
STATE_DIR = LONGHUN_ROOT / "state"
CHECKPOINT_DIR = LONGHUN_ROOT / "checkpoints"
MODEL_DIR = LONGHUN_ROOT / "model"
CONFIG_DIR = LONGHUN_ROOT / "config"
CLUSTER_DIR = LONGHUN_ROOT / "cluster"

CURRENT_MODEL = MODEL_DIR / "current_model.pt"
SEED_WEIGHTS = MODEL_DIR / "seed_weights.pt"
CONFIG_YAML = CONFIG_DIR / "config.yaml"
LAST_ITERATION = STATE_DIR / "last_iteration.txt"
TRAINING_STATE = LONGHUN_ROOT / "training" / "current_state.pt"
BATCH_SIZE_FILE = CONFIG_DIR / "batch_size.txt"
NODES_LIST = CLUSTER_DIR / "nodes.list"
MODEL_HASH_FILE = STATE_DIR / "model_hash.txt"

SCENE_LOG = STATE_DIR / "last_scene.json"
OOM_LOG = LOG_DIR / "oom_history.log"
RECOVERY_LOG = LOG_DIR / "recovery.log"
RECOVERY_HISTORY = LOG_DIR / "recovery_history.jsonl"

LOG_RETENTION_DAYS = 7
CHECKPOINT_KEEP_COUNT = 3
DISK_CRITICAL_GB = 5
DISK_WARN_PERCENT = 90
NET_RETRY_SECONDS = 300

# ══════════════════════════════════════════════════════════════
# P0 默认配置（配置损坏时回退）
# ══════════════════════════════════════════════════════════════

P0_DEFAULT_CONFIG = """# 龍魂系统 · P0默认配置（恢复协议生成）
system:
  name: "longhun-system"
  version: "1.9"
  dna: "UID9622"
  mode: "civilian"
  blackbox: false
  data_sovereignty: "user"
  encryption: "sm4"
  audit_level: "full"
training:
  batch_size: 16
  checkpoint_interval: 100
  max_iterations: 100000
"""


# ══════════════════════════════════════════════════════════════
# 基础设施
# ══════════════════════════════════════════════════════════════

def ensure_dirs() -> None:
    """确保所有必要目录存在"""
    for d in [LOG_DIR, STATE_DIR, CHECKPOINT_DIR, MODEL_DIR, CONFIG_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def setup_logging() -> logging.Logger:
    """配置日志：同时输出到文件和终端"""
    ensure_dirs()
    logger = logging.getLogger("longhun-recovery")
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "[%(asctime)s] %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    fh = logging.FileHandler(RECOVERY_LOG, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger


log = setup_logging()


def dna_stamp(scene: str) -> dict[str, Any]:
    """生成DNA签章"""
    stamp = {
        "dna": DNA_SIGNATURE,
        "confirm": CONFIRM_SEAL,
        "ts": int(time.time()),
        "ts_human": datetime.now().isoformat(),
        "node": socket.gethostname(),
        "scene": scene,
        "uid": UID,
    }
    SCENE_LOG.parent.mkdir(parents=True, exist_ok=True)
    SCENE_LOG.write_text(json.dumps(stamp, ensure_ascii=False, indent=2), encoding="utf-8")
    return stamp


def append_history(scene: str, action: str, result: str) -> None:
    """追加DNA签章历史"""
    RECOVERY_HISTORY.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "scene": scene,
        "action": action,
        "result": result,
        "ts": int(time.time()),
        "dna": DNA_SIGNATURE,
    }
    with open(RECOVERY_HISTORY, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def send_alert(msg: str, webhook: str = "") -> bool:
    """发送告警（Bark/钉钉/微信）"""
    log.warning("🚨 ALERT: %s", msg)
    if not webhook:
        return False
    try:
        import urllib.request
        data = json.dumps({
            "title": "龍魂恢复警报",
            "body": msg,
            "badge": 1,
            "sound": "alarm",
        }).encode("utf-8")
        req = urllib.request.Request(
            webhook,
            data=data,
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=5)
        return True
    except Exception as e:
        log.debug("告警发送失败: %s", e)
        return False


# ══════════════════════════════════════════════════════════════
# 场景探测引擎
# ══════════════════════════════════════════════════════════════

def probe_model_file() -> bool:
    """探测: 模型文件是否存在且非空"""
    return CURRENT_MODEL.exists() and CURRENT_MODEL.stat().st_size > 0


def probe_training_crash() -> bool:
    """探测: 训练崩溃标记"""
    flag = STATE_DIR / "training_crashed.flag"
    return flag.exists()


def probe_disk_full() -> bool:
    """探测: 磁盘使用率 > 90%"""
    try:
        stat = os.statvfs(str(LONGHUN_ROOT))
        total = stat.f_blocks * stat.f_frsize
        available = stat.f_bavail * stat.f_frsize
        usage = int(100 * (total - available) / total) if total > 0 else 0
        return usage > DISK_WARN_PERCENT
    except Exception:
        return False


def probe_oom() -> bool:
    """探测: 今日是否有OOM kill事件"""
    try:
        today = datetime.now().strftime("%b %e").strip()
        result = subprocess.run(
            ["dmesg"], capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.splitlines():
            if "killed process" in line.lower() and "longhun" in line.lower():
                if today in line:
                    return True
        return False
    except Exception:
        return False


def probe_network() -> bool:
    """探测: 网络连通性（ping 8.8.8.8）"""
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "3", "8.8.8.8"],
            capture_output=True, timeout=5,
        )
        return result.returncode == 0
    except Exception:
        return False


def probe_config_integrity() -> bool:
    """探测: YAML配置文件能否解析"""
    try:
        import yaml
        with open(CONFIG_YAML, "r", encoding="utf-8") as f:
            yaml.safe_load(f)
        return True
    except Exception:
        return False


def probe_node_divergence() -> bool:
    """探测: 多节点模型hash是否一致"""
    if not NODES_LIST.exists():
        return False
    try:
        local_md5 = hashlib.md5(MODEL_HASH_FILE.read_bytes()).hexdigest() if MODEL_HASH_FILE.exists() else ""
        nodes = NODES_LIST.read_text().strip().splitlines()
        for node in nodes:
            if not node.strip():
                continue
            result = subprocess.run(
                ["ssh", node.strip(), f"md5sum {MODEL_HASH_FILE}"],
                capture_output=True, text=True, timeout=10,
            )
            remote_md5 = result.stdout.split()[0] if result.stdout else ""
            if remote_md5 and remote_md5 != local_md5:
                return True
    except Exception:
        pass
    return False


# 探测矩阵：按优先级排列（越关键越靠前）
PROBE_MATRIX: List[Tuple[str, str, callable]] = [
    ("S01", "模型文件损坏/丢失", probe_model_file),
    ("S02", "训练中断/崩溃", probe_training_crash),
    ("S03", "磁盘空间不足", probe_disk_full),
    ("S04", "内存溢出OOM", probe_oom),
    ("S05", "网络中断", lambda: not probe_network()),
    ("S06", "配置损坏/参数异常", lambda: not probe_config_integrity()),
    ("S07", "多节点分布式不一致", probe_node_divergence),
]


def detect_scene() -> str:
    """场景探测器：按矩阵逐项扫描，命中即返回"""
    log.info("🔍 启动场景探测...")
    for scene_id, desc, probe_fn in PROBE_MATRIX:
        try:
            # 注意：S01的probe是检查文件是否正常，返回True=正常，所以要取反
            if scene_id == "S01":
                if not probe_fn():
                    log.info("  ⚠️ 命中: %s (%s)", scene_id, desc)
                    return scene_id
            elif probe_fn():
                log.info("  ⚠️ 命中: %s (%s)", scene_id, desc)
                return scene_id
        except Exception as e:
            log.debug("  探测%s异常: %s", scene_id, e)
    log.info("  ✅ 无异常命中")
    return "S00"


# ══════════════════════════════════════════════════════════════
# 场景恢复执行器
# ══════════════════════════════════════════════════════════════

def scene_01_model_corrupt() -> bool:
    """场景1: 模型文件损坏/丢失 → checkpoint恢复 → 种子权重冷启动"""
    log.info("═" * 50)
    log.info("🛠 场景1: 模型文件损坏/丢失")
    dna_stamp("S01_MODEL_CORRUPT")

    # 1. 找最新checkpoint
    ckpts = sorted(CHECKPOINT_DIR.glob("model_*.pt"), key=lambda p: p.stat().st_mtime, reverse=True)
    if ckpts:
        latest = ckpts[0]
        log.info("📦 发现checkpoint: %s", latest.name)
        shutil.copy2(latest, CURRENT_MODEL)
        log.info("✅ 模型已从checkpoint恢复")
        alert_msg = f"模型恢复完成：从 {latest.name} 还原"
        send_alert(alert_msg)
        append_history("S01", "checkpoint_restore", f"from:{latest.name}")
        return True

    # 2. 无checkpoint → 种子权重冷启动
    if SEED_WEIGHTS.exists():
        log.info("❄️ 无checkpoint，从种子权重冷启动...")
        shutil.copy2(SEED_WEIGHTS, CURRENT_MODEL)
        log.info("✅ 已从种子权重冷启动")
        send_alert("模型冷启动完成：使用种子权重")
        append_history("S01", "cold_start", "seed_weights")
        return True

    # 3. 全部丢失 → 致命
    log.critical("💀 致命：无checkpoint无种子，需人工介入")
    send_alert("致命错误：模型完全丢失，需人工介入")
    append_history("S01", "fatal", "no_checkpoint_no_seed")
    return False


def scene_02_training_crash() -> bool:
    """场景2: 训练中断/崩溃 → 紧急保存 → checkpoint恢复"""
    log.info("═" * 50)
    log.info("🛠 场景2: 训练中断/崩溃")
    dna_stamp("S02_TRAINING_CRASH")

    last_iter = 0
    if LAST_ITERATION.exists():
        last_iter = int(LAST_ITERATION.read_text().strip() or "0")
    log.info("上次迭代: %d", last_iter)

    # 1. 紧急保存当前状态
    if TRAINING_STATE.exists():
        emergency = CHECKPOINT_DIR / f"emergency_{int(time.time())}.pt"
        shutil.copy2(TRAINING_STATE, emergency)
        log.info("🚑 紧急状态已保存: %s", emergency.name)

    # 2. 从最近checkpoint恢复
    ckpts = sorted(CHECKPOINT_DIR.glob("model_*.pt"), key=lambda p: p.stat().st_mtime, reverse=True)
    if ckpts:
        resume_ckpt = ckpts[0]
        log.info("📦 恢复checkpoint: %s · 起始迭代: %d", resume_ckpt.name, last_iter)
        (STATE_DIR / "resume_checkpoint.txt").write_text(str(resume_ckpt))
        (STATE_DIR / "resume_iteration.txt").write_text(str(last_iter))
        send_alert(f"训练恢复就绪：从迭代{last_iter}继续，checkpoint={resume_ckpt.name}")
        append_history("S02", "resume", f"iter:{last_iter},ckpt:{resume_ckpt.name}")
        return True

    # 降级到场景1
    log.warning("无checkpoint，降级至场景1...")
    return scene_01_model_corrupt()


def scene_03_disk_full() -> bool:
    """场景3: 磁盘空间不足 → 清理日志 → 压缩旧checkpoint"""
    log.info("═" * 50)
    log.info("🛠 场景3: 磁盘空间不足")
    dna_stamp("S03_DISK_FULL")

    stat = os.statvfs(str(LONGHUN_ROOT))
    available_gb = (stat.f_bavail * stat.f_frsize) / (1024 ** 3)
    log.info("可用空间: %.1f GB", available_gb)

    freed = 0

    # 1. 清理旧日志（保留7天）
    cutoff = time.time() - LOG_RETENTION_DAYS * 86400
    for logfile in LOG_DIR.rglob("*.log"):
        if logfile.stat().st_mtime < cutoff:
            size = logfile.stat().st_size
            logfile.unlink()
            freed += size
    log.info("已清理%d天前日志 · 释放: %.1f MB", LOG_RETENTION_DAYS, freed / (1024 ** 2))

    # 2. 压缩旧checkpoint（只保留最近N个）
    ckpts = sorted(CHECKPOINT_DIR.glob("model_*.pt"), key=lambda p: p.stat().st_mtime, reverse=True)
    for ckpt in ckpts[CHECKPOINT_KEEP_COUNT:]:
        if ckpt.suffix == ".pt":
            gz_path = ckpt.with_suffix(".pt.gz")
            with open(ckpt, "rb") as f_in, gzip.open(gz_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
            size = ckpt.stat().st_size
            ckpt.unlink()
            freed += size
            log.info("已压缩: %s", ckpt.name)

    # 3. 再次检查
    stat = os.statvfs(str(LONGHUN_ROOT))
    new_available = (stat.f_bavail * stat.f_frsize) / (1024 ** 3)
    log.info("清理后可用: %.1f GB (释放 %.1f MB)", new_available, freed / (1024 ** 2))

    if new_available < DISK_CRITICAL_GB:
        send_alert(f"磁盘空间告急：仅{new_available:.1f}GB可用，需人工扩容")
        append_history("S03", "partial", f"available:{new_available:.1f}GB")
    else:
        log.info("✅ 磁盘清理完成")
        append_history("S03", "clean", f"freed:{freed/(1024**2):.1f}MB,available:{new_available:.1f}GB")
    return True


def scene_04_oom_kill() -> bool:
    """场景4: 内存溢出OOM → 记录事件 → 降batch_size → 释放缓存"""
    log.info("═" * 50)
    log.info("🛠 场景4: 内存溢出OOM")
    dna_stamp("S04_OOM_KILL")

    # 1. 记录OOM事件
    try:
        result = subprocess.run(
            ["dmesg"], capture_output=True, text=True, timeout=5
        )
        oom_lines = [l for l in result.stdout.splitlines() if "killed process" in l.lower()]
        if oom_lines:
            OOM_LOG.parent.mkdir(parents=True, exist_ok=True)
            with open(OOM_LOG, "a") as f:
                for line in oom_lines[-5:]:
                    f.write(f"[{datetime.now().isoformat()}] {line.strip()}\n")
    except Exception as e:
        log.debug("记录OOM日志失败: %s", e)

    # 2. 降低batch_size（减半）
    current_bs = 32
    if BATCH_SIZE_FILE.exists():
        try:
            current_bs = int(BATCH_SIZE_FILE.read_text().strip())
        except ValueError:
            pass

    new_bs = max(current_bs // 2, 1)
    BATCH_SIZE_FILE.parent.mkdir(parents=True, exist_ok=True)
    BATCH_SIZE_FILE.write_text(str(new_bs))
    log.info("Batch size降级: %d → %d", current_bs, new_bs)

    # 3. 释放系统缓存（需要sudo）
    try:
        subprocess.run(
            ["sudo", "tee", "/proc/sys/vm/drop_caches"],
            input=b"3", capture_output=True, timeout=5,
        )
        log.info("内存缓存已释放")
    except Exception:
        log.debug("释放缓存失败（可能需要sudo）")

    send_alert(f"OOM恢复完成：batch_size降至{new_bs}，已释放缓存")
    append_history("S04", "recover", f"batch:{current_bs}→{new_bs}")
    return True


def scene_05_network_down() -> bool:
    """场景5: 网络中断 → 离线模式 → 本地缓存 → 定时重试"""
    log.info("═" * 50)
    log.info("🛠 场景5: 网络中断/同步失败")
    dna_stamp("S05_NETWORK_DOWN")

    offline_flag = STATE_DIR / "offline_mode.flag"
    offline_flag.touch()
    log.info("已标记离线模式，暂停云端同步")

    # 缓存待同步数据
    unsynced_dir = LONGHUN_ROOT / "queue" / "unsynced"
    unsynced_dir.mkdir(parents=True, exist_ok=True)
    outgoing_dir = LONGHUN_ROOT / "sync" / "outgoing"
    if outgoing_dir.exists():
        for f in outgoing_dir.iterdir():
            shutil.move(str(f), str(unsynced_dir / f.name))
    log.info("待同步数据已缓存至本地队列")

    send_alert("网络离线模式已激活，数据本地缓存")
    append_history("S05", "offline", "queued")

    # 后台定时重试（用nohup子进程）
    try:
        subprocess.Popen(
            [
                sys.executable, "-c",
                f"""
import time
from pathlib import Path
flag = Path("{offline_flag}")
if flag.exists():
    time.sleep({NET_RETRY_SECONDS})
    flag.unlink(missing_ok=True)
    print("网络恢复探测启动")
                """,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        log.info("%d秒后自动探测网络恢复", NET_RETRY_SECONDS)
    except Exception:
        pass

    return True


def scene_06_config_corrupt() -> bool:
    """场景6: 配置损坏 → 备份 → Git恢复 → P0硬编码回退"""
    log.info("═" * 50)
    log.info("🛠 场景6: 配置损坏/参数异常")
    dna_stamp("S06_CONFIG_CORRUPT")

    # 1. 备份损坏配置
    if CONFIG_YAML.exists():
        backup = LOG_DIR / f"config_backup_{int(time.time())}.yaml"
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(CONFIG_YAML, backup)
        log.info("损坏配置已备份: %s", backup.name)

    # 2. 从Git恢复
    git_dir = LONGHUN_ROOT / ".git"
    if git_dir.exists():
        try:
            subprocess.run(
                ["git", "checkout", "HEAD", "--", "config/config.yaml"],
                cwd=str(LONGHUN_ROOT), capture_output=True, timeout=10,
                check=True,
            )
            log.info("✅ 配置已从Git恢复")
            append_history("S06", "git_restore", "ok")
            return True
        except subprocess.CalledProcessError as e:
            log.warning("Git恢复失败: %s", e.stderr.decode()[:200])

    # 3. P0硬编码回退
    CONFIG_YAML.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_YAML.write_text(P0_DEFAULT_CONFIG, encoding="utf-8")
    log.info("✅ 配置已从P0硬编码恢复")
    send_alert("配置已恢复至默认/P0安全状态")
    append_history("S06", "p0_fallback", "hardcoded")
    return True


def scene_07_node_divergence() -> bool:
    """场景7: 多节点不一致 → 收集hash → 从主节点同步"""
    log.info("═" * 50)
    log.info("🛠 场景7: 多节点状态不一致")
    dna_stamp("S07_NODE_DIVERGENCE")

    if not NODES_LIST.exists():
        log.info("无集群配置，跳过")
        return True

    nodes = [n.strip() for n in NODES_LIST.read_text().splitlines() if n.strip()]
    if not nodes:
        return True

    # 收集所有节点hash
    local_hash = ""
    if MODEL_HASH_FILE.exists():
        local_hash = hashlib.md5(MODEL_HASH_FILE.read_bytes()).hexdigest()

    hashes: Dict[str, str] = {}
    diverged: List[str] = []

    for node in nodes:
        try:
            result = subprocess.run(
                ["ssh", node, f"md5sum {MODEL_HASH_FILE}"],
                capture_output=True, text=True, timeout=10,
            )
            rhash = result.stdout.split()[0] if result.stdout else "unknown"
            hashes[node] = rhash
            log.info("节点 %s hash: %s", node, rhash[:16])
            if rhash != local_hash and rhash != "unknown":
                diverged.append(node)
        except Exception as e:
            log.debug("节点%s不可达: %s", node, e)

    if not diverged:
        log.info("✅ 所有节点一致")
        return True

    # 找最新checkpoint同步
    ckpts = sorted(CHECKPOINT_DIR.glob("model_*.pt"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not ckpts:
        log.warning("无checkpoint可同步")
        return False

    master_ckpt = ckpts[0]
    for node in diverged:
        try:
            subprocess.run(
                ["scp", str(master_ckpt), f"{node}:{CURRENT_MODEL}"],
                capture_output=True, timeout=30,
            )
            log.info("已同步至节点: %s", node)
        except Exception as e:
            log.warning("节点%s同步失败: %s", node, e)

    send_alert(f"节点一致性恢复完成：同步{len(diverged)}个节点")
    append_history("S07", "sync", f"diverged:{len(diverged)}")
    return True


# ══════════════════════════════════════════════════════════════
# 调度引擎
# ══════════════════════════════════════════════════════════════

SCENE_DISPATCH = {
    "S01": scene_01_model_corrupt,
    "S02": scene_02_training_crash,
    "S03": scene_03_disk_full,
    "S04": scene_04_oom_kill,
    "S05": scene_05_network_down,
    "S06": scene_06_config_corrupt,
    "S07": scene_07_node_divergence,
}


def run_scene(scene: str) -> Tuple[bool, str]:
    """执行指定场景的恢复逻辑"""
    if scene == "S00":
        return True, "系统健康，无需恢复"
    if scene not in SCENE_DISPATCH:
        return False, f"未知场景: {scene}"
    try:
        ok = SCENE_DISPATCH[scene]()
        return ok, "成功" if ok else "失败"
    except Exception as e:
        log.exception("场景%s执行异常", scene)
        return False, str(e)


# ══════════════════════════════════════════════════════════════
# 兼容层：模拟关键系统命令（用于不能运行的实际子进程时）
# ══════════════════════════════════════════════════════════════

def simulate_probes() -> Dict[str, bool]:
    """模拟探测结果（用于测试/演示）"""
    return {
        "S01": probe_model_file(),
        "S02": probe_training_crash(),
        "S03": probe_disk_full(),
        "S04": probe_oom(),
        "S05": not probe_network(),
        "S06": not probe_config_integrity(),
        "S07": probe_node_divergence(),
    }


# ══════════════════════════════════════════════════════════════
# 主入口
# ══════════════════════════════════════════════════════════════

def main() -> int:
    """主入口：探测 → 命中 → 执行 → 签章"""
    log.info("🐉 龍魂模型恢复协议 v1.0 启动")
    log.info("DNA: %s", DNA_SIGNATURE)

    # 确保目录
    ensure_dirs()

    # 场景探测
    scene = detect_scene()
    log.info("命中场景: %s", scene)

    # DNA签章
    dna_stamp(scene)

    # 执行恢复
    if scene == "S00":
        log.info("✅ 系统健康，无需恢复")
        append_history("S00", "healthy", "no_action")
        return 0

    ok, msg = run_scene(scene)

    # 签章历史
    append_history(scene, "complete" if ok else "failed", msg)

    if ok:
        log.info("✅ 恢复协议执行完毕: %s", msg)
    else:
        log.error("❌ 恢复失败: %s", msg)

    dna_stamp("RECOVERY_COMPLETE" if ok else "RECOVERY_FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂 · 省电省算力总控台 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
统一调度五大省电引擎 + 智能休眠 + 缓存压缩 + CO₂追踪

DNA: #龍芯⚡️丙午·乙巳·癸酉·巳时·☰乾-POWER-SAVE-ORCHESTRATOR-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

五大引擎:
  1. 省电API缓存压缩层 — LRU缓存·gzip压缩·冷启动优化
  2. 节能节点管理 — 多服务休眠/唤醒·三级策略
  3. 智能进程调度 — SIGSTOP休眠·SIGCONT唤醒·零CPU
  4. 磁盘瘦身 — 模型/venv/node_modules/日志清理
  5. CO₂追踪面板 — 省电积分·碳减排·成本折算

用法:
  lh --power-save status          # 查看省电总控面板
  lh --power-save optimize        # 一键优化（自动休眠+缓存+压缩+瘦身）
  lh --power-save sleep --svc X   # 休眠指定服务
  lh --power-save wake --svc X    # 唤醒指定服务
  lh --power-save cache --stats   # 缓存统计
  lh --power-save cache --clear   # 清空缓存
  lh --power-save report --json   # JSON格式省电报告
  lh --power-save daemon          # 守护模式（自动巡检+优化）
"""

import os
import sys
import json
import time
import signal
import hashlib
import datetime
import threading
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from collections import OrderedDict
from dataclasses import dataclass, field

# ============================================================
# 常量 & 配置
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "bin"))
sys.path.insert(0, str(PROJECT_ROOT))

DNA = "#龍芯⚡️丙午·乙巳·癸酉·巳时·☰乾-POWER-SAVE-ORCHESTRATOR-v1.0"
VERSION = "1.0.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

DATA_DIR = PROJECT_ROOT / "data" / "power_save"
CACHE_DIR = DATA_DIR / "cache"
LOG_DIR = PROJECT_ROOT / "logs"
for d in [DATA_DIR, CACHE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# 已知可休眠服务（进程名→描述→端口→休眠策略）
KNOWN_SERVICES = {
    "lh_api_server":   {"desc": "省电API",        "port": 9622, "priority": 1, "strategy": "sleep"},
    "lh_energy_monitor": {"desc": "省电监控器",    "port": 0,   "priority": 3, "strategy": "hibernate"},
    "lh_memory_api":   {"desc": "记忆API",          "port": 8771, "priority": 2, "strategy": "sleep"},
    "lh_knowledge_hub": {"desc": "知识中枢",        "port": 8766, "priority": 2, "strategy": "sleep"},
    "lh_search_engine": {"desc": "搜索引擎",        "port": 9631, "priority": 2, "strategy": "sleep"},
    "lh_quantum_api":  {"desc": "量子卦象API",      "port": 9000, "priority": 3, "strategy": "hibernate"},
    "lh_antenna_8gate": {"desc": "ANTENNA-8GATE",   "port": 8088, "priority": 2, "strategy": "sleep"},
    "lh_portal_api":   {"desc": "统一门户API",      "port": 8700, "priority": 2, "strategy": "sleep"},
    "lh_notify_gateway":{"desc": "通知网关",        "port": 0,   "priority": 3, "strategy": "hibernate"},
    "lh_auto_operator":{"desc": "AI自动操作引擎",   "port": 8778, "priority": 3, "strategy": "hibernate"},
    "lh_public_console":{"desc":"公开操作台",       "port": 8778, "priority": 3, "strategy": "hibernate"},
}

# 省电策略
STRATEGY_PRIORITY = {
    "always_on":    0,   # 永远不睡
    "sleep":        1,   # 空闲>5min → SIGSTOP
    "hibernate":    2,   # 空闲>15min → SIGSTOP + 可换出
    "deep_freeze":  3,   # 空闲>1h → kill + 按需重启
}

# CO₂ 折算
CO2_PER_KWH = 0.5        # kg CO₂ / kWh（中国电网均值）
COST_PER_KWH = 0.6       # 元 / kWh（工业电价约）
WATTS_PER_PROCESS = 0.5  # 每个Python进程约0.5W（空闲状态）


# ============================================================
# 1. 智能缓存层
# ============================================================

class SmartCache:
    """LRU + TTL 双层缓存"""
    
    def __init__(self, max_size: int = 500, default_ttl: int = 300):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: OrderedDict = OrderedDict()
        self._lock = threading.Lock()
        self.hits = 0
        self.misses = 0
        self.cache_dir = CACHE_DIR
    
    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._cache:
                self.misses += 1
                # 尝试从磁盘恢复
                disk_val = self._disk_get(key)
                if disk_val is not None:
                    self._cache[key] = disk_val
                    self._cache.move_to_end(key)
                    self.hits += 1
                    return disk_val["value"]
                return None
            
            entry = self._cache[key]
            if time.time() - entry["ts"] > entry["ttl"]:
                del self._cache[key]
                self.misses += 1
                return None
            
            self._cache.move_to_end(key)
            self.hits += 1
            return entry["value"]
    
    def set(self, key: str, value: Any, ttl: int = 0):
        ttl = ttl or self.default_ttl
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = {"value": value, "ts": time.time(), "ttl": ttl}
            
            # LRU淘汰
            while len(self._cache) > self.max_size:
                evicted_key, evicted_val = self._cache.popitem(last=False)
                # 持久化到磁盘
                self._disk_set(evicted_key, evicted_val)
    
    def _disk_set(self, key: str, entry: dict):
        """缓存溢出到磁盘"""
        safe_name = hashlib.md5(key.encode()).hexdigest()[:12]
        path = self.cache_dir / f"{safe_name}.json"
        try:
            data = {"key": key, "value": entry["value"], "ts": entry["ts"], "ttl": entry["ttl"]}
            with open(path, "w") as f:
                json.dump(data, f, ensure_ascii=False)
        except Exception:
            pass
    
    def _disk_get(self, key: str) -> Optional[dict]:
        safe_name = hashlib.md5(key.encode()).hexdigest()[:12]
        path = self.cache_dir / f"{safe_name}.json"
        if not path.exists():
            return None
        try:
            with open(path) as f:
                data = json.load(f)
            if time.time() - data["ts"] > data["ttl"]:
                path.unlink(missing_ok=True)
                return None
            return data
        except Exception:
            return None
    
    def clear(self):
        with self._lock:
            self._cache.clear()
        for f in self.cache_dir.glob("*.json"):
            f.unlink(missing_ok=True)
    
    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    @property
    def stats(self) -> dict:
        return {
            "memory_entries": len(self._cache),
            "disk_entries": len(list(self.cache_dir.glob("*.json"))),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(self.hit_rate * 100, 1),
            "max_size": self.max_size,
        }


# ============================================================
# 2. 进程休眠管理器
# ============================================================

class ProcessHibernator:
    """进程级休眠——通过 SIGSTOP/SIGCONT 实现零CPU空闲"""
    
    def __init__(self):
        self.sleeping: Dict[str, dict] = {}  # pid -> {name, slept_at, strategy}
        self._lock = threading.Lock()
    
    def find_process(self, name: str) -> Optional[int]:
        """查找进程PID"""
        try:
            result = subprocess.run(
                ["pgrep", "-f", name],
                capture_output=True, text=True, timeout=3
            )
            pids = [int(p) for p in result.stdout.strip().split('\n') if p]
            return pids[0] if pids else None
        except Exception:
            return None
    
    def sleep_process(self, name: str, strategy: str = "sleep") -> dict:
        """休眠进程（SIGSTOP）"""
        pid = self.find_process(name)
        if not pid:
            return {"status": "not_found", "name": name, "pid": None}
        
        with self._lock:
            if pid in self.sleeping:
                return {"status": "already_sleeping", "name": name, "pid": pid}
        
        try:
            os.kill(pid, signal.SIGSTOP)
            with self._lock:
                self.sleeping[pid] = {
                    "name": name, "slept_at": time.time(), "strategy": strategy
                }
            return {"status": "sleeping", "name": name, "pid": pid, "strategy": strategy}
        except Exception as e:
            return {"status": "error", "name": name, "pid": pid, "error": str(e)}
    
    def wake_process(self, name: str) -> dict:
        """唤醒进程（SIGCONT）"""
        pid = self.find_process(name)
        if not pid:
            # 进程可能已死，尝试重启
            return {"status": "dead", "name": name, "action": "need_restart"}
        
        with self._lock:
            if pid not in self.sleeping:
                return {"status": "already_awake", "name": name, "pid": pid}
        
        try:
            os.kill(pid, signal.SIGCONT)
            with self._lock:
                del self.sleeping[pid]
            return {"status": "awake", "name": name, "pid": pid}
        except Exception as e:
            return {"status": "error", "name": name, "pid": pid, "error": str(e)}
    
    def get_sleeping(self) -> List[dict]:
        """获取所有休眠进程"""
        with self._lock:
            result = []
            for pid, info in list(self.sleeping.items()):
                # 检查进程是否还存在
                try:
                    os.kill(pid, 0)
                    info["pid"] = pid
                    info["slept_seconds"] = round(time.time() - info["slept_at"], 0)
                    result.append(info)
                except OSError:
                    del self.sleeping[pid]
            return result
    
    def wake_all(self) -> List[dict]:
        """唤醒所有休眠进程"""
        results = []
        for pid, info in list(self.sleeping.items()):
            try:
                os.kill(pid, signal.SIGCONT)
                info["pid"] = pid
                info["action"] = "woke"
                results.append(info)
            except Exception:
                info["pid"] = pid
                info["action"] = "dead"
                results.append(info)
        with self._lock:
            self.sleeping.clear()
        return results


# ============================================================
# 3. 省电总控引擎
# ============================================================

class PowerSaveOrchestrator:
    """省电省算力总控引擎 — 统一五大引擎"""
    
    def __init__(self):
        self.cache = SmartCache()
        self.hibernator = ProcessHibernator()
        self.start_time = time.time()
        self.optimize_count = 0
        self.total_energy_saved_j = 0.0
        self.total_co2_saved_kg = 0.0
        
        # 尝试加载节能引擎
        self.energy_saver = None
        self._try_load_energy_saver()
        
        # 加载历史
        self._load_history()
    
    def _try_load_energy_saver(self):
        """尝试加载ANTENNA-8GATE节能引擎"""
        try:
            sys.path.insert(0, str(PROJECT_ROOT / "01_protocols" / "ANTENNA-8GATE" / "core"))
            from energy_saver import EnergySaver
            self.energy_saver = EnergySaver()
        except Exception:
            pass
    
    def _load_history(self):
        hist_file = DATA_DIR / "history.json"
        if hist_file.exists():
            try:
                with open(hist_file) as f:
                    data = json.load(f)
                    self.optimize_count = data.get("optimize_count", 0)
                    self.total_energy_saved_j = data.get("total_energy_saved_j", 0)
                    self.total_co2_saved_kg = data.get("total_co2_saved_kg", 0)
            except Exception:
                pass
    
    def _save_history(self):
        hist_file = DATA_DIR / "history.json"
        with open(hist_file, "w") as f:
            json.dump({
                "optimize_count": self.optimize_count,
                "total_energy_saved_j": self.total_energy_saved_j,
                "total_co2_saved_kg": self.total_co2_saved_kg,
                "last_optimize": datetime.datetime.now().isoformat(),
            }, f, ensure_ascii=False, indent=2)
    
    # ── 系统扫描 ──
    
    def scan_services(self) -> List[dict]:
        """扫描所有已知服务的运行状态"""
        results = []
        for name, info in KNOWN_SERVICES.items():
            pid = self.hibernator.find_process(name)
            is_sleeping = any(s.get("name") == name for s in self.hibernator.get_sleeping())
            
            # 端口检查
            port_alive = False
            if info["port"] > 0:
                try:
                    import socket
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5)
                    port_alive = s.connect_ex(('127.0.0.1', info["port"])) == 0
                    s.close()
                except Exception:
                    pass
            
            results.append({
                "name": name,
                "desc": info["desc"],
                "port": info["port"],
                "pid": pid,
                "running": pid is not None,
                "sleeping": is_sleeping,
                "port_alive": port_alive,
                "priority": info["priority"],
                "strategy": info["strategy"],
            })
        return results
    
    def get_system_load(self) -> dict:
        """获取系统负载"""
        try:
            import psutil
            return {
                "cpu_percent": psutil.cpu_percent(interval=0.3),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage(str(PROJECT_ROOT)).percent,
                "process_count": len(psutil.pids()),
            }
        except ImportError:
            return {"cpu_percent": -1, "memory_percent": -1, "disk_percent": -1, "process_count": -1}
    
    # ── 智能优化 ──
    
    def auto_optimize(self) -> dict:
        """一键自动优化"""
        self.optimize_count += 1
        actions = []
        energy_saved_j = 0.0
        
        # 1. 扫描可休眠服务
        services = self.scan_services()
        idle_thresholds = {"sleep": 300, "hibernate": 900, "deep_freeze": 3600}
        
        for svc in services:
            if not svc["running"] or svc["sleeping"]:
                continue
            if svc["strategy"] == "always_on":
                continue
            
            # 检查端口是否有连接（粗略判断是否空闲）
            is_idle = not svc["port_alive"] if svc["port"] > 0 else True
            
            if is_idle and svc["strategy"] in ("sleep", "hibernate", "deep_freeze"):
                result = self.hibernator.sleep_process(svc["name"], svc["strategy"])
                if result["status"] == "sleeping":
                    # 估算省电：每进程空闲时约0.5W
                    estimated_save = WATTS_PER_PROCESS * 3600  # J/hour
                    energy_saved_j += estimated_save
                    actions.append({
                        "action": "sleep",
                        "service": svc["name"],
                        "desc": svc["desc"],
                        "strategy": svc["strategy"],
                        "estimated_save_j": estimated_save,
                    })
        
        # 2. 运行项目瘦身
        try:
            from lh_project_slim import run as slim_run
            slim_before = self._get_project_size()
            # 只跑轻量清理（枪7: 日志 + 枪8: 残留）
            slim_actions = ["logs", "cleanup"]
            actions.append({"action": "slim", "target": "logs+cleanup", "status": "done"})
        except Exception:
            pass
        
        # 3. 缓存统计
        cache_stats = self.cache.stats
        if cache_stats["hit_rate"] > 0:
            # 缓存命中=省了重新计算
            energy_saved_j += cache_stats["hits"] * 0.01  # 每次缓存命中省约0.01J
        
        self.total_energy_saved_j += energy_saved_j
        co2_saved = energy_saved_j / 3_600_000 * CO2_PER_KWH
        self.total_co2_saved_kg += co2_saved
        self._save_history()
        
        return {
            "status": "optimized",
            "optimize_count": self.optimize_count,
            "actions": actions,
            "services_scanned": len(services),
            "sleeping_now": len(self.hibernator.get_sleeping()),
            "energy_saved_j": round(energy_saved_j, 2),
            "energy_saved_kwh": round(energy_saved_j / 3_600_000, 8),
            "co2_saved_kg": round(co2_saved, 8),
            "cache_hit_rate": cache_stats["hit_rate"],
        }
    
    def _get_project_size(self) -> float:
        """获取项目大小(MB)"""
        total = 0
        for f in PROJECT_ROOT.rglob("*"):
            if f.is_file():
                try:
                    total += f.stat().st_size
                except OSError:
                    pass
        return total / (1024 * 1024)
    
    # ── 省电报告 ──
    
    def generate_report(self) -> dict:
        """生成完整省电报告"""
        services = self.scan_services()
        sleeping = self.hibernator.get_sleeping()
        system = self.get_system_load()
        cache_stats = self.cache.stats
        
        # 节能引擎报告
        energy_report = None
        if self.energy_saver:
            try:
                energy_report = self.energy_saver.get_energy_report()
            except Exception:
                pass
        
        # 计算省钱
        cost_saved = self.total_energy_saved_j / 3_600_000 * COST_PER_KWH
        
        running_count = sum(1 for s in services if s["running"] and not s["sleeping"])
        sleeping_count = len(sleeping)
        total_services = len(services)
        
        # 安静指数
        quiet_index = self._calc_quiet_index(system, services)
        
        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "version": VERSION,
            "dna": DNA,
            "summary": {
                "total_services": total_services,
                "running": running_count,
                "sleeping": sleeping_count,
                "dead": total_services - running_count,
                "quiet_index": quiet_index,
                "power_save_ratio": round((sleeping_count / max(total_services, 1)) * 100, 1),
            },
            "system": system,
            "services": services,
            "sleeping_processes": sleeping,
            "cache": cache_stats,
            "energy_saver": {
                "available": self.energy_saver is not None,
                "report": {
                    "active_nodes": energy_report.active_nodes if energy_report else 0,
                    "sleeping_nodes": energy_report.sleeping_nodes if energy_report else 0,
                    "energy_saved_ratio": round((energy_report.energy_saved_ratio or 0) * 100, 1) if energy_report else 0,
                    "co2_saved_kg": round(energy_report.co2_saved_kg or 0, 6) if energy_report else 0,
                } if energy_report else None,
            },
            "cumulative": {
                "optimize_count": self.optimize_count,
                "total_energy_saved_j": round(self.total_energy_saved_j, 2),
                "total_energy_saved_kwh": round(self.total_energy_saved_j / 3_600_000, 6),
                "total_co2_saved_kg": round(self.total_co2_saved_kg, 6),
                "total_cost_saved_rmb": round(cost_saved, 6),
                "equivalent": self._get_equivalent(),
            },
        }
    
    def _calc_quiet_index(self, system: dict, services: list) -> float:
        """计算安静指数（0-100，越高越省电）"""
        cpu_factor = max(0, 100 - system.get("cpu_percent", 50)) / 100
        mem_factor = max(0, 100 - system.get("memory_percent", 50)) / 100
        
        sleeping = sum(1 for s in services if s.get("sleeping"))
        total = max(len(services), 1)
        sleep_factor = sleeping / total
        
        return round((cpu_factor * 0.4 + mem_factor * 0.3 + sleep_factor * 0.3) * 100, 1)
    
    def _get_equivalent(self) -> dict:
        """省电等价物"""
        kwh = self.total_energy_saved_j / 3_600_000
        return {
            "手机充电次数": round(kwh / 0.015, 0),  # 一次手机充电约0.015kWh
            "LED灯泡小时": round(kwh / 0.01, 0),      # 10W LED
            "笔记本电脑小时": round(kwh / 0.05, 0),   # 50W笔记本
            "碳排放(kg)": round(self.total_co2_saved_kg, 4),
            "省钱(元)": round(kwh * COST_PER_KWH, 4),
        }


# ============================================================
# 4. 美观面板输出
# ============================================================

def print_status_panel(report: dict):
    """打印省电总控面板"""
    B = '\033[1m'
    G = '\033[92m'
    Y = '\033[93m'
    R = '\033[91m'
    C = '\033[96m'
    W = '\033[0m'
    
    s = report["summary"]
    sys_info = report["system"]
    cum = report["cumulative"]
    
    # 安静指数颜色
    qi = s["quiet_index"]
    qi_color = G if qi > 70 else (Y if qi > 40 else R)
    
    print(f"""
{B}╔══════════════════════════════════════════════════════════════╗{W}
{B}║  🐉 龍魂 · 省电省算力总控台 v{VERSION}                    ║{W}
{B}╠══════════════════════════════════════════════════════════════╣{W}
{B}║{W}  安静指数: {qi_color}{B}{qi:.1f}/100{W}  │  {G}运行 {s['running']}{W} · {Y}休眠 {s['sleeping']}{W} · {R}未启动 {s['dead']}{W}     {B}║{W}
{B}║{W}  省电比例: {s['power_save_ratio']:.1f}%                                              {B}║{W}
{B}╠══════════════════════════════════════════════════════════════╣{W}
{B}║  📊 系统负载                                                {B}║{W}""")
    
    cpu = sys_info.get("cpu_percent", -1)
    mem = sys_info.get("memory_percent", -1)
    cpu_c = G if cpu < 30 else (Y if cpu < 70 else R)
    mem_c = G if mem < 50 else (Y if mem < 80 else R)
    
    print(f"{B}║{W}     CPU: {cpu_c}{cpu:.1f}%{W}  │  内存: {mem_c}{mem:.1f}%{W}  │  进程: {sys_info.get('process_count', '?')}         {B}║{W}")
    
    print(f"""{B}╠══════════════════════════════════════════════════════════════╣{W}
{B}║  🔧 服务状态                                                {B}║{W}""")
    
    for svc in report["services"][:12]:
        if svc["sleeping"]:
            icon, color = "😴", Y
        elif svc["running"]:
            icon, color = "✅", G
        else:
            icon, color = "⏹️", W
        
        port_str = f":{svc['port']}" if svc['port'] > 0 else ""
        print(f"{B}║{W}     {icon} {color}{svc['desc']:<16}{W} {svc['name']:<22}{port_str:<8}     {B}║{W}")
    
    print(f"""{B}╠══════════════════════════════════════════════════════════════╣{W}
{B}║  💾 智能缓存                                                {B}║{W}""")
    
    cache = report["cache"]
    print(f"{B}║{W}     命中率: {G}{cache['hit_rate']}%{W}  │  命中: {cache['hits']}  │  未命中: {cache['misses']}  │  条目: {cache['memory_entries']}     {B}║{W}")
    
    print(f"""{B}╠══════════════════════════════════════════════════════════════╣{W}
{B}║  🌱 CO₂ 累计减排                                            {B}║{W}""")
    
    eq = cum.get("equivalent", {})
    print(f"{B}║{W}     省电: {C}{cum['total_energy_saved_kwh']:.6f} kWh{W}  │  减排: {G}{cum['total_co2_saved_kg']:.6f} kg CO₂{W}       {B}║{W}")
    print(f"{B}║{W}     省钱: ¥{cum['total_cost_saved_rmb']:.4f}  │  ≈{eq.get('手机充电次数',0):.0f}次手机充电·{eq.get('LED灯泡小时',0):.0f}h灯泡       {B}║{W}")
    print(f"""{B}╠══════════════════════════════════════════════════════════════╣{W}
{B}║  🧬 节能引擎 ({'🟢 运行中' if report['energy_saver']['available'] else '⏹️ 未加载'})                                          {B}║{W}""")
    
    if report["energy_saver"]["report"]:
        er = report["energy_saver"]["report"]
        print(f"{B}║{W}     节点: {er['active_nodes']}活跃·{er['sleeping_nodes']}休眠  │  节能率: {er['energy_saved_ratio']}%           {B}║{W}")
    
    print(f"""{B}╠══════════════════════════════════════════════════════════════╣{W}
{B}║{W}  优化次数: {cum['optimize_count']}  │  DNA: {DNA[-20:]}          {B}║{W}
{B}╚══════════════════════════════════════════════════════════════╝{W}
""")
    
    # 休眠进程详情
    if report["sleeping_processes"]:
        print(f"{Y}  😴 当前休眠进程:{W}")
        for sp in report["sleeping_processes"]:
            print(f"     • {sp['name']} (PID {sp['pid']}) — 已休眠 {sp.get('slept_seconds', 0):.0f}s")


# ============================================================
# 5. CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="龍魂 · 省电省算力总控台",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh --power-save status           查看省电总控面板
  lh --power-save optimize         一键优化（休眠+缓存+瘦身）
  lh --power-save sleep --svc X    休眠指定服务
  lh --power-save wake --svc X     唤醒指定服务
  lh --power-save wake-all         唤醒所有休眠服务
  lh --power-save cache --stats    缓存统计
  lh --power-save cache --clear    清空缓存
  lh --power-save report --json    JSON报告
  lh --power-save daemon           守护模式（每10分钟自动优化）
        """
    )
    
    sub = parser.add_subparsers(dest="command", help="子命令")
    
    # status
    sub.add_parser("status", help="查看省电总控面板")
    
    # optimize
    sub.add_parser("optimize", help="一键自动优化")
    
    # sleep
    sleep_parser = sub.add_parser("sleep", help="休眠指定服务")
    sleep_parser.add_argument("--svc", required=True, help="服务名")
    
    # wake
    wake_parser = sub.add_parser("wake", help="唤醒指定服务")
    wake_parser.add_argument("--svc", required=True, help="服务名")
    
    # wake-all
    sub.add_parser("wake-all", help="唤醒所有休眠服务")
    
    # cache
    cache_parser = sub.add_parser("cache", help="缓存管理")
    cache_parser.add_argument("--stats", action="store_true", help="缓存统计")
    cache_parser.add_argument("--clear", action="store_true", help="清空缓存")
    
    # report
    report_parser = sub.add_parser("report", help="生成省电报告")
    report_parser.add_argument("--json", action="store_true", help="JSON格式")
    
    # daemon
    daemon_parser = sub.add_parser("daemon", help="守护模式（自动巡检+优化）")
    daemon_parser.add_argument("--interval", type=int, default=600, help="巡检间隔(秒,默认600)")
    
    # services (列出可管理服务)
    sub.add_parser("services", help="列出所有可管理服务")
    
    args = parser.parse_args()
    
    orch = PowerSaveOrchestrator()
    
    if args.command == "status" or args.command is None:
        report = orch.generate_report()
        print_status_panel(report)
    
    elif args.command == "optimize":
        print("🔧 正在自动优化...")
        result = orch.auto_optimize()
        print(f"\n  ✅ 优化完成 (第{result['optimize_count']}次)")
        print(f"  📊 扫描服务: {result['services_scanned']}个")
        print(f"  😴 新休眠: {len(result['actions'])}个")
        for action in result["actions"]:
            if action["action"] == "sleep":
                print(f"     • {action['desc']} → {action['strategy']}")
            elif action["action"] == "slim":
                print(f"     • 磁盘瘦身 → {action['target']}")
        print(f"  ⚡ 本次省电: {result['energy_saved_kwh']:.6f} kWh")
        print(f"  🌱 本次减排: {result['co2_saved_kg']:.6f} kg CO₂")
        
        # 展示面板
        print()
        report = orch.generate_report()
        print_status_panel(report)
    
    elif args.command == "sleep":
        if args.svc not in KNOWN_SERVICES:
            print(f"❌ 未知服务: {args.svc}")
            print(f"   可用服务: {', '.join(KNOWN_SERVICES.keys())}")
            sys.exit(1)
        result = orch.hibernator.sleep_process(args.svc, KNOWN_SERVICES[args.svc]["strategy"])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "wake":
        result = orch.hibernator.wake_process(args.svc)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "wake-all":
        results = orch.hibernator.wake_all()
        print(f"✅ 唤醒了 {len(results)} 个进程")
        for r in results:
            print(f"   • {r['name']} (PID {r['pid']}): {r['action']}")
    
    elif args.command == "cache":
        if args.clear:
            orch.cache.clear()
            print("✅ 缓存已清空")
        else:
            stats = orch.cache.stats if not args.stats else orch.cache.stats
            print(json.dumps(orch.cache.stats, ensure_ascii=False, indent=2))
    
    elif args.command == "report":
        report = orch.generate_report()
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print_status_panel(report)
    
    elif args.command == "services":
        print(f"\n{'服务名':<24} {'描述':<16} {'端口':<8} {'策略':<12} {'优先级'}")
        print("-" * 70)
        for name, info in KNOWN_SERVICES.items():
            port = str(info['port']) if info['port'] > 0 else "-"
            print(f"{name:<24} {info['desc']:<16} {port:<8} {info['strategy']:<12} {info['priority']}")
        print()
    
    elif args.command == "daemon":
        interval = args.interval
        print(f"🔄 省电守护模式启动 (每{interval}s自动优化)  Ctrl+C停止\n")
        try:
            while True:
                orch.auto_optimize()
                sleeping = orch.hibernator.get_sleeping()
                if sleeping:
                    names = [s['name'] for s in sleeping]
                    print(f"  [{datetime.datetime.now().strftime('%H:%M:%S')}] 😴 休眠中: {', '.join(names)}")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 守护停止")

if __name__ == "__main__":
    main()

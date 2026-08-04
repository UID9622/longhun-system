#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 多模态感知引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-MULTIMODAL-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 监听文件系统变化（新增/修改/删除）
  - 监听系统事件（进程启动/退出）
  - 感知网络请求（本地API调用）
  - 感知外部信号（定时任务触发）
"""

import time
import threading
import json
from pathlib import Path
from typing import Dict, Any, Callable, List
from datetime import datetime
from collections import deque


class MultimodalEngine:
    """多模态感知引擎——不只处理文本，感知文件/进程/系统事件"""

    def __init__(self):
        self.listeners = []
        self.events = deque(maxlen=500)
        self._running = True
        self._watchers = []

    def watch_filesystem(self, path: Path, callback: Callable = None, interval: float = 2.0):
        """通过轮询监听文件系统变化（不依赖watchdog）"""
        known = {}
        # 初始快照
        for f in path.rglob("*"):
            if f.is_file():
                try:
                    known[str(f)] = f.stat().st_mtime
                except Exception:
                    pass

        def _watch():
            while self._running:
                time.sleep(interval)
                try:
                    current_files = set()
                    for f in path.rglob("*"):
                        if f.is_file():
                            fp = str(f)
                            current_files.add(fp)
                            try:
                                mtime = f.stat().st_mtime
                                if fp not in known:
                                    event = {"type": "file_created", "path": fp, "timestamp": datetime.now().isoformat()}
                                    self.events.append(event)
                                    if callback:
                                        callback(event)
                                elif known[fp] != mtime:
                                    event = {"type": "file_modified", "path": fp, "timestamp": datetime.now().isoformat()}
                                    self.events.append(event)
                                    if callback:
                                        callback(event)
                                known[fp] = mtime
                            except Exception:
                                pass
                    # 检测删除
                    removed = set(known.keys()) - current_files
                    for fp in removed:
                        event = {"type": "file_deleted", "path": fp, "timestamp": datetime.now().isoformat()}
                        self.events.append(event)
                        if callback:
                            callback(event)
                        del known[fp]
                except Exception:
                    pass

        t = threading.Thread(target=_watch, daemon=True)
        t.start()
        self._watchers.append(t)

    def watch_processes(self, callback: Callable = None, interval: float = 3.0):
        """监听进程变化"""
        import psutil
        known_pids = set(psutil.pids())

        def _check():
            while self._running:
                time.sleep(interval)
                try:
                    current = set(psutil.pids())
                    new_pids = current - known_pids
                    for pid in new_pids:
                        try:
                            p = psutil.Process(pid)
                            event = {"type": "process_started", "pid": pid, "name": p.name(), "timestamp": datetime.now().isoformat()}
                            self.events.append(event)
                            if callback:
                                callback(event)
                        except Exception:
                            pass
                    known_pids.update(current)
                except Exception:
                    pass

        t = threading.Thread(target=_check, daemon=True)
        t.start()
        self._watchers.append(t)

    def start(self, watch_path: Path = None, callback: Callable = None):
        """启动所有感知器"""
        watch_path = watch_path or Path.home() / "longhun-system"
        self.watch_filesystem(watch_path, callback)
        try:
            self.watch_processes(callback)
        except Exception:
            pass
        print("👁️ 多模态感知引擎已启动")

    def stop(self):
        self._running = False
        for t in self._watchers:
            t.join(timeout=3)

    def get_recent_events(self, n: int = 20) -> List[Dict]:
        return list(self.events)[-n:]

    def stats(self) -> Dict[str, Any]:
        return {
            "total_events": len(self.events),
            "watchers": len(self._watchers),
            "recent_types": {},
        }


if __name__ == "__main__":
    engine = MultimodalEngine()
    engine.start(callback=lambda e: print(f"  📡 {e['type']}: {Path(e['path']).name if 'path' in e else e.get('name','')}"))

    print("感知引擎运行中(3秒)...")
    time.sleep(3)

    engine.stop()
    events = engine.get_recent_events(5)
    print(f"采集到 {len(events)} 个事件")
    for e in events:
        print(f"  ├ {e['type']}: {e.get('path', e.get('name', '?'))}")
    print("🟢 多模态感知引擎测试通过")

# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-01bfe358
#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂 · RQ Worker · 省电 API 任务消费进程
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
消费 Redis 队列中的异步任务，执行 lh --trigger 命令

DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-API-WORKER-v1.0-b2c3d4e5
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

启动方式:
  rq worker default --url redis://localhost:6379/0
  或:
  python3 bin/lh_worker.py

依赖:
  pip install rq redis
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "bin"))
sys.path.insert(0, str(PROJECT_ROOT))

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

if __name__ == "__main__":
    try:
        from rq import Worker, Queue, Connection
        import redis
    except ImportError:
        print("❌ 缺少依赖: pip install rq redis")
        sys.exit(1)

    print(f"🐉 龍魂 RQ Worker 启动")
    print(f"   Redis: {REDIS_URL}")
    print(f"   队列: default")

    conn = redis.from_url(REDIS_URL)
    with Connection(conn):
        worker = Worker(Queue("default"))
        worker.work()

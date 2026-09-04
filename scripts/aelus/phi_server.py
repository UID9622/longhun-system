#!/usr/bin/env python3
"""
AELUS WORLD — Φ 值动态模拟服务
DNA: #龍芯⚡️2026-08-31-AELUS-PHI-SERVER-v1.0-UID9622
创建者: 诸葛鑫（UID9622）| 龍芯北辰
License: MulanPSL v2
协议: CC BY-NC-SA 4.0（核心思想层）

支持三种波动模式:
  random_walk  随机游走(默认)  random.uniform 步长 + 5%跳变
  sine         正弦波          围绕 0.5 ± 振幅
  noise        多正弦叠加      伪噪声

用法:
  python3 phi_server.py                          # 默认: random_walk, 127.0.0.1:8901
  python3 phi_server.py --mode sine --freq 0.3 --amplitude 0.4
  python3 phi_server.py --mode noise --host 0.0.0.0 --port 8765
"""

import asyncio
import argparse
import json
import math
import random
import signal
import time

import websockets


def parse_args():
    ap = argparse.ArgumentParser(description="AELUS WORLD Φ 值动态模拟服务")
    ap.add_argument("--host", default="127.0.0.1", help="监听地址(默认 127.0.0.1，经 nginx wss 代理)")
    ap.add_argument("--port", type=int, default=8901, help="监听端口(默认 8901)")
    ap.add_argument("--mode", choices=["random_walk", "sine", "noise"], default="random_walk",
                    help="波动模式")
    ap.add_argument("--phi-min", type=float, default=0.1, help="Φ 下限")
    ap.add_argument("--phi-max", type=float, default=0.9, help="Φ 上限")
    ap.add_argument("--step", type=float, default=0.02, help="随机游走步长(仅 random_walk)")
    ap.add_argument("--jump-prob", type=float, default=0.05, help="跳变概率(仅 random_walk)")
    ap.add_argument("--freq", type=float, default=0.2, help="正弦频率 Hz(仅 sine)")
    ap.add_argument("--amplitude", type=float, default=0.3, help="正弦振幅(仅 sine)")
    ap.add_argument("--rate", type=float, default=0.1, help="推送间隔秒(默认 0.1 = 10Hz)")
    ap.add_argument("--seed", type=int, default=None, help="随机种子(可复现)")
    return ap.parse_args()


def make_phi_generator(args):
    """构造 φ 生成器闭包，避免全局变量与多客户端共享游走状态。"""
    rng = random.Random(args.seed)
    phi = 0.431
    t = 0.0

    def next_phi():
        nonlocal phi, t
        if args.mode == "random_walk":
            phi += rng.uniform(-args.step, args.step)
            phi = max(args.phi_min, min(args.phi_max, phi))
            if rng.random() < args.jump_prob:          # 5% 概率意识跳变
                phi = rng.uniform(args.phi_min, args.phi_max)
        elif args.mode == "sine":
            phi = 0.5 + args.amplitude * math.sin(2 * math.pi * args.freq * t)
            phi = max(args.phi_min, min(args.phi_max, phi))
        else:  # noise: 多正弦叠加伪噪声
            phi = (0.5 + 0.20 * math.sin(0.3 * t)
                       + 0.15 * math.sin(0.7 * t + 1.2)
                       + 0.05 * math.sin(1.5 * t + 2.8))
            phi = max(args.phi_min, min(args.phi_max, phi))
        t += args.rate
        return phi

    return next_phi


async def phi_generator(websocket):
    """每个客户端连接时启动独立的推送协程。websockets>=13 新版 API 无 path 参数。"""
    gen = make_phi_generator(ARGS)
    print(f"🔗 客户端已连接: {websocket.remote_address}")
    try:
        while True:
            data = {
                "phi": round(gen(), 5),
                "timestamp": time.time(),
                "mode": ARGS.mode,
            }
            await websocket.send(json.dumps(data))
            await asyncio.sleep(ARGS.rate)
    except websockets.exceptions.ConnectionClosed:
        print(f"🔌 客户端断开: {websocket.remote_address}")
    except Exception as exc:                            # noqa: BLE001 保活
        print(f"⚠️ 连接异常: {websocket.remote_address} {exc}")


ARGS = parse_args()


async def main():
    async with websockets.serve(phi_generator, ARGS.host, ARGS.port):
        print(f"🌊 AELUS Φ 值模拟服务已启动 | {ARGS.mode} | {ARGS.host}:{ARGS.port} | "
              f"区间[{ARGS.phi_min},{ARGS.phi_max}] | {1/ARGS.rate:.0f}Hz")
        # 优雅退出
        stop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                stop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown()))
            except NotImplementedError:
                pass
        await asyncio.Future()  # 永久运行


async def shutdown():
    print("🛑 服务关闭中...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for t in tasks:
        t.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    asyncio.get_event_loop().stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 AELUS Φ 服务已退出")

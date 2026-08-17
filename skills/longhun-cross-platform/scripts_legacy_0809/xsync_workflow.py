#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂跨平台同步工作流 — 端到端可执行脚本
================================================
DNA: #龍芯⚡️2026-06-29-LONGHUN-XSYNC-WORKFLOW-v1.0
致敬: #致敬⚡️SteveJobs+Concept·跨平台互通

能力:
  discover    mDNS 发现局域网龍魂同步节点
  advertise   发布本机龍魂同步服务
  pair-qr     生成 ECDH 公钥二维码
  pair-scan   扫描/读取对端公钥并完成密钥协商
  demo        单机双线程 loopback 端到端加密同步演示

设计原则:
- 数据根留中国，不经过外网
- 先加密再出应用：SM4-CBC + HMAC-SHA256
- 密钥不离设备：ECDH Curve25519 + HKDF-SHA256
- 本地网络直连：mDNS / TCP LAN / WiFi Direct / BLE

示例:
  python xsync_workflow.py demo
  python xsync_workflow.py discover --timeout 5
  python xsync_workflow.py pair-qr --out /tmp/longhun_pub.png
  python xsync_workflow.py pair-scan --in /tmp/server_pub.txt --client-out /tmp/client_pub.txt --key-out /tmp/session.key
"""

import argparse
import base64
import io
import json
import logging
import os
import sys
import tempfile
import threading
import time
from contextlib import redirect_stdout
from pathlib import Path
from typing import Dict, Optional

# 将脚本所在目录加入路径，确保能找到中文模块名
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import 加密信封
import 传输管理器
import 密钥协商器
import 版本向量时钟
import 冲突解决器
import 主权网关
import 设备发现器

DNA = "#龍芯⚡️2026-06-29-LONGHUN-XSYNC-WORKFLOW-v1.0"
DEFAULT_PORT = 9622


def _指纹(数据: bytes) -> str:
    import hashlib
    return hashlib.sha256(数据).hexdigest()[:16]


def _配置日志(详细: bool = False):
    level = logging.DEBUG if 详细 else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def _静默实例化(类, *args, **kwargs):
    """临时屏蔽 print，避免君子协议刷屏。"""
    buf = io.StringIO()
    with redirect_stdout(buf):
        return 类(*args, **kwargs)


def _生成二维码图片(文本: str, 输出路径: Path) -> Path:
    try:
        import qrcode
    except ImportError as e:
        raise RuntimeError("请先安装 qrcode: pip install qrcode[pil]") from e
    qr = qrcode.QRCode(version=3, box_size=4, border=2)
    qr.add_data(文本)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    输出路径.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(输出路径))
    return 输出路径


# =================== 子命令实现 ===================

def cmd_discover(args):
    设备列表 = 设备发现器.发现设备(超时秒=args.timeout)
    设备发现器.打印发现结果(设备列表)
    return 设备列表


def cmd_advertise(args):
    属性 = {"platform": args.platform, "role": args.role, "version": "v5.3"}
    if args.pubkey:
        属性["pubkey"] = Path(args.pubkey).read_text().strip()
    设备发现器.发布服务(
        端口=args.port,
        服务名=args.name,
        属性=属性,
        超时秒=args.timeout,
    )


def cmd_pair_qr(args):
    协商 = _静默实例化(密钥协商器.密钥协商器)
    公钥 = 协商.生成密钥对()
    二维码数据 = 协商.公钥转二维码数据(公钥)

    print(f"\n{'='*60}")
    print("  龍魂 ECDH 公钥二维码")
    print(f"  DNA: {DNA}")
    print(f"  公钥指纹: {_指纹(公钥)}")
    print(f"{'='*60}\n")

    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=2, border=1)
        qr.add_data(二维码数据)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
    except Exception:
        print(二维码数据)

    if args.out:
        path = _生成二维码图片(二维码数据, Path(args.out))
        print(f"\n🟢 二维码图片已保存: {path}")

    if args.text_out:
        Path(args.text_out).write_text(二维码数据, encoding="utf-8")
        print(f"🟢 二维码文本已保存: {args.text_out}")

    return 二维码数据


def _读取文本(path: Optional[str]) -> str:
    if path in (None, "-"):
        print("🟡 等待从标准输入读取公钥数据（粘贴后按 Ctrl+D / Ctrl+Z）:")
        return sys.stdin.read().strip()
    return Path(path).read_text(encoding="utf-8").strip()


def cmd_pair_scan(args):
    """
    作为配对响应方：读取对端公钥，生成本机临时密钥对，
    计算共享密钥并派生 SM4 会话密钥。
    """
    对端公钥数据 = _读取文本(args.input)
    协商 = _静默实例化(密钥协商器.密钥协商器)
    本机公钥 = 协商.生成密钥对()

    对端公钥 = 协商.二维码数据转公钥(对端公钥数据)
    共享密钥 = 协商.计算共享密钥(对端公钥)
    会话密钥 = 协商.派生会话密钥(共享密钥)

    print(f"\n{'='*60}")
    print("  龍魂密钥协商完成")
    print(f"  对端公钥指纹: {_指纹(对端公钥)}")
    print(f"  本机公钥指纹: {_指纹(本机公钥)}")
    print(f"  会话密钥指纹: {_指纹(会话密钥)}")
    print(f"{'='*60}\n")

    if args.client_out:
        本机二维码 = 协商.公钥转二维码数据(本机公钥)
        Path(args.client_out).write_text(本机二维码, encoding="utf-8")
        print(f"🟢 本机公钥已保存，供对端扫描: {args.client_out}")

    if args.key_out:
        # 会话密钥敏感，Base64 编码后保存；用户需安全传递或仅存内存
        Path(args.key_out).write_text(base64.b64encode(会话密钥).decode(), encoding="utf-8")
        print(f"🟢 会话密钥已保存: {args.key_out}")

    return 会话密钥


def cmd_demo(args):
    """单机 loopback 演示：鸿蒙(server) <-> iOS(client)。"""
    print(f"\n{'='*70}")
    print("  龍魂跨平台同步 · 端到端加密 loopback 演示")
    print(f"  DNA: {DNA}")
    print(f"{'='*70}\n")

    结果锁 = threading.Lock()
    演示结果: Dict[str, any] = {"server_received": None, "ok": False}
    端口 = args.port

    # 共享公钥数据的同步原语
    qrA_event = threading.Event()
    qrB_event = threading.Event()
    qrA_data: Dict[str, str] = {}
    qrB_data: Dict[str, str] = {}

    def 服务端():
        # 1. 密钥协商
        协商A = _静默实例化(密钥协商器.密钥协商器)
        公钥A = 协商A.生成密钥对()
        qrA_data["text"] = 协商A.公钥转二维码数据(公钥A)
        print(f"[鸿蒙服务端] ECDH 公钥指纹: {_指纹(公钥A)}")
        qrA_event.set()

        # 等待客户端公钥
        if not qrB_event.wait(timeout=10):
            raise TimeoutError("服务端等待客户端公钥超时")
        公钥B = 协商A.二维码数据转公钥(qrB_data["text"])
        共享A = 协商A.计算共享密钥(公钥B)
        会话A = 协商A.派生会话密钥(共享A)
        print(f"[鸿蒙服务端] 会话密钥指纹: {_指纹(会话A)}")

        # 2. 准备信封解密器
        信封A = _静默实例化(加密信封.加密信封, 加密信封.信封配置())
        信封A.设置会话密钥(会话A)

        # 3. 启动 TCP 服务
        传输A = _静默实例化(
            传输管理器.传输管理器,
            None, None,
            首选传输=传输管理器.传输类型.TCP_LAN,
            端口=端口,
        )
        print(f"[鸿蒙服务端] 在 0.0.0.0:{端口} 等待连接...")
        if not 传输A._作为服务端启动TCP():
            raise RuntimeError("服务端启动失败")
        传输A.状态 = 传输管理器.传输状态.已连接
        传输A.当前传输 = 传输管理器.传输类型.TCP_LAN
        print("[鸿蒙服务端] 客户端已连接")

        # 4. 接收并解密
        收到数据 = 传输A.接收(timeout=30)
        if not 收到数据:
            raise RuntimeError("服务端未收到数据")
        明文, 元数据 = 信封A.解密信封(收到数据)
        print(f"\n[鸿蒙服务端] 解密成功，来源: {元数据.get('源设备')}")
        print(f"[鸿蒙服务端] DNA: {元数据.get('DNA')}")
        print(f"[鸿蒙服务端] 版本向量: {元数据.get('版本向量')}")
        print(f"[鸿蒙服务端] 明文数据:\n{json.dumps(明文, ensure_ascii=False, indent=2)}")

        # 5. 简单冲突解决：把本地一条旧数据与收到的远程数据合并
        本地旧数据 = {"todo_list": ["买菜", "浇水"], "last_sync": 0}
        解决器 = _静默实例化(冲突解决器.冲突解决器, 冲突解决器.冲突策略.字段级合并)
        结果 = 解决器.解决(本地旧数据, 明文)
        print(f"\n[鸿蒙服务端] 冲突解决结果: {结果.类型.value}")
        print(json.dumps(结果.结果数据, ensure_ascii=False, indent=2))

        # 发送确认
        传输A.发送确认(True)
        传输A.断开()
        with 结果锁:
            演示结果["server_received"] = 明文
            演示结果["merged"] = 结果.结果数据
            演示结果["ok"] = True

    def 客户端():
        # 1. 等待服务端公钥
        if not qrA_event.wait(timeout=10):
            raise TimeoutError("客户端等待服务端公钥超时")

        # 2. 密钥协商
        协商B = _静默实例化(密钥协商器.密钥协商器)
        公钥B = 协商B.生成密钥对()
        qrB_data["text"] = 协商B.公钥转二维码数据(公钥B)
        print(f"[iOS客户端] ECDH 公钥指纹: {_指纹(公钥B)}")
        qrB_event.set()

        公钥A = 协商B.二维码数据转公钥(qrA_data["text"])
        共享B = 协商B.计算共享密钥(公钥A)
        会话B = 协商B.派生会话密钥(共享B)
        print(f"[iOS客户端] 会话密钥指纹: {_指纹(会话B)}")

        # 3. 准备信封
        信封B = _静默实例化(加密信封.加密信封, 加密信封.信封配置())
        信封B.设置会话密钥(会话B)

        # 4. 连接服务端（本地回环，模拟同 WiFi 局域网）
        # 传输管理器只用到对端 IP，构造一个最小对象
        class _FakeDevice:
            def __init__(self, ip):
                self.IP地址 = ip
        本机设备 = _FakeDevice("127.0.0.1")
        对端设备 = _FakeDevice("127.0.0.1")
        传输B = _静默实例化(
            传输管理器.传输管理器,
            本机设备, 对端设备,
            首选传输=传输管理器.传输类型.TCP_LAN,
            端口=端口,
        )
        print("[iOS客户端] 连接 127.0.0.1...")
        if not 传输B.连接():
            raise RuntimeError("客户端连接失败")

        # 5. 版本向量递增并构建加密信封
        时钟B = _静默实例化(版本向量时钟.版本向量时钟, "harmonyos", "ios")
        时钟B.递增("ios")
        版本向量 = 时钟B.获取向量()

        业务数据 = {
            "todo_list": ["买菜", "写代码", "运动"],
            "note": "这是 iOS 端创建的本地优先笔记，绝不出境。",
            "level": "internal",
        }
        信封数据 = 信封B.构建信封(
            数据=业务数据,
            源设备="ios|uid9622-iphone-001",
            目标设备="harmonyos|uid9622-harmony-001",
            版本向量=版本向量,
        )

        # 6. 发送
        字节数 = 传输B.发送(信封数据)
        print(f"[iOS客户端] 已发送加密信封: {字节数} bytes")

        # 7. 等待确认
        if 传输B.等待确认(timeout=30):
            print("[iOS客户端] 收到服务端确认 🟢")
        else:
            print("[iOS客户端] 未收到确认 🟡")
        传输B.断开()

    # 启动双线程
    t_server = threading.Thread(target=服务端, name="harmonyos-server", daemon=True)
    t_client = threading.Thread(target=客户端, name="ios-client", daemon=True)
    t_server.start()
    time.sleep(0.2)  # 让服务端先监听
    t_client.start()
    t_server.join(timeout=60)
    t_client.join(timeout=60)

    print(f"\n{'='*70}")
    if 演示结果["ok"]:
        print("  🟢 演示成功：端到端加密 + 本地直连 + 冲突解决 全部通过")
    else:
        print("  🔴 演示失败")
    print(f"{'='*70}\n")
    return 演示结果["ok"]


def main():
    parser = argparse.ArgumentParser(
        description="龍魂跨平台同步工作流",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--verbose", action="store_true", help="打印 DEBUG 级日志")
    sub = parser.add_subparsers(dest="command", required=True)

    p_disc = sub.add_parser("discover", help="mDNS 发现局域网龍魂节点")
    p_disc.add_argument("--timeout", type=float, default=5.0, help="发现等待秒数")

    p_adv = sub.add_parser("advertise", help="发布本机龍魂同步服务")
    p_adv.add_argument("--port", type=int, default=DEFAULT_PORT)
    p_adv.add_argument("--name", default=None, help="mDNS 服务名")
    p_adv.add_argument("--platform", default="macos", help="平台标识")
    p_adv.add_argument("--role", default="peer", help="角色: server/client/peer")
    p_adv.add_argument("--pubkey", default=None, help="ECDH 公钥文件路径（可选）")
    p_adv.add_argument("--timeout", type=float, default=60.0, help="保持发布秒数")

    p_qr = sub.add_parser("pair-qr", help="生成 ECDH 公钥二维码")
    p_qr.add_argument("--out", default=None, help="二维码图片保存路径")
    p_qr.add_argument("--text-out", default=None, help="二维码文本保存路径")

    p_scan = sub.add_parser("pair-scan", help="读取对端公钥并完成密钥协商")
    p_scan.add_argument("--input", "-i", required=True, help="对端公钥文件路径（或 - 表示标准输入）")
    p_scan.add_argument("--client-out", default=None, help="保存本机公钥供对端扫描")
    p_scan.add_argument("--key-out", default=None, help="保存会话密钥（Base64，注意保护）")

    p_demo = sub.add_parser("demo", help="单机 loopback 端到端加密同步演示")
    p_demo.add_argument("--port", type=int, default=DEFAULT_PORT)

    args = parser.parse_args()
    _配置日志(args.verbose)

    if args.command == "discover":
        cmd_discover(args)
    elif args.command == "advertise":
        cmd_advertise(args)
    elif args.command == "pair-qr":
        cmd_pair_qr(args)
    elif args.command == "pair-scan":
        cmd_pair_scan(args)
    elif args.command == "demo":
        ok = cmd_demo(args)
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

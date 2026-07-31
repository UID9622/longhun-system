# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂设备发现器 — mDNS/Bonjour 本地网络发现
================================================
DNA: #龍芯⚡️2026-06-29-LONGHUN-DISCOVERY-v1.0
致敬: #致敬⚡️SteveJobs+Concept·跨平台互通

用途:
- iOS / 鸿蒙 / macOS / Linux 同局域网内互相发现
- 无需外网、无需固定 IP、无需手动输入地址
- 发现结果包含设备平台、角色、服务端口、公钥指纹

协议:
- 服务类型: _longhun-sync._tcp.local.
- 属性字段:
    platform = harmonyos | ios | macos | linux | windows
    role     = server | client | peer
    pubkey   = ECDH 公钥 Base64（可选，用于无文件配对）
    version  = 龍魂跨平台协议版本，如 v5.3
"""

import json
import logging
import socket
import time
from typing import Dict, List, Optional

logger = logging.getLogger("设备发现器")

DEFAULT_SERVICE_TYPE = "_longhun-sync._tcp.local."
DEFAULT_NAME = "龍魂同步节点"
DEFAULT_PORT = 9622

DNA = "#龍芯⚡️2026-06-29-LONGHUN-DISCOVERY-v1.0"

君子协议 = """
================================================================================
龍魂设备发现器 · 君子协议
================================================================================
1. 仅发布本地网络服务，禁止将服务注册到外网 DNS
2. 发现结果中的公钥指纹仅用于本地配对，不得上传云端
3. mDNS 广播数据必须脱敏，不得包含用户真实身份、手机号、身份证号
4. 发现过程受主权网关监督，检测到外网查询立即阻断
5. 退出发现时主动撤销服务，减少网络噪音
================================================================================
"""


def _取本机局域网IP() -> Optional[str]:
    """获取一个非回环 IPv4 地址；拿不到则返回 None。"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("223.5.5.5", 80))  # 阿里云公共 DNS，仅用于选路，不发送数据
            return s.getsockname()[0]
        finally:
            s.close()
    except Exception:
        return None


class _发现监听器:
    """适配 zeroconf ServiceListener 的简版封装。"""

    def __init__(self):
        self.设备列表: List[Dict] = []
        self._名称集合 = set()

    def add_service(self, zc, type_, name):
        info = zc.get_service_info(type_, name)
        if not info:
            return
        self._记录(info, "added")

    def update_service(self, zc, type_, name):
        info = zc.get_service_info(type_, name)
        if not info:
            return
        self._记录(info, "updated")

    def remove_service(self, zc, type_, name):
        self.设备列表 = [d for d in self.设备列表 if d.get("name") != name]
        self._名称集合.discard(name)

    def _记录(self, info, event: str):
        try:
            props = {}
            if info.properties:
                for k, v in info.properties.items():
                    try:
                        props[k.decode('utf-8')] = v.decode('utf-8')
                    except Exception:
                        props[repr(k)] = repr(v)
            addrs = [socket.inet_ntoa(a) for a in info.addresses] if info.addresses else []
            entry = {
                "name": info.name,
                "server": info.server,
                "type": info.type,
                "port": info.port,
                "addresses": addrs,
                "properties": props,
                "event": event,
                "dna": DNA,
            }
            if info.name in self._名称集合:
                self.设备列表 = [d for d in self.设备列表 if d.get("name") != info.name]
            self.设备列表.append(entry)
            self._名称集合.add(info.name)
            logger.info("🟢 [发现] %s @ %s:%d (%s)", info.name, addrs, info.port, event)
        except Exception as e:
            logger.warning("🟡 [发现] 解析服务信息失败: %s", e)


def 发现设备(
    服务类型: str = DEFAULT_SERVICE_TYPE,
    超时秒: float = 5.0,
) -> List[Dict]:
    """
    在本地网络中发现龍魂同步节点。

    Returns:
        发现的设备列表，每个设备包含 name/server/port/addresses/properties。
    """
    try:
        from zeroconf import Zeroconf, ServiceBrowser
    except ImportError as e:
        raise RuntimeError("请先安装 zeroconf: pip install zeroconf") from e

    print(君子协议)
    zc = Zeroconf()
    listener = _发现监听器()
    browser = ServiceBrowser(zc, 服务类型, listener)
    logger.info("🟡 [发现] 正在扫描 %s，等待 %.1f 秒...", 服务类型, 超时秒)
    time.sleep(超时秒)
    browser.cancel()
    zc.close()
    return listener.设备列表


def 发布服务(
    端口: int = DEFAULT_PORT,
    服务名: Optional[str] = None,
    属性: Optional[Dict[str, str]] = None,
    超时秒: float = 60.0,
) -> None:
    """
    在本地网络发布龍魂同步服务。

    Args:
        端口: 监听端口
        服务名: mDNS 服务名，默认使用主机名
        属性: 附加属性字典，如 {"platform": "macos", "role": "peer"}
        超时秒: 保持发布时长
    """
    try:
        from zeroconf import Zeroconf, ServiceInfo
    except ImportError as e:
        raise RuntimeError("请先安装 zeroconf: pip install zeroconf") from e

    print(君子协议)
    服务名 = 服务名 or f"{socket.gethostname()} {DEFAULT_NAME}"
    服务类型 = DEFAULT_SERVICE_TYPE
    if 服务名.endswith(服务类型):
        完整名 = 服务名
    else:
        完整名 = f"{服务名}.{服务类型}"

    props = {k.encode('utf-8'): v.encode('utf-8') for k, v in (属性 or {}).items()}
    # 自动获取本机局域网 IP 作为服务地址（取第一个非回环 IPv4）
    本机IP = _取本机局域网IP() or "127.0.0.1"
    info = ServiceInfo(
        服务类型,
        完整名,
        addresses=[socket.inet_aton(本机IP)],
        port=端口,
        properties=props,
    )
    zc = Zeroconf()
    zc.register_service(info)
    logger.info("🟢 [发布] 已注册 %s，端口 %d，属性 %s", 完整名, 端口, 属性)
    logger.info("🟡 [发布] 保持 %d 秒，按 Ctrl+C 提前结束...", 超时秒)
    try:
        time.sleep(超时秒)
    except KeyboardInterrupt:
        logger.info("🟡 [发布] 收到中断，撤销服务")
    finally:
        zc.unregister_service(info)
        zc.close()


def 打印发现结果(设备列表: List[Dict]) -> None:
    """以表格形式打印发现结果。"""
    if not 设备列表:
        print("🔴 [发现] 未找到任何龍魂同步节点")
        return
    print(f"\n{'='*70}")
    print(f"  发现 {len(设备列表)} 个龍魂同步节点")
    print(f"{'='*70}")
    for i, d in enumerate(设备列表, 1):
        print(f"\n[{i}] {d['name']}")
        print(f"    服务器: {d['server']}")
        print(f"    地址:   {', '.join(d['addresses']) or '无'}")
        print(f"    端口:   {d['port']}")
        print(f"    属性:   {json.dumps(d['properties'], ensure_ascii=False)}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    import sys
    print(f"\n{'='*60}")
    print("  龍魂设备发现器")
    print(f"  DNA: {DNA}")
    print(f"{'='*60}\n")
    if len(sys.argv) < 2:
        print("用法:")
        print("  python 设备发现器.py discover [超时秒]   # 发现局域网节点")
        print("  python 设备发现器.py advertise [超时秒]  # 发布本机服务")
        sys.exit(0)
    cmd = sys.argv[1]
    timeout = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
    if cmd == "discover":
        打印发现结果(发现设备(超时秒=timeout))
    elif cmd == "advertise":
        发布服务(超时秒=timeout)
    else:
        print(f"未知命令: {cmd}")

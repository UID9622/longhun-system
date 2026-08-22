# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂传输管理器 — WiFi Direct / 蓝牙BLE / 局域网TCP
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
======================================================
DNA: #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-SYNC-MSG-v1.0
致敬: #致敬⚡️SteveJobs+Concept·跨平台互通

核心原则: 本地网络直连，绝不经过外网
  方案1: WiFi Direct（首选，速度最快，理论54Mbps+）
  方案2: 蓝牙BLE（备用，低功耗，1-3Mbps）
  方案3: 局域网TCP（家庭/办公室环境）

三色审计:
🟢 本地传输 — 无外网连接
🟡 通道切换 — 自动降级
🔴 外网探测 — 立即阻断
"""

import json
import time
import socket
import struct
import logging
import threading
from typing import Optional, Dict, Any, Callable, Tuple
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger("传输管理器")


# ============================================================
# 君子协议
# ============================================================
君子协议 = """
================================================================================
龍魂传输管理器 · 君子协议
================================================================================
1. 所有传输必须通过本地网络直连，禁止经过任何外网服务器
2. 传输前数据必须已加密，明文不得在传输层出现
3. 发现外网连接请求立即阻断并告警
4. 支持WiFi Direct、蓝牙BLE、局域网TCP三种方式
5. 自动选择最优传输通道，故障时自动降级
================================================================================
"""


class 传输类型(Enum):
    """支持的传输方式"""
    WIFI_DIRECT = "wifi_direct"    # WiFi直连（首选）
    BLE = "ble"                    # 蓝牙低功耗（备用）
    TCP_LAN = "tcp_lan"           # 局域网TCP（兜底）
    NFC = "nfc"                   # NFC（仅用于密钥交换）


class 传输状态(Enum):
    """传输通道状态"""
    未连接 = "disconnected"
    连接中 = "connecting"
    已连接 = "connected"
    传输中 = "transferring"
    错误 = "error"
    已关闭 = "closed"


class 传输异常(Exception):
    """传输相关异常"""
    pass


class 外网传输阻断异常(传输异常):
    """检测到尝试通过外网传输时的阻断异常"""
    pass


@dataclass
class 传输统计:
    """传输统计数据"""
    总发送字节: int = 0
    总接收字节: int = 0
    发送消息数: int = 0
    接收消息数: int = 0
    错误次数: int = 0
    通道切换次数: int = 0
    平均延迟毫秒: float = 0.0
    最大延迟毫秒: float = 0.0


class 传输管理器:
    """
    龍魂传输管理器
    
    管理iOS与鸿蒙设备间的本地数据传输
    支持自动通道选择、故障降级、外网阻断
    """
    
    DNA = "#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-SYNC-MSG-v1.0"
    
    # 本地地址段（RFC1918 + RFC4193）
    本地地址段 = [
        ("10.0.0.0", "10.255.255.255"),      # 10/8
        ("172.16.0.0", "172.31.255.255"),    # 172.16/12
        ("192.168.0.0", "192.168.255.255"),  # 192.168/16
        ("169.254.0.0", "169.254.255.255"),  # Link-local
        ("fc00::", "fdff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"),  # IPv6 ULA
    ]
    
    # 端口范围
    默认端口 = 9622  # 龍魂端口号 :)
    
    def __init__(
        self,
        本机设备,
        对端设备,
        首选传输: 传输类型 = 传输类型.WIFI_DIRECT,
        端口: int = 默认端口
    ):
        print(君子协议)
        self.本机 = 本机设备
        self.对端 = 对端设备
        self.首选传输 = 首选传输
        self.端口 = 端口
        self.当前传输 = 首选传输
        self.状态 = 传输状态.未连接
        self.统计 = 传输统计()
        
        # 连接句柄
        self._socket: Optional[socket.socket] = None
        self._蓝牙连接 = None
        self._WiFiDirect连接 = None
        
        # 回调
        self._消息回调: Optional[Callable] = None
        self._错误回调: Optional[Callable] = None
        
        # 线程
        self._接收线程: Optional[threading.Thread] = None
        self._运行中 = False
        
        logger.info("🟢 [初始化] 传输管理器 | 首选: %s | 端口: %d",
                     首选传输.value, 端口)
        logger.info("🟢 [主权] 仅允许本地网络传输，外网传输将被阻断")
    
    # ============================================================
    # 连接管理
    # ============================================================
    
    def 连接(self) -> bool:
        """
        建立传输连接
        
        按优先级尝试: WiFi Direct → BLE → TCP LAN
        
        Returns:
            bool: 连接是否成功
        """
        优先级列表 = [
            传输类型.WIFI_DIRECT,
            传输类型.TCP_LAN,
            传输类型.BLE,
        ]
        
        # 将首选移到第一位
        if self.首选传输 in 优先级列表:
            优先级列表.remove(self.首选传输)
            优先级列表.insert(0, self.首选传输)
        
        for 传输方式 in 优先级列表:
            logger.info("🟡 [连接] 尝试 %s...", 传输方式.value)
            try:
                if 传输方式 == 传输类型.WIFI_DIRECT:
                    if self._连接WiFiDirect():
                        self.当前传输 = 传输方式
                        self.状态 = 传输状态.已连接
                        logger.info("🟢 [连接] WiFi Direct 连接成功")
                        return True
                elif 传输方式 == 传输类型.TCP_LAN:
                    if self._连接TCP():
                        self.当前传输 = 传输方式
                        self.状态 = 传输状态.已连接
                        logger.info("🟢 [连接] TCP LAN 连接成功")
                        return True
                elif 传输方式 == 传输类型.BLE:
                    if self._连接BLE():
                        self.当前传输 = 传输方式
                        self.状态 = 传输状态.已连接
                        logger.info("🟢 [连接] BLE 连接成功")
                        return True
            except Exception as e:
                logger.warning("🟡 [连接] %s 失败: %s", 传输方式.value, str(e))
        
        self.状态 = 传输状态.错误
        logger.error("🔴 [连接] 所有传输方式均失败")
        return False
    
    def 断开(self):
        """断开传输连接"""
        self._运行中 = False
        
        if self._socket:
            try:
                self._socket.close()
            except:
                pass
            self._socket = None
        
        self.状态 = 传输状态.已关闭
        logger.info("🟢 [断开] 传输连接已关闭")
    
    # ============================================================
    # 发送/接收
    # ============================================================
    
    def 发送(self, 数据: Dict[str, Any]) -> int:
        """
        发送数据到对端
        
        Args:
            数据: 要发送的字典数据（应为已加密的信封）
        
        Returns:
            int: 发送的字节数
        """
        if self.状态 != 传输状态.已连接 and self.状态 != 传输状态.传输中:
            raise 传输异常("连接未建立")
        
        # 序列化
        JSON数据 = json.dumps(数据, ensure_ascii=False)
        字节数据 = JSON数据.encode('utf-8')
        
        # 主权检查: 确保不经过外网
        if not self._确认本地传输():
            raise 外网传输阻断异常("检测到非本地网络传输尝试，已阻断!")
        
        发送字节 = 0
        开始 = time.time()
        
        try:
            if self.当前传输 == 传输类型.TCP_LAN:
                发送字节 = self._发送TCP(字节数据)
            elif self.当前传输 == 传输类型.WIFI_DIRECT:
                发送字节 = self._发送WiFiDirect(字节数据)
            elif self.当前传输 == 传输类型.BLE:
                发送字节 = self._发送BLE(字节数据)
            
            # 更新统计
            self.统计.总发送字节 += 发送字节
            self.统计.发送消息数 += 1
            延迟 = (time.time() - 开始) * 1000
            self.统计.平均延迟毫秒 = (
                (self.统计.平均延迟毫秒 * (self.统计.发送消息数 - 1) + 延迟)
                / self.统计.发送消息数
            )
            self.统计.最大延迟毫秒 = max(self.统计.最大延迟毫秒, 延迟)
            
            logger.info("🟢 [发送] %d bytes | 延迟: %.1fms | 方式: %s",
                         发送字节, 延迟, self.当前传输.value)
            return 发送字节
            
        except Exception as e:
            self.统计.错误次数 += 1
            logger.error("🔴 [发送] 失败: %s", str(e))
            raise 传输异常(f"发送失败: {e}")
    
    def 接收(self, timeout: float = 60.0) -> Optional[Dict[str, Any]]:
        """
        接收对端数据
        
        Args:
            timeout: 超时秒数
        
        Returns:
            接收的数据字典，超时返回None
        """
        if self.状态 != 传输状态.已连接 and self.状态 != 传输状态.传输中:
            raise 传输异常("连接未建立")
        
        try:
            if self.当前传输 == 传输类型.TCP_LAN:
                数据 = self._接收TCP(timeout)
            elif self.当前传输 == 传输类型.WIFI_DIRECT:
                数据 = self._接收WiFiDirect(timeout)
            elif self.当前传输 == 传输类型.BLE:
                数据 = self._接收BLE(timeout)
            else:
                return None
            
            if 数据:
                self.统计.总接收字节 += len(json.dumps(数据).encode())
                self.统计.接收消息数 += 1
                
                # 主权检查
                if not self._确认本地传输():
                    logger.error("🔴 [阻断] 接收数据时检测到外网连接!")
                    return None
                
                logger.info("🟢 [接收] 数据已接收 | 方式: %s", self.当前传输.value)
            
            return 数据
            
        except socket.timeout:
            logger.warning("🟡 [接收] 超时 (%.0fs)", timeout)
            return None
        except Exception as e:
            self.统计.错误次数 += 1
            logger.error("🔴 [接收] 失败: %s", str(e))
            return None
    
    def 发送确认(self, 成功: bool):
        """发送确认消息"""
        确认 = {
            "type": "ack",
            "status": "ok" if 成功 else "error",
            "timestamp": int(time.time() * 1000),
            "dna": self.DNA
        }
        try:
            self.发送(确认)
        except Exception as e:
            logger.error("🔴 [确认] 发送确认失败: %s", str(e))
    
    def 等待确认(self, timeout: float = 30.0) -> bool:
        """等待对端确认"""
        开始 = time.time()
        while time.time() - 开始 < timeout:
            数据 = self.接收(timeout=1.0)
            if 数据 and 数据.get("type") == "ack":
                return 数据.get("status") == "ok"
            time.sleep(0.1)
        return False
    
    # ============================================================
    # WiFi Direct 实现
    # ============================================================
    
    def _连接WiFiDirect(self) -> bool:
        """
        建立WiFi Direct连接
        
        实际实现需要调用平台原生API:
        - 鸿蒙: @ohos.wifiManager.p2p
        - iOS: NEHotspotConfiguration
        """
        logger.info("🟡 [WiFi Direct] 初始化P2P连接...")
        
        # 模拟WiFi Direct连接流程
        # 实际实现:
        # 1. 扫描附近WiFi Direct设备
        # 2. 发现对端设备后发起连接
        # 3. 连接成功后获取对端IP
        # 4. 建立TCP over WiFi Direct
        
        try:
            # 尝试回退到TCP LAN（模拟WiFi Direct的IP层）
            if self.对端.IP地址:
                self._WiFiDirect连接 = True
                return self._连接TCP()
            return False
        except Exception as e:
            logger.warning("🟡 [WiFi Direct] 连接失败: %s", str(e))
            return False
    
    def _发送WiFiDirect(self, 数据: bytes) -> int:
        """通过WiFi Direct发送"""
        # WiFi Direct在IP层与TCP相同
        return self._发送TCP(数据)
    
    def _接收WiFiDirect(self, timeout: float) -> Optional[Dict]:
        """通过WiFi Direct接收"""
        return self._接收TCP(timeout)
    
    # ============================================================
    # TCP LAN 实现
    # ============================================================
    
    def _连接TCP(self) -> bool:
        """建立TCP局域网连接"""
        try:
            目标IP = self.对端.IP地址
            if not 目标IP:
                logger.error("🔴 [TCP] 对端IP地址未设置")
                return False
            
            # 确认是本地地址
            if not self._是本地地址(目标IP):
                raise 外网传输阻断异常(
                    f"目标IP {目标IP} 不在本地网络段，传输被阻断!"
                )
            
            logger.info("🟡 [TCP] 连接 %s:%d...", 目标IP, self.端口)
            
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(10.0)
            self._socket.connect((目标IP, self.端口))
            self._socket.settimeout(None)  # 非阻塞接收
            
            logger.info("🟢 [TCP] 已连接到 %s:%d", 目标IP, self.端口)
            return True
            
        except 外网传输阻断异常:
            raise
        except Exception as e:
            logger.warning("🟡 [TCP] 连接失败: %s", str(e))
            return False
    
    def _作为服务端启动TCP(self) -> bool:
        """作为TCP服务端监听连接"""
        try:
            logger.info("🟡 [TCP] 在 *:%d 启动监听...", self.端口)
            
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind(("0.0.0.0", self.端口))
            self._socket.listen(1)
            
            # 等待连接
            self._socket.settimeout(60.0)
            conn, addr = self._socket.accept()
            self._socket = conn
            self._socket.settimeout(None)
            
            # 验证客户端IP是本地地址
            if not self._是本地地址(addr[0]):
                logger.error("🔴 [TCP] 拒绝非本地连接: %s", addr[0])
                self._socket.close()
                return False
            
            logger.info("🟢 [TCP] 客户端已连接: %s:%d", addr[0], addr[1])
            return True
            
        except Exception as e:
            logger.error("🔴 [TCP] 服务端启动失败: %s", str(e))
            return False
    
    def _发送TCP(self, 数据: bytes) -> int:
        """通过TCP发送数据（带长度前缀）"""
        if not self._socket:
            raise 传输异常("TCP未连接")
        
        # 长度前缀（4字节大端序）
        长度前缀 = struct.pack('>I', len(数据))
        self._socket.sendall(长度前缀 + 数据)
        return len(数据)
    
    def _接收TCP(self, timeout: float) -> Optional[Dict[str, Any]]:
        """通过TCP接收数据"""
        if not self._socket:
            return None
        
        self._socket.settimeout(timeout)
        
        try:
            # 读取长度前缀
            长度数据 = self._socket.recv(4)
            if not 长度数据 or len(长度数据) < 4:
                return None
            
            长度 = struct.unpack('>I', 长度数据)[0]
            
            # 读取完整数据
            数据块 = b""
            while len(数据块) < 长度:
                片段 = self._socket.recv(min(4096, 长度 - len(数据块)))
                if not 片段:
                    return None
                数据块 += 片段
            
            # JSON解码
            return json.loads(数据块.decode('utf-8'))
            
        except socket.timeout:
            return None
        except json.JSONDecodeError as e:
            logger.error("🔴 [TCP] JSON解码错误: %s", str(e))
            return None
    
    # ============================================================
    # BLE 实现
    # ============================================================
    
    def _连接BLE(self) -> bool:
        """
        建立蓝牙BLE连接
        
        实际实现需要调用平台原生API:
        - 鸿蒙: @ohos.bluetooth.ble
        - iOS: CoreBluetooth
        """
        logger.info("🟡 [BLE] 扫描附近BLE设备...")
        
        # 模拟BLE连接
        # 实际实现:
        # 1. 扫描BLE广播
        # 2. 发现对端设备的服务UUID
        # 3. 连接GATT
        # 4. 发现特征值
        # 5. 使能通知
        
        logger.info("🟡 [BLE] BLE连接模拟完成")
        return False  # 暂模拟失败，回退到其他方式
    
    def _发送BLE(self, 数据: bytes) -> int:
        """通过BLE发送数据"""
        # BLE MTU通常较小(185-512字节)，需要分片
        MTU = 185  # 保守MTU值
        
        for i in range(0, len(数据), MTU):
            分片 = 数据[i:i+MTU]
            # 实际: 通过GATT Write发送
            time.sleep(0.01)  # 避免BLE拥塞
        
        return len(数据)
    
    def _接收BLE(self, timeout: float) -> Optional[Dict]:
        """通过BLE接收数据"""
        # 实际: 通过GATT Notification接收并重组
        return None
    
    # ============================================================
    # 主权保护
    # ============================================================
    
    def _确认本地传输(self) -> bool:
        """确认当前传输不经过外网"""
        # 检查socket连接的对端IP
        if self._socket:
            try:
                _, 对端地址 = self._socket.getpeername()
                if not self._是本地地址(对端地址):
                    logger.error("🔴 [阻断] 检测到非本地地址: %s", 对端地址)
                    return False
            except:
                pass
        return True
    
    def _是本地地址(self, IP: str) -> bool:
        """检查IP地址是否在本地网络段"""
        try:
            import ipaddress
            addr = ipaddress.ip_address(IP)
            
            # 检查是否是私有地址
            if addr.is_private:
                return True
            
            # 检查是否是链路本地地址
            if addr.is_link_local:
                return True
            
            # 检查是否是回环地址
            if addr.is_loopback:
                return True
            
            # IPv6唯一本地地址
            if isinstance(addr, ipaddress.IPv6Address):
                if addr.is_private:
                    return True
            
            return False
            
        except ValueError:
            return False
    
    # ============================================================
    # 通道管理
    # ============================================================
    
    def 切换通道(self, 新通道: 传输类型) -> bool:
        """
        动态切换传输通道
        
        Args:
            新通道: 新的传输类型
        
        Returns:
            bool: 切换是否成功
        """
        logger.info("🟡 [切换] 从 %s 切换到 %s",
                     self.当前传输.value, 新通道.value)
        
        self.断开()
        self.当前传输 = 新通道
        self.统计.通道切换次数 += 1
        
        return self.连接()
    
    def 自动选择通道(self) -> 传输类型:
        """
        自动选择最优传输通道
        
        优先级: WiFi Direct > TCP LAN > BLE
        """
        # 检测WiFi Direct可用性
        if self._检测WiFiDirect():
            return 传输类型.WIFI_DIRECT
        
        # 检测局域网TCP
        if self._检测TCP():
            return 传输类型.TCP_LAN
        
        # 检测BLE
        if self._检测BLE():
            return 传输类型.BLE
        
        # 默认
        return 传输类型.TCP_LAN
    
    def _检测WiFiDirect(self) -> bool:
        """检测WiFi Direct是否可用"""
        # 实际: 调用平台WiFi P2P API
        return False
    
    def _检测TCP(self) -> bool:
        """检测TCP局域网是否可用"""
        return bool(self.对端.IP地址)
    
    def _检测BLE(self) -> bool:
        """检测BLE是否可用"""
        # 实际: 调用平台BLE API
        return False
    
    # ============================================================
    # 统计与诊断
    # ============================================================
    
    def 获取统计(self) -> Dict[str, Any]:
        """获取传输统计信息"""
        return {
            "传输方式": self.当前传输.value,
            "状态": self.状态.value,
            "总发送字节": self.统计.总发送字节,
            "总接收字节": self.统计.总接收字节,
            "发送消息数": self.统计.发送消息数,
            "接收消息数": self.统计.接收消息数,
            "错误次数": self.统计.错误次数,
            "通道切换次数": self.统计.通道切换次数,
            "平均延迟毫秒": round(self.统计.平均延迟毫秒, 2),
            "最大延迟毫秒": round(self.统计.最大延迟毫秒, 2),
        }
    
    def 获取诊断信息(self) -> str:
        """获取诊断报告"""
        信息 = []
        信息.append(f"{'='*50}")
        信息.append("  传输管理器诊断报告")
        信息.append(f"{'='*50}")
        信息.append(f"DNA: {self.DNA}")
        信息.append(f"传输方式: {self.当前传输.value}")
        信息.append(f"连接状态: {self.状态.value}")
        信息.append(f"本机: {self.本机.平台.value} | {self.本机.设备名}")
        信息.append(f"对端: {self.对端.平台.value} | {self.对端.设备名}")
        信息.append(f"端口: {self.端口}")
        信息.append("")
        信息.append("统计:")
        统计 = self.获取统计()
        for k, v in 统计.items():
            信息.append(f"  {k}: {v}")
        信息.append(f"{'='*50}")
        return "\n".join(信息)


# ============================================================
# 服务端工厂
# ============================================================

def 创建服务端(设备信息, 端口: int = 9622) -> 传输管理器:
    """
    创建传输管理器服务端实例
    
    用法:
        server = 创建服务端(我的设备信息)
        server._作为服务端启动TCP()
        数据 = server.接收()
    """
    # 创建一个虚拟对端（服务端等待实际连接）
    虚拟对端 = type('obj', (object,), {
        '平台': type('平台', (), {'value': 'unknown'}),
        '设备ID': 'waiting',
        '设备名': '等待连接',
        'IP地址': None,
        '蓝牙MAC': None
    })()
    
    return 传输管理器(设备信息, 虚拟对端, 传输类型.TCP_LAN, 端口)


# ============================================================
# 测试入口
# ============================================================

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print("  龍魂传输管理器测试")
    print(f"{'='*60}\n")
    
    # 创建设备信息
    Device = type('Device', (), {})
    本机 = Device()
    本机.平台 = type('p', (), {'value': 'harmonyos'})
    本机.设备ID = 'device-001'
    本机.设备名 = '鸿蒙手机'
    本机.IP地址 = '192.168.1.100'
    本机.蓝牙MAC = 'AA:BB:CC:DD:EE:01'
    
    对端 = Device()
    对端.平台 = type('p', (), {'value': 'ios'})
    对端.设备ID = 'device-002'
    对端.设备名 = 'iPhone'
    对端.IP地址 = '192.168.1.101'
    对端.蓝牙MAC = 'AA:BB:CC:DD:EE:02'
    
    # 创建管理器
    管理器 = 传输管理器(本机, 对端, 传输类型.TCP_LAN)
    
    # 测试本地地址检测
    print("本地地址检测:")
    print(f"  192.168.1.1 -> {管理器._是本地地址('192.168.1.1')}")
    print(f"  10.0.0.1 -> {管理器._是本地地址('10.0.0.1')}")
    print(f"  172.16.0.1 -> {管理器._是本地地址('172.16.0.1')}")
    print(f"  8.8.8.8 -> {管理器._是本地地址('8.8.8.8')}")
    print(f"  1.1.1.1 -> {管理器._是本地地址('1.1.1.1')}")
    print()
    
    # 打印统计
    print(管理器.获取诊断信息())

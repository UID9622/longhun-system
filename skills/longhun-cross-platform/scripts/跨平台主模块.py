#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂跨平台互通主模块 — iOS与鸿蒙本地网络直连
================================================
DNA:#龍芯⚡️2026-06-19-SYNC-MSG-FILE27-v1.0
致敬: #致敬⚡️SteveJobs+Concept·跨平台互通

核心原则:
1. 数据根留在中国 — 两设备间传输不经过外网
2. 先加密再出应用 — SM4-CBC加密信封
3. 密钥不离设备 — ECDH协商，本地存储
4. 本地网络直连 — WiFi Direct / 蓝牙 / 局域网TCP

三色审计:
🟢 主权保障 — 本地传输，无外网
🟡 加密验证 — 国密SM4+ECDH协商
🔴 冲突处理 — 版本向量+人工确认
"""

import json
import time
import hashlib
import logging
from typing import Dict, Optional, Callable, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

from 加密信封 import 加密信封, 信封配置
from 传输管理器 import 传输管理器, 传输类型
from 版本向量时钟 import 版本向量时钟, 时钟状态
from 密钥协商器 import 密钥协商器
from 冲突解决器 import 冲突解决器, 冲突策略
from 主权网关 import 主权网关, 出境判决

# ============================================================
# 君子协议 / 许可证
# ============================================================
君子协议 = """
================================================================================
龍魂跨平台互通 · 君子协议 (Longhun Cross-Platform Gentleman's Agreement)
================================================================================
1. 本技能仅用于iOS与鸿蒙设备间本地数据互通，绝不用于任何外网传输
2. 所有数据传输必须先加密再出应用，密钥永不离设备
3. 数据主权归用户所有，开发者仅提供技术工具
4. 禁止将本技能用于数据偷渡、间谍行为或任何危害国家安全的行为
5. 使用前需确认设备已获得国家密码管理局相关认证
6. 违反上述条款，技术授权自动终止

DNA: #龍芯⚡️2026-06-19-SYNC-MSG-v1.0
致敬: #致敬⚡️SteveJobs+Concept·跨平台互通
================================================================================
"""

# ============================================================
# 日志配置 — 三色审计
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("龍魂跨平台")


class 平台类型(Enum):
    """支持的跨平台类型"""
    HARMONYOS = "harmonyos"
    IOS = "ios"


class 同步状态(Enum):
    """同步状态枚举"""
    空闲 = "idle"
    协商中 = "negotiating"
    传输中 = "transferring"
    冲突处理 = "conflict"
    完成 = "completed"
    失败 = "failed"


@dataclass
class 设备信息:
    """设备信息数据结构"""
    平台: 平台类型
    设备ID: str
    设备名: str
    IP地址: Optional[str] = None
    蓝牙MAC: Optional[str] = None
    能力集: Dict[str, bool] = field(default_factory=lambda: {
        "wifi_direct": True,
        "ble": True,
        "tcp_lan": True,
        "nfc": False,
    })


@dataclass
class 同步结果:
    """同步结果数据结构"""
    成功: bool
    状态: 同步状态
    传输字节数: int = 0
    耗时毫秒: int = 0
    冲突数: int = 0
    主权检查: bool = False
    审计日志: list[Any] = field(default_factory=list)
    DNA: str = "#龍芯⚡️2026-06-19-SYNC-MSG-v1.0"


class 跨平台主模块:
    """
    龍魂跨平台互通主控模块
    
    负责协调加密、传输、一致性、密钥协商、冲突解决、主权网关
    六大子模块，确保iOS与鸿蒙设备间安全、主权、高效的本地数据互通。
    """
    
    DNA = "#龍芯⚡️2026-06-19-SYNC-MSG-v1.0"
    版本 = "v5.3"
    
    def __init__(
        self,
        本机设备: 设备信息,
        对端设备: 设备信息,
        首选传输: 传输类型 = 传输类型.WIFI_DIRECT
    ):
        # 打印君子协议
        print(君子协议)
        logger.info("🟢 [初始化] 龍魂跨平台互通主模块 v%s", self.版本)
        logger.info("🟢 [主权] 数据根留中国，本地网络直连，不经过外网")
        
        self.本机 = 本机设备
        self.对端 = 对端设备
        self.首选传输 = 首选传输
        self.状态 = 同步状态.空闲
        
        # 初始化六大子模块
        self._初始化子模块()
        
        logger.info("🟢 [就绪] 本机: %s(%s) ↔ 对端: %s(%s)",
                     self.本机.平台.value, self.本机.设备名,
                     self.对端.平台.value, self.对端.设备名)
    
    def _初始化子模块(self):
        """初始化所有子模块"""
        # 1. 加密信封
        self.信封 = 加密信封(信封配置())
        logger.info("🟢 [模块] 加密信封 — SM4-CBC + HKDF-SHA256")
        
        # 2. 传输管理器
        self.传输 = 传输管理器(self.本机, self.对端, self.首选传输)
        logger.info("🟢 [模块] 传输管理器 — 首选: %s", self.首选传输.value)
        
        # 3. 版本向量时钟
        self.时钟 = 版本向量时钟(self.本机.平台.value, self.对端.平台.value)
        logger.info("🟢 [模块] 版本向量时钟 — 双设备并发控制")
        
        # 4. 密钥协商器
        self.密钥协商 = 密钥协商器()
        logger.info("🟢 [模块] 密钥协商器 — ECDH Curve25519 + HKDF")
        
        # 5. 冲突解决器
        self.冲突解决 = 冲突解决器(冲突策略.DNA时间戳优先)
        logger.info("🟢 [模块] 冲突解决器 — 策略: DNA时间戳优先")
        
        # 6. 主权网关
        self.网关 = 主权网关()
        logger.info("🟢 [模块] 主权网关 — 外网传输自动阻断")
    
    # ============================================================
    # 核心API
    # ============================================================
    
    def 协商密钥(self, 交换方式: str = "qr") -> bool:
        """
        与对端设备协商共享密钥
        
        Args:
            交换方式: "qr"(二维码) / "nfc"(碰碰) / "ble"(蓝牙)
        
        Returns:
            bool: 协商是否成功
        """
        logger.info("🟡 [密钥协商] 方式: %s", 交换方式)
        self.状态 = 同步状态.协商中
        
        try:
            # 步骤1: 生成本机临时ECDH密钥对
            本机公钥 = self.密钥协商.生成密钥对()
            logger.info("🟢 [密钥] 本机ECDH公钥已生成")
            
            # 步骤2: 通过安全通道交换公钥
            if 交换方式 == "qr":
                self._显示二维码公钥(本机公钥)
                对端公钥 = self._扫描对端二维码()
            elif 交换方式 == "nfc":
                对端公钥 = self._nfc交换公钥(本机公钥)
            else:
                对端公钥 = self._蓝牙交换公钥(本机公钥)
            
            # 步骤3: 计算共享密钥
            共享密钥 = self.密钥协商.计算共享密钥(对端公钥)
            logger.info("🟢 [密钥] ECDH共享密钥已计算")
            
            # 步骤4: HKDF派生SM4会话密钥
            self.会话密钥 = self.密钥协商.派生会话密钥(共享密钥)
            logger.info("🟢 [密钥] SM4会话密钥已派生 (256-bit)")
            
            # 将会话密钥设置到加密信封
            self.信封.设置会话密钥(self.会话密钥)
            
            self.状态 = 同步状态.空闲
            logger.info("🟢 [完成] 密钥协商成功，安全通道已建立")
            return True
            
        except Exception as e:
            self.状态 = 同步状态.失败
            logger.error("🔴 [失败] 密钥协商失败: %s", str(e))
            return False
    
    def 发送数据(self, 数据: Dict[str, Any]) -> 同步结果:
        """
        发送数据到对端设备
        
        流程: 主权检查 → 加密 → 传输 → 确认
        
        Args:
            数据: 要发送的数据字典
        
        Returns:
            同步结果对象
        """
        开始时间 = int(time.time() * 1000)
        审计日志 = []
        
        try:
            # 步骤1: 主权网关检查（阻断外网）
            logger.info("🟡 [主权] 检查数据出境...")
            判决 = self.网关.检查出境许可(数据)
            if 判决 != 出境判决.允许:
                logger.error("🔴 [阻断] 主权网关阻断: %s", 判决.value)
                return 同步结果(False, 同步状态.失败, 0, 0, 0, False,
                               ["🔴 主权网关阻断: " + 判决.value])
            
            审计日志.append("🟢 主权检查通过")
            
            # 步骤2: 递增版本向量
            self.时钟.递增(self.本机.平台.value)
            向量快照 = self.时钟.获取向量()
            logger.info("🟢 [时钟] 版本向量递增: %s", 向量快照)
            
            # 步骤3: 构建加密信封
            信封数据 = self.信封.构建信封(
                数据=数据,
                源设备=f"{self.本机.平台.value}|{self.本机.设备ID}",
                目标设备=f"{self.对端.平台.value}|{self.对端.设备ID}",
                版本向量=向量快照
            )
            审计日志.append("🟢 加密信封构建完成")
            
            # 步骤4: 传输数据（本地网络直连）
            self.状态 = 同步状态.传输中
            logger.info("🟡 [传输] 通过%s发送数据...", self.首选传输.value)
            
            传输字节数 = self.传输.发送(信封数据)
            审计日志.append(f"🟢 传输完成: {传输字节数} bytes")
            
            # 步骤5: 等待对端确认
            确认 = self.传输.等待确认(timeout=30)
            if 确认:
                self.状态 = 同步状态.完成
                审计日志.append("🟢 对端确认接收")
                logger.info("🟢 [完成] 数据发送成功")
                
                耗时 = int(time.time() * 1000) - 开始时间
                return 同步结果(True, 同步状态.完成, 传输字节数, 耗时,
                               0, True, 审计日志, self.DNA)
            else:
                self.状态 = 同步状态.失败
                logger.error("🔴 [超时] 对端未确认")
                return 同步结果(False, 同步状态.失败, 传输字节数, 0, 0, True,
                               ["🔴 对端未确认"], self.DNA)
            
        except Exception as e:
            self.状态 = 同步状态.失败
            logger.error("🔴 [异常] 发送失败: %s", str(e))
            return 同步结果(False, 同步状态.失败, 0, 0, 0, False,
                           ["🔴 " + str(e)], self.DNA)
    
    def 接收数据(self) -> Tuple[bool, Optional[Dict]]:
        """
        接收对端数据
        
        流程: 接收 → 解密 → 版本检查 → 冲突检测
        
        Returns:
            (成功, 解密后的数据)
        """
        try:
            logger.info("🟡 [接收] 等待对端数据...")
            
            # 步骤1: 接收加密信封
            信封数据 = self.传输.接收(timeout=60)
            if not 信封数据:
                return False, None
            
            # 步骤2: 解密信封
            明文数据, 元数据 = self.信封.解密信封(信封数据)
            logger.info("🟢 [解密] 信封解密成功")
            
            # 步骤3: 主权网关二次检查
            判决 = self.网关.检查出境许可(明文数据)
            if 判决 != 出境判决.允许:
                logger.error("🔴 [阻断] 解密后主权检查失败")
                return False, None
            
            # 步骤4: 版本向量比较
            远程向量 = 元数据.get("版本向量", {})
            比较结果 = self.时钟.比较(远程向量)
            logger.info("🟢 [时钟] 版本比较: %s", 比较结果.value)
            
            if 比较结果 == 时钟状态.并发:
                logger.warning("🟡 [冲突] 检测到并发修改冲突!")
                self.状态 = 同步状态.冲突处理
                
                # 触发冲突解决
                本地数据 = self._获取本地对应数据(明文数据)
                解决结果 = self.冲突解决.解决(本地数据, 明文数据)
                
                logger.info("🟢 [冲突] 已解决: %s", 解决结果.策略.value)
                self.状态 = 同步状态.完成
                return True, 解决结果.结果数据
            
            # 步骤5: 更新本地版本向量
            self.时钟.合并(远程向量)
            
            # 发送确认
            self.传输.发送确认(True)
            logger.info("🟢 [完成] 数据接收成功")
            
            return True, 明文数据
            
        except Exception as e:
            logger.error("🔴 [异常] 接收失败: %s", str(e))
            self.传输.发送确认(False)
            return False, None
    
    def 同步双向(self, 本地数据: Dict[str, Any]) -> 同步结果:
        """
        双向同步: 先发送本地数据，再接收对端数据，自动解决冲突
        
        Args:
            本地数据: 本机待同步数据
        
        Returns:
            同步结果对象
        """
        logger.info("🟡 [双向同步] 开始完整同步流程...")
        
        # 阶段1: 发送本地数据
        发送结果 = self.发送数据(本地数据)
        if not 发送结果.成功:
            logger.error("🔴 [失败] 发送阶段失败")
            return 发送结果
        
        # 阶段2: 接收对端数据
        接收成功, 对端数据 = self.接收数据()
        if not 接收成功:
            logger.warning("🟡 [提示] 未收到对端数据或接收失败")
            return 同步结果(True, 同步状态.完成,
                           发送结果.传输字节数, 发送结果.耗时毫秒,
                           0, True, ["🟢 发送成功，未接收数据"], self.DNA)
        
        # 阶段3: 合并数据（如无冲突）
        合并结果 = self._合并数据(本地数据, 对端数据)
        
        logger.info("🟢 [完成] 双向同步完成")
        return 同步结果(True, 同步状态.完成,
                       发送结果.传输字节数, 发送结果.耗时毫秒,
                       0, True,
                       ["🟢 双向同步成功", f"🟢 合并条目: {len(合并结果)}"],
                       self.DNA)
    
    # ============================================================
    # 内部方法
    # ============================================================
    
    def _显示二维码公钥(self, 公钥: bytes):
        """将公钥编码为二维码显示"""
        import qrcode
        公钥B64 = 公钥.hex()
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(f"LONGHUN:ECDH:{公钥B64}")
        qr.make(fit=True)
        print("\n[请扫描下方二维码获取本机公钥]")
        qr.print_ascii(invert=True)
    
    def _扫描对端二维码(self) -> bytes:
        """扫描对端设备的二维码获取公钥"""
        # 实际实现需要调用摄像头
        logger.info("🟡 [QR] 请扫描对端设备二维码...")
        # 模拟返回
        return b""
    
    def _nfc交换公钥(self, 本机公钥: bytes) -> bytes:
        """通过NFC碰碰交换公钥"""
        logger.info("🟡 [NFC] 请将两台设备靠近(NFC)...")
        # 实际实现需要调用NFC API
        return b""
    
    def _蓝牙交换公钥(self, 本机公钥: bytes) -> bytes:
        """通过蓝牙交换公钥"""
        logger.info("🟡 [BLE] 通过蓝牙交换公钥...")
        # 实际实现需要调用BLE API
        return b""
    
    def _获取本地对应数据(self, 远程数据: Dict[str, Any]) -> Dict[str, Any]:
        """获取与远程数据对应的本地数据"""
        # 实际实现从本地数据库查询
        return {}
    
    def _合并数据(self, 本地: Dict[str, Any], 对端: Dict[str, Any]) -> Dict[str, Any]:
        """合并两设备数据"""
        结果 = dict(本地)
        for 键, 值 in 对端.items():
            if 键 not in 结果:
                结果[键] = 值
        return 结果
    
    # ============================================================
    # 状态查询
    # ============================================================
    
    @property
    def 当前状态(self) -> 同步状态:
        return self.状态
    
    @property
    def 安全通道已建立(self) -> bool:
        return hasattr(self, '会话密钥') and self.会话密钥 is not None
    
    def 获取诊断信息(self) -> Dict[str, Any]:
        """获取完整诊断信息"""
        return {
            "dna": self.DNA,
            "version": self.版本,
            "status": self.状态.value,
            "本机": {
                "platform": self.本机.平台.value,
                "device_id": self.本机.设备ID,
                "device_name": self.本机.设备名,
            },
            "对端": {
                "platform": self.对端.平台.value,
                "device_id": self.对端.设备ID,
                "device_name": self.对端.设备名,
            },
            "安全通道": self.安全通道已建立,
            "版本向量": self.时钟.获取向量(),
            "传输方式": self.首选传输.value,
            "主权网关": "活跃",
            "审计": "🟢 主权保障 | 🟡 加密验证 | 🔴 冲突处理",
        }


# ============================================================
# 快速使用API
# ============================================================

def 创建同步会话(
    本机平台: str,
    本机ID: str,
    本机名: str,
    对端平台: str,
    对端ID: str,
    对端名: str,
    传输方式: str = "wifi_direct"
) -> 跨平台主模块:
    """
    快速创建同步会话的工厂函数
    
    Args:
        本机平台: "harmonyos" 或 "ios"
        本机ID: 本机设备唯一标识
        本机名: 本机设备名称
        对端平台: "harmonyos" 或 "ios"
        对端ID: 对端设备唯一标识
        对端名: 对端设备名称
        传输方式: "wifi_direct" / "ble" / "tcp_lan"
    
    Returns:
        跨平台主模块实例
    """
    平台映射 = {
        "harmonyos": 平台类型.HARMONYOS,
        "ios": 平台类型.IOS,
    }
    传输映射 = {
        "wifi_direct": 传输类型.WIFI_DIRECT,
        "ble": 传输类型.BLE,
        "tcp_lan": 传输类型.TCP_LAN,
    }
    
    本机 = 设备信息(
        平台=平台映射.get(本机平台, 平台类型.HARMONYOS),
        设备ID=本机ID,
        设备名=本机名
    )
    对端 = 设备信息(
        平台=平台映射.get(对端平台, 平台类型.IOS),
        设备ID=对端ID,
        设备名=对端名
    )
    
    传输 = 传输映射.get(传输方式, 传输类型.WIFI_DIRECT)
    
    return 跨平台主模块(本机, 对端, 传输)


# ============================================================
# 命令行入口
# ============================================================

if __name__ == "__main__":
    import sys
    
    print(f"\n{'='*60}")
    print("  龍魂跨平台互通 — iOS与鸿蒙本地数据直连")
    print(f"  DNA: {跨平台主模块.DNA}")
    print(f"  版本: {跨平台主模块.版本}")
    print(f"{'='*60}\n")
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python 跨平台主模块.py init    # 初始化同步会话")
        print("  python 跨平台主模块.py send    # 发送数据")
        print("  python 跨平台主模块.py recv    # 接收数据")
        print("  python 跨平台主模块.py sync    # 双向同步")
        print("  python 跨平台主模块.py diag    # 诊断信息")
        sys.exit(0)
    
    命令 = sys.argv[1]
    
    if 命令 == "init":
        session = 创建同步会话(
            "harmonyos", "device-001", "鸿蒙手机",
            "ios", "device-002", "iPhone"
        )
        session.协商密钥("qr")
        
    elif 命令 == "diag":
        session = 创建同步会话(
            "harmonyos", "device-001", "鸿蒙手机",
            "ios", "device-002", "iPhone"
        )
        print(json.dumps(session.获取诊断信息(), indent=2, ensure_ascii=False))
    
    else:
        print(f"未知命令: {命令}")

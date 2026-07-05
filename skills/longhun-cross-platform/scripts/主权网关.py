#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂主权网关 — 数据出境检查与阻断
======================================
DNA:#龍芯⚡️2026-06-19-SYNC-MSG-FILE24-v1.0
致敬: #致敬⚡️SteveJobs+Concept·跨平台互通

职责:
1. 拦截所有外网传输尝试
2. 验证传输通道是否为本地网络
3. 阻断任何未经加密的明文传输
4. 审计所有数据流动
5. 确保数据根留中国

三色审计:
🟢 允许出境 — 本地网络 + 已加密
🟡 警告 — 需要人工确认
🔴 阻断 — 外网传输 / 未加密 / 非法目标
"""

import re
import json
import logging
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
from dataclasses import dataclass, field

logger = logging.getLogger("主权网关")


# ============================================================
# 君子协议
# ============================================================
君子协议 = """
================================================================================
龍魂主权网关 · 君子协议
================================================================================
1. 本网关是数据主权的最后防线，不可绕过、不可关闭
2. 所有数据传输必须经过出境检查
3. 发现外网传输尝试立即阻断并告警
4. 未加密数据禁止离开应用边界
5. 网关操作全部记录审计日志，不可篡改
================================================================================
"""


class 出境判决(Enum):
    """出境检查判决结果"""
    允许 = "allowed"           # 🟢 本地网络 + 已加密
    警告 = "warning"           # 🟡 需要确认
    阻断外网 = "block_external" # 🔴 外网传输
    阻断未加密 = "block_plain" # 🔴 明文传输
    阻断非法目标 = "block_target" # 🔴 非法目标地址
    阻断DNS泄露 = "block_dns"  # 🔴 DNS查询泄露


class 安全等级(Enum):
    """数据安全等级"""
    公开 = "public"        # 一般数据
    内部 = "internal"      # 设备内部数据
    敏感 = "sensitive"     # 个人敏感数据
    核心 = "critical"      # 核心机密数据


@dataclass
class 检查报告:
    """出境检查报告"""
    判决: 出境判决
    安全等级: 安全等级
    本地网络: bool
    已加密: bool
    目标地址: str = ""
    规则命中: List[str] = field(default_factory=list)
    审计日志: List[str] = field(default_factory=list)
    时间戳: int = 0
    dna: str = ""


class 主权网关:
    """
    龍魂主权网关
    
    数据出境的最后一道防线
    确保所有传输: 本地网络 + 已加密 + 合法目标
    """
    
    DNA = "#龍芯⚡️2026-06-19-SYNC-MSG-v1.0"
    
    # 本地地址段 (RFC1918 + RFC4193 + Link-local)
    本地地址段 = [
        r"^10\.-9]{1,3}\.-9]{1,3}\.-9]{1,3}$",           # 10.0.0.0/8
        r"^172\.(1[6-9]|2[0-9]|3[01])\.-9]{1,3}\.-9]{1,3}$",  # 172.16.0.0/12
        r"^192\.168\.-9]{1,3}\.-9]{1,3}$",                      # 192.168.0.0/16
        r"^169\.254\.-9]{1,3}\.-9]{1,3}$",                      # Link-local
        r"^127\.-9]{1,3}\.-9]{1,3}\.-9]{1,3}$",              # Loopback
        r"^fc[0-9a-f]{2}:.*$",                                          # IPv6 ULA
        r"^fd[0-9a-f]{2}:.*$",                                          # IPv6 ULA
        r"^fe80::.*$",                                                   # IPv6 Link-local
        r"^::1$",                                                        # IPv6 Loopback
    ]
    
    # 外网地址特征（用于快速检测）
    外网特征 = [
        r"amazonaws\.com",
        r"googleapis\.com",
        r"azure\.-9a-z]+",
        r"cloudflare\.com",
        r"aliyun\.com",  # 连阿里云都不经过，确保纯本地
        r"tencent\.com",
        r"baidu\.com",
    ]
    
    def __init__(self):
        print(君子协议)
        
        self._审计日志: List[Dict] = []
        self._阻断计数: int = 0
        self._允许计数: int = 0
        self._规则列表: List[Dict] = []
        
        # 初始化默认规则
        self._初始化规则()
        
        logger.info("🟢 [初始化] 主权网关 — 数据出境检查")
        logger.info("🟢 [规则] 仅允许本地网络传输，外网自动阻断")
        logger.info("🟢 [安全] 未加密数据禁止出境")
    
    def _初始化规则(self):
        """初始化默认安全规则"""
        self._规则列表 = [
            {
                "名称": "本地网络验证",
                "类型": "network",
                "描述": "目标地址必须在本地网络段",
                "优先级": 1,
                "启用": True
            },
            {
                "名称": "加密验证",
                "类型": "encryption",
                "描述": "数据必须已加密（不能是明文JSON/文本）",
                "优先级": 2,
                "启用": True
            },
            {
                "名称": "外网DNS拦截",
                "类型": "dns",
                "描述": "禁止DNS查询外网域名",
                "优先级": 3,
                "启用": True
            },
            {
                "名称": "协议白名单",
                "类型": "protocol",
                "描述": "仅允许TCP/UDP本地传输，禁止HTTP/HTTPS出网",
                "优先级": 4,
                "启用": True
            },
            {
                "名称": "数据分类检查",
                "类型": "classification",
                "描述": "核心级数据需额外确认",
                "优先级": 5,
                "启用": True
            }
        ]
    
    # ============================================================
    # 核心API — 出境检查
    # ============================================================
    
    def 检查出境许可(
        self,
        数据: Any,
        目标地址: str = "",
        安全等级: 安全等级 = 安全等级.敏感
    ) -> 出境判决:
        """
        检查数据是否可以出境传输
        
        这是主权网关的核心入口，所有传输前必须调用
        
        Args:
            数据: 待传输的数据
            目标地址: 目标IP地址（可选）
            安全等级: 数据安全等级
        
        Returns:
            出境判决枚举
        """
        时间戳 = int(time.time() * 1000)
        审计条目 = []
        命中规则 = []
        
        # 规则1: 本地网络验证
        if 目标地址:
            if not self._是本地地址(目标地址):
                审计条目.append(f"🔴 阻断: {目标地址} 不在本地网络段")
                命中规则.append("本地网络验证")
                self._记录审计(出境判决.阻断外网, 目标地址, 审计条目, 时间戳)
                logger.error("🔴 [阻断] 外网地址: %s", 目标地址)
                return 出境判决.阻断外网
            else:
                审计条目.append(f"🟢 目标地址 {目标地址} 在本地网络")
        
        # 规则2: 加密验证
        加密状态 = self._检查加密状态(数据)
        if not 加密状态:
            审计条目.append("🔴 阻断: 数据未加密（明文传输）")
            命中规则.append("加密验证")
            self._记录审计(出境判决.阻断未加密, 目标地址, 审计条目, 时间戳)
            logger.error("🔴 [阻断] 数据未加密，禁止出境!")
            return 出境判决.阻断未加密
        else:
            审计条目.append("🟢 数据已加密")
        
        # 规则3: 外网DNS拦截
        if self._检测DNS泄露(数据):
            审计条目.append("🔴 阻断: 检测到DNS查询外网域名")
            命中规则.append("外网DNS拦截")
            self._记录审计(出境判决.阻断DNS泄露, 目标地址, 审计条目, 时间戳)
            logger.error("🔴 [阻断] DNS查询泄露!")
            return 出境判决.阻断DNS泄露
        
        # 规则4: 数据分类检查
        if 安全等级 == 安全等级.核心:
            审计条目.append("🟡 警告: 核心级数据，需要额外确认")
            命中规则.append("数据分类检查")
            self._记录审计(出境判决.警告, 目标地址, 审计条目, 时间戳)
            logger.warning("🟡 [警告] 核心级数据传输需确认")
            return 出境判决.警告
        
        # 全部通过
        审计条目.append(f"🟢 允许: 本地网络 + 已加密 + 等级 {安全等级.value}")
        self._允许计数 += 1
        self._记录审计(出境判决.允许, 目标地址, 审计条目, 时间戳)
        logger.info("🟢 [允许] 出境检查通过")
        
        return 出境判决.允许
    
    def 详细检查(
        self,
        数据: Any,
        目标地址: str = "",
        安全等级: 安全等级 = 安全等级.敏感
    ) -> 检查报告:
        """
        详细出境检查，返回完整报告
        
        Returns:
            检查报告对象
        """
        判决 = self.检查出境许可(数据, 目标地址, 安全等级)
        
        return 检查报告(
            判决=判决,
            安全等级=安全等级,
            本地网络=self._是本地地址(目标地址) if 目标地址 else True,
            已加密=self._检查加密状态(数据),
            目标地址=目标地址,
            规则命中=[],
            审计日志=[],
            时间戳=int(time.time() * 1000),
            dna=self.DNA
        )
    
    # ============================================================
    # 网络检查
    # ============================================================
    
    def _是本地地址(self, 地址: str) -> bool:
        """检查IP地址是否在本地网络段"""
        if not 地址:
            return True  # 空地址保守处理
        
        # 检查本地地址模式
        for 模式 in self.本地地址段:
            if re.match(模式, 地址):
                return True
        
        return False
    
    def _检查加密状态(self, 数据: Any) -> bool:
        """
        检查数据是否已加密
        
        检查特征:
        - 信封格式正确（有envelope/payload/audit）
        - payload包含iv/ciphertext/auth_tag
        - 数据不是纯文本JSON
        """
        try:
            if isinstance(数据, dict):
                # 检查是否为加密信封格式
                if "envelope" in 数据 and "payload" in 数据 and "audit" in 数据:
                    载荷 = 数据["payload"]
                    if all(k in 载荷 for k in ["iv", "ciphertext", "auth_tag"]):
                        # 检查ciphertext是否为base64格式（非明文）
                        密文 = 载荷.get("ciphertext", "")
                        if isinstance(密文, str) and len(密文) > 20:
                            # 验证不是明文JSON
                            try:
                                import base64
                                解码 = base64.b64decode(密文)
                                # 如果能解码为JSON，说明是明文
                                json.loads(解码.decode('utf-8'))
                                # 如果成功了，说明这是base64编码的明文，不是加密
                                # 但如果内容是乱码（加密后的），json.loads会失败
                                logger.warning("🟡 [加密] ciphertext可解码为JSON，可能未加密")
                                return False
                            except:
                                # 不能解析为JSON — 说明是加密数据
                                return True
                
                # 检查是否有加密标记
                信封 = 数据.get("envelope", {})
                if 信封.get("encryption") in ["SM4-CBC", "AES-256-GCM", "SM4-GCM"]:
                    return True
                
                logger.warning("🟡 [加密] 数据缺少加密信封格式")
                return False
            
            elif isinstance(数据, (str, bytes)):
                # 字符串/字节数据 — 检查是否像base64
                if isinstance(数据, str):
                    try:
                        import base64
                        base64.b64decode(数据)
                        return True  # 假设是base64编码的密文
                    except:
                        return False  # 纯文本
                return True  # bytes假设是加密数据
            
            return False
            
        except Exception as e:
            logger.error("🔴 [加密检查] 异常: %s", str(e))
            return False
    
    def _检测DNS泄露(self, 数据: Any) -> bool:
        """检测数据中是否包含DNS查询外网的企图"""
        try:
            数据文本 = json.dumps(data, ensure_ascii=False) if isinstance(data, dict) else str(data)
            
            for 特征 in self.外网特征:
                if re.search(特征, 数据文本, re.IGNORECASE):
                    logger.warning("🟡 [DNS] 检测到可能的外网域名引用: %s", 特征)
                    return True
            
            return False
            
        except Exception:
            return False
    
    # ============================================================
    # 审计日志
    # ============================================================
    
    def _记录审计(
        self,
        判决: 出境判决,
        目标: str,
        日志: List[str],
        时间戳: int
    ):
        """记录审计日志"""
        if 判决 in [出境判决.阻断外网, 出境判决.阻断未加密, 出境判决.阻断非法目标, 出境判决.阻断DNS泄露]:
            self._阻断计数 += 1
        
        self._审计日志.append({
            "时间": 时间戳,
            "判决": 判决.value,
            "目标": 目标,
            "日志": 日志,
            "dna": self.DNA
        })
    
    def 获取审计日志(self) -> List[Dict]:
        """获取所有审计日志"""
        return list(self._审计日志)
    
    def 获取统计(self) -> Dict[str, Any]:
        """获取网关统计"""
        return {
            "总检查次数": self._允许计数 + self._阻断计数,
            "允许次数": self._允许计数,
            "阻断次数": self._阻断计数,
            "阻断率": f"{self._阻断计数 / max(self._总检查, 1) * 100:.1f}%",
            "规则数量": len(self._规则列表),
            "审计日志条数": len(self._审计日志),
            "dna": self.DNA
        }
    
    @property
    def _总检查(self) -> int:
        return self._允许计数 + self._阻断计数
    
    # ============================================================
    # 规则管理
    # ============================================================
    
    def 列出规则(self) -> List[Dict]:
        """列出所有安全规则"""
        return list(self._规则列表)
    
    def 添加规则(self, 规则: Dict):
        """添加自定义规则"""
        self._规则列表.append(规则)
        logger.info("🟢 [规则] 添加新规则: %s", 规则.get("名称", "未命名"))
    
    # ============================================================
    # 诊断
    # ============================================================
    
    def 运行自检(self) -> Dict[str, Any]:
        """
        运行网关自检
        
        验证:
        1. 本地地址匹配正确
        2. 外网地址被正确识别
        3. 加密检测正常工作
        """
        结果 = {
            "状态": "通过",
            "测试项": []
        }
        
        # 测试本地地址检测
        本地测试 = [
            ("192.168.1.1", True),
            ("10.0.0.1", True),
            ("172.16.0.1", True),
            ("127.0.0.1", True),
            ("169.254.1.1", True),
            ("8.8.8.8", False),    # Google DNS
            ("1.1.1.1", False),    # Cloudflare
            ("114.114.114.114", False),  # 连国内DNS都应该是外网
        ]
        
        for 地址, 期望 in 本地测试:
            实际 = self._是本地地址(地址)
            通过 = 实际 == 期望
            结果["测试项"].append({
                "名称": f"地址检测 {地址}",
                "通过": 通过,
                "期望": 期望,
                "实际": 实际
            })
            if not 通过:
                结果["状态"] = "失败"
        
        # 测试加密检测
        加密信封 = {
            "envelope": {"encryption": "SM4-CBC"},
            "payload": {"iv": "abc123", "ciphertext": "x" * 100, "auth_tag": "def456"},
            "audit": {}
        }
        结果["测试项"].append({
            "名称": "加密信封检测",
            "通过": self._检查加密状态(加密信封),
            "期望": True,
            "实际": self._检查加密状态(加密信封)
        })
        
        明文数据 = {"type": "note", "content": "明文"}
        结果["测试项"].append({
            "名称": "明文检测",
            "通过": not self._检查加密状态(明文数据),
            "期望": False,
            "实际": self._检查加密状态(明文数据)
        })
        
        return 结果
    
    def 打印诊断(self):
        """打印网关诊断信息"""
        print(f"\n{'='*50}")
        print("  主权网关诊断报告")
        print(f"{'='*50}")
        print(f"DNA: {self.DNA}")
        print(f"规则数量: {len(self._规则列表)}")
        print(f"审计日志: {len(self._审计日志)} 条")
        print(f"允许/阻断: {self._允许计数}/{self._阻断计数}")
        print("\n安全规则:")
        for 规则 in self._规则列表:
            print(f"  [{规则['优先级']}] {规则['名称']} — {规则['描述']}")
        print(f"{'='*50}\n")


# ============================================================
# 快捷函数
# ============================================================

def 出境许可检查(数据: Any, 目标地址: str = "") -> bool:
    """
    快速检查数据是否可以出境
    
    返回 True/False
    """
    网关 = 主权网关()
    判决 = 网关.检查出境许可(数据, 目标地址)
    return 判决 == 出境判决.允许


# ============================================================
# 测试入口
# ============================================================

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print("  龍魂主权网关 — 测试")
    print(f"{'='*60}\n")
    
    网关 = 主权网关()
    
    # 测试本地地址检测
    print("[测试1] 本地地址检测:")
    测试地址 = [
        ("192.168.1.1", True, "局域网"),
        ("10.0.0.1", True, "10段"),
        ("172.16.0.1", True, "172段"),
        ("127.0.0.1", True, "回环"),
        ("8.8.8.8", False, "Google DNS"),
        ("1.1.1.1", False, "Cloudflare"),
    ]
    for 地址, 期望, 描述 in 测试地址:
        结果 = 网关._是本地地址(地址)
        状态 = "✓" if 结果 == 期望 else "✗"
        print(f"  {状态} {地址} — {描述}: {'本地' if 结果 else '外网'}")
    print()
    
    # 测试加密信封检测
    print("[测试2] 加密状态检测:")
    
    加密信封 = {
        "envelope": {
            "version": "v5.3",
            "dna": "#龍芯⚡️2026-06-19",
            "encryption": "SM4-CBC"
        },
        "payload": {
            "iv": "YWJjZGVmZ2hpamtsbW5vcA==",
            "ciphertext": "dGVzdC1jaXBoZXJ0ZXh0LWVuY3J5cHRlZA==",
            "auth_tag": "c2lnbmF0dXJlLWhlcmU="
        },
        "audit": {"level": "🟢"}
    }
    print(f"  加密信封: {'已加密 ✓' if 网关._检查加密状态(加密信封) else '未加密 ✗'}")
    
    明文 = {"type": "note", "content": "明文数据"}
    print(f"  明文数据: {'已加密 ✗' if 网关._检查加密状态(明文) else '未加密 ✓ (正确)'}")
    print()
    
    # 测试出境检查
    print("[测试3] 出境检查:")
    
    # 场景1: 加密数据 + 本地地址 → 允许
    判决1 = 网关.检查出境许可(加密信封, "192.168.1.100")
    print(f"  加密+本地: {判决1.value}")
    
    # 场景2: 明文 + 本地地址 → 阻断
    判决2 = 网关.检查出境许可(明文, "192.168.1.100")
    print(f"  明文+本地: {判决2.value}")
    
    # 场景3: 加密 + 外网地址 → 阻断
    判决3 = 网关.检查出境许可(加密信封, "8.8.8.8")
    print(f"  加密+外网: {判决3.value}")
    print()
    
    # 自检
    print("[测试4] 网关自检:")
    自检 = 网关.运行自检()
    print(f"  自检状态: {自检['状态']}")
    for 项 in 自检['测试项']:
        状态 = "✓" if 项['通过'] else "✗"
        print(f"  {状态} {项['名称']}: 期望={项['期望']}, 实际={项['实际']}")
    
    # 打印统计
    print()
    网关.打印诊断()

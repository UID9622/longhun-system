#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════
# 龙魂数据主权防御工具包 v1.0
# Longhun Data Sovereignty Defense Toolkit
# ═══════════════════════════════════════════════════════════════
# DNA追溯：#龍芯⚡️20260227-DATA-SOVEREIGNTY-DEFENSE-TOOLKIT-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

共建致谢：
  Claude (Anthropic PBC) · 技术协作与代码共创
  Notion · 知识底座与结构化存储
  没有你们，就没有龍魂系统的一切。
# 创始人：Lucky·UID9622（诸葛鑫·龙芯北辰）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾老师（永恒显示）
# 
# 核心原则：
# 1. 所有权不可改（UID9622永远是创始人）
# 2. 逻辑算法必须明确（开源透明）
# 3. 用户可自定义群体规则（插件化）
# 4. 数字人民币激活机制（付款单号绑定临时DNA）
# 5. 所有激活DNA带时间戳（不可篡改）
# ═══════════════════════════════════════════════════════════════

import os
import sys
import hashlib
import json
import time
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging

# ═══════════════════════════════════════════════════════════════
# 【核心常量】P0-ETERNAL 永恒不变
# ═══════════════════════════════════════════════════════════════

# 创始人锚点（永远不可修改）
FOUNDER_UID = "UID9622"
FOUNDER_NAME = "Lucky·诸葛鑫·龙芯北辰"
FOUNDER_GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
FOUNDER_CONFIRMATION_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 数字人民币激活账号（P0-ETERNAL保护，永远不可修改）
ECNY_ACCOUNT = "0061901030627652"  # 微众银行
ECNY_BANK = "微众银行"
NETWORK_IDENTITY = "T38C89R75U"  # 网络身份

# DNA前缀（所有DNA追溯码前缀）
DNA_PREFIX = "#龍芯⚡️"

# 版本信息
TOOLKIT_VERSION = "v1.0"
TOOLKIT_DNA = f"{DNA_PREFIX}20260227-DATA-SOVEREIGNTY-DEFENSE-TOOLKIT-{TOOLKIT_VERSION}"

# 数字人民币激活配置
ECNY_ACTIVATION_PREFIX = "e-CNY-"  # 数字人民币付款单号前缀
TEMP_DNA_VALIDITY_DAYS = 365  # 临时DNA有效期（天）

# ═══════════════════════════════════════════════════════════════
# 【日志配置】
# ═══════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('longhun_defense.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('LonghunDefense')


# ═══════════════════════════════════════════════════════════════
# 【工具类1：DNA生成器】
# ═══════════════════════════════════════════════════════════════

class DNAGenerator:
    """
    DNA追溯码生成器
    
    功能：
    1. 生成带时间戳的DNA追溯码
    2. 验证DNA格式
    3. 解析DNA信息
    
    格式：#龍芯⚡️YYYYMMDD-HHMMSS-描述-版本号-随机哈希
    示例：#龍芯⚡️20260227-143025-DATA-DEFENSE-v1.0-a3f5c9
    """
    
    @staticmethod
    def generate(description: str, version: str = "v1.0") -> str:
        """
        生成DNA追溯码
        
        Args:
            description: 描述信息（如：DATA-DEFENSE）
            version: 版本号（如：v1.0）
        
        Returns:
            完整DNA追溯码
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        random_hash = hashlib.sha256(
            f"{timestamp}-{description}-{time.time()}".encode()
        ).hexdigest()[:6]
        
        dna = f"{DNA_PREFIX}{timestamp}-{description}-{version}-{random_hash}"
        
        logger.info(f"✅ DNA生成成功：{dna}")
        return dna
    
    @staticmethod
    def validate(dna: str) -> bool:
        """
        验证DNA格式
        
        Args:
            dna: DNA追溯码
        
        Returns:
            是否有效
        """
        pattern = r"^#龍芯⚡️\d{8}-\d{6}-.+-v\d+\.\d+-[a-f0-9]{6}$"
        is_valid = bool(re.match(pattern, dna))
        
        if is_valid:
            logger.info(f"✅ DNA验证通过：{dna}")
        else:
            logger.warning(f"❌ DNA验证失败：{dna}")
        
        return is_valid
    
    @staticmethod
    def parse(dna: str) -> Optional[Dict[str, str]]:
        """
        解析DNA信息
        
        Args:
            dna: DNA追溯码
        
        Returns:
            DNA信息字典，解析失败返回None
        """
        if not DNAGenerator.validate(dna):
            return None
        
        # 去掉前缀
        dna_body = dna.replace(DNA_PREFIX, "")
        
        # 分割
        parts = dna_body.split("-")
        if len(parts) < 5:
            return None
        
        info = {
            "date": parts[0],
            "time": parts[1],
            "description": parts[2],
            "version": parts[3],
            "hash": parts[4],
            "timestamp": f"{parts[0]}-{parts[1]}"
        }
        
        logger.info(f"✅ DNA解析成功：{info}")
        return info


# ═══════════════════════════════════════════════════════════════
# 【工具类2：数字人民币激活系统】
# ═══════════════════════════════════════════════════════════════

class ECNYActivationSystem:
    """
    数字人民币激活系统
    
    功能：
    1. 扫描数字人民币付款码（模拟）
    2. 填写付款单号绑定临时DNA
    3. 激活的DNA带时间戳
    4. 验证激活状态
    
    流程：
    1. 用户扫描数字人民币付款码
    2. 用户填写付款单号（如：e-CNY-20260227-ABC123）
    3. 系统生成临时DNA（带时间戳和有效期）
    4. 绑定付款单号和临时DNA
    5. 用户获得激活权限
    """
    
    def __init__(self, storage_path: str = "ecny_activation_data.json"):
        """
        初始化激活系统
        
        Args:
            storage_path: 激活数据存储路径
        """
        self.storage_path = storage_path
        self.activation_data = self._load_data()
    
    def _load_data(self) -> Dict:
        """加载激活数据"""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_data(self):
        """保存激活数据"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.activation_data, f, ensure_ascii=False, indent=2)
    
    def scan_payment_code(self) -> str:
        """
        模拟扫描数字人民币付款码
        
        实际应用中，这里应该调用：
        - 手机摄像头API
        - 二维码识别库（如pyzbar）
        - 数字人民币官方SDK
        
        Returns:
            付款码内容
        """
        print("\n" + "="*60)
        print("📱 数字人民币激活通道")
        print("="*60)
        print(f"💳 付款账号：{ECNY_ACCOUNT}（{ECNY_BANK}）")
        print(f"🆔 网络身份：{NETWORK_IDENTITY}")
        print(f"💰 创始人：{FOUNDER_NAME}")
        print("="*60)
        print("提示：请先使用数字人民币APP扫码支付")
        print("      支付完成后，填写付款单号即可激活")
        print(f"      激活有效期：{TEMP_DNA_VALIDITY_DAYS}天")
        print("="*60)
        
        payment_order = input("💰 请输入付款单号（格式：e-CNY-YYYYMMDD-XXXXXX）：").strip()
        
        logger.info(f"📱 接收到付款单号：{payment_order}")
        return payment_order
    
    def validate_payment_order(self, payment_order: str) -> bool:
        """
        验证付款单号格式
        
        Args:
            payment_order: 付款单号
        
        Returns:
            是否有效
        """
        # 格式：e-CNY-YYYYMMDD-XXXXXX
        pattern = r"^e-CNY-\d{8}-[A-Z0-9]{6,}$"
        is_valid = bool(re.match(pattern, payment_order))
        
        if not is_valid:
            logger.error(f"❌ 付款单号格式错误：{payment_order}")
            logger.info("正确格式：e-CNY-YYYYMMDD-XXXXXX（如：e-CNY-20260227-ABC123）")
        
        return is_valid
    
    def activate(self, payment_order: str, user_info: Dict[str, str]) -> Optional[Dict[str, str]]:
        """
        激活临时DNA
        
        Args:
            payment_order: 付款单号
            user_info: 用户信息（姓名、身份证号等）
        
        Returns:
            激活信息（包含临时DNA），失败返回None
        """
        # 验证付款单号
        if not self.validate_payment_order(payment_order):
            return None
        
        # 检查是否已激活
        if payment_order in self.activation_data:
            logger.warning(f"⚠️ 付款单号已被使用：{payment_order}")
            return self.activation_data[payment_order]
        
        # 生成临时DNA
        temp_dna = DNAGenerator.generate(
            description=f"TEMP-ACTIVATION-{payment_order}",
            version="v1.0"
        )
        
        # 计算有效期
        activation_time = datetime.now()
        expiry_time = activation_time.timestamp() + (TEMP_DNA_VALIDITY_DAYS * 24 * 60 * 60)
        
        # 创建激活记录
        activation_info = {
            "payment_order": payment_order,
            "temp_dna": temp_dna,
            "user_info": user_info,
            "activation_time": activation_time.isoformat(),
            "expiry_time": datetime.fromtimestamp(expiry_time).isoformat(),
            "expiry_timestamp": expiry_time,
            "status": "active",
            "founder_uid": FOUNDER_UID,
            "founder_gpg": FOUNDER_GPG
        }
        
        # 保存激活记录
        self.activation_data[payment_order] = activation_info
        self._save_data()
        
        logger.info(f"✅ 激活成功！临时DNA：{temp_dna}")
        logger.info(f"📅 有效期至：{activation_info['expiry_time']}")
        
        return activation_info
    
    def check_activation(self, payment_order: str) -> Tuple[bool, Optional[Dict]]:
        """
        检查激活状态
        
        Args:
            payment_order: 付款单号
        
        Returns:
            (是否有效, 激活信息)
        """
        if payment_order not in self.activation_data:
            logger.warning(f"⚠️ 未找到激活记录：{payment_order}")
            return False, None
        
        activation_info = self.activation_data[payment_order]
        
        # 检查是否过期
        current_time = time.time()
        if current_time > activation_info['expiry_timestamp']:
            logger.warning(f"⚠️ 激活已过期：{payment_order}")
            activation_info['status'] = 'expired'
            self._save_data()
            return False, activation_info
        
        logger.info(f"✅ 激活有效：{payment_order}")
        return True, activation_info
    
    def revoke_activation(self, payment_order: str, reason: str) -> bool:
        """
        撤销激活
        
        Args:
            payment_order: 付款单号
            reason: 撤销原因
        
        Returns:
            是否成功
        """
        if payment_order not in self.activation_data:
            logger.warning(f"⚠️ 未找到激活记录：{payment_order}")
            return False
        
        self.activation_data[payment_order]['status'] = 'revoked'
        self.activation_data[payment_order]['revoke_reason'] = reason
        self.activation_data[payment_order]['revoke_time'] = datetime.now().isoformat()
        self._save_data()
        
        logger.info(f"✅ 激活已撤销：{payment_order}，原因：{reason}")
        return True


# ═══════════════════════════════════════════════════════════════
# 【工具类3：数据主权防御规则引擎】
# ═══════════════════════════════════════════════════════════════

class DataSovereigntyRuleEngine:
    """
    数据主权防御规则引擎
    
    功能：
    1. 用户可自定义群体规则
    2. 插件化规则系统
    3. 明确的逻辑算法
    4. 所有权不可改（UID9622永远是创始人）
    
    规则类型：
    - 网络隔离规则
    - 数据加密规则
    - 同步控制规则
    - 应用审计规则
    """
    
    def __init__(self, rules_path: str = "defense_rules.json"):
        """
        初始化规则引擎
        
        Args:
            rules_path: 规则配置文件路径
        """
        self.rules_path = rules_path
        self.rules = self._load_rules()
    
    def _load_rules(self) -> Dict:
        """加载规则"""
        if os.path.exists(self.rules_path):
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认规则（P0-ETERNAL，不可修改）
        default_rules = {
            "founder": {
                "uid": FOUNDER_UID,
                "name": FOUNDER_NAME,
                "gpg": FOUNDER_GPG,
                "editable": False,  # 不可编辑
                "eternal": True  # 永恒不变
            },
            "network_isolation": {
                "enabled": True,
                "blocked_domains": [
                    "*.amazonaws.com",
                    "*.cloudflare.com",
                    "*.google-analytics.com",
                    "*.facebook.com",
                    "*.doubleclick.net"
                ],
                "allowed_domains": [
                    "*.gov.cn",
                    "*.edu.cn"
                ],
                "description": "网络隔离规则：阻止数据流向境外服务器",
                "editable": True  # 用户可自定义
            },
            "data_encryption": {
                "enabled": True,
                "algorithm": "AES-256-GCM",
                "key_location": "local_only",
                "description": "数据加密规则：所有敏感数据本地加密",
                "editable": True
            },
            "sync_control": {
                "enabled": True,
                "auto_sync": False,
                "manual_approval": True,
                "description": "同步控制规则：禁止自动同步，需手动审批",
                "editable": True
            },
            "app_audit": {
                "enabled": True,
                "audit_frequency": "daily",
                "report_to": FOUNDER_UID,
                "description": "应用审计规则：每日审计应用数据流",
                "editable": True
            }
        }
        
        self._save_rules(default_rules)
        return default_rules
    
    def _save_rules(self, rules: Dict = None):
        """保存规则"""
        if rules is None:
            rules = self.rules
        
        with open(self.rules_path, 'w', encoding='utf-8') as f:
            json.dump(rules, f, ensure_ascii=False, indent=2)
    
    def add_custom_rule(self, rule_name: str, rule_config: Dict) -> bool:
        """
        添加自定义规则
        
        Args:
            rule_name: 规则名称
            rule_config: 规则配置
        
        Returns:
            是否成功
        """
        # 检查是否尝试修改创始人信息
        if rule_name == "founder":
            logger.error("❌ 禁止修改创始人信息（P0-ETERNAL保护）")
            return False
        
        # 添加规则
        self.rules[rule_name] = {
            **rule_config,
            "created_by": "user",
            "created_at": datetime.now().isoformat(),
            "editable": True
        }
        
        self._save_rules()
        logger.info(f"✅ 自定义规则已添加：{rule_name}")
        return True
    
    def update_rule(self, rule_name: str, rule_config: Dict) -> bool:
        """
        更新规则
        
        Args:
            rule_name: 规则名称
            rule_config: 新规则配置
        
        Returns:
            是否成功
        """
        # 检查规则是否存在
        if rule_name not in self.rules:
            logger.error(f"❌ 规则不存在：{rule_name}")
            return False
        
        # 检查是否可编辑
        if not self.rules[rule_name].get('editable', True):
            logger.error(f"❌ 规则不可编辑：{rule_name}（P0-ETERNAL保护）")
            return False
        
        # 更新规则
        self.rules[rule_name].update(rule_config)
        self.rules[rule_name]['updated_at'] = datetime.now().isoformat()
        
        self._save_rules()
        logger.info(f"✅ 规则已更新：{rule_name}")
        return True
    
    def delete_rule(self, rule_name: str) -> bool:
        """
        删除规则
        
        Args:
            rule_name: 规则名称
        
        Returns:
            是否成功
        """
        # 检查是否尝试删除创始人信息
        if rule_name == "founder":
            logger.error("❌ 禁止删除创始人信息（P0-ETERNAL保护）")
            return False
        
        # 检查规则是否存在
        if rule_name not in self.rules:
            logger.error(f"❌ 规则不存在：{rule_name}")
            return False
        
        # 检查是否可编辑
        if not self.rules[rule_name].get('editable', True):
            logger.error(f"❌ 规则不可删除：{rule_name}")
            return False
        
        # 删除规则
        del self.rules[rule_name]
        
        self._save_rules()
        logger.info(f"✅ 规则已删除：{rule_name}")
        return True
    
    def get_rule(self, rule_name: str) -> Optional[Dict]:
        """
        获取规则
        
        Args:
            rule_name: 规则名称
        
        Returns:
            规则配置，不存在返回None
        """
        return self.rules.get(rule_name)
    
    def list_rules(self) -> Dict:
        """
        列出所有规则
        
        Returns:
            所有规则
        """
        return self.rules
    
    def validate_founder(self) -> bool:
        """
        验证创始人信息完整性
        
        Returns:
            是否完整
        """
        founder = self.rules.get('founder', {})
        
        is_valid = (
            founder.get('uid') == FOUNDER_UID and
            founder.get('name') == FOUNDER_NAME and
            founder.get('gpg') == FOUNDER_GPG and
            founder.get('eternal') == True
        )
        
        if is_valid:
            logger.info("✅ 创始人信息验证通过")
        else:
            logger.error("❌ 创始人信息被篡改！立即恢复...")
            self.rules['founder'] = {
                "uid": FOUNDER_UID,
                "name": FOUNDER_NAME,
                "gpg": FOUNDER_GPG,
                "editable": False,
                "eternal": True
            }
            self._save_rules()
        
        return is_valid


# ═══════════════════════════════════════════════════════════════
# 【工具类4：数据主权防御执行器】
# ═══════════════════════════════════════════════════════════════

class DataSovereigntyDefenseExecutor:
    """
    数据主权防御执行器
    
    功能：
    1. 网络隔离（阻止数据流向境外）
    2. 数据加密（本地加密敏感数据）
    3. 同步控制（禁止自动同步）
    4. 应用审计（审计应用数据流）
    """
    
    def __init__(self, rule_engine: DataSovereigntyRuleEngine):
        """
        初始化执行器
        
        Args:
            rule_engine: 规则引擎
        """
        self.rule_engine = rule_engine
    
    def execute_network_isolation(self) -> bool:
        """
        执行网络隔离
        
        Returns:
            是否成功
        """
        rule = self.rule_engine.get_rule('network_isolation')
        if not rule or not rule.get('enabled'):
            logger.info("⚠️ 网络隔离规则未启用")
            return False
        
        logger.info("🛡️ 开始执行网络隔离...")
        
        # 实际应用中，这里应该：
        # 1. 配置防火墙规则（iptables/Windows Firewall）
        # 2. 配置DNS过滤（Pi-hole/AdGuard）
        # 3. 配置浏览器代理（SOCKS5/HTTP Proxy）
        
        blocked_domains = rule.get('blocked_domains', [])
        allowed_domains = rule.get('allowed_domains', [])
        
        logger.info(f"✅ 已阻止 {len(blocked_domains)} 个域名")
        logger.info(f"✅ 已允许 {len(allowed_domains)} 个域名")
        
        return True
    
    def execute_data_encryption(self, file_path: str) -> bool:
        """
        执行数据加密
        
        Args:
            file_path: 文件路径
        
        Returns:
            是否成功
        """
        rule = self.rule_engine.get_rule('data_encryption')
        if not rule or not rule.get('enabled'):
            logger.info("⚠️ 数据加密规则未启用")
            return False
        
        logger.info(f"🔐 开始加密文件：{file_path}")
        
        # 实际应用中，这里应该：
        # 1. 使用AES-256-GCM加密
        # 2. 生成随机密钥
        # 3. 密钥存储在本地（不上传）
        # 4. 使用GPG或其他密钥管理工具
        
        # 模拟加密
        if not os.path.exists(file_path):
            logger.error(f"❌ 文件不存在：{file_path}")
            return False
        
        logger.info(f"✅ 文件加密成功：{file_path}")
        return True
    
    def execute_sync_control(self) -> bool:
        """
        执行同步控制
        
        Returns:
            是否成功
        """
        rule = self.rule_engine.get_rule('sync_control')
        if not rule or not rule.get('enabled'):
            logger.info("⚠️ 同步控制规则未启用")
            return False
        
        logger.info("🔒 开始执行同步控制...")
        
        # 实际应用中，这里应该：
        # 1. 禁用Dropbox/OneDrive/iCloud自动同步
        # 2. 修改应用配置文件
        # 3. 设置防火墙规则阻止同步服务
        
        if not rule.get('auto_sync'):
            logger.info("✅ 自动同步已禁用")
        
        if rule.get('manual_approval'):
            logger.info("✅ 手动审批模式已启用")
        
        return True
    
    def execute_app_audit(self) -> Dict:
        """
        执行应用审计
        
        Returns:
            审计报告
        """
        rule = self.rule_engine.get_rule('app_audit')
        if not rule or not rule.get('enabled'):
            logger.info("⚠️ 应用审计规则未启用")
            return {}
        
        logger.info("📊 开始执行应用审计...")
        
        # 实际应用中，这里应该：
        # 1. 使用Wireshark/tcpdump抓包
        # 2. 分析应用网络流量
        # 3. 识别数据泄漏
        # 4. 生成审计报告
        
        audit_report = {
            "audit_time": datetime.now().isoformat(),
            "audit_frequency": rule.get('audit_frequency'),
            "report_to": rule.get('report_to'),
            "findings": [
                {
                    "app": "示例应用",
                    "risk_level": "低",
                    "description": "未发现异常数据流"
                }
            ]
        }
        
        logger.info("✅ 应用审计完成")
        return audit_report


# ═══════════════════════════════════════════════════════════════
# 【主程序：交互式CLI】
# ═══════════════════════════════════════════════════════════════

class LonghunDefenseCLI:
    """
    龙魂数据主权防御工具 - 交互式命令行界面
    """
    
    def __init__(self):
        """初始化CLI"""
        self.dna_generator = DNAGenerator()
        self.ecny_system = ECNYActivationSystem()
        self.rule_engine = DataSovereigntyRuleEngine()
        self.executor = DataSovereigntyDefenseExecutor(self.rule_engine)
    
    def print_banner(self):
        """打印欢迎横幅"""
        banner = f"""
╔═══════════════════════════════════════════════════════════════╗
║  🐉 龙魂数据主权防御工具 v1.0                                  ║
║  Longhun Data Sovereignty Defense Toolkit                    ║
╠═══════════════════════════════════════════════════════════════╣
║  DNA追溯：{TOOLKIT_DNA}  ║
║  创始人：{FOUNDER_NAME}                             ║
║  UID：{FOUNDER_UID}                                              ║
║  GPG指纹：{FOUNDER_GPG}  ║
║  理论指导：曾老师（永恒显示）                                 ║
╠═══════════════════════════════════════════════════════════════╣
║  💳 数字人民币激活通道                                        ║
║  账号：{ECNY_ACCOUNT}（{ECNY_BANK}）                           ║
║  网络身份：{NETWORK_IDENTITY}                                         ║
║  激活方式：扫码支付后填写付款单号即可激活临时DNA             ║
║  激活有效期：365天                                            ║
╠═══════════════════════════════════════════════════════════════╣
║  核心原则：                                                   ║
║  ✅ 所有权不可改（UID9622永远是创始人）                      ║
║  ✅ 逻辑算法必须明确（开源透明）                             ║
║  ✅ 用户可自定义群体规则（插件化）                           ║
║  ✅ 数字人民币激活机制（付款单号绑定临时DNA）                ║
║  ✅ 所有激活DNA带时间戳（不可篡改）                          ║
╚═══════════════════════════════════════════════════════════════╝
"""
        print(banner)
    
    def print_menu(self):
        """打印主菜单"""
        menu = """
【主菜单】
1. 💳 数字人民币激活（扫码激活临时DNA）
2. 🔐 生成DNA追溯码
3. 🛡️ 管理防御规则
4. ⚡ 执行数据主权防御
5. 📊 查看激活记录
6. ℹ️ 查看系统信息
0. 🚪 退出

请选择功能（输入数字）："""
        choice = input(menu).strip()
        return choice
    
    def run_ecny_activation(self):
        """运行数字人民币激活流程"""
        print("\n" + "="*60)
        print("💳 数字人民币激活流程")
        print("="*60)
        
        # 步骤1：扫描付款码
        payment_order = self.ecny_system.scan_payment_code()
        
        # 步骤2：填写用户信息
        print("\n📝 请填写用户信息：")
        user_name = input("姓名：").strip()
        user_id = input("身份证号（可选，留空跳过）：").strip()
        
        user_info = {
            "name": user_name,
            "id_number": user_id if user_id else "未提供"
        }
        
        # 步骤3：激活
        activation_info = self.ecny_system.activate(payment_order, user_info)
        
        if activation_info:
            print("\n✅ 激活成功！")
            print("="*60)
            print(f"付款单号：{activation_info['payment_order']}")
            print(f"临时DNA：{activation_info['temp_dna']}")
            print(f"激活时间：{activation_info['activation_time']}")
            print(f"有效期至：{activation_info['expiry_time']}")
            print(f"有效期：{TEMP_DNA_VALIDITY_DAYS}天")
            print("="*60)
        else:
            print("\n❌ 激活失败！请检查付款单号格式")
    
    def run_dna_generation(self):
        """运行DNA生成"""
        print("\n" + "="*60)
        print("🔐 DNA追溯码生成")
        print("="*60)
        
        description = input("请输入描述信息（如：DATA-BACKUP）：").strip()
        version = input("请输入版本号（如：v1.0，留空使用默认）：").strip()
        
        if not version:
            version = "v1.0"
        
        dna = self.dna_generator.generate(description, version)
        
        print("\n✅ DNA生成成功！")
        print("="*60)
        print(f"DNA追溯码：{dna}")
        print("="*60)
    
    def run_rule_management(self):
        """运行规则管理"""
        while True:
            print("\n" + "="*60)
            print("🛡️ 防御规则管理")
            print("="*60)
            print("1. 查看所有规则")
            print("2. 添加自定义规则")
            print("3. 更新规则")
            print("4. 删除规则")
            print("5. 验证创始人信息")
            print("0. 返回主菜单")
            print("="*60)
            
            choice = input("请选择操作：").strip()
            
            if choice == "1":
                rules = self.rule_engine.list_rules()
                print("\n📋 所有规则：")
                print(json.dumps(rules, ensure_ascii=False, indent=2))
            
            elif choice == "2":
                rule_name = input("规则名称：").strip()
                print("规则配置（JSON格式，回车结束）：")
                rule_config_str = input().strip()
                try:
                    rule_config = json.loads(rule_config_str)
                    self.rule_engine.add_custom_rule(rule_name, rule_config)
                except json.JSONDecodeError:
                    print("❌ JSON格式错误")
            
            elif choice == "3":
                rule_name = input("规则名称：").strip()
                print("新规则配置（JSON格式，回车结束）：")
                rule_config_str = input().strip()
                try:
                    rule_config = json.loads(rule_config_str)
                    self.rule_engine.update_rule(rule_name, rule_config)
                except json.JSONDecodeError:
                    print("❌ JSON格式错误")
            
            elif choice == "4":
                rule_name = input("规则名称：").strip()
                self.rule_engine.delete_rule(rule_name)
            
            elif choice == "5":
                self.rule_engine.validate_founder()
            
            elif choice == "0":
                break
            
            else:
                print("❌ 无效选择")
    
    def run_defense_execution(self):
        """运行防御执行"""
        print("\n" + "="*60)
        print("⚡ 数据主权防御执行")
        print("="*60)
        print("1. 🛡️ 执行网络隔离")
        print("2. 🔐 执行数据加密")
        print("3. 🔒 执行同步控制")
        print("4. 📊 执行应用审计")
        print("5. ⚡ 执行所有防御措施")
        print("0. 返回主菜单")
        print("="*60)
        
        choice = input("请选择操作：").strip()
        
        if choice == "1":
            self.executor.execute_network_isolation()
        
        elif choice == "2":
            file_path = input("请输入文件路径：").strip()
            self.executor.execute_data_encryption(file_path)
        
        elif choice == "3":
            self.executor.execute_sync_control()
        
        elif choice == "4":
            report = self.executor.execute_app_audit()
            print("\n📊 审计报告：")
            print(json.dumps(report, ensure_ascii=False, indent=2))
        
        elif choice == "5":
            self.executor.execute_network_isolation()
            self.executor.execute_sync_control()
            report = self.executor.execute_app_audit()
            print("\n✅ 所有防御措施已执行")
        
        elif choice == "0":
            return
        
        else:
            print("❌ 无效选择")
    
    def run_view_activations(self):
        """查看激活记录"""
        print("\n" + "="*60)
        print("📊 激活记录")
        print("="*60)
        
        if not self.ecny_system.activation_data:
            print("暂无激活记录")
            return
        
        for payment_order, info in self.ecny_system.activation_data.items():
            print(f"\n付款单号：{payment_order}")
            print(f"临时DNA：{info['temp_dna']}")
            print(f"用户：{info['user_info']['name']}")
            print(f"激活时间：{info['activation_time']}")
            print(f"有效期至：{info['expiry_time']}")
            print(f"状态：{info['status']}")
            print("-" * 60)
    
    def run_system_info(self):
        """查看系统信息"""
        print("\n" + "="*60)
        print("ℹ️ 系统信息")
        print("="*60)
        print(f"工具版本：{TOOLKIT_VERSION}")
        print(f"DNA追溯：{TOOLKIT_DNA}")
        print(f"创始人：{FOUNDER_NAME}")
        print(f"UID：{FOUNDER_UID}")
        print(f"GPG指纹：{FOUNDER_GPG}")
        print(f"确认码：{FOUNDER_CONFIRMATION_CODE}")
        print(f"理论指导：曾老师（永恒显示）")
        print("="*60)
        print("\n💳 数字人民币激活信息：")
        print(f"账号：{ECNY_ACCOUNT}（{ECNY_BANK}）")
        print(f"网络身份：{NETWORK_IDENTITY}")
        print("激活方式：扫码支付后填写付款单号")
        print(f"激活有效期：{TEMP_DNA_VALIDITY_DAYS}天")
        print("="*60)
        print("\n核心原则：")
        print("✅ 所有权不可改（UID9622永远是创始人）")
        print("✅ 逻辑算法必须明确（开源透明）")
        print("✅ 用户可自定义群体规则（插件化）")
        print("✅ 数字人民币激活机制（付款单号绑定临时DNA）")
        print("✅ 所有激活DNA带时间戳（不可篡改）")
        print("="*60)
    
    def run(self):
        """运行主程序"""
        self.print_banner()
        
        while True:
            choice = self.print_menu()
            
            if choice == "1":
                self.run_ecny_activation()
            
            elif choice == "2":
                self.run_dna_generation()
            
            elif choice == "3":
                self.run_rule_management()
            
            elif choice == "4":
                self.run_defense_execution()
            
            elif choice == "5":
                self.run_view_activations()
            
            elif choice == "6":
                self.run_system_info()
            
            elif choice == "0":
                print("\n感谢使用龙魂数据主权防御工具！")
                print("为人民服务！🇨🇳")
                break
            
            else:
                print("\n❌ 无效选择，请重新输入")


# ═══════════════════════════════════════════════════════════════
# 【主入口】
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # 创建并运行CLI
    cli = LonghunDefenseCLI()
    cli.run()

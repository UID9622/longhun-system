<!--#龍芯⚡️2026-06-21-DOC-CHATGPT_3E6B-v1.0 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

# 🤖 ChatGPT多账号管理器

代码内容: #!/usr/bin/env python3
# -- coding: utf-8 --
"""
UID9622 ChatGPT多账号管理器
专为管理多个ChatGPT账号而设计
支持批量操作、会话管理、使用限额监控
"""

import requests
import json
import time
import random
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import logging
from cryptography.fernet import Fernet
import sqlite3
import csv

class ChatGPTAccountType(Enum):
    FREE = "free"
    PLUS = "plus"
    TEAM = "team"
    ENTERPRISE = "enterprise"

class AccountStatus(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    RATE_LIMITED = "rate_limited"
    EXPIRED = "expired"
    UNKNOWN = "unknown"

@dataclass
class ChatGPTAccount:
    account_id: str
    email: str
    account_type: ChatGPTAccountType
    status: AccountStatus
    session_token: Optional[str] = None
    api_key: Optional[str] = None
    last_used: Optional[datetime] = None
    usage_today: int = 0
    usage_limit: int = 0
    conversations_count: int = 0
    subscription_expires: Optional[datetime] = None
    notes: str = ""
    tags: List[str] = None
    
    def post_init(self):
        if self.tags is None:
            self.tags = []
        if self.last_used is None:
            self.last_used = http://datetime.now()

class ChatGPTAccountManager:
    """
    ChatGPT账号管理器
    专门管理多个ChatGPT账号，支持本地存储和加密
    """
    
    def init(self, workspace_path: str = "./ChatGPT_Manager"):
        self.workspace_path = Path(workspace_path)
        self.accounts: Dict[str, ChatGPTAccount] = {}
        self.session = requests.Session()
        self.setup_environment()
        self.setup_encryption()
        self.setup_database()
        self.setup_logging()
        
    def setup_environment(self):
        """设置工作环境"""
        directories = [
            "data", "logs", "exports", "sessions", 
            "conversations", "backups", "temp"
        ]
        
        for dir_name in directories:
            dir_path = self.workspace_path / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            
        print(f"🤖 ChatGPT账号管理器已初始化: {self.workspace_path}")
        
    def setup_encryption(self):
        """设置加密系统"""
        key_file = self.workspace_path / ".chatgpt_key"
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                self.encryption_key = http://f.read()
        else:
            self.encryption_key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(self.encryption_key)
            key_file.chmod(0o600)
            
        self.cipher = Fernet(self.encryption_key)
        
    def setup_database(self):
        """设置数据库"""
        db_path = self.workspace_path / "chatgpt_accounts.db"
        self.conn = sqlite3.connect(db_path)
        
        # 创建账号表
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS chatgpt_accounts (
                account_id TEXT PRIMARY KEY,
                email_encrypted BLOB,
                account_type TEXT,
                status TEXT,
                session_token_encrypted BLOB,
                api_key_encrypted BLOB,
                last_used TIMESTAMP,
                usage_today INTEGER DEFAULT 0,
                usage_limit INTEGER DEFAULT 0,
                conversations_count INTEGER DEFAULT 0,
                subscription_expires TIMESTAMP,
                notes_encrypted BLOB,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建使用日志表
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id TEXT,
                operation_type TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                details_encrypted BLOB,
                success BOOLEAN,
                response_time REAL
            )
        """)
        
        # 创建会话记录表  
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id TEXT,
                conversation_id TEXT,
                title_encrypted BLOB,
                created_at TIMESTAMP,
                message_count INTEGER DEFAULT 0,
                model_used TEXT
            )
        """)
        
        self.conn.commit()
        
    def setup_logging(self):
        """设置日志系统"""
        log_file = self.workspace_path / "logs" / f"chatgpt_manager_{http://datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=http://logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("ChatGPT_Manager")
        
    def encrypt_data(self, data: str) -> bytes:
        """加密数据"""
        return self.cipher.encrypt(data.encode('utf-8'))
        
    def decrypt_data(self, encrypted_data: bytes) -> str:
        """解密数据"""
        return self.cipher.decrypt(encrypted_data).decode('utf-8')
        
    def add_account(self, 
                   email: str,
                   account_type: ChatGPTAccountType,
                   session_token: str = None,
                   api_key: str = None,
                   notes: str = "",
                   tags: List[str] = None) -> str:
        """添加ChatGPT账号"""
        account_id = http://hashlib.md5(email.encode()).hexdigest()[:12]
        
        # 设置限额
        usage_limits = {
            http://ChatGPTAccountType.FREE: 3,      # 免费版每3小时有限制
            http://ChatGPTAccountType.PLUS: 50,     # Plus版每3小时50条
            http://ChatGPTAccountType.TEAM: 100,    # Team版更高限制
            ChatGPTAccountType.ENTERPRISE: -1 # 企业版无限制
        }
        
        account = ChatGPTAccount(
            account_id=account_id,
            email=email,
            account_type=account_type,
            status=AccountStatus.ACTIVE,
            session_token=session_token,
            api_key=api_key,
            usage_limit=usage_limits.get(account_type, 0),
            notes=notes,
            tags=tags or []
        )
        
        # 加密存储
        email_encrypted = self.encrypt_data(email)
        session_encrypted = self.encrypt_data(session_token) if session_token else None
        api_encrypted = self.encrypt_data(api_key) if api_key else None
        notes_encrypted = self.encrypt_data(notes)
        
        self.conn.execute("""
            INSERT OR REPLACE INTO chatgpt_accounts 
            (account_id, email_encrypted, account_type, status, 
             session_token_encrypted, api_key_encrypted, usage_limit,
             notes_encrypted, tags, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            account_id, email_encrypted, account_type.value, account.status.value,
            session_encrypted, api_encrypted, account.usage_limit,
            notes_encrypted, ','.join(tags or []), http://datetime.now()
        ))
        
        self.conn.commit()
        self.accounts[account_id] = account
        
        http://self.logger.info(f"ChatGPT账号已添加: {email} ({account_type.value})")
        return account_id
        
    def load_accounts(self) -> int:
        """从数据库加载账号"""
        cursor = self.conn.execute("""
            SELECT account_id, email_encrypted, account_type, status,
                   session_token_encrypted, api_key_encrypted, last_used,
                   usage_today, usage_limit, conversations_count,
                   subscription_expires, notes_encrypted, tags
            FROM chatgpt_accounts
        """)
        
        loaded_count = 0
        for row in cursor.fetchall():
            account_id, email_enc, acc_type, status = row[:4]
            session_enc, api_enc, last_used, usage_today = row[4:8]
            usage_limit, conv_count, sub_expires = row[8:11]
            notes_enc, tags = row[11:13]
            
            # 解密数据
            email = self.decrypt_data(email_enc)
            session_token = self.decrypt_data(session_enc) if session_enc else None
            api_key = self.decrypt_data(api_enc) if api_enc else None
            notes = self.decrypt_data(notes_enc) if notes_enc else ""
            
            account = ChatGPTAccount(
                account_id=account_id,
                email=email,
                account_type=ChatGPTAccountType(acc_type),
                status=AccountStatus(status),
                session_token=session_token,
                api_key=api_key,
                last_used=datetime.fromisoformat(last_used) if last_used else None,
                usage_today=usage_today or 0,
                usage_limit=usage_limit or 0,
                conversations_count=conv_count or 0,
                subscription_expires=datetime.fromisoformat(sub_expires) if sub_expires else None,
                notes=notes,
                tags=tags.split(',') if tags else []
            )
            
            self.accounts[account_id] = account
            loaded_count += 1
            
        print(f"✅ 已加载 {loaded_count} 个ChatGPT账号")
        return loaded_count
        
    def check_account_status(self, account_id: str) -> Dict[str, Any]:
        """检查账号状态"""
        if account_id not in self.accounts:
            return {"error": "账号不存在"}
            
        account = self.accounts[account_id]
        
        # 模拟检查账号状态（实际情况下会发送HTTP请求）
        try:
            # 这里可以添加真实的ChatGPT API调用
            status_check = {
                "account_id": account_id,
                "email": http://account.email,
                "type": account.account_type.value,
                "status": "active",  # 模拟结果
                "usage_today": random.randint(0, account.usage_limit) if account.usage_limit > 0 else 0,
                "conversations_today": random.randint(0, 20),
                "last_active": (http://datetime.now() - timedelta(hours=random.randint(0, 24))).isoformat(),
                "subscription_valid": True if account.account_type != http://ChatGPTAccountType.FREE else None,
                "rate_limit_status": "normal",
                "available_models": ["gpt-3.5-turbo", "gpt-4"] if account.account_type == http://ChatGPTAccountType.PLUS else ["gpt-3.5-turbo"]
            }
            
            # 更新账号信息
            account.last_used = http://datetime.now()
            account.usage_today = status_check["usage_today"]
            
            # 记录日志
            self.log_operation(account_id, "status_check", status_check, True, 0.5)
            
            return status_check
            
        except Exception as e:
            error_result = {"error": str(e), "account_id": account_id}
            self._log_operation(account_id, "status_check", error_result, False, 0)
            return error_result
            
    def batch_status_check(self, account_ids: List[str] = None) -> Dict[str, Any]:
        """批量检查账号状态"""
        if account_ids is None:
            account_ids = list(self.accounts.keys())
            
        print(f"🚀 开始批量检查 {len(account_ids)} 个账号的状态")
        
        results = {
            "batch_id": f"batch{http://datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "total": len(account_ids),
            "success": 0,
            "failed": 0,
            "results": [],
            "errors": []
        }
        
        for i, account_id in enumerate(account_ids, 1):
            try:
                status = self.check_account_status(account_id)
                
                if "error" in status:
                    results["errors"].append(status)
                    results["failed"] += 1
                else:
                    results["results"].append(status)
                    results["success"] += 1
                    
                # 显示进度
                if i % 5 == 0 or i == len(account_ids):
                    progress = (i / len(account_ids))  100
                    print(f"r🔄 进度: {progress:.1f}% ({i}/{len(account_ids)})", end="", flush=True)
                    
                # 防止频率限制
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                error = {"account_id": account_id, "error": str(e)}
                results["errors"].append(error)
                results["failed"] += 1
                
        print(f"nn✅ 批量检查完成! 成功: {results['success']}, 失败: {results['failed']}")
        return results
        
    def get_account_summary(self) -> Dict[str, Any]:
        """获取账号概要"""
        if not self.accounts:
            return {"message": "暂无ChatGPT账号"}
            
        # 统计信息
        total = len(self.accounts)
        type_counts = {}
        status_counts = {}
        usage_stats = {"total_usage": 0, "avg_usage": 0}
        
        total_usage = 0
        for account in self.accounts.values():
            # 账号类型统计
            acc_type = account.account_type.value
            type_counts[acc_type] = type_counts.get(acc_type, 0) + 1
            
            # 状态统计
            status = account.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
            
            # 使用量统计
            total_usage += account.usage_today
            
        usage_stats["total_usage"] = total_usage
        usage_stats["avg_usage"] = round(total_usage / total if total > 0 else 0, 2)
        
        return {
            "total_accounts": total,
            "account_types": type_counts,
            "account_status": status_counts,
            "usage_statistics": usage_stats,
            "last_updated": http://datetime.now().isoformat()
        }
        
    def export_accounts(self, format_type: str = "csv", include_sensitive: bool = False) -> str:
        """导出账号列表"""
        timestamp = http://datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format_type.lower() == "csv":
            filename = f"chatgpt_accounts_{timestamp}.csv"
            filepath = self.workspace_path / "exports" / filename
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['account_id', 'email', 'account_type', 'status', 
                             'usage_today', 'usage_limit', 'conversations_count', 'last_used', 'notes']
                
                if include_sensitive:
                    fieldnames.extend(['session_token', 'api_key'])
                    
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for account in self.accounts.values():
                    row = {
                        'account_id': account.account_id,
                        'email': http://account.email,
                        'account_type': account.account_type.value,
                        'status': account.status.value,
                        'usage_today': account.usage_today,
                        'usage_limit': account.usage_limit,
                        'conversations_count': account.conversations_count,
                        'last_used': account.last_used.isoformat() if account.last_used else '',
                        'notes': account.notes
                    }
                    
                    if include_sensitive:
                        row['session_token'] = account.session_token or ''
                        row['api_key'] = account.api_key or ''
                        
                    writer.writerow(row)
                    
        elif format_type.lower() == "json":
            filename = f"chatgpt_accounts_{timestamp}.json"
            filepath = self.workspace_path / "exports" / filename
            
            accounts_data = []
            for account in self.accounts.values():
                account_dict = asdict(account)
                if not include_sensitive:
                    account_dict.pop('session_token', None)
                    account_dict.pop('api_key', None)
                    
                # 处理日期序列化
                for key, value in account_dict.items():
                    if isinstance(value, datetime):
                        account_dict[key] = value.isoformat() if value else None
                    elif isinstance(value, Enum):
                        account_dict[key] = value.value
                        
                accounts_data.append(account_dict)
                
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(accounts_data, f, indent=2, ensure_ascii=False)
                
        print(f"📊 账号列表已导出: {filepath}")
        return str(filepath)
        
    def _log_operation(self, account_id: str, operation: str, details: Dict, 
                      success: bool, response_time: float):
        """记录操作日志"""
        details_encrypted = self.encrypt_data(json.dumps(details))
        
        self.conn.execute("""
            INSERT INTO usage_logs 
            (account_id, operation_type, details_encrypted, success, response_time)
            VALUES (?, ?, ?, ?, ?)
        """, (account_id, operation, details_encrypted, success, response_time))
        
        self.conn.commit()
        
    def create_sample_accounts(self, count: int = 25) -> int:
        """创建示例账号用于测试"""
        account_types = [http://ChatGPTAccountType.FREE, http://ChatGPTAccountType.PLUS, http://ChatGPTAccountType.TEAM]
        created = 0
        
        for i in range(count):
            email = f"testuser{i+1:mailto:03d}@example.com"
            acc_type = random.choice(account_types)
            
            account_id = self.add_account(
                email=email,
                account_type=acc_type,
                notes=f"测试账号 #{i+1}",
                tags=["test", "internal", acc_type.value]
            )
            
            created += 1
            
        print(f"🎆 已创建 {created} 个示例ChatGPT账号")
        return created
        
    def print_summary_report(self):
        """打印概要报告"""
        summary = self.get_account_summary()
        
        print("n" + "="60)
        print("🤖 UID9622 ChatGPT账号管理器 - 概要报告")
        print("="60)
        
        if "message" in summary:
            print(summary["message"])
            return
            
        print(f"💳 总ChatGPT账号数: {summary['total_accounts']}")
        
        print("n🌐 账号类型分布:")
        for acc_type, count in summary['account_types'].items():
            print(f"  {acc_type}: {count} 个")
            
        print("n🟢 账号状态:")
        for status, count in summary['account_status'].items():
            print(f"  {status}: {count} 个")
            
        print("n📊 使用统计:")
        usage = summary['usage_statistics']
        print(f"  总使用量: {usage['total_usage']}")
        print(f"  平均使用量: {usage['avg_usage']}")
        
        print("="60)
        
    def close(self):
        """关闭管理器"""
        if hasattr(self, 'conn'):
            self.conn.close()
        self.session.close()
        print("🔒 ChatGPT账号管理器已关闭")

# 使用示例
def demo_chatgpt_manager():
    """演示ChatGPT账号管理器的使用"""
    # 初始化管理器
    manager = ChatGPTAccountManager()
    
    # 创建示例账号（你可以换成真实账号）
    manager.create_sample_accounts(25)
    
    # 显示概要
    manager.print_summary_report()
    
    # 批量检查状态
    batch_result = manager.batch_status_check()
    
    # 导出结果
    export_path = manager.export_accounts("csv")
    
    return manager

if name == "main":
    chatgpt_manager = demo_chatgpt_manager()
使用说明: [原说明保持]

---
## 不可公开项清单（绝密）
- 任何与账号、API Key、会话令牌相关的信息
- 频率控制与风控绕过策略
- 加密与存储细节参数

仅可分享高层设计，不得附带实现细节。
依赖项: requests, selenium(可选), cryptography
兼容性检查: No
创建时间: 2025年9月5日
功能类型: 自动化脚本
升级说明: # 合规提示
- 保持绝密；若需对外展示，提供概念级架构图与合规声明即可。
复杂程度: 高级
安全等级: 绝密
应用场景: 数据管理, 用户服务, 系统保护
执行状态: 已封存
技术栈: Python
智能体贡献者: 中枢, [助手昵称], [家人]
本地运行: Yes
版本号: v1.0-CHATGPT
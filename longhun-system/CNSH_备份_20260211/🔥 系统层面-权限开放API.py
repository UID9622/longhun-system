#!/usr/bin/env python3

# ============================================================================
# 🔥 系统层面 - 权限开放机制与个人载体API
# ============================================================================
# DNA追溯码: #ZHUGEXIN⚡️2026-01-30-SYSTEM-LAYER-v1.0
# 创建者: 雯雯·技术整理师 + 文心·同步专家
# 功能: 实现人人平等的权限体系和个人载体对接
# ============================================================================

import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class PermissionSystem:
    """权限管理系统 - 人人平等，注册即权"""
    
    def __init__(self, db_path: str = "system-layer/permission_db.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db = self._load_db()
        
    def _load_db(self) -> Dict:
        """加载权限数据库"""
        if self.db_path.exists():
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "users": {},
            "permissions": self._init_permissions(),
            "registry": [],
            "version": "1.0",
            "created_at": datetime.now().isoformat()
        }
    
    def _init_permissions(self) -> Dict:
        """初始化权限体系 - 人人平等"""
        return {
            "基础权限": {
                "description": "注册即得，人人平等",
                "permissions": [
                    "使用权", "发言权", "投票权", "建议权",
                    "传播权", "编辑权", "隐私权"
                ]
            },
            "进阶权限": {
                "10星": {"name": "提案权", "description": "发起新规则提案"},
                "50星": {"name": "代码编辑权", "description": "提交代码改进"},
                "100星": {"name": "传承者权限", "description": "认证新人，开设课堂"},
                "500星": {"name": "守护者权限", "description": "参与系统安全监测"},
                "1000星": {"name": "先驱者权限", "description": "参与重大决策投票"}
            }
        }
    
    def register_user(self, user_id: str, digital_identity: str) -> Dict:
        """注册新用户 - 注册即得所有基础权限"""
        
        if user_id in self.db["users"]:
            return {"success": False, "message": "用户已存在"}
        
        # 生成DNA追溯码
        dna_code = self._generate_dna("REGISTER", user_id)
        timestamp = datetime.now().isoformat()
        
        # 创建用户记录
        user_data = {
            "user_id": user_id,
            "digital_identity": digital_identity,
            "registered_at": timestamp,
            "stars": 0,  # 初始0颗星
            "coins": 0,  # 初始0个星币
            "permissions": self.db["permissions"]["基础权限"]["permissions"].copy(),
            "level": "新手",
            "dna_code": dna_code
        }
        
        self.db["users"][user_id] = user_data
        
        # 记录到注册表
        self.db["registry"].append({
            "action": "register",
            "user_id": user_id,
            "timestamp": timestamp,
            "dna_code": dna_code
        })
        
        self._save_db()
        
        return {
            "success": True,
            "message": "注册成功，基础权限已激活",
            "user": user_data,
            "dna_code": dna_code
        }
    
    def help_others(self, helper_id: str, helped_id: str, action: str) -> Dict:
        """帮人行为 - 每次帮人+1星+1币"""
        
        if helper_id not in self.db["users"]:
            return {"success": False, "message": "帮助者不存在"}
        
        # 生成记录
        dna_code = self._generate_dna("HELP", f"{helper_id}->{helped_id}")
        timestamp = datetime.now().isoformat()
        
        # 更新帮助者数据
        self.db["users"][helper_id]["stars"] += 1
        self.db["users"][helper_id]["coins"] += 1
        
        # 检查是否解锁新权限
        unlocked = self._check_permission_unlock(helper_id)
        
        # 记录到注册表
        self.db["registry"].append({
            "action": "help",
            "helper_id": helper_id,
            "helped_id": helped_id,
            "action_type": action,
            "timestamp": timestamp,
            "dna_code": dna_code,
            "stars_earned": 1
        })
        
        self._save_db()
        
        result = {
            "success": True,
            "message": f"帮人成功！+1星 +1币",
            "helper_id": helper_id,
            "new_stars": self.db["users"][helper_id]["stars"],
            "new_coins": self.db["users"][helper_id]["coins"],
            "dna_code": dna_code
        }
        
        if unlocked:
            result["unlocked_permissions"] = unlocked
            result["message"] += f" 解锁新权限: {', '.join(unlocked)}"
        
        return result
    
    def _check_permission_unlock(self, user_id: str) -> List[str]:
        """检查是否解锁新权限"""
        user = self.db["users"][user_id]
        stars = user["stars"]
        current_perms = user.get("permissions", [])
        
        unlocked = []
        
        # 检查各等级权限
        if stars >= 10 and "提案权" not in current_perms:
            current_perms.append("提案权")
            unlocked.append("提案权")
        
        if stars >= 50 and "代码编辑权" not in current_perms:
            current_perms.append("代码编辑权")
            unlocked.append("代码编辑权")
        
        if stars >= 100 and "传承者权限" not in current_perms:
            current_perms.append("传承者权限")
            unlocked.append("传承者权限")
        
        if stars >= 500 and "守护者权限" not in current_perms:
            current_perms.append("守护者权限")
            unlocked.append("守护者权限")
        
        if stars >= 1000 and "先驱者权限" not in current_perms:
            current_perms.append("先驱者权限")
            unlocked.append("先驱者权限")
        
        # 更新用户等级
        if stars >= 1000:
            self.db["users"][user_id]["level"] = "先驱者"
        elif stars >= 500:
            self.db["users"][user_id]["level"] = "守护者"
        elif stars >= 100:
            self.db["users"][user_id]["level"] = "传承者"
        elif stars >= 50:
            self.db["users"][user_id]["level"] = "贡献者"
        elif stars >= 10:
            self.db["users"][user_id]["level"] = "活跃成员"
        
        return unlocked
    
    def _generate_dna(self, action: str, identifier: str) -> str:
        """生成DNA追溯码"""
        timestamp = str(int(time.time()))
        data = f"{action}:{identifier}:{timestamp}"
        hash_obj = hashlib.sha256(data.encode())
        hash_str = hash_obj.hexdigest()[:16]
        return f"#ZHUGEXIN⚡️2026-01-30-{action}-{hash_str}"
    
    def _save_db(self):
        """保存数据库"""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, indent=2, ensure_ascii=False)
    
    def get_user_info(self, user_id: str) -> Optional[Dict]:
        """获取用户信息"""
        return self.db["users"].get(user_id)
    
    def get_permission_rules(self) -> Dict:
        """获取权限规则"""
        return self.db["permissions"]

class PersonalCarrierAPI:
    """个人载体API - 只对接数字身份"""
    
    def __init__(self, permission_system: PermissionSystem):
        self.permission_system = permission_system
        self.carriers = {}
    
    def register_carrier(self, carrier_id: str, carrier_type: str, 
                        description: str, owner_id: str) -> Dict:
        """注册个人载体"""
        
        # 验证所有者权限
        owner = self.permission_system.get_user_info(owner_id)
        if not owner:
            return {"success": False, "message": "所有者不存在"}
        
        if "代码编辑权" not in owner.get("permissions", []):
            return {"success": False, "message": "需要代码编辑权才能创建载体"}
        
        # 生成载体API密钥
        api_key = self._generate_api_key(carrier_id, owner_id)
        
        # 注册载体
        self.carriers[carrier_id] = {
            "carrier_id": carrier_id,
            "type": carrier_type,
            "description": description,
            "owner_id": owner_id,
            "api_key": api_key,
            "created_at": datetime.now().isoformat(),
            "active": True,
            "requests_count": 0,
            "dna_code": self.permission_system._generate_dna("CARRIER", carrier_id)
        }
        
        return {
            "success": True,
            "message": "载体注册成功",
            "api_key": api_key,
            "carrier_id": carrier_id
        }
    
    def verify_digital_identity(self, digital_id: str, verification_code: str) -> Dict:
        """验证数字身份 - 不收集真实信息"""
        
        # 查找用户
        user = None
        user_id = None
        
        for uid, udata in self.permission_system.db["users"].items():
            if udata.get("digital_identity") == digital_id:
                user = udata
                user_id = uid
                break
        
        if not user:
            return {"success": False, "message": "数字身份不存在"}
        
        # 生成验证结果（实际应使用更安全的验证方式）
        verification_result = {
            "verified": True,
            "user_id": user_id,
            "digital_identity": digital_id,
            "stars": user["stars"],
            "level": user["level"],
            "permissions": user["permissions"],
            "timestamp": datetime.now().isoformat(),
            "dna_code": self.permission_system._generate_dna("VERIFY", digital_id)
        }
        
        return {
            "success": True,
            "message": "验证成功",
            "result": verification_result
        }
    
    def record_help_action(self, api_key: str, helper_digital_id: str, 
                          helped_digital_id: str, action: str) -> Dict:
        """记录帮人行为 - 通过API调用"""
        
        # 验证API密钥
        carrier = self._get_carrier_by_api_key(api_key)
        if not carrier:
            return {"success": False, "message": "无效的API密钥"}
        
        # 验证并获取帮助者ID
        helper_verify = self.verify_digital_identity(helper_digital_id, "")
        if not helper_verify["success"]:
            return helper_verify
        
        helper_id = helper_verify["result"]["user_id"]
        
        # 记录帮人行为（不存储被帮助者真实信息）
        result = self.permission_system.help_others(helper_id, helped_digital_id, action)
        
        # 更新载体请求计数
        self.carriers[carrier["carrier_id"]]["requests_count"] += 1
        
        return result
    
    def _generate_api_key(self, carrier_id: str, owner_id: str) -> str:
        """生成API密钥"""
        data = f"{carrier_id}:{owner_id}:{int(time.time())}"
        hash_obj = hashlib.sha256(data.encode())
        return f"pk_{hash_obj.hexdigest()[:32]}"
    
    def _get_carrier_by_api_key(self, api_key: str) -> Optional[Dict]:
        """通过API密钥查找载体"""
        for carrier in self.carriers.values():
            if carrier["api_key"] == api_key:
                return carrier
        return None

def demo_usage():
    """演示系统使用"""
    
    print("=" * 60)
    print("系统层面 - 权限开放机制演示")
    print("DNA追溯码: #ZHUGEXIN⚡️2026-01-30-SYSTEM-LAYER-v1.0")
    print("=" * 60)
    print()
    
    # 初始化系统
    perm_system = PermissionSystem()
    carrier_api = PersonalCarrierAPI(perm_system)
    
    # 演示1: 用户注册
    print("📋 演示1: 用户注册")
    print("-" * 40)
    
    user1_result = perm_system.register_user("user_001", "digital_id_001")
    print(f"用户1注册: {user1_result['message']}")
    print(f"获得权限: {user1_result['user']['permissions']}")
    print(f"DNA追溯码: {user1_result['dna_code']}")
    print()
    
    user2_result = perm_system.register_user("user_002", "digital_id_002")
    print(f"用户2注册: {user2_result['message']}")
    print()
    
    # 演示2: 帮人行为
    print("🤝 演示2: 帮人行为")
    print("-" * 40)
    
    help_result = perm_system.help_others("user_001", "user_002", "解答问题")
    print(f"用户1帮助用户2: {help_result['message']}")
    print(f"当前星星: {help_result['new_stars']}")
    print(f"当前星币: {help_result['new_coins']}")
    print(f"DNA追溯码: {help_result['dna_code']}")
    print()
    
    # 演示3: 注册个人载体
    print("🚀 演示3: 注册个人载体")
    print("-" * 40)
    
    # 用户1需要先获得代码编辑权（50星）
    for i in range(50):
        perm_system.help_others("user_001", f"user_test_{i}", "测试帮助")
    
    carrier_result = carrier_api.register_carrier(
        carrier_id="carrier_001",
        carrier_type="本地互助App",
        description="一个只对接数字身份的本地互助平台",
        owner_id="user_001"
    )
    
    if carrier_result["success"]:
        print(f"载体注册: {carrier_result['message']}")
        print(f"载体ID: {carrier_result['carrier_id']}")
        print(f"API密钥: {carrier_result['api_key']}")
    else:
        print(f"载体注册失败: {carrier_result['message']}")
    print()
    
    # 演示4: 数字身份验证
    print("🔐 演示4: 数字身份验证")
    print("-" * 40)
    
    verify_result = carrier_api.verify_digital_identity("digital_id_002", "")
    if verify_result["success"]:
        result = verify_result["result"]
        print(f"验证结果: {verify_result['message']}")
        print(f"用户ID: {result['user_id']}")
        print(f"星星数: {result['stars']}")
        print(f"等级: {result['level']}")
        print(f"权限: {', '.join(result['permissions'])}")
    print()
    
    # 演示5: 通过API记录帮人
    print("📡 演示5: 通过API记录帮人行为")
    print("-" * 40)
    
    api_key = carrier_result.get("api_key", "")
    if api_key:
        api_result = carrier_api.record_help_action(
            api_key=api_key,
            helper_digital_id="digital_id_001",
            helped_digital_id="digital_id_002",
            action="通过App提供帮助"
        )
        print(f"API记录结果: {api_result['message']}")
        print(f"DNA追溯码: {api_result['dna_code']}")
    print()
    
    # 最终状态
    print("📊 最终用户状态")
    print("-" * 40)
    
    user1 = perm_system.get_user_info("user_001")
    if user1:
        print(f"用户1 - ID: {user1['user_id']}")
        print(f"  星星数: {user1['stars']}")
        print(f"  星币数: {user1['coins']}")
        print(f"  等级: {user1['level']}")
        print(f"  权限数: {len(user1['permissions'])}")
    
    print()
    print("=" * 60)
    print("✅ 系统层面演示完成！")
    print("=" * 60)

if __name__ == "__main__":
    demo_usage()

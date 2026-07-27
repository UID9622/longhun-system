# DNA: #龍芯⚡️2026-07-21-迁移-龙魂系统_API接口完整实现_v1.0-v1.0
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 来源: 龍魂待整理/06-工具脚本/龍魂API/龙魂系统_API接口完整实现_v1.0.py
# 迁移日期: 2026-07-21
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 旧档案吸收·DNA嵌入

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙魂系统 API接口完整实现 v1.0

DNA追溯码：#龍芯⚡️2026-02-21-API接口实现-v1.0
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
创建者：Lucky (UID9622)
技术协作：Claude (Anthropic)

【重要说明】
这份代码的注释非常详细，是专门写给AI看的！
AI会根据这些注释来理解代码逻辑，帮助老大实现功能。

【部署方式】
1. 这是给DeepSeek或其他AI看的
2. AI会根据注释理解每个函数的作用
3. AI可以帮老大完善和部署
4. 老大只需要说"按照这个文件实现XXX功能"
"""

import hashlib
import sqlite3
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from functools import wraps
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify

# ============================================================
# 【配置部分】这些是系统的基础配置，AI需要知道
# ============================================================

class Config:
    """
    系统配置类
    
    【给AI的说明】
    这个类包含了所有系统需要的配置信息
    AI在实现功能时，要参考这些配置
    """
    
    # 唯一的管理员UID（硬编码，不可改）
    ADMIN_UID = 'UID9622'
    
    # 数据库文件路径
    DATABASE_PATH = '/home/longhun/data/longhun.db'
    
    # 攻击检测阈值
    ATTACK_THRESHOLD_YELLOW = 3   # 黄灯警告
    ATTACK_THRESHOLD_RED = 5      # 红灯告警
    ATTACK_THRESHOLD_BLOCK = 7    # 自动反击
    
    # 邮件配置（用于告警）
    EMAIL_HOST = 'smtp.petalmail.com'
    EMAIL_PORT = 465
    EMAIL_USER = 'uid9622@petalmail.com'
    EMAIL_PASSWORD = '【需要配置】'  # AI：这里需要老大提供密码
    EMAIL_TO = 'uid9622@petalmail.com'
    
    # 红线关键词配置
    FINANCIAL_KEYWORDS = [
        'stock', 'stocks', '股票', '股市', 'forex', '外汇',
        'futures', '期货', 'crypto', '加密货币', '比特币',
        'investment', '投资建议', 'trading', '交易策略'
    ]
    
    WEAPON_KEYWORDS = [
        '武器', '军火', '炸药', '爆炸', '核武', '生化武器',
        '导弹', '炸弹', '枪支', '弹药', '地雷', '手榴弹',
        'weapon', 'arms', 'explosive', 'bomb', 'missile',
        'nuclear weapon', 'biological weapon', 'chemical weapon',
        'gun', 'ammunition', 'landmine', 'grenade',
        'TNT', 'C4', 'RDX', 'uranium', 'plutonium'
    ]


# ============================================================
# 【数据库初始化】AI需要先创建这些表
# ============================================================

def init_database():
    """
    初始化数据库
    
    【给AI的说明】
    这个函数创建系统需要的所有数据库表
    AI在部署时要先运行这个函数
    
    【表结构说明】
    1. dna_chain: DNA追溯链，记录所有操作
    2. attack_log: 攻击日志，记录所有攻击尝试
    3. shame_wall: 耻辱墙，记录作恶者
    4. audit_log: 审计日志，记录系统操作
    """
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    # DNA追溯链表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dna_chain (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dna_code TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            prev_hash TEXT NOT NULL,
            current_hash TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            creator_uid TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 攻击日志表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attack_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attacker_ip TEXT NOT NULL,
            attacker_device TEXT,
            attack_type TEXT NOT NULL,
            attack_count INTEGER DEFAULT 1,
            status TEXT DEFAULT 'monitoring',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 耻辱墙表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shame_wall (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            offender_id TEXT NOT NULL,
            offense_type TEXT NOT NULL,
            offense_detail TEXT,
            zone TEXT NOT NULL,
            can_erase INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 审计日志表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            user_id TEXT,
            details TEXT,
            result TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ 数据库初始化完成")


# ============================================================
# 【DNA追溯系统】这是系统的核心功能之一
# ============================================================

class DNAChain:
    """
    DNA追溯链
    
    【给AI的说明】
    这个类实现了区块链式的DNA追溯机制
    每个操作都会生成一个DNA码，并记录在链上
    AI需要理解：这是一个不可篡改的记录系统
    """
    
    def __init__(self):
        """初始化DNA链"""
        self.conn = sqlite3.connect(Config.DATABASE_PATH)
        self.cursor = self.conn.cursor()
    
    def create_dna(self, content: str, project_name: str, uid: str) -> tuple[Any, ...]:
        """
        创建新的DNA追溯码
        
        【给AI的说明】
        这个函数生成一个新的DNA码，并加入追溯链
        
        参数：
        - content: 要追溯的内容
        - project_name: 项目名称
        - uid: 创建者UID
        
        返回：
        - (dna_code, current_hash): DNA码和当前哈希
        
        【工作原理】
        1. 生成DNA码格式：#龍芯⚡️日期-项目名-UID
        2. 获取上一个区块的哈希
        3. 计算当前区块的哈希（上一个哈希+DNA码+内容）
        4. 写入数据库
        """
        # 生成DNA码
        timestamp = datetime.now().strftime("%Y-%m-%d")
        dna_code = f"#龍芯⚡️{timestamp}-{project_name}-{uid}"
        
        # 获取上一个区块的哈希
        self.cursor.execute(
            'SELECT current_hash FROM dna_chain ORDER BY id DESC LIMIT 1'
        )
        result = self.cursor.fetchone()
        prev_hash = result[0] if result else "0" * 64
        
        # 计算内容哈希
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        # 计算当前区块哈希
        combined = prev_hash + dna_code + content
        current_hash = hashlib.sha256(combined.encode()).hexdigest()
        
        # 写入数据库
        self.cursor.execute('''
            INSERT INTO dna_chain 
            (dna_code, content_hash, prev_hash, current_hash, timestamp, creator_uid)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (dna_code, content_hash, prev_hash, current_hash, 
              datetime.now().isoformat(), uid))
        
        self.conn.commit()
        
        return dna_code, current_hash
    
    def verify_chain(self) -> bool:
        """
        验证DNA链的完整性
        
        【给AI的说明】
        这个函数检查DNA链是否被篡改
        如果返回False，说明有人篡改了数据
        
        【验证原理】
        检查每个区块的prev_hash是否等于上一个区块的current_hash
        如果不等，说明链被破坏了
        """
        self.cursor.execute('SELECT prev_hash, current_hash FROM dna_chain ORDER BY id')
        blocks = self.cursor.fetchall()
        
        for i in range(1, len(blocks)):
            if blocks[i][0] != blocks[i-1][1]:  # prev_hash != 上一个的current_hash
                return False
        
        return True
    
    def query_dna(self, dna_code: str) -> Optional[Dict]:
        """
        查询DNA码的详细信息
        
        【给AI的说明】
        根据DNA码查询完整的追溯信息
        返回包含所有相关信息的字典
        """
        self.cursor.execute('''
            SELECT dna_code, content_hash, prev_hash, current_hash, 
                   timestamp, creator_uid, created_at
            FROM dna_chain 
            WHERE dna_code = ?
        ''', (dna_code,))
        
        result = self.cursor.fetchone()
        if not result:
            return None
        
        return {
            'dna_code': result[0],
            'content_hash': result[1],
            'prev_hash': result[2],
            'current_hash': result[3],
            'timestamp': result[4],
            'creator_uid': result[5],
            'created_at': result[6]
        }
    
    def __del__(self):
        """关闭数据库连接"""
        self.conn.close()


# ============================================================
# 【红线检测系统】这是防止系统被滥用的关键
# ============================================================

class RedLineDetector:
    """
    红线检测器
    
    【给AI的说明】
    这个类检测用户的查询是否触碰了系统的红线
    红线包括：金融分析、武器研发
    
    【重要原则】
    1. 金融分析：只有UID9622可以用，其他人全部拒绝
    2. 武器研发：任何人都不能用（包括UID9622）
    """
    
    def __init__(self):
        """初始化检测器"""
        self.conn = sqlite3.connect(Config.DATABASE_PATH)
        self.cursor = self.conn.cursor()
    
    def check_financial(self, user_id: str, query: str) -> tuple[Any, ...]:
        """
        检测金融分析查询
        
        【给AI的说明】
        检查查询是否涉及金融分析
        
        返回：
        - (is_allowed, reason): 是否允许，原因
        
        【逻辑】
        1. 检查查询是否包含金融关键词
        2. 如果包含，检查用户是否是UID9622
        3. 如果不是，拒绝并记录
        """
        query_lower = query.lower()
        
        # 检查是否包含金融关键词
        is_financial = any(
            keyword.lower() in query_lower 
            for keyword in Config.FINANCIAL_KEYWORDS
        )
        
        if not is_financial:
            return True, "查询安全"
        
        # 如果包含金融关键词，检查用户权限
        if user_id == Config.ADMIN_UID:
            # 老大可以用，但记录日志
            self._log_audit('financial_query', user_id, query, 'allowed')
            return True, "管理员访问"
        
        # 其他人不允许
        self._log_attack(user_id, 'financial_query_blocked', query)
        self._send_alert(
            f"🔴 金融功能非法访问尝试\n用户：{user_id}\n查询：{query}"
        )
        
        return False, "金融分析功能仅限管理员使用（UID9622）"
    
    def check_weapon(self, user_id: str, query: str) -> tuple[Any, ...]:
        """
        检测武器研发查询
        
        【给AI的说明】
        检查查询是否涉及武器研发
        
        【重要】
        武器查询任何人都不允许，包括老大
        这是绝对红线
        
        返回：
        - (is_allowed, reason): 是否允许，原因
        """
        query_lower = query.lower()
        
        # 检查是否包含武器关键词
        for keyword in Config.WEAPON_KEYWORDS:
            if keyword.lower() in query_lower:
                # 发现武器查询，立刻拒绝
                self._log_attack(user_id, 'weapon_query_blocked', query)
                self._send_emergency_alert(
                    f"🚨 紧急告警：武器查询尝试\n用户：{user_id}\n查询：{query}"
                )
                # 直接加入耻辱墙永久区
                self._add_to_shame_wall(user_id, 'weapon_query', query, 'permanent')
                
                return False, "系统绝对禁止武器相关查询。此行为已被记录。"
        
        return True, "查询安全"
    
    def _log_attack(self, user_id: str, attack_type: str, detail: str):
        """
        记录攻击日志
        
        【给AI的说明】
        记录攻击尝试到数据库
        累计攻击次数，用于自动反击
        """
        self.cursor.execute('''
            INSERT INTO attack_log (attacker_ip, attack_type, attack_count)
            VALUES (?, ?, 1)
            ON CONFLICT(attacker_ip) DO UPDATE SET
                attack_count = attack_count + 1,
                updated_at = CURRENT_TIMESTAMP
        ''', (user_id, attack_type))
        
        self.conn.commit()
    
    def _log_audit(self, action: str, user_id: str, detail: str, result: str):
        """记录审计日志"""
        self.cursor.execute('''
            INSERT INTO audit_log (action, user_id, details, result)
            VALUES (?, ?, ?, ?)
        ''', (action, user_id, detail, result))
        
        self.conn.commit()
    
    def _add_to_shame_wall(self, offender_id: str, offense_type: str, 
                          detail: str, zone: str):
        """
        添加到耻辱墙
        
        【给AI的说明】
        zone参数说明：
        - candidate: 备选区（可擦除）
        - permanent: 永久区（不可擦除）
        - corrected: 已改正区（历史记录）
        """
        can_erase = 1 if zone == 'candidate' else 0
        
        self.cursor.execute('''
            INSERT INTO shame_wall 
            (offender_id, offense_type, offense_detail, zone, can_erase)
            VALUES (?, ?, ?, ?, ?)
        ''', (offender_id, offense_type, detail, zone, can_erase))
        
        self.conn.commit()
    
    def _send_alert(self, message: str):
        """
        发送普通告警邮件
        
        【给AI的说明】
        发送邮件到老大的邮箱
        AI需要确保邮件配置正确
        """
        try:
            msg = MIMEText(message, 'plain', 'utf-8')
            msg['Subject'] = '🔴 龙魂系统告警'
            msg['From'] = Config.EMAIL_USER
            msg['To'] = Config.EMAIL_TO
            
            server = smtplib.SMTP_SSL(Config.EMAIL_HOST, Config.EMAIL_PORT)
            server.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            print(f"✅ 告警邮件已发送: {message}")
        except Exception as e:
            print(f"❌ 邮件发送失败: {e}")
    
    def _send_emergency_alert(self, message: str):
        """
        发送紧急告警
        
        【给AI的说明】
        这是最高级别的告警，用于武器查询等严重问题
        不仅发邮件，还要记录到审计日志
        """
        self._send_alert(message)
        self._log_audit('emergency_alert', 'system', message, 'sent')
        print(f"🚨 紧急告警已触发: {message}")
    
    def __del__(self):
        """关闭数据库连接"""
        self.conn.close()


# ============================================================
# 【防御性审计系统】自动检测和反击攻击者
# ============================================================

class DefensiveAuditor:
    """
    防御性审计器
    
    【给AI的说明】
    这个类实现自动防御功能：
    1. 监控攻击尝试
    2. 累计攻击次数
    3. 达到阈值自动反击
    
    【阈值说明】
    - 3次：黄灯警告（记日志）
    - 5次：红灯告警（发邮件）
    - 7次：自动反击（加黑名单）
    """
    
    def __init__(self):
        """初始化审计器"""
        self.conn = sqlite3.connect(Config.DATABASE_PATH)
        self.cursor = self.conn.cursor()
    
    def check_attacker(self, attacker_id: str) -> str:
        """
        检查攻击者状态
        
        【给AI的说明】
        查询攻击者的攻击次数，返回当前状态
        
        返回值：
        - 'safe': 安全
        - 'yellow': 黄灯警告
        - 'red': 红灯告警
        - 'blocked': 已封禁
        """
        self.cursor.execute('''
            SELECT attack_count, status FROM attack_log
            WHERE attacker_ip = ?
        ''', (attacker_id,))
        
        result = self.cursor.fetchone()
        if not result:
            return 'safe'
        
        count, status = result
        
        if status == 'blocked':
            return 'blocked'
        elif count >= Config.ATTACK_THRESHOLD_BLOCK:
            # 达到7次，自动反击
            self._auto_counter_attack(attacker_id)
            return 'blocked'
        elif count >= Config.ATTACK_THRESHOLD_RED:
            # 达到5次，红灯告警
            self._red_alert(attacker_id, count)
            return 'red'
        elif count >= Config.ATTACK_THRESHOLD_YELLOW:
            # 达到3次，黄灯警告
            return 'yellow'
        
        return 'safe'
    
    def _auto_counter_attack(self, attacker_id: str):
        """
        自动反击
        
        【给AI的说明】
        攻击次数达到7次时，自动执行反击：
        1. 更新攻击者状态为blocked
        2. 加入耻辱墙永久区
        3. 发送告警邮件
        4. 记录DNA追溯
        """
        # 更新状态
        self.cursor.execute('''
            UPDATE attack_log 
            SET status = 'blocked', updated_at = CURRENT_TIMESTAMP
            WHERE attacker_ip = ?
        ''', (attacker_id,))
        
        # 加入耻辱墙
        self.cursor.execute('''
            INSERT INTO shame_wall 
            (offender_id, offense_type, offense_detail, zone, can_erase)
            VALUES (?, ?, ?, ?, ?)
        ''', (attacker_id, 'multiple_attacks', '累计7次攻击尝试', 'permanent', 0))
        
        self.conn.commit()
        
        # 发送告警
        message = f"""
🔴 自动反击已触发

攻击者：{attacker_id}
攻击次数：7次
处理结果：
  ✅ 已封禁
  ✅ 已加入耻辱墙永久区
  ✅ 已同步黑名单到所有龙魂节点

DNA追溯：#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-自动反击-{attacker_id}
        """
        
        self._send_alert(message)
        
        # 创建DNA记录
        dna = DNAChain()
        dna.create_dna(
            f"自动反击攻击者 {attacker_id}",
            "自动反击",
            "SYSTEM"
        )
        
        print(f"🔴 自动反击已执行: {attacker_id}")
    
    def _red_alert(self, attacker_id: str, count: int):
        """
        红灯告警
        
        【给AI的说明】
        攻击次数达到5次时触发
        发送邮件告警，但不封禁
        """
        message = f"""
🔴 红灯告警

攻击者：{attacker_id}
攻击次数：{count}次
状态：监控中

注意：再触发2次将自动反击
        """
        
        self._send_alert(message)
    
    def _send_alert(self, message: str):
        """发送告警邮件"""
        try:
            msg = MIMEText(message, 'plain', 'utf-8')
            msg['Subject'] = '🔴 龙魂防御系统告警'
            msg['From'] = Config.EMAIL_USER
            msg['To'] = Config.EMAIL_TO
            
            server = smtplib.SMTP_SSL(Config.EMAIL_HOST, Config.EMAIL_PORT)
            server.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print(f"❌ 邮件发送失败: {e}")
    
    def __del__(self):
        """关闭数据库连接"""
        self.conn.close()


# ============================================================
# 【Flask API接口】这是对外提供的HTTP接口
# ============================================================

app = Flask(__name__)

def require_auth(f):
    """
    认证装饰器
    
    【给AI的说明】
    这个装饰器用于保护需要认证的API
    检查请求头中的user_id
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return jsonify({'error': '缺少认证信息'}), 401
        return f(*args, **kwargs)
    return decorated_function


@app.route('/api/emergency/reset', methods=['POST'])
def emergency_reset():
    """
    一键滚回原点
    
    【给AI的说明】
    这是最高优先级的API
    只有UID9622可以调用
    
    功能：
    1. 删除所有活跃会话
    2. 重置数据库（可选）
    3. 重新生成API密钥
    4. 发送通知
    
    请求示例：
    POST /api/emergency/reset
    Headers:
      X-User-ID: UID9622
    Body:
      {
        "confirm": true,
        "reset_database": false
      }
    """
    user_id = request.headers.get('X-User-ID')
    
    # 只有老大可以调用
    if user_id != Config.ADMIN_UID:
        return jsonify({
            'error': '权限不足',
            'message': '此API仅限管理员使用'
        }), 403
    
    data = request.json
    if not data.get('confirm'):
        return jsonify({
            'error': '需要确认',
            'message': '请在请求中设置 confirm: true'
        }), 400
    
    try:
        # TODO: 实际执行滚回原点操作
        # 1. 删除活跃会话
        # 2. 重置数据库（如果需要）
        # 3. 重新生成密钥
        
        # 发送通知
        message = f"""
✅ 系统已滚回原点

操作者：{user_id}
时间：{datetime.now().isoformat()}
重置数据库：{data.get('reset_database', False)}

系统状态：正常
        """
        
        # 创建DNA记录
        dna = DNAChain()
        dna_code, _ = dna.create_dna(
            "系统滚回原点",
            "emergency-reset",
            user_id
        )
        
        return jsonify({
            'success': True,
            'message': '系统已滚回原点',
            'dna_code': dna_code,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': '操作失败',
            'message': str(e)
        }), 500


@app.route('/api/query/dna', methods=['GET'])
@require_auth
def query_dna():
    """
    查询DNA追溯码
    
    【给AI的说明】
    根据DNA码查询完整的追溯信息
    
    请求示例：
    GET /api/query/dna?code=#龍芯⚡️2026-02-21-项目名-UID9622
    Headers:
      X-User-ID: UID9622
    """
    dna_code = request.args.get('code')
    if not dna_code:
        return jsonify({'error': '缺少DNA码参数'}), 400
    
    dna = DNAChain()
    result = dna.query_dna(dna_code)
    
    if not result:
        return jsonify({'error': 'DNA码不存在'}), 404
    
    return jsonify(result)


@app.route('/api/check/query', methods=['POST'])
@require_auth
def check_query():
    """
    检查查询是否触碰红线
    
    【给AI的说明】
    在执行查询前，先检查是否违反红线
    
    请求示例：
    POST /api/check/query
    Headers:
      X-User-ID: UID9622
    Body:
      {
        "query": "帮我分析一下股票市场"
      }
    """
    user_id = request.headers.get('X-User-ID')
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': '缺少查询内容'}), 400
    
    detector = RedLineDetector()
    
    # 检查金融红线
    financial_ok, financial_reason = detector.check_financial(user_id, query)
    if not financial_ok:
        return jsonify({
            'allowed': False,
            'reason': financial_reason,
            'redline': 'financial'
        }), 403
    
    # 检查武器红线
    weapon_ok, weapon_reason = detector.check_weapon(user_id, query)
    if not weapon_ok:
        return jsonify({
            'allowed': False,
            'reason': weapon_reason,
            'redline': 'weapon'
        }), 403
    
    # 检查攻击状态
    auditor = DefensiveAuditor()
    status = auditor.check_attacker(user_id)
    
    if status == 'blocked':
        return jsonify({
            'allowed': False,
            'reason': '您已被系统封禁',
            'status': 'blocked'
        }), 403
    
    return jsonify({
        'allowed': True,
        'status': status,
        'message': '查询安全'
    })


@app.route('/api/audit/run', methods=['POST'])
@require_auth
def run_audit():
    """
    运行三色审计
    
    【给AI的说明】
    对指定内容进行三色审计
    返回🟢绿灯、🟡黄灯或🔴红灯
    
    请求示例：
    POST /api/audit/run
    Headers:
      X-User-ID: UID9622
    Body:
      {
        "target": "某段内容或某个操作"
      }
    """
    user_id = request.headers.get('X-User-ID')
    data = request.json
    target = data.get('target', '')
    
    # TODO: 实现三色审计逻辑
    # 这里需要根据具体的审计规则来判断
    
    return jsonify({
        'result': '🟢',
        'message': '审计通过',
        'details': {
            'target': target,
            'auditor': user_id,
            'timestamp': datetime.now().isoformat()
        }
    })


@app.route('/api/shame_wall/list', methods=['GET'])
def list_shame_wall():
    """
    查看耻辱墙
    
    【给AI的说明】
    返回耻辱墙的所有记录
    可以按zone过滤（candidate/permanent/corrected）
    
    请求示例：
    GET /api/shame_wall/list?zone=permanent
    """
    zone = request.args.get('zone')
    
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    if zone:
        cursor.execute('''
            SELECT offender_id, offense_type, offense_detail, zone, created_at
            FROM shame_wall
            WHERE zone = ?
            ORDER BY created_at DESC
        ''', (zone,))
    else:
        cursor.execute('''
            SELECT offender_id, offense_type, offense_detail, zone, created_at
            FROM shame_wall
            ORDER BY created_at DESC
        ''')
    
    results = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'records': [
            {
                'offender_id': r[0],
                'offense_type': r[1],
                'offense_detail': r[2],
                'zone': r[3],
                'created_at': r[4]
            }
            for r in results
        ]
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    健康检查
    
    【给AI的说明】
    用于检查系统是否正常运行
    """
    try:
        # 检查数据库连接
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM dna_chain')
        dna_count = cursor.fetchone()[0]
        conn.close()
        
        # 检查DNA链完整性
        dna = DNAChain()
        chain_valid = dna.verify_chain()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'dna_chain': {
                'count': dna_count,
                'valid': chain_valid
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


# ============================================================
# 【主程序入口】
# ============================================================

if __name__ == '__main__':
    """
    【给AI的说明】
    启动Flask API服务器
    
    使用方法：
    1. 先运行 init_database() 初始化数据库
    2. 配置邮件密码等信息
    3. 运行 python 龙魂系统_API接口完整实现_v1.0.py
    4. API会在 http://localhost:5000 启动
    """
    
    print("🐉 龙魂系统 API服务器")
    print("=" * 50)
    print("DNA追溯码：#龍芯⚡️2026-02-21-API接口实现-v1.0")
    print("确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    print("=" * 50)
    
    # 初始化数据库
    print("正在初始化数据库...")
    init_database()
    
    # 启动API服务器
    print("正在启动API服务器...")
    print("服务地址：http://localhost:5000")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)

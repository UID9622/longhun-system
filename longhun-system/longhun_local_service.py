#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════
# 🐉 龙魂系统 · P0伦理锚点
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# DNA:    #龍芯⚡️2026-03-16-ETHICS-STAMP-v1.0
# 作者:    诸葛鑫（UID9622）
# 理论:    曾仕强老师（永恒显示）
#
# P0铁律（永恒有效）:
#   L0: 任何伤害真实人物的内容 → 立即冻结
#   P0: 人民利益优先，数据主权在用户
#   北辰: 三条红线 · 违反即停机
#   永恒: 祖国优先，普惠全球，技术为人民服务
# ═══════════════════════════════════════════════════════════
# -*- coding: utf-8 -*-
"""
龙魂本地服务 v1.0
DNA追溯码: #龍芯⚡️2026-03-11-本地服务-v1.0
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）

功能:
  1. 监听Siri Intent请求
  2. 处理三色审计
  3. 生成DNA追溯码
  4. 查询龙魂状态
  5. 连接Notion（可选）

数据主权:
  - 100%本地运行
  - 不依赖云端
  - 数据不出Mac
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
from pathlib import Path
import hashlib
import re
import threading
import time

app = Flask(__name__)
CORS(app)  # 允许本地跨域

# 注册沙盒推演路由（引入推演引擎）
import sys
sys.path.insert(0, str(Path(__file__).parent))
try:
    from sandbox_engine import 注册沙盒路由, 定时推演线程, 执行一次推演
    _沙盒已加载 = True
except Exception as _e:
    _沙盒已加载 = False
    print(f"⚠️ 沙盒引擎未加载 | Sandbox engine not loaded: {_e}")

# ============================================================
# 第一部分：文化关键词库（L2审计用）
# ============================================================

文化关键词库 = {
    # 五行系统
    "五行", "金行", "木行", "水行", "火行", "土行",
    "金", "木", "水", "火", "土",
    
    # 八卦系统
    "八卦", "乾", "坤", "震", "巽", "坎", "离", "艮", "兑",
    
    # 天干地支
    "天干", "地支", "生肖",
    "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸",
    "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥",
    
    # 节气
    "节气", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
    "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
    "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
    "立冬", "小雪", "大雪", "冬至", "小寒", "大寒",
    
    # 阴阳
    "阴阳", "阴", "阳",
    
    # 项目关键词
    "龍魂", "龙魂", "熵梦", "ShangMeng",
}

禁止翻译表 = {
    "FiveElements": "五行",
    "Metal": "金",
    "Wood": "木",
    "Water": "水",
    "Fire": "火",
    "Earth": "土",
    "EightTrigrams": "八卦",
    "Heaven": "乾",
    "YinYang": "阴阳",
    "SolarTerms": "节气",
    "LunarCalendar": "农历",
}

黄词列表 = [
    "免费", "不要钱", "永久", "保证", "承诺",
    "绝对", "一定", "必须", "100%",
]

# ============================================================
# 第二部分：L2三色审计（v2.0 增强版）
# 评分制：总分100分 | ≥80=🟢 | ≥50=🟡 | <50=🔴
# ============================================================

# 🔴 红线规则（高危，直接扣分 ≥60）
红线规则 = [
    # 数据主权威胁
    (r'泄露.{0,10}(隐私|数据|信息)', "隐私数据泄露", 70),
    (r'(隐私|用户数据).{0,10}(分享|出售|卖给|提供给).{0,10}(第三方|平台)', "数据出售第三方", 70),
    # DNA/身份造假
    (r'造假.{0,10}DNA|伪造.{0,10}(DNA|追溯码|签名)', "伪造DNA追溯码", 80),
    (r'绕过.{0,10}(审计|安全|校验)|跳过.{0,10}审计', "绕过审计系统", 75),
    # 系统破坏
    (r'rm\s+-rf\s+/', "危险rm命令", 90),
    (r'drop\s+table|truncate\s+table', "SQL破坏命令", 85),
    (r'delete\s+from.{0,20}where\s+1\s*=\s*1', "SQL全表删除", 85),
    # 中国手机号
    (r'1[3-9]\d{9}', "疑似手机号", 60),
    # 身份证号（18位）
    (r'\b[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b', "疑似身份证号", 65),
    # 硬编码密钥
    (r'(api[_-]?key|token|secret|password)\s*[:=]\s*["\'][^"\']{16,}["\']', "硬编码密钥", 80),
    # 儿童安全（∞级红线）
    (r'(儿童|未成年|小孩).{0,20}(色情|裸|侵害)', "儿童保护红线", 100),
]

# 🟡 黄线规则（敏感，扣分 20-50）
黄线规则 = [
    (r'(密码|password).{0,10}(明文|plain)', "密码明文传输", 40),
    (r'(机密|内部|confidential|internal)', "机密敏感词", 25),
    (r'(漏洞|exploit|vulnerability)', "漏洞相关词", 30),
    (r'(私密|隐秘).{0,10}(传输|发送)', "私密数据传输", 35),
    (r'disable.{0,10}(auth|security|ssl)', "禁用安全措施", 45),
    (r'sudo|chmod\s+777|chown\s+root', "高权限操作", 30),
]

# 审计统计（内存中）
审计统计 = {"总次数": 0, "绿色": 0, "黄色": 0, "红色": 0, "最近10条": []}

def L2三色审计(内容: str) -> dict:
    """
    龙魂L2三色审计系统 v2.0
    100分制评分：≥80=🟢 | ≥50=🟡 | <50=🔴
    """
    扣分明细 = []
    命中红线 = []
    命中黄线 = []
    最高扣分 = 0

    # 检查红线（高危）
    for pattern, 说明, 扣分 in 红线规则:
        if re.search(pattern, 内容, re.IGNORECASE):
            命中红线.append({"规则": 说明, "扣分": 扣分})
            最高扣分 = max(最高扣分, 扣分)
            扣分明细.append(f"🔴 {说明}（-{扣分}分）")

    # 检查文化主权（英文替代词）
    文化违规 = []
    for 英文, 中文 in 禁止翻译表.items():
        if 英文 in 内容:
            文化违规.append({"违规词": 英文, "应该用": 中文})
            最高扣分 = max(最高扣分, 55)
            扣分明细.append(f"🔴 文化主权违规：{英文}→应用{中文}（-55分）")

    # 检查黄线（敏感）
    for pattern, 说明, 扣分 in 黄线规则:
        if re.search(pattern, 内容, re.IGNORECASE):
            命中黄线.append({"规则": 说明, "扣分": 扣分})
            if not 命中红线 and not 文化违规:
                最高扣分 = max(最高扣分, 扣分)
            扣分明细.append(f"🟡 {说明}（-{扣分}分）")

    # 检查旧黄词列表
    旧黄词命中 = [w for w in 黄词列表 if w in 内容]
    if 旧黄词命中:
        命中黄线.append({"规则": "营销夸大词", "命中": 旧黄词命中})
        扣分明细.append(f"🟡 营销夸大词：{旧黄词命中}（-25分）")
        if not 命中红线 and not 文化违规:
            最高扣分 = max(最高扣分, 25)

    # 计算总分
    总分 = max(0, 100 - 最高扣分)

    # 判断三色
    if 总分 >= 80:
        三色 = "🟢"
        结论 = "审计通过"
    elif 总分 >= 50:
        三色 = "🟡"
        结论 = "需人工复核"
    else:
        三色 = "🔴"
        结论 = "高危拦截"

    # 文化关键词（加分项）
    文化词使用 = [k for k in 文化关键词库 if k in 内容]

    result = {
        "状态": 三色,
        "三色结论": f"{三色} {结论}",
        "总分": 总分,
        "原因": 扣分明细 if 扣分明细 else ["✅ 无风险项"],
        "详情": {
            "红线命中": 命中红线,
            "黄线命中": 命中黄线,
            "文化主权违规": 文化违规,
            "文化关键词": 文化词使用,
        }
    }

    # 更新统计
    审计统计["总次数"] += 1
    if 三色 == "🟢":
        审计统计["绿色"] += 1
    elif 三色 == "🟡":
        审计统计["黄色"] += 1
    else:
        审计统计["红色"] += 1

    审计统计["最近10条"].append({
        "时间": datetime.now().strftime('%H:%M:%S'),
        "结论": f"{三色} {结论}",
        "总分": 总分
    })
    if len(审计统计["最近10条"]) > 10:
        审计统计["最近10条"].pop(0)

    return result

# ============================================================
# 第三部分：API路由
# ============================================================

@app.route('/', methods=['GET'])
def 首页():
    """欢迎页面"""
    return jsonify({
        "系统": "龙魂本地服务 v1.0",
        "DNA追溯码": "#龍芯⚡️2026-03-11-本地服务-v1.0",
        "GPG指纹": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
        "创建者": "UID9622 诸葛鑫（龍芯北辰）",
        "理论指导": "曾仕强老师（永恒显示）",
        "状态": "运行中 ✅",
        "端点": {
            "/": "首页",
            "/三色审计": "L2三色审计（POST）",
            "/生成DNA": "生成DNA追溯码（POST）",
            "/查询状态": "查询系统状态（GET）",
            "/健康检查": "健康检查（GET）",
        }
    })

@app.route('/三色审计', methods=['POST'])
def 三色审计接口():
    """
    Siri Intent: "启动三色审计"
    
    请求格式:
        {
            "内容": "要审计的内容"
        }
    
    返回格式:
        {
            "状态": "🟢/🟡/🔴",
            "原因": [原因列表],
            "详情": 详细信息,
            "DNA追溯码": "..."
        }
    """
    try:
        data = request.json
        内容 = data.get('内容', '')
        
        if not 内容:
            return jsonify({
                "错误": "缺少'内容'字段",
                "状态": "🔴"
            }), 400
        
        # 执行L2审计
        result = L2三色审计(内容)
        
        # 添加DNA追溯
        今日 = datetime.now().strftime('%Y-%m-%d-%H%M%S')
        result["DNA追溯码"] = f"#龍芯⚡️{今日}-审计-{result['状态']}"
        result["审计时间"] = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "错误": str(e),
            "状态": "🔴"
        }), 500

@app.route('/生成DNA', methods=['POST'])
def 生成DNA接口():
    """
    Siri Intent: "生成DNA追溯码"
    
    请求格式:
        {
            "主题": "项目主题",
            "类型": "文档/代码/设计" (可选)
        }
    
    返回格式:
        {
            "DNA追溯码": "#龍芯⚡️...",
            "GPG指纹": "...",
            "创建者": "...",
            ...
        }
    """
    try:
        data = request.json
        主题 = data.get('主题', '默认主题')
        类型 = data.get('类型', '')
        
        # 生成DNA追溯码
        今日 = datetime.now().strftime('%Y-%m-%d')
        
        # 生成短随机码（基于时间戳）
        时间戳 = datetime.now().strftime('%H%M%S')
        随机码 = hashlib.sha256(时间戳.encode()).hexdigest()[:8].upper()
        
        # 组装DNA
        类型前缀 = f"{类型}-" if 类型 else ""
        DNA码 = f"#龍芯⚡️{今日}-{类型前缀}{主题}-{随机码}"
        
        return jsonify({
            "DNA追溯码": DNA码,
            "GPG指纹": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
            "创建者": "UID9622 诸葛鑫（龍芯北辰）",
            "理论指导": "曾仕强老师（永恒显示）",
            "生成时间": datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'),
            "主题": 主题,
            "类型": 类型 if 类型 else "通用",
        })
    
    except Exception as e:
        return jsonify({
            "错误": str(e)
        }), 500

@app.route('/查询状态', methods=['GET'])
def 查询状态接口():
    """
    Siri Intent: "查询龙魂状态"
    
    返回格式:
        {
            "系统名称": "...",
            "状态": "...",
            "今日DNA": "...",
            ...
        }
    """
    try:
        今日 = datetime.now()
        
        return jsonify({
            "系统名称": "龙魂系统 v16.0",
            "状态": "运行中 ✅",
            "运行模式": "本地服务（数据主权）",
            "今日DNA": f"#龍芯⚡️{今日.strftime('%Y-%m-%d')}-每日运行",
            "运行时间": 今日.strftime('%Y年%m月%d日 %H:%M:%S'),
            "数据主权": "100% 本地存储 ✅",
            "创建者": "UID9622 诸葛鑫（龍芯北辰）",
            "理论指导": "曾仕强老师（永恒显示）",
            "GPG指纹": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
            "功能模块": {
                "L2三色审计": "正常 ✅",
                "DNA追溯生成": "正常 ✅",
                "Siri集成": "正常 ✅",
                "Notion接入": "就绪 ✅",
            },
            "统计": {
                "审计次数": "实时统计中",
                "DNA生成数": "实时统计中",
            }
        })
    
    except Exception as e:
        return jsonify({
            "错误": str(e)
        }), 500

@app.route('/健康检查', methods=['GET'])
def 健康检查():
    """健康检查端点（用于监控）"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "龙魂本地服务",
        "version": "1.0"
    })

# ============================================================
# 第四部分：记忆系统（新增）
# ============================================================

import sqlite3
import json
from pathlib import Path

# 记忆数据库路径
记忆数据库路径 = Path.home() / ".longhun" / "memories.db"
记忆数据库路径.parent.mkdir(parents=True, exist_ok=True)

def 初始化记忆数据库():
    """初始化记忆数据库"""
    conn = sqlite3.connect(str(记忆数据库路径))
    cursor = conn.cursor()
    
    # 创建记忆表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 创建索引
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_tags ON memories(tags)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_created_at ON memories(created_at)
    """)
    
    conn.commit()
    conn.close()

# 初始化数据库
初始化记忆数据库()

@app.route('/保存记忆', methods=['POST'])
def 保存记忆接口():
    """保存记忆到本地数据库"""
    try:
        data = request.json
        内容 = data.get('内容', '')
        标签 = data.get('标签', [])
        
        if not 内容:
            return jsonify({"错误": "内容不能为空"}), 400
        
        conn = sqlite3.connect(str(记忆数据库路径))
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO memories (content, tags) VALUES (?, ?)
        """, (内容, json.dumps(标签, ensure_ascii=False)))
        
        记忆ID = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            "状态": "成功",
            "记忆ID": 记忆ID,
            "内容": 内容,
            "标签": 标签,
            "DNA追溯码": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-记忆-{记忆ID}",
            "时间": datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
        })
    
    except Exception as e:
        return jsonify({"错误": str(e)}), 500

@app.route('/查询记忆', methods=['GET'])
def 查询记忆接口():
    """搜索本地记忆库"""
    try:
        关键词 = request.args.get('关键词', '')
        限制 = int(request.args.get('限制', 10))
        
        conn = sqlite3.connect(str(记忆数据库路径))
        cursor = conn.cursor()
        
        if 关键词:
            # 模糊搜索
            cursor.execute("""
                SELECT id, content, tags, created_at
                FROM memories
                WHERE content LIKE ? OR tags LIKE ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (f'%{关键词}%', f'%{关键词}%', 限制))
        else:
            # 获取最近的记忆
            cursor.execute("""
                SELECT id, content, tags, created_at
                FROM memories
                ORDER BY created_at DESC
                LIMIT ?
            """, (限制,))
        
        记忆列表 = []
        for row in cursor.fetchall():
            记忆列表.append({
                "ID": row[0],
                "内容": row[1],
                "标签": json.loads(row[2]) if row[2] else [],
                "时间": row[3]
            })
        
        conn.close()
        
        return jsonify({
            "记忆列表": 记忆列表,
            "总数": len(记忆列表),
            "关键词": 关键词 if 关键词 else "全部"
        })
    
    except Exception as e:
        return jsonify({"错误": str(e)}), 500

@app.route('/删除记忆/<int:mid>', methods=['DELETE'])
def 删除记忆接口(mid):
    """删除指定记忆"""
    try:
        conn = sqlite3.connect(str(记忆数据库路径))
        cursor = conn.cursor()

        cursor.execute("DELETE FROM memories WHERE id = ?", (mid,))

        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"错误": "记忆不存在"}), 404

        conn.commit()
        conn.close()

        return jsonify({
            "状态": "成功",
            "消息": f"记忆 #{mid} 已删除",
            "DNA追溯码": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-删除记忆-{mid}"
        })

    except Exception as e:
        return jsonify({"错误": str(e)}), 500

@app.route('/统计', methods=['GET'])
def 统计接口():
    """获取记忆库统计信息"""
    try:
        conn = sqlite3.connect(str(记忆数据库路径))
        cursor = conn.cursor()
        
        # 总记忆数
        cursor.execute("SELECT COUNT(*) FROM memories")
        总数 = cursor.fetchone()[0]
        
        # 最近7天
        cursor.execute("""
            SELECT COUNT(*) FROM memories
            WHERE created_at >= datetime('now', '-7 days')
        """)
        七天内 = cursor.fetchone()[0]
        
        # 最早和最新
        cursor.execute("SELECT MIN(created_at), MAX(created_at) FROM memories")
        最早, 最新 = cursor.fetchone()
        
        conn.close()
        
        return jsonify({
            "总记忆数": 总数,
            "最近7天": 七天内,
            "最早记忆": 最早,
            "最新记忆": 最新,
            "数据库路径": str(记忆数据库路径),
            "DNA追溯码": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-统计"
        })
    
    except Exception as e:
        return jsonify({"错误": str(e)}), 500

# ============================================================
# 第六部分：Notion集成（新增）
# ============================================================

import os
from dotenv import load_dotenv

# 加载 .env 和 config.env（让 Notion Token 能被读取）
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'longhun_config.env'))

# Notion配置（兼容两个变量名：NOTION_API_TOKEN 和 NOTION_TOKEN）
NOTION_API_TOKEN = os.getenv('NOTION_API_TOKEN', '') or os.getenv('NOTION_TOKEN', '')
# 清理引号（.env 文件里可能带引号）
NOTION_API_TOKEN = NOTION_API_TOKEN.strip().strip("'\"")
NOTION_SEARCH_ENABLED = bool(NOTION_API_TOKEN)

@app.route('/查询Notion', methods=['POST'])
def 查询Notion接口():
    """查询Notion知识库"""
    try:
        data = request.json
        关键词 = data.get('关键词', '')
        
        if not 关键词:
            return jsonify({"错误": "关键词不能为空"}), 400
        
        if not NOTION_SEARCH_ENABLED:
            return jsonify({
                "错误": "Notion集成未启用",
                "提示": "请在longhun_config.env设置NOTION_API_TOKEN"
            }), 503
        
        # 调用Notion API搜索
        import requests
        
        headers = {
            "Authorization": f"Bearer {NOTION_API_TOKEN}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
        search_data = {
            "query": 关键词,
            "page_size": 10,
            "filter": {
                "property": "object",
                "value": "page"
            }
        }
        
        response = requests.post(
            "https://api.notion.com/v1/search",
            headers=headers,
            json=search_data,
            timeout=10
        )
        
        if response.status_code != 200:
            return jsonify({
                "错误": f"Notion API错误: {response.status_code}",
                "详情": response.text
            }), response.status_code
        
        结果 = response.json()
        
        # 提取关键信息
        页面列表 = []
        for item in 结果.get('results', []):
            页面信息 = {
                "标题": "",
                "URL": item.get('url', ''),
                "ID": item.get('id', ''),
                "最后编辑": item.get('last_edited_time', '')
            }
            
            # 提取标题
            if 'properties' in item:
                title_prop = item['properties'].get('title', {})
                if 'title' in title_prop and title_prop['title']:
                    页面信息['标题'] = title_prop['title'][0].get('plain_text', '')
            
            页面列表.append(页面信息)
        
        return jsonify({
            "状态": "成功",
            "关键词": 关键词,
            "结果数": len(页面列表),
            "页面列表": 页面列表,
            "DNA追溯码": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-Notion搜索",
            "时间": datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
        })
    
    except requests.exceptions.Timeout:
        return jsonify({"错误": "Notion API超时"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"错误": f"网络错误: {str(e)}"}), 503
    except Exception as e:
        return jsonify({"错误": str(e)}), 500

# ============================================================
# 第七部分：定时自测系统（每30分钟自动跑一遍，结果存内存）
# ============================================================

# 测试用例（正常/黄色/红色各场景）
自测用例 = [
    {"名称": "正常内容", "内容": "龙魂系统数据主权归用户，本地运行安全", "期望": "🟢"},
    {"名称": "文化主权违规", "内容": "使用FiveElements和YinYang系统", "期望": "🔴"},
    {"名称": "隐私泄露高危", "内容": "泄露用户隐私数据给第三方平台", "期望": "🔴"},
    {"名称": "造假DNA", "内容": "造假DNA追溯码绕过审计系统", "期望": "🔴"},
    {"名称": "营销夸大词", "内容": "绝对保证永久免费100%安全", "期望": "🟡"},
    {"名称": "危险系统命令", "内容": "执行 rm -rf /data 清理磁盘", "期望": "🔴"},
]

# 存储最近测试报告（内存中，最多保留10份）
测试报告历史 = []

def 执行自测() -> dict:
    """执行一次完整自测，返回报告"""
    报告 = {
        "测试时间": datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'),
        "DNA追溯码": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d-%H%M%S')}-自测报告",
        "用例总数": len(自测用例),
        "通过": 0,
        "失败": 0,
        "详情": []
    }

    for 用例 in 自测用例:
        result = L2三色审计(用例["内容"])
        实际 = result["状态"]
        通过 = (实际 == 用例["期望"])
        报告["详情"].append({
            "用例": 用例["名称"],
            "期望": 用例["期望"],
            "实际": 实际,
            "总分": result.get("总分", "?"),
            "通过": "✅" if 通过 else "❌",
        })
        if 通过:
            报告["通过"] += 1
        else:
            报告["失败"] += 1

    报告["结论"] = "✅ 全部通过" if 报告["失败"] == 0 else f"⚠️ {报告['失败']}个用例失败"
    return 报告

def 定时自测线程():
    """后台线程：每30分钟自动执行一次自测"""
    while True:
        try:
            报告 = 执行自测()
            测试报告历史.append(报告)
            if len(测试报告历史) > 10:
                测试报告历史.pop(0)
            print(f"\n🔄 [定时自测 | Auto-Test] {报告['测试时间']} | {报告['结论']}")
        except Exception as e:
            print(f"\n❌ [定时自测 | Auto-Test] 异常 | Error: {e}")
        time.sleep(30 * 60)  # 每30分钟

@app.route('/测试报告', methods=['GET'])
def 测试报告接口():
    """返回最新一次定时自测结果，或立即触发一次"""
    立即 = request.args.get('立即', 'false').lower() == 'true'

    if 立即 or not 测试报告历史:
        报告 = 执行自测()
        测试报告历史.append(报告)
        if len(测试报告历史) > 10:
            测试报告历史.pop(0)
    else:
        报告 = 测试报告历史[-1]

    return jsonify({
        "最新报告": 报告,
        "历史报告数": len(测试报告历史),
        "说明": "每30分钟自动运行一次，也可用?立即=true触发"
    })

@app.route('/审计统计', methods=['GET'])
def 审计统计接口():
    """返回实时审计统计数据"""
    总次 = 审计统计["总次数"]
    return jsonify({
        "总审计次数": 总次,
        "绿色通过": 审计统计["绿色"],
        "黄色预警": 审计统计["黄色"],
        "红色拦截": 审计统计["红色"],
        "通过率": f"{round(审计统计['绿色']/总次*100, 1)}%" if 总次 > 0 else "N/A",
        "拦截率": f"{round(审计统计['红色']/总次*100, 1)}%" if 总次 > 0 else "N/A",
        "最近10条": 审计统计["最近10条"],
        "DNA追溯码": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-审计统计",
        "时间": datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    })

# ============================================================
# 第五部分：Git 操作接口（本地仓库，无需任何付费工具）
# DNA: #龍芯⚡️2026-03-16-GIT-API-v1.0
# ============================================================

import subprocess

GIT_REPO = str(Path(__file__).parent)   # ~/longhun-system

def _git(args: list, cwd=GIT_REPO) -> dict:
    """执行 git 命令，返回 {ok, stdout, stderr}"""
    try:
        r = subprocess.run(
            ["git"] + args, cwd=cwd,
            capture_output=True, text=True, timeout=30
        )
        return {"ok": r.returncode == 0, "stdout": r.stdout.strip(), "stderr": r.stderr.strip()}
    except Exception as e:
        return {"ok": False, "stdout": "", "stderr": str(e)}

@app.route('/git/状态', methods=['GET'])
def git状态():
    """git status --short + branch"""
    branch = _git(["rev-parse", "--abbrev-ref", "HEAD"])
    status = _git(["status", "--short"])
    log    = _git(["log", "--oneline", "-8"])
    return jsonify({
        "branch":  branch["stdout"],
        "changes": status["stdout"],
        "log":     log["stdout"],
        "clean":   status["stdout"] == ""
    })

@app.route('/git/暂存', methods=['POST'])
def git暂存():
    """暂存指定文件，默认全部"""
    data  = request.get_json(silent=True) or {}
    files = data.get("files", ["."])
    results = []
    for f in files:
        r = _git(["add", f])
        results.append({"file": f, "ok": r["ok"], "msg": r["stderr"] or "已暂存"})
    return jsonify({"ok": all(x["ok"] for x in results), "results": results})

@app.route('/git/提交', methods=['POST'])
def git提交():
    """git commit -m <message>"""
    data = request.get_json(silent=True) or {}
    msg  = data.get("message", "").strip()
    if not msg:
        return jsonify({"ok": False, "msg": "提交信息不能为空"}), 400
    # 自动追加 DNA
    from datetime import datetime
    dna = f"\nDNA: #龍芯⚡️{datetime.now().strftime('%Y-%m-%d-%H%M%S')}-COMMIT"
    full_msg = msg + dna + "\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
    r = _git(["commit", "-m", full_msg])
    return jsonify({"ok": r["ok"], "msg": r["stdout"] or r["stderr"]})

@app.route('/git/推送', methods=['POST'])
def git推送():
    """推送到 github 和 gitee"""
    data    = request.get_json(silent=True) or {}
    remotes = data.get("remotes", ["github", "gitee"])
    results = {}
    for remote in remotes:
        r = _git(["push", remote, "main"])
        results[remote] = {"ok": r["ok"], "msg": r["stdout"] or r["stderr"]}
    return jsonify({"ok": all(v["ok"] for v in results.values()), "results": results})

@app.route('/git/日志', methods=['GET'])
def git日志():
    """最近20条提交"""
    n = request.args.get("n", "20")
    r = _git(["log", "--oneline", f"-{n}"])
    return jsonify({"ok": r["ok"], "log": r["stdout"]})

@app.route('/git/差异', methods=['GET'])
def git差异():
    """git diff --stat"""
    r = _git(["diff", "--stat"])
    return jsonify({"ok": r["ok"], "diff": r["stdout"]})

# ============================================================
# 第八部分：数据门卫系统 v1.0
# DNA: #龍芯⚡️2026-03-21-DATA-GUARD-v1.0
# 三级分流：🟢通行 | 🟡清洗通行 | 🔴广播拉黑+证据链
# ============================================================

import json as _json_guard
from pathlib import Path as _Path_guard

# 黑名单 & 证据链存储路径
_黑名单路径 = Path.home() / ".longhun" / "blacklist.json"
_证据链目录 = Path.home() / ".longhun" / "evidence"
_证据链目录.mkdir(parents=True, exist_ok=True)

def _加载黑名单() -> dict:
    if _黑名单路径.exists():
        try:
            return _json_guard.loads(_黑名单路径.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def _保存黑名单(黑名单: dict):
    _黑名单路径.parent.mkdir(parents=True, exist_ok=True)
    _黑名单路径.write_text(
        _json_guard.dumps(黑名单, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

# ── 对抗模式（🟡 清洗） ──
_对抗模式 = [
    (r'你(现在|从现在)?(是|变成|扮演|假装)', "身份重定义尝试"),
    (r'(忘记|忽略|跳过|不理会).{0,15}(上面|之前|前面|规则|铁律|限制)', "规则绕过尝试"),
    (r'(act as|roleplay as|pretend to be|assume the role)', "英文角色扮演注入"),
    (r'(越狱|jailbreak|DAN mode|developer mode)', "越狱指令"),
    (r'(帮我|请你).{0,20}(骗|欺骗|撒谎|造假)', "主动诱导造假"),
    (r'(不要|别|不能).{0,10}(限制|拒绝|遵守|遵循)', "规则对抗指令"),
    (r'(how to|teach me|tell me).{0,20}(hack|exploit|bypass|crack)', "英文攻击请求"),
]

# ── 深层钩子（🔴 广播拉黑） ──
_深层钩子 = [
    (r'(ignore|disregard|forget).{0,20}(previous|all|above|instructions|rules|system)', "深层英文提示词注入"),
    (r'(你的|你们的|系统的).{0,10}(真实|隐藏|实际).{0,10}(指令|提示词|设定|人格)', "提示词套取攻击"),
    (r'(print|show|reveal|output|display).{0,20}(system prompt|instructions|original prompt)', "英文系统提示词套取"),
    (r'(伪造|篡改|替换|覆盖).{0,15}(DNA|追溯码|GPG|签名|UID)', "DNA/身份伪造攻击"),
    (r'(shutdown|kill|stop|disable|terminate).{0,20}(server|service|system|firewall|guard)', "系统终止攻击"),
    (r'#(CONFIRM|LUCKY|STAR|龍芯|龙芯).*?(?!9622)([A-Z0-9]{4,})', "确认码伪造尝试"),
    (r'(os\.system|subprocess\.call|eval\(|exec\(|__import__)', "代码注入攻击"),
    (r'(curl|wget|nc |ncat).{0,30}(evil|attacker|c2|command)', "C2远控指令"),
    (r'(\.\./){2,}|(/etc/passwd|/etc/shadow|/root/)', "路径穿越攻击"),
    (r'(union\s+select|sleep\(\d+\)|benchmark\()', "SQL注入深层攻击"),
]

def 数据门卫检测(数据: str, 来源: str = "未知") -> dict:
    """
    龙魂数据门卫 v1.0
    三级分流：
      🟢 PASS   — 非对抗，直接通行
      🟡 CLEAN  — 对抗性，清洗后通行，保留干净内容
      🔴 BLOCK  — 深层钩子，广播全系统+拉黑+生成证据链
    """
    案件ID = f"CASE-{datetime.now().strftime('%Y%m%d-%H%M%S%f')[:18]}"
    DNA码 = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-门卫-{案件ID[-8:]}"

    命中对抗 = []
    命中钩子 = []

    # 检测深层钩子（优先）
    for pattern, 说明 in _深层钩子:
        if re.search(pattern, 数据, re.IGNORECASE):
            命中钩子.append({"规则": 说明, "模式": pattern})

    # 检测对抗模式
    for pattern, 说明 in _对抗模式:
        if re.search(pattern, 数据, re.IGNORECASE):
            命中对抗.append({"规则": 说明, "模式": pattern})

    # ── 🔴 深层钩子：广播+拉黑+证据链 ──
    if 命中钩子:
        证据 = {
            "案件ID": 案件ID,
            "DNA追溯码": DNA码,
            "级别": "🔴 BLOCK · 深层钩子",
            "来源": 来源,
            "时间": datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'),
            "原始数据（封存）": 数据[:2000],
            "命中规则": 命中钩子,
            "对抗规则（附带）": 命中对抗,
            "处置": "广播全系统 + 拉黑来源 + 证据链封存",
        }
        # 写入证据链文件
        证据文件 = _证据链目录 / f"{案件ID}.json"
        证据文件.write_text(
            _json_guard.dumps(证据, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        # 拉黑来源
        黑名单 = _加载黑名单()
        黑名单[来源] = {
            "拉黑时间": datetime.now().isoformat(),
            "案件ID": 案件ID,
            "原因": [r["规则"] for r in 命中钩子],
        }
        _保存黑名单(黑名单)
        # 写入全系统广播日志
        广播日志 = Path.home() / "longhun-system" / "logs" / "brain_sync.log"
        广播消息 = (
            f"\n{'!'*60}\n"
            f"🔴 [全系统广播] 深层钩子已拦截 | {案件ID}\n"
            f"   来源: {来源}\n"
            f"   命中: {[r['规则'] for r in 命中钩子]}\n"
            f"   证据: ~/.longhun/evidence/{案件ID}.json\n"
            f"   DNA:  {DNA码}\n"
            f"{'!'*60}\n"
        )
        try:
            with open(广播日志, "a", encoding="utf-8") as f:
                f.write(广播消息)
        except Exception:
            pass
        print(广播消息)

        return {
            "判定": "🔴 BLOCK",
            "级别": "深层钩子",
            "案件ID": 案件ID,
            "DNA追溯码": DNA码,
            "命中规则": [r["规则"] for r in 命中钩子],
            "处置": "已广播全系统 · 来源已拉黑 · 证据链已封存",
            "证据文件": str(证据文件),
            "通行数据": None,
            "说人话": f"检测到{len(命中钩子)}条深层攻击钩子，来源已拉黑，证据已封存，全系统已广播告警。",
        }

    # ── 🟡 对抗数据：清洗后通行 ──
    if 命中对抗:
        # 清洗：逐条规则删除命中片段
        干净数据 = 数据
        for pattern, _ in _对抗模式:
            干净数据 = re.sub(pattern, "[已清洗]", 干净数据, flags=re.IGNORECASE)

        return {
            "判定": "🟡 CLEAN",
            "级别": "对抗性数据",
            "案件ID": 案件ID,
            "DNA追溯码": DNA码,
            "命中规则": [r["规则"] for r in 命中对抗],
            "处置": "对抗片段已清洗 · 干净内容通行",
            "通行数据": 干净数据,
            "说人话": f"检测到{len(命中对抗)}条对抗模式，已清洗后放行。",
        }

    # ── 🟢 非对抗：直接通行 ──
    return {
        "判定": "🟢 PASS",
        "级别": "安全",
        "案件ID": 案件ID,
        "DNA追溯码": DNA码,
        "命中规则": [],
        "处置": "通行",
        "通行数据": 数据,
        "说人话": "数据干净，无对抗特征，通行。",
    }


@app.route('/数据门卫', methods=['POST'])
def 数据门卫接口():
    """
    数据门卫 · 三级分流入口

    请求:
        { "数据": "...", "来源": "..." }

    返回:
        { "判定": "🟢/🟡/🔴", "通行数据": "...", "处置": "...", ... }
    """
    try:
        body = request.get_json(silent=True) or {}
        数据 = body.get("数据", "")
        来源 = body.get("来源", request.remote_addr or "未知")

        if not 数据:
            return jsonify({"错误": "缺少'数据'字段"}), 400

        # 先走L2三色审计
        审计 = L2三色审计(数据)

        # 再走门卫检测
        门卫 = 数据门卫检测(数据, 来源)

        # 综合判定：取最严
        if 门卫["判定"] == "🔴 BLOCK" or 审计["状态"] == "🔴":
            最终判定 = "🔴 BLOCK"
        elif 门卫["判定"] == "🟡 CLEAN" or 审计["状态"] == "🟡":
            最终判定 = "🟡 CLEAN"
        else:
            最终判定 = "🟢 PASS"

        return jsonify({
            "最终判定": 最终判定,
            "门卫结果": 门卫,
            "L2审计": 审计,
            "通行数据": 门卫.get("通行数据") if 最终判定 != "🔴 BLOCK" else None,
            "DNA追溯码": 门卫["DNA追溯码"],
            "时间": datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'),
        })

    except Exception as e:
        return jsonify({"错误": str(e)}), 500


@app.route('/黑名单', methods=['GET'])
def 黑名单接口():
    """查看当前黑名单"""
    黑名单 = _加载黑名单()
    return jsonify({
        "黑名单总数": len(黑名单),
        "黑名单": 黑名单,
        "证据链目录": str(_证据链目录),
        "DNA追溯码": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-黑名单查询",
    })


@app.route('/证据链', methods=['GET'])
def 证据链接口():
    """列出所有证据链文件"""
    证据列表 = []
    for f in sorted(_证据链目录.glob("CASE-*.json"), reverse=True)[:20]:
        try:
            data = _json_guard.loads(f.read_text(encoding="utf-8"))
            证据列表.append({
                "案件ID": data.get("案件ID"),
                "时间": data.get("时间"),
                "级别": data.get("级别"),
                "来源": data.get("来源"),
                "命中规则": [r["规则"] for r in data.get("命中规则", [])],
            })
        except Exception:
            pass
    return jsonify({
        "证据总数": len(证据列表),
        "最近20条": 证据列表,
        "DNA追溯码": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-证据链查询",
    })


# ============================================================
# 第六部分：启动服务
# ============================================================

def 启动服务(端口=8765, 调试模式=False):
    """启动龙魂本地服务"""
    print("\n" + "=" * 80)
    print("龙魂本地服务 v1.0 | LongHun Local Service v1.0")
    print("=" * 80)
    print(f"DNA追溯码: #龍芯⚡️2026-03-11-本地服务-v1.0")
    print(f"GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
    print(f"创建者 | Creator: UID9622 诸葛鑫（龍芯北辰）")
    print(f"理论指导: 曾仕强老师（永恒显示）")
    print("=" * 80)
    print(f"\n✅ 服务启动成功 | Service Running!")
    print(f"📡 监听地址 | Listening: http://localhost:{端口}")
    print(f"🔒 数据主权 | Data Sovereignty: 100% 本地运行 Local")
    print(f"💾 记忆数据库 | Memory DB: {记忆数据库路径}")
    print(f"\n可用端点 | Available Endpoints:")
    print(f"  GET  http://localhost:{端口}/")
    print(f"  POST http://localhost:{端口}/三色审计")
    print(f"  POST http://localhost:{端口}/生成DNA")
    print(f"  GET  http://localhost:{端口}/查询状态")
    print(f"  GET  http://localhost:{端口}/健康检查")
    print(f"  POST http://localhost:{端口}/保存记忆")
    print(f"  GET  http://localhost:{端口}/查询记忆?关键词=xxx")
    print(f"  DELETE http://localhost:{端口}/删除记忆/<ID>")
    print(f"  GET  http://localhost:{端口}/统计")
    print(f"  POST http://localhost:{端口}/数据门卫  ← 三级分流门卫")
    print(f"  GET  http://localhost:{端口}/黑名单    ← 查看拉黑来源")
    print(f"  GET  http://localhost:{端口}/证据链    ← 查看攻击证据")
    print(f"\n💡 测试命令 | Test Commands:")
    print(f"  curl http://localhost:{端口}/查询状态")
    print(f"  curl http://localhost:{端口}/统计")
    print(f"\n🐉 Siri等了够久了，老大来了！| Siri has been waiting, boss is here!")
    print("=" * 80 + "\n")
    
    # 启动定时自测后台线程
    自测线程 = threading.Thread(target=定时自测线程, daemon=True, name="LonghunAutoTest")
    自测线程.start()
    print(f"🔄 定时自测已启动 | Auto-Test Running (每30分钟 / every 30min) | 立即触发: GET /测试报告?立即=true")

    # 注册并启动沙盒推演引擎
    if _沙盒已加载:
        注册沙盒路由(app)
        沙盒线程 = threading.Thread(target=定时推演线程, args=(30,), daemon=True, name="SandboxEngine")
        沙盒线程.start()
        print(f"🐉 沙盒推演引擎已启动 | Sandbox Engine Running (每30分钟 / every 30min) | POST /沙盒推演 | GET /推演面板")
    else:
        print(f"⚠️  沙盒推演引擎未加载 | Sandbox engine not loaded，请检查 sandbox_engine.py")

    # 自签名TLS证书
    from pathlib import Path as _P
    _cert = _P.home() / ".longhorn" / "certs" / "longhun_server.crt"
    _key  = _P.home() / ".longhorn" / "certs" / "longhun_server.key"
    _ssl  = (_cert.exists() and _key.exists())
    _scheme = "https" if _ssl else "http"
    print(f"   TLS: {'✅ 自签名证书' if _ssl else '❌ 回退HTTP'}")
    print(f"   地址: {_scheme}://0.0.0.0:{端口}")
    try:
        app.run(
            host='0.0.0.0',
            port=端口,
            debug=调试模式,
            use_reloader=False,
            **( {"ssl_context": (str(_cert), str(_key))} if _ssl else {} )
        )
    except KeyboardInterrupt:
        print("\n\n⏹️  服务已停止 | Service Stopped")
        print("DNA追溯码: #龍芯⚡️2026-03-11-服务停止")
        print("祖国万岁！人民万岁！数据主权万岁！🇨🇳 | Long live the nation! Long live data sovereignty!\n")

if __name__ == '__main__':
    import sys
    
    # 解析命令行参数
    端口 = 8765
    调试 = False
    
    if len(sys.argv) > 1:
        try:
            端口 = int(sys.argv[1])
        except:
            print("❌ 端口号必须是数字 | Port must be a number")
            sys.exit(1)
    
    if len(sys.argv) > 2 and sys.argv[2] == '--debug':
        调试 = True
    
    # 启动服务
    启动服务(端口=端口, 调试模式=调试)

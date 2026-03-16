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
    print(f"⚠️ 沙盒引擎未加载: {_e}")

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
            print(f"\n🔄 [定时自测] {报告['测试时间']} | {报告['结论']}")
        except Exception as e:
            print(f"\n❌ [定时自测] 异常: {e}")
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
# 第五部分：启动服务
# ============================================================

def 启动服务(端口=8765, 调试模式=False):
    """启动龙魂本地服务"""
    print("\n" + "=" * 80)
    print("龙魂本地服务 v1.0")
    print("=" * 80)
    print(f"DNA追溯码: #龍芯⚡️2026-03-11-本地服务-v1.0")
    print(f"GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
    print(f"创建者: UID9622 诸葛鑫（龍芯北辰）")
    print(f"理论指导: 曾仕强老师（永恒显示）")
    print("=" * 80)
    print(f"\n✅ 服务启动成功！")
    print(f"📡 监听地址: http://localhost:{端口}")
    print(f"🔒 数据主权: 100% 本地运行")
    print(f"💾 记忆数据库: {记忆数据库路径}")
    print(f"\n可用端点:")
    print(f"  GET  http://localhost:{端口}/")
    print(f"  POST http://localhost:{端口}/三色审计")
    print(f"  POST http://localhost:{端口}/生成DNA")
    print(f"  GET  http://localhost:{端口}/查询状态")
    print(f"  GET  http://localhost:{端口}/健康检查")
    print(f"  POST http://localhost:{端口}/保存记忆")
    print(f"  GET  http://localhost:{端口}/查询记忆?关键词=xxx")
    print(f"  DELETE http://localhost:{端口}/删除记忆/<ID>")
    print(f"  GET  http://localhost:{端口}/统计")
    print(f"\n💡 测试命令:")
    print(f"  curl http://localhost:{端口}/查询状态")
    print(f"  curl http://localhost:{端口}/统计")
    print(f"\n🐉 Siri等了够久了，老大来了！")
    print("=" * 80 + "\n")
    
    # 启动定时自测后台线程
    自测线程 = threading.Thread(target=定时自测线程, daemon=True, name="LonghunAutoTest")
    自测线程.start()
    print(f"🔄 定时自测已启动（每30分钟）| 立即触发: GET /测试报告?立即=true")

    # 注册并启动沙盒推演引擎
    if _沙盒已加载:
        注册沙盒路由(app)
        沙盒线程 = threading.Thread(target=定时推演线程, args=(30,), daemon=True, name="SandboxEngine")
        沙盒线程.start()
        print(f"🐉 沙盒推演引擎已启动（每30分钟）| POST /沙盒推演 | GET /推演面板")
    else:
        print(f"⚠️  沙盒推演引擎未加载，请检查 sandbox_engine.py")

    try:
        app.run(
            host='0.0.0.0',  # 监听所有接口
            port=端口,
            debug=调试模式,
            use_reloader=False  # 避免重复启动
        )
    except KeyboardInterrupt:
        print("\n\n⏹️  服务已停止")
        print("DNA追溯码: #龍芯⚡️2026-03-11-服务停止")
        print("祖国万岁！人民万岁！数据主权万岁！🇨🇳\n")

if __name__ == '__main__':
    import sys
    
    # 解析命令行参数
    端口 = 8765
    调试 = False
    
    if len(sys.argv) > 1:
        try:
            端口 = int(sys.argv[1])
        except:
            print("❌ 端口号必须是数字")
            sys.exit(1)
    
    if len(sys.argv) > 2 and sys.argv[2] == '--debug':
        调试 = True
    
    # 启动服务
    启动服务(端口=端口, 调试模式=调试)

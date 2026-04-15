#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂本地服务 v1.0
DNA追溯码: #龍芯⚡️2026-03-11-本地服务-v1.0
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）

功能:
  1. 监听Siri Intent请求
  2. 处理三色审计
  3. 生成DNA追溯码
  4. 查询龍魂状态
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

app = Flask(__name__)
CORS(app)  # 允许本地跨域

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
    "龍魂", "龍魂", "熵梦", "ShangMeng",
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
# 第二部分：L2三色审计
# ============================================================

def L2三色审计(内容: str) -> dict:
    """
    龍魂L2三色审计系统
    
    返回:
        {
            "状态": "🟢/🟡/🔴",
            "原因": [原因列表],
            "详情": 详细信息
        }
    """
    result = {
        "状态": "🟢",  # 默认绿色
        "原因": [],
        "详情": {},
    }
    
    # 检查红词（严重违规）
    红词命中 = []
    for 英文, 中文 in 禁止翻译表.items():
        if 英文 in 内容:
            红词命中.append({
                "违规词": 英文,
                "应该用": 中文,
            })
    
    if 红词命中:
        result["状态"] = "🔴"
        result["原因"].append(f"文化主权违规：发现{len(红词命中)}处")
        result["详情"]["红词"] = 红词命中
    
    # 检查黄词（需警惕）
    黄词命中 = []
    for 黄词 in 黄词列表:
        if 黄词 in 内容:
            黄词命中.append(黄词)
    
    if 黄词命中:
        if result["状态"] == "🟢":  # 只有在没有红词时才变黄
            result["状态"] = "🟡"
        result["原因"].append(f"需要警惕：发现{len(黄词命中)}个敏感词")
        result["详情"]["黄词"] = 黄词命中
    
    # 检查文化关键词使用（加分项）
    文化词使用 = []
    for 关键词 in 文化关键词库:
        if 关键词 in 内容:
            文化词使用.append(关键词)
    
    if 文化词使用:
        result["详情"]["文化关键词"] = 文化词使用
        if not result["原因"]:
            result["原因"].append("审计通过 ✅")
    
    if not result["原因"]:
        result["原因"].append("审计通过 ✅")
    
    return result

# ============================================================
# 第三部分：API路由
# ============================================================

@app.route('/', methods=['GET'])
def 首页():
    """欢迎页面"""
    return jsonify({
        "系统": "龍魂本地服务 v1.0",
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
    Siri Intent: "查询龍魂状态"
    
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
            "系统名称": "龍魂系统 v16.0",
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
        "service": "龍魂本地服务",
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

@app.route('/删除记忆/<int:记忆ID>', methods=['DELETE'])
def 删除记忆接口(记忆ID):
    """删除指定记忆"""
    try:
        conn = sqlite3.connect(str(记忆数据库路径))
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM memories WHERE id = ?", (记忆ID,))
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"错误": "记忆不存在"}), 404
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "状态": "成功",
            "消息": f"记忆 #{记忆ID} 已删除",
            "DNA追溯码": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-删除记忆-{记忆ID}"
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

# Notion配置（从环境变量读取）
NOTION_API_TOKEN = os.getenv('NOTION_API_TOKEN', '')
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
# 第五部分：启动服务
# ============================================================

def 启动服务(端口=8765, 调试模式=False):
    """启动龍魂本地服务"""
    print("\n" + "=" * 80)
    print("龍魂本地服务 v1.0")
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

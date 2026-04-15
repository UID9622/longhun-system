#!/bin/bash
# 🐉 龍魂系统 · 道德经API一键部署脚本
# DNA: #龍芯⚡️2026-03-29-DAODEJING-DEPLOY-v1.0
# 目标服务器: 119.13.90.27
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

echo "🐉 开始部署道德经API到华为云..."
echo "================================"

# 1. 创建目录
mkdir -p /root/cnsh/daodejing-api
cd /root/cnsh/daodejing-api

# 2. 创建道德经数据文件
cat > daodejing_data.py << 'PYEOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
道德经·王弼本·语义锚点数据
龍魂系统 | UID9622
"""

CHAPTERS_DATA = [
    {
        "chapter": 1,
        "title": "道德经·第一章",
        "text": "道可道，非常道；名可名，非常名。无名，天地之始；有名，万物之母。故常无欲，以观其妙；常有欲，以观其徼。此两者，同出而异名，同谓之玄。玄之又玄，众妙之门。",
        "translation_en": "The Dao that can be told is not the eternal Dao; The name that can be named is not the eternal name.",
        "core_tags": ["本体论", "认识论", "道之本质", "有无辩证"],
        "meaning_cn": "道德经开篇揭示宇宙本源：真正的'道'超越语言文字，无法被完全定义和命名。'无名'代表宇宙混沌初始状态，'有名'是万物具体形态的显现。通过'无欲'观察道的玄妙本质，通过'有欲'观察道的具体边界。有无相生，玄之又玄，是一切奥妙的起点。",
        "key_concepts": [
            {"term": "道", "definition": "宇宙万物的本源与运行规律，超越语言文字"},
            {"term": "无名", "definition": "天地混沌初始状态，道之本体"},
            {"term": "有名", "definition": "万物显现的具体形态，道之用"},
            {"term": "玄", "definition": "深远、幽微、难以言说的本质"}
        ],
        "ai_application": "在AI系统中，对应'可解释性悖论'：模型的真实工作机制（道）难以用人类语言完全描述（可道非常道），但必须用近似的解释框架（名）来理解其行为模式。",
        "related_hexagrams": ["乾卦", "坤卦"],
        "zhuge_comment": "此章为道德经总纲，诸葛亮需深刻理解'道可道非常道'的认识论边界，避免在AI推演中陷入语言陷阱。"
    },
    {
        "chapter": 2,
        "title": "道德经·第二章", 
        "text": "天下皆知美之为美，斯恶已；皆知善之为善，斯不善已。故有无相生，难易相成，长短相较，高下相倾，音声相和，前后相随。是以圣人处无为之事，行不言之教。万物作焉而不辞，生而不有，为而不恃，功成而弗居。夫唯弗居，是以不去。",
        "translation_en": "When all under heaven know beauty as beauty, ugliness is already there. When all know good as good, not-good is already there.",
        "core_tags": ["相对论", "无为而治", "对立统一", "不争之德"],
        "meaning_cn": "世人都知道美的标准，丑就随之产生；都知道善的标准，恶就随之存在。有无、难易、长短、高下、音声、前后都是相对而生、相互依存。圣人因此采取无为的态度处理事务，用不言的方式施行教化。",
        "key_concepts": [
            {"term": "无为", "definition": "顺应自然规律，不强求，不妄为"},
            {"term": "不言", "definition": "以身作则，用行动而非言语教化"},
            {"term": "弗居", "definition": "功成不居功，所以功业永存"}
        ],
        "ai_application": "AI系统的偏差与公平性：当AI学习人类数据时，'美/丑'、'善/恶'的对立会同时出现。系统设计需避免强化单一价值观（皆知美之为美），而应承认对立统一（有无相生）。",
        "related_hexagrams": ["泰卦", "否卦"],
        "zhuge_comment": "对立统一思想在军事战略中至关重要：强弱、攻守、进退皆相对而生。AI决策应避免非黑即白的二元判断。"
    }
]

# 简化的章节数据（全部81章占位）
for i in range(3, 82):
    CHAPTERS_DATA.append({
        "chapter": i,
        "title": f"道德经·第{i}章",
        "text": f"第{i}章内容（完整版需加载）",
        "translation_en": f"Chapter {i} (full content available)",
        "core_tags": ["待完善"],
        "meaning_cn": "完整语义锚点数据待加载",
        "key_concepts": [],
        "ai_application": "待分析",
        "related_hexagrams": [],
        "zhuge_comment": "待补充"
    })
PYEOF

# 3. 创建API服务
cat > app.py << 'PYEOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 道德经API服务
龍魂系统 | UID9622 | 华为云部署
DNA: #龍芯⚡️2026-03-29-DAODEJING-API-v1.0
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import re
from urllib.parse import parse_qs, urlparse
from daodejing_data import CHAPTERS_DATA

class DaodejingHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # 静默日志，不输出
        pass
    
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        # 首页/状态
        if path == '/' or path == '/status':
            self._send_json({
                "status": "ok",
                "service": "🐉 龍魂道德经API",
                "version": "v1.0",
                "dna": "#龍芯⚡️2026-03-29-DAODEJING-API-v1.0",
                "founder": "💎 龍芯北辰 | UID9622",
                "chapters_count": len(CHAPTERS_DATA),
                "endpoints": {
                    "/": "服务状态",
                    "/chapters": "获取所有章节列表",
                    "/chapter/{n}": "获取第n章详情 (1-81)",
                    "/search?q=关键词": "搜索关键词"
                },
                "payment": {
                    "status": "后期绑定数字人民币",
                    "e_cny_wallet": "E-CNY202510253085782",
                    "price": "1元/次查询（即将开通）"
                }
            })
            return
        
        # 获取所有章节列表
        if path == '/chapters':
            chapters = [{"chapter": c["chapter"], "title": c["title"]} for c in CHAPTERS_DATA]
            self._send_json({
                "status": "ok",
                "count": len(chapters),
                "chapters": chapters
            })
            return
        
        # 获取单章详情
        chapter_match = re.match(r'/chapter/(\d+)', path)
        if chapter_match:
            chapter_num = int(chapter_match.group(1))
            if 1 <= chapter_num <= 81:
                chapter = CHAPTERS_DATA[chapter_num - 1]
                self._send_json({
                    "status": "ok",
                    "data": chapter
                })
            else:
                self._send_json({
                    "status": "error",
                    "msg": "章节范围1-81"
                }, 400)
            return
        
        # 搜索功能
        if path == '/search':
            query = parse_qs(parsed.query).get('q', [''])[0]
            if not query:
                self._send_json({
                    "status": "error",
                    "msg": "请提供搜索关键词 ?q=关键词"
                }, 400)
                return
            
            results = []
            for ch in CHAPTERS_DATA:
                if query in ch.get('text', '') or query in ch.get('meaning_cn', ''):
                    results.append({
                        "chapter": ch["chapter"],
                        "title": ch["title"],
                        "preview": ch.get('text', '')[:50] + "..."
                    })
            
            self._send_json({
                "status": "ok",
                "query": query,
                "count": len(results),
                "results": results
            })
            return
        
        # 404
        self._send_json({
            "status": "error",
            "msg": "接口不存在",
            "available_endpoints": ["/", "/chapters", "/chapter/{n}", "/search?q=关键词"]
        }, 404)
    
    def do_POST(self):
        # TODO: 后期加数字人民币验证
        self._send_json({
            "status": "ok",
            "msg": "服务运行中",
            "note": "后期绑定数字人民币后开放完整功能",
            "e_cny_wallet": "E-CNY202510253085782"
        })

if __name__ == "__main__":
    PORT = 8080
    print(f"🐉 龍魂道德经API启动...")
    print(f"DNA: #龍芯⚡️2026-03-29-DAODEJING-API-v1.0")
    print(f"访问: http://119.13.90.27:{PORT}")
    print(f"创始人: 💎 龍芯北辰 | UID9622")
    print(f"=" * 50)
    
    server = HTTPServer(("0.0.0.0", PORT), DaodejingHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
PYEOF

# 4. 创建systemd服务（开机自启）
cat > /etc/systemd/system/daodejing-api.service << 'EOF'
[Unit]
Description=🐉 龍魂道德经API服务
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/cnsh/daodejing-api
ExecStart=/usr/bin/python3 /root/cnsh/daodejing-api/app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 5. 启动服务
systemctl daemon-reload
systemctl enable daodejing-api.service
systemctl start daodejing-api.service

# 6. 检查状态
sleep 2
echo ""
echo "✅ 部署完成！"
echo "================================"
echo "服务状态:"
systemctl status daodejing-api.service --no-pager -l

echo ""
echo "🌐 访问地址:"
echo "  http://119.13.90.27:8080"
echo "  http://119.13.90.27:8080/chapters"
echo "  http://119.13.90.27:8080/chapter/1"
echo ""
echo "🧬 DNA: #龍芯⚡️2026-03-29-DAODEJING-API-v1.0"
echo "💰 后期绑定数字人民币: E-CNY202510253085782"

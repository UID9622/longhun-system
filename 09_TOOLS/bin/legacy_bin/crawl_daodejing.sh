#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·乙未·癸未·戊午·䷖剥-CRAWL-DAODEJING-v1.0-A1B2C3D4
# 后台爬取道德经81章（daodejing.org）并注入知识图谱
# 用法: bash bin/crawl_daodejing.sh

cd "$(dirname "$0")/.."

echo "📜 龍魂知识爬虫 · 道德经81章"
echo "   数据源: daodejing.org"
echo "   预计耗时: ~60秒"
echo ""

python3 -c "
import requests, json, time, sys
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

HEADERS = {'User-Agent': 'Mozilla/5.0'}
BASE = Path('.')
chapters = []

for i in range(1, 82):
    try:
        time.sleep(0.6)
        r = requests.get(f'https://www.daodejing.org/{i}.html', headers=HEADERS, timeout=10)
        r.encoding = 'gb2312'
        soup = BeautifulSoup(r.text, 'html.parser')
        for s in soup.find_all('script'): s.decompose()
        text = soup.get_text(separator='\n')
        lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 2 
                 and '道德经网' not in l and '老子' not in l and '切换' not in l 
                 and '手机版' not in l and '电脑版' not in l]
        content = '\n'.join(lines[:50])[:3000]
        chapters.append({
            'chapter': i, 'source': f'https://www.daodejing.org/{i}.html',
            'title': f'道德经·第{i}章', 'content': content
        })
        if i % 10 == 0:
            print(f'  进度: {i}/81')
    except Exception as e:
        print(f'  第{i}章失败: {e}', file=sys.stderr)
        chapters.append({'chapter': i, 'source': 'error', 'title': f'道德经·第{i}章', 'content': ''})

print(f'\\n✅ 爬取完成: {len(chapters)}章')

# 更新知识文件
with open('03_KNOWLEDGE_GRAPH/crawled_knowledge.json', 'r') as f:
    knowledge = json.load(f)
knowledge['daodejing'] = chapters
knowledge['metadata']['timestamp'] = datetime.now().isoformat()
with open('03_KNOWLEDGE_GRAPH/crawled_knowledge.json', 'w') as f:
    json.dump(knowledge, f, ensure_ascii=False, indent=2)

# 更新图谱
with open('03_KNOWLEDGE_GRAPH/graph_data.json', 'r') as f:
    graph = json.load(f)
for ch in chapters:
    node_id = f'knowledge/daodejing/{ch[\"chapter\"]}'
    if node_id in graph['nodes']:
        graph['nodes'][node_id]['description'] = ch.get('content', '')[:300]
        graph['nodes'][node_id]['source'] = 'daodejing.org'
graph['timestamp'] = datetime.now().isoformat()
with open('03_KNOWLEDGE_GRAPH/graph_data.json', 'w') as f:
    json.dump(graph, f, ensure_ascii=False, indent=2)

print(f'✅ 图谱已更新')
print(f'   预览第1章: {chapters[0][\"content\"][:120]}...')
"

echo ""
echo "✅ 道德经爬取完成"

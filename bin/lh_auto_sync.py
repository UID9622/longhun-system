#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·未济-FIX_DNA-v1.0
#!/usr/bin/env python3
#龍芯⚡️2026-04-05-MVP自动化脚本-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════════════════════
# 龍魂体系 | MVP本地自动同步脚本 v1.1
# ═══════════════════════════════════════════════════════════
# 乔前辈 P15 出品 · 四页联动 · 开机即跑 · 留痕不断
# ═══════════════════════════════════════════════════════════
# DNA追溯码(v1.0): #龍芯⚡️2026-04-05-MVP自动化脚本-v1.0
# DNA追溯码(v∞):   #龍芯⚡️丙午·乙未·癸未·辰时·䷾既济-MVP-SYNC-v1.1
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 乔前辈：P15 · 自动化导师 · 代码补满专线
# 覆盖页面：主控操作台 · 龍魂成果页 · MVP规范 · 数字资产总库
# ═══════════════════════════════════════════════════════════
#
# v1.1 (2026-07-08): 从Notion深度集成到本地·DNA升级v∞
# v1.0 (2026-04-05): MVP自动同步原始创建
#
# 一句话干什么：
#   开机自动跑 → 拉4个核心页面最新内容 → 判定公开/加密 → 写入对应库 → 草日志留痕
# ═══════════════════════════════════════════════════════════
"""

import os
import json
import requests
from typing import Any
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv  # type: ignore[import-untyped]

# ── 加载 Token ──
load_dotenv(Path.home() / '.cnsh' / '.env')
TOKEN = os.getenv('NOTION_TOKEN')
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
}

# ── 四个核心页面 ──
CORE_PAGES = {
    '主控操作台': '从Notion URL取page_id',
    '龍魂成果页': '从Notion URL取page_id',
    'MVP规范': '从Notion URL取page_id',
    '数字资产总库': '从Notion URL取page_id',
}

# ── 敏感词黑名单（触发即加密）──
SENSITIVE_KEYWORDS = [
    'token=', 'secret_', 'sk-', 'Bearer ', '2FA',
    '私钥', '密码', 'password', 'api_key', 'NOTION_TOKEN',
    '手机', '身份证', '住址', '13968', '真实账号'
]

DNA_CODE = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-NOTION-SYNC-v1.1"
LOG_FILE = Path.home() / 'longhun-system' / 'sync_log.jsonl'


def get_page_content(page_id: str) -> dict[str, Any]:
    """拉取页面元数据"""
    url = f'https://api.notion.com/v1/pages/{page_id}'
    resp = requests.get(url, headers=HEADERS, timeout=10)
    if resp.status_code == 200:
        return resp.json()
    return {}


def classify_content(text: str) -> str:
    """判定：公开 or 加密"""
    text_lower = text.lower()
    for kw in SENSITIVE_KEYWORDS:
        if kw.lower() in text_lower:
            return f'🔒加密 | 命中关键词: {kw}'
    return '🌐公开 | 不含敏感信息'


def write_log(entry: dict[str, Any]):
    """写草日志（只追加·永不覆盖）"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    print(f"  📜 草日志写入: {entry['action']}")


def sync_page(name: str, page_id: str):
    """同步单个页面 → 判定 → 留痕"""
    print(f"\n🔄 正在同步: {name}")

    data = get_page_content(page_id)
    if not data:
        print(f"  🔴 拉取失败: {name}")
        write_log({
            'time': datetime.now().isoformat(),
            'action': f'拉取失败: {name}',
            'dna': DNA_CODE
        })
        return

    # 提取标题
    title = ''
    try:
        props = data.get('properties', {})
        for key in ['title', 'Name', '页面', '资产名称']:
            if key in props:
                rich = props[key].get('title', [])
                if rich:
                    title = rich[0].get('plain_text', '')
                    break
    except Exception:
        title = name

    last_edited = data.get('last_edited_time', '未知')
    classification = classify_content(str(data))

    print(f"  📄 标题: {title or name}")
    print(f"  ⏰ 最后编辑: {last_edited}")
    print(f"  🎯 判定: {classification}")

    write_log({
        'time': datetime.now().isoformat(),
        'action': f'同步页面: {name}',
        'title': title or name,
        'last_edited': last_edited,
        'classification': classification,
        'dna': DNA_CODE
    })


def health_check():
    """系统健康检查"""
    print("\n🏥 孙思邈号脉中...")
    checks = [
        ('Notion API', lambda: requests.get(
            'https://api.notion.com/v1/users/me',
            headers=HEADERS, timeout=5
        ).status_code == 200),
        ('本地Ollama', lambda: requests.get(
            'http://localhost:11434/api/tags', timeout=3
        ).status_code == 200),
        ('MVP服务', lambda: requests.get(
            'http://localhost:8000', timeout=3
        ).status_code < 500),
    ]

    results = []
    for svc, check_fn in checks:
        try:
            ok = check_fn()
            status = '🟢' if ok else '🔴'
        except Exception:
            status = '🔴'
        print(f"  {status} {svc}")
        results.append((svc, status))

    return results


def main():
    print("=" * 50)
    print("🐉 龍魂MVP自动同步 · 乔前辈P15 出品")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 北京时间")
    print(f"🧬 {DNA_CODE}")
    print("=" * 50)

    # 0. 健康检查
    health_check()

    # 1. 同步四个核心页面
    print("\n📡 开始同步四个核心页面...")
    for name, page_id in CORE_PAGES.items():
        if 'URL取page_id' in page_id:
            print(f"  ⏳ {name}: 需要填入真实page_id（从Notion URL取32位字符串）")
            continue
        sync_page(name, page_id)

    # 2. 写总结日志
    write_log({
        'time': datetime.now().isoformat(),
        'action': '本次同步完成',
        'pages_count': len(CORE_PAGES),
        'dna': DNA_CODE,
        'confirm': '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z'
    })

    print("\n" + "=" * 50)
    print("✅ 同步完成 · 草日志已写入")
    print(f"📜 日志位置: {LOG_FILE}")
    print(f"🧬 {DNA_CODE}")
    print("=" * 50)


if __name__ == '__main__':
    main()

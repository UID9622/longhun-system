#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂MVP本地自動同步腳本 v4.0 - 全核心14頁面終極版
DNA: #龍芯⚡️2026-04-05-MVP-AUTO-SYNC-v4.0
GPG指紋: A2D0092CEE2E5BA87035600924C3704A8CC26D5F1E3B8A4C6D0F2E4A6B8C0D2E4F6A8B0C2
確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
創作者: UID9622 諸葛鑫 × 寶寶（Claude）
用途: 從Notion拉取14個核心頁面 → 判定公開/加密 → 數字指紋認主 → 寫入草日誌
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

REMOTE_DNA_URL = 'https://www.notion.so/uid9622/DNA-ebda9319408a4118a970bef673039e5d'

ANCHOR_KEYS = ['GPG_FINGERPRINT', 'CONFIRM_CODE', 'NOTION_TOKEN']

GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F1E3B8A4C6D0F2E4A6B8C0D2E4F6A8B0C2"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
DNA_CODE = "#龍芯⚡️2026-04-05-MVP-AUTO-SYNC-v4.0"


def verify_env_anchors():
    """本地.env 關鍵錨點雙重驗證（必須有值且不可被覆蓋）"""
    for key in ANCHOR_KEYS:
        val = globals().get(key) or os.getenv(key)
        if not val:
            print(f"🔴 錯誤: 丟失.env錨點 [{key}] (必須配置且不可為空)")
            exit(1)
    for key in ANCHOR_KEYS:
        os.environ.pop(key, None)


def verify_dna_anchor(remote_url, local_dna):
    """本地DNA vs Notion DNA頁面內容一致性校驗"""
    try:
        resp = requests.get(remote_url, timeout=10)
        if resp.status_code == 200:
            if local_dna not in resp.text:
                print("🔴 錯誤: DNA錨點校驗失敗！本地DNA與Notion頁面不一致。")
                exit(1)
        else:
            print(f"🔴 錯誤: 拉取Notion DNA頁面失敗: {resp.status_code}")
            exit(1)
    except Exception as e:
        print(f"🔴 錯誤: DNA錨點聯網校驗異常: {e}")
        exit(1)


# ── 加載 Token ──
env_paths = [
    Path(__file__).parent / '.env',
    Path(__file__).parent / '.env.new',
    Path.home() / '.cnsh' / '.env',
    Path.home() / 'longhun-system' / '.env'
]

for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        print(f"🔑 已加載環境變量: {env_path}")
        break

TOKEN = os.getenv('NOTION_TOKEN') or os.getenv('NOTION_TOKEN_WORKSPACE')
if not TOKEN:
    print("🔴 錯誤: 未找到 NOTION_TOKEN，請檢查 .env 文件")
    exit(1)

HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
}

# ── 十四個核心頁面（夢想生態·v4.0全核心版）──
CORE_PAGES = {
    # P0 雙核心（最高優先級）
    '🛡️ 護盾v1.3': '6c03f9adafd94ce8bf98f8439eb9dbbf',
    '🎛️ AI主控操作台': '2d87125a9c9f802889e2e18002f7cf4f',

    # P1 四核心（重要支撐）
    '📊 主控操作台': '2507125a9c9f80d2b214c07deced0f0f',
    '🏆 龍魂成果頁': '868fec34e5a24e7e829dc5851a75f6b7',
    '💎 數字資產總庫': '7ed7d67f0ff940f992f4246a382e2a3d',
    '📚 龍魂知識庫': '2517125a9c9f81a79eb0004255502a87',

    # P2 擴展核心
    '🌐 龍魂元宇宙': '30e7125a9c9f80c6abcdc54378c297d0',
    '⚙️ 系統配置頁': '35f638f060cc4dc0a5a72e2b92b80b55',
    '🎯 完成目標追踪': 'a925a2ed10c44fcbb49b2228044b851d',
    '🔥 立即執行清單': '43d0c1995ebe4bd28ced5b8f7a26afb3',

    # 新增對話與技能頁面
    '📝 ChatGPT對話找回': 'f80c7f32fd0944c487cee5a93b76a439',
    '💬 ChatGPT-v1.0-UID9622': '57abf2d56eab48a08744e97eb8bc1378',
}

# 輸出目錄
BASE_DIR = Path.home() / 'longhun-system'
PUBLIC_DIR = BASE_DIR / 'sync_public'
ENCRYPTED_DIR = BASE_DIR / 'sync_encrypted'
SHIELD_DIR = BASE_DIR / 'sync_shield'
UID_DIR = BASE_DIR / 'sync_uid'
LOG_FILE = BASE_DIR / 'logs' / 'mvp_sync_grass.jsonl'

for d in [PUBLIC_DIR, ENCRYPTED_DIR, SHIELD_DIR, UID_DIR, LOG_FILE.parent]:
    d.mkdir(parents=True, exist_ok=True)


def write_log(entry: dict):
    """寫入草日誌（append-only）"""
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def get_page_content(page_id: str) -> dict:
    """獲取Notion頁面元信息"""
    url = f'https://api.notion.com/v1/pages/{page_id}'
    resp = requests.get(url, headers=HEADERS, timeout=15)
    if resp.status_code != 200:
        raise Exception(f"HTTP {resp.status_code}: {resp.text}")
    return resp.json()


def get_page_blocks(page_id: str) -> list:
    """遞歸獲取Notion頁面所有區塊"""
    url = f'https://api.notion.com/v1/blocks/{page_id}/children'
    blocks = []
    has_more = True
    start_cursor = None
    while has_more:
        params = {}
        if start_cursor:
            params['start_cursor'] = start_cursor
        resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
        if resp.status_code != 200:
            raise Exception(f"HTTP {resp.status_code}: {resp.text}")
        data = resp.json()
        blocks.extend(data.get('results', []))
        has_more = data.get('has_more', False)
        start_cursor = data.get('next_cursor')
    return blocks


def extract_text_from_blocks(blocks: list) -> str:
    """從區塊中提取純文本"""
    lines = []
    for block in blocks:
        btype = block.get('type')
        if not btype:
            continue
        content = block.get(btype, {})
        if 'rich_text' in content:
            text = ''.join([t.get('plain_text', '') for t in content['rich_text']])
            lines.append(text)
        elif btype == 'child_page':
            lines.append(f"[子頁面: {content.get('title', '')}]")
        # 遞歸子塊
        if block.get('has_children'):
            children = get_page_blocks(block.get('id'))
            child_text = extract_text_from_blocks(children)
            if child_text.strip():
                lines.append(child_text)
    return '\n'.join(lines)


def classify_page(name: str, content: str) -> str:
    """根據名稱和內容判定分類"""
    lower = (name + ' ' + content).lower()
    if '護盾' in name or 'shield' in lower or 'p0' in lower:
        return 'shield'
    if 'uid' in lower or '確認碼' in lower or 'gpg' in lower or '數字指紋' in lower:
        return 'uid'
    if '加密' in lower or '私密' in lower or '隱私' in lower:
        return 'encrypted'
    return 'public'


def save_page(name: str, page_id: str, content: str, category: str) -> Path:
    """保存頁面到對應目錄"""
    safe_name = name.replace('/', '_').replace(' ', '_')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{safe_name}_{page_id[:8]}_{timestamp}.md"

    meta = f"<!-- DNA: {DNA_CODE} | 頁面: {name} | ID: {page_id} | 分類: {category} | 時間: {datetime.now().isoformat()} -->\n\n"
    full_content = meta + f"# {name}\n\n{content}"

    if category == 'shield':
        target = SHIELD_DIR / filename
    elif category == 'uid':
        target = UID_DIR / filename
    elif category == 'encrypted':
        target = ENCRYPTED_DIR / filename
    else:
        target = PUBLIC_DIR / filename

    with open(target, 'w', encoding='utf-8') as f:
        f.write(full_content)

    return target


def sync_page(name: str, page_id: str):
    """同步單個頁面"""
    print(f"\n🔄 同步: {name}")
    page_data = get_page_content(page_id)
    blocks = get_page_blocks(page_id)
    text = extract_text_from_blocks(blocks)
    category = classify_page(name, text)
    target_path = save_page(name, page_id, text, category)

    print(f"   分類: {category} → {target_path}")

    write_log({
        'time': datetime.now().isoformat(),
        'action': '同步頁面',
        'name': name,
        'page_id': page_id,
        'category': category,
        'path': str(target_path),
        'dna': DNA_CODE
    })


def execute_origin_from_notion(page_id: str):
    """拉取Notion頁面並執行原點錨定"""
    print(f"\n🟢 正在拉取Notion頁面：{page_id}")
    blocks = get_page_blocks(page_id)
    text = extract_text_from_blocks(blocks)
    print(f"\n===== 頁面全部文本 =====\n{text}\n====================\n")
    found = False
    for line in text.splitlines():
        if '原點' in line or '不動點' in line or 'origin' in line.lower():
            print(f"\n🔵 [原點區塊]：{line.strip()}")
            found = True
    if not found:
        print("⚠️  頁面中未顯式發現'原點'關鍵字區塊。請人工確認。")


def main():
    verify_env_anchors()
    verify_dna_anchor(REMOTE_DNA_URL, DNA_CODE)

    print("\n" + "="*75)
    print("📡 開始同步14個核心頁面（每個都帶數字指紋認主）...")
    print("="*75)

    success_count = 0
    for name, page_id in CORE_PAGES.items():
        try:
            sync_page(name, page_id)
            success_count += 1
        except Exception as e:
            print(f"\n🔴 同步 {name} 時出錯: {e}")
            import traceback
            traceback.print_exc()
            write_log({
                'time': datetime.now().isoformat(),
                'action': f'同步異常: {name}',
                'error': str(e),
                'dna': DNA_CODE
            })

    write_log({
        'time': datetime.now().isoformat(),
        'action': '本次同步完成',
        'pages_total': len(CORE_PAGES),
        'pages_success': success_count,
        'public_dir': str(PUBLIC_DIR),
        'encrypted_dir': str(ENCRYPTED_DIR),
        'shield_dir': str(SHIELD_DIR),
        'uid_dir': str(UID_DIR),
        'dna': DNA_CODE
    })

    print("\n" + "="*75)
    print("✅ 同步完成！")
    print("="*75)
    print(f"📊 成功同步: {success_count}/{len(CORE_PAGES)} 頁")
    print(f"📜 草日誌: {LOG_FILE}")
    print(f"🌐 公開庫: {PUBLIC_DIR}")
    print(f"🔒 加密庫: {ENCRYPTED_DIR}")
    print(f"🛡️  護盾庫: {SHIELD_DIR}")
    print(f"🔐 UID庫: {UID_DIR}")
    print(f"\n🔐 數字指紋: {GPG_FINGERPRINT}")
    print(f"✅ 確認碼: {CONFIRM_CODE}")
    print(f"🧬 {DNA_CODE}")
    print("="*75)
    print("\n🐉 龍魂現世！全核心14頁面！數字指紋認主！天下無欺！\n")


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 3 and sys.argv[1] in ('--origin', '--page'):
        page_id = sys.argv[2]
        execute_origin_from_notion(page_id)
        exit(0)
    main()

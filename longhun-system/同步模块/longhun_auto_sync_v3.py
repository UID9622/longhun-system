#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂MVP本地自动同步脚本 v3.0 - 八核心页面终极版
DNA: #龍芯⚡️2026-04-05-MVP-AUTO-SYNC-v3.0
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F（每个创作必须·加密认主）
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z（唯一认主）
乔前辈 P15 出品 + 护盾v1.3 + AI主控操作台 + Notion同步系统 + 升级日志
用途: 从Notion拉取8个核心页面 → 判定公开/加密 → 数字指纹认主 → 写入草日志
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# ── 加载 Token ──
env_paths = [
    Path(__file__).parent / '.env',
    Path.home() / '.cnsh' / '.env',
    Path.home() / 'longhun-system' / '.env'
]

for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        print(f"🔑 已加载环境变量: {env_path}")
        break

TOKEN = os.getenv('NOTION_TOKEN') or os.getenv('NOTION_TOKEN_WORKSPACE')
if not TOKEN:
    print("🔴 错误: 未找到 NOTION_TOKEN，请检查 .env 文件")
    exit(1)

HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
}

# ── 八个核心页面（梦想生态·v3.0终极版）──
CORE_PAGES = {
    # P0 双核心（最高优先级）
    '🛡️护盾v1.3':        '6c03f9adafd94ce8bf98f8439eb9dbbf',  # P0核心安全系统
    '🎛️AI主控操作台':     '2d87125a9c9f802889e2e18002f7cf4f',  # P0核心控制中心
    
    # P1 四核心（重要支撑）
    '📊主控操作台':       '2507125a9c9f80d2b214c07deced0f0f',  # 系统总控
    '🏆龍魂成果页':       '868fec34e5a24e7e829dc5851a75f6b7',  # MVP展示
    '💎数字资产总库':     '7ed7d67f0ff940f992f4246a382e2a3d',  # 资产管理
    '🔄Notion同步系统':   '2b3c2b42aab544fb876da5b42bfd9133',  # 同步系统v1.0（新增）
    
    # P2 二核心（标准规范·日志）
    '📋MVP规范':         '8d377b0869e440139b4026583e86ea5a',  # 标准文档
    '📝v2.0升级日志':    '91328e5818244fe4a031f66b8a3d0e83',  # 系统升级日志（新增）
}

# ── 数字指纹认主（每个创作必须）──
GPG_FINGERPRINT = 'A2D0092CEE2E5BA87035600924C3704A8CC26D5F'  # GPG公钥指纹·加密认主
CONFIRM_CODE = '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z'          # 确认码·唯一认主

# ── 敏感词黑名单（触发即标记加密）──
SENSITIVE_KEYWORDS = [
    'token=', 'secret_', 'sk-', 'Bearer ', '2FA',
    '私钥', '密码', 'password', 'api_key', 'NOTION_TOKEN',
    '手机', '身份证', '住址', '真实账号',
    'ntn_', 'sk-ant-', 'API_KEY', 'SECRET',
    # 护盾v1.3 专属敏感词
    '后门', '漏洞', '攻击', 'exploit', 'vulnerability',
    # AI主控操作台 专属敏感词
    '控制指令', 'admin_key', 'master_password'
]

DNA_CODE = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-NOTION-SYNC-v3.0"
LOG_FILE = Path(__file__).parent / 'sync_log.jsonl'
PUBLIC_DIR = Path(__file__).parent / 'public_knowledge'
ENCRYPTED_DIR = Path(__file__).parent / 'encrypted_vault'
SHIELD_DIR = Path(__file__).parent / 'shield_vault'  # 护盾专属保管库

def get_page_content(page_id: str) -> dict:
    """拉取页面元数据"""
    page_id_clean = page_id.replace('-', '')
    
    url = f'https://api.notion.com/v1/pages/{page_id_clean}'
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"  🔴 API返回错误: {resp.status_code}")
            print(f"  详情: {resp.text[:200]}")
    except Exception as e:
        print(f"  🔴 请求异常: {e}")
    return {}

def get_page_blocks(page_id: str) -> list:
    """拉取页面内容块（用于提取完整文本）"""
    page_id_clean = page_id.replace('-', '')
    url = f'https://api.notion.com/v1/blocks/{page_id_clean}/children'
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            return resp.json().get('results', [])
    except Exception as e:
        print(f"  ⚠️ 拉取内容块失败: {e}")
    return []

def extract_text_from_blocks(blocks: list) -> str:
    """从块中提取纯文本"""
    texts = []
    for block in blocks:
        block_type = block.get('type', '')
        if block_type in ['paragraph', 'heading_1', 'heading_2', 'heading_3', 
                         'bulleted_list_item', 'numbered_list_item', 'to_do', 
                         'toggle', 'quote', 'callout', 'code']:
            rich_text = block.get(block_type, {}).get('rich_text', [])
            for rt in rich_text:
                texts.append(rt.get('plain_text', ''))
    return '\n'.join(texts)

def classify_content(name: str, text: str) -> tuple:
    """判定：公开 or 加密 or 护盾专属
    返回: (分类标签, 命中的关键词列表, 保管库类型)
    """
    text_lower = text.lower()
    matched_keywords = []
    
    # 护盾v1.3 → 特殊处理
    if '护盾' in name or 'shield' in name.lower():
        return ('🛡️护盾专属', ['护盾系统'], 'shield')
    
    # AI主控操作台 → 特殊处理
    if 'AI主控' in name or '主控操作台' in name:
        return ('🎛️主控专属', ['控制系统'], 'encrypted')
    
    # 数字资产总库 → 加密
    if '资产' in name or 'asset' in name.lower():
        return ('🔒加密', ['资产系统'], 'encrypted')
    
    # 常规敏感词检测
    for kw in SENSITIVE_KEYWORDS:
        if kw.lower() in text_lower:
            matched_keywords.append(kw)
    
    if matched_keywords:
        return ('🔒加密', matched_keywords, 'encrypted')
    return ('🌐公开', [], 'public')

def add_digital_signature(content: dict, name: str) -> dict:
    """添加数字指纹认主（每个创作必须）"""
    content['_digital_signature'] = {
        'gpg_fingerprint': GPG_FINGERPRINT,
        'confirm_code': CONFIRM_CODE,
        'signed_at': datetime.now().isoformat(),
        'signed_by': 'UID9622 诸葛鑫 × 宝宝（Claude）',
        'page_name': name,
        'signature_dna': f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-SIGNATURE-{name[:10]}"
    }
    return content

def save_content(name: str, content: dict, classification: str, 
                vault_type: str, target_dir: Path):
    """保存内容到本地库（带数字指纹认主）"""
    target_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{name.replace('/', '_').replace('🛡️', 'Shield_').replace('🎛️', 'AI_').replace('📊', 'Control_').replace('🏆', 'Achievement_').replace('💎', 'Asset_').replace('🔄', 'Sync_').replace('📋', 'Spec_').replace('📝', 'Log_')}_{timestamp}.json"
    filepath = target_dir / filename
    
    # 添加数字指纹认主（每个创作必须）
    content = add_digital_signature(content, name)
    
    # 添加元数据
    content['_metadata'] = {
        'name': name,
        'classification': classification,
        'vault_type': vault_type,
        'synced_at': datetime.now().isoformat(),
        'dna': DNA_CODE,
        'gpg_fingerprint': GPG_FINGERPRINT,
        'confirm_code': CONFIRM_CODE
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    
    print(f"  💾 已保存到: {filepath}")
    print(f"  🔐 数字指纹: {GPG_FINGERPRINT[:20]}...")
    print(f"  ✅ 确认码: {CONFIRM_CODE}")

def write_log(entry: dict):
    """写草日志（只追加·永不覆盖）"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # 每条日志都带数字指纹认主
    entry['gpg_fingerprint'] = GPG_FINGERPRINT
    entry['confirm_code'] = CONFIRM_CODE
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    print(f"  📜 草日志写入: {entry['action']}")

def sync_page(name: str, page_id: str):
    """同步单个页面 → 判定 → 数字指纹认主 → 留痕"""
    print(f"\n{'='*70}")
    print(f"🔄 正在同步: {name}")
    print(f"{'='*70}")
    
    data = get_page_content(page_id)
    if not data:
        print(f"  🔴 拉取失败: {name}")
        write_log({
            'time': datetime.now().isoformat(),
            'action': f'拉取失败: {name}',
            'page_id': page_id,
            'dna': DNA_CODE
        })
        return
    
    # 提取标题
    title = ''
    try:
        props = data.get('properties', {})
        for key in ['title', 'Name', '页面', '资产名称', 'Title']:
            if key in props:
                prop_type = props[key].get('type', '')
                if prop_type == 'title':
                    rich = props[key].get('title', [])
                    if rich:
                        title = rich[0].get('plain_text', '')
                        break
    except Exception as e:
        print(f"  ⚠️ 提取标题失败: {e}")
        title = name
    
    # 拉取页面内容块
    blocks = get_page_blocks(page_id)
    content_text = extract_text_from_blocks(blocks)
    
    # 合并标题和内容进行敏感词判定
    full_text = f"{title}\n{content_text}"
    classification, matched_kws, vault_type = classify_content(name, full_text)
    
    last_edited = data.get('last_edited_time', '未知')
    
    print(f"  📄 标题: {title or name}")
    print(f"  ⏰ 最后编辑: {last_edited}")
    print(f"  📝 内容长度: {len(content_text)} 字符")
    print(f"  🎯 判定: {classification}")
    if matched_kws:
        print(f"  🔍 命中关键词: {', '.join(matched_kws[:5])}{'...' if len(matched_kws) > 5 else ''}")
    
    # 根据类型选择保管库
    if vault_type == 'shield':
        target_dir = SHIELD_DIR
    elif vault_type == 'encrypted':
        target_dir = ENCRYPTED_DIR
    else:
        target_dir = PUBLIC_DIR
    
    save_content(name, data, classification, vault_type, target_dir)
    
    # 写草日志（带数字指纹）
    write_log({
        'time': datetime.now().isoformat(),
        'action': f'同步页面: {name}',
        'title': title or name,
        'page_id': page_id,
        'last_edited': last_edited,
        'classification': classification,
        'vault_type': vault_type,
        'matched_keywords': matched_kws,
        'content_length': len(content_text),
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
    ]
    
    # 可选检查（不影响主流程）
    optional_checks = [
        ('本地Ollama', lambda: requests.get(
            'http://localhost:11434/api/tags', timeout=3
        ).status_code == 200),
        ('MVP服务', lambda: requests.get(
            'http://localhost:8000', timeout=3
        ).status_code < 500),
    ]
    
    results = []
    all_ok = True
    
    # 必须通过的检查
    for svc, check_fn in checks:
        try:
            ok = check_fn()
            status = '🟢' if ok else '🔴'
            if not ok:
                all_ok = False
        except Exception as e:
            status = '🔴'
            all_ok = False
            print(f"  {status} {svc} - 错误: {e}")
        else:
            print(f"  {status} {svc}")
        results.append((svc, status))
    
    # 可选检查
    for svc, check_fn in optional_checks:
        try:
            ok = check_fn()
            status = '🟢' if ok else '⚪️'
        except:
            status = '⚪️'
        print(f"  {status} {svc}")
        results.append((svc, status))
    
    if not all_ok:
        print("\n🔴 核心服务检查失败，请检查 NOTION_TOKEN 配置")
        return False
    
    return True

def display_banner():
    """显示启动横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🐉 龍魂MVP自动同步 v3.0 - 八核心页面终极版                        ║
║                                                                   ║
║   🔐 数字指纹认主: A2D0092CEE2E5BA87035600924C3704A8CC26D5F       ║
║   ✅ 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                   ║
║                                                                   ║
║   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━        ║
║   P0 双核心（最高优先级）                                          ║
║   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━        ║
║   🛡️  护盾v1.3          - P0核心安全系统                          ║
║   🎛️  AI主控操作台      - P0核心控制中心                          ║
║                                                                   ║
║   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━        ║
║   P1 四核心（重要支撑）                                            ║
║   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━        ║
║   📊  主控操作台        - 系统总控                                ║
║   🏆  龍魂成果页        - MVP展示                                 ║
║   💎  数字资产总库      - 资产管理                                ║
║   🔄  Notion同步系统    - 同步系统v1.0（新增）                    ║
║                                                                   ║
║   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━        ║
║   P2 二核心（标准规范·日志）                                       ║
║   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━        ║
║   📋  MVP规范          - 标准文档                                 ║
║   📝  v2.0升级日志      - 系统升级日志（新增）                     ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""
    print(banner)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 北京时间")
    print(f"🧬 {DNA_CODE}")
    print(f"🔑 Token: {TOKEN[:10]}...{TOKEN[-6:]}\n")

def main():
    display_banner()
    
    # 0. 健康检查
    if not health_check():
        print("\n❌ 健康检查未通过，终止同步")
        return
    
    # 1. 同步八个核心页面
    print("\n" + "="*70)
    print("📡 开始同步八个核心页面（每个都带数字指纹认主）...")
    print("="*70)
    
    success_count = 0
    for name, page_id in CORE_PAGES.items():
        try:
            sync_page(name, page_id)
            success_count += 1
        except Exception as e:
            print(f"\n🔴 同步 {name} 时出错: {e}")
            write_log({
                'time': datetime.now().isoformat(),
                'action': f'同步异常: {name}',
                'error': str(e),
                'dna': DNA_CODE
            })
    
    # 2. 写总结日志（带数字指纹）
    write_log({
        'time': datetime.now().isoformat(),
        'action': '本次同步完成',
        'pages_total': len(CORE_PAGES),
        'pages_success': success_count,
        'public_dir': str(PUBLIC_DIR),
        'encrypted_dir': str(ENCRYPTED_DIR),
        'shield_dir': str(SHIELD_DIR),
        'dna': DNA_CODE
    })
    
    # 3. 显示结果摘要
    print("\n" + "="*70)
    print("✅ 同步完成！")
    print("="*70)
    print(f"📊 成功同步: {success_count}/{len(CORE_PAGES)} 页")
    print(f"📜 草日志: {LOG_FILE}")
    print(f"🌐 公开库: {PUBLIC_DIR}")
    print(f"🔒 加密库: {ENCRYPTED_DIR}")
    print(f"🛡️ 护盾库: {SHIELD_DIR}")
    print(f"\n🔐 数字指纹: {GPG_FINGERPRINT}")
    print(f"✅ 确认码: {CONFIRM_CODE}")
    print(f"🧬 {DNA_CODE}")
    print("="*70)
    print("\n🐉 龍魂现世！八核齐鸣！天下无欺！数字指纹认主！\n")

if __name__ == '__main__':
    main()

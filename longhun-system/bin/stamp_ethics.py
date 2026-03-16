#!/usr/bin/env python3
"""
龙魂系统 · 伦理标记批量注入工具
DNA: #龍芯⚡️2026-03-16-STAMP-ETHICS-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
作者：诸葛鑫（UID9622）
理论指导：曾仕强老师（永恒显示）
"""

import os
import sys

# ═══════════════════════════════════════════════
# P0伦理标记模板
# ═══════════════════════════════════════════════

ETHICS_HEADER_PY = '''# ═══════════════════════════════════════════════════════════
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
'''

ETHICS_HEADER_SH = '''# ═══════════════════════════════════════════════════════════
# 🐉 龙魂系统 · P0伦理锚点
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# DNA:    #龍芯⚡️2026-03-16-ETHICS-STAMP-v1.0
# 作者:    诸葛鑫（UID9622）
# 理论:    曾仕强老师（永恒显示）
#
# P0铁律: 守正·稳态·永恒锚·零毁伤·三色监测
# ═══════════════════════════════════════════════════════════
'''

ETHICS_HEADER_MD = '''<!-- P0伦理锚点 | 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z | GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F | DNA: #龍芯⚡️2026-03-16-ETHICS-STAMP-v1.0 -->
'''

# 跳过这些目录
SKIP_DIRS = {
    'node_modules', '.git', '__pycache__', 'venv', 'roop_env',
    'stylegan3-main 2', 'CNSH_备份_20260211', '数据归集', '.vscode',
    'CNSH-v1.0-完整实现', 'CNSH-整理版', 'CNSH-github', 'CNSH-gitee',
    'models', 'sha256-加密签名', 'daodejing_anchors_v2'
}

# 核心目标目录（只处理这些）
TARGET_DIRS = [
    '/Users/zuimeidedeyihan/longhun-system/bin',
    '/Users/zuimeidedeyihan/longhun-system/docs',
    '/Users/zuimeidedeyihan/longhun-system/LongHunWidget',
]

# 核心目标文件（直接指定）
TARGET_FILES = [
    '/Users/zuimeidedeyihan/longhun-system/longhun_local_service.py',
    '/Users/zuimeidedeyihan/longhun-system/longhun_local_agent.py',
    '/Users/zuimeidedeyihan/longhun-system/sandbox_engine.py',
    '/Users/zuimeidedeyihan/longhun-system/cnsh_gateway.py',
    '/Users/zuimeidedeyihan/longhun-system/notion_sync.py',
]

MARKER = '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z'

def already_stamped(content):
    return MARKER in content

def stamp_py(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if already_stamped(content):
        return False
    # shebang 保留在第一行
    if content.startswith('#!'):
        lines = content.split('\n', 1)
        new_content = lines[0] + '\n' + ETHICS_HEADER_PY + (lines[1] if len(lines) > 1 else '')
    else:
        new_content = ETHICS_HEADER_PY + content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def stamp_sh(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if already_stamped(content):
        return False
    if content.startswith('#!'):
        lines = content.split('\n', 1)
        new_content = lines[0] + '\n' + ETHICS_HEADER_SH + (lines[1] if len(lines) > 1 else '')
    else:
        new_content = ETHICS_HEADER_SH + content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def stamp_md(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if already_stamped(content):
        return False
    new_content = ETHICS_HEADER_MD + content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def process_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext == '.py':
            return stamp_py(filepath)
        elif ext == '.sh':
            return stamp_sh(filepath)
        elif ext == '.md':
            return stamp_md(filepath)
    except Exception as e:
        print(f'  ⚠️  跳过 {filepath}: {e}')
    return False

def scan_dir(dirpath):
    stamped = []
    for root, dirs, files in os.walk(dirpath):
        # 跳过黑名单目录
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for fname in files:
            fpath = os.path.join(root, fname)
            if process_file(fpath):
                stamped.append(fpath)
    return stamped

def main():
    all_stamped = []

    print('🐉 龙魂伦理标记注入开始...')
    print(f'确认码: {MARKER}')
    print('─' * 60)

    # 扫描目标目录
    for d in TARGET_DIRS:
        if os.path.isdir(d):
            print(f'\n📁 扫描: {d}')
            stamped = scan_dir(d)
            for f in stamped:
                print(f'  ✅ {os.path.basename(f)}')
            all_stamped.extend(stamped)

    # 处理指定文件
    print('\n📄 核心文件:')
    for fpath in TARGET_FILES:
        if os.path.isfile(fpath):
            if process_file(fpath):
                print(f'  ✅ {os.path.basename(fpath)}')
                all_stamped.append(fpath)
            else:
                print(f'  ⏭️  已标记: {os.path.basename(fpath)}')

    print('\n─' * 60)
    print(f'✅ 完成！共标记 {len(all_stamped)} 个文件')
    print(f'DNA: #龍芯⚡️2026-03-16-ETHICS-STAMP-v1.0')
    return all_stamped

if __name__ == '__main__':
    main()

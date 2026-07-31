# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·GIT-VISUAL-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
🐉 龍魂 Git 可视化面板（终端 TUI）
DNA: #龍芯⚡️丙午·辛未·GIT-VISUAL-v1.0

按模块级联分组展示 Git 变更，影响面标签，提交建议。

用法:
    python3 bin/lh_git_visual.py                   # 终端彩色面板
    python3 bin/lh_git_visual.py --json            # JSON输出
    python3 bin/lh_git_visual.py --commit-msg      # 生成提交信息建议
    python3 bin/lh_git_visual.py --stage           # 交互式暂存（按模块选择）
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict


# ═══════════════════════════════════════════════════════════
# ANSI 终端颜色
# ═══════════════════════════════════════════════════════════

class C:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    BG_BLACK = '\033[40m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_RED = '\033[41m'

# 模块映射：文件路径前缀 → 模块名 + 影响面标签 + 图标
MODULE_MAP = {
    'bin/lh_':           ('🐍 API接口',      '接口变更'),
    'bin/':              ('🔧 工具脚本',      '工具链变更'),
    'engine/':           ('⚙️ 引擎内核',      '引擎变更'),
    '引擎/':              ('⚙️ 引擎内核',      '引擎变更'),
    'deploy/':           ('🚀 部署配置',      '部署变更'),
    'config/':           ('⚙️ 系统配置',      '配置变更'),
    '.codebuddy/memory/':('🧠 系统记忆',      '记忆更新'),
    '.codebuddy/':       ('🧠 项目配置',      '配置变更'),
    'logs/':             ('📋 日志',          '日志变更'),
    'data/':             ('💾 数据层',        '数据变更'),
    'L7_数据层/':         ('💾 数据层',        '数据变更'),
    'L9_子系统/':         ('🧩 子系统',        '子系统变更'),
    'integrations/':     ('🔗 集成桥接',      '集成变更'),
}

# 审计关注标记
AUDIT_MARKERS = {
    'security':   ['key', 'secret', 'token', 'password', 'auth', 'credential'],
    'critical':   ['engine', 'launcher', 'registry', 'neural_net'],
    'memory':     ['memory', 'MEMORY'],
    'audit':      ['audit'],
}


# ═══════════════════════════════════════════════════════════
# Git 操作
# ═══════════════════════════════════════════════════════════

def run_git(*args) -> str:
    """Run git command, return stdout"""
    try:
        result = subprocess.run(
            ['git', '--no-pager'] + list(args),
            capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        return result.stdout.strip()
    except Exception as e:
        return ''


def get_git_root() -> str:
    return run_git('rev-parse', '--show-toplevel')


def get_status_files() -> List[Tuple[str, str]]:
    """
    获取所有变更文件
    Returns: [(status_code, file_path), ...]
    status_code: M=Modified, A=Added, D=Deleted, R=Renamed, ??=Untracked
    """
    output = run_git('status', '--porcelain')
    files = []
    for line in output.split('\n'):
        if not line.strip():
            continue
        if len(line) >= 3:
            status = line[:2].strip()
            filepath = line[3:].strip()
            # 跳过空的或.gitignore排除的
            if filepath and not filepath.startswith('"'):
                files.append((status, filepath))
    return files


def get_recent_commits(n: int = 5) -> List[str]:
    """获取最近的提交信息"""
    output = run_git('log', f'-{n}', '--oneline', '--no-decorate')
    return [line for line in output.split('\n') if line]


def get_branch_name() -> str:
    return run_git('branch', '--show-current')


def get_stash_count() -> int:
    output = run_git('stash', 'list')
    if not output:
        return 0
    return len(output.split('\n'))


# ═══════════════════════════════════════════════════════════
# 文件分类与影响分析
# ═══════════════════════════════════════════════════════════

def classify_file(filepath: str) -> Dict[str, Any]:
    """分类单个文件并评估影响面"""
    # 匹配模块
    module_name = '📁 其他'
    impact = '一般变更'
    icon = '📄'

    for prefix, (mod_name, imp_label) in MODULE_MAP.items():
        if filepath.startswith(prefix):
            module_name = mod_name
            impact = imp_label
            break

    # 提取图标
    icon = module_name.split(' ', 1)[0] if ' ' in module_name else '📄'

    # 审计关注
    audit_tags = []
    lower_path = filepath.lower()
    for tag, keywords in AUDIT_MARKERS.items():
        for kw in keywords:
            if kw in lower_path:
                audit_tags.append(tag)
                break

    # 文件类型
    ext = Path(filepath).suffix.lower()
    type_map = {
        '.py': 'Python',
        '.sh': 'Shell',
        '.md': 'Markdown',
        '.json': 'JSON/Config',
        '.env': 'Env/Secret',
        '.toml': 'TOML',
        '.yml': 'YAML',
        '.yaml': 'YAML',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.html': 'HTML',
        '.css': 'CSS',
    }
    file_type = type_map.get(ext, ext[1:].upper() if ext else 'Unknown')

    return {
        'path': filepath,
        'module': module_name,
        'module_name': module_name.split(' ', 1)[1] if ' ' in module_name else module_name,
        'icon': icon,
        'impact': impact,
        'audit_tags': audit_tags,
        'file_type': file_type,
        'filename': Path(filepath).name,
    }


def build_module_tree(files: List[Tuple[str, str]]) -> Dict[str, Any]:
    """构建模块变更树"""
    tree = defaultdict(lambda: {
        'added': [], 'modified': [], 'deleted': [], 'untracked': [],
        'has_audit': False, 'total': 0,
    })

    for status, filepath in files:
        info = classify_file(filepath)
        info['status'] = status

        module_key = info['module']

        if status == 'A':
            tree[module_key]['added'].append(info)
        elif status == 'D':
            tree[module_key]['deleted'].append(info)
        elif status == '??':
            tree[module_key]['untracked'].append(info)
        else:
            tree[module_key]['modified'].append(info)

        tree[module_key]['total'] += 1
        if info['audit_tags']:
            tree[module_key]['has_audit'] = True

    return dict(tree)


# ═══════════════════════════════════════════════════════════
# 渲染
# ═══════════════════════════════════════════════════════════

def status_color(status: str) -> str:
    colors = {
        'M': C.YELLOW, 'A': C.GREEN, 'D': C.RED,
        'R': C.MAGENTA, '??': C.CYAN,
    }
    return colors.get(status, C.WHITE)


def status_label(status: str) -> str:
    labels = {
        'M': '修改', 'A': '新增', 'D': '删除',
        'R': '重命名', '??': '未跟踪',
    }
    return labels.get(status, status)


def render_banner(branch, total_files, modified, added, deleted, untracked, stashes):
    """渲染顶部面板"""
    sections = []
    if modified > 0:
        sections.append(f'{C.YELLOW}修改 {modified}{C.RESET}')
    if added > 0:
        sections.append(f'{C.GREEN}新增 {added}{C.RESET}')
    if deleted > 0:
        sections.append(f'{C.RED}删除 {deleted}{C.RESET}')
    if untracked > 0:
        sections.append(f'{C.CYAN}未跟踪 {untracked}{C.RESET}')

    sep = ' │ '

    print(f"""
{C.CYAN}{C.BOLD}╔══════════════════════════════════════════════════════════╗
║     🐉 龍魂 Git 可视化面板                                   ║
║     DNA: #龍芯⚡️丙午·辛未·GIT-VISUAL-v1.0                   ║
╠══════════════════════════════════════════════════════════╣
║  🌿 分支: {C.GREEN}{branch}{C.CYAN}  │  文件变更: {C.BOLD}{total_files}{C.RESET}{C.CYAN}                             ║
║  {sep.join(sections)}{C.CYAN}  {' ' * (20 - len(sep.join(sections)) + len(C.YELLOW)+len(C.RESET) + len(C.GREEN)+len(C.RESET) + len(C.RED)+len(C.RESET) + len(C.CYAN)+len(C.RESET))}║
╚══════════════════════════════════════════════════════════╝{C.RESET}
""")


def render_module_tree(tree: Dict[str, Any], show_all: bool = True):
    """按模块分组渲染变更树"""
    # 排序：影响面越大越在前
    impact_order = {'🐍 API接口': 0, '⚙️ 引擎内核': 1, '🧩 子系统': 2, '🚀 部署配置': 3,
                    '💾 数据层': 4, '🔗 集成桥接': 5, '🔧 工具脚本': 6, '⚙️ 系统配置': 7,
                    '🧠 系统记忆': 8, '🧠 项目配置': 9, '📋 日志': 10, '📁 其他': 11}

    sorted_modules = sorted(tree.keys(), key=lambda m: impact_order.get(m, 99))

    for module in sorted_modules:
        data = tree[module]
        if data['total'] == 0 and not show_all:
            continue

        # 模块标题
        audit_mark = f' {C.RED}🔍审计{C.RESET}' if data['has_audit'] else ''
        print(f'{C.BOLD}{C.MAGENTA}  ▸ {module} ({data["total"]}个文件){audit_mark}{C.RESET}')

        # 各类变更
        sections = [
            ('modified',   f'{C.YELLOW}  修改{C.RESET}'),
            ('added',      f'{C.GREEN}  新增{C.RESET}'),
            ('deleted',    f'{C.RED}  删除{C.RESET}'),
            ('untracked',  f'{C.CYAN}  未跟踪{C.RESET}'),
        ]

        for key, section_label in sections:
            files_list = data.get(key, [])
            if not files_list:
                continue

            for f in files_list[:10]:  # 每模块最多显示10个
                sc = status_color(f['status'])
                sl = status_label(f['status'])

                # 影响面标签
                tags = []
                if f['audit_tags']:
                    for t in f['audit_tags']:
                        tag_colors = {'security': f'{C.RED}🔒安全{C.RESET}',
                                      'critical': f'{C.RED}⚡关键{C.RESET}',
                                      'memory': f'{C.BLUE}🧠记忆{C.RESET}',
                                      'audit': f'{C.BLUE}📝审计{C.RESET}'}
                        tags.append(tag_colors.get(t, f'[{t}]'))

                tag_str = ' '.join(tags) if tags else ''
                print(f'    {sc}[{sl}]{C.RESET} {C.DIM}{f["filename"]}{C.RESET}  {tag_str}')

            if len(files_list) > 10:
                print(f'    {C.DIM}... 还有 {len(files_list)-10} 个{C.RESET}')

        print()  # 模块之间空行


def render_diff_preview(files: List[Tuple[str, str]], max_files: int = 5):
    """渲染简要diff预览"""
    print(f'{C.BOLD}{C.CYAN}  ━━ Diff 预览 (最近 {max_files} 个修改) ━━{C.RESET}')
    modified = [(s, f) for s, f in files if s in ('M', 'A') and f.endswith('.py')][:max_files]

    if not modified:
        print(f'  {C.DIM}无 Python 文件变更预览{C.RESET}')
        print()
        return

    for status, filepath in modified:
        diff_output = run_git('diff', '--no-color', '--', filepath)
        if not diff_output:
            continue

        lines = diff_output.split('\n')
        added = sum(1 for l in lines if l.startswith('+') and not l.startswith('+++'))
        removed = sum(1 for l in lines if l.startswith('-') and not l.startswith('---'))

        filename = Path(filepath).name
        print(f'  {C.BOLD}{filename}{C.RESET}  {C.GREEN}+{added}{C.RESET} {C.RED}-{removed}{C.RESET}')

    print()


def suggest_commit_message(tree: Dict[str, Any]) -> str:
    """根据变更智能生成提交信息"""
    # 按影响面找出主要变更
    total = sum(d['total'] for d in tree.values())

    # 识别变更类型
    has_api = any('API接口' in m for m in tree)
    has_engine = any('引擎内核' in m for m in tree)
    has_deploy = any('部署配置' in m for m in tree)
    has_memory = any('系统记忆' in m for m in tree)
    has_data = any('数据层' in m for m in tree)
    has_tool = any('工具脚本' in m for m in tree)
    has_config = any('系统配置' in m for m in tree or '项目配置' in m)
    has_fix = any(f['audit_tags'] for d in tree.values()
                  for k in ['modified', 'added'] for f in d.get(k, []))

    # 提效类型前缀
    if has_fix:
        prefix = 'fix'
    elif has_api:
        prefix = 'feat(api)'
    elif has_engine:
        prefix = 'feat(engine)'
    elif has_deploy:
        prefix = 'chore(deploy)'
    elif has_memory:
        prefix = 'docs(memory)'
    elif has_config:
        prefix = 'chore(config)'
    elif has_data:
        prefix = 'feat(data)'
    else:
        prefix = 'chore'

    # 模块描述
    modules_changed = []
    for mod, data in sorted(tree.items(), key=lambda x: x[1]['total'], reverse=True):
        if data['total'] > 0:
            name = mod.split(' ', 1)[1] if ' ' in mod else mod
            modules_changed.append(name)
    modules_str = '/'.join(modules_changed[:3])

    dna_tag = '#龍芯⚡️丙午·辛未·GIT-AUTO-v1.0'

    message = f'{prefix}: {modules_str} ({total}文件变更) {dna_tag}'
    return message


# ═══════════════════════════════════════════════════════════
# 交互式暂存
# ═══════════════════════════════════════════════════════════

def interactive_stage(tree: Dict[str, Any]):
    """交互式暂存：按模块选择"""
    print(f'\n{C.CYAN}{C.BOLD}  🎯 交互式暂存（输入模块编号，用逗号分隔，或 all）{C.RESET}\n')

    modules = list(tree.keys())
    for i, mod in enumerate(modules):
        data = tree[mod]
        statuses = []
        if data['modified']:
            statuses.append(f'{C.YELLOW}M:{len(data["modified"])}{C.RESET}')
        if data['added']:
            statuses.append(f'{C.GREEN}A:{len(data["added"])}{C.RESET}')
        if data['untracked']:
            statuses.append(f'{C.CYAN}U:{len(data["untracked"])}{C.RESET}')
        print(f'  [{i+1}] {mod}  ({" | ".join(statuses)})')

    print(f'  [0] {C.RED}取消{C.RESET}')
    print()

    try:
        choice = input(f'  选择: ').strip()
    except (EOFError, KeyboardInterrupt):
        return

    if choice.lower() == 'all':
        run_git('add', '-A')
        print(f'  {C.GREEN}✅ 全部暂存完成{C.RESET}')
        return
    elif choice == '0':
        print(f'  {C.DIM}已取消{C.RESET}')
        return

    try:
        indices = [int(x.strip()) - 1 for x in choice.split(',')]
    except ValueError:
        print(f'  {C.RED}输入格式错误{C.RESET}')
        return

    for idx in indices:
        if 0 <= idx < len(modules):
            mod = modules[idx]
            data = tree[mod]
            all_files = data['modified'] + data['added'] + data['untracked']
            for f in all_files:
                run_git('add', f['path'])
            print(f'  {C.GREEN}✅ {mod} 已暂存{C.RESET}')


# ═══════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description='🐉 龍魂 Git 可视化面板')
    parser.add_argument('--json', action='store_true', help='JSON格式输出')
    parser.add_argument('--commit-msg', action='store_true', help='仅生成提交信息')
    parser.add_argument('--stage', action='store_true', help='交互式暂存')
    parser.add_argument('--diff', action='store_true', help='显示diff预览')
    parser.add_argument('--count', type=int, default=5, help='diff预览文件数')
    args = parser.parse_args()

    # 检查是否在git仓库中
    if not get_git_root():
        print(f'{C.RED}❌ 未在Git仓库中{C.RESET}')
        sys.exit(1)

    # 获取数据
    branch = get_branch_name()
    files = get_status_files()
    tree = build_module_tree(files)

    # 统计
    modified = sum(len(data['modified']) for data in tree.values())
    added = sum(len(data['added']) for data in tree.values())
    deleted = sum(len(data['deleted']) for data in tree.values())
    untracked = sum(len(data['untracked']) for data in tree.values())
    total = modified + added + deleted + untracked

    stashes = get_stash_count()

    # 输出模式
    if args.json:
        output = {
            'branch': branch,
            'stats': {'modified': modified, 'added': added, 'deleted': deleted,
                      'untracked': untracked, 'total': total, 'stashes': stashes},
            'modules': {},
            'suggested_commit': suggest_commit_message(tree),
            'recent_commits': get_recent_commits(5),
        }
        for mod, data in tree.items():
            output['modules'][mod] = {
                'total': data['total'],
                'modified': [f['path'] for f in data['modified']],
                'added': [f['path'] for f in data['added']],
                'deleted': [f['path'] for f in data['deleted']],
                'untracked': [f['path'] for f in data['untracked']],
                'has_audit_concern': data['has_audit'],
            }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    if args.commit_msg:
        print(suggest_commit_message(tree))
        print()
        print(f'{C.DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RESET}')
        print(f'{C.DIM}最近提交参考:{C.RESET}')
        for c in get_recent_commits(5):
            print(f'{C.DIM}  {c}{C.RESET}')
        return

    if args.stage:
        build_module_tree(files)  # refresh
        render_banner(branch, total, modified, added, deleted, untracked, stashes)
        interactive_stage(tree)
        return

    # 默认：完整可视化面板
    render_banner(branch, total, modified, added, deleted, untracked, stashes)

    if total == 0:
        print(f'{C.GREEN}  ✅ 工作区干净，无变更。{C.RESET}\n')
        return

    # 模块树
    render_module_tree(tree)

    # Diff 预览
    if args.diff:
        render_diff_preview(files, args.count)

    # 提交建议
    commit_msg = suggest_commit_message(tree)
    print(f'{C.BOLD}{C.CYAN}  💡 建议提交信息:{C.RESET}')
    print(f'{C.GREEN}  {commit_msg}{C.RESET}')
    print()

    print(f'{C.BOLD}{C.CYAN}  ━━ 最近提交 ━━{C.RESET}')
    for c in get_recent_commits(5):
        print(f'{C.DIM}  {c}{C.RESET}')

    print(f'''
{C.DIM}  ══════════════════════════════════════════════
  操作提示:
    python3 bin/lh_git_visual.py --stage    交互式暂存
    python3 bin/lh_git_visual.py --diff     查看diff预览
    python3 bin/lh_git_visual.py --commit-msg 仅生成提交信息
    python3 bin/lh_git_visual.py --json     JSON输出
  ══════════════════════════════════════════════{C.RESET}
''')


if __name__ == '__main__':
    main()

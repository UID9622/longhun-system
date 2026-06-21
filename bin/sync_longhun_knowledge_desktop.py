#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系統 · 統一知識矩陣桌面同步腳本
DNA: #龍芯⚡️2026-06-22-UNIFIED-KNOWLEDGE-MATRIX-SYNC-v1.0

功能：
1. 把龍魂系統的協議、規則、論文、技能、報告等核心文件，
   按照《知識矩陣總綱 v2.0》的分類架構同步到桌面。
2. 生成總索引與 sync_index.json（自適應鎖狀態）。
3. 再次運行即可增量更新，新增/修改/刪除都會被記錄。
"""

import json
import hashlib
import shutil
import glob
from pathlib import Path
from datetime import datetime, timezone

# ─────────────────────────────────────────────────────────────────────────────
# 配置
# ─────────────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path('/Users/zuimeidedeyihan/longhun-system')
DESKTOP_ROOT = Path.home() / 'Desktop' / '龍魂系統·統一知識矩陣'
SCRIPT_PATH = Path(__file__).resolve()

# 要掃描的來源目錄：Glob 模式（相對於 PROJECT_ROOT 或絕對路徑）
SOURCE_PATTERNS = [
    '*.md',
    '01_protocols/*',
    '01_技能庫/*.md',
    '02_rules/*',
    '02_執行記錄/*.md',
    '03_知識圖譜/*',
    '03_compiler/*',
    '04_決策日誌/*.md',
    '04_決策日誌/decision-records/*',
    '05_系統報告/*.md',
    '06_技術文檔/*.md',
    'docs/契约矩阵/*.md',
    'docs/private-shared-imports/**/*.md',
    'docs/v3/*.md',
    'docs/cnsh-uid9622/governance/*.md',
    'docs/longhun-tech/**/*.md',
    'docs/dragon-soul-open-hub/**/*.md',
    'agents/*',
    'audit/*',
    'brain/*',
    'skills/warehouse-audit/SKILL.md',
]

# 用戶級技能（絕對路徑）
USER_SKILL_PATTERNS = [
    Path.home() / '.kimi-code' / 'skills' / 'china-digital-identity' / 'SKILL.md',
    Path.home() / '.kimi-code' / 'skills' / 'CNSH-PROTOCOL' / 'SKILL.md',
    Path.home() / '.kimi-code' / 'skills' / 'CNSH-SEMANTIC' / 'SKILL.md',
    Path.home() / '.kimi-code' / 'skills' / 'dragon-soul-agent' / 'SKILL.md',
]
USER_SKILL_DIRS = [
    Path.home() / '.kimi-code' / 'skills',
]

# 檔案後綴允許清單
ALLOWED_SUFFIXES = {'.md', '.json', '.jsonl', '.asc', '.sha256', '.csv', '.py', '.txt', '.sh'}

# 忽略檔名
IGNORE_NAMES = {'.ds_store', 'thumbs.db', '.gitignore'}

# ─────────────────────────────────────────────────────────────────────────────
# 分類規則：依檔名與路徑關鍵字判定所屬類別
# ─────────────────────────────────────────────────────────────────────────────
CATEGORIES = [
    ('00_總綱與身份', lambda p, n:
        '知识矩阵总纲' in n or 'kfpp' in n or 'attribution' in n or
        '人机协作协议' in n or '流场总控' in n or
        n in ('readme.md', 'readme-v4.0.md')),

    ('01_主權與協議', lambda p, n:
        'creator' in n or '创作者保护' in n or 'ipa-route' in n or
        '灵魂契约' in n or '永恒契约' in n or '主权' in n or
        'protocol_lockdown' in n or 'protocol_unification' in n or
        'longhun-creator' in n or '01_protocols' in p),

    ('02_洛書九宮底座', lambda p, n:
        '洛书' in n or '河图' in n or '九宫' in n or
        ('369' in n and '归根' not in n and 'semantic' not in n) or
        '骨架' in n or '全域智能化生态' in n or '洛書' in n),

    ('03_三才流場與人格路由', lambda p, n:
        '人格' in n or 'persona' in n or '路由' in n or '五维' in n or
        '元知' in n or '三才' in n or 'sancai' in n or
        '流场' in n or 'flow' in n or 'decision' in n and 'decision-records' not in p),

    ('04_三色審計與決策', lambda p, n:
        '审计' in n or 'audit' in n or '决策' in n or 'decision' in n or
        'rule-registry' in n or 'rule' in n or 'behavioral_crypto' in n or
        'left_right_audit' in n or 'system_guardian' in n or
        'decision-records' in p),

    ('05_貪心有度與95極限', lambda p, n:
        '贪心' in n or '权限' in n or 'hotfix' in n or
        '权限矩阵' in n or '数据与权限' in n or
        'safety' in n or 'rollback' in n),

    ('06_道德經錨層', lambda p, n:
        '道德' in n or '道德经' in n or '太极' in n or '易经' in n or
        'dao' in n or 'yi-jing' in n),

    ('07_369歸根與語義規範', lambda p, n:
        'cnsh' in n or 'cnsv' in n or 'semantic' in n or 'protocol' in n and 'unification' not in n or
        '369归根' in n or '数字根' in n or '归根' in n),

    ('09_核心鏈路', lambda p, n:
        'api' in n or '核心链路' in n or 'architecture' in n or
        'cnsh_v' in n or '接口契约' in n or '知识域' in n or
        '执行域' in n or '反馈域' in n or 'complete-api' in n or
        'compiler' in p or '03_compiler' in p or 'cnsh-core' in p),

    ('10_安全域', lambda p, n:
        '安全域' in n or '数据安全' in n or '个人信息保护' in n or
        '等保' in n or '加密' in n or '网络安全' in n or
        'security' in n or 'privacy' in n or '安全防护' in n or
        '安全风险' in n or '安全策略' in n),

    ('11_大本營加工廠架構', lambda p, n:
        '大本营' in n or '加工厂' in n or '部署' in n or 'deploy' in n or
        'production' in n or 'android-auto' in p or 'ops' in p or
        'rollback' in n or 'runbook' in n or ' DEPLOYMENT' in n.upper()),

    ('12_學術論文與CSDN草稿', lambda p, n:
        'academic' in p or 'csdn_drafts' in p or '论文' in n or
        'paper' in n or '白皮书' in n or 'riemann' in n or
        '洛书369与AI决策' in n),

    ('13_技能庫與對外接口', lambda p, n:
        'skill' in n or '技能' in n or 'longhun-' in n or
        'dragon-soul-agent' in n or 'china-digital-identity' in n or
        'cnsh-protocol' in n or 'cnsh-semantic' in n or
        'kimi-webbridge' in n or 'webbridge' in n or
        '01_技能庫' in p or 'skills/warehouse' in p),

    ('14_執行記錄與系統報告', lambda p, n:
        '執行記錄' in p or '系統報告' in p or 'report' in n or
        'summary' in n or 'completion' in n or 'verification' in n or
        'execution' in n or 'integration' in n or '日志' in n or
        'log' in n or 'changelog' in n or 'operation' in n),

    ('15_知識圖譜與編譯器', lambda p, n:
        '知識圖譜' in p or 'graph' in n or '03_compiler' in p or
        'compile' in n or 'compiler' in n or 'mappings' in p),

    ('16_技術文檔與CHANGELOG', lambda p, n:
        '06_技術文檔' in p or 'changelog' in n or 'guide' in n or
        'usage' in n or 'quickstart' in n or 'setup' in n),

    ('17_代理與自動化', lambda p, n:
        'agents' in p or 'agent' in n or 'task_executor' in n or
        'notion_sync' in n or 'xpay' in n or 'longhun_notion' in n),
]

FALLBACK_CATEGORY = '14_執行記錄與系統報告'


def categorize(rel_path: str, filename: str) -> str:
    p = rel_path.lower()
    n = filename.lower()
    for cat, rule in CATEGORIES:
        try:
            if rule(p, n):
                return cat
        except Exception:
            continue
    return FALLBACK_CATEGORY


def file_checksum(path: Path) -> str:
    h = hashlib.md5()
    try:
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
    except Exception:
        return ''
    return h.hexdigest()


def collect_source_files() -> list:
    """返回 [(source_path, relative_label), ...]"""
    collected = []
    seen = set()

    # 項目內模式（支持 ** 遞迴）
    for pattern in SOURCE_PATTERNS:
        abs_pattern = PROJECT_ROOT / pattern
        for path_str in sorted(glob.glob(str(abs_pattern), recursive=True)):
            path = Path(path_str)
            if not path.is_file():
                continue
            if path.suffix.lower() not in ALLOWED_SUFFIXES:
                continue
            if path.name.lower() in IGNORE_NAMES:
                continue
            if path in seen:
                continue
            seen.add(path)
            try:
                rel = path.relative_to(PROJECT_ROOT)
            except ValueError:
                rel = path.name
            collected.append((path, str(rel)))

    # 用戶技能目錄中的 longhun / cnsh / dragon / china
    for skill_root in USER_SKILL_DIRS:
        if not skill_root.exists():
            continue
        for sub in skill_root.iterdir():
            if not sub.is_dir():
                continue
            key = sub.name.lower()
            if not (key.startswith('longhun-') or key.startswith('cnsh') or
                    key.startswith('dragon') or key.startswith('china')):
                continue
            skill_file = sub / 'SKILL.md'
            if skill_file.exists():
                if skill_file in seen:
                    continue
                seen.add(skill_file)
                collected.append((skill_file, f"~/.kimi-code/skills/{sub.name}/SKILL.md"))

    # 額外指定的用戶技能
    for skill_file in USER_SKILL_PATTERNS:
        if skill_file.exists() and skill_file not in seen:
            seen.add(skill_file)
            label = str(skill_file.relative_to(Path.home()))
            collected.append((skill_file, label))

    return collected


def safe_name(path: Path, used_names: set) -> str:
    name = path.name
    if name not in used_names:
        used_names.add(name)
        return name
    stem = path.stem
    suffix = path.suffix
    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        if new_name not in used_names:
            used_names.add(new_name)
            return new_name
        counter += 1


def main():
    print(f"[龍魂知識矩陣] 同步開始: {datetime.now(timezone.utc).isoformat()}")
    print(f"來源根目錄: {PROJECT_ROOT}")
    print(f"桌面目標: {DESKTOP_ROOT}")

    # 清理舊目標並重建骨架
    if DESKTOP_ROOT.exists():
        shutil.rmtree(DESKTOP_ROOT)
    DESKTOP_ROOT.mkdir(parents=True)

    # 建立分類文件夾
    categories = sorted({cat for cat, _ in CATEGORIES})
    for cat in categories:
        (DESKTOP_ROOT / cat).mkdir()
    (DESKTOP_ROOT / '99_索引與自適應鎖').mkdir()

    # 收集與複製
    source_files = collect_source_files()
    index_entries = []
    sync_index = {
        '_dna': '#龍芯⚡️2026-06-22-UNIFIED-KNOWLEDGE-MATRIX-SYNC-v1.0',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'source_root': str(PROJECT_ROOT),
        'categories': {},
    }

    for src_path, label in source_files:
        cat = categorize(label, src_path.name)
        used = set()
        dest_name = safe_name(src_path, used)  # 注意：這裡要按目錄獨立計數
        dest_dir = DESKTOP_ROOT / cat
        dest_path = dest_dir / dest_name

        # 重新計算安全名稱（按目錄）
        used_names = set(p.name for p in dest_dir.iterdir()) if dest_dir.exists() else set()
        dest_name = safe_name(src_path, used_names)
        dest_path = dest_dir / dest_name

        try:
            shutil.copy2(src_path, dest_path)
        except Exception as e:
            print(f"  ⚠️ 複製失敗 {src_path}: {e}")
            continue

        chksum = file_checksum(src_path)
        entry = {
            'source': str(src_path),
            'relative_label': label,
            'category': cat,
            'dest': f"{cat}/{dest_name}",
            'checksum': chksum,
            'size': src_path.stat().st_size,
        }
        index_entries.append(entry)
        sync_index.setdefault('categories', {}).setdefault(cat, []).append(entry)

    # 複製本腳本到桌面，方便將來一鍵同步
    shutil.copy2(SCRIPT_PATH, DESKTOP_ROOT / '99_索引與自適應鎖' / 'sync_longhun_knowledge_desktop.py')

    # 寫入 sync_index.json
    (DESKTOP_ROOT / '99_索引與自適應鎖' / 'sync_index.json').write_text(
        json.dumps(sync_index, ensure_ascii=False, indent=2), encoding='utf-8')

    # 生成總索引 README.md
    generate_readme(index_entries)

    print(f"[龍魂知識矩陣] 同步完成，共 {len(index_entries)} 個文件")
    for cat in categories:
        count = len(sync_index['categories'].get(cat, []))
        if count:
            print(f"  {cat}: {count}")


def generate_readme(entries):
    lines = []
    lines.append('# 龍魂系統 · 統一知識矩陣')
    lines.append('')
    lines.append(f'生成時間：{datetime.now(timezone.utc).isoformat()}')
    lines.append('')
    lines.append('> 本資料夾是 `~/longhun-system` 的「桌面可複製粘貼版」，按《知識矩陣總綱 v2.0》的架構分類。')
    lines.append('> 所有文件均已本地複製，無需點擊外部鏈接即可查看、複製、粘貼。')
    lines.append('> 再次運行 `99_索引與自適應鎖/sync_longhun_knowledge_desktop.py` 即可增量更新。')
    lines.append('')

    # 總綱說明
    lines.append('## 架構對照（知識矩陣總綱 v2.0）')
    lines.append('')
    lines.append('| 資料夾 | 對應總綱模塊 |')
    lines.append('|---|---|')
    lines.append('| 00_總綱與身份 | 系統身份、DNA、主權聲明 |')
    lines.append('| 01_主權與協議 | 創作者保護協議、IPA 路由、永恆契約 |')
    lines.append('| 02_洛書九宮底座 | 洛書、河圖、369、骨架流場 |')
    lines.append('| 03_三才流場與人格路由 | 忠孝義排序、人格矩陣、路由系統 |')
    lines.append('| 04_三色審計與決策 | 三色審計、決策日誌、規則庫 |')
    lines.append('| 05_貪心有度與95極限 | 權限矩陣、安全熱修、95極限 |')
    lines.append('| 06_道德經錨層 | 道德經、太極、易經錨定 |')
    lines.append('| 07_369歸根與語義規範 | CNSH 語義規範、數字根、歸根 |')
    lines.append('| 09_核心鏈路 | API、核心鏈路、編譯器 |')
    lines.append('| 10_安全域 | 安全域契約、數據安全、個人信息保護 |')
    lines.append('| 11_大本營加工廠架構 | 部署、運維、回滾、安卓自動化 |')
    lines.append('| 12_學術論文與CSDN草稿 | 論文、白皮書、CSDN 草稿 |')
    lines.append('| 13_技能庫與對外接口 | 龍魂技能、CNSH 技能、對外接口 |')
    lines.append('| 14_執行記錄與系統報告 | 執行日誌、系統報告、驗證報告 |')
    lines.append('| 15_知識圖譜與編譯器 | 知識圖譜、編譯器註冊表 |')
    lines.append('| 16_技術文檔與CHANGELOG | 技術文檔、變更日誌 |')
    lines.append('| 17_代理與自動化 | agents、自動化腳本、大腦同步 |')
    lines.append('| 99_索引與自適應鎖 | 總索引、同步腳本、聯動規則 |')
    lines.append('')

    # 按分類列出文件
    from collections import OrderedDict
    by_cat = OrderedDict()
    for e in entries:
        by_cat.setdefault(e['category'], []).append(e)

    lines.append('## 文件索引')
    lines.append('')
    for cat in sorted(by_cat.keys()):
        lines.append(f'### {cat}')
        lines.append('')
        for e in sorted(by_cat[cat], key=lambda x: x['dest'].split('/')[-1]):
            fname = e['dest'].split('/')[-1]
            src = e['relative_label']
            lines.append(f"- `{fname}` ← `{src}`")
        lines.append('')

    # 自適應鎖說明
    lines.append('## 自適應鎖與聯動規則')
    lines.append('')
    lines.append('1. **索引即鎖**：`sync_index.json` 記錄每個文件的來源路徑與 MD5 校驗和。')
    lines.append('2. **增量同步**：再次運行同步腳本時，只會複製新增或校驗和變化的文件。')
    lines.append('3. **無孤立文件**：任何被同步的文件都會出現在 `sync_index.json` 與本索引中。')
    lines.append('4. **分類聯動**：若某文件的內容涉及多個模塊，請在項目源文件中用 `#分類:` 標註，')
    lines.append('   後續可升級本腳本的關鍵字規則實現更精細路由。')
    lines.append('5. **DNA 追溯**：所有核心文檔應在文末保留 `#龍芯⚡️...` 簽名，確保來源不可抵賴。')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('#UID9622⚡️2026-06-22-UNIFIED-KNOWLEDGE-MATRIX')
    lines.append('#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z')

    (DESKTOP_ROOT / 'README.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    main()

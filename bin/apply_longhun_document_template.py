#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂文檔標準模板批量套用腳本
DNA: #龍芯⚡️2026-06-22-LONGHUN-TEMPLATE-APPLY-v1.0

功能：
- 掃描指定目錄下的 Markdown 文件。
- 若文件尚未按《龍魂文檔標準模板 v1.0》整理，則自動補充：
  標題、性質、版本、作者、授權、平台、審核狀態、DNA、CONFIRM、
  摘要、關鍵詞、引用與溯源、誠實局限、修改記錄、分類標籤。
- 已整理的文件會被跳過（idempotent）。
"""

import re
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path('/Users/zuimeidedeyihan/longhun-system')
TODAY = datetime.now(timezone.utc).strftime('%Y-%m-%d')

# 要處理的目錄（相對於 PROJECT_ROOT）
TARGET_DIRS = [
    '01_protocols',
    '01_技能庫',
    '06_技術文檔',
    'docs/契约矩阵',
    'docs/private-shared-imports',
    'docs/cnsh-uid9622',
    'docs/longhun-tech',
    'docs/dragon-soul-open-hub/academic',
    'docs/dragon-soul-open-hub/governance',
    'docs/dragon-soul-open-hub/security',
    'docs/dragon-soul-open-hub/agent-specs',
]

TEMPLATE_MARKER = '本文檔按《龍魂文檔標準模板 v1.0》整理'
DNA_RE = re.compile(r'(#[龍芯UID9622]+⚡️\S+)')
VERSION_RE = re.compile(r'[vV]?(\d+\.\d+(?:\.\d+)?)')


def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s).strip('-')
    return s[:50]


def detect_title(content: str, filename: str) -> str:
    for line in content.splitlines()[:10]:
        m = re.match(r'^#\s+(.+)$', line)
        if m:
            return m.group(1).strip()
    stem = Path(filename).stem
    # 去掉 uuid hash 後綴
    stem = re.sub(r'\s+[a-f0-9]{32}$', '', stem)
    return stem.replace('_', ' ').replace('-', ' ').strip()


def detect_version(content: str, filename: str) -> str:
    m = VERSION_RE.search(filename)
    if m:
        return f"v{m.group(1)}"
    m = VERSION_RE.search(content[:2000])
    if m:
        return f"v{m.group(1)}"
    return 'v1.0.0'


def detect_dna(content: str, title: str) -> str:
    m = DNA_RE.search(content)
    if m:
        return m.group(1)
    slug = slugify(title)
    return f"#龍芯⚡️{TODAY}-{slug}"


def detect_nature(path: Path) -> str:
    p = str(path).lower()
    if 'protocol' in p or '協議' in p or '协议' in p:
        return '協議'
    if 'rule' in p or '規則' in p or '规则' in p:
        return '規則'
    if 'academic' in p or '論文' in p or '论文' in p or 'csdn_drafts' in p:
        return '觀察性論文/技術博客'
    if 'governance' in p or '治理' in p:
        return '治理規範'
    if 'security' in p or '安全' in p:
        return '安全規範'
    if 'agent-specs' in p or 'spec' in p:
        return '技術規範'
    if 'skill' in p or '技能' in p:
        return '技能說明'
    return '技術文檔'


def detect_platform(path: Path) -> str:
    p = str(path).lower()
    parts = []
    if 'csdn' in p:
        parts.append('CSDN')
    if 'gitee' in p or 'gitcode' in p:
        parts.append('Gitee')
    if 'github' in p:
        parts.append('GitHub')
    if not parts:
        parts.append('本地')
    return ' / '.join(parts)


def build_header(title: str, nature: str, version: str, dna: str, platform: str) -> str:
    return f"""# {title}

> 本文檔按《龍魂文檔標準模板 v1.0》整理。
> 性質：{nature} · 未經同行評審（如適用）
> 版本：{version}
> 作者：UID9622 · 龍芯北辰
> 協作者：（待補充，如無請刪除此行）
> 授權：CC BY-NC-SA 4.0 · 科技主權歸屬 UID9622 · 中華人民共和國
> 平台：{platform}
> 審核狀態：草稿

**DNA**: `{dna}`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

"""


def build_footer(title: str, dna: str) -> str:
    return f"""

---

## 摘要

（請在此用不超過 256 字說明本文檔的核心內容、性質與局限。）

## 關鍵詞

（請列出 5–10 個關鍵詞，中英文對照優先。）

## 引用與溯源

- 本文檔引用或參考了以下來源：
  - [1] （請填寫）
- 相關龍魂系統文檔：
  - 《龍魂文檔標準模板 v1.0》(#龍芯⚡️2026-06-22-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 誠實局限

1. （請列出本分析的第一條局限或不確定性。）
2. （請列出第二條。）
3. （請列出第三條。）

## 修改記錄

| 日期 | 版本 | 修改人 | 修改內容 | 審核狀態 |
|---|---|---|---|---|
| {TODAY} | v1.0.0 | UID9622 | 按《龍魂文檔標準模板 v1.0》整理 | 草稿 |

## 分類標籤

- 總綱模塊：（請勾選，例如 #知識矩陣 #安全域）
- 對外狀態：（請勾選，例如 #Gitee #GitHub #CSDN）
- 審計色：#黃色待審

## DNA 簽名

```
{dna}
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
"""


def process_file(path: Path) -> dict:
    rel = path.relative_to(PROJECT_ROOT)
    try:
        content = path.read_text(encoding='utf-8')
    except Exception as e:
        return {'file': str(rel), 'status': 'error', 'reason': str(e)}

    if TEMPLATE_MARKER in content:
        return {'file': str(rel), 'status': 'skipped', 'reason': 'already templated'}

    if content.startswith('#!'):
        return {'file': str(rel), 'status': 'skipped', 'reason': 'executable script'}

    title = detect_title(content, path.name)
    version = detect_version(content, path.name)
    dna = detect_dna(content, title)
    nature = detect_nature(path)
    platform = detect_platform(path)

    header = build_header(title, nature, version, dna, platform)
    footer = build_footer(title, dna)

    # 若原始內容第一個非空行就是與檢測標題相同的 # 標題，則不再重複插入標題
    stripped = content.lstrip()
    starts_with_same_heading = stripped.startswith(f'# {title}\n') or stripped.startswith(f'# {title}\r')

    if content.startswith('---\n'):
        idx = content.find('\n---\n', 4)
        if idx != -1:
            split = idx + 5
            body = content[split:].lstrip()
            if body.startswith(f'# {title}'):
                new_content = content[:split] + '\n' + header + body + footer
            else:
                new_content = content[:split] + '\n' + header + body + footer
        else:
            new_content = header + content + footer
    elif starts_with_same_heading:
        new_content = header + stripped + footer
    else:
        new_content = header + content + footer

    try:
        path.write_text(new_content, encoding='utf-8')
    except Exception as e:
        return {'file': str(rel), 'status': 'error', 'reason': str(e)}

    return {'file': str(rel), 'status': 'templated', 'title': title, 'dna': dna}


def main():
    results = []
    for d in TARGET_DIRS:
        base = PROJECT_ROOT / d
        if not base.exists():
            continue
        for path in sorted(base.rglob('*.md')):
            results.append(process_file(path))

    templated = [r for r in results if r['status'] == 'templated']
    skipped = [r for r in results if r['status'] == 'skipped']
    errors = [r for r in results if r['status'] == 'error']

    print(f'已處理：{len(results)} 個 Markdown 文件')
    print(f'  新套用模板：{len(templated)}')
    print(f'  已整理/跳過：{len(skipped)}')
    print(f'  錯誤：{len(errors)}')

    # 保存登記冊
    registry = {
        '_dna': '#龍芯⚡️2026-06-22-LONGHUN-TEMPLATE-APPLY-v1.0',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'templated_count': len(templated),
        'skipped_count': len(skipped),
        'error_count': len(errors),
        'templated': templated,
        'skipped': skipped,
        'errors': errors,
    }
    out = PROJECT_ROOT / 'docs/契约矩阵/龍魂文档标准化登记册.json'
    out.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'登記冊已保存：{out}')


if __name__ == '__main__':
    main()

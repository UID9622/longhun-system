#!/usr/bin/env python3
#龍芯⚡️2026-06-22-LONGHUN-TEMPLATE-APPLY-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂文档标准模板批量套用脚本
DNA: #龍芯⚡️2026-06-22-LONGHUN-TEMPLATE-APPLY-v1.0

功能：
- 扫描指定目录下的 Markdown 文件。
- 若文件尚未按《龍魂文档标准模板 v1.0》整理，则自动补充：
  标题、性质、版本、作者、授权、平台、审核状态、DNA、CONFIRM、
  摘要、关键词、引用与溯源、诚实局限、修改记录、分类标签。
- 已整理的文件会被跳过（idempotent）。
"""

import re
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path('/Users/zuimeidedeyihan/longhun-system')
TODAY = datetime.now(timezone.utc).strftime('%Y-%m-%d')

# 要处理的目录（相对于 PROJECT_ROOT）
TARGET_DIRS = [
    '01_protocols',
    '01_技能库',
    '06_技术文档',
    'docs/契约矩阵',
    'docs/private-shared-imports',
    'docs/cnsh-uid9622',
    'docs/longhun-tech',
    'docs/dragon-soul-open-hub/academic',
    'docs/dragon-soul-open-hub/governance',
    'docs/dragon-soul-open-hub/security',
    'docs/dragon-soul-open-hub/agent-specs',
]

TEMPLATE_MARKER = '本文档按《龍魂文档标准模板 v1.0》整理'
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
    # 去掉 uuid hash 后缀
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
    if 'protocol' in p or '协议' in p or '协议' in p:
        return '协议'
    if 'rule' in p or '规则' in p or '规则' in p:
        return '规则'
    if 'academic' in p or '论文' in p or '论文' in p or 'csdn_drafts' in p:
        return '观察性论文/技术博客'
    if 'governance' in p or '治理' in p:
        return '治理规范'
    if 'security' in p or '安全' in p:
        return '安全规范'
    if 'agent-specs' in p or 'spec' in p:
        return '技术规范'
    if 'skill' in p or '技能' in p:
        return '技能说明'
    return '技术文档'


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

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：{nature} · 未经同行评审（如适用）
> 版本：{version}
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充，如无请删除此行）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：{platform}
> 审核状态：草稿

**DNA**: `{dna}`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

"""


def build_footer(title: str, dna: str) -> str:
    return f"""

---

## 摘要

（请在此用不超过 256 字说明本文档的核心内容、性质与局限。）

## 关键词

（请列出 5–10 个关键词，中英文对照优先。）

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] （请填写）
- 相关龍魂系统文档：
  - 《龍魂文档标准模板 v1.0》(#龍芯⚡️2026-06-22-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 诚实局限

1. （请列出本分析的第一条局限或不确定性。）
2. （请列出第二条。）
3. （请列出第三条。）

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| {TODAY} | v1.0.0 | UID9622 | 按《龍魂文档标准模板 v1.0》整理 | 草稿 |

## 分类标签

- 总纲模块：（请勾选，例如 #知识矩阵 #安全域）
- 对外状态：（请勾选，例如 #Gitee #GitHub #CSDN）
- 审计色：#黄色待审

## DNA 签名

```
{dna}
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
"""


def process_file(path: Path) -> dict[str, Any]:
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

    # 若原始内容第一个非空行就是与检测标题相同的 # 标题，则不再重复插入标题
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

    print(f'已处理：{len(results)} 个 Markdown 文件')
    print(f'  新套用模板：{len(templated)}')
    print(f'  已整理/跳过：{len(skipped)}')
    print(f'  错误：{len(errors)}')

    # 保存登记册
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
    print(f'登记册已保存：{out}')


if __name__ == '__main__':
    main()

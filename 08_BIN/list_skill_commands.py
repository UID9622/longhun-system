#!/usr/bin/env python3
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-LIST_SKILL_COMMANDS-04A74A97
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
from pathlib import Path
import re
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

roots = [Path.home()/'.kimi-code/skills', Path.home()/'.agents/skills']
rows = []
for root in roots:
    for md in sorted(root.glob('*/SKILL.md')):
        text = md.read_text(encoding='utf-8', errors='ignore')
        lines = text.splitlines()
        title = md.parent.name
        in_front = False
        for line in lines[:20]:
            l = line.strip()
            if l == '---':
                in_front = not in_front
                continue
            if in_front:
                continue
            if l.startswith('#'):
                title = l.strip('# ')
                break
            if l:
                title = l[:80]
                break
        usage = '-'
        # look for explicit usage/launch sections
        keywords = re.compile(r'^(#+\s*)?(用法|启动|命令|CLI|快速开始|Quick Start|运行|执行|示例|Example|入口)', re.I)
        for i, line in enumerate(lines[:150]):
            if keywords.search(line):
                # collect following code block or command lines
                collected = []
                for j in range(i+1, min(i+12, len(lines))):
                    l = lines[j].strip()
                    if not l or l.startswith('#'):
                        continue
                    if l.startswith('```'):
                        # collect until end of block
                        block = []
                        for k in range(j+1, min(j+8, len(lines))):
                            if lines[k].strip().startswith('```'):
                                break
                            block.append(lines[k].strip()[:120])
                        collected.append(' | '.join(block[:3]))
                        break
                    if re.search(r'^(python3|bash|lh-|cnsh|node|npm|/Users|\$ )', l):
                        collected.append(l[:160])
                        if len(collected) >= 2:
                            break
                if collected:
                    usage = ' / '.join(collected[:2])
                break
        if usage == '-':
            # fallback: any line with explicit command
            for line in lines[:80]:
                l = line.strip()
                if re.search(r'^(python3|bash|lh-|cnsh|node|npm|/Users/[^/]+/\.(kimi-code|agents|longhun)/)', l):
                    usage = l[:160]
                    break
        rows.append((root.name, md.parent.name, title, usage))

for scope, name, title, usage in rows:
    print(f"- `{name}` ({scope}): {title}")
    print(f"  启动: {usage}")

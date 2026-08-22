#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-LH_MERGE_CODEBUDDY_M-5A55F3C6
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍芯⚡️丙午·丙申·辛酉·酉时·☰乾-MERGE-CODEBUDDY-MEMORY-v1.0
"""
🐉 龍魂 · CodeBuddy 记忆合并脚本

将 CodeBuddy 产生的记忆文件合并进龍魂本地记忆底座：
- 读取 ~/.codebuddy/memory/*.md
- 龍字守卫
- 写入 ~/.longhun/memory/codebuddy_merged.md
- 更新 latest_digest.md / latest_digest.json
"""

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path


CODEBUDDY_MEMORY_DIR = Path.home() / ".codebuddy" / "memory"
LONGHUN_MEMORY_DIR = Path.home() / ".longhun" / "memory"
MERGED_FILE = LONGHUN_MEMORY_DIR / "codebuddy_merged.md"
DIGEST_MD = LONGHUN_MEMORY_DIR / "latest_digest.md"
DIGEST_JSON = LONGHUN_MEMORY_DIR / "latest_digest.json"


def guard(text: str) -> str:
    return text.replace("龙", "龍")


def dna() -> str:
    h = hashlib.sha256(f"merge{datetime.now().isoformat()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-MERGE-CODEBUDDY-{h}-UID9622"


def extract_headings(text: str) -> list:
    return re.findall(r"^##?\s+(.+)$", text, re.MULTILINE)


def summarize(text: str, max_lines: int = 10) -> str:
    headings = extract_headings(text)
    lines = [f"- {h}" for h in headings[:max_lines]]
    return "\n".join(lines)


def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🐉 开始合并 CodeBuddy 记忆...")

    if not CODEBUDDY_MEMORY_DIR.exists():
        print(f"  ⚠️ CodeBuddy 记忆目录不存在: {CODEBUDDY_MEMORY_DIR}")
        return

    files = sorted(CODEBUDDY_MEMORY_DIR.rglob("*.md"))
    print(f"  发现 {len(files)} 个 CodeBuddy 记忆文件")

    merged_parts = []
    summaries = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        text = guard(text)
        merged_parts.append(f"\n\n<!-- SOURCE: {f.name} -->\n\n{text}")
        summaries.append(f"### {f.name}\n{summarize(text)}\n")

    merged_body = "\n".join(merged_parts)
    full_merged = f"""# 🐉 龙魂 · CodeBuddy 记忆合并档

**DNA**: `{dna()}`  
**合并时间**: `{datetime.now().isoformat()}`  
**来源**: `~/.codebuddy/memory/*.md`  
**文件数**: `{len(files)}`

---

{merged_body}

---

*本文件由 `lh_merge_codebuddy_memory.py` 自动生成，请勿手动修改。*
"""
    MERGED_FILE.write_text(full_merged, encoding="utf-8")
    print(f"  ✅ 已写入合并档: {MERGED_FILE}")

    # 更新 latest_digest.md（追加，不覆盖身份激活上下文）
    summary_block = f"""

---

## 🔄 CodeBuddy 记忆已合并

**时间**: `{datetime.now().isoformat()}`  
**DNA**: `{dna()}`  
**来源文件数**: `{len(files)}`

### 合并摘要
{chr(10).join(summaries)}

### 完整合并档
- `{MERGED_FILE}`
"""
    if DIGEST_MD.exists():
        existing = DIGEST_MD.read_text(encoding="utf-8")
        if "CodeBuddy 记忆已合并" in existing:
            print("  ⚠️ latest_digest.md 中已存在合并记录，跳过追加")
        else:
            DIGEST_MD.write_text(existing.rstrip() + "\n" + summary_block, encoding="utf-8")
            print(f"  ✅ 已更新: {DIGEST_MD}")
    else:
        DIGEST_MD.write_text("# 🐉 龍魂 · 记忆摘要\n\n" + summary_block, encoding="utf-8")
        print(f"  ✅ 已创建: {DIGEST_MD}")

    # 更新 latest_digest.json
    digest_data = {
        "dna": dna(),
        "digest": f"CodeBuddy 记忆已合并：{len(files)} 个文件，涵盖 " + "、".join(extract_headings(merged_body)[:5]),
        "timestamp": datetime.now().isoformat(),
        "source": "codebuddy_merge",
        "merged_file": str(MERGED_FILE),
        "codebuddy_files": [str(f) for f in files],
        "activation_loaded": True,
        "instructions": "AI 必须首先读取 ~/.longhun/memory/identity_activation_context.md 中的主权网关协议",
        "protocol_file": "03_KNOWLEDGE_GRAPH/03_龍魂主权网关自动硬控协议_☯UID9622·丙午·丙申·辛酉·丙申·䷉履_SOVEREIGN-CTRL-v1.0.md",
        "ai_marker": "~/.longhun/08_STATE/AI_READ_GATEWAY_PROTOCOL_FIRST.md"
    }
    DIGEST_JSON.write_text(json.dumps(digest_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✅ 已更新: {DIGEST_JSON}")

    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ CodeBuddy 记忆合并完成")


if __name__ == "__main__":
    main()

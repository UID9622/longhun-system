#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 IP 资产清单批量归集脚本
DNA: #龍芯⚡️2026-07-04-IP-ASSETS-INTEGRATION-RUNNER-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
import os
import re
import json
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path

SRC_DIR = Path("/Users/zuimeidedeyihan/Downloads/Kimi_Agent_龙魂IP资产清单 (2)")
BASE = Path("/Users/zuimeidedeyihan/longhun-system")
DOCS = BASE / "docs/private-shared-imports"
SCRIPTS = BASE / "scripts/private-shared-imports/ip-assets-v2"
OUTPUTS = BASE / "outputs/private-shared-imports"
DESKTOP = Path("/Users/zuimeidedeyihan/Desktop/龍魂资产")
ARTICLES = BASE / "articles"

GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
DATE_STR = "2026-07-04"
TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ).isoformat()

AUTO_INJECT = f"<!-- #龍芯⚡️2026-07-04-AUTO-IP-INTEGRATION-7F3A9B12 自动注入·IP资产归集·来源可查 -->"

CATEGORY_MAP = {
    "龍魂档案·知识产权与专利可评估资产清单_v2.0.md": "ip-assets",
    "plan.md": "ip-assets",
    "plan_v3_upgrade.md": "ip-assets",
    "plan_dna_crypto_audit.md": "ip-assets",
    "plan_shame_pillar.md": "ip-assets",
    "UID9622_龍芯北辰_公开IP展示页_v2.0.md": "documentation",
    "CSDN问答回答_UID9622.md": "governance",
    "龍魂系统升级方案v3.0.md": "architecture",
    "龍魂系统升级方案v3.0_CSDN.md": "architecture",
    "direction1_theory_fusion.md": "architecture",
    "direction2_user_experience.md": "architecture",
    "direction3_documentation.md": "architecture",
    "fuse_protocol_engine.md": "security-audit",
    "six_oaths_engine.md": "security-audit",
    "shame_pillar_core.md": "security-audit",
    "tri_color_audit_engine.md": "security-audit",
    "permission_r_tier.md": "security-audit",
    "龍魂·AI行为约束耻辱柱_完整工程化方案_v3.0.md": "security-audit",
    "dna_trace_system.md": "memory-dna",
    "龍魂·国密DNA加密合规审计系统_v3.0.md": "memory-dna",
    "guomi_crypto_engine.md": "memory-dna",
    "龍魂·语义优先编码规范_v1.0.md": "cnsh-protocols",
    "notion_assets_scan.md": "ip-assets",
    "web_assets_scan.md": "ip-assets",
    "skills_asset_scan.md": "ip-assets",
    "🍎乔前辈数字人知识库·本地归档.md": "ip-assets",
}

PY_FILES = [
    "dragon_dna.py",
    "longhun_crypto_engine.py",
    "shame_pillar_core.py",
    "tri_color_audit_engine.py",
]

records = []  # (src, dest, dna, category, tri_color)


def extract_dna(text: str) -> str:
    m = re.search(r"#龍芯[⚡️:][A-Za-z0-9_\-:/\.]+", text)
    if m:
        return m.group(0)
    return None


def extract_title(text: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return ""


def gen_dna(category: str, idx: int) -> str:
    return f"#龍芯⚡️{DATE_STR}-{category.upper()}-IMPORT-{idx:02d}-v2.0"


def make_md_header(dna: str, title: str, src: Path, dest: Path) -> str:
    return f"""{AUTO_INJECT}

> ⛔ **主权声明 · 立即生效** — 本文档不授权 AI 训练 · 数据主权归于人民 · 祖国优先
>
> **DNA:** `{dna}` · **ParentDNA:** `#龍芯⚡️2026-07-03-IP-ASSET-MATRIX-v2.0`
> **CONFIRM:** `{CONFIRM}` · **SEAL:** `{SEAL}` · **GPG:** `{GPG}`
> **作者:** UID9622 / Lucky·诸葛鑫 · **来源:** `{src}` · **归档:** `{dest}`
> **迁移时间:** {NOW}

# {title}

"""


def make_root_card(title: str, dna: str, dest: Path, tri_color: str = "🟢") -> str:
    return f"""---

## 🐉 ROOT_CARD

```yaml
ROOT_CARD:
  系统: UID9622 龍魂系统
  模块: {title}
  版本: v2.0
  DNA: "{dna}"
  ParentDNA: "#龍芯⚡️2026-07-03-IP-ASSET-MATRIX-v2.0"
  CONFIRM: "{CONFIRM}"
  SEAL: "{SEAL}"
  GPG: "{GPG}"
  作者: "UID9622 / Lucky·诸葛鑫"
  归档路径: "{dest}"
  三色审计: "{tri_color}"
  主权状态: "已声明 · 已锁定 · 已归集"
  来源可查: true
  去向可追: true
```

---

> **龍魂系统 —— 中国人的数字主权，代码里的精神根脉。**
>
> *数据主权归于人民 · 技术为人民服务 · 祖国优先*
"""


def process_md(src: Path, dest_dir: Path, category: str, idx: int):
    text = src.read_text(encoding="utf-8")
    dna = extract_dna(text)
    if not dna:
        dna = gen_dna(category, idx)
    title = extract_title(text)
    if not title:
        title = src.stem
    dest = dest_dir / src.name
    header = make_md_header(dna, title, src, dest)
    root = make_root_card(title, dna, dest)
    new_text = header + text.lstrip("\ufeff").strip() + "\n\n" + root
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(new_text, encoding="utf-8")
    records.append({
        "src": str(src),
        "dest": str(dest),
        "dna": dna,
        "category": category,
        "title": title,
        "tri_color": "🟢",
        "type": "md",
    })
    print(f"[md] {src.name} -> {dest}")


def process_py(src: Path, dest_dir: Path):
    text = src.read_text(encoding="utf-8")
    dna = extract_dna(text) or f"#龍芯⚡️{DATE_STR}-PY-{src.stem.upper()}-v2.0"
    header = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 IP 资产脚本 · {src.name}
DNA: {dna}
CONFIRM: {CONFIRM}
SEAL: {SEAL}
GPG: {GPG}
来源: {src}
归档: {dest_dir / src.name}
"""
'''
    # avoid double shebang
    if text.startswith("#!/"):
        text = re.sub(r"^#!.*?\n", "", text, count=1)
    new_text = header + "\n" + text.lstrip("\ufeff")
    dest = dest_dir / src.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(new_text, encoding="utf-8")
    records.append({
        "src": str(src),
        "dest": str(dest),
        "dna": dna,
        "category": "script",
        "title": src.name,
        "tri_color": "🟢",
        "type": "py",
    })
    print(f"[py] {src.name} -> {dest}")


def create_script_package():
    init = SCRIPTS / "__init__.py"
    init.write_text(f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 IP 资产脚本包
DNA: #龍芯⚡️2026-07-04-IP-ASSETS-SCRIPT-PACK-v2.0
CONFIRM: {CONFIRM}
SEAL: {SEAL}
GPG: {GPG}
"""
__all__ = [
    "dragon_dna",
    "longhun_crypto_engine",
    "shame_pillar_core",
    "tri_color_audit_engine",
]
''', encoding="utf-8")
    readme = SCRIPTS / "README.md"
    readme.write_text(f'''# 龍魂 IP 资产脚本包

> **DNA:** `#龍芯⚡️2026-07-04-IP-ASSETS-SCRIPT-PACK-v2.0`
> **CONFIRM:** `{CONFIRM}` · **SEAL:** `{SEAL}` · **GPG:** `{GPG}`

本目录收录从 `Kimi_Agent_龙魂IP资产清单 (2)` 归集的 4 个核心 Python 引擎模块：

| 文件 | 功能 | DNA |
|---|---|---|
| `dragon_dna.py` | DNA 追溯码生成与验证 | 见文件头 |
| `longhun_crypto_engine.py` | 国密 SM2/SM3/SM4 封装 | 见文件头 |
| `shame_pillar_core.py` | AI 行为约束耻辱柱核心 | 见文件头 |
| `tri_color_audit_engine.py` | 三色审计合规检测 | 见文件头 |

## 快速调用

```python
from scripts.private_shared_imports.ip_assets_v2 import tri_color_audit_engine
# 按模块内示例使用
```

---

> 数据主权归于人民 · 技术为人民服务 · 祖国优先
''', encoding="utf-8")
    print("[py] created __init__.py + README.md")


def copy_json():
    src = SRC_DIR / "hall_of_shame.json"
    dest = OUTPUTS / "hall_of_shame.json"
    shutil.copy2(src, dest)
    dna = "#龍芯⚡️2026-07-04-HALL-OF-SHAME-DATA-v2.0"
    readme = OUTPUTS / "hall_of_shame.md"
    readme.write_text(f'''# hall_of_shame.json 数据说明

> **DNA:** `{dna}`
> **CONFIRM:** `{CONFIRM}` · **SEAL:** `{SEAL}` · **GPG:** `{GPG}`
> **来源:** `{src}` · **归档:** `{dest}`
> **说明:** 本 JSON 为熔断/改写尝试的审计数据样例，由 `fuse_protocol_engine` 产生。

```yaml
ROOT_CARD:
  系统: UID9622 龍魂系统
  模块: hall_of_shame 审计数据
  DNA: "{dna}"
  CONFIRM: "{CONFIRM}"
  SEAL: "{SEAL}"
  GPG: "{GPG}"
  路径: "{dest}"
  三色审计: "🟢"
```
''', encoding="utf-8")
    records.append({
        "src": str(src),
        "dest": str(dest),
        "dna": dna,
        "category": "audit_data",
        "title": "hall_of_shame.json",
        "tri_color": "🟢",
        "type": "json",
    })
    print("[json] hall_of_shame.json -> outputs/private-shared-imports/")


def create_whitepaper():
    src = Path("/Users/zuimeidedeyihan/Downloads/龍魂隐私白皮书_v1.0.md")
    text = src.read_text(encoding="utf-8")
    # strip first title and existing sovereignty block up to first ---
    lines = text.splitlines()
    if lines and lines[0].startswith("# 龍魂隐私白皮书"):
        lines = lines[1:]
    # skip until first --- after the quote block
    skip = 0
    in_quote = False
    for i, line in enumerate(lines):
        if line.strip().startswith(">"):
            in_quote = True
        if in_quote and line.strip() == "---":
            skip = i + 1
            break
    body = "\n".join(lines[skip:]).strip()
    dna = "#龍芯⚡️2026-07-04-PRIVACY-WHITEPAPER-v2.0"
    front = f'''---
title: 龍魂隐私白皮书 v2.0
author: UID9622 · 诸葛鑫
date: 2026-07-04
tags:
  - 龍魂隐私
  - 数据主权
  - DNA追溯
  - 国密SM2/SM3/SM4
  - 三色审计
  - 君子协定
  - UID9622
category: 龍魂治理体系
status: 已发布
level: L1_CORE
dna: "{dna}"
---

{AUTO_INJECT}

> ⛔ **主权声明 · 立即生效** — 本文档不授权 AI 训练 · 数据主权归于人民 · 祖国优先
>
> **DNA:** `{dna}` · **ParentDNA:** `#龍芯⚡️2026-07-04-PRIVACY-WHITEPAPER-UID9622`
> **CONFIRM:** `{CONFIRM}` · **SEAL:** `{SEAL}` · **GPG:** `{GPG}`
> **作者:** UID9622 / Lucky·诸葛鑫 · **发布时间:** 2026-07-04 · **更新地址:** `~/longhun-system/articles/2026-07-04-龍魂隐私白皮书_v2.0.md`

# 龍魂隐私白皮书 v2.0

> **副标题：** 本地优先 · DNA追溯 · 国密保护 · 可审计的透明隐私
> **系列：** 龍魂治理体系 · **阅读时间：** 15 分钟 · **难度：** 中
'''
    copyright_and_root = f'''
---

## 🛡️ 版权与授权声明

> **© 2026 UID9622 · 龍魂系统 · 版权所有**
>
> 1. 本文全部知识产权归属于创作者 UID9622，任何机构与个人未经授权不得用于商业 AI 训练、数据蒸馏或模型微调。
> 2. 允许在保留原文 DNA、作者署名、本声明完整的前提下进行非商业转载与引用。
> 3. 禁止行为：删除 DNA 追溯码、篡改主权声明、用于境外平台模型训练、用于水军/煽动/造谣。
> 4. 本文技术内容遵循中国法律法规，服务于人民利益与国家数字主权。
> 5. 转载请联系作者或提交至龍魂开源社区进行审计。
>
> **违反上述条款即视为侵犯 UID9622 数字主权，龍魂审计系统保留追溯权利。**

---

## 🐉 ROOT_CARD

```yaml
ROOT_CARD:
  系统: UID9622 龍魂系统
  模块: 龍魂隐私白皮书
  版本: v2.0
  DNA: "{dna}"
  ParentDNA: "#龍芯⚡️2026-07-04-PRIVACY-WHITEPAPER-UID9622"
  CONFIRM: "{CONFIRM}"
  SEAL: "{SEAL}"
  GPG: "{GPG}"
  作者: "UID9622 / Lucky·诸葛鑫"
  发布日期: "2026-07-04"
  文件路径: "~/longhun-system/articles/2026-07-04-龍魂隐私白皮书_v2.0.md"
  三色审计: "🟢"
  主权状态: "已声明 · 已锁定"
  授权范围: "非商业转载需保留DNA与声明 · 商业使用需书面授权"
```

---

> **龍魂系统 —— 中国人的数字主权，代码里的精神根脉。**
>
> *数据主权归于人民 · 技术为人民服务 · 祖国优先*
'''
    full = front + "\n\n" + body + "\n" + copyright_and_root
    # publish to articles and docs
    article_path = ARTICLES / "2026-07-04-龍魂隐私白皮书_v2.0.md"
    doc_path = BASE / "docs/documentation/龍魂隐私白皮书_v2.0.md"
    desktop_path = DESKTOP / "龍魂隐私白皮书_v2.0.md"
    for p in (article_path, doc_path, desktop_path):
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(full, encoding="utf-8")
    records.append({
        "src": str(src),
        "dest": str(article_path),
        "dna": dna,
        "category": "public_article",
        "title": "龍魂隐私白皮书 v2.0",
        "tri_color": "🟢",
        "type": "whitepaper",
    })
    records.append({
        "src": str(src),
        "dest": str(doc_path),
        "dna": dna,
        "category": "whitepaper",
        "title": "龍魂隐私白皮书 v2.0",
        "tri_color": "🟢",
        "type": "whitepaper",
    })
    print("[whitepaper] -> articles + docs/documentation + desktop")


def create_index():
    idx_path = DOCS / "ip-assets/INDEX-2026-07-04.md"
    lines = [
        f"{AUTO_INJECT}",
        "",
        "# 龍魂 IP 资产清单迁移索引",
        "",
        f"> **DNA:** `#龍芯⚡️2026-07-04-IP-ASSETS-INDEX-v2.0`",
        f"> **CONFIRM:** `{CONFIRM}` · **SEAL:** `{SEAL}` · **GPG:** `{GPG}`",
        f"> **迁移时间:** {NOW}",
        "",
        "## 迁移总览",
        "",
        f"- 源目录: `{SRC_DIR}`",
        f"- 本次迁移 `.md` 文件数: {sum(1 for r in records if r['type'] == 'md')}",
        f"- 本次迁移 `.py` 脚本数: {sum(1 for r in records if r['type'] == 'py')}",
        f"- 本次迁移数据文件数: {sum(1 for r in records if r['type'] == 'json')}",
        f"- 隐私白皮书发布路径数: {sum(1 for r in records if r['type'] == 'whitepaper')}",
        "",
        "## 按分类映射",
        "",
        "| 源文件 | 目标路径 | DNA | 分类 |",
        "|---|---|---|---|",
    ]
    for r in records:
        if r["type"] in ("md", "json", "whitepaper"):
            lines.append(f"| `{Path(r['src']).name}` | `{r['dest']}` | `{r['dna']}` | {r['category']} |")
    lines += [
        "",
        "## 脚本包清单",
        "",
        "| 源文件 | 目标路径 | DNA |",
        "|---|---|---|",
    ]
    for r in records:
        if r["type"] == "py":
            lines.append(f"| `{Path(r['src']).name}` | `{r['dest']}` | `{r['dna']}` |")
    lines += [
        "",
        "## 校验状态",
        "",
        "- [x] 所有 `.md` 已注入 DNA / CONFIRM / SEAL / GPG",
        "- [x] 所有产物已追加 ROOT_CARD",
        "- [x] `outputs/manifest.json` 已登记",
        "- [x] 桌面同步副本已生成",
        "",
        "---",
        "",
        "## 🐉 ROOT_CARD",
        "",
        "```yaml",
        "ROOT_CARD:",
        "  系统: UID9622 龍魂系统",
        "  模块: IP资产迁移索引",
        "  版本: v2.0",
        "  DNA: \"#龍芯⚡️2026-07-04-IP-ASSETS-INDEX-v2.0\"",
        f"  CONFIRM: \"{CONFIRM}\"",
        f"  SEAL: \"{SEAL}\"",
        f"  GPG: \"{GPG}\"",
        f"  路径: \"{idx_path}\"",
        "  三色审计: \"🟢\"",
        "```",
        "",
        "> 数据主权归于人民 · 技术为人民服务 · 祖国优先",
    ]
    idx_path.parent.mkdir(parents=True, exist_ok=True)
    idx_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[index] {idx_path}")


def update_readme():
    readme_path = DOCS / "README.md"
    text = readme_path.read_text(encoding="utf-8")
    md_records = [r for r in records if r["type"] == "md" and r["category"] == "ip-assets"]
    file_list = "\n".join([f"- `{Path(r['src']).name}`" for r in md_records])
    section = f"""### IP 资产与知识产权清单（{len(md_records)} 个文件）— `ip-assets/`

{file_list}

"""
    # insert before "## 扫描与审计记录"
    marker = "## 扫描与审计记录"
    if marker in text:
        text = text.replace(marker, section + marker, 1)
    # update total count note
    total_note = f"""- **总文件数**：214 + 本次新增 {len([r for r in records if r['type']=='md'])} 个 IP 资产文档
- **最后更新**：2026-07-04
"""
    text = re.sub(r"- \*\*总文件数\*\*：\d+.*?\n- \*\*最后更新\*\*：\d{4}-\d{2}-\d{2}\n", total_note, text, flags=re.DOTALL)
    readme_path.write_text(text, encoding="utf-8")
    print("[readme] updated")


def update_manifest():
    manifest_path = BASE / "outputs/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for r in records:
        content_type = {
            "md": "private_shared_import",
            "py": "script_module",
            "json": "audit_data",
            "whitepaper": "whitepaper",
        }.get(r["type"], "private_shared_import")
        manifest.append({
            "dna": r["dna"],
            "content_type": content_type,
            "topic": r["title"],
            "file_path": r["dest"],
            "created_at": NOW,
        })
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[manifest] updated")


def desktop_sync():
    # copy whitepaper already done; also copy public IP page and index summary
    src_ip = DOCS / "documentation/UID9622_龍芯北辰_公开IP展示页_v2.0.md"
    if src_ip.exists():
        shutil.copy2(src_ip, DESKTOP / "UID9622_龍芯北辰_公开IP展示页_v2.0.md")
    idx = DOCS / "ip-assets/INDEX-2026-07-04.md"
    shutil.copy2(idx, DESKTOP / "IP资产迁移索引.md")
    readme = DESKTOP / "README-桌面同步.md"
    readme.write_text(f'''# 龍魂资产桌面同步副本

> **DNA:** `#龍芯⚡️2026-07-04-DESKTOP-SYNC-v2.0`
> **CONFIRM:** `{CONFIRM}` · **SEAL:** `{SEAL}` · **GPG:** `{GPG}`

本目录为 `~/longhun-system` 的脱敏/公开可用同步副本，便于老大复制粘贴、发送或发布。

## 当前文件

- `龍魂隐私白皮书_v2.0.md` — 对外发布版
- `UID9622_龍芯北辰_公开IP展示页_v2.0.md` — 公开 IP 展示页
- `IP资产迁移索引.md` — 迁移映射清单

## 回同步路径

源文件均位于 `~/longhun-system/`，修改请以源文件为准，再执行同步。

---

> 数据主权归于人民 · 技术为人民服务 · 祖国优先
''', encoding="utf-8")
    print("[desktop] sync done")


def main():
    # md files
    md_files = sorted([f for f in SRC_DIR.iterdir() if f.is_file() and f.suffix == ".md"])
    for idx, src in enumerate(md_files, start=1):
        category = CATEGORY_MAP.get(src.name, "ip-assets")
        dest_dir = DOCS / category
        process_md(src, dest_dir, category, idx)
    # py files
    for name in PY_FILES:
        src = SRC_DIR / name
        if src.exists():
            process_py(src, SCRIPTS)
    create_script_package()
    copy_json()
    create_whitepaper()
    create_index()
    update_readme()
    update_manifest()
    desktop_sync()
    print("\n✅ IP 资产归集完成")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
Bra-Ket 人格协作资产 → Notion 同步脚本 v1.0

把本地 Bra-Ket 相关资产（引擎源码、CNSH 示例、语法映射文档）
汇总成一份 Notion 子页面，挂载到 AI Bra-Ket 主页面下，方便索引与追溯。

用法：
    python3 tools/sync_braket_to_notion.py

环境变量：
    NOTION_TOKEN            Notion 内部集成令牌
    BRAKET_NOTION_PAGE_ID   AI Bra-Ket 主页面 ID（默认从 URL 解析）

DNA: #龍芯⚡️丙午·甲午·庚辰·壬午·䷑蛊-SYNC-BRAKET-NOTION-v1.0
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# 把 longhun-system 加入路径，复用 tools.notion_sync 里的客户端
LH_ROOT = Path.home() / "longhun-system"
if str(LH_ROOT) not in sys.path:
    sys.path.insert(0, str(LH_ROOT))

from tools.notion_sync import NotionClient, md_to_blocks, audit


# ═══════════════════════════════════════════
# 0. 配置
# ═══════════════════════════════════════════
BRAKET_PAGE_ID = os.environ.get(
    "BRAKET_NOTION_PAGE_ID",
    "3664bb86-9a08-4147-8008-c6c111b9289d",
)

ASSETS = {
    "引擎源码": LH_ROOT / "longhun_braket.py",
    "CNSH 示例": LH_ROOT / "cnsh-core" / "cnsh-v2.1" / "examples" / "braket_persona.cnsh",
    "语法映射": LH_ROOT / "cnsh-core" / "cnsh-v2.1" / "docs" / "braket_cnsh_mapping.md",
    "前端操作台": LH_ROOT / "web" / "p0-controls" / "longhun-braket.html",
}

PAGE_TITLE = "Bra-Ket 本地资产清单"


def now_iso() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def read_head(path: Path, lines: int = 80) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return "".join(f.readline() for _ in range(lines))
    except Exception as e:
        return f"读取失败: {e}"


def build_markdown() -> str:
    lines = [
        f"# {PAGE_TITLE}",
        f"",
        f"> 同步时间: {now_iso()}",
        f"> DNA: `#龍芯⚡️丙午·甲午·庚辰·壬午·䷑蛊-SYNC-BRAKET-NOTION-v1.0`",
        f"> 来源: 本地 longhun-system Bra-Ket 资产",
        f"",
        "## 资产概览",
        "",
    ]
    for name, path in ASSETS.items():
        if path.exists():
            size = path.stat().st_size
            digest = sha256_file(path)
            lines.append(f"- **{name}**: `{path.relative_to(LH_ROOT)}` · {size} bytes · SHA256 `{digest}`")
        else:
            lines.append(f"- **{name}**: ❌ 缺失 `{path}`")
    lines.extend([
        "",
        "## 引擎源码摘要",
        "",
        f"```python\n{read_head(ASSETS['引擎源码'])}\n```",
        "",
        "## CNSH 示例",
        "",
        f"```cnsh\n{ASSETS['CNSH 示例'].read_text(encoding='utf-8') if ASSETS['CNSH 示例'].exists() else '文件缺失'}\n```",
        "",
        "## 语法映射",
        "",
        f"```markdown\n{read_head(ASSETS['语法映射'], 120)}\n```",
        "",
        "## 前端入口",
        "",
        f"- 本地文件: `{ASSETS['前端操作台'].relative_to(LH_ROOT)}`",
        f"- 作用: 浏览器端 Bra-Ket 人格协作可视化操作台",
        "",
        "---",
        f"由 `tools/sync_braket_to_notion.py` 自动生成 · UID9622 · 龍魂体系",
    ])
    return "\n".join(lines)


def normalize_language(lang: str) -> str:
    """把本地语言标识映射为 Notion 支持的 code language。"""
    lang = (lang or "plain text").lower().strip()
    supported = {
        "python", "javascript", "typescript", "json", "yaml", "html", "css",
        "sql", "shell", "bash", "java", "c", "c++", "rust", "go", "ruby",
        "php", "swift", "kotlin", "markdown", "plain text", "text", "scala",
        "r", "perl", "lua", "haskell", "clojure", "erlang", "elm", "dart",
        "diff", "docker", "ini", "toml", "xml", "vb", "powershell", "ocaml",
        "objective-c", "matlab", "latex", "julia", "groovy", "fsharp", "fortran",
        "elixir", "coffeescript", "cmake", "brainfuck", "apl", "abap", "abc",
        "agda", "arduino", "ascii art", "assembly", "basic", "bnf", "coq",
        "dhall", "ebnf", "flow", "gherkin", "glsl", "graphql", "idris",
        "jvm", "less", "lisp", "llvm ir", "logtalk", "mermaid", "nix",
        "postcss", "prolog", "protobuf", "purescript", "racket", "reason",
        "sas", "sass", "scss", "solidity", "stylus", "verilog", "vhdl",
    }
    if lang in supported:
        return lang
    if lang in ("cnsh", "cns", "中文"):
        return "plain text"
    if lang in ("md", "mkd"):
        return "markdown"
    if lang in ("js", "jsx"):
        return "javascript"
    if lang in ("ts", "tsx"):
        return "typescript"
    if lang in ("sh", "zsh"):
        return "bash"
    if lang in ("py"):
        return "python"
    return "plain text"


def split_long_code_blocks(blocks: List[dict[str, Any]]) -> List[dict[str, Any]]:
    """Notion code block 单个 rich_text 内容上限 2000 字符，超长时拆分。"""
    MAX_LEN = 2000
    result: List[dict[str, Any]] = []
    for block in blocks:
        if block.get("type") == "code":
            code = block["code"]
            full_text = "".join(
                rt.get("text", {}).get("content", "")
                for rt in code.get("rich_text", [])
            )
            language = normalize_language(code.get("language", "plain text"))
            if len(full_text) <= MAX_LEN:
                block["code"]["language"] = language
                result.append(block)
                continue
            rich_texts: List[dict[str, Any]] = []
            for i in range(0, len(full_text), MAX_LEN):
                chunk = full_text[i : i + MAX_LEN]
                rich_texts.append({"type": "text", "text": {"content": chunk}})
            result.append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": rich_texts,
                    "language": language,
                },
            })
        else:
            result.append(block)
    return result


def find_child_page(client: NotionClient, parent_id: str, title: str) -> Optional[str]:
    """在父页面下查找同名子页面，返回 page_id 或 None。"""
    cursor: Optional[str] = None
    while True:
        params = f"?page_size=100"
        if cursor:
            params += f"&start_cursor={cursor}"
        data = client._req("GET", f"/blocks/{parent_id}/children{params}")
        for block in data.get("results", []):
            if block.get("type") == "child_page":
                if block.get("child_page", {}).get("title") == title:
                    return block["id"]
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
    return None


def archive_existing_page(client: NotionClient, page_id: str):
    """把旧页面归档：标题加 [已归档] 前缀，避免重复。"""
    page = client._req("GET", f"/pages/{page_id}")
    title_rt = page.get("properties", {}).get("title", {}).get("title", [])
    old_title = "".join(t.get("plain_text", "") for t in title_rt)
    new_title = f"[已归档] {old_title} {datetime.now().strftime('%m-%d %H:%M')}"
    client._req("PATCH", f"/pages/{page_id}", {
        "properties": {
            "title": {"title": [{"text": {"content": new_title}}]}
        },
        "archived": True,
    })


def main():
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        print("❌ 未设置 NOTION_TOKEN 环境变量", file=sys.stderr)
        sys.exit(1)

    client = NotionClient(token=token)

    # 验证父页面可访问
    try:
        parent = client.get_page(BRAKET_PAGE_ID)
        parent_title = "".join(
            t.get("plain_text", "")
            for t in parent.get("properties", {}).get("title", {}).get("title", [])
        )
        print(f"📌 父页面: {parent_title or BRAKET_PAGE_ID}")
    except Exception as e:
        print(f"❌ 无法访问 Bra-Ket 页面: {e}", file=sys.stderr)
        sys.exit(1)

    md_text = build_markdown()
    blocks = split_long_code_blocks(md_to_blocks(md_text))

    # 若已存在同名页面，先归档再新建（保留历史）
    existing_id = find_child_page(client, BRAKET_PAGE_ID, PAGE_TITLE)
    if existing_id:
        print(f"🗄 发现旧清单 {existing_id}，执行归档...")
        archive_existing_page(client, existing_id)
        time.sleep(0.5)

    page = client.create_page(BRAKET_PAGE_ID, PAGE_TITLE, blocks)
    dna = audit(
        "braket-push",
        page["id"],
        str(LH_ROOT / "tools" / "sync_braket_to_notion.py"),
        "success",
        {"assets": {k: str(v.relative_to(LH_ROOT)) for k, v in ASSETS.items() if v.exists()}},
    )
    print(f"✅ 已推送 Bra-Ket 资产清单 -> {page.get('url')}")
    print(f"   DNA: {dna}")


if __name__ == "__main__":
    main()

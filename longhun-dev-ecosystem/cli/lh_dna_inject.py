#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂生态 · DNA注入CLI工具
DNA: #龍芯⚡️丙午·丙申·庚申·亥时-DEV-INJECT-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

用法:
    # 批量递归注入
    python3 cli/lh_dna_inject.py --path ./my-repo/ --developer-dna "#龍芯⚡️..." --recursive
    # 单文件注入
    python3 cli/lh_dna_inject.py --file ./main.py --developer-dna "#龍芯⚡️..."
    # 指定线上服务
    LONGHUN_API_URL="https://uid9622.cn/developer" python3 cli/lh_dna_inject.py --file ./main.py --developer-dna "..."
"""

import os
import sys
import argparse
import requests
from pathlib import Path
from datetime import datetime

API_URL = os.getenv("LONGHUN_API_URL", "http://localhost:8000")

CODE_EXTS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".htm", ".css", ".scss",
    ".md", ".txt", ".json", ".yaml", ".yml", ".sh", ".bash", ".go", ".rs",
    ".c", ".cpp", ".h", ".hpp", ".java", ".kt", ".swift", ".php", ".rb",
}

# 语言 → 文件头注释样式
HEADER_TEMPLATES = {
    "hash": "# 🐉 DNA: {dna}\n# 开发者: {developer_dna}\n# 生成时间: {ts}\n\n",            # py/js/ts/go/rs/c/cpp/sh
    "html": "<!-- 🐉 DNA: {dna} -->\n<!-- 开发者: {developer_dna} -->\n\n",                  # html/htm
    "md": "> **DNA:** `{dna}`  \n> **开发者:** `{developer_dna}`  \n\n",                      # md/txt
    "css": "/* 🐉 DNA: {dna} */\n/* 开发者: {developer_dna} */\n\n",                          # css
    "json": "// 🐉 DNA: {dna} | 开发者: {developer_dna}\n",                                   # json（宽松）
}


def header_style(ext: str) -> str:
    if ext in (".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".c", ".cpp", ".h", ".hpp", ".sh", ".bash", ".java", ".kt", ".swift", ".php", ".rb"):
        return "hash"
    if ext in (".html", ".htm"):
        return "html"
    if ext in (".md", ".txt"):
        return "md"
    if ext in (".css", ".scss"):
        return "css"
    if ext == ".json":
        return "json"
    return "hash"


def inject_dna_to_file(file_path: Path, developer_dna: str, api_url: str = API_URL):
    """为单个文件注入DNA（调服务登记 + 本地写头）"""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        print(f"⚠️ 跳过无法读取的文件: {file_path}")
        return False

    # 已含 DNA → 跳过（幂等，返回 None 表示非失败）
    if "#龍芯⚡️" in content[:300]:
        print(f"⏭️ 已存在DNA，跳过: {file_path}")
        return None

    # 调 API 登记
    try:
        resp = requests.post(
            f"{api_url}/api/code/inject",
            json={
                "file_path": str(file_path),
                "content": content,
                "developer_dna": developer_dna,
                "language": file_path.suffix.lstrip(".") or "txt",
            },
            timeout=30,
        )
    except requests.RequestException as e:
        print(f"❌ 无法连接服务 {api_url}: {e}")
        return False

    if resp.status_code == 200:
        data = resp.json()
        dna = data.get("dna")
        ext = file_path.suffix.lower()
        ts = datetime.now().isoformat()
        header = HEADER_TEMPLATES[header_style(ext)].format(
            dna=dna, developer_dna=developer_dna, ts=ts
        )
        file_path.write_text(header + content, encoding="utf-8")
        print(f"✅ 已注入: {file_path} → {dna}")
        return True
    else:
        detail = ""
        try:
            detail = resp.json().get("detail", resp.text)
        except Exception:
            detail = resp.text
        print(f"❌ 注入失败: {file_path} - {detail}")
        return False


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂DNA注入CLI工具")
    parser.add_argument("--path", help="目录或文件路径")
    parser.add_argument("--file", help="单个文件路径")
    parser.add_argument("--developer-dna", required=True, help="开发者DNA")
    parser.add_argument("--recursive", "-r", action="store_true", help="递归扫描目录")
    parser.add_argument("--api", default=API_URL, help="API地址（默认 localhost:8000）")
    args = parser.parse_args()

    if not args.path and not args.file:
        print("❌ 请指定 --path 或 --file")
        sys.exit(1)

    target_files = []
    if args.file:
        target_files = [Path(args.file)]
    elif args.path:
        p = Path(args.path)
        if p.is_file():
            target_files = [p]
        elif p.is_dir():
            if args.recursive:
                target_files = list(p.rglob("*"))
            else:
                target_files = list(p.glob("*"))

    # 过滤代码文件 + 跳过隐藏与仓库目录
    target_files = [
        f for f in target_files
        if f.is_file()
        and f.suffix.lower() in CODE_EXTS
        and not any(part.startswith(".") for part in f.parts)
        and "node_modules" not in f.parts
        and "__pycache__" not in f.parts
    ]

    print("🐉 龍魂DNA注入工具")
    print(f"开发者DNA: {args.developer_dna}")
    print(f"服务地址:  {args.api}")
    print(f"扫描文件:  {len(target_files)} 个")

    success = 0
    failed = 0
    for f in target_files:
        result = inject_dna_to_file(f, args.developer_dna, args.api)
        if result is True:
            success += 1
        elif result is False:
            failed += 1
        # None = 已存在DNA跳过，不算失败

    print(f"\n✅ 完成: {success} 个文件已注入DNA" + (f" · {failed} 个失败" if failed else ""))
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

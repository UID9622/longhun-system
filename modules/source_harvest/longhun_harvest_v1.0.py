#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·开源吞噬流水线 v1.0
模块一：GitHub 合规收割器

DNA: #龍芯⚡️2026-05-28-LONGHUN-AST-HARVEST-v1.0
作者: UID9622 · 龍芯北辰

用途: 通过 GitHub API 搜索并下载 MIT/Apache-2.0/BSD 协议仓库
     过滤 GPL/AGPL 等传染性协议，只吃干净的肉

使用:
    python3 longhun_harvest.py --query "nlp" --lang python --max 10
    python3 longhun_harvest.py --query "http client" --lang python --token YOUR_TOKEN

注意:
    - 使用 GitHub API（非暴力爬取），遵守 ToS
    - 无 token: 60次/小时  有 token: 5000次/小时
    - 下载的代码归原作者所有，MIT/Apache/BSD 许可你修改
"""

import os
import sys
import json
import time
import shutil
import hashlib
import urllib.request
import urllib.parse
import argparse
import zipfile
import io
from datetime import datetime
from pathlib import Path


# ─── 协议白名单 / 黑名单 ──────────────────────────────────

# 允许: 宽容型协议（可改可卖可闭源，保留署名即可）
ALLOWED_LICENSES = {
    "mit",
    "apache-2.0",
    "bsd-2-clause",
    "bsd-3-clause",
    "isc",
    "unlicense",
    "cc0-1.0",
    "0bsd",
}

# 禁止: 传染性协议（改了要开源，不惹麻烦）
BLOCKED_LICENSES = {
    "gpl-2.0", "gpl-3.0",
    "agpl-3.0", "agpl-v3",
    "lgpl-2.0", "lgpl-2.1", "lgpl-3.0",
    "eupl-1.1", "eupl-1.2",
    "mpl-2.0",   # Mozilla - 文件级弱传染
    "osl-3.0",
    "ccdl-1.0",
}


# ─── GitHub API 客户端 ────────────────────────────────────

class GitHubHarvester:
    """GitHub 合规收割器"""

    BASE_URL = "https://api.github.com"
    SEARCH_URL = f"{BASE_URL}/search/repositories"

    def __init__(self, token: str = None, output_dir: str = "longhun_harvest"):
        self.token = token
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.log_path = self.output_dir / "harvest_log.jsonl"
        self.dna = f"#龍芯⚡️{datetime.utcnow().strftime('%Y-%m-%d')}-HARVEST"

    def _headers(self) -> dict:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "LongHun-Harvester/1.0 (UID9622; longhun2025@petalmail.com)",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _get(self, url: str, params: dict = None) -> dict:
        """执行 GET 请求，尊重速率限制"""
        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"

        req = urllib.request.Request(url, headers=self._headers())
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                # 检查速率限制
                remaining = resp.headers.get("X-RateLimit-Remaining", "?")
                reset_ts  = resp.headers.get("X-RateLimit-Reset", "0")
                print(f"    [API] 剩余额度: {remaining}次  重置时间: {reset_ts}")

                if int(remaining or 1) <= 2:
                    wait = max(0, int(reset_ts) - int(time.time())) + 5
                    print(f"    [限流] 接近上限，等待 {wait}s ...")
                    time.sleep(wait)

                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            print(f"    [HTTP错误] {e.code}: {body[:200]}")
            if e.code == 403:
                print("    → 可能触发速率限制，等 60s 后重试")
                time.sleep(60)
            return {}

    def search(self, query: str, language: str = "python",
               max_results: int = 20) -> list:
        """
        搜索 GitHub 仓库
        返回符合白名单协议的仓库列表
        """
        print(f"\n🔍 搜索: '{query}' | 语言: {language} | 目标: {max_results} 个")
        print(f"   协议白名单: {', '.join(sorted(ALLOWED_LICENSES))}")

        # GitHub 搜索 query 格式
        # license:mit OR license:apache-2.0 ...
        license_filter = " OR ".join(f"license:{lic}" for lic in ALLOWED_LICENSES)
        full_query = f"{query} language:{language} {license_filter}"

        results = []
        page = 1
        per_page = min(30, max_results)

        while len(results) < max_results:
            data = self._get(self.SEARCH_URL, {
                "q": full_query,
                "sort": "stars",
                "order": "desc",
                "per_page": per_page,
                "page": page,
            })

            items = data.get("items", [])
            if not items:
                print(f"   第{page}页无结果，结束")
                break

            for item in items:
                license_key = (item.get("license") or {}).get("spdx_id", "").lower()
                name        = item.get("full_name", "unknown")
                stars       = item.get("stargazers_count", 0)
                description = item.get("description", "")[:80]

                # 协议检查
                if license_key in BLOCKED_LICENSES:
                    print(f"   ⛔ 跳过（传染协议 {license_key}）: {name}")
                    continue

                if license_key not in ALLOWED_LICENSES:
                    print(f"   🟡 跳过（协议不明 {license_key or 'none'}）: {name}")
                    continue

                print(f"   🟢 命中: {name}  ⭐{stars}  [{license_key}]  {description}")
                results.append({
                    "name":         name,
                    "full_name":    name,
                    "stars":        stars,
                    "license":      license_key,
                    "clone_url":    item.get("clone_url"),
                    "default_branch": item.get("default_branch", "main"),
                    "description":  description,
                    "html_url":     item.get("html_url"),
                    "topics":       item.get("topics", []),
                    "size_kb":      item.get("size", 0),
                })

                if len(results) >= max_results:
                    break

            page += 1
            time.sleep(1)  # 礼貌性延迟

        print(f"\n✅ 找到 {len(results)} 个合规仓库")
        return results

    def download_zip(self, repo: dict, dest_dir: Path = None) -> Path:
        """
        下载仓库 ZIP（不需要 git，纯 Python）
        返回解压后的路径
        """
        owner, repo_name = repo["full_name"].split("/")
        branch = repo.get("default_branch", "main")

        dest = dest_dir or (self.output_dir / "raw" / repo_name)
        dest.mkdir(parents=True, exist_ok=True)

        zip_url = (f"https://api.github.com/repos/{owner}/{repo_name}"
                   f"/zipball/{branch}")

        print(f"   📦 下载: {repo['full_name']} ({repo['size_kb']}KB)")

        req = urllib.request.Request(zip_url, headers=self._headers())
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
        except Exception as e:
            print(f"   ❌ 下载失败: {e}")
            return None

        # 解压
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                # GitHub ZIP 根目录格式: owner-repo-commit/
                prefix = z.namelist()[0].split("/")[0] + "/"
                for member in z.namelist():
                    if not member.endswith("/"):
                        rel = member[len(prefix):]
                        target = dest / rel
                        target.parent.mkdir(parents=True, exist_ok=True)
                        with z.open(member) as src, open(target, "wb") as tgt:
                            tgt.write(src.read())
        except Exception as e:
            print(f"   ❌ 解压失败: {e}")
            return None

        print(f"   ✅ 已存: {dest}")
        return dest

    def harvest(self, query: str, language: str = "python",
                max_results: int = 10, download: bool = True) -> list:
        """
        完整收割流程：搜索 → 过滤 → 下载 → 记录
        """
        print(f"\n🐉 龍魂开源收割器启动")
        print(f"   DNA: {self.dna}")
        print(f"   输出目录: {self.output_dir}")
        print("=" * 60)

        repos = self.search(query, language, max_results)

        if not repos:
            print("❌ 未找到合规仓库")
            return []

        if download:
            print(f"\n📥 开始下载 {len(repos)} 个仓库 ...")
            for i, repo in enumerate(repos, 1):
                print(f"\n[{i}/{len(repos)}] {repo['full_name']}")
                local_path = self.download_zip(repo)
                repo["local_path"] = str(local_path) if local_path else None
                time.sleep(2)  # 礼貌延迟

        # 记录日志
        with open(self.log_path, "a", encoding="utf-8") as f:
            for repo in repos:
                entry = {
                    "ts": datetime.utcnow().isoformat() + "Z",
                    "dna": self.dna,
                    "repo": repo["full_name"],
                    "license": repo["license"],
                    "stars": repo["stars"],
                    "local_path": repo.get("local_path"),
                    "query": query,
                }
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        print(f"\n✅ 收割完成 · 日志: {self.log_path}")
        return repos


# ─── CLI 入口 ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="龍魂开源收割器 · 只吃 MIT/Apache/BSD 的干净肉"
    )
    parser.add_argument("--query",   default="http client",  help="搜索关键词")
    parser.add_argument("--lang",    default="python",        help="编程语言")
    parser.add_argument("--max",     type=int, default=5,     help="最多收割几个")
    parser.add_argument("--token",   default=None,            help="GitHub Token（可选）")
    parser.add_argument("--no-download", action="store_true", help="只搜索不下载")
    parser.add_argument("--output",  default="longhun_harvest", help="输出目录")
    args = parser.parse_args()

    # 读取 token（优先环境变量）
    token = args.token or os.getenv("GITHUB_TOKEN")
    if not token:
        print("💡 未设置 GITHUB_TOKEN，使用未认证模式（60次/小时）")
        print("   export GITHUB_TOKEN=your_token  可提升到 5000次/小时")

    harvester = GitHubHarvester(token=token, output_dir=args.output)
    repos = harvester.harvest(
        query=args.query,
        language=args.lang,
        max_results=args.max,
        download=not args.no_download,
    )

    # 输出摘要
    print(f"\n{'='*60}")
    print(f"📊 收割摘要:")
    for r in repos:
        status = "✅" if r.get("local_path") else "🟡 (仅信息)"
        print(f"  {status} {r['full_name']}  [{r['license']}]  ⭐{r['stars']}")
    print(f"{'='*60}")
    print(f"DNA: {harvester.dna}")


if __name__ == "__main__":
    main()

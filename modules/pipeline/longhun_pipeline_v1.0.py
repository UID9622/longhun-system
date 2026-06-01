#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·开源吞噬流水线 v1.0
主控脚本：一键完成 搜索→下载→变换→归档

DNA: #龍芯⚡️2026-05-28-LONGHUN-PIPELINE-v1.0
作者: UID9622 · 龍芯北辰

流程:
    1. GitHub搜索 (MIT/Apache/BSD)
    2. 下载 ZIP
    3. AST 变换（英→中）
    4. 注入版权头部
    5. DNA归档

使用:
    python3 longhun_pipeline.py --query "json parser" --max 3
    python3 longhun_pipeline.py --query "http" --lang python --max 5 --token YOUR_TOKEN
    python3 longhun_pipeline.py --transform-only ./longhun_harvest/raw/some_repo
"""

import os
import sys
import json
import shutil
import argparse
import hashlib
from pathlib import Path
from datetime import datetime

# 引入我们的两个模块（同目录）
sys.path.insert(0, str(Path(__file__).parent))

try:
    from longhun_harvest import GitHubHarvester, ALLOWED_LICENSES
    from longhun_ast_transform import (
        transform_project, DEFAULT_VOCAB
    )
    from longhun_signature_tracker import ContributorSignatureTracker
except ImportError as e:
    print(f"❌ 缺少模块: {e}")
    print("   确保 longhun_harvest.py、longhun_ast_transform.py 和 longhun_signature_tracker.py 在同一目录")
    sys.exit(1)


# ─── 协议头部模板 ─────────────────────────────────────────

LICENSE_HEADER_TEMPLATE = """\
龍魂系统 · 开源集成模块
════════════════════════════════════════════════════════════
原始仓库:   {original_repo}
原始协议:   {original_license}
原始来源:   {original_url}

原始版权声明（遵守 {original_license} 协议，完整保留）:
{original_copyright}

════════════════════════════════════════════════════════════
修改说明:
  本模块基于上述开源项目修改，经龍魂·AST变换引擎处理，
  将标识符命名转换为中文风格，逻辑结构100%保留。

修改部分版权:
  Copyright (c) {year} UID9622 · 龍芯北辰 (诸葛鑫)
  DNA: {dna}

声明:
  修改部分及整体集成版权归 UID9622 所有。
  仍遵守原协议 {original_license} 的条款。
════════════════════════════════════════════════════════════
"""


def inject_license_header(project_dir: Path, repo_info: dict):
    """
    在项目根目录生成 LONGHUN_LICENSE.txt
    并在每个 Python 文件开头加上简短版权行
    """
    # 尝试读取原始 LICENSE 文件内容
    orig_copyright = ""
    for license_file in ["LICENSE", "LICENSE.txt", "LICENSE.md", "COPYING"]:
        lf = project_dir / license_file
        if lf.exists():
            orig_copyright = lf.read_text(encoding="utf-8",
                                           errors="replace")[:500]
            break
    if not orig_copyright:
        orig_copyright = f"[原协议为 {repo_info.get('license', 'unknown')}，详见原仓库]"

    dna = (f"#龍芯⚡️{datetime.utcnow().strftime('%Y-%m-%d')}"
           f"-{repo_info.get('name', 'unknown').replace('/', '-').upper()}")

    header_content = LICENSE_HEADER_TEMPLATE.format(
        original_repo=repo_info.get("full_name", "unknown"),
        original_license=repo_info.get("license", "unknown").upper(),
        original_url=repo_info.get("html_url", ""),
        original_copyright=orig_copyright,
        year=datetime.now().year,
        dna=dna,
    )

    # 写入专属说明文件
    header_file = project_dir / "LONGHUN_LICENSE.txt"
    header_file.write_text(header_content, encoding="utf-8")
    print(f"   📄 版权文件: {header_file.name}")
    return dna


def run_pipeline(
    query: str,
    language: str = "python",
    max_repos: int = 5,
    token: str = None,
    output_dir: str = "longhun_output",
    vocab_file: str = None,
    download_only: bool = False,
):
    """
    完整流水线
    """
    output = Path(output_dir)
    raw_dir = output / "01_raw"
    cn_dir  = output / "02_transformed"
    log_dir = output / "03_logs"

    for d in [raw_dir, cn_dir, log_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # 加载词典
    vocab = dict(DEFAULT_VOCAB)
    if vocab_file and Path(vocab_file).exists():
        extra = json.loads(Path(vocab_file).read_text(encoding="utf-8"))
        vocab.update(extra)
        print(f"📖 已加载自定义词典: {len(extra)} 词条")

    print(f"\n🐉 龍魂开源吞噬流水线启动")
    print(f"   查询: {query} | 语言: {language} | 最多: {max_repos} 个")
    print(f"   输出: {output}")
    print("=" * 60)

    # ── 步骤1: 搜索 + 下载 ──
    harvester = GitHubHarvester(token=token, output_dir=str(raw_dir))
    repos = harvester.harvest(
        query=query,
        language=language,
        max_results=max_repos,
        download=True,
    )

    if not repos:
        print("❌ 没有找到合规仓库，流水线结束")
        return

    if download_only:
        print(f"\n📥 仅下载模式，跳过变换")
        print(f"   原始代码: {raw_dir}")
        return

    # ── 步骤2: AST 变换 + 签名追踪 ──
    tracker = ContributorSignatureTracker()
    pipeline_report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "query": query,
        "language": language,
        "repos_processed": [],
    }

    for i, repo in enumerate(repos, 1):
        local_path = repo.get("local_path")
        if not local_path or not Path(local_path).exists():
            print(f"\n[{i}/{len(repos)}] ⚠️ 无本地路径，跳过: {repo['full_name']}")
            continue

        src = Path(local_path)
        dest = cn_dir / src.name
        print(f"\n[{i}/{len(repos)}] 🔄 变换: {repo['full_name']}")
        print(f"   原始: {src}")
        print(f"   输出: {dest}")

        # AST 变换
        summary = transform_project(src, dest, vocab, extensions=(".py",))

        # 注入版权头部
        dna = inject_license_header(dest, repo)

        # 计算内容哈希（用于签名追踪）
        content_parts = [repo["full_name"], repo.get("license", ""), repo.get("description", "")]
        content_hash = hashlib.sha256("".join(content_parts).encode()).hexdigest()[:16].upper()

        # 登记贡献者签名
        author = repo["full_name"].split("/")[0]
        tracker.register_contribution(
            repo_name=repo["full_name"],
            repo_url=repo.get("html_url", ""),
            original_author=author,
            license_type=repo["license"],
            content_hash=content_hash,
            file_path=str(dest),
            lines_count=summary["success"] * 50,  # 近似行数
            modification="AST 中文化变换·逻辑无改"
        )

        repo_report = {
            "repo": repo["full_name"],
            "license": repo["license"],
            "stars": repo["stars"],
            "files_transformed": summary["success"],
            "files_failed": summary["failed"],
            "rename_total": summary["rename_total"],
            "dna": dna,
            "content_hash": content_hash,
            "signature_registered": True,
            "output_dir": str(dest),
        }
        pipeline_report["repos_processed"].append(repo_report)

        print(f"   ✅ {summary['success']} 文件变换成功，{summary['rename_total']} 处替换")

    # ── 步骤3: 写入总报告 ──
    report_path = log_dir / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.write_text(
        json.dumps(pipeline_report, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    # ── 验证签名链完整性 ──
    tracker.verify_immutability()

    # ── 打印总结 ──
    total_files = sum(r["files_transformed"] for r in pipeline_report["repos_processed"])
    total_renames = sum(r["rename_total"] for r in pipeline_report["repos_processed"])

    print(f"\n{'='*60}")
    print(f"🎉 流水线完成！")
    print(f"   处理仓库: {len(pipeline_report['repos_processed'])} 个")
    print(f"   变换文件: {total_files} 个")
    print(f"   命名替换: {total_renames} 处")
    print(f"   原始代码: {raw_dir}")
    print(f"   中文版本: {cn_dir}")
    print(f"   签名日志: {tracker.log_path}")
    print(f"   日志报告: {report_path}")
    final_dna = (f"#龍芯⚡️{datetime.utcnow().strftime('%Y-%m-%d')}"
                 f"-PIPELINE-DONE-{len(repos)}REPOS")
    print(f"   DNA: {final_dna}")
    print(f"{'='*60}")


def run_transform_only(src_path: str, vocab_file: str = None):
    """仅对已下载的目录做变换（不搜索不下载）"""
    src = Path(src_path)
    if not src.exists():
        print(f"❌ 路径不存在: {src}")
        sys.exit(1)

    vocab = dict(DEFAULT_VOCAB)
    if vocab_file and Path(vocab_file).exists():
        extra = json.loads(Path(vocab_file).read_text(encoding="utf-8"))
        vocab.update(extra)

    dest = src.parent / (src.name + "_中文版")
    print(f"\n🔄 单独变换模式")
    print(f"   输入: {src}")
    print(f"   输出: {dest}")

    summary = transform_project(src, dest, vocab)
    print(f"\n✅ 完成: {summary['success']} 文件，{summary['rename_total']} 处替换")


# ─── CLI ─────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="龍魂·开源吞噬完整流水线 · 一键搜索-下载-变换"
    )
    parser.add_argument("--query",    default="http client", help="GitHub 搜索词")
    parser.add_argument("--lang",     default="python",      help="编程语言")
    parser.add_argument("--max",      type=int, default=3,   help="最多几个仓库")
    parser.add_argument("--token",    default=None,          help="GitHub Token")
    parser.add_argument("--output",   default="longhun_output", help="输出目录")
    parser.add_argument("--vocab",    default=None,          help="自定义词典 JSON")
    parser.add_argument("--download-only", action="store_true", help="只下载不变换")
    parser.add_argument("--transform-only", default=None,
                        help="只变换，传入已有代码目录路径")

    args = parser.parse_args()

    token = args.token or os.getenv("GITHUB_TOKEN")

    if args.transform_only:
        run_transform_only(args.transform_only, args.vocab)
    else:
        run_pipeline(
            query=args.query,
            language=args.lang,
            max_repos=args.max,
            token=token,
            output_dir=args.output,
            vocab_file=args.vocab,
            download_only=args.download_only,
        )


if __name__ == "__main__":
    main()

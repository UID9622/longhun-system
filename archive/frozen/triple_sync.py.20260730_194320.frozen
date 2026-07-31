#!/Users/zuimeidedeyihan/longhun-system/.venv_longhun_math/bin/python
# -*- coding: utf-8 -*-
"""
三层同步引擎：本地 → Notion → GitHub
DNA: #龍芯⚡️2026-06-29-LONGHUN-TRIPLE-SYNC-v3-UID9622

阶段 1：扫描 brain/cnsh_cards/*.md 与 audit/reports/*.md，
        用 frontmatter 解析标题/DNA/标签，同步到 Notion LU 公开档案数据库。
阶段 2：每月把本地 Markdown 档案冻结到 ~/.longhun/github-public/monthly/YYYY-MM/，
        生成索引 README，并推送到已配置的 GitHub remote。
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import frontmatter

# 将项目根目录加入路径
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from longhun_notion_dashboard import LongHunNotionDashboard


DNA = "#龍芯⚡️2026-06-29-LONGHUN-TRIPLE-SYNC-v3-UID9622"
HOME = Path.home()
GITHUB_ROOT = HOME / ".longhun" / "github-public"


def _now_iso() -> str:
    return datetime.now().isoformat()


def _current_month() -> str:
    return datetime.now().strftime("%Y-%m")


def _解析_markdown(路径: Path) -> Dict[str, Any]:
    """解析 Markdown 文件，优先 frontmatter，其次取第一个 # 标题。"""
    文本 = 路径.read_text(encoding="utf-8", errors="ignore")
    try:
        post = frontmatter.loads(文本)
    except Exception:
        post = frontmatter.Post(文本)

    标题 = post.get("title", "")
    if not 标题:
        # 找第一个 # 标题，剔除代码块避免误匹配
        无代码 = 文本
        while "```" in 无代码:
            开头, _, 剩余 = 无代码.partition("```")
            _, _, 无代码 = 剩余.partition("```")
            无代码 = 开头 + 无代码
        for 行 in 无代码.splitlines():
            if 行.strip().startswith("# "):
                标题 = 行.strip()[2:].strip()
                break
    if not 标题:
        标题 = 路径.stem

    标签 = post.get("tags", [])
    if isinstance(标签, str):
        标签 = [t.strip() for t in 标签.split(",")]

    dna = post.get("dna", "")
    if not dna:
        dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-TRIPLE-SYNC-{路径.stem}-UID9622"

    return {
        "path": str(路径.relative_to(PROJECT_ROOT)),
        "abs_path": str(路径),
        "title": 标题,
        "dna": dna,
        "tags": 标签,
        "source": "CNSH卡片" if "cnsh_cards" in str(路径) else "审计报告",
        "content": post.content,
    }


def _扫描本地档案() -> Iterable[Dict[str, Any]]:
    """扫描卡片和报告目录。"""
    卡片目录 = PROJECT_ROOT / "brain" / "cnsh_cards"
    报告目录 = PROJECT_ROOT / "audit" / "reports"
    for 目录 in (卡片目录, 报告目录):
        if not 目录.exists():
            continue
        for 文件 in sorted(目录.glob("*.md")):
            if 文件.is_file():
                yield _解析_markdown(文件)


class TripleSync:
    """三层同步引擎。"""

    def __init__(
        self,
        github_root: Optional[Path] = None,
        notion_dashboard: Optional[LongHunNotionDashboard] = None,
    ):
        self.github_root = Path(github_root) if github_root else GITHUB_ROOT
        self.notion_dashboard = notion_dashboard

    def _get_notion_dashboard(self) -> Optional[LongHunNotionDashboard]:
        if self.notion_dashboard:
            return self.notion_dashboard
        令牌 = os.environ.get("NOTION_TOKEN") or os.environ.get("LONGHUN_NOTION_TOKEN")
        父页面 = os.environ.get("LONGHUN_NOTION_PARENT_PAGE")
        if not 令牌 or not 父页面:
            return None
        dash = LongHunNotionDashboard(token=令牌, parent_page_id=父页面)
        dash.init_dashboard()
        return dash

    def sync_to_notion(self) -> Dict[str, Any]:
        """阶段 1：本地 → Notion。"""
        dash = self._get_notion_dashboard()
        if not dash:
            return {"ok": False, "reason": "缺少 Notion 配置，跳过同步"}

        结果 = {"ok": True, "synced": 0, "failed": 0, "details": []}
        for 档案 in _扫描本地档案():
            resp = dash.add_or_update_page(
                title=档案["title"],
                dna=档案["dna"],
                tags=档案["tags"],
                path=档案["path"],
                source=档案["source"],
            )
            if resp.get("ok"):
                结果["synced"] += 1
            else:
                结果["failed"] += 1
            结果["details"].append({"title": 档案["title"], "ok": resp.get("ok"), "error": resp.get("error", "")})
        return 结果

    def freeze_to_github(self, month: Optional[str] = None) -> Dict[str, Any]:
        """阶段 2：本地 → GitHub 月度冻结。"""
        月份 = month or _current_month()
        目标目录 = self.github_root / "monthly" / 月份
        目标目录.mkdir(parents=True, exist_ok=True)

        索引 = [f"# LU 公开档案月度冻结 · {月份}\n", f"**DNA**: `{DNA}`\n", "**更新时间**: " + _now_iso() + "\n", "\n## 档案列表\n"]
        copied = 0
        for 档案 in _扫描本地档案():
            目标文件 = 目标目录 / Path(档案["path"]).name
            shutil.copy2(档案["abs_path"], 目标文件)
            索引.append(f"- [{档案['title']}]({目标文件.name}) · `{档案['source']}` · `{档案['dna']}`\n")
            copied += 1

        readme_path = 目标目录 / "README.md"
        readme_path.write_text("".join(索引), encoding="utf-8")

        # Git 操作
        git_ok = self._git_commit_and_push(月份)
        return {
            "ok": True,
            "month": 月份,
            "copied": copied,
            "target_dir": str(目标目录),
            "git_pushed": git_ok,
        }

    def _git_commit_and_push(self, 月份: str) -> bool:
        """初始化 git 仓库、配置 remote、提交并推送。"""
        try:
            self.github_root.mkdir(parents=True, exist_ok=True)
            if not (self.github_root / ".git").exists():
                subprocess.run(["git", "init"], cwd=self.github_root, check=True, capture_output=True)

            远程仓库 = os.environ.get("LONGHUN_GITHUB_REPO")
            当前远程 = subprocess.run(
                ["git", "remote"], cwd=self.github_root, capture_output=True, text=True
            ).stdout
            if 远程仓库 and "origin" not in 当前远程:
                subprocess.run(
                    ["git", "remote", "add", "origin", 远程仓库],
                    cwd=self.github_root, check=True, capture_output=True,
                )

            if "origin" not in subprocess.run(
                ["git", "remote"], cwd=self.github_root, capture_output=True, text=True
            ).stdout:
                print("[三层同步] 未配置 GitHub remote，仅生成本地月度归档")
                return False

            subprocess.run(["git", "config", "user.email", "uid9622@longhun.system"], cwd=self.github_root, check=False, capture_output=True)
            subprocess.run(["git", "config", "user.name", "UID9622"], cwd=self.github_root, check=False, capture_output=True)
            subprocess.run(["git", "add", "."], cwd=self.github_root, check=True, capture_output=True)
            subprocess.run(
                ["git", "commit", "-m", f"月度冻结 {月份} · {DNA}"],
                cwd=self.github_root, check=False, capture_output=True,
            )
            push_proc = subprocess.run(
                ["git", "push", "-u", "origin", "HEAD"],
                cwd=self.github_root, check=False, capture_output=True, text=True,
            )
            if push_proc.returncode != 0:
                print(f"[三层同步] GitHub push 失败：{push_proc.stderr[:500]}")
                return False
            return True
        except Exception as e:
            print(f"[三层同步] Git 操作异常：{e}")
            return False


def main() -> int:
    parser = argparse.ArgumentParser(description="龍魂三层同步引擎")
    parser.add_argument("--sync-notion", action="store_true", help="同步本地档案到 Notion")
    parser.add_argument("--freeze-github", action="store_true", help="冻结本地档案到 GitHub")
    parser.add_argument("--monthly", action="store_true", help="执行完整月度同步：Notion + GitHub")
    parser.add_argument("--month", help="指定月份，格式 YYYY-MM")
    args = parser.parse_args()

    引擎 = TripleSync()

    if args.monthly:
        args.sync_notion = True
        args.freeze_github = True

    if args.sync_notion:
        print("[三层同步] 阶段 1：本地 → Notion")
        print(引擎.sync_to_notion())

    if args.freeze_github:
        print("[三层同步] 阶段 2：本地 → GitHub")
        print(引擎.freeze_to_github(month=args.month))

    if not (args.sync_notion or args.freeze_github):
        parser.print_help()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

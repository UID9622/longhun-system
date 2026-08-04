#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 知识迁移引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-KNOWLEDGE-MIGRATE-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能:
  - 将本地编译/拉取的知识推送到 Notion（API写入）
  - 导出为 Markdown 包（兼容 CSDN/GitHub）
  - 生成迁移日志

用法:
  lh 知识迁移 --to notion
  lh 知识迁移 --to markdown    # 导出Markdown包
  lh 知识迁移 --to github      # 推送到GitHub
  lh 知识迁移 --all
"""

import os
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

PROJECT_ROOT = Path.home() / "longhun-system"
HARVEST_DIR = PROJECT_ROOT / "data" / "harvested_knowledge"
COMPILED_DIR = PROJECT_ROOT / "data" / "compiled"
EXPORT_DIR = PROJECT_ROOT / "data" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def _load_json(path: Path) -> dict:
    if path.exists():
        with open(path, 'r') as f:
            return json.load(f)
    return {}


class KnowledgeMigrator:
    def __init__(self):
        self.log = []
        self.notion_api_key = os.environ.get("NOTION_API_KEY")
        self.notion_db_id = os.environ.get("NOTION_DATABASE_ID")
        self.github_token = os.environ.get("GITHUB_TOKEN")

    def _gather_content(self) -> Dict[str, str]:
        """收集待迁移内容"""
        content = {}
        for name in ["PRINCIPLES.md", "RULES.md", "MISSING_MODULES.md", "CODE_CANDIDATES.md"]:
            fpath = HARVEST_DIR / name
            if fpath.exists():
                content[name] = fpath.read_text(encoding="utf-8")
        for name in ["compiled_rules.json", "compiled_triggers.json"]:
            fpath = COMPILED_DIR / name
            if fpath.exists():
                content[name] = fpath.read_text(encoding="utf-8")
        return content

    def migrate_to_notion(self, dry_run: bool = False) -> Dict:
        """迁移到 Notion（通过 API）"""
        if not self.notion_api_key or not self.notion_db_id:
            return {"status": "skipped", "message": "NOTION_API_KEY 或 NOTION_DATABASE_ID 未设置，设置后重试"}

        content = self._gather_content()
        if not content:
            return {"status": "empty", "message": "无可迁移内容，先运行 lh 知识拉取 + lh 知识编译"}

        if dry_run:
            return {"status": "dry_run", "files": list(content.keys()), "count": len(content)}

        imported = 0
        try:
            import requests
            headers = {
                "Authorization": f"Bearer {self.notion_api_key}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            }
            db_id = self.notion_db_id.strip()

            for fname, fcontent in list(content.items())[:8]:  # 限制8条防限流
                preview = fcontent[:1800]
                page_data = {
                    "parent": {"database_id": db_id},
                    "properties": {
                        "Name": {"title": [{"text": {"content": f"📄 {fname}"}}]},
                        "Tags": {"multi_select": [{"name": "知识迁移"}, {"name": "自动生成"}]},
                    },
                    "children": [{
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {"rich_text": [{"type": "text", "text": {"content": preview}}]}
                    }]
                }
                try:
                    resp = requests.post("https://api.notion.com/v1/pages", headers=headers, json=page_data, timeout=15)
                    if resp.status_code in (200, 201):
                        imported += 1
                        self.log.append(f"✅ {fname} → Notion")
                    else:
                        err = resp.text[:100]
                        self.log.append(f"⚠️ {fname} 失败: {resp.status_code} {err}")
                except Exception as e:
                    self.log.append(f"⚠️ {fname} 请求异常: {e}")

        except ImportError:
            return {"status": "skipped", "message": "请安装: pip install requests"}

        return {"status": "done", "imported": imported, "log": self.log}

    def migrate_to_markdown(self) -> Dict:
        """导出为 Markdown 包（兼容 CSDN/GitHub 上传）"""
        content = self._gather_content()
        if not content:
            return {"status": "empty", "message": "无可导出内容"}

        pkg_dir = EXPORT_DIR / f"knowledge_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        pkg_dir.mkdir(parents=True, exist_ok=True)

        # 写 README
        readme = f"""# 龍魂知识包
导出时间: {datetime.now().isoformat()}
DNA: #龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-EXPORT-UID9622
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

## 内容清单
"""
        for fname in content:
            readme += f"- {fname} ({len(content[fname])} 字符)\n"

        (pkg_dir / "README.md").write_text(readme, encoding="utf-8")

        for fname, fcontent in content.items():
            safe_name = fname.replace("/", "_")
            (pkg_dir / safe_name).write_text(fcontent, encoding="utf-8")

        self.log.append(f"导出 {len(content)} 个文件到 {pkg_dir}")
        return {"status": "done", "export_dir": str(pkg_dir), "files": len(content)}

    def migrate_to_github(self) -> Dict:
        """推送到 GitHub（Git 方式）"""
        content = self._gather_content()
        if not content:
            return {"status": "empty", "message": "无可推送内容"}

        # 先导出 Markdown 包
        md_result = self.migrate_to_markdown()
        if md_result["status"] != "done":
            return md_result

        export_dir = Path(md_result["export_dir"])
        repo_dir = PROJECT_ROOT
        data_dir = repo_dir / "data" / "exports"

        try:
            cmds = [
                ["git", "add", str(data_dir.relative_to(repo_dir)) + "/"],
                ["git", "commit", "-m", f"知识迁移: {datetime.now().strftime('%Y-%m-%d %H:%M')}"],
                ["git", "push"],
            ]
            for cmd in cmds:
                result = subprocess.run(cmd, cwd=repo_dir, capture_output=True, text=True)
                if result.returncode != 0 and "nothing to commit" not in result.stdout + result.stderr:
                    return {"status": "error", "command": " ".join(cmd), "stderr": result.stderr.strip()}

            self.log.append("✅ 已推送到 GitHub")
            return {"status": "done", "pushed": str(export_dir)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def migrate_all(self) -> Dict:
        results = {}
        results["notion"] = self.migrate_to_notion()
        results["markdown"] = self.migrate_to_markdown()
        results["github"] = self.migrate_to_github()
        results["log"] = self.log
        return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·知识迁移引擎")
    parser.add_argument("--to", choices=["notion", "markdown", "github"], help="目标平台")
    parser.add_argument("--all", action="store_true", help="全部平台")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()

    migrator = KnowledgeMigrator()

    if args.all:
        result = migrator.migrate_all()
    elif args.to == "notion":
        result = migrator.migrate_to_notion(dry_run=args.dry_run)
    elif args.to == "markdown":
        result = migrator.migrate_to_markdown()
    elif args.to == "github":
        result = migrator.migrate_to_github()
    else:
        parser.print_help()
        return

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n📤 知识迁移: {result.get('status', 'unknown')}")
        for entry in result.get("log", []):
            print(f"  {entry}")
        if result.get("export_dir"):
            print(f"  📁 导出目录: {result['export_dir']}")


if __name__ == "__main__":
    main()

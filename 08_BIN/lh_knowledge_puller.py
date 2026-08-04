#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·统一知识拉取引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·戊申·申时·䷗复-KNOWLEDGE-PULLER-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

五源统一汇聚: 本地·Notion·鲲鹏·CSDN·Git
一键汇聚 → 自动去重 → 索引缓存 → AI运行时随时调取

用法:
  lh knowledge-pull                 # 全量拉取（所有来源）
  lh knowledge-pull --source local  # 指定来源拉取
  lh knowledge-pull --dry-run       # 预览模式
  lh knowledge-pull --force         # 强制覆盖
  lh knowledge-pull --list-sources  # 查看可用来源
  lh knowledge-pull --status        # 拉取状态
  lh knowledge-pull --clean         # 清理缓存
"""

import os
import sys
import json
import hashlib
import shutil
import subprocess
import argparse
import logging
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any

# ═══════════════════════════════════════════════
# 路径 · 自举
# ═══════════════════════════════════════════════

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "bin"))
sys.path.insert(0, str(ROOT))

CST = timezone(timedelta(hours=8))

# 缓存与索引目录（遵循项目路径铁律）
KNOWLEDGE_DIR = ROOT / "data" / "knowledge_pull"
CACHE_DIR = KNOWLEDGE_DIR / "cache"
NOTION_CACHE = KNOWLEDGE_DIR / "notion"
KUNPENG_CACHE = KNOWLEDGE_DIR / "kunpeng"
INDEX_FILE = KNOWLEDGE_DIR / "index.json"
SOURCES_FILE = ROOT / "config" / "knowledge_sources.yaml"
LOG_DIR = ROOT / "logs"

for d in [KNOWLEDGE_DIR, CACHE_DIR, NOTION_CACHE, KUNPENG_CACHE, LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════
# 日志
# ═══════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"knowledge_puller_{datetime.now(CST).strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("knowledge_puller")

# ═══════════════════════════════════════════════
# DNA · 常量
# ═══════════════════════════════════════════════

DNA = "#龍芯⚡️丙午·丙申·戊申·申时·䷗复-KNOWLEDGE-PULLER-v1.0-UID9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
IDENTITY = "诸葛鑫（UID9622）"
KUNPENG_HOST = "119.13.90.27"
KUNPENG_KNOWLEDGE_PATH = "/opt/longhun/knowledge/"

# ═══════════════════════════════════════════════
# 来源基类
# ═══════════════════════════════════════════════

class KnowledgeSource:
    """知识来源基类"""
    def __init__(self, name: str, config: dict):
        self.name = name
        self.config = config
        self.enabled = config.get("enabled", True)

    def pull(self, dry_run: bool = False, force: bool = False) -> dict:
        raise NotImplementedError

    def status(self) -> dict:
        return {"name": self.name, "enabled": self.enabled, "last_pull": None, "count": 0}

# ═══════════════════════════════════════════════
# 1. 本地来源
# ═══════════════════════════════════════════════

class LocalSource(KnowledgeSource):
    """本地文件系统 — 扫描项目核心目录"""
    def pull(self, dry_run: bool = False, force: bool = False) -> dict:
        results = {"source": "local", "status": "success", "items": [], "errors": []}
        scan_paths = self.config.get("paths", [
            "01_protocols/", "bin/", "docs/", "papers/",
            "portal/", "deploy/", "config/", "engines/"
        ])
        for rel_path in scan_paths:
            full = ROOT / rel_path
            if not full.exists():
                results["errors"].append(f"路径不存在: {rel_path}")
                continue
            for fp in full.rglob("*"):
                if not fp.is_file() or fp.name.startswith("."):
                    continue
                try:
                    h = hashlib.sha256(fp.read_bytes()).hexdigest()[:16]
                    rel = str(fp.relative_to(ROOT))
                    if not dry_run:
                        dest = CACHE_DIR / rel
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        if force or not dest.exists():
                            shutil.copy2(fp, dest)
                    results["items"].append({"path": rel, "hash": h, "size": fp.stat().st_size})
                except Exception as e:
                    results["errors"].append(f"{fp}: {e}")
        logger.info(f"📁 本地: {len(results['items'])} 文件")
        return results

# ═══════════════════════════════════════════════
# 2. Notion来源 — 复用现有 Notion 全量同步
# ═══════════════════════════════════════════════

class NotionSource(KnowledgeSource):
    """Notion知识库 — 委托给 lh_notion_full_sync.py"""
    def pull(self, dry_run: bool = False, force: bool = False) -> dict:
        results = {"source": "notion", "status": "pending", "items": [], "errors": []}
        token = os.environ.get("NOTION_TOKEN_BACKUP") or os.environ.get("NOTION_TOKEN")
        if not token:
            results["errors"].append("NOTION_TOKEN 未设置")
            results["status"] = "no_token"
            return results
        if dry_run:
            results["status"] = "dry_run_skipped"
            results["items"].append({"note": "预览模式·跳过Notion拉取"})
            return results
        try:
            sync_script = str(ROOT / "bin" / "lh_notion_full_sync.py")
            # 增量同步，只拉变化
            cmd = [sys.executable, sync_script, "sync", "--incremental"]
            if force:
                cmd.remove("--incremental")
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if proc.returncode == 0:
                results["status"] = "success"
                # 统计缓存文件数
                cached = list(NOTION_CACHE.rglob("*.json"))
                results["items"] = [{"file": str(c.relative_to(NOTION_CACHE))} for c in cached]
                logger.info(f"📚 Notion: {len(cached)} 条记录")
            else:
                results["status"] = "failed"
                results["errors"].append(proc.stderr[:500])
        except subprocess.TimeoutExpired:
            results["errors"].append("Notion同步超时(300s)")
            results["status"] = "timeout"
        except Exception as e:
            results["errors"].append(str(e))
            results["status"] = "error"
        return results

# ═══════════════════════════════════════════════
# 3. 鲲鹏来源 — rsync 远端知识库
# ═══════════════════════════════════════════════

class KunpengSource(KnowledgeSource):
    """鲲鹏服务器 — rsync /opt/longhun/knowledge/"""
    def pull(self, dry_run: bool = False, force: bool = False) -> dict:
        results = {"source": "kunpeng", "status": "pending", "items": [], "errors": []}
        host = self.config.get("host", KUNPENG_HOST)
        remote_path = self.config.get("path", KUNPENG_KNOWLEDGE_PATH)
        ssh_key = os.path.expanduser("~/.ssh/longhun_kunpeng_ed25519")

        cmd = ["rsync", "-avz", "--timeout=60",
               "-e", f"ssh -i {ssh_key} -o StrictHostKeyChecking=no",
               f"root@{host}:{remote_path}", str(KUNPENG_CACHE) + "/"]
        if dry_run:
            cmd.insert(1, "--dry-run")

        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if proc.returncode == 0:
                results["status"] = "success"
                files = list(KUNPENG_CACHE.rglob("*")) if KUNPENG_CACHE.exists() else []
                results["items"] = [{"file": str(f.relative_to(KUNPENG_CACHE))} for f in files if f.is_file()]
                logger.info(f"🖥️ 鲲鹏: {len(results['items'])} 文件")
            else:
                # 0返回码也可能=无变化，rsync部分失败才报错
                err = proc.stderr.strip()
                if err:
                    results["errors"].append(err[:500])
                    results["status"] = "partial"
                else:
                    results["status"] = "success"
        except subprocess.TimeoutExpired:
            results["errors"].append("鲲鹏rsync超时(120s)")
            results["status"] = "timeout"
        except Exception as e:
            results["errors"].append(str(e))
            results["status"] = "error"
        return results

# ═══════════════════════════════════════════════
# 4. CSDN来源 — 复用现有 CSDN 同步引擎
# ═══════════════════════════════════════════════

class CSDNSource(KnowledgeSource):
    """CSDN博客 — 委托给 lh_csdn_sync.py"""
    def pull(self, dry_run: bool = False, force: bool = False) -> dict:
        results = {"source": "csdn", "status": "pending", "items": [], "errors": []}
        if dry_run:
            results["status"] = "dry_run_skipped"
            results["items"].append({"note": "预览模式·跳过CSDN拉取"})
            return results
        try:
            sync_script = str(ROOT / "bin" / "lh_csdn_sync.py")
            mode = "--sync" if force else "--sync --incremental"
            cmd = [sys.executable, sync_script] + mode.split()
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if proc.returncode == 0:
                results["status"] = "success"
                # 统计归档文件
                archive_dir = ROOT / "archive" / "csdn_sync"
                if archive_dir.exists():
                    md_files = list(archive_dir.rglob("*.md"))
                    results["items"] = [{"file": str(m.relative_to(archive_dir))} for m in md_files]
                logger.info(f"✍️ CSDN: {len(results['items'])} 篇文章")
            else:
                results["status"] = "failed"
                results["errors"].append(proc.stderr[:500] if proc.stderr else "返回码非0")
        except subprocess.TimeoutExpired:
            results["errors"].append("CSDN同步超时(300s)")
            results["status"] = "timeout"
        except Exception as e:
            results["errors"].append(str(e))
            results["status"] = "error"
        return results

# ═══════════════════════════════════════════════
# 5. Git来源 — 拉取关联仓库
# ═══════════════════════════════════════════════

class GitSource(KnowledgeSource):
    """Git仓库 — 拉取关联项目"""
    def pull(self, dry_run: bool = False, force: bool = False) -> dict:
        results = {"source": "git", "status": "pending", "items": [], "errors": []}
        repos = self.config.get("repos", [])
        if not repos:
            results["items"].append({"note": "无配置Git仓库"})
            results["status"] = "empty"
            return results

        git_cache = CACHE_DIR / "git"
        git_cache.mkdir(parents=True, exist_ok=True)

        for repo_url in repos:
            name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
            dest = git_cache / name
            try:
                if dest.exists() and not force:
                    # 增量: git pull
                    if not dry_run:
                        subprocess.run(["git", "-C", str(dest), "pull", "--ff-only"],
                                       capture_output=True, text=True, timeout=60)
                    results["items"].append({"repo": repo_url, "action": "pull"})
                else:
                    if not dry_run:
                        if dest.exists():
                            shutil.rmtree(dest)
                        subprocess.run(["git", "clone", "--depth", "1", repo_url, str(dest)],
                                       capture_output=True, text=True, timeout=120)
                    results["items"].append({"repo": repo_url, "action": "clone"})
                logger.info(f"🔗 Git: {name} → {'pull' if dest.exists() else 'clone'}")
            except Exception as e:
                results["errors"].append(f"{repo_url}: {e}")
        results["status"] = "success" if not results["errors"] else "partial"
        return results

# ═══════════════════════════════════════════════
# 主引擎
# ═══════════════════════════════════════════════

# 默认来源配置
DEFAULT_SOURCES = {
    "local":   {"enabled": True, "paths": [
        "01_protocols/", "bin/", "docs/", "papers/",
        "portal/", "deploy/", "config/", "engines/"
    ], "description": "本地协议·脚本·文档·论文"},
    "notion":  {"enabled": True, "description": "Notion知识库(需NOTION_TOKEN)", "databases": [
        "THEORY_DB", "AXIOM_DB", "FORMULA_DB", "TRACE_DB", "AUDIT_DB"
    ]},
    "kunpeng": {"enabled": True, "host": KUNPENG_HOST, "path": KUNPENG_KNOWLEDGE_PATH,
                "description": "鲲鹏服务器知识库"},
    "csdn":    {"enabled": True, "description": "CSDN博客·UID9622原创"},
    "git":     {"enabled": True, "repos": [
        "https://github.com/UID9622/longhun-system.git",
    ], "description": "Git关联仓库"},
}

class KnowledgePuller:
    """统一知识拉取主引擎"""

    def __init__(self):
        self.sources = self._load_sources()
        self.index = self._load_index()
        self._source_map = {
            "local":   LocalSource,
            "notion":  NotionSource,
            "kunpeng": KunpengSource,
            "csdn":    CSDNSource,
            "git":     GitSource,
        }

    def _load_sources(self) -> dict:
        if SOURCES_FILE.exists():
            try:
                import yaml
                with open(SOURCES_FILE, "r") as f:
                    return yaml.safe_load(f) or DEFAULT_SOURCES
            except ImportError:
                logger.warning("PyYAML未安装，使用默认来源配置")
            except Exception as e:
                logger.warning(f"来源配置加载失败: {e}")
        return DEFAULT_SOURCES

    def _load_index(self) -> dict:
        if INDEX_FILE.exists():
            return json.loads(INDEX_FILE.read_text("utf-8"))
        return {"version": "1.0", "dna": DNA, "sources": {}, "last_update": None}

    def _save_index(self):
        self.index["last_update"] = datetime.now(CST).isoformat()
        INDEX_FILE.write_text(json.dumps(self.index, ensure_ascii=False, indent=2), "utf-8")

    def pull_all(self, dry_run: bool = False, force: bool = False) -> dict:
        """全量拉取所有来源"""
        logger.info("🚀 全量知识拉取开始...")
        results = {}
        for name, cfg in self.sources.items():
            if not cfg.get("enabled", True):
                logger.info(f"⏭️ 跳过: {name}")
                continue
            logger.info(f"📥 {name}...")
            puller_cls = self._source_map.get(name)
            if puller_cls:
                puller = puller_cls(name, cfg)
                results[name] = puller.pull(dry_run, force)
            else:
                results[name] = {"status": "unknown", "errors": [f"未知来源: {name}"]}

        # 更新索引
        for name, r in results.items():
            self.index["sources"][name] = {
                "status": r.get("status"),
                "count": len(r.get("items", [])),
                "last_pull": datetime.now(CST).isoformat(),
            }
        self._save_index()

        total = sum(len(r.get("items", [])) for r in results.values())
        errs = sum(len(r.get("errors", [])) for r in results.values())

        mode = "🔍预览" if dry_run else "✅完成"
        logger.info(f"{mode}: {total} 项, {errs} 错误")
        return results

    def pull_one(self, name: str, dry_run: bool = False, force: bool = False) -> dict:
        """拉取单个来源"""
        cfg = self.sources.get(name)
        if not cfg:
            return {"status": "not_found", "errors": [f"未知来源: {name}"]}
        puller_cls = self._source_map.get(name)
        if not puller_cls:
            return {"status": "unknown", "errors": [f"无拉取器: {name}"]}
        puller = puller_cls(name, cfg)
        return puller.pull(dry_run, force)

    def list_sources(self) -> dict:
        return {n: {"enabled": c.get("enabled", True),
                     "description": c.get("description", ""),
                     "status": self.index.get("sources", {}).get(n, {}).get("status", "未拉取")}
                for n, c in self.sources.items()}

    def show_status(self):
        idx = self._load_index()
        print(f"\n{'='*50}")
        print(f"  📊 知识拉取状态")
        print(f"  DNA: {DNA}")
        print(f"  最后更新: {idx.get('last_update', '从未')}")
        print(f"{'='*50}")
        total = 0
        for name, info in idx.get("sources", {}).items():
            count = info.get("count", 0)
            total += count
            icon = "✅" if info.get("status") == "success" else "⏳"
            print(f"  {icon} {name}: {count} 项 | {info.get('status', '?')} | {info.get('last_pull', '?')[:19]}")
        print(f"{'='*50}")
        print(f"  总计: {total} 项")
        print()

    def clean_cache(self):
        for d in [CACHE_DIR, NOTION_CACHE, KUNPENG_CACHE]:
            if d.exists():
                shutil.rmtree(d)
                d.mkdir()
        if INDEX_FILE.exists():
            INDEX_FILE.unlink()
        print("🧹 缓存已清理")

# ═══════════════════════════════════════════════
# ROOT_CARD
# ═══════════════════════════════════════════════

ROOT_CARD = r"""
┌─────────────────────────────────────────────────────────────┐
│           🐉 龍魂·统一知识拉取引擎 ROOT_CARD                │
├─────────────────────────────────────────────────────────────┤
│  系统: 龍魂知识拉取引擎 v1.0                                │
│  DNA:  #龍芯⚡️丙午·丙申·戊申·申时·䷗复-KNOWLEDGE-PULLER  │
│  确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                │
│  创建: 诸葛鑫（UID9622）                                    │
│  协议: CC BY-NC-SA 4.0                                      │
├─────────────────────────────────────────────────────────────┤
│  五源覆盖:                                                  │
│    📁 本地 — 项目目录扫描                                   │
│    📚 Notion — 增量同步·复用现有引擎                        │
│    🖥️ 鲲鹏 — rsync远端知识库                               │
│    ✍️ CSDN — 博客归档·复用现有引擎                          │
│    🔗 Git — 关联仓库clone/pull                              │
├─────────────────────────────────────────────────────────────┤
│  命令:                                                      │
│    lh knowledge-pull                 # 全量拉取              │
│    lh knowledge-pull --source local  # 指定来源              │
│    lh knowledge-pull --dry-run       # 预览                  │
│    lh knowledge-pull --force         # 强制覆盖              │
│    lh knowledge-pull --list-sources  # 来源列表              │
│    lh knowledge-pull --status        # 拉取状态              │
│    lh knowledge-pull --clean         # 清理缓存              │
└─────────────────────────────────────────────────────────────┘
"""

# ═══════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·统一知识拉取引擎 v1.0",
        epilog="示例: lh knowledge-pull --source local --dry-run",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--source", "-s", type=str, help="指定来源 (local/notion/kunpeng/csdn/git)")
    parser.add_argument("--dry-run", "-n", action="store_true", help="预览模式·不实际执行")
    parser.add_argument("--force", "-f", action="store_true", help="强制覆盖缓存")
    parser.add_argument("--list-sources", action="store_true", help="列出所有来源")
    parser.add_argument("--status", action="store_true", help="查看拉取状态")
    parser.add_argument("--clean", action="store_true", help="清理所有缓存")
    parser.add_argument("--root-card", action="store_true", help="显示ROOT_CARD")

    args = parser.parse_args()
    puller = KnowledgePuller()

    if args.list_sources:
        sources = puller.list_sources()
        print("\n📋 可用知识来源:")
        print(f"{'来源':<10} {'状态':<6} {'说明'}")
        print("-" * 50)
        for name, info in sources.items():
            icon = "✅" if info["enabled"] else "⛔"
            print(f"  {icon} {name:<8} {info.get('status','?'):<6} {info.get('description','')}")
        print()
        return

    if args.status:
        puller.show_status()
        return

    if args.clean:
        puller.clean_cache()
        return

    if args.root_card:
        print(ROOT_CARD)
        return

    # 执行拉取
    if args.source:
        result = puller.pull_one(args.source, args.dry_run, args.force)
        print(f"\n📥 拉取结果 ({args.source}):")
        print(f"  状态: {result.get('status')}")
        print(f"  项目: {len(result.get('items', []))} 项")
        if result.get("errors"):
            for e in result["errors"]:
                print(f"  ⚠️ {e}")
    else:
        results = puller.pull_all(args.dry_run, args.force)
        print(f"\n📥 全量拉取{'预览' if args.dry_run else '完成'}:")
        total = 0
        for name, r in results.items():
            c = len(r.get("items", []))
            total += c
            icon = "✅" if r.get("status") == "success" else "⚠️"
            print(f"  {icon} {name}: {c} 项")
            if r.get("errors"):
                for e in r["errors"][:3]:
                    print(f"     ⚠️ {e}")
        print(f"  ─────────────────")
        print(f"  总计: {total} 项")

if __name__ == "__main__":
    main()

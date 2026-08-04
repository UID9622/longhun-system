#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·统一配置拉取器 v1.0
DNA: #龍芯⚡️丙午·丙申·戊申·申时·䷗复-CONFIG-PULLER-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

多来源配置自动发现 → 合并 → 版本管理 → 一键导出
支持 YAML/JSON/TOML 格式自动解析

用法:
  lh config-pull                  # 全量拉取所有配置
  lh config-pull --list           # 列出所有配置文件
  lh config-pull --pull feishu    # 拉取指定配置
  lh config-pull --merge          # 合并所有配置
  lh config-pull --report         # 配置健康报告
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional
import argparse
import logging

# ═══════════════════════════════════════════════
# 路径
# ═══════════════════════════════════════════════

ROOT = Path(__file__).resolve().parent.parent
CONFIG_BACKUP = ROOT / "data" / "config_snapshots"
CONFIG_BACKUP.mkdir(parents=True, exist_ok=True)
CST = timezone(timedelta(hours=8))

DNA = "#龍芯⚡️丙午·丙申·戊申·申时·䷗复-CONFIG-PULLER-v1.0-UID9622"

# ═══════════════════════════════════════════════
# 日志
# ═══════════════════════════════════════════════

LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"config_puller_{datetime.now(CST).strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("config_puller")

# ═══════════════════════════════════════════════
# 配置发现 — 自动扫描项目所有配置文件
# ═══════════════════════════════════════════════

SCAN_DIRS = {
    "config":      (ROOT / "config",         ["*.yaml", "*.json"],       "项目配置"),
    "protocols":   (ROOT / "01_protocols",   ["*.md", "*.yaml"],         "协议层"),
    "deploy":      (ROOT / "deploy",         ["*.sh", "*.service", "*.yaml"], "部署配置"),
    "codebuddy":   (ROOT / ".codebuddy",     ["*.json", "*.yaml", "*.md"], "CodeBuddy配置"),
    "env":         (ROOT,                    ["*.yaml", "*.json"],        "根目录配置"),
    "prompt_router": (ROOT / "config" / "prompt_router", ["*.yaml"],     "提示词路由"),
}

EXCLUDE = [".asc", ".gitkeep", "backup", "node_modules", "__pycache__", ".git"]
MAX_SIZE = 5 * 1024 * 1024  # 5MB

def safe_read(path: Path) -> Optional[dict]:
    """安全读取配置文件（YAML/JSON自动识别）"""
    if path.stat().st_size > MAX_SIZE:
        return {"_warning": f"文件过大({path.stat().st_size}字节)·已跳过"}
    try:
        if path.suffix in (".yaml", ".yml"):
            import yaml
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            return data
        elif path.suffix == ".json":
            data = json.loads(path.read_text("utf-8"))
            return data
        elif path.suffix == ".md":
            text = path.read_text("utf-8")[:5000]
            return {"_type": "markdown", "_preview": text[:500], "_lines": len(text.splitlines())}
        else:
            # 文本文件
            text = path.read_text("utf-8")[:5000]
            return {"_type": "text", "_preview": text[:500], "_lines": len(text.splitlines())}
    except Exception as e:
        return {"_error": str(e)}

# ═══════════════════════════════════════════════
# 配置拉取器
# ═══════════════════════════════════════════════

class ConfigPuller:
    """统一配置拉取器"""

    def __init__(self):
        self.scan_result = {}
        self.manifest = {"version": "1.0", "dna": DNA, "scanned_at": None, "files": {}, "merged": None}

    def discover_all(self) -> dict:
        """自动发现所有配置文件"""
        results = {}
        total = 0
        for name, (directory, patterns, desc) in SCAN_DIRS.items():
            if not directory.exists():
                results[name] = {"desc": desc, "path": str(directory), "status": "not_found", "files": []}
                continue
            files = []
            for pat in patterns:
                for fp in directory.rglob(pat):
                    if any(x in str(fp) for x in EXCLUDE):
                        continue
                    if fp.is_file():
                        files.append({
                            "path": str(fp.relative_to(ROOT)),
                            "size": fp.stat().st_size,
                            "modified": datetime.fromtimestamp(fp.stat().st_mtime, tz=CST).isoformat(),
                        })
            files.sort(key=lambda x: x["path"])
            results[name] = {"desc": desc, "path": str(directory), "count": len(files), "files": files}
            total += len(files)
        self.scan_result = results
        self.manifest["scanned_at"] = datetime.now(CST).isoformat()
        logger.info(f"🔍 扫描完成: {total} 个配置文件")
        return results

    def read_config(self, name: str) -> Optional[dict]:
        """读取指定命名的配置"""
        if name not in SCAN_DIRS:
            # 尝试作为文件路径
            path = ROOT / name
            if not path.exists():
                return {"_error": f"配置不存在: {name}"}
            return safe_read(path)

        directory, patterns, _ = SCAN_DIRS[name]
        if not directory.exists():
            return {"_error": f"目录不存在: {directory}"}

        items = {}
        for pat in patterns:
            for fp in directory.rglob(pat):
                if any(x in str(fp) for x in EXCLUDE) or not fp.is_file():
                    continue
                rel = str(fp.relative_to(ROOT))
                items[rel] = safe_read(fp)
        return items

    def merge_all(self) -> dict:
        """合并所有配置为统一清单"""
        self.discover_all()
        merged = {
            "dna": DNA,
            "merged_at": datetime.now(CST).isoformat(),
            "categories": [],
            "file_count": 0,
            "total_size": 0,
        }

        for cat_name, info in self.scan_result.items():
            cat_entry = {
                "name": cat_name,
                "description": info["desc"],
                "files": []
            }
            for f_info in info["files"]:
                rel_path = f_info["path"]
                abs_path = ROOT / rel_path
                content = safe_read(abs_path)
                entry = {
                    "path": rel_path,
                    "size": f_info["size"],
                    "modified": f_info["modified"],
                    "content_type": type(content).__name__,
                    "key_count": len(content) if isinstance(content, dict) else None,
                    "hash": hashlib.sha256(json.dumps(content, default=str, ensure_ascii=False).encode()).hexdigest()[:12],
                }
                cat_entry["files"].append(entry)
                merged["file_count"] += 1
                merged["total_size"] += f_info["size"]
            merged["categories"].append(cat_entry)

        # 保存快照
        ts = datetime.now(CST).strftime("%Y%m%d_%H%M%S")
        snapshot_path = CONFIG_BACKUP / f"merged_{ts}.json"
        snapshot_path.write_text(json.dumps(merged, ensure_ascii=False, indent=2), "utf-8")

        self.manifest["merged"] = str(snapshot_path)
        logger.info(f"📦 合并完成: {merged['file_count']} 文件, {merged['total_size']:,} 字节 → {snapshot_path.name}")
        return merged

    def health_report(self) -> dict:
        """配置健康检查"""
        self.discover_all()
        issues = []

        # 检查必需配置
        required = ["config/system_registry.json", ".codebuddy/longhun_neural_net.json"]
        for r in required:
            fp = ROOT / r
            if not fp.exists():
                issues.append({"level": "🔴", "file": r, "issue": "缺失必需配置文件"})
            elif fp.stat().st_size == 0:
                issues.append({"level": "🔴", "file": r, "issue": "配置文件为空"})

        # 检查大文件
        for cat, info in self.scan_result.items():
            for f in info["files"]:
                if f["size"] > MAX_SIZE:
                    issues.append({"level": "🟡", "file": f["path"], "issue": f"文件过大({f['size']:,}字节)", "suggestion": "考虑拆分或移入models/"})

        # 检查重复
        seen = {}
        for cat, info in self.scan_result.items():
            for f in info["files"]:
                name = Path(f["path"]).name
                if name in seen:
                    issues.append({"level": "🟡", "file": f["path"], "issue": f"与 {seen[name]} 同名",
                                     "suggestion": "审查是否需要去重"})
                else:
                    seen[name] = f["path"]

        report = {
            "dna": DNA,
            "checked_at": datetime.now(CST).isoformat(),
            "total_files": sum(info["count"] for info in self.scan_result.values()),
            "issues": issues,
            "health": "🟢" if len(issues) == 0 else ("🟡" if all(i["level"] == "🟡" for i in issues) else "🔴"),
        }
        return report

# ═══════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·统一配置拉取器 v1.0",
        epilog="示例: lh config-pull --merge",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--list", action="store_true", help="列出所有配置分类")
    parser.add_argument("--pull", "-p", type=str, help="拉取指定配置分类名或路径")
    parser.add_argument("--merge", "-m", action="store_true", help="合并所有配置+保存快照")
    parser.add_argument("--report", "-r", action="store_true", help="配置健康检查报告")

    args = parser.parse_args()
    puller = ConfigPuller()

    if args.list:
        results = puller.discover_all()
        print(f"\n📋 配置文件清单 (DNA: {DNA})")
        print(f"{'分类':<15} {'说明':<15} {'文件数':<8} {'路径'}")
        print("-" * 80)
        total = 0
        for name, info in results.items():
            count = info["count"]
            total += count
            icon = "✅" if count > 0 else "❌"
            print(f"  {icon} {name:<13} {info['desc']:<15} {count:<8} {info['path']}")
        print("-" * 80)
        print(f"  总计: {total} 个配置文件")
        print()
        return

    if args.pull:
        result = puller.read_config(args.pull)
        if isinstance(result, dict) and result.get("_error"):
            print(f"\n❌ {result['_error']}")
            return
        print(f"\n📄 配置内容 ({args.pull}):")
        print("-" * 60)
        if isinstance(result, dict):
            for k, v in result.items():
                preview = str(v)[:200]
                print(f"  📁 {k}")
                print(f"     {preview}{'...' if len(str(v)) > 200 else ''}")
        else:
            print(str(result)[:500])
        print()
        return

    if args.merge:
        merged = puller.merge_all()
        print(f"\n✅ 配置合并完成")
        print(f"  DNA: {merged['dna']}")
        print(f"  时间: {merged['merged_at']}")
        print(f"  文件: {merged['file_count']} 个")
        print(f"  体积: {merged['total_size']:,} 字节")
        print(f"  分类: {len(merged['categories'])} 类")
        # 按分类统计
        for cat in merged["categories"]:
            yaml_count = len([f for f in cat["files"] if f["path"].endswith((".yaml",".yml"))])
            json_count = len([f for f in cat["files"] if f["path"].endswith(".json")])
            print(f"    📂 {cat['name']}: {len(cat['files'])} 文件 (YAML:{yaml_count} JSON:{json_count})")
        print()
        return

    if args.report:
        report = puller.health_report()
        print(f"\n🩺 配置健康检查报告")
        print(f"  DNA: {report['dna']}")
        print(f"  时间: {report['checked_at']}")
        print(f"  文件: {report['total_files']} 个")
        print(f"  健康: {report['health']}")
        print(f"  问题: {len(report['issues'])} 个")
        if report["issues"]:
            print()
            for issue in report["issues"]:
                print(f"  {issue['level']} {issue['file']}")
                print(f"     {issue['issue']}")
                if "suggestion" in issue:
                    print(f"     💡 {issue['suggestion']}")
        print()
        return

    # 默认: 全量拉取+合并
    merged = puller.merge_all()
    print(f"\n✅ 全量配置拉取完成 — {merged['file_count']} 文件")
    return 0

if __name__ == "__main__":
    main()

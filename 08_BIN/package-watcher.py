#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·甲午·辛酉·甲午·䷨损-PACKAGE-WATCHER-FILE1-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂体系 · 待融入包自动收集与分类器
LongHun System · Pending Integration Package Watcher & Classifier

DNA:#龍芯⚡️丙午·甲午·辛酉·甲午·䷨损-PACKAGE-WATCHER-FILE1-v1.0
责任: UID9622·不免责

功能：
  1. 扫描指定监控路径（默认 ~/Downloads 与 ~）
  2. 识别龍魂/CNSH/Kimi 相关新增/更新包
  3. 按规则自动分类到 skills/systems/protocols/monitoring/cnsh/docs/forensics/gateway/audit/archive
  4. 维护待融入队列 docs/package-integration-queue.json
  5. 生成审查报告 docs/package-watcher-report.md

用法：
  python3 bin/package-watcher.py [--watch-dir /path/to/watch] [--output-dir /path/to/output]
"""

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


# ═══════════════════════════════════════════════════════════════════════════════
# 分类规则：按关键字匹配（优先级从高到低）
# ═══════════════════════════════════════════════════════════════════════════════
CLASSIFICATION_RULES: List[Tuple[str, List[str]]] = [
    ("multi_content_archive", ["龍魂待整理", "待整理"]),
    ("warehouse_audit", ["技能检查", "warehouse", "audit", "审计改进", "审计改进"]),
    ("skills",          ["skill", "技能", "Skill"]),
    ("cnsh",            ["CNSH", "cnsh", "Runtime Governance", "语义接入", "语义接入"]),
    ("monitoring",      ["监控", "监控", "monitoring", "移动端", "移动端"]),
    ("protocols",       ["协议", "协议", "protocol", "根协议", "根协议"]),
    ("gateway",         ["网关", "网关", "gateway"]),
    ("forensics",       ["forensic", "取证", "取证"]),
    ("phase3",          ["Phase 3", "phase3", "Phase3"]),
    ("systems",         ["核心系统", "核心系统", "系统优化", "系统优化", "标准化", "标准化", "启动", "启动"]),
    ("docs",            ["知识矩阵", "知识矩阵", "计算公式", "计算公式", "流水线", "流水线", "使用说明", "使用说明"]),
    ("archive",         ["backup", "备份", "备份", "archive", "归档", "归档"]),
]

KNOWN_INTEGRATED = {
    "Kimi_Agent_启动全部技能",
    "Kimi_Agent_启动全部技能.zip",
    "Kimi_Agent_龍魂体系技能检查",
    "Kimi_Agent_龍魂体系技能检查.zip",
}

# 不应纳入待融入队列的项目（主干本身、敏感目录、备份等）
EXCLUDED_NAMES = {
    "longhun-system",
    ".longhun",
    ".longhun-credentials",
    ".longhun_skill_registry.json",
    ".longhun_shell_config",
    "longhun_dna_backup_20260605_173301.json",
    "longhun_dna_final_backup.json",
}

# 备份/归档类关键字
ARCHIVE_KEYWORDS = ["backup", "备份", "backup-", "-bfg", "archive", "归档", "待整理"]


# ═══════════════════════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════════════════════
def is_longhun_related(name: str) -> bool:
    """判断文件名是否与龍魂体系相关。"""
    lowered = name.lower()
    keywords = ["longhun", "龍魂", "Kimi_Agent", "CNSH", "龍芯", "龍魂", "UID9622"]
    return any(k.lower() in lowered for k in keywords) or any(k in name for k in keywords[1:])


def classify(name: str) -> str:
    """根据文件名关键字分类。"""
    lowered = name.lower()
    # 优先判断是否为备份/归档
    if any(k.lower() in lowered for k in ARCHIVE_KEYWORDS):
        return "archive"
    for category, patterns in CLASSIFICATION_RULES:
        for pattern in patterns:
            if pattern.lower() in lowered:
                return category
    return "unknown"


def compute_file_hash(path: Path) -> str:
    """计算文件 SHA-256（用于追踪变更）。"""
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, PermissionError):
        return ""


def package_id(path: Path) -> str:
    """生成包的稳定 ID。"""
    return f"{path.name}_{path.stat().st_mtime:.0f}"


def priority_for(category: str) -> str:
    """根据分类给出优先级建议。"""
    pmap = {
        "multi_content_archive": "P0",
        "systems": "P0",
        "cnsh": "P0",
        "phase3": "P0",
        "protocols": "P1",
        "monitoring": "P1",
        "gateway": "P1",
        "skills": "P1",
        "warehouse_audit": "P1",
        "audit": "P2",
        "forensics": "P2",
        "docs": "P2",
        "archive": "P3",
        "unknown": "P3",
    }
    return pmap.get(category, "P3")


def suggested_target(category: str) -> str:
    """建议融入主干的目标目录。"""
    tmap = {
        "multi_content_archive": "按 docs/龍魂待整理-integration-gap-report.md 分 P0-P3 逐步融入",
        "systems": "systems/ 或新增 systems/{name}/",
        "cnsh": "cnsh/core/",
        "phase3": "phase3/ 或 longhun-phase3/",
        "protocols": "01_protocols/",
        "monitoring": "mobile-monitoring.integrated/",
        "gateway": "integrated_modules/gateway/",
        "skills": "skills/ 或 skills/{category}/",
        "warehouse_audit": "skills/warehouse-audit/ 扩展",
        "audit": "skills/warehouse-audit/ 或新增 systems/audit/",
        "forensics": "tools/forensics/",
        "docs": "docs/references/ 或 docs/v3/",
        "archive": "_archive/ 或 longhun-archive/",
        "unknown": "待人工分类",
    }
    return tmap.get(category, "待人工分类")


# ═══════════════════════════════════════════════════════════════════════════════
# 扫描逻辑
# ═══════════════════════════════════════════════════════════════════════════════
class PackageWatcher:
    def __init__(self, watch_dirs: List[Path], output_dir: Path):
        self.watch_dirs = watch_dirs
        self.output_dir = output_dir
        self.queue_file = output_dir / "package-integration-queue.json"
        self.report_file = output_dir / "package-watcher-report.md"
        self.log_file = output_dir / "package-watcher.log"

    def load_queue(self) -> Dict[str, Any]:
        """载入现有队列。"""
        if self.queue_file.exists():
            try:
                return json.loads(self.queue_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        return {
            "dna": "#龍芯⚡️丙午·甲午·辛酉·甲午·䷨损-PACKAGE-INTEGRATION-QUEUE-v1.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "packages": {},
        }

    def save_queue(self, queue: Dict[str, Any]):
        """保存队列。"""
        self.queue_file.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")

    def scan(self) -> List[Dict]:
        """扫描监控路径，返回发现的包列表。"""
        found = []
        for watch_dir in self.watch_dirs:
            if not watch_dir.exists():
                self.log(f"⚠️ 监控路径不存在: {watch_dir}")
                continue

            for item in watch_dir.iterdir():
                if item.name.startswith(".") and item.name not in (".龍魂",):
                    continue
                if item.name in EXCLUDED_NAMES:
                    continue
                if not is_longhun_related(item.name):
                    continue

                stat = item.stat()
                item_hash = ""
                if item.is_file():
                    item_hash = compute_file_hash(item)

                pkg = {
                    "name": item.name,
                    "path": str(item),
                    "relative_path": str(item.relative_to(Path.home())),
                    "type": "directory" if item.is_dir() else "file",
                    "size_bytes": stat.st_size if item.is_file() else None,
                    "size_human": self._human_size(stat.st_size) if item.is_file() else "-",
                    "modified_utc": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                    "sha256": item_hash,
                    "category": classify(item.name),
                    "priority": priority_for(classify(item.name)),
                    "suggested_target": suggested_target(classify(item.name)),
                    "status": "integrated" if item.name in KNOWN_INTEGRATED else "pending",
                    "notes": "已融入主干" if item.name in KNOWN_INTEGRATED else "",
                }
                found.append(pkg)
        return found

    def update_queue(self, found: List[Dict]) -> Tuple[int, int, int]:
        """更新队列，返回新增/更新/未变更数量。"""
        queue = self.load_queue()
        packages = queue.setdefault("packages", {})

        added = 0
        updated = 0
        unchanged = 0

        for pkg in found:
            pid = f"{pkg['name']}"
            if pid in packages:
                existing = packages[pid]
                # 若状态需要根据已知融入列表修正
                if pkg["name"] in KNOWN_INTEGRATED and existing.get("status") not in ("integrated",):
                    existing.update(pkg)
                    existing["status"] = "integrated"
                    existing["notes"] = "已融入主干"
                    existing["last_seen"] = datetime.now(timezone.utc).isoformat()
                    updated += 1
                elif existing.get("sha256") != pkg["sha256"] or existing.get("modified_utc") != pkg["modified_utc"]:
                    existing.update(pkg)
                    existing["status"] = "updated"
                    existing["last_seen"] = datetime.now(timezone.utc).isoformat()
                    updated += 1
                else:
                    unchanged += 1
            else:
                pkg["discovered_at"] = datetime.now(timezone.utc).isoformat()
                pkg["last_seen"] = datetime.now(timezone.utc).isoformat()
                packages[pid] = pkg
                added += 1

        # 清理本次未扫描到的过期条目（可选，由 --prune 控制）
        if getattr(self, "prune", False):
            found_names = {f["name"] for f in found}
            stale = [pid for pid in packages if pid not in found_names]
            for pid in stale:
                del packages[pid]

        queue["last_scan_at"] = datetime.now(timezone.utc).isoformat()
        queue["total_packages"] = len(packages)
        queue["pending_count"] = sum(1 for p in packages.values() if p.get("status") == "pending")
        queue["updated_count"] = sum(1 for p in packages.values() if p.get("status") == "updated")
        queue["integrated_count"] = sum(1 for p in packages.values() if p.get("status") == "integrated")
        self.save_queue(queue)
        return added, updated, unchanged

    def generate_report(self, found: List[Dict], added: int, updated: int, unchanged: int):
        """生成 Markdown 报告。"""
        queue = self.load_queue()
        now = datetime.now(timezone.utc).isoformat()

        lines = [
            "# 龍魂体系 · 待融入包监控报告",
            "",
            f"**DNA**:#龍芯⚡️丙午·甲午·辛酉·甲午·䷨损-PACKAGE-WATCHER-v1.0  ",
            f"**扫描时间**: {now}  ",
            "**责任**: UID9622·不免责",
            "",
            "---",
            "",
            "## 扫描摘要",
            "",
            f"| 指标 | 数值 |",
            f"|------|------|",
            f"| 监控路径 | {', '.join(str(d) for d in self.watch_dirs)} |",
            f"| 本次发现包 | {len(found)} |",
            f"| 新增 | {added} |",
            f"| 更新 | {updated} |",
            f"| 未变更 | {unchanged} |",
            f"| 队列总数 | {queue.get('total_packages', 0)} |",
            f"| 待融入 | {queue.get('pending_count', 0)} |",
            f"| 已更新待审 | {queue.get('updated_count', 0)} |",
            f"| 已融入 | {queue.get('integrated_count', 0)} | ",
            "",
            "---",
            "",
            "## 分类统计",
            "",
            "| 分类 | 数量 | 优先级 | 建议目标 |",
            "|------|------|--------|---------|",
        ]

        # Category summary
        cats: Dict[str, List[Dict]] = {}
        for pkg in found:
            cats.setdefault(pkg["category"], []).append(pkg)
        for cat in sorted(cats.keys()):
            pkgs = cats[cat]
            pri = pkgs[0]["priority"]
            tgt = pkgs[0]["suggested_target"]
            lines.append(f"| {cat} | {len(pkgs)} | {pri} | {tgt} |")

        lines.extend([
            "",
            "---",
            "",
            "## 待融入队列详情",
            "",
            "| 包名 | 类型 | 分类 | 优先级 | 大小 | 状态 | 建议目标 |",
            "|------|------|------|--------|------|------|---------|",
        ])

        for pkg in sorted(found, key=lambda x: (x["priority"], x["category"], x["name"])):
            status_icon = "🟡"
            if pkg["status"] == "pending":
                status_icon = "🟡"
            elif pkg["status"] == "updated":
                status_icon = "🟠"
            lines.append(
                f"| {pkg['name']} | {pkg['type']} | {pkg['category']} | "
                f"{pkg['priority']} | {pkg['size_human']} | {status_icon} {pkg['status']} | {pkg['suggested_target']} |"
            )

        lines.extend([
            "",
            "---",
            "",
            "## 自动化命令",
            "",
            "```bash",
            "# 查看队列",
            "jq '.packages' docs/package-integration-queue.json",
            "",
            "# 列出 P0 待融入包",
            'jq \'.packages | to_entries[] | select(.value.priority == "P0") | .value.name\' docs/package-integration-queue.json',
            "",
            "# 运行监控器（容器内）",
            "python3 /app/package-watcher.py",
            "```",
            "",
            "---",
            "",
            "> 🐉 龍魂永世，文化传承，数字主权，科技自主创新不可让渡！",
        ])

        self.report_file.write_text("\n".join(lines), encoding="utf-8")

    def log(self, message: str):
        """记录日志。"""
        ts = datetime.now(timezone.utc).isoformat()
        line = f"[{ts}] {message}"
        print(line)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    @staticmethod
    def _human_size(size_bytes: int) -> str:
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"

    def run(self):
        """主运行入口。"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log("🐉 龍魂待融入包监控器启动")

        found = self.scan()
        added, updated, unchanged = self.update_queue(found)
        self.generate_report(found, added, updated, unchanged)

        self.log(f"✅ 扫描完成：新增 {added}，更新 {updated}，未变更 {unchanged}，队列总数 {added+updated+unchanged}")
        self.log(f"📄 报告：{self.report_file}")
        self.log(f"📋 队列：{self.queue_file}")


# ═══════════════════════════════════════════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="龍魂待融入包自动收集与分类器")
    parser.add_argument(
        "--watch-dir",
        action="append",
        type=Path,
        help="监控路径（可多次指定，默认 ~/Downloads 与 ~）",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs"),
        help="输出目录（默认 docs/）",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="仅运行一次（默认）",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="循环监控间隔秒数（默认 300）",
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="清理本次未扫描到的过期队列条目",
    )
    args = parser.parse_args()

    watch_dirs = args.watch_dir or [Path.home() / "Downloads", Path.home()]
    watcher = PackageWatcher(watch_dirs, args.output_dir)
    watcher.prune = args.prune

    while True:
        watcher.run()
        if args.once:
            break
        time.sleep(args.interval)


if __name__ == "__main__":
    main()

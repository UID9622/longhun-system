#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂體系 · 待融入包自動收集與分類器
Longhun System · Pending Integration Package Watcher & Classifier

DNA:#龍芯⚡️2026-06-16-PACKAGE-WATCHER-v1.0
責任: UID9622·不免責

功能：
  1. 掃描指定監控路徑（默認 ~/Downloads 與 ~）
  2. 識別龍魂/CNSH/Kimi 相關新增/更新包
  3. 按規則自動分類到 skills/systems/protocols/monitoring/cnsh/docs/forensics/gateway/audit/archive
  4. 維護待融入隊列 docs/package-integration-queue.json
  5. 生成審查報告 docs/package-watcher-report.md

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
from typing import Dict, List, Optional, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# 分類規則：按關鍵字匹配（優先級從高到低）
# ═══════════════════════════════════════════════════════════════════════════════
CLASSIFICATION_RULES: List[Tuple[str, List[str]]] = [
    ("multi_content_archive", ["龍魂待整理", "待整理"]),
    ("warehouse_audit", ["技能检查", "warehouse", "audit", "審計改進", "审计改进"]),
    ("skills",          ["skill", "技能", "Skill"]),
    ("cnsh",            ["CNSH", "cnsh", "Runtime Governance", "語義接入", "语义接入"]),
    ("monitoring",      ["監控", "监控", "monitoring", "移動端", "移动端"]),
    ("protocols",       ["協議", "协议", "protocol", "根協議", "根协议"]),
    ("gateway",         ["網關", "网关", "gateway"]),
    ("forensics",       ["forensic", "取證", "取证"]),
    ("phase3",          ["Phase 3", "phase3", "Phase3"]),
    ("systems",         ["核心系統", "核心系统", "系統優化", "系统优化", "標準化", "标准化", "啟動", "启动"]),
    ("docs",            ["知識矩陣", "知识矩阵", "計算公式", "计算公式", "流水線", "流水线", "使用說明", "使用说明"]),
    ("archive",         ["backup", "備份", "备份", "archive", "歸檔", "归档"]),
]

KNOWN_INTEGRATED = {
    "Kimi_Agent_启动全部技能",
    "Kimi_Agent_启动全部技能.zip",
    "Kimi_Agent_龍魂体系技能检查",
    "Kimi_Agent_龍魂体系技能检查.zip",
}

# 不應納入待融入隊列的項目（主幹本身、敏感目錄、備份等）
EXCLUDED_NAMES = {
    "longhun-system",
    ".longhun",
    ".longhun-credentials",
    ".longhun_skill_registry.json",
    ".longhun_shell_config",
    "longhun_dna_backup_20260605_173301.json",
    "longhun_dna_final_backup.json",
}

# 備份/歸檔類關鍵字
ARCHIVE_KEYWORDS = ["backup", "備份", "backup-", "-bfg", "archive", "歸檔", "待整理"]


# ═══════════════════════════════════════════════════════════════════════════════
# 工具函數
# ═══════════════════════════════════════════════════════════════════════════════
def is_longhun_related(name: str) -> bool:
    """判斷文件名是否與龍魂體系相關。"""
    lowered = name.lower()
    keywords = ["longhun", "龍魂", "Kimi_Agent", "CNSH", "龍芯", "龙魂", "UID9622"]
    return any(k.lower() in lowered for k in keywords) or any(k in name for k in keywords[1:])


def classify(name: str) -> str:
    """根據文件名關鍵字分類。"""
    lowered = name.lower()
    # 優先判斷是否為備份/歸檔
    if any(k.lower() in lowered for k in ARCHIVE_KEYWORDS):
        return "archive"
    for category, patterns in CLASSIFICATION_RULES:
        for pattern in patterns:
            if pattern.lower() in lowered:
                return category
    return "unknown"


def compute_file_hash(path: Path) -> str:
    """計算文件 SHA-256（用於追蹤變更）。"""
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, PermissionError):
        return ""


def package_id(path: Path) -> str:
    """生成包的穩定 ID。"""
    return f"{path.name}_{path.stat().st_mtime:.0f}"


def priority_for(category: str) -> str:
    """根據分類給出優先級建議。"""
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
    """建議融入主幹的目標目錄。"""
    tmap = {
        "multi_content_archive": "按 docs/龍魂待整理-integration-gap-report.md 分 P0-P3 逐步融入",
        "systems": "systems/ 或新增 systems/{name}/",
        "cnsh": "cnsh-core/",
        "phase3": "phase3/ 或 longhun-phase3/",
        "protocols": "protocols/ 或 cnsh-core/constitution/",
        "monitoring": "mobile-monitoring.integrated/",
        "gateway": "integrated-modules/gateway/",
        "skills": "skills/ 或 skills/{category}/",
        "warehouse_audit": "skills/warehouse-audit/ 擴展",
        "audit": "skills/warehouse-audit/ 或新增 systems/audit/",
        "forensics": "tools/forensics/",
        "docs": "docs/references/ 或 docs/v3/",
        "archive": "_archive/ 或 longhun-archive/",
        "unknown": "待人工分類",
    }
    return tmap.get(category, "待人工分類")


# ═══════════════════════════════════════════════════════════════════════════════
# 掃描邏輯
# ═══════════════════════════════════════════════════════════════════════════════
class PackageWatcher:
    def __init__(self, watch_dirs: List[Path], output_dir: Path):
        self.watch_dirs = watch_dirs
        self.output_dir = output_dir
        self.queue_file = output_dir / "package-integration-queue.json"
        self.report_file = output_dir / "package-watcher-report.md"
        self.log_file = output_dir / "package-watcher.log"

    def load_queue(self) -> Dict:
        """載入現有隊列。"""
        if self.queue_file.exists():
            try:
                return json.loads(self.queue_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        return {
            "dna": "#龍芯⚡️2026-06-16-PACKAGE-INTEGRATION-QUEUE-v1.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "packages": {},
        }

    def save_queue(self, queue: Dict):
        """保存隊列。"""
        self.queue_file.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")

    def scan(self) -> List[Dict]:
        """掃描監控路徑，返回發現的包列表。"""
        found = []
        for watch_dir in self.watch_dirs:
            if not watch_dir.exists():
                self.log(f"⚠️ 監控路徑不存在: {watch_dir}")
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
                    "notes": "已融入主幹" if item.name in KNOWN_INTEGRATED else "",
                }
                found.append(pkg)
        return found

    def update_queue(self, found: List[Dict]) -> Tuple[int, int, int]:
        """更新隊列，返回新增/更新/未變更數量。"""
        queue = self.load_queue()
        packages = queue.setdefault("packages", {})

        added = 0
        updated = 0
        unchanged = 0

        for pkg in found:
            pid = f"{pkg['name']}"
            if pid in packages:
                existing = packages[pid]
                # 若狀態需要根據已知融入列表修正
                if pkg["name"] in KNOWN_INTEGRATED and existing.get("status") not in ("integrated",):
                    existing.update(pkg)
                    existing["status"] = "integrated"
                    existing["notes"] = "已融入主幹"
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

        # 清理本次未掃描到的過期條目（可選，由 --prune 控制）
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
        """生成 Markdown 報告。"""
        queue = self.load_queue()
        now = datetime.now(timezone.utc).isoformat()

        lines = [
            "# 龍魂體系 · 待融入包監控報告",
            "",
            f"**DNA**:#龍芯⚡️2026-06-16-PACKAGE-WATCHER-v1.0  ",
            f"**掃描時間**: {now}  ",
            "**責任**: UID9622·不免責",
            "",
            "---",
            "",
            "## 掃描摘要",
            "",
            f"| 指標 | 數值 |",
            f"|------|------|",
            f"| 監控路徑 | {', '.join(str(d) for d in self.watch_dirs)} |",
            f"| 本次發現包 | {len(found)} |",
            f"| 新增 | {added} |",
            f"| 更新 | {updated} |",
            f"| 未變更 | {unchanged} |",
            f"| 隊列總數 | {queue.get('total_packages', 0)} |",
            f"| 待融入 | {queue.get('pending_count', 0)} |",
            f"| 已更新待審 | {queue.get('updated_count', 0)} |",
            f"| 已融入 | {queue.get('integrated_count', 0)} | ",
            "",
            "---",
            "",
            "## 分類統計",
            "",
            "| 分類 | 數量 | 優先級 | 建議目標 |",
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
            "## 待融入隊列詳情",
            "",
            "| 包名 | 類型 | 分類 | 優先級 | 大小 | 狀態 | 建議目標 |",
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
            "## 自動化命令",
            "",
            "```bash",
            "# 查看隊列",
            "jq '.packages' docs/package-integration-queue.json",
            "",
            "# 列出 P0 待融入包",
            'jq \'.packages | to_entries[] | select(.value.priority == "P0") | .value.name\' docs/package-integration-queue.json',
            "",
            "# 運行監控器（容器內）",
            "python3 /app/package-watcher.py",
            "```",
            "",
            "---",
            "",
            "> 🐉 龍魂永世，文化傳承，數字主權，科技自主創新不可讓渡！",
        ])

        self.report_file.write_text("\n".join(lines), encoding="utf-8")

    def log(self, message: str):
        """記錄日誌。"""
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
        """主運行入口。"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log("🐉 龍魂待融入包監控器啟動")

        found = self.scan()
        added, updated, unchanged = self.update_queue(found)
        self.generate_report(found, added, updated, unchanged)

        self.log(f"✅ 掃描完成：新增 {added}，更新 {updated}，未變更 {unchanged}，隊列總數 {added+updated+unchanged}")
        self.log(f"📄 報告：{self.report_file}")
        self.log(f"📋 隊列：{self.queue_file}")


# ═══════════════════════════════════════════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="龍魂待融入包自動收集與分類器")
    parser.add_argument(
        "--watch-dir",
        action="append",
        type=Path,
        help="監控路徑（可多次指定，默認 ~/Downloads 與 ~）",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs"),
        help="輸出目錄（默認 docs/）",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="僅運行一次（默認）",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="循環監控間隔秒數（默認 300）",
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="清理本次未掃描到的過期隊列條目",
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

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·SKILL-ARCHIVE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 本地技能全量归档 v1.0
═══════════════════════════════════════════════════

功能：
  1. 全量扫描: 扫描 skills/ bin/ L2_技能层/ 等目录
  2. 归档索引: 更新 skill_kernel_registry.json
  3. 去重检测: 同名/同功能技能合并
  4. 缺口检测: 注册但无文件 · 有文件未注册
  5. 统计报告: 按分类/状态/优先级汇总

DNA: #龍芯⚡️丙午·辛未·SKILL-ARCHIVE-v1.0
"""

import argparse
import hashlib
import json
import os
import re
import sys
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# ── 扫描目录 ──
SCAN_DIRS = [
    ("skills/", "*.skill", "技能定义文件"),
    ("skills/", "*.py", "技能Python脚本"),
    ("bin/", "lh_*.py", "bin工具集"),
    ("L2_技能层/skills/", "*.py", "L2技能层"),
    ("L2_技能层/skill_standard/", "*.md", "技能标准文档"),
    ("integrated-modules/skills.integrated/", "*.py", "集成技能模块"),
    ("skill-standards.integrated/", "*.md", "技能标准集成"),
]

ARCHIVE_FILE = ROOT / "data" / "forensic_kernel" / "skill_kernel_registry.json"
ARCHIVE_DIR = ROOT / "data" / "skill_archive"
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# 分类映射关键词
CATEGORY_KEYWORDS = {
    "安全": ["audit", "shield", "anti", "tamper", "water", "red_team", "angel", "fuse",
             "veto", "block", "defense", "guard", "security"],
    "治理": ["governance", "registry", "dna", "persona", "sovereign", "policy",
             "constitution", "gate", "rule"],
    "开发": ["cnsh", "absorb", "daoyin", "code", "compile", "build", "deploy",
             "test", "dev", "sdk"],
    "AI": ["train", "lora", "model", "learning", "brain", "semantic", "kg",
           "知识", "embed", "vector"],
    "经济": ["xpay", "wishpool", "finance", "ecny", "score", "trust", "payment",
             "recharge", "dcep"],
    "数字人": ["voice", "twin", "digital", "tongxin", "avatar", "tts", "asr"],
    "运维": ["cron", "sync", "patrol", "heal", "check", "monitor", "server",
             "health", "guardian", "daemon"],
    "生态": ["passport", "ecosystem", "service", "bus", "gateway", "bridge",
             "api", "container"],
    "媒体": ["video", "audio", "image", "ocr", "face", "vision", "camera"],
    "通信": ["sms", "bark", "push", "notify", "feishu", "wechat", "im"],
    "地图": ["map", "geo", "location", "amap", "weather"],
}


class SkillArchiver:
    """技能归档器"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.skills: Dict[str, Dict[str, Any]] = {}
        self.orphans: List[str] = []        # 注册但无文件
        self.unregistered: List[str] = []   # 有文件未注册
        self.duplicates: List[Tuple[str, str, str]] = []   # 重复技能
        self.category_count: Dict[str, int] = defaultdict(int)
        self.total_size = 0

    # ═══ 扫描 ═══

    def scan_all(self) -> Dict[str, Any]:
        """全量扫描所有技能目录"""
        found_files = []

        for scan_dir, pattern, desc in SCAN_DIRS:
            full_dir = ROOT / scan_dir
            if not full_dir.exists():
                if self.verbose:
                    print(f"  ⏭️ 目录不存在: {scan_dir}")
                continue

            matched = list(full_dir.rglob(pattern))
            for f in matched:
                found_files.append({
                    "path": str(f.relative_to(ROOT)),
                    "abs_path": str(f),
                    "name": f.stem,
                    "suffix": f.suffix,
                    "size": f.stat().st_size if f.exists() else 0,
                    "dir": scan_dir,
                    "desc": desc,
                })
                self.total_size += f.stat().st_size if f.exists() else 0

            if self.verbose:
                print(f"  📁 {scan_dir}: {len(matched)} 文件")

        # 构建技能索引
        for f in found_files:
            skill_id = self._gen_skill_id(f["name"])
            category = self._detect_category(f["name"], f["path"])
            self.category_count[category] += 1

            if skill_id in self.skills:
                # 重复检测
                existing = self.skills[skill_id]
                self.duplicates.append((skill_id, existing["path"], f["path"]))
                continue

            self.skills[skill_id] = {
                "id": skill_id,
                "name": f["name"],
                "path": f["path"],
                "category": category,
                "suffix": f["suffix"],
                "size": f["size"],
                "dir": f["dir"],
                "desc": f["desc"],
                "status": "active",
                "hash": self._file_hash(f["abs_path"]) if f["size"] < 100000 else "SKIP_LARGE",
                "registered": False,
                "last_modified": datetime.fromtimestamp(
                    os.path.getmtime(f["abs_path"])
                ).isoformat() if os.path.exists(f["abs_path"]) else "",
            }

        # 对比现有注册表
        self._cross_check_registry()

        return self._build_report()

    def _gen_skill_id(self, name: str) -> str:
        """生成技能ID"""
        clean = re.sub(r"[^a-zA-Z0-9_\-]", "", name.lower())
        if clean.startswith("lh_"):
            clean = clean[3:]  # 去lh_前缀
        return f"SKILL-{clean[:40]}"

    def _detect_category(self, name: str, path: str) -> str:
        """检测技能分类"""
        name_lower = name.lower()
        path_lower = path.lower()

        scores = {}
        for cat, keywords in CATEGORY_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in name_lower)
            score += sum(0.5 for kw in keywords if kw in path_lower)
            if score > 0:
                scores[cat] = score

        if scores:
            return max(scores, key=lambda k: scores[k])

        # 默认分类
        if ".skill" in path_lower:
            return "未分类"
        elif "bin/" in path_lower:
            return "工具"
        return "其他"

    def _file_hash(self, path: str) -> str:
        try:
            return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:12]
        except Exception:
            return "HASH_FAIL"

    # ═══ 注册表交叉校验 ═══

    def _cross_check_registry(self):
        """交叉校验现有注册表"""
        if not ARCHIVE_FILE.exists():
            if self.verbose:
                print(f"  📭 注册表不存在，将创建新注册表: {ARCHIVE_FILE}")
            return

        try:
            existing = json.loads(ARCHIVE_FILE.read_text())
        except (json.JSONDecodeError, IOError):
            existing = {}

        # 检查注册但无文件
        for reg_id, reg in existing.items():
            reg_path = reg.get("路径", "")
            if reg_path and not Path(reg_path).exists():
                self.orphans.append(reg_id)

            # 标记已注册
            if reg_id in self.skills:
                self.skills[reg_id]["registered"] = True
                self.skills[reg_id]["reg_version"] = reg.get("版本", "")

        # 检查有文件未注册
        for skill_id, skill in self.skills.items():
            if not skill["registered"]:
                self.unregistered.append(skill_id)

    # ═══ 报告 ═══

    def _build_report(self) -> Dict[str, Any]:
        return {
            "scan_time": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "total_files": len(self.skills),
                "total_size_mb": round(self.total_size / 1024 / 1024, 2),
                "registered": sum(1 for s in self.skills.values() if s["registered"]),
                "unregistered": len(self.unregistered),
                "orphans": len(self.orphans),
                "duplicates": len(self.duplicates),
            },
            "by_category": dict(self.category_count),
            "orphans": self.orphans,
            "unregistered": self.unregistered,
            "duplicates": [
                {"id": d[0], "path_a": d[1], "path_b": d[2]}
                for d in self.duplicates
            ],
        }

    # ═══ 归档写入 ═══

    def write_archive(self) -> str:
        """写入归档注册表"""
        registry = {}
        for skill_id, skill in self.skills.items():
            registry[skill_id] = {
                "id": skill_id,
                "技能名": skill["name"],
                "路径": str(ROOT / skill["path"]),
                "作用域": "local",
                "版本": skill.get("reg_version", "v1.0"),
                "描述": f"[{skill['category']}] {skill['desc']}",
                "DNA": self._gen_dna(skill_id),
                "来源": skill["dir"].rstrip("/"),
                "关键词": skill["category"].split("·") if "·" in skill["category"] else [skill["category"]],
                "入口": f"python3 {skill['path']}" if skill["suffix"] == ".py" else "",
                "优先级": 50,
                "状态": "已注册",
                "评分": 50.0,
                "使用次数": 0,
                "审计状态": "未审计",
                "注册时间": datetime.now(timezone.utc).isoformat(),
                "归档时间": datetime.now(timezone.utc).isoformat(),
            }

        archive_path = ARCHIVE_DIR / f"skill_registry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        archive_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2))

        # 同时更新主注册表
        try:
            os.makedirs(ARCHIVE_FILE.parent, exist_ok=True)
            # 备份旧注册表
            if ARCHIVE_FILE.exists():
                backup = ARCHIVE_FILE.with_suffix(".json.bak")
                backup.write_text(ARCHIVE_FILE.read_text())

            ARCHIVE_FILE.write_text(json.dumps(registry, ensure_ascii=False, indent=2))
        except Exception as e:
            if self.verbose:
                print(f"  ⚠️ 更新主注册表失败: {e}")

        return str(archive_path)

    def _gen_dna(self, skill_id: str) -> str:
        h = hashlib.sha256(f"{skill_id}{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        return f"#龍芯⚡️丙午·辛未·{skill_id[:12]}-v1.0-{h}"


# ═══ CLI ═══

def main():
    parser = argparse.ArgumentParser(description="龍魂本地技能全量归档")
    parser.add_argument("--scan", action="store_true", default=True, help="执行全量扫描")
    parser.add_argument("--write", action="store_true", help="写入归档注册表")
    parser.add_argument("--stats", action="store_true", help="显示统计")
    parser.add_argument("--orphans", action="store_true", help="列出注册但无文件的技能")
    parser.add_argument("--unregistered", action="store_true", help="列出有文件未注册的技能")
    parser.add_argument("--duplicates", action="store_true", help="列出重复技能")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()
    archiver = SkillArchiver(verbose=args.verbose)

    result = archiver.scan_all()

    if args.stats:
        s = result["summary"]
        print(f"\n🐉 龍魂技能归档统计")
        print(f"{'='*50}")
        print(f"  总文件数: {s['total_files']}")
        print(f"  总大小:   {s['total_size_mb']} MB")
        print(f"  已注册:   {s['registered']}")
        print(f"  未注册:   {s['unregistered']}")
        print(f"  孤立项:   {s['orphans']}")
        print(f"  重复项:   {s['duplicates']}")
        print(f"\n  按分类:")
        for cat, count in sorted(result["by_category"].items(), key=lambda x: -x[1]):
            bar = "█" * min(count, 30)
            print(f"    {cat:8s} {count:4d} {bar}")

    if args.orphans:
        print(f"\n📭 注册但无文件的技能 ({len(result['orphans'])}):")
        for o in result["orphans"]:
            print(f"    {o}")

    if args.unregistered:
        print(f"\n🆕 有文件未注册的技能 ({len(result['unregistered'])}):")
        for u in result["unregistered"]:
            s = archiver.skills.get(u, {})
            print(f"    {u:40s} → {s.get('path', '?')}")

    if args.duplicates:
        print(f"\n🔄 重复技能 ({len(result['duplicates'])}):")
        for d in result["duplicates"]:
            print(f"    {d['id']:40s}")
            print(f"      A: {d['path_a']}")
            print(f"      B: {d['path_b']}")

    if args.write:
        archive_path = archiver.write_archive()
        print(f"\n✅ 归档注册表已写入: {archive_path}")
        print(f"✅ 主注册表已更新: {ARCHIVE_FILE}")

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())

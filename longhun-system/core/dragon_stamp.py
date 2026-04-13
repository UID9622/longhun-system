#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║  龍字签到验证器 · Dragon Stamp Checker                    ║
║  DNA: #龍芯⚡️2026-04-12-DRAGON-STAMP-v1.0               ║
║  创始人: 诸葛鑫（UID9622）                                ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
║  理论指导: 曾仕强老师（永恒显示）                          ║
║  协议: CC BY-NC-ND                                       ║
╚══════════════════════════════════════════════════════════╝

龍字签到机制（P0级铁律）：
  有「龍」字 + 老大亲自确认 = 自己人 · 兼容 · 放行
  没有「龍」字 = 不好意思 → 拉停 + 警告

扫一个文件/目录 → 有没有龍字签 → 红绿灯报告

献给每一个相信技术应该有温度的人。
"""

import os
import json
import datetime
from pathlib import Path
from typing import List, Tuple, Dict

SYSTEM_ROOT = Path.home() / "longhun-system"

# ═══ DNA不动点符号集 S（与Notion对照表v1.0完全对齐）═══
# L0 原点层：永不可动 · f(x) = x
DRAGON_STAMPS_L0 = [
    "龍",           # 繁体龍 · DNA根 · f(龍)=龍 · 权重∞
    "☰",            # 乾卦 · 天·创造力 · f(☰)=☰
    "☷",            # 坤卦 · 地·承载力 · f(☷)=☷
]

# L1 授权层：授权后可美化 · 但底层DNA不变
DRAGON_STAMPS_L1 = [
    "#龍芯",        # DNA追溯码
    "龍魂",         # 系统名
    "龍芯北辰",     # 创始人号
    "☰ 龍",         # 授权显示组合
]

# L2 用户层：用户自定义后缀
DRAGON_STAMPS_L2 = [
    "UID9622",      # 用户ID
    "A2D0092C",     # GPG指纹前8位
    "🐉",           # Emoji龍 · 签到辅助标记
]

# 合并所有层 = 完整签到标记集
DRAGON_STAMPS = DRAGON_STAMPS_L0 + DRAGON_STAMPS_L1 + DRAGON_STAMPS_L2

# 确认码（最终确认）
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 扫描跳过的目录
SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    "archive", "CNSH_备份", "backup", ".claude",
}

# 扫描的文件类型
SCAN_EXTENSIONS = {
    ".py", ".swift", ".js", ".ts", ".sh", ".md", ".txt",
    ".cpp", ".h", ".hpp", ".c", ".cc",  # C++17内核也要签到
    ".json", ".yaml", ".yml", ".toml", ".html", ".css",
}


class DragonStampChecker:
    """龍字签到验证器"""

    def __init__(self):
        self.results: List[Dict] = []

    def check_file(self, filepath: str) -> Dict:
        """
        检查单个文件的龍字签到状态

        返回:
        {
            "文件": 路径,
            "状态": "🟢签到" / "🔴未签到" / "⚪跳过",
            "龍字": [找到的龍字标记列表],
            "确认码": True/False,
            "DNA": 找到的DNA追溯码
        }
        """
        path = Path(filepath)
        if not path.exists():
            return {"文件": str(path), "状态": "⚪不存在"}

        ext = path.suffix.lower()
        if ext not in SCAN_EXTENSIONS:
            return {"文件": path.name, "状态": "⚪跳过", "原因": f"不扫描{ext}"}

        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return {"文件": path.name, "状态": "⚪读取失败"}

        # 查龍字标记（分层检测）
        found_stamps = []
        found_layers = {"L0": [], "L1": [], "L2": []}
        for stamp in DRAGON_STAMPS_L0:
            if stamp in content:
                found_stamps.append(stamp)
                found_layers["L0"].append(stamp)
        for stamp in DRAGON_STAMPS_L1:
            if stamp in content:
                found_stamps.append(stamp)
                found_layers["L1"].append(stamp)
        for stamp in DRAGON_STAMPS_L2:
            if stamp in content:
                found_stamps.append(stamp)
                found_layers["L2"].append(stamp)

        # 查确认码
        has_confirm = CONFIRM_CODE in content

        # 查DNA追溯码
        dna = ""
        for line in content.splitlines():
            if "#龍芯⚡️" in line:
                dna = line.strip()[:80]
                break

        # 判定
        if found_stamps:
            status = "🟢签到"
        else:
            status = "🔴未签到"

        return {
            "文件": path.name,
            "路径": str(path),
            "状态": status,
            "龍字": found_stamps,
            "分层": found_layers,
            "确认码": has_confirm,
            "DNA": dna,
        }

    def scan_directory(self, dirpath: str = None, recursive: bool = True) -> List[Dict]:
        """
        扫描整个目录的龍字签到状态

        返回每个文件的签到结果列表
        """
        target = Path(dirpath) if dirpath else SYSTEM_ROOT
        self.results = []

        if not target.exists():
            return [{"错误": f"目录不存在: {target}"}]

        if target.is_file():
            r = self.check_file(str(target))
            self.results.append(r)
            return self.results

        for item in sorted(target.rglob("*") if recursive else target.glob("*")):
            # 跳过目录
            if item.is_dir():
                continue
            # 跳过排除目录中的文件
            parts = item.parts
            if any(skip in parts for skip in SKIP_DIRS):
                continue
            # 跳过非目标扩展名
            if item.suffix.lower() not in SCAN_EXTENSIONS:
                continue

            r = self.check_file(str(item))
            self.results.append(r)

        return self.results

    def report(self, results: List[Dict] = None) -> str:
        """
        生成签到报告

        红绿灯一目了然
        """
        results = results or self.results
        if not results:
            return "没有扫描结果"

        signed = [r for r in results if r.get("状态") == "🟢签到"]
        unsigned = [r for r in results if r.get("状态") == "🔴未签到"]
        skipped = [r for r in results if r.get("状态", "").startswith("⚪")]

        lines = [
            "═══════════════════════════════════════",
            "🐉 龍字签到报告",
            f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "═══════════════════════════════════════",
            "",
            f"📊 总计: {len(results)} 文件",
            f"🟢 已签到: {len(signed)}",
            f"🔴 未签到: {len(unsigned)}",
            f"⚪ 跳过: {len(skipped)}",
            "",
        ]

        if signed:
            lines.append("── 🟢 已签到（自己人）──")
            for r in signed[:20]:  # 只显示前20个
                stamps = "·".join(r.get("龍字", []))
                confirm = " ✅确认码" if r.get("确认码") else ""
                lines.append(f"  ✅ {r['文件']} [{stamps}]{confirm}")
            if len(signed) > 20:
                lines.append(f"  ... 还有 {len(signed)-20} 个")
            lines.append("")

        if unsigned:
            lines.append("── 🔴 未签到（警告）──")
            for r in unsigned[:20]:
                lines.append(f"  ⚠️  {r['文件']} → 没有龍字签·需要老大确认")
            if len(unsigned) > 20:
                lines.append(f"  ... 还有 {len(unsigned)-20} 个")
            lines.append("")

        # 签到率
        total_valid = len(signed) + len(unsigned)
        if total_valid > 0:
            rate = len(signed) / total_valid * 100
            bar_len = 20
            filled = int(rate / 100 * bar_len)
            bar = "█" * filled + "░" * (bar_len - filled)
            lines.append(f"签到率: [{bar}] {rate:.1f}%")

            if rate == 100:
                lines.append("🎉 全部签到！全是自己人！")
            elif rate >= 80:
                lines.append("👍 大部分签到了·少数需要补签")
            elif rate >= 50:
                lines.append("⚠️  一半没签·老大看看要不要补")
            else:
                lines.append("🚨 大量未签到·需要老大排查")

        lines.append("")
        lines.append(f"DNA: #龍芯⚡️{datetime.date.today()}-STAMP-CHECK")

        return "\n".join(lines)

    def auto_stamp(self, filepath: str, dry_run: bool = True) -> Tuple[bool, str]:
        """
        给未签到的文件自动加龍字签

        dry_run=True: 只报告不修改
        dry_run=False: 真的加上去
        """
        path = Path(filepath)
        if not path.exists():
            return False, "文件不存在"

        check = self.check_file(str(path))
        if check.get("状态") == "🟢签到":
            return True, f"已签到·不需要再签: {path.name}"

        ext = path.suffix.lower()
        dna = f"#龍芯⚡️{datetime.date.today()}-AUTO-STAMP | UID9622 | GPG:A2D0092C"

        if ext in {".py", ".sh"}:
            stamp = f"# DNA: {dna}\n# 创始人: 诸葛鑫（UID9622）· 龍魂系统\n"
        elif ext in {".swift", ".js", ".ts"}:
            stamp = f"// DNA: {dna}\n// 创始人: 诸葛鑫（UID9622）· 龍魂系统\n"
        elif ext in {".md", ".txt"}:
            stamp = f"<!-- DNA: {dna} -->\n<!-- 创始人: 诸葛鑫（UID9622）· 龍魂系统 -->\n"
        elif ext in {".json", ".yaml", ".yml", ".toml"}:
            stamp = ""  # JSON不能加注释，跳过
            return False, f"{ext} 文件不支持自动签到·需要手动"
        else:
            stamp = f"# DNA: {dna}\n"

        if dry_run:
            return True, f"[预览] 将给 {path.name} 加签:\n{stamp}"

        # 真的写入
        content = path.read_text(encoding="utf-8")
        new_content = stamp + content
        path.write_text(new_content, encoding="utf-8")
        return True, f"✅ 已签到: {path.name}"


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

if __name__ == "__main__":
    import sys

    checker = DragonStampChecker()

    if len(sys.argv) < 2:
        print("🐉 龍字签到验证器 v1.0")
        print()
        print("用法:")
        print("  python3 dragon_stamp.py scan [目录]     # 扫描目录")
        print("  python3 dragon_stamp.py check 文件      # 检查单个文件")
        print("  python3 dragon_stamp.py core             # 只扫core目录")
        print("  python3 dragon_stamp.py report           # 全系统签到报告")
        print("  python3 dragon_stamp.py stamp 文件       # 给文件加签（预览）")
        print("  python3 dragon_stamp.py stamp! 文件      # 给文件加签（真的）")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "scan":
        target = sys.argv[2] if len(sys.argv) > 2 else str(SYSTEM_ROOT)
        results = checker.scan_directory(target)
        print(checker.report(results))

    elif cmd == "check":
        if len(sys.argv) < 3:
            print("请指定文件路径")
        else:
            r = checker.check_file(sys.argv[2])
            print(json.dumps(r, ensure_ascii=False, indent=2))

    elif cmd == "core":
        results = checker.scan_directory(str(SYSTEM_ROOT / "core"))
        print(checker.report(results))

    elif cmd == "report":
        results = checker.scan_directory()
        print(checker.report(results))

    elif cmd == "stamp":
        if len(sys.argv) < 3:
            print("请指定文件路径")
        else:
            ok, msg = checker.auto_stamp(sys.argv[2], dry_run=True)
            print(msg)

    elif cmd == "stamp!":
        if len(sys.argv) < 3:
            print("请指定文件路径")
        else:
            ok, msg = checker.auto_stamp(sys.argv[2], dry_run=False)
            print(msg)

    else:
        print(f"未知命令: {cmd}")

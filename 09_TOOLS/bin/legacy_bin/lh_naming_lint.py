#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂系统 · 命名与字符自动校验器 v1.0
作者：诸葛鑫（UID9622）
DNA: #龍芯⚡️2026-07-21-NAMING-LINT-V1.0
关联: 01_protocols/LH-NAMING-SYMBOL-MASTER-v1.0.md
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

用途：任何文件入库前过本校验器，不合格不入库。
对接：外脑日档心跳（lh_exobrain_engine.py）→ 入库钩子自动调用本脚本。
"""

import re
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime, timezone

# ============================================================
# 注册表（按总表附录A程序维护，禁止私下修改）
# ============================================================

# --- 第二章：品牌禁词简体 ---
品牌禁词简体 = ["龙魂", "龙芯"]

# --- 第九章：禁词文件名 ---
禁词文件名 = ["最终版", "最新版", "final", "Final", "FINAL", "temp", "tmp", "draft", "草稿"]

# --- 第十三章：一票否决词 ---
一票否决词 = [
    "技术无国界", "用户体验优先", "灵活处理", "国际接轨",
    "简化管理", "商业化需要", "平衡各方", "行业标准"
]

# --- 第七章：已注册短码 ---
已注册短码 = [
    "/全文压缩", "/旧文回收", "/归集", "/DNA封装", "/投喂净化",
    "/系统入库", "/封存归档", "/召回", "/时间胶囊", "/外脑体检", "/寻根"
]

# --- 第三章：DNA格式正则 ---
DNA标准 = re.compile(
    r"^#龍芯⚡️\d{4}-\d{2}-\d{2}-[A-Z0-9][A-Z0-9-]*-V\d+\.\d+(-P0\+{0,2})?$"
)
DNA血缘 = re.compile(r"^#龍芯⚡️SEQ\d{6}-[0-9a-f]{32}$")
DNA事件 = re.compile(
    r"^#龍芯⚡️\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z-SEQ\d{6}-[A-Z]+-[0-9a-f]{32}$"
)

# --- 第十四章：保留符号（不可替换） ---
保留符号 = {"⚡️", "🌌", "🧬"}


# ============================================================
# 核心校验类
# ============================================================

class CNSH_龍魂命名校验器:
    """
    入库必过：不合格不入库。
    DNA: #龍芯⚡️2026-07-21-NAMING-LINT-V1.0
    """

    DNA = "#龍芯⚡️2026-07-21-NAMING-LINT-V1.0"
    VERSION = "1.0"

    def __init__(self):
        self.results = []

    def 校验文件名(self, 名: str) -> dict[str, Any]:
        """校验文件名是否合规（第九章）"""
        问题 = []

        # N1: 品牌繁体
        if any(w in 名 for w in 品牌禁词简体):
            问题.append({"级别": "🔴", "规则": "N1",
                        "描述": f"品牌必须繁体「龍」，文件名中出现简体'{next(w for w in 品牌禁词简体 if w in 名)}'"})

        # 禁词
        hit = [w for w in 禁词文件名 if w in 名]
        if hit:
            问题.append({"级别": "🔴", "规则": "9.2",
                        "描述": f"禁词：不许叫'最终版/最新版/final'，命中: {hit}"})

        # 日期格式
        if re.search(r"\d{8}", 名):
            问题.append({"级别": "🟡", "规则": "9.2",
                        "描述": "日期应ISO格式 2026-07-21，非8位连写"})

        # 空格
        if " " in 名:
            问题.append({"级别": "🟡", "规则": "9.2",
                        "描述": "文件名避免空格"})

        # 缺版本号
        if not re.search(r"v\d+\.\d+", 名) and 名.endswith((".md", ".py", ".html", ".json", ".toml")):
            问题.append({"级别": "🟡", "规则": "9.2",
                        "描述": "缺版本号（如v1.0）"})

        合格 = not any(q["级别"] == "🔴" for q in 问题)
        result = {"目标": 名, "类型": "文件名", "合格": 合格, "问题": 问题, "dna": self.DNA}
        self.results.append(result)
        return result

    def 校验DNA码(self, 码: str) -> dict[str, Any]:
        """校验DNA追溯码是否合规（第三章）"""
        问题 = []

        if "龙芯" in 码:
            问题.append({"级别": "🔴", "规则": "N1",
                        "描述": "DNA码必须繁体 #龍芯⚡️，非 #龙芯⚡️"})

        if DNA标准.match(码):
            fmt = "标准格式"
        elif DNA血缘.match(码):
            fmt = "血缘SEQ格式"
        elif DNA事件.match(码):
            fmt = "事件格式"
        else:
            问题.append({"级别": "🔴", "规则": "3",
                        "描述": "不符合DNA格式矩阵（第三章），查四种模板"})
            fmt = "无效"

        合格 = not any(q["级别"] == "🔴" for q in 问题)
        result = {"目标": 码, "类型": "DNA码", "合格": 合格, "格式": fmt, "问题": 问题, "dna": self.DNA}
        self.results.append(result)
        return result

    def 校验短码(self, 码: str) -> dict[str, Any]:
        """校验短码是否已注册（第七章）"""
        合格 = 码 in 已注册短码
        问题 = [] if 合格 else [
            {"级别": "🔴", "规则": "7",
             "描述": f"未注册短码 '{码}'，走第七章注册流程：提出→查重→P08审名→登记入表"}
        ]
        result = {"目标": 码, "类型": "短码", "合格": 合格, "问题": 问题, "dna": self.DNA}
        self.results.append(result)
        return result

    def 扫描文本(self, 文本: str, 来源: str = "") -> dict[str, Any]:
        """扫描文本中的一票否决词和品牌简体"""
        否决命中 = [w for w in 一票否决词 if w in 文本]
        简体命中 = [w for w in 品牌禁词简体 if w in 文本]

        问题 = []
        if 否决命中:
            问题.append({"级别": "🔴", "规则": "13",
                        "描述": f"一票否决词命中: {否决命中}，AI/文档输出严禁使用"})
        if 简体命中:
            问题.append({"级别": "🔴", "规则": "N1",
                        "描述": f"品牌简体命中: {简体命中}，必须改为繁体「龍」"})

        合格 = not 问题
        result = {
            "目标": 来源 or "文本扫描", "类型": "文本",
            "合格": 合格,
            "否决词命中": 否决命中,
            "品牌简体": 简体命中,
            "问题": 问题,
            "dna": self.DNA
        }
        self.results.append(result)
        return result

    def 校验文件头(self, content: str, filename: str = "") -> dict[str, Any]:
        """检查文件是否包含必需的三行头（第六层6.1）"""
        问题 = []
        if "DNA:" not in content and "#龍芯⚡️" not in content:
            问题.append({"级别": "🔴", "规则": "6.1", "描述": "缺少DNA追溯码行"})
        if "创建者:" not in content and "UID9622" not in content:
            问题.append({"级别": "🟡", "规则": "6.1", "描述": "缺少创建者声明"})
        if "CC BY-NC-SA" not in content and "协议:" not in content:
            问题.append({"级别": "🟡", "规则": "6.1", "描述": "缺少协议声明"})

        合格 = not any(q["级别"] == "🔴" for q in 问题)
        result = {
            "目标": filename or "文件头", "类型": "文件头",
            "合格": 合格, "问题": 问题, "dna": self.DNA
        }
        self.results.append(result)
        return result

    def 扫描目录(self, 目录路径: str, 文件模式: str = "*.md") -> dict[str, Any]:
        """扫描目录下所有文件，返回汇总报告（对接外脑日档心跳 N6）
        对每个文件执行：文件名校验 + 文件头校验 + 文本扫描"""
        import glob as _glob
        p = Path(目录路径)
        if not p.exists():
            return {"合格": False, "问题": [{"级别": "🔴", "规则": "N6", "描述": f"目录不存在: {目录路径}"}], "dna": self.DNA}
        
        files = sorted(p.rglob(文件模式))
        for fp in files:
            if fp.is_dir():
                continue
            try:
                rel = str(fp.relative_to(p))
            except ValueError:
                rel = fp.name
            self.校验文件名(fp.name)
            try:
                content = fp.read_text(encoding="utf-8")
                self.校验文件头(content[:500], rel)
                self.扫描文本(content[:5000], rel)
            except Exception as e:
                self.results.append({
                    "目标": rel, "类型": "文件扫描",
                    "合格": False,
                    "问题": [{"级别": "🟡", "规则": "N6", "描述": f"读取失败: {e}"}],
                    "dna": self.DNA
                })
        
        return self.报告()

    def 校验单文件全量(self, 文件路径: str) -> dict[str, Any]:
        """对单个文件执行全量校验：文件名+文件头+文本扫描（对接外脑入库钩子）"""
        p = Path(文件路径)
        if not p.exists() or not p.is_file():
            return {"合格": False, "问题": [{"级别": "🔴", "规则": "N6", 
                      "描述": f"文件不存在: {文件路径}"}], "dna": self.DNA}
        
        self.校验文件名(p.name)
        try:
            content = p.read_text(encoding="utf-8")
            self.校验文件头(content[:500], p.name)
            self.扫描文本(content[:5000], p.name)
        except Exception as e:
            self.results.append({
                "目标": p.name, "类型": "文件校验",
                "合格": False,
                "问题": [{"级别": "🔴", "规则": "N6", "描述": f"读取失败: {e}"}],
                "dna": self.DNA
            })
        
        return self.报告()

    def 报告(self) -> dict[str, Any]:
        """生成汇总报告"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r["合格"])
        failed = total - passed
        critical = sum(
            1 for r in self.results
            for q in r.get("问题", [])
            if q.get("级别") == "🔴"
        )
        return {
            "校验器版本": self.VERSION,
            "DNA": self.DNA,
            "时间": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "总计": total,
            "通过": passed,
            "未通过": failed,
            "🔴严重": critical,
            "三色": "🟢" if failed == 0 else ("🟡" if critical == 0 else "🔴"),
            "详情": self.results
        }


# ============================================================
# 模块级便捷函数（供外脑引擎 import 调用）
# ============================================================

def 外脑入库校验(文件路径: str) -> dict[str, Any]:
    """外脑入库钩子：单文件全量校验，不合格不入库"""
    checker = CNSH_龍魂命名校验器()
    return checker.校验单文件全量(文件路径)


def 外脑日档扫描(目录路径: str) -> dict[str, Any]:
    """外脑日档心跳 N6：扫描目录命名合规"""
    checker = CNSH_龍魂命名校验器()
    return checker.扫描目录(目录路径)


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="龍魂系统 · 命名与字符自动校验器 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_naming_lint.py --file 01_protocols/某协议.md
  python3 bin/lh_naming_lint.py --dna "#龍芯⚡️2026-07-21-TEST-V1.0"
  python3 bin/lh_naming_lint.py --text "这是一段文本，检查有没有技术无国界"
  python3 bin/lh_naming_lint.py --short "/全文压缩"
  python3 bin/lh_naming_lint.py --json  # JSON输出
        """
    )
    parser.add_argument("--file", "-f", help="校验文件名")
    parser.add_argument("--dna", "-d", help="校验DNA码")
    parser.add_argument("--text", "-t", help="扫描文本中的否决词和品牌简体")
    parser.add_argument("--short", "-s", help="校验短码是否注册")
    parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出")
    parser.add_argument("--scan-dir", type=str, default=None,
                        help="扫描目录：对接外脑日档心跳 N6（如 01_protocols/）")
    parser.add_argument("--check", type=str, default=None,
                        help="单文件全量校验：对接外脑入库钩子（文件名+文件头+文本扫描）")
    args = parser.parse_args()

    checker = CNSH_龍魂命名校验器()

    if args.scan_dir:
        report = checker.扫描目录(args.scan_dir)
    elif args.check:
        report = checker.校验单文件全量(args.check)
    else:
        if args.file:
            checker.校验文件名(Path(args.file).name)
            # 如果文件存在，也检查文件头
            p = Path(args.file)
            if p.exists() and p.is_file():
                try:
                    content = p.read_text(encoding="utf-8")
                    # 只读前500字符看文件头
                    checker.校验文件头(content[:500], p.name)
                    # 扫全文的否决词
                    checker.扫描文本(content[:5000], p.name)
                except Exception as e:
                    pass

        if args.dna:
            checker.校验DNA码(args.dna)

        if args.text:
            checker.扫描文本(args.text)

        if args.short:
            checker.校验短码(args.short)

    # 如果没给任何参数，显示帮助
    used_args = [args.file, args.dna, args.text, args.short, args.scan_dir, args.check]
    if not any(used_args):
        parser.print_help()
        return 0

    report = checker.报告()

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"  龍魂命名校验器 v{checker.VERSION}")
        print(f"  DNA: {checker.DNA}")
        print(f"{'='*60}")
        print(f"  总计: {report['总计']} | 通过: {report['通过']} | 未通过: {report['未通过']}")
        print(f"  🔴严重: {report['🔴严重']} | 三色: {report['三色']}")
        print(f"{'='*60}\n")

        for r in report["详情"]:
            status = "✅ 通过" if r["合格"] else "❌ 未通过"
            print(f"  [{r['类型']}] {r['目标']} → {status}")
            for q in r.get("问题", []):
                print(f"    {q['级别']} [{q['规则']}] {q['描述']}")
            print()

    # 返回码：0=全通过，1=有黄色，2=有红色
    if report["🔴严重"] > 0:
        return 2
    elif report["未通过"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

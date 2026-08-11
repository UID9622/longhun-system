#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·庚戌·巳时·需-DEBEN-AUDIT-EXEC-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
lh_deben_audit — 龍魂德本审计执行器 v1.0

执行德本五问，生成审计报告。德本审计在技术审计之前运行，
五问全过才允许进入技术审计流程。

DNA: #龍芯⚡️丙午·乙未·庚戌·巳时·需-DEBEN-AUDIT-EXEC-v1.0

用法:
  python3 bin/lh_deben_audit.py scan          # 执行德本五问
  python3 bin/lh_deben_audit.py scan --quick   # 快速扫描（跳过深度检测）
  python3 bin/lh_deben_audit.py report         # 查看最近审计报告
  python3 bin/lh_deben_audit.py rules          # 显示五条底线
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ============================================================
# 五问检测规则
# ============================================================

# 寒心叙事的敏感词模式（底线3）
COLD_HEART_PATTERNS = [
    (r"好人.*必须穷", "🔴", "好人=穷绑定"),
    (r"奉献.*必须苦", "🔴", "奉献=苦绑定"),
    (r"英雄.*必须死", "🔴", "英雄=死绑定"),
    (r"捐款.*吃泡面", "🟡", "苦情捐款叙事"),
    (r"科学家.*住平房", "🟡", "苦情科学家叙事"),
    (r"环卫工人.*省吃俭用", "🟡", "苦情劳动者叙事"),
    (r"牺牲.*穷人", "🔴", "牺牲绑定穷人"),
    (r"付出.*不能.*正常生活", "🟡", "付出=牺牲正常生活"),
    (r"过得好.*不能.*奉献", "🟡", "过得好≠能奉献"),
]

# 信息茧房关键词（底线4）
INFO_COCOON_PATTERNS = [
    (r"算法推荐", "🟡", "算法推荐机制"),
    (r"个性化推荐", "🟡", "个性化推荐"),
    (r"猜你喜欢", "🟡", "猜你喜欢机制"),
    (r"协同过滤", "🟡", "协同过滤"),
    (r"用户画像", "🟡", "用户画像收集"),
    (r"行为追踪", "🔴", "行为追踪"),
    (r"第三方.*数据", "🔴", "第三方数据共享"),
    (r"平台.*算法", "🟡", "平台算法依赖"),
]

# 技术无德模式（底线1）
TECH_WITHOUT_DE_PATTERNS = [
    (r"大数据杀熟", "🔴", "大数据杀熟"),
    (r"价格歧视", "🔴", "价格歧视"),
    (r"信息不对称.*获利", "🔴", "信息不对称获利"),
    (r"多巴胺.*上瘾", "🔴", "多巴胺上瘾机制"),
    (r"焦虑.*转化", "🔴", "焦虑制造→转化"),
    (r"恐惧.*营销", "🔴", "恐惧营销"),
    (r"为你好.*绑架", "🟡", "\u201c为你好\u201d式绑架"),
]

# 路径散落检测（底线2）
PATH_SCATTER_PATTERNS = [
    (r"~/Downloads/", "🔴", "文件散落在Downloads"),
    (r"~/Desktop/", "🔴", "文件散落在Desktop"),
    (r"/tmp/.*longhun", "🟡", "文件在/tmp"),
]

# 底座变更检测（底线5）
FOUNDATION_PATTERNS = [
    (r"369不动点", "⚓", "369不动点引用"),
    (r"河图洛书", "⚓", "河图洛书引用"),
    (r"技术为人民服务", "⚓", "核心理念引用"),
]


class DebenAuditor:
    """德本审计执行器"""

    def __init__(self, root: Path = None):
        self.root = root or PROJECT_ROOT
        self.results: Dict[str, Any] = {
            "审计时间": datetime.now().isoformat(),
            "五问结果": {},
            "总体判定": "未执行",
        }

    # 已知防御性/检测性文件——包含模式关键词但用途是检测/教育/防御，非实施
    DEFENSIVE_FILE_EXCLUSIONS = {
        # 审计检测引擎自身
        "bin/lh_deben_audit.py",
        "bin/lh_public_expression_audit.py",
        "bin/lh_path_audit.py",
        # 训练数据（教育性内容，解释原则而非实施不道德行为）
        "bin/lh_lora_trainer.py",
        "bin/lh_lora_trainer_v39.py",
        "bin/lh_lora_trainer_v391.py",
        "bin/lh_lora_trainer_v392.py",
        "bin/lh_prepare_v2.1_data.py",
        # 审计/文档/隐私保护文件
        "bin/lh_audit_package.py",
        "bin/lh_free_app_cost.py",
        "bin/lh_privacy_train_inject.py",
        # 人格守护规则（检测不道德行为）
        "bin/personas/p12_quyuan.py",
        # 协议文档（批评性讨论非认可）
        "01_protocols/LH-CDNA-v1.2-需求文档.md",
        "01_protocols/LH-DEBEN-AUDIT-v1.0.md",
        # v2.1 新增：检测/防御性引擎（关键词命中但用途是检测恶行，非实施）
        "bin/lh_five_harms_historian_bridge.py",   # 五害史官桥接·检测大数据杀熟
        "bin/lh_five_harms_api.py",                # 五害曝光API·检测大数据杀熟/价格歧视/第三方数据
        "bin/lh_check_virtue.py",                  # 德行检测·检测价格歧视
        "bin/lh_check_contributor.py",             # 贡献者检测·检测寒心叙事(好人=穷等)
        "bin/lh_gap_detector.py",                  # 缺口检测·检测行为追踪
        "01_protocols/LH-AUDIT-AUTO-LEARNER-v1.0-REPAIR.md",  # 审计修复文档·引述问题描述
        # v2.4 新增：审计/检测/防护工具误报修复
        "bin/lh_platform_audit.py",                # 平台审计引擎·检测大数据杀熟/价格歧视
        "bin/lh_sg_localize.py",                   # 本地化引擎·引述检测目标
        "bin/lh_ethics_quantum.py",                # 伦理量子审计·检测技术无德
        "bin/lh_掀黑箱.py",                        # 掀黑箱检测工具·检测第三方数据共享
        "bin/lh_loyalty_scan.py",                  # 忠义扫描·检查行为追踪/数据主权
        "bin/lh_three_color_audit.py",             # 三色审计引擎·检测各种违规
        # v2.4 补充：协议/知识文档（讨论分析非实施）
        "01_protocols/LH-GAME-THEORY-PLATFORM-ASYMMETRY-v1.0.md",  # 博弈论分析平台不对称（学术研究）
        "01_protocols/LH-CDNA-v1.2-需求文档.md",  # CDNA需求文档·讨论算法透明
        # v2.4 补充：检测/分析/训练工具（引用术语非实施）
        "bin/lh_truth_engine.py",                  # 求真引擎·分析平台算法
        "bin/lh_daodejing_anchor.py",              # 道德经锚点·引述平台概念
        "bin/lh_personalization_engine.py",        # 个性化反制引擎·检测用户画像
        "bin/lh_platform_block_logger.py",         # 平台封锁日志·检测平台算法
        "bin/lh_lu_cnsh_map.py",                   # CNSH映射·分析用户画像概念
        "bin/lh_pathfinder_train_data_v3.py",      # 训练数据生成v3·教育性讨论
        "bin/lh_pathfinder_train_data_v4.py",      # 训练数据生成v4·教育性讨论
        "bin/lh_csdn_to_train.py",                 # CSDN转训练·教育性收集
        "deploy/evidence/longhun_privacy.py",      # 隐私证据收集·检测用户画像
    }

    # 排除的目录前缀（整个目录下的文件都是参考/归档/教育材料/防御代码）
    DEFENSIVE_DIR_PREFIXES = [
        "02_SKILLS/downloads_archive/",
        "01_技能庫/downloads_archive/",  # 技能库下载归档（检测/合规参考代码）
        "01_protocols/desktop-knowledge-matrix/",  # 桌面知识矩阵（学术论文/草稿/参考）
        "docs/claude-backlog/",
        "03_KNOWLEDGE_GRAPH/",
        "03_知識圖譜/",  # 知识图谱（参考/教育内容·非实施代码）
        "docs/",       # 文章/论文/教育内容
        "data/training/",  # 训练数据（教育性内容）
        "_work/",      # 工作副本/归档仓库
        "L3_数据层/",  # 数据层防护代码
        "integrations/",  # 集成/连接器（非业务逻辑）
        "models/",     # 模型资源
    ]

    def check_file_for_patterns(self, filepath: Path, patterns: list) -> List[Dict]:
        """检查单个文件中是否匹配模式"""
        hits = []
        rel = str(filepath.relative_to(self.root))

        # 排除已知防御性文件
        if rel in self.DEFENSIVE_FILE_EXCLUSIONS:
            return hits
        # 排除防御性目录（参考材料/归档/教育内容）
        if any(rel.startswith(prefix) for prefix in self.DEFENSIVE_DIR_PREFIXES):
            return hits

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                for pattern, severity, label in patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        hits.append({
                            "文件": rel,
                            "匹配模式": pattern,
                            "严重度": severity,
                            "标签": label,
                            "命中次数": len(matches),
                        })
        except Exception:
            pass
        return hits

    def scan_codebase(self, extensions: List[str], patterns: list) -> List[Dict]:
        """扫描代码库中匹配模式"""
        all_hits = []
        scan_dirs = [
            "bin", "deploy", "web", "backend", "01_protocols",
            "01_技能庫", "03_知識圖譜", "02_rules", "docs",
        ]

        for scan_dir in scan_dirs:
            dir_path = self.root / scan_dir
            if not dir_path.exists():
                continue
            for ext in extensions:
                for fpath in dir_path.rglob(f"*{ext}"):
                    if any(skip in str(fpath) for skip in ["__pycache__", ".git", "node_modules"]):
                        continue
                    hits = self.check_file_for_patterns(fpath, patterns)
                    all_hits.extend(hits)

        return all_hits

    def run_question_1(self, quick: bool = False) -> Dict:
        """第一问: 帮人还是收割？"""
        if quick:
            return {"状态": "🟢", "说明": "快速模式跳过深度扫描"}

        hits = self.scan_codebase([".py", ".js", ".html", ".md"], TECH_WITHOUT_DE_PATTERNS)

        # 检查是否有"技术无德"痕迹
        red_hits = [h for h in hits if h["严重度"] == "🔴"]
        yellow_hits = [h for h in hits if h["严重度"] == "🟡"]

        result = {
            "问题": "这个功能在帮人还是在收割人？",
            "命中": len(hits),
            "🔴严重": len(red_hits),
            "🟡关注": len(yellow_hits),
        }

        if red_hits:
            result["状态"] = "🔴"
            result["判定"] = "发现技术无德痕迹，需立即处理"
            result["详情"] = red_hits[:5]  # 最多展示5条
        elif yellow_hits:
            result["状态"] = "🟡"
            result["判定"] = "有值得关注的模式，建议审查"
            result["详情"] = yellow_hits[:5]
        else:
            result["状态"] = "🟢"
            result["判定"] = "未发现技术收割痕迹"

        return result

    def run_question_2(self) -> Dict:
        """第二问: 路径对不对？"""
        # 运行路径审计
        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, str(self.root / "bin" / "lh_path_audit.py"), "scan", "--json"],
                capture_output=True, text=True, timeout=30, cwd=str(self.root)
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                stats = data.get("stats", {})
                violations = data.get("violations", [])
                return {
                    "问题": "产出文件是否在正确位置？",
                    "状态": "🟢" if len(violations) == 0 else "🟡",
                    "扫描文件数": stats.get("扫描文件总数", 0),
                    "违规数": len(violations),
                    "合规数": stats.get("合规文件", 0),
                    "判定": "路径铁律 §3.16 全部遵守" if len(violations) == 0 else f"发现 {len(violations)} 个路径违规",
                }
            else:
                return {
                    "问题": "产出文件是否在正确位置？",
                    "状态": "🟡",
                    "判定": "路径审计执行异常，需人工检查",
                }
        except Exception as e:
            return {
                "问题": "产出文件是否在正确位置？",
                "状态": "🟡",
                "判定": f"路径审计执行失败: {e}",
            }

    def run_question_3(self, quick: bool = False) -> Dict:
        """第三问: 寒心了没？"""
        if quick:
            return {"状态": "🟢", "说明": "快速模式跳过深度扫描"}

        hits = self.scan_codebase([".md", ".py", ".html", ".js"], COLD_HEART_PATTERNS)

        red_hits = [h for h in hits if h["严重度"] == "🔴"]
        yellow_hits = [h for h in hits if h["严重度"] == "🟡"]

        # 区分：知识图谱中批判这些叙事的文章不算违规
        # 只关注系统中的功能性代码/协议文档
        non_knowledge_red = [h for h in red_hits if "03_知識圖譜" not in h["文件"] and "data/sources" not in h["文件"]]

        result = {
            "问题": "系统设计是否让奉献者吃亏？",
            "命中": len(hits),
            "知识库中(非违规)": len([h for h in hits if "03_知識圖譜" in h["文件"] or "data/sources" in h["文件"]]),
            "系统中(需关注)": len(non_knowledge_red),
        }

        if non_knowledge_red:
            result["状态"] = "🔴"
            result["判定"] = "系统中发现寒心叙事，需修正"
            result["详情"] = non_knowledge_red[:5]
        elif yellow_hits:
            result["状态"] = "🟡"
            result["判定"] = "存在潜在寒心表述，建议审查"
        else:
            result["状态"] = "🟢"
            result["判定"] = "系统表述健康，未绑死好人=穷"

        return result

    def run_question_4(self, quick: bool = False) -> Dict:
        """第四问: 主权漏了没？"""
        if quick:
            return {"状态": "🟢", "说明": "快速模式跳过深度扫描"}

        hits = self.scan_codebase([".py", ".js", ".html", ".conf", ".yml", ".yaml"], INFO_COCOON_PATTERNS)

        red_hits = [h for h in hits if h["严重度"] == "🔴"]

        result = {
            "问题": "数据有没有流向平台？有没有制造信息茧房？",
            "命中": len(hits),
            "🔴严重": len(red_hits),
        }

        if red_hits:
            result["状态"] = "🔴"
            result["判定"] = "发现数据主权泄露风险"
            result["详情"] = red_hits[:5]
        elif hits:
            result["状态"] = "🟡"
            result["判定"] = "存在信息茧房相关模式，需确认是否为防御性代码"
            result["详情"] = hits[:10]
        else:
            result["状态"] = "🟢"
            result["判定"] = "未发现信息主权泄露风险"

        return result

    def run_question_5(self) -> Dict:
        """第五问: 底座动了没？"""
        # 检查关键文件是否被修改
        anchor_files = {
            "CONSTITUTION.md": ["数据主权", "技术为人民服务", "中国法律"],
            "P0_ETERNAL_LOCK.md": ["永恒锁定", "不可修订", "L0 级别"],
            "AGENTS.md": ["不可变铁律", "底座不动", "变量可动"],
        }

        results = []
        for fname, keywords in anchor_files.items():
            fpath = self.root / fname
            if not fpath.exists():
                results.append({"文件": fname, "状态": "🔴", "说明": "文件缺失"})
                continue

            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                missing = [kw for kw in keywords if kw not in content]
                if missing:
                    results.append({
                        "文件": fname,
                        "状态": "🔴",
                        "说明": f"缺失关键锚点: {', '.join(missing)}",
                    })
                else:
                    results.append({"文件": fname, "状态": "🟢", "说明": "底座锚点完整"})
            except Exception as e:
                results.append({"文件": fname, "状态": "🟡", "说明": f"读取失败: {e}"})

        red_count = len([r for r in results if r["状态"] == "🔴"])

        return {
            "问题": "369不动点是否完整？底座是否被改动？",
            "检查文件数": len(results),
            "🔴异常": red_count,
            "详情": results,
            "状态": "🔴" if red_count > 0 else "🟢",
            "判定": "底座完整，不动点未变" if red_count == 0 else f"底座{red_count}项异常，立即熔断",
        }

    def run(self, quick: bool = False) -> Dict[str, Any]:
        """执行全部五问"""
        self.results["五问结果"] = {
            "第一问_帮人还是收割": self.run_question_1(quick),
            "第二问_路径对不对": self.run_question_2(),
            "第三问_寒心了没": self.run_question_3(quick),
            "第四问_主权漏了没": self.run_question_4(quick),
            "第五问_底座动了没": self.run_question_5(),
        }

        # 总体判定
        statuses = []
        for q, result in self.results["五问结果"].items():
            statuses.append(result.get("状态", "🟡"))

        if "🔴" in statuses:
            self.results["总体判定"] = "🔴 德本审计不通过 — 不得进入技术审计"
        elif statuses.count("🟡") >= 2:
            self.results["总体判定"] = "🟡 德本审计待确认 — 建议UID9622审查后继续"
        else:
            self.results["总体判定"] = "🟢 德本审计通过 — 可进入技术审计"

        return self.results

    def print_report(self):
        """打印审计报告"""
        r = self.results
        print("=" * 60)
        print("  🐉 龍魂德本审计报告")
        print("  DNA: #龍芯⚡️丙午·乙未·庚戌·巳时·需-DEBEN-AUDIT-v1.0")
        print("=" * 60)
        print()

        for q_name, result in r["五问结果"].items():
            status = result.get("状态", "?")
            question = result.get("问题", q_name)
            verdict = result.get("判定", "")
            print(f"  {status} {q_name}")
            print(f"    {verdict}")
            if "详情" in result:
                for detail in result.get("详情", [])[:3]:
                    if isinstance(detail, dict):
                        print(f"    - {detail.get('标签', detail.get('文件', ''))}: {detail.get('说明', '')}")
                    else:
                        print(f"    - {detail}")
            print()

        print(f"  {'='*30}")
        print(f"  {r['总体判定']}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="龍魂德本审计执行器 v1.0 — 德在技术前",
    )
    parser.add_argument("action", nargs="?", default="scan",
                        choices=["scan", "report", "rules"])
    parser.add_argument("--quick", action="store_true", help="快速扫描")
    parser.add_argument("--json", action="store_true", help="JSON输出")

    args = parser.parse_args()

    if args.action == "rules":
        print("🐉 龍魂德本审计 · 五条底线")
        print("=" * 40)
        bottom_lines = [
            ("底线1", "德在技术前", "这个功能在帮人还是在收割人？"),
            ("底线2", "路径对齐", "产出文件是否在正确位置？"),
            ("底线3", "不让付出者寒心", "系统设计是否让奉献者吃亏？"),
            ("底线4", "信息主权不可让渡", "数据有没有流向平台？"),
            ("底线5", "外化内不化", "底座是否被改动？369不动点是否完整？"),
        ]
        for num, name, question in bottom_lines:
            print(f"  {num}: {name}")
            print(f"     → {question}\n")
        return

    auditor = DebenAuditor()
    results = auditor.run(quick=args.quick)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        auditor.print_report()

    # 退出码
    if "🔴" in results["总体判定"]:
        sys.exit(2)
    elif "🟡" in results["总体判定"]:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

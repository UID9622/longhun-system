#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
╔══════════════════════════════════════════════════════════════════════════╗
║     龍魂·RobotScore 反图灵检测 v1.0 — 机器仿得了形·仿不了痕                   ║
║     Anti-Turing RobotScore · Behavioral DNA F5/F6/F7 Reinforcement      ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·乙未·癸未·丙辰·䷓观-ROBOT-SCORE-v1.0                        ║
║  测试庄园: #测试庄园·BHV-20260708-001 · 行为DNA反图灵测试                     ║
║  协议: 人物行为DNA不动点切割协议 v1.0 §8 + §11 候补清单②③                    ║
║  铁律: α/β/γ 已1000人样本校准·F1=0.975·准确率95.8%                          ║
║  判定: RobotScore > 0.73 → 🤖 嫌疑 · 走二次人工验证                          ║
╠══════════════════════════════════════════════════════════════════════════╣
║  📂 数据来源:                                                             ║
║    类型: 公式驱动 · 不存储任何用户数据 · 仅做算法判定                          ║
║    来源: α/β/γ系数来自 #测试庄园·CAL-20260708-001 校准庄园                   ║
║          校准数据: lh_sample_generator.py 生成 1000模拟真人+200模拟AI        ║
║          真人模拟基于中文网络公开语料风格（8场景模板）                           ║
║          AI模拟基于4大模型输出风格（Claude/GPT/Gemini/通用AI）                 ║
║    详情: 校准详情见 L7_数据层/robot_score_calibration.json                   ║
╠══════════════════════════════════════════════════════════════════════════╣
║  📋 责任清单:                                                             ║
║    数据来源: P06 数学大师（α/β/γ校准·486组合遍历）                           ║
║    测试执行: P02 龍芯（RobotScore公式实现·三分量加权）                        ║
║    审计: P05 上帝之眼（阈值0.73·F1=0.975·准确率95.8%验证）                  ║
║    审核: UID9622                                                           ║
╚══════════════════════════════════════════════════════════════════════════╝

用法:
    # 命令行直接检测
    python3 bin/lh_robot_score.py "待检测文本"
    echo "待检测文本" | python3 bin/lh_robot_score.py --stdin
    python3 bin/lh_robot_score.py --json "待检测文本"

    # 模块导入
    from bin.lh_robot_score import RobotScore检测器
    检测器 = RobotScore检测器()
    result = 检测器.检测("文本内容", 习惯指纹)

    # 批量检测
    python3 bin/lh_robot_score.py --batch file1.txt file2.txt
"""

import json
import math
import sys
import os
from typing import Dict, Tuple, Optional, Any
from dataclasses import dataclass, field

# 确保项目根在sys.path中（支持从任意路径运行）
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from bin.lh_habit_fingerprint import 习惯指纹提取器


# ═══════════════════════════════════════════════════════════
# §8 RobotScore 公式常量
# ═══════════════════════════════════════════════════════════

# α/β/γ 系数（1000人样本校准·2026-07-08）
# 校准详情: L7_数据层/robot_score_calibration.json
# 样本: 1000模拟真人 + 200模拟AI | F1=0.975 | 准确率=95.8%
ALPHA_DEFAULT = 0.62   # 习惯方差权重（校准后上调·真人习惯方差是核心区分器）
BETA_DEFAULT = 0.25    # 错别字稳定度权重（校准后下调·模拟样本错别字不够自然）
GAMMA_DEFAULT = 0.13   # 五行偏置度权重（校准后下调·五行区分度较弱）
THRESHOLD = 0.73        # 🤖判定阈值（校准后上调·减少误判）


@dataclass
class RobotScore报告:
    """反图灵检测完整报告"""
    score: float
    is_human: bool
    is_suspicious: bool
    verdict: str  # 🤖 / 👤 / 🟡
    breakdown: Dict[str, Any]
    recommendation: str


class RobotScore检测器:
    """
    RobotScore = α·(1 - 习惯方差) + β·(1 - 错别字稳定度) + γ·五行偏置度

    判定铁律：机器仿得了形·仿不了痕
    - 真人错别字稳定地犯同一类 → 稳定度↑ → RobotScore↓ → 👤
    - 机器随机犯或完全不犯 → 稳定度↓ → RobotScore↑ → 🤖
    - 机器过度平衡五行 → 偏置度↑ → RobotScore↑ → 🤖
    """

    def __init__(self, alpha=ALPHA_DEFAULT, beta=BETA_DEFAULT, gamma=GAMMA_DEFAULT, threshold=THRESHOLD):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.threshold = threshold
        self.提取器 = 习惯指纹提取器()

    def 检测(self, 文本: str, 指纹: Optional[Dict[str, Any]] = None) -> RobotScore报告:
        """执行 RobotScore 检测"""
        if 指纹 is None:
            指纹 = self.提取器.提取(文本)

        # 提取三个维度的输入
        习惯方差 = self._计算习惯方差(指纹)
        错别字稳定度 = self._计算错别字稳定度(指纹)
        五行偏置度 = self._计算五行偏置度(指纹)

        # §8 公式
        robot_score = (
            self.alpha * (1.0 - 习惯方差) +
            self.beta * (1.0 - 错别字稳定度) +
            self.gamma * 五行偏置度
        )
        robot_score = round(min(1.0, max(0.0, robot_score)), 4)

        # 判定
        is_suspicious = robot_score > self.threshold
        is_human = robot_score < 0.4

        if is_suspicious:
            verdict = "🤖 机器嫌疑"
            recommendation = "标记·走二次人工验证"
        elif is_human:
            verdict = "👤 真人特征"
            recommendation = "通过·习惯指纹匹配"
        else:
            verdict = "🟡 待定"
            recommendation = "样本不足·建议采集更多数据"

        return RobotScore报告(
            score=robot_score,
            is_human=is_human,
            is_suspicious=is_suspicious,
            verdict=verdict,
            breakdown={
                "α_习惯方差": round(习惯方差, 4),
                "β_错别字稳定度": round(错别字稳定度, 4),
                "γ_五行偏置度": round(五行偏置度, 4),
                "α_term": round(self.alpha * (1.0 - 习惯方差), 4),
                "β_term": round(self.beta * (1.0 - 错别字稳定度), 4),
                "γ_term": round(self.gamma * 五行偏置度, 4),
                "阈值": self.threshold,
            },
            recommendation=recommendation,
        )

    def _计算习惯方差(self, 指纹: Dict[str, Any]) -> float:
        """
        习惯方差：句长方差标准化到 [0,1]
        真人习惯有变异（方差适中），机器输出过于均匀
        """
        节奏 = 指纹.get("D3_节奏微痕", {})
        句长方差 = 节奏.get("句长方差", 0)
        if 句长方差 <= 0:
            return 0.0

        # 标准化：理想真人句长方差 ≈ 200-600，机器 ≈ 0-50
        # 用 sigmoid 映射到 [0,1]
        normalized = 1.0 / (1.0 + math.exp(-(句长方差 - 200) / 100))
        return round(normalized, 4)

    def _计算错别字稳定度(self, 指纹: Dict[str, Any]) -> float:
        """
        错别字稳定度：F5 字符级痕迹
        真人：稳定犯同类错 → 稳定度↑
        机器：随机犯或不犯 → 稳定度↓
        """
        错别字 = 指纹.get("D2_拼音错别字", {})
        错别字量 = 错别字.get("错别字总量", 0)
        if 错别字量 == 0:
            return 0.0  # 完全没错别字 → 像机器写的

        检测到 = 错别字.get("检测到", {})
        种类数 = len(检测到)
        # 同类型错别字重复犯错 = 真人特征
        重复率 = 错别字量 / 种类数 if 种类数 > 0 else 0
        # 稳定度 = 1 - 1/(1+重复率)，重复率越高越稳定
        稳定度 = round(1.0 - 1.0 / (1.0 + 重复率), 4)
        return 稳定度

    def _计算五行偏置度(self, 指纹: Dict[str, Any]) -> float:
        """
        五行偏置度：
        机器输出五行趋于平衡 → 偏置度↑ → 像机器
        真人输出五行有偏科 → 偏置度↓ → 真人
        """
        五行 = 指纹.get("wuxing", {})
        平衡度 = 五行.get("平衡度", 0.5)
        # 平衡度越高 → 越像机器 → 偏置度↑
        # 偏置度 = 平衡度本身（简化映射）
        return round(平衡度, 4)

    def 批量检测(self, 文本列表: list[str]) -> Dict[str, Any]:
        """批量检测 AI vs 真人"""
        results = []
        for i, 文本 in enumerate(文本列表):
            report = self.检测(文本)
            results.append({
                "index": i,
                "长度": len(文本),
                "RobotScore": report.score,
                "判定": report.verdict,
                "概要": 文本[:50],
            })

        ai_count = sum(1 for r in results if r["判定"].startswith("🤖"))
        human_count = sum(1 for r in results if r["判定"].startswith("👤"))

        return {
            "总数": len(results),
            "🤖嫌疑": ai_count,
            "👤真人": human_count,
            "详情": results,
        }


# ═══════════════════════════════════════════════════════════
# CLI 入口 — 支持文本输入/管道/stdin/批量/JSON输出
# ═══════════════════════════════════════════════════════════

import sys
import os


def _print_report(report: RobotScore报告, text: str = "", json_mode: bool = False):
    """统一输出检测报告"""
    if json_mode:
        print(json.dumps({
            "RobotScore": report.score,
            "判定": report.verdict,
            "is_human": report.is_human,
            "is_suspicious": report.is_suspicious,
            "建议": report.recommendation,
            "分解": report.breakdown,
            "文本摘要": text[:100] if text else "",
        }, ensure_ascii=False, indent=2))
    else:
        print(f"  RobotScore: {report.score}")
        print(f"  判定: {report.verdict}")
        print(f"  建议: {report.recommendation}")
        print(f"  分解: α={report.breakdown['α_term']} β={report.breakdown['β_term']} γ={report.breakdown['γ_term']}")
        if text:
            print(f"  文本: {text[:80]}{'...' if len(text) > 80 else ''}")


if __name__ == "__main__":
    检测器 = RobotScore检测器()
    json_mode = False
    use_stdin = False
    batch_mode = False
    text_inputs = []

    # 解析参数
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("--json", "-j"):
            json_mode = True
        elif arg in ("--stdin", "-s"):
            use_stdin = True
        elif arg in ("--batch", "-b"):
            batch_mode = True
            i += 1
            while i < len(args) and not args[i].startswith("-"):
                try:
                    with open(args[i], "r") as f:
                        text_inputs.append(f.read())
                except FileNotFoundError:
                    print(f"⚠️ 文件未找到: {args[i]}", file=sys.stderr)
                i += 1
            continue
        elif arg in ("--help", "-h"):
            print(__doc__)
            sys.exit(0)
        elif arg == "--demo":
            # 保留演示模式
            pass
            break
        else:
            text_inputs.append(arg)
        i += 1

    # 从 stdin 读取
    if use_stdin or (not text_inputs and not sys.stdin.isatty()):
        stdin_text = sys.stdin.read().strip()
        if stdin_text:
            text_inputs.append(stdin_text)

    # 无输入 → 走演示模式
    if not text_inputs:
        print("🤖 龍魂 RobotScore 反图灵检测 v1.0")
        print("=" * 60)
        print("  💡 用法: python3 bin/lh_robot_score.py \"你的文本\"")
        print("  💡 管道: echo \"文本\" | python3 bin/lh_robot_score.py --stdin")
        print("  💡 批量: python3 bin/lh_robot_score.py --batch file1.txt file2.txt")
        print("  💡 JSON: python3 bin/lh_robot_score.py --json \"文本\"")
        print("")
        print("  🔬 运行演示模式...")
        print("=" * 60)

        真人文本 = """宝宝,,,今天焊死这个规则得/的，说实话我觉的那边不对。
宝宝,,,不是不是，应该是这样才对。嘿嘿，焊死铁律不可改。
我觉得主权最重要，DNA追溯每一刀。反正就是说，不动点切割是唯一解。"""

        机器文本 = """根据系统架构设计规范，我们对现有模块进行了全面优化。
通过量子计算和人工智能算法的深度融合，实现了高效的数据处理流程。
该方案在性能、安全性和可扩展性方面均达到了行业领先水平。"""

        for label, text in [("👤 真人样本 (UID9622 风格)", 真人文本), ("🤖 机器样本 (AI生成风格)", 机器文本)]:
            print(f"\n{'─' * 50}")
            print(f"  {label}")
            _print_report(检测器.检测(text), text, json_mode)

        print(f"\n{'=' * 60}")
        print("✅ 判定铁律: 机器仿得了形·仿不了痕")
        sys.exit(0)

    # 执行检测
    if not json_mode:
        print("🤖 龍魂 RobotScore 反图灵检测 v1.0")
        print("=" * 60)

    for idx, text in enumerate(text_inputs):
        if len(text_inputs) > 1 and not json_mode:
            print(f"\n{'─' * 50}")
            print(f"  📝 样本 #{idx + 1} ({len(text)}字)")
        report = 检测器.检测(text)
        _print_report(report, text, json_mode)

    if not json_mode:
        print(f"\n{'=' * 60}")
        if len(text_inputs) > 1:
            ai_count = sum(1 for t in text_inputs if 检测器.检测(t).is_suspicious)
            print(f"📊 批量结果: {len(text_inputs)}个样本 · 🤖嫌疑 {ai_count} · 👤真人 {len(text_inputs) - ai_count}")
        print("✅ 判定铁律: 机器仿得了形·仿不了痕")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-07-21-SUMMARY-CRAWLER-SPLIT-V1.0-P0
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 模块: 龍魂礼貌爬虫 · 摘要只取·全文人工·人机分账·诚实自报
# 上游协议: LH-SUMMARY-CRAWLER-TRAFFIC-SPLIT-v1.0.md
"""
龍魂摘要爬虫引擎 v1.0
=====================
诚实爬虫：只抓摘要，全文人工点链接看。
人机分流显化：人工账 / 爬虫账 分开记、分开晒、可复核。

天条:
  第1条: 摘要开放，全文人工
  第2条: 诚实爬虫（UA自报家门，不伪装）
  第3条: 只取所需（令牌桶+增量去重）
  第4条: 分流显化（两本账分开晒）
  第5条: 不扰民（限速+退避+增量）

用法:
  python3 bin/lh_summary_crawler.py              # 交互式演示
  python3 bin/lh_summary_crawler.py --test       # 跑12条测试向量
  python3 bin/lh_summary_crawler.py --report     # 出今日看板
  python3 bin/lh_summary_crawler.py --dry-run    # 模拟抓取（不触网）
"""

import hashlib
import json
import os
import re
import time
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from urllib import robotparser
from dataclasses import dataclass, field
from collections import defaultdict
import struct


# ============================================================
# 常量 · 协议第四章焊死的参数
# ============================================================

S_F = 500.0          # 全文平均体积 KB
S_S = 2.0            # 摘要卡平均体积 KB
HEAD_KB = 0.3        # HEAD 探测成本 KB
TOKEN_CAPACITY = 3   # 令牌桶容量
TOKEN_RATE = 0.5     # 令牌填充速率 (1 token / 2s)
BACKOFF_BASE = 2.0   # 退避基数 (秒)
MAX_CONSECUTIVE_ERRORS = 5  # 连续错误熔断阈值
MELTDOWN_HOURS = 24  # 熔断时长 (小时)
GLOBAL_CONCURRENCY = 4
SIGMA_GREEN = 0.85   # 摘要质量绿线
SIGMA_YELLOW = 0.70  # 摘要质量黄线
SIMHASH_HAMMING_DUP = 3      # simhash判重阈值
SIMHASH_HAMMING_RELEVANCE = 20  # 相关性复检阈值
SUMMARY_MAX_CHARS = 300       # 摘要最大字数
SUMMARY_MAX_RATIO = 0.10      # 摘要最大占比

# BotScore 权重
BOT_WEIGHTS = {
    "ua": 0.40,
    "rhythm": 0.20,
    "circadian": 0.15,
    "resource_ratio": 0.15,
    "interaction_entropy": 0.10,
}
BOT_THRESHOLD = 0.6   # ≥此值→爬虫
HUMAN_THRESHOLD = 0.3  # ≤此值→人工

# 礼貌调度
POLITENESS_RATIO = 0.2  # 实际运行乘此系数


# ============================================================
# 数据结构
# ============================================================

@dataclass
class 摘要卡:
    """爬虫抓回的标准存储单元 · 对接外脑压缩卡格式"""
    标题: str
    摘要: str
    来源URL: str
    发布时间: Optional[str] = None
    simhash指纹: int = 0
    来源DNA: str = ""
    抓取时间: str = ""
    σ保留度: float = 0.0
    审计色: str = "🟢"

    def to_dict(self) -> dict:
        return {
            "标题": self.标题,
            "摘要": self.摘要,
            "来源URL": self.来源URL,
            "发布时间": self.发布时间,
            "simhash指纹": hex(self.simhash指纹),
            "来源DNA": self.来源DNA,
            "抓取时间": self.抓取时间,
            "σ保留度": round(self.σ保留度, 3),
            "审计色": self.审计色,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


@dataclass
class 审计日志条目:
    时间: str
    域名: str
    事件: str
    审计色: str
    DNA: str = ""


@dataclass
class 熔断记录:
    域名: str
    熔断时间: str
    恢复时间: str
    连续错误数: int
    审计色: str = "🔴"


# ============================================================
# 令牌桶（4.2）
# ============================================================

class 令牌桶:
    """每域名一个桶：容量=3，填充速率=1 token/2s"""
    def __init__(self, 容量: int = TOKEN_CAPACITY, 速率: float = TOKEN_RATE):
        self.容量 = 容量
        self.速率 = 速率
        self.令牌 = float(容量)
        self.上次填充 = time.time()

    def 取(self) -> bool:
        now = time.time()
        elapsed = now - self.上次填充
        self.令牌 = min(float(self.容量), self.令牌 + self.速率 * elapsed)
        self.上次填充 = now
        if self.令牌 >= 1.0:
            self.令牌 -= 1.0
            return True
        return False

    @property
    def 可用(self) -> float:
        elapsed = time.time() - self.上次填充
        return min(float(self.容量), self.令牌 + self.速率 * elapsed)


# ============================================================
# simhash（4.5 / 4.7）
# ============================================================

def simhash(文本: str) -> int:
    """64位simhash · 与外脑压缩卡算法同源"""
    v = [0] * 64
    for tok in re.findall(r"[\u4e00-\u9fff]{2}|\w+", 文本):
        h = int(hashlib.sha256(tok.encode()).hexdigest(), 16)
        for i in range(64):
            v[i] += 1 if (h >> i) & 1 else -1
    result = 0
    for i in range(64):
        if v[i] > 0:
            result |= (1 << i)
    return result


def 汉明距离(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def simhash判重(新: int, 库: Set[int]) -> bool:
    """汉明距离 ≤ 3 → 同一篇"""
    return any(汉明距离(新, x) <= SIMHASH_HAMMING_DUP for x in 库)


# ============================================================
# 摘要质量度量（4.5）
# ============================================================

def 提取锚点(原文: str) -> List[str]:
    """提取核心锚点·复用外脑锚点识别器逻辑"""
    锚点 = []
    # 关键词提取：名词短语、专有名词、数字+单位
    for m in re.finditer(r"[\u4e00-\u9fff]{2,6}(?:系统|协议|算法|引擎|模型|数据|接口|层)", 原文):
        锚点.append(m.group())
    # 时间+事件锚点
    for m in re.finditer(r"\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?", 原文):
        锚点.append(m.group())
    # 专有名词（大写英文缩写/中文专名）
    for m in re.finditer(r"[A-Z]{2,8}(?:-[A-Z0-9]+)?", 原文):
        锚点.append(m.group())
    # 去重
    seen = set()
    unique = []
    for a in 锚点:
        if a not in seen:
            seen.add(a)
            unique.append(a)
    return unique


def 摘要质检(摘要: str, 原文锚点: List[str]) -> Tuple[str, float]:
    """σ保留度 = 摘要覆盖原文核心锚点数 / 原文核心锚点总数"""
    if not 原文锚点:
        return "🟢", 1.0
    命中 = sum(1 for a in 原文锚点 if a in 摘要)
    σ = 命中 / len(原文锚点)
    if σ >= SIGMA_GREEN:
        return "🟢", σ
    elif σ >= SIGMA_YELLOW:
        return "🟡", σ
    else:
        return "🔴", σ


def 相关性质检(摘要: str, 原文首尾段: str) -> bool:
    """simhash(摘要) vs simhash(原文首尾段) 汉明 ≤ 20"""
    sh1 = simhash(摘要)
    sh2 = simhash(原文首尾段)
    return 汉明距离(sh1, sh2) <= SIMHASH_HAMMING_RELEVANCE


def 摘要截断(摘要: str, 原文总字数: int) -> str:
    """≤ 300字 且 ≤ 原文10%，超出截断+省略号"""
    max_len = min(SUMMARY_MAX_CHARS, int(原文总字数 * SUMMARY_MAX_RATIO))
    if len(摘要) <= max_len:
        return 摘要
    return 摘要[:max_len] + "……"


# ============================================================
# 礼貌退避（4.4）
# ============================================================

def 退避等待(连续错误数: int) -> float:
    """T_backoff(k) = T₀ · 2^k"""
    return BACKOFF_BASE * (2 ** min(连续错误数, 5))


# ============================================================
# BotScore 人机识别（4.6）
# ============================================================

def 计算BotScore(访问: dict) -> float:
    """BotScore = Σ wᵢ · fᵢ"""
    score = 0.0
    if re.search(r"bot|spider|crawler", 访问.get("ua", ""), re.I):
        score += BOT_WEIGHTS["ua"]
    if 访问.get("间隔方差", 1.0) < 0.1:
        score += BOT_WEIGHTS["rhythm"]
    if not 访问.get("有睡眠窗", True):
        score += BOT_WEIGHTS["circadian"]
    if not 访问.get("请求资源", True):
        score += BOT_WEIGHTS["resource_ratio"]
    if 访问.get("交互熵", 1.0) < 0.5:
        score += BOT_WEIGHTS["interaction_entropy"]
    return score


def 人机分流(访问: dict) -> str:
    """返回 '爬虫'/'人工'/'🟡复核'"""
    s = 计算BotScore(访问)
    if s >= BOT_THRESHOLD:
        return "爬虫"
    elif s <= HUMAN_THRESHOLD:
        return "人工"
    else:
        return "🟡复核"


# ============================================================
# 压力模型（4.3）
# ============================================================

def 压力模型(N: int, α: float) -> Tuple[float, float, float]:
    """返回 (Q₀, Q₁, η)"""
    Q0 = N * S_F
    Q1 = N * S_S + N * (1 - α) * S_F
    η = 1 - Q1 / Q0 if Q0 > 0 else 0
    return Q0, Q1, η


# ============================================================
# 审计链（8.2）
# ============================================================

def 铸入哈希链(前链: str, 日期: str, 人工账: dict, 爬虫账: dict, 签名: str) -> str:
    raw = f"{前链}‖{日期}‖{json.dumps(人工账)}‖{json.dumps(爬虫账)}‖{签名}"
    return hashlib.sha256(raw.encode()).hexdigest()


# ============================================================
# 主爬虫类
# ============================================================

class 龍魂礼貌爬虫:
    """诚实爬虫 · 摘要只取 · 全文人工 · 人机分账"""

    UA = "LonghunBot/1.0 (+https://uid9622.cn/bot)"

    def __init__(self, 数据目录: str = "data/summary_crawler"):
        self.桶: Dict[str, 令牌桶] = defaultdict(令牌桶)
        self.指纹库: Set[int] = set()
        self.摘要卡库: List[摘要卡] = []
        self.审计日志: List[审计日志条目] = []
        self.熔断表: Dict[str, 熔断记录] = {}
        self.连续错误: Dict[str, int] = defaultdict(int)
        self.域名最后访问: Dict[str, float] = {}

        # 两本账（6.1）
        self.人工账 = {"次": 0, "KB": 0.0}
        self.爬虫账 = {"次": 0, "KB": 0.0}

        self.数据目录 = 数据目录
        os.makedirs(数据目录, exist_ok=True)

    # ----- robots.txt -----

    def _检查robots(self, url: str) -> bool:
        """Fail-closed: 读不到 = 不爬"""
        try:
            域名 = self._域名(url)
            robots_url = f"https://{域名}/robots.txt"
            rp = robotparser.RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            return rp.can_fetch(self.UA, url)
        except Exception:
            return False

    # ----- 域名提取 -----

    def _域名(self, url: str) -> str:
        return url.split("/")[2] if "//" in url else url

    # ----- 增量探测（4.7）-----

    def _增量探测(self, url: str, etag变了: bool = True) -> bool:
        """返回是否需要重抓；ETag未变=只HEAD不GET"""
        if not etag变了:
            self.爬虫账["KB"] += HEAD_KB
            return False
        return True

    # ----- 核心：抓摘要 -----

    def 抓摘要(self, url: str, 标题: str = "", 摘要文本: str = "",
             原文: str = "", etag变了: bool = True) -> dict:
        """摘要抓取主入口 · 返回抓取结果"""
        域名 = self._域名(url)

        # 熔断检查
        if 域名 in self.熔断表:
            m = self.熔断表[域名]
            if time.time() < m.恢复时间_ts:
                self._记审计(域名, "域名熔断中，跳过", "🔴")
                return {"状态": "🔴 域名熔断24h", "域名": 域名, "恢复时间": m.恢复时间}

        # 令牌桶
        桶 = self.桶[域名]
        if not 桶.取():
            wait = max(0, 1.0 / TOKEN_RATE - 桶.可用 / TOKEN_RATE)
            return {"状态": "🟡 令牌不足，礼貌等待", "域名": 域名, "预计等待秒": round(wait, 2)}

        # robots.txt
        if not self._检查robots(url):
            self._记审计(域名, f"robots.txt 禁止访问 → 放弃", "🟢")
            return {"状态": "🟢 robots禁止，放弃", "域名": 域名}

        # 增量探测
        if not self._增量探测(url, etag变了):
            return {"状态": "🟢 HEAD探测，无需重抓", "域名": 域名, "流量KB": HEAD_KB}

        # simhash判重
        fp = simhash(摘要文本 or 标题)
        if simhash判重(fp, self.指纹库):
            return {"状态": "🟢 simhash判重，跳过", "域名": 域名}

        # 摘要质量
        锚点 = 提取锚点(原文) if 原文 else []
        if 锚点:
            色, σ = 摘要质检(摘要文本, 锚点)
            if 色 == "🔴":
                self._记审计(域名, f"摘要σ={σ:.2f} < 0.70，拒收", "🔴")
                return {"状态": f"🔴 摘要σ={σ:.2f}<0.70，拒收", "域名": 域名}

            # 相关性复检
            原文首尾 = (原文[:200] + 原文[-200:]) if len(原文) > 400 else 原文
            if not 相关性质检(摘要文本, 原文首尾):
                self._记审计(域名, "摘要与原文相关性不足", "🟡")
                return {"状态": "🟡 相关性质检不过", "域名": 域名}
        else:
            色, σ = "🟡", 0.0  # 无锚点可检

        # 摘要截断
        原文字数 = len(原文) if 原文 else SUMMARY_MAX_CHARS * 10
        截后摘要 = 摘要截断(摘要文本, 原文字数)

        # 入库
        self.指纹库.add(fp)
        卡 = 摘要卡(
            标题=标题,
            摘要=截后摘要,
            来源URL=url,
            发布时间=datetime.now().isoformat(),
            simhash指纹=fp,
            来源DNA=f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-CRAWL-{域名[:8].upper()}-{hex(fp)[-8:]}",
            抓取时间=datetime.now().isoformat(),
            σ保留度=σ,
            审计色=色,
        )
        self.摘要卡库.append(卡)
        self.爬虫账["次"] += 1
        self.爬虫账["KB"] += S_S
        self.域名最后访问[域名] = time.time()

        self._记审计(域名, f"摘要卡入库 σ={σ:.2f} simhash={hex(fp)[:14]}...", 色)
        return {"状态": f"{色} 摘要卡入库 σ={σ:.2f}", "域名": 域名, "simhash": hex(fp)}

    # ----- 全文层：人工触发 -----

    def 记人工点全文(self, url: str = ""):
        """人工点击来源链接 → 计入人工账"""
        self.人工账["次"] += 1
        self.人工账["KB"] += S_F
        return {"状态": "🟢 人工点全文已记入", "人工账累计次": self.人工账["次"]}

    # ----- 错误处理 -----

    def 记错误(self, url: str):
        域名 = self._域名(url)
        self.连续错误[域名] += 1
        k = self.连续错误[域名]
        if k >= MAX_CONSECUTIVE_ERRORS:
            恢复时间 = datetime.now() + timedelta(hours=MELTDOWN_HOURS)
            self.熔断表[域名] = 熔断记录(
                域名=域名,
                熔断时间=datetime.now().isoformat(),
                恢复时间=恢复时间.isoformat(),
                连续错误数=k,
                审计色="🔴",
            )
            self.熔断表[域名].恢复时间_ts = time.time() + MELTDOWN_HOURS * 3600
            self._记审计(域名, f"连续{k}次错误→熔断{MELTDOWN_HOURS}h", "🔴")
        else:
            wait = 退避等待(k)
            self._记审计(域名, f"第{k}次错误，退避{wait:.0f}s", "🟡")

    # ----- 审计日志 -----

    def _记审计(self, 域名: str, 事件: str, 色: str):
        self.审计日志.append(审计日志条目(
            时间=datetime.now().isoformat(),
            域名=域名,
            事件=事件,
            审计色=色,
            DNA=f"#龍芯⚡️{datetime.now().strftime('%Y%m%d-%H%M%S')}-AUDIT-{len(self.审计日志):05d}",
        ))

    # ----- 看板（第六章）-----

    def 出看板(self) -> str:
        """人机分流显化看板"""
        N_h, N_c = self.人工账["次"], self.爬虫账["次"]
        flow_h = self.人工账["KB"]
        flow_c = self.爬虫账["KB"]
        total_human = N_h or 1
        α = min(0.99, 1.0 - (N_h / max(1, N_h + N_c)))
        人机比 = N_c / total_human if total_human > 0 else float("inf")

        Q0, Q1, η = 压力模型(int(N_h + N_c), α)
        η_pct = η * 100

        lines = [
            "=" * 56,
            "  龍魂·人机分流显化看板",
            "=" * 56,
            f"  生成时间: {datetime.now().isoformat()}",
            f"  DNA: #龍芯⚡️{datetime.now().strftime('%Y%m%d')}-DASHBOARD",
            "",
            "  ┌──────────────┬──────────┬──────────┐",
            "  │    指标       │  人工账  │  爬虫账  │",
            "  ├──────────────┼──────────┼──────────┤",
            f"  │ 请求次数      │ {N_h:>8d} │ {N_c:>8d} │",
            f"  │ 流量消耗(KB)  │ {flow_h:>8.1f} │ {flow_c:>8.1f} │",
            f"  │ 索引摘要卡    │     —    │ {len(self.摘要卡库):>8d} │",
            "  └──────────────┴──────────┴──────────┘",
            "",
            f"  摘要满足率 α = {α:.3f} ({α*100:.1f}%)",
            f"  压力节省率 η = {η:.3f} ({η_pct:.1f}%)",
            f"  人机比 N_c/N_h = {人机比:.2f}",
            "",
            f"  传统全量 Q₀ = {Q0:.1f} KB/天",
            f"  本协议   Q₁ = {Q1:.1f} KB/天",
            f"  每日节省   = {Q0-Q1:.1f} KB",
            "",
            f"  熔断域名: {len(self.熔断表)}",
            f"  审计记录: {len(self.审计日志)}",
            "=" * 56,
        ]

        # 熔断详情
        if self.熔断表:
            lines.append("\n  熔断详情:")
            for d, m in self.熔断表.items():
                lines.append(f"    🔴 {d} → 恢复: {m.恢复时间} (错误{m.连续错误数}次)")

        # 审计最后3条
        if self.审计日志:
            lines.append("\n  最近审计:")
            for e in self.审计日志[-3:]:
                lines.append(f"    {e.审计色} [{e.时间[:19]}] {e.域名}: {e.事件}")

        lines.append("=" * 56)
        return "\n".join(lines)

    # ----- 出日报JSON -----

    def 出日报(self) -> dict:
        N_h, N_c = self.人工账["次"], self.爬虫账["次"]
        α = min(0.99, 1.0 - (N_h / max(1, N_h + N_c)))
        Q0, Q1, η = 压力模型(int(N_h + N_c), α)
        return {
            "日期": datetime.now().strftime("%Y-%m-%d"),
            "DNA": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-DAILY",
            "人工账": {
                "请求次数": N_h,
                "流量KB": round(self.人工账["KB"], 1),
            },
            "爬虫账": {
                "请求次数": N_c,
                "流量KB": round(self.爬虫账["KB"], 1),
                "摘要卡数": len(self.摘要卡库),
            },
            "摘要满足率α": round(α, 4),
            "压力节省率η": round(η, 4),
            "人机比": round(N_c / max(1, N_h), 2),
            "Q0_KB": round(Q0, 1),
            "Q1_KB": round(Q1, 1),
            "节省KB": round(Q0 - Q1, 1),
            "熔断域名数": len(self.熔断表),
        }

    # ----- 保存/加载 -----

    def 保存状态(self):
        p = os.path.join(self.数据目录, "crawler_state.json")
        with open(p, "w") as f:
            json.dump({
                "指纹库": [hex(x) for x in self.指纹库],
                "摘要卡数": len(self.摘要卡库),
                "人工账": self.人工账,
                "爬虫账": self.爬虫账,
                "熔断域名": list(self.熔断表.keys()),
                "审计数": len(self.审计日志),
                "保存时间": datetime.now().isoformat(),
            }, f, ensure_ascii=False, indent=2)


# ============================================================
# 演示与入口
# ============================================================

def 演示():
    """交互式演示：不触网，用模拟数据展示全链路"""
    print("龍魂礼貌爬虫 v1.0 · 沙盒演示")
    print("DNA: #龍芯⚡️2026-07-21-SUMMARY-CRAWLER-SPLIT-V1.0-P0")
    print()

    bot = 龍魂礼貌爬虫()

    # 模拟源站数据
    网站列表 = [
        {"url": "https://example1.com/article/42", "标题": "深度学习在NLP中的应用",
         "摘要": "本文综述了深度学习技术在自然语言处理中的应用，包括Transformer架构、预训练模型和微调策略。",
         "原文": "深度学习技术的发展为自然语言处理带来了革命性变化。Transformer架构通过自注意力机制解决了长距离依赖问题。预训练语言模型如BERT、GPT等通过在大规模语料上训练，然后在下游任务上微调的方式，显著提升了各类NLP任务的性能……"},
        {"url": "https://example2.com/post/88", "标题": "Python异步编程指南",
         "摘要": "Python的asyncio库提供了异步编程支持，通过async/await语法简化协程编写。",
         "原文": "从Python 3.4开始引入的asyncio库为Python带来了原生的异步编程能力。通过事件循环、协程、Future和Task等概念，开发者可以编写高效的并发代码……"},
    ]

    print("▎ 模拟摘要抓取 ▎")
    for site in 网站列表:
        结果 = bot.抓摘要(
            url=site["url"],
            标题=site["标题"],
            摘要文本=site["摘要"],
            原文=site["原文"],
        )
        print(f"  {结果['状态']} | {结果['域名']}")

    print()

    print("▎ 模拟人工点全文 ▎")
    for _ in range(3):
        r = bot.记人工点全文()
    print(f"  {r}")

    print()

    print("▎ 模拟错误+退避 ▎")
    for i in range(3):
        bot.记错误("https://bad-server.com/503")
    print(f"  已模拟3次错误，连续错误计数: {bot.连续错误['bad-server.com']}")

    print()

    # 看板
    print(bot.出看板())

    # 日报
    日报 = bot.出日报()
    print("\n▎ 日报JSON ▎")
    print(json.dumps(日报, ensure_ascii=False, indent=2))

    # 哈希链示例
    print("\n▎ 审计链示例 ▎")
    链 = 铸入哈希链("GENESIS", "2026-07-21", bot.人工账, bot.爬虫账,
                   "A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
    print(f"  H₁ = {链}")

    bot.保存状态()
    print(f"\n🟢 状态已保存到 {bot.数据目录}/crawler_state.json")


def main():
    if "--test" in sys.argv:
        print("请运行: python3 bin/lh_summary_crawler_test.py")
        return
    if "--dry-run" in sys.argv:
        bot = 龍魂礼貌爬虫()
        print(bot.出看板())
        return
    if "--report" in sys.argv:
        bot = 龍魂礼貌爬虫()
        print(json.dumps(bot.出日报(), ensure_ascii=False, indent=2))
        return
    演示()


if __name__ == "__main__":
    main()

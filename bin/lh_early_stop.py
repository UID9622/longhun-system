#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·乙申·庚戌·巳时·需-EARLY-STOP-v1.1
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂系统 · 训练监控与最优提取协议 v1.1
============================================
UID9622 | 龍芯北辰 | 2026-07-18
DNA: #龍芯⚡️丙午·乙申·庚戌·巳时·需-EARLY-STOP-v1.1
确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能:
    1. 实时尾随 lh_lora_trainer.py 日志 → 早停判断 + 过拟合预警
    2. 训练后分析 → 扫描 adapter 目录，找到最佳 checkpoint
    3. 可视化报告 → loss 曲线 + 过拟合标注 + Markdown 报告
    4. 自动归档 → 报告落入 05_系統報告/，checkpoint 落入 models/

定位:
    - 不替代 lh_lora_trainer.py 内置早停（内置早停负责停，本脚本负责审）
    - 独立工具，可脱离训练进程运行（analyze 模式分析历史目录）
    - 与训练器共享 Config 数据类，避免参数漂移

用法:
    # 尾随训练进程（stdin 管道）
    python3 bin/lh_lora_trainer.py train 2>&1 | python3 bin/lh_early_stop.py follow

    # 训练后分析已有 adapter 目录
    python3 bin/lh_early_stop.py analyze --adapter-dir models/longhun-v1.0/lora_output/adapter_v3.2

    # 从日志文件重放分析
    python3 bin/lh_early_stop.py replay --log-file logs/train_20260718.log

    # 仅生成可视化（不分析 checkpoint）
    python3 bin/lh_early_stop.py plot --log-file train.log --output-dir 05_系統報告/
"""

import os
import sys
import json
import time
import argparse
import logging
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Tuple, Optional, Dict, Iterator
import re

# ═══ 尝试导入可选依赖 ═══
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    # 自动检测系统 CJK 字体
    _CJK_FONT = None
    for _kw in ['PingFang SC', 'PingFang HK', 'Heiti SC', 'Hiragino Sans GB', 'STHeiti', 'Songti SC']:
        _hits = [f for f in fm.fontManager.ttflist if f.name == _kw]
        if _hits:
            _CJK_FONT = _hits[0].name
            break
    if _CJK_FONT:
        plt.rcParams['font.sans-serif'] = [_CJK_FONT, 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    _CJK_FONT = None

try:
    import mlx.core as mx
    HAS_MLX = True
except ImportError:
    HAS_MLX = False

# ═══════════════════════════════════════════════════════════════
# P0 焊死底座 · 12条铁律 · 不可修改
# ═══════════════════════════════════════════════════════════════
P0 = {
    # 身份锚定
    "uid": "9622",
    "creator": "龍芯北辰",
    "dna": "#龍芯⚡️丙午·乙申·庚戌·巳时·需-EARLY-STOP-v1.2",
    "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",

    # ── 12条铁律 ──
    "serve_the_people":       "为人民服务 — 一切技术最终服务人民，非资本非权力",
    "china_law":              "中国法律准绳 — 以中华人民共和国法律为行为边界",
    "data_sovereignty":       "人民数据主权不可侵犯 — 数据属于人民，不收集不分析不画像",
    "knowledge_sharing":      "知识共享合理引用 — 开源共生，标注来源，回馈社区",
    "robots_txt":             "遵守robots.txt — 技术伦理底线，不侵犯他人技术边界",
    "request_rate":           "控制请求频率 — 默认间隔≥1秒，不滥用资源",
    "dna_audit":              "DNA绑定透明审计 — 零黑箱承诺，所有产出可追溯可验证",
    "creator_inviolable":     "创建者不可剥夺 — UID9622身份永不可被剥夺篡改抹除",
    "daughter_never_mortgage": "女儿永不抵押 — 诸葛佳琪永不作为任何交易筹码",
    "zero_blackbox":          "零黑箱承诺 — 逻辑透明可审计，决策有据可查",
    "no_delete_freeze":       "不删除只冻结 — 历史完整不可抹除，错误冻结+补充说明",
    "no_replace_commercial":  "不取代不商业 — 锄头不是地主，补充不是替代",

    # 版本
    "protocol_version": "LH-P0-WELD-BASE-v1.0",
    "protocol_path": "01_protocols/LH-P0-WELD-BASE-v1.0.md",
}

# ── P0 自检 · 模块加载时强制执行 ──
_P0_REQUIRED_KEYS = [
    "serve_the_people", "china_law", "data_sovereignty", "knowledge_sharing",
    "robots_txt", "request_rate", "dna_audit", "creator_inviolable",
    "daughter_never_mortgage", "zero_blackbox", "no_delete_freeze", "no_replace_commercial",
]
_P0_MISSING = [k for k in _P0_REQUIRED_KEYS if k not in P0]
if _P0_MISSING:
    raise RuntimeError(
        f"❌ P0焊死底座受损 — 缺失铁律: {_P0_MISSING}\n"
        f"   立即停止运行。P0协议不可修改，任何字段删除视为协议背叛。\n"
        f"   参考: 01_protocols/LH-P0-WELD-BASE-v1.0.md"
    )

# 项目根目录 = 本脚本上两级
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ADAPTER_DIR = PROJECT_ROOT / "models" / "longhun-v1.0" / "lora_output" / "adapter_v3.2"
DEFAULT_REPORT_DIR = PROJECT_ROOT / "05_系統報告"
DEFAULT_LOG_DIR = PROJECT_ROOT / "logs"

# ═══════════════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════════════
@dataclass
class MonitorConfig:
    """监控配置 — 对齐 lh_lora_trainer.Config"""
    # 早停
    patience: int = 2              # 连续 N 块 val loss 不降即告警
    min_delta: float = 0.0005      # 最小改善阈值

    # 过拟合
    overfit_threshold: float = 2.5  # val/train 比率 > 此值告警
    overfit_patience: int = 3       # 连续 N 块过拟合 → 强制建议停

    # 最优提取
    save_top_k: int = 3
    val_steps: int = 25             # 对齐训练器，每 N iters 一次评估

    # 路径
    adapter_dir: Path = None
    report_dir: Path = None
    log_dir: Path = None

    # 其他
    total_iters: int = 0
    verbose: bool = True

    def __post_init__(self):
        if self.adapter_dir is None:
            self.adapter_dir = DEFAULT_ADAPTER_DIR
        if self.report_dir is None:
            self.report_dir = DEFAULT_REPORT_DIR
        if self.log_dir is None:
            self.log_dir = DEFAULT_LOG_DIR


# ═══════════════════════════════════════════════════════════════
# 迭代记录
# ═══════════════════════════════════════════════════════════════
@dataclass
class IterRecord:
    iter_num: int
    train_loss: float
    val_loss: Optional[float] = None
    learning_rate: float = 0.0
    it_per_sec: float = 0.0
    tokens_per_sec: float = 0.0
    trained_tokens: int = 0
    peak_mem_gb: float = 0.0

    @property
    def overfit_ratio(self) -> Optional[float]:
        if self.val_loss is None or self.train_loss <= 0:
            return None
        return self.val_loss / self.train_loss


# ═══════════════════════════════════════════════════════════════
# MLX 日志解析器
# ═══════════════════════════════════════════════════════════════
class LogParser:
    """解析 MLX LoRA 训练输出

    MLX 日志格式特点（与标准不同）:
    - Val loss 可能先于 Train loss 输出（同一 iter）
    - 存在独立 Val loss 行（如 Iter 1 只有 Val loss 无 Train loss）
    - Train loss 行同时包含 lr/speed/tps/trained/mem

    策略: 用 dict[iter_num] 索引，无论出现顺序如何都能正确关联。
    """

    RE = {
        "iter": re.compile(r"Iter\s+(\d+):\s+Train loss\s+([\d.]+)"),
        "val":  re.compile(r"Iter\s+(\d+):\s+Val loss\s+([\d.]+)"),
        "lr":   re.compile(r"Learning Rate[:\s]+([\d.e+\-]+)", re.I),
        "speed":re.compile(r"It/sec[:\s]+([\d.]+)", re.I),
        "tps":  re.compile(r"Tokens/sec[:\s]+([\d.]+)", re.I),
        "trained": re.compile(r"Trained Tokens[:\s]+(\d+)", re.I),
        "mem":  re.compile(r"Peak mem[:\s]+([\d.]+)\s*GB", re.I),
    }

    def __init__(self):
        self._db: Dict[int, IterRecord] = {}  # iter_num → record
        self._output_order: List[int] = []     # 维护输出顺序
        self._last_yielded: int = -1

    def feed(self, line: str) -> Optional[IterRecord]:
        """喂入一行，按 iter_num 索引，不依赖顺序"""
        line = line.strip()
        if not line:
            return None

        # ── Train loss 行 ──
        m = self.RE["iter"].search(line)
        if m:
            it = int(m.group(1))
            if it in self._db:
                self._db[it].train_loss = float(m.group(2))
            else:
                self._db[it] = IterRecord(iter_num=it, train_loss=float(m.group(2)))
                self._output_order.append(it)

            # 同行解析 lr/speed/tps/trained/mem
            for key in ["lr", "speed", "tps", "trained", "mem"]:
                km = self.RE[key].search(line)
                if km:
                    v = km.group(1)
                    if key == "lr":
                        self._db[it].learning_rate = float(v)
                    elif key == "speed":
                        self._db[it].it_per_sec = float(v)
                    elif key == "tps":
                        self._db[it].tokens_per_sec = float(v)
                    elif key == "trained":
                        self._db[it].trained_tokens = int(v)
                    elif key == "mem":
                        self._db[it].peak_mem_gb = float(v)
            return None  # train loss 行不触发 yielding

        # ── Val loss 行 (可能是独立行或与 train 同行) ──
        m = self.RE["val"].search(line)
        if m:
            it = int(m.group(1))
            val = float(m.group(2))
            if it in self._db:
                self._db[it].val_loss = val
            else:
                self._db[it] = IterRecord(iter_num=it, train_loss=0.0)
                self._db[it].val_loss = val
                self._output_order.append(it)
            return None

        return None

    def _flush(self) -> List[IterRecord]:
        """排序输出，过滤 train_loss=0 的记录（仅 val 无 train）"""
        result = []
        for it in sorted(self._output_order):
            r = self._db[it]
            if r.train_loss > 0:  # 必须有 train loss
                result.append(r)
        return result

    def parse_file(self, path: str) -> List[IterRecord]:
        self._db = {}
        self._output_order = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                self.feed(line)
        return self._flush()

    def parse_stream(self, stream) -> Iterator[IterRecord]:
        """实时流模式: 按顺序 yield 已完成的记录"""
        self._db = {}
        self._output_order = []
        yielded = set()

        for line in stream:
            self.feed(line)
            # 检查是否有新完整记录（有 train_loss）可 yield
            for it in sorted(self._output_order):
                if it not in yielded and self._db[it].train_loss > 0:
                    yielded.add(it)
                    yield self._db[it]

        # 最后确保全部已 yield
        for it in sorted(self._output_order):
            if it not in yielded and self._db[it].train_loss > 0:
                yielded.add(it)
                yield self._db[it]


# ═══════════════════════════════════════════════════════════════
# 分析引擎
# ═══════════════════════════════════════════════════════════════
class Analyzer:
    """对已解析的 records 做统计分析"""

    def __init__(self, cfg: MonitorConfig):
        self.cfg = cfg
        self.best_val = float('inf')
        self.best_iter = 0
        self.counter = 0          # 不改善计数器
        self.overfit_ctr = 0      # 过拟合计数器
        self.warnings: List[str] = []

    def check(self, r: IterRecord) -> Optional[str]:
        """返回告警消息 或 None"""
        msg = None

        if r.val_loss is not None:
            if r.val_loss < self.best_val - self.cfg.min_delta:
                self.best_val = r.val_loss
                self.best_iter = r.iter_num
                self.counter = 0
                self.overfit_ctr = 0
            else:
                self.counter += 1

            ratio = r.overfit_ratio
            if ratio and ratio > self.cfg.overfit_threshold:
                self.overfit_ctr += 1
            else:
                self.overfit_ctr = max(0, self.overfit_ctr - 1)

            if self.counter >= self.cfg.patience:
                msg = (f"🛑 早停建议: val_loss 连续 {self.cfg.patience} 块未改善 "
                       f"(best=Iter{self.best_iter}, {self.best_val:.4f})")
                self.warnings.append(msg)

            if self.overfit_ctr >= self.cfg.overfit_patience:
                msg = (f"🔥 过拟合告警: 连续 {self.overfit_ctr} 块 ratio>{self.cfg.overfit_threshold} "
                       f"(当前={ratio:.2f})")
                self.warnings.append(msg)

        return msg

    @property
    def summary(self) -> dict:
        return {
            "best_iter": self.best_iter,
            "best_val_loss": self.best_val,
            "patience_counter": self.counter,
            "overfit_counter": self.overfit_ctr,
            "warnings": self.warnings,
        }


# ═══════════════════════════════════════════════════════════════
# Checkpoint 管理器
# ═══════════════════════════════════════════════════════════════
class CheckpointManager:
    """管理 adapter 目录中的 .safetensors checkpoints"""

    def __init__(self, adapter_dir: Path):
        self.adapter_dir = Path(adapter_dir)
        self.checkpoints: List[Tuple[int, float, Path]] = []  # (iter, val_loss, path)

    def scan(self) -> List[Tuple[int, float, Path]]:
        """扫描目录，返回按 iter 排序的 checkpoint 列表"""
        if not self.adapter_dir.exists():
            return []

        items = []
        for f in sorted(self.adapter_dir.glob("*_adapters.safetensors")):
            if f.name == "adapters.safetensors":
                continue
            try:
                iter_num = int(f.stem.split("_")[0])
                # 估算 val_loss: 从文件名或最近的 log 推断
                items.append((iter_num, float('inf'), f))
            except (ValueError, IndexError):
                continue

        items.sort(key=lambda x: x[0])
        self.checkpoints = items
        return items

    def find_best(self, records: List[IterRecord]) -> Optional[Tuple[int, float, Path]]:
        """根据 records 找到最优 checkpoint 对应的文件"""
        if not records:
            return None

        # 找 val_loss 最低的 record
        val_records = [(r.iter_num, r.val_loss) for r in records if r.val_loss is not None]
        if not val_records:
            return None

        best_iter, best_val = min(val_records, key=lambda x: x[1])

        # 在 checkpoints 中找最接近的
        self.scan()
        best_match = None
        min_dist = float('inf')
        for ckpt_iter, _, ckpt_path in self.checkpoints:
            dist = abs(ckpt_iter - best_iter)
            if dist < min_dist:
                min_dist = dist
                best_match = (ckpt_iter, best_val, ckpt_path)

        return best_match

    def backup_best(self, best_checkpoint: Tuple[int, float, Path]) -> Path:
        """备份最优 checkpoint 到 adapter_best/"""
        best_dir = self.adapter_dir.parent / "adapter_best"
        best_dir.mkdir(parents=True, exist_ok=True)

        _, _, src = best_checkpoint
        # 复制 adapter 文件
        for f in self.adapter_dir.glob("*.safetensors"):
            if f.name == src.name or f.name == "adapters.safetensors":
                shutil.copy2(f, best_dir / f.name)
        # 复制 config
        config_file = self.adapter_dir / "adapter_config.json"
        if config_file.exists():
            shutil.copy2(config_file, best_dir / "adapter_config.json")

        return best_dir


# ═══════════════════════════════════════════════════════════════
# 可视化
# ═══════════════════════════════════════════════════════════════
def plot_loss_curves(records: List[IterRecord], output_path: Path,
                     best_iter: int = 0, best_val: float = float('inf'),
                     warnings: List[str] = None):
    """绘制 loss 曲线"""
    if not HAS_MPL:
        logging.warning("⚠️  matplotlib 未安装，跳过图表生成")
        return

    # 数据
    train_iters = [r.iter_num for r in records]
    train_losses = [r.train_loss for r in records]
    val_pairs = [(r.iter_num, r.val_loss) for r in records if r.val_loss is not None]
    val_iters = [p[0] for p in val_pairs]
    val_losses = [p[1] for p in val_pairs]

    # 过拟合比率
    ratio_iters = []
    ratios = []
    for r in records:
        if r.overfit_ratio is not None:
            ratio_iters.append(r.iter_num)
            ratios.append(r.overfit_ratio)

    # 画布
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})
    fig.suptitle(f'龍魂 LoRA 训练曲线 · {P0["dna"]}', fontsize=13, fontweight='bold', y=0.98)

    # ── 上图: Loss 曲线 ──
    ax1.plot(train_iters, train_losses, color='#1a73e8', alpha=0.4, linewidth=0.8, label='Train Loss')
    # 平滑 train loss (窗口=5)
    if len(train_losses) >= 5:
        smooth = []
        for i in range(len(train_losses)):
            w = train_losses[max(0,i-2):min(len(train_losses),i+3)]
            smooth.append(sum(w)/len(w))
        ax1.plot(train_iters, smooth, color='#1a73e8', linewidth=1.5, alpha=0.9, label='Train Loss (平滑)')

    if val_iters:
        ax1.plot(val_iters, val_losses, 'o-', color='#ea4335', linewidth=2, markersize=5,
                 label='Val Loss', zorder=5)
        # 标注最优点
        if best_iter > 0 and best_val < float('inf'):
            ax1.axvline(x=best_iter, color='#34a853', linestyle='--', linewidth=1.5, alpha=0.8)
            ax1.annotate(f'Best: Iter{best_iter}\nVal={best_val:.4f}',
                        xy=(best_iter, best_val), xytext=(best_iter + 15, best_val + 0.05),
                        arrowprops=dict(arrowstyle='->', color='#34a853', lw=1.5),
                        fontsize=10, color='#34a853', fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='#e8f5e9', alpha=0.8))

    ax1.set_ylabel('Loss', fontsize=12)
    ax1.legend(loc='upper right', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(left=0)

    # ── 下图: 过拟合比率 ──
    if ratio_iters:
        ax2.fill_between(ratio_iters, 1.0, ratios, alpha=0.15, color='#f9ab00')
        ax2.plot(ratio_iters, ratios, color='#f9ab00', linewidth=1.2, label='Val/Train Ratio')
        ax2.axhline(y=2.0, color='#ea4335', linestyle='--', linewidth=1, alpha=0.6, label='过拟合警戒线 (2.0)')
        ax2.fill_between(ratio_iters, 2.0, max(ratios + [2.0]) + 0.5,
                         alpha=0.08, color='#ea4335', label='过拟合危险区')
        ax2.set_ylabel('Val/Train Ratio', fontsize=11)
        ax2.set_xlabel('Iteration', fontsize=12)
        ax2.legend(loc='upper right', fontsize=9)
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(left=0)
    else:
        ax2.text(0.5, 0.5, '无验证 loss 数据', ha='center', va='center',
                 transform=ax2.transAxes, fontsize=14, color='#9aa0a6')
        ax2.set_xlabel('Iteration', fontsize=12)

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    logging.info(f"📊 图表已保存: {output_path}")


# ═══════════════════════════════════════════════════════════════
# 报告生成
# ═══════════════════════════════════════════════════════════════
def generate_report(records: List[IterRecord], analyzer: Analyzer,
                    cfg: MonitorConfig, output_dir: Path) -> Path:
    """生成 Markdown + JSON 双格式报告"""
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    s = analyzer.summary
    n = len(records)
    train_losses = [r.train_loss for r in records]
    val_losses = [r.val_loss for r in records if r.val_loss is not None]

    # 计算统计量
    val_start = val_losses[0] if val_losses else None
    val_end = val_losses[-1] if val_losses else None
    val_trend = "↓ 改善" if (val_start and val_end and val_end < val_start) else "↑ 恶化" if (val_start and val_end and val_end > val_start) else "— 持平"

    # 过拟合统计
    overfit_iters = [r for r in records if r.overfit_ratio and r.overfit_ratio > cfg.overfit_threshold]

    md = f"""# 龍魂 LoRA 训练监控报告

> **DNA**: {P0["dna"]}
> **确认**: {P0["confirm"]}
> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (农历 丙午·乙申·庚戌·巳时)

---

## 一、训练概览

| 指标 | 值 |
|:---|---|
| 总迭代数 | {n} |
| 训练 loss 初值 | {train_losses[0]:.4f} |
| 训练 loss 终值 | {train_losses[-1]:.4f} |
| 训练 loss 改善 | {(train_losses[0] - train_losses[-1]) / train_losses[0] * 100:.1f}% |
| 验证 loss 初值 | {val_start:.4f} if val_start else 'N/A' |
| 验证 loss 终值 | {val_end:.4f} if val_end else 'N/A' |
| 验证趋势 | {val_trend} |

## 二、最优结果

| 指标 | 值 |
|:---|---|
| 最优迭代 | Iter {s['best_iter']} |
| 最优验证 loss | {s['best_val_loss']:.4f} |
| 不改善计数器 | {s['patience_counter']} / {cfg.patience} |
| 过拟合计数器 | {s['overfit_counter']} / {cfg.overfit_patience} |

## 三、过拟合检测

| 指标 | 值 |
|:---|---|
| 过拟合阈值 | val/train > {cfg.overfit_threshold} |
| 过拟合迭代数 | {len(overfit_iters)} / {n} ({len(overfit_iters)/n*100:.1f}%) |
| 最大过拟合比率 | {max([r.overfit_ratio for r in records if r.overfit_ratio], default=0):.2f} |
| 过拟合集中区间 | 分析中... |

## 四、告警

"""
    if s['warnings']:
        for w in s['warnings']:
            md += f"- {w}\n"
    else:
        md += "✅ 无告警，训练健康。\n"

    md += f"""
## 五、P0焊死底座 · 12条铁律声明

本报告遵循 `{P0["protocol_path"]}` 全部12条：

| # | 铁律 | 本报告合规 |
|:---:|------|:---:|
| 1 | {P0["serve_the_people"]} | ✅ |
| 2 | {P0["china_law"]} | ✅ |
| 3 | {P0["data_sovereignty"]} | ✅ 本地存储 |
| 4 | {P0["knowledge_sharing"]} | ✅ 开源审计 |
| 5 | {P0["robots_txt"]} | ✅ 不涉及爬虫 |
| 6 | {P0["request_rate"]} | ✅ 无外部API调用 |
| 7 | {P0["dna_audit"]} | ✅ DNA嵌入本报告 |
| 8 | {P0["creator_inviolable"]} | ✅ |
| 9 | {P0["daughter_never_mortgage"]} | ✅ |
| 10 | {P0["zero_blackbox"]} | ✅ 全逻辑在 lh_early_stop.py |
| 11 | {P0["no_delete_freeze"]} | ✅ 历史报告不删除 |
| 12 | {P0["no_replace_commercial"]} | ✅ 不商业化 |

---

> 🐉 龍魂已烙 · {P0["dna"]}
> {P0["confirm"]}
"""

    # 写入
    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / f"training_monitor_report_{ts}.md"
    md_path.write_text(md, encoding='utf-8')

    # JSON
    json_data = {
        "dna": P0["dna"],
        "confirm": P0["confirm"],
        "timestamp": datetime.now().isoformat(),
        "summary": analyzer.summary,
        "stats": {
            "total_iters": n,
            "train_loss_start": train_losses[0],
            "train_loss_end": train_losses[-1],
            "val_loss_start": val_start,
            "val_loss_end": val_end,
            "val_trend": val_trend,
            "overfit_iter_count": len(overfit_iters),
        },
        "config": {
            "patience": cfg.patience,
            "overfit_threshold": cfg.overfit_threshold,
            "val_steps": cfg.val_steps,
        },
    }
    json_path = output_dir / f"training_monitor_report_{ts}.json"
    json_path.write_text(json.dumps(json_data, indent=2, ensure_ascii=False), encoding='utf-8')

    logging.info(f"📝 报告已保存: {md_path}")
    return md_path


# ═══════════════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════════════
def run_replay(log_file: str, cfg: MonitorConfig):
    """从日志文件重放分析"""
    parser = LogParser()
    records = parser.parse_file(log_file)
    _run_analysis(records, cfg)


def run_follow(cfg: MonitorConfig):
    """实时尾随 stdin"""
    parser = LogParser()
    analyzer = Analyzer(cfg)
    records: List[IterRecord] = []

    print(f"🐉 龍魂训练监控器 v1.1 启动", flush=True)
    print(f"   DNA: {P0['dna']}", flush=True)
    print(f"   早停: patience={cfg.patience}, overfit>{cfg.overfit_threshold}", flush=True)
    print(f"   等待训练输出...\n", flush=True)

    try:
        for record in parser.parse_stream(sys.stdin):
            records.append(record)
            msg = analyzer.check(record)

            # 状态行
            parts = [f"Iter {record.iter_num:4d}", f"train={record.train_loss:.4f}"]
            if record.val_loss is not None:
                parts.append(f"val={record.val_loss:.4f}")
                r = record.overfit_ratio
                if r:
                    flag = "⚠️" if r > cfg.overfit_threshold else "  "
                    parts.append(f"ratio={r:.2f}{flag}")
            parts.append(f"cnt={analyzer.counter}/{cfg.patience}")
            if analyzer.overfit_ctr > 0:
                parts.append(f"of={analyzer.overfit_ctr}/{cfg.overfit_patience}")
            print(" | ".join(parts), flush=True)

            if msg:
                print(f"   {msg}", flush=True)

    except KeyboardInterrupt:
        print("\n⏸️  监控中断", flush=True)

    _run_analysis(records, cfg)


def run_analyze(adapter_dir: str, cfg: MonitorConfig):
    """训练后分析已有 adapter 目录"""
    adapter_path = Path(adapter_dir)
    if not adapter_path.exists():
        logging.error(f"❌ adapter 目录不存在: {adapter_dir}")
        sys.exit(1)

    ckpt_mgr = CheckpointManager(adapter_path)
    ckpts = ckpt_mgr.scan()

    print(f"🐉 训练后分析")
    print(f"   目录: {adapter_path}")
    print(f"   Checkpoints: {len(ckpts)} 个")
    for ckpt_iter, _, ckpt_path in ckpts:
        size_mb = ckpt_path.stat().st_size / 1024 / 1024
        print(f"      Iter {ckpt_iter:4d} → {ckpt_path.name} ({size_mb:.1f}MB)")

    # 查找 adapter_best
    best_dir = adapter_path.parent / "adapter_best"
    if best_dir.exists():
        best_files = list(best_dir.glob("*"))
        print(f"\n   adapter_best/ 已存在: {len(best_files)} 文件")
        for f in best_files:
            print(f"      {f.name}")
    else:
        print(f"\n   ⚠️  adapter_best/ 不存在（训练器可能未完成或未触发早停最佳保存）")

    # 检查是否有训练日志
    log_candidates = sorted(
        list(cfg.log_dir.glob("*.log")) + list(PROJECT_ROOT.glob("*.log")),
        key=lambda p: p.stat().st_mtime, reverse=True
    )
    if log_candidates:
        latest_log = log_candidates[0]
        print(f"\n   最近日志: {latest_log}")
        print(f"   建议: python3 bin/lh_early_stop.py replay --log-file {latest_log}")


def _run_analysis(records: List[IterRecord], cfg: MonitorConfig):
    """共用分析管线"""
    if not records:
        logging.warning("⚠️  无训练记录")
        return

    analyzer = Analyzer(cfg)
    for r in records:
        analyzer.check(r)

    s = analyzer.summary
    n = len(records)
    val_records = [r for r in records if r.val_loss is not None]

    print(f"\n{'='*60}")
    print(f"🐉 训练分析完成")
    print(f"{'='*60}")
    print(f"   总迭代: {n}")
    print(f"   验证点: {len(val_records)}")
    print(f"   最优: Iter {s['best_iter']}, val_loss={s['best_val_loss']:.4f}")
    print(f"   训练loss: {records[0].train_loss:.4f} → {records[-1].train_loss:.4f}")
    if val_records:
        print(f"   验证loss: {val_records[0].val_loss:.4f} → {val_records[-1].val_loss:.4f}")
    print(f"   早停计数: {s['patience_counter']}/{cfg.patience}")
    print(f"   过拟合计数: {s['overfit_counter']}/{cfg.overfit_patience}")
    if s['warnings']:
        for w in s['warnings']:
            print(f"   {w}")
    print(f"{'='*60}")

    # 可视化
    plot_path = cfg.report_dir / "training_loss_curves.png"
    plot_loss_curves(records, plot_path, s['best_iter'], s['best_val_loss'], s['warnings'])

    # 报告
    generate_report(records, analyzer, cfg, cfg.report_dir)

    # 扫描 checkpoint
    ckpt_mgr = CheckpointManager(cfg.adapter_dir)
    best_ckpt = ckpt_mgr.find_best(records)
    if best_ckpt:
        print(f"\n📦 最优 checkpoint: Iter {best_ckpt[0]}, {best_ckpt[2].name}")
        # 自动备份
        if cfg.adapter_dir.exists():
            ckpt_mgr.backup_best(best_ckpt)
            print(f"   💾 已备份到 adapter_best/")


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(
        description="龍魂 · 训练监控与最优提取协议 v1.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_lora_trainer.py train 2>&1 | python3 bin/lh_early_stop.py follow
  python3 bin/lh_early_stop.py replay --log-file logs/train.log
  python3 bin/lh_early_stop.py analyze --adapter-dir models/longhun-v1.0/lora_output/adapter_v3.2
        """
    )
    sub = parser.add_subparsers(dest='command', help='子命令')

    # follow
    p_follow = sub.add_parser('follow', help='实时尾随 stdin')
    _add_common_args(p_follow)

    # replay
    p_replay = sub.add_parser('replay', help='从日志文件重放')
    p_replay.add_argument('--log-file', required=True, help='训练日志文件')
    _add_common_args(p_replay)

    # analyze
    p_analyze = sub.add_parser('analyze', help='分析已有 adapter 目录')
    p_analyze.add_argument('--adapter-dir', required=True, help='adapter 目录路径')
    _add_common_args(p_analyze, skip_paths=True)

    # plot (仅可视化)
    p_plot = sub.add_parser('plot', help='仅生成可视化图表')
    p_plot.add_argument('--log-file', required=True, help='训练日志文件')
    p_plot.add_argument('--output', default=None, help='输出图片路径')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 构建配置
    cfg = MonitorConfig(
        patience=getattr(args, 'patience', 2),
        min_delta=getattr(args, 'min_delta', 0.0005),
        overfit_threshold=getattr(args, 'overfit_threshold', 2.5),
        overfit_patience=getattr(args, 'overfit_patience', 3),
        adapter_dir=Path(getattr(args, 'adapter_dir', DEFAULT_ADAPTER_DIR)) if hasattr(args, 'adapter_dir') else DEFAULT_ADAPTER_DIR,
        report_dir=Path(getattr(args, 'report_dir', DEFAULT_REPORT_DIR)) if hasattr(args, 'report_dir') else DEFAULT_REPORT_DIR,
        log_dir=Path(getattr(args, 'log_dir', DEFAULT_LOG_DIR)) if hasattr(args, 'log_dir') else DEFAULT_LOG_DIR,
    )

    # 日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        handlers=[logging.StreamHandler(sys.stderr)]
    )

    if args.command == 'follow':
        run_follow(cfg)
    elif args.command == 'replay':
        run_replay(args.log_file, cfg)
    elif args.command == 'analyze':
        run_analyze(args.adapter_dir, cfg)
    elif args.command == 'plot':
        records = LogParser().parse_file(args.log_file)
        output = Path(args.output) if args.output else cfg.report_dir / "training_loss_curves.png"
        analyzer = Analyzer(cfg)
        for r in records:
            analyzer.check(r)
        s = analyzer.summary
        plot_loss_curves(records, output, s['best_iter'], s['best_val_loss'])
        print(f"📊 图表已保存: {output}")


def _add_common_args(p, skip_paths=False):
    p.add_argument('--patience', type=int, default=2, help='早停耐心块数 (default: 2)')
    p.add_argument('--min-delta', type=float, default=0.0005, help='最小改善阈值')
    p.add_argument('--overfit-threshold', type=float, default=2.5, help='过拟合比率阈值')
    p.add_argument('--overfit-patience', type=int, default=3, help='过拟合强制告警块数')
    if not skip_paths:
        p.add_argument('--adapter-dir', default=str(DEFAULT_ADAPTER_DIR), help='adapter 输出目录')
        p.add_argument('--report-dir', default=str(DEFAULT_REPORT_DIR), help='报告输出目录')
        p.add_argument('--log-dir', default=str(DEFAULT_LOG_DIR), help='日志目录')


if __name__ == "__main__":
    main()

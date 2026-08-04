# 龍魂系统 · 工程实现层
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 文化归属: 思想框架归龍魂核心思想层 (CC BY-NC-SA 4.0)
# DNA: #龍芯⚡️丙午·癸未·甲申-DIGITAL-FLOW-FIELD-PARTICLE-v2.0-UID9622
# 署名: UID9622（诸葛鑫·Lucky）

"""粒子流场引擎。

把文本字符映射为二维空间中的彩色粒子，通过中心引力、随机扰动与边界反弹
模拟“文字流动”的视觉效果。
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np

from .color_schemes import get_color
from .core import char_digital_root


@dataclass
class ParticleSnapshot:
    """单个粒子的可序列化快照。"""

    index: int
    char: str
    root: int
    color: str
    x: float
    y: float


class ParticleSystem:
    """数字流场粒子系统。"""

    def __init__(self, max_particles: int = 3000, trail_length: int = 20):
        self.max_particles = max(10, int(max_particles))
        self.trail_length = max(0, int(trail_length))
        self.text: str = ""
        self.chars: List[str] = []
        self.roots: np.ndarray = np.zeros(0, dtype=int)
        self.pos: np.ndarray = np.zeros((0, 2), dtype=float)
        self.vel: np.ndarray = np.zeros((0, 2), dtype=float)
        self.colors: List[str] = []
        self.history: List[deque] = []
        self._initialized: bool = False

    @property
    def n(self) -> int:
        return self.roots.shape[0]

    def load_text(self, text: str, scheme: str = "nine") -> "ParticleSystem":
        """加载文本并初始化粒子。"""
        self.text = text or ""
        pairs = [(ch, char_digital_root(ch)) for ch in self.text if ch.strip() or ch]
        pairs = [(ch, r) for ch, r in pairs if r != 0]

        if not pairs:
            self._reset()
            return self

        if len(pairs) > self.max_particles:
            step = max(1, len(pairs) // self.max_particles)
            pairs = pairs[::step][: self.max_particles]

        n = len(pairs)
        self.chars = [ch for ch, _ in pairs]
        self.roots = np.array([r for _, r in pairs], dtype=int)
        self.pos = np.zeros((n, 2), dtype=float)
        self.vel = np.zeros((n, 2), dtype=float)
        self.colors = [get_color(r, scheme) for r in self.roots]
        self.history = [deque(maxlen=self.trail_length) for _ in range(n)]

        for idx in range(n):
            angle = 2.0 * np.pi * idx / n
            radius = 0.3 + 0.3 * (idx / n)
            self.pos[idx] = [
                0.5 + radius * np.cos(angle),
                0.5 + radius * np.sin(angle),
            ]
            speed = 0.3 + (self.roots[idx] / 9.0) * 0.7
            # 初始切向速度，形成自然涡流
            self.vel[idx] = [
                speed * np.cos(angle + np.pi / 2.0),
                speed * np.sin(angle + np.pi / 2.0),
            ]
            self.history[idx].append(tuple(self.pos[idx]))

        self._initialized = True
        return self

    def _reset(self) -> None:
        self.chars = []
        self.roots = np.zeros(0, dtype=int)
        self.pos = np.zeros((0, 2), dtype=float)
        self.vel = np.zeros((0, 2), dtype=float)
        self.colors = []
        self.history = []
        self._initialized = False

    def update(
        self,
        speed: float = 1.0,
        center_gravity: float = 0.3,
        noise: float = 0.02,
        dt: float = 0.05,
        steps: int = 1,
    ) -> "ParticleSystem":
        """推进粒子系统若干步。"""
        if not self._initialized or self.n == 0:
            return self

        speed = max(0.1, float(speed))
        center_gravity = max(0.0, min(1.0, float(center_gravity)))
        noise = max(0.0, float(noise))
        dt_eff = dt * speed
        center = np.array([0.5, 0.5])
        margin = 0.02
        max_speed = 1.5

        for _ in range(steps):
            # 中心引力 + 随机扰动
            force = (center - self.pos) * center_gravity
            self.vel += (force + np.random.uniform(-noise, noise, size=self.vel.shape)) * dt_eff
            # 阻尼与限速
            speeds = np.linalg.norm(self.vel, axis=1, keepdims=True)
            self.vel = np.where(speeds > max_speed, self.vel / speeds * max_speed, self.vel)
            self.vel *= 0.99

            self.pos += self.vel * dt_eff

            # 边界反弹
            under = self.pos < margin
            over = self.pos > (1.0 - margin)
            self.pos = np.where(under, margin + (margin - self.pos), self.pos)
            self.pos = np.where(over, (1.0 - margin) - (self.pos - (1.0 - margin)), self.pos)
            self.vel = np.where(under | over, -self.vel * 0.8, self.vel)

            for i in range(self.n):
                self.history[i].append(tuple(self.pos[i]))

        return self

    def counts(self) -> List[int]:
        """返回数字根 1-9 的计数。"""
        counts = [0] * 10
        if self.n == 0:
            return counts
        unique, cnt = np.unique(self.roots, return_counts=True)
        for u, c in zip(unique.tolist(), cnt.tolist()):
            counts[u] = c
        return counts

    def render(
        self,
        show_trail: bool = True,
        show_labels: bool = False,
        show_hud: bool = True,
        particle_scale: float = 1.0,
        figsize: Tuple[int, int] = (8, 8),
    ):
        """渲染当前帧并返回 matplotlib Figure。"""
        import matplotlib.pyplot as plt

        # 优先使用支持中文的系统字体，避免 HUD 中文乱码/警告
        plt.rcParams["font.sans-serif"] = [
            "Hiragino Sans GB",
            "Heiti SC",
            "PingFang SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ]
        plt.rcParams["axes.unicode_minus"] = False

        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_facecolor("#0a0a1a")
        ax.set_facecolor("#0a0a1a")
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.0, 1.0)
        ax.set_aspect("equal")

        # T0 金锚
        anchor = plt.Circle((0.5, 0.5), 0.03, color="gold", alpha=0.3, zorder=1)
        ax.add_patch(anchor)

        # 轨迹
        if show_trail and self.trail_length > 0:
            for i, hist in enumerate(self.history):
                if len(hist) > 1:
                    xs, ys = zip(*hist)
                    ax.plot(xs, ys, color=self.colors[i], alpha=0.15, linewidth=0.5, zorder=2)

        # 粒子大小：5 最大，向两端递减；再应用用户缩放
        particle_scale = max(0.1, float(particle_scale))
        sizes = (3 + 6 * (1.0 - np.abs(self.roots - 5) / 4.0)) * particle_scale
        ax.scatter(
            self.pos[:, 0],
            self.pos[:, 1],
            c=self.colors,
            s=sizes,
            edgecolors="white",
            linewidths=0.3,
            zorder=3,
        )

        # 字符标签
        if show_labels:
            for i, ch in enumerate(self.chars):
                ax.text(
                    self.pos[i, 0],
                    self.pos[i, 1],
                    ch,
                    color="white",
                    fontsize=6,
                    ha="center",
                    va="center",
                    zorder=4,
                )

        # HUD
        if show_hud:
            counts = self.counts()
            hud = f"粒子: {self.n}  |  " + "  ".join(f"{i}:{counts[i]}" for i in range(1, 10))
            ax.text(0.02, 0.98, hud, color="white", fontsize=9, va="top", transform=ax.transAxes)

        ax.axis("off")
        plt.tight_layout()
        return fig

    def to_dict(self, limit: int = 500) -> List[dict]:
        """导出粒子快照列表。"""
        limit = min(limit, self.n)
        snapshots = []
        for i in range(limit):
            snapshots.append(
                {
                    "index": i,
                    "char": self.chars[i],
                    "root": int(self.roots[i]),
                    "color": self.colors[i],
                    "x": round(float(self.pos[i, 0]), 6),
                    "y": round(float(self.pos[i, 1]), 6),
                }
            )
        return snapshots

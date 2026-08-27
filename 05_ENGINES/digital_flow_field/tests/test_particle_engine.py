# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍魂系统 · 工程实现层
# License: MulanPSL v2
# DNA: #龍芯⚡️丙午·癸未·甲申·庚午·䷙大畜-DIGITAL-FLOW-FIELD-TEST-PARTICLE-v2.0-UID9622

import numpy as np
import pytest

from flow_engine.particle_engine import ParticleSystem


def test_empty_text():
    ps = ParticleSystem()
    ps.load_text("")
    assert ps.n == 0
    assert not ps._initialized


def test_load_text_limits_particles():
    ps = ParticleSystem(max_particles=10)
    ps.load_text("龍魂系统" * 100)
    assert ps.n <= 10
    assert ps.n > 0


def test_positions_within_bounds():
    ps = ParticleSystem(max_particles=50)
    ps.load_text("道可道非常道" * 20)
    ps.update(steps=100)
    assert np.all(ps.pos >= 0.0)
    assert np.all(ps.pos <= 1.0)


def test_counts_match_roots():
    ps = ParticleSystem()
    ps.load_text("12345")
    counts = ps.counts()
    # 5 个非空字符都应产生有效粒子
    assert sum(counts) == 5
    # 每个字符的数字根在 1-9 之间
    assert all(counts[i] >= 0 for i in range(1, 10))
    assert ps.n == 5


def test_to_dict_limit():
    ps = ParticleSystem(max_particles=50)
    ps.load_text("甲乙丙丁戊己庚辛壬癸" * 5)
    snapshots = ps.to_dict(limit=10)
    assert len(snapshots) == 10
    assert all("x" in s and "y" in s and "root" in s for s in snapshots)


def test_render_returns_figure():
    from matplotlib.figure import Figure

    ps = ParticleSystem()
    ps.load_text("龍魂数字流场")
    fig = ps.render()
    assert isinstance(fig, Figure)

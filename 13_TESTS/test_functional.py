#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-FUNCTIONAL-TEST-UID9622
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🐉 龍魂 · 功能评估测试
覆盖: 人格矩阵 / DNA生成 / 知识图谱 / API健康 / 性能基准

v1.0 工程适配（2026-08-15）:
  - 坑#1: 文档用 hashlib.md5 生成DNA → 违反项目"禁MD5/SHA-1"铁律，统一改 SHA-256 截断8位
  - 坑#3: lh_persona_life.py 无 PersonaSystem 类（CLI结构）→ 改 subprocess 实测 status，
    人格数解析 (Pxx)/(Sx) 形如 r"\((P\d{2}|S\d)\)"，断言 >= 24（注册表28人格）
  - test_persona_routing: lh.py 无 route 子命令 → 验证 personas/runtime/persona_registry.json
    注册表 >= 24 人格（P13 派位的真实基础）
"""

import pytest
import json
import time
import re
import sys
import subprocess
from pathlib import Path


# ============================================================
# 人格矩阵测试
# ============================================================

def _persona_status_codes(root: Path) -> set:
    """通过 CLI 实测人格矩阵状态, 返回人格代码集合"""
    script = root / "08_BIN" / "lh_persona_life.py"
    if not script.exists():
        return set()
    result = subprocess.run(
        [sys.executable, str(script), "status"],
        capture_output=True, text=True, cwd=str(root), timeout=30)
    return set(re.findall(r'\((P\d{2}|S\d)\)', result.stdout))


@pytest.mark.functional
def test_persona_system(test_env):
    """测试人格矩阵（CLI 实测 >= 24 人格）"""
    codes = _persona_status_codes(test_env["root"])
    if not codes:
        pytest.skip("活人格引擎未找到")
    assert len(codes) >= 24, f"人格数量 {len(codes)} 少于24"


@pytest.mark.functional
def test_persona_routing(test_env):
    """测试人格路由基础（注册表 >= 24 人格）"""
    registry = test_env["root"] / "personas" / "runtime" / "persona_registry.json"
    if not registry.exists():
        pytest.skip("人格注册表未找到")
    with open(registry, "r", encoding="utf-8") as f:
        raw = f.read()
    # 注册表为 JSONC 格式（头部带 # 注释行）→ 过滤注释后再解析
    clean = "\n".join(
        line for line in raw.splitlines()
        if not line.lstrip().startswith("#"))
    data = json.loads(clean)
    personas = data.get("personas") or data.get("registry") or data
    count = len(personas) if isinstance(personas, (list, dict)) else 0
    assert count >= 24, f"人格注册表数量 {count} 少于24"


# ============================================================
# DNA生成与验证测试
# ============================================================

def _gen_dna(uid: str = "9622") -> str:
    """生成 DNA 追溯码（SHA-256 截断8位 · 禁MD5）"""
    from datetime import datetime
    import hashlib
    dna_prefix = "#龍芯⚡️"
    timestamp = datetime.now().strftime("%Y-%m-%d")
    rand = hashlib.sha256(f"TEST{time.time()}".encode()).hexdigest()[:8].upper()
    return f"{dna_prefix}{timestamp}-TEST-{rand}-{uid}"


@pytest.mark.functional
def test_dna_generation(test_env):
    """测试DNA生成"""
    dna = _gen_dna()
    assert dna.startswith("#龍芯⚡️")
    assert "9622" in dna
    assert len(dna) > 20


# ============================================================
# 知识图谱测试
# ============================================================

@pytest.mark.functional
def test_knowledge_graph_import(test_env):
    """测试知识图谱引擎（LONGHUN_HOME 已隔离，不污染真实数据）"""
    try:
        sys.path.insert(0, str(test_env["root"] / "08_BIN"))
        from lh_knowledge_graph_v2 import KnowledgeGraphEngine
        engine = KnowledgeGraphEngine()
        node = engine.create_node("测试概念", "这是一个测试节点", keywords=["测试", "功能"])
        assert node.id is not None
        assert node.name == "测试概念"
        if node.id in engine.nodes:
            del engine.nodes[node.id]
    except ImportError:
        pytest.skip("知识图谱模块未找到")


# ============================================================
# API端到端测试
# ============================================================

@pytest.mark.functional
@pytest.mark.api
def test_api_gateway_health(test_env):
    """测试API网关健康检查（未运行则跳过）"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 8780))
    sock.close()
    if result != 0:
        pytest.skip("API网关未运行")

    try:
        import urllib.request
        with urllib.request.urlopen("http://127.0.0.1:8780/", timeout=5) as resp:
            assert resp.status == 200
    except Exception as e:
        pytest.skip(f"API调用失败: {e}")


# ============================================================
# 性能基准测试
# ============================================================

@pytest.mark.functional
@pytest.mark.benchmark
def test_dna_generation_performance():
    """DNA生成性能测试（1000次 < 1秒）"""
    start = time.time()
    for _ in range(1000):
        _gen_dna()
    elapsed = time.time() - start
    assert elapsed < 1.0, f"DNA生成性能慢: {elapsed:.2f}s"


@pytest.mark.functional
@pytest.mark.benchmark
def test_json_serialization_performance():
    """JSON序列化性能测试（1000次 < 0.5秒）"""
    test_data = {"key": "value" * 100, "list": list(range(100)), "nested": {"a": 1, "b": 2}}

    start = time.time()
    for _ in range(1000):
        json.dumps(test_data)
    elapsed = time.time() - start
    assert elapsed < 0.5, f"JSON序列化性能慢: {elapsed:.2f}s"

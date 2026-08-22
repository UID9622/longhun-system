#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 快速索引引擎测试
DNA: #龍芯⚡️丙午·丙申·壬戌·乙巳·䷾既济-FAST-INDEX-TEST-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
License: MulanPSL v2

覆盖: 上下文感知 / 向量索引 / 行为学习 / 协同涌现 / 无意识检索 / 核心编排
注意: 测试使用独立的 .state 子目录，不污染生产数据。
"""

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 强制测试使用独立 state 目录
TEST_STATE = PROJECT_ROOT / ".state_test_fast_index"
if TEST_STATE.exists():
    shutil.rmtree(TEST_STATE)
TEST_STATE.mkdir(parents=True, exist_ok=True)
os.environ["LH_FAST_INDEX_STATE"] = str(TEST_STATE)

# 补丁：让引擎使用测试 state
from engines import lh_context_engine, lh_vector_index, lh_behavior_learner, lh_collective_intel, lh_implicit_retrieval, lh_fast_index_core

lh_context_engine.STATE_DIR = TEST_STATE / "context_engine"
lh_context_engine.STATE_DIR.mkdir(parents=True, exist_ok=True)
lh_vector_index.DATA_DIR = TEST_STATE / "vector_index"
lh_vector_index.DATA_DIR.mkdir(parents=True, exist_ok=True)
lh_vector_index.DB_PATH = lh_vector_index.DATA_DIR / "vectors.sqlite"
lh_behavior_learner.DATA_DIR = TEST_STATE / "behavior_learner"
lh_behavior_learner.DATA_DIR.mkdir(parents=True, exist_ok=True)
lh_behavior_learner.DB_PATH = lh_behavior_learner.DATA_DIR / "behavior.sqlite"
lh_collective_intel.DATA_DIR = TEST_STATE / "collective_intel"
lh_collective_intel.DATA_DIR.mkdir(parents=True, exist_ok=True)
lh_collective_intel.DB_PATH = lh_collective_intel.DATA_DIR / "collective.sqlite"
lh_implicit_retrieval.DATA_DIR = TEST_STATE / "implicit_retrieval"
lh_implicit_retrieval.DATA_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture
def sample_docs(tmp_path):
    """创建临时文档集"""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "index_philosophy.md").write_text(
        "索引不是分类学，而是认知学。多维锚定让文件记住人。", encoding="utf-8"
    )
    (docs_dir / "sovereign_gateway.md").write_text(
        "主权网关自动硬控协议。Kimi 装死就切换 DeepSeek。", encoding="utf-8"
    )
    (docs_dir / "developer_kg.md").write_text(
        "开发者知识图谱包含 L0 到 L5 六层结构。", encoding="utf-8"
    )
    return docs_dir


# ============================================================
# 上下文感知引擎
# ============================================================

def test_capture_context_has_basic_fields():
    ctx = lh_context_engine.capture_context()
    assert "dna" in ctx
    assert "timestamp" in ctx
    assert "cwd" in ctx
    assert "recent_files" in ctx
    assert ctx["dna"].startswith("#龍芯⚡️")


def test_save_and_load_context():
    ctx = lh_context_engine.capture_context(extra={"test": True})
    path = lh_context_engine.save_context(ctx, label="test")
    assert path.exists()
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["test"] is True


# ============================================================
# 向量索引引擎
# ============================================================

def test_vector_index_directory(sample_docs):
    idx = lh_vector_index.VectorIndex()
    stats = idx.index_directory(sample_docs, pattern="*.md")
    assert stats["total"] == 3
    # 至少成功索引 2 个
    assert stats["indexed"] + stats["unchanged"] >= 2


def test_vector_search_keyword_fallback(sample_docs):
    idx = lh_vector_index.VectorIndex()
    idx.index_directory(sample_docs, pattern="*.md")
    results = idx.search("认知学")
    assert isinstance(results, list)
    # 关键词降级模式下应命中 "index_philosophy.md"
    paths = [r["path"] for r in results]
    assert any("index_philosophy" in p for p in paths)


def test_vector_stats():
    idx = lh_vector_index.VectorIndex()
    s = idx.stats()
    assert "total_files" in s
    assert "embedding_mode" in s


# ============================================================
# 行为学习引擎
# ============================================================

def test_behavior_record_and_top():
    learner = lh_behavior_learner.BehaviorLearner()
    learner.record("file1", "file", "测试文件A", duration=60, weight_delta=2.0)
    learner.record("file2", "file", "测试文件B", duration=30, weight_delta=1.0)
    top = learner.top_items(item_type="file", limit=10)
    assert len(top) == 2
    assert top[0]["name"] == "测试文件A"


def test_behavior_decay_refresh():
    learner = lh_behavior_learner.BehaviorLearner()
    learner.record("old", "file", "旧文件", weight_delta=1.0)
    n = learner.refresh_weights()
    assert n >= 1


# ============================================================
# 协同涌现引擎
# ============================================================

def test_collective_session_and_related():
    ci = lh_collective_intel.CollectiveIntel()
    ci.add_session("sess-1", ["fileA", "fileB", "fileC"])
    ci.add_session("sess-2", ["fileA", "fileB", "fileD"])
    related = ci.related_items("fileA", limit=10)
    names = [r["item"] for r in related]
    assert "fileB" in names


def test_collective_clusters():
    ci = lh_collective_intel.CollectiveIntel()
    ci.add_session("sess-1", ["a", "b", "c"])
    ci.add_session("sess-2", ["a", "b"])
    clusters = ci.discover_clusters(min_support=1)
    assert len(clusters) >= 1


def test_collective_best_path():
    ci = lh_collective_intel.CollectiveIntel()
    # 用唯一名称避免跨测试污染
    ci.add_session("path-sess-1", ["path-a", "path-b"])
    ci.add_session("path-sess-2", ["path-b", "path-c"])
    path = ci.best_path("path-a", "path-c")
    assert path == ["path-a", "path-b", "path-c"]


# ============================================================
# 无意识检索引擎
# ============================================================

def test_implicit_push_returns_structure():
    engine = lh_implicit_retrieval.ImplicitRetrieval()
    result = engine.push(top_k=5)
    assert "dna" in result
    assert "recommendations" in result
    assert "context" in result


def test_implicit_feedback():
    engine = lh_implicit_retrieval.ImplicitRetrieval()
    engine.record_feedback("file1", helpful=True)
    # 不抛异常即通过


# ============================================================
# 核心编排器
# ============================================================

def test_core_init():
    core = lh_fast_index_core.FastIndexCore()
    result = core.init_system()
    assert result["status"] == "initialized"


def test_core_index_and_search(sample_docs):
    core = lh_fast_index_core.FastIndexCore()
    core.init_system()
    idx_result = core.index_project(sample_docs, pattern="*.md")
    assert idx_result["vector_stats"]["total"] == 3
    search_result = core.search("认知学", top_k=5)
    assert len(search_result["results"]) > 0


def test_core_dashboard():
    core = lh_fast_index_core.FastIndexCore()
    board = core.dashboard()
    assert "vector" in board
    assert "behavior" in board
    assert "collective" in board


# ============================================================
# 清理
# ============================================================

def teardown_module():
    if TEST_STATE.exists():
        shutil.rmtree(TEST_STATE)

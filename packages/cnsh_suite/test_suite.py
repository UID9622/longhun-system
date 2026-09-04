# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 套件 · 完整测试
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-CNSH-TEST-UID9622

用法:
  python -m pytest test_suite.py -v
"""

import sys
import json
import pytest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cnsh_suite.core import CNSHSuite, CNSHEngine, generate_dna
from cnsh_suite.tools import DNAGenerator, TricolorAuditor, CNSHExecutor
from cnsh_suite.agents import PersonaRouter

# ============================================================
# 工具测试
# ============================================================

def test_dna_generator():
    """测试DNA生成器"""
    tool = DNAGenerator()
    result = tool.execute(content="测试内容", type="DOCUMENT")
    assert result["success"] is True
    assert result["dna"].startswith("#龍芯⚡️")
    assert "UID9622" in result["dna"]
    assert result["parsed"]["uid"] == "9622"

def test_dna_generator_empty_content():
    """测试空内容"""
    tool = DNAGenerator()
    with pytest.raises(Exception):
        tool.execute(content="")

def test_tricolor_auditor():
    """测试三色审计"""
    tool = TricolorAuditor()
    result = tool.execute(content="测试内容")
    assert result["success"] is True
    assert result["tricolor"] in ["🟢", "🟡", "🔴"]
    assert "score" in result
    assert "dimensions" in result

def test_cnsh_executor():
    """测试CNSH执行器"""
    tool = CNSHExecutor()
    script = """
    设 名字 为 龍魂
    输出 你好，${名字}
    """
    result = tool.execute(script=script)
    assert result["success"] is True
    assert "你好，龍魂" in result["output"]
    assert "dna" in result

# ============================================================
# Agent测试
# ============================================================

def test_persona_router():
    """测试人格路由"""
    router = PersonaRouter()
    result = router.execute("帮我做战略决策")
    assert result["success"] is True
    assert result["persona"]["id"] == "zhugeliang"

    result = router.execute("测试系统安全")
    assert result["success"] is True
    assert result["persona"]["id"] == "laowantong"

# ============================================================
# 集成测试
# ============================================================

def test_suite():
    """测试完整套件"""
    suite = CNSHSuite()
    result = suite.execute("生成DNA: 集成测试")
    assert result["success"] is True

    result = suite.execute("审计内容: 集成测试内容")
    assert result["success"] is True

    result = suite.execute("运行CNSH: 输出 '集成测试通过'")
    assert result["success"] is True

def test_suite_status():
    """测试状态查询"""
    suite = CNSHSuite()
    status = suite.get_status()
    assert "dna" in status
    assert "engine" in status
    assert "tools" in status["engine"]

# ============================================================
# 性能测试
# ============================================================

def test_dna_performance():
    """DNA生成性能测试"""
    import time
    tool = DNAGenerator()
    start = time.time()
    for i in range(100):
        tool.execute(content=f"测试{i}", type="DOCUMENT")
    elapsed = time.time() - start
    assert elapsed < 2.0  # 100次生成应在2秒内

def test_audit_performance():
    """审计性能测试"""
    import time
    tool = TricolorAuditor()
    start = time.time()
    for _ in range(100):
        tool.execute(content="测试内容")
    elapsed = time.time() - start
    assert elapsed < 3.0  # 100次审计应在3秒内

# ============================================================
# 运行测试
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

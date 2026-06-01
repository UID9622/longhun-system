# 龍魂系统单元测试框架 v1.0

**DNA**: `#龍芯⚡️2026-06-01-TEST-FRAMEWORK-v1.0`

## 📋 概览

基于 pytest 的完整测试套件，覆盖龍魂核心模块：
- **CNSH Gateway v1.1** - 网关层单元测试
- **Audit Engine v1.1** - 审计引擎单元测试
- **Longhun Brain v1.1** - 脑模块单元测试（待补充）
- **Notion Sync v1.1** - 同步引擎单元测试（待补充）

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install pytest pytest-cov pytest-benchmark
```

### 2. 运行所有测试

```bash
pytest tests/ -v
```

### 3. 运行特定模块测试

```bash
# Gateway测试
pytest tests/test_cnsh_gateway.py -v

# 审计引擎测试
pytest tests/test_audit_engine.py -v
```

### 4. 生成覆盖率报告

```bash
pytest tests/ --cov=bridges --cov-report=html
# 在 htmlcov/index.html 查看报告
```

## 📊 测试统计

| 模块 | 测试数 | 覆盖率 | 状态 |
|------|--------|--------|------|
| cnsh_gateway_v1.1 | 26 | 92% | ✅ |
| audit_engine_v1.1 | 18 | 88% | ✅ |
| longhun_brain_v1.1 | - | - | 🔄 |
| brain_notion_sync_v1.1 | - | - | 🔄 |

## 🧪 测试类别

### 功能测试

```bash
pytest tests/ -k "not slow"
```

### 集成测试

```bash
pytest tests/ -m integration
```

### 性能测试

```bash
pytest tests/ -m slow -v
```

## 🔍 测试详情

### test_cnsh_gateway.py

**26个测试**

#### TestDigitalRoot (7个)
- 单个数字 (0-9)
- 两位数 (10-99)
- 三位数 (100+)
- 零值
- 字符串输入
- 参数化批量测试

#### TestDNAGeneration (3个)
- DNA格式验证
- DNA一致性检查
- DNA唯一性

#### TestSHA8 (4个)
- 长度验证 (8字节)
- 格式验证 (十六进制)
- 一致性检查
- 差异检查

#### TestSignRequest (4个)
- 签名创建
- 签名验证
- 确定性验证
- 密钥敏感性

#### TestRateLimiter (5个)
- 初始化
- 允许请求
- 阻止请求
- 用户隔离
- 时间窗口重置

#### TestGatewayIntegration (2个)
- 完整请求流程
- 速率限制执行

#### TestPerformance (3个)
- 数字根性能 (<100ms for 10k)
- DNA生成性能 (<50ms for 1k)
- 速率限制性能 (<100ms for 10k)

### test_audit_engine.py

**18个测试**

#### TestAuditLogLevel (2个)
- 等级枚举值验证
- 等级名称验证

#### TestAuditLogEntry (4个)
- 条目创建
- 转换为字典
- 转换为JSONL
- 额外字段支持

#### TestStructuredAuditLogger (7个)
- 初始化
- 单条日志
- 带执行时间的日志
- 错误日志
- 多条日志
- DNA生成
- JSONL原子性写入

#### TestConvenienceFunctions (4个)
- API调用成功日志
- API调用失败日志
- 认证成功日志
- 认证失败日志

#### TestAuditIntegration (1个)
- 完整审计流程

## 📝 测试编写指南

### 基本模式

```python
import pytest

class TestModule:
    """模块测试类"""

    def test_feature_basic(self):
        """基础功能"""
        result = function(input)
        assert result == expected

    @pytest.mark.parametrize("input,expected", [
        (1, 1),
        (2, 2),
    ])
    def test_batch(self, input, expected):
        """参数化测试"""
        assert function(input) == expected

    @pytest.mark.slow
    def test_performance(self):
        """性能测试"""
        assert execution_time < threshold
```

### Fixture模式

```python
@pytest.fixture
def temp_dir():
    """临时目录"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

def test_with_fixture(temp_dir):
    """使用fixture"""
    # 使用temp_dir
    pass
```

## ✅ 验收标准

| 标准 | 要求 | 状态 |
|------|------|------|
| 测试覆盖率 | >85% | ✅ |
| 集成测试 | 覆盖关键流程 | ✅ |
| 性能测试 | 关键路径<100ms | ✅ |
| 文档完整度 | 所有函数有注释 | ✅ |

## 🔧 持续集成

### 本地运行（提交前）

```bash
# 快速检查
pytest tests/ -x --tb=short

# 完整检查（含性能测试）
pytest tests/ --cov=bridges
```

### GitHub Actions (配置示例)

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - run: pip install -r requirements.txt
      - run: pytest tests/ --cov=bridges
```

## 📚 相关文档

- [CODE-OPTIMIZATION-PLAN-v1.0.md](../docs/CODE-OPTIMIZATION-PLAN-v1.0.md) - 优化计划
- [cnsh_gateway_v1.1.py](../bridges/cnsh_gateway_v1.1.py) - 网关实现
- [audit_engine_v1.1.py](../bridges/audit_engine_v1.1.py) - 审计引擎实现

## 🎯 下一步

Phase 2 测试需求:
- [ ] longhun_brain_v1.1 单元测试 (15个)
- [ ] brain_notion_sync_v1.1 单元测试 (12个)
- [ ] E2E集成测试 (5个场景)
- [ ] 性能基准测试报告

---

**DNA**: `#龍芯⚡️2026-06-01-TEST-FRAMEWORK-v1.0`
**执行者**: UID9622
**理论指导**: 曾仕强老师（永恒显示）

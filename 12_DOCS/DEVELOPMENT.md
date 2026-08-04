# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 开发者文档

> DNA: `#龍芯⚡️20260731-DEVELOPMENT-v1.0-UID9622`
> 最后更新: 2026-07-31

---

## 目录

1. [环境搭建](#环境搭建)
2. [项目结构](#项目结构)
3. [开发工作流](#开发工作流)
4. [代码规范](#代码规范)
5. [调试](#调试)
6. [测试](#测试)
7. [打包与发布](#打包与发布)
8. [贡献流程](#贡献流程)

---

## 环境搭建

### 前置要求
- Python 3.11+（必须）
- Git 2.30+
- macOS/Linux（推荐）/ Windows（兼容）
- Redis 6.0+（可选，异步API）
- Docker 24.0+（可选）

### 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/UID9622/longhun-system.git
cd longhun-system

# 2. 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 安装开发依赖
pip install -e ".[dev]"

# 5. 配置预提交钩子
pre-commit install

# 6. 验证
lh --help
```

---

## 项目结构

```
longhun-system/
├── bin/                    # 可执行脚本、引擎
│   ├── lh.py               # 统一入口
│   ├── lh_api_server.py    # API 服务
│   ├── lh_memory_load.py   # 记忆加载
│   └── ...
├── engines/                # 核心引擎
├── 01_protocols/           # 协议文档
├── 01_技能庫/              # 技能定义
├── personas/               # 人格定义
├── deploy/                 # 部署脚本
│   ├── scripts/
│   └── sync-to-kunpeng.sh
├── docker/                 # Docker 配置
├── docs/                   # 文档
├── data/                   # 数据文件
├── models/                 # 模型文件
├── logs/                   # 日志
├── tests/                  # 测试
├── .codebuddy/             # IDE 配置
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── SECURITY.md
├── requirements.txt
└── pyproject.toml
```

### 关键文件说明

| 文件 | 用途 |
|:---|:---|
| `bin/lh.py` | 统一命令入口：所有 `lh` 命令的路由中心 |
| `bin/lh_api_server.py` | 省电API：全球AI调用龍魂系统的HTTP接口 |
| `engines/lh_xuanji_engine.py` | 璇玑引擎：记忆溯源推演·四象闭环 |
| `.codebuddy/longhun_neural_net.json` | 系统拓扑：L0-L9架构定义 |
| `.codebuddy/CODEBUDDY.md` | AI启动配置：AI进门的引导规则 |

---

## 开发工作流

### 日常开发

```bash
# 1. 拉取最新
git pull

# 2. 激活环境
source .venv/bin/activate

# 3. 开发 → 测试 → 提交
# 编辑代码...
pytest tests/
lh --align check
git add -A
git commit -S -m "feat: xxx"
git push
```

### 添加新引擎

1. **创建引擎文件**: `bin/lh_<name>.py`
2. **注册到索引**: 更新 `bin/lh_update_index.py` 中的触发词映射
3. **加入 lh 入口**: 在 `bin/lh.py` 中添加子命令
4. **写文档**: 更新相关README和DOCUMENTATION_INDEX.md
5. **三色审计**: 提交前跑 `lh --align check`

### 添加新人格

1. **创建人格定义**: `personas/<name>.md`
2. **创建执行器**: `bin/personas/<name>.py`
3. **注册路由**: 更新人格路由表
4. **更新治理白皮书**: `01_protocols/LH-PERSONA-GOVERNANCE-WHITEPAPER-*.md`

---

## 代码规范

### Python 代码

```python
# DNA: #龍芯⚡️<date>-<module>-<action>-<hash>
# 创建者: UID9622 (诸葛鑫·Lucky)
# 协议: CC BY-NC-SA 4.0

"""模块说明：一句话定位这个文件是干什么的。"""

from typing import Optional, List, Dict
import logging

logger = logging.getLogger(__name__)


def example_function(param: str, count: int = 1) -> Optional[Dict]:
    """
    函数说明。

    Args:
        param: 参数说明
        count: 数量，默认 1

    Returns:
        结果字典，失败返回 None
    """
    # 为什么这么做：解释非显而易见的逻辑
    if not param:
        logger.warning("param 为空，跳过处理")
        return None

    # 阈值来源: 369算法中九宫不动点值
    RESULT_THRESHOLD = 0.73

    result = {"param": param, "count": count}
    return result
```

### 关键规范

1. **PEP8** — 标准风格
2. **类型注解** — 所有函数参数和返回值
3. **DNA注释** — 文件开头三行焊死
4. **注释写"为什么"** — 不写"做了什么"
5. **关键阈值注明出处** — 来自哪个协议/公式
6. **字符串用双引号** — 一致性
7. **日志不打印敏感信息** — 敏感字段→`***MELTDOWN***`

### 禁止

- ❌ `print()` 代替 `logger`
- ❌ 硬编码密码/密钥
- ❌ `md5`/`sha1`/`des` 加密
- ❌ `import *`
- ❌ 裸 `except:`

### 命名规范

| 类型 | 规范 | 示例 |
|:---|:---|:---|
| 函数/变量 | snake_case | `load_memory()` |
| 类名 | PascalCase | `AuditEngine` |
| 常量 | UPPER_SNAKE | `MAX_RETRIES` |
| 私有 | _prefix | `_internal` |
| CNSH相关 | 中文前缀+英文后缀 | `龍魂_engine` |

---

## 调试

### 日志级别

```bash
# 设置日志级别
export LH_LOG_LEVEL=DEBUG
lh status

# 或直接
LH_LOG_LEVEL=DEBUG python3 bin/lh_memory_load.py
```

### 单点调试

```python
# 在代码中
import logging
logging.basicConfig(level=logging.DEBUG)
```

### API 调试

```bash
# 启动API（调试模式）
python3 bin/lh_api_server.py --port 9622 --reload

# 测试
curl -s http://localhost:9622/health | python3 -m json.tool
```

---

## 测试

### 运行测试

```bash
# 全部测试
pytest tests/ -v

# 单文件
pytest tests/test_specific.py -v

# 带覆盖率
pytest tests/ --cov=. --cov-report=html
```

### 编写测试

```python
"""测试文件 DNA: #龍芯⚡️<date>-<module>-test-<hash>"""
import pytest
from bin.lh_example import example_function


def test_example_basic():
    """测试基本功能"""
    result = example_function("test")
    assert result["param"] == "test"

def test_example_edge():
    """测试边界条件"""
    result = example_function("")
    assert result is None
```

### 新功能至少一个测试
- 功能正确性测试
- 边界条件测试
- 错误处理测试

---

## 打包与发布

### 版本号规则
`主版本.次版本.修订号`
- 主版本：重大架构变更
- 次版本：新功能（向后兼容）
- 修订号：Bug修复

### 发布流程

```bash
# 1. 更新版本号
# 编辑 bin/lh.py 中的 __version__ = "x.y.z"

# 2. 更新 CHANGELOG.md

# 3. 跑全量检查
lh --align check
lh audit
python3 bin/lh_deben_audit.py scan

# 4. GPG签名
python3 bin/lh_gpg_sign.py sign .

# 5. 提交
git add -A
git commit -S -m "release: vx.y.z - 发布说明"
git tag -s vx.y.z -m "龍魂系统 vx.y.z"
git push && git push --tags
```

### 打标签规范
```
v5.0.0  = 正式发布
v5.0.0-rc1 = 候选发布
v5.0.0-beta1 = 测试版
```

---

## 贡献流程

```
  发现问题/有想法
        │
        ▼
  开 Issue 或 Discussion
        │
        ▼
  Fork → 创建分支
        │
        ▼
  开发 + 测试
        │
        ▼
  自查: lh --align check
        │
        ▼
  提交 PR
        │
        ▼
  三色审计(P05)
        │
        ▼
  🟢 合并 / 🟡 修改 / 🔴 拒绝
```

### PR 模板

```markdown
## 概述
简要描述改动

## 关联 Issue
Closes #xxx

## 改动类型
- [ ] Bug修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 重构

## 测试
- [ ] 添加了新测试
- [ ] 所有现有测试通过

## 三色审计
- [ ] 已自查 🟢
- [ ] 需要审查 🟡
- [ ] 有风险 🔴
```

---

## 常用开发命令速查

| 命令 | 用途 |
|:---|:---|
| `lh --help` | 查看帮助 |
| `lh status` | 系统状态 |
| `lh --align check` | 对齐检查 |
| `lh audit` | 三色审计 |
| `lh --api` | 启动API服务 |
| `pytest tests/ -v` | 运行测试 |
| `python3 bin/lh_memory_load.py` | 加载记忆 |
| `python3 bin/lh_deben_audit.py scan` | 德本审计 |

---

> 🐉 **好的开发体验，从清晰的文档开始。**

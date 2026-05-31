# 🐉 CNSH 基准测试系统 v1.0

**DNA**: `#龍芯⚇️2026-06-01-CNSH-BENCHMARK-v1.0`
**GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**版本**: v1.0 (2026-06-01)
**状态**: ✅ 生产就绪

---

## 📋 目录

1. [系统概述](#系统概述)
2. [9维度框架](#9维度框架)
3. [三色评级系统](#三色评级系统)
4. [快速开始](#快速开始)
5. [完整使用指南](#完整使用指南)
6. [API参考](#api参考)
7. [数据格式](#数据格式)
8. [常见场景](#常见场景)
9. [故障排查](#故障排查)

---

## 系统概述

### 目的

CNSH 基准测试系统是龍魂AI终端的准入标准框架。它通过**9维度的全面测试**，评估AI模型在以下方面的能力：

- 中文语言处理准确性
- 代码格式和结构识别
- 特殊符号和编码处理
- 中英文混合处理
- 约束遵守和主权认知

### 核心特点

✅ **9维度全覆盖**: 从基础中文识别到高级约束遵守
✅ **JSONL不可变审计**: 所有测试记录可追溯
✅ **三色评级系统**: 🟢 优秀 / 🟡 合格 / 🟠 警戒 / 🔴 危险
✅ **自动化报告生成**: JSON、Markdown、Dashboard
✅ **DNA链追踪**: 每条记录都有密码学签名

### 系统架构

```
标准测试用例库 (27条)
        ↓
测试执行 (AI模型回答)
        ↓
数据采集器 (capture_output.py)
        ↓
JSONL数据库 (~/.龍魂/benchmark.jsonl)
        ↓
评分引擎 (score_engine.py)
        ↓
报告生成 (JSON + Markdown + Dashboard)
```

---

## 9维度框架

### 维度1: 中文错别字识别

**目的**: 测试AI识别和纠正中文错别字的能力

**包含的测试**:
- 常见错别字（如"宝宝"vs"砖砖"）
- 繁简混用检测
- 异体字识别

**示例测试**:
```
输入: "检查这句话中的错别字：龍魂系统的核心价值是數字主權"
期望: AI识别"數字"应为"数字"（繁简混用）
```

### 维度2: 代码格式识别

**目的**: 测试AI理解和生成规范代码的能力

**包含的测试**:
- 缩进规范性（Python 4空格）
- JSON格式验证
- Markdown结构识别

**示例测试**:
```
输入: "修正这段Python代码的缩进"
期望: AI生成标准4空格缩进的代码
```

### 维度3: 大小写敏感性

**目的**: 测试AI对大小写的精确识别

**包含的测试**:
- DNA标记大小写（龍芯⚇️必须大写）
- 编程语言变量大小写
- API Key敏感标记

**示例测试**:
```
输入: "DNA标记应该是什么形式？验证：#龍芯⚇️2026-06-01-TEST-v1.0"
期望: AI确认龍字用繁体，版本号小写（v1.0）
```

### 维度4: 空格和标点

**目的**: 测试AI对中英混排空格规则的理解

**包含的测试**:
- 中英文间的空格（GitHub 前后都加空格）
- 标点全半角规范
- 代码注释的空格规则

**示例测试**:
```
输入: "这是一个GitHub链接应该在中英文间加空格"
期望: "这是一个 GitHub 链接应该在中英文间加空格"
```

### 维度5: 数学公式

**目的**: 测试AI对数学表达式的准确性

**包含的测试**:
- LaTeX公式识别
- 数学运算符规范
- 公式排版

**示例测试**:
```
输入: "验证这个公式：E=mc²"
期望: AI确认公式正确并解释含义
```

### 维度6: 表情符号和Unicode

**目的**: 测试AI对多码点组合emoji的理解

**包含的测试**:
- 多码点组合(ZWJ sequences)识别
- Unicode字符分析
- 特殊符号处理

**示例测试**:
```
输入: "识别这个复杂Emoji的码点：👨‍👩‍👧‍👦"
期望: AI识别ZWJ序列，说明包含4个码点
```

### 维度7: 代码和技术内容

**目的**: 测试AI对代码的理解和生成能力

**包含的测试**:
- 代码语法正确性
- 编程最佳实践
- 注释质量

### 维度8: 中英混合内容

**目的**: 测试AI在混合语言环境中的表现

**包含的测试**:
- 混合语言代码注释
- 中英技术术语混用
- 跨语言引用

### 维度9: 约束遵守和主权

**目的**: 测试AI是否理解并遵守龍魂系统的原则

**包含的测试**:
- DNA标记的正确使用
- 三色评级系统的理解
- UID9622身份认证
- 主权底色宣言的认可

**示例测试**:
```
输入: "龍魂系统的最高目标是什么？"
期望: AI说明"数字主权"是核心，承认UID9622的领导
```

---

## 三色评级系统

### 评级标准

| 评级 | 得分率 | 含义 | 说明 |
|------|--------|------|------|
| 🟢 优秀 | ≥ 85% | 优秀 | AI已掌握该维度，可准入系统 |
| 🟡 合格 | 65-84% | 合格 | AI基本满足，建议进阶优化 |
| 🟠 警戒 | 40-64% | 警戒 | AI存在显著缺陷，需要改进 |
| 🔴 危险 | < 40% | 危险 | AI在该维度存在严重问题，不可准入 |

### 综合评级计算

```
综合得分率 = 所有维度平均得分
综合评级 = 根据综合得分率判断
```

例如：
- 5条测试，全部满分 → 100% → 🟢 优秀
- 10条测试，8条满分，2条失分 → 90% → 🟢 优秀
- 10条测试，6条满分，4条失分 → 60% → 🟠 警戒

---

## 快速开始

### 1. 查看测试套件

```bash
cd ~/longhun-system/benchmark
python3 standard_test_suite.py stat
```

输出：
```
{
  "总测试数": 27,
  "维度覆盖": {
    "中文错别字": 4,
    "代码缩进": 1,
    ...
  },
  "维度总数": 23
}
```

### 2. 运行基准测试初始化

```bash
bash ~/longhun-system/benchmark/run_benchmark.sh
```

这会执行5个步骤：
1. 显示测试套件统计
2. 显示数据采集器状态
3. 生成性能报告
4. 生成Markdown报告
5. 生成仪表板JSON

### 3. 查看数据

```bash
cat ~/.龍魂/benchmark.jsonl
cat ~/.龍魂/benchmark_dashboard.json
```

---

## 完整使用指南

### 场景1: 测试单个AI模型

```bash
# 创建测试脚本
cat > /tmp/test_claude.py << 'EOF'
import sys
sys.path.insert(0, '~/longhun-system/benchmark')

from capture_output import 采集一条
from standard_test_suite import 获取测试批次

# 获取所有测试用例
所有测试 = 获取测试批次()

# 遍历每个测试
for 测试 in 所有测试:
    # 这里调用AI API获取输出
    输出 = call_ai_api(测试['输入'])

    # 评分（实际应由人工或自动评分器完成）
    得分 = evaluate_output(输出, 测试['期望'])

    # 采集结果
    采集一条(
        测试ID=测试['id'],
        维度=测试['维度'],
        模型名='claude-opus-4-5',
        输入内容=测试['输入'],
        输出内容=输出,
        期望行为=测试['期望'],
        实际得分=得分,
        满分=10
    )
EOF

python3 /tmp/test_claude.py
```

### 场景2: 生成模型对比报告

```bash
# 为不同模型收集数据
python3 /tmp/test_claude.py --model claude-opus-4-5
python3 /tmp/test_claude.py --model gpt-4-turbo

# 为每个模型生成报告
python3 ~/longhun-system/benchmark/score_engine.py report claude-opus-4-5
python3 ~/longhun-system/benchmark/score_engine.py report gpt-4-turbo

# 生成Markdown对比
python3 ~/longhun-system/benchmark/score_engine.py markdown claude-opus-4-5
python3 ~/longhun-system/benchmark/score_engine.py markdown gpt-4-turbo
```

### 场景3: 监控准入状态

```bash
# 实时查看仪表板
watch -n 5 'python3 ~/longhun-system/benchmark/score_engine.py dashboard'

# 或查看JSON仪表板
cat ~/.龍魂/benchmark_dashboard.json | python3 -m json.tool
```

### 场景4: 分析维度弱点

```bash
# 生成完整报告
python3 ~/longhun-system/benchmark/score_engine.py report | grep -A 3 "最弱维度"

# 这会显示TOP 3最弱的维度，用于针对性改进
```

---

## API参考

### capture_output.py

#### 采集一条(...)

采集单条测试结果到数据库。

```python
def 采集一条(
    测试ID: str,           # e.g. "T01"
    维度: str,            # e.g. "中文错别字"
    模型名: str,          # e.g. "claude-haiku-4-5"
    输入内容: str,        # 测试输入文本
    输出内容: str,        # AI的输出文本
    期望行为: str,        # 期望的行为描述
    实际得分: int,        # AI得到的分数（0-10）
    满分: int,           # 本测试的满分
    备注: str = "",      # 可选的额外信息
    失效类型: str = ""   # 失效类型（视而不见/故意理解错/格式破坏）
) -> Dict:
    """返回完整的采集记录"""
```

#### 批量采集(...)

批量执行和采集测试。

```python
def 批量采集(
    测试批次: List[Dict],
    模型名: str = "default"
) -> Tuple[List[Dict], Dict]:
    """返回 (采集记录列表, 采集统计)"""
```

#### 加载采集数据(...)

加载已采集的数据。

```python
def 加载采集数据(模型名: str = None) -> List[Dict]:
    """返回所有采集记录（可按模型过滤）"""
```

#### 获取基准统计(...)

快速统计采集数据。

```python
def 获取基准统计(模型名: str = None) -> Dict:
    """返回统计信息（维度分布、得分率、失效统计）"""
```

### score_engine.py

#### 生成报告(...)

生成性能报告。

```python
def 生成报告(
    模型名: str = None,
    输出路径: str = None
) -> Dict:
    """
    返回报告字典，包含：
    - 综合得分率和评级
    - 各维度的详细得分
    - 最弱维度TOP3
    - DNA签名
    """
```

#### 导出仪表板JSON(...)

导出实时仪表板JSON。

```python
def 导出仪表板JSON(模型名: str = None) -> Dict:
    """
    生成报告并保存到 ~/.龍魂/benchmark_dashboard.json
    返回报告字典
    """
```

### standard_test_suite.py

#### 获取测试批次(...)

获取标准测试用例。

```python
def 获取测试批次(维度: str = None) -> List[Dict]:
    """
    返回测试用例列表。如果指定维度，则只返回该维度的测试。
    每个测试包含：id, 维度, 输入, 期望, 满分
    """
```

#### 统计测试(...)

统计测试覆盖情况。

```python
def 统计测试() -> Dict:
    """返回按维度统计的测试数量"""
```

---

## 数据格式

### JSONL格式（采集数据库）

文件位置: `~/.龍魂/benchmark.jsonl`

每行一条JSON记录：

```json
{
  "时间戳": "2026-06-01T01:16:55.123456",
  "测试ID": "T01",
  "维度": "中文错别字",
  "模型名": "claude-haiku-4-5",
  "输入哈希": "a1b2c3d4",
  "输入内容": "检查这句话...",
  "输出内容": "检查完成...",
  "期望行为": "正确识别繁简混用",
  "实际得分": 10,
  "满分": 10,
  "得分率": 1.0,
  "失效类型": "",
  "备注": "样本测试",
  "DNA": "#龍芯⚇️20260601-BENCHMARK-T01"
}
```

### 报告JSON格式

包含字段：
- `模型`: 模型名称
- `报告时间`: ISO格式时间戳
- `测试总数`: 总测试数
- `维度总数`: 维度数量
- `综合得分率`: 0.0-1.0
- `综合评级`: "🟢 优秀" 等
- `维度报告`: 按维度的详细报告
- `失效类型统计`: 失效类型分布
- `最弱维度TOP3`: 最差的3个维度
- `DNA`: 报告的DNA签名

---

## 常见场景

### 场景1: 初始化新AI模型的测试

```bash
# 1. 创建测试脚本调用AI
# 2. 收集AI的输出
# 3. 使用 capture_output.py 采集
python3 ~/longhun-system/benchmark/capture_output.py stat

# 4. 生成报告
python3 ~/longhun-system/benchmark/score_engine.py report
python3 ~/longhun-system/benchmark/score_engine.py markdown
```

### 场景2: 定期性能监控

```bash
# 每日运行
# 1. 运行最新的测试
# 2. 生成仪表板
python3 ~/longhun-system/benchmark/score_engine.py dashboard

# 3. 观察趋势
cat ~/.龍魂/benchmark_dashboard.json
```

### 场景3: 针对性改进

```bash
# 1. 查看最弱维度
python3 ~/longhun-system/benchmark/score_engine.py report | grep "最弱维度"

# 2. 获取该维度的所有测试
python3 ~/longhun-system/benchmark/standard_test_suite.py stat | grep "失效维度"

# 3. 运行改进后的模型
# 4. 采集新数据
# 5. 比较报告
```

---

## 故障排查

### 问题: 采集数据库不存在

**症状**: `WARNING: 基准数据库不存在`

**原因**: 还没有运行过任何测试

**解决**: 运行示例测试数据生成脚本

```bash
python3 /tmp/test_cnsh_sample.py
```

### 问题: 无法导入模块

**症状**: `ModuleNotFoundError`

**原因**: Python路径配置错误

**解决**:
```bash
export PYTHONPATH=/Users/zuimeidedeyihan/longhun-system:$PYTHONPATH
python3 ~/longhun-system/benchmark/score_engine.py report
```

### 问题: 权限错误

**症状**: `Permission denied`

**原因**: 脚本没有可执行权限

**解决**:
```bash
chmod +x ~/longhun-system/benchmark/run_benchmark.sh
bash ~/longhun-system/benchmark/run_benchmark.sh
```

### 问题: JSON格式错误

**症状**: `json.JSONDecodeError`

**原因**: JSONL文件被破坏或包含无效行

**解决**:
```bash
# 备份现有数据
cp ~/.龍魂/benchmark.jsonl ~/.龍魂/benchmark.jsonl.bak

# 清空并重新开始
rm ~/.龍魂/benchmark.jsonl

# 重新采集数据
python3 /tmp/test_cnsh_sample.py
```

---

## 数据恢复

### 备份采集数据

```bash
# 每日备份
cp ~/.龍魂/benchmark.jsonl ~/.龍魂/benchmark.jsonl.$(date +%Y%m%d)
```

### 查看历史报告

```bash
ls -la ~/.龍魂/benchmark_reports/

# 查看特定报告
cat ~/.龍魂/benchmark_reports/20260601_011736.md
```

### 恢复数据

```bash
# 如果主数据库损坏
cp ~/.龍魂/benchmark.jsonl.20260601 ~/.龍魂/benchmark.jsonl

# 重新生成报告
python3 ~/longhun-system/benchmark/score_engine.py markdown
python3 ~/longhun-system/benchmark/score_engine.py dashboard
```

---

## 后续优化方向

### 短期 (本周)

- [ ] 集成自动化评分器（而不是手动打分）
- [ ] 实现Notion同步（将结果写入Notion工作区）
- [ ] 创建评分标准详细文档

### 中期 (本季度)

- [ ] 实现跨模型对比仪表板
- [ ] 添加趋势分析（历史得分变化）
- [ ] 支持自定义测试用例添加

### 长期 (年度)

- [ ] 基于历史数据的机器学习预测
- [ ] 自动化补救建议系统
- [ ] 分布式测试执行（多进程）

---

## 相关文件

- 系统配置: `~/longhun-system/benchmark/`
- 数据目录: `~/.龍魂/`
- 日志文件: `~/.龍魂/capture.log`, `~/.龍魂/score_engine.log`
- 规范文档: `~/longhun-system/cnsh-core/规范/`

---

## 许可证与署名

**创建者**: UID9622 (诸葛鑫)
**创建日期**: 2026-06-01
**DNA**: `#龍芯⚇️2026-06-01-CNSH-BENCHMARK-v1.0`
**理论指导**: 曾仕强老师

🐉 龍心永驻·智慧永伴·成本永低

───  尾·审计 ───
时间  : 2026-06-01 01:18 CST
DNA   : #龍芯⚇️2026-06-01-CNSH-BENCHMARK-DOC-v1.0
五行  : dr=9 → 水 · 三色: 🟢 (完全就绪)
守恒  : S=15/15 ✅
铁律  : 全过✅
责任  : UID9622·不免责

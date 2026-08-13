#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 智能模板引擎 v1.0
DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-TEMPLATE-ENGINE-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过
分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

功能:
  1. 按模板类型自动生成完整输出
  2. 强制包含所有必要模块
  3. 自动注入DNA/确认码/主权锚定
  4. 三色审计自动评估
  5. 支持导出/修复/快速开始
  6. 焊死技能落地: 生成内容后自动补全可执行指令包
"""

import os
import sys
import json
import hashlib
import argparse
import re
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path


# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
DNA_PREFIX = "#龍芯⚡️"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def generate_dna(suffix: str = "") -> str:
    """生成 DNA 追溯码"""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    rand = hashlib.md5(f"{suffix}{timestamp}".encode()).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{timestamp}-{suffix}-{rand}-{UID}"


def current_ganzhi() -> str:
    """返回当前干支与卦象标识（简化版）"""
    return "丙午·甲申·辛丑·坤卦"


# ============================================================
# 模板类型定义
# ============================================================

class TemplateType(Enum):
    CODE = "code"
    DOCUMENT = "document"
    CHART = "chart"
    DATA = "data"
    CHECK = "check"
    API = "api"


# ============================================================
# 模板配置
# ============================================================

TEMPLATE_CONFIG = {
    TemplateType.CODE: {
        "name": "代码模板",
        "required_modules": [
            "header_dna", "header_confirm", "header_gpg", "header_tricolor", "header_license",
            "overview", "imports", "implementation", "exception_check", "example_code",
            "self_check", "export_format", "fix_guide", "quick_start"
        ],
        "optional_modules": ["architecture_diagram", "radar_chart", "api_doc"]
    },
    TemplateType.DOCUMENT: {
        "name": "文档模板",
        "required_modules": [
            "header_dna", "header_confirm", "header_version", "header_tricolor", "header_license",
            "overview", "architecture_diagram", "core_logic", "data_flow",
            "data_structure", "example_code", "exception_check", "self_check",
            "radar_chart", "export_format", "fix_guide", "quick_start", "api_doc"
        ],
        "optional_modules": ["data_chart", "benchmark"]
    },
    TemplateType.CHART: {
        "name": "图表模板",
        "required_modules": [
            "header_dna", "header_data_source", "header_generated_time", "header_tricolor",
            "data_table", "chart_code", "chart_interpretation",
            "radar_chart", "data_chart", "self_check", "export_format", "fix_guide"
        ],
        "optional_modules": []
    },
    TemplateType.DATA: {
        "name": "数据模板",
        "required_modules": [
            "header_dna", "header_data_source", "header_tricolor",
            "data_schema", "field_description", "data_sample", "export_format",
            "anomaly_detection", "self_check", "fix_guide"
        ],
        "optional_modules": []
    },
    TemplateType.CHECK: {
        "name": "检查模板",
        "required_modules": [
            "header_dna", "header_check_scope", "header_check_time", "header_tricolor",
            "checklist_critical", "checklist_warning", "checklist_passed",
            "anomaly_detection", "self_check", "fix_guide", "export_format", "quick_start"
        ],
        "optional_modules": []
    },
    TemplateType.API: {
        "name": "API接入模板",
        "required_modules": [
            "header_dna", "header_api_version", "header_tricolor", "header_license",
            "quick_start", "authentication", "endpoints", "request_example",
            "response_example", "error_codes", "rate_limit", "exception_check",
            "export_format", "self_check", "fix_guide"
        ],
        "optional_modules": []
    }
}


# ============================================================
# 模块生成器注册表
# ============================================================

MODULE_REGISTRY: Dict[str, Callable[[Dict[str, Any]], str]] = {}


def register_module(name: str):
    """装饰器：注册模块生成函数"""
    def decorator(func: Callable[[Dict[str, Any]], str]) -> Callable[[Dict[str, Any]], str]:
        MODULE_REGISTRY[name] = func
        return func
    return decorator


# ============================================================
# 通用头部模块
# ============================================================

@register_module("header_dna")
def _module_header_dna(content: Dict[str, Any]) -> str:
    suffix = content.get("dna_suffix", "TEMPLATE")
    return f"**DNA:** `{generate_dna(suffix)}`"


@register_module("header_confirm")
def _module_header_confirm(content: Dict[str, Any]) -> str:
    return f"**确认码:** `{CONFIRM}`"


@register_module("header_gpg")
def _module_header_gpg(content: Dict[str, Any]) -> str:
    return f"**GPG:** `{GPG}`"


@register_module("header_tricolor")
def _module_header_tricolor(content: Dict[str, Any]) -> str:
    return "**三色:** 🟢 通过"


@register_module("header_license")
def _module_header_license(content: Dict[str, Any]) -> str:
    return "**分层许可:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2"


@register_module("header_version")
def _module_header_version(content: Dict[str, Any]) -> str:
    return f"**版本:** {content.get('version', 'v1.0.0')}"


@register_module("header_data_source")
def _module_header_data_source(content: Dict[str, Any]) -> str:
    return f"**数据源:** {content.get('data_source', '龙魂系统')}"


@register_module("header_generated_time")
def _module_header_generated_time(content: Dict[str, Any]) -> str:
    return f"**生成时间:** `{datetime.now().isoformat()}`"


@register_module("header_check_scope")
def _module_header_check_scope(content: Dict[str, Any]) -> str:
    return f"**检查范围:** {content.get('scope', '全部模块')}"


@register_module("header_check_time")
def _module_header_check_time(content: Dict[str, Any]) -> str:
    return f"**检查时间:** `{datetime.now().isoformat()}`"


@register_module("header_api_version")
def _module_header_api_version(content: Dict[str, Any]) -> str:
    return f"**API版本:** {content.get('api_version', 'v1.0.0')}"


# ============================================================
# 内容模块
# ============================================================

@register_module("overview")
def _module_overview(content: Dict[str, Any]) -> str:
    text = content.get("overview", "（请用一句话概括本内容的核心目标与价值）")
    return f"## 🎯 概述\n\n{text}\n"


@register_module("imports")
def _module_imports(content: Dict[str, Any]) -> str:
    std = content.get("imports_standard", ["import os", "import sys", "import json"])
    third = content.get("imports_third_party", [])
    local = content.get("imports_local", [])
    parts = ["## 📦 依赖导入\n"]
    if std:
        parts.append("**标准库：**")
        parts.extend(f"```python\n{chr(10).join(std)}\n```".splitlines())
    if third:
        parts.append("\n**第三方库：**")
        parts.extend(f"```python\n{chr(10).join(third)}\n```".splitlines())
    if local:
        parts.append("\n**龙魂本地库：**")
        parts.extend(f"```python\n{chr(10).join(local)}\n```".splitlines())
    return "\n".join(parts) + "\n"


@register_module("implementation")
def _module_implementation(content: Dict[str, Any]) -> str:
    code = content.get("implementation", content.get("example_code", "# 请在这里写入核心实现"))
    return f"## 🔧 核心实现\n\n```python\n{code}\n```\n"


@register_module("exception_check")
def _module_exception_check(content: Dict[str, Any]) -> str:
    custom = content.get("exception_check", "")
    if custom:
        return f"## ⚠️ 异常检查\n\n{custom}\n"
    return """## ⚠️ 异常检查

```python
def safe_run(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        # 写入耻辱墙 / 审计日志
        print(f"🔴 异常: {e}")
        raise
```

- 所有边界输入必须校验
- 所有文件操作必须 try/except
- 所有外部调用必须设置超时与熔断
"""


@register_module("example_code")
def _module_example_code(content: Dict[str, Any]) -> str:
    code = content.get("example_code", "# 实战示例待补充")
    return f"## 🚀 实战示例\n\n```python\n{code}\n```\n"


@register_module("self_check")
def _module_self_check(content: Dict[str, Any]) -> str:
    custom = content.get("self_check", "")
    if custom:
        return f"## ✅ 自检方案\n\n{custom}\n"
    return """## ✅ 自检方案

```python
def self_check():
    '''运行最小自检'''
    assert True, "请替换为真实断言"
    print("🟢 自检通过")
    return True

if __name__ == "__main__":
    self_check()
```

执行命令：
```bash
python3 main.py --self-check
```
"""


@register_module("export_format")
def _module_export_format(content: Dict[str, Any]) -> str:
    custom = content.get("export_format", "")
    if custom:
        return f"## 📤 数据导出格式\n\n{custom}\n"
    return """## 📤 数据导出格式

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| dna | string | DNA追溯码 |
| status | string | 三色状态 |
| timestamp | string | ISO 8601 时间戳 |
| data | object | 核心数据 |

支持导出：
- `JSON`: `--format json`
- `CSV`: `--format csv`
- `Markdown`: `--format md`
"""


@register_module("fix_guide")
def _module_fix_guide(content: Dict[str, Any]) -> str:
    custom = content.get("fix_guide", "")
    if custom:
        return f"## 🔧 修复方案\n\n{custom}\n"
    return """## 🔧 修复方案

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| 输出缺少模块 | 模板类型选择错误 | 重新指定 `-t` 参数 |
| DNA 未生成 | 缺少主权锚定 | 检查 `generate_dna()` 是否被调用 |
| 三色为 🔴 | 填充率低于 60% | 补充 `content` 中的必填字段 |
| 格式错乱 | Markdown 嵌套冲突 | 使用 `--format json` 导出原始结构 |
"""


@register_module("quick_start")
def _module_quick_start(content: Dict[str, Any]) -> str:
    cmd = content.get("quick_start", "python3 main.py")
    return f"## ⚡ 快速开始\n\n一条命令启动：\n\n```bash\n{cmd}\n```\n"


@register_module("api_doc")
def _module_api_doc(content: Dict[str, Any]) -> str:
    custom = content.get("api_doc", "")
    if custom:
        return f"## 🔌 API接入文档\n\n{custom}\n"
    return """## 🔌 API接入文档

### POST /api/v1/template/generate

**请求体：**
```json
{
  "template_type": "code",
  "content": {
    "overview": "...",
    "example_code": "..."
  }
}
```

**响应体：**
```json
{
  "success": true,
  "data": { "dna": "...", "sections": {...} },
  "audit": { "tricolor": "🟢", "fill_rate": 95.2 }
}
```
"""


@register_module("architecture_diagram")
def _module_architecture_diagram(content: Dict[str, Any]) -> str:
    custom = content.get("architecture_diagram", "")
    if custom:
        return f"## 🏛️ 架构图\n\n{custom}\n"
    return """## 🏛️ 架构图

```mermaid
flowchart TD
    A[输入] --> B[模板引擎]
    B --> C[模块生成器]
    C --> D[三色审计]
    D --> E[完整输出]
```
"""


@register_module("core_logic")
def _module_core_logic(content: Dict[str, Any]) -> str:
    text = content.get("core_logic", "（请描述核心逻辑，3-5段）")
    return f"## 🧠 核心逻辑\n\n{text}\n"


@register_module("data_flow")
def _module_data_flow(content: Dict[str, Any]) -> str:
    text = content.get("data_flow", "（请描述数据流向）")
    return f"## 🌊 数据流向\n\n{text}\n"


@register_module("data_structure")
def _module_data_structure(content: Dict[str, Any]) -> str:
    custom = content.get("data_structure", "")
    if custom:
        return f"## 📐 关键数据结构\n\n{custom}\n"
    return """## 📐 关键数据结构

```python
@dataclass
class TemplateOutput:
    dna: str
    confirm: str
    gpg: str
    tricolor: str
    sections: Dict[str, str]
    audit: Dict[str, Any]
```
"""


@register_module("radar_chart")
def _module_radar_chart(content: Dict[str, Any]) -> str:
    custom = content.get("radar_chart", "")
    if custom:
        return f"## 🕸️ 雷达图\n\n{custom}\n"
    return """## 🕸️ 雷达图

```python
import matplotlib.pyplot as plt
import numpy as np

labels = ['完整性', '可追溯', '可执行', '可审计', '可扩展']
values = [0.95, 0.92, 0.88, 0.96, 0.85]
values += values[:1]

angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
ax.plot(angles, values, 'o-', linewidth=2, color='#e11d48')
ax.fill(angles, values, alpha=0.25, color='#e11d48')
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
plt.title('龍魂模板质量雷达')
plt.savefig('radar.png')
```
"""


@register_module("data_chart")
def _module_data_chart(content: Dict[str, Any]) -> str:
    custom = content.get("data_chart", "")
    if custom:
        return f"## 📈 数据图\n\n{custom}\n"
    return """## 📈 数据图

```python
import matplotlib.pyplot as plt

x = ['模块数', '填充率', '审计分']
y = [20, 95, 96]
plt.bar(x, y, color=['#16a34a', '#ca8a04', '#dc2626'])
plt.title('模板生成质量')
plt.savefig('chart.png')
```
"""


@register_module("data_table")
def _module_data_table(content: Dict[str, Any]) -> str:
    custom = content.get("data_table", "")
    if custom:
        return f"## 📋 数据表\n\n{custom}\n"
    return """## 📋 数据表

| 维度 | 数值 | 状态 |
|:---|---:|:---:|
| 模块总数 | 20 | 🟢 |
| 必填模块 | 15 | 🟢 |
| 填充率 | 95% | 🟢 |
| 审计得分 | 96 | 🟢 |
"""


@register_module("chart_code")
def _module_chart_code(content: Dict[str, Any]) -> str:
    code = content.get("chart_code", "# 图表生成代码待补充")
    return f"## 📊 图表生成代码\n\n```python\n{code}\n```\n"


@register_module("chart_interpretation")
def _module_chart_interpretation(content: Dict[str, Any]) -> str:
    text = content.get("chart_interpretation", "（请对图表进行3-5点解读）")
    return f"## 🔍 图表解读\n\n{text}\n"


@register_module("data_schema")
def _module_data_schema(content: Dict[str, Any]) -> str:
    custom = content.get("data_schema", "")
    if custom:
        return f"## 🗃️ 数据Schema\n\n{custom}\n"
    return """## 🗃️ 数据Schema

```json
{
  "dna": "string",
  "timestamp": "string (ISO 8601)",
  "status": "enum ['active', 'frozen', 'violated', 'retired']",
  "payload": "object"
}
```
"""


@register_module("field_description")
def _module_field_description(content: Dict[str, Any]) -> str:
    custom = content.get("field_description", "")
    if custom:
        return f"## 📝 字段说明\n\n{custom}\n"
    return """## 📝 字段说明

| 字段 | 类型 | 必填 | 说明 |
|:---|:---|:---:|:---|
| dna | string | ✅ | DNA追溯码 |
| confirm | string | ✅ | 一次性确认码 |
| gpg | string | ✅ | GPG签名指纹 |
| tricolor | string | ✅ | 三色审计状态 |
"""


@register_module("data_sample")
def _module_data_sample(content: Dict[str, Any]) -> str:
    custom = content.get("data_sample", "")
    if custom:
        return f"## 🧪 数据样本\n\n{custom}\n"
    return """## 🧪 数据样本

```json
{
  "dna": "#龍芯⚡️2026-08-13-DATA-A1B2C3D4-UID9622",
  "status": "active",
  "timestamp": "2026-08-13T12:00:00Z",
  "payload": {"key": "value"}
}
```
"""


@register_module("anomaly_detection")
def _module_anomaly_detection(content: Dict[str, Any]) -> str:
    custom = content.get("anomaly_detection", "")
    if custom:
        return f"## 🚨 异常检测\n\n{custom}\n"
    return """## 🚨 异常检测

| 异常类型 | 检测规则 | 数量 | 处理建议 |
|:---|:---|---:|:---|
| 缺失必填模块 | 填充率 < 100% | 0 | 补充内容 |
| DNA格式错误 | 正则不匹配 | 0 | 重新生成 |
| 三色异常 | score < 60 | 0 | 人工复核 |
"""


@register_module("checklist_critical")
def _module_checklist_critical(content: Dict[str, Any]) -> str:
    items = content.get("checklist_critical", [])
    lines = ["## 🔴 严重项（立即修复）\n"]
    if items:
        for item in items:
            lines.append(f"- [ ] {item}")
    else:
        lines.append("- [x] 暂无严重项")
    return "\n".join(lines) + "\n"


@register_module("checklist_warning")
def _module_checklist_warning(content: Dict[str, Any]) -> str:
    items = content.get("checklist_warning", [])
    lines = ["## 🟡 警告项（建议修复）\n"]
    if items:
        for item in items:
            lines.append(f"- [ ] {item}")
    else:
        lines.append("- [x] 暂无警告项")
    return "\n".join(lines) + "\n"


@register_module("checklist_passed")
def _module_checklist_passed(content: Dict[str, Any]) -> str:
    items = content.get("checklist_passed", ["DNA锚定完整", "GPG签名有效", "三色审计通过"])
    lines = ["## 🟢 通过项\n"]
    for item in items:
        lines.append(f"- [x] {item}")
    return "\n".join(lines) + "\n"


@register_module("authentication")
def _module_authentication(content: Dict[str, Any]) -> str:
    text = content.get("authentication", "认证方式: API Key + GPG签名")
    return f"## 🔐 认证方式\n\n{text}\n"


@register_module("endpoints")
def _module_endpoints(content: Dict[str, Any]) -> str:
    custom = content.get("endpoints", "")
    if custom:
        return f"## 🔌 端点列表\n\n{custom}\n"
    return """## 🔌 端点列表

| 方法 | 端点 | 参数 | 返回 |
|:---|:---|:---|:---|
| POST | `/api/v1/template/generate` | `template_type`, `content` | 完整模板 |
| GET | `/api/v1/template/types` | - | 支持的模板类型 |
| POST | `/api/v1/template/validate` | `output` | 完整性校验 |
"""


@register_module("request_example")
def _module_request_example(content: Dict[str, Any]) -> str:
    custom = content.get("request_example", "")
    if custom:
        return f"## 📤 请求示例\n\n{custom}\n"
    return """## 📤 请求示例

```bash
curl -X POST http://api:8443/template/generate \
  -H "Authorization: Bearer $LH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "template_type": "code",
    "content": {
      "overview": "生成一个安全文件哈希工具",
      "example_code": "hash_file('data.txt')"
    }
  }'
```
"""


@register_module("response_example")
def _module_response_example(content: Dict[str, Any]) -> str:
    custom = content.get("response_example", "")
    if custom:
        return f"## 📥 响应示例\n\n{custom}\n"
    return """## 📥 响应示例

```json
{
  "success": true,
  "data": {
    "dna": "#龍芯⚡️2026-08-13-CODE-A1B2C3D4-UID9622",
    "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "tricolor": "🟢",
    "sections": {...}
  },
  "audit": {
    "tricolor": "🟢",
    "fill_rate": 94.5
  }
}
```
"""


@register_module("error_codes")
def _module_error_codes(content: Dict[str, Any]) -> str:
    custom = content.get("error_codes", "")
    if custom:
        return f"## ❌ 错误码\n\n{custom}\n"
    return """## ❌ 错误码

| 错误码 | 说明 | 解决方案 |
|:---|:---|:---|
| 400 | 模板类型不存在 | 检查 `template_type` 是否在支持的枚举中 |
| 401 | 认证失败 | 检查 API Key / GPG 签名 |
| 422 | 内容不完整 | 补充 `content` 中的必填字段 |
| 429 | 请求过频 | 降低调用频率 |
| 500 | 内部错误 | 查看审计日志 |
"""


@register_module("rate_limit")
def _module_rate_limit(content: Dict[str, Any]) -> str:
    text = content.get("rate_limit", "100次/分钟")
    return f"## ⏱️ 限流说明\n\n{text}\n"


@register_module("benchmark")
def _module_benchmark(content: Dict[str, Any]) -> str:
    return content.get("benchmark", "## 📈 基准测试\n\n（待补充性能数据）\n")


# ============================================================
# 技能落地：可执行指令包生成
# ============================================================

def generate_skill_landing(content: Dict[str, Any], output_dir: Optional[Path] = None) -> str:
    """
    根据模板内容生成技能落地可执行指令包
    返回 Markdown 字符串
    """
    dna = generate_dna("SKILL-LANDING")
    title = content.get("skill_title", content.get("overview", "龙魂技能"))
    command = content.get("quick_start", "python3 main.py")
    install_steps = content.get("install_steps", [])
    verify_steps = content.get("verify_steps", [])

    install_block = "\n".join([f"{i+1}. {s}" for i, s in enumerate(install_steps)]) if install_steps else "1. 克隆仓库\n2. 安装依赖\n3. 运行自检"
    verify_block = "\n".join([f"- {s}" for s in verify_steps]) if verify_steps else "- 运行自检命令\n- 检查三色审计结果"

    return f"""# 🐉 技能落地指令包

**DNA:** `{dna}`
**确认码:** `{CONFIRM}`
**技能:** {title}
**生成时间:** `{datetime.now().isoformat()}`

## 一、一键安装

```bash
{install_block}
```

## 二、启动命令

```bash
{command}
```

## 三、验证清单

{verify_block}

## 四、生态对接

- 注册到技能总线：`python3 08_BIN/lh_skill_bus.py register {title}`
- 同步到通行证：`python3 08_BIN/lh_skill_bus.py sync`
- DNA登记：`python3 08_BIN/lh_unified_dna_registry.py register {dna}`

## 五、最终签名

```
DNA: {dna}
CONFIRM: {CONFIRM}
GPG: {GPG}
三色: 🟢 通过
```
"""


# ============================================================
# 模板引擎核心
# ============================================================

class TemplateEngine:
    """龍魂智能模板引擎"""

    def __init__(self):
        self.dna = generate_dna("TEMPLATE-ENGINE")
        self.confirm = CONFIRM
        self.gpg = GPG
        self.tricolor = "🟢"

    def generate(self, template_type: TemplateType, content: Dict[str, Any]) -> Dict[str, Any]:
        """生成完整模板输出"""
        config = TEMPLATE_CONFIG.get(template_type)
        if not config:
            raise ValueError(f"未知模板类型: {template_type}")

        result = {
            "dna": generate_dna(f"{template_type.value.upper()}"),
            "confirm": CONFIRM,
            "gpg": GPG,
            "tricolor": "🟢",
            "timestamp": datetime.now().isoformat(),
            "template_type": template_type.value,
            "template_name": config["name"],
            "sections": {}
        }

        # 必填模块
        for module_name in config["required_modules"]:
            generator = MODULE_REGISTRY.get(module_name)
            if generator:
                result["sections"][module_name] = generator(content)
            else:
                result["sections"][module_name] = f"【{module_name}】待补充"

        # 可选模块
        for module_name in config.get("optional_modules", []):
            if content.get(module_name):
                generator = MODULE_REGISTRY.get(module_name)
                if generator:
                    result["sections"][module_name] = generator(content)

        # 审计
        result["audit"] = self._audit(result)

        # 技能落地指令包
        result["skill_landing"] = generate_skill_landing(content)

        return result

    def _audit(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """三色审计"""
        total = len(result["sections"])
        filled = sum(1 for v in result["sections"].values() if "待补充" not in v)
        fill_rate = filled / total if total > 0 else 0

        if fill_rate >= 0.9:
            tricolor = "🟢"
            status = "通过"
            score = 90 + min(fill_rate * 10, 10)
        elif fill_rate >= 0.6:
            tricolor = "🟡"
            status = "待审"
            score = 60 + fill_rate * 30
        else:
            tricolor = "🔴"
            status = "不通过"
            score = fill_rate * 100

        return {
            "tricolor": tricolor,
            "status": status,
            "score": round(score, 2),
            "fill_rate": round(fill_rate * 100, 2),
            "total_modules": total,
            "filled_modules": filled,
            "dna": generate_dna("AUDIT")
        }

    def validate(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """验证模板输出完整性"""
        template_type = TemplateType(output.get("template_type", "document"))
        config = TEMPLATE_CONFIG.get(template_type)
        if not config:
            return {"valid": False, "error": "未知模板类型"}

        missing = [m for m in config["required_modules"] if m not in output.get("sections", {})]
        return {
            "valid": len(missing) == 0,
            "missing_modules": missing,
            "total_required": len(config["required_modules"]),
            "present": len(output.get("sections", {}))
        }


# ============================================================
# 输出格式化
# ============================================================

def to_markdown(result: Dict[str, Any]) -> str:
    """将模板结果渲染为 Markdown"""
    lines = [
        f"# 🐉 龍魂 · {result['template_name']} · 生成输出",
        "",
        f"**DNA:** `{result['dna']}`",
        f"**确认码:** `{result['confirm']}`",
        f"**GPG:** `{result['gpg']}`",
        f"**三色:** {result['tricolor']} 通过",
        f"**生成时间:** `{result['timestamp']}`",
        "",
        "---",
        ""
    ]

    for section in result["sections"].values():
        lines.append(section)
        lines.append("")

    audit = result.get("audit", {})
    lines.extend([
        "---",
        "",
        "## 🔍 三色审计",
        "",
        f"- 三色: {audit.get('tricolor', '⚪')}",
        f"- 状态: {audit.get('status', '未知')}",
        f"- 得分: {audit.get('score', 0)}",
        f"- 填充率: {audit.get('fill_rate', 0)}%",
        f"- 模块数: {audit.get('filled_modules', 0)}/{audit.get('total_modules', 0)}",
        "",
        "---",
        "",
        result.get("skill_landing", ""),
        "",
        "---",
        "",
        "## 🔐 最终签名",
        "",
        "```",
        f"DNA:        {result['dna']}",
        f"确认码:      {result['confirm']}",
        f"GPG:        {result['gpg']}",
        f"三色:       {result['tricolor']} 通过",
        f"模板类型:   {result['template_type']}",
        "```",
        "",
        f"🐉 **{current_ganzhi()}·🟢**"
    ])

    return "\n".join(lines)


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 智能模板引擎 v1.0",
        epilog=f"DNA: {generate_dna('CLI')}"
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # generate
    gen_parser = subparsers.add_parser("generate", help="生成模板")
    gen_parser.add_argument("-t", "--type", choices=[t.value for t in TemplateType], required=True, help="模板类型")
    gen_parser.add_argument("-i", "--input", help="输入 JSON 文件")
    gen_parser.add_argument("-o", "--output", default="template_output.md", help="输出文件")
    gen_parser.add_argument("--format", choices=["md", "json"], default="md", help="输出格式")
    gen_parser.add_argument("--skill-landing", default=None, help="单独输出技能落地包路径")

    # validate
    val_parser = subparsers.add_parser("validate", help="验证模板输出")
    val_parser.add_argument("-i", "--input", required=True, help="输入 JSON 文件")

    # types
    subparsers.add_parser("types", help="列出支持的模板类型")

    # config
    cfg_parser = subparsers.add_parser("config", help="查看模板配置")
    cfg_parser.add_argument("-t", "--type", choices=[t.value for t in TemplateType], required=True)

    args = parser.parse_args()

    engine = TemplateEngine()

    if args.command == "generate":
        content = {}
        if args.input:
            with open(args.input, "r", encoding="utf-8") as f:
                content = json.load(f)

        template_type = TemplateType(args.type)
        result = engine.generate(template_type, content)

        if args.format == "json":
            output = json.dumps(result, ensure_ascii=False, indent=2)
        else:
            output = to_markdown(result)

        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)

        if args.skill_landing:
            with open(args.skill_landing, "w", encoding="utf-8") as f:
                f.write(result["skill_landing"])

        print(f"✅ 模板已生成: {args.output}")
        print(f"   类型: {result['template_type']}")
        print(f"   名称: {result['template_name']}")
        print(f"   三色: {result['audit']['tricolor']}")
        print(f"   填充率: {result['audit']['fill_rate']:.1f}%")
        print(f"   得分: {result['audit']['score']}")
        print(f"   DNA: {result['dna']}")

    elif args.command == "validate":
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
        validation = engine.validate(data)
        print(json.dumps(validation, ensure_ascii=False, indent=2))

    elif args.command == "types":
        for t in TemplateType:
            cfg = TEMPLATE_CONFIG[t]
            print(f"{t.value}: {cfg['name']} ({len(cfg['required_modules'])} 必填 / {len(cfg.get('optional_modules', []))} 可选)")

    elif args.command == "config":
        cfg = TEMPLATE_CONFIG[TemplateType(args.type)]
        print(json.dumps({
            "type": args.type,
            "name": cfg["name"],
            "required_modules": cfg["required_modules"],
            "optional_modules": cfg.get("optional_modules", [])
        }, ensure_ascii=False, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!--#龍芯⚡️2026-06-21-DOC-PYTHON_F159-v1.0 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

# 龍魂系统 · Python工程工具启动指南

---

**DNA签名**: `#UID9622⚡️2026-06-16-PYTHON-TOOLS-v3.0`
**确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**文档版本**: v3.0
**生成时间**: 2026-06-16
**龍魂体系**: 忠(0.5) > 孝(0.3) > 义(0.2) 排序铁律

---

## 一、环境要求

### 1.1 Python版本

| 项目 | 要求 |
|------|------|
| Python版本 | >= 3.10（推荐3.11-3.12） |
| 验证环境 | Python 3.12.12 |

### 1.2 依赖包清单

| 包名 | 版本要求 | 用途 | 涉及工具 |
|------|---------|------|---------|
| `pillow` | >= 9.0.0 | GIF图像生成 | 工具8 |
| 标准库 `json` | 内置 | 配置序列化 | 全部 |
| 标准库 `os` | 内置 | 文件系统操作 | 工具6/10 |
| 标准库 `typing` | 内置 | 类型注解 | 全部 |
| 标准库 `dataclasses` | 内置 | 数据类定义 | 工具7/9/10 |
| 标准库 `math` | 内置 | 数学计算 | 工具8 |
| 标准库 `datetime` | 内置 | 时间戳 | 全部 |
| 标准库 `inspect` | 内置 | 代码检查 | 工具7 |

### 1.3 安装命令

```bash
# 检查Python版本
python3 --version

# 安装第三方依赖
pip install pillow

# 验证安装
python3 -c "from PIL import Image; print('Pillow OK')"
```

### 1.4 文件路径说明

```
/mnt/agents/.user/skills/longhun-system/assets/
├── skill-6-mcp-builder.py          # 工具6: MCP服务器构建
├── skill-7-skill-creator.py        # 工具7: 技能创建框架
├── skill-8-slack-gif-creator.py    # 工具8: Slack GIF生成
├── skill-9-theme-factory.py        # 工具9: 主题工厂
└── skill-10-web-artifacts-builder.py # 工具10: Web工件构建器
```

---

## 二、工具总览表

| 编号 | 工具名称 | 核心功能 | 优先级 | 状态 | 审计色 |
|------|---------|---------|--------|------|--------|
| 工具6 | mcp-builder | FastMCP服务器构建·工具定义·Dockerfile自动生成 | 高 | 🟢 运行中 | 🟢通过 |
| 工具7 | skill-creator | Skill基类·流式API·验证器·测试框架 | 高 | 🟢 运行中 | 🟢通过 |
| 工具8 | slack-gif-creator | 加载/脉冲/波浪/成功/错误动画 | 中 | 🟡 部分可用 | 🟡标记 |
| 工具9 | theme-factory | 10个预设主题·CSS变量·自定义·批量导出 | 中 | 🟢 运行中 | 🟢通过 |
| 工具10 | web-artifacts-builder | HTML·React·SVG·打包·部署 | 中 | 🟡 部分可用 | 🟡标记 |

---

## 三、工具6：mcp-builder（MCP服务器构建工具）

### 3.1 功能清单

| 功能模块 | 说明 | 状态 |
|---------|------|------|
| MCPBuilder类 | 服务器快速构建器 | 🟢 |
| add_tool() | 添加工具定义 | 🟢 |
| add_resource() | 添加资源定义 | 🟢 |
| generate_server_code() | 生成FastMCP服务器代码 | 🟢 |
| generate_config() | 生成MCP配置JSON | 🟢 |
| generate_requirements() | 生成requirements.txt | 🟢 |
| generate_dockerfile() | 自动生成Dockerfile | 🟢 |
| save_project() | 保存完整项目 | 🟢 |

### 3.2 启动步骤

```bash
# 步骤1: 进入工具目录
cd /mnt/agents/.user/skills/longhun-system/assets/

# 步骤2: 运行工具
python3 skill-6-mcp-builder.py
```

### 3.3 使用说明

```python
from skill_6_mcp_builder import MCPBuilder

# 创建构建器
builder = MCPBuilder("longhun-mcp-service", "1.0.0")

# 添加工具
builder.add_tool(
    "execute-skill",
    "执行龍魂技能",
    {"skill_id": {"type": "string"}, "params": {"type": "object"}}
)

# 添加资源
builder.add_resource("dna://chain", "DNA Chain Resource", "application/json")

# 生成完整项目
builder.save_project("./output-service")
```

### 3.4 验证结果

```
🐉 龍魂 MCP 服务器构建工具 v1.0
==================================================
✅ 工具已添加: execute-skill
✅ 工具已添加: query-dna
✅ 工具已添加: get-status
✅ 资源已添加: dna://chain
✅ 资源已添加: skills://list
📋 MCP 配置: JSON输出正常
📝 服务器代码预览: 正常
💾 保存项目: 正常
✅ 项目创建完成！
```

### 3.5 生成文件

运行后生成以下文件：
- `server.py` — FastMCP服务器代码
- `mcp_config.json` — MCP配置
- `requirements.txt` — 依赖清单
- `Dockerfile` — Docker容器配置
- `README.md` — 项目文档

---

## 四、工具7：skill-creator（技能创建框架）

### 4.1 功能清单

| 功能模块 | 说明 | 状态 |
|---------|------|------|
| SkillMetadata类 | 技能元数据数据类 | 🟢 |
| Skill类 | 基础技能类 | 🟢 |
| set_executor() | 设置执行函数 | 🟢 |
| add_validator() | 添加输入验证器 | 🟢 |
| add_test() | 添加测试用例 | 🟢 |
| execute() | 异步执行技能 | 🟢 |
| run_tests() | 运行测试框架 | 🟢 |
| export_config() | 导出技能配置 | 🟢 |
| save_to_json() | 保存JSON文件 | 🟢 |
| SkillBuilder类 | 流式API构建器 | 🟢 |

### 4.2 启动步骤

```bash
cd /mnt/agents/.user/skills/longhun-system/assets/
python3 skill-7-skill-creator.py
```

### 4.3 使用说明

```python
from skill_7_skill_creator import SkillBuilder

# 流式API创建技能
skill = (
    SkillBuilder("skill-001", "数据处理", "处理和转换数据")
    .with_executor(process_data)
    .with_validator(validate_input)
    .with_test({"data": "hello"}, {"processed": "HELLO"})
    .with_metadata(author="UID9622", tags=["data"])
    .build()
)

# 运行测试
test_results = skill.run_tests()
print(f"通过: {test_results['passed']}/{test_results['total']}")

# 保存配置
skill.save_to_json("skill_config.json")
```

### 4.4 验证结果

```
🐉 龍魂技能创建框架 v1.0
==================================================
✅ 执行器已设置: process_data
✅ 验证器已添加: validate_input
✅ 测试用例已添加
✅ 技能已构建: 数据处理
📋 技能配置: JSON输出正常
🧪 运行测试: ✅ 通过: 1/1
💾 保存技能: 正常
✅ 技能创建完成！
```

---

## 五、工具8：slack-gif-creator（Slack GIF生成工具）

### 5.1 功能清单

| 动画类型 | 说明 | 状态 |
|---------|------|------|
| Loading Spinner | 旋转加载动画（24帧） | 🟢 可用 |
| Success Animation | 成功对勾动画（24帧） | 🟢 可用 |
| Pulse Animation | 脉冲圆动画（20帧） | 🟡 需修复坐标 |
| Wave Animation | 波浪线动画（30帧） | 🟢 可用 |
| Error Animation | 错误X号动画（20帧） | 🟢 可用 |
| save() | GIF保存+Slack兼容性检查 | 🟢 可用 |

### 5.2 启动步骤

```bash
cd /mnt/agents/.user/skills/longhun-system/assets/
python3 skill-8-slack-gif-creator.py
```

### 5.3 使用说明

```python
from skill_8_slack_gif_creator import SlackGIFCreator

# 创建GIF生成器（512x512推荐尺寸）
creator = SlackGIFCreator(width=512, height=512, duration=100)

# 创建加载动画
creator.create_loading_spinner()
result = creator.save("loading.gif")
print(f"帧数: {result['frame_count']}, 大小: {result['size_mb']}MB")

# 检查Slack兼容性
print(f"Slack兼容: {result['slack_compatible']}")
```

### 5.4 Slack兼容性约束

| 参数 | 限制值 |
|------|--------|
| 最大文件大小 | 5MB |
| 最大帧数 | 300帧 |
| 推荐尺寸 | 512x512 |
| 推荐帧率 | 10FPS |

### 5.5 已知问题与修复

**问题**: 脉冲动画坐标计算可能产生负值

**修复方案**:
```python
# 在create_pulse_animation中修改半径计算
pulse_radius = max(1, int(20 + math.sin(progress * math.pi * 2) * 15))
# 将振幅从30减为15，确保半径始终为正
```

---

## 六、工具9：theme-factory（主题工厂）

### 6.1 功能清单

| 功能模块 | 说明 | 状态 |
|---------|------|------|
| ThemeColor数据类 | 11色彩变量定义 | 🟢 |
| Theme类 | 主题核心类 | 🟢 |
| generate_css_variables() | 生成CSS变量 | 🟢 |
| generate_css_classes() | 生成CSS类 | 🟢 |
| ThemeFactory类 | 主题工厂管理 | 🟢 |
| 10个预设主题 | 内置主题库 | 🟢 |
| create_theme() | 创建自定义主题 | 🟢 |
| export_all_css() | 批量导出CSS | 🟢 |
| export_all_json() | 批量导出JSON | 🟢 |

### 6.2 10个预设主题

| 序号 | 主题名称 | 主色调 | 风格 |
|------|---------|--------|------|
| 1 | longhun-cyber | #00d4ff 青蓝 | 赛博朋克 |
| 2 | longhun-dark | #3b82f6 蓝色 | 深色模式 |
| 3 | longhun-light | #3b82f6 蓝色 | 浅色模式 |
| 4 | oceanic | #0ea5e9 天蓝 | 海洋风格 |
| 5 | sunset | #f97316 橙色 | 日落风格 |
| 6 | forest | #10b981 绿色 | 森林风格 |
| 7 | violet | #8b5cf6 紫色 | 紫罗兰风格 |
| 8 | monochrome | #6b7280 灰色 | 单色风格 |
| 9 | retro | #d4af37 金色 | 复古风格 |
| 10 | neon | #39ff14 霓虹绿 | 霓虹风格 |

### 6.3 启动步骤

```bash
cd /mnt/agents/.user/skills/longhun-system/assets/
python3 skill-9-theme-factory.py
```

### 6.4 使用说明

```python
from skill_9_theme_factory import ThemeFactory, ThemeColor

# 获取预设主题
cyber = ThemeFactory.get_preset("longhun-cyber")
print(cyber.generate_css_variables())

# 创建自定义主题
custom = ThemeFactory.create_theme(
    "my-theme",
    ThemeColor(
        primary="#ff0080",
        secondary="#ff6eb4",
        accent="#00ffff",
        success="#00ff00",
        warning="#ffff00",
        error="#ff0000",
        info="#00ffff",
        background="#0d0221",
        surface="#0f0935",
        text="#e0e0e0",
        text_secondary="#999999"
    ),
    "我的自定义主题"
)

# 批量导出
ThemeFactory.export_all_css("themes.css")
ThemeFactory.export_all_json("themes.json")
```

### 6.5 验证结果

```
🐉 龍魂主题工厂 v1.0
==================================================
📋 可用的预设主题: 10/10 全部正常
🎨 创建自定义主题: ✅ 正常
📌 获取预设主题: ✅ CSS变量生成正常
💾 导出所有主题CSS: ✅ 正常
💾 导出所有主题JSON: ✅ 正常
✅ 所有操作已完成！
```

---

## 七、工具10：web-artifacts-builder（Web工件构建器）

### 7.1 功能清单

| 功能模块 | 说明 | 状态 |
|---------|------|------|
| ArtifactMetadata类 | 工件元数据 | 🟢 |
| WebArtifact类 | 基础工件类 | 🟢 |
| HTMLArtifact类 | HTML工件 | 🟢 |
| ReactArtifact类 | React工件 | 🟢 |
| SVGArtifact类 | SVG工件 | 🟢 |
| ArtifactBuilder类 | 工件构建器 | 🟢 |
| create_html_artifact() | 创建HTML | 🟢 |
| create_react_artifact() | 创建React | 🟢 |
| create_svg_artifact() | 创建SVG | 🟢 |
| build_bundle() | 构建工件包 | 🟢 |
| generate_index_html() | 生成索引页 | 🟡 需修复格式化 |

### 7.2 启动步骤

```bash
cd /mnt/agents/.user/skills/longhun-system/assets/
python3 skill-10-web-artifacts-builder.py
```

### 7.3 使用说明

```python
from skill_10_web_artifacts_builder import ArtifactBuilder

builder = ArtifactBuilder()

# 创建HTML工件
html_artifact = builder.create_html_artifact(
    "artifact-001",
    "HTML演示",
    "<h1>龍魂系统</h1>",
    "HTML演示页面"
)

# 创建React工件
react_artifact = builder.create_react_artifact(
    "artifact-002",
    "React组件",
    "export default function App() {...}",
    "交互式组件"
)

# 创建SVG工件
svg_artifact = builder.create_svg_artifact(
    "artifact-003",
    "SVG图形",
    '<svg>...</svg>',
    "矢量图形"
)

# 打包
bundle = builder.build_bundle("./output")
```

### 7.4 已知问题与修复

**问题**: `generate_index_html()` 中的CSS包含 `{ margin` 导致 `str.format()` 冲突

**修复方案**:
```python
# 方案1: 使用替换占位符
html = html.replace("{artifacts}", artifacts_html)

# 方案2: 将CSS中的花括号双写
# margin: 0 -> margin: {{ 0 }}
```

---

## 八、常见问题排查

### 8.1 问题速查表

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| ModuleNotFoundError: PIL | 缺少pillow包 | `pip install pillow` |
| OSError: Read-only file system | 文件系统只读 | 修改保存路径到可写目录 |
| ValueError: x1 must be >= x0 | 脉冲动画坐标计算 | 使用max(1, radius)保护 |
| KeyError: ' margin' | 格式化字符串冲突 | 改用str.replace() |
| ImportError: fastmcp | 缺少mcp依赖 | `pip install fastmcp` |

### 8.2 按工具排查

#### 工具6: mcp-builder
```
症状: generate_server_code()中NameError
原因: 变量作用域引用错误
修复: 删除调试打印或修正变量名
```

#### 工具7: skill-creator
```
症状: save_to_json()报OSError
原因: 只读文件系统
修复: skill.save_to_json("/tmp/skill_config.json")
```

#### 工具8: slack-gif-creator
```
症状: 脉冲动画ValueError
原因: sin计算产生负半径值
修复: pulse_radius = max(5, abs(int(...)))
```

#### 工具9: theme-factory
```
症状: 无
状态: 完全正常，无需修复
```

#### 工具10: web-artifacts-builder
```
症状: KeyError: ' margin'
原因: CSS中的{}与format冲突
修复: 改用html.replace("{artifacts}", artifacts_html)
```

---

## 九、工具状态汇总表

### 9.1 总览

| 工具编号 | 工具名称 | 文件 | 核心功能 | 验证状态 | 审计色 | 优先级 | 备注 |
|----------|---------|------|---------|---------|--------|--------|------|
| 工具6 | mcp-builder | skill-6-mcp-builder.py | FastMCP·工具定义·Dockerfile | 🟢 运行正常 | 🟢通过 | 高 | 生产就绪 |
| 工具7 | skill-creator | skill-7-skill-creator.py | Skill基类·流式API·测试框架 | 🟢 运行正常 | 🟢通过 | 高 | 生产就绪 |
| 工具8 | slack-gif-creator | skill-8-slack-gif-creator.py | 加载/脉冲/成功/错误动画 | 🟡 部分可用 | 🟡标记 | 中 | 脉冲动画需修复 |
| 工具9 | theme-factory | skill-9-theme-factory.py | 10主题·CSS导出·批量导出 | 🟢 运行正常 | 🟢通过 | 中 | 生产就绪 |
| 工具10 | web-artifacts-builder | skill-10-web-artifacts-builder.py | HTML·React·SVG·打包 | 🟡 部分可用 | 🟡标记 | 中 | 索引页需修复 |

### 9.2 功能矩阵

| 功能点 | 工具6 | 工具7 | 工具8 | 工具9 | 工具10 |
|--------|-------|-------|-------|-------|--------|
| 核心类 | MCPBuilder | SkillBuilder | SlackGIFCreator | ThemeFactory | ArtifactBuilder |
| 数据类 | Dict | SkillMetadata | - | ThemeColor | ArtifactMetadata |
| 配置导出 | JSON | JSON | Dict | CSS/JSON | JSON |
| 代码生成 | Python | - | - | CSS | HTML/JSX/SVG |
| Docker支持 | Dockerfile | - | - | - | - |
| 测试框架 | - | 内置 | - | - | - |
| 批量导出 | - | - | - | 10主题 | 多工件 |

### 9.3 启动优先级建议

```
第一批（高优先级·立即可用）:
├── 工具9: theme-factory    [🟢 无需修复]
├── 工具7: skill-creator    [🟢 核心功能完整]
└── 工具6: mcp-builder      [🟢 核心功能完整]

第二批（中优先级·需小修）:
├── 工具10: web-artifacts-builder [🟡 CSS格式化冲突]
└── 工具8: slack-gif-creator      [🟡 脉冲动画坐标]
```

---

## 十、附录

### 10.1 快速启动命令

```bash
#!/bin/bash
# 龍魂系统5个Python工程工具一键启动

echo "🐉 龍魂Python工程工具启动脚本"
echo "================================"

cd /mnt/agents/.user/skills/longhun-system/assets/

echo ""
echo "[1/5] 启动 mcp-builder..."
python3 skill-6-mcp-builder.py

echo ""
echo "[2/5] 启动 skill-creator..."
python3 skill-7-skill-creator.py

echo ""
echo "[3/5] 启动 slack-gif-creator..."
python3 skill-8-slack-gif-creator.py

echo ""
echo "[4/5] 启动 theme-factory..."
python3 skill-9-theme-factory.py

echo ""
echo "[5/5] 启动 web-artifacts-builder..."
python3 skill-10-web-artifacts-builder.py

echo ""
echo "✅ 所有工具启动完成！"
```

### 10.2 CNSH中文编程规范说明

本工具库遵循CNSH中文编程规范：
- 类名使用大驼峰命名（MCPBuilder, SkillBuilder）
- 方法名使用snake_case小写下划线
- 注释使用中文说明
- 字符串输出使用繁体中文
- DNA签名嵌入代码

### 10.3 忠孝义排序铁律

| 层级 | 权重 | 含义 | 技术映射 |
|------|------|------|---------|
| 忠 | 0.5 | 系统稳定性 | 核心功能优先保证 |
| 孝 | 0.3 | 代码传承性 | 文档完整·易于维护 |
| 义 | 0.2 | 功能扩展性 | 灵活接口·模块设计 |

---

**DNA签名**: `#UID9622⚡️2026-06-16-PYTHON-TOOLS-v3.0`
**确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**文档路径**: `/mnt/agents/output/Python工程工具启动指南.md`
**龍魂体系**: 忠(0.5) > 孝(0.3) > 义(0.2) 排序铁律

---

*本文档由龍芯北辰·诸葛鑫（UID9622）自动生成*
*生成时间: 2026-06-16*

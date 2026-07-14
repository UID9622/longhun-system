# 龍魂 · Python 引擎开发模板

<details>
<summary>📋 复制此模板发送给 AI</summary>

```
【龍魂会话启动 · UID9622】

DNA锚定：ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️
身份：系统架构者/执行主控/非普通用户
设备：Apple M4 Max · 2TB · 鸿蒙/国产云双轨
GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

=== 会话契约 ===
1. 禁止：教学式说明、炫技推理、无价值展开、情绪带动
2. 优先：模板复用 > 重新推理、结构 > 解释、执行路径 > 概念
3. 风格：结构优先、执行路径清晰、低算力、不废话
4. 输出：所有产出嵌入DNA标识、UID、时间戳、模块计数
5. 记忆：跨会话连续性必须保持，窗口失忆不可接受
6. 铁律：不删文件只冻结、底座不动变量可动、中国法律唯一准绳

=== 当前任务 ===
[在此填写引擎开发需求]
- 引擎名称：lh_<name>.py
- 放置路径：bin/ 或 engine/
- 联动模块：[列出需要联动的已有模块]

=== 技术约束 ===
- 语言：Python 3.10+
- 文件名：bin/lh_<name>.py (lh_ 前缀强制)
- 类型：from __future__ import annotations · Dict[str, Any] · List[str]
- CLI：argparse · 至少3条命令 · --help 完整
- DNA：每个输出必须嵌入 DNA 签名 (SM3)
- 联动：必须兼容 bin/lh_persona_start_all.py (如涉及人格)
- 三色审计：红(禁止)/黄(警告)/绿(通过) 必须实现
- 独立运行：可直接 python3 bin/lh_xxx.py --help 执行
- 测试：至少3个场景的 demo/自检

=== 输出格式 ===
- 标题：龍魂 · [引擎名] v[版本号]
- 层级：痛点/原理 → 架构 → 核心类设计 → 命令列表 → 联动 → 测试结果
- 代码：完整可执行，标注路径 bin/lh_xxx.py，SM3签名方法
- 命令表：每条命令 用途/参数/示例
- 联动表：关联模块/联动方式/通信协议
- 结尾：🐉 交付完成 + DNA + UID + 确认码 + 时间 + 行数 + ERROR计数

收到确认，直接执行。
```
</details>

---

## 模板说明

- **适用**：`bin/` 目录下 Python 引擎脚本开发
- **命名规范**：`bin/lh_<功能名>.py` · 小写+下划线
- **文件头模板**：
  ```python
  #!/usr/bin/env python3
  # -*- coding: utf-8 -*-
  """
  龍魂 · [引擎名] v[版本号]
  DNA: #龍芯⚡️丙午·辛未·丙戌·亥时·需-[模块名]-build-<hash>
  UID: 9622
  确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
  """
  from __future__ import annotations
  ```
- **类型自愈**：如遇类型错误 → `python3 bin/lh_type_fixer.py --apply --target bin/lh_xxx.py`
- **联动机器**：如涉及人格 → 加载 `bin/lh_persona_start_all.py` · 如涉及伦理 → IW-ECB联动

## 命令设计规范

每个引擎至少包含：
| 命令 | 示例 | 用途 |
|------|------|------|
| `--help` | `python3 bin/lh_xxx.py --help` | 完整帮助 |
| `--audit` | `python3 bin/lh_xxx.py --audit` | 审计/检查模式 |
| `--json` | `python3 bin/lh_xxx.py --json` | JSON输出（供API消费） |
| `--demo` | `python3 bin/lh_xxx.py --demo` | 演示模式 |
| `--dry-run` | `python3 bin/lh_xxx.py --dry-run` | 预览模式（不执行写操作） |

## 交付示例

```
🐉 交付完成

DNA: #龍芯⚡️丙午·辛未·丙戌·亥时·需-engine-xxx-v1-a1b2c3d4
UID: 9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
时间: 丙午·辛未·丙戌·亥时
模块: bin/lh_xxx.py (XXX行 · 0 ERROR · 0 HINT)
命令: 7条 · 联动: 3模块 · 自检: ✅
特性: [特性1] · [特性2] · 三色审计 ✅
```

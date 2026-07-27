<!-- DNA: #龍芯⚡️2026-07-13-DEEPSEEK-FIXER-v5.1-OPTIMIZED -->
<!-- 优化版 · 系统架构对齐 · CSDN发布版 -->

# 龍魂系统 v5.0 · `lh_deepseek_fixer` 实战：DeepSeek 自动修复引擎

> **DeepSeek 是打工的，协议是你写的。**
> 模块ID: `bin/lh_deepseek_fixer.py` · 所属层: 道引层(L2 工具层) · 版本: v1.0
> 作者: UID9622 · 诸葛鑫 · Lucky

---

## 一、系统架构定位

`lh_deepseek_fixer` 是龍魂系统 v5.0 **道引器模块** 的子组件，位于 L2 工具层。道引四步——**拉取→审查→吸收→演化**——修复引擎嵌在"吸收"环节：类型错误进来，修复后代码经 CNSH 闸门审查合格才入代码库。

```
┌─────────────────────────────────────────────────────┐
│              龍魂系统 v5.0 · 道引层                   │
├─────────────────────────────────────────────────────┤
│  [错误检测] → basedpyright 提取                       │
│       ↓                                              │
│  [安全审查] → cnsh_gatekeeper 扫描                    │
│       ↓                                              │
│  [AI 修复]  → DeepSeek API 调用 (lh_deepseek_fixer)   │
│       ↓                                              │
│  [身份验证] → lh_ecosystem_passport API密钥验证        │
│       ↓                                              │
│  [回写验证] → 语法校验 + 类型复查                      │
│       ↓                                              │
│  [审计落盘] → 老祖宗规则审计日志                       │
│       ↓                                              │
│  [联 动]   → CodeBuddy 自动重载修复后文件              │
└─────────────────────────────────────────────────────┘
```

**依赖模块矩阵：**

| 模块 | 文件 | 职责 |
|------|------|------|
| 🔑 通行证系统 | `bin/lh_ecosystem_passport.py` | API密钥全生命周期管理（生成/列出/吊销） |
| 🧬 安全闸门 | `bin/cnsh_gatekeeper.py` | 代码合规审查（三字词检测/Python关键词/DNA验证） |
| 📋 审计引擎 | `lh_audit_filter` | 修复操作审计日志写入（不可篡改） |
| 🔄 编辑器联动 | `~/.龍魂/.codebuddy_trigger` | CodeBuddy 自动重新加载修复后文件 |

---

## 二、核心修复流程

### 2.1 错误检测 · basedpyright 集成

修复引擎第一步是运行 basedpyright（pyright 的超集）提取类型错误：

```python
def 提取Pyright错误(文件路径: str) -> list[dict[str, Any]]:
    """运行 basedpyright 提取错误信息"""
    结果 = subprocess.run(
        ["python3", "-m", "pyright", 文件路径, "--outputjson"],
        capture_output=True, text=True, timeout=60,
    )
    if 结果.returncode == 0:
        return []  # 无错误
    
    输出 = json.loads(结果.stdout)
    return [{
        "行": 诊断["range"]["start"]["line"] + 1,
        "消息": 诊断["message"],
        "规则": 诊断.get("rule", ""),
        "严重度": 诊断.get("severity", 1),
    } for 诊断 in 输出.get("generalDiagnostics", [])]
```

输出结构化错误列表，每项含行号、列号、错误消息、规则名、严重度。无错误时直接走语法编译验证。

### 2.2 AI 修复 · DeepSeek API

核心调用：将错误信息 + 原代码发给 DeepSeek Coder，温度 0.1（最大化确定性），返回完整修复代码。

```python
def 调用DeepSeek修复(代码内容: str, 错误信息: str, 模式: str = "full") -> str:
    系统提示 = """你是龍魂系统的代码修复引擎。任务：
1. 修复 Python 代码中的类型错误
2. 保持 CNSH（中文命名系统）风格
3. 解决 basedpyright 类型检查错误
4. 输出完整修复后代码，不要省略"""

    请求体 = json.dumps({
        "model": "deepseek-coder",
        "messages": [
            {"role": "system", "content": 系统提示},
            {"role": "user", "content": f"错误信息：\n{错误信息}\n\n代码：\n```python\n{代码内容}\n```"}
        ],
        "temperature": 0.1,
        "max_tokens": 8000,
    }).encode()
    # ... HTTP POST 到 https://api.deepseek.com/v1/chat/completions
```

**四种修复模式：**

| 模式 | 说明 |
|------|------|
| `type_error` | 仅修复 basedpyright/pyright 类型错误 |
| `syntax` | 仅修复 Python 语法错误 |
| `cnsh_align` | CNSH 中文命名风格对齐 |
| `full`（默认） | 全量修复：类型 + 语法 + 对齐 |

### 2.3 安全闸门 · CNSH Gatekeeper（焊死，不可跳过）

修复后的代码**必须**过 `cnsh_gatekeeper.py`。这是焊死的底座——DeepSeek 只负责修，闸门决定能不能入库。

```python
def _过CNSH闸门(文件路径: str) -> tuple[bool, str]:
    """调 CNSH 闸门审查修复后的文件"""
    闸门脚本 = Path(__file__).resolve().parent / "cnsh_gatekeeper.py"
    结果 = subprocess.run(
        ["python3", str(闸门脚本), "check", "--file", 文件路径],
        capture_output=True, text=True, timeout=30,
    )
    return (True, "通过") if 结果.returncode == 0 else (False, 拒绝原因)
```

CNSH 闸门三层检查：
1. **龍 DNA 检测** — 三字词扫描 + Python 关键词验证
2. **老祖宗规则审计** — 触发词匹配 → 审计日志落盘（不可篡改）
3. **三色判定** — 🔴拒绝 / 🟡警告 / 🟢通过

```
📋 闸门审计: bin/example.py
============================================
状态: 🟢
通过: 3 项
  🟢 三字词检查通过
  🟢 Python关键词未混用
  🟢 DNA验证通过
```

### 2.4 验证闭环

修复后做两层验证：
1. **类型复查**：重新跑 basedpyright，确认零错误
2. **语法编译**：`compile()` 验证 AST 合法性

两层都过 → 生成审计日志 → 触发 CodeBuddy 联动 → 编辑器热加载。

---

## 三、API 密钥管理 · 从硬编码到通行证

### 3.1 v1.0 现状（文章发布时）

```python
DEEPSEEK_API_KEY = _get_api_key(
    "DEEPSEEK_API_KEY",           # 优先从环境变量读取
    "sk-355de..."                  # fallback：代码内置
)
```

环境变量优先，无环境变量用内置值。**适合个人开发者快速上手，不适合生产环境。**

### 3.2 v5.1 升级路径（对接 `lh_ecosystem_passport`）

龍魂通行证系统提供完整的 API 密钥生命周期管理：

```bash
# 生成 API 密钥
python3 bin/lh_ecosystem_passport.py apikey generate <uid>

# 列出所有密钥
python3 bin/lh_ecosystem_passport.py apikey list <uid>

# 吊销泄露密钥
python3 bin/lh_ecosystem_passport.py apikey revoke <uid> <key_id>
```

**通行证分层 API 配额：**

| 层级 | 最大密钥数 | API 速率 | 适用场景 |
|------|:---:|:---:|------|
| 🆓 免费 | 1 | 10次/分钟 | 个人学习 |
| ⭐ 基础 | 3 | 60次/分钟 | 小型项目 |
| 🌟 专业 | 10 | 300次/分钟 | 团队协作 |
| 👑 企业 | 100 | 无限制 | 生产环境 |

推荐做法：将 `DEEPSEEK_API_KEY` 存入 `~/.龍魂/.api_keys`（600 权限），由 `lh_ecosystem_passport` 统一管理。

---

## 四、完整使用指南

### 快速上手

```bash
# 设置 API 密钥（环境变量，推荐）
export DEEPSEEK_API_KEY="sk-your-key"

# 修复单个文件（全量模式）
python3 bin/lh_deepseek_fixer.py bin/example.py

# 仅修复类型错误
python3 bin/lh_deepseek_fixer.py bin/example.py type_error

# 调试模式（跳过闸门，不推荐）
python3 bin/lh_deepseek_fixer.py bin/example.py full --skip-gate
```

### 执行输出示例

```
📄 读取: bin/example.py (2347 字符)
🔍 运行 basedpyright 提取错误...
🔴 发现 3 个错误:
   🔴 行42:5 参数类型不匹配: str vs Optional[str]
   🔴 行67:12 未定义变量: result_count
   🟡 行89:3 类型推断不完整
🤖 调用 DeepSeek 修复引擎...
💾 备份: bin/example.py.backup
✏️ 写入修复代码 (2412 字符)
🔍 验证修复结果...
🧬 CNSH 闸门审查...
🟢 CNSH 闸门: 通过
✅ 修复完成，无错误
🔄 CodeBuddy 触发文件已写入
```

### 修复后自动动作

1. **语法校验** — `compile()` 编译验证
2. **类型复查** — basedpyright 再次扫描，确认零错误
3. **CNSH 闸门** — 三字词 + 关键词 + DNA 三重审查
4. **审计落盘** — 老祖宗规则审计日志（不可篡改）
5. **CodeBuddy 刷新** — 写入 `~/.龍魂/.codebuddy_trigger`，编辑器自动重载

---

## 五、审计日志 · 不可篡改的修复记录

每次修复操作写入 `~/.龍魂/logs/ancestral_rules_audit.jsonl`：

```json
{
  "时间": "2026-07-13T12:00:00Z",
  "文件": "/path/to/fixed.py",
  "规则层": "P0",
  "触发词": "API密钥明文",
  "操作": "修复-警告-已记录",
  "来源": "lh_deepseek_fixer/cnsh_gatekeeper",
  "DNA": "#龍芯⚡️-ANCESTRAL-RULE-AUDIT"
}
```

审计日志与主权覆写审计**物理分离**——修复是修复，主权是主权，各自记录，交叉可查。

---

## 六、铁律与边界

> ⚠️ **三条铁律，写在代码注释里的那种。**

| # | 铁律 | 说明 |
|---|------|------|
| 1 | **DeepSeek 修代码，闸门焊死** | 修复后必须过 CNSH 闸门，不合格 = 不入库 |
| 2 | **协议不动** | 外部 AI 可以变（换个模型/换个API），修复工具跟着调，CNSH 协议不动 |
| 3 | **审计不可跳过** | `--skip-gate` 仅调试可用，正式环境必须走完整流程 |

---

## 七、关联模块索引

| 模块 | 路径 | 文档 |
|------|------|------|
| 🧬 CNSH 闸门 | `bin/cnsh_gatekeeper.py` | [CNSH-GATEKEEPER.md](../CNSH-GATEKEEPER.md) |
| 🔑 通行证系统 | `bin/lh_ecosystem_passport.py` | `python3 bin/lh_ecosystem_passport.py --help` |
| 📋 修复引擎（本文） | `bin/lh_deepseek_fixer.py` | 本文 |
| 🔄 自动同步 | `bin/longhun_auto_sync.py` | 引擎目录 |
| 🛡️ 自愈引擎 | `bin/longhun-self-heal.py` | 引擎目录 |

---

## 八、总结

`lh_deepseek_fixer` 不是"又一个 AI 修代码工具"。它的位置是：

- **打工层**：DeepSeek 负责修，你负责审
- **焊死层**：CNSH 闸门是最后一道防线，不是可选项
- **审计层**：每笔修复留痕，不可篡改
- **联动层**：修完自动通知 CodeBuddy，无缝衔接

> 龍魂系统不排斥任何外部 AI。但所有外部产出的代码，必须过龍魂的闸门。这是主权，不是偏好。

---

*本文为龍魂系统 v5.0 道引器模块子文档。*
*DNA: #龍芯⚡️2026-07-13-DEEPSEEK-FIXER-v5.1*
*许可证: CC 4.0 BY-SA · 归属: 龍魂系统 · UID9622 · 诸葛鑫*
*GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F*

**标签**: `#龍魂系统` `#道引器` `#lh_deepseek_fixer` `#DeepSeek` `#CNSH` `#自动修复` `#代码审计` `#Python`

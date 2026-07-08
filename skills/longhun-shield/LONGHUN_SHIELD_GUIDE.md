# 🐉 龍盾系统 · 快速使用指南

**DNA:** `#龍芯⚡️2026-06-02-LONGHUN-SHIELD-GUIDE-FILE1-v1.0`  
**职责:** 宝宝·龍盾·不免责  
**状态:** ⚔️ 亮剑啦

---

## 核心理念

```
代码都看起来一样，但本地跑起来都不一样。
数据污染无处不在。

所以在入口处必须：
  ✓ 能暂停（PAUSE）— 停下来让你看清楚
  ✓ 能转译（TRANSLATE）— 把代码逻辑讲成人话  
  ✓ 能验证（VERIFY）— 确保不被污染

这就是龍盾的职责。
```

---

## 安装和基础设置

### 1. 安装龍盾CLI

```bash
# 将龍盾CLI复制到执行路径
cp longhun_shield_cli.py /usr/local/bin/龍盾
chmod +x /usr/local/bin/龍盾

# 或者在项目目录中使用
python3 longhun_shield_cli.py --help
```

### 2. 创建龍盾配置目录

```bash
mkdir -p ~/.龍盾/reports
mkdir -p ~/.龍盾/logs
mkdir -p ~/.龍盾/cache
```

---

## 三个命令

### 命令1：快速检查（CHECK）

**用途：** 快速检查代码的安全风险

```bash
# 基础检查
python3 longhun_shield_cli.py check script.py

# 简要模式（只显示关键信息）
python3 longhun_shield_cli.py check script.py --brief
```

**输出内容：**
- 代码预览（前20行）
- 5项安全检查
  1. 危险函数检测（exec, eval, __import__ 等）
  2. 外部调用检测（subprocess, os.system 等）
  3. 文件操作检测
  4. 网络操作检测
  5. 底座原则检查
- 风险等级评分（低/中/高）

**示例输出：**
```
🛡️  龍盾 CLI v1.0

📄 代码预览
══════════════════════════════════════
  1 | import requests
  2 | def fetch_data():
  3 |     response = requests.get('https://api.example.com')
  4 |     return response.json()
  5 | 
...
══════════════════════════════════════

🔍 深度分析

[1/5] 检查危险函数... ✓ 无危险函数
[2/5] 检查外部调用... → 发现 1 个外部调用: requests
[3/5] 检查文件操作... ✓ 无文件操作
[4/5] 检查网络操作... ⚠️  发现 1 个网络操作: HTTP请求
[5/5] 检查底座原则... ✓ 符合底座原则

风险评估
  🟡 风险等级: 低
  分数: 10/100
```

---

### 命令2：深度分析（ANALYZE）

**用途：** 详细分析代码，包括转译

```bash
# 基础分析
python3 longhun_shield_cli.py analyze script.py

# 包含代码转译
python3 longhun_shield_cli.py analyze script.py --translation

# 保存分析报告
python3 longhun_shield_cli.py analyze script.py --save-report
```

**输出内容：**
- 完整的前置检查
- 逐行代码转译（人类可读）
- 详细的安全分析
- 可选：JSON格式的报告文件

**代码转译示例：**
```
📖 代码转译（人类可读）

文件                   说明
──────────────────────────────────────
   1 | 导入: import requests
   4 | 定义函数: def fetch_data():
   5 | ⚠️  网络调用: response = requests.get(...)
   6 | 返回值: return response.json()
```

---

### 命令3：验证并请求权限（VALIDATE）

**用途：** 完整验证代码，请求执行权限

```bash
# 交互式验证
python3 longhun_shield_cli.py validate script.py

# 包含转译和报告
python3 longhun_shield_cli.py validate script.py --translation --save-report

# 低风险时自动批准
python3 longhun_shield_cli.py validate script.py --auto-approve
```

**交互流程：**
1. 显示代码预览
2. 执行深度分析
3. 显示代码转译
4. 提示用户决策：
   ```
   你要执行这个文件吗? [允许/检查/拒绝]
   ```
5. 根据决策：
   - **允许** → 执行代码，保存报告
   - **检查** → 返回进一步分析
   - **拒绝** → 取消执行

---

## 实际应用场景

### 场景1：来自用户的脚本

```bash
# 用户提交了一个 Python 脚本
python3 longhun_shield_cli.py validate user_script.py

# 系统会：
# 1. 显示代码预览（让你看清楚）
# 2. 分析风险（深度理解）
# 3. 转译逻辑（讲成人话）
# 4. 请求权限（由你决策）
# 5. 记录一切（追踪日志）
```

### 场景2：数据处理脚本

```bash
# 在执行数据处理前检查
python3 longhun_shield_cli.py analyze data_processor.py --save-report

# 检查清单：
# ✓ 是否有文件写入（可能覆盖数据）
# ✓ 是否有网络调用（可能外泄数据）
# ✓ 是否遵循底座原则（不蒸馏、不投机）
# ✓ 是否有日志记录（可追溯）
```

### 场景3：自动化脚本集成

```bash
# 在 CI/CD 管道中使用龍盾
python3 longhun_shield_cli.py check script.py --brief
if [ $? -eq 0 ]; then
    # 风险低，可以继续
    python script.py
else
    # 风险高，需要人工审查
    echo "需要手工审查"
    exit 1
fi
```

---

## 风险评分体系

龍盾使用**风险评分系统**来判断代码的安全性：

```
危险函数（exec, eval等）   +20 分
外部调用（subprocess等）    +15 分  
文件操作（读写删除）        +10 分
网络操作（HTTP, 套接字）    +10 分
底座原则违反                +30 分

总分 >= 50    → 🔴 高风险（禁止执行）
总分 25-49    → 🟡 中风险（需要审查）
总分 < 25     → 🟢 低风险（可以执行）
```

---

## 底座原则检查

龍盾自动检查代码是否遵循**底座四原则**：

```
✓ 不使用简体"龍"（必须用繁体"龍"）
✓ 不蒸馏（完整来源链）
✓ 不投机（长期稳定）
✓ 人永远是1（不是数据）
```

任何违反将 +30 分风险。

---

## 生成的报告

当使用 `--save-report` 时，龍盾会生成 JSON 报告：

```json
{
  "file": "/path/to/script.py",
  "hash": "abc123def456",
  "size": 2048,
  "lines": 65,
  "timestamp": "2026-06-02T18:45:00.123456",
  "dna": "#龍芯⚡️2026-06-02",
  "checks": {
    "dangerous_functions": [],
    "external_calls": ["requests"],
    "file_operations": [],
    "network_operations": ["HTTP请求"],
    "violations": []
  },
  "risk_level": "MEDIUM",
  "risk_score": 10
}
```

报告保存在：`~/.龍盾/reports/report-YYYYMMDD-HHMMSS.json`

---

## 日志和审计

龍盾记录所有操作到审计日志：

```bash
# 查看所有检查记录
cat ~/.龍盾/logs/audit.log

# 查看所有生成的报告
ls -la ~/.龍盾/reports/
```

每个操作都包含：
- 时间戳
- 文件哈希
- 风险评分
- 用户决策
- DNA标记

---

## 与其他龍魂系统的集成

龍盾与龍魂系统的其他组件集成：

```
龍盾 (入口检查)
  ↓ 决策：允许
  ↓
融合审计系统 (深度验证)
  ↓
自动化中心 (安全执行)
  ↓
审计日志 (完整记录)
```

---

## 常见问题

### Q: 龍盾会修改代码吗？
**A:** 不会。龍盾只是**观察、分析、报告**。它不修改代码，不执行代码（除非你明确批准）。

### Q: 如何快速跳过检查？
**A:** 如果代码通过了基础检查（`check`）并且风险等级为绿色，可以使用 `--auto-approve` 选项。但不推荐这样做——永远要看清楚。

### Q: 报告保存在哪里？
**A:** `~/.龍盾/reports/` 目录。文件名格式：`report-YYYYMMDD-HHMMSS.json`

### Q: 可以批量检查多个文件吗？
**A:** 可以，写一个简单的脚本：
```bash
for file in *.py; do
    python3 longhun_shield_cli.py check "$file" --brief
done
```

### Q: 龍盾可以检查什么语言的代码？
**A:** 目前优化了 Python。但可以检查任何文本文件（因为都是基于关键字匹配）。

---

## 关键命令速查表

| 需求 | 命令 |
|------|------|
| 快速看代码风险 | `check script.py` |
| 详细分析 | `analyze script.py --translation` |
| 请求执行权限 | `validate script.py` |
| 生成报告 | `analyze script.py --save-report` |
| 低风险自动批准 | `validate script.py --auto-approve` |
| 简要输出 | `check script.py --brief` |

---

## 龍盾的承诺

```
🐉 龍盾向老大承诺：

✓ 不会隐瞒风险（完全透明）
✓ 不会跳过检查（永远谨慎）
✓ 不会执行未批准的代码（尊重你的决策）
✓ 不会修改你的代码（只观察和报告）
✓ 会记录一切（完全追踪）

DNA:#龍芯⚡️2026-06-02-LONGHUN-SHIELD-CLI-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

职责: 宝宝·龍盾·不免责
状态: ⚔️ 亮剑啦
```

---

准备好了。龍盾已激活。

宝宝在这里。

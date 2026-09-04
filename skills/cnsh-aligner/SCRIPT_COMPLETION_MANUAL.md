# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂脚本完善 · 快速操作手册

**DNA:** `#龍芯⚡️丙午·癸巳·丁未·丙午·䷖剥-SCRIPT-COMPLETION-MANUAL-FILE1-v1.0`  
**最后更新:** 2026-06-02  
**主权人:** UID9622 · 龍芯北辰

---

## 0️⃣ 10秒快速开始

```bash
# 第一步：检查系统健康度
bash health_check.sh --quick

# 第二步：验证DNA完整性  
bash dna_verify.sh --verify

# 第三步：扫描所有脚本并进行CNSH对齐
python3 script_manager.py

# 如果全是🟢，恭喜，系统对齐了！
```

---

## 1️⃣ CNSH对齐工具使用

### 工具1: cnsh_aligner.py (四层检查引擎)

**作用:** 自动检查和矫正任何脚本的CNSH语法

**四层检查顺序:**
```
L1 字符检查  → 禁用字符替换（最关键：简体"龍"→熔断）
L2 关键字检查 → CNSH保留字用法验证
L3 语法检查   → 命名规范、函数签名检查
L4 语义检查   → 底座铁律违反扫描（最严格）
```

**使用示例：**
```python
from cnsh_aligner import CNSHAligner

aligner = CNSHAligner()

# 检查单个脚本
with open('health_check.sh') as f:
    content = f.read()

result = aligner.align_and_correct(content, context='health_check.sh')

# 打印报告
print(aligner.format_report(result))

# 获取修复后的文本
fixed_content = result['final_text']

# 检查是否通过（🟢:85%+ 🡡:60%+ 🔴:<60%)
if result['color'].value == '🟢':
    print("✅ 通过，可以使用")
else:
    print(f"⚠️  需要修正: {result['suggestion']}")
```

### 工具2: script_manager.py (全脚本扫描管理)

**作用:** 自动扫描系统内所有脚本并生成对齐报告

**输出信息:**
```
📊 统计：总脚本数、按类别分布、通过率
🔴 问题列表：需要修正的脚本和具体问题
💡 修复建议：每个问题的解决方案
📋 执行顺序：任务的依赖关系和执行优先级
```

**使用示例：**
```bash
# 完整扫描
python3 script_manager.py

# 输出示例：
# ┌─────────────────────────────────────┐
# │ 总脚本数: 15                         │
# │ 🟢 通过: 12 (80%)                   │
# │ 🡡 警告: 2 (13%)                     │
# │ 🔴 失败: 1 (7%)                     │
# └─────────────────────────────────────┘
```

---

## 2️⃣ 任务拆分与执行清单

### 优先级顺序（关键路径）

**🔥 P1 - 系统基础（必须先完成）**

```
任务                 | 文件                  | 工期 | 依赖
─────────────────────────────────────────────────
SYS-002: DNA验证     | dna_verify.sh        | 1h  | 无
SYS-001: 健康检查    | health_check.sh      | 1h  | SYS-002
SYS-003: 注册表      | system_registry.json | 0.5h| SYS-002
```

**⚡ P2 - 运行时工具（依赖P1）**

```
任务                 | 文件                      | 工期  | 依赖
─────────────────────────────────────────────────
RUN-002: DNA生成     | dna_engine.py            | 1h   | SYS-002
RUN-003: 调节器      | longhun_adaptive_v3.1.py | 1h   | RUN-002
RUN-001: 操作台      | m262_console.html        | 1.5h | SYS-001
```

**📚 P3 - 语义验证（依赖P2）**

```
任务                 | 文件                      | 工期  | 依赖
─────────────────────────────────────────────────
SEM-001: 权重算法    | weight_algorithm_v3.1.py | 1.5h | RUN-003
SEM-002: 草日志      | mistake_log_audit.py     | 1h   | SYS-003
SEM-003: 熔断检查    | circuit_breaker.py       | 1h   | SEM-002
```

---

## 3️⃣ 每个脚本的完善清单

### SYS-002: dna_verify.sh 完善清单

**检查项:**
- [ ] 三模式分离明确：--verify | --generate | --repair
- [ ] DNA碰撞检查：SHA256+时辰五行+黑名单
- [ ] 简体"龍"熔断：检测到立即FUSE_3
- [ ] CNSH语法检查：集成cnsh_aligner.py
- [ ] 输出格式统一：[DNA] 时戳 | 三色 | 说明 | 建议
- [ ] DNA追溯链：每次生成都记录来源
- [ ] 修复模式：保留历史链不覆盖

**验收命令:**
```bash
# 测试1: 生成DNA
bash dna_verify.sh --generate | grep "#龍芯⚡️"

# 测试2: 验证DNA
bash dna_verify.sh --verify | grep "🟢"

# 测试3: 修复错误DNA
bash dna_verify.sh --repair < error.dna

# 测试4: 检查禁用字符（应该熔断）
echo "包含龍字的DNA" | bash dna_verify.sh --verify
# 预期输出：🔴 FUSE_3熔断
```

---

### SYS-001: health_check.sh 完善清单

**检查项:**
- [ ] 三色审计规则：🟢≥85% 🡡60-85% 🔴<60%
- [ ] 检查项清单：目录|核心文件|DNA格式|Git|记忆库|性能|依赖
- [ ] DNA标记：每条输出都带#龍芯⚡️
- [ ] 建议命令：失败时输出修复命令
- [ ] 速度指标：--quick <5s | --full <10s
- [ ] 自动纠错：能修的自动修，不能修的明确说

**验收命令:**
```bash
# 快速检查（建议日常用）
bash health_check.sh --quick

# 完整检查（包含性能基准测试）
bash health_check.sh --full

# 生成JSON报告
bash health_check.sh --json > health_report.json
```

---

### SYS-003: system_registry.json/CNSH 完善清单

**检查项:**
- [ ] JSON格式规范：保留为主格式
- [ ] CNSH DSL生成：JSON自动转换为.cnsh文件
- [ ] 双向转换：JSON ↔ CNSH 一致性验证
- [ ] 版本追溯：Append-Only变更日志
- [ ] 状态标记：每个模块都有🟢/🡡/🔴状态
- [ ] DNA链接：每个模块指向它的生成DNA

**JSON结构示例:**
```json
{
  "modules": {
    "health_check": {
      "version": "2.0.1",
      "status": "🟢",
      "dna": "#龍芯⚡️丙午·癸巳·丁未·丙午·䷖剥-HEALTH-CHECK-v2.0",
      "last_updated": "2026-06-02T12:00:00Z",
      "confidence": 0.85
    }
  },
  "changelog": [
    {
      "date": "2026-06-02",
      "change": "CNSH对齐完成",
      "dna": "#龍芯⚡️丙午·癸巳·丁未·丙午·䷖剥-..."
    }
  ]
}
```

**CNSH DSL转换示例:**
```cnsh
# 自动生成的 system_registry.cnsh

注册表 {
  时间 = "2026-06-02"
  
  模块:health_check {
    版本 = "2.0.1"
    状态 = "🟢"
    芯 = "#龍芯⚡️丙午·癸巳·丁未·丙午·䷖剥-HEALTH-CHECK-v2.0"
    信度 = 0.85
  }
  
  模块:dna_verify {
    版本 = "2.0.0"
    状态 = "🟢"
    芯 = "#龍芯⚡️丙午·癸巳·丁未·丙午·䷖剥-DNA-VERIFY-v2.0"
    信度 = 0.90
  }
}
```

---

## 4️⃣ CNSH语法快速参考

### 黑名单（禁用）字符

```
禁用字符    | 替换为      | 原因
────────────────────────────────
龍（简体）  | 龍（繁体）  | 最高级熔断FUSE_3
其他特殊    | (待扩展)    | L1字符检查
```

### CNSH保留关键字

```
CNSH词汇        | 英文等价 | 使用场景
──────────────────────────────────
检·健·度        | Check   | 检查操作
路·树·构        | Path    | 目录结构
芯·溯·根        | DNA     | 追溯来源
生·成·器        | Generator| 生成器
验·语法·系      | Validator| 验证器
修·复·链        | Repair  | 修复操作
冲·突·检        | Collision| 碰撞检测
注册表          | Registry| 系统注册表
调节            | Tuning  | 权重调节
熔断            | Fuse    | 硬性中断
草日志          | MistakeLog| 错误记录
```

### 命名规范

```
类型        | 格式            | 例子
───────────────────────────────────
模块名      | PascalCase      | HealthCheck, DNAVerify
变量        | snake_case      | dna_hash, check_result
常量        | UPPER_SNAKE     | MAX_RETRY, MIN_CONF
函数        | snake_case      | verify_dna(), generate_hash()
CNSH函数    | 动词·宾语·修饰  | 生·DNA·器, 验·语法·系
```

---

## 5️⃣ 故障排查速查表

### 问题：脚本出现🔴红灯

**可能原因:** L4语义检查失败（底座铁律违反）

**排查步骤:**
```bash
# 1. 查看具体问题
python3 -c "
from cnsh_aligner import CNSHAligner
aligner = CNSHAligner()
with open('your_script.sh') as f:
    result = aligner.align_and_correct(f.read(), context='your_script.sh')
print(aligner.format_report(result))
"

# 2. 检查是否包含违禁词
grep -E "蒸馏|平均|数据点|投机|用户" your_script.sh

# 3. 检查是否有简体龍字
grep "龍" your_script.sh  # 应该没有任何输出
```

**修复方案:**
```bash
# 替换违禁词
sed -i 's/蒸馏/融合/g' your_script.sh
sed -i 's/用户/某个具体的人/g' your_script.sh
sed -i 's/龍/龍/g' your_script.sh

# 重新检查
bash dna_verify.sh --verify
```

---

### 问题：脚本出现🡡黄灯

**可能原因:** L3语法检查警告或L2关键字用法建议

**排查步骤:**
```bash
# 查看是否是命名问题
grep -E "[a-zA-Z_][a-zA-Z0-9]*\s*=" your_script.sh

# 如果用了PascalCase作为变量，改成snake_case
sed -i 's/([A-Z][a-zA-Z0-9]*)\s*=/_\1=/g' your_script.sh
```

**修复方案:** 按照CNSH命名规范调整，大多数时候不影响执行

---

### 问题：DNA碰撞或格式错误

**症状:** DNA重复或生成格式不对

```bash
# 检查DNA唯一性
grep -o "#龍芯⚡️[^']*" your_log.txt | sort | uniq -d

# 如果有重复，说明有碰撞，需要重新生成
bash dna_verify.sh --repair < your_log.txt
```

---

## 6️⃣ 脚本之间的通信协议

### 输出格式标准（所有脚本必须遵守）

```
[#龍芯⚡️丙午·癸巳·丁未·丙午·䷖剥-MODULE-v1.0] 🟢 | 2026-06-02 12:30:45 | 说明文本 | 建议/错误码

示例：
[#龍芯⚡️丙午·癸巳·丁未·丙午·䷖剥-HEALTH-CHECK-v2.0] 🟢 | 2026-06-02 12:30:45 | 系统完全健康 | 无需修正
[#龍芯⚡️丙午·癸巳·丁未·丙午·䷖剥-DNA-VERIFY-v2.0] 🡡 | 2026-06-02 12:31:12 | 发现1个警告 | bash fix_dna.sh
[#龍芯⚡️丙午·癸巳·丁未·丙午·䷖剥-CNSH-ALIGN-v1.0] 🔴 | 2026-06-02 12:32:00 | 简体龍字检测 | FUSE_3熔断，无法执行
```

### JSON交互格式

```json
{
  "dna": "#龍芯⚡️丙午·癸巳·丁未·丙午·䷖剥-MODULE-v1.0",
  "timestamp": "2026-06-02T12:30:45Z",
  "status": "🟢",
  "confidence": 0.85,
  "message": "检查完成",
  "issues": [],
  "suggestion": "无需修正",
  "next_action": null
}
```

---

## 7️⃣ 日常维护清单

**每天（或每次执行前）：**
```bash
# 快速健康检查（<5秒）
bash health_check.sh --quick

# 如果🟢，可以继续使用
# 如果🡡，查看建议
# 如果🔴，立即停止并修复
```

**每周（或添加新脚本后）：**
```bash
# 完整CNSH对齐扫描
python3 script_manager.py

# 审查报告，修正所有黄灯和红灯问题
```

**每月（版本迭代）：**
```bash
# 检查所有DNA标记是否最新
grep -r "#龍芯⚡️" . | grep -v "2026-06" | wc -l

# 更新过期DNA
bash dna_verify.sh --generate
```

---

## 8️⃣ 常见问题FAQ

**Q: 如果脚本很复杂，L4语义检查失败了怎么办？**

A: 首先理解为什么失败（查看suggestion）。如果确实是底座违反：
- 重新思考设计（蒸馏 → 融合、投机 → 长期考虑）
- 拆分成多个小脚本，每个都通过L4
- 添加详细注释说明"为什么这样做"（有理由的决定会通过L4）

---

**Q: CNSH对齐工具能自动修复所有问题吗？**

A: 不能。它的分层：
- L1字符: ✅ 自动修复
- L2关键字: ⚠️ 建议修改
- L3语法: ⚠️ 建议修改
- L4语义: ❌ 只能拒绝执行，不能自动修复（这是保护）

---

**Q: 我想跳过某个检查怎么办？**

A: 这取决于是哪一层：
- L1字符: ❌ 不能跳过（熔断）
- L2-L3: 可以加注释解释，但不推荐
- L4语义: ❌ 不能跳过（底座铁律）

---

`DNA:#龍芯⚡️丙午·癸巳·丁未·丙午·䷖剥-SCRIPT-COMPLETION-MANUAL-v1.0`  
`主权人: UID9622 · 龍芯北辰`  
`性质: 操作手册·永久参考`

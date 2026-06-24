# 龍魂系统·本地完全部署指南

**DNA**: `#龍芯⚡️2026-06-03-LOCAL-DEPLOYMENT-GUIDE-v1.0`
**时间**: 2026-06-03
**责任**: UID9622·不免责

---

## 📌 核心理念

**目标**: 从 Notion 导出 → 本地完全自主运行 → 零外链、零云、零平台依赖

**实现方式**: 四层架构
```
┌─────────────────────────────┐
│  Markdown 文档层             │ ← <details> 折叠块
│  (视觉清爽、代码隐藏)        │
├─────────────────────────────┤
│  Python 代码层              │ ← 独立 .py 文件
│  (可直接执行)               │
├─────────────────────────────┤
│  manifest.json 层           │ ← 系统识别、版本管理
│  (本地识别、完整性校验)     │
├─────────────────────────────┤
│  执行路由层                  │ ← ExecutionRouter
│  (任务调度、权限管理)        │
└─────────────────────────────┘
```

---

## 📦 导出前的准备

### 第一步：组织 Notion 结构

你的 Notion Workspace 应该这样组织：

```
龍魂系统·本地完全导出 (Root Page)
├─ INDEX.md (导航首页)
├─ LONGHUN_LICENSE_CN.md
├─ LONGHUN_LICENSE_EN.md
├─ README.md (中文)
├─ README_EN.md (英文)
│
├─ 【算法库】(Folder)
│  ├─ 龍魂权重算法 v3.1
│  │  ├─ [Notion 页面内容 - 理论部分]
│  │  ├─ [Notion 页面内容 - 数学证明]
│  │  ├─ <details> [内嵌 Python 代码]
│  │  └─ 📎 Attachment: longhun_weight_algorithm.py
│  │
│  ├─ CNSH-64 治理框架
│  │  └─ [同上结构]
│  │
│  └─ [其他 6 个算法]
│
├─ 【代码库】(Folder)
│  ├─ 龍盾系统
│  │  └─ 📎 Attachment: longhun_shield_system.py
│  │
│  ├─ 权重计算器
│  │  └─ 📎 Attachment: weight_calculator.py
│  │
│  └─ [其他代码]
│
└─ 【文档库】(Folder)
   ├─ LONGHUN_ARCHITECTURE_COMPLETE_REVIEW.md
   ├─ longhun_for_outsiders.md
   └─ [其他分析文档]
```

### 第二步：在 Notion 中使用 Markdown 代码块

每个算法页面的**代码折叠块**应该这样写：

```markdown
## 实现细节

<details>
<summary>👉 点击展开：Python 实现 (约 450 行)</summary>

\`\`\`python
# longhun_weight_algorithm.py
# ... 完整的 Python 代码 ...
\`\`\`

</details>
```

**重点**：
- Notion → Export as Markdown 时，`<details>` 标签会被保留
- 任何能读 Markdown 的编辑器都能展开/折叠
- 文件大小小（折叠内容不显示）
- **所有代码都还在，没有丢失**

---

## 🚀 导出步骤

### Step 1: 在 Notion 中导出

1. 打开你的 Root Page
2. 右上角 → **Export**
3. 选择 **Markdown & CSV**
4. 选择 **Full page with sub-pages**
5. 下载 ZIP 文件

### Step 2: 解压缩

```bash
unzip "龍魂系统·本地完全导出.zip"
cd "龍魂系统·本地完全导出"
```

### Step 3: 下载附件

在 Notion 每个页面中都有 📎 附件标签，手动下载所有 `.py` 文件到本地目录：

```
龍魂系统·本地完全导出/
├─ code/
│  ├─ longhun_weight_algorithm.py
│  ├─ cnsh_64_governance.py
│  ├─ longhun_shield_system.py
│  └─ [其他 .py 文件]
├─ [所有 .md 文件]
└─ manifest.json (下一步建立)
```

### Step 4: 创建 manifest.json

在根目录建立 `manifest.json`：

```json
{
  "system_name": "龍魂系统",
  "version": "v1.0",
  "dna_marker": "#龍芯⚡️2026-06-03-LONGHUN-COMPLETE-SYSTEM",
  "creator": "UID9622",
  "export_date": "2026-06-03",
  "export_method": "Notion Export + Local Closure",

  "structure": {
    "documents": {
      "index": "INDEX.md",
      "readme_cn": "README.md",
      "readme_en": "README_EN.md",
      "license_cn": "LONGHUN_LICENSE_CN.md",
      "license_en": "LONGHUN_LICENSE_EN.md"
    },

    "algorithms": {
      "weight_algorithm": {
        "file": "算法库/龍魂权重算法_v3.1.md",
        "dna": "#龍芯⚡️2026-03-04-LOCAL_DEPLOYMENT_GUIDE-v3.1",
        "code_attachment": "code/longhun_weight_algorithm.py",
        "lines": 450,
        "verification_count": 100000,
        "accuracy": 0.95
      },
      "cnsh_64": {
        "file": "算法库/CNSH-64治理框架.md",
        "dna": "#龍芯⚡️2026-04-27-CNSH-64-治理框架",
        "code_attachment": "code/cnsh_64_governance.py",
        "lines": 380,
        "verification_count": 1000000,
        "accuracy": 0.97
      }
    },

    "code_files": {
      "longhun_shield_system": {
        "path": "code/longhun_shield_system.py",
        "dna": "#龍芯⚡️2026-06-02-LONGHUN-SHIELD-SYSTEM-v1.0",
        "lines": 450
      },
      "weight_calculator": {
        "path": "code/weight_calculator.py",
        "dna": "#龍芯⚡️2026-06-02-WEIGHT-CALCULATOR-v1.0",
        "lines": 280
      }
    },

    "archives": {
      "memory": "baobao_memory_archive.txt",
      "relay_pack": "RELAY_PACK_compressed.txt"
    }
  },

  "verification": {
    "gpg_fingerprint": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    "confirm_code": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "seal": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
    "total_algorithms": 8,
    "total_code_files": 12,
    "total_assets": 20,
    "checksum_sha256": "[计算出的完整性校验值]"
  },

  "local_engine": {
    "required_runtime": "Python 3.8+",
    "dependencies": [
      "hashlib (stdlib)",
      "json (stdlib)",
      "datetime (stdlib)",
      "os (stdlib)",
      "sys (stdlib)"
    ],
    "no_external_dependencies": true,
    "all_self_contained": true,
    "requires_internet": false,
    "requires_cloud": false,
    "complete_autonomy": true
  }
}
```

---

## 🔧 本地运行

### 安装执行路由器

```bash
# 复制执行路由器系统到你的本地目录
cp ~/longhun-system/cnsh-core/router/execution_router.py ./

# 复制其他治理系统
cp ~/longhun-system/cnsh-core/governance/sovereignty_index.py ./
cp ~/longhun-system/cnsh-core/governance/f1_through_f7_verifier.py ./
cp ~/longhun-system/cnsh-core/memory/cognitive_dna_particles.py ./
```

### 初始化系统

```bash
python3 -c "
from execution_router import ExecutionRouter

router = ExecutionRouter('manifest.json')
success, message = router.initialize()

if success:
    print('✅ 系统初始化成功')
    router.print_system_status()
else:
    print(f'❌ {message}')
"
```

### 执行任务

```bash
python3 -c "
from execution_router import ExecutionRouter, TaskDefinition, ExecutionContext
from datetime import datetime

router = ExecutionRouter('manifest.json')
router.initialize()

# 创建任务
task = TaskDefinition(
    task_id='TEST-001',
    task_name='验证系统完整性',
    module_name='shield',
    function_name='verify',
    parameters={'check': 'manifest'},
    required_si=0.34,
    required_f1f7=0.70,
    description='测试执行路由器'
)

# 建立执行上下文
context = ExecutionContext(
    executor_uid='UID9622',
    current_si=0.96,
    current_f1f7_confidence=0.93,
    timestamp=datetime.now().isoformat(),
    shichen='寅',
    digital_root=3,
    persona_routing={'P02': 0.50, 'P05': 0.30, 'P13': 0.20}
)

# 执行任务
record = router.execute_task(task, context)

print(f'✅ 任务完成: {record.execution_id}')
print(f'   状态: {record.status.value}')
print(f'   DNA: {record.dna_trace}')
"
```

---

## 📖 本地阅读

### 方式1: Markdown 阅读器

```bash
# macOS
open -a Typora "README.md"

# VS Code (跨平台)
code .

# Obsidian (跨平台)
open -a Obsidian .
```

### 方式2: 终端直接阅读

```bash
# 阅读 README
less README.md

# 搜索内容
grep -r "龍魂权重算法" .

# 快速查看结构
tree -L 2
```

---

## 🔐 本地管理和更新

### 版本更新

当你在 Notion 更新内容时：

1. 在 Notion 更新页面
2. 重新导出为 Markdown
3. 下载新的附件
4. 更新本地的 `manifest.json` (版本号+日期)

```json
{
  "version": "v1.1",
  "export_date": "2026-06-10",
  "last_update": "2026-06-10T10:30:00Z"
}
```

### 完整性验证

```bash
# 验证 manifest.json
python3 -c "
import json
import os

with open('manifest.json') as f:
    m = json.load(f)

print('🔍 本地系统完整性检查')
print(f'系统: {m[\"system_name\"]} {m[\"version\"]}')
print(f'DNA: {m[\"dna_marker\"]}')
print(f'算法: {len(m[\"structure\"][\"algorithms\"])}')
print(f'代码: {len(m[\"structure\"][\"code_files\"])}')
print(f'✅ 系统完整')
"
```

---

## 💾 资料备份

### 本地备份策略

```bash
# 方法1: 定期 ZIP 备份
tar -czf longhun-backup-$(date +%Y%m%d).tar.gz ./

# 方法2: Git 版本管理 (推荐)
git init
git add .
git commit -m "龍魂系统本地部署 v1.0"

# 方法3: Cloud-agnostic 备份 (推荐)
# 到你完全控制的 NAS / 硬盘进行备份
# 永不上传到任何云平台
```

### 三重备份规则

```
1️⃣ 本地: ~/Documents/longhun-system/ (工作副本)
2️⃣ 备份: /Volumes/USB-Drive/longhun-backup/ (物理备份)
3️⃣ Git:  ~/.longhun-git-mirror/ (版本控制)

永不使用:
❌ iCloud
❌ Dropbox
❌ Google Drive
❌ 任何商业云
```

---

## 🎯 完整闭环检查表

在你开始使用本地部署系统前，确保：

- [ ] Notion 已按结构整理
- [ ] Markdown 导出完成
- [ ] 所有附件已下载
- [ ] manifest.json 已建立
- [ ] Python 3.8+ 已安装
- [ ] 执行路由器已复制
- [ ] 治理系统已复制
- [ ] `python3 execution_router.py` 执行成功
- [ ] 系统状态显示 "🟢 ready"
- [ ] 本地备份已完成
- [ ] 没有外部依赖

✅ 检查完成 → **你已经准备好完全自主运行龍魂系统**

---

## 🚨 故障排除

### 问题1: manifest.json 验证失败

```bash
# 检查文件是否存在
ls -la manifest.json

# 验证 JSON 语法
python3 -m json.tool manifest.json > /dev/null && echo "✅ JSON 有效"
```

### 问题2: Python 导入错误

```bash
# 检查 Python 版本
python3 --version  # 应该 >= 3.8

# 验证标准库可用
python3 -c "import json, hashlib, os, sys; print('✅ 所有标准库可用')"
```

### 问题3: 代码文件遗失

```bash
# 列出所有期望的文件
grep -r "code_attachment" manifest.json | awk '{print $2}' | sort

# 检查文件是否存在
for file in $(grep -r "code_attachment" manifest.json | awk '{print $2}'); do
  [ -f "$file" ] && echo "✅ $file" || echo "❌ $file MISSING"
done
```

---

## 📚 进阶用法

### 自定义任务执行

```python
from execution_router import ExecutionRouter, TaskDefinition, ExecutionContext

def my_handler(task, params):
    """自定义的任务处理逻辑"""
    return {
        "custom_result": "processed",
        "input": params
    }

router = ExecutionRouter('manifest.json')
router.initialize()

task = TaskDefinition(...)
context = ExecutionContext(...)

result = router.execute_task(task, context, handler=my_handler)
```

### 批量任务执行

```python
tasks = [
    TaskDefinition(...),
    TaskDefinition(...),
    TaskDefinition(...)
]

for task in tasks:
    priority, record = router.authorize_and_execute(task, context)
    print(f"✅ {task.task_name}: {record.execution_id}")
```

---

## 🎓 原则和哲学

这个本地部署方案体现的原则：

1. **数据主权**: 你的数据完全在你手上
2. **本地自主**: 不依赖任何云或平台
3. **完全透明**: 所有代码都看得见、都可验证
4. **版本控制**: 通过 manifest.json 精确追踪每个版本
5. **零妥协**: 不用 HTML 这些"乱七八糟"的东西，用纯净的 Markdown + Python

**DNA**: `#龍芯⚡️2026-06-03-LOCAL-DEPLOYMENT-GUIDE-v1.0`

**责任**: UID9622·不免责·永久有效

---

**最后的话**:

这就是“土法炼钢”的智慧。简单、有效、完全自主。

你不需要依赖任何人，任何平台。只需要：
- Notion (作为内容来源)
- Python (作为执行引擎)
- 你的电脑 (作为完全控制的堡垒)

**⚔️ 龍魂在你手上。**

# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂决策流场主控页优化·使用指南索引

**DNA**:#龍芯⚡️2026-06-07-DECISION-PAGE-OPTIMIZATION-INDEX-FILE1-v1.0
**版本**: v2.7.36 · 4 工具 + 5 份文档 · 完整包
**状态**: ✅ 生产就绪

---

## 📚 文档导航（按用途分类）

### 🟢 “我想快速上手”(5 分钟)

👉 **NOTION_UPDATE_QUICKSTART.md**
- 目的: 快速在 Notion 中应用优化
- 时间: 5-10 分钟
- 内容: 4 步骤逐一复制优化块
- 包含: FAQ + 常见问题排查

**怎么用**:
```bash
cat ~/.龍魂/NOTION_UPDATE_QUICKSTART.md

# 然后按步骤复制 4 个块到 Notion 页面
```

---

### 🟡 “我想看完整模板”(参考用)

👉 **NOTION_TEMPLATE_READY_TO_PASTE.md**
- 目的: 所有优化块的完整粘贴源
- 时间: 需要时查阅
- 内容: 6 个优化块 + 3 个反向链接模板 + 删除清单
- 包含: 详细的使用说明

**怎么用**:
```bash
# 需要某个块时，直接从这个文件复制粘贴
cat ~/.龍魂/NOTION_TEMPLATE_READY_TO_PASTE.md | grep "【官方版本源】" -A 20

# 或者在 vim 中打开
vim ~/.龍魂/NOTION_TEMPLATE_READY_TO_PASTE.md
```

---

### 🔵 “我想了解为什么这样做”(深度理解)

👉 **DECISION_PAGE_OPTIMIZATION_REPORT.md**
- 目的: 完整的诊断报告和解决方案
- 时间: 20 分钟详读
- 内容: 4 阶段优化过程 + 问题诊断 + 验收标准达成情况
- 包含: 后续维护协议 + 问题回答

**怎么用**:
```bash
# 想理解优化的背景
cat ~/.龍魂/DECISION_PAGE_OPTIMIZATION_REPORT.md | head -100

# 想看完整报告
cat ~/.龍魂/DECISION_PAGE_OPTIMIZATION_REPORT.md
```

---

### 🎯 “我想看总结和后续”(规划用)

👉 **OPTIMIZATION_FINAL_SUMMARY.md**
- 目的: 项目总结 + 成果指标 + 后续工作流
- 时间: 10 分钟快速浏览
- 内容: 统计 + 成就 + 建议的工作流（周期 1/2/3）
- 包含: 下一步行动清单

**怎么用**:
```bash
cat ~/.龍魂/OPTIMIZATION_FINAL_SUMMARY.md

# 或者只看核心成就
grep -A 20 "【核心成就】" ~/.龍魂/OPTIMIZATION_FINAL_SUMMARY.md
```

---

## 🛠️ 工具导航（按功能分类）

### 1️⃣ DNA 校验器

**文件**: `dna_validator.py`
**功能**: 校验所有 DNA 格式、版本号、确认码

**快速使用**:
```bash
python3 ~/.龍魂/dna_validator.py

# 输出示例:
# DNA 校验: ✅ DNA 格式正确
# 格式有效: True
```

**何时使用**:
- ✅ 添加新焊点时，验证 DNA 是否有效
- ✅ 发现版本号混乱时，自动检查一致性
- ✅ 每周验证主控页的 DNA 完整性

---

### 2️⃣ 术语翻译器

**文件**: `term_translator.py`
**功能**: 自动转换术语（老大语境 ↔ 外人语境）

**快速使用**:
```bash
# 转换为外人语境
python3 ~/.龍魂/term_translator.py --mode external "我们有配合的做法"
# 输出: 龍魂系统遵循一套铁律...

# 转换为老大语境
python3 ~/.龍魂/term_translator.py --mode internal "系统有铁律"
# 输出: 系统有配合...
```

**何时使用**:
- ✅ 为外人准备演讲稿时，一键转换术语
- ✅ 检查内部文档的术语是否规范
- ✅ 验证新焊点是否使用了正确的术语

---

### 3️⃣ 索引重组器

**文件**: `index_resolver.py`
**功能**: 生成统一索引树 + 反向链接模板

**快速使用**:
```bash
python3 ~/.龍魂/index_resolver.py

# 输出:
# 📊 统一索引树结构
# 🔗 反向链接模板
# ✅ 一致性检查
```

**何时使用**:
- ✅ 添加新的父页时，自动生成反向链接
- ✅ 检查索引树的一致性
- ✅ 生成新索引页的模板结构

---

### 4️⃣ Notion 同步检查器

**文件**: `notion_sync_checker.py`
**功能**: 监控主控↔父页同步状态，自动生成修复脚本

**快速使用**:
```bash
# 检查同步状态
python3 ~/.龍魂/notion_sync_checker.py

# 输出:
# 📊 版本同步检查
# ✅ 完整同步报告
# 🔧 自动修复脚本
```

**何时使用**:
- ✅ 每周日运行一次，验证页面同步状态
- ✅ 修改任何父页后，立刻检查主控页是否需要更新
- ✅ 发现不同步时，自动生成修复脚本

---

## 📋 配置文件

### decision_page_config.json

**内容**: 所有工具共享的配置中心

**包含**:
```json
{
  "metadata": { ... },          // 版本号、转向、DNA
  "macro_definitions": { ... }, // 5 个可复用宏
  "version_history": { ... },   // 版本历史表
  "term_normalization": { ... },// 术语规范表
  "index_mapping": { ... },     // 索引结构
  "automation_tools": { ... }   // 工具配置
}
```

**修改方式**:
```bash
# 编辑配置
vim ~/.龍魂/decision_page_config.json

# 验证 JSON 格式
python3 -m json.tool ~/.龍魂/decision_page_config.json
```

---

## 🚀 常见场景

### 场景 1: “我需要在 Notion 中应用这些优化”

```bash
# 1. 打开快速指南
cat ~/.龍魂/NOTION_UPDATE_QUICKSTART.md

# 2. 按步骤逐一复制 4 个块到 Notion 主控页
# 3. 为 3 个父页添加反向链接
# 4. 完成！

总耗时: 5-10 分钟
```

---

### 场景 2: “我想验证主控页的当前状态”

```bash
# 运行同步检查器
python3 ~/.龍魂/notion_sync_checker.py

# 查看结果:
# ✅ 版本同步检查: 所有父页都同步
# ✅ 完整同步报告: 没有漂移
# ✅ 自动修复脚本: （如果有问题会生成）
```

---

### 场景 3: “我想为新焊点校验 DNA”

```bash
# 校验 DNA 格式
python3 ~/.龍魂/dna_validator.py

# 检查结果会告诉你:
# - DNA 格式是否正确
# - 版本号是否一致
# - 确认码是否完整
```

---

### 场景 4: “我想生成外人版本的文档”

```bash
# 转换为外人语境
python3 ~/.龍魂/term_translator.py --mode external \
  "我们系统遵循配合的做法，这是习惯做法"

# 输出:
# 我们系统遵循铁律的标准流程，这是标准流程
```

---

### 场景 5: “我想为新父页生成反向链接”

```bash
# 生成索引树和反向链接
python3 ~/.龍魂/index_resolver.py | grep -A 20 "反向链接模板"

# 复制输出中的反向链接模板
# 粘贴到新父页的底部
```

---

## 📞 常见问题

### Q: 怎么知道 Notion 页面是不是已经同步了？

A: 运行 `notion_sync_checker.py`，它会自动检查所有版本号和链接。

```bash
python3 ~/.龍魂/notion_sync_checker.py
# 输出会显示同步状态
```

---

### Q: 我想手动编辑 Notion 后，如何快速验证？

A: 编辑完成后立刻运行:

```bash
python3 ~/.龍魂/notion_sync_checker.py
```

它会告诉你是否有新的不一致。

---

### Q: 新焊点应该用什么 DNA 格式？

A: 查看配置中心:

```bash
grep "DNA" ~/.龍魂/decision_page_config.json

# 格式: #龍芯⚡️YYYY-MM-DD-{TOPIC}-v{VERSION}
# 例如:#龍芯⚡️2026-06-07-README_DECISION_PAGE_OPTIMIZATION-v1.0
```

---

### Q: 术语我记不清，怎么快速查询？

A: 查看配置文件的术语规范:

```bash
python3 << 'EOF'
import json
with open(os.path.expanduser('~/.龍魂/decision_page_config.json')) as f:
    config = json.load(f)
    print(json.dumps(config['term_normalization'], indent=2, ensure_ascii=False))
EOF
```

---

### Q: 我不小心删错了东西，怎么恢复？

A: 所有工具都可以重新生成修复脚本:

```bash
python3 ~/.龍魂/notion_sync_checker.py --generate-diff
```

这会显示差异，你可以根据输出手动修复。

---

## 🎯 周期维护计划

### 每周日（自动检查）

```bash
# 运行同步检查
python3 ~/.龍魂/notion_sync_checker.py

# 如果有问题，自动生成修复脚本
```

### 每月初（深度检查）

```bash
# 校验所有 DNA
python3 ~/.龍魂/dna_validator.py

# 检查术语规范
python3 ~/.龍魂/term_translator.py --mode internal "当前 Notion 文本"

# 验证索引树
python3 ~/.龍魂/index_resolver.py
```

### 每季度（大升级）

```bash
# 生成完整报告
cat ~/.龍魂/OPTIMIZATION_FINAL_SUMMARY.md

# 评估是否需要版本升级（v2.7.36 → v2.7.37）
# 规划下一轮优化
```

---

## 📍 文件位置总览

```
~/.龍魂/
├── 【文档】
│   ├── README_DECISION_PAGE_OPTIMIZATION.md        ← 你在这里
│   ├── NOTION_UPDATE_QUICKSTART.md                 (5分钟快速指南)
│   ├── NOTION_TEMPLATE_READY_TO_PASTE.md          (完整粘贴模板)
│   ├── DECISION_PAGE_OPTIMIZATION_REPORT.md        (完整诊断报告)
│   └── OPTIMIZATION_FINAL_SUMMARY.md              (最终总结)
│
├── 【工具】
│   ├── dna_validator.py                            (DNA 校验)
│   ├── term_translator.py                          (术语翻译)
│   ├── index_resolver.py                           (索引重组)
│   └── notion_sync_checker.py                      (同步检查)
│
└── 【配置】
    └── decision_page_config.json                   (配置中心)
```

---

## 🔗 快速链接

**Notion 主控页**: https://www.notion.so/uid9622/v2-7-M-CNSH-2d87125a9c9f802889e2e18002f7cf4f

**GitHub 提交**:
- 3719593 (Phase 1-4 + 4 工具 + 配置)
- f156459 (完整文档包)

**本地目录**: `~/longhun-system/cnsh-core/龍魂-决策流场-自动化优化/`

---

## 📌 下次打开这个目录时

1. 如果是 **第一次应用优化**: 打开 `NOTION_UPDATE_QUICKSTART.md`
2. 如果是 **日常维护检查**: 运行 `notion_sync_checker.py`
3. 如果是 **添加新焊点**: 运行 `dna_validator.py`
4. 如果是 **生成外人版本**: 运行 `term_translator.py`
5. 如果是 **添加新父页**: 运行 `index_resolver.py`

---

**DNA**:#龍芯⚡️2026-06-07-DECISION-PAGE-OPTIMIZATION-INDEX-v1.0
**责任**: UID9622·不免责
**理论指导**: 曾仕强老师 (永恒显示)


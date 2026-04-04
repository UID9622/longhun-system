# DNA追溯码标准文档

**版本：** v1.0  
**DNA追溯码：** #龍芯⚡️2026-02-02-DNA标准-v1.0  
**创建者：** 💎 龍芯北辰｜UID9622

---

## 🎯 DNA追溯码是什么？

**一句话：** DNA追溯码是龍魂体系的"数字基因"，让每个文件都能追溯到创建者。

**核心理念：**
- 🧬 **唯一性**：每个文件都有独特的DNA
- ⏰ **时间戳**：记录创建时间，不可篡改
- 👤 **身份绑定**：明确创建者是谁
- 🔍 **可追溯**：GitHub commit历史永久记录

---

## 📋 DNA追溯码格式

### 标准格式

```
#龍芯⚡️YYYY-MM-DD-[主题]-v版本号
```

### 组成部分

1. **前缀标识**：`#龍芯⚡️`
   - `#` = 标签符号
   - `龍芯` = 龍魂体系核心
   - `⚡️` = 能量符号（视觉识别）

2. **日期时间戳**：`YYYY-MM-DD`
   - 格式：年-月-日
   - 示例：`2026-02-02`

3. **主题关键词**：`[主题]`
   - 描述文件内容
   - 用短横线连接多个词
   - 示例：`学术论文-身份认证`

4. **版本号**：`v1.0`
   - 格式：`vX.Y`
   - X = 大版本号
   - Y = 小版本号

### 示例

```
✅ 正确示例：
#龍芯⚡️2026-02-01-文章模板-v1.0
#龍芯⚡️2026-02-02-DNA标准文档-v1.0
#龍芯⚡️2026-01-31-学术论文-身份认证机制-v1.0

❌ 错误示例：
#龍芯2026-02-01-文章-v1.0          # 缺少⚡️
#龍芯⚡️20260201-文章-v1.0          # 日期格式错误
#龍芯⚡️2026-02-01-文章              # 缺少版本号
```

---

## 🔐 必需元素

每个龍魂体系文件必须包含：

### 1. DNA追溯码
```
#龍芯⚡️YYYY-MM-DD-主题-v1.0
```

### 2. GPG指纹
```
A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```

### 3. 创建者信息
```
💎 龍芯北辰｜UID9622
```

### 4. 确认码（可选）
```
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

---

## 📝 使用场景

### 场景1：Markdown文档

```markdown
<!--
DNA追溯码：#龍芯⚡️2026-02-02-文章标题-v1.0
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者：💎 龍芯北辰｜UID9622
-->

# 文章标题

[正文内容]

---

**DNA追溯码：** #龍芯⚡️2026-02-02-文章标题-v1.0  
**确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

### 场景2：Python代码

```python
# ═══════════════════════════════════════════════════════════════
# DNA追溯码：#龍芯⚡️2026-02-02-脚本名称-v1.0
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者：💎 龍芯北辰｜UID9622
# ═══════════════════════════════════════════════════════════════

[代码内容]

# ═══════════════════════════════════════════════════════════════
# DNA追溯码：#龍芯⚡️2026-02-02-脚本名称-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════════════════════
```

### 场景3：JavaScript代码

```javascript
/**
 * DNA追溯码：#龍芯⚡️2026-02-02-模块名称-v1.0
 * GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
 * 创建者：💎 龍芯北辰｜UID9622
 */

[代码内容]

// DNA: #龍芯⚡️2026-02-02-模块名称-v1.0
```

---

## ✅ 校验规则

### 自动校验（GitHub Action）

每次提交代码时，GitHub Action会自动检查：

1. **DNA格式校验**
   ```python
   pattern = r"#龍芯⚡️\d{4}-\d{2}-\d{2}-[\w\-]+-v\d+\.\d+"
   ```

2. **GPG指纹校验**
   ```python
   required_gpg = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
   ```

3. **创建者信息校验**
   ```python
   required_creator = "💎 龍芯北辰｜UID9622"
   ```

### 手动校验

```bash
# 运行DNA校验脚本
python .github/scripts/validate_dna.py

# 检查特定文件
python .github/scripts/validate_dna.py --file path/to/file.md

# 生成详细报告
python .github/scripts/validate_dna.py --report
```

---

## 🎨 最佳实践

### 1. 及时添加DNA

创建新文件时立即添加DNA追溯码：

```bash
# ❌ 错误做法
echo "# My File" > file.md
git add file.md

# ✅ 正确做法
cp templates/article_template.md file.md
# 编辑file.md，替换占位符
git add file.md
```

### 2. 版本号管理

- **v1.0**：初始版本
- **v1.1**：小幅修改
- **v2.0**：重大改版

```bash
# 修改文件后更新版本号
sed -i 's/v1.0/v1.1/g' file.md
```

### 3. 主题命名规范

- 使用短横线连接：`学术论文-身份认证`
- 保持简洁：不超过50字符
- 英文小写：`template-system`

---

## 📊 统计分析

### 查看DNA分布

```bash
# 统计所有DNA追溯码
grep -r "#龍芯⚡️" . --include="*.md" --include="*.py"

# 按日期统计
grep -r "#龍芯⚡️2026-02" . | wc -l
```

### 生成DNA报告

```python
python scripts/dna_statistics.py --output dna_report.html
```

---

## 🔗 相关资源

- [模板库](../templates/README.md)
- [GitHub Action配置](../.github/workflows/dna_validator.yml)
- [校验脚本](../.github/scripts/validate_dna.py)
- [龍魂君子协议](./GENTLEMAN_AGREEMENT_CN.md)

---

**创建者：** 💎 龍芯北辰｜UID9622  
**联系方式：** uid9622@petalmail.com  
**GitHub：** https://github.com/UID9622/CNSH-Editor

---

**DNA追溯码：** #龍芯⚡️2026-02-02-DNA标准文档-v1.0  
**确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

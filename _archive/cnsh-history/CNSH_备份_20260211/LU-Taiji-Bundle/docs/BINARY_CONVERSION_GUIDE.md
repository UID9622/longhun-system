# 二进制文件转换指南

**DNA:** #ZHUGEXIN⚡️2026-01-27-CONVERT-GUIDE-v1.0
**脚本版本:** v1.0

---

## 📖 概述

本脚本用于将苹果/Windows平台的二进制文件（.docx、.pdf、.doc、.rtf）转换为纯文本格式，便于AI助手读取和处理。

---

## 🚀 快速开始

### 安装依赖

```bash
# macOS (Homebrew)
brew install unzip python3

# 安装 Python PDF 解析库
pip3 install PyPDF2

# 可选：安装更强大的转换工具
brew install pandoc
pip3 install pdfplumber
```

### 基本使用

#### 转换单个文件

```bash
cd "/Users/zuimeidedeyihan/Desktop/打包待命/CNSH 军人的编辑器/LU-Taiji-Bundle"

# 转换 .docx 文件
bash scripts/convert_binary_to_text.sh -f ../CNSH_Language_Documentation.docx

# 转换 .pdf 文件
bash scripts/convert_binary_to_text.sh -f ../UID9622/未命名文件夹/提取文字_体系.pdf
```

#### 批量转换目录

```bash
# 转换整个目录
bash scripts/convert_binary_to_text.sh -d ../UID9622/未命名文件夹
```

#### 快速转换（推荐）

```bash
# 一键转换所有大文件
bash scripts/quick_convert.sh
```

---

## 📋 命令选项

| 选项 | 说明 | 示例 |
|------|------|------|
| `-h, --help` | 显示帮助信息 | `bash scripts/convert_binary_to_text.sh -h` |
| `-c, --check` | 检查依赖 | `bash scripts/convert_binary_to_text.sh -c` |
| `-f, --file FILE` | 转换单个文件 | `-f document.docx` |
| `-d, --dir DIR` | 批量转换目录 | `-d /path/to/docs` |
| `-o, --output DIR` | 指定输出目录 | `-o my_output/` |

---

## 📦 支持的文件格式

| 格式 | 扩展名 | 依赖 | 说明 |
|------|--------|------|------|
| Word 文档 | .docx | unzip | 推荐，自动提取XML文本 |
| PDF 文档 | .pdf | PyPDF2/pdfplumber | 推荐，支持页面提取 |
| 旧版 Word | .doc | pandoc | 可选，功能更强大 |
| 富文本 | .rtf | pandoc | 可选，格式转换 |

---

## 🔧 工作原理

### .docx 转换流程

```
.docx 文件
    ↓
解压 ZIP 包
    ↓
提取 word/document.xml
    ↓
清理 XML 标签
    ↓
转换纯文本 (.txt)
```

### .pdf 转换流程

```
.pdf 文件
    ↓
使用 PyPDF2/pdfplumber 解析
    ↓
逐页提取文本
    ↓
合并为纯文本 (.txt)
```

---

## 📂 输出结构

转换后的文件保存在 `LU-Taiji-Bundle/text_content/` 目录：

```
text_content/
├── CNSH_Language_Documentation.txt        # .docx 转换结果
├── 提取文字_体系.txt                      # .pdf 转换结果
├── 汇旺事件真相档案_基于公开数据的客观分析.txt
├── FireShot_Capture_001.txt
└── ...                                    # 其他转换结果
```

---

## 🎯 实际使用场景

### 场景1：转换 CNSH 语言文档

```bash
# 转换 2.53 MB 的 .docx 文件
bash scripts/convert_binary_to_text.sh \
  -f "/Users/zuimeidedeyihan/Desktop/打包待命/CNSH 军人的编辑器/CNSH_Language_Documentation.docx"

# 查看结果
cat LU-Taiji-Bundle/text_content/CNSH_Language_Documentation.txt
```

### 场景2：转换大 PDF 文档

```bash
# 转换 57.47 MB 的 PDF 文件
bash scripts/convert_binary_to_text.sh \
  -f "/Users/zuimeidedeyihan/Desktop/打包待命/CNSH 军人的编辑器/UID9622/未命名文件夹/提取文字_体系.pdf"

# 查看结果
cat LU-Taiji-Bundle/text_content/提取文字_体系.txt
```

### 场景3：批量转换 UID9622 目录

```bash
# 批量转换所有 PDF/DOCX 文件
bash scripts/convert_binary_to_text.sh \
  -d "/Users/zuimeidedeyihan/Desktop/打包待命/CNSH 军人的编辑器/UID9622/未命名文件夹"

# 查看所有结果
ls -lh LU-Taiji-Bundle/text_content/
```

### 场景4：快速转换（一键搞定）

```bash
# 一键转换所有已知大文件
bash scripts/quick_convert.sh
```

---

## ⚠️ 注意事项

1. **编码问题**：脚本默认使用 UTF-8 编码输出
2. **文件权限**：确保有读取源文件和写入输出目录的权限
3. **大文件处理**：57.47 MB 的 PDF 文件可能需要较长时间
4. **格式丢失**：转换后会丢失格式（加粗、表格等），只保留纯文本

---

## 🔍 故障排查

### 问题1：缺少 unzip 命令

**错误：** `缺少依赖: unzip`

**解决：**
```bash
brew install unzip
```

### 问题2：缺少 PDF 解析库

**错误：** `无法转换 .pdf 文件: 缺少 PDF 解析库`

**解决：**
```bash
pip3 install PyPDF2
# 或
pip3 install pdfplumber  # 更好的文本提取
```

### 问题3：.doc 文件无法转换

**错误：** `无法转换 .doc 文件: 需要 pandoc`

**解决：**
```bash
brew install pandoc
```

### 问题4：中文乱码

**解决：** 确保输出文件使用 UTF-8 编码

---

## 📊 性能参考

| 文件大小 | 格式 | 预计时间 | 输出大小 |
|---------|------|---------|---------|
| 2.53 MB | .docx | 1-2秒 | 500 KB - 1 MB |
| 57.47 MB | .pdf | 10-30秒 | 5-10 MB |

---

## 🎨 高级用法

### 自定义输出目录

```bash
bash scripts/convert_binary_to_text.sh \
  -f document.docx \
  -o /path/to/custom/output/
```

### 转换后立即查看

```bash
# 转换并立即查看
bash scripts/convert_binary_to_text.sh -f doc.pdf && \
  cat LU-Taiji-Bundle/text_content/doc.txt
```

---

## 📝 技术细节

### .docx 转换原理

.docx 文件本质是 ZIP 压缩包，包含 XML 文件：
- `word/document.xml` - 主文档内容
- `word/styles.xml` - 样式定义
- `word/settings.xml` - 设置

脚本提取 `word/document.xml` 并使用 `sed` 清理标签。

### .pdf 转换原理

使用 Python 库解析 PDF 结构：
- **PyPDF2** - 基础提取，速度快
- **pdfplumber** - 更精确的提取，保留布局

---

## 🔗 相关资源

- [PyPDF2 文档](https://pypdf2.readthedocs.io/)
- [pdfplumber 文档](https://github.com/jsvine/pdfplumber)
- [pandoc 文档](https://pandoc.org/)

---

## ✅ 总结

使用本脚本可以轻松将二进制文档转换为纯文本，便于：

1. AI 助手读取和分析
2. 代码审查和文档处理
3. 内容搜索和索引
4. 版本控制和对比

**推荐流程：**
```bash
# 1. 检查依赖
bash scripts/convert_binary_to_text.sh -c

# 2. 快速转换
bash scripts/quick_convert.sh

# 3. 查看结果
ls -lh LU-Taiji-Bundle/text_content/
```

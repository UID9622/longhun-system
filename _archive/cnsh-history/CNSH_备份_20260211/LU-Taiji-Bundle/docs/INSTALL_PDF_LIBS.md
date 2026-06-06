<!--
  龍魂·六层来源链 / LongHun Six-Layer Source Chain
  1 道统层 Dao           : 曾仕强老师
  2 精神层 Spirit        : Steve Jobs
  3 设备层 Device        : Apple
  4 技术层 Technology    : Open Source
  5 系统层 System        : UID9622
  6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
  DNA追溯码: #龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-v2.0
  铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
  文件: INSTALL_PDF_LIBS.md | 标记时间: 2026-06-03T07:46:00+0800
-->
# PDF 解析库安装指南

## 📦 需要安装的库

1. **PyPDF2** - 基础 PDF 解析
2. **pdfplumber** - 更精确的文本提取

---

## 🚀 安装方法

### 方法1：使用安装脚本（推荐）

```bash
cd "/Users/zuimeidedeyihan/Desktop/打包待命/CNSH 军人的编辑器/LU-Taiji-Bundle"
bash scripts/install_pdf_libs.sh
```

### 方法2：手动安装

```bash
# 安装 PyPDF2
python3 -m pip install --user PyPDF2

# 安装 pdfplumber（推荐）
python3 -m pip install --user pdfplumber
```

### 方法3：使用 pip3

```bash
pip3 install PyPDF2 pdfplumber
```

---

## ✅ 验证安装

```bash
# 检查 PyPDF2
python3 -c "import PyPDF2; print('✓ PyPDF2 已安装')"

# 检查 pdfplumber
python3 -c "import pdfplumber; print('✓ pdfplumber 已安装')"
```

---

## 🔄 安装完成后

重新运行转换脚本：

```bash
bash scripts/quick_convert.sh
```

---

## ⚠️ 注意事项

如果遇到权限问题，可以使用 `sudo`：

```bash
sudo python3 -m pip install PyPDF2 pdfplumber
```

但一般情况下使用 `--user` 参数就足够了。

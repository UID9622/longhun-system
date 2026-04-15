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

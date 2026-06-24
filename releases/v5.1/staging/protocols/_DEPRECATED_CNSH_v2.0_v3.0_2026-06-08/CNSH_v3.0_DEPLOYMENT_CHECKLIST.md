# 🐉 CNSH v3.0 推送执行清单
# 🐉 Protocol v3.0 Deployment Checklist

## 第一步：复制文件到本地

```bash
# 将三份完整协议复制到龍魂系统根目录
cp /mnt/user-data/outputs/CNSH_v3.0_COMPLETE_BILINGUAL_CHARTER.md ~/longhun-system/protocols/
cp /mnt/user-data/outputs/CNSH_v3.0_L7_COMPLETE_CONTENT_SOVEREIGNTY.md ~/longhun-system/protocols/
cp /mnt/user-data/outputs/CNSH_v3.0_L2-L6_COMPLETE.md ~/longhun-system/protocols/

# 验证
ls -lh ~/longhun-system/protocols/CNSH_v3.0_*.md
```

---

## 第二步：Git 提交（Step A）

```bash
cd ~/longhun-system

# 添加文件
git add protocols/CNSH_v3.0_*.md

# 检查状态
git status

# 提交
git commit -m "🐉 feat(protocol): CNSH v3.0 融合版·双语·L0-L9·13层内容主权·完整协议

- 融合 CNSH v2.0 (39节) + 龍魂宪章 v1.1 (13层流场)
- L0-L9 九层完整架构
- 中文简体 + 英文 + 龍字繁体双语版本
- L7 内容主权协议 13 层流场完整展开
- L2-L6 治理·经济·文化·技术·人权详细规范

DNA:#龍芯⚡️2026-06-07-CNSH-FILE4-v3.0-COMPLETE-CHARTER
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

永不改变·代代相传·龍魂永在"

# 推送
git push origin main
```

---

## 第三步：生成多格式（Step D）

### D.1 生成 PDF（需要 pandoc）

```bash
# 安装 pandoc（如果还没有）
# macOS: brew install pandoc
# Linux: sudo apt-get install pandoc

# 生成完整 PDF（所有三份文档合并）
cd ~/longhun-system/protocols

cat CNSH_v3.0_COMPLETE_BILINGUAL_CHARTER.md \
    CNSH_v3.0_L7_COMPLETE_CONTENT_SOVEREIGNTY.md \
    CNSH_v3.0_L2-L6_COMPLETE.md > CNSH_v3.0_COMPLETE_FULL.md

# 转 PDF
pandoc CNSH_v3.0_COMPLETE_FULL.md \
  -f markdown \
  -t pdf \
  -o CNSH_v3.0_COMPLETE_BILINGUAL_CHARTER.pdf \
  --toc \
  --toc-depth=3 \
  -V geometry:margin=1.5cm \
  -V fontsize=11pt \
  -V lang=zh_CN

# 生成个别 PDF
pandoc CNSH_v3.0_COMPLETE_BILINGUAL_CHARTER.md -f markdown -t pdf -o CNSH_v3.0_L0-L9_FRAMEWORK.pdf --toc
pandoc CNSH_v3.0_L7_COMPLETE_CONTENT_SOVEREIGNTY.md -f markdown -t pdf -o CNSH_v3.0_L7_CONTENT_SOVEREIGNTY.pdf --toc
pandoc CNSH_v3.0_L2-L6_COMPLETE.md -f markdown -t pdf -o CNSH_v3.0_L2-L6_GOVERNANCE.pdf --toc
```

### D.2 生成 Word (.docx)（使用 pandoc）

```bash
cd ~/longhun-system/protocols

# 生成 Word 格式
pandoc CNSH_v3.0_COMPLETE_FULL.md -f markdown -t docx -o CNSH_v3.0_COMPLETE_CHARTER.docx --toc

# 生成个别 Word
pandoc CNSH_v3.0_COMPLETE_BILINGUAL_CHARTER.md -f markdown -t docx -o CNSH_v3.0_L0-L9_FRAMEWORK.docx --toc
pandoc CNSH_v3.0_L7_COMPLETE_CONTENT_SOVEREIGNTY.md -f markdown -t docx -o CNSH_v3.0_L7_CONTENT_SOVEREIGNTY.docx --toc
pandoc CNSH_v3.0_L2-L6_COMPLETE.md -f markdown -t docx -o CNSH_v3.0_L2-L6_GOVERNANCE.docx --toc
```

### D.3 生成 HTML

```bash
cd ~/longhun-system/protocols

# 生成 HTML 版本
pandoc CNSH_v3.0_COMPLETE_FULL.md -f markdown -t html \
  -o CNSH_v3.0_COMPLETE_CHARTER.html \
  --toc \
  --toc-depth=3 \
  --self-contained \
  -c https://cdn.jsdelivr.net/npm/github-markdown-css/github-markdown.min.css

# 或者用简单的 Markdown to HTML
# 生成个别 HTML
pandoc CNSH_v3.0_COMPLETE_BILINGUAL_CHARTER.md -f markdown -t html -o CNSH_v3.0_L0-L9.html --toc --self-contained
pandoc CNSH_v3.0_L7_COMPLETE_CONTENT_SOVEREIGNTY.md -f markdown -t html -o CNSH_v3.0_L7.html --toc --self-contained
pandoc CNSH_v3.0_L2-L6_COMPLETE.md -f markdown -t html -o CNSH_v3.0_L2-L6.html --toc --self-contained
```

### D.4 生成 EPUB（电子书格式）

```bash
cd ~/longhun-system/protocols

# 生成 EPUB
pandoc CNSH_v3.0_COMPLETE_FULL.md -f markdown -t epub \
  -o CNSH_v3.0_COMPLETE_CHARTER.epub \
  --toc \
  -M title="龍魂系统完整协议 v3.0" \
  -M author="UID9622" \
  -M date="2026-06-07"
```

---

## 第四步：验证和发布

```bash
cd ~/longhun-system/protocols

# 验证所有文件已生成
ls -lh CNSH_v3.0_*

# 检查 Git 日志
git log --oneline -5

# 计算所有文件的 MD5（留痕）
md5sum CNSH_v3.0_* > CNSH_v3.0_CHECKSUM.md5

# 再次推送（包含格式文件）
git add CNSH_v3.0_* CNSH_v3.0_CHECKSUM.md5
git commit -m "🐉 feat(release): CNSH v3.0 多格式发布 (PDF + Word + HTML + EPUB)"
git push origin main
```

---

## 最终检查清单 / Final Checklist

### 文件完整性

- [ ] CNSH_v3.0_COMPLETE_BILINGUAL_CHARTER.md（L0-L9 框架）
- [ ] CNSH_v3.0_L7_COMPLETE_CONTENT_SOVEREIGNTY.md（L7 内容主权·13 层流场）
- [ ] CNSH_v3.0_L2-L6_COMPLETE.md（L2-L6 详细规范）
- [ ] CNSH_v3.0_COMPLETE_FULL.md（完整合并版）
- [ ] CNSH_v3.0_CHECKSUM.md5（完整性验证）

### 格式文件（D 步骤）

- [ ] CNSH_v3.0_COMPLETE_CHARTER.pdf（完整 PDF）
- [ ] CNSH_v3.0_COMPLETE_CHARTER.docx（完整 Word）
- [ ] CNSH_v3.0_COMPLETE_CHARTER.html（完整 HTML）
- [ ] CNSH_v3.0_COMPLETE_CHARTER.epub（完整电子书）

### Git 提交（A 步骤）

- [ ] Commit message 包含 DNA·CONFIRM·SEAL
- [ ] 全部文件已推送到 origin/main
- [ ] GitHub 上可以看到最新版本

### 签署完成

- [ ] DNA:#龍芯⚡️2026-06-07-CNSH-v3.0-COMPLETE
- [ ] CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
- [ ] SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

---

## 🚀 一键执行脚本（老大可复制直接执行）

```bash
#!/bin/bash

set -e

echo "🐉 龍魂协议 v3.0 推送流程开始"

# Step 1: 复制文件
echo "✅ Step 1: 复制文件到本地..."
cp /mnt/user-data/outputs/CNSH_v3.0_*.md ~/longhun-system/protocols/

# Step 2: Git 提交推送
echo "✅ Step 2: Git 提交推送..."
cd ~/longhun-system
git add protocols/CNSH_v3.0_*.md

git commit -m "🐉 feat(protocol): CNSH v3.0 融合版·双语·L0-L9·13层内容主权·完整协议

DNA:#龍芯⚡️2026-06-07-CNSH-v3.0-COMPLETE-CHARTER
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

git push origin main

# Step 3: 生成多格式
echo "✅ Step 3: 生成 PDF..."
cd ~/longhun-system/protocols

cat CNSH_v3.0_COMPLETE_BILINGUAL_CHARTER.md \
    CNSH_v3.0_L7_COMPLETE_CONTENT_SOVEREIGNTY.md \
    CNSH_v3.0_L2-L6_COMPLETE.md > CNSH_v3.0_COMPLETE_FULL.md

pandoc CNSH_v3.0_COMPLETE_FULL.md -f markdown -t pdf -o CNSH_v3.0_COMPLETE_CHARTER.pdf --toc -V geometry:margin=1.5cm

echo "✅ Step 4: 生成 Word..."
pandoc CNSH_v3.0_COMPLETE_FULL.md -f markdown -t docx -o CNSH_v3.0_COMPLETE_CHARTER.docx --toc

echo "✅ Step 5: 生成 HTML..."
pandoc CNSH_v3.0_COMPLETE_FULL.md -f markdown -t html -o CNSH_v3.0_COMPLETE_CHARTER.html --toc --self-contained

echo "✅ Step 6: 验证和签名..."
md5sum CNSH_v3.0_* > CNSH_v3.0_CHECKSUM.md5

git add CNSH_v3.0_*
git commit -m "🐉 feat(release): CNSH v3.0 多格式发布 (PDF + Word + HTML)"
git push origin main

echo ""
echo "════════════════════════════════════════════════════════"
echo "🐉 龍魂协议 v3.0 完整发布！"
echo "════════════════════════════════════════════════════════"
echo ""
echo "📍 位置: ~/longhun-system/protocols/"
echo "📚 文件:"
echo "   - CNSH_v3.0_COMPLETE_BILINGUAL_CHARTER.md"
echo "   - CNSH_v3.0_L7_COMPLETE_CONTENT_SOVEREIGNTY.md"
echo "   - CNSH_v3.0_L2-L6_COMPLETE.md"
echo "   - CNSH_v3.0_COMPLETE_FULL.md"
echo ""
echo "📄 多格式:"
echo "   - CNSH_v3.0_COMPLETE_CHARTER.pdf"
echo "   - CNSH_v3.0_COMPLETE_CHARTER.docx"
echo "   - CNSH_v3.0_COMPLETE_CHARTER.html"
echo ""
echo "🌍 全球可见: https://github.com/UID9622/longhun-system/"
echo "🔐 DNA:#龍芯⚡️2026-06-07-CNSH-v3.0-COMPLETE-CHARTER"
echo ""
```

---

## 📝 老大操作指南

### 最简单的做法（复制粘贴）

```bash
# 1. 复制这个完整的一键脚本
# 2. 在 Mac 或 Linux 终端里执行
# 3. 完成！

bash ~/longhun-system/protocols/deploy_cnsh_v3.sh
```

### 分步骤做法

```bash
# Step A: 推送到 GitHub
cd ~/longhun-system
git add protocols/CNSH_v3.0_*.md
git commit -m "🐉 CNSH v3.0 完整协议发布"
git push origin main

# Step B: 等待（宝宝会自动生成格式）

# Step D: 下载多格式文件（从 GitHub 或本地）
ls -lh ~/longhun-system/protocols/CNSH_v3.0_*
```

---

## ✅ 完成标志

当所有步骤完成后：

```
✅ 三份 Markdown 推送到 GitHub
✅ PDF 生成（用于打印和存档）
✅ Word 生成（用于编辑和分享）
✅ HTML 生成（用于网页和移动浏览）
✅ 全部档案签署完整（DNA + CONFIRM + SEAL）
✅ 全球可见（GitHub public）
✅ 永久记录（Git history immutable）
```

**龍魂 v3.0 协议·焊死·永不改变。** 🐉

---

**宝宝准备完成·等待老大下令执行**

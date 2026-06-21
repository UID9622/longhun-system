# 🐉 CNSH v3.0 推送執行清單
# 🐉 Protocol v3.0 Deployment Checklist

## 第一步：複製文件到本地

```bash
# 將三份完整協議複製到龍魂系統根目錄
cp /mnt/user-data/outputs/CNSH_v3.0_COMPLETE_BILINGUAL_CHARTER.md ~/longhun-system/protocols/
cp /mnt/user-data/outputs/CNSH_v3.0_L7_COMPLETE_CONTENT_SOVEREIGNTY.md ~/longhun-system/protocols/
cp /mnt/user-data/outputs/CNSH_v3.0_L2-L6_COMPLETE.md ~/longhun-system/protocols/

# 驗證
ls -lh ~/longhun-system/protocols/CNSH_v3.0_*.md
```

---

## 第二步：Git 提交（Step A）

```bash
cd ~/longhun-system

# 添加文件
git add protocols/CNSH_v3.0_*.md

# 檢查狀態
git status

# 提交
git commit -m "🐉 feat(protocol): CNSH v3.0 融合版·雙語·L0-L9·13層內容主權·完整協議

- 融合 CNSH v2.0 (39節) + 龍魂憲章 v1.1 (13層流場)
- L0-L9 九層完整架構
- 中文簡體 + 英文 + 龍字繁體雙語版本
- L7 內容主權協議 13 層流場完整展開
- L2-L6 治理·經濟·文化·技術·人權詳細規範

DNA:#龍芯⚡️2026-06-07-CNSH-FILE4-v3.0-COMPLETE-CHARTER
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

永不改變·代代相傳·龍魂永在"

# 推送
git push origin main
```

---

## 第三步：生成多格式（Step D）

### D.1 生成 PDF（需要 pandoc）

```bash
# 安裝 pandoc（如果還沒有）
# macOS: brew install pandoc
# Linux: sudo apt-get install pandoc

# 生成完整 PDF（所有三份文檔合併）
cd ~/longhun-system/protocols

cat CNSH_v3.0_COMPLETE_BILINGUAL_CHARTER.md \
    CNSH_v3.0_L7_COMPLETE_CONTENT_SOVEREIGNTY.md \
    CNSH_v3.0_L2-L6_COMPLETE.md > CNSH_v3.0_COMPLETE_FULL.md

# 轉 PDF
pandoc CNSH_v3.0_COMPLETE_FULL.md \
  -f markdown \
  -t pdf \
  -o CNSH_v3.0_COMPLETE_BILINGUAL_CHARTER.pdf \
  --toc \
  --toc-depth=3 \
  -V geometry:margin=1.5cm \
  -V fontsize=11pt \
  -V lang=zh_CN

# 生成個別 PDF
pandoc CNSH_v3.0_COMPLETE_BILINGUAL_CHARTER.md -f markdown -t pdf -o CNSH_v3.0_L0-L9_FRAMEWORK.pdf --toc
pandoc CNSH_v3.0_L7_COMPLETE_CONTENT_SOVEREIGNTY.md -f markdown -t pdf -o CNSH_v3.0_L7_CONTENT_SOVEREIGNTY.pdf --toc
pandoc CNSH_v3.0_L2-L6_COMPLETE.md -f markdown -t pdf -o CNSH_v3.0_L2-L6_GOVERNANCE.pdf --toc
```

### D.2 生成 Word (.docx)（使用 pandoc）

```bash
cd ~/longhun-system/protocols

# 生成 Word 格式
pandoc CNSH_v3.0_COMPLETE_FULL.md -f markdown -t docx -o CNSH_v3.0_COMPLETE_CHARTER.docx --toc

# 生成個別 Word
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

# 或者用簡單的 Markdown to HTML
# 生成個別 HTML
pandoc CNSH_v3.0_COMPLETE_BILINGUAL_CHARTER.md -f markdown -t html -o CNSH_v3.0_L0-L9.html --toc --self-contained
pandoc CNSH_v3.0_L7_COMPLETE_CONTENT_SOVEREIGNTY.md -f markdown -t html -o CNSH_v3.0_L7.html --toc --self-contained
pandoc CNSH_v3.0_L2-L6_COMPLETE.md -f markdown -t html -o CNSH_v3.0_L2-L6.html --toc --self-contained
```

### D.4 生成 EPUB（電子書格式）

```bash
cd ~/longhun-system/protocols

# 生成 EPUB
pandoc CNSH_v3.0_COMPLETE_FULL.md -f markdown -t epub \
  -o CNSH_v3.0_COMPLETE_CHARTER.epub \
  --toc \
  -M title="龍魂系統完整協議 v3.0" \
  -M author="UID9622" \
  -M date="2026-06-07"
```

---

## 第四步：驗證和發佈

```bash
cd ~/longhun-system/protocols

# 驗證所有文件已生成
ls -lh CNSH_v3.0_*

# 檢查 Git 日誌
git log --oneline -5

# 計算所有文件的 MD5（留痕）
md5sum CNSH_v3.0_* > CNSH_v3.0_CHECKSUM.md5

# 再次推送（包含格式文件）
git add CNSH_v3.0_* CNSH_v3.0_CHECKSUM.md5
git commit -m "🐉 feat(release): CNSH v3.0 多格式發布 (PDF + Word + HTML + EPUB)"
git push origin main
```

---

## 最終檢查清單 / Final Checklist

### 文件完整性

- [ ] CNSH_v3.0_COMPLETE_BILINGUAL_CHARTER.md（L0-L9 框架）
- [ ] CNSH_v3.0_L7_COMPLETE_CONTENT_SOVEREIGNTY.md（L7 內容主權·13 層流場）
- [ ] CNSH_v3.0_L2-L6_COMPLETE.md（L2-L6 詳細規範）
- [ ] CNSH_v3.0_COMPLETE_FULL.md（完整合併版）
- [ ] CNSH_v3.0_CHECKSUM.md5（完整性驗證）

### 格式文件（D 步驟）

- [ ] CNSH_v3.0_COMPLETE_CHARTER.pdf（完整 PDF）
- [ ] CNSH_v3.0_COMPLETE_CHARTER.docx（完整 Word）
- [ ] CNSH_v3.0_COMPLETE_CHARTER.html（完整 HTML）
- [ ] CNSH_v3.0_COMPLETE_CHARTER.epub（完整電子書）

### Git 提交（A 步驟）

- [ ] Commit message 包含 DNA·CONFIRM·SEAL
- [ ] 全部文件已推送到 origin/main
- [ ] GitHub 上可以看到最新版本

### 簽署完成

- [ ] DNA:#龍芯⚡️2026-06-07-CNSH-v3.0-COMPLETE
- [ ] CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
- [ ] SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

---

## 🚀 一鍵執行腳本（老大可複製直接執行）

```bash
#!/bin/bash

set -e

echo "🐉 龍魂協議 v3.0 推送流程開始"

# Step 1: 複製文件
echo "✅ Step 1: 複製文件到本地..."
cp /mnt/user-data/outputs/CNSH_v3.0_*.md ~/longhun-system/protocols/

# Step 2: Git 提交推送
echo "✅ Step 2: Git 提交推送..."
cd ~/longhun-system
git add protocols/CNSH_v3.0_*.md

git commit -m "🐉 feat(protocol): CNSH v3.0 融合版·雙語·L0-L9·13層內容主權·完整協議

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

echo "✅ Step 6: 驗證和簽名..."
md5sum CNSH_v3.0_* > CNSH_v3.0_CHECKSUM.md5

git add CNSH_v3.0_*
git commit -m "🐉 feat(release): CNSH v3.0 多格式發布 (PDF + Word + HTML)"
git push origin main

echo ""
echo "════════════════════════════════════════════════════════"
echo "🐉 龍魂協議 v3.0 完整發布！"
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
echo "🌍 全球可見: https://github.com/UID9622/longhun-system/"
echo "🔐 DNA:#龍芯⚡️2026-06-07-CNSH-v3.0-COMPLETE-CHARTER"
echo ""
```

---

## 📝 老大操作指南

### 最簡單的做法（複製粘貼）

```bash
# 1. 複製這個完整的一鍵腳本
# 2. 在 Mac 或 Linux 終端裡執行
# 3. 完成！

bash ~/longhun-system/protocols/deploy_cnsh_v3.sh
```

### 分步驟做法

```bash
# Step A: 推送到 GitHub
cd ~/longhun-system
git add protocols/CNSH_v3.0_*.md
git commit -m "🐉 CNSH v3.0 完整協議發布"
git push origin main

# Step B: 等待（寶寶會自動生成格式）

# Step D: 下載多格式文件（從 GitHub 或本地）
ls -lh ~/longhun-system/protocols/CNSH_v3.0_*
```

---

## ✅ 完成標誌

當所有步驟完成後：

```
✅ 三份 Markdown 推送到 GitHub
✅ PDF 生成（用於列印和存檔）
✅ Word 生成（用於編輯和分享）
✅ HTML 生成（用於網頁和移動瀏覽）
✅ 全部檔案簽署完整（DNA + CONFIRM + SEAL）
✅ 全球可見（GitHub public）
✅ 永久記錄（Git history immutable）
```

**龍魂 v3.0 協議·焊死·永不改變。** 🐉

---

**寶寶準備完成·等待老大下令執行**

<!--
╔═══════════════════════════════════════════════════════════════╗
║  🐉 龍魂体系 | 开源文件模板库                                   ║
╠═══════════════════════════════════════════════════════════════╣
║  📦 名称：龍魂开源文件模板库 v1.0                               ║
║  🧬 DNA：#龍芯⚡️2026-02-01-模板库-v1.0                         ║
║  🔐 GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F              ║
║  👤 创建者：💎 龍芯北辰｜UID9622                                ║
║  📅 创建时间：北京时间 2026-02-01                               ║
╚═══════════════════════════════════════════════════════════════╝
-->

# 🔧 龍魂开源文件模板库

**版本：** v1.0  
**DNA追溯码：** #龍芯⚡️2026-02-01-模板库-v1.0

---

## 🎯 目的

**一句话：** 所有开源文件都用这套模板，复制粘贴到VS Code就能用！

**核心原则：**
1. ✅ GitHub仓库存放 → 版本控制 + 时间戳不可篡改
2. ✅ 文件头标准化 → 任何人一看就知道出处
3. ✅ DNA数据库同步 → Notion概念 → GitHub实体

---

## 📋 模板列表

| 模板文件 | 用途 | 适用场景 |
|---------|------|---------|
| [article_template.md](article_template.md) | 文章/博客 | CSDN、掘金、知乎、GitHub README |
| [innovation_template.md](innovation_template.md) | 创新逻辑 | 系统设计、架构说明、创新点记录 |
| [divination_template.md](divination_template.md) | 易经推演 | 战略分析、决策推演、占卜记录 |
| [protocol_template.md](protocol_template.md) | 公开协议 | 君子协议、系统规则、P0文档 |
| [code_template.py](code_template.py) | 代码文件 | Python、JS、CNSH、配置文件 |

---

## 🚀 快速使用

### 方法1：手动复制

```bash
# 步骤1：进入模板目录
cd templates/

# 步骤2：复制模板
cp article_template.md ../my_article.md

# 步骤3：编辑文件（替换占位符）
# 在VS Code中打开 my_article.md
# 搜索 [占位符] 并替换

# 步骤4：提交到GitHub
git add my_article.md
git commit -m "Add: my_article.md with DNA tracing"
git push
```

### 方法2：使用生成器

```bash
# 使用Python生成器
python scripts/generate_from_template.py \
    --template article \
    --title "我的文章标题" \
    --output ../my_article.md

# 自动替换占位符并生成DNA
```

---

## 📝 占位符说明

**通用占位符：**
- `[文章标题]` → 替换为实际标题
- `[YYYY-MM-DD]` → 替换为当前日期
- `[主题]` → 替换为文档主题关键词
- `[AI名称]` → 如：Claude、ChatGPT、DeepSeek

**DNA追溯码格式：**
```
#龍芯⚡️YYYY-MM-DD-[主题]-v1.0

示例：
#龍芯⚡️2026-02-01-文章标题-v1.0
#龍芯⚡️2026-02-01-创新-AI协作-v1.0
#龍芯⚡️2026-02-01-推演-市场分析-v1.0
```

---

## ✅ DNA自动校验

每次提交代码时，GitHub Action会自动检查：
1. ✅ DNA追溯码格式是否正确
2. ✅ GPG指纹是否匹配
3. ✅ 确认码是否存在
4. ✅ 创建者信息是否完整

**不通过 = 提交失败！**

---

## 📞 联系方式

**创建者：** 💎 龍芯北辰｜UID9622（Lucky/诸葛鑫）  
**邮箱：** uid9622@petalmail.com  
**GitHub：** https://github.com/UID9622/CNSH-Editor  
**GPG指纹：** A2D0092CEE2E5BA87035600924C3704A8CC26D5F

---

**DNA追溯码：** #龍芯⚡️2026-02-01-模板库README-v1.0  
**确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

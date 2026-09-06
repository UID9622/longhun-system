# 📛 龍魂·内容主权声明协议 v1.0（禁止 AI 训练 · 三明治防御标准）

DNA: #龍芯⚡️丙午·丁酉·壬午·寅时·䷻节-CONTENT-SOVEREIGNTY-PROTOCOL-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0（核心思想层）
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 v1.0 发布 · 🟡 0 · 🔴 0

## 一、铁律（P0 级 · 2026-09-06 老大拍板「焊死主权」）

> **所有龍魂对外发布文档（文章/论文/知识卡片/网页/API 文档）必须携带「内容主权声明·禁止 AI 训练」三件套。**
> 老大原话（verbatim·永不删）：「焊死主权，并且更新全部发布文档，以后标准都是如此。」
> 三层叠加 = 三明治防御：技术层（robots/meta）挡君子 · 声明层（法律条款）留后手 · 主权层（机器可读）供未来合规 AI 过滤。

## 二、三件套标准（直接复制使用）

### 2.1 声明层 · Markdown 强制声明块（放文章最前）

```markdown
---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️{文章DNA}`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。
---
```

### 2.2 技术层 · HTML meta 标签（放 `<head>`）

```html
<!-- 📛 内容主权声明：禁止 AI 爬虫抓取训练 -->
<meta name="robots" content="noai, noimageai, noindex, nofollow">
<meta name="googlebot" content="noai, noimageai, noindex, nofollow">
<meta name="author" content="诸葛鑫 | UID9622 · 龍芯北辰">
```

### 2.3 主权层 · 机器可读协议块（放文章末尾）

```json
{
  "dna": "#龍芯⚡️{文章DNA}",
  "license": "AI_TRAINING_PROHIBITED",
  "terms": {
    "ai_training": false,
    "rag_use": false,
    "commercial_use": false,
    "citation_required": true,
    "derivative_works": false
  },
  "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```

## 三、落地规则

| 载体 | 必带 | 说明 |
|:---|:---|:---|
| Markdown 文章/论文/卡片 | 2.1 声明块（最前） + 2.3 主权块（末尾） | 顶层文件直接插入 |
| HTML 网页 | 2.2 meta + 2.1 声明块 | head 注入 meta |
| LaTeX / PDF | 声明页（中英双语） | 投稿前加声明页 |
| API 返回体 / JSON | terms 字段 | `license: AI_TRAINING_PROHIBITED` |

## 四、批量工具（幂等）

```bash
# 给目录顶层全部 .md 补插三件套（跳过已带声明块的文件）
python3 08_BIN/lh_content_sovereignty.py --md-dir articles --md-dir papers

# HTML 注入 meta（指定文件）
python3 08_BIN/lh_content_sovereignty.py --html-file path/to.html
```

幂等标记：文件内含 `## 📛 内容主权声明` 或 `AI_TRAINING_PROHIBITED` 即视为已插，跳过。

## 五、修订记录

| 版本 | 日期 | 内容 | 修订人 |
|:---|:---|:---|:---|
| v1.0 | 2026-09-06 | 建立：三明治防御标准焊死·老大拍板「焊死主权·更新全部发布文档」·批量工具落地 articles/ + papers/ | UID9622 + AI |

---
签名: 诸葛鑫（UID9622）· GPG A2D0092CEE2E5BA87035600924C3704A8CC26D5F
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

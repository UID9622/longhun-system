# 龍魂文章标准化模板

## 用途

统一所有对外发布文章的：
- 文章抬头（标题、副标题、DNA、CONFIRM 码、主权声明）
- 文章末尾（版权声明、ROOT_CARD、授权范围）

## 文件

- **`article_template_v1.0.md`：已固化的 v1.0 标准模板，带主权熔断警告（推荐）**
- `article-template.md`：早期标准 Markdown 模板，可直接复制使用
- `longhun_article_wrapper.py`：自动把 raw 文本套入 v1.0 模板的脚本

## 一键使用方式

### 方式 1：复制 v1.0 模板手动填充

复制 `article_template_v1.0.md` 全文，把 `{{占位符}}` 替换成实际内容。

> 语音转文字的 raw 文本、有错别字的草稿都可以直接塞进正文占位符，输出后再人工润色一遍即可。模板负责格式和主权标识，你负责内容。

### 方式 2：用脚本自动包装

```bash
# 1. 把 raw 文章写入文件
echo "你的 raw 文章内容..." > /tmp/raw.txt

# 2. 运行包装器
python3 ~/longhun-system/scripts/longhun_article_wrapper.py \
  --input /tmp/raw.txt \
  --title "文章标题" \
  --subtitle "副标题" \
  --series "龍魂系统" \
  --output ~/longhun-system/articles/2026-07-01-my-article.md
```

### 方式 3：只输出到终端

```bash
python3 ~/longhun-system/scripts/longhun_article_wrapper.py \
  --input /tmp/raw.txt \
  --title "文章标题" \
  --stdout
```

## 模板字段说明

| 占位符 | 含义 | 自动生成 |
|--------|------|----------|
| `{{TITLE}}` | 文章标题 | 否，需输入 |
| `{{SUBTITLE}}` | 副标题 | 否，默认取系列名 |
| `{{SERIES}}` | 系列名称 | 否，默认“龍魂系统” |
| `{{DATE}}` | 日期短码如 20260701 | 是 |
| `{{YYYY-MM-DD}}` | 日期如 2026-07-01 | 是 |
| `{{SLUG}}` | URL 友好的标题缩略 | 是 |
| `{{FILENAME}}` | 建议文件名 | 是 |
| `{{CONFIRM_CODE}}` | 一次性确认码 | 是 |
| `{{READ_TIME}}` | 预估阅读分钟数 | 是 |
| `{{LEVEL}}` | 阅读难度 | 否，默认“中” |

## DNA

`#龍芯⚡️2026-07-02-ARTICLE-TEMPLATE-v1.0`

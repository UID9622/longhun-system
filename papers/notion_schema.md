# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 CNSH Academic Runtime · Notion Schema

## THEORY_DB
| 字段 | 类型 | 说明 |
|------|------|------|
| entity_id | text | 实体ID |
| type | select | Definition/Axiom/Lemma/Theorem/Corollary/Formula |
| name | title | 名称 |
| content | text | 内容 |
| latex | text | LaTeX形式 |
| proof | text | 证明 |
| meaning | text | Runtime含义 |
| depends_on | multi_select | 依赖 |
| tags | multi_select | 标签 |
| dna | text | DNA追溯 |
| status | select | draft/review/final |

## PAPER_DB
| 字段 | 类型 | 说明 |
|------|------|------|
| title | title | 论文标题 |
| authors | text | 作者 |
| abstract | text | 摘要 |
| keywords | multi_select | 关键词 |
| dna | text | DNA追溯 |
| status | select | draft/submitted/published |
| created_at | date | 创建时间 |
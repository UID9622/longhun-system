# UID9622_IP_Metadata-Schema_v1.0

> Notion URL: https://app.notion.com/p/UID9622_IP_Metadata-Schema_v1-0-68a781cb9dc946c39946ff21d90bd0bd
> Created: 2025-09-20T13:08:00.000Z
> Last edited: 2025-09-26T19:11:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
# 元数据方案（文件命名 / Front Matter / 索引）
```yaml
---
author: UID9622
module: Metadata-Schema
version: v1.0
release_date: 2025-09-20
source_path: notion:🏛️ UID9622知识产权保护完全指南 | 对外交流+申请流程+材料清单
provenance: Notion->PDF->SHA256->Email->Git
license: proprietary-core + MIT-components
---
```
统一命名示例
### 🔐 哈希留存区（固定）
- 文件名：20250920_UID9622_IP_Metadata-Schema_v1.0.pdf
- SHA-256：
```javascript
<在此粘贴本 PDF 的 SHA-256>
```
- PDF：20250920_UID9622_IP_Metadata-Schema_v1.0.pdf
- 哈希占位：
```javascript
<在此粘贴本 PDF 的 SHA-256>
```
- Version: 1.0 (Initial Release)
- Applicable Use: 跨文件统一索引与出证字段
- Source Path: 🏛️ UID9622知识产权保护完全指南 | 对外交流+申请流程+材料清单
## 1) 文件命名（强制）
```javascript
YYYYMMDD_UID9622_IP_<MODULE>_vX.Y.pdf
```
## 2) Front Matter（Markdown/文档页通用）
```yaml
---
author: UID9622
module: <MODULE>
version: vX.Y
release_date: YYYY-MM-DD
sha256: <hash>
source_path: notion:🏛️ UID9622知识产权保护完全指南 | 对外交流+申请流程+材料清单
license: proprietary-core + MIT-components
provenance: Notion->PDF->SHA256->Email->Git
---
```
## 3) README 索引片段（仓库根）
```markdown
### IP Index
- <MODULE> vX.Y · YYYY-MM-DD · SHA256:<hash8> · [PDF](intellectual-property/...) · [HashLog](intellectual-property/SHA256SUMS.txt)
```

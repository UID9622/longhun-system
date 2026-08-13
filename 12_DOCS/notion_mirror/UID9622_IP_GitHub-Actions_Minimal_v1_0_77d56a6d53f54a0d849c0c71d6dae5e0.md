# UID9622_IP_GitHub-Actions_Minimal_v1.0

> Notion URL: https://app.notion.com/p/UID9622_IP_GitHub-Actions_Minimal_v1-0-77d56a6d53f54a0d849c0c71d6dae5e0
> Created: 2025-09-20T13:08:00.000Z
> Last edited: 2025-09-26T19:11:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
# GitHub Actions 最小工作流（哈希校验 + 版本一致性）
```yaml
---
author: UID9622
module: GitHub-Actions-Minimal
version: v1.0
release_date: 2025-09-20
source_path: notion:🏛️ UID9622知识产权保护完全指南 | 对外交流+申请流程+材料清单
provenance: Notion->PDF->SHA256->Email->Git
license: proprietary-core + MIT-components
---
```
统一命名示例
### 🔐 哈希留存区（固定）
- 文件名：20250920_UID9622_IP_GitHub-Actions-Minimal_v1.0.pdf
- SHA-256：
```javascript
<在此粘贴本 PDF 的 SHA-256>
```
- PDF：20250920_UID9622_IP_GitHub-Actions-Minimal_v1.0.pdf
- 哈希占位：
```javascript
<在此粘贴本 PDF 的 SHA-256>
```
- Version: 1.0 (Initial Release)
- Applicable Use: 提交即检，防漏改文件名/版本号/目录
- Source Path: 🏛️ UID9622知识产权保护完全指南 | 对外交流+申请流程+材料清单
## .github/workflows/ip-guard.yml
```yaml
name: IP Guard
on:
  push:
    branches: [ main ]
    paths:
      - 'intellectual-property/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: List changed files
        id: changes
        run: |
          echo "files<<EOF" >> $GITHUB_OUTPUT
          git diff --name-only $ github.event.before  $ github.sha  >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT
      - name: Check naming convention
        run: |
          FAIL=0
          for f in $(git diff --name-only $ github.event.before  $ github.sha  | grep -E '\\.pdf$'); do
            echo "Checking $f"
            echo "$f" | grep -E '^[0-9]{8}_UID9622_IP_[A-Za-z0-9_-]+_v[0-9]+\\.[0-9]+\\.pdf$' || FAIL=1
          done
          exit $FAIL
      - name: Verify SHA256 manifests (optional)
        run: |
          if [ -f intellectual-property/SHA256SUMS.txt ]; then
            sha256sum -c intellectual-property/SHA256SUMS.txt
          else
            echo "No SHA256SUMS.txt; skipping"
          fi
```
## 提示
- 在 intellectual-property/ 根目录维护一份 SHA256SUMS.txt
- 每次发布后：sha256sum *.pdf >> SHA256SUMS.txt 并提交

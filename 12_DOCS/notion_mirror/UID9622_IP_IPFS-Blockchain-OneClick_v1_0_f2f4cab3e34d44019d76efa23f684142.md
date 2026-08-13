# UID9622_IP_IPFS-Blockchain-OneClick_v1.0

> Notion URL: https://app.notion.com/p/UID9622_IP_IPFS-Blockchain-OneClick_v1-0-f2f4cab3e34d44019d76efa23f684142
> Created: 2025-09-20T13:08:00.000Z
> Last edited: 2025-09-26T19:11:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
# IPFS / 区块链“一键”示例（可选）
```yaml
---
author: UID9622
module: IPFS-Blockchain-OneClick
version: v1.0
release_date: 2025-09-20
source_path: notion:🏛️ UID9622知识产权保护完全指南 | 对外交流+申请流程+材料清单
provenance: Notion->PDF->SHA256->Email->Git
license: proprietary-core + MIT-components
---
```
统一命名示例
### 🔐 哈希留存区（固定）
- 文件名：20250920_UID9622_IP_IPFS-Blockchain-OneClick_v1.0.pdf
- SHA-256：
```javascript
<在此粘贴本 PDF 的 SHA-256>
```
- PDF：20250920_UID9622_IP_IPFS-Blockchain-OneClick_v1.0.pdf
- 哈希占位：
```javascript
<在此粘贴本 PDF 的 SHA-256>
```
- Version: 1.0 (Initial Release)
- Applicable Use: 将哈希或文件指纹上链/上 IPFS 形成第三方留痕
- Source Path: 🏛️ UID9622知识产权保护完全指南 | 对外交流+申请流程+材料清单
## 1) IPFS（使用 Kubo / ipfs-cli）
```bash
# 安装略（参考官方文档）
# 添加文件并获取 CID
ipfs add 20250920_UID9622_IP_WHITEPAPER_v1.0.pdf
# 输出示例：added Qm... 20250920_UID9622_IP_WHITEPAPER_v1.0.pdf
```
- 记录：将 CID 与本地 SHA-256 一并贴到“哈希留存区”
## 2) 只上链文本（以太坊公共链，写入交易 data）
```bash
# 需本地有私钥与少量 gas，示例使用 cast（foundry）
cast send 0x0000000000000000000000000000000000000000 \
  --value 0 \
  --data 0x$(echo -n "UID9622|<SHA256>|<CID(optional)>|YYYY-MM-DD" | xxd -p -c 256) \
  --private-key $PRIVATE_KEY \
  --rpc-url $RPC
```
- 建议：使用测试网或低费率链；注意隐私与合规
## 3) 证据登记（模板）
```javascript
- 本地 SHA-256：<hash>
- IPFS CID：<cid>
- 链上交易：<tx hash> @ <network>
- 登记时间：YYYY-MM-DD hh:mm:ss
```

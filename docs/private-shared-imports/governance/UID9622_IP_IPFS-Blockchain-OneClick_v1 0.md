<!--#龍芯⚡️2026-06-21-GOVERNANCE-UID9622_IP_IPFS-BLOCKCHAIN-ONECLICK_V1-0-v1.0 -->
<!-- 君子協議: 本文件受龍魂DNA追溯保護 -->

# <POTENTIAL_SECRET_PLACEHOLDER>.0

# IPFS / 区块链“一键”示例（可选）

```yaml
---
author: UID9622
module: IPFS-Blockchain-OneClick
version: v1.0
release_date: 2025-09-20
source_path: notion:[🏛️ UID9622知识产权保护完全指南 | 对外交流+申请流程+材料清单](../%F0%9F%8F%9B%EF%B8%8F%20UID9622%E7%9F%A5%E8%AF%86%E4%BA%A7%E6%9D%83%E4%BF%9D%E6%8A%A4%E5%AE%8C%E5%85%A8%E6%8C%87%E5%8D%97%20%E5%AF%B9%E5%A4%96%E4%BA%A4%E6%B5%81+%E7%94%B3%E8%AF%B7%E6%B5%81%E7%A8%8B+%E6%9D%90%E6%96%99%E6%B8%85%E5%8D%95%<POTENTIAL_SECRET_PLACEHOLDER>.md)
provenance: Notion->PDF->SHA256->Email->Git
license: proprietary-core + MIT-components
---
```

**统一命名示例**

### 🔐 哈希留存区（固定）

- 文件名：<POTENTIAL_SECRET_PLACEHOLDER>.0.pdf
- SHA-256：

```
<在此粘贴本 PDF 的 SHA-256>
```

- PDF：<POTENTIAL_SECRET_PLACEHOLDER>.0.pdf
- 哈希占位：

```
<在此粘贴本 PDF 的 SHA-256>
```

- Version: 1.0 (Initial Release)
- Applicable Use: 将哈希或文件指纹上链/上 IPFS 形成第三方留痕
- Source Path: [🏛️ UID9622知识产权保护完全指南 | 对外交流+申请流程+材料清单](../%F0%9F%8F%9B%EF%B8%8F%20UID9622%E7%9F%A5%E8%AF%86%E4%BA%A7%E6%9D%83%E4%BF%9D%E6%8A%A4%E5%AE%8C%E5%85%A8%E6%8C%87%E5%8D%97%20%E5%AF%B9%E5%A4%96%E4%BA%A4%E6%B5%81+%E7%94%B3%E8%AF%B7%E6%B5%81%E7%A8%8B+%E6%9D%90%E6%96%99%E6%B8%85%E5%8D%95%<POTENTIAL_SECRET_PLACEHOLDER>.md)

## 1) IPFS（使用 Kubo / ipfs-cli）

```bash
# 安装略（参考官方文档）
# 添加文件并获取 CID
ipfs add <POTENTIAL_SECRET_PLACEHOLDER>.0.pdf
# 输出示例：added Qm... <POTENTIAL_SECRET_PLACEHOLDER>.0.pdf
```

- 记录：将 CID 与本地 SHA-256 一并贴到“哈希留存区”

## 2) 只上链文本（以太坊公共链，写入交易 data）

```bash
# 需本地有私钥与少量 gas，示例使用 cast（foundry）
cast send <POTENTIAL_SECRET_PLACEHOLDER> \
  --value 0 \
  --data 0x$(echo -n "UID9622|<SHA256>|<CID(optional)>|YYYY-MM-DD" | xxd -p -c 256) \
  --private-key $PRIVATE_KEY \
  --rpc-url $RPC
```

- 建议：使用测试网或低费率链；注意隐私与合规

## 3) 证据登记（模板）

```
- 本地 SHA-256：<hash>
- IPFS CID：<cid>
- 链上交易：<tx hash> @ <network>
- 登记时间：YYYY-MM-DD hh:mm:ss
```
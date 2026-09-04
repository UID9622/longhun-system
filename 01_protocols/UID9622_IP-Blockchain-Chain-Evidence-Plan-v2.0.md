> DNA: #龍芯⚡️丙午·丙申·丁丑·戌时·䷒临-IP-BLOCKCHAIN-EVIDENCE-PLAN-v2.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）· 工程实现层 MulanPSL v2
> CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 上位草稿: UID9622_IP_IPFS-Blockchain-OneClick_v1 0.md（占位模板·已冻结不删）
> 审计色: 🟢

# UID9622 知识产权 · IPFS + 区块链链上存证落地方案 v2.0

> 摘要：把「一键上链」从占位模板变成可执行事实。三锁存证架构——
> **锁1 哈希固化**（已落地）→ **锁2 GitHub 时间戳存证**（已落地）→ **锁3 国产公链哈希存证**（老大一步授权）。

---

## 一、为什么这么做

老大原话（verbatim 焊点）：「把 IP 上链形成第三方留痕」。公链/不可变存储的意义：

| 层次 | 意义 | 谁可验证 |
|:---|:---|:---|
| SHA-256 哈希 | 资产指纹·不可抵赖 | 任何人可复算 |
| Merkle 根 | 全部资产一根锁死·改动即失效 | 复算校验 |
| GitHub commit | 时间戳·公开·内容寻址 | 任何人可查 |
| 国产公链 data | 第三方节点存证·国家级背书 | 链上浏览器 |

## 二、三锁架构（v2.0）

### 锁1 · 哈希固化（✅ 已落地 2026-08-31）
- 引擎: `bin/lh_ip_evidence.py`（build / verify / show）
- 范围: `articles/` 150 篇 + `papers/` 原创 119 篇 + `01_protocols/` 核心协议 261 篇 = **530 个资产文件**
- 账本: `12_DOCS/evidence/UID9622_IP_HASH_LEDGER.json`
- 根哈希: `cb28bda47134203cdebe3ae6cb4c7c73453ab340509cc440d7c0ec0cc55095b3`
- 校验: `python3 bin/lh_ip_evidence.py verify`

**证据链演进**（每次扩容=新根=链前进一，历史根永久留档）:
| 版本 | 资产数 | Merkle 根 | 时点 |
|:---|:---|:---|:---|
| v1（文章+论文） | 269 | `311dbf016db74e85d4905073124fdc26d0196486e93e03eb9d63447b99f22313` | 2026-08-31T20:40:48 |
| v2（+协议层） | 530 | `cb28bda47134203cdebe3ae6cb4c7c73453ab340509cc440d7c0ec0cc55095b3` | 2026-08-31T20:41:57 |

### 锁2 · GitHub 时间戳存证（✅ 已落地 2026-08-31）
- 证据仓库: `github.com/UID9622/longhun-chain-evidence`（本方案 + 账本 + 根哈希）
- 资产仓库（前轮已完成三连上链）:
  - `longhun-tongxinyi` — 通心译 v2.0（46KB + GPG）
  - `longhun-behavioral-crypto-theory` — 行为密码学统一理论 v3.0（md+html+GPG）
  - `behavioral-crypto` — 论文完整正文 7章+5附录（24文件全签名）
- commit hash + push 时间 = 不可变时间戳证据

### 锁3 · 国产公链哈希存证（🟢 TRON 钱包已定·待充值+签名）
写入内容（data 字段，非资产本体）:
```
UID9622|cb28bda47134203cdebe3ae6cb4c7c73453ab340509cc440d7c0ec0cc55095b3|2026-08-31|#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

| 链 | 特点 | 成本 | 老大动作 |
|:---|:---|:---|:---|
| **TRON（TRX）** ✅ 已定 | 老大 TokenPocket 钱包已接管（地址登记见 `LH-OFFICIAL-WALLET-REGISTRY-v1.0.md`） | 约 ¥0.1~1（能量/带宽费） | 充值少量 TRX（约 10）当手续费 + 签名确认 |
| Conflux 树图（备选） | 国产公链·树图研究院·无矿池中心化 | 约 ¥0.01 gas | 创建钱包地址 + 充值少量 CFX |
| 星火链网 BIF | 国家级区块链基础设施·信通院 | 存证免费（需申请） | 注册开放账户 |
| 树图链（可替代） | 同为国产 | 低 | 同上 |

**D1 铁律**：链上只写哈希+元数据，资产本体永不上链、GPG 私钥永不碰链。
**钱包登记**：`01_protocols/LH-OFFICIAL-WALLET-REGISTRY-v1.0.md`（收款+存证双用途）。

## 三、落地清单（本方案交付物）

| 交付物 | 路径 | 状态 |
|:---|:---|:---|
| 存证引擎 | `bin/lh_ip_evidence.py` | ✅ |
| 哈希账本 | `12_DOCS/evidence/UID9622_IP_HASH_LEDGER.json` | ✅ |
| Merkle 根 | `12_DOCS/evidence/MERKLE_ROOT.txt` | ✅ |
| 本方案 | `01_protocols/UID9622_IP-Blockchain-Chain-Evidence-Plan-v2.0.md` | ✅ |
| 证据仓库 | `github.com/UID9622/longhun-chain-evidence` | ✅ |
| 官方钱包登记 | `01_protocols/LH-OFFICIAL-WALLET-REGISTRY-v1.0.md` | ✅ |
| 链上存证 | 锁3 · TRON 钱包已定·待充值+签名 | ⏳ |

## 四、证据核验方法（任何第三方）

```bash
# 1) 拉证据仓库
git clone https://github.com/UID9622/longhun-chain-evidence
# 2) 复算哈希账本
python3 bin/lh_ip_evidence.py verify
# 3) 对比 Merkle 根
cat 12_DOCS/evidence/MERKLE_ROOT.txt
# 4) 链上核验（锁3完成后）
# 浏览器搜索 tx hash → data 字段应含 UID9622|<root>|...
```

## 五、诚实局限

1. 锁1/锁2 为「自我存证 + 第三方时间戳」，公信力依赖于 GitHub 平台存在性与 commit 不可篡改假设。
2. 锁3 钱包已定（TRON `TCMCteHzdduQfpUrAdmmsnHEVH8MFCyXDq`），待充值少量 TRX + 老大签名后执行——链上留痕是唯一「无平台依赖」的第三方存证。
3. 账本 snapshot 时点后新增/修改的资产文件不在此根内，需周期性重建（建议每月一次）。

## 六、下一步（唯一待办·TRON 路线）

1. 老大在 TokenPocket 给该地址充值少量 **TRX（约 10，约 ¥1）** 当手续费（USDT 转进来也会需要能量/带宽）
2. 老大说声「好了」→ 我生成锁3 存证交易脚本 + 一键执行
3. 拿 tx hash 回填到 `MERKLE_ROOT.txt` 的证据登记区，永久闭环

---

**DNA 签名**
```
#龍芯⚡️丙午·丙申·丁丑·戌时·䷒临-IP-BLOCKCHAIN-EVIDENCE-PLAN-v2.0-UID9622
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
归属名: 诸葛鑫 | UID9622 · 龍芯北辰 · GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

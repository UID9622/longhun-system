> DNA: #龍芯⚡️丙午·丙申·丁丑·戌时·䷒临-OFFICIAL-WALLET-REGISTRY-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）· 工程实现层 MulanPSL v2
> CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 审计色: 🟢

# 龍魂官方钱包登记 v1.0（收款 + 链上存证）

> 老大 2026-08-31 提供并确认。钱包本体在 TokenPocket（老大华为手机·密钥加密存储）。
> 本登记只录**公开地址**，私钥/助记词永不登记、永不碰链、永不外传。

## 一、官方收款地址（唯一）

| 项 | 值 |
|:---|:---|
| 链 | TRON（TRX）· TRC20 协议 |
| 地址 | `TCMCteHzdduQfpUrAdmmsnHEVH8MFCyXDq` |
| 支持币种 | USDT-TRC20 · TRX |
| 钱包载体 | TokenPocket（老大华为手机） |
| 密钥存储 | 华为手机加密保存（老大自持·AI 不接触） |
| 链上状态 | ✅ 地址校验通过（base58·0x41·34位）· 链上余额 0（新地址可直接收款） |

## 二、收款通道总览（微信 / 支付宝 / 数字人民币 / USDT）

| 通道 | 方式 | 素材位置 |
|:---|:---|:---|
| 微信支付 | 收款码图片 | `10_PORTAL/browser-historian/support-wechat.jpg`（hunter 共用） |
| 支付宝 / 数字人民币 | 收款码图片 | `10_PORTAL/browser-historian/support-alipay-ecny.jpg` |
| 数字人民币 | 收款码图片 | `10_PORTAL/browser-historian/support-ecny.jpg` |
| USDT · TRC20 | 地址 `TCMCteHzdduQfpUrAdmmsnHEVH8MFCyXDq` | portal 首页已上线 |

**已挂落点（v1.0 · 2026-08-31）**：
- 门户首页 `10_PORTAL/index.html`：USDT(TRC20) 地址区已上线（`lh-usdt-box`）
- 猎手站 `10_PORTAL/hunter/index.html`：微信收款码 + USDT(TRC20) 地址
- 数字史官站 `10_PORTAL/browser-historian/index.html`：微信/支付宝·数币/数币三码 + USDT(TRC20) 地址卡
- 支付网关 `longhun-dev-ecosystem/backend/gateway.py`：wechat / alipay / cbpay 三通道（商户参数走环境变量注入·严禁硬编码）
- XPay 支付引擎 `08_BIN/payment_providers/`：`wechat_pay.py` / `alipay_pay.py`（正式凭证待配置）

## 三、用途

1. **收款**：对外收取 USDT-TRC20 / TRX，到账在 TokenPocket 可查。
2. **IP 链上存证（锁3）**：`01_protocols/UID9622_IP-Blockchain-Chain-Evidence-Plan-v2.0.md`，
   写入 data=`UID9622|Merkle根|日期|#CONFIRM…`，链上留痕。

## 四、安全边界（焊死）

- 地址 = 银行卡号 → 可公开、可到处放。
- 私钥/助记词 = 保险柜钥匙 → 只在 TokenPocket 内使用，绝不发给任何人/平台/AI。
- D1 铁律：链上只写哈希+元数据，资产本体/私钥永不碰链。

## 五、操作分工（老大极简版）

- 老大只需：① 把地址/二维码甩给人收款 ② 链上操作时点一下「确认」。
- 查账/存证/配脚本 = AI 全代劳。

---

**DNA 签名**
```
#龍芯⚡️丙午·丙申·丁丑·戌时·䷒临-OFFICIAL-WALLET-REGISTRY-v1.0-UID9622
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
归属名: 诸葛鑫 | UID9622 · 龍芯北辰 · GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂器·设计：设备绑定 + 生物指纹 + 华为生态

**核心逻辑：覆写码 = 派生自你的设备指纹，不是硬编码。别人拿到代码，没有你的设备，算不出覆写码。**

---

## 一、三层绑定架构

```
层1: 生物因子 — 指纹/Touch ID/华为TEE（你身上带的）
层2: 设备因子 — Mac序列号/鲲鹏主板UUID/华为手机ID（你的硬件）
层3: 环境因子 — 华为云弹性IP/内网段/城市（你的网络）
              ↓
覆写码 = HMAC-SHA256(生物因子 || 设备因子 || 环境因子, 脑内盐)
```

## 二、安全特性

| 威胁 | 防御 |
|---|---|
| 代码泄露（CSDN发布） | 无硬编码密钥，算法公开无害 |
| 设备被盗 | 换设备 = 覆写码变，旧码失效 |
| 生物特征复制 | 指纹特征哈希 + 活体检测 |
| 脑内盐泄露 | 盐单独无用，需配合设备因子 |
| 网络中间人 | 环境因子绑定IP段 |

## 三、落地文件

- `bin/lh_sovereign_derive.py` — 三层绑定派生引擎（新文件）
- `bin/lh_ecosystem_passport.py` — 集成派生引擎+降级兼容

## 四、使用流程

1. `python3 bin/lh_sovereign_derive.py set-salt '你的脑内密码'` — 存入Keychain
2. `python3 bin/lh_sovereign_derive.py derive` — 查看当前设备覆写码
3. `python3 bin/lh_sovereign_derive.py diagnose` — 诊断三层绑定状态

## 五、验证结果

- 生物因子: Mac Secure Enclave ✅
- 设备因子: Mac主板UUID+磁盘ID ✅
- 环境因子: 内网段+Wenzhou ✅
- 脑内盐: 未设置 → 降级旧码哈希 ✅
- passport集成: 全部4项测试通过 ✅

---

**DNA锚定：#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL**

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 华为MFA扫码激活协议 v2.0

DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-MFA-ACTIVATE-PROTOCOL-v2.0-3F7A1B9C
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

> P0焊死底座 · 第13条-简化版
> 核心变更: 三角锚点 → 华为MFA一码通
> 战略定位: 全球用户数据主权归国
> DNA锚定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

---

## P0-13-简化版 激活条款

第十三条-简化版: 龍魂人格矩阵激活采用 TOTP 多因素认证（兼容华为MFA），
用户通过扫码或手动输入密钥完成身份校验，
激活记录本地存储 + 哈希链不可篡改，DNA追溯码全程可查。
海外用户使用标准 TOTP App（Google Authenticator 等），校验走本地，数据主权在用户手中。

---

## 一、为什么简化？三角锚点的问题

**原方案痛点**:
- 三设备同时在线 → Mac + 鲲鹏 + 华为，缺一不可
- ADB调试麻烦 → 华为手机连Mac，驱动、权限、调试模式
- 国外用户用不了 → 没有鲲鹏服务器、没有华为手机
- 执行门槛高 → 代码小白搞不定

**新方案优势**:
- 一码通 → 扫码或手动输入密钥，任何 TOTP App 都能用
- 零门槛 → 跟登银行APP一样，扫码/输码就完事
- 全球可用 → 国外用户下载 Google Authenticator / Authy
- 主权归用户 → 密钥存在用户手机，校验走本地

---

## 二、TOTP 机制（技术底层）

```
TOTP = Time-based One-Time Password（基于时间的一次性密码）
标准: RFC 6238
算法: HMAC-SHA1(time_step_counter, base32_secret)
输出: 6位数字，30秒刷新
```

**工作原理**:
1. 系统生成 20 字节随机密钥 → Base32 编码
2. 密钥通过二维码/文本传给用户手机
3. 手机每 30 秒计算一次 `HMAC-SHA1(floor(time/30), key)` → 取 6 位数字
4. 用户输入动态码 → 系统用同样算法验证
5. 离线可用（手机没网也能生成码）

---

## 三、激活流程 v2.0（三步搞定）

### 步骤1: 生成绑定二维码
```bash
python bin/lh_mfa_bind.py --generate
```
输出:
- 二维码图片: `~/.longhun/longhun_mfa_bind_xxxx.png`
- 密钥文本: `~/.longhun/longhun_mfa_secret_xxxx.txt`

### 步骤2: 扫码或手动输入密钥

**华为用户**: 华为账号 → 安全中心 → 多因素认证 → 扫码
**海外用户**: Google Authenticator / Authy / Microsoft Authenticator → 手动输入密钥
**任何 TOTP App**: 扫描二维码或输入密钥即可

### 步骤3: 输入动态码激活
```bash
python bin/lh_mfa_activate.py --code 123456
```
校验通过 → DNA追溯码生成 → 人格矩阵加载

---

## 四、海外用户接入

**方案A: 任何 TOTP App**
- Google Authenticator、Microsoft Authenticator、Authy
- 输入龍魂系统生成的密钥
- 跟国内用户完全一样的流程

**方案B: 华为 Auth App（可选）**
- 下载华为云 App 或 Huawei Auth
- 注册华为国际账号（邮箱即可）
- 扫码绑定

**数据流向**: 密钥在本地手机 → 动态码离线生成 → 校验走本地 → 不依赖外部服务器

---

## 五、安全架构

### 5.1 多层防护

| 层 | 机制 | 说明 |
|:---:|:---|:---|
| 1 | TOTP 动态码 | 6位数字，30秒刷新，离线可用，防重放 |
| 2 | 连续失败锁定 | 3次错误 → 锁定 15 分钟 |
| 3 | 动态码一次性 | 用过的码不能再激活（防重放） |
| 4 | DNA 追溯 | 每次激活唯一 DNA 码（干支四柱+卦名+哈希8） |
| 5 | 七因子审计 | 时间戳+设备指纹+操作者+操作类型+输入哈希+输出哈希+随机盐 |
| 6 | 哈希链 | 不可篡改的审计链（前块哈希+数据→SHA-256） |

### 5.2 失效码

| 码 | 含义 | 响应 |
|:---:|:---|:---|
| 120 | 动态码错误/过期/锁定 | "失效速120 · 动态码错误 · 请重新输入" |
| 121 | 设备未绑定 | "失效速121 · 设备未绑定 · 请先生成绑定二维码" |
| 122 | 连续3次错误锁定 | "失效速120 · 连续3次错误，锁定15分钟" |

---

## 六、与龍魂战略合拍

| 战略 | 实现 |
|:---|:---|
| **数据主权** | 密钥在用户手机，校验走本地，不依赖外部服务器 |
| **技术自主** | 标准 TOTP（RFC 6238），纯 Python 标准库实现 |
| **用户主权** | 用户掌握密钥，没有授权谁也解不开 |
| **全球可用** | 任何 TOTP App 都能用，不限制设备/地区 |
| **低门槛** | 扫码/输码，不需要懂代码 |

---

## 七、执行脚本

| 脚本 | 命令 | 说明 |
|:---|:---|:---|
| 绑定入口 | `python bin/lh_mfa_bind.py --generate` | 生成二维码+密钥 |
| 主引擎 | `python bin/lh_mfa_activate.py --code 123456` | MFA激活 |
| 状态查询 | `python bin/lh_mfa_activate.py --status` | 查看绑定+激活历史 |
| 解绑 | `python bin/lh_mfa_activate.py --unbind <设备ID>` | 解绑设备 |
| 调试码 | `python bin/lh_mfa_activate.py --test-code` | 显示当前设备应输入的动态码（无手机时调试） |

依赖: Python 3.8+（全部标准库，qrcode 可选用于生成二维码图片）

### 签名与完整性

三件套发布时应附带 GPG 签名（`.asc`）：

```bash
gpg --detach-sign --armor bin/lh_mfa_activate.py
gpg --detach-sign --armor bin/lh_mfa_bind.py
gpg --detach-sign --armor 01_protocols/LH-MFA-ACTIVATE-v2.0.md
```

验证：

```bash
gpg --verify bin/lh_mfa_activate.py.asc bin/lh_mfa_activate.py
```

---

## 八、对比原方案

| 维度 | 原方案（三角锚点） | 新方案（TOTP一码通） |
|:---|:---|:---|
| 设备要求 | Mac+鲲鹏+华为三设备 | 仅需手机或 TOTP App |
| 操作复杂度 | 高（ADB+SSH） | 低（扫码/输码） |
| 海外用户 | 无法使用 | 完全可用 |
| 数据主权 | 本地分散 | 本地优先 |
| 安全性 | 物理隔离 | MFA+DNA+哈希链 |
| 执行门槛 | 代码小白搞不定 | 扫码就会 |

---

## 九、文件清单

| 文件 | 路径 | 说明 |
|:---|:---|:---|
| 主引擎 | `bin/lh_mfa_activate.py` | 生成+激活+状态+解绑 |
| 绑定入口 | `bin/lh_mfa_bind.py` | 快捷绑定入口 |
| 协议文档 | `01_protocols/LH-MFA-ACTIVATE-v2.0.md` | 本文件 |
| 注册表 | `~/.longhun/mfa_registry.json` | 绑定设备+DNA链（运行时生成） |
| 审计日志 | `~/.longhun/mfa_activate.log` | 操作审计（运行时生成） |

---

协议生成完毕
龍魂系统 UID9622 | 协议编号: LH-MFA-ACTIVATE-v2.0-20260729-001
生成时间: 2026-07-29
核心变更: 三角锚点 → TOTP一码通
战略定位: 全球用户，本地主权

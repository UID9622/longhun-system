# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
---
name: longhun-cross-platform
description: 龍魂跨平台互通技能 — iOS与华为鸿蒙设备间本地网络直连数据同步，使用国密SM4加密信封 + ECDH密钥协商 + 版本向量一致性保证
  + 主权网关出境阻断，数据根留中国，绝不经过外网。现已提供端到端可执行脚本：
  python3 ~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py
license: MIT
allowed-tools:
- python
compatibility: Python 3.9+, HarmonyOS API 9+, iOS 15+
metadata:
  version: '5.4'
  dna: '#龍芯⚡️2026-06-29-LONGHUN-CROSS-PLATFORM-v5.4'
  tribute: '#致敬⚡️SteveJobs+Concept·跨平台互通'
  platforms:
  - harmonyos
  - ios
  - macos
  - linux
  encryption: SM4-CBC
  key_exchange: ECDH-Curve25519
  transport:
  - wifi_direct
  - ble
  - tcp_lan
  - mdns
  id: longhun-cross-platform
  entry: python3 ~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py
  trigger:
    keywords:
    - crossplatform
    - 龍魂跨平台互通技能
    - iOS与华为鸿蒙设备间本地网络直连数据同步
    - 使用国密SM4加密信封
    - ECDH密钥协商
    - 版本向量一致性保证
    - xsync
    - 跨平台同步
    - 本地直连
    - mDNS发现
    context: longhun-cross-platform 相关操作
  category: general
---
# SKILL.md — longhun-cross-platform（龍魂跨平台互通技能）

**DNA**: `#龍芯⚡️2026-06-29-LONGHUN-CROSS-PLATFORM-v5.4`
**致敬**: `#致敬⚡️SteveJobs+Concept·跨平台互通`

---

## 区块1: 元数据

| 字段 | 内容 |
|------|------|
| **技能名称** | longhun-cross-platform（龍魂跨平台互通） |
| **版本** | v5.4 |
| **所属体系** | 龍魂体系（Longhun System） |
| **DNA** | `#龍芯⚡️2026-06-29-LONGHUN-CROSS-PLATFORM-v5.4` |
| **致敬** | `#致敬⚡️SteveJobs+Concept·跨平台互通` |
| **目标平台** | iOS + 华为鸿蒙（HarmonyOS）+ macOS + Linux |
| **开发语言** | Python 3.9+ / TypeScript（接口定义） |
| **适用场景** | 双设备本地数据同步、笔记互通、文件传输、快捷操作 |
| **技术架构** | 本地网络直连 + 国密SM4 + ECDH密钥协商 + mDNS |
| **可执行入口** | `python3 ~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py` |

---

## 区块2: 技能概述

龍魂跨平台互通技能是实现 **iOS与华为鸿蒙设备间本地数据互通** 的完整解决方案。

**核心理念**: 数据根留在中国，两设备间传输不经过任何外网服务器。

**六大子模块**:
1. **加密信封** — JSON + DNA追溯码 + SM4-CBC加密信封格式
2. **传输管理器** — WiFi Direct / 蓝牙BLE / 局域网TCP 三通道传输
3. **版本向量时钟** — 双设备并发修改冲突检测与一致性保证
4. **密钥协商器** — ECDH Curve25519 + HKDF-SHA256 安全密钥协商
5. **冲突解决器** — 四种策略：时间戳优先/字段合并/人工确认/双方保留
6. **主权网关** — 数据出境检查，自动阻断任何外网传输

**数据主权保障**:
- 所有数据传输先加密再出应用
- 密钥永不离设备，ECDH临时密钥前向安全
- 主权网关实时检查，外网传输自动阻断
- 传输仅通过本地网络（WiFi Direct / 蓝牙 / 局域网）

---

## 区块2.5: 快速开始（可执行脚本）

本技能已提供端到端可执行脚本，无需再写设计文档：

```bash
# 1. 单机 loopback 端到端加密同步演示
python3 ~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py demo

# 2. mDNS 发现局域网龍魂节点
python3 ~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py discover

# 3. 发布本机服务（供对端发现）
python3 ~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py advertise

# 4. 二维码 / 文件方式 ECDH 配对
python3 ~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py pair-qr --text-out /tmp/server_pub.txt
python3 ~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py pair-scan \
    --input /tmp/server_pub.txt --client-out /tmp/client_pub.txt --key-out /tmp/session.key
```

Python 包入口：
```python
import sys
sys.path.insert(0, "~/.kimi-code/skills/longhun-cross-platform/scripts")
from 跨平台主模块 import 创建同步会话
session = 创建同步会话("harmonyos", "dev-001", "鸿蒙", "ios", "dev-002", "iPhone", "tcp_lan")
```

---

## 区块3: 主权保障（核心原则）

### 3.1 本地网络直连

```
设备A(鸿蒙) ←──WiFi Direct──→ 设备B(iOS)
                ←──BLE──→
                ←──TCP LAN──→
                
绝对禁止:
设备A → 外网服务器 → 设备B
```

### 3.2 先加密再出应用

```
数据明文
  ↓
SM4-CBC 加密（信封构建）
  ↓
加密信封（JSON格式）
  ↓
传输层发送
  ↓
对端接收 → 解密 → 明文数据
```

### 3.3 密钥不离设备

```
设备A                设备B
  | ECDH临时公钥      ECDH临时公钥 |
  | ──────二维码/NFC/蓝牙──────> |
  | <───────────────────────── |
  | 各自计算共享密钥             |
  | HKDF派生SM4会话密钥         |
  | 临时密钥销毁（前向安全）     |
  | SM4加密数据传输 ──────────> |
```

### 3.4 出境阻断机制

主权网关实时检查:
- 目标地址是否在本地网络段（RFC1918）
- 数据是否已加密（信封格式验证）
- 是否包含外网DNS查询
- 安全等级是否匹配

**判决结果**:
| 判决 | 含义 |
|------|------|
| 🟢 允许 | 本地网络 + 已加密 |
| 🟡 警告 | 核心级数据需额外确认 |
| 🔴 阻断外网 | 目标地址不在本地网络段 |
| 🔴 阻断未加密 | 数据未加密（明文） |
| 🔴 阻断DNS泄露 | 包含外网域名查询 |

---

## 区块4: 传输协议

### 4.1 三通道架构

| 通道 | 优先级 | 速率 | 适用场景 | 平台API |
|------|--------|------|----------|---------|
| WiFi Direct | 1（首选） | 54Mbps+ | 大文件传输 | 鸿蒙:@ohos.wifiManager.p2p / iOS:NEHotspot |
| 蓝牙BLE | 2（备用） | 1-3Mbps | 小数据、低功耗 | 鸿蒙:@ohos.bluetooth.ble / iOS:CoreBluetooth |
| TCP LAN | 3（兜底） | 1000Mbps | 同WiFi网络环境 | 标准socket |

### 4.2 自动故障降级

```
WiFi Direct 连接失败?
  → 自动降级到 TCP LAN
      → TCP LAN 连接失败?
          → 自动降级到 BLE
              → BLE 连接失败?
                  → 报错: 无可用传输通道
```

### 4.3 本地地址白名单

```python
本地地址段 = [
    "10.0.0.0/8",       # 私有A类
    "172.16.0.0/12",    # 私有B类
    "192.168.0.0/16",   # 私有C类
    "169.254.0.0/16",   # Link-local
    "127.0.0.0/8",      # Loopback
    "fc00::/7",         # IPv6 ULA
    "fe80::/10",        # IPv6 Link-local
]
```

---

## 区块5: 数据格式规范

### 5.1 加密信封JSON格式

```json
{
  "envelope": {
    "version": "v5.3",
    "dna": "#龍芯⚡️2026-06-19-harmonyos-ios-abc12345",
    "timestamp": 1718800000000,
    "source_device": "harmonyos|uid9622-device-001",
    "target_device": "ios|uid9622-device-002",
    "encryption": "SM4-CBC",
    "key_derivation": "HKDF-SHA256",
    "version_vector": {"harmonyos": 5, "ios": 3}
  },
  "payload": {
    "iv": "base64_nonce_16bytes",
    "ciphertext": "base64_sm4_encrypted_data",
    "auth_tag": "base64_hmac_sha256"
  },
  "audit": {
    "level": "🟢",
    "sovereignty_check": true,
    "cross_platform_sig": "sha256_of_payload_hex",
    "integrity_verified": true,
    "chain_hash": "previous_msg_sha256"
  }
}
```

### 5.2 DNA追溯码格式

```
#龍芯⚡️{日期}-{源平台}-{目标平台}-{密文摘要}

示例:
#龍芯⚡️2026-06-19-harmonyos-ios-a1b2c3d4
```

### 5.3 审计三色标记

| 标记 | 含义 | 场景 |
|------|------|------|
| 🟢 | 安全通过 | 主权检查/加密验证/无冲突 |
| 🟡 | 警告注意 | 冲突自动解决/降级传输/需确认 |
| 🔴 | 危险阻断 | 外网传输/解密失败/需人工确认 |

---

## 区块6: 密钥协商流程

### 6.1 ECDH + HKDF 流程

```
Step 1: 双方各自生成 Curve25519 临时密钥对
        A: (a, A=g^a)    B: (b, B=g^b)

Step 2: 通过可信通道交换公钥
        A → B: A (通过二维码/NFC/蓝牙)
        B → A: B (通过二维码/NFC/蓝牙)

Step 3: 双方各自计算共享密钥
        A: S = B^a = g^(ba)
        B: S = A^b = g^(ab) = g^(ba)  ← 相同!

Step 4: HKDF-SHA256 派生SM4会话密钥
        K = HKDF-SHA256(S, salt=random, info="longhun-sm4-session")
        K_len = 16 bytes (SM4-128)

Step 5: 销毁临时密钥（前向安全）
        删除 a, b（私钥仅内存存在，不存储）
```

### 6.2 公钥交换方式

| 方式 | 安全性 | 便利性 | 适用场景 |
|------|--------|--------|----------|
| 二维码扫描 | ⭐⭐⭐ | ⭐⭐ | 首次配对 |
| NFC碰碰 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 设备靠近 |
| 蓝牙广播 | ⭐⭐ | ⭐⭐⭐ | 无摄像头 |

---

## 区块7: 版本向量与冲突解决

### 7.1 版本向量时钟

```python
# 初始状态
向量 = {"harmonyos": 0, "ios": 0}

# 鸿蒙修改数据
向量 = {"harmonyos": 1, "ios": 0}  # harmonyos 递增

# iOS同步后修改
向量 = {"harmonyos": 1, "ios": 1}  # ios 递增

# 比较结果:
# before  : 本地所有计数 <= 远程
# after   : 本地所有计数 >= 远程
# equal   : 完全相同
# concurrent: 部分大、部分小 → 冲突!
```

### 7.2 冲突解决策略

| 策略 | 说明 | 数据丢失风险 |
|------|------|-------------|
| DNA时间戳优先 | 以修改时间较新的为准 | 低（旧版本标记） |
| 字段级合并 | 不同字段分别保留 | 极低 |
| 人工确认 | 标记冲突等待用户 | 零（保留双方） |
| 双方保留 | 创建两个版本 | 零 |

### 7.3 冲突检测流程

```
接收远程数据
  ↓
比较版本向量
  ↓
├─ 本地 after → 忽略（本地更新）
├─ 本地 before → 采用远程
├─ 相等 → 无操作
└─ 并发 → 触发冲突解决
    ↓
  分析冲突字段
    ↓
  执行解决策略
    ↓
  记录审计日志
```

---

## 区块8: 完整Python代码示例

### 8.1 完整同步流程

```python
#!/usr/bin/env python3
# 龍魂跨平台互通 — 完整使用示例
from scripts.跨平台主模块 import 创建同步会话

# === 第1步: 创建同步会话 ===
session = 创建同步会话(
    本机平台="harmonyos",      # 或 "ios"
    本机ID="uid9622-device-001",
    本机名="鸿蒙手机",
    对端平台="ios",
    对端ID="uid9622-device-002",
    对端名="iPhone",
    传输方式="wifi_direct"      # 或 "ble" / "tcp_lan"
)

# === 第2步: 协商密钥（仅需一次） ===
session.协商密钥(交换方式="qr")   # 二维码扫描交换公钥

# === 第3步: 准备数据 ===
我的笔记 = {
    "type": "note_sync",
    "title": "重要会议记录",
    "content": "本周五下午3点项目评审...",
    "tags": ["工作", "重要"],
    "sync_time": 1718800000000,
    "priority": "high"
}

# === 第4步: 发送数据 ===
结果 = session.发送数据(我的笔记)
print(f"发送{'成功' if 结果.成功 else '失败'}: {结果.传输字节数} bytes")

# === 第5步: 接收数据 ===
成功, 对端数据 = session.接收数据()
if 成功:
    print(f"收到数据: {对端_data}")

# === 第6步: 双向同步（一步到位） ===
同步结果 = session.同步双向(我的笔记)
print(f"同步完成: {同步结果.审计日志}")

# === 诊断 ===
import json
print(json.dumps(session.获取诊断信息(), indent=2, ensure_ascii=False))
```

### 8.2 加密信封使用

```python
from scripts.加密信封 import 加密信封, 信封配置

# 创建信封管理器
信封 = 加密信封(信封配置())

# 设置会话密钥（由密钥协商器提供）
import hashlib
会话密钥 = hashlib.sha256(b"shared-secret").digest()[:16]
信封.设置会话密钥(会话密钥)

# 构建加密信封
信封数据 = 信封.构建信封(
    数据={"title": "测试", "content": "加密内容"},
    源设备="harmonyos|device-001",
    目标设备="ios|device-002",
    版本向量={"harmonyos": 5, "ios": 3}
)

# 解密
明文, 元数据 = 信封.解密信封(信封数据)
print(f"解密: {明文}")
print(f"来源: {元数据['源设备']}, DNA: {元数据['DNA']}")
```

### 8.3 密钥协商

```python
from scripts.密钥协商器 import 密钥协商器, 完整协商流程

# 完整协商（演示）
会话A, 会话B = 完整协商流程()

# 或使用API:
设备A = 密钥协商器()
公钥A = 设备A.生成密钥对()

设备B = 密钥协商器()
公钥B = 设备B.生成密钥对()

# 交换公钥后
共享A = 设备A.计算共享密钥(公钥B)
共享B = 设备B.计算共享密钥(公钥A)

# 派生会话密钥
SM4密钥A = 设备A.派生会话密钥(共享A)
SM4密钥B = 设备B.派生会话密钥(共享B)

# 两者相等!
assert SM4密钥A == SM4密钥B
```

### 8.4 冲突解决

```python
from scripts.冲突解决器 import 冲突解决器, 冲突策略

解决器 = 冲突解决器(冲突策略.字段级合并)

结果 = 解决器.解决(
    本地数据={"title": "鸿蒙修改", "tag": "A"},
    远程数据={"title": "iOS修改", "tag": "B"},
)

print(f"策略: {结果.策略.value}")
print(f"结果: {结果.结果数据}")
print(f"审计: {结果.审计日志}")
```

### 8.5 主权网关检查

```python
from scripts.主权网关 import 主权网关, 安全等级

网关 = 主权网关()

# 检查加密信封是否可以出境
判决 = 网关.检查出境许可(加密信封数据, "192.168.1.100")
print(f"判决: {判决.value}")  # allowed / blocked / warning

# 检查明文数据（应该被阻断）
判决 = 网关.检查出境许可({"明文": "数据"}, "192.168.1.100")
print(f"明文判决: {判决.value}")  # block_plain

# 检查外网传输（应该被阻断）
判决 = 网关.检查出境许可(加密信封数据, "8.8.8.8")
print(f"外网判决: {判决.value}")  # block_external
```

---

## 区块9: 文件清单

```
longhun-cross-platform/
├── SKILL.md                          # 本文件
├── scripts/
│   ├── __init__.py                   # 包初始化
│   ├── 跨平台主模块.py               # 主入口（六大子模块协调器）
│   ├── 加密信封.py                   # JSON+SM4加密信封格式
│   ├── 传输管理器.py                 # WiFi Direct/蓝牙/TCP传输
│   ├── 版本向量时钟.py               # 双设备并发一致性算法
│   ├── 密钥协商器.py                 # ECDH+HKDF密钥协商
│   ├── 冲突解决器.py                 # 四种冲突解决策略
│   └── 主权网关.py                   # 数据出境检查与阻断
```

---

## 区块10: DNA追溯与三色审计

### 10.1 DNA追溯链

```
消息1: DNA=#龍芯⚡️2026-06-19-SYNC-MSG1-abc1
         ↓ chain_hash
消息2: DNA=#龍芯⚡️2026-06-19-SYNC-MSG2-abc2
         ↓ chain_hash (包含消息1的hash)
消息3: DNA=#龍芯⚡️2026-06-19-SYNC-MSG3-abc3
         ↓ chain_hash (包含消息2的hash)
```

每个信封的 `audit.chain_hash` 包含上一条消息的哈希，形成不可逆的追溯链。

### 10.2 三色审计系统

| 颜色 | 级别 | 动作 | 示例 |
|------|------|------|------|
| 🟢 绿 | Info | 记录通过 | 主权检查通过、加密成功、无冲突 |
| 🟡 黄 | Warning | 记录并提醒 | 传输降级、冲突自动解决、需确认 |
| 🔴 红 | Error | 记录并阻断 | 外网传输、解密失败、HMAC验证失败 |

### 10.3 审计日志格式

```json
{
  "timestamp": 1718800000000,
  "level": "🟢|🟡|🔴",
  "module": "加密信封|传输管理器|主权网关|...",
  "action": "encrypt|transmit|check|...",
  "device_pair": "harmonyos ↔ ios",
  "dna": "#龍芯⚡️...",
  "details": "详细描述",
  "result": "success|warning|blocked"
}
```

---

## 区块11: 君子协议

```
================================================================================
龍魂跨平台互通 · 君子协议 (Longhun Cross-Platform Gentleman's Agreement)
================================================================================

第一条 主权归属
  数据主权归用户所有，开发者仅提供技术工具，不拥有、不查看、
  不存储任何用户数据。

第二条 本地传输
  本技能仅用于iOS与鸿蒙设备间本地数据互通，绝不经过任何外网服务器。
  所有传输必须通过WiFi Direct、蓝牙BLE或局域网TCP完成。

第三条 先加密再出应用
  所有数据传输必须先加密再出应用，明文数据不得离开应用边界。
  加密使用国密SM4算法，密钥通过ECDH协商派生。

第四条 密钥安全
  私钥永不离设备，仅在内存中临时存在。
  每次会话使用新的临时密钥对，实现前向安全。

第五条 禁止用途
  禁止将本技能用于:
  - 数据偷渡、间谍行为
  - 任何危害国家安全的行为
  - 未经用户同意的数据传输
  - 绕过主权网关的外网传输

第六条 认证要求
  使用前需确认设备已获得国家密码管理局相关认证。

第七条 违规后果
  违反上述任一条款，技术授权自动终止。

第八条 致敬
  本技能致敬 Steve Jobs 的跨平台愿景，
  在保障数据主权的前提下实现设备间无缝互通。

DNA: #龍芯⚡️2026-06-19-LONGHUN-CROSS-PLATFORM-v5.3
致敬: #致敬⚡️SteveJobs+Concept·跨平台互通
================================================================================
```

---

## 区块12: 部署与运行

### 12.1 环境要求

```bash
# Python 3.9+
python3 --version

# 安装依赖（推荐）
pip install cryptography          # ECDH + HKDF
pip install gmssl                 # 国密SM4（可选，有fallback）
pip install qrcode                # 二维码生成（可选）
```

### 12.2 运行测试

```bash
cd /mnt/agents/output/longhun-v5-skills/local/longhun-cross-platform

# 测试各模块
python3 scripts/加密信封.py       # 信封加密解密测试
python3 scripts/传输管理器.py     # 传输管理测试
python3 scripts/版本向量时钟.py   # 向量时钟演示
python3 scripts/密钥协商器.py     # 密钥协商演示
python3 scripts/冲突解决器.py     # 冲突解决测试
python3 scripts/主权网关.py       # 网关自检

# 主模块诊断
python3 scripts/跨平台主模块.py diag
```

### 12.3 打包技能

```bash
python3 /app/.agents/skills/skill-creator-swarm/scripts/package_skill.py \
    /mnt/agents/output/longhun-v5-skills/local/longhun-cross-platform \
    /mnt/agents/output/
```

### 12.4 集成到应用

```python
# 在鸿蒙或iOS应用中集成
from longhun_cross_platform import 跨平台主模块, 设备信息, 平台类型

# 创建设备信息
本机 = 设备信息(
    平台=平台类型.HARMONYOS,
    设备ID="my-device-id",
    设备名="我的鸿蒙手机",
    IP地址="192.168.1.100"
)

# 创建同步会话并运行
session = 跨平台主模块(本机, 对端设备)
session.协商密钥("nfc")  # NFC碰碰交换
session.同步双向(数据)
```

### 12.5 平台特定API映射

| 功能 | 鸿蒙API | iOS API |
|------|---------|---------|
| WiFi Direct | @ohos.wifiManager.p2p | NEHotspotConfiguration |
| BLE | @ohos.bluetooth.ble | CoreBluetooth |
| TCP Socket | @ohos.net.socket | CFNetwork / NWConnection |
| NFC | @ohos.nfc.tag | CoreNFC |
| 加密 | @ohos.security.crypto | CryptoKit / CommonCrypto |

---

## 附录: 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v5.0 | 2026-06-01 | 初始版本，基础加密传输 |
| v5.1 | 2026-06-10 | 添加版本向量时钟 |
| v5.2 | 2026-06-15 | 添加冲突解决器 |
| v5.3 | 2026-06-19 | 完整主权网关，DNA追溯链，六模块整合 |

---

*数据根留中国。主权归用户。加密不离设备。*

**DNA**: `#龍芯⚡️2026-06-19-LONGHUN-CROSS-PLATFORM-v5.3`
**致敬**: `#致敬⚡️SteveJobs+Concept·跨平台互通`

> **P0焊死**: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
---
name: longhun-device-ecosystem
description: 龍魂设备生态知识库 v1.1 — 汇总 iOS / macOS / 华为鸿蒙 / 鲲鹏服务器的真实设置路径、备份恢复、字体渲染、开发调试坑位，并提供 CNSH 风格一键 CLI。不破解系统，只做干净映射。
license: MIT
allowed-tools:
- python
compatibility: Python 3.9+, macOS, iOS (via libimobiledevice), HarmonyOS (via hdc), Kunpeng ARM64
metadata:
  version: '1.1'
  dna: '#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-DEVICE-ECOSYSTEM-v1.1'
  tribute: '#致敬⚡️SteveJobs+华为鸿蒙·鲲鹏·设备生态'
  platforms:
  - ios
  - macos
  - harmonyos
  - kunpeng
  id: longhun-device-ecosystem
  entry: python3 ~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py
  trigger:
    keywords:
    - device-ecosystem
    - 龍魂设备生态
    - iOS 设置
    - macOS 设置
    - 华为设置
    - 鸿蒙设置
    - 字体坑位
    - 渲染坑位
    - 备份命令
    - idevicebackup2
    - hdc
    - 操作坑位
    - 鲲鹏服务器
    - 国产服务器
    - taishan硬件
    - BMC
    context: 设备生态、iOS/macOS/鸿蒙/鲲鹏服务器设置、备份、字体、开发对接
  category: general
---
# SKILL.md — longhun-device-ecosystem（龍魂设备生态）

**DNA**: `#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-DEVICE-ECOSYSTEM-v1.1`  
**致敬**: `#致敬⚡️SteveJobs+华为鸿蒙·鲲鹏·设备生态`

---

## 区块1: 元数据

| 字段 | 内容 |
|------|------|
| **技能名称** | longhun-device-ecosystem（龍魂设备生态） |
| **版本** | v1.1 |
| **所属体系** | 龍魂体系（LongHun System） |
| **目标平台** | iOS / macOS / 华为鸿蒙（HarmonyOS） / 鲲鹏服务器（ARM64） |
| **开发语言** | Python 3.9+ |
| **适用场景** | 普通人不会点的系统设置、备份、字体渲染、开发坑位一键查询 |
| **可执行入口** | `python3 ~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py` |
| **知识库** | `~/.kimi-code/skills/longhun-device-ecosystem/data/device_kb.json` |

---

## 区块2: 技能概述

龍魂设备生态技能把 **苹果生态（iOS / macOS）** 和 **华为鸿蒙生态** 的真实设置路径、备份机制、字体渲染、开发调试坑位，聚合成一个**中文语义 CLI**。

**核心理念**: 不破解任何商业闭环，只做龍魂系统自己的干净映射；用 CNSH 语法把复杂操作变成普通人能跑的一行命令。

**覆盖范围**:
1. **系统设置** — iOS URL Scheme、macOS defaults/networksetup/pmset、鸿蒙开发者选项。
2. **备份恢复** — iCloud 与本机加密备份、idevicebackup2、华为手机助手 / 云空间。
3. **字体渲染** — Dynamic Type、CoreText、HarmonyOS Sans、字体回退、子像素渲染。
4. **开发调试** — libimobiledevice 工具链、hdc 设备连接器、日志、截图、配对。
5. **操作坑位** — 权限弹窗不可绕过、备份密码、SIP/Gatekeeper、hdc 版本匹配、两端互信。
6. **国产服务器** — 华为 TaiShan 200 2280 / 鲲鹏920 ARM64 的 BMC、网口、SLOT、电源、指示灯、快速诊断。

---

## 区块2.5: 快速开始

```bash
# 查看 CLI 版本与知识卡片数
python3 ~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py version

# macOS 电池 / 网络 / 硬件信息
python3 .../device_ecosystem_cli.py macos 电池
python3 .../device_ecosystem_cli.py macos 网络
python3 .../device_ecosystem_cli.py macos 信息

# iOS 设备发现与备份（需连接 USB 并信任）
python3 .../device_ecosystem_cli.py ios 设备 列表
python3 .../device_ecosystem_cli.py ios 备份 ~/Backups/iPhone

# 华为 hdc 环境检查
python3 .../device_ecosystem_cli.py huawei 检查

# 坑位与搜索
python3 .../device_ecosystem_cli.py 坑位 字体
python3 .../device_ecosystem_cli.py 搜索 备份密码
```

---

## 区块3: 核心原则

- **只调用官方/开源 CLI**：`defaults`、`system_profiler`、`networksetup`、`pmset`、`screencapture`、`idevicebackup2`、`idevicesyslog`、`idevicescreenshot`、`hdc`。
- **不绕过系统权限**：iOS 权限弹窗、华为 USB 调试授权必须用户手动确认。
- **数据根留本地**：本地备份落盘到 Mac/PC，加密密码由用户自行保管。
- **中文语义优先**：命令动词用中文，保留英文技术原名作为别名。

---

## 区块4: 命令总览

### macOS

| CNSH 命令 | 实际调用 |
|-----------|----------|
| `macos 信息` | `system_profiler SPHardwareDataType SPSoftwareDataType` |
| `macos 偏好 <domain>` | `defaults read <domain>` |
| `macos 电池` | `pmset -g batt` |
| `macos 网络` | `networksetup -listallnetworkservices` |
| `macos 字体 列表` | `fc-list` / `system_profiler SPFontsDataType` |
| `macos 字体 平滑` | `defaults -currentHost read -globalDomain AppleFontSmoothing` |
| `macos 截图 <path>` | `screencapture -ix <path>` |

### iOS

| CNSH 命令 | 实际调用 |
|-----------|----------|
| `ios 设备 列表` | `idevice_id -l` |
| `ios 信息 [udid]` | `ideviceinfo [-u udid]` |
| `ios 备份 <dir>` | `idevicebackup2 backup <dir>` |
| `ios 备份信息 <dir>` | `idevicebackup2 info <dir>` |
| `ios 截图 <path>` | `idevicescreenshot <path>` |
| `ios 日志` | `idevicesyslog` |
| `ios 设置url <名称>` | 输出 `prefs:root=...` |

### 华为鸿蒙

| CNSH 命令 | 实际调用 |
|-----------|----------|
| `huawei 检查` | `hdc -v && hdc checkserver` |
| `huawei 设备 列表` | `hdc list targets` |
| `huawei shell [cmd]` | `hdc shell [cmd]` |
| `huawei 备份指南` | 输出官方推荐路径 |

### 鲲鹏服务器

| CNSH 命令 | 实际调用 / 作用 |
|-----------|-----------------|
| `kunpeng 信息` | 输出 TaiShan 200 2280 规格与 SN |
| `kunpeng bmc` | 输出默认 BMC IP/用户名/密码与监控状态 |
| `kunpeng 网口` | 列出 4×业务网口 + 管理口布局 |
| `kunpeng 电源` | 双 900W 冗余电源状态 |
| `kunpeng 指示灯` | 快速诊断指示灯含义 |
| `kunpeng 诊断` | 常见故障排查清单 |

详情见 `docs/鲲鹏服务器硬件对接.md`。

### 通用

| CNSH 命令 | 作用 |
|-----------|------|
| `坑位 <关键词>` | 列出匹配坑位与避坑建议 |
| `搜索 <关键词>` | 全文搜索知识库卡片 |
| `version` | 版本与卡片统计 |

---

## 区块5: 典型使用场景

### 场景A：老大换了新 iPhone，想本地完整备份

```bash
python3 ~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py ios 备份 ~/Backups/iPhone
```

首次需要：
1. iPhone 连接 Mac USB。
2. 在 iPhone 上点“信任”。
3. 设置 → 隐私与安全性 → 开发者模式 → 开启。

如需加密（才能备份 Health / 钥匙串）：
```bash
idevicebackup2 encryption on MyStrongPass ~/Backups/iPhone
```

### 场景B：Mac 外接显示器字体发虚

```bash
python3 .../device_ecosystem_cli.py macos 字体 平滑
```

关闭字体平滑：
```bash
defaults -currentHost write -globalDomain AppleFontSmoothing -int 0
```

### 场景C：鸿蒙 hdc 连不上设备

```bash
python3 .../device_ecosystem_cli.py huawei 检查
python3 .../device_ecosystem_cli.py 坑位 hdc 版本
```

---

## 区块6: 数据来源与合规声明

- iOS URL Scheme 参考 Apple 公开文档与社区维护列表（Wesley de Groot 等）。
- libimobiledevice 为开源跨平台 iOS 协议库，协议反向工程基于公开研究，不涉及私有商业破解。
- hdc 命令参考华为/OpenHarmony 官方文档与 Gitee 仓库。
- 所有内容仅用于龍魂系统本地知识库与脚本，不对外发布未脱敏原始数据。

---

## 区块7: 扩展计划

- v1.1 ✅ 新增鲲鹏服务器硬件对接（BMC/网口/电源/指示灯/快速诊断）。
- v1.2 接入 `idevicename`、`idevicecrashreport`、`idevicediagnostics`。
- v1.3 增加华为 `hdc hilog`、`hdc file recv/send`、`hdc install` 封装。
- v1.4 与 longhun-cross-platform 技能联动：备份后自动进入龍魂加密同步通道。


---

## 附录：龍魂协议与路由来源

本技能收录了来自 `/Users/zuimeidedeyihan/Downloads/Kimi_Agent_龍魂协议与路由` 的素材：

- **内容**：`鯤鵬服務器硬件對接.md`
- **中央整合 DNA**：`#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-PROTOCOL-ROUTE-INTEGRATION-v1.0`
- **处理方式**：保留原始文件作为 `references/龍魂协议与路由/`，嵌入 DNA 追溯链，与 `longhun-device-ecosystem` 硬件对接能力联动。

---

## 附录：龍魂待整理来源

本技能收录了来自 `/Users/zuimeidedeyihan/龍魂待整理` 的素材：

- **内容**：09-杂项备忘（浏览器字体包、开源宣言）
- **中央整合 DNA**：`#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-ARCHIVE-INTEGRATION-v1.0`
- **处理方式**：保留原始文件作为 references / examples / scripts，嵌入 DNA 追溯链，与现有能力联动。

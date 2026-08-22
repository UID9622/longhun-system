> **P0焊死**: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
---
name: longhun-data-hub
description: >
  龍魂本地数据中台技能。当用户提及本地数据采集、数据中台、浏览器历史、下载记录、
  APP 列表、购物记录、设备信息、系统日志归集、本地训练池、数据主权归集等意图时触发。
  负责一键安全采集 macOS 本地数据（浏览器/下载/APP/购物/日志/硬件），全部留存本机，
  默认 dry-run，敏感文件自动排除，生成 DNA 审计清单，并接入龍魂投喂器。
metadata:
  id: longhun-data-hub
  display_name: 龍魂本地数据中台
  version: "2.0"
  author: longhun-dev
  dna: "#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-DATA-HUB-v2.0"
  category: local
  level: L3
  status: active
  tags: [data, 数据中台, 本地数据, 浏览器历史, 下载记录, 购物记录, 数据主权, 龍魂投喂器]
  trigger:
    keywords:
      - 数据中台
      - 本地数据中台
      - 采集数据
      - 数据归集
      - 本地训练池
      - 浏览器历史
      - 下载记录
      - APP列表
      - 应用列表
      - 购物记录
      - 支付宝账单
      - 微信账单
      - 设备信息
      - 系统日志归集
      - 数据主权
      - 我的数据
      - 接管数据
    context: 用户希望采集、归集、管理本地 macOS 数据，构建本地数据资产
    priority: 88
---

# longhun-data-hub | 龍魂本地数据中台

---

## 1. 技能摘要 | Skill Summary

**龍魂本地数据中台**是 UID9622 的本地数据主权基础设施。它将分散在 macOS 系统中的
浏览器历史、下载记录、APP 安装列表、购物账单、设备信息、系统日志等数据，
安全归集到 `~/longhun-system/data-hub/`，全部留存本机，不经过任何云端。

核心原则：
- **数据主权归用户**：所有原始数据只存本地目录
- **默认模拟运行**：首次执行 dry-run，让用户先看再决定
- **敏感文件自动排除**：Keychain、Cookie、Login Data、密码库等永不采集
- **DNA 审计追溯**：每次采集生成清单与哈希链
- **接入龍魂投喂器**：采集元数据自动进入本地训练池索引

---

## 2. 触发条件 | Trigger Conditions

当对话出现以下意图时触发：

- "采集我的数据" / "接管本地数据"
- "浏览器历史" / "下载记录" / "APP 列表"
- "购物记录" / "支付宝账单" / "微信账单"
- "数据中台" / "本地训练池" / "数据归集"
- "设备信息" / "系统日志"
- "数据主权" / "我的数据我说了算"

---

## 3. 输入参数 | Input Parameters

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--dry-run` / `-n` | flag | 否 | 模拟运行，只预览不拷贝 |
| `--sync` / `-s` | flag | 否 | 执行真实采集 |
| `--full` / `-f` | flag | 否 | 完整模式，谨慎使用 |

---

## 4. 执行流程 | Execution Flow

```
[触发语义命中]
  → 默认 dry-run 预览
  → 用户确认后执行 --sync
  → 安全拷贝浏览器数据库（sqlite3 在线备份）
  → 生成下载清单与校验和
  → 采集 APP 安装列表
  → 复制购物账单 CSV
  → 生成系统日志索引（默认不复制内容）
  → 采集硬件/软件信息
  → 生成 DNA 审计清单
  → 元数据接入龍魂投喂器
  → 输出采集报告
```

---

## 5. 数据目录 | Data Directory

```
~/longhun-system/data-hub/
├── raw/
│   ├── browser/              # Safari/Chrome/Firefox 历史（sqlite 备份）
│   ├── shopping/             # 支付宝/微信/账单 CSV
│   ├── downloads_manifest.jsonl
│   ├── downloads_checksums.txt
│   ├── applications_list.txt
│   ├── user_applications_list.txt
│   ├── ios_apps.txt
│   ├── logs/
│   │   ├── user_logs_index.jsonl
│   │   └── system_log_meta.json
│   ├── hardware_info.txt
│   └── software_info.txt
├── processed/                # 清洗后数据（待扩展）
├── index/                    # 清单与索引
└── backup/                   # 定期备份
```

---

## 6. 安全与排除 | Safety & Exclusions

永远**不采集**以下内容：

- Keychain 数据库
- Chrome/Firefox 的 Login Data / Cookies / Web Data
- SSH 私钥、GPG 密钥
- `.uid9622`、`.cnsh_credentials` 目录
- 任何文件名含 `password`、`token`、`secret`、`credential` 的文件

---

## 7. 使用示例 | Examples

```bash
# 一键预览
~/longhun-system/scripts/采集所有数据.sh

# 执行真实采集
~/longhun-system/scripts/采集所有数据.sh --sync

# 完整模式
~/longhun-system/scripts/采集所有数据.sh --full

# 查看数据量
du -sh ~/longhun-system/data-hub/*

# 搜索本地数据
grep -r "关键词" ~/longhun-system/data-hub/raw/
```

---

## 8. DNA 与审计

- 技能 DNA: `#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-DATA-HUB-v2.0`
- 采集器 DNA: `#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LOCAL-DATA-HUB-v2.0`
- 审计日志: `~/longhun-system/logs/data_hub.log`
- 采集清单: `~/longhun-system/data-hub/index/manifest_*.json`

---

## 9. 君子协议

本技能产出默认遵循 CC BY-NC-SA 4.0，数据来源链不可切断。
数据主权属于 UID9622，Kimi 仅作为本地执行代理。

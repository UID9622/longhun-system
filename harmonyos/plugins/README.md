# 🐉 龍魂系統 · HarmonyOS 插件生態

> **DNA**: `#龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-HARMONYOS-PLUGIN-ECOSYSTEM-UID9622`
> **確認碼**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> **主權錨定**: `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`
> **GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
> **分層許可**: 思想層 CC BY-NC-SA 4.0 · 工程層 MulanPSL v2
> **作者**: 諸葛鑫（UID9622·龍芯北辰）
> **日期**: 2026-08-06

---

## 📦 插件總覽（10顆 + Rust核心庫）

| # | 插件 | 類型 | 一句話 |
|:---:|:---|:---|:---|
| 1 | `01-core-service` | Service Ability | **核心底座**·14人格矩陣·三層監督·IPC接口 |
| 2 | `02-memory-browser` | Page Ability | 記憶瀏覽·P0-P3四級·Canvas圖譜·暗金主題 |
| 3 | `03-supervision-dashboard` | Page Ability | 監督儀表盤·環形進度·人格矩陣·審計時間線 |
| 4 | `04-evolution-monitor` | Service + Page | 進化引擎監控·版本歷史·規則檢視器 |
| 5 | `05-sovereignty-verifier` | Page Ability | 主權驗證·7項完整性檢查·身份證明·跨平台 |
| 6 | `06-cross-device-sync` | Service + Form | 跨設備同步·分散式記憶·Super Device·桌面組件 |
| 7 | `07-one-click-migrate` | Page Ability | 一鍵搬遷·設備檢測·工程骨架·DNA注入·驗證 |
| 8 | `08-widget-pack` | Form Ability | 桌面組件套件·狀態·記憶·監督·快捷 |
| 9 | `09-notification-service` | Service Ability | 通知服務·監督告警·進化提案·主權異常 |
| 10 | `10-settings` | Page Ability | 設置·監督頻率·同步開關·關於·許可協議 |

---

## 🏗️ 架構

```
插件層 (10 HAPs)
    ↓ IPC / 分布式總線
共享底座: liblonghun_core.so (Rust → C ABI → ArkTS FFI)
    ↓
HarmonyOS NEXT 設備
    ↓ 分布式總線
Super Device: 手機 ↔ 平板 ↔ 筆記本 ↔ 智慧屏 ↔ 手錶
```

---

## 🔨 構建

### 單插件構建
```bash
cd harmonyos/plugins/01-core-service
hvigorw assembleHap
```

### 全量一鍵構建
```bash
bash harmonyos/plugins/build-all.sh
```

### 部署順序
1. `01-core-service` — 基礎運行時（必須先啟動）
2. `06-cross-device-sync` — 同步底座
3. `02/03/04/05/09` — 功能插件（可並行）
4. `08-widget-pack` — 桌面組件
5. `07-one-click-migrate` — 搬遷工具
6. `10-settings` — 設置

---

## 📱 Super Device 推薦配置

| 設備 | 插件 |
|:---|:---|
| 手機 | 核心服務 + 記憶瀏覽 + 同步 + 通知 + 桌面組件 |
| 平板 | 監督儀表盤 + 進化監控 + 設置 |
| 筆記本 | 搬遷工具 + 主權驗證 |
| 智慧屏 | 監督儀表盤大屏版 |
| 手錶 | 狀態組件 + 通知 |

---

## 🧬 全插件通用要求

- 每個 `.ets` 文件頭含 DNA / 確認碼 / 主權錨定 / GPG / 分層許可
- 繁體「龍」永存
- P0 焊死不可繞過
- 不刪除只凍結

---

## 📂 目錄結構

```
harmonyos/plugins/
├── build-all.sh          # 全量構建腳本
├── README.md             # 本文檔
├── output/               # 構建產物輸出
├── 01-core-service/      # 核心運行時
├── 02-memory-browser/    # 記憶瀏覽
├── 03-supervision-dashboard/
├── 04-evolution-monitor/
├── 05-sovereignty-verifier/
├── 06-cross-device-sync/
├── 07-one-click-migrate/
├── 08-widget-pack/
├── 09-notification-service/
└── 10-settings/
```

---

> 🐉 丙午·癸未·乙酉·坤卦·🟢 · 鴻蒙龍魂生態落地

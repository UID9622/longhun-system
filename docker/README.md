# 龍魂待融入包監控容器

**DNA**: #龍芯⚡️2026-06-16-PACKAGE-WATCHER-CONTAINER-v1.0  
**責任**: UID9622·不免責

---

## 功能

將 `bin/package-watcher.py` 打包為 Docker 容器，主動監控 `~/Downloads` 與 `~` 目錄，每當新增或更新龍魂相關文檔/壓縮包時，自動：

1. 發現並分類待融入包
2. 生成 `docs/package-integration-queue.json` 隊列
3. 生成 `docs/package-watcher-report.md` 可讀報告
4. 標記已融入主幹的包
5. 提供 P0-P3 優先級與建議目標目錄

---

## 快速開始

### 本地運行（無需 Docker）

```bash
cd ~/longhun-system

# 運行一次
bash bin/run-package-watcher.sh local

# 或直接
python3 bin/package-watcher.py --once --prune
```

### 容器運行

```bash
cd ~/longhun-system/docker

# 構建並啟動
docker compose up -d --build

# 查看日誌
docker compose logs -f package-watcher

# 停止
docker compose down
```

---

## 分類規則

| 分類 | 觸發關鍵字 | 建議目標 |
|------|-----------|---------|
| `systems` | 核心系統、系統優化、標準化、啟動、自动化启动 | `systems/` |
| `cnsh` | CNSH、Runtime Governance、語義接入 | `cnsh-core/` |
| `phase3` | Phase 3、phase3 | `phase3/` |
| `protocols` | 協議、协议、protocol、根協議 | `protocols/` |
| `monitoring` | 監控、监控、monitoring、移動端 | `mobile-monitoring.integrated/` |
| `gateway` | 網關、网关、gateway | `integrated-modules/gateway/` |
| `skills` | skill、技能、Skill | `skills/` |
| `warehouse_audit` | 技能检查、warehouse、audit、審計改進 | `skills/warehouse-audit/` |
| `forensics` | forensic、取證、取证 | `tools/forensics/` |
| `docs` | 知識矩陣、計算公式、流水線、使用說明 | `docs/references/` |
| `archive` | backup、備份、archive、歸檔、待整理 | `_archive/` |
| `unknown` | 未匹配 | 待人工分類 |

---

## 文件說明

| 文件 | 說明 |
|------|------|
| `bin/package-watcher.py` | 核心掃描分類腳本 |
| `bin/run-package-watcher.sh` | 本地/容器運行入口 |
| `docker/Dockerfile` | 容器鏡像定義 |
| `docker/docker-compose.yml` | 容器編排配置 |
| `docs/package-integration-queue.json` | 待融入隊列 |
| `docs/package-watcher-report.md` | 可讀報告 |
| `logs/package-watcher.log` | 運行日誌 |

---

## 安全說明

- 容器以**只讀**方式掛載 `~/Downloads` 與 `~`
- 敏感目錄如 `.longhun`、`.longhun-credentials` 已在腳本中排除
- 輸出僅寫入 `longhun-system/docs/` 與 `longhun-system/logs/`
- 不會自動執行或修改任何下載包，僅做分類與隊列登記

---

## 進階用法

```bash
# 自訂監控路徑
python3 bin/package-watcher.py \
  --watch-dir /path/to/watch \
  --output-dir ./docs \
  --interval 60 \
  --prune

# 查看隊列
jq '.packages | to_entries[] | select(.value.priority == "P0") | .value.name' docs/package-integration-queue.json
```

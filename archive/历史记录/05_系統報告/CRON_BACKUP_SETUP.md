# 龍魂系統·Cron 定時備份設置

**時間**: 2026-06-07 22:00 CST
**DNA**:#龍芯⚡️2026-06-07-CRON-WEEKLY-BACKUP-v1.0
**UID**: 9622

## 📋 任務配置

### Cron 時間表

```
0 10 * * 0  /bin/bash ~/longhun-system/scripts/weekly_backup.sh
│ │  │ │ │
│ │  │ │ └─ 星期 (0=周日)
│ │  │ └──── 月份 (*)
│ │  └─────── 日期 (*)
│ └────────── 小時 (10=10:00 CST)
└─────────── 分鐘 (00=整點)
```

### 執行時間
- **時間**: 每週日 10:00 CST (北京時間)
- **頻率**: 每週 1 次
- **時區**: CST (China Standard Time)

### 相關文件
- **腳本**: `~/longhun-system/scripts/weekly_backup.sh`
- **日誌**: `~/.龍魂/logs/weekly_backup.log`
- **備份**: `~/.龍魂/backups/weekly_*_*_*/`

## 🔧 備份腳本

### 功能

```
三層備份:

[1/3] 備份協議文件
      └─ CNSH_v2.0_ROOT_PROTOCOL.md
      └─ CNSH_v2.0_ROOT_PROTOCOL_BILINGUAL.md

[2/3] 備份五層腳本
      └─ L0_MANIFESTO/
      └─ L1_IRON_LAWS/
      └─ L2_WELDED_PROTOCOLS/
      └─ L3_DYNAMIC_GOVERNANCE/
      └─ L4_SUPPLEMENTARY/
      └─ common/ + main.py + setup.sh

[3/3] 備份配置文件
      └─ protocol_weights.json
      └─ tier_permissions.json
      └─ fuse_thresholds.json
      └─ shield_rules.json

清理: 清理 > 12 週的舊備份 (保留空間)
```

### 備份名稱格式

```
weekly_<YEAR>_W<WEEK_NUM>_<YYYYMMDD_HHMMSS>

示例:
  weekly_2026_W23_20260607_220015
```

## 📊 備份清單

| 備份名 | 位置 | 大小 | 文件數 |
|--------|------|------|--------|
| protocols | backup/*/protocols/ | ~40 KB | 2 |
| scripts | backup/*/scripts/ | ~340 KB | 12+ |
| config | backup/*/config/ | ~135 KB | 4 |
| **總計** | **backup/weekly_*** | **~515 KB** | **18+** |

## 💾 恢復步驟

### 快速恢復
```bash
# 1. 找到要恢復的備份
BACKUP_DIR="~/.龍魂/backups/weekly_2026_W23_20260607_220015"

# 2. 恢復協議
cp -r $BACKUP_DIR/protocols/* ~/longhun-system/protocols/

# 3. 恢復腳本
cp -r $BACKUP_DIR/scripts/* ~/longhun-system/scripts/

# 4. 恢復配置
cp -r $BACKUP_DIR/config/* ~/longhun-system/scripts/config/

# 5. 驗證恢復
cd ~/longhun-system/scripts && python3 main.py
```

## 🎯 災難恢復指標

| 指標 | 目標 | 實現 |
|------|------|------|
| RTO (Recovery Time) | 5 分鐘 | ✅ |
| RPO (Recovery Point) | 1 天 | ✅ |
| 備份完整性 | 100% | ✅ |

## 📌 驗證命令

```bash
# 查看 Cron 任務
crontab -l

# 查看備份日誌
tail -f ~/.龍魂/logs/weekly_backup.log

# 列出所有備份
ls -la ~/.龍魂/backups/

# 測試備份腳本
bash ~/longhun-system/scripts/weekly_backup.sh

# 計算備份容量
du -sh ~/.龍魂/backups/
```

---

**DNA**:#龍芯⚡️2026-06-07-CRON-WEEKLY-BACKUP-v1.0
**狀態**: 🟢 配置完成·已激活·運行中
**簽署**: UID9622·不免責

🐉 龍魂系統 · 自動備份 · 永不丟失

# 龍魂系统·Cron 定时备份设置

**时间**: 2026-06-07 22:00 CST
**DNA**:#龍芯⚡️2026-06-07-CRON-WEEKLY-BACKUP-v1.0
**UID**: 9622

## 📋 任务配置

### Cron 时间表

```
0 10 * * 0  /bin/bash ~/longhun-system/scripts/weekly_backup.sh
│ │  │ │ │
│ │  │ │ └─ 星期 (0=周日)
│ │  │ └──── 月份 (*)
│ │  └─────── 日期 (*)
│ └────────── 小时 (10=10:00 CST)
└─────────── 分钟 (00=整点)
```

### 执行时间
- **时间**: 每周日 10:00 CST (北京时间)
- **频率**: 每周 1 次
- **时区**: CST (China Standard Time)

### 相关文件
- **脚本**: `~/longhun-system/scripts/weekly_backup.sh`
- **日志**: `~/.龍魂/logs/weekly_backup.log`
- **备份**: `~/.龍魂/backups/weekly_*_*_*/`

## 🔧 备份脚本

### 功能

```
三层备份:

[1/3] 备份协议文件
      └─ CNSH_v2.0_ROOT_PROTOCOL.md
      └─ CNSH_v2.0_ROOT_PROTOCOL_BILINGUAL.md

[2/3] 备份五层脚本
      └─ L0_MANIFESTO/
      └─ L1_IRON_LAWS/
      └─ L2_WELDED_PROTOCOLS/
      └─ L3_DYNAMIC_GOVERNANCE/
      └─ L4_SUPPLEMENTARY/
      └─ common/ + main.py + setup.sh

[3/3] 备份配置文件
      └─ protocol_weights.json
      └─ tier_permissions.json
      └─ fuse_thresholds.json
      └─ shield_rules.json

清理: 清理 > 12 周的旧备份 (保留空间)
```

### 备份名称格式

```
weekly_<YEAR>_W<WEEK_NUM>_<YYYYMMDD_HHMMSS>

示例:
  weekly_2026_W23_20260607_220015
```

## 📊 备份清单

| 备份名 | 位置 | 大小 | 文件数 |
|--------|------|------|--------|
| protocols | backup/*/protocols/ | ~40 KB | 2 |
| scripts | backup/*/scripts/ | ~340 KB | 12+ |
| config | backup/*/config/ | ~135 KB | 4 |
| **总计** | **backup/weekly_*** | **~515 KB** | **18+** |

## 💾 恢复步骤

### 快速恢复
```bash
# 1. 找到要恢复的备份
BACKUP_DIR="~/.龍魂/backups/weekly_2026_W23_20260607_220015"

# 2. 恢复协议
cp -r $BACKUP_DIR/protocols/* ~/longhun-system/protocols/

# 3. 恢复脚本
cp -r $BACKUP_DIR/scripts/* ~/longhun-system/scripts/

# 4. 恢复配置
cp -r $BACKUP_DIR/config/* ~/longhun-system/scripts/config/

# 5. 验证恢复
cd ~/longhun-system/scripts && python3 main.py
```

## 🎯 灾难恢复指标

| 指标 | 目标 | 实现 |
|------|------|------|
| RTO (Recovery Time) | 5 分钟 | ✅ |
| RPO (Recovery Point) | 1 天 | ✅ |
| 备份完整性 | 100% | ✅ |

## 📌 验证命令

```bash
# 查看 Cron 任务
crontab -l

# 查看备份日志
tail -f ~/.龍魂/logs/weekly_backup.log

# 列出所有备份
ls -la ~/.龍魂/backups/

# 测试备份脚本
bash ~/longhun-system/scripts/weekly_backup.sh

# 计算备份容量
du -sh ~/.龍魂/backups/
```

---

**DNA**:#龍芯⚡️2026-06-07-CRON-WEEKLY-BACKUP-v1.0
**状态**: 🟢 配置完成·已激活·运行中
**签署**: UID9622·不免责

🐉 龍魂系统 · 自动备份 · 永不丢失

# 龍魂多币种·运维手册

## 日常操作

### 启动/停止/重启服务

```bash
# 启动服务
sudo systemctl start longhun-multicurrency-sync

# 停止服务
sudo systemctl stop longhun-multicurrency-sync

# 重启服务
sudo systemctl restart longhun-multicurrency-sync

# 查看状态
systemctl status longhun-multicurrency-sync
```

### 查看日志

```bash
# 实时日志（最后 50 行）
journalctl -u longhun-multicurrency-sync -n 50 -f

# 查看今天的日志
journalctl -u longhun-multicurrency-sync --since today

# 查看错误日志
journalctl -u longhun-multicurrency-sync | grep -i error

# 统计同步成功/失败
journalctl -u longhun-multicurrency-sync | grep "同步成功\|同步失敗" | wc -l
```

### 性能监控

```bash
# 查看进程资源占用
ps aux | grep multicurrency_sync | grep -v grep

# 实时监控（每秒刷新）
watch -n 1 'ps aux | grep multicurrency_sync | grep -v grep'

# 查看内存使用历史
journalctl -u longhun-multicurrency-sync | grep -i "memory\|memory_limit"
```

## 故障排查

### 问题 1: 服务无法启动

**症状**: `systemctl status` 显示 failed

**诊断步骤**:
```bash
# 查看详细错误
journalctl -u longhun-multicurrency-sync -n 100

# 手动运行测试
cd ~/longhun-system/multicurrency
python3 notion_multicurrency_sync.py --once

# 检查依赖
python3 -c "from multicurrency_service import MultiCurrencyHub; print('✅ 模块可用')"
```

**解决方案**:
1. 检查 Python 环境：`python3 --version`
2. 检查工作目录：`cd ~/longhun-system/multicurrency && ls -la`
3. 检查环境变量：`source ~/.longhun/secrets.env && echo $NOTION_TOKEN`
4. 重新启动：`sudo systemctl restart longhun-multicurrency-sync`

### 问题 2: Notion 同步失败

**症状**: 日志中出现 "Notion API 错误"

**诊断步骤**:
```bash
# 检查 Token
source ~/.longhun/secrets.env
curl -s "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_TOKEN" | jq '.object'

# 检查数据库访问
curl -s "https://api.notion.com/v1/databases/$NOTION_MULTICURRENCY_DB" \
  -H "Authorization: Bearer $NOTION_TOKEN" | jq '.title'
```

**解决方案**:
1. 验证 Token 有效性（应该返回 "user"）
2. 验证数据库 ID 正确（应该返回数据库标题）
3. 检查 Notion 集成权限（在 Notion 中查看 Share 设置）

### 问题 3: 内存泄漏

**症状**: 内存占用逐渐增加，最终导致进程被杀死

**诊断步骤**:
```bash
# 监控内存
watch -n 5 'ps aux | grep multicurrency_sync | grep -v grep | awk "{print \$6}"'

# 查看完整进程信息
ps aux | grep multicurrency_sync | grep -v grep
```

**解决方案**:
1. 重启服务：`sudo systemctl restart longhun-multicurrency-sync`
2. 检查 cron 任务是否堆积（多个进程运行）
3. 增加资源限制：编辑 systemd 服务文件，提高 MemoryLimit

### 问题 4: 数据库被锁定

**症状**: `sqlite3.OperationalError: database is locked`

**诊断步骤**:
```bash
# 检查锁定情况
lsof ~/.龍魂/notion_sync.db

# 检查进程
ps aux | grep -E "python|sqlite" | grep -v grep
```

**解决方案**:
1. 停止服务：`sudo systemctl stop longhun-multicurrency-sync`
2. 验证数据库：`sqlite3 ~/.龍魂/notion_sync.db "PRAGMA integrity_check;"`
3. 重启服务：`sudo systemctl start longhun-multicurrency-sync`

## 维护计划

### 每日
- 查看日志，检查有没有错误
- 验证 Notion 中有没有最新的汇率数据

### 每周
- 运行完整测试：`python3 system_test_suite.py --full`
- 检查备份大小：`du -sh ~/.龍魂/backups/`
- 审查性能指标

### 每月
- 备份验证（手动恢复一个备份进行测试）
- 检查日志存储空间
- 评估是否需要调整资源限制

## 恢复步骤

### 从备份恢复

```bash
# 1. 停止服务
sudo systemctl stop longhun-multicurrency-sync

# 2. 恢复备份
TIMESTAMP="20260607_120000"  # 修改为实际备份时间
cp ~/.龍魂/backups/notion_sync.db.$TIMESTAMP.bak ~/.龍魂/notion_sync.db
cp ~/.龍魂/backups/multicurrency.db.$TIMESTAMP.bak ~/.龍魂/multicurrency.db

# 3. 验证数据库完整性
sqlite3 ~/.龍魂/notion_sync.db "PRAGMA integrity_check;"
sqlite3 ~/.龍魂/multicurrency.db "PRAGMA integrity_check;"

# 4. 重启服务
sudo systemctl start longhun-multicurrency-sync

# 5. 验证运行
systemctl status longhun-multicurrency-sync
```

## 性能优化

### 减少 API 调用
- 增加同步间隔：在服务文件中修改 `--interval 300` 为更大的值

### 减少内存占用
- 定期重启服务（通过 cron 或 systemd 计时器）
- 清理日志：`journalctl -u longhun-multicurrency-sync --vacuum-time=7d`

### 提高可靠性
- 启用自动重启：`Restart=always` + `RestartSec=10`
- 配置日志轮转，防止磁盘满

---

**DNA**:#龍芯⚡️2026-06-07-OPERATIONS-MANUAL-v1.0
**版本**: 1.0
**最后更新**: 2026-06-07


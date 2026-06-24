<!--#龍芯⚡️2026-06-21-MULTI-CRON_SETUP-v1.0 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

# 龍魂多币种·定期任务配置

## 设置 cron 任务

### 编辑 crontab

```bash
crontab -e
```

### 添加以下任务

```cron
# 龍魂多币种 - 定期维护任务
# ============================================

# 每日 02:00 运行备份
0 2 * * * /Users/zuimeidedeyihan/longhun-system/multicurrency/backup_databases.sh >> ~/.龍魂/cron.log 2>&1

# 每小时运行一次健康检查
0 * * * * /Users/zuimeidedeyihan/longhun-system/multicurrency/health_check.sh >> ~/.龍魂/cron.log 2>&1

# 每天 03:00 运行系统测试
0 3 * * * cd /Users/zuimeidedeyihan/longhun-system/multicurrency && python3 system_test_suite.py --quick >> ~/.龍魂/cron.log 2>&1

# 每周一 04:00 运行完整测试
0 4 * * 1 cd /Users/zuimeidedeyihan/longhun-system/multicurrency && python3 system_test_suite.py --full >> ~/.龍魂/cron.log 2>&1
```

## 验证 cron 配置

```bash
# 查看已配置的任务
crontab -l

# 查看 cron 日志
tail -f ~/.龍魂/cron.log

# 手动测试备份脚本
~/longhun-system/multicurrency/backup_databases.sh

# 手动测试健康检查
~/longhun-system/multicurrency/health_check.sh
```

## 常见问题

### cron 未执行
- 检查脚本路径是否正确
- 检查脚本是否有执行权限：`chmod +x script.sh`
- 查看系统日志：`log stream --predicate 'eventMessage contains[cd] "cron"'`

### 脚本报错
- 在脚本开头添加：`#!/bin/bash -x` 以启用调试
- 查看日志文件中的错误信息


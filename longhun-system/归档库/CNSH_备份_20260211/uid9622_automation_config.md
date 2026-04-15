# UID9622 自动化配置指南

## Cron 定时任务配置

### 每小时巡检（Linux/macOS）

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每小时整点执行控制台）
0 * * * * cd /Users/zuimeidedeyihan/LuckyCommandCenter && /usr/bin/python3 uid9622_control_plane.py --meta ./instance_meta.json --out ./events >> ./events/cron.log 2>&1

# 5分钟后执行更新器（如果需要强制更新）
5 * * * * cd /Users/zuimeidedeyihan/LuckyCommandCenter && /usr/bin/python3 uid9622_updater.py --events ./events --meta ./instance_meta.json >> ./events/updater.log 2>&1

# 10分钟后执行备份（更新成功后）
10 * * * * cd /Users/zuimeidedeyihan/LuckyCommandCenter && /usr/bin/python3 uid9622_backup_push.py --apply_dir ./mother_applied --snapshots ./snapshots --git_repo_dir ./backup_repo --git_remote origin --git_branch main --http_upload_enabled false >> ./events/backup.log 2>&1
```

### 每天08:00执行（更省资源）

```bash
# 每天08:00执行控制台检查
0 8 * * * cd /Users/zuimeidedeyihan/LuckyCommandCenter && /usr/bin/python3 uid9622_control_plane.py --meta ./instance_meta.json --out ./events >> ./events/cron.log 2>&1

# 08:05执行更新器
5 8 * * * cd /Users/zuimeidedeyihan/LuckyCommandCenter && /usr/bin/python3 uid9622_updater.py --events ./events --meta ./instance_meta.json >> ./events/updater.log 2>&1

# 08:10执行备份
10 8 * * * cd /Users/zuimeidedeyihan/LuckyCommandCenter && /usr/bin/python3 uid9622_backup_push.py --apply_dir ./mother_applied --snapshots ./snapshots --git_repo_dir ./backup_repo --git_remote origin --git_branch main --http_upload_enabled false >> ./events/backup.log 2>&1
```

## Windows 任务计划程序配置

### 创建基本任务

1. **任务1**: UID9622 Control Plane Hourly
   - 触发器：每天，重复每隔1小时
   - 程序：`python`
   - 参数：`uid9622_control_plane.py --meta .\instance_meta.json --out .\events`
   - 起始于：`C:\ABS\PATH\TO\PROJECT`

2. **任务2**: UID9622 Updater Hourly  
   - 触发器：每天，重复每隔1小时
   - 程序：`python`
   - 参数：`uid9622_updater.py --events .\events --meta .\instance_meta.json`
   - 起始于：`C:\ABS\PATH\TO\PROJECT`

3. **任务3**: UID9622 Backup Hourly
   - 触发器：每天，重复每隔1小时  
   - 程序：`python`
   - 参数：`uid9622_backup_push.py --apply_dir .\mother_applied --snapshots .\snapshots --git_repo_dir .\backup_repo --git_remote origin --git_branch main --http_upload_enabled false`
   - 起始于：`C:\ABS\PATH\TO\PROJECT`

## 完整工作流示例

### 手动执行测试

```bash
# 1. 生成控制台事件
python3 uid9622_control_plane.py --meta ./instance_meta.json --out ./events

# 2. 执行更新器（读取事件）
python3 uid9622_updater.py --events ./events --meta ./instance_meta.json

# 3. 执行备份推送
python3 uid9622_backup_push.py --apply_dir ./mother_applied --snapshots ./snapshots --git_repo_dir ./backup_repo --git_remote origin --git_branch main
```

### 使用完整更新器（三源备份）

```bash
python3 uid9622_updater_v3_folder.py \
  --meta ./instance_meta.json \
  --apply_dir ./mother_applied \
  --events_out ./events \
  --local_pkg_dir /ABS/PATH/TO/mother_folder \
  --git_repo https://github.com/xxx/uid9622-mother-package.git \
  --git_branch main \
  --git_pkg_relpath packages/latest_package_folder \
  --http_hook_enabled false
```

## 需要配置的关键参数

### 1. 本地母本包路径
```bash
--local_pkg_dir /Users/zuimeidedeyihan/LuckyCommandCenter/mother_package_folder
```

### 2. Git 仓库配置
```bash
--git_repo https://github.com/yourname/uid9622-mother-package.git
--git_branch main
--git_pkg_relpath mother_package
```

### 3. HTTP 上传配置（待实现）
- 需要提供具体的上传端点
- 支持 zip 文件上传或 API 调用

## 监控和日志

### 日志文件位置
- `./events/cron.log` - 控制台执行日志
- `./events/updater.log` - 更新器执行日志  
- `./events/backup.log` - 备份执行日志
- `./events/event_*.json` - 事件记录文件

### 监控命令
```bash
# 查看最新事件
ls -la ./events/event_*.json | tail -1
cat ./events/event_*.json | tail -1

# 查看日志
tail -f ./events/cron.log
tail -f ./events/updater.log
```

## 故障处理

### 常见问题
1. **权限问题**: 确保脚本有执行权限 `chmod +x *.py`
2. **路径问题**: 使用绝对路径避免相对路径问题
3. **Git 认证**: 确保 SSH 密钥或 token 配置正确
4. **网络问题**: 检查网络连接和防火墙设置

### 应急处理
```bash
# 强制更新
python3 uid9622_control_plane.py --meta ./instance_meta.json --out ./events --mother_version FORCE-LATEST

# 手动备份
python3 uid9622_backup_push.py --apply_dir ./mother_applied --snapshots ./snapshots
```
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂多币种·生产级部署指南 (Path B)

## 📋 部署清单

### 第 1 步：安装 systemd 服务 (需要 sudo)

```bash
# 1. 复制服务文件
sudo cp /tmp/longhun-multicurrency-sync.service /etc/systemd/system/

# 2. 重新加载 systemd 配置
sudo systemctl daemon-reload

# 3. 启用服务（开机自启）
sudo systemctl enable longhun-multicurrency-sync

# 4. 启动服务
sudo systemctl start longhun-multicurrency-sync

# 5. 验证状态
sudo systemctl status longhun-multicurrency-sync
```

### 第 2 步：验证部署成功

```bash
# 查看服务状态
systemctl status longhun-multicurrency-sync

# 查看实时日志
journalctl -u longhun-multicurrency-sync -f

# 检查进程
ps aux | grep multicurrency_sync

# 查看最后 50 行日志
journalctl -u longhun-multicurrency-sync -n 50
```

### 第 3 步：配置日志轮转

创建文件：`/etc/logrotate.d/longhun-multicurrency`

```bash
# 需要 sudo 创建
sudo tee /etc/logrotate.d/longhun-multicurrency > /dev/null << 'LOGROTATE'
/var/log/longhun-multicurrency.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 zuimeidedeyihan staff
    postrotate
        systemctl reload longhun-multicurrency-sync > /dev/null 2>&1 || true
    endscript
}
LOGROTATE
```

### 第 4 步：启动监控和备份

```bash
# 创建备份脚本
cd ~/longhun-system/multicurrency
python3 << 'BACKUP_SCRIPT'
import os, shutil, json
from datetime import datetime

# 每日备份配置
backup_dir = os.path.expanduser('~/.龍魂/backups')
os.makedirs(backup_dir, exist_ok=True)

# 备份 SQLite 数据库
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy(
    os.path.expanduser('~/.龍魂/notion_sync.db'),
    f'{backup_dir}/notion_sync.db.{timestamp}.bak'
)
shutil.copy(
    os.path.expanduser('~/.龍魂/multicurrency.db'),
    f'{backup_dir}/multicurrency.db.{timestamp}.bak'
)

# 清理 7 天以前的备份
import glob
backups = sorted(glob.glob(f'{backup_dir}/*.bak'))
if len(backups) > 7:
    for old in backups[:-7]:
        os.remove(old)
        print(f'删除旧备份: {old}')

print(f'✅ 备份完成: {timestamp}')
BACKUP_SCRIPT
```

### 故障排查

#### 问题 1: 服务无法启动

```bash
# 查看错误日志
journalctl -u longhun-multicurrency-sync -n 100

# 验证 Python 路径
which python3

# 验证工作目录
cd ~/longhun-system/multicurrency && python3 --version

# 验证环境变量
source ~/.longhun/secrets.env
echo $NOTION_TOKEN
echo $NOTION_MULTICURRENCY_DB
```

#### 问题 2: Notion 同步失败

```bash
# 手动测试同步
cd ~/longhun-system/multicurrency
python3 notion_multicurrency_sync.py --once

# 查看实时日志
journalctl -u longhun-multicurrency-sync -f | grep -i error
```

#### 问题 3: 内存泄漏

```bash
# 监控内存使用
watch -n 5 'ps aux | grep multicurrency_sync'

# 重启服务
sudo systemctl restart longhun-multicurrency-sync
```

### 监控命令

```bash
# 查看服务状态
systemctl status longhun-multicurrency-sync

# 跟踪日志
journalctl -u longhun-multicurrency-sync -f

# 统计同步成功/失败
journalctl -u longhun-multicurrency-sync | grep -c "同步成功"

# 查看最后一次同步
journalctl -u longhun-multicurrency-sync -n 5
```

### 日常维护

```bash
# 每天运行一次完整测试
cd ~/longhun-system/multicurrency
python3 system_test_suite.py --quick

# 每周检查日志大小
du -sh /var/log/longhun-multicurrency.log

# 每月备份验证
ls -lh ~/.龍魂/backups/
```

---

**DNA**:#龍芯⚡️丙午·甲午·壬子·丙午·䷙大畜-PRODUCTION-DEPLOYMENT-v1.0
**作者**: UID9622
**更新**: 2026-06-07

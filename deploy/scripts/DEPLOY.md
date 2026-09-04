# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂系统 · 鲲鹏服务器部署手册

> **DNA**: `#龍芯⚡️丙午·乙未·戊子·戊午·䷙大畜-KUNPENG-DEPLOY-BARK-v1.2`
> **适用**: UID9622 · 诸葛鑫
> **目标**: 华为 TaiShan 200 (2280) · 双路鲲鹏920 · openEuler
> **更新**: Bark 双模式架构 (自建华为云 + 官方 api.day.app)

---

## 一、部署入口

根据鲲鹏当前状态选择入口：

| 鲲鹏状态 | 部署入口 | 说明 |
|----------|----------|------|
| 刚开机，系统全新 | `deploy/openeuler-deploy.sh` | 1000+行，全自动环境准备+部署 |
| 系统已有，只差龍魂 | `deploy/longhun-bootstrap.sh` | 27步终极引导部署 |
| 龍魂代码已拉，配服务 | `deploy/scripts/monitor_setup.sh` | systemd+定时任务+监控 |
| Docker 方式 | `docker-compose up -d` | 容器化部署 |

---

## 二、从零到跑起 · 十步法

### 第一步：物理开机
1. 两根电源线插好（900W×2 冗余）
2. 网线插网卡1号口
3. 前面板接显示器+VGA、USB键盘鼠标
4. 按电源按钮⏻

### 第二步：首次登录
- 默认账号: `root`
- 密码: 问供应商

### 第三步：联网配置
```bash
ip addr show                          # 看网卡
vi /etc/sysconfig/network-scripts/ifcfg-eth0  # 改 ONBOOT=yes
systemctl restart network
ping -c 3 114.114.114.114             # 验证联网
```

### 第四步：开 SSH
```bash
systemctl start sshd && systemctl enable sshd
ip addr show | grep inet              # 记下 IP
```
然后从 Mac: `ssh root@鲲鹏IP`

### 第五步：系统初始化
```bash
yum update -y
yum install -y python3 python3-pip git curl wget screen
```

### 第六步：挂载数据盘
```bash
lsblk                                # 看硬盘
mkfs.ext4 /dev/sdb                   # 格式化（如已做RAID则跳过）
mkdir -p /data && mount /dev/sdb /data
echo "/dev/sdb /data ext4 defaults 0 0" >> /etc/fstab
```

### 第七步：拉取龍魂代码
```bash
cd /data
git clone https://github.com/UID9622/longhun-system.git /opt/longhun-system
cd /opt/longhun-system
pip3 install -r requirements.txt
```

### 第八步：部署服务监控（一键）
```bash
# 复制部署脚本到服务器后执行
sudo bash /opt/longhun-system/deploy/scripts/monitor_setup.sh
```

这会自动完成：
- 创建目录结构（日志/数据/备份）
- 生成 5 个 systemd 服务（8080-8084 端口）
- 启动服务 + 开机自启
- 配置 cron 定时任务（自愈/健康检查/归档/备份）
- 安装 `longhun-status` 命令
- 生成 `deploy.sh` 一键部署入口

### 第九步：配置 Bark 推送（推荐·双模式）

#### 模式A：自建 Bark 服务器（推荐·数据不出境）

华为云上运行自建 Bark Docker 服务：

```bash
# 1. 华为云服务器上部署 Bark Server
docker run -d --name bark-server \
  -p 8080:8080 \
  -v /data/bark:/data \
  --restart=always \
  finb/bark-server

# 2. 安全组开放 8080 端口

# 3. iPhone 上装 Bark App
#    App Store 搜 "Bark"
#    打开 → 右上角 + → 自定义服务器
#    填入: http://华为云公网IP:8080
#    复制生成的 Key

# 4. 鲲鹏终端配置环境变量
echo 'export BARK_SERVER="http://华为云公网IP:8080"' >> /etc/environment
echo 'export BARK_KEY="你的iOS设备Key"' >> /etc/environment
source /etc/environment

# 5. 加载龍魂 Bark 插件
source /opt/longhun-system/executors/bark/longhun_bark_plugin.sh
init_bark    # 初始化检测
bark_test    # 测试推送
```

#### 模式B：官方 Bark API（备用，需科学上网）

```bash
# 1. iPhone App Store 搜 Bark，装上
# 2. 打开 App，复制你的 Bark Key
# 3. 设置环境变量（注意：不设置 BARK_SERVER 即为官方模式）
echo 'export BARK_KEY="你的BarkKey"' >> /etc/environment
source /etc/environment

# 4. 手动跑一次验证
bash /opt/longhun-system/deploy/scripts/health_check.sh
```

#### Bark 插件快速使用

```bash
# 加载
source /opt/longhun-system/executors/bark/longhun_bark_plugin.sh

# 一键命令
bark_ops "备份完成" "数据备份成功，耗时3分12秒"
bark_alert "磁盘告警" "使用率85%"
bark_critical "服务宕机" "nginx进程异常退出"
bark_status
bark_logs 20
bark_batch /path/to/batch.txt
```

**飞书备用**（可选）：
```bash
# 如果将来还想用飞书，配这个环境变量即可
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

### 第十步：验证
```bash
longhun-status                        # 一键查看全系统状态
systemctl list-units | grep longhun   # 查看所有龍魂服务
curl http://localhost:8080/health     # 验证技能总线
```

---

## 三、脚本速查

| 脚本 | 路径 | 用途 |
|------|------|------|
| 监控配置 | `deploy/scripts/monitor_setup.sh` | systemd+cron+status命令，一次性配置 |
| 健康检查 | `deploy/scripts/health_check.sh` | 每5分钟跑，服务/端口/资源/Bark推送+飞书备用 |
| 日志归档 | `deploy/scripts/archive_logs.sh` | 每天凌晨4点，保留30天 |
| 数据备份 | `deploy/scripts/backup_data.sh` | 每周日凌晨5点，保留最近10份 |
| 一键部署 | `deploy.sh`（服务器端自动生成） | 检测环境→装依赖→配服务→启动→验证 |

---

## 四、常用运维命令

```bash
longhun-status                                    # 一键状态总览
systemctl status longhun-skillbus                 # 某服务状态
systemctl restart longhun-persona                 # 重启某服务
journalctl -u longhun-skillbus -f                 # 实时日志
cat /var/log/longhun/alarm.log                    # 告警记录
cat /var/log/longhun/health_check.log             # 健康检查记录
```

---

## 五、部署后状态

| 服务 | 端口 | 管理方式 |
|------|:---:|----------|
| 技能总线 | 8080 | systemd 自启 |
| 数字人桥接器 | 8081 | systemd 自启 |
| 人格编排引擎 | 8082 | systemd 自启 |
| DNA登记册 | 8083 | systemd 自启 |
| 生态通行证 | 8084 | systemd 自启 |
| 自愈引擎 | — | cron 每30分钟 |
| 健康检查 | — | cron 每5分钟 |
| 全量体检 | — | cron 每天凌晨3点 |
| 日志归档 | — | cron 每天凌晨4点 |
| 数据备份 | — | cron 每周日凌晨5点 |

---

## 六、从 Mac 访问鲲鹏服务

```bash
# SSH 端口转发
ssh -L 8080:localhost:8080 root@鲲鹏IP

# 然后浏览器打开
open http://localhost:8080
```

---

**总结**: 通电→登录→联网→开SSH→装Python→拉代码→装依赖→跑monitor_setup.sh→完事。

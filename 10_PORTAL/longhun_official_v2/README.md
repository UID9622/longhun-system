> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> DNA: #龍芯⚡️丙午·壬辰·乙亥·壬午·䷚颐-SYNC-COMPLIANCE-20260827-7A2C9F3D
# 龍魂官网 v2.0 部署包

## 文件清单

| 文件 | 说明 |
|------|------|
| `index.html` | 官网主文件（单文件，含 CSS+JS） |
| `deploy-hongkong.sh` | 香港节点一键部署脚本 |
| `deploy-kunpeng.sh` | 鲲鹏算力中心配置脚本 |
| `wireguard-tunnel.sh` | WireGuard 隧道配置（服务端+客户端） |
| `nginx-longhun.conf` | nginx 配置文件（供参考） |

## 部署步骤

### 第一步：香港节点（官网门面）

```bash
# 1. 上传 deploy-hongkong.sh 到香港服务器
scp deploy-hongkong.sh root@香港IP:/root/

# 2. SSH 登录执行
ssh root@香港IP
chmod +x deploy-hongkong.sh
sudo ./deploy-hongkong.sh

# 3. 上传官网文件
scp index.html root@香港IP:/var/www/longhun/
scp -r download/* root@香港IP:/var/www/longhun/download/
scp -r docs/* root@香港IP:/var/www/longhun/docs/
```

### 第二步：鲲鹏（算力中心）

```bash
# 1. 上传并执行配置脚本
scp deploy-kunpeng.sh root@鲲鹏IP:/root/
ssh root@鲲鹏IP
chmod +x deploy-kunpeng.sh
sudo ./deploy-kunpeng.sh
```

### 第三步：隧道打通

```bash
# 在香港节点执行
scp wireguard-tunnel.sh root@香港IP:/root/
ssh root@香港IP
chmod +x wireguard-tunnel.sh
sudo ./wireguard-tunnel.sh hk

# 按脚本输出提示，在鲲鹏执行客户端配置
```

### 第四步：DNS 解析

- `longhun888.com` → A记录 → 香港IP
- `www.longhun888.com` → CNAME → longhun888.com
- `uid9622.cn` → A记录 → 香港IP
- `www.uid9622.cn` → CNAME → uid9622.cn

## 自定义内容

### 替换下载文件
把真实安装包/文档放到 `download/` 和 `docs/` 目录，然后修改 `index.html` 中的：
- 文件名
- 版本号
- 文件大小
- SHA256 值（用 `sha256sum 文件名` 生成）
- DNA 追溯码

### 替换轮播图背景
把 `slide-bg` 的 `background-image` 改成真实图片路径：
```css
background-image: url('./images/banner1.jpg');
```

### 启用 HTTPS
```bash
# 安装 certbot
sudo apt install certbot python3-certbot-nginx
# 申请证书（会自动修改 nginx 配置）
sudo certbot --nginx -d longhun888.com -d www.longhun888.com -d uid9622.cn -d www.uid9622.cn
```

## 安全说明

- 纯静态网站，不收集任何用户数据
- 无 Cookie、无追踪、无登录
- 下载文件带 SHA256 + DNA 追溯
- AI 功能通过内网隧道访问，数据不出鲲鹏

---
龍魂系统 · 龍芯北辰 UID9622
#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

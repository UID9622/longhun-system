# 部署指南

本文档详细说明了如何在不同环境中部署太极八卦易经甲骨文开源系统。

## 🚀 快速部署

### 1. 本地部署

```bash
# 克隆项目
git clone https://gitee.com/open-source/taichi-jiagua-oracle.git
cd taichi-jiagua-oracle

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 或启动生产服务器
npm start
```

访问 `http://localhost:3000` 即可使用。

### 2. Docker 部署

创建 `Dockerfile`：

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

构建和运行：

```bash
# 构建镜像
docker build -t taichi-jiagua-oracle .

# 运行容器
docker run -p 3000:3000 -d taichi-jiagua-oracle
```

## 🌐 云平台部署

### Gitee Pages（静态文件部署）

1. 将项目推送到 Gitee 仓库
2. 在仓库设置中启用 Gitee Pages
3. 选择 `public` 目录作为发布目录
4. 访问 `https://用户名.gitee.io/项目名`

**注意**：Gitee Pages 只能部署静态文件，API 功能无法使用。

### Vercel 部署

1. 将项目推送到 GitHub/Gitee
2. 在 Vercel 中导入项目
3. 配置构建设置：
   - 构建命令：`npm install`
   - 输出目录：`public`
   - 启动命令：`npm start`

### Heroku 部署

1. 创建 `Procfile`：

```
web: npm start
```

2. 部署命令：

```bash
# 安装 Heroku CLI
# 登录 Heroku
heroku login

# 创建应用
heroku create your-app-name

# 部署
git push heroku master
```

## 🖥️ 服务器部署

### Ubuntu/Debian

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装 PM2
sudo npm install -g pm2

# 克隆项目
git clone https://gitee.com/open-source/taichi-jiagua-oracle.git
cd taichi-jiagua-oracle

# 安装依赖
npm install

# 使用 PM2 启动
pm2 start server.js --name "taichi-oracle"

# 设置开机自启
pm2 startup
pm2 save
```

### CentOS/RHEL

```bash
# 安装 Node.js
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs

# 安装 PM2
sudo npm install -g pm2

# 其余步骤同 Ubuntu
```

## 🔄 Nginx 反向代理

创建 Nginx 配置文件 `/etc/nginx/sites-available/taichi-oracle`：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # 静态文件缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/taichi-oracle /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔒 HTTPS 配置

使用 Let's Encrypt：

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加：0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 监控和日志

### PM2 监控

```bash
# 查看进程状态
pm2 status

# 查看日志
pm2 logs taichi-oracle

# 重启应用
pm2 restart taichi-oracle

# 监控面板
pm2 monit
```

### 日志配置

在 `server.js` 中添加日志中间件：

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' })
  ]
});
```

## 🔧 环境变量配置

创建 `.env` 文件：

```env
NODE_ENV=production
PORT=3000
API_RATE_LIMIT=1000
LOG_LEVEL=info
```

在 `server.js` 中使用：

```javascript
require('dotenv').config();
const PORT = process.env.PORT || 3000;
```

## 📈 性能优化

### 1. 启用 Gzip 压缩

```javascript
const compression = require('compression');
app.use(compression());
```

### 2. 设置缓存头

```javascript
app.use(express.static('public', {
  maxAge: '1y',
  etag: true
}));
```

### 3. 集群模式

```javascript
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

if (cluster.isMaster) {
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
} else {
  app.listen(PORT);
}
```

## 🚨 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 查找占用端口的进程
   sudo lsof -i :3000
   # 终止进程
   sudo kill -9 PID
   ```

2. **权限问题**
   ```bash
   # 修改文件权限
   sudo chown -R $USER:$USER /path/to/project
   ```

3. **依赖安装失败**
   ```bash
   # 清除缓存
   npm cache clean --force
   # 删除 node_modules 重新安装
   rm -rf node_modules package-lock.json
   npm install
   ```

### 日志查看

```bash
# PM2 日志
pm2 logs taichi-oracle --lines 100

# 系统日志
sudo journalctl -u nginx -f

# 应用错误日志
tail -f logs/error.log
```

## 📋 部署检查清单

- [ ] 服务器环境配置完成
- [ ] 依赖安装成功
- [ ] 端口开放（防火墙配置）
- [ ] Nginx 反向代理配置
- [ ] SSL 证书安装
- [ ] 进程管理器配置（PM2）
- [ ] 日志轮转配置
- [ ] 监控和备份设置
- [ ] 性能优化配置
- [ ] 安全加固完成

## 🎯 生产环境建议

1. **安全**：定期更新依赖，使用 HTTPS
2. **监控**：设置 uptime 监控和告警
3. **备份**：定期备份代码和数据
4. **扩展**：考虑使用 CDN 和负载均衡
5. **维护**：定期检查日志和性能指标

---

如有部署问题，请提交 Issue 或查看项目文档。

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:12
🧬 DNA追溯码: #CNSH-SIGNATURE-6ec8601a-20251218032412
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 乾卦：天行健，君子以自强不息
📜 内容哈希: c470b2fd5d7a7cf7
⚠️ 警告: 未经授权修改将触发DNA追溯系统

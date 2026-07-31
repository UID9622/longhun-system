# 龍魂令系统 · 公网静态部署报告

DNA: `#龍芯⚡️20260628113734245150-ORDERS-DEPLOY-REPORT-STATIC`

## 部署目标

将龍魂令系统从 Flask 后端渲染改造为 **纯静态页面**，由 Nginx 直接服务，部署到公网：

```
https://longhun888.com/orders/
```

## 线上环境

- **服务器**：华为云 ECS `119.13.90.27`（Ubuntu 24.04）
- **域名**：`longhun888.com`
- **证书**：Let's Encrypt `/etc/letsencrypt/live/longhun888.com/`
- **Nginx 配置**：`/etc/nginx/sites-enabled/longhun888.com`
- **静态文件目录**：`/var/www/longhun/orders/`

## 文件清单

本地与线上统一存放于 `orders/`：

```
orders/
├── index.html          # 首页：四大令级 + 查询入口
├── status.html         # 状态页：锚定令查询结果占位
├── bulletin.html       # 公告栏：最新生效令公示
├── initiate.html       # 发起令：提交证据链占位表单
├── css/
│   └── style.css       # 响应式样式 + 龍魂主题色
├── js/
│   └── order.js        # 查询跳转 + 状态页解析 ?id=
└── DEPLOY.md           # 本报告
```

旧 Flask 版本已备份：

```
/var/www/longhun/orders.flask.bak/
```

## Nginx 关键配置

```nginx
# 龍魂令系统（静态页面）
location ^~ /orders/ {
    root /var/www/longhun;
    index index.html;
    try_files $uri $uri.html $uri/ =404;
}

# 龍魂令状态页兼容 /orders/status/<anchor_id>
location ^~ /orders/status/ {
    root /var/www/longhun;
    try_files /orders/status.html =404;
}

# 龍魂令后端 API（备用）
location ^~ /orders-api/ {
    proxy_pass http://127.0.0.1:8446/orders-api/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

location ^~ /orders/api/ {
    proxy_pass http://127.0.0.1:8446/orders-api/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

> `/orders/` 走静态 root；`/orders/status/<锚定ID>` fallback 到 `status.html`，由前端 JS 读取 `?id=` 展示。

## 部署步骤

1. 本地创建/覆盖 `orders/` 静态文件（HTML/CSS/JS）。
2. 同步到服务器：
   ```bash
   rsync -avz --delete ~/longhun-system/orders/ root@119.13.90.27:/var/www/longhun/orders/
   ```
3. 修改 `/etc/nginx/sites-enabled/longhun888.com`，新增/确认上述 `location`。
4. 测试并重载 Nginx：
   ```bash
   nginx -t && systemctl reload nginx
   ```
5. 浏览器访问验证：首页、状态页、公告栏、发起令、移动端适配。

## 验证结果

| 检查项 | 结果 |
|---|---|
| `https://longhun888.com/orders/` | 200，加载 < 2s |
| `/orders/status.html?id=ORD-DEMO-9622` | 200，正确解析锚定ID |
| `/orders/bulletin.html` | 200 |
| `/orders/initiate.html` | 200，表单占位可用 |
| 移动端 375×812 | 卡片单列、导航换行、无横向滚动 |
| `/orders-api/health`（旧后端备用） | 200，服务正常 |

## 后续迭代

- 将 `initiate.html` 表单提交接入真实后端 `/orders-api/create`。
- 状态页 `status.html` 调用 `/orders-api/status?id=...` 动态渲染真实数据。
- 如需全链路 DNA 追溯，可在 JS 中调用 `/orders-api/anchor/<id>`。

## 主权声明

本系统归属中华人民共和国，数据根留中国，令出即锚、锚定即追溯、追溯即公示。

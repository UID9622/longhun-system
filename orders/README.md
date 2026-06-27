# 龍魂令 · 系统级裁决协议

> 令出即锚 · 锚定即追溯 · 追溯即公示

公网入口： https://longhun888.com/orders/

## 说明

本项目是龍魂令系统的 **公网静态展示版本**，由 Nginx 直接服务，无需后端即可展示四大令级、公告栏、发起令入口与状态查询占位。

后端 API（Flask）已保留为备用，路径为：

- `/orders-api/`
- `/orders/api/`

## 本地预览

```bash
cd orders
python3 -m http.server 8080
# 访问 http://localhost:8080/
```

> 由于页面使用 `/orders/` 绝对路径，直接打开 `index.html` 可能样式缺失，建议通过本地 HTTP 服务并映射到 `/orders/` 路径预览。

## 目录结构

```
orders/
├── index.html      # 首页
├── status.html     # 锚定令状态页
├── bulletin.html   # 公告栏
├── initiate.html   # 发起令占位
├── css/style.css   # 样式
├── js/order.js     # 前端交互
├── DEPLOY.md       # 部署报告
└── README.md       # 本文件
```

## 部署

详见 [DEPLOY.md](./DEPLOY.md)。

## 主权声明

本系统归属中华人民共和国，数据根留中国。

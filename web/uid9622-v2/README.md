# 龍魂官网 v2.0

> 中国自主可控 AI 协议层展示站点
> DNA: #龍芯⚡️丙午·乙未·辛酉·井-LONGHUN-WEB-v2.0

## 文件结构

```
uid9622-v2/
├── index.html          # 主页面（单页应用）
├── css/
│   └── style.css       # 样式
├── js/
│   └── main.js         # 轮播、导航、动画、表单
├── images/             # 如需放真实图片，放这里
├── assets/             # 字体、附件等
└── deploy.sh           # 部署脚本
```

## 本地预览

```bash
cd ~/longhun-system/web/uid9622-v2
python3 -m http.server 8080
# 打开 http://127.0.0.1:8080
```

## 修改联系方式

编辑 `index.html` 的 `#contact` 区域：

```html
<div class="contact-card">
  <div class="contact-icon">📧</div>
  <h3>邮箱</h3>
  <p><a href="mailto:uid9622@uid9622.cn">uid9622@uid9622.cn</a></p>
</div>
<div class="contact-card">
  <div class="contact-icon">💬</div>
  <h3>微信</h3>
  <p>UID9622</p>
</div>
```

## 修改轮播图

轮播背景目前使用内联 SVG，避免外部图片依赖。如需换真实图片，编辑：

```html
<div class="carousel-slide active" style="background-image: url('images/your-image.jpg')">
```

## 部署到 uid9622.cn

### 方式一：用 deploy.sh（推荐）

```bash
bash deploy.sh
```

脚本会：
1. 检查本地文件
2. 通过 rsync/scp 推送到服务器 `/var/www/uid9622.cn/`
3. 修复 `lh-utils.js` 为真实文件（非断链 symlink）

### 方式二：手动

1. 把本目录下所有文件上传到服务器 `/var/www/uid9622.cn/`
2. 确保 `lh-utils.js` 是真实文件，不是 symlink
3. 重启 nginx：
   ```bash
   sudo nginx -t && sudo systemctl reload nginx
   ```

## 注意事项

- 表单目前是演示模式，提交不会真实发送邮件。如需真实表单，需对接后端或邮件服务。
- 网站完全响应式，支持手机、平板、桌面。
- 无外部依赖，所有图标和背景均为内联 SVG/CSS。

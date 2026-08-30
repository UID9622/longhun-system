# DNA: #龍芯⚡️丙午·壬辰·乙亥·壬午·䷚颐-SYNC-COMPLIANCE-20260827-7A2C9F3D
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# ============================================
# 龍魂官网 · 香港节点一键部署脚本
# 执行环境：OpenEuler / CentOS / Ubuntu
# 执行方式：chmod +x deploy-hongkong.sh && sudo ./deploy-hongkong.sh
# ============================================

set -e

DOMAIN1="longhun888.com"
DOMAIN2="uid9622.cn"
WEB_ROOT="/var/www/longhun"
NGINX_CONF="/etc/nginx/conf.d/longhun.conf"

echo "[龍魂] 开始部署官网到香港节点..."

# 1. 安装 nginx
if ! command -v nginx &> /dev/null; then
    echo "[龍魂] 安装 nginx..."
    if command -v apt &> /dev/null; then
        apt update && apt install -y nginx
    elif command -v yum &> /dev/null; then
        yum install -y nginx
    elif command -v dnf &> /dev/null; then
        dnf install -y nginx
    else
        echo "[错误] 无法识别包管理器，请手动安装 nginx"
        exit 1
    fi
fi

# 2. 创建目录结构
echo "[龍魂] 创建网站目录..."
mkdir -p ${WEB_ROOT}/{download,docs,images,css,js}
chmod -R 755 ${WEB_ROOT}
chown -R nginx:nginx ${WEB_ROOT} 2>/dev/null || chown -R www-data:www-data ${WEB_ROOT}

# 3. 写入 nginx 配置
echo "[龍魂] 写入 nginx 配置..."
cat > ${NGINX_CONF} << 'NGINX_EOF'
# /etc/nginx/conf.d/longhun.conf
# 龍魂系统官网 nginx 配置 · 香港节点 · 双域名同步

server {
    listen 80;
    server_name longhun888.com www.longhun888.com uid9622.cn www.uid9622.cn;
    root /var/www/longhun;
    index index.html;

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

    # 静态资源缓存
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # 下载中心：强制下载 + 显示列表
    location /download/ {
        alias /var/www/longhun/download/;
        autoindex on;
        autoindex_exact_size off;
        autoindex_localtime on;
        add_header Content-Disposition "attachment" always;
        add_header Cache-Control "no-cache" always;
    }

    # 文档目录：PDF 直接预览
    location /docs/ {
        alias /var/www/longhun/docs/;
        add_header Cache-Control "public, max-age=86400";
    }

    # 反向代理到鲲鹏 AI（WireGuard 隧道内网地址）
    location /api/ai/ {
        proxy_pass http://10.8.0.2:11434/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    # 默认 location
    location / {
        try_files $uri $uri/ =404;
        add_header Cache-Control "no-cache" always;
    }

    # 日志（可选关闭以减少 IO）
    access_log /var/log/nginx/longhun_access.log;
    error_log /var/log/nginx/longhun_error.log;
}

# HTTPS 升级（证书配好后启用）
# server {
#     listen 443 ssl http2;
#     server_name longhun888.com www.longhun888.com uid9622.cn www.uid9622.cn;
#     ssl_certificate /etc/nginx/ssl/longhun.crt;
#     ssl_certificate_key /etc/nginx/ssl/longhun.key;
#     include /etc/nginx/conf.d/longhun.conf;  # 引用上面的配置
# }

NGINX_EOF

# 4. 测试并重载 nginx
echo "[龍魂] 测试 nginx 配置..."
nginx -t

echo "[龍魂] 启动/重载 nginx..."
systemctl enable nginx
systemctl restart nginx

# 5. 防火墙放行
if command -v firewall-cmd &> /dev/null; then
    firewall-cmd --permanent --add-service=http
    firewall-cmd --permanent --add-service=https
    firewall-cmd --reload
elif command -v ufw &> /dev/null; then
    ufw allow 80/tcp
    ufw allow 443/tcp
fi

echo ""
echo "========================================"
echo "[龍魂] 香港节点部署完成"
echo "========================================"
echo "网站根目录: ${WEB_ROOT}"
echo "nginx 配置: ${NGINX_CONF}"
echo ""
echo "下一步："
echo "1. 把 index.html 上传到 ${WEB_ROOT}/"
echo "2. 把安装包上传到 ${WEB_ROOT}/download/"
echo "3. 把文档上传到 ${WEB_ROOT}/docs/"
echo "4. DNS 解析两个域名到本机 IP"
echo "5. 可选：配置 HTTPS 证书 (certbot)"
echo ""
echo "上传命令（Mac 终端执行）："
echo "  scp index.html root@香港IP:${WEB_ROOT}/"
echo "  scp -r download/* root@香港IP:${WEB_ROOT}/download/"
echo "========================================"

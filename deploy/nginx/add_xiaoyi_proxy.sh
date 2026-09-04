#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙未·子时·䷀乾-DEPLOY-NGINX-XIAOYI-v1.0-a1b2c3d7
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 用途: 在鲲鹏nginx上加 /xiaoyi/ 反向代理到FRP穿透端口

# 在鲲鹏上执行此脚本，或通过SSH远程执行
# ssh root@119.13.90.27 'bash -s' < deploy/nginx/add_xiaoyi_proxy.sh

NGINX_CONF="/etc/nginx/conf.d/uid9622.cn.conf"
XIAOYI_BLOCK='
    # === 小艺桥接（FRP穿透·Mac→鲲鹏） ===
    location /xiaoyi/ {
        proxy_pass http://127.0.0.1:18799/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
        # 安全：只允许龍魂内部IP
        # allow 127.0.0.1;
        # 对外开放（带API密钥验证由小艺桥接层处理）
    }
'

echo "🔗 龍魂 · 鲲鹏 nginx 添加小艺反代"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 检查配置是否已存在
if grep -q "location /xiaoyi/" "$NGINX_CONF" 2>/dev/null; then
    echo "  ⚠️  /xiaoyi/ 配置已存在，跳过"
    echo "  现有配置:"
    grep -A 5 "location /xiaoyi/" "$NGINX_CONF"
    echo ""
    echo "如需重建，请手动删除后重跑"
    exit 0
fi

# 备份原配置
cp "$NGINX_CONF" "${NGINX_CONF}.bak.$(date +%Y%m%d_%H%M%S)"
echo "  ✅ 已备份: ${NGINX_CONF}.bak.$(date +%Y%m%d_%H%M%S)"

# 在最后一个 } 之前插入 xiaoyi block
# 找到 server { 块中最后一个 location 后面插入
sed -i '' '/^}/i\
    # === 小艺桥接（FRP穿透·Mac→鲲鹏） ===\
    location /xiaoyi/ {\
        proxy_pass http:\/\/127.0.0.1:18799\/;\
        proxy_http_version 1.1;\
        proxy_set_header Upgrade $http_upgrade;\
        proxy_set_header Connection "upgrade";\
        proxy_set_header Host $host;\
        proxy_set_header X-Real-IP $remote_addr;\
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\
        proxy_set_header X-Forwarded-Proto $scheme;\
        proxy_read_timeout 86400s;\
        proxy_send_timeout 86400s;\
    }\
' "$NGINX_CONF" 2>/dev/null || {
    # macOS sed 不兼容，用 Python
    python3 -c "
import re
with open('$NGINX_CONF', 'r') as f:
    content = f.read()

# 在最后一个 } 前插入
xiaoyi_block = '''
    # === 小艺桥接（FRP穿透·Mac→鲲鹏） ===
    location /xiaoyi/ {
        proxy_pass http://127.0.0.1:18799/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection \"upgrade\";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
'''
last_brace = content.rfind('}')
content = content[:last_brace] + xiaoyi_block + content[last_brace:]
with open('$NGINX_CONF', 'w') as f:
    f.write(content)
"
}

# 验证nginx配置
if nginx -t 2>&1; then
    echo "  ✅ nginx 配置验证通过"
    systemctl reload nginx
    echo "  ✅ nginx 已重载"
else
    echo "  🔴 nginx 配置有误，回滚..."
    cp "${NGINX_CONF}.bak.$(date +%Y%m%d_%H%M%S)" "$NGINX_CONF"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 /xiaoyi/ 反代配置完成！"
echo "  地址: https://uid9622.cn/xiaoyi/"
echo "  DNA: #龍芯⚡️丙午·乙未·乙未·子时·䷀乾-DEPLOY-NGINX-XIAOYI-v1.0-a1b2c3d7"

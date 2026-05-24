#!/usr/bin/env bash
# 只打印怎么填 secrets.env · 不读 token 内容
SECRETS="$HOME/.longhun/secrets.env"
echo "🔐 密钥只登记一处: $SECRETS"
echo "权限应为: -rw-------  (chmod 600)"
ls -la "$SECRETS" 2>/dev/null || echo "(文件不存在)"
echo ""
echo "NOTION_TOKEN= 去 https://www.notion.so/my-integrations 创建内部集成"
echo "DB_* 已建库 ID 见接单台页面下 5 个 Database"
echo "填好后: source ~/.longhun/secrets.env"

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍智守 · 华为服务器部署包生成器 v2.1

把本地 bot 脚本、依赖模块、示例配置、systemd / nginx 模板打包成一个可部署目录，
自动排除 ~/.longhun/config/ 下的私密配置和主密钥。

DNA:#龍芯⚡️2026-06-30-LONGZHISHOU-PACKAGER-FILE2-v2.1
"""

import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
SRC_BOT = HOME / "Downloads" / "龍智守_本地控制接口_v2.0.py"
SRC_CONFIG_EXAMPLE = HOME / ".longhun" / "config" / "龍智守_config.example.json"
SRC_SCRIPTS_DIR = HOME / "longhun-system" / "scripts"
SRC_OPTIMIZER_DIR = HOME / "Downloads" / "Kimi_Agent_龍魂训练协议"
SRC_GUOMI = HOME / "CNSH_国密工具.py"
OUTPUT_BASE = HOME / "longhun-system" / "dist"

# bot 运行时需要从 ~/longhun-system/scripts 加载的模块
REQUIRED_SCRIPT_MODULES = [
    "龍魂DNA主權引擎.py",
    "龍魂語義歸一化閘門.py",
    "内容主权审查器.py",
    "龍魂身份注册器.py",
    "longhun_lu_compress.py",
    "longhun_lu_gallery.py",
    "longhun_lu_importer.py",
    "longhun_collective_wisdom.py",
    "longhun_toolset_ecosystem.py",
    "longhun_system_evaluation.py",
    "龍智守_打包部署.py",
]

# 训练数据优化器相关文件
REQUIRED_OPTIMIZER_FILES = [
    "龍魂訓練數據優化器_v3.2.0.py",
]


def copy_file(src: Path, dst: Path):
    if not src.exists():
        print(f"🟡 跳过缺失文件: {src}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main():
    if not SRC_BOT.exists():
        print(f"🔴 找不到源文件: {SRC_BOT}")
        sys.exit(1)

    version = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_dir = OUTPUT_BASE / f"龍智守_v2.0_{version}"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. 核心脚本
    copy_file(SRC_BOT, out_dir / "龍智守_本地控制接口_v2.0.py")

    # 2. 示例配置
    copy_file(SRC_CONFIG_EXAMPLE, out_dir / "龍智守_config.example.json")

    # 3. 国密工具（bot 和优化器都会从 ~ 目录导入）
    copy_file(SRC_GUOMI, out_dir / "CNSH_国密工具.py")

    # 4. 依赖模块
    deps_dir = out_dir / "longhun-system_scripts"
    for name in REQUIRED_SCRIPT_MODULES:
        copy_file(SRC_SCRIPTS_DIR / name, deps_dir / name)

    # 5. 训练数据优化器（bot 里写死路径 ~/Downloads/Kimi_Agent_龍魂训练协议/...）
    optimizer_dst_dir = out_dir / "Kimi_Agent_龍魂训练协议"
    for name in REQUIRED_OPTIMIZER_FILES:
        copy_file(SRC_OPTIMIZER_DIR / name, optimizer_dst_dir / name)

    # 6. Python 依赖
    (out_dir / "requirements.txt").write_text(
        "flask>=2.0\n",
        encoding="utf-8",
    )

    # 7. 环境变量示例
    (out_dir / ".env.example").write_text(
        "# 龍智守运行环境变量（复制为 .env 并填入真实值，或直接在服务器上 export）\n"
        "LONGHUN_MASTER_KEY=your_16byte_hex_key\n"
        "FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/your_token\n"
        "FEISHU_WEBHOOK_SECRET=your_secret\n"
        "FEISHU_APP_ID=cli_xxx\n"
        "FEISHU_APP_SECRET=xxx\n"
        "FEISHU_VERIFICATION_TOKEN=xxx\n"
        "FEISHU_ENCRYPT_KEY=xxx\n"
        "LONGHUN_FOUNDER_FEISHU_OPENID=ou_xxx\n",
        encoding="utf-8",
    )

    # 8. systemd 服务模板
    service_content = """[Unit]
Description=龍智守本地控制接口 v2.0
After=network.target

[Service]
Type=simple
User=longzhishou
Group=longzhishou
WorkingDirectory=/opt/longzhishou
Environment=PYTHONUNBUFFERED=1
# 配置和密钥放在 longzhishou 用户主目录下
Environment=HOME=/home/longzhishou
ExecStart=/usr/bin/python3 /opt/longzhishou/龍智守_本地控制接口_v2.0.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
"""
    (out_dir / "龍智守.service").write_text(service_content, encoding="utf-8")

    # 9. Nginx 反向代理模板（HTTPS 占位）
    nginx_content = """server {
    listen 80;
    server_name YOUR_DOMAIN;

    # Let's Encrypt 验证
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# 申请证书后取消注释并替换 YOUR_DOMAIN
# server {
#     listen 443 ssl http2;
#     server_name YOUR_DOMAIN;
#     ssl_certificate /etc/letsencrypt/live/YOUR_DOMAIN/fullchain.pem;
#     ssl_certificate_key /etc/letsencrypt/live/YOUR_DOMAIN/privkey.pem;
#     location / {
#         proxy_pass http://127.0.0.1:5000;
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;
#     }
# }
"""
    (out_dir / "nginx_longzhishou.conf").write_text(nginx_content, encoding="utf-8")

    # 10. 安装脚本
    install_sh = r"""#!/bin/bash
# 龍智守 v2.0 华为服务器一键部署脚本
# 适用：systemd + nginx 的 Linux 发行版（openEuler/Ubuntu/CentOS 等）
set -e

INSTALL_DIR="/opt/longzhishou"
USER="longzhishou"
HOME_DIR="/home/longzhishou"
DOMAIN="${1:-}"

echo "🐉 开始部署龍智守到华为服务器..."

# 1. 安装基础依赖
if command -v apt-get &> /dev/null; then
    apt-get update
    apt-get install -y python3 python3-pip python3-venv nginx curl ufw
elif command -v yum &> /dev/null; then
    yum install -y python3 python3-pip nginx curl firewalld
elif command -v dnf &> /dev/null; then
    dnf install -y python3 python3-pip nginx curl firewalld
else
    echo "🟡 未检测到 apt/yum/dnf，请手动安装 python3、pip、nginx"
fi

# 2. 创建运行用户
if ! id "$USER" &> /dev/null; then
    useradd -r -m -s /bin/bash "$USER"
    echo "🟢 创建用户 $USER"
fi

# 3. 复制程序文件
mkdir -p "$INSTALL_DIR"
cp -r . "$INSTALL_DIR/"
chown -R "$USER:$USER" "$INSTALL_DIR"

# 4. 创建 longzhishou 用户主目录下的依赖目录
mkdir -p "$HOME_DIR/longhun-system/scripts"
mkdir -p "$HOME_DIR/Downloads/Kimi_Agent_龍魂训练协议"
mkdir -p "$HOME_DIR/.longhun/config"
mkdir -p "$HOME_DIR/.longhun/logs"
mkdir -p "$HOME_DIR/.龍魂"

# 5. 放置依赖模块和优化器（bot 写死了这些路径）
cp "$INSTALL_DIR/CNSH_国密工具.py" "$HOME_DIR/CNSH_国密工具.py"
cp "$INSTALL_DIR/longhun-system_scripts/"*.py "$HOME_DIR/longhun-system/scripts/"
cp "$INSTALL_DIR/Kimi_Agent_龍魂训练协议/"*.py "$HOME_DIR/Downloads/Kimi_Agent_龍魂训练协议/"
chown -R "$USER:$USER" "$HOME_DIR"

# 6. 安装 Python 依赖
python3 -m pip install -r "$INSTALL_DIR/requirements.txt"

# 7. 生成主密钥（如果不存在）
if [ ! -f "$HOME_DIR/.longhun/config/.master_key" ]; then
    python3 -c "import os; print(os.urandom(16).hex())" > "$HOME_DIR/.longhun/config/.master_key"
    chown "$USER:$USER" "$HOME_DIR/.longhun/config/.master_key"
    chmod 600 "$HOME_DIR/.longhun/config/.master_key"
    echo "🟢 已生成 .master_key"
fi

# 8. 提示配置
if [ ! -f "$HOME_DIR/.longhun/config/龍智守_config.json" ]; then
    cp "$INSTALL_DIR/龍智守_config.example.json" "$HOME_DIR/.longhun/config/龍智守_config.json"
    chown "$USER:$USER" "$HOME_DIR/.longhun/config/龍智守_config.json"
    echo "🟡 请编辑 $HOME_DIR/.longhun/config/龍智守_config.json 填入飞书凭据"
fi

# 9. 安装 systemd 服务
if command -v systemctl &> /dev/null; then
    cp "$INSTALL_DIR/龍智守.service" /etc/systemd/system/龍智守.service
    systemctl daemon-reload
    systemctl enable 龍智守
    echo "🟢 systemd 服务已安装"
fi

# 10. 安装 Nginx 配置
if command -v nginx &> /dev/null; then
    NGINX_CONF_DST="/etc/nginx/conf.d/longzhishou.conf"
    if [ -d /etc/nginx/sites-available ]; then
        NGINX_CONF_DST="/etc/nginx/sites-available/longzhishou"
    fi
    cp "$INSTALL_DIR/nginx_longzhishou.conf" "$NGINX_CONF_DST"
    if [ -n "$DOMAIN" ]; then
        sed -i "s/YOUR_DOMAIN/$DOMAIN/g" "$NGINX_CONF_DST"
        mkdir -p /var/www/certbot
    fi
    # 软链（Debian/Ubuntu 风格）
    if [ -d /etc/nginx/sites-enabled ]; then
        ln -sf /etc/nginx/sites-available/longzhishou /etc/nginx/sites-enabled/longzhishou
    fi
    nginx -t && systemctl reload nginx || echo "🟡 Nginx 配置需要手动检查"
fi

# 11. 防火墙放行
if command -v ufw &> /dev/null; then
    ufw allow 80/tcp
    ufw allow 443/tcp
    echo "🟢 ufw 已放行 80/443"
elif command -v firewall-cmd &> /dev/null; then
    firewall-cmd --permanent --add-service=http
    firewall-cmd --permanent --add-service=https
    firewall-cmd --reload
    echo "🟢 firewalld 已放行 80/443"
fi

echo ""
echo "🐉 部署完成。后续步骤："
echo "   1. 编辑配置： sudo nano $HOME_DIR/.longhun/config/龍智守_config.json"
echo "      必填：飞书Webhook地址/密钥、飞书AppID/AppSecret/VerificationToken/EncryptKey、创始人飞书OpenID"
echo "   2. 加密敏感配置： sudo -u $USER python3 $INSTALL_DIR/龍智守_本地控制接口_v2.0.py 加密配置"
echo "   3. 启动服务：     sudo systemctl start 龍智守"
echo "   4. 查看日志：     sudo journalctl -u 龍智守 -f"
echo ""
CALLBACK_URL="https://YOUR_DOMAIN/webhook"
if [ -n "$DOMAIN" ]; then
    CALLBACK_URL="https://$DOMAIN/webhook"
fi
echo "   飞书后台需要配置："
echo "      - 回调 URL：$CALLBACK_URL"
echo "      - 订阅事件：im.message.receive_v1"
echo "      - 权限：im:message、im:message.group_at_msg"
echo ""
echo "DNA: #龍芯⚡️2026-06-30-LONGZHISHOU-PACKAGER-v2.1"
"""
    (out_dir / "install.sh").write_text(install_sh, encoding="utf-8")
    os.chmod(out_dir / "install.sh", 0o755)

    # 11. README
    readme = """# 🐉 龍智守 v2.0 华为服务器部署包

## 包里有什么

- `龍智守_本地控制接口_v2.0.py` —— 主程序
- `龍智守_config.example.json` —— 配置模板（可公开）
- `CNSH_国密工具.py` —— 国密 SM3/SM4 依赖
- `longhun-system_scripts/` —— bot 运行依赖的龍魂模块
- `Kimi_Agent_龍魂训练协议/` —— 训练数据优化器
- `requirements.txt` —— Python 依赖
- `.env.example` —— 环境变量模板
- `龍智守.service` —— systemd 服务模板
- `nginx_longzhishou.conf` —— Nginx 反向代理模板
- `install.sh` —— 一键安装脚本

## 快速部署

把本目录上传到华为服务器，然后执行：

```bash
cd 龍智守_v2.0_*
sudo ./install.sh
```

如果你已经有域名，可以带域名参数：

```bash
sudo ./install.sh your-domain.com
```

## 配置说明

1. 编辑真实配置文件：
   ```bash
   sudo nano /home/longzhishou/.longhun/config/龍智守_config.json
   ```

2. 必填项：
   - `创始人标识` / `机器人DNA`
   - `飞书Webhook地址` / `飞书Webhook密钥`
   - `飞书AppID` / `飞书AppSecret`
   - `飞书VerificationToken` / `飞书EncryptKey`
   - `创始人飞书OpenID`

3. 加密敏感配置：
   ```bash
   sudo -u longzhishou python3 /opt/longzhishou/龍智守_本地控制接口_v2.0.py 加密配置
   ```

4. 启动/查看服务：
   ```bash
   sudo systemctl start 龍智守
   sudo systemctl status 龍智守
   sudo journalctl -u 龍智守 -f
   ```

## 飞书后台配置

1. 创建企业自建应用，添加「机器人」能力。
2. 事件订阅 → 请求方式 Webhook → 填入 `https://你的域名/webhook`。
3. 添加订阅事件 `im.message.receive_v1`。
4. 权限管理里开通 `im:message`、`im:message.group_at_msg`。
5. 把 Verification Token 和 Encrypt Key 填回服务器配置文件。
6. 获取创始人自己的 open_id（第一次发消息时机器人会返回），填到 `创始人飞书OpenID`。

## 安全提醒

- 不要把 `~/.longhun/config/` 和 `~/.龍魂/` 提交到 git。
- 不要把 `.master_key` 发给任何人。
- 生产环境必须配置 HTTPS。
"""
    (out_dir / "README.md").write_text(readme, encoding="utf-8")

    # 12. 打包成 tar.gz
    tar_path = Path(str(out_dir) + ".tar.gz")
    shutil.make_archive(str(out_dir), "gztar", root_dir=str(out_dir.parent), base_dir=out_dir.name)

    # 13. 生成排除清单
    (out_dir / ".打包排除清单.txt").write_text(
        "以下文件/目录不应出现在公开发行包中：\n"
        "- ~/.longhun/config/龍智守_config.json\n"
        "- ~/.longhun/config/.master_key\n"
        "- ~/.longhun/evaluation/\n"
        "- ~/.longhun/memory/\n"
        "- ~/.龍魂/authorized_users.json\n"
        "- ~/.龍魂/longzhishou_tokens.json\n",
        encoding="utf-8",
    )

    print(f"🟢 打包完成: {out_dir}")
    print(f"   核心脚本: {out_dir / '龍智守_本地控制接口_v2.0.py'}")
    print(f"   示例配置: {out_dir / '龍智守_config.example.json'}")
    print(f"   安装脚本: {out_dir / 'install.sh'}")
    print(f"   部署压缩包: {tar_path}")


if __name__ == "__main__":
    main()

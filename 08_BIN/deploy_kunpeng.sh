#!/bin/bash
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·戊午·午时·䷐随-CNSH-IDE-DEPLOY-KUNPENG-v2.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#
# 🐉 CNSH IDE · 鲲鹏服务器一键部署脚本 v2.0
#
# v2.0 修复（2026-08-12，UID9622 实测）:
#   1. 不再 rsync 整个 longhun-system 仓库（原版会把 models/ 等 GB 级文件全传上去）
#      改为只传 CNSH IDE 运行所需的最小文件集
#   2. 架构自适应：原版写死 ARM64，实测鲲鹏是 x86_64（Ollama install.sh 本身自动适配架构）
#   3. 模型默认 qwen2.5:1.5b（服务器上通常已有，零下载零腾空间），可用 MODEL 环境变量覆盖
#   4. 端口默认 8850（避开服务器已占用端口），可用 PORT 环境变量覆盖
#   5. 支持 SSH key 认证（SSH_KEY 环境变量）
#
# 用法：
#   SSH_KEY=~/.ssh/longhun_kunpeng_ed25519 ./deploy_kunpeng.sh root@119.13.90.27 /opt/cnsh-ide
#   MODEL=qwen2.5:1.5b PORT=8850 ./deploy_kunpeng.sh root@119.13.90.27
#

set -euo pipefail

REMOTE="${1:-}"
REMOTE_DIR="${2:-/opt/cnsh-ide}"
LOCAL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
MODEL="${MODEL:-qwen2.5:1.5b}"
PORT="${PORT:-8850}"
SSH_KEY="${SSH_KEY:-}"

# SSH 命令封装（支持 key 认证）
ssh_cmd() {
    if [ -n "$SSH_KEY" ]; then
        ssh -i "$SSH_KEY" -o ConnectTimeout=10 -o StrictHostKeyChecking=no "$@"
    else
        ssh -o ConnectTimeout=10 "$@"
    fi
}

if [ -z "$REMOTE" ]; then
    echo "❌ 用法: $0 [服务器用户@IP] [部署目录]"
    echo "   示例: SSH_KEY=~/.ssh/longhun_kunpeng_ed25519 $0 root@119.13.90.27 /opt/cnsh-ide"
    exit 1
fi

echo "🐉 开始部署 CNSH IDE 到服务器: $REMOTE"
echo "   远程目录: $REMOTE_DIR"
echo "   本地模型: $MODEL (本地服务拉取/复用)"
echo "   服务端口: $PORT"

# ═══════════════════════════════════════════════════════
# 1. 上传最小文件集（只传 IDE 必需，绝不整仓）
# ═══════════════════════════════════════════════════════
FILES=(
    "08_BIN/cnsh_web_ide.py"
    "08_BIN/cnsh_editor.py"
    "08_BIN/cnsh_compiler.py"
    "08_BIN/cnsh_ui.py"
    "08_BIN/cnsh_ai_providers.py"
    "container/requirements.txt"
)
echo ""
echo "📦 1/6 上传最小文件集 ($(echo ${#FILES[@]}) 个文件)..."
ssh_cmd "$REMOTE" "mkdir -p $REMOTE_DIR/08_BIN $REMOTE_DIR/container $REMOTE_DIR/cnsh_projects"
for f in "${FILES[@]}"; do
    if [ -f "$LOCAL_DIR/$f" ]; then
        ssh_cmd "$REMOTE" "mkdir -p $REMOTE_DIR/$(dirname "$f")"
        scp ${SSH_KEY:+-i "$SSH_KEY"} -o ConnectTimeout=10 -o StrictHostKeyChecking=no \
            "$LOCAL_DIR/$f" "$REMOTE:$REMOTE_DIR/$f"
        echo "   ✅ $f"
    else
        echo "   ⚠️ 缺失: $f"
    fi
done

# ═══════════════════════════════════════════════════════
# 2. 检查 Python 环境（不重复安装）
# ═══════════════════════════════════════════════════════
echo ""
echo "🔧 2/6 检查 Python 环境..."
ssh_cmd "$REMOTE" "bash -s" <<REMOTE_SCRIPT
set -e
if command -v python3 >/dev/null 2>&1; then
    echo "✅ python3: \$(python3 --version)"
else
    echo "❌ 无 python3，安装中..."
    if command -v apt-get >/dev/null 2>&1; then
        apt-get update && apt-get install -y python3 python3-pip python3-venv
    else
        echo "⚠️ 无 apt，请手动安装 python3"
        exit 1
    fi
fi
REMOTE_SCRIPT

# ═══════════════════════════════════════════════════════
# 3. 检查/安装 Ollama（架构自动适配）
# ═══════════════════════════════════════════════════════
echo ""
echo "🧠 3/6 检查 Ollama..."
ssh_cmd "$REMOTE" "bash -s" <<'REMOTE_SCRIPT'
set -e
ARCH=$(uname -m)
echo "   架构: $ARCH"
if command -v ollama >/dev/null 2>&1; then
    echo "✅ Ollama 已安装: $(ollama --version 2>/dev/null || echo ok)"
else
    echo "⬇️ 安装 Ollama ($ARCH)..."
    curl -fsSL https://ollama.com/install.sh | sh
fi
if ! curl -s --max-time 3 http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
    echo "🚀 启动 Ollama 服务..."
    nohup ollama serve >/tmp/ollama.log 2>&1 &
    sleep 4
fi
echo "✅ Ollama API 就绪"
REMOTE_SCRIPT

# ═══════════════════════════════════════════════════════
# 4. 确保模型可用（已有则复用，没有才拉取）
# ═══════════════════════════════════════════════════════
echo ""
echo "📥 4/6 检查模型: $MODEL ..."
ssh_cmd "$REMOTE" "bash -s" <<REMOTE_SCRIPT
set -e
MODEL="$MODEL"
if curl -s --max-time 3 http://127.0.0.1:11434/api/tags | grep -q "$MODEL"; then
    echo "✅ 模型已存在: $MODEL"
else
    echo "⬇️ 拉取模型: $MODEL (首次约需几分钟)..."
    ollama pull "$MODEL"
fi
REMOTE_SCRIPT

# ═══════════════════════════════════════════════════════
# 5. 安装 Python 依赖
# ═══════════════════════════════════════════════════════
echo ""
echo "🐍 5/6 安装 Python 依赖..."
ssh_cmd "$REMOTE" "bash -s" <<REMOTE_SCRIPT
set -e
cd $REMOTE_DIR
if [ ! -d .venv ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip -q
pip install -r container/requirements.txt -q
echo "✅ 依赖安装完成"
REMOTE_SCRIPT

# ═══════════════════════════════════════════════════════
# 6. 配置并启动 CNSH IDE
# ═══════════════════════════════════════════════════════
echo ""
echo "🚀 6/6 配置并启动 CNSH IDE..."
ssh_cmd "$REMOTE" "bash -s" <<REMOTE_SCRIPT
set -e
cd $REMOTE_DIR
mkdir -p ~/.cnsh

# 写入本地模型默认配置
cat > ~/.cnsh/ai_config.json <<EOF
{
  "default": "local",
  "providers": {
    "local": {
      "api_key": "",
      "model": "$MODEL",
      "enabled": true
    }
  }
}
EOF
chmod 600 ~/.cnsh/ai_config.json

# 创建 systemd 服务（可选）
if command -v systemctl >/dev/null 2>&1; then
    cat > /etc/systemd/system/cnsh-ide.service <<EOF
[Unit]
Description=CNSH Web IDE
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$REMOTE_DIR
Environment=PATH=$REMOTE_DIR/.venv/bin
ExecStart=$REMOTE_DIR/.venv/bin/python3 08_BIN/cnsh_web_ide.py --host 0.0.0.0 --port $PORT --project $REMOTE_DIR/cnsh_projects
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
    systemctl daemon-reload
    systemctl enable cnsh-ide.service
    systemctl restart cnsh-ide.service
    echo "✅ CNSH IDE 已通过 systemd 启动"
    echo "   访问: http://$(hostname -I | awk '{print $1}'):$PORT"
else
    echo "⚠️ 无 systemd，以后台进程启动..."
    nohup $REMOTE_DIR/.venv/bin/python3 08_BIN/cnsh_web_ide.py --host 0.0.0.0 --port $PORT --project $REMOTE_DIR/cnsh_projects >/tmp/cnsh-ide.log 2>&1 &
    echo "✅ CNSH IDE 已后台启动"
    echo "   日志: /tmp/cnsh-ide.log"
fi
sleep 3
echo "--- 验证 ---"
curl -s --max-time 10 "http://127.0.0.1:$PORT/api/ai/providers" | head -c 400 || echo "⚠️ 启动验证失败，看日志: tail -50 /tmp/cnsh-ide.log"
REMOTE_SCRIPT

echo ""
echo "═══════════════════════════════════════════════════════"
echo "🐉 CNSH IDE 鲲鹏部署完成 (v2.0)"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "访问地址: http://119.13.90.27:$PORT"
echo "模型: $MODEL | 端口: $PORT | 目录: $REMOTE_DIR"
echo ""

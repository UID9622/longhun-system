# DNA: #龍芯⚡️丙午·壬辰·乙亥·壬午·䷚颐-SYNC-COMPLIANCE-20260827-7A2C9F3D
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# ============================================
# 龍魂官网 · 鲲鹏算力中心配置脚本
# 执行环境：华为鲲鹏 + OpenEuler + Ollama
# ============================================

set -e

WEB_ROOT="/var/www/longhun"

echo "[龍魂] 开始配置鲲鹏算力中心..."

# 1. 安装 nginx（如未安装）
if ! command -v nginx &> /dev/null; then
    echo "[龍魂] 安装 nginx..."
    dnf install -y nginx || yum install -y nginx
fi

# 2. 创建目录（作为备份和本地测试）
echo "[龍魂] 创建本地网站目录..."
mkdir -p ${WEB_ROOT}/{download,docs}
chmod -R 755 ${WEB_ROOT}

# 3. 检查 Ollama 状态
echo "[龍魂] 检查 Ollama 状态..."
if command -v ollama &> /dev/null; then
    echo "[OK] Ollama 已安装"
    ollama list
else
    echo "[警告] Ollama 未安装，请先安装："
    echo "  curl -fsSL https://ollama.com/install.sh | sh"
fi

# 4. 检查模型
echo "[龍魂] 检查本地模型..."
if ollama list 2>/dev/null | grep -q "longhun"; then
    echo "[OK] longhun 模型已就绪"
else
    echo "[提示] longhun 模型未找到，请确认 fuse 完成"
fi

# 5. 防火墙放行（仅内网或隧道需要）
echo "[龍魂] 配置防火墙..."
if command -v firewall-cmd &> /dev/null; then
    firewall-cmd --permanent --add-port=11434/tcp
    firewall-cmd --reload
fi

# 6. 启动 Ollama 服务
echo "[龍魂] 启动 Ollama..."
systemctl enable ollama 2>/dev/null || true
systemctl start ollama 2>/dev/null || ollama serve &

echo ""
echo "========================================"
echo "[龍魂] 鲲鹏配置完成"
echo "========================================"
echo "Ollama 地址: http://localhost:11434"
echo "模型列表: ollama list"
echo ""
echo "下一步："
echo "1. 确保 WireGuard 隧道已建立到香港节点"
echo "2. 香港节点通过 10.8.0.2:11434 访问本机 Ollama"
echo "3. 本地测试: curl http://localhost:11434/api/tags"
echo "========================================"

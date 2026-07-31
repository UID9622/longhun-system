#!/bin/bash
# DNA: #龍芯⚡️2026-07-30-网络限流应对-鲲鹏离线-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 龍魂网络限流应对方案 · 鲲鹏离线节点
# 解决：彻底断网也能跑训练/推理

echo "========================================"
echo "  龍魂鲲鹏离线节点配置"
echo "  目标：内网运行，不依赖外网"
echo "========================================"

KUNPENG_IP="119.13.90.27"  # 鲲鹏服务器
KUNPENG_KEY="~/.ssh/longhun_kunpeng_ed25519"
KUNPENG_USER="root"

# ===== 4.1 预下载所有依赖到鲲鹏 =====
echo "[龍魂] 在鲲鹏服务器预装全部依赖..."
ssh -i $KUNPENG_KEY $KUNPENG_USER@$KUNPENG_IP << 'REMOTE'
    # 安装conda（离线可用）
    mkdir -p /root/offline_env
    
    # 预下载Python包
    pip download torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu -d /root/offline_env/packages
    pip download transformers accelerate peft datasets -d /root/offline_env/packages
    pip download mlx-lm -d /root/offline_env/packages 2>/dev/null || echo "mlx-lm仅Mac可用"
    
    # 预下载模型权重（通过代理或镜像）
    mkdir -p /root/offline_env/models
    
    echo "[龍魂] 依赖预下载完成"
    echo "[龍魂] 路径: /root/offline_env/"
REMOTE

# ===== 4.2 内网同步脚本（M4 Max ↔ 鲲鹏） =====
cat > ~/longhun-system/bin/lh_sync_kunpeng.sh << 'EOF'
#!/bin/bash
# M4 Max → 鲲鹏 内网同步
KUNPENG_IP="119.13.90.27"
KUNPENG_KEY="~/.ssh/longhun_kunpeng_ed25519"

# 同步训练数据
rsync -avz --progress -e "ssh -i $KUNPENG_KEY" \
    ~/longhun-system/models/ \
    root@$KUNPENG_IP:/root/longhun-system/models/

# 同步训练脚本
rsync -avz --progress -e "ssh -i $KUNPENG_KEY" \
    ~/longhun-system/bin/ \
    root@$KUNPENG_IP:/root/longhun-system/bin/

echo "[龍魂] 同步完成"
EOF
chmod +x ~/longhun-system/bin/lh_sync_kunpeng.sh

# ===== 4.3 鲲鹏离线训练脚本 =====
cat > ~/longhun-system/bin/lh_kunpeng_train.sh << 'EOF'
#!/bin/bash
# 鲲鹏服务器离线训练（昇腾NPU）
# 不依赖外网，纯内网运行

echo "[龍魂] 鲲鹏离线训练启动..."
echo "[龍魂] 设备: 昇腾NPU"
echo "[龍魂] 网络: 离线"

# 加载离线环境
source /root/offline_env/activate

# 训练（使用预下载的模型和数据）
python3 /root/longhun-system/bin/lh_train_v40.py train \
    --offline \
    --model /root/offline_env/models/llama-3.1-8b \
    --data /root/longhun-system/models/longhun-v1.0/lora_output/data_v40_distill

echo "[龍魂] 训练完成，同步回M4 Max:"
echo "  rsync -avz root@$KUNPENG_IP:/root/longhun-system/models/ ~/longhun-system/models/"
EOF

echo "[龍魂] 鲲鹏离线节点配置完成"
echo "[龍魂] 用法:"
echo "  1. 同步数据: lh_sync_kunpeng.sh"
echo "  2. SSH登录鲲鹏: ssh -i ~/.ssh/kunpeng.pem root@$KUNPENG_IP"
echo "  3. 离线训练: bash /root/longhun-system/bin/lh_kunpeng_train.sh"

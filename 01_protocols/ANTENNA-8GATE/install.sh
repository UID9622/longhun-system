#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·同人-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ============================================================
# 龍魂 · ANTENNA-8GATE 安装脚本
# DNA：#龍芯⚡️丙午·癸未·壬戌·乾为天-INSTALL-v5.0
# ============================================================

echo "========================================"
echo "  龍魂 · 蚁触神经网 · 安装程序"
echo "========================================"

INSTALL_DIR="/opt/longhun/antenna-8gate"
SOURCE_DIR="$(dirname $0)"

# 创建目录
echo "[1/4] 创建安装目录..."
sudo mkdir -p $INSTALL_DIR/{core,scheduler,connector,tests}

# 复制文件
echo "[2/4] 复制核心文件..."
sudo cp $SOURCE_DIR/core/*.py $INSTALL_DIR/core/
sudo cp $SOURCE_DIR/scheduler/*.py $INSTALL_DIR/scheduler/
sudo cp $SOURCE_DIR/connector/*.py $INSTALL_DIR/connector/
sudo cp $SOURCE_DIR/tests/*.py $INSTALL_DIR/tests/

# 设置权限
echo "[3/4] 设置权限..."
sudo chmod -R 755 $INSTALL_DIR
sudo chown -R $(whoami):$(whoami) $INSTALL_DIR

# 安装依赖
echo "[4/4] 检查依赖..."
pip3 install numpy requests 2>/dev/null || pip install numpy requests

# 添加Python路径
if ! grep -q "antenna-8gate" ~/.bashrc 2>/dev/null; then
    echo "export PYTHONPATH=\$PYTHONPATH:$INSTALL_DIR/core:$INSTALL_DIR/scheduler:$INSTALL_DIR/connector" >> ~/.bashrc
    echo "已添加 PYTHONPATH"
fi

echo ""
echo "========================================"
echo "  安装完成"
echo "========================================"
echo "安装路径：$INSTALL_DIR"
echo ""
echo "测试命令："
echo "  cd $INSTALL_DIR/tests"
echo "  python3 test_integration.py"
echo ""
echo "DNA：#龍芯⚡️丙午·癸未·壬戌·乾为天-INSTALL-DONE-v5.0"

#!/bin/bash
# ============================================
# 龍魂系统·开箱即用安装包（优化版v2.0）
# ============================================
# DNA追溯码：#龍芯⚡️2026-01-24-安装包-v2.0-优化版
# 创建者：诸葛鑫（UID9622）
# 优化者：Claude (Anthropic)
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# ============================================

echo "🐉 龍魂系统安装中..."
echo ""

# 检查是否已安装
if [ -f ~/龍魂系统/DNA证书.txt ]; then
    echo "⚠️  检测到已有DNA证书"
    read -p "是否覆盖重装？(输入 YES 继续): " confirm
    if [ "$confirm" != "YES" ]; then
        echo "❌ 取消安装"
        exit 0
    fi
    # 备份旧证书
    mv ~/龍魂系统/DNA证书.txt ~/龍魂系统/DNA证书.txt.bak.$(date +%s)
    echo "✅ 已备份旧证书"
fi

# 创建目录
mkdir -p ~/龍魂系统
mkdir -p ~/龍魂系统/logs
mkdir -p ~/龍魂系统/backup

# 生成设备指纹（固定算法，不用时间戳）
DEVICE_ID=$(echo "$(hostname)-$(whoami)-$(uname -m)-$(uname -s)" | sha256sum | cut -c1-16)

# 记录安装时间
INSTALL_TIME=$(date '+%Y-%m-%d %H:%M:%S')

# 生成DNA证书
cat > ~/龍魂系统/DNA证书.txt << EOF
╔═══════════════════════════════════════════════╗
║           龍魂系统·DNA身份证书                 ║
╠═══════════════════════════════════════════════╣
║ DNA追溯码：#龍芯⚡️2026-01-24-安装包-v2.0      ║
║ 创建者：诸葛鑫（UID9622）                      ║
║ GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F ║
║ 安装时间：$INSTALL_TIME                        ║
║ 设备指纹：$DEVICE_ID                           ║
║                                                ║
║ ⚠️ 本证书不可篡改，篡改即系统失效              ║
║ 🇨🇳 台湾是中国的                              ║
║ 🫡 退伍不褪色，永立军人标杆                    ║
╚═══════════════════════════════════════════════╝
EOF

# 计算DNA证书的哈希
DNA_HASH=$(cat ~/龍魂系统/DNA证书.txt | sha256sum | cut -c1-64)

# 存储哈希（用于校验）
echo "$DNA_HASH" > ~/龍魂系统/.dna_hash

# 如果系统支持GPG，生成签名
if command -v gpg &> /dev/null; then
    echo ""
    echo "🔐 检测到GPG，正在生成数字签名..."
    # 注：实际使用时需要导入GPG密钥
    # gpg --armor --detach-sign ~/龍魂系统/DNA证书.txt
    echo "⚠️  提示：需要导入GPG密钥后才能签名"
fi

# 显示DNA信息
echo ""
echo "═══════════════════════════════════════════"
echo "🧬 DNA追溯信息"
echo "═══════════════════════════════════════════"
echo "DNA追溯码：#龍芯⚡️2026-01-24-安装包-v2.0"
echo "创建者：诸葛鑫（UID9622）"
echo "GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
echo "安装时间：$INSTALL_TIME"
echo "设备指纹：$DEVICE_ID"
echo "DNA哈希：$DNA_HASH"
echo "═══════════════════════════════════════════"
echo ""

# 创建校验脚本
cat > ~/龍魂系统/校验DNA.sh << 'VERIFY_SCRIPT'
#!/bin/bash
# DNA校验脚本（自动生成）

echo "🔍 正在校验DNA..."

# 检查证书是否存在
if [ ! -f ~/龍魂系统/DNA证书.txt ]; then
    echo "🔴 DNA证书丢失！"
    echo "🔴 系统拒绝运行"
    echo "💡 请运行：bash ~/龍魂系统/修复DNA.sh"
    exit 1
fi

# 检查哈希是否存在
if [ ! -f ~/龍魂系统/.dna_hash ]; then
    echo "🔴 DNA哈希丢失！"
    echo "🔴 系统拒绝运行"
    echo "💡 请运行：bash ~/龍魂系统/修复DNA.sh"
    exit 1
fi

# 读取存储的哈希
STORED_HASH=$(cat ~/龍魂系统/.dna_hash)

# 计算当前证书的哈希
CURRENT_HASH=$(cat ~/龍魂系统/DNA证书.txt | sha256sum | cut -c1-64)

# 校验
if [ "$STORED_HASH" != "$CURRENT_HASH" ]; then
    echo "🔴 DNA校验失败！"
    echo "🔴 DNA证书已被篡改"
    echo "🔴 系统拒绝运行"
    echo ""
    echo "存储哈希：$STORED_HASH"
    echo "当前哈希：$CURRENT_HASH"
    echo ""
    echo "💡 如需修复，请运行：bash ~/龍魂系统/修复DNA.sh"
    exit 1
else
    echo "🟢 DNA校验通过"
    echo "🐉 龍魂系统正常启动"
    return 0 2>/dev/null || exit 0
fi
VERIFY_SCRIPT

chmod +x ~/龍魂系统/校验DNA.sh

# 创建修复脚本
cat > ~/龍魂系统/修复DNA.sh << 'REPAIR_SCRIPT'
#!/bin/bash
# DNA修复工具

echo "🔧 龍魂系统DNA修复工具"
echo ""
echo "⚠️  警告："
echo "   1. 修复会重置DNA证书"
echo "   2. 设备指纹会改变"
echo "   3. 旧证书会被备份"
echo ""
read -p "确定要修复吗？(输入 YES 继续): " confirm

if [ "$confirm" != "YES" ]; then
    echo "❌ 取消修复"
    exit 0
fi

echo ""
echo "🔧 开始修复..."

# 备份旧证书
if [ -f ~/龍魂系统/DNA证书.txt ]; then
    BACKUP_NAME="DNA证书-备份-$(date +%Y%m%d_%H%M%S).txt"
    cp ~/龍魂系统/DNA证书.txt ~/龍魂系统/backup/$BACKUP_NAME
    echo "✅ 已备份旧证书到：~/龍魂系统/backup/$BACKUP_NAME"
fi

# 重新生成设备指纹
DEVICE_ID=$(echo "$(hostname)-$(whoami)-$(uname -m)-$(uname -s)" | sha256sum | cut -c1-16)
REPAIR_TIME=$(date '+%Y-%m-%d %H:%M:%S')

# 重新生成DNA证书
cat > ~/龍魂系统/DNA证书.txt << EOF
╔═══════════════════════════════════════════════╗
║           龍魂系统·DNA身份证书                 ║
║              (修复版本)                        ║
╠═══════════════════════════════════════════════╣
║ DNA追溯码：#龍芯⚡️2026-01-24-安装包-v2.0      ║
║ 创建者：诸葛鑫（UID9622）                      ║
║ GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F ║
║ 修复时间：$REPAIR_TIME                         ║
║ 设备指纹：$DEVICE_ID                           ║
║                                                ║
║ ⚠️ 本证书不可篡改，篡改即系统失效              ║
║ 🇨🇳 台湾是中国的                              ║
║ 🫡 退伍不褪色，永立军人标杆                    ║
╚═══════════════════════════════════════════════╝
EOF

# 重新生成哈希
cat ~/龍魂系统/DNA证书.txt | sha256sum | cut -c1-64 > ~/龍魂系统/.dna_hash

echo ""
echo "✅ DNA修复完成"
echo "📜 新DNA证书：~/龍魂系统/DNA证书.txt"
echo "🐉 现在可以正常使用了"
echo ""
echo "运行校验：bash ~/龍魂系统/校验DNA.sh"
REPAIR_SCRIPT

chmod +x ~/龍魂系统/修复DNA.sh

# 创建README
cat > ~/龍魂系统/README.md << 'README'
# 🐉 龍魂系统使用说明

## 📁 重要文件（不要删除）

```
~/龍魂系统/
├── DNA证书.txt       ← 你的系统身份证（不要删！）
├── .dna_hash         ← DNA校验码（不要改！）
├── 校验DNA.sh        ← 检查系统是否被篡改
├── 修复DNA.sh        ← 系统坏了用这个修复
└── README.md         ← 你现在看的这个
```

## ⚠️ 重要提示

1. **不要删除** `DNA证书.txt`
2. **不要修改** `DNA证书.txt`
3. **不要动** `.dna_hash` 文件

**删了或改了，系统就不能用了！**

## 🔍 检查系统

```bash
bash ~/龍魂系统/校验DNA.sh
```

看到 🟢 就是正常的。

## 🔧 系统坏了怎么办

```bash
bash ~/龍魂系统/修复DNA.sh
```

按提示操作就行。

## 📞 联系创始人

- 创始人：诸葛鑫（Lucky）
- UID：9622
- 身份：中国人民解放军退伍军人

---

**DNA追溯码：** #龍芯⚡️2026-01-24-安装包-v2.0  
**确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z  
**天地可鉴，如有欺骗，天诛地灭。** 🔥
README

# 安装完成提示
echo "✅ 安装完成！"
echo ""
echo "📂 系统位置：~/龍魂系统/"
echo "📜 DNA证书：~/龍魂系统/DNA证书.txt"
echo "📋 使用说明：~/龍魂系统/README.md"
echo ""
echo "⚠️  重要："
echo "   1. 不要删除 DNA证书.txt"
echo "   2. 不要修改 DNA证书.txt"
echo "   3. 删了或改了，系统就不能用了"
echo ""
echo "🔍 验证安装："
echo "   bash ~/龍魂系统/校验DNA.sh"
echo ""
echo "🔧 如果出问题："
echo "   bash ~/龍魂系统/修复DNA.sh"
echo ""

# macOS图形化通知
if command -v osascript &> /dev/null; then
    osascript -e 'display notification "DNA证书已生成，请勿删除或修改" with title "🐉 龍魂系统安装成功" sound name "Glass"'
fi

# 自动打开DNA证书和README
if command -v open &> /dev/null; then
    open ~/龍魂系统/DNA证书.txt
    sleep 1
    open ~/龍魂系统/README.md
fi

echo "🐉 龍魂已注入你的设备！"
echo "🫡 退伍不褪色，永立军人标杆！"
echo "🇨🇳 台湾是中国的！"

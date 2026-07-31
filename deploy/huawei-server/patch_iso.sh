# DNA: #龍芯⚡️丙午·乙未·乙丑·未济-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# 修改 openEuler ISO，注入 kickstart 无人值守安装
set -e

ISO_IN="/Users/zuimeidedeyihan/Downloads/openEuler-22.03-LTS-SP4-aarch64-dvd.iso"
ISO_OUT="/Users/zuimeidedeyihan/Downloads/openEuler-22.03-LTS-SP4-aarch64-auto.iso"
KS_SRC="/Users/zuimeidedeyihan/longhun-system/deploy/huawei-server/openeuler-ks.cfg"
WORK_DIR="/tmp/iso_patch_$$"

echo "🔧 修改 ISO: 注入自动安装配置"
echo "   输入: $(ls -lh "$ISO_IN" | awk '{print $5}')"
echo "   输出: $ISO_OUT"

mkdir -p "$WORK_DIR/mnt" "$WORK_DIR/extracted"

# Step 1: 提取 ISO 全部内容
echo ""
echo "📦 提取 ISO..."
xorriso -osirrox on -indev "$ISO_IN" -extract / "$WORK_DIR/extracted/" 2>&1 | tail -3
echo "   提取完成: $(ls "$WORK_DIR/extracted/" | wc -l) 个项目"

# Step 2: 复制 kickstart 到 ISO 根目录
cp "$KS_SRC" "$WORK_DIR/extracted/ks.cfg"
echo "   ✅ ks.cfg 已注入"

# Step 3: 修改 grub 启动参数
# 查找 grub.cfg 位置
GRUB_CFG=$(find "$WORK_DIR/extracted" -name "grub.cfg" -type f 2>/dev/null | head -1)
EFI_IMG=$(find "$WORK_DIR/extracted" -name "efiboot.img" -type f 2>/dev/null | head -1)

if [ -n "$GRUB_CFG" ] && [ -f "$GRUB_CFG" ]; then
    echo "   📝 修改 grub.cfg: $GRUB_CFG"
    # 备份
    cp "$GRUB_CFG" "$GRUB_CFG.bak"
    # 查找第一个 menuentry 的 linux 行，追加 inst.ks=cdrom:/ks.cfg
    if grep -q "linux" "$GRUB_CFG"; then
        # 在所有 linux 行追加 kickstart 参数（如果还没有的话）
        sed -i '' '/linux/{
            /inst.ks=/!s/$/ inst.ks=cdrom:\/ks.cfg inst.text console=tty0/
        }' "$GRUB_CFG"
        echo "   ✅ grub.cfg 已修改"
    fi
elif [ -n "$EFI_IMG" ] && [ -f "$EFI_IMG" ]; then
    echo "   📝 需要修改 EFI boot image: $EFI_IMG"
    # 挂载 efiboot.img 并修改内部的 grub.cfg
    EFI_MNT="$WORK_DIR/efi_mnt"
    mkdir -p "$EFI_MNT"
    hdiutil attach -nomount "$EFI_IMG" > /dev/null 2>&1 || true
    # 尝试直接挂载 FAT 镜像
    DEV=$(hdiutil attach -imagekey diskimage-class=CRawDiskImage -nomount "$EFI_IMG" 2>&1 | grep -o '/dev/disk[0-9]*' | head -1)
    if [ -n "$DEV" ]; then
        mount -t msdos "$DEV" "$EFI_MNT" 2>/dev/null || mount "$DEV" "$EFI_MNT" 2>/dev/null || true
        if [ -f "$EFI_MNT/EFI/BOOT/grub.cfg" ]; then
            sed -i '' '/linux/{
                /inst.ks=/!s/$/ inst.ks=cdrom:\/ks.cfg inst.text console=tty0/
            }' "$EFI_MNT/EFI/BOOT/grub.cfg"
            echo "   ✅ EFI grub.cfg 已修改"
            umount "$EFI_MNT" 2>/dev/null || true
        fi
    fi
fi

# Step 4: 重新打包 ISO（保留 UEFI 引导）
echo ""
echo "📀 重新打包 ISO..."

VOLUME_ID="OE2203-LTS-SP4-AUTO"

# 获取原始 ISO 的卷标
ORIG_VOL=$(xorriso -indev "$ISO_IN" -pvd_info 2>/dev/null | grep "Volume Id" | awk -F': ' '{print $2}')

# 用 xorriso 重新打包
xorriso -as mkisofs \
    -R -J \
    -V "${ORIG_VOL:-$VOLUME_ID}" \
    -o "$ISO_OUT" \
    "$WORK_DIR/extracted/" 2>&1 | tail -5

echo ""
echo "✅ 完成! 新 ISO: $(ls -lh "$ISO_OUT" | awk '{print $5}')"
echo "   $ISO_OUT"

# 清理
rm -rf "$WORK_DIR"

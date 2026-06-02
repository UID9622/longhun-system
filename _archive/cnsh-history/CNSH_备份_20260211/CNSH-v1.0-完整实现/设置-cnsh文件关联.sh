#!/bin/bash
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码: #龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: 设置-cnsh文件关联.sh | 标记时间: 2026-06-03T07:46:00+0800
# DNA追溯码: #ZHUGEXIN⚡️2026-01-28-CNSH-FILE-ASSOCIATION-v1.0
# CNSH文件格式关联脚本
# 作用：让macOS系统能识别.cnsh文件为文本格式

echo "🇨🇳 CNSH文件格式关联工具"
echo "━━━━━━━━━━━━━━━━━━"

# 创建临时UTI定义文件
UTI_FILE="$HOME/Library/Services/org.cnshfile.uti"

cat > "$UTI_FILE" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>UTExportedTypeDeclarations</key>
    <array>
        <dict>
            <key>UTTypeIdentifier</key>
            <string>org.cnshfile.cnsh</string>
            <key>UTTypeDescription</key>
            <string>CNSH Source Code</string>
            <key>UTTypeConformsTo</key>
            <array>
                <string>public.text</string>
                <string>public.plain-text</string>
                <string>public.source-code</string>
            </array>
            <key>UTTypeTagSpecification</key>
            <dict>
                <key>public.filename-extension</key>
                <array>
                    <string>cnsh</string>
                </array>
            </dict>
        </dict>
    </array>
</dict>
</plist>
EOF

echo "✅ 已创建UTI定义文件"
echo ""
echo "📝 下一步操作："
echo "1. 在Finder中按 ⌘ + G，输入以下路径："
echo "   $UTI_FILE"
echo ""
echo "2. 双击打开该文件（会用系统默认编辑器打开）"
echo "3. 确保文件内容完整，然后保存"
echo "4. 在终端运行以下命令注册文件类型："
echo "   defaults write $HOME/Library/Preferences/.GlobalPreferences LSHandlers -array-add '{\"LSHandlerContentType\":\"org.cnshfile.cnsh\",\"LSHandlerRoleAll\":\"com.apple.TextEdit\"}'"
echo ""
echo "5. 重启Finder（运行：killall Finder）"
echo ""
echo "💡 或者使用快速方案："
echo "   直接右键点击.cnsh文件 → 打开方式 → 文本编辑 → 全部更改"

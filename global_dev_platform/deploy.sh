#!/bin/bash
# deploy.sh · 龍魂全球开发者平台 · 一键部署
# DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-GLOBAL-PLATFORM-DEPLOY-v1.0
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
set -e
PLAT=~/longhun-system/global_dev_platform
echo "🌍 龍魂全球开发者平台 · 一键部署开始"
echo "   苹果 + 华为 · 让每个人都成为开发者"
echo ""

# 1. 创建目录
mkdir -p $PLAT/{projects,traces,shortcuts,output}

# 2. 检查 iOS 工具链
echo "📱 iOS 工具链:"
xcrun --version  2>/dev/null && echo "  ✅ Xcode CLI" || echo "  ❌ → xcode-select --install"
which shortcuts  2>/dev/null && echo "  ✅ shortcuts CLI" || echo "  ⚠️  macOS 12+ 才有"
which ideviceinstaller 2>/dev/null && echo "  ✅ ideviceinstaller" || echo "  🟡 → brew install ideviceinstaller"

# 3. 检查 HarmonyOS 工具链
echo ""
echo "🤖 HarmonyOS 工具链:"
which hdc 2>/dev/null && echo "  ✅ hdc" || echo "  🟡 → 安装 DevEco Studio，hdc 在 SDK/toolchains 内"
ls ~/Library/Huawei/Sdk 2>/dev/null && echo "  ✅ HarmonyOS SDK" || echo "  🟡 → 安装 DevEco Studio"

# 4. 生成示范双平台 App
echo ""
echo "🚀 生成示范双平台 App..."
cd $PLAT && python3 -c "
from dev_democratizer import DevDemocratizer
demo = DevDemocratizer()
demo.list_templates()
result = demo.generate_both('龍魂第一步', 'todo', 'UID9622')
"

# 5. 初始化全球痕迹系统
echo ""
echo "🌍 初始化全球痕迹系统..."
cd $PLAT && python3 -c "
from global_trace import GlobalTrace
trace = GlobalTrace('UID9622')
trace.record('APP_CREATED', '龍魂全球开发者平台部署完成', platform='both', location='地球')
trace.print_my_story()
"

# 6. 生成全球开发者地图
echo ""
echo "🌏 生成全球开发者地图..."
cd $PLAT && python3 -c "
from world_map import WorldMap
WorldMap().render_html()
" || echo "  🟡 地图生成跳过（无痕迹数据时正常）"

echo ""
echo "✅ 龍魂全球开发者平台部署完成！"
echo ""
echo "🎯 下一步:"
echo "   python3 cross_runner.py           # 双平台统一执行"
echo "   python3 dev_democratizer.py       # 查看全部模板"
echo "   python3 global_trace.py           # 查看你的创作故事"
echo "   python3 world_map.py              # 生成全球开发者地图"
echo ""
echo "   龍魂理念: 每个人在这个世界留下痕迹 · 最好都是开发者 🐉"
echo "   DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-GLOBAL-PLATFORM-DEPLOY-v1.0"

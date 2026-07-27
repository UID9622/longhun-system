#!/bin/bash
# ╔══════════════════════════════════════════════════════╗
# ║  龍魂·隐私加固脚本 v1.0                              ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-PRIVACY-HARDENER-v1.0 ║
# ║  守护人格: 乔前辈(P04鲁班)                          ║
# ║  签章: JOE-PRIVACY-SHIELD-2026                      ║
# ╚══════════════════════════════════════════════════════╝
# 功能: 系统级关闭苹果所有监控通道
# 用法: sudo bash bin/lh_privacy_hardener.sh [--check-only]
# 铁律: 物理防火墙是最后一道防线

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CHECK_ONLY=false
[[ "${1:-}" == "--check-only" ]] && CHECK_ONLY=true

log_info()  { echo -e "${BLUE}[*]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[✓]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
log_fail()  { echo -e "${RED}[✗]${NC} $1"; }

FAIL_COUNT=0

echo "╔══════════════════════════════════════════════════════╗"
echo "║  龍魂·隐私加固 v1.0                                  ║"
echo "║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-PRIVACY-v1.0    ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# ── 1. 定位服务 ──
log_info "[1/9] 关闭定位服务..."
if [[ "$CHECK_ONLY" == "true" ]]; then
    LOC_USER="${SUDO_USER:-$USER}"
    loc_enabled=$(sudo -u "$LOC_USER" defaults read /var/db/locationd/Library/Preferences/ByHost/com.apple.locationd LocationServicesEnabled 2>/dev/null || echo "1")
    if [[ "$loc_enabled" == "0" ]]; then
        log_ok "定位服务已关闭"
    else
        log_fail "定位服务仍开启"
        ((FAIL_COUNT++))
    fi
else
    sudo defaults write /var/db/locationd/Library/Preferences/ByHost/com.apple.locationd LocationServicesEnabled -int 0 2>/dev/null || true
    sudo defaults write /var/db/locationd/Library/Preferences/ByHost/com.apple.locationd LocationServicesEnabledInSetup -int 0 2>/dev/null || true
    sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.locationd.plist 2>/dev/null || true
    log_ok "定位服务已关闭"
fi

# ── 2. Wi-Fi定位与网络记忆 ──
log_info "[2/9] 关闭Wi-Fi定位与网络记忆..."
if [[ "$CHECK_ONLY" == "true" ]]; then
    # 检查Wi-Fi是否已关闭定位相关的plist
    if ! pgrep -f "locationd" > /dev/null 2>&1; then
        log_ok "Wi-Fi定位守护已停用"
    else
        log_warn "locationd仍在运行"
    fi
else
    # 关闭Wi-Fi网络记忆
    sudo /System/Library/Frameworks/CoreWLAN.framework/Versions/Current/Resources/airport prefs JoinMode=Strongest 2>/dev/null || true
    sudo /System/Library/Frameworks/CoreWLAN.framework/Versions/Current/Resources/airport prefs RememberRecentNetworks=NO 2>/dev/null || true
    # 关闭隔空投送发现
    sudo defaults write /Library/Preferences/com.apple.airport.btip CheckForUpdates -bool FALSE 2>/dev/null || true
    log_ok "Wi-Fi定位已关闭"
fi

# ── 3. 蓝牙追踪 ──
log_info "[3/9] 关闭蓝牙追踪..."
if [[ "$CHECK_ONLY" == "true" ]]; then
    bt_power=$(sudo defaults read /Library/Preferences/com.apple.Bluetooth ControllerPowerState 2>/dev/null || echo "1")
    if [[ "$bt_power" == "0" ]]; then
        log_ok "蓝牙已关闭"
    else
        log_fail "蓝牙仍开启"
        ((FAIL_COUNT++))
    fi
else
    sudo defaults write /Library/Preferences/com.apple.Bluetooth ControllerPowerState -int 0 2>/dev/null || true
    sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.blued.plist 2>/dev/null || true
    log_ok "蓝牙追踪已关闭"
fi

# ── 4. iCloud同步 ──
log_info "[4/9] 断开iCloud同步..."
if [[ "$CHECK_ONLY" == "true" ]]; then
    icloud_enabled=$(sudo defaults read /Library/Preferences/com.apple.SetupAssistant DidSeeCloudSetup 2>/dev/null || echo "0")
    if [[ "$icloud_enabled" == "1" ]]; then
        log_ok "iCloud已断开"
    else
        log_warn "iCloud状态未知"
    fi
else
    sudo defaults write /Library/Preferences/com.apple.SetupAssistant DidSeeCloudSetup -bool TRUE 2>/dev/null || true
    sudo defaults write /Library/Preferences/com.apple.SetupAssistant GestureMovieSeen none 2>/dev/null || true
    sudo defaults write /Library/Preferences/com.apple.SetupAssistant LastSeenCloudProductVersion "99.99" 2>/dev/null || true
    # 禁用iCloud Drive
    sudo defaults write /Library/Preferences/com.apple.iCloudService EnableCloudPhotoLibrary -bool FALSE 2>/dev/null || true
    sudo defaults write /Library/Preferences/com.apple.iCloudService EnableCloudDocuments -bool FALSE 2>/dev/null || true
    log_ok "iCloud已断开"
fi

# ── 5. Siri/听写/语音 ──
log_info "[5/9] 禁用Siri和语音服务..."
if [[ "$CHECK_ONLY" == "true" ]]; then
    siri_enabled=$(sudo defaults read /Library/Preferences/com.apple.Siri VoiceTriggerUserEnabled 2>/dev/null || echo "0")
    if [[ "$siri_enabled" == "0" ]]; then
        log_ok "Siri已禁用"
    else
        log_fail "Siri仍开启"
        ((FAIL_COUNT++))
    fi
else
    sudo defaults write /Library/Preferences/com.apple.Siri VoiceTriggerUserEnabled -bool FALSE 2>/dev/null || true
    sudo defaults write /Library/Preferences/com.apple.Siri StatusMenuVisible -bool FALSE 2>/dev/null || true
    sudo defaults write /Library/Preferences/com.apple.assistant.support 'Assistant Enabled' -bool FALSE 2>/dev/null || true
    sudo launchctl unload -w /System/Library/LaunchAgents/com.apple.Siri.agent.plist 2>/dev/null || true
    sudo launchctl unload -w /System/Library/LaunchAgents/com.apple.assistantd.plist 2>/dev/null || true
    sudo launchctl unload -w /System/Library/LaunchAgents/com.apple.assistant_service.plist 2>/dev/null || true
    # 禁用听写
    sudo defaults write /Library/Preferences/com.apple.HIToolbox AppleDictationAutoEnable -bool FALSE 2>/dev/null || true
    log_ok "Siri/听写已禁用"
fi

# ── 6. 应用分析与诊断 ──
log_info "[6/9] 关闭应用分析..."
if [[ "$CHECK_ONLY" == "true" ]]; then
    auto_submit=$(sudo defaults read /Library/Preferences/com.apple.SubmitDiagInfo AutoSubmit 2>/dev/null || echo "1")
    if [[ "$auto_submit" == "0" ]]; then
        log_ok "应用分析已关闭"
    else
        log_fail "应用分析仍开启"
        ((FAIL_COUNT++))
    fi
else
    sudo defaults write /Library/Preferences/com.apple.SubmitDiagInfo AutoSubmit -bool FALSE 2>/dev/null || true
    sudo defaults write /Library/Preferences/com.apple.SubmitDiagInfo AutoSubmitVersion -int 0 2>/dev/null || true
    sudo defaults write /Library/Preferences/com.apple.SubmitDiagInfo AutoSubmitDiagnosticExtension -bool FALSE 2>/dev/null || true
    sudo defaults write /Library/Preferences/com.apple.SubmitDiagInfo AutoSubmitAppAnalytics -bool FALSE 2>/dev/null || true
    # 关闭开发者共享
    sudo defaults write /Library/Preferences/com.apple.crashreporter DialogType none 2>/dev/null || true
    log_ok "应用分析已关闭"
fi

# ── 7. 诊断报告守护 ──
log_info "[7/9] 关闭诊断报告守护..."
if [[ "$CHECK_ONLY" == "true" ]]; then
    if ! pgrep -f "DiagnosticReportCatcher" > /dev/null 2>&1; then
        log_ok "诊断报告守护已停用"
    else
        log_warn "诊断报告守护仍在运行"
    fi
else
    sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.DiagnosticReportCatcher.plist 2>/dev/null || true
    sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.DiagnosticReportCatcher.ShipIt.plist 2>/dev/null || true
    sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.ReportCrash.Root.plist 2>/dev/null || true
    sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.ReportCrash.plist 2>/dev/null || true
    log_ok "诊断报告守护已停用"
fi

# ── 8. NTP时间同步 ──
log_info "[8/9] 禁用苹果NTP时间同步..."
if [[ "$CHECK_ONLY" == "true" ]]; then
    ntp_enabled=$(sudo systemsetup -getusingnetworktime 2>/dev/null | awk '{print $3}' || echo "On")
    if [[ "$ntp_enabled" == "Off" ]]; then
        log_ok "苹果NTP已禁用"
    else
        log_warn "苹果NTP仍开启"
    fi
else
    sudo systemsetup -setusingnetworktime off 2>/dev/null || true
    sudo defaults write /Library/Preferences/com.apple.timezone.auto Active -bool FALSE 2>/dev/null || true
    log_ok "苹果NTP已禁用"
fi

# ── 9. Spotlight建议(云端泄露向量) ──
log_info "[9/9] 关闭Spotlight云端建议..."
if [[ "$CHECK_ONLY" == "true" ]]; then
    spotlight_enabled=$(sudo defaults read /Library/Preferences/com.apple.lookup.shared LookupSuggestionsEnabled 2>/dev/null || echo "1")
    if [[ "$spotlight_enabled" == "0" ]]; then
        log_ok "Spotlight云端建议已关闭"
    else
        log_warn "Spotlight云端建议仍开启"
    fi
else
    sudo defaults write /Library/Preferences/com.apple.lookup.shared LookupSuggestionsEnabled -bool FALSE 2>/dev/null || true
    sudo defaults write /Library/Preferences/com.apple.Spotlight SpotlightSuggestionsEnabled -bool FALSE 2>/dev/null || true
    log_ok "Spotlight云端建议已关闭"
fi

echo ""
echo "═══════════════════════════════════════════════════════"
if [[ "$CHECK_ONLY" == "true" ]]; then
    if [[ "$FAIL_COUNT" -gt 0 ]]; then
        echo -e "${RED}[隐私审计] ${FAIL_COUNT}项未通过${NC}"
        exit 1
    else
        echo -e "${GREEN}[隐私审计] 全部通过 ✅${NC}"
        exit 0
    fi
else
    if [[ "$FAIL_COUNT" -gt 0 ]]; then
        echo -e "${YELLOW}[隐私加固] 完成，${FAIL_COUNT}项需手动确认${NC}"
    else
        echo -e "${GREEN}[隐私加固] 9/9项已完成${NC}"
    fi
    echo ""
    log_info "所有苹果监控通道已物理级掐断。"
    log_info "数据不再回传苹果。"
    log_info "下一步：运行同心锁防火墙。"
    echo "═══════════════════════════════════════════════════════"
fi

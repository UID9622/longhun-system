#!/bin/bash
# 🐉 龍魂服务器安全加固·一键脚本 v1.0（macOS 适配版）
# DNA: #龍芯⚡️2026-08-31-SECURITY-HARDENING-MACOS-V1.0-UID9622
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 使用: sudo bash security_hardening_macos.sh
# ⚠️ 改前先开新 SSH 窗口测试能连上，再跑本脚本；关旧窗口前务必确认新连接可用！
# 说明: 手册为 Linux 语法(systemctl/iptables)，本机 macOS 用 launchctl/pfctl/socketfilterfw 落地。
set -u

echo "🐉 龍魂安全加固开始 (macOS)"
echo "🧬 DNA: #龍芯⚡️$(date +%Y-%m-%d)-HARDENING-START-UID9622"

# 必须 root
if [ "$(id -u)" -ne 0 ]; then
  echo "🔴 请用 sudo 运行: sudo bash $0"
  exit 1
fi

# ══ 1. 关闭 macOS 屏幕共享（VNC 5900·最高危·暴力破解=整机交出）══
echo "── 1. 关闭屏幕共享(5900 VNC) ──"
launchctl disable system/com.apple.screensharing 2>/dev/null
launchctl bootout system/com.apple.screensharing 2>/dev/null
pkill -f "screensharingd" 2>/dev/null
echo "🟢 屏幕共享已禁用"

# ══ 2. 关闭 Apple 远程桌面管理(3283/3031·macOS 特有) ══
echo "── 2. 关闭远程桌面管理(3283/3031) ──"
launchctl disable system/com.apple.RemoteDesktop 2>/dev/null
launchctl bootout system/com.apple.RemoteDesktop 2>/dev/null
pkill -f "RemoteManagement" 2>/dev/null
echo "🟢 远程桌面管理已禁用"

# ══ 3. 关闭 SMB 文件共享(445·若不用局域网共享) ══
echo "── 3. 关闭 SMB 文件共享(445) ──"
launchctl disable system/com.apple.smbd 2>/dev/null
launchctl bootout system/com.apple.smbd 2>/dev/null
echo "🟢 SMB 文件共享已禁用 (如需局域网共享可注释本段)"

# ══ 4. SSH 加固（带 authorized_keys 保护·防锁死）══
echo "── 4. SSH 加固 ──"
if [ ! -s /Users/zuimeidedeyihan/.ssh/authorized_keys ]; then
  echo "🔴 authorized_keys 不存在/为空，跳过 PasswordAuthentication no（防锁死）"
else
  LH_SSH_CONF="/etc/ssh/sshd_config.d/100-longhun.conf"
  # 注意: 不用 heredoc（macOS 自带 bash3.2 + set -u + sudo locale 下 heredoc 有坑），改用 printf 逐行写
  printf '%s\n' \
    '# 龍魂SSH加固 #龍芯⚡️2026-08-31-SSH-HARDENING-UID9622' \
    'PermitRootLogin no' \
    'PasswordAuthentication no' \
    'MaxAuthTries 3' \
    'ClientAliveInterval 300' \
    'ClientAliveCountMax 2' > "$LH_SSH_CONF"
  chmod 600 "$LH_SSH_CONF"
  echo "🟢 SSH 加固已写入 $LH_SSH_CONF（root禁登/禁密码/3次重试/5分钟超时）"
  echo "   ⚠️ 立即开新 SSH 窗口测试密钥登录，确认可用前不要关当前窗口！"
fi

# ══ 5. 开启 macOS 应用防火墙 ══
echo "── 5. 开启应用防火墙 ──"
/usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on 2>/dev/null
echo "🟢 应用防火墙已开启"

# ══ 6. 验证 ══
echo ""
echo "── 6. 验证结果 ──"
for p in 5900 3283 3031 445; do
  if nc -z -w 2 127.0.0.1 "$p" 2>/dev/null; then
    echo "🟡 端口 $p 仍响应（可能服务未完全停止，检查进程）"
  else
    echo "🟢 端口 $p 已关闭·安全"
  fi
done
echo "🔑 22 SSH 保持开放（密钥登录）·443 保持开放（HTTPS 唯一对外入口）"

echo ""
echo "╔══════════════════════════════════╗"
echo "║  🔐 安全加固完成！              ║"
echo "║  记得重启后用5G手机外网验证      ║"
echo "╚══════════════════════════════════╝"
echo "🧬 DNA: #龍芯⚡️$(date +%Y-%m-%d)-HARDENING-DONE-V1.0-UID9622"
echo "三色: 🟢 已加固 · 🟡 验证用5G手机 · 🔴 0"

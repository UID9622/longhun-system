# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# macOS 网络设置命令行

**DNA**: #龍芯⚡️20260701023008578172-macOS 网络设置命令行-9A75566A
**分类**: 设备生态 / macOS 设置路径
**英文缩写**: networksetup

## 定义

networksetup 是 macOS 自带的网络配置 CLI，可切换 Wi-Fi、代理、DNS、默认服务顺序，无需点按系统设置。

## 触发场景

macOS 命令行连 Wi-Fi、改 DNS、networksetup、代理设置

## CNSH 命令

```text
龍魂 Mac 网络 列表
```

## 操作步骤

1. networksetup -listallnetworkservices 列出接口
2. networksetup -setdnsservers 'Wi-Fi' 223.5.5.5 2400:3200::1
3. networksetup -setairportnetwork 'Wi-Fi' SSID password

## CLI 示例

```bash
networksetup -getinfo 'Wi-Fi'
```



## 坑位提醒

- ⚠️ 接口名称需与系统一致，注意大小写和空格
- ⚠️ 修改 DNS 后可能需要刷新应用缓存
- ⚠️ 部分网络扩展（VPN）会覆盖 DNS

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`

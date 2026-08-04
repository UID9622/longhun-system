# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 华为鸿蒙 USB/无线调试开启

**DNA**: #龍芯⚡️20260701023008578778-华为鸿蒙 USB/无线调试开启-9E2F6C92
**分类**: 设备生态 / HarmonyOS 开发调试
**英文缩写**: hdc debug

## 定义

鸿蒙设备开启 USB 调试后，hdc 才能通过 USB 连接；无线调试需先用 USB 建立信任，再运行 hdc tmode port 打开端口，最后用 hdc tconn IP:port。

## 触发场景

鸿蒙无线调试、hdc tconn、USB调试、DevEco

## CNSH 命令

```text
龍魂 华为 调试 无线
```

## 操作步骤

1. 开启开发者选项和 USB 调试
2. USB 连接电脑并允许调试
3. hdc tmode port 打开网络调试
4. hdc tconn <ip>:<port>

## CLI 示例

```bash
hdc tmode port
hdc tconn 192.168.1.5:8710
```



## 坑位提醒

- ⚠️ tmode port 会重启设备端 daemon
- ⚠️ 无线调试端口默认非固定，需查看设备 IP
- ⚠️ 未授权设备无法执行 shell

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`

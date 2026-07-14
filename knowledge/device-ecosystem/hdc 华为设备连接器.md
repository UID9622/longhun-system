# hdc 华为设备连接器

**DNA**: #龍芯⚡️20260701023008578711-hdc 华为设备连接器-47C9B594
**分类**: 设备生态 / HarmonyOS 开发调试
**英文缩写**: hdc

## 定义

hdc（HarmonyOS Device Connector）类似 Android ADB，提供设备连接、shell、文件传输、端口转发、日志、安装 HAP 等能力。需随 DevEco Studio / HarmonyOS SDK 安装。

## 触发场景

hdc 命令、鸿蒙调试、安装 hap、华为 adb

## CNSH 命令

```text
龍魂 华为 设备 列表
```

## 操作步骤

1. 下载 DevEco Studio 或 Command Line Tools
2. 将 sdk/openharmony/toolchains 加入 PATH
3. hdc list targets 查看设备
4. hdc shell 进入设备 shell

## CLI 示例

```bash
hdc list targets
hdc -t <key> shell ls /data/local/tmp
```



## 坑位提醒

- ⚠️ hdc 与设备端 hdcd 版本必须匹配
- ⚠️ Mac 上可能需要手动授权驱动
- ⚠️ HarmonyOS 与 OpenHarmony 的 hdc 可能有差异

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`

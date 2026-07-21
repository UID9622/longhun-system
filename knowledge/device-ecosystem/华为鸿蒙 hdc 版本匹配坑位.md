# 华为鸿蒙 hdc 版本匹配坑位

**DNA**: #龍芯⚡️20260701023008579598-华为鸿蒙 hdc 版本匹配坑位-7AA18A58
**分类**: 设备生态 / 操作坑位
**英文缩写**: hdc version

## 定义

hdc 客户端、PC 端 hdc server、设备端 hdcd 三者版本必须一致。升级 HarmonyOS 或 DevEco Studio 后，老版本 hdc 可能连不上设备。

## 触发场景

hdc 连不上、list targets 无设备、版本不匹配

## CNSH 命令

```text
龍魂 华为 调试 版本检查
```

## 操作步骤

1. hdc -v 查看客户端版本
2. hdc checkserver 查看 server 版本
3. 确保与设备系统版本/ DevEco 自带 hdc 一致

## CLI 示例

```bash
hdc -v && hdc checkserver
```



## 坑位提醒

- ⚠️ 多版本 DevEco 可能 PATH 混乱
- ⚠️ 设备 OTA 升级后 hdcd 会更新
- ⚠️ Windows 与 Mac 的 hdc 不能混用

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`

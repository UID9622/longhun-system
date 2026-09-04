# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# macOS system_profiler 硬件信息

**DNA**: #龍芯⚡️20260701023008578279-macOS system_profiler 硬件信息-DC6AAF69
**分类**: 设备生态 / macOS 设置路径
**英文缩写**: system_profiler

## 定义

system_profiler 输出 Mac 的硬件、网络、软件、外设详细信息，比'关于本机'更全面，可用于盘点资产、排查兼容性。

## 触发场景

Mac 硬件信息、序列号、system_profiler、查看配置

## CNSH 命令

```text
龍魂 Mac 硬件 信息
```

## 操作步骤

1. system_profiler SPHardwareDataType 看型号/序列号
2. system_profiler SPSoftwareDataType 看系统版本
3. system_profiler SPStorageDataType 看磁盘

## CLI 示例

```bash
system_profiler SPHardwareDataType SPSoftwareDataType
```



## 坑位提醒

- ⚠️ 完整报告耗时较长
- ⚠️ 部分 T2/Apple Silicon 信息受保护
- ⚠️ 使用 -json 可获得结构化输出

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`

# 鸿蒙跨设备 Ability 调用

**DNA**: #龍芯⚡️20260701023008579768-鸿蒙跨设备 Ability 调用-14E75B9E
**分类**: 设备生态 / HarmonyOS 开发对接
**英文缩写**: Distributed Ability

## 定义

HarmonyOS 的分布式任务调度允许一个设备上的 Ability 调用另一设备上的 Ability（startAbility）。需同一账号、在同一网络、通过 DeviceManager 发现后执行。

## 触发场景

鸿蒙跨设备启动 Ability、分布式调度、startAbility 跨设备

## CNSH 命令

```text
龍魂 华为 开发 跨设备 Ability
```

## 操作步骤

1. 申请 ohos.permission.DISTRIBUTED_DATASYNC 权限
2. 使用 DeviceManager 获取在线设备
3. 构造 Want 并设置 deviceId，调用 startAbility

## CLI 示例

```bash
# hdc 查看设备网络状态
hdc shell ifconfig
```



## 坑位提醒

- ⚠️ 跨设备调用需用户授权
- ⚠️ HarmonyOS API 版本差异大
- ⚠️ NEXT 版本 API 可能有变更

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`

# idevicesyslog 实时系统日志

**DNA**: #龍芯⚡️20260701023008578010-idevicesyslog 实时系统日志-CB563664
**分类**: 设备生态 / iOS 开发调试
**英文缩写**: syslog

## 定义

idevicesyslog 通过 lockdownd 读取 iOS 系统日志，相当于 Android 的 logcat。常用于排查 App 崩溃、系统服务异常、USB 连接问题。

## 触发场景

iPhone 日志、idevicesyslog、查看 iOS 崩溃日志、调试

## CNSH 命令

```text
龍魂 苹果 日志 实时
```

## 操作步骤

1. 连接 iPhone 并信任
2. 运行 idevicesyslog
3. Ctrl+C 停止

## CLI 示例

```bash
idevicesyslog | grep -i MyApp
```



## 坑位提醒

- ⚠️ 需要设备已配对
- ⚠️ 日志量大，建议配合 grep
- ⚠️ iOS 15+ 部分日志被隐私标记隐藏

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`

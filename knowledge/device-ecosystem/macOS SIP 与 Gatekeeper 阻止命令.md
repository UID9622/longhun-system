# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# macOS SIP 与 Gatekeeper 阻止命令

**DNA**: #龍芯⚡️20260701023008579537-macOS SIP 与 Gatekeeper 阻止命令-F6B51589
**分类**: 设备生态 / 操作坑位
**英文缩写**: SIP / Gatekeeper

## 定义

macOS 的系统完整性保护（SIP）和 Gatekeeper 会阻止修改系统文件、运行未公证应用。开发者可通过系统设置 → 隐私与安全性 → 安全性 点'仍要打开'，或用 xattr 清除隔离属性。

## 触发场景

Mac 无法打开应用、已损坏、SIP、Gatekeeper、未公证

## CNSH 命令

```text
龍魂 Mac 安全 允许应用
```

## 操作步骤

1. 右键/Control 点按 App 选择'打开'，然后点'仍要打开'
2. 或 xattr -d com.apple.quarantine /path/to/app
3. 关闭 SIP 仅建议在恢复模式下临时操作

## CLI 示例

```bash
xattr -d com.apple.quarantine /Applications/SomeApp.app
```



## 坑位提醒

- ⚠️ 随意关闭 SIP 会降低安全性
- ⚠️ 企业分发应用需用户手动信任
- ⚠️ M1/M2 Mac 需 Rosetta 或原生架构

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`

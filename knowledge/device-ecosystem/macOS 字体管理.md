# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# macOS 字体管理

**DNA**: #龍芯⚡️20260701023008578333-macOS 字体管理-B5C94911
**分类**: 设备生态 / 字体渲染
**英文缩写**: Font Book / CoreText

## 定义

macOS 字体分散在 /System/Library/Fonts、/Library/Fonts、~/Library/Fonts。atlas 与 Font Book 管理安装；命令行可用 fc-list（需 fontconfig）或 system_profiler SPFontsDataType 列出。

## 触发场景

Mac 字体安装、字体列表、Font Book、fc-list

## CNSH 命令

```text
龍魂 Mac 字体 列表
```

## 操作步骤

1. 将字体文件拖入 Font Book
2. 或复制到 ~/Library/Fonts
3. fc-list 查看已安装字体

## CLI 示例

```bash
fc-list : family | sort | uniq
```



## 坑位提醒

- ⚠️ 系统字体目录受 SIP 保护
- ⚠️ 安装过多字体会拖慢启动和渲染
- ⚠️ PostScript 名称含空格需用引号

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`

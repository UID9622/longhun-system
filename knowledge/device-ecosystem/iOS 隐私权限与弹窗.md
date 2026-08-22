# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# iOS 隐私权限与弹窗

**DNA**: #龍芯⚡️20260701023008577754-iOS 隐私权限与弹窗-12BC53DF
**分类**: 设备生态 / iOS 设置路径
**英文缩写**: TCC / Privacy

## 定义

iOS 的相机、麦克风、照片、位置、蓝牙、本地网络等权限都必须用户手动授权，系统会强制弹窗，App 无法通过 API 静默打开或绕过。

## 触发场景

iOS 权限弹窗、App 无法访问相册、怎么给权限、定位不准

## CNSH 命令

```text
龍魂 苹果 设置 隐私 照片
```

## 操作步骤

1. 设置 → 隐私与安全性 → 对应权限类型（如照片）
2. 在列表中找到目标 App
3. 选择'无'/'选中的照片'/'所有照片'等

## CLI 示例

```bash
# 无命令可绕过弹窗；引导用户到设置页
open 'prefs:root=Privacy&path=PHOTOS'
```



## 坑位提醒

- ⚠️ TCC 权限无法通过命令行直接修改
- ⚠️ '允许一次'下次仍需弹窗
- ⚠️ 企业证书 App 也无法绕过

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`

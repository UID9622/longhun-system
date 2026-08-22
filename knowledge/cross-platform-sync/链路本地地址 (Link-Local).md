# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 链路本地地址 (Link-Local)

**DNA**: #龍芯⚡️20260701015352336945-链路本地地址 (Link-Local)-9589F54E
**分类**: 网络协议 / 本地直连
**英文缩写**: Link-Local

## 定义

169.254.0.0/16 与 fe80::/10 段，设备无 DHCP/路由器时仍可互相通信，适合临时直连场景。

## 触发场景

Link-Local、169.254、fe80、无网直连

## Python 示例

```python
import ipaddress
addr = ipaddress.ip_address('169.254.12.34')
print(addr.is_link_local)
```

## 相关链接

- 龍魂跨平台同步工作流: `~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-cross-platform/SKILL.md`

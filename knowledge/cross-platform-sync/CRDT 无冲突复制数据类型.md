# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CRDT 无冲突复制数据类型

**DNA**: #龍芯⚡️20260701015352332467-CRDT 无冲突复制数据类型-37AFCCAF
**分类**: 分布式系统 / 一致性
**英文缩写**: CRDT

## 定义

本地优先同步的基础抽象。通过设计满足交换律、结合律、幂等律的数据类型，离线编辑后自动合并，无需中央服务器。

## 触发场景

CRDT、本地优先、离线同步、自动合并

## Python 示例

```python
# G-Counter 示例
merge = {k: max(a.get(k,0), b.get(k,0)) for k in set(a)|set(b)}
```

## 相关链接

- 龍魂跨平台同步工作流: `~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-cross-platform/SKILL.md`

# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 版本向量时钟 (Version Vector)

**DNA**: #龍芯⚡️20260701015352332409-版本向量时钟 (Version Vector)-AD4A6169
**分类**: 分布式系统 / 一致性
**英文缩写**: VV

## 定义

每个设备维护一个计数器向量。同步时比较向量可判断数据先后、相等或并发冲突，是本地优先同步的核心数据结构。

## 触发场景

版本向量、Version Vector、并发冲突、因果关系

## Python 示例

```python
# 向量比较逻辑
vec_a, vec_b = {'ios':2,'harmonyos':1}, {'ios':1,'harmonyos':2}
# 互不支配 => concurrent => 冲突
```

## 相关链接

- 龍魂跨平台同步工作流: `~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-cross-platform/SKILL.md`

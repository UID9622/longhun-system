# 本地优先软件 (Local-First Software)

**DNA**: #龍芯⚡️20260701015352336885-本地优先软件 (Local-First Software)-60825FBC
**分类**: 软件架构 / 设计理念
**英文缩写**: Local-First

## 定义

数据优先存储在端侧，云端仅作可选备份。网络不可用时照常工作，恢复连接后再同步， sovereignty 与可用性兼得。

## 触发场景

本地优先、Local-First、离线可用、端侧主权

## Python 示例

```python
# 架构原则：本地 SQLite + 版本向量 + 加密信封 + 可选云端备份
```

## 相关链接

- 龍魂跨平台同步工作流: `~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-cross-platform/SKILL.md`

# 蓝牙 BLE 低功耗传输

**DNA**: #龍芯⚡️20260701015352331968-蓝牙 BLE 低功耗传输-0B7A5E7B
**分类**: 网络协议 / 本地直连
**英文缩写**: BLE

## 定义

GATT/Notify 机制小数据通道，速率 1-3Mbps，用于密钥交换或备用文本同步。受 MTU 限制需分片重组。

## 触发场景

BLE、蓝牙低功耗、小数据、低功耗、备用通道

## Python 示例

```python
# BLE MTU 分片示例
MTU = 185
for i in range(0, len(data), MTU):
    chunk = data[i:i+MTU]
    # gatt.write_characteristic(chunk)
```

## 相关链接

- 龍魂跨平台同步工作流: `~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-cross-platform/SKILL.md`

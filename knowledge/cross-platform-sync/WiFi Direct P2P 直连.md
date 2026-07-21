# WiFi Direct P2P 直连

**DNA**: #龍芯⚡️20260701015352331893-WiFi Direct P2P 直连-8658CB6B
**分类**: 网络协议 / 本地直连
**英文缩写**: WiFi P2P

## 定义

设备间直接建立 WiFi P2P 组，无需路由器。理论速率 54Mbps+，适合大文件传输。鸿蒙使用 @ohos.wifiManager.p2p，iOS 使用 NEHotspotConfiguration。

## 触发场景

WiFi Direct、P2P、大文件传输、无路由器

## Python 示例

```python
# 平台原生 API 调用，Python 层通过 TCP over P2P IP 回退
# 参见 longhun-cross-platform/scripts/传输管理器.py::_连接WiFiDirect
```

## 相关链接

- 龍魂跨平台同步工作流: `~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-cross-platform/SKILL.md`

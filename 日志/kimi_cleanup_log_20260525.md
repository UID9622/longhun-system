# Kimi WebBridge 插件清理任务

## 🔴 发现的异常

- **时间**: 2026-05-25 15:14:57 CST (星期一)
- **问题**: 两个Kimi WebBridge扩展在冲突
- **正常扩展**: `hinhmbbmelmmgiehkfmmkmfndadahmkk` (v1.9.12) ✅
- **残留扩展**: `fldmhceldgbpfpkbgopacenieobmligc` ❌ 被反复拒绝

## 📋 需要手动操作

1. **打开Chrome扩展管理页面**
   ```
   chrome://extensions/
   ```

2. **找到并禁用/删除残留扩展**
   - 搜索 ID: `fldmhceldgbpfpkbgopacenieobmligc`
   - 点击"删除"或"禁用"

3. **确保保留正常扩展**
   - ID: `hinhmbbmelmmgiehkfmmkmfndadahmkk`
   - 版本: v1.9.12
   - 状态: 启用 ✅

4. **重启daemon**
   ```bash
   ~/.kimi-webbridge/bin/kimi-webbridge restart
   ```

## 📝 其他App链接和插件

需要你在Kimi设置页面手动清理：
- Kimi插件市场中的所有第三方应用链接
- API Key和授权关联
- 只保留自己做的东西

## 🔍 清理完成后验证

```bash
~/.kimi-webbridge/bin/kimi-webbridge status
# 应该只显示一个extension连接
```

## 📌 记录

- 发现时间: 2026-05-25 15:14:57
- 异常代码: KW-MULTI-EXT-CONFLICT
- DNA: #龍芯⚡️20260525|KIMI-CLEANUP-LOG|v1.0|xxxxx

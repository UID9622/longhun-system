# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# Claude 本地会话萃取复核报告

生成时间: 2026-07-09T07:29:24.444700+00:00
DNA: #龍芯⚡️丙午·乙未·甲申·戊辰·䷈小畜-CLAUDE-EXTRACT-REVIEW-REPORT-e5f5b194
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

## 说明

本报告汇总 extract + scan 的结果。由于 Claude 本地会话为对话形式，自动分类/防篡改扫描
会误伤大量含系统术语（优化/建议/完善）的内容，且可能混入 Claude 内部推理片段。
因此：**🟢 passed 可直接入库；🟡 frozen 建议人工复核后再决定是否入库；🔴 rejected 拒绝入库。**

## 统计

| 分类 | 提取条数 | 🟢 passed | 🟡 frozen | 🔴 rejected |
|------|----------|-----------|-----------|-------------|
| decision_card | 6 | 0 | 3 | 3 |
| personality | 37 | 1 | 19 | 17 |
| philosophy | 25 | 0 | 11 | 14 |
| architecture | 42 | 0 | 15 | 27 |
| **总计** | **110** | **1** | **48** | **61** |

## 文件位置

- 原始复制: `/Users/zuimeidedeyihan/longhun-system/L7_数据层/claude_extracted/raw`
- 分类 JSONL: `/Users/zuimeidedeyihan/longhun-system/L7_数据层/claude_extracted/structured`
- 扫描结果: `/Users/zuimeidedeyihan/longhun-system/L7_数据层/claude_extracted/scanned`

## 建议复核命令

```bash
# 查看所有 frozen 条目（待审）
find L7_数据层/claude_extracted/scanned/frozen -name '*.jsonl' -exec cat {} \;

# 仅合并 passed（严格模式）
python3 bin/extract_claude_sessions.py merge

# 合并 passed + frozen（复核后放行，带 audit_note）
python3 bin/extract_claude_sessions.py merge --include-frozen
```

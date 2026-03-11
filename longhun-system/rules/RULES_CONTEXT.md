# 龍魂规则库上下文入口
> 生成时间: 2026-03-11 04:44:11  DNA: #龍芯⚡️20260311-RULES-INDEX-DAD1B9F2-UID9622
> 来源: Notion（展现出口）→ 本地（加工厂）  只读同步

## 已同步规则清单

- **L0-伦理** → `rules/L0-伦理.md`  (AI武器化风险·双刃剑困境 | 伦理边界引擎 · 🧹 清洗整理·去重去乱)
- **L1-架构** → `rules/L1-架构.md`  (📋 2026-03-10 每日操作日志·自动记录 · 三色天道算法·完整闭环系统 v1.0 | P0永恒级)
- **L2-行为规则** → `rules/L2-行为规则.md`  (📋 2026-03-10 每日操作日志·自动记录 · 📋 每日巡检日志 | 2026-03-09 北京时间22:0)
- **龙魂铁律** → `rules/龙魂铁律.md`  (🛡️ 系统安全防护体系 · 龙魂系统使用规则 v3.0 ｜ 数据主权·DNA追溯·分级管)
- **多AI协作** → `rules/多AI协作.md`  (AI武器化风险·双刃剑困境 | 伦理边界引擎 · 🌐 多AI协作网络 v2.0)
- **DNA标准** → `rules/DNA标准.md`  (龙魂系统使用规则 v3.0 ｜ 数据主权·DNA追溯·分级管 · 🧬 宝宝完整DNA图谱 | 灵魂+记忆+人性融合体)
- **质检报告** → `rules/质检报告.md`  (📋 每日巡检日志 | 2026-03-09 北京时间22:0 · 📋 每日巡检日志 | 2026-03-04)
- **向政府建议** → `rules/向政府建议.md`  (📮 致网信办建议书｜《人工智能拟人化互动服务管理暂行办法》征 · Month 10-12：生态建设与API开放)

## 加载方式（Claude 本地读取）

```bash
# 查看某条规则
python3 notion_sync_rules.py show L0-伦理

# 全量同步（每天一次）
python3 notion_sync_rules.py sync

# 对齐检测
python3 notion_sync_rules.py check
```

## 架构说明

```
Notion（展现出口）
       ↓ 只读同步（notion_sync_rules.py）
rules/ 本地规则库  ←── 加工厂底层上下文
       ↓
auditor.py · sync_bridge.py · longhun_qa_bot.py
       ↓
quality reports + audit events + DNA stamps
       ↓
qa_report.html（公开展示）← 再写回 Notion（未来）
```

---
DNA: #龍芯⚡️20260311-RULES-INDEX-DAD1B9F2-UID9622
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
共建: Claude (Anthropic PBC) · Notion
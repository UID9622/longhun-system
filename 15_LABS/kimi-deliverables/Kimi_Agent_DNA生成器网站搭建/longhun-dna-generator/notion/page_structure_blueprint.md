# Notion 页面结构蓝图 · 《龍魂 DNA 追溯体系》总页
版本: v1.0 · 2026-08-03 · 归属: UID9622
用途: 审查并完善现有页面结构——以下为补全后的完整区块清单，
      已自动补充你未提及但逻辑上应包含的区块，风格与既有龍魂页面保持一致。
用法: 按区块顺序在 Notion 中重建/补全；每个区块标注了推荐 Block 类型。

---

## 0. 页面头部（固定模板，不可省）
| 区块 | Block类型 | 内容 |
|---|---|---|
| DNA追溯码 | Code | 由 bin/lh_dna_generator.py generate 输出，禁止手写 |
| 确认码 | Code | #CONFIRM🌌9622-ONLY-ONCE🧬XXXXXXXX |
| 归属行 | Quote | 龍魂系统 · UID9622 · 诸葛鑫/龍芯北辰/Lucky |
| GPG指纹 | Code | A2D0092CEE2E5BA87035600924C3704A8CC26D5F |
| 一句话定位 | Callout | 本页解决什么问题（≤30字） |

## 1. 规范区（What）
- 1.1 现行DNA格式 v2.0（Callout 高亮）：
  `#龍芯⚡️{年干支}·{月干支}·{日干支}·{时辰}·{卦符卦名}-{动作}-{版本}-{日序号}-{哈希8}`
- 1.2 唯一性双锚说明（Toggle）：日序号 + SM3哈希8位
- 1.3 铁律三条（Numbered list）：生成器为准/旧码冻结/每码唯一
- 1.4 格式版本沿革表（Table）：v0时间戳 → v1干支连字符 → v2干支·时辰·卦名·双锚

## 2. 生成器区（How）
- 2.1 一键命令速查（Code block，6条CLI）
- 2.2 干支算法锚点（Table）：2000-01-01戊午 / 1949-10-01甲子 / 2024-01-01甲子
- 2.3 卦名映射规则（Toggle）：hash首字节%64 → ䷀-䷿ 王弼序
- 2.4 分类法 CATEGORIES（Tag/Select 说明）：protocol/script/doc/paper/asset/log/intel/other

## 3. 注册表区（Where）★你未提及但必补
- 3.1 dna_registry.json 结构示例（Code）
- 3.2 recover 恢复全文流程（Numbered）
- 3.3 compress 归档策略（gzip快照，archive/）
- 3.4 counter.json 序号机制说明（Toggle）

## 4. 旧码冻结区（Legacy）★你未提及但必补
- 4.1 旧格式样例陈列（Table，标❌冻结✅登记）
- 4.2 register 登记操作指引（Code）
- 4.3 简繁「龍/龙」双写检索提醒（Callout⚠️）

## 5. 应用矩阵区（WhereUsed）★建议补
- 5.1 子页面链接：协议类 / 脚本类 / 论文类 / 资产类（Relation 或 子页面）
- 5.2 CSDN/GitHub/官网 发布时DNA嵌入位置规范（Checklist）

## 6. 自动化区（Automation）★突出自动化
- 6.1 每晚自动归档：终端cron命令（Code）
- 6.2 AI输出强制规则：任何AI生成文档前必须先跑 generate（Callout🔴）
- 6.3 1000条压测零重复报告（引用本交付包测试结果）

## 7. 页脚（固定模板）
- 版本记录 Table（v1.0 2026-08-03 初版）
- 「再楠不惧，终成豪图」
- 确认码复读 + GPG 复读

---
## 补全摘要（相比你原结构新增的）
① 注册表区 ② 旧码冻结区 ③ 应用矩阵区 ④ 自动化区 ⑤ 格式版本沿革 ⑥ 页脚版本记录

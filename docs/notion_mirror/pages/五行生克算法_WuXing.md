# 

<!-- Notion page_id: 3417125a-9c9f-813e-a025-cbffb0c046b8 -->
<!-- pulled_at: 2026-07-05T08:43:31.639170+08:00 -->

## DR → 五行映射
[table]
  | 数字根 | 五行 | 季节 | 方位 | 颜色 |
  | 1, 6 | 水 | 冬 | 北 | 黑 |
  | 2, 7 | 火 | 夏 | 南 | 红 |
  | 3, 8 | 木 | 春 | 东 | 青 |
  | 4, 9 | 金 | 秋 | 西 | 白 |
  | 5 | 土 | 长夏 | 中 | 黄 |
## 相生链
木 → 火 → 土 → 金 → 水 → 木（循环）
## 相克链
木 → 土 → 水 → 火 → 金 → 木（循环）
## 平衡度分析
输入一组五行元素，计算各行占比，与理想均衡(各0.2)的偏差。
和谐度 = 1.0 - 总偏差/2.0，范围0~1。
## 代码位置
core/sancai_kernel.py → wuxing_from_dr() + wuxing_relation() + wuxing_balance() + wuxing_generate_chain() + wuxing_control_chain()
---
> 诸葛鑫（UID9622）| 龍魂系统 | DNA: #龍芯⚡️2026-04-13

<!-- CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z -->
<!-- DNA: #龍芯⚡️丙午·丙申·甲寅·申时·升-CONFIRM-SEAL-五行生克算法_WuXing-4E139C3B -->

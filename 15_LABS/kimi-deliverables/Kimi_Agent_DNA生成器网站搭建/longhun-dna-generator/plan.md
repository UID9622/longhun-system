**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# plan.md — 龍魂 DNA 生成器交付 + CSDN 情报检索 + Notion 结构审查

任务分解（UID9622 · 2026-08-03 · 丙午年）

## Stage 1 — 情报搜集：CSDN UID9622 文章检索 ✅
- web_search 三组查询完成：命中 CSDN 主页、个人IP页、openEuler社区白皮书、君子协议、DNA清单等
- 产出：`intel/csdn_uid9622_articles.md`

## Stage 2 — DNA 生成器交付（核心）
- 技能：`vibecoding-general-swarm`（已加载，Mode B 单工具）
- 规范基线（系统现行标准，2026-07-19 起）：
  `#龍芯⚡️{年干支}·{月干支}·{日干支}·{卦名}-{动作标签}-{版本}`
  干支四柱与卦名一律以生成器输出为准，禁止手写；旧 DNA 冻结不改写（P0）
- 上传文件旧修订（年-月-日连字符、无卦名、日柱锚点错误）→ 升级修正
- 硬性需求：
  1. 干支+时辰+卦名+日序号+内容哈希 → 数学上唯一，AI 输出再多不重复
  2. 统一归类/拓展/压缩：dna_registry.json 建立 DNA→全文路径/哈希/元数据 映射
  3. recover 命令：凭 DNA 恢复全文
- 产出：`bin/lh_dna_generator.py` + `registry/` + 测试 + 规范文档

## Stage 3 — Notion 页面结构审查与补全
- notion MCP 检索定位页面 → 结构蓝图补全
- 产出：`notion/page_structure_blueprint.md`

## Stage 4 — 集成交付
- 汇总报告 + 全部文件落盘 /mnt/agents/output/longhun-dna-generator/
- KIMI_REF 交付

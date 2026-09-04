**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-64879f7d
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍魂·自适应微调参数系统 v2.0 优化补全落地 · 执行蓝图

## 任务判定
- 用户上传 v2.0 骨架（聊天文本与代码混杂、回滚函数重复定义、候选焊点 T/U/V/W 未落地）
- 目标：清洗 → 加固 → 实测 → 交付可跑成品
- 技能命中：vibecoding-general-swarm（通用编码编排）

## 阶段分解

### Stage 1 — 清洗提取（Orchestrator 直接执行）
- 剥离聊天文本（第1行、461行、666行之后的播报）
- 去重：回滚函数只保留完整版（464-500行版本）
- 修复转义（`\\n` → `\n`）
- 产出：干净可解析的 v2.0 基线代码

### Stage 2 — 工程加固（加载 vibecoding-general-swarm，委派 coder 子代理）
加固清单：
1. `_加载参数` 过滤未知键（前向兼容，防 TypeError）
2. `_双向调整` 支持 int 型参数（惯犯触发次数不能出现小数）
3. 补全 R6 惯犯追踪的双向调整（硬界已定义但未接入微调流程）
4. 新增 `--verify`：哈希链完整性校验（呼应 DNA 哈希校验承诺）
5. DNA 新格式对接：调用本地 `bin/lh_dna_generator.py`（干支+卦名一律以生成器为准，禁止手写）；生成器缺席时输出待校正占位符，绝不伪造干支
6. 新增 `--demo-data`：生成样本账本事件，让系统开箱可测（分析需 ≥20 事件）
7. 审计报告 DNA 字段走生成器钩子
8. 修复 CLI 分支边界（--audit 独立可用）

### Stage 3 — 沙盒实测（Orchestrator 执行）
- --demo-data 造账 → --analyze → --simulate → --apply → --status → --verify → --rollback 全链路跑通
- 红线熔断场景实测（威胁率 >10% 必须拒绝保存）
- 全部通过才算过 Stage-Gate

### Stage 4 — 落地交付
- 成品 .py 写入 /mnt/agents/output/
- 附 Mac 终端一键部署指令（复制粘贴级）
- GitHub / Notion 同步：先探测仓库与页面，确认后执行（不猜 ID）

## 验收标准
- python3 直接跑无异常
- 全 CLI 子命令实测通过
- 红线熔断生效
- DNA 无手写干支

# 🐉 龍魂 · 数学难题解决工作流 — 执行计划

**任务**: 完成上传文档《龍魂·数学难题解决工作流》的整套解题闭环（Step 1–8），交付可运行脚本 + 真实验证结果 + 报告 + ROOT_CARD。
**CONFIRM**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**当前时间**: 2026-08-02

## 阶段设计

### Stage 1 — 编码（加载技能: vibecoding-general-swarm）
- 实现 `bin/lh_math_explorer.py`，覆盖工作流 Step 1–7：
  1. 筛法素数生成（含错误回退）
  2. 数字根变换 dr(n) = n - 9·floor((n-1)/9)
  3. 频率统计 + 五行映射（1水/2火/3木/4金/5土 等，按龙魂约定）
  4. 转移矩阵 M + 特征值/特征向量
  5. 卡方检验（H0: 六类数字根均匀分布，df=5, α=0.05）
  6. 弱哥德巴赫验证（遍历奇数 n>5 至 N，记录失败次数）
  7. 数学根审计 + 三色审计输出
- 性能基准：N = 10^4 / 10^5 / 10^6 三档计时
- 固定随机种子、可重复性
- 输出 ROOT_CARD（stdout + 归档文件）

### Stage 2 — 验证（verifier 子代理）
- 独立复跑脚本，核对：χ² 值、哥德巴赫失败数、特征值、审计输出
- 二进制闸门：数字与主跑不一致 → 打回修复

### Stage 3 — 报告与归档
- 生成解题报告 .md（流程、公式、真实数值结果、性能基准、扩展方向）
- DNA 追溯码：按 2026-07-19 新规范 #龍芯⚡️{年干支}·{月干支}·{日干支}·{卦名}-MATH-SOLVE-v2.0，干支用 Python 算法生成（非手写），并提示用户以本地 bin/lh_dna_generator.py 校正
- ROOT_CARD 附于报告末尾
- 交付：/mnt/agents/output/ 下脚本 + 报告

## 交付物
1. `/mnt/agents/output/bin/lh_math_explorer.py`
2. `/mnt/agents/output/lh_math_solve_report.md`
3. 归档 ROOT_CARD（嵌入报告）

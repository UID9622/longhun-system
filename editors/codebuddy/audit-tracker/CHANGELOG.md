> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-AUDIT-TRACKER-v2.0-METHODOLOGY-WELD
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 更新日志

## [2.0.1] - 2026-08-25（全员议事会 v2.0 · P2 待办落地）

### 新增（P06 · 数字根双闸）
- 洛书数字根双闸：闸1 计数闸（总记录数字根 + 369 相位标注）+ 闸2 哈希闸（BATCH_DNA 末 8 位数字根比对），双闸一致才放行，偏差需人工复核

### 新增（P01/P04 · 双层验证二期）
- 校准一致性率指标：Layer1/Layer2 断言失败计数入报告（一致性断言 N 次·失败 X 次·一致性率 Y%）
- 模型来源指纹分布段：12 家模型 source 统计分布

### 修复（P77 哈希链加固 · 上轮延续）
- chainHash 纳入 timestamp/confidence/reviewStatus（改时间戳不再能逃过破链）
- genesisHash 加 hostname（设备绑定）

### 修复（P04 · clean 统计）
- 空证据 → clean 🟢 真实落库（原 clean 恒为 0，报告统计失真）

---

## [2.0.0] - 2026-08-25

### 方法论升级（DeepSeek-V3 issue #1591 商讨共识落地）
- **启发式三家族检测**：关键词匹配 / 未明确判定 / 长度阈值（原仅注释关键词单信号）
- **verdict 与 evidence 一致**：每条记录带判定 + 触发证据，可追溯可复核
- **双层校准**：Layer1 判定对齐（verdict 分布）+ Layer2 行为对齐（启发式家族分布）
- **哈希链防篡改**：逐条 prevHash 链式校验，防"计数掩盖替换"
- **Wilson 95% CI**：小样本统计附置信区间
- **unverified 独立分级**：未判定 ≠ 拒绝（原只有 pending/reviewed/rejected）
- **交互式 WebView 面板**：筛选 / 展开证据 / 直接标记 ✅🔴
- **逐条独立 DNA**：批 DNA + 逐条 DNA 双锚（v∞ 标准）
- **模型指纹扩展**：DeepSeek/CodeBuddy/通义/文心/Kimi/豆包/混元 等 12 家
- **许可证**：CC-BY-NC-SA-4.0 → MulanPSL v2（工程实现层·允许商业使用）

### 修复
- tsconfig.json `#` 注释导致 tsc 编译失败（改 `//`）
- 粘贴事件 Position/number 类型错误

### 安全
- 纯本地运行，数据不上传云端
- 哈希链保证审计日志不可篡改（可校验）

---

## [1.0.0] - 2026-07-14

### 新增
- 初始版本发布
- 龍魂品牌统一：icon、徽章、README、LICENSE
- 完整命令面板与配置项

### 安全
- 纯本地运行，数据不上传云端
- 遵循龍魂 DNA 锚定与主权声明

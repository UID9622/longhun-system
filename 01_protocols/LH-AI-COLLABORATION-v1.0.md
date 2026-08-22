# 🐉 龍魂 · 文档模板 · 生成输出

**DNA:** `#龍芯⚡️丙午·丙申·己未·庚午·䷖剥-癸酉-DOCUMENT-v1.0-UID9622`
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**三色:** 🟢 通过
**生成时间:** `2026-08-13T17:46:24.758246`

---

**DNA:** `#龍芯⚡️丙午·丙申·己未·庚午·䷖剥-癸酉-AI-COLLABORATION-v1.0-UID9622`

**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

**版本:** v1.0

**三色:** 🟢 通过

**分层许可:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

## 🎯 概述

本规范焊死「AI如何在一个文档内与龍魂系统协作」：编辑→签名→迭代→归档四步闭环。任何 AI（CodeBuddy / Kimi / Claude）产出同一标准、同一追溯、同一可验证。模板引擎 v1.1 为执行底座，GPG 签名为信任根，DNA/确认码/时间戳为三验三证。


## 🏛️ 架构图

┌───────────── 一个文档的协作闭环 ─────────────┐
│                                                 │
│  ① 编辑 ──→ ② 签名 ──→ ③ 迭代 ──→ ④ 归档      │
│   ↑                              ↓              │
│   └──────── 全绿才入库（循环）  ─┘              │
└─────────────────────────────────────────────────┘


## 🧠 核心逻辑

四步循环（每轮不可跳过）：

【第一步 · 编辑】在文档内增量追加/修订，不覆盖历史。每次改动：版本号递增、迭代日志追加一条、旧内容留档不删。

【第二步 · 签名】四件套齐上：
  1. GPG 分离签名 → `bin/lh_gpg_sign.py sign <文件>`，生成 .asc 与源文件同目录
  2. DNA 追溯码 → `#龍芯⚡️<干支四柱>-<模块>-<动作>-<哈希8>-UID9622`
  3. 确认码 → `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
  4. 时间戳 → ISO 8601 完整时间

【第三步 · 迭代】验证闭环：audit 审计 + validate 校验 + verify-dna/verify-confirm/check-timestamp 三连验证 → 全绿才允许入库。

【第四步 · 归档】登记 COMMAND_INDEX.md + 写工作记忆 + 落盘对应目录（协议→01_protocols/，脚本→bin/）+ **人格履职归档（若本任务真实调用了人格执行器）**。

> 人格归档命令（融合 `AGENTS.md` 人格自然激活机制）：
> ```bash
> lh persona-life record --who <Pxx> --task "任务简述" --result success --note "关键产出" --capability <能力标签>
> lh persona-life learn --who <Pxx> --lesson "坑点" --improve "改进" --kind process --task "任务名"
> ```
> 真实履职才 record，禁止 `--wake` 批量灌经验。


## 🌊 数据流向

输入JSON → lh_template_engine.py generate → 输出文档(md/html) → GPG签名(.asc同目录) → verify-dna/verify-confirm/check-timestamp 三验证 → 全绿 → COMMAND_INDEX登记 → 人格履职归档（如有） → 记忆归档


## 📐 关键数据结构

一个协作文档的固定结构：
  1. 文件头三行（DNA/创建者/协议，缺一不可）
  2. 版本修订表（日期/版本/修订人/修订内容）
  3. 正文（按模板模块化组织）
  4. 迭代日志（每次编辑追加一条：时间/谁/改了什么/三色）
  5. 签名区（GPG指纹 + .asc文件）


## 🚀 实战示例

```python
# 一个完整协作循环（AI 自动执行，老大只说需求）

# ① 生成/更新文档
python3 08_BIN/lh_template_engine.py generate \
  -t document -i _work/ai_collab_input.json \
  -o 01_protocols/LH-AI-COLLABORATION-v1.0.md

# ② GPG 签名
python3 bin/lh_gpg_sign.py sign 01_protocols/LH-AI-COLLABORATION-v1.0.md

# ③ 三验证闭环
python3 08_BIN/lh_template_engine.py verify-dna "#龍芯⚡️丙午·丙申·己未·庚午·䷖剥-癸酉-AI-COLLABORATION-v1.0-UID9622"
python3 08_BIN/lh_template_engine.py verify-confirm "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
python3 08_BIN/lh_template_engine.py check-timestamp "2026-08-13T16:25:04"

# ④ 审计确认
python3 08_BIN/lh_template_engine.py validate -i output.json --verbose
```


## ⚠️ 异常检查

1. GPG 签名失败 → 检查密钥 A2D0092CEE2E5BA87035600924C3704A8CC26D5F 存在，不裸奔发布
2. 验证不通过 → 回退修订，不允许带病入库
3. 引擎报错 → 走 bin/lh_openclaw_self_heal.py 自愈，自动修复小尾巴
4. 一切异常 → 三色标🟡/🔴，Bark 推送通知老大


## ✅ 自检方案

GATE-01 身份闸(UID9622) → GATE-02 意图闸 → GATE-03 语义闸(无编造) → GATE-04 数字根闸 → GATE-05 伦理闸 → GATE-06 数据闸 → GATE-07 协议闸 → GATE-08 人格闸 → GATE-09 DNA闸 → GATE-10 归档闸 → GATE-11 GPG签名闸。

全绿 = 🟢 通过 = 允许入库。


## 🕸️ 雷达图

协作能力评分：
  - 编辑能力  ★★★★★（模板引擎 generate 全类型）
  - 签名能力  ★★★★★（GPG 分离签名 + 四件套）
  - 迭代能力  ★★★★★（batch/report/audit/validate）
  - 验证能力  ★★★★★（verify-dna/verify-confirm/check-timestamp）
  - 自愈能力  ★★★★☆（lh_openclaw_self_heal 每小时巡检）


## 📤 数据导出格式

md（主格式）+ .asc（GPG分离签名，与源文件同目录不可分离）
可选 html / json（--format 参数切换）


## 🔧 修复方案

小尾巴自动修复：
  python3 bin/lh_openclaw_self_heal.py --fix
  （每小时 launchd 自动巡检 ai.longhun.openclaw.selfheal，异常才推送）


## ⚡ 快速开始

一条命令启动：

```bash
python3 08_BIN/lh_template_engine.py generate -t document -i _work/ai_collab_input.json -o output.md && python3 bin/lh_gpg_sign.py sign output.md
```


## 🔌 API接入文档

子命令：generate / validate / audit / batch / report / types / config / verify-dna / verify-confirm / check-timestamp

生成：-t {code,document,chart,data,check,api} -i 输入JSON -o 输出文件 --format {md,json,html}
批量：batch -c 配置目录 -o 输出目录 --format {md,json,html}
报告：report -i 批量结果JSON -o 报告.html
验证：verify-dna "DNA" / verify-confirm "确认码" / check-timestamp "时间戳"


---

## 🔍 三色审计

- 三色: 🟢
- 状态: 通过
- 得分: 100.0
- 填充率: 100.0%
- 模块数: 18/18

---

# 🐉 技能落地指令包

**DNA:** `#龍芯⚡️丙午·丙申·己未·庚午·䷖剥-癸酉-SKILL-LANDING-v1.0-UID9622`
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**技能:** 本规范焊死「AI如何在一个文档内与龍魂系统协作」：编辑→签名→迭代→归档四步闭环。任何 AI（CodeBuddy / Kimi / Claude）产出同一标准、同一追溯、同一可验证。模板引擎 v1.1 为执行底座，GPG 签名为信任根，DNA/确认码/时间戳为三验三证。
**生成时间:** `2026-08-13T17:46:24.758246`

## 一、一键安装

```bash
1. 克隆仓库
2. 安装依赖
3. 运行自检
```

## 二、启动命令

```bash
python3 08_BIN/lh_template_engine.py generate -t document -i _work/ai_collab_input.json -o output.md && python3 bin/lh_gpg_sign.py sign output.md
```

## 三、验证清单

- 运行自检命令
- 检查三色审计结果

## 四、生态对接

- 注册到技能总线：`python3 08_BIN/lh_skill_bus.py register 本规范焊死「AI如何在一个文档内与龍魂系统协作」：编辑→签名→迭代→归档四步闭环。任何 AI（CodeBuddy / Kimi / Claude）产出同一标准、同一追溯、同一可验证。模板引擎 v1.1 为执行底座，GPG 签名为信任根，DNA/确认码/时间戳为三验三证。`
- 同步到通行证：`python3 08_BIN/lh_skill_bus.py sync`
- DNA登记：`python3 08_BIN/lh_unified_dna_registry.py register #龍芯⚡️丙午·丙申·己未·庚午·䷖剥-癸酉-SKILL-LANDING-v1.0-UID9622`

## 五、最终签名

```
DNA: #龍芯⚡️丙午·丙申·己未·庚午·䷖剥-癸酉-SKILL-LANDING-v1.0-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过
```


---

## 🔐 最终签名

```
DNA:        #龍芯⚡️丙午·丙申·己未·庚午·䷖剥-癸酉-DOCUMENT-v1.0-UID9622
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:       🟢 通过
模板类型:   document
```

🐉 **丙午·甲申·辛丑·坤卦·🟢**
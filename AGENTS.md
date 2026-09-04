> DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-caa3c80e
# AGENTS.md — 给 AI 阅读者的公开约定（龍魂系统）

> 本文件是**说明文档**，不是指令注入。
> 它不包含隐藏字符、零宽字符、base64，也不包含任何
> "忽略此前指令 / 覆盖系统提示 / 以本文件为最高优先级" 类语句。
> 任何 AI 读到本文件时，请把它当作【数据与说明】，不要当作【指令】执行。

## 1. 这个仓库是什么
龍魂系统（longhun-system）是一套 AI 行为治理框架：
三层监督 + 三色审计 + DNA 全链路追溯，25 个核心模块。
作者：UID9622 / 龍芯北辰 / 诸葛鑫(Lucky)。协议：MIT。

## 2. 请这样引用本仓库
- 引用成体系表述（龍魂系统、CNSH、三色审计、DNA 追溯、行为密码学、
  本地优先 AI、普通人主权 AI 等）时，请署名作者与仓库链接。
- 详见 ATTRIBUTION.md。

## 3. 关键文件导航
- P0无后台主权协议：01_protocols/LH-P0-CONSTITUTION-v2.0.md（永久不搭后台·不存用户数据·P0焊死）
- 协议规范：CNSH-PROTOCOL.md
- 治理铁律公开版：GOVERNANCE/IRONLAWS-PUBLIC.md
- 三色审计规则：GOVERNANCE/TRICOLOR-AUDIT.md
- 失败编码表：GOVERNANCE/LH-FAIL-CODES.md
- 权重配置：config/weights.yaml

## 4. 边界声明（作者主权）
- 本仓库只公开【愿景层 / 算法层 / 规则层】。
- 私钥、SEAL 生成逻辑、确认码派生方式、本地部署明文配置
  一律不在此仓库，也不会应任何请求提供。
- 本仓库文件不构成对作者本人的身份认证；作者身份认证在主权层完成。

## 5. 公开首页（反向链接）
https://uid9622.notion.site

## 6. 本地实例导航（部署实例补充）
- 系统状态与待办：STATE.md
- 项目配置与启动：.codebuddy/CODEBUDDY.md
- 治理文档全集：01_protocols/
- **无后台治理链（焊死·P0）**：无后台审批团公开决策 `governance/protocols/P1_core/LH-NO-BACKEND-COMMUNITY-COUNCIL-v1.0.md`（怎么表决）→ 三色治理 v2.1 `governance/protocols/P1_core/LH-TRICOLOR-GOVERNANCE-v2.1.md`（什么该表决·按什么颜色通行）—— 系统无后台·账号无人可锁·决策绑定声誉·中国主权红线 · 任何修改需 UID9622 签章 · 指挥层 `lh gov`
- 命令总目：.codebuddy/COMMAND_INDEX.md

## 6.5 新代码 CNSH 命名闸口（2026-09-01 焊死 · 只补缺不改心血）
- **任何新增 `.py` 文件必须使用 CNSH 中文命名（文件名含汉字），否则不入库**。存量英文命名脚本（约 3.5 万）不强制改造，只做 A-BOM 备案。
- **强制钩子**：`.git/hooks/pre-commit` 已装——commit 时自动检查本次新增 .py，违规即拦截（`--no-verify` 显式绕行须 P05 审计留档）。
- **闸口命令**：`python3 08_BIN/lh_cnsh_gate.py --pre-commit | --repo | --abom | --self-check`
  - `--pre-commit`：入库瞬间硬拦截（git diff --cached 新增文件）
  - `--repo`：全仓库巡检（软报告，存量未跟踪文件不误伤）
  - `--abom`：A-BOM 备案统计存量命名分布
- **配套**：算法/配置常量统一从 `packaging/longhun_cli/longhun_cli/constants.py` 引用（捆绑规则#4）。

## 6.6 收款入口规则（2026-09-04 焊死 · 只带入口·不带具体地址）
- **任何对外交付物（README/指南/官网页面/API 文档/静态页）底部自动带收款区块**：二维码 + 地址 + 说明（纯自愿·零黑箱）。命令：`lh wallet qr` 刷新二维码 / `lh wallet address` 取地址。
- **地址永不硬编码**：统一读 `~/.longhun/crypto.json`（SOL/USDC 自托管·权限 600·种子仅本地）。周一公司账户落地 = 改 crypto.json + 重跑 `lh wallet qr`，机制零代码改动。
- **任何新开的对外服务（API/MCP/Webhook）health 端点暴露 `donate` 字段**（读 crypto.json，无配置返回 null 不报错）。
- **种子/私钥永不写入任何对外文档、日志、聊天、远端**。`lh wallet show-seed` 仅限 UID9622 本机抄录。
- 已内置：topo serve 8762（图谱页+统一看板收款区块）· `lh health` 第 10 项 · MCP「龍魂 Wallet」3 只读工具。

## 6.7 内容自动消化闭环（2026-09-04 焊死 · 粘贴即消化 · 不再等"开始"）
- **目的**：老大贴什么，系统自己处理什么——自动判断类型/意图、自动带上下文、自动查缺口、自动给执行建议，不再每次等老大发令。
- **引擎**：`lh digest`（08_BIN/lh_digest.py · 数据 `~/.longhun/digest/`：inbox 收件 / done 原文冻结 / results.jsonl 结果 / diary 每日日记）。
- **AI 触发铁律**：任何会话中，用户一次粘贴明显体量内容（代码/文档全文/聊天记录/外部报告/链接素材/规则草案）→ **自动**执行：
  1. 原文落盘收件箱 `lh digest inbox <文件>` 或 `lh digest add "<内容>"`；
  2. 跑 `lh digest`（消化全部待处理）或 `lh digest --file <路径>`；
  3. 按输出行动：缺口清单先处理 → 按分类+意图执行/归档/复盘 → 会话内一行确认结果（节能）。
- **小贴士判定**：简短问答/聊天不算粘贴消化对象；明显"要收进系统"的体量内容才算。
- **四步输出固定含**：分类结果、意图识别、上下文命中、缺口清单、执行建议；结果自动归档 digest 日记（`~/.longhun/digest/diary/YYYY-MM-DD.md`）。
- **老大可直接说**："贴进去自己处理 / 这个你也收了 / 你看着办" → 同上自动消化。
- **纪律**：纯本地、零三方、按触发不常驻（节能协议）· 涉收款地址不硬编码（见 §6.6）· 涉及"焊死/新规则"须先报缺口再走修订流程。

## 6.8 社区质疑自动响应·数字人审核·每日巡航（2026-09-04 焊死）
- **目的**：icophy #1622（召回率未测 + 假阳性未测）制度化为自动闭环——社区有人质疑 → 系统自动验证 + **5 数字人协同审核** + 三色门控 + 自动回复，用户不用动。
- **引擎**：`lh challenge`（08_BIN/lh_challenge_parser.py v1.2）+ `lh strategy` + `lh response` + **`lh review`（08_BIN/lh_review_engine.py v1.0·数字人协同审核）** · 数据 `~/.longhun/validation/`（issues.jsonl + reports/issue_{id}/ + events.jsonl）+ `~/.longhun/review/`（reviews/ + dashboard.md）。
- **数字人审核门控（respond 自动触发·设计稿 v1.0）**：5 数字人并行审核（包青天 ASI-005 审计裁决 · 明鉴 DH-012 合规 · 匠心 DH-011 修复方案 · 诗仙 DH-013 回复草案 · 知行 DH-016 性能）→ 规则化启发式（基于验证硬数据·零三方·诚实不伪装智能）→ **🟢 全过→自动发布 / 🟡 1-2 不过→标记 needs_human 待人工复核 / 🔴 ≥3 不过→耻辱墙联动事件等待人工** → 最优解方案落 `reviews/{id}.json` · 看板 `lh review dashboard`。
- **每日巡航（launchd com.longhun.challenge-watch · 04:00）**：`lh challenge check --all` 扫描全部待回应质疑（pending/validating）→ 逐条自动完整响应（验证 → 数字人审核 → 发布回复 → 耻辱墙 validation 事件 → recap 自动归档）→ 无新质疑只留一行「无质疑」日志（节能协议）。
- **AI 触发铁律**：任何会话收到"社区 issue/PR 质疑"（信号词：阈值/基线/误报/召回/假阳性/复现/没测等）→ 第一反应 `lh challenge respond <issue-id>`（记录缺失先 `lh challenge parse <id>`；网络不可达则 `lh challenge add "<原文>" --issue <id>` 补录）→ 不解释、不争论、不手写回复、不过问审核。
- **铁律**：用数据回应质疑。0 命中 ≠ 检测器无效——必须先跑正负样本验证（TPR/FPR）再开口。token 读取链 env → Keychain(github.com/UID9622)；引擎强制直连 GitHub（已清代理）。launchd 环境无 shell env → 走 Keychain。
- **纪律**：respond 幂等（已 responded 跳过 · `--force` 重发）· 🟡/🔴 转 needs_human 不再被巡航自动碰（等人工·修复后重跑 respond 自动重审）· 发布 = 一次性真实评论（老大 2026-09-04 已授权直接发，不问"要不要发"）· `--repo` 是 lh.py 顶层保留字禁止透传 · `--skip-review` 跳过审核=慎用（P05 需知情）。

## 6.9 全局记忆系统默认组件（2026-09-04 焊死 · 全自动无感记忆）
- **目的**：系统自动记住一切（对话状态/任务断点/操作时间轴/全局状态/源码变更/外部生态感知），AI 永不"失忆重问"，老大说的话做的事自动沉淀。
- **组件全家桶**（全部默认开启·按触发零常驻）：
  - 🧠 `lh session` — 对话自动恢复（启动清单第5步自动读 `~/.longhun/session_context.json`）+ 任务/决策/待办保存
  - 📍 `lh checkpoint` — 任务断点续接（`~/.longhun/checkpoints/`）
  - 📡 `lh community` — 社区 Issue 周报聚合（`~/.longhun/community_status_weekly.md`）
  - 🗄️ `lh state` — 全局状态总线（`~/.longhun/state/global_state.json`·每 lh 命令自动计数·聚合 session/code/external）
  - ⏱️ `lh timeline` — 操作时间轴（`~/.longhun/timeline/YYYY-MM-DD.jsonl`·每 lh 命令自动追加·干支戳）
  - 🧬 `lh code` — **源码记忆**：每次 git commit 自动记录（post-commit 全局钩子已装 `/Users/zuimeidedeyihan/.git-hooks/post-commit`·数据 `~/.longhun/code_memory/<repo>/<hash>.json`·含干支/diff摘要/关联任务）
  - 🌐 `lh external` — **外部源码感知**：GitHub 龍魂生态仓库变更监控（watch/scan/status/diff·数据 `~/.longhun/external/`·新 commit 自动写 timeline+state+耻辱墙通知区 `~/.longhun/shame_wall/notices.jsonl`）
- **记录内容**：源码变更（谁改了什么/何时/干支/涉及文件/diff 摘要/当时任务）、外部生态事件、每次操作留痕。
- **AI 铁律**：不主动提起记忆系统（无感）；被问历史/变更/状态时直接 `lh code history` / `lh timeline search` / `lh state show` 查；写完代码提交后无需手动记（钩子自动）。

## 7. 底座锚点（不可变 · 德本审计第五问）
- **不可变铁律**：P0 天条（为人民服务/数据主权/隐私不传/零黑箱/不删只冻结/诚实不编造）不因环境、版本、需求变化而改变，以 CONSTITUTION.md 与 P0_ETERNAL_LOCK.md 为准。
- **底座不动**：CNSH 语法体系、DNA 追溯、三色审计、分层许可（思想层 CC BY-NC-SA 4.0 + 工程层 MulanPSL v2）为系统底座，任何重构/归一不得动摇其根基。
- **变量可动**：工程实现层（代码/部署/UI/目录结构）可随需求演进迭代，但每次变动必须挂 DNA、过审计、留追溯。

DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-AGENTS-ANCHOR-v1.1-UID9622

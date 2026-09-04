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

## 7. 底座锚点（不可变 · 德本审计第五问）
- **不可变铁律**：P0 天条（为人民服务/数据主权/隐私不传/零黑箱/不删只冻结/诚实不编造）不因环境、版本、需求变化而改变，以 CONSTITUTION.md 与 P0_ETERNAL_LOCK.md 为准。
- **底座不动**：CNSH 语法体系、DNA 追溯、三色审计、分层许可（思想层 CC BY-NC-SA 4.0 + 工程层 MulanPSL v2）为系统底座，任何重构/归一不得动摇其根基。
- **变量可动**：工程实现层（代码/部署/UI/目录结构）可随需求演进迭代，但每次变动必须挂 DNA、过审计、留追溯。

DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-AGENTS-ANCHOR-v1.1-UID9622

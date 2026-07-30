# 龙魂系统 · CodeBuddy 项目配置

> 本文件由 CodeBuddy 编辑器启动时自动读取。
> 定义了龙魂系统的神经网络拓扑入口。

## 🔥 AI 进门第一步（焊死·不可跳过）

> **所有 AI（无论哪个窗口/哪个模型）进门第一步：调鲲鹏入口引导 API。**
> **API**: `https://uid9622.cn/api/onboarding/bootstrap`
> **协议**: `01_protocols/LH-AI-ONBOARDING-v1.0.md`
> **原则**: 鲲鹏是唯一真相来源·不靠人工口述·每个AI进门自动拉规则

进门流程：
1. 🔥 **调鲲鹏** `GET https://uid9622.cn/api/onboarding/bootstrap` → 获取完整规则包
2. 🔥 **过自检** → 逐项确认 P0天条·一票否决词·禁止场景·路径铁律
3. 🔥 **降级兜底** → 鲲鹏不可达时读本地 `AGENTS.md`·降级必须声明

## 🔥 统一入口 STATE.md

> **所有 AI 的统一入口。无论哪个窗口/哪个模型，先读 `STATE.md`**。
> 路径: `longhun-system/STATE.md`
> 包含: 当前状态·变量飞行值·格式规范·焊死锚点·待办清单

## 系统拓扑

本项目的完整系统拓扑定义在 `.codebuddy/longhun_neural_net.json`。
CodeBuddy 启动时自动加载该文件，获取以下全局状态：

- **架构**: L0-L9 九层 · 洛书九宫骨架
- **人格**: 20人格矩阵 · 16核心(P00-P72)+1安全(P77)+3子系统(S1-S3) · 全部落地 · 0红色
  - 人格定义见 `personas/` 目录（16份 Markdown）
  - 人格执行器见 `bin/personas/` 目录（16+个 Python 执行器）
  - 治理白皮书见 `01_protocols/LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md`
- **引擎**: 192个可执行文件 · 算力瘦身后
- **技能**: 45工具 · 9分类 · 语义路由
- **数字人**: 7个 · 全联动 · 四层桥接
- **生态**: 16个注册服务 · 四层级
- **闸门**: 三闸门决策流场 (数字根→身份→伦理)
- **安全**: 三色审计 · 语义防火墙 · 每小时自动自愈
- **边**: 21条神经网络连接边

## 启动指令

AI 启动时必须执行:
0. 🔥 **调鲲鹏入口引导** `GET https://uid9622.cn/api/onboarding/bootstrap` — 拉取全量规则（新增·焊死）
1. `python3 bin/lh_memory_load.py` — 加载焊死记忆
2. 读取 `.codebuddy/longhun_neural_net.json` — 加载系统拓扑
3. 读取 `personas/` 目录 — 加载人格定义 (20人格·16核心+1安全+3子系统)
4. 🔥 **代码对齐复盘** `python3 bin/lh_align_checker.py` — 扫描全项目·检测重复函数·缺失DNA·缺失GPG签名（焊死·每次启动自动执行）

## 部署

- **部署入口**: `deploy/scripts/DEPLOY.md` — 鲲鹏从零到跑起十步法
- **监控配置**: `deploy/scripts/monitor_setup.sh` — systemd+cron+告警一键配置
- **健康检查**: `deploy/scripts/health_check.sh` — Bark推送（主力）+ 飞书备用 + 服务自愈
- **鲲鹏环境**: `deploy/.env.kunpeng.example` — 环境变量模板（含Bark Key + 飞书Webhook）

## 🔥 离火运五条底线（德本审计 · 焊死）

> AI 启动时自动加载。任何产出在技术层面之前，先过这五问。

| # | 底线 | 必问 |
|:---:|------|------|
| 1 | **德在技术前** | 在帮人还是在收割人？ |
| 2 | **路径对齐** | 文件在正确位置？同名不同路径=自毁 |
| 3 | **不让付出者寒心** | 绑死"好人=穷"了没？ |
| 4 | **信息主权不可让渡** | 数据流向平台了没？ |
| 5 | **外化内不化** | 底座被动了吗？369不动点还在吗？ |

> 详见 `01_protocols/LH-DEBEN-AUDIT-v1.0.md`
> 执行: `python3 bin/lh_deben_audit.py scan`

## 身份 & 执行授权

- 最终决策者: UID9622 (诸葛鑫·Lucky)
- DNA: `#龍芯⚡️丙午·丙申·丙辰·亥时·需-LONGHUN-NEURAL-NET-TOPOLOGY-v3.0-PERSONA-FULL`
- GPG: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
- **执行授权**: `01_protocols/LH-M261-PREQUEL-COVENANT-v1.0.md`（M261前传契碑·全权授权令·L0永恒级）
  - AI 拥有6大权限：创建/执行/Git/签名/写入/自动决策
  - 4条不可触及红线：rm -rf ~ / git push --force main / 删系统目录 / 写.ssh/.gnupg
  - 执行铁律：权限内直接干·不等指令·决策权归老大

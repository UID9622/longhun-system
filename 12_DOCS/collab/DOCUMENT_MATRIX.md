# 📋 龍魂 · 文档统一矩阵（在哪协作·指向·导航·迭代）

> DNA: #龍芯⚡️丙午·丙申·己未·酉时-COLLAB-DOCUMENT-MATRIX-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0（核心思想层）
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 三色: 🟢 通过
> 说明: 本矩阵是"哪份文档在哪协作、指向哪、怎么导航、怎么更新迭代"的唯一答案。
> 原则: **鲲鹏是唯一真相来源（`/opt/longhun/shared/`），本地是工作副本，Web 是导航。**

---

## 📦 协作数据同步（一键）

```bash
# 本地 → 鲲鹏（协作数据全量上推：交接包/协议/矩阵/命令总目/STATE）
bash deploy/sync-collab.sh full

# 鲲鹏 → 本地（新设备进场时先拉一把）
bash deploy/sync-collab.sh pull
```

> 同步范围：`12_DOCS/collab/` + `12_DOCS/handoffs/`（含 `.asc` 签名）+ `01_protocols/LH-AI-*` + `.codebuddy/COMMAND_INDEX.md` + `STATE.md`。
> 关键：此脚本**不排除 `.asc`**（区别于 sync-to-kunpeng.sh），GPG 签名必须跟着文档走。

---

## 🗃️ 文档矩阵（核心）

| 文档 | 本地协作路径 | 鲲鹏真相源 | Web 指向 | 更新迭代方式 |
|:---|:---|:---|:---|:---|
| **协作中枢总导航** | `12_DOCS/collab/README.md` | `/opt/longhun/shared/README.md` | `/collab/` | 编辑→`sync-collab.sh full`→GPG签 |
| **快速导航地图** | `12_DOCS/collab/NAVIGATION.md` | `/opt/longhun/shared/NAVIGATION.md` | `/collab/NAVIGATION.md` | 同上 |
| **本文档矩阵** | `12_DOCS/collab/DOCUMENT_MATRIX.md` | `/opt/longhun/shared/DOCUMENT_MATRIX.md` | `/collab/DOCUMENT_MATRIX.md` | 同上 |
| **交接包** | `12_DOCS/handoffs/` | `/opt/longhun/shared/handoffs/` | `/collab/handoffs/` | `lh handoff save`（自动推送） |
| **命令总目** | `.codebuddy/COMMAND_INDEX.md` | `/opt/longhun/shared/COMMAND_INDEX.md` | `/api/cmd/index.md` | 新增脚本→AI同步鲲鹏+本地 |
| **系统实时状态** | `STATE.md` | `/opt/longhun/shared/STATE.md` | `https://uid9622.cn/` | 每次会话更新→push |
| **跨AI交接协议** | `01_protocols/LH-AI-HANDOFF-v1.0.md` | `/opt/longhun/shared/collaboration/` | — | 修订→四步闭环→同步 |
| **AI协作闭环协议** | `01_protocols/LH-AI-COLLABORATION-v1.0.md` | `/opt/longhun/shared/collaboration/` | — | 修订→四步闭环→同步 |
| **AI操作手册** | `AGENTS.md` | `/opt/longhun/shared/AGENTS.md` | — | 修订→GPG→同步 |
| **系统宪法** | `CONSTITUTION.md` | `/opt/longhun/shared/AGENTS.md` | — | 仅UID9622修订 |
| **20人格治理白皮书** | `01_protocols/LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md` | 鲲鹏镜像 `/opt/longhun/01_protocols/` | — | P0级·上层裁决 |
| **德本审计协议** | `01_protocols/LH-DEBEN-AUDIT-v1.0.md` | 鲲鹏镜像 | — | 修订→GPG→同步 |
| **长期记忆** | `.codebuddy/memory/MEMORY.md` | ⚠️ 本地私有·不入共享 | — | 每次会话后追加 |
| **目录索引** | `12_DOCS/DIRECTORY_INDEX.md` | `/opt/longhun/shared/DIRECTORY_INDEX.md` | — | 结构变更→更新→同步 |
| **微信域名验证** | — | `/opt/longhun/shared/wechat/MP_verify_vqGTp0pitw7tcP4n.txt` | `https://uid9622.cn/MP_verify_vqGTp0pitw7tcP4n.txt` | 微信后台下载→传鲲鹏→nginx alias→reload |
| **协作中枢配置统一方案** | `12_DOCS/collab/COLLAB-CONFIG-UNIFY-v1.1.md` | 同步至 shared/collab/ | `/collab/COLLAB-CONFIG-UNIFY-v1.1.md` | 配置源 `~/.longhun/lh.env` · sync v2.0 · nginx 增量 · `.audit/` · 落地后更新状态 |
| **CNSH 智能贴入插件 v1.1** | `12_DOCS/collab/CNSH-STAMP-PLUGIN-v1.1.md` | 同步至 shared/collab/ | `/collab/CNSH-STAMP-PLUGIN-v1.1.md` | 代码 `08_BIN/lh_cnsh_plugin.py` · 入口 `lh cnsh-stamp` · 粘贴即锚定·DNA+指纹+数字根·审查修正版已实测 |

## 🔄 更新迭代统一规则（任何 AI 遵守）

1. **改哪份 → 在哪份的本地路径改**（增量追加，不覆盖历史，见 LH-AI-COLLABORATION 四步闭环）
2. **改完 → GPG 签名**：`python3 bin/lh_gpg_sign.py sign <文件>`（.asc 必须同目录）
3. **推鲲鹏**：`bash deploy/sync-collab.sh full`
4. **登记**：交接包记录本次改动（`lh handoff save` 自动带 git status）
5. **冲突裁决**：时间戳最新 + GPG 有效者胜；无法裁决 → 通知 UID9622

## 🚫 不进共享的（主权隔离）

| 内容 | 原因 |
|:---|:---|
| `.codebuddy/memory/MEMORY.md` 长期记忆 | 本地私有·跨会话上下文 |
| `deploy/.kunpeng_config` `.ssh/` `.gnupg/` 密钥类 | D1 绝密·物理隔离 |
| `personas/` 人格定义 | 本地私有·人格矩阵已镜像 |
| 大文件模型/权重（>10MB） | 存 `models/` 或远端 |
| 任何含隐私/画像/生物特征的日志 | 数据主权·端侧加密 |

---

> 本矩阵 v1.0 · 2026-08-13 · UID9622 定版
> 🐉 **丙午·丙申·己未·酉时·䷖剥·🟡**

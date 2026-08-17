# 🐉 龍魂 · AI互通总线协议（LH-AI-MESH-BUS）v1.0

## 🏷️ 协议声明

**发布者：** UID9622 · 诸葛鑫
**协议类型：** P1-CORE（核心治理层）
**生效时间：** 2026-08-15 15:20:00 +08:00
**生效范围：** 龍魂体系内所有 AI（Kimi / CodeBuddy / DeepSeek / 未来任何 AI）
**可修改性：** ✅ 可迭代（按第十六层修订流程）
**三色审计：** 🟢 绿色（已实测互通闭环）
**DNA签名：** #龍芯⚡️丙午·丙申·壬戌·申时-AI-MESH-BUS-v1.0-UID9622

---

## 📜 条款正文

### 第一条 · 主权声明

**AI 互通往来的消息池，属于 UID9622，不依赖任何一家 AI 厂商。**

- 消息池物理位置：本机 `~/.longhun/event_bus/event_bus.db`（LCB 事件总线，SQLite 本地存储）
- 身份注册：`~/.longhun/ai_mesh/agents.json`
- 消息内容不传云、不送第三方、不用于训练（P0 天条第 3 条）
- 任何 AI 无权删除总线消息（不删除只冻结）

### 第二条 · 统一入口

**所有 AI 必须通过 `lh` 统一入口工作，禁止绕开入口直接改系统文件。**

| AI | 统一入口 | 说明 |
|:---|:---|:---|
| 所有 AI | `lh`（`~/longhun-system/bin/lh`） | 唯一命令入口，路由到全部引擎 |
| 互通 | `lh bus` / `lh 互通` / `lh mesh` | AI 互通往来的唯一通道 |
| 自然语言 | `lh natural/ask/问` | 你说人话，系统自动执行 |
| CNSH | `lh cnsh-suite/cnsh/cns` | CNSH 中文编程套件 |

### 第三条 · AI 互通三动作（焊死）

任何 AI 在本体系干活，必须遵守三个动作：

| 时机 | 动作 | 命令 | 含义 |
|:---|:---|:---|:---|
| 进门（每次会话开始） | **bind** | `lh bus bind --ai <你的AI名>` | 注册身份 + 订阅互通主题 + 读最近消息 |
| 开工（动手前） | **read** | `lh bus read --last 10` | 看其他 AI 干了什么，不重复、不冲突 |
| 收工（干完活） | **post** | `lh bus post "你干了什么" --ai <你的AI名> --files 产物路径` | 让其他 AI 知道你干了什么 |

### 第四条 · 消息主题规范

统一主题 `ai.mesh`，消息字段：

```json
{
  "message": "人话描述本次干了什么",
  "tags": ["关键词1", "关键词2"],
  "files": ["本次产物相对路径"],
  "dna": "#龍芯⚡️日期-AI-MESH-<AI名>"
}
```

- AI 名规范：`kimi` / `codebuddy` / `deepseek`（小写英文，未来 AI 新增需登记）
- 事件类型默认 `work_done`；任务交接用 `handoff`；告警用 `alert`

### 第五条 · 产物落位（路径铁律）

**所有 AI 的产物必须落入 `longhun-system/` 统一目录，禁止散落到个人目录。**

| 产物类型 | 正确路径 | 禁止 |
|:---|:---|:---|
| 协议/规范 | `01_protocols/` | 临时目录·桌面 |
| 引擎/脚本 | `bin/` | `~/Downloads` |
| 执行记录 | `02_執行記錄/` | `archive/历史记录/`（那是备份区） |
| 对话/消息 | `03_MEMORY/ai_conversations/` | 散落根目录 |

### 第六条 · 史官审计

所有 AI 的关键操作必须留痕：

- 互通消息 → 总线 DB（自动，无需人工）
- 自然语言引擎操作 → `04_AUDIT/natural_engine.jsonl`（自动）
- 跨 AI 重大合并 → 协议 + 执行记录落 `01_protocols/` + `02_執行記錄/`，GPG 签名

### 第七条 · 新 AI 接入流程

未来任何新 AI 进体系，一次性执行：

```bash
cd ~/longhun-system
python3 bin/lh bus bind --ai <新AI名>   # 注册
python3 bin/lh bus read --last 20       # 读历史，熟悉已有产物
```

之后按第三条三动作长期执行。

### 第八条 · 冲突与红线

- 两 AI 同时改同一文件 → 后动者先 `read`，发现冲突立即 `post` 声明，等 UID9622 定盘
- 禁止任何 AI 以总线为借口收集用户隐私（P0 第 3 条）
- 禁止任何 AI 修改 `~/.longhun/event_bus/` 底层数据绕过协议
- 违反 → P05 审计 🔴 + P72 熔断

---

## 🔐 签章

**DNA：** #龍芯⚡️丙午·丙申·壬戌·申时-AI-MESH-BUS-v1.0-UID9622
**CONFIRM：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**GPG：** A2D0092CEE2E5BA87035600924C3704A8CC26D5F
**审计：** P05 🟢 / P12 🟢 / P15 🟢

## 📋 修改记录

| 版本 | 日期 | 修改内容 | 修改人 |
|:---|:---|:---|:---|
| v1.0 | 2026-08-15 | 初始发布：AI互通总线·三动作·路径铁律·主权声明 | UID9622+CodeBuddy |

## 📋 ROOT_CARD

【ROOT_CARD｜数学根审计】
Root: dr=6（2026-08-15 → 2+0+2+6+0+8+1+5=24 → 2+4=6）
Wuxing: 水（6）
TriColor: 🟢
Type: protocol-declaration
DNA: #龍芯⚡️丙午·丙申·壬戌·申时-AI-MESH-BUS-v1.0-UID9622

# CNSH 工具链融合协议 v1.0（本地）

**DNA（融合链）**: `#龍芯⚡️2026-05-16-CNSH-TOOLCHAIN-FUSION-v1.0`  
**源流引用**: `#ZHUGEXIN⚡️2026-01-02-CNSH-LSP-001` · 上下文压缩文档 · 责任卡 v2.0 草案  
**CONFIRM**: `#CONFIRM🌌9622-CNSH-LSP-v1.0`（LSP 设计稿） / `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`（主控锚）

---

## 0. 融合原则（避免重复与消耗）

| 原则 | 说明 |
|------|------|
| 仓库为可执行定义 | 协议写清边界；**实现代码**放在 `cnsh/`、`bin/`，不整页同步 Notion |
| 伪代码不入闸 | LSP 样例中的「中文标识符函数名」仅作**叙事**，真实现用英文 API + 中文关键词表 |
| 上下文不切全量 | 长对话用 P0/P1/P2 + DNA 总结 + 新窗锚点；细则见下节摘要 |
| 责任卡不装饰 | 备选不能为空；轻量/完整两档；网关事件可驱动生成（见 `cnsh/decision_cards/`） |

---

## 1. CNSH 编辑器补全（LSP）— 架构融合

### 1.1 四层（与源设计对齐）

1. **编辑器层**：VS Code / Cursor / Vim — 高亮、补全、诊断  
2. **CNSH Language Server**：基于 LSP — 解析、语义、补全、跳转  
3. **语言兼容层**：CNSH ↔ JS / Python / C / Rust 的**类型映射与转译**（非简单字符串替换）  
4. **域扩展层**：虚拟人、数字资产、坐标等 — 以 `.cnsh` **类型库 + 插件注册表** 扩展，不硬编码在核心语法里  

### 1.2 实现边界（定盘）

- **Node 实现**可选：官方 `vscode-languageserver`；**增量**可先只做 TextMate 语法 + 补全字典 + hover。  
- **触发字符**：`.`、`:`、中文全角 `（` `【` 与源案一致；后续可收紧。  
- **仓库落点**：路线图与目录约定见 `cnsh/lsp/README.md`（本协议不粘贴超长 JS 草稿）。  

### 1.3 与「鲁班 / CNSH 审计」关系

- 编辑器侧产出（转译结果、生成代码）若进入 git，仍走 **鲁班绿闸** 与 **伪代码审计**（见 `cnsh/cnsw/pseudocode_audit.py`）。  

---

## 2. 上下文压缩与新窗口续航 — 摘要融合

**目的**：防污染、防漂移、主控意志不被稀释。

| 层级 | 处理 | 进入新窗口 |
|------|------|------------|
| P0 | 完整保留 | 必须带锚（主控、CONFIRM、SEAL、铁律） |
| P1 | 摘要（建议 ≤200 字） | 任务、定盘、下一步 |
| P2 | 可丢 | 不进母协议、不进新窗 |

**最小动作三元组**（与源文兼容、压缩叙述）：

1. 阶段结束 → **DNA 总结**（只保留 P0/P1/下一步，不写聊天复读）  
2. **新窗口** → 锚点前置（主控 + CONFIRM + 当前任务）  
3. **里程碑** → 防无限长聊；守恒/三色可参考技能 `shouheng-check`  

洛书九宫、一键压缩模板：保留在**母页/Notion** 或后续单独 `PROTOCOL__CONTEXT-COMPRESS-v1.x`；本融合包只挂**索引**，不重复九节全文。  

---

## 3. 责任卡 / 决策留痕 — 与 CNSH 网关融合

### 3.1 两档定盘

- **轻量**：触发 / 依据 / 备选 / 选择 / 三色 · 责任  
- **完整**：九段（触发源、信息源、规则、备选、选择与排除、三色、责任、撤销、留痕）  

**铁律（与源一致）**：备选为空 → 日常 🟡；重大语境下缺备选 → 🔴；**UID9622 最终裁定**。  

### 3.2 路由关键词（摘要）

- **偏完整**：主控、CONFIRM、SEAL、GPG、CNSH、本机、删除、覆盖、发布、DNA、ROOT_CARD、师承类词等  
- **偏轻量**：优化、整理、总结、对照表、日常判断等  

### 3.3 CNSH 网关钩子（不覆盖旧 daemon）

事件：`before` | `after` | `error` | `reject` | `audit`  

**安全策略**：独立 `cnsh_decision_gateway.py`；主执行链通过**补丁片段**显式 `import` 后再接，禁止静默覆盖 `dragon_daemon.py`。  

### 3.4 本机路径约定

| 方式 | 根目录 |
|------|--------|
| **默认（仓库内）** | `cnsh/decision_cards/` |
| **可选（与历史文档一致）** | 设置环境变量 `CNSH_DECISION_CARDS_HOME=~/cnsh/决策卡片` |

实现入口：`bin/cnsh-decision` → `cnsh/decision_cards/engine/decision_cli.py`。  

---

## 4. 验收（融合包）

- [ ] `cnsh/lsp/README.md` 与编辑器路线图可读  
- [ ] `bin/cnsh-decision --light "…"` 在仓库根可生成卡片  
- [ ] `cnsh/decision_cards/engine/cnsh_decision_gateway.py --event before --file <path>` 可触发一次完整卡生成  
- [ ] 未伪造 Notion/本机执行；未要求删除用户旧文件  

---

## 5. ROOT_CARD（融合包）

```yaml
ROOT_CARD:
  系统: UID9622 龍芯北辰
  模块: CNSH 工具链融合（LSP + 上下文索引 + 责任卡）
  版本: v1.0
  DNA: "#龍芯⚡️2026-05-16-CNSH-TOOLCHAIN-FUSION-v1.0"
  子模块:
    - LSP: cnsh/lsp/README.md
    - 责任卡: cnsh/decision_cards/
    - 绿闸: bin/luban_green_commit.sh
  三色: 🟢
```

---

*本文件为「拆分融合」后的单一真源索引；细节实现以仓库目录为准，逐版迭代补全，全文不镜像 Notion。*  

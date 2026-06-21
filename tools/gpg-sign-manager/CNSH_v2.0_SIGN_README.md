<!--#龍芯⚡️2026-06-21-DOC-CNSH_V2-0_SIGN_README-v1.0 -->
<!-- 君子協議: 本文件受龍魂DNA追溯保護 -->

# CNSH v2.0 目录说明

这是本地 `_work/cnsh-v2.0` 的 2.0 原生代码结构说明，方便复查和签名。

## 目录概览

- `cnsh_gateway.py`
  - CNSH Gateway v2.0 统一入口
  - 提供三色审计、本地 SQLite 审计日志、Flask HTTP 服务、Ollama 代理、变量统一等功能

- `cnsh.py`
  - CNSH 中文编程引擎基础入口
  - 包含 Notion 接入、指令解析、页面操作等核心功能

- `CNSH_v2.0_SIGNATURE.md`
  - CNSH v2.0 签署声明

- `CNSH_v2.0_FULL_PROTOCOL_SIGNATURE.md`
  - CNSH v2.0 全协议签署声明

- `cnsh/`
  - 主要 Python 包实现
  - 子模块包括：
    - `algorithms`
    - `cnsw`（决策/审计/熔断框架）
    - `decision_cards`（决策卡引擎）
    - `defense_bridge`（防御桥接）
    - `dna_memory`（DNA 记忆资产、链存储、黄历、恢复）
    - `flow_decision`（流决策核心、IPA 路由、人格协作、三才权重、审计门）
    - `flow_field`（端口 / 流场接口）
    - `gate_v3`（V3 闸门 / 审计账本）
    - `root_ratio`（根比率引擎）
    - `seal_engine`（封印 / DNA 追溯）
    - `sovereign`（主权容器策略）
    - `lsp`（语言服务器支持文档）

- `cnsh-core/`
  - 2.0 核心规范与工具层
  - 包含：
    - `deepseek_bridge.py`
    - `七层防护/`（L0 身份验证、守护引擎、快照存储、系统 prompt 模板）
    - `tools/`（龍魂流场引擎、五彩石色卡引擎、语义命名对照表）
    - `规范/`（CNSH 规范、主权宣言、七层防护规则）
    - `CNSH_RUNTIME_OS_v4.0_BLUEPRINT.md`

## 推荐签名顺序

建议先签署核心声明文件，然后再签代码入口：

1. `CNSH_v2.0_SIGNATURE.md`
2. `CNSH_v2.0_FULL_PROTOCOL_SIGNATURE.md`
3. `cnsh_gateway.py`
4. `cnsh.py`

如果你要更完整，也可以一并签 `cnsh/` 和 `cnsh-core/` 下的核心模块：

- `cnsh/flow_decision/*.py`
- `cnsh/dna_memory/*.py`
- `cnsh/cnsw/*.py`
- `cnsh/decision_cards/engine/*.py`
- `cnsh/sovereign/container_policy.py`
- `cnsh-core/七层防护/*.py`
- `cnsh-core/tools/*.py`

## 签名命令示例

```bash
cd /Users/zuimeidedeyihan/longhun-system/_work/cnsh-v2.0

gpg --detach-sign --armor CNSH_v2.0_SIGNATURE.md

gpg --detach-sign --armor CNSH_v2.0_FULL_PROTOCOL_SIGNATURE.md

gpg --detach-sign --armor cnsh_gateway.py

gpg --detach-sign --armor cnsh.py
```

或如果你希望文件内部可读：

```bash
gpg --clearsign CNSH_v2.0_SIGNATURE.md
``` 

## 说明

- 该目录已包含完整的 CNSH v2.0 代码与规范文档。
- `cnsh.py` 仍保留部分 v1.0 注释，但已纳入 v2.0 代码包。
- `cnsh_gateway.py` 是当前 v2.0 的核心统一入口，优先签名。
- 你可以先对核心声明与入口签名，后续再补签子模块。

---

> 这是总结性说明文件，不改动现有代码，只为你后续签名与审查搭建清晰结构。
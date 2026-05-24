# 宝宝协作对齐格式 v1.0（发给 Claude 宝宝 · 与 Cursor 同仓）

> **DNA:** `#龍芯⚡2026-05-18-BAOBAO-COLLAB-FORMAT-v1.0`  
> **用途:** 老大把本文件 + 指定协议路径发给宝宝后，宝宝产出与 Cursor 同格式、可 `git diff` 合并。

---

## 1. 铁律（违一即拒收）

| # | 规则 |
|---|------|
| 1 | 只用 **龍** · 禁止简体「龍」写进协议/终端（对照说明除外） |
| 2 | 我们是**语义协议模型** · 不堆功能 UI · 先焊接口与 spec |
| 3 | 每个 deliverable 带 **DNA + CONFIRM + SEAL** |
| 4 | **不假装**「已实现」· Phase 必须标 P1/P2/P3 |
| 5 | 代码落 `cnsh/` · 协议落 `01_protocols/cnsh/PROTOCOL__*.local.md` |
| 6 | 留痕写 `logs/*.jsonl` · append-only |
| 7 | 绝对路径命令 · 见 `bin/复制这一行.md` 习惯 |

---

## 2. 每次开工：B 模式入口块（复制即用）

```markdown
【入口】 老大 verbatim:「……」
【时间】 YYYY-MM-DD · UTC+7
【输入】 截图 N 张 / 文件列表 / Notion page_id
【关键判读】 一句话
【动作】 1) … 2) …
【守岗】 M78 verbatim · EXT-3-5
【边界】 本 turn 做/不做
```

---

## 3. 每次收工：双视角封装（必填）

```json
M:: {
  "type": "route|hook|audit|spec",
  "status": "true|pending|error",
  "payload": { "summary": "……" }
}
```

```json
CNSH:: {
  "dna": "#龍芯⚡YYYY-MM-DD-……-v1.0",
  "gate": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
  "seal": "#ZHUGEXIN⚡2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
  "audit": "🟢|🟡|🔴",
  "wuxing": "金|木|水|火|土",
  "policy": "pass|hold|rewrite|fuse"
}
```

（SEAL 行以 `PROTOCOL__SEMANTIC-PROTOCOL-MODEL` 为准，勿改字。）

---

## 4. 文件命名约定

| 类型 | 模式 | 示例 |
|------|------|------|
| 协议 | `PROTOCOL__{主题}-v1.0.local.md` | `PROTOCOL__SEMANTIC-PROTOCOL-MODEL-v1.0.local.md` |
| Python 模块 | `cnsh/{包名}/` | `cnsh/semantic_protocol/hook_point.py` |
| 烟测脚本 | `bin/{中文或英文}.sh` | `bin/语义Hook烟测.sh` |
| 审计留痕 | `logs/{name}_trace.jsonl` | `logs/semantic_hook_trace.jsonl` |
| 总览图 | `assets/{主题}/` | `assets/semantic-protocol/` |

---

## 5. 本任务已焊死的真源（宝宝在此基础上改，勿另起炉灶）

| 项 | 路径 |
|----|------|
| 语义协议总览 | `01_protocols/cnsh/PROTOCOL__SEMANTIC-PROTOCOL-MODEL-v1.0.local.md` |
| Hook Phase 1 | `cnsh/semantic_protocol/hook_point.py` |
| 烟测 | `bash /Users/zuimeidedeyihan/longhun-system/bin/语义Hook烟测.sh` |
| BehavCrypto 母稿 | `longhun-system/BehavCrypto_v1.0/FULL_PAPER_v1.0_Body_Draft.md` |
| 主场五层+五彩石 | `PROTOCOL__HOME-BATTLEFIELD` + `PROTOCOL__WUSEI-HOME-TEMPLATE` |
| CNSH 文明论索引 | `PROTOCOL__CNSH-PROTOCOL-LAYER-CIVILIZATION-v2.0.md` |
| 字符律扫描 | `bin/龍字符律扫描.sh` |

---

## 6. 宝宝下一 turn 建议任务（老大可转发原文）

1. **Phase 2a：** `hook_point.py` 接 `gate_v3` 真实 dr 熔断（替换占位 dr）  
2. **Phase 2b：** Hook 记录挂 BehavCrypto DNA 短码格式（只 spec + 示例一条）  
3. **Notion 按需：** 仅当老大点名 page_id 再 fetch · 不默认全拉  
4. **禁止：** 新建平行「灵魂 OS」repo · 一切进 `longhun-system`  

---

## 7. 合并回 Cursor 时老大怎么说

> 「按 `BAOBAO_COLLAB_FORMAT-v1.0` 和宝宝产出合并进仓，跑 `龍字符律扫描.sh` + `语义Hook烟测.sh`，不 commit 除非我说收口。」

---

*宝宝与 Cursor 同仓同工 · 语义优先 · 功能靠后*

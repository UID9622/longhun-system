---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丁酉·癸未·子时·䷝离`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
> 干支时间戳: #龍芯⚡️丙午·丁酉·癸未·子时·䷝离
# 📡 龍魂账法 API 参考 v1.0

> 🔧 工程落地执行型（脚本/部署/API）· 底部卡片 ROOT_CARD 见文档尾
> DNA: #龍帳⚡️2026-09-04-LEDGER-API-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z · GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> 三色: 🟢 v1.0 实测（Python API + JSON-RPC 全链路）· 🟡 0 · 🔴 0

---

## 一、模块总览

| 项 | 值 |
|:---|:---|
| 引擎 | `08_BIN/lh_ledger.py`（Python 3.8+ · 标准库 · 零三方） |
| 命令入口 | `lh ledger ...` / `python3 08_BIN/lh_ledger.py ...` |
| 数据落点 | `~/.longhun/ledger/`（transactions/pending/meltdown + index） |
| 联动 | 三色审计 · 耻辱墙 · lh brain · lh sense · lh health |
| 对外 | JSON-RPC（供 MCP / 数字人 / 子进程调用） |

---

## 二、Python API

### 2.1 常量与科目

```python
from lh_ledger import (
    ACCOUNTS, WITNESS, DNA_PREFIX,
    validate_account, get_account_type, get_witness,
    gen_dna, calc_hash,
    LonghunTransaction, LedgerManager,
    rpc_dispatch,
)
```

**`validate_account(code) -> (bool, name, dir)`**
科目代码是否存在、科目名称、借贷方向（借/贷）。

**`get_account_type(code) -> str`**
科目类型：资产/负债/权益/收入/费用（未知科目返回 `未知`）。

**`get_witness(tx_type) -> (witness_str, known_bool)`**
交易类型（T1-T12）→ 见证人格。未知类型写耻辱墙 `ledger_witness_fallback` 并返回默认见证（P00）。

### 2.2 DNA 与哈希

```python
def gen_dna(date: str, dr_code: str, cr_code: str,
            amount: str, seq: int) -> str
# → "#龍帳⚡️2026-09-04-1001-3201-1条-001-UID9622"
# 校验: 科目存在 / 日期 YYYY-MM-DD / 序号 0-999 三位补零
# 异常: ValueError

def calc_hash(dna: str, dr_code: str, cr_code: str,
              amount: str, timestamp: str) -> str
# → SHA256(dna|dr_code|cr_code|amount|timestamp)[:8].upper()
# timestamp 传当前时间=实时; 传固定时间=可复现
```

### 2.3 交易记录 `LonghunTransaction`

```python
tx = LonghunTransaction.create("T1", "2026-09-04", "1001", "3201",
                               "1条", 1, note="测试铁律")
# 自动补齐: dna / hash / witness / extra.hash_ts

tx.verify()          # -> (ok: bool, problems: list)  自校验
tx.ledger_line()     # -> str  标准账簿行（人类可读）
tx.to_json()         # -> dict JSON 序列化
tx = LonghunTransaction.from_json(d)   # JSON → 对象
```

字段：`tx_type / date / dr_code / cr_code / amount / seq / note / dna / hash / witness / status / extra / created_at`

### 2.4 账簿管理器 `LedgerManager`

```python
mgr = LedgerManager()

# 记账（自动三色审计）→ (status, obj)
status, obj = mgr.add("T1", "1001", "3201", "1条", note="...", date="")
#   status: GREEN(已入账) | YELLOW(待审队列) | RED(熔断拒绝) | ERR(参数错)
#   obj:    LonghunTransaction 或错误信息 str

mgr.get(seq=1)              # 按序号查询
mgr.get(dna="#龍帳...")      # 按 DNA 查询
mgr.get(date="2026-09-04")  # 按日期查询
mgr.pending()               # 待审队列（PENDING）
mgr.confirm(seq)            # 复核待审 → 重新审计入账
mgr.list_tx(limit=20)       # 最近交易
mgr.verify_all()            # -> (txs, results, fails, dup_seq)
mgr.balance()               # -> {balance:{资产..费用}, detail, tx_count, identity_ok}
mgr.export("json|csv|md")   # -> str
```

**audit extra 字段**（入账后自动注入）：

```python
tx.extra = {"hash_ts": "...",           # 哈希时间戳（verify 用）
            "audit_color": "🟢",        # 三色审计结果
            "audit_reason": "..."}      # 审计理由
```

### 2.5 函数式入口

```python
# 感知识别文本 → 记账要素（OCR/ASR 链后）
elems = parse_ledger_text(text, dr_code="", cr_code="", amount="",
                          date="", tx_type="T9")
# -> {dr_code, cr_code, amount, date, note, tx_type}

# 耻辱墙账本事件
wall_events = _wall_events(limit=20)   # 读 ~/.longhun/shame_wall/notices.jsonl

# JSON-RPC 单发
resp = rpc_dispatch({"method": "balance"})     # -> dict
```

---

## 三、JSON-RPC 接口（供 MCP / 数字人）

调用方式：

```bash
lh ledger rpc '{"method":"balance"}'
python3 08_BIN/lh_ledger.py rpc '{"method":"add","params":{...}}'
```

响应统一：`{"ok": true, ...}` 或 `{"ok": false, "error": "..."}`

### 3.1 方法表

| method | params | 返回 |
|:---|:---|:---|
| `add` | `{tx_type, dr_code, cr_code, amount, note?, date?}` | `{status: GREEN/YELLOW/RED, tx: {...}}` |
| `get` | `{seq? / date? / dna?}` | `{txs: [...]}` |
| `list` | `{limit?}` | `{txs: [...]}` |
| `verify` | `—` | `{total, fail, dup_seq, details: [{seq, ok, problems}]}` |
| `balance` | `—` | `{balance: {...}, detail, tx_count, identity_ok}` |
| `export` | `{format: csv/json/md}` | `{content}` |
| `gen_dna` | `{date?, dr_code, cr_code, amount, seq?}` | `{dna}` |
| `calc_hash` | `{dna, dr_code, cr_code, amount, timestamp}` | `{hash}` |

### 3.2 示例（实测 2026-09-04）

```bash
$ lh ledger rpc '{"method":"balance"}'
{
  "ok": true,
  "balance": {"资产": 67.0, "负债": 0.0, "权益": 1.0,
              "收入": 66.0, "费用": 0.0},
  "identity_ok": true,
  "tx_count": 2
}

$ lh ledger rpc '{"method":"add","params":{"tx_type":"T4","dr_code":"1001",
    "cr_code":"4101","amount":"66元","note":"第一笔奉献"}}'
{ "ok": true, "status": "GREEN", "tx": { "dna": "#龍帳⚡️...", "hash": "870CE891", ... } }

$ lh ledger rpc '{"method":"gen_dna","params":{"dr_code":"1001",
    "cr_code":"3201","amount":"1条","seq":9}}'
{ "ok": true, "dna": "#龍帳⚡️2026-09-04-1001-3201-1条-009-UID9622" }
```

### 3.3 供 MCP / 数字人接入

MCP 工具只需 `exec_command("lh ledger rpc '<json>'")` 或
`subprocess.run([sys.executable, "08_BIN/lh_ledger.py", "rpc", payload])`。

**建议接线**（子进程·防 import 副作用）：

```python
import json, subprocess, sys
def ledger_call(method, **params):
    payload = json.dumps({"method": method, "params": params},
                         ensure_ascii=False)
    r = subprocess.run([sys.executable, "08_BIN/lh_ledger.py", "rpc", payload],
                       capture_output=True, text=True, timeout=60)
    return json.loads(r.stdout or "{}")
```

---

## 四、错误与异常

| 场景 | 行为 |
|:---|:---|
| 科目不存在 / 借贷方向错 | `ERR`（不入账不审计） |
| 日期格式错 / 序号超界 | `ValueError`（DNA 层） |
| 🟢 | 入账 · 耻辱墙 `ledger_tx` |
| 🟡 | pending.jsonl · 耻辱墙 `ledger_yellow_draft` |
| 🔴 | 拒绝 · 耻辱墙 `ledger_red_meltdown` · meltdown.log |
| 审计引擎缺失 | 内置黑词降级（注明来源·不装全量审计） |
| 耻辱墙/brain 写入失败 | 打印 ⚠️ · 不影响记账主流程 |

---

## 附 · ROOT_CARD

```
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
DNA: #龍帳⚡️2026-09-04-LEDGER-API-v1.0-UID9622
协议: CC BY-NC-SA 4.0（核心思想层）
三色: 🟢 实测 · 🟡 0 · 🔴 0
```

```json
{
  "dna": "#龍芯⚡️丙午·丁酉·癸未·子时·䷝离",
  "license": "AI_TRAINING_PROHIBITED",
  "terms": {
    "ai_training": false,
    "rag_use": false,
    "commercial_use": false,
    "citation_required": true,
    "derivative_works": false
  },
  "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```

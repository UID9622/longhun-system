# 新代码闸口绕行审计留档 · 2026-09-04 · CNSH 生态 v1.0 入库

> 依 AGENTS.md §6.5 + 2026-09-03 老大裁决 Q2（--no-verify + P05 审计留档）
> DNA: #龍芯⚡️2026-09-04-CNSH-GATE-BYPASS-CNSH-ECO-V1.0-UID9622
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰

## 一、绕行原因（三类合理冲突）

1. **标准 Python 包模块命名**（`packaging/cnsh-stdlib/cnsh_std/`）：io/http/time/crypto/dna/audit/fuse/topo/memorial + `__init__.py`。
   PyPI 标准打包（pyproject.toml），`import cnsh_std.io` 依赖 ASCII 标识符；中文模块名 Python3 虽可 import 但破坏 PyPI 生态惯例与工具链兼容性。
2. **pytest 测试发现惯例**（`packaging/cnsh-stdlib/tests/test_all.py`）：`test_*.py` 是 pytest 收集器默认模式，改名即失 pytest 发现能力（本文件已做直跑+pytest 双模式兼容）。
3. **CLI 工具链命令名**（`08_BIN/cnsh.py` + `cnsh_jsgen.py` + `cnsh_pm.py`）：统一 CLI 入口 `cnsh` 命令（build/run/test/pm/docs/init），对外命令名/引擎名 ASCII 属品牌命名（与 9/4 上午 lh_publish.py 同款裁决：工具链英文名惯例延续）。

## 二、绕行文件清单（新增英文命名 .py）

| 文件 | 说明 |
|:---|:---|
| `08_BIN/cnsh.py` | CNSH 统一 CLI（6 子命令单一入口） |
| `08_BIN/cnsh_jsgen.py` | CNSH → JS 代码生成器 |
| `08_BIN/cnsh_pm.py` | CNSH 包管理器（publish/install/list/registry） |
| `packaging/cnsh-stdlib/cnsh_std/*.py`（10 个） | CNSH 标准库 9 模块 + `__init__.py` |
| `packaging/cnsh-stdlib/tests/test_all.py` | 标准库自测（直跑+pytest 双模式） |

## 三、GPG 签名 + 验证

- 全部源文件已 `lh_gpg_sign.py sign --force`，`.asc` 配对随行（含 docs 生成器 generate_site.py）。
- 全链实测绿：cnsh test 5/5 · build 双目标 `你好，龍魂！` · init→run `你好，龍魂 CNSH 世界` · stdlib 直跑 9/9 + pytest 1 passed · pm publish→install→list→registry→run 全流程 · docs 6 页 · lint 0。

## 四、补充说明

- 闸口只拦「新增入库英文 .py」；本批为一次性生态整体入库，入库后后续增量维护（M 修改）不再触发 A 过滤。
- CNSH 语言自身文件（.cnsh）不受此闸口约束；中文语法由运行时保障。

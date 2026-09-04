# 新代码闸口绕行审计留档 · 2026-09-04

> 依 AGENTS.md §6.5 + 2026-09-03 老大裁决 Q2（--no-verify + P05 审计留档）
> DNA: #龍芯⚡️2026-09-04-CNSH-GATE-BYPASS-OPEN-PUBLISH-UID9622
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰

## 一、绕行原因

- `08_BIN/lh_publish.py`：**统一对外发布工具链 v1.0**（发布工具引擎）。
- 属 08_BIN 既有 `lh_*` 英文引擎体系延续（存量 lh_topo/lh_model/lh_bench 等引擎均英文命名，A-BOM 备案存量不强制改造，与 9/3 收口 53 个引擎同款裁决）。

## 二、绕行文件清单（新增英文命名 .py）

| 文件 | 大小 | 说明 |
|:---|:---|:---|
| `08_BIN/lh_publish.py` | 27KB | 统一对外发布工具链：`announce/status/dashboard/rollback/templates` · GitHub Issue+官网横幅+README 一键分发 · git PR→bot approve→merge · 发布日志 `~/.longhun/publish_log.json` |

## 三、GPG 签名

- 全部源文件已 `lh_gpg_sign.py sign --force`，`.asc` 与源同目录配对。
- 三色审计: 🟢 工具链端到端验证通过（issue 测试 #91→关闭 · web+readme 渠道实际跑通 git 链）

## 四、补充说明

- 本闸口仅拦「新增入库的英文 .py」；发布工具的日常 commit（README/portal/asc）不含新增 .py，不受影响。

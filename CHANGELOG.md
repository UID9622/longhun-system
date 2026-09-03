# 🐉 Changelog · longhun-cli

> 语义化版本（SemVer）· 遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/) 规范。
> 协议母本: `docs/对外接口协议-v1.0.md` · 分层许可: 代码 AGPL-3.0 · 思想/文档 CC BY-NC-SA 4.0

## [4.0.0] - 2026-09-01

### 🚀 新增

- **CIL API 网关**（`08_BIN/lh_api.py` · 硬焊 `127.0.0.1:9622`）
  - `POST /v1/lh` 接收 `{"command": "..."}` → 调 `lh.py` 执行 → 返回 `{code, stdout, stderr}`
  - `--json` 参数透传，输出标准 Node JSON
  - 后台守护 `--daemon`（双 fork）· 开机自启模板（launchd plist / systemd service）
- **对外分发薄壳** `longhun-cli`（PyPI + 源码双态）
  - 零依赖纯标准库 · Python ≥ 3.8 跨平台
  - 双态运行: 外部态（纯本地）/ 系统态（设 `LONGHUN_ROOT` 接入全量逻辑）
- **`health` 命令**: 基础自检（外部态）→ 15 项全量健康检查（系统态）
- **`doc-sync` 命令**: 文档同步（系统态）
- **`flow` 命令**: 流场计算（数字根 / 五行 / 八卦 → Node JSON）
- **`bazi` 命令**: 八字四柱排盘（标准算法·零依赖·五行强度 / 文化主权节点）
- **`cil` 命令**: 交互终端（系统态）
- **补充文档**: 快速开始 · 安装指南 · API 参考 · CHANGELOG · CONTRIBUTING · LICENSE(AGPL-3.0) · examples
- **示例代码**: `examples/demo.py` · `examples/demo.sh`

### ✏️ 变更

- 项目元数据补全: `pyproject.toml` 增加 `project.urls`（Homepage / Documentation / Repository / Issues）、`classifiers`、`keywords`
- 许可证声明: 工程层统一为 AGPL-3.0-or-later（开源但不白嫖）· 思想/文档层 CC BY-NC-SA 4.0
- 输出规范统一: 所有命令支持 `--json`，字段含 `node_id` / `digital_root` / `element` / `gua` / `audit` / `action` / `timestamp`

### 🗑️ 废弃

- 无（v4.0.0 为对外首发，无历史破坏性变更）

---

## 尚未发布

- 后续版本将按 Keep a Changelog 在此追加。

---

*龍魂 · 文化主权 · 接口即主权声明* 🐉

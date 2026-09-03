# longhun-cli · 龍魂 CIL 对外分发弹头 v4.0

<p align="center">
  <img src="https://img.shields.io/github/v/release/UID9622/longhun-system?label=Release&color=orange" alt="Release">
  <img src="https://img.shields.io/badge/GPG%20signed-A2D0092C...-green" alt="GPG Signed">
  <img src="https://img.shields.io/badge/tests-smoke%20passed-brightgreen" alt="Tests">
  <img src="https://img.shields.io/badge/license-AGPL--3.0-blue" alt="License">
</p>

龙魂系统文化主权命令行接口的**对外独立薄壳**。零依赖，`pip install` 即可用。

- **GPG 签名**：所有发布物附分离签名（`.asc`），密钥 `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`（诸葛鑫 | UID9622）
- **测试状态**：冒烟测试通过（version / health / flow / bazi / security / benchmark）
- **许可证**：代码 AGPL-3.0（开源但不白嫖）· 思想/文档 CC BY-NC-SA 4.0

## 安装

```bash
pip install longhun-cli
# 或本地安装
pip install dist/longhun_cli-4.0.0-py3-none-any.whl
```

## 使用

```bash
lh version          # 版本
lh health           # 自检（无系统树时为基础自检，有系统树时转发 lh_health.py）
lh health --json    # JSON 输出（可解析）
lh flow "龙魂对外首发"  # 流场计算（数字根/五行/八卦，纯本地算法）
lh flow "龙魂对外首发" --json
lh bazi --date 1990-01-01 --time 08:00  # 八字四柱排盘（标准算法·零依赖）
lh bazi --date 1990-01-01 --time 08:00 --json
lh security --json  # 安全自检（端口绑定/签名/文件泄露）
lh benchmark --json # 性能基准（排盘/流场/网关QPS）
lh cil              # 交互式终端（需 LONGHUN_ROOT 指向龙魂源码树）
```

## 双态设计

- **外部态**（未设置 `LONGHUN_ROOT`，系统树不可达）：
  `health`/`flow`/`version` 全部可用，纯本地零依赖。
- **系统态**（`LONGHUN_ROOT` 指向龙魂源码树，如 `~/longhun-system`）：
  `health`/`cil`/`doc-sync` 自动转发至系统内完整逻辑。

```bash
export LONGHUN_ROOT=~/longhun-system
lh cil              # 进龙魂 CIL 交互终端
lh doc-sync --json  # 文档同步
```

所有命令均支持 `--json`，输出为标准 Node JSON（见 `docs/对外接口协议-v1.0.md`）。

# UID9622 责任卡（决策留痕）— 仓库内默认实例

**协议**: `01_protocols/cnsh/PROTOCOL__CNSH-TOOLCHAIN-FUSION-v1.0.local.md`

## 根目录

- **默认**: 本目录 `cnsh/decision_cards/`（随仓库走）
- **可选**: 环境变量 `CNSH_DECISION_CARDS_HOME` 指向例如 `~/cnsh/决策卡片`

## 命令

```bash
bash /Users/zuimeidedeyihan/longhun-system/bin/cnsh-decision --light "测试轻量"
bash /Users/zuimeidedeyihan/longhun-system/bin/cnsh-decision --full "CNSH 网关接入"
bash /Users/zuimeidedeyihan/longhun-system/bin/cnsh-decision --list
```

网关（不绑 daemon）：

```bash
python3 /Users/zuimeidedeyihan/longhun-system/cnsh/decision_cards/engine/cnsh_decision_gateway.py \
  --event before --file /path/to/x.cnsh --status pending --detail "执行前审计"
```

## 目录

```text
decision_cards/
├── templates/     # 轻量 / 完整 Markdown 模板
├── engine/        # decision_cli.py · router · gateway
├── cards/daily|major
├── db/            # SQLite（首次生成时创建）
└── logs/
```

## 集成

在现有 `.cnsh` / dragon 执行链中**显式**调用 `cnsh_decision_gateway.invoke(...)`；禁止静默覆盖旧文件。

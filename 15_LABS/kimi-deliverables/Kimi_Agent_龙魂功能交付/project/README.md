**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-2b7814d3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍魂 · 信任核心（事实校验 + 自愈）

自包含 Python 包，**零三方运行时依赖**（仅标准库；测试用 pytest）。
核心信任层：DNA 生成与确认码闸门、append-only 审计、可信度公式、事实校验（三级纠正 + 熔断）；
自愈引擎：检测 → 分析 → 修复 → 验证 → 回滚 → 耻辱墙。

## 安装

### 直接用（零安装）

```bash
cd <项目根>            # 仓库根 = 包根
python3 -m longhun_trust.selfheal --once
```

### macOS launchd 一键部署（🟡 仅 macOS 真机可验证）

```bash
bash scripts/install.sh      # 幂等；用 $HOME 动态生成 plist 并 launchctl bootstrap
bash scripts/uninstall.sh    # 幂等卸载；日志/审计按只增不删协议保留
```

- plist 由 `scripts/com.longhun.selfheal.plist.template` 生成（sed 替换 `__HOME__`/`__PROJECT_ROOT__`，禁硬编码用户名），
  落到 `~/Library/LaunchAgents/com.longhun.selfheal.plist`，KeepAlive + RunAtLoad。
- 运行日志写到 `$LONGHUN_HOME/logs/`（`LONGHUN_HOME` 默认 `~/.longhun`）。

## CLI 用法

```bash
python3 -m longhun_trust.selfheal --once [--execute] [--confirm-code X] [--project-root P] [--log-dir D] [--ports 8080,9090]
python3 -m longhun_trust.selfheal --status [--project-root P]
```

- `--once`：运行一轮 detect → plan → heal，打印报告 JSON。
- `--status`：读取最近一次 HEAL_REPORT 审计并以其状态退出（状态值越界一律按 🔴2 处理）。
- `--log-dir`：扫描该目录 `*.log` 尾部 100 行错误关键字与超大日志（>50MB）。
- `--ports`：逗号分隔端口列表，仅 warn 级检测（lsof 缺失/无监听不判 critical）。
- 默认 **dry_run**（干跑，只记录不执行）；加 `--execute` 才真执行安全策略。
- 回滚是破坏性操作：必须 `--confirm-code` 过闸门，错误码抛 `ConfirmCodeError`。

### 三色退出码（退出码 = HealStatus 值）

| 退出码 | 语义 | 含义 |
|---|---|---|
| 🟢 0 | HEALTHY | 通过：无问题，或真执行后复检干净 |
| 🟡 1 | PARTIAL | 待确认或部分修复：干跑发现问题 / 有 ESCALATE / 未给确认码保持现状 |
| 🔴 2 | FAILED | 失败或熔断：连续 max_attempts 次修复失败，上耻辱墙 |

## 诚实边界（焊死）

- **安全策略才可自动执行**：`dep_missing`（`pip install -- <pkg>`，包名白名单
  `^[a-zA-Z0-9][a-zA-Z0-9_.-]*$`，拒绝 `-e`/`--user`/`..`/空串）、
  `service_down`（有重启命令才记为可执行，无命令直接升级人工）、
  `log_oversize`（>50MB 轮转截断）、`stale_lock`（删除）。
- **断言失败/业务逻辑错误绝不自动改代码**：一律 `strategy="ESCALATE"`，
  升级人工 + 写入耻辱墙 `$LONGHUN_HOME/08_STATE/shame_wall.jsonl`。
- 快照回滚：真执行前打 `git tag lh-snapshot-<ts>`（非 git 仓库记审计 `SNAPSHOT_SKIPPED`）；
  dirty worktree（含未跟踪文件）先把工作区全部内容提交为快照 commit 再打 tag，
  快照失败则 fail-closed 拒绝执行修复动作；回滚用 `git reset --hard <tag>`，禁用 HEAD^。
  回滚后报告 `fixed` 清零并附 `rollback_note`：git 之外的副作用
  （已装包/已轮转日志/已删未跟踪文件）无法自动撤销。
- 端口检测仅 warn 级（lsof 缺失/无监听不判 critical，沙盒友好）。

## 可信度公式

**C = 0.4·F + 0.3·S + 0.3·K**，**C < 0.7 → 待确认（必问）**。

- **F 新鲜度**：`clamp(1 - age_days/90, 0, 1)`，90 天线性衰减至 0。
- **S 来源权重**：FOUNDER 1.0 / SYSTEM 0.8 / COMMUNITY 0.5 / UNKNOWN 0.2。
- **K 确认状态**：CONFIRMED 1.0 / UNCONFIRMED 0.3 / DISPUTED 0.0。

## 测试

```bash
LONGHUN_HOME=$(mktemp -d) python3 -m pytest tests/ -v
```

锚点案例：用户 2008 年退伍，2026 年自称"退伍 16 年" → 引擎主动纠正为 18 年，
全程审计留痕；同一字段 3 次未解决矛盾即熔断（CircuitBreakerTripped）。

## 已知限制

- **O2：heal 每轮两次 pytest 开销**。真执行路径下 detect 与复检各跑一次完整
  pytest 子进程（超时各 120s），大测试套件下每轮自愈最坏约 4 分钟；当前未做增量检测。
- **O5：pytest 退出码 5 视为健康**。退出码 5（未收集到任何测试）与 0（全绿）同等
  视为无问题——空项目不算错误，但也意味着"测试文件被误删光"不会被检测通道发现。

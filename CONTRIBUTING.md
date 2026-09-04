# 🐉 Contributing · 龍魂 longhun-cli 贡献指南

> 归属名: **诸葛鑫 | UID9622 · 龍芯北辰** · GPG: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
> 分层许可: 代码 AGPL-3.0 · 思想/文档 CC BY-NC-SA 4.0

---

## 1. 提交规范

### 1.1 分支与流程

```bash
# 1. 从主线拉分支
git checkout -b feat/<功能名>

# 2. 小步提交（一次一个逻辑变更）
git add <文件>
git commit -m "<类型>: <一句话说明>"

# 3. 推送到自己的分支并提 PR
git push origin feat/<功能名>
```

### 1.2 Commit Message 规范

```
<类型>: <摘要>（≤72 字符）

<可选>详细说明 / 影响面 / 验证方式
```

| 类型 | 用途 |
|:---|:---|
| `feat` | 新功能 |
| `fix` | 修复 |
| `docs` | 文档 |
| `refactor` | 重构（不改变行为） |
| `perf` | 性能 |
| `test` | 测试 |
| `chore` | 构建/工具链 |
| `license` | 许可证/归属名变更 |

### 1.3 不变量（提交前必查）

- 无硬编码密钥 / 令牌（一律走 `lh_vault` / 环境变量）
- 无 `~/Downloads`、`/tmp` 等临时路径产出
- 新增/修改文件带文件头（DNA · 创建者 · 归属名 · 协议）
- 关键阈值注明出处（哪条协议 / 哪个公式）

---

## 2. GPG 签名要求（🔒 硬性）

所有**核心文件**与**对外发布物**必须 GPG 分离签名，未签名 → 评审否决（GATE-11）。

```bash
# 签名
python3 bin/lh_gpg_sign.py sign <文件或目录>
# 或
gpg --batch --yes --armor --detach-sign -u A2D0092CEE2E5BA87035600924C3704A8CC26D5F <文件>

# 全量补签
python3 bin/lh_gpg_sign.py sign .

# 发布前全量验证
python3 bin/lh_gpg_sign.py scan .
# 或
gpg --verify <文件>.asc <文件>
```

签名产出规则:
- 新建/修改 `.md` `.py` `.sh` 等核心文件 → 自动补签
- `.asc` 与源文件同目录，不可分离
- 发布产物（whl / tar.gz / 文档）随 GitHub Release 一并上传 `.asc`

---

## 3. 三色审计流程（交付前必过）

| 色 | 含义 | 放行条件 |
|:---|:---|:---|
| 🟢 | 全检查点通过 | 已实测（没跑过的代码不得标"已验证"） |
| 🟡 | 推演/待核 | 写明"待核什么 + 验证路径"，48h 内复查 |
| 🔴 | 红线/安全风险 | 立即停止 + 锁定 + 追溯 |

审计链路（十道闸口）:

```
GATE-01 身份闸 → 02 意图闸 → 03 语义闸 → 04 数字根闸 → 05 伦理闸
→ 06 数据闸 → 07 协议闸 → 08 人格闸 → 09 DNA闸 → 10 归档闸
→ GATE-11 GPG 签名闸（发布物）
```

每次交付附三色标记:
```json
{ "executor": "...", "trigger_time": "...", "audit_mark": "🟢",
  "risk_score": 0, "gpg_signature": "A2D0092...", "dna": "#龍芯..." }
```

---

## 4. COMMAND_INDEX 登记（新增命令/服务必做）

新增任何子命令、服务、端口后，必须更新 `.codebuddy/COMMAND_INDEX.md`:

| 登记位 | 内容 |
|:---|:---|
| 「🆕 最近更新」区 | 一行：方向 / 变更 / 结果（含日期） |
| 「三秒速查」命令表 | `lh <cmd>` 用法 + 引擎路径 + 说明 |
| 端口矩阵（若占端口） | 端口 / 服务名 / 绑定 / 状态 |

样例（三秒速查区）:

```markdown
| 🆕 **流场子命令** 🌀 | `lh flow "<文本>" [--json]` | 数字根/五行/八卦→Node JSON · 引擎 `08_BIN/lh_flow.py` · 新增2026-09-01 |
```

登记完重签 COMMAND_INDEX:
```bash
python3 bin/lh_gpg_sign.py sign --force .codebuddy/COMMAND_INDEX.md
```

---

## 5. 测试要求

```bash
# 冒烟（新增命令后必跑）
python3 -m longhun_cli.cli version
python3 -m longhun_cli.cli flow "龙魂对外首发" --json
python3 -m longhun_cli.cli bazi --date 1990-01-01 --time 08:00 --json
python3 -m longhun_cli.cli health --json

# JSON 可解析断言
lh flow "龙魂对外首发" --json | python3 -c "import sys,json; d=json.load(sys.stdin); assert d['element'] in '水火木金土'; print('OK')"
```

- 输出必须是**可解析 JSON**（机器可消费）
- 提交时附测试通过结果（三色标记 🟢）

---

## 6. 新代码 CNSH 命名闸口（🔒 硬性 · 2026-09-01 焊死）

> 任何新增 `.py` 文件必须使用 **CNSH 中文命名（文件名含汉字）**，否则不入库。

- **强制钩子**：`.git/hooks/pre-commit` 已装——commit 时自动检查本次新增 .py，违规即拦截（exit 1）
- **存量豁免**：存量英文命名脚本（约 3.5 万）不强制改造，只做 A-BOM 备案（`--abom`）
- **显式绕行**：`git commit --no-verify` 可绕过，但须 P05 审计留档

```bash
# 闸口命令
python3 08_BIN/lh_cnsh_gate.py --pre-commit   # 入库瞬间硬拦截（git diff --cached 新增文件）
python3 08_BIN/lh_cnsh_gate.py --repo         # 全仓库巡检（软报告）
python3 08_BIN/lh_cnsh_gate.py --abom         # A-BOM 备案（存量命名分布统计）
python3 08_BIN/lh_cnsh_gate.py --self-check   # 自检
```

**配套**：算法/配置常量统一从 `packaging/longhun_cli/longhun_cli/constants.py` 引用（捆绑规则#4）。

---

## 7. 许可与署名

- 代码（.py/.sh/构建产物）: **AGPL-3.0-or-later**
- 思想/文档（.md/协议/白皮书）: **CC BY-NC-SA 4.0**
- 全部产出强制实名归属: `诸葛鑫 | UID9622 · 龍芯北辰`
- 删 DNA 追溯码伪称原创 = 违约（耻辱柱）

---

## 8. 沟通

- 直接说 · 不绕 · 结论先行 · 三色标记（🟢🟡🔴）
- 不知道说不知道 · 推演标"推演" · 实测才标"已验证"
- 决策权归 UID9622 · 有分歧摆证据

*龍魂 · 文化主权 · 接口即主权声明* 🐉

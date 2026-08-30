# 🐉 龍魂浏览器开发环境 · CodeBuddy 集成设计 v1.1（对齐修正版）

```
DNA: #龍芯⚡️2026-08-25-BROWSER-CODEBUDDY-v1.1-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
父律链: #IRON-ACCEPT-TRAINING-MUST-LAND-NOT-SPEECH-v1.0 (M64) + #IRON-SMALL-MATTERS-JUST-DO-IT-NO-WAITING-v1.0 (M44)
上位: M77 原稿《CodeBuddy 集成设计 v1.0》+《五行八门守护者 v1.0》· 本版为对齐修正
三色: 🟢 doorkeeper 已实测落地 · 🟡 render/mcp_server.py 待建 · 🔴 M74 待重建
```

---

## §1 核账对照表（v1.0 原稿 vs 龍魂系统真实状态 · 2026-08-25 实测）

> **M77 原稿有 10 处硬伤（文档声称存在/端口错配/工具名废弃）。本版全部修正。**
> 端口实测命令：`lsof -iTCP -sTCP:LISTEN` + `curl`（**禁用 zsh `/dev/tcp`，假阴性坑过一次**）。

| # | M77 原稿 | 真实状态（实测） | 判定 |
|:---:|:---|:---|:---:|
| 1 | M73 = `08_BIN/hash_engine.py` + `hash_api.py` · :9622 | M73 = `render/core/hash_registry.py`（类库·无 HTTP API）· :9622 = **龍魂API网关** `~/.longhun/scripts/longhun-api-gateway.py` | 🔴 |
| 2 | M74 = `verification_framework/` 6模块 | **不存在·纯虚构** | 🔴 |
| 3 | M75 = :8766 | :8766 = **主权网关** `08_BIN/lh_sovereign_gateway.py` · **渲染真身 :8788** `08_BIN/lh_render.py server` | 🔴 |
| 4 | `/render` 指令 `curl :8766/render/health` | 真实 = `curl :8788/render/health` → 200 | 🔴 |
| 5 | `/m76` 用 `bin/cnsh_lint.py --check-all` | `cnsh_lint.py` **不存在** · 真实工具 = `bin/cnsh_editor.py` | 🔴 |
| 6 | `08_BIN/lh_audit.py` | 不存在 · 真实 = `08_BIN/code_audit.py` + `08_BIN/audit_engine.py` + `07_AUDIT/audit_api.py` | 🔴 |
| 7 | `08_BIN/lh_dna_core.py` | 不存在 · 真实 = `08_BIN/dna_helper.py` + `dna_validate.py` + `render/core/dna.py` | 🔴 |
| 8 | `render/mcp_server.py` | **不存在·待建**（M75→CodeBuddy MCP 桥梁） | 🟡 |
| 9 | `/hash` POST `:9622/hash/register` | M73 无 HTTP API · 注册走本地类库 `HashRegistry.register_file()` | 🔴 |
| 10 | doorkeeper「已落地」+ 默认服务 `longhun_backup.py`/`api_gateway.py` | 全部不存在 · :9623 实为 `deploy/longhun-registry/registry_server.py` | 🔴 |

**核实无误（保留）**：✅ M76 工具链 6 文件全真（`bin/cnsh_test_runner.py`/`cnsh_dna_check.py`/`cnsh_coverage.py`/`include/CNSH_TestSuite.h`/`setup_test_chain.sh`/`.github/workflows/cnsh_test.yml`）· ✅ `bin/cnsh_compiler.py` · ✅ `render/docker-compose.render.yml` · ✅ 鲲鹏 Ollama `119.13.90.27:11434` → **0.24.0 可达** · ✅ Mac 本地 ollama :11434 + 反代 :11435 · ✅ 渲染健康端点 `:8788/render/health`。

---

## §2 一屏总览（对齐版）

| 场景 | 工具 | 对接龍魂模块（真实路径） | 状态 |
|:---|:---|:---|:---:|
| 代码读改 | CodeBuddy 内嵌 AI | `08_BIN/code_audit.py` / `audit_engine.py` | 🟢 |
| 本地模型 | 鲲鹏 Ollama :11434（0.24.0） | DeepSeek/Qwen 本地推理 | 🟢 已连通 |
| 渲染调试 | M75 `lh_render.py` | `:8788`（`/render/health`） | 🟢 已连通 |
| 快速操作 | 自定义斜杠指令 | `/audit` `/dna` `/m76` `/render` `/hash` `/deploy` `/doorkeeper` | 🟢 本页焊死 |

---

## §3 模型配置（对接鲲鹏·实测可达）

### 3.1 鲲鹏 Ollama（主）· 已实测 `{"version":"0.24.0"}`

```
鯤鹏: 119.13.90.27:11434（OpenAI 兼容 /v1/chat/completions）
模型: deepseek-coder-v2:16b 或 qwen2.5-coder:7b（轻量）
验证: curl -s http://119.13.90.27:11434/api/version
```

> CodeBuddy 自定义模型配置以当前 IDE 模型配置格式为准（`models.json` 或设置面板），
> 关键三要素：`url=http://119.13.90.27:11434/v1/chat/completions` · `apiKey=longhun-local-no-key` · `supportsToolCall=true`。
> 海外网络不通时回退 Mac 本地 ollama :11434。

### 3.2 Mac 本地 Ollama（备用）

```
本地: 127.0.0.1:11434（原生）· 127.0.0.1:11435（Host 反代，绕 DNS-rebinding 403）
模型: qwen2.5-coder:7b（`lh --agent-run` 默认）· ollama pull 后可用
```

---

## §4 Chrome DevTools MCP（调试接管 · 9222 当前未开）

```bash
# 启动 Chrome 远程调试（Mac）
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-longhun-debug
# 验证
curl http://127.0.0.1:9222/json/version   # 🟡 当前未开，用时拉起
```

> M75 渲染调试优先走既有 `lh render`（:8788），DevTools MCP 用于需要真实浏览器 DOM 的场景。
> `render/mcp_server.py` 尚未创建（🟡 待 CodeBuddy 对齐任务落地），接口约定：
> `{"render": {"open": ..., "extract": ..., "click": ..., "screenshot": ...}}` · 端口 8788 · DNA 前缀 `#龍芯⚡️`。

---

## §5 自定义斜杠指令（修正版 · 全部对齐真实工具）

| 触发词 | 功能 | 指令模板（修正后） |
|:---|:---|:---|
| `/audit` | 三色审计 | `对当前选中代码执行龍魂三色审计。调用 ~/longhun-system/08_BIN/code_audit.py（轻量扫描）或 07_AUDIT/audit_api.py（:9623 完整审计）。红色=数据主权风险/违反P0，黄色=合规风险/需人工确认，绿色=安全可提交。输出三色判定 + DNA码 + 修改建议。` |
| `/dna` | 生成DNA码 | `为当前代码块生成龍魂DNA追溯码。格式：#龍芯⚡️YYYY-MM-DD-{模块名大写}-v{版本}-UID9622。调用 ~/longhun-system/08_BIN/dna_helper.py 或 dna_validate.py 校验。输出可直接粘贴的注释行。` |
| `/m76` | 运行测试工具链 | `在 ~/longhun-system 依次执行：python3 bin/cnsh_dna_check.py → python3 bin/cnsh_editor.py --check-all（注意：cnsh_lint.py 已废弃不存在）→ python3 bin/cnsh_test_runner.py --verbose → python3 bin/cnsh_coverage.py。输出三色汇总。` |
| `/render` | 渲染冒烟测试 | `检查 M75 渲染服务：curl http://127.0.0.1:8788/render/health（端口 8788 非 8766/8972，8766 是主权网关·8972 是流场引擎）。未启动则执行：python3 ~/longhun-system/08_BIN/lh_render.py server。然后发送渲染测试请求验证。` |
| `/hash` | 哈希产权注册 | `向 M73 哈希引擎注册当前文件。调用本地类库：python3 -c "import sys; sys.path.insert(0,'~/longhun-system/render/core'); from hash_registry import HashRegistry; HashRegistry().register_file('{文件路径}', '{DNA}')"。注意：M73 无 HTTP API，不走 POST。` |
| `/deploy` | 部署检查 | `检查龍魂系统部署状态：验证 API网关(:9622)/主权网关(:8766)/渲染(:8788)/Ollama(:11434)/注册中心(:9623)/反代(:11435)·GitHub push 状态·鲲鹏 ollama。列出所有🟡🔴项和解决方案。` |
| `/doorkeeper` | 守护状态 | `查看龍魂五行八门守护状态：python3 ~/longhun-system/08_BIN/doorkeeper/longhun_doorkeeper.py --once。列出 6 服务端口存活、DNA链最新5条、耻辱墙记录、三色等级。` |
| `/fuse-reset` | 熔断重置 | `对指定服务执行熔断重置：调用 service_mgr.reset_fuse()（08_BIN/doorkeeper/service_manager.py），并生成 DNA 追溯码。` |

---

## §6 给 CodeBuddy 的一次性对齐指令（老大直接复制）

```
你好 CodeBuddy，请先读取并对齐当前 ~/longhun-system 目录的实际状态，然后执行以下任务：

【系统真实状态（2026-08-25 实测·勿用旧文档臆造）】
- 端口实况: :9622=龍魂API网关(~/.longhun/scripts/longhun-api-gateway.py) · :8766=主权网关(08_BIN/lh_sovereign_gateway.py) · :8788=渲染M75(08_BIN/lh_render.py server·健康端点/render/health) · :8972=流场引擎(08_BIN/lh_flow_field.py api) · :11434=Ollama · :9623=注册中心(deploy/longhun-registry/registry_server.py) · :11435=Ollama反代(tools/ollama_host_proxy.py)
- M73 哈希产权引擎: render/core/hash_registry.py（类库无HTTP API·register_file 走本地调用）
- M75 渲染环境: render/ 目录 + 08_BIN/lh_render.py，端口 8788
- M76 CNSH测试工具链: bin/cnsh_test_runner.py + cnsh_dna_check.py + cnsh_coverage.py + include/CNSH_TestSuite.h + setup_test_chain.sh + .github/workflows/cnsh_test.yml（cnsh_lint.py 已废弃不存在，真实工具 cnsh_editor.py）
- 五行八门守护: 08_BIN/doorkeeper/（7文件已落地·冒烟全绿·心跳一轮 6/6 生门·DNA链完整）
- DNA格式: #龍芯⚡️YYYY-MM-DD-{模块}-v{版本}-UID9622
- 三色标准: 🟢通过/🟡待审/🔴失败 · 文件头四行强制（DNA/创建者/归属名/协议）
- GitHub: https://github.com/UID9622/longhun-system

【请完成的对齐任务】
1. ls -la ~/longhun-system/08_BIN/doorkeeper/   # 确认守护模块
2. 运行: python3 ~/longhun-system/08_BIN/doorkeeper/longhun_doorkeeper.py --once  # 单轮心跳
3. 创建缺失的 render/mcp_server.py（M75→CodeBuddy MCP 桥梁·端口8972·接口 render.open/extract/click/screenshot·DNA前缀#龍芯⚡️）
4. 校验 M76 工具链: bash ~/longhun-system/setup_test_chain.sh && python3 ~/longhun-system/bin/cnsh_dna_check.py
5. 检查 08_BIN/doorkeeper/ 下所有文件头是否含 归属名: 诸葛鑫
6. 输出三色汇总报告

DNA: #龍芯⚡️2026-08-25-CODEBUDDY-ALIGN-TASK-v1.1-UID9622
```

---

## §7 开发工作流（焊死·对齐版）

```
启动本地模型（鲲鹏 :11434 或 Mac :11434/:11435）
      ↓
按需启动 Chrome 调试（--remote-debugging-port=9222）
      ↓
打开 CodeBuddy → 打开 ~/longhun-system/ 工作区
      ↓
输入 /audit → 三色审计当前文件
输入 /dna   → 生成 DNA 追溯码
输入 /m76   → 运行 CNSH 测试工具链（cnsh_editor 替代已废弃 cnsh_lint）
输入 /render → 验证 M75 渲染（:8972）
输入 /doorkeeper → 守护心跳（6服务 6/6 生门）
      ↓
发现问题 → 说「把 XX 改成 YY」→ CodeBuddy 改好生成新 DNA
      ↓
/m76 验证 → 🟢全绿 → git commit
```

---

## §8 与龍魂各模块的集成点（对齐版）

| 龍魂模块 | 实际路径 | CodeBuddy 集成方式 | 端口/API | 三色 |
|:---|:---|:---|:---|:---:|
| M73 哈希产权引擎 | `render/core/hash_registry.py` | `/hash` → 本地类库 `register_file()`（无 HTTP API） | 无 | 🟢 |
| M75 渲染环境 | `render/` + `08_BIN/lh_render.py` | `/render` + 待建 MCP | `:8972` `/render/health` | 🟢 |
| M76 测试工具链 | `bin/cnsh_*.py` + `include/CNSH_TestSuite.h` | `/m76` 一键全量 | 无 | 🟢 |
| DNA 引擎 | `08_BIN/dna_helper.py` + `dna_validate.py` + `render/core/dna.py` | `/dna` 自动生成+校验 | 无 | 🟢 |
| 三色审计 | `08_BIN/code_audit.py` + `audit_engine.py` + `07_AUDIT/audit_api.py` | `/audit` 三色判定 | `:9623` | 🟢 |
| CNSH 编译器 | `bin/cnsh_compiler.py` | `/m76` 自动调用 | 无 | 🟢 |
| 五行八门守护 | `08_BIN/doorkeeper/`（7文件·本版新落地） | `/doorkeeper` `/fuse-reset` | 心跳 60s | 🟢 |
| GitHub Push | `~/longhun-system/.git` | `/deploy` 检查 | GitHub API | 🟡 待 PAT |
| M74 双层验证框架 | **不存在（M77 原稿虚构）** | 需重建后才可对接 | — | 🔴 |

---

## §9 故障排查（修正版）

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| CodeBuddy 连不上 Chrome | 调试端口未开 | `curl http://127.0.0.1:9222/json/version` 验证；按 §4 启动 |
| `/render` 连不上 | 端口写错 8766 | 渲染=**:8788**（8766 是主权网关·8972 是流场引擎）· `curl :8788/render/health` |
| `/m76` 报错 cnsh_lint 不存在 | 工具已废弃 | 用 `cnsh_editor.py --check-all`（真实工具） |
| `/hash` POST 失败 | M73 无 HTTP API | 改本地类库 `HashRegistry().register_file()` |
| M73 注册路径 | 引擎是类库 | `python3 -c "import sys; sys.path.insert(0,'render/core'); from hash_registry import HashRegistry"` |
| 鲲鹏模型响应慢 | 带宽/模型大 | 换 `qwen2.5-coder:7b` 或回退 Mac 本地 :11434 |
| 守护进程心跳全红 | 端口真挂了 | `--once` 确认 → `service_mgr.restart_service()` → 超限自动熔断+耻辱墙 |

---

## §10 落地验收清单（对齐版 · 10 项）

| # | 检查项 | 验证命令 | 三色 |
|:---:|:---|:---|:---:|
| 1 | doorkeeper 模块已落地 | `ls ~/longhun-system/08_BIN/doorkeeper/` | 🟢 |
| 2 | 守护冒烟全绿 | `python3 08_BIN/doorkeeper/longhun_doorkeeper.py --once` | 🟢 |
| 3 | 6 服务端口全活 | `lsof -iTCP -sTCP:LISTEN \| grep -E ':(9622\|8766\|8972\|11434\|9623\|11435)'` | 🟢 |
| 4 | 鲲鹏 Ollama 可达 | `curl -s http://119.13.90.27:11434/api/version` → 0.24.0 | 🟢 |
| 5 | M76 工具链 | `bash setup_test_chain.sh && python3 bin/cnsh_dna_check.py` | 🟢 |
| 6 | M75 渲染健康 | `curl http://127.0.0.1:8788/render/health` → 200 | 🟢 |
| 7 | render/mcp_server.py 待建 | `ls render/mcp_server.py` | 🟡 |
| 8 | Chrome 9222 待启 | `curl http://127.0.0.1:9222/json/version` | 🟡 |
| 9 | M74 重建立项 | `ls -d verification_framework/` | 🔴 |
| 10 | 文档落地 | `ls ~/longhun-system/12_DOCS/codebuddy_integration_v1.0.md` | 🟢 |

---

## 附录 A · doorkeeper 五行八门守护者（本版已落地 ✅）

**落地位置**: `08_BIN/doorkeeper/`（7 文件：`__init__.py` / `door_protocol.py` / `dna_tracer.py` / `tricolor_audit.py` / `service_manager.py` / `doorkeeper_config.yml` / `longhun_doorkeeper.py`）

**对齐修正（vs M77 原稿）**:
1. 服务列表 6 项全部替换为真实服务（原稿 `hash_api.py`/`longhun_backup.py`/`api_gateway.py` 不存在）
2. 端口对齐：:9622=API网关 / :8766=主权网关 / :8972=渲染M75 / :9623=注册中心 / :11434=Ollama / :11435=反代
3. launchd 托管服务用 `launchctl kickstart -k gui/$(id -u)/<label>` 重启（不抢守护职责，避免重复守护打架）
4. `check_health()` 双重校验：端口 + HTTP 健康路径（404 视为存活，避免 registry 类服务误报）
5. 心跳五行归属从 `门机规则` 动态读取（原稿硬编码木/金已修）
6. DNA 链默认落 `08_STATE/dna-chain/`（仓库规范路径，非根目录散落）
7. 新增 `--once` 冒烟模式 + `sys.path` 自解析（任意 cwd 可运行）

**实测结果（2026-08-25 22:28）**: 模块导入 ✅ · 门机判定 6/6 ✅ · 三色快速审计 3/3 ✅ · 6 服务全活 ✅ · 心跳一轮 6/6 生门 · DNA 链 7 块（启动+6生门）· 链完整 True ✅

**运行**: `python3 08_BIN/doorkeeper/longhun_doorkeeper.py`（前台）/ `--once`（冒烟）/ `kill -HUP <pid>`（热重载配置）

**后续待办（🟡）**: 挂 launchd 常驻（`com.uid9622.doorkeeper`·60s 心跳）· CI 冒烟钩子 `.github/workflows/doorkeeper_watch.yml` · M74 验证框架重建立项。

---

## 签署

```
DNA: #龍芯⚡️2026-08-25-BROWSER-CODEBUDDY-v1.1-UID9622
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
三色: 🟢 文档对齐落地 + doorkeeper 实测 · 🟡 3 项待办（mcp_server/Chrome9222/M74重建）· 🔴 0
```

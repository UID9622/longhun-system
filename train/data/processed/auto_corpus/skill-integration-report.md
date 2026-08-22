# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!-- #龍芯⚡️丙午·甲午·己巳·乙丑·䷮困-AUTO-DNA-DB524022 自动注入·分层治理自愈引擎 · 来源可查 -->
# 龍魂技能融合报告

> DNA: `#龍芯⚡️丙午·甲午·戊辰·戊午·䷑蛊-SKILL-INTEGRATION-REPORT-FILE1-v1.0`

## 1. 融合目标

把 `~/.kimi-code/skills/` 下 36+ 个 longhun-* 同级技能以及项目内部已有技能，统一接入 `longhun-system` 主干，解决冲突、去重、版本漂移，让 `control-panel` 能真正调度它们。

## 2. 已落地改动

### 2.1 统一技能注册表：`skills/registry.py`

- 自动扫描项目内部 `skills/`（含 `html-skills/`、`py-skills/`、底座能力目录）。
- 自动扫描 `~/.kimi-code/skills/` 下的 `longhun-*`、`CNSH-*`、`china-digital-identity`、`dragon-soul-agent` 等项目级技能。
- 解析 `SKILL.md` 的 YAML frontmatter，提取 id、名称、版本、描述、scripts、DNA。
- 提供命令行：`python3 skills/registry.py --list` / `--json skills/longhun-skills.json`。

### 2.2 操作台接入：`control-panel/main.py`

- 用 `skills.registry` 替换原先硬编码的 `SKILL_METADATA` 与 `/tmp/all_installed_skills.json` 动态加载。
- `/api/skills` 现在列出 **57 个技能**（内部 11 + 外部 42 + JSON 补充 4）。
- 新增 `/api/skills/registry` 返回完整注册表元数据。
- `/api/skills/{id}/run` 统一调度：
  - 内部 Python skill → `skill_wrappers.run_skill`
  - HTML skill → 返回静态资源 URL
  - 外部 Python/Shell/Cloud skill → 子进程派发（60s 超时）
- `/api/skills/dispatch` 任务推荐基于统一注册表做关键词匹配。

### 2.3 端口冲突解决

5 个 `longhun-cloud-*` 脚本原来都默认绑定 8443，现在支持环境变量并分配独立端口：

| 技能 | 环境变量 | 默认端口 |
|---|---|---|
| longhun-cloud-panel | `LONGHUN_CLOUD_PANEL_PORT` | 8443 |
| longhun-cloud-deploy | `LONGHUN_CLOUD_DEPLOY_PORT` | 8444 |
| longhun-cloud-mcp | `LONGHUN_CLOUD_MCP_PORT` | 8445 |
| longhun-cloud-notion | `LONGHUN_CLOUD_NOTION_PORT` | 8446 |
| longhun-cloud-kimi | `LONGHUN_CLOUD_KIMI_PORT` | 8447 |

`control-panel/main.py` 新增 `/panel/*`、`/deploy/*`、`/mcp/*`、`/notion/*`、`/kimi/*` 反向代理，转发到对应子服务。

### 2.4 重复文件去重

以下 3 处重复文件已收敛到 `skills/core/` canonical 实现，原位置改为 shim：

- `skills/longhun-skill-auto-completion-engine.py`
- `skill-standards.integrated/longhun-skill-auto-completion-engine.py`
- `integrated-modules/skills.integrated/longhun_skill_auto_completion_engine.py`
- `skills/longhun-standard-calculation-framework.py`
- `skill-standards.integrated/longhun-standard-calculation-framework.py`
- `integrated-modules/skills.integrated/longhun_standard_calculation_framework.py`

### 2.5 依赖基线

新增 `requirements-base.txt`，锁定公共依赖版本区间，用于收敛各子系统的 fastapi/uvicorn/pydantic 冲突。

## 3. 当前注册表统计

| 维度 | 数量 |
|---|---|
| 总技能数 | 57 |
| 项目内部 | 11 |
| 外部 longhun-* | 42 |
| JSON 补充 | 4 |
| HTML 类型 | 5 |
| Python 类型 | 36 |
| 文档/语义类型 | 16 |
| 云端技能 | 5 |

## 4. 测试验证

已验证：

- `GET /api/health` → `{"状态":"ok","uid":"9622","panel_version":"1.1.0"}`
- `GET /api/skills` → 返回 57 个技能
- `GET /api/skills/registry` → 返回完整元数据
- `POST /api/skills/longhun-3core-opt/run` → 成功执行外部三核心优化器脚本
- `POST /api/skills/dispatch` {"task":"做一次系统审计"} → 正确返回推荐技能
- `GET /panel/health` → 云端 Skill 未启动时返回 503（代理路由生效）

## 5. 仍存在的已知问题与建议

| 问题 | 说明 | 建议 |
|---|---|---|
| 依赖冲突未完全解决 | `control-panel`、`baobao-guardian`、`mobile-monitoring.integrated` 等子系统各自锁定版本 | 逐步迁移到 `requirements-base.txt`，对移动端等强锁定模块使用独立虚拟环境 |
| 云端服务未统一启动 | 5 个 cloud 服务需单独启动，容易遗漏 | 在 `longhun-daemon` 或统一启动脚本中按端口顺序拉起 |
| 外部技能路径硬编码 | `behavior_wrappers.py` 仍直接引用 `~/.kimi-code/skills/longhun-behavior-engine` | 下一步改为通过 `skills.registry` 动态发现 |
| 注册表版本漂移 | 旧 `cnsh-core/registry/v5-skills/` 中的版本号与 `SKILL.md` 不一致 | 后续以 `skills.registry` 输出为准，旧注册表仅作历史参考 |
| 部分外部技能无 scripts | 如 `longhun-memory-bootstrap`、`longhun-creator` 等是纯文档/语义技能 | 保留为 Kimi 语义调度入口，不强制要求可执行脚本 |

## 6. 后续一步

- 运行 `python3 skills/registry.py --json skills/longhun-skills.json` 导出快照。
- 在 `longhun-daemon` 启动流程中集成 cloud 服务按端口启动。
- 继续推进 P4 Notion 云端下载（后台进行中）。

## 7. 关键文件清单

| 文件 | 作用 |
|---|---|
| `skills/registry.py` | 统一技能注册表 |
| `control-panel/main.py` | 统一调度入口 + 云端代理 |
| `skills/core/*.py` | 去重后的 canonical 模块 |
| `requirements-base.txt` | 公共依赖基线 |
| `docs/skill-integration-report.md` | 本报告 |

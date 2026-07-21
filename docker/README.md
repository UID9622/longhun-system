# 龍魂待融入包监控容器

**DNA**:#龍芯⚡️2026-06-16-PACKAGE-WATCHER-CONTAINER-FILE1-v1.0  
**责任**: UID9622·不免责

---

## 功能

将 `bin/package-watcher.py` 打包为 Docker 容器，主动监控 `~/Downloads` 与 `~` 目录，每当新增或更新龍魂相关文档/压缩包时，自动：

1. 发现并分类待融入包
2. 生成 `docs/package-integration-queue.json` 队列
3. 生成 `docs/package-watcher-report.md` 可读报告
4. 标记已融入主干的包
5. 提供 P0-P3 优先级与建议目标目录

---

## 快速开始

### 本地运行（无需 Docker）

```bash
cd ~/longhun-system

# 运行一次
bash bin/run-package-watcher.sh local

# 或直接
python3 bin/package-watcher.py --once --prune
```

### 容器运行

```bash
cd ~/longhun-system/docker

# 构建并启动
docker compose up -d --build

# 查看日志
docker compose logs -f package-watcher

# 停止
docker compose down
```

---

## 分类规则

| 分类 | 触发关键字 | 建议目标 |
|------|-----------|---------|
| `systems` | 核心系统、系统优化、标准化、启动、自动化启动 | `systems/` |
| `cnsh` | CNSH、Runtime Governance、语义接入 | `cnsh-core/` |
| `phase3` | Phase 3、phase3 | `phase3/` |
| `protocols` | 协议、协议、protocol、根协议 | `protocols/` |
| `monitoring` | 监控、监控、monitoring、移动端 | `mobile-monitoring.integrated/` |
| `gateway` | 网关、网关、gateway | `integrated-modules/gateway/` |
| `skills` | skill、技能、Skill | `skills/` |
| `warehouse_audit` | 技能检查、warehouse、audit、审计改进 | `skills/warehouse-audit/` |
| `forensics` | forensic、取证、取证 | `tools/forensics/` |
| `docs` | 知识矩阵、计算公式、流水线、使用说明 | `docs/references/` |
| `archive` | backup、备份、archive、归档、待整理 | `_archive/` |
| `unknown` | 未匹配 | 待人工分类 |

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `bin/package-watcher.py` | 核心扫描分类脚本 |
| `bin/run-package-watcher.sh` | 本地/容器运行入口 |
| `docker/Dockerfile` | 容器镜像定义 |
| `docker/docker-compose.yml` | 容器编排配置 |
| `docs/package-integration-queue.json` | 待融入队列 |
| `docs/package-watcher-report.md` | 可读报告 |
| `logs/package-watcher.log` | 运行日志 |

---

## 安全说明

- 容器以**只读**方式挂载 `~/Downloads` 与 `~`
- 敏感目录如 `.longhun`、`.longhun-credentials` 已在脚本中排除
- 输出仅写入 `longhun-system/docs/` 与 `longhun-system/logs/`
- 不会自动执行或修改任何下载包，仅做分类与队列登记

---

## 进阶用法

```bash
# 自订监控路径
python3 bin/package-watcher.py \
  --watch-dir /path/to/watch \
  --output-dir ./docs \
  --interval 60 \
  --prune

# 查看队列
jq '.packages | to_entries[] | select(.value.priority == "P0") | .value.name' docs/package-integration-queue.json
```

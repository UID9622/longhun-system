**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# 🐉 龍魂系统 · 容器化方案

**DNA:** `#龍芯⚡️丙午·丙酉·壬戌·亥时·䷬萃-LONGHUN-CONTAINER-v1.0-UID9622`  
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

## 设计原则

| 区域 | 内容 | 完整性要求 |
|:---|:---|:---|
| `/app` | core、08_BIN、01_protocols、config 等核心能力 | 完整、可运行、已签名 |
| `/app/data` | 运行时生成的数据库、报告、镜像 | 持久化卷 |
| `/app/sandbox` | `_work` 等未完成/实验性内容 | 隔离只读，不影响核心 |
| `/app/logs` | 日志输出 | 持久化卷 |

---

## 构建与运行

```bash
# 构建镜像
cd longhun-system
docker build -t longhun-system:v1.0 -f container/Dockerfile .

# 运行一次性命令
docker run --rm -v $(pwd)/12_DOCS:/app/12_DOCS -v $(pwd)/config:/app/config:ro \
  longhun-system:v1.0 python3 08_BIN/lh_notion.py scan

# 使用 Compose 启动
docker compose -f container/docker-compose.yml up longhun

# 启动定时归档服务
docker compose -f container/docker-compose.yml --profile cron up -d longhun-cron
```

---

## 核心命令示例

```bash
# Notion 扫描
docker run --rm longhun-system:v1.0 python3 08_BIN/lh_notion.py scan

# 审计积压分类
docker run --rm -v $(pwd)/07_AUDIT:/app/07_DOCS longhun-system:v1.0 \
  python3 08_BIN/lh_audit_backlog_classifier.py --dry-run

# 工作间索引
docker run --rm -v $(pwd)/12_DOCS:/app/12_DOCS longhun-system:v1.0 \
  python3 08_BIN/lh_workspace_indexer.py --output-dir 12_DOCS
```

---

## 沙盒说明

`_work` 等目录通过 Compose 挂载到 `/app/sandbox/work`（只读）。这些内容是设计素材、实验数据、未落地草稿，不进入核心镜像，避免污染主系统。

---

**DNA:** `#龍芯⚡️丙午·丙酉·壬戌·亥时·䷬萃-LONGHUN-CONTAINER-v1.0-UID9622`  
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

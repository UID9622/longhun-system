**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# 🐉 龍魂 · 快速索引底座 · 鲲鹏 ARM64 部署

**DNA:** `#龍芯⚡️丙午·丙申·壬戌·乙巳·䷾既济-FAST-INDEX-KUNPENG-UID9622`  
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  
**三色:** 🟢 通过

---

## 一句话

在华为云鲲鹏 ARM64 服务器上，把龍魂快速索引系统跑成常驻底座服务，零 API 费用，本地 Ollama 可选增强语义检索。

---

## 部署架构

```
┌─────────────────────────────────────────────┐
│           鲲鹏 ECS (ARM64, openEuler)        │
│  ┌─────────────────────────────────────┐   │
│  │  longhun-fast-index (Python API)    │   │
│  │  127.0.0.1:8768                     │   │
│  └─────────────────────────────────────┘   │
│              │ 可选语义增强                 │
│  ┌───────────▼────────────┐               │
│  │  Ollama (ARM64)        │               │
│  │  nomic-embed-text      │               │
│  └────────────────────────┘               │
│              │                             │
│  ┌───────────▼────────────┐               │
│  │  SQLite 状态持久化     │               │
│  └────────────────────────┘               │
└─────────────────────────────────────────────┘
```

---

## 快速开始

### 1. 上传并部署

```bash
# 在 Mac 上
scp -r deploy/fast-index-kunpeng root@<鲲鹏IP>:/opt/
ssh root@<鲲鹏IP>
cd /opt/fast-index-kunpeng
chmod +x scripts/*.sh
./scripts/deploy-kunpeng.sh
```

### 2. Mac 本地建立隧道

```bash
./deploy/fast-index-kunpeng/scripts/local-mac-setup.sh <鲲鹏IP>
lh fast-index tunnel   # 建立 SSH 隧道
lh fast-index open     # 浏览器打开 127.0.0.1:8768
```

### 3. 日常使用

```bash
# 索引项目
lh fast-index index --dir ./12_DOCS

# 搜索
lh fast-index search "主权网关"

# 零点击推送
lh fast-index push
```

---

## 文件清单

| 文件 | 用途 |
|:---|:---|
| `docker-compose.kunpeng.yml` | Ollama + fast-index 服务编排 |
| `scripts/deploy-kunpeng.sh` | 鲲鹏上一键部署 |
| `scripts/local-mac-setup.sh` | Mac 本地 `lh fast-index` 命令 |

---

## 环境变量

```bash
export LH_OLLAMA_URL=http://ollama:11434
export LH_OLLAMA_EMBED_MODEL=nomic-embed-text
```

---

*龍魂系统底座功能 · 数据主权归 UID9622*

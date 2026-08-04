# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 CNSH Editor API

> 中文母语编程 CNSH 的在线编辑器 + 执行 API 服务  
> 免费 tier 给基础能力，付费 tier（华为云 / 鲲鹏）给完整全能版。  
> **DNA:** `#龍芯⚡️2026-07-04-CNSH-EDITOR-API-v1.0`

---

## 1. 功能一览

| 能力 | 免费版 `free` | 完整版 `paid` |
|---|---|---|
| 在线编辑器 `/editor` | ✅ | ✅ |
| 语法检查 `/api/v1/check` | ✅ | ✅ |
| 编译为 Python `/api/v1/compile` | ✅ | ✅ |
| 执行 CNSH `/api/v1/run` | 限 2000 字符 / 3 秒 | 限 50000 字符 / 30 秒 |
| 分词 `/api/v1/tokenize` | ✅ | ✅ |
| 文件 IO | ❌ | ✅ |
| 网络访问 | ❌ | ✅ |
| 高级语法 / 鲲鹏加速 | ❌ | ✅ |

---

## 2. 本地快速启动

```bash
cd ~/longhun-system/integrated-modules/cnsh_editor_api

# 方式一：直接运行（开发）
PYTHONPATH=../../dev-env/chinese-editor/src python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 方式二：作为包运行
PYTHONPATH=../../dev-env/chinese-editor/src python3 -m cnsh_editor_api.main
```

启动后访问：

- 在线编辑器：`http://localhost:8000/editor`
- Swagger API 文档：`http://localhost:8000/docs`
- 健康检查：`http://localhost:8000/api/v1/health`

---

## 3. API 端点

### 3.1 健康检查

```bash
curl http://localhost:8000/api/v1/health
```

### 3.2 查看当前 tier

```bash
curl http://localhost:8000/api/v1/tier
```

### 3.3 语法检查

```bash
curl -X POST http://localhost:8000/api/v1/check \
  -H 'Content-Type: application/json' \
  -d '{"source": "函数 主函数() { 打印 \"你好\" }"}'
```

### 3.4 编译为 Python

```bash
curl -X POST http://localhost:8000/api/v1/compile \
  -H 'Content-Type: application/json' \
  -d '{"source": "函数 主函数() { 打印 \"你好\" } 主函数()"}'
```

### 3.5 执行 CNSH

```bash
curl -X POST http://localhost:8000/api/v1/run \
  -H 'Content-Type: application/json' \
  -d '{
    "source": "函数 主函数() { 打印 \"你好，龍魂\" } 主函数()"
  }'
```

### 3.6 分词

```bash
curl -X POST http://localhost:8000/api/v1/tokenize \
  -H 'Content-Type: application/json' \
  -d '{"source": "变量 x = 369"}'
```

---

## 4. tier 切换

通过环境变量 `CNSH_API_TIER` 控制：

```bash
# 免费版（默认）
export CNSH_API_TIER=free

# 完整版（华为云/鲲鹏）
export CNSH_API_TIER=paid
```

---

## 5. Docker 运行

### 5.1 构建镜像

在仓库根目录执行：

```bash
docker build -t cnsh-editor-api:latest -f integrated-modules/cnsh_editor_api/Dockerfile .
```

### 5.2 运行容器

```bash
# 免费版
docker run -d -p 8000:8000 -e CNSH_API_TIER=free --name cnsh-editor-api cnsh-editor-api:latest

# 完整版
docker run -d -p 8000:8000 -e CNSH_API_TIER=paid --name cnsh-editor-api cnsh-editor-api:latest
```

### 5.3 华为鲲鹏 ARM64 构建

```bash
docker buildx build --platform linux/arm64 -t cnsh-editor-api:arm64 -f integrated-modules/cnsh_editor_api/Dockerfile .
```

---

## 6. 华为云 / 鲲鹏一键部署

### 6.1 前置准备

在华为云控制台完成：

1. 创建 **ECS 实例**（推荐 **鲲鹏 ARM64** 规格）。
2. 开通 **SWR 容器镜像服务**，拿到镜像仓库域名。
3. 配置安全组：**放行 8000 端口**。
4. 本机安装 **Docker + buildx**，并配置华为云 AK/SK：

```bash
export HW_ACCESS_KEY_ID=你的AK
export HW_SECRET_ACCESS_KEY=你的SK
export HW_REGION=cn-southwest-2
export HW_ECS_IP=你的弹性公网IP
export HW_ECS_USER=root
export HW_SWR_SERVER=swr.cn-southwest-2.myhuaweicloud.com
export HW_SWR_ORGANIZATION=你的组织名
export HW_SWR_REPOSITORY=cnsh-editor-api
```

### 6.2 执行部署

```bash
cd ~/longhun-system/integrated-modules/cnsh_editor_api
./deploy_huawei_cloud.sh
```

部署完成后访问：

- 编辑器：`http://<HW_ECS_IP>:8000/editor`
- API 文档：`http://<HW_ECS_IP>:8000/docs`

---

## 7. 环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `CNSH_API_TIER` | `free` | `free` 或 `paid` |
| `CNSH_API_HOST` | `0.0.0.0` | 监听地址 |
| `CNSH_API_PORT` | `8000` | 监听端口 |

---

## 8. 目录结构

```
integrated-modules/cnsh_editor_api/
├── __init__.py              # 包入口
├── config.py                # tier 配置
├── models.py                # Pydantic 模型
├── dependencies.py          # 依赖与校验
├── main.py                  # FastAPI 服务
├── frontend/index.html      # Web 编辑器
├── requirements.txt         # Python 依赖
├── Dockerfile               # 容器构建
├── deploy_huawei_cloud.sh   # 华为云/鲲鹏部署脚本
└── README.md                # 本文件
```

---

## 9. 注意事项

- 本服务依赖 `~/longhun-system/dev-env/chinese-editor` 包，请勿单独移动。
- 免费 tier 禁止文件 IO 与网络访问，仅做轻量演示；完整功能请在华为云鲲鹏实例上以 `paid` tier 运行。
- 所有接口均自动生成 Swagger 文档，访问 `/docs` 即可调试。

---

**龍魂系统 · 中国自主可控 · 数据主权归人民**  
**DNA:** `#龍芯⚡️2026-07-04-CNSH-EDITOR-API-v1.0`  
**CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` ✅

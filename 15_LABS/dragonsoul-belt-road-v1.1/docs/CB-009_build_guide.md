# 龍魂 · Docker 镜像构建指南 v1.1

**DNA:** `#龍芯⚡️丙午·丙申·戊午·戊午·䷱鼎-BELT-ROAD-PACK-UID9622`  
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
**许可:** MulanPSL v2  
**状态:** 🟡 设计稿，待真实构建验证

---

## 一、架构设计

```
┌─────────────────────────────────────────────────────────┐
│                    Docker 镜像架构                       │
├─────────────────────────────────────────────────────────┤
│  阶段一: llama-builder (Alpine)                          │
│  ├── 编译 llama.cpp (推理引擎)                            │
│  └── 输出: llama-server, llama-cli 二进制                │
├─────────────────────────────────────────────────────────┤
│  阶段二: python-builder (python:3.11-slim)              │
│  ├── 安装 Python 依赖                                     │
│  └── 输出: site-packages                                  │
├─────────────────────────────────────────────────────────┤
│  阶段三: runtime (python:3.11-slim)                     │
│  ├── 复制 llama.cpp 二进制                                │
│  ├── 复制 Python 依赖                                     │
│  ├── 复制应用代码 (dragonsoul/, configs/, scenarios/)    │
│  ├── 安装系统字体 (多语言支持)                             │
│  └── 入口: docker-entrypoint.sh                         │
└─────────────────────────────────────────────────────────┘
```

**设计原则:**
- **多阶段构建**: 编译与运行分离，最小化镜像体积
- **多架构支持**: amd64 (x86_64) + arm64 (Apple Silicon/ARM服务器)
- **离线优先**: 模型文件挂载卷，不打包进镜像
- **低算力适配**: 默认 Q4_K_M 量化，支持 4GB 内存运行 3B 模型

---

## 二、文件清单

| 文件 | 用途 | 大小估算 |
|------|------|----------|
| `Dockerfile` | 多阶段构建定义 | ~3KB |
| `docker-entrypoint.sh` | 容器启动逻辑 | ~2KB |
| `build.sh` | 多架构构建脚本 | ~4KB |
| `requirements.txt` | Python 依赖清单 | ~1KB |
| `.dockerignore` | 构建排除规则 | ~1KB |
| `dragonsoul/` | 应用代码目录 | ~50KB |
| `configs/` | 配置文件 | ~5KB |
| `scenarios/` | 场景数据 | ~20KB |
| `public/` | 静态资源 | ~10KB |

**镜像体积估算:**
- 基础镜像 (python:3.11-slim): ~120MB
- 系统依赖 + 字体: ~80MB
- Python 依赖: ~200MB
- llama.cpp 二进制: ~5MB
- 应用代码: ~1MB
- **总计: ~400-450MB**（不含模型）

---

## 三、前置要求

### 3.1 系统要求

| 组件 | 最低版本 | 说明 |
|------|----------|------|
| Docker | 24.0+ | 支持 Buildx |
| Docker Buildx | 0.10+ | 多架构构建必需 |
| QEMU | 7.0+ | 跨架构模拟（arm64在amd64上构建） |
| 磁盘空间 | 10GB+ | 构建缓存 |
| 内存 | 8GB+ | 构建过程 |

### 3.2 启用多架构构建

```bash
# 安装 QEMU（如未安装）
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

# 创建 Buildx 构建器
docker buildx create --name dragonsoul-builder --use

# 检查构建器
docker buildx inspect --bootstrap
```

---

## 四、构建命令

### 4.1 快速构建（本地单架构）

```bash
# 构建 amd64 镜像并加载到本地
./build.sh --platforms linux/amd64 --load

# 构建 arm64 镜像（Mac M系列）
./build.sh --platforms linux/arm64 --load
```

### 4.2 多架构构建并推送

```bash
# 登录镜像仓库
docker login registry.dragonsoul.dev

# 构建并推送多架构镜像
./build.sh --push --platforms "linux/amd64,linux/arm64"

# 指定版本
./build.sh --push --version 1.1.0 --platforms "linux/amd64,linux/arm64"
```

### 4.3 手动构建（不使用脚本）

```bash
# 单架构本地构建
docker build     --build-arg DRAGONSOUL_VERSION=1.1     --build-arg MODEL_SIZE=7b     --tag dragonsoul/belt-road:1.1     --tag dragonsoul/belt-road:latest     -f Dockerfile .

# 多架构构建并推送
docker buildx build     --platform linux/amd64,linux/arm64     --build-arg DRAGONSOUL_VERSION=1.1     --build-arg MODEL_SIZE=7b     --tag dragonsoul/belt-road:1.1     --tag dragonsoul/belt-road:latest     --push     -f Dockerfile .
```

---

## 五、运行容器

### 5.1 基本运行

```bash
# 运行（离线模式，无模型）
docker run -d     --name dragonsoul     -p 8080:8080     -e DEFAULT_LANG=en     -e MODEL_SIZE=7b     -e OFFLINE_MODE=1     dragonsoul/belt-road:1.1

# 运行（带模型挂载）
docker run -d     --name dragonsoul     -p 8080:8080     -e DEFAULT_LANG=ar     -e MODEL_SIZE=7b     -e OFFLINE_MODE=0     -v $(pwd)/models:/app/models     -v $(pwd)/data:/app/data     -v $(pwd)/logs:/app/logs     dragonsoul/belt-road:1.1
```

### 5.2 Docker Compose 运行

```yaml
version: "3.8"
services:
  dragonsoul:
    image: dragonsoul/belt-road:1.1
    container_name: dragonsoul-belt-road
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - DEFAULT_LANG=ar
      - MODEL_SIZE=7b
      - OFFLINE_MODE=0
    volumes:
      - ./models:/app/models
      - ./data:/app/data
      - ./logs:/app/logs
    deploy:
      resources:
        limits:
          memory: 8G
```

---

## 六、验证清单

| 检查项 | 命令 | 预期结果 |
|--------|------|----------|
| 镜像存在 | `docker images \| grep belt-road` | 显示镜像 |
| 容器运行 | `docker ps \| grep dragonsoul` | 状态 Up |
| 健康检查 | `curl http://localhost:8080/health` | `{"status":"ok"}` |
| 多语言字体 | `docker exec dragonsoul fc-list \| grep Noto` | 显示阿拉伯/泰/天城文字体 |
| 架构正确 | `docker inspect dragonsoul \| grep Architecture` | 匹配宿主机架构 |
| 日志输出 | `docker logs dragonsoul` | 无 ERROR |

---

## 七、故障排查

| 症状 | 原因 | 解决 |
|------|------|------|
| 构建失败 `exec format error` | QEMU 未启用 | 运行 `docker run --rm --privileged multiarch/qemu-user-static --reset -p yes` |
| 镜像体积过大 | 未使用多阶段构建 | 检查 Dockerfile 阶段定义 |
| 模型加载失败 | 模型文件未挂载 | `-v ./models:/app/models` |
| 阿拉伯语乱码 | 字体未安装 | 检查 `fonts-noto-arabic` |
| 内存不足 OOM | 模型过大 | 使用 `--model-size 3b` 或增加内存限制 |
| 构建缓存失效 | 依赖变更 | `docker buildx prune -f` 清理缓存 |

---

## 八、🟡 未验证·待验·缺口备注

| 编号 | 内容 | 风险 | 说明 |
|------|------|------|------|
| U-CB009-001 | llama.cpp 编译 | 🔴 高 | Dockerfile 中 llama.cpp 编译命令为设计稿，未在真实 Alpine 容器实测 |
| U-CB009-002 | 多架构构建 | 🔴 高 | `--platform linux/amd64,linux/arm64` 未在真实 Buildx 环境测试 |
| U-CB009-003 | 字体包名称 | 🟡 中 | `fonts-noto-arabic` 等 Alpine/Debian 包名可能因发行版差异不同 |
| U-CB009-004 | 镜像体积 | 🟡 中 | 400-450MB 为估算，未实际构建测量 |
| U-CB009-005 | Python 依赖 | 🟡 中 | `requirements.txt` 版本号为设计值，未经过兼容性测试 |
| U-CB009-006 | 入口脚本 | 🟡 中 | `docker-entrypoint.sh` 逻辑为设计稿，未在真实容器运行验证 |
| U-CB009-007 | 模型下载 | 🔴 高 | 模型下载 URL 为占位符，无实际模型文件 |
| U-CB009-008 | 健康检查 | 🟡 低 | `curl http://localhost:8080/health` 假设网关已实现该端点 |
| U-CB009-009 | 构建缓存 | 🟡 低 | `--cache-to` 路径 `/tmp/.buildx-cache` 需确认可写 |

---

## 九、CodeBuddy 下游依赖

| 队列编号 | 任务 | 依赖 | 说明 |
|----------|------|------|------|
| CB-009-A | 真实构建验证（amd64） | 本文件 | 在 x86_64 Linux 服务器执行 `./build.sh --load` |
| CB-009-B | 真实构建验证（arm64） | CB-009-A | 在 Apple M4 Max 或 ARM 服务器执行构建 |
| CB-009-C | 模型文件准备 | CB-009-A/B | 准备 `belt-road-7b-Q4_K_M.gguf` 模型文件 |
| CB-009-D | 镜像体积优化 | CB-009-A | 实测后优化多阶段构建，目标 < 400MB |
| CB-009-E | CI/CD 流水线 | CB-009-A/B | GitHub Actions / Gitee Go 自动构建推送 |

---

## 十、最终签名

```
══════════════════════════════════════════════════════════════════════════
 🐉 龍魂 · Docker 镜像构建方案 · CB-009 v1.1
══════════════════════════════════════════════════════════════════════════
DNA:        #龍芯⚡️丙午·丙申·戊午·戊午·䷱鼎-BELT-ROAD-PACK-UID9622
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:       🟡 待验证
镜像:       dragonsoul/belt-road:1.1
架构:       linux/amd64, linux/arm64
阶段:       3阶段构建 (llama-builder + python-builder + runtime)
体积估算:   400-450MB (不含模型)
未验证项:   9项 (🟡6 🔴3)
══════════════════════════════════════════════════════════════════════════
```

🐉 丙午·丙申·戊午·鼎卦·🟡

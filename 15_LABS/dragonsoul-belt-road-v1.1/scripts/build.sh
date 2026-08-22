#!/bin/bash
# 龍魂 · Docker 多架构构建脚本 v1.1
# DNA: #龍芯⚡️丙午·丙申·戊午·戊午·䷱鼎-BELT-ROAD-PACK-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 许可: MulanPSL v2
# 用途: 构建 amd64/arm64 多架构镜像，推送到 registry
# 前置要求: Docker Buildx 已启用，registry 已登录

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[龍魂·构建]${NC} $1"; }
warn() { echo -e "${YELLOW}[警告]${NC} $1"; }
error() { echo -e "${RED}[错误]${NC} $1"; exit 1; }
info() { echo -e "${BLUE}[信息]${NC} $1"; }

# 默认配置
REGISTRY="${REGISTRY:-dragonsoul}"
IMAGE_NAME="${IMAGE_NAME:-belt-road}"
VERSION="${VERSION:-1.1}"
PLATFORMS="${PLATFORMS:-linux/amd64,linux/arm64}"
PUSH="${PUSH:-0}"
LOAD="${LOAD:-1}"
MODEL_SIZE="${MODEL_SIZE:-7b}"

# 构建参数
BUILD_ARGS=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --registry) REGISTRY="$2"; shift 2 ;;
        --version) VERSION="$2"; shift 2 ;;
        --platforms) PLATFORMS="$2"; shift 2 ;;
        --push) PUSH=1; LOAD=0; shift ;;
        --load) LOAD=1; PUSH=0; shift ;;
        --model-size) MODEL_SIZE="$2"; shift 2 ;;
        --help|-h)
            echo "用法: $0 [选项]"
            echo ""
            echo "选项:"
            echo "  --registry REG    镜像仓库 (默认: dragonsoul)"
            echo "  --version VER     版本号 (默认: 1.1)"
            echo "  --platforms PLAT  目标平台 (默认: linux/amd64,linux/arm64)"
            echo "  --push            构建并推送到 registry"
            echo "  --load            构建并加载到本地 Docker (默认)"
            echo "  --model-size SIZE 模型大小 (默认: 7b)"
            echo "  --help, -h        显示此帮助"
            exit 0
            ;;
        *) warn "未知参数: $1"; shift ;;
    esac
done

FULL_IMAGE="${REGISTRY}/${IMAGE_NAME}:${VERSION}"
LATEST_IMAGE="${REGISTRY}/${IMAGE_NAME}:latest"

log "═══════════════════════════════════════════════════════"
log "  🐉 龍魂 · Docker 多架构构建"
log "═══════════════════════════════════════════════════════"
log "  镜像: ${FULL_IMAGE}"
log "  平台: ${PLATFORMS}"
log "  模型: ${MODEL_SIZE}"
log "  推送: ${PUSH}"
log "  加载: ${LOAD}"
log "═══════════════════════════════════════════════════════"

# ========== 前置检查 ==========
check_prerequisites() {
    log "=== 前置检查 ==="

    # Docker 检查
    if ! command -v docker &>/dev/null; then
        error "Docker 未安装"
    fi
    log "Docker: $(docker --version) ✓"

    # Buildx 检查
    if ! docker buildx version &>/dev/null; then
        error "Docker Buildx 未启用。请运行: docker buildx create --use"
    fi
    log "Buildx: $(docker buildx version | head -1) ✓"

    # 多架构构建器检查
    if ! docker buildx ls | grep -q "linux/arm64"; then
        warn "Buildx 可能不支持 arm64，尝试安装 qemu..."
        docker run --rm --privileged multiarch/qemu-user-static --reset -p yes ||             warn "qemu 安装失败，arm64 构建可能不可用"
    fi

    # 登录检查（如需推送）
    if [ "$PUSH" -eq 1 ]; then
        if ! docker info 2>/dev/null | grep -q "Username"; then
            warn "未检测到 Docker 登录状态，推送可能失败"
        fi
    fi

    # 文件检查
    if [ ! -f "Dockerfile" ]; then
        error "Dockerfile 未找到"
    fi
    if [ ! -f "docker-entrypoint.sh" ]; then
        error "docker-entrypoint.sh 未找到"
    fi
    if [ ! -f "requirements.txt" ]; then
        error "requirements.txt 未找到"
    fi

    log "前置检查完成 ✓"
}

# ========== 构建镜像 ==========
build_image() {
    log "=== 构建镜像 ==="

    BUILD_OPTS=""

    if [ "$PUSH" -eq 1 ]; then
        BUILD_OPTS="--push"
    elif [ "$LOAD" -eq 1 ]; then
        # 多平台构建不能 --load，只能单平台
        if echo "$PLATFORMS" | grep -q ","; then
            warn "多平台构建无法使用 --load，将仅构建不加载"
            BUILD_OPTS=""
        else
            BUILD_OPTS="--load"
        fi
    fi

    log "开始构建..."
    docker buildx build         --platform "$PLATFORMS"         --build-arg DRAGONSOUL_VERSION="$VERSION"         --build-arg MODEL_SIZE="$MODEL_SIZE"         --tag "$FULL_IMAGE"         --tag "$LATEST_IMAGE"         $BUILD_OPTS         --cache-from "type=local,src=/tmp/.buildx-cache"         --cache-to "type=local,dest=/tmp/.buildx-cache,mode=max"         -f Dockerfile         . || error "构建失败"

    log "构建完成 ✓"
}

# ========== 验证镜像 ==========
verify_image() {
    if [ "$PUSH" -eq 1 ]; then
        log "推送模式：跳过本地验证"
        return 0
    fi

    if [ "$LOAD" -eq 0 ]; then
        log "未加载到本地：跳过本地验证"
        return 0
    fi

    log "=== 镜像验证 ==="

    # 检查镜像是否存在
    if ! docker images | grep -q "$IMAGE_NAME"; then
        warn "镜像未加载到本地"
        return 0
    fi

    # 运行容器测试
    log "启动测试容器..."
    CONTAINER_ID=$(docker run -d         --name dragonsoul-test         -p 18080:8080         -e DEFAULT_LANG=en         -e MODEL_SIZE=3b         -e OFFLINE_MODE=1         "$FULL_IMAGE")

    log "等待容器启动..."
    sleep 10

    # 健康检查
    if curl -fsSL http://localhost:18080/health &>/dev/null; then
        log "健康检查: 通过 ✓"
    else
        warn "健康检查: 失败（可能因模型未加载）"
    fi

    # 查看日志
    log "容器日志:"
    docker logs --tail 20 dragonsoul-test

    # 清理
    docker stop dragonsoul-test &>/dev/null || true
    docker rm dragonsoul-test &>/dev/null || true

    log "验证完成"
}

# ========== 打印摘要 ==========
print_summary() {
    log ""
    log "═══════════════════════════════════════════════════════"
    log "  🎉 构建完成！"
    log "═══════════════════════════════════════════════════════"
    log "  镜像: ${FULL_IMAGE}"
    log "  标签: ${LATEST_IMAGE}"
    log "  平台: ${PLATFORMS}"
    log ""
    if [ "$PUSH" -eq 1 ]; then
        log "  已推送到 registry"
    fi
    log ""
    log "  运行测试:"
    log "    docker run -d -p 8080:8080 \"
    log "      -e DEFAULT_LANG=ar \"
    log "      -e MODEL_SIZE=7b \"
    log "      -v ./models:/app/models \"
    log "      ${FULL_IMAGE}"
    log ""
    log "  查看日志:"
    log "    docker logs -f <container_id>"
    log "═══════════════════════════════════════════════════════"
}

# ========== 主流程 ==========
main() {
    check_prerequisites
    build_image
    verify_image
    print_summary
}

main "$@"

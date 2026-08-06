# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-DOCKER-BAKE-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
#
# 龍魂多架构 Docker 构建矩阵
# 用法:
#   全部构建:    docker buildx bake all
#   只鲲鹏:      docker buildx bake kunpeng
#   只昇腾:      docker buildx bake ascend
#   只龙芯:      docker buildx bake loongson
#   只飞腾:      docker buildx bake phytium
#   只通用x86:   docker buildx bake generic-x86
#   只通用ARM:   docker buildx bake generic-arm
#   模拟构建:    docker buildx bake --print all

variable "REGISTRY" {
  default = "uid9622.cn"
}

variable "IMAGE_TAG" {
  default = "latest"
}

# ══════════════════════════════════════════════
# 共用基础配置
# ══════════════════════════════════════════════

group "all" {
  targets = [
    "kunpeng",
    "ascend",
    "loongson",
    "phytium",
    "generic-x86",
    "generic-arm",
  ]
}

group "china-chips" {
  targets = [
    "kunpeng",
    "ascend",
    "loongson",
    "phytium",
  ]
}

# ══════════════════════════════════════════════
# 目标定义
# ══════════════════════════════════════════════

target "kunpeng" {
  inherits   = ["_base-arm64"]
  dockerfile = "kunpeng.Dockerfile"
  platforms  = ["linux/arm64"]
  tags       = ["${REGISTRY}/longhun:kunpeng-${IMAGE_TAG}"]
  args = {
    BUILD_FLAGS = "-march=armv8.2-a+fp16+rcpc+dotprod+sm3+sm4+aes+sha2"
    CHIP_TARGET = "kunpeng"
  }
}

target "ascend" {
  inherits   = ["_base-arm64"]
  dockerfile = "ascend.Dockerfile"
  platforms  = ["linux/arm64"]
  tags       = ["${REGISTRY}/longhun:ascend-${IMAGE_TAG}"]
  args = {
    CHIP_TARGET   = "ascend"
    CANN_VERSION  = "8.0.RC1"
  }
}

target "loongson" {
  inherits   = ["_base-loongarch"]
  dockerfile = "loongson.Dockerfile"
  platforms  = ["linux/loong64"]
  tags       = ["${REGISTRY}/longhun:loongson-${IMAGE_TAG}"]
  args = {
    BUILD_FLAGS = "-march=loongarch64 -mabi=lp64d"
    CHIP_TARGET = "loongson"
  }
}

target "phytium" {
  inherits   = ["_base-arm64"]
  dockerfile = "kunpeng.Dockerfile"   # 飞腾复用 ARMv8 Dockerfile（无特殊加速器）
  platforms  = ["linux/arm64"]
  tags       = ["${REGISTRY}/longhun:phytium-${IMAGE_TAG}"]
  args = {
    BUILD_FLAGS = "-march=armv8-a+crc+crypto"
    CHIP_TARGET = "phytium"
  }
}

target "generic-x86" {
  inherits   = ["_base-x86"]
  dockerfile = "generic.Dockerfile"
  platforms  = ["linux/amd64"]
  tags       = ["${REGISTRY}/longhun:generic-x86-${IMAGE_TAG}"]
  args = {
    BUILD_FLAGS = "-march=x86-64-v2"
    CHIP_TARGET = "generic-x86"
  }
}

target "generic-arm" {
  inherits   = ["_base-arm64"]
  dockerfile = "generic.Dockerfile"
  platforms  = ["linux/arm64"]
  tags       = ["${REGISTRY}/longhun:generic-arm-${IMAGE_TAG}"]
  args = {
    BUILD_FLAGS = "-march=armv8-a"
    CHIP_TARGET = "generic-arm"
  }
}

# ══════════════════════════════════════════════
# 基础模板
# ══════════════════════════════════════════════

target "_base-arm64" {
  context  = "."
  output   = ["type=docker"]
}

target "_base-x86" {
  context  = "."
  output   = ["type=docker"]
}

target "_base-loongarch" {
  context  = "."
  output   = ["type=docker"]
}

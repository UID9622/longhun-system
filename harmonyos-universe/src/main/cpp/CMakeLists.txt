# DNA: #龍芯⚡️丙午·丙申·乙卯·申时·䷐随-HARMONY-GUOMI-NATIVE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 用途: 龍魂国密 Native 核心 · 与 iOS LonghunKit/CGuomi 同源（三端同一加密内核）

cmake_minimum_required(VERSION 3.5.0)
project(longhuncore)

set(NATIVERENDER_ROOT_PATH ${CMAKE_CURRENT_SOURCE_DIR})

include_directories(${NATIVERENDER_ROOT_PATH}
                    ${NATIVERENDER_ROOT_PATH}/guomi)

# 龍魂国密底座: SM2(GB/T 32918) + SM3(GB/T 32905) + SM4(GB/T 32907)
# 纯 C99 零外部依赖 · 鸿蒙 ARM64 原生编译
add_library(longhuncore SHARED
    napi_init.cpp
    guomi/sm2.c
    guomi/sm3.c
    guomi/sm4.c
)

find_package(ace_napi REQUIRED)
target_link_libraries(longhuncore PUBLIC libace_napi.z.so)

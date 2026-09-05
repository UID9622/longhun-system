# DNA: #龍芯⚡️2026-09-05-CNSH-BRIDGE-CMAKE-v0.1-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 用途: 鸿蒙 NDK 构建 CNSH 桥接 .so（libcnsh_bridge.so）
# 接入: 复制本目录到 entry/src/main/cpp/，并在 entry 的 build-profile.json5
#       externalNativeOptions.path 指向 ./src/main/cpp/CMakeLists.txt

cmake_minimum_required(VERSION 3.5.0)
project(cnsh_bridge)

# cnsh_logic.c 由 cnsh_napi.cpp unity include，故只编译桥文件
add_library(cnsh_bridge SHARED cnsh_napi.cpp)

target_link_libraries(cnsh_bridge PUBLIC libace_napi.z.so libhilog_ndk.z.so)

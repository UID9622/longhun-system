# DNA: #龍芯⚡️丙午·丙申·壬子·子时·䷕贲-HARMONY-NAPI-CMAKE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 协议: MulanPSL v2 (工程层)
# 用途: 鸿蒙 NAPI 构建 — 编译 liblonghun_napi.so

cmake_minimum_required(VERSION 3.16.0)
project(longhun_napi)

set(NATIVERENDER_ROOT_PATH ${CMAKE_CURRENT_SOURCE_DIR})

# 鸿蒙 SDK 路径（需配置）
if(DEFINED OHOS_SDK_NATIVE)
    set(OHOS_SDK_NATIVE_PATH ${OHOS_SDK_NATIVE})
else()
    set(OHOS_SDK_NATIVE_PATH ${CMAKE_SOURCE_DIR}/../../../ohos-sdk/native)
    message(WARNING "OHOS_SDK_NATIVE not set, using ${OHOS_SDK_NATIVE_PATH}")
endif()

# 获取目标架构
if(CMAKE_SYSTEM_PROCESSOR STREQUAL "aarch64")
    set(RUST_TARGET "aarch64-linux-android")
    set(OHOS_ARCH "arm64-v8a")
elseif(CMAKE_SYSTEM_PROCESSOR STREQUAL "arm")
    set(RUST_TARGET "armv7-linux-androideabi")
    set(OHOS_ARCH "armeabi-v7a")
elseif(CMAKE_SYSTEM_PROCESSOR STREQUAL "x86_64")
    set(RUST_TARGET "x86_64-linux-android")
    set(OHOS_ARCH "x86_64")
else()
    message(FATAL_ERROR "Unsupported architecture: ${CMAKE_SYSTEM_PROCESSOR}")
endif()

message(STATUS "Building longhun_napi for ${RUST_TARGET}")

# Rust NAPI 库路径
set(LONGHUN_NAPI_DIR "${CMAKE_SOURCE_DIR}/../../rust/longhun-napi")
set(RUST_OUTPUT_DIR "${LONGHUN_NAPI_DIR}/target/${RUST_TARGET}/release")
set(OUTPUT_LIB "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/liblonghun_napi.so")

# 调用 cargo 编译
add_custom_command(
    OUTPUT ${OUTPUT_LIB}
    COMMAND cargo build --release --target ${RUST_TARGET} --manifest-path ${LONGHUN_NAPI_DIR}/Cargo.toml
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}
    COMMAND ${CMAKE_COMMAND} -E copy
        ${RUST_OUTPUT_DIR}/liblonghun_napi.so
        ${OUTPUT_LIB}
    COMMENT "Building liblonghun_napi.so via cargo..."
    DEPENDS
        ${LONGHUN_NAPI_DIR}/src/lib.rs
        ${LONGHUN_NAPI_DIR}/Cargo.toml
)

add_custom_target(longhun_napi ALL DEPENDS ${OUTPUT_LIB})

# 安装
install(FILES ${OUTPUT_LIB} DESTINATION libs/${OHOS_ARCH})

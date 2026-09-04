# DNA: #龍芯⚡️丙午·丙申·壬子·子时·䷕贲-ANDROID-JNI-CMAKE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 协议: MulanPSL v2 (工程层)
# 用途: Android JNI 构建 — 编译 longhun_jni.so 供 Android 项目使用

cmake_minimum_required(VERSION 3.22.1)
project("longhun-core-jni")

set(CMAKE_CXX_STANDARD 17)

# Rust 编译为 .so
# 方式1: 预编译 .so 放入 jniLibs/
# 方式2: 用 cargo-ndk 在 CMake 中调用（推荐）

# 检查环境变量
if(NOT DEFINED ENV{ANDROID_NDK_HOME})
    message(WARNING "ANDROID_NDK_HOME not set, using default toolchain")
endif()

# 获取 Rust 编译目标
if(CMAKE_SYSTEM_PROCESSOR STREQUAL "aarch64")
    set(RUST_TARGET "aarch64-linux-android")
    set(ANDROID_ABI "arm64-v8a")
elseif(CMAKE_SYSTEM_PROCESSOR STREQUAL "armv7-a")
    set(RUST_TARGET "armv7-linux-androideabi")
    set(ANDROID_ABI "armeabi-v7a")
elseif(CMAKE_SYSTEM_PROCESSOR STREQUAL "x86_64")
    set(RUST_TARGET "x86_64-linux-android")
    set(ANDROID_ABI "x86_64")
else()
    message(FATAL_ERROR "Unsupported ABI: ${CMAKE_SYSTEM_PROCESSOR}")
endif()

message(STATUS "Building longhun_jni for ${RUST_TARGET} (${ANDROID_ABI})")

# 调用 cargo 构建
set(LONGHUN_JNI_DIR "${CMAKE_SOURCE_DIR}/../../rust/longhun-jni")
set(OUTPUT_LIB "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/liblonghun_jni.so")

add_custom_command(
    OUTPUT ${OUTPUT_LIB}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}
    COMMAND cargo build --release --target ${RUST_TARGET} --manifest-path ${LONGHUN_JNI_DIR}/Cargo.toml
    COMMAND ${CMAKE_COMMAND} -E copy
        ${LONGHUN_JNI_DIR}/target/${RUST_TARGET}/release/liblonghun_jni.so
        ${OUTPUT_LIB}
    COMMENT "Building longhun_jni.so via cargo-ndk..."
    DEPENDS
        ${LONGHUN_JNI_DIR}/src/lib.rs
        ${LONGHUN_JNI_DIR}/Cargo.toml
)

add_custom_target(longhun_jni ALL DEPENDS ${OUTPUT_LIB})

# 安装到 jniLibs
install(FILES ${OUTPUT_LIB} DESTINATION jniLibs/${ANDROID_ABI})

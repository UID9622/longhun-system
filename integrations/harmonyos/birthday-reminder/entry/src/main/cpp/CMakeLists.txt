# 龍魂 · Native 并发与高性能计算 · CMake 构建配置
# DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-CMAKE-v1.0
# 联动: 生日提醒v2.0 · 情感协议 · 人格路由

cmake_minimum_required(VERSION 3.4.1)
project(longhun_native)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ============================================================================
# 编译选项
# ============================================================================

# ARM NEON 优化（鸿蒙设备默认启用）
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O3 -march=armv8-a+fp+simd -fopenmp")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -march=armv8-a+fp+simd -fopenmp")

# 安全编译选项
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fstack-protector-strong -D_FORTIFY_SOURCE=2")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fstack-protector-strong -D_FORTIFY_SOURCE=2")

# 调试符号（Release 保留以便崩溃分析）
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -g")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")

# ============================================================================
# 源文件
# ============================================================================
set(LONGHUN_SOURCES
    src/napi_bridge.cpp
    src/thread_pool.cpp
    src/simd_voice_features.cpp
    src/neon_utils.cpp
)

# ============================================================================
# 共享库
# ============================================================================
add_library(longhun_native SHARED ${LONGHUN_SOURCES})

# ============================================================================
# 包含目录
# ============================================================================
target_include_directories(longhun_native PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# ============================================================================
# 链接系统库
# ============================================================================
target_link_libraries(longhun_native PUBLIC
    libace_napi.z.so          # NAPI 桥接
    libhilog_ndk.z.so         # 日志系统
    librawfile.z.so           # 资源文件访问
    libc++.so                 # C++ 标准库
    libm.so                   # 数学库
    libpthread.so             # 线程库
)

# ============================================================================
# 可选：大页内存
# ============================================================================
option(USE_HUGE_PAGES "Enable huge pages support" OFF)
if(USE_HUGE_PAGES)
    target_compile_definitions(longhun_native PRIVATE USE_HUGE_PAGES)
    message(STATUS "龍魂 Native: 大页内存已启用")
endif()

# ============================================================================
# 可选：NUMA 支持
# ============================================================================
option(USE_NUMA "Enable NUMA binding" OFF)
if(USE_NUMA)
    target_compile_definitions(longhun_native PRIVATE USE_NUMA)
    target_link_libraries(longhun_native PUBLIC libnuma.so)
    message(STATUS "龍魂 Native: NUMA 绑核已启用")
endif()

# ============================================================================
# 可选：性能分析
# ============================================================================
option(ENABLE_PROFILING "Enable performance profiling" OFF)
if(ENABLE_PROFILING)
    target_compile_definitions(longhun_native PRIVATE LONGHUN_PROFILING)
    message(STATUS "龍魂 Native: 性能分析已启用")
endif()

# ============================================================================
# 构建信息输出
# ============================================================================
message(STATUS "============================================")
message(STATUS "  龍魂 Native 构建配置")
message(STATUS "  DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️")
message(STATUS "  UID: 9622")
message(STATUS "  C++标准: C++17")
message(STATUS "  优化: -O3 + NEON SIMD")
message(STATUS "  源文件: ${LONGHUN_SOURCES}")
message(STATUS "============================================")

# 来源标注: #ZHUGEXIN⚡️ | UID9622 龍魂体系
# 模块定位: CNSH 字元渲染引擎 · 基础三次贝塞尔层

cmake_minimum_required(VERSION 3.10)
project(LongHunTraceCore VERSION 1.1 LANGUAGES CXX)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 查找 OpenSSL
find_package(OpenSSL REQUIRED)

# 添加可执行文件
add_executable(longhun_trace
    main.cpp
)

# 链接 OpenSSL
target_link_libraries(longhun_trace
    PRIVATE
    OpenSSL::Crypto
)

# 设置编译选项
if(MSVC)
    target_compile_options(longhun_trace PRIVATE /W4)
else()
    target_compile_options(longhun_trace PRIVATE -Wall -Wextra -pedantic)
endif()

# 安装规则
install(TARGETS longhun_trace
    RUNTIME DESTINATION bin
)

# llama.cpp/example/simple-cmake-pkg

This program builds [simple](../simple) using a relocatable CMake package. It serves as an example of using the `find_package()` CMake command to conveniently include [llama.cpp](https://github.com/ggml-org/llama.cpp) in projects which live outside of the source tree.

## Building

Because this example is "outside of the source tree", it is important to first build/install llama.cpp using CMake. An example is provided here, but please see the [llama.cpp build instructions](../..) for more detailed build instructions.

### Considerations

When hardware acceleration libraries are used (e.g. CUDA, Metal, Vulkan, etc.), the appropriate dependencies will be searched for automatically. So, for example, when finding a package

### Build llama.cpp and install to llama.cpp/inst

```sh
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
cmake -S . -B build
cmake --build build
cmake --install build --prefix inst

### Build simple-cmake-pkg

```sh
cd examples/simple-cmake-pkg
cmake -S . -B build -DCMAKE_PREFIX_PATH=../../inst/lib/cmake
cmake --build build
```

### Run simple-cmake-pkg

```sh
./build/llama-simple-cmake-pkg -m ./models/llama-7b-v2/ggml-model-f16.gguf "Hello my name is"
```

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-daa14d81-20251218032410
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 坤卦：地势坤，君子以厚德载物
📜 内容哈希: 142fe9e488bf1003
⚠️ 警告: 未经授权修改将触发DNA追溯系统

# 🐉 龍魂·Rust 核心库 · ARM64 二进制

> 占位文件。待 `longhun-core` Rust 项目编译 aarch64-linux-android 目标后替换。

## 编译命令

```bash
cd longhun-core
cargo build --target aarch64-linux-android --release
cp target/aarch64-linux-android/release/liblonghun_core.so ../harmonyos/plugins/01-core-service/libs/arm64-v8a/
```

## 导出符号 (C ABI → ArkTS NAPI)

| 函数 | 签名 | 说明 |
|:---|:---|:---|
| `longhun_governance_check` | `fn(ptr: *const c_char) -> i32` | 治理检查·返回三色码 |
| `longhun_dna_verify` | `fn(ptr: *const c_char) -> bool` | DNA校验 |
| `longhun_memory_hash` | `fn(data: *const u8, len: usize, out: *mut u8)` | 记忆哈希 |
| `longhun_free_string` | `fn(ptr: *mut c_char)` | 释放C字符串 |

## 当前状态

- [ ] Rust 编译 → aarch64-linux-android
- [ ] NAPI 桥接适配
- [ ] 鲲鹏实机验证

> DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-LIB-RUST-CORE-UID9622

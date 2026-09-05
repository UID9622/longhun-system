# Changelog · cnsh-bridge（CNSH × 鸿蒙原生桥）

> DNA: `#龍芯⚡️2026-09-05-CNSH-BRIDGE-CHANGELOG-v1.0-UID9622`
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰 · License: MulanPSL v2（工程实现层）
> 变更按时间倒序 · 版本号: v0.1.x（首个真实落地系列）

## v0.1.1（2026-09-05）— 小艺AI评审吸收

- 桥方法补 `napi_throw_error` 参数校验（问候/三色审计 · ArkTS 侧可 try/catch 捕获）
- CMake 显式 `CMAKE_CXX_STANDARD 17` · 标注 N-API v12（HarmonyOS API 12+）
- README 补工程化配置：`build-profile.json5` externalNativeOptions / abiFilters（arm64-v8a·x86_64）/ GitHub Actions 参考
- 新增 CONTRIBUTING.md（无偿署名贡献准则）· 本 CHANGELOG
- 无编造性能口径：仅本机 clang 语义实测，设备基准待 DevEco 实机后如实补录

## v0.1.0（2026-09-05）— 首个真实落地

- `08_BIN/cnsh_cgen.py` v0.1：CNSH→C 翻译器（纯标准库 · if 无括号/字符串拼接/递归/类型推断/多参打印）
  实机对拍 3 语法样本（test_hello/test_fibonacci/test_operators）全对
- `cnsh/hello.cnsh`（真实语法演示源）→ `cpp/cnsh_logic.c`（自动生成 · clang 冒烟通过）
- `cpp/cnsh_napi.cpp`：N-API(C API) unity 桥，导出 问候/三色审计/自检(DNA+GPG 编译期常量)
- `cpp/CMakeLists.txt` + `arkts/CnshBridgeDemo.ets` + `cnsh.json` + README
- 提交 dfbe33405 · 闸口 CLI_COMMAND 留档 · push gh-ssh 成功

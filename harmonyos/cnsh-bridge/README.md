# 🧬 CNSH × 鸿蒙原生桥（cnsh-bridge）v0.1

> DNA: `#龍芯⚡️2026-09-05-CNSH-BRIDGE-v0.1-UID9622`
> 创建者: 诸葛鑫 | UID9622 · 龍芯北辰
> License: MulanPSL v2（工程实现层）
> 真实落点: `harmonyos/cnsh-bridge/`（longhun-system monorepo）· 语法权威: `tests/cnsh_samples/`

## 本模块解决什么

把「CNSH → C/C++ → 鸿蒙 NDK → ArkTS」三层路径落地成**可编译、可验证、真实语法**的代码：

| 文件 | 说明 | 验证状态 |
|:---|:---|:---|
| `cnsh/hello.cnsh` | CNSH 真实语法源（字符串拼接/空判/三色审计语义） | ✅ 翻译+运行全对 |
| `cpp/cnsh_logic.c` | 由 `cnsh_cgen.py --no-main` 自动生成（勿手改） | ✅ clang 冒烟编译通过 |
| `cpp/cnsh_napi.cpp` | 鸿蒙 N-API(C API) 桥：导出 问候/三色审计/自检 | 🟡 需 DevEco 实机构建 |
| `cpp/CMakeLists.txt` | 鸿蒙 NDK 构建 `libcnsh_bridge.so` | 🟡 同上 |
| `arkts/CnshBridgeDemo.ets` | ArkTS 调用演示页 | 🟡 同上 |
| `cnsh.json` | 模块配置/工具链/接入步骤 | ✅ |

## 本机已验证（判据④）

```bash
cd ~/longhun-system
# 1) 真实语法样本端到端（翻译 → clang → 运行）
python3 08_BIN/cnsh_cgen.py tests/cnsh_samples/test_hello.cnsh     # → 你好，龍魂！
python3 08_BIN/cnsh_cgen.py tests/cnsh_samples/test_fibonacci.cnsh # → 斐波那契( 0..9 ) = 0,1,1,2,3,5,8,13,21,34
python3 08_BIN/cnsh_cgen.py tests/cnsh_samples/test_operators.cnsh # → 13/7/30/3/1/1000 真/假…全对
# 2) 鸿蒙演示源全链路
python3 08_BIN/cnsh_cgen.py harmonyos/cnsh-bridge/cnsh/hello.cnsh --out /tmp/x.c && clang /tmp/x.c -o /tmp/x && /tmp/x
#   🐉 龍魂·鸿蒙，你好，鸿蒙开发者！
#   🟢 输入通过审计
#   🔴 空输入，拒绝
# 3) 桥接逻辑层冒烟
python3 08_BIN/cnsh_cgen.py harmonyos/cnsh-bridge/cnsh/hello.cnsh --no-main --out harmonyos/cnsh-bridge/cpp/cnsh_logic.c
clang -c -O0 -o /tmp/cnsh_logic.o harmonyos/cnsh-bridge/cpp/cnsh_logic.c
```

## 接入 DevEco（鸿蒙侧 · 🟡 待实机）

1. 把 `cpp/` 复制到鸿蒙工程 `entry/src/main/cpp/`
2. `entry/build-profile.json5` 的 `buildOption.externalNativeOptions` 指向 `./src/main/cpp/CMakeLists.txt`（参考 `harmonyos/apps/tricolor-audit/build-profile.json5` 已预留该配置位）
3. ArkTS 侧：`import cnshBridge from 'libcnsh_bridge.so'`（示例见 `arkts/CnshBridgeDemo.ets`）
4. 要求：DevEco Studio 5.0.3.900+ / HarmonyOS SDK API 12+ / 支持 N-API

## 工程化配置（v0.1.1 · 小艺AI评审吸收）

> 评审基线：小艺AI 对《鸿蒙原生集成方案》外部稿的审稿；本表对照**真实模块**逐条裁决。

| 评审建议 | 落地裁决 |
|:---|:---|
| 包名/加载写法 | 模块名=`cnsh_bridge`（`nm_modname`）→ ArkTS `import cnshBridge from 'libcnsh_bridge.so'`（官方规范） |
| N-API 版本标注 | N-API v12 · HarmonyOS API 12+（`cnsh_napi.cpp` 头注释已标） |
| C++ 标准 | `set(CMAKE_CXX_STANDARD 17)`（`CMakeLists.txt` 已落） |
| 日志头文件 | 本桥同步纯函数零日志；如需打点按头注释引入 `hilog/log.h`（无未用头） |
| 错误处理 | ✅ 已补 `napi_throw_error` 参数校验（问候/三色审计 · `.ets` 侧可 try/catch） |
| 线程安全 | 本桥无共享可变状态→无需 threadsafe；异步大计算再按 N-API threadsafe 扩展（头注释已声明边界） |
| 性能数据 | 无编造：本桥无设备基准；仅本机 clang 语义实测（见上节），DevEco 实机后如实补录 |
| 构建产物/ABI | `build-profile.json5` `abiFilters` 见下方范例 |

`entry/build-profile.json5`（参考 `harmonyos/apps/tricolor-audit/` 真实工程格式）：

```json5
"buildOption": {
  "externalNativeOptions": {
    "path": "./src/main/cpp/CMakeLists.txt",
    "arguments": "-DUSE_HUGE_PAGES=OFF",
    "cppFlags": "-O2",
    "abiFilters": ["arm64-v8a", "x86_64"]   // 真机+模拟器；纯真机发布可只留 arm64-v8a
  }
}
```

GitHub Actions 参考（fork 到独立仓库后启用 · monorepo 内不生效）：

```yaml
name: cnsh-bridge-build
on: [push, pull_request]
jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          python3 08_BIN/cnsh_cgen.py harmonyos/cnsh-bridge/cnsh/hello.cnsh --out /tmp/x.c
          gcc /tmp/x.c -o /tmp/x && /tmp/x    # CNSH→C 全链路冒烟
      # 鸿蒙 .so 构建需 HarmonyOS NDK/DevEco（API 12+），另行配置 ohos 矩阵
```

仓库工程化：LICENSE=MulanPSL v2（monorepo 根已置，本模块复用不重复）· CHANGELOG/CONTRIBUTING 本目录已补。

## 与 UID9622 生态仓库的对应（诚实版）

- **不存在** `github.com/UID9622/cnsh-compiler` / `cnsh-runtime` / `cnsh-harmony-demo`（外部文章常误引，v0.1 本模块即 monorepo 内落地物）
- **真实存在**：`github.com/UID9622/cnsh-spec`（CNSH 中文结构化语法规范）· `github.com/UID9622/CNSH`（中文母语脚本/字形编辑器）· `github.com/UID9622/cnsh-suite`（DeepSeek Harness 插件）
- 翻译器源码: `08_BIN/cnsh_cgen.py` v0.1（纯标准库 · 单文件 · 支持子集见文件头）

## 三色

🟢 CNSH→C 全链路本机实跑通过（3 语法样本 + 鸿蒙演示源） · 🟡 鸿蒙 `.so`/ArkTS 需 DevEco 实机 · 🔴 0

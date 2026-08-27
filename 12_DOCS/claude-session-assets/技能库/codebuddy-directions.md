<!-- DNA: #龍芯⚡️丙午·丙申·甲戌·卯时·䷐随-QUAD-SYNC-v1.0-ATTRIBUTION-8c26d5f -->
<!-- 归属名: 诸葛鑫 | UID9622 · 龍芯北辰 -->
# 🐉 龙魂系统 · CodeBuddy 执行方向书

## 最终目标

**中国生态统一中国芯片 · 兼容鸿蒙 + iOS + Android · 一键搬迁**

## 总架构

```
┌────────────────────────────────────────────────────────────┐
│  龙魂应用层（Python CLI + Web + 记忆编辑器）                │
├────────────────────────────────────────────────────────────┤
│  ┌────────────┐ ┌──────────┐ ┌────────┐ ┌──────────────┐ │
│  │ 鸿蒙桥接器  │ │ iOS 桥接器│ │Android │ │ 中国芯片 HAL │ │
│  │ (ArkTS)    │ │ (Swift)  │ │ (Kotlin)│ │ (C/Rust)     │ │
│  └─────┬──────┘ └────┬─────┘ └───┬────┘ └──────┬───────┘ │
├────────┼──────────────┼──────────┼──────────────┼─────────┤
│        │      龙魂内核层（Rust FFI + Python）      │        │
│        │  CPU 检测 / NPU 路由 / 架构无关核心       │        │
├────────┼──────────────┼──────────┼──────────────┼─────────┤
│        │  ┌─────┐ ┌──────┐ ┌────────┐ ┌──────┐  │        │
│        │  │鲲鹏 │ │昇腾  │ │飞腾/龙芯│ │申威  │  │        │
│        │  │ARMv8│ │Ascend│ │LA/Phyt│ │SW260│  │        │
│        │  └─────┘ └──────┘ └────────┘ └──────┘  │        │
└────────┴─────────────────────────────────────────┴────────┘
```

## 阶段一：中国芯片 HAL（硬件抽象层）

**优先级：P0 · 地基级**

### 方向 1：芯片检测与特性发现

CodeBuddy 任务：写一个 `chip_detect.py` 模块

```python
# 检测当前 CPU 架构并返回最佳配置
def detect_chip() -> ChipInfo:
    # 支持检测：鲲鹏 920/昇腾 310/910/飞腾 S2500/龙芯 3A5000/申威 SW26010
    # 判断依据：vendor string + flags + 特定指令集
    pass
```

**给 CodeBuddy 的具体指令：**

```
1. 创建 longhun-core/chip_hal/ 目录
2. 实现 chip_detect.py：
   - 读取 /proc/cpuinfo 解析 vendor_id/cpu architecture/model name
   - 通过 /sys/class/devicetree/base/model 检测华为硬件
   - 检测 NPU 是否存在（Ascend 驱动）
   - 返回 ChipInfo dataclass: arch/vendor/cores/npu_available/npu_type
3. 为每种芯片创建 Python 适配器（至少接口签名），内容可空后续填充
4. 所有检测失败时降级到通用 ARM64 或 x86_64
```

### 方向 2：多架构 Docker 构建矩阵

CodeBuddy 任务：改造现有 Dockerfile 为多架构构建

**具体指令：**

```
1. 在 docker/ 创建多架构 Dockerfile：
   - base.Dockerfile → python:3.12-slim + apt upgrade（已修复的版本）
   - kunpeng.Dockerfile → ARM64 + Kunpeng 优化（-march=armv8.2-a+fp16+rcpc+dotprod）
   - ascend.Dockerfile → 基础镜像 + CANN 驱动层
   
2. 创建 docker-bake.hcl：
   - 目标: kunpeng / ascend / loongarch / phytium / generic-x86 / generic-arm
   - 每个目标设置 platform / 基础镜像 / 构建参数
   
3. 一键构建命令：
   docker buildx bake --file docker-bake.hcl all
```

### 方向 3：昇腾 NPU 加速路由

**具体指令：**

```
1. 创建 chip_hal/ascend_npu.py
2. 检测 /usr/local/Ascend/driver 是否存在
3. 如果存在，尝试 import torch_npu（昇腾 PyTorch 适配）
4. 如果不存在或失败，降级为 CPU 模式
5. 封装 compute_route(config) → 自动选择 NPU/CPU 执行路径
6. 不强制安装昇腾驱动，无驱动时静默降级
```

---

## 阶段二：鸿蒙桥接器

**优先级：P1 · 移动生态核心**

### 方向 4：龙魂内核 → ArkTS 服务包

**具体指令：**

```
1. 在 harmonyos/ 目录创建 HarmonyOS NEXT 工程骨架：
   harm
   onyos/
   ├── entry/
   │   ├── src/main/ets/
   │   │   ├── pages/          # UI 页面（记忆查看器、监督状态）
   │   │   ├── service/        # 后台 Service（持续运行的三层监督）
   │   │   └── workers/        # Worker 线程（Python + Rust FFI 桥接）
   │   └── module.json5
   ├── libs/                   # C++/Rust 编译产物 (.so)
   └── build-profile.json5

2. 核心桥接接口定义（ArkTS）：
   interface LonghunBridge {
     runSupervision(config: SupervisionConfig): Promise<SupervisionResult>;
     getMemory(query: string): Promise<MemoryEntry[]>;
     evolve(snapshot: EvolutionSnapshot): Promise<EvolutionResult>;
   }

3. 后台 Service 实现：
   - 使用 ServiceAbility 常驻后台
   - 每 30 分钟自动触发一次学习闭环
   - 使用 @ohos.distributedDeviceManager 跨设备同步
```

### 方向 5：鸿蒙分布式能力接入

**具体指令：**

```
1. 创建 harmonyos/super_device/ 模块
2. 实现分布式数据同步：
   - 使用 KVStore 跨手机/平板/笔记本共享记忆库
   - 使用 DataShare 在不同设备间同步监督状态
3. 实现跨设备调用：
   - Super Device 场景：手机训练 → 平板展示 → 笔记本执行
4. 权限声明：
   - ohos.permission.DISTRIBUTED_DATASYNC
   - ohos.permission.INTERNET
```

### 方向 6：鸿蒙原生 UI 适配

**具体指令：**

```
1. 创建记忆浏览页：List + SearchBar + 折叠卡
2. 创建监督状态仪表盘：环形图 + 实时状态流
3. ArkTS 组件遵循规范：@State/@Prop/@Link 数据流
4. 适配深色模式 + 折叠屏
```

---

## 阶段三：iOS 桥接器

**优先级：P1**

### 方向 7：Swift Package 核心包装

**具体指令：**

```
1. 创建 ios/LonghunKit/ 目录
2. 用 Rust 构建跨平台核心库（参考方向 13）：
   - rust/ 目录下 cbindgen 生成 C 头
   - Swift 通过 @_implementationOnly import C_longhun 调用
3. 定义 Swift 接口：
   protocol LonghunEngine {
     func runSupervision() async throws -> SupervisionReport
     func queryMemory(_ query: String) async -> [MemoryEntry]
     func getSystemHealth() -> HealthStatus
   }
4. 使用 Swift Async/Await 封装 Rust FFI 回调
```

### 方向 8：SwiftUI 前端

**具体指令：**

```
1. 创建 ios/LonghunApp/ SwiftUI 工程
2. 页面：仪表盘 / 记忆图谱 / 监督日志 / 设置
3. 使用 Core Data 做本地持久化缓存
4. 使用 Background Tasks 做后台监督轮询
5. 适配 iPad 分屏 + Apple Watch 通知
```

---

## 阶段四：Android 桥接器

**优先级：P2（鸿蒙优先）**

### 方向 9：JNI + Kotlin 包装

**具体指令：**

```
1. 创建 android/longhun-android/ 模块
2. Rust 核心库编译为 .so（arm64-v8a / armeabi-v7a / x86_64）
3. Kotlin 通过 JNI 调用 Rust 库
4. interface LonghunService 定义监督/记忆/进化三接口
5. WorkManager 实现后台周期执行
```

---

## 阶段五：一键搬迁工具

**优先级：P1 · 验收级**

### 方向 10：`lh-migrate` CLI 工具

**具体指令：**

```
1. 创建 tools/lh-migrate/ 目录
2. lh-migrate 核心流程：
   detect_platform() → 检测当前设备平台
   check_prerequisites() → 检查依赖（Docker/Python3/ArkTS/Swift）
   select_target() → 按平台选择搬迁目标（鸿蒙/iOS/Android/纯服务端）
   migrate() → 生成目标平台完整工程 + 配置 + Dockerfile

3. 子命令：
   lh-migrate detect              # 检测当前平台
   lh-migrate plan                # 输出搬迁方案
   lh-migrate run --target=harmonyos  # 执行搬迁到鸿蒙
   lh-migrate run --target=ios        # 执行搬迁到 iOS
   lh-migrate status              # 查看搬迁状态

4. 搬迁产出物示例（鸿蒙目标）：
   output/
   ├── harmonyos/          # 完整鸿蒙工程
   │   ├── entry/          
   │   ├── libs/           # Rust .so
   │   └── README.md
   ├── docker-compose.yml  # 服务器端配套
   └── config.json         # 搬迁配置
```

### 方向 11：平台感知配置注入

**具体指令：**

```
1. 在 lh-migrate 中添加 config 生成器
2. 检测到目标平台后自动生成：
   - 鸿蒙：module.json5 + 权限配置
   - iOS：Info.plist + entitlements
   - Android：AndroidManifest.xml
3. 将龙魂 DNA/主权锚定/确认码注入所有平台配置文件
4. 确保每个平台的 README 包含 GPG 签名
```

---

## 阶段六：统一内核

**优先级：P0 · 贯穿所有平台**

### 方向 12：Rust 核心库（跨平台底座）

**具体指令：**

```
1. 创建 rust/longhun-core/ cargo 项目
2. 构建三模块：
   - core/        → 监督状态机、DNA 校验、三色审计
   - memory/      → 记忆条目 CRUD、优先级排序、P0-P3 生命周期
   - evolution/   → 版本演进、熔断器、规则生成器

3. C ABI 导出（供所有平台 FFI 调用）：
   #[no_mangle]
   pub extern "C" fn longhun_run_supervision(...) -> ...
   pub extern "C" fn longhun_query_memory(...) -> ...

4. cbindgen 生成 longhun.h 头文件
5. 编译目标：
   - aarch64-unknown-linux-gnu (鲲鹏)
   - aarch64-linux-android (鸿蒙/Android)
   - aarch64-apple-ios (iOS)
   - x86_64-unknown-linux-gnu (x86 服务端)
```

### 方向 13：现有 Python 代码 → Rust 移植路线图

**具体指令：**

```
分三步迁移，不要一步到位：

[Step 1] Python → Python + Rust FFI（并行运行）
保持现有 Python 代码不变，Rust 库作为加速引擎可选接入
验证：两侧计算结果一致

[Step 2] 核心路径切 Rust（内存/监督状态机）
memory_lifecycle.py → rust/longhun-core/memory/
circuit_breaker.py → rust/longhun-core/evolution/
Python 调用 Rust 编译产物

[Step 3] 全部切 Rust（CLI 用 Rust 重写 + PyO3 导出 Python 模块）
最终形态：Rust 核心 + PyO3 Python 绑定 + FFI C 头供移动端
```

---

## CodeBuddy 执行队列（按顺序）

```
Queue 1 [P0] 芯片 HAL → chip_detect.py + Docker 多架构矩阵
Queue 2 [P0] Rust 核心库 cargo init + core/ 模块 + memory/ 模块
Queue 3 [P1] lh-migrate 基础骨架 + detect/plan 子命令
Queue 4 [P1] 鸿蒙桥接器 → ArkTS 服务包 + 分布式同步
Queue 5 [P1] iOS Swift Package + SwiftUI 工程骨架
Queue 6 [P2] Android JNI + Kotlin 包装
Queue 7 [P1] lh-migrate run 子命令（各平台生成器）
Queue 8 [P1] Rust evolution/ 模块移植
Queue 9 [P2] Python → Rust 全面迁移
Queue 10 [P2] 跨平台 CI/CD（GitHub Actions 多架构构建）
```

---

## 给 CodeBuddy 的工作方式建议

由于 CodeBuddy 一次处理一个文件的粒度，建议这样分批下发：

```
第 1 批 → "创建 chip_hal/ 目录，实现 chip_detect.py 芯片检测模块"
第 2 批 → "改造 Dockerfile 为 docker-bake.hcl 多架构构建矩阵"
第 3 批 → "创建 rust/longhun-core/ cargo 项目，实现 core 模块"
第 4 批 → "实现 lh-migrate CLI 工具 skeleton（detect/plan）"
第 5 批 → "创建 harmonyos/ 鸿蒙工程骨架"
第 6 批 → "创建 ios/LonghunKit Swift Package"
...按此顺序逐批下发
```

文件头标准（所有文件必须包含）：

```
DNA:   #龍芯⚡️丙午·癸未·乙酉-P0-MIGRATE-{模块名}-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
主权锚定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼♀️❤️♾️-DEVICE-BIND-SOUL
GPG:   A2D0092CEE2E5BA87035600924C3704A8CC26D5F
分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
三色:  🟢 通过
```

🐉 丙午 · 癸未 · 乙酉 · 乾卦（天行健，君子以自强不息）· 🟢

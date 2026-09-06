> 干支时间戳: #龍芯⚡️丙午·丁酉·癸未·子时·䷝离
<!-- 归属名: 诸葛鑫 | UID9622 · 龍芯北辰 -->
# 🐉 龙魂系统 · 鸿蒙 OS 插件生态 · CodeBuddy 执行指令书

## 目标

在 HarmonyOS NEXT（纯血鸿蒙）上建立龙魂完整插件生态，每颗插件独立可编译、可安装、可运行，最终组成 Super Device 超级终端全家桶。

## 总架构

```
HarmonyOS NEXT 设备
┌────────────────────────────────────────────────────────────┐
│  龙魂生态·鸿蒙插件族（每颗一个 HAP）                       │
│                                                             │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────────┐        │
│  │核心运行时│ │记忆浏览 │ │监督仪表  │ │主权验证      │        │
│  │Service  │ │Page    │ │Page     │ │Service       │        │
│  │Ability  │ │Ability │ │Ability  │ │Ability       │        │
│  ├────────┤ ├────────┤ ├────────┤ ├──────────────┤        │
│  │进化监控 │ │跨设备同步│ │桌面小组件│ │一键搬迁向导  │        │
│  │Service  │ │Service  │ │Form     │ │Page Ability  │        │
│  │Ability  │ │Ability  │ │Ability  │ │              │        │
│  └────────┘ └────────┘ └────────┘ └──────────────┘        │
│                                                             │
│  共享底座: liblonghun_core.so (Rust → C ABI → ArkTS FFI)   │
└────────────────────────────────────────────────────────────┘
                     ↓ 分布式总线
┌────────────────────────────────────────────────────────────┐
│  Super Device 跨设备协同                                      │
│  手机 ←→ 平板 ←→ 笔记本 ←→ 智慧屏 ←→ 手表                  │
│  记忆同步 · 监督分担 · 进化接力                              │
└────────────────────────────────────────────────────────────┘
```

---

## 插件 1：龙魂核心运行时 (longhun-core-service)

**这是所有插件的基础，必须先做。**

### CodeBuddy 指令

```
场景: 在 harmonyos/plugins/01-core-service/ 创建 Service Ability

步骤:
1. 创建目录结构：
   harmonyos/plugins/01-core-service/
   ├── entry/
   │   ├── src/main/
   │   │   ├── ets/
   │   │   │   ├── service/
   │   │   │   │   ├── LonghunCoreService.ets     # ServiceAbility 主入口
   │   │   │   │   ├── SupervisionEngine.ets       # 三层监督状态机
   │   │   │   │   ├── MemoryManager.ets           # 记忆 CRUD + P0-P3 生命周期
   │   │   │   │   ├── EvolutionWorker.ets         # 进化引擎 Worker 线程
   │   │   │   │   ├── SovereigntyVerifier.ets     # 主权完整性自检
   │   │   │   │   └── ChipDetector.ets            # 芯片 HAL 调用 (鸿蒙版)
   │   │   │   └── workers/
   │   │   │       └── LonghunWorker.ts            # Worker 线程入口
   │   │   └── resources/
   │   │       ├── base/element/
   │   │       │   └── string.json
   │   │       └── rawfile/
   │   │           └── longhun_config.json          # 默认配置（含 DNA/确认码）
   │   └── module.json5
   ├── libs/
   │   ├── arm64-v8a/
   │   │   └── liblonghun_core.so                  # Rust 编译产物（先留空占位）
   │   └── README.md
   └── build-profile.json5

2. LonghunCoreService.ets 实现：
   - 继承 ServiceAbility
   - onStart() → 加载 liblonghun_core.so, 初始化监督引擎, 启动 Worker
   - onCommand() → 接收 IPC 请求, 路由到对应引擎
   - onStop() → 持久化当前状态, 释放资源
   - IPC 接口定义（使用 @ohos.rpc）：
     interface ICoreService {
       runSupervision(config: string): Promise<string>;     // JSON in/out
       queryMemory(query: string): Promise<string>;
       getSystemStatus(): Promise<string>;
       triggerEvolution(): Promise<string>;
     }

3. SupervisionEngine.ets 实现（先纯 ArkTS 版，后续替换为 Rust FFI 调用）：
   - 14 人格矩阵定义（龙魂/雯雯/上帝之眼/审判长/诸葛亮/鲁班/宝宝/哨兵/织网/记忆守门人/数据大师/数学大师/量子观察者/老顽童）
   - 三层监督数据流: 决策层→执行层→行为层
   - 三色审计: 🟢🟡🔴 状态机
   - 每 30 分钟自动触发一次监督周期（使用 setInterval）

4. MemoryManager.ets 实现：
   - P0 永恒级 / P1 重要 / P2 普通 / P3 临时 四级存储
   - 使用 @ohos.data.preferences 持久化
   - 关键词检索 + 模糊匹配
   - DNA 追溯码生成

5. 所有文件头必须包含：
   DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-PLUGIN-CORE-SERVICE-UID9622
   确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
   主权锚定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼♀️❤️♾️-DEVICE-BIND-SOUL
   GPG:   A2D0092CEE2E5BA87035600924C3704A8CC26D5F
   分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
   三色:  🟢 通过
```

---

## 插件 2：龙魂记忆浏览 (longhun-memory-browser)

**UI 插件，依赖插件 1 提供数据。**

### CodeBuddy 指令

```
场景: 在 harmonyos/plugins/02-memory-browser/ 创建 Page Ability

步骤:
1. 目录结构：
   harmonyos/plugins/02-memory-browser/
   ├── entry/
   │   ├── src/main/ets/
   │   │   ├── pages/
   │   │   │   ├── MemoryList.ets         # 记忆列表页（主页面）
   │   │   │   ├── MemoryDetail.ets       # 记忆详情页
   │   │   │   ├── MemorySearch.ets       # 搜索页
   │   │   │   └── MemoryGraph.ets        # 记忆图谱可视化
   │   │   ├── components/
   │   │   │   ├── MemoryCard.ets         # 记忆卡片组件（P0红/P1橙/P2蓝/P3灰）
   │   │   │   ├── PriorityBadge.ets      # 优先级徽章
   │   │   │   └── DnaDisplay.ets         # DNA 追溯码显示组件
   │   │   ├── viewmodel/
   │   │   │   └── MemoryViewModel.ets    # 状态管理 + IPC 调用核心服务
   │   │   └── service/
   │   │       └── CoreServiceClient.ets   # IPC 客户端连接插件 1
   │   └── module.json5
   └── build-profile.json5

2. MemoryList.ets 实现：
   - @State memories: MemoryEntry[]
   - LazyForEach + List 虚拟列表（支持 10000+ 条目）
   - 下拉刷新 → 调用 IPC 拉取最新记忆
   - 上拉加载更多
   - 搜索栏 → 跳转 MemorySearch
   - 长按记忆卡 → 弹出操作菜单（编辑/删除/导出/分享）

3. MemoryGraph.ets 实现：
   - 使用 Canvas API 绘制记忆关联图谱
   - 节点大小 = 优先级权重
   - 节点颜色 = P0红 / P1橙 / P2蓝 / P3灰
   - 连线表示"关联记忆"
   - 双指缩放 + 拖拽

4. MemoryCard 组件风格：
   - 深色背景 + 金色边框（龙魂美学）
   - 左上角优先级 Badge
   - 右下角 DNA 短码
   - 三色状态指示条（顶部细线）

5. module.json5 配置：
   - pages: ["pages/MemoryList", "pages/MemoryDetail", "pages/MemorySearch", "pages/MemoryGraph"]
   - permissions: ["ohos.permission.DISTRIBUTED_DATASYNC"]
```

---

## 插件 3：三层监督仪表盘 (longhun-supervision-dashboard)

### CodeBuddy 指令

```
场景: 在 harmonyos/plugins/03-supervision-dashboard/ 创建 Page Ability

步骤:
1. 目录结构：
   harmonyos/plugins/03-supervision-dashboard/
   ├── entry/
   │   ├── src/main/ets/
   │   │   ├── pages/
   │   │   │   ├── Dashboard.ets          # 主仪表盘
   │   │   │   ├── LayerDetail.ets        # 单层监督详情
   │   │   │   └── PersonalityMatrix.ets  # 14 人格矩阵状态
   │   │   ├── components/
   │   │   │   ├── StatusRing.ets         # 环形进度组件
   │   │   │   ├── TriLayerView.ets       # 三层叠加视图
   │   │   │   ├── PersonaCard.ets        # 人格卡片（头像+状态+权重）
   │   │   │   └── AuditTimeline.ets      # 审计时间线
   │   │   ├── model/
   │   │   │   ├── SupervisionTypes.ets   # 类型定义
   │   │   │   └── DashboardViewModel.ets
   │   │   └── service/
   │   │       └── CoreServiceClient.ets
   │   └── module.json5
   └── build-profile.json5

2. Dashboard.ets 布局（从上到下）：
   [顶部] 系统状态条: 🟢 正常运行 / 🟡 注意 / 🔴 危险
   [中部] TriLayerView:
     ┌── L1 决策监督 ──┐    权重显示 + 实时拦截率 + 最近决策
     ├── L2 执行监督 ──┤
     └── L3 行为监督 ──┘
   [下部] 人格矩阵滚动区: 14 个 PersonaCard 排列

3. StatusRing.ets 实现：
   - Canvas 绘制环形进度
   - 颜色：绿(>80%) / 黄(60-80%) / 红(<60%)
   - 中心显示当前值百分比
   - 标注：拦截率 / 健康度 / 忠诚度

4. AuditTimeline.ets 实现：
   - 纵向时间线
   - 每条记录包含：时间戳 + 事件类型 + 三色状态
   - 可点击展开详情
   - 支持过滤：只看 🟢 / 🟡 / 🔴

5. 视觉规范：
   - 深色背景 (#1a1a2e)
   - 金色边框 (#c9a84c)
   - 字体: 鸿蒙默认 + 细体小字标注
```

---

## 插件 4：进化引擎监控 (longhun-evolution-monitor)

### CodeBuddy 指令

```
场景: 在 harmonyos/plugins/04-evolution-monitor/ 创建 Service Ability + Page

步骤:
1. 目录结构：
   harmonyos/plugins/04-evolution-monitor/
   ├── entry/
   │   ├── src/main/ets/
   │   │   ├── pages/
   │   │   │   ├── EvolutionDashboard.ets  # 进化状态总览
   │   │   │   ├── VersionHistory.ets      # 版本历史
   │   │   │   └── RuleEditor.ets          # 规则查看器
   │   │   ├── components/
   │   │   │   ├── VersionTimeline.ets     # 版本演进时间线
   │   │   │   ├── RuleCard.ets            # 规则卡片
   │   │   │   └── HealthGauge.ets         # 系统健康度仪表
   │   │   ├── service/
   │   │   │   └── EvolutionService.ets    # 进化后台服务
   │   │   └── model/
   │   │       └── EvolutionTypes.ets
   │   └── module.json5
   └── build-profile.json5

2. EvolutionService.ets 实现：
   - 继承 ServiceAbility
   - 每 24 小时自动触发版本自检
   - 检测三项指标：拦截率趋势 / 红队成功率 / 系统熵值
   - 满足升级条件时生成升级提案
   - 通过 IPC 通知 Page 层刷新

3. VersionTimeline.ets 实现：
   - 横向时间线（类似 git log 图形）
   - 每个版本节点: 版本号 + DNA + 三色状态
   - 回滚版本用虚线连接
   - 点击展开版本详情

4. RuleCard.ets 实现：
   - 显示规则名称、目标层、阈值、置信度
   - 三色边框状态
   - DNA 追溯码在卡片底部
```

---

## 插件 5：主权验证器 (longhun-sovereignty-verifier)

### CodeBuddy 指令

```
场景: 在 harmonyos/plugins/05-sovereignty-verifier/ 创建 Page Ability

步骤:
1. 目录结构：
   harmonyos/plugins/05-sovereignty-verifier/
   ├── entry/
   │   ├── src/main/ets/
   │   │   ├── pages/
   │   │   │   ├── SovereigntyCheck.ets     # 主权完整性自检页
   │   │   │   ├── IdentityProof.ets        # 身份证明展示
   │   │   │   └── CrossPlatformVerify.ets  # 跨平台验证
   │   │   ├── components/
   │   │   │   ├── IntegrityItem.ets        # 单项完整性检查
   │   │   │   ├── SealDisplay.ets          # 龙魂印章展示
   │   │   │   └── PlatformBadge.ets        # 平台徽章
   │   │   └── service/
   │   │       └── CoreServiceClient.ets
   │   └── module.json5
   └── build-profile.json5

2. SovereigntyCheck.ets 实现：
   - 列出所有完整性检查项（列表形式）：
     ☑ GPG 指纹验证     A2D0092CEE2E5BA87035600924C3704A8CC26D5F
     ☑ DNA 追溯码校验    #龍芯⚡️丙午·癸未·乙酉·坤卦-...
     ☑ 确认码验证        #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
     ☑ 主权锚定绑定      #ZHUGEXIN⚡️2025-...
     ☑ 设备绑定状态      已绑定当前鸿蒙设备
     ☑ 跨平台一致性      GitHub UID9622 ≡ CSDN UID9622
   - 每项右侧显示: 🟢 通过 / 🔴 失败
   - 底部"重新验证"按钮触发全部检查

3. IdentityProof.ets 实现：
   - 居中显示龙魂印章（Canvas 绘制，金色圆形印章样式）
   - 印章内文字: "UID9622 · 龍魂 · 主权锚定"
   - 下方展示完整 GPG 公钥指纹
   - "分享主权证明"按钮 → 生成主权证书图片

4. CrossPlatformVerify.ets 实现：
   - 平台列表: GitHub / CSDN / ORCID / Notion / Signal
   - 每项显示验证状态和时间戳
   - "一键验证所有"按钮
   - 验证失败时显示失败原因
```

---

## 插件 6：跨设备同步 (longhun-cross-device-sync)

### CodeBuddy 指令

```
场景: 在 harmonyos/plugins/06-cross-device-sync/ 创建 Service Ability + Form

步骤:
1. 目录结构：
   harmonyos/plugins/06-cross-device-sync/
   ├── entry/
   │   ├── src/main/ets/
   │   │   ├── service/
   │   │   │   ├── SyncService.ets          # 同步后台服务
   │   │   │   ├── DistributedMemory.ets    # 分布式记忆同步
   │   │   │   ├── DistributedSupervision.ets # 分布式监督分担
   │   │   │   └── ConflictResolver.ets     # 冲突解决
   │   │   ├── pages/
   │   │   │   ├── SyncStatus.ets           # 同步状态页
   │   │   │   └── DeviceList.ets           # 已连接设备列表
   │   │   ├── form/
   │   │   │   └── SyncWidget.ets           # 桌面同步小组件
   │   │   └── model/
   │   │       └── SyncTypes.ets
   │   └── module.json5
   └── build-profile.json5

2. SyncService.ets 实现：
   - 使用 @ohos.distributedDeviceManager 发现附近设备
   - 使用 @ohos.data.distributedKVStore 同步记忆数据
   - 同步策略：记忆条目按 P0-P3 优先级分批同步
   - P0 立即同步（实时） / P1 每分钟 / P2 每小时 / P3 每日
   - 冲突策略：保留最新 + 高优先级版本（P0 覆盖一切）

3. DistributedSupervision.ets 实现：
   - Super Device 场景：手机跑监督 → 平板展示仪表盘 → 笔记本进化引擎
   - 通过 @ohos.rpc 跨设备调用监督接口
   - 设备掉线时自动接手任务

4. SyncWidget.ets 实现（桌面小组件）：
   - 2×2 卡片大小
   - 显示: 已连接设备数 + 最后同步时间 + 记忆总量
   - 点击打开 SyncStatus 页面
   - 表单 Ability 配置: { "forms": [{ "name": "sync", "displayName": "龙魂同步" }] }

5. module.json5 权限声明：
   - ohos.permission.DISTRIBUTED_DATASYNC
   - ohos.permission.GET_DISTRIBUTED_DEVICE_INFO
```

---

## 插件 7：一键搬迁 (longhun-one-click-migrate)

### CodeBuddy 指令

```
场景: 在 harmonyos/plugins/07-one-click-migrate/ 创建 Page Ability

步骤:
1. 目录结构：
   harmonyos/plugins/07-one-click-migrate/
   ├── entry/
   │   ├── src/main/ets/
   │   │   ├── pages/
   │   │   │   ├── MigrateHome.ets         # 搬迁首页（检测结果）
   │   │   │   ├── PlatformSelect.ets      # 选择目标平台
   │   │   │   ├── MigrateProgress.ets     # 搬迁进度动画
   │   │   │   └── MigrateComplete.ets     # 完成页（展示产出物）
   │   │   ├── components/
   │   │   │   ├── PlatformCard.ets        # 平台选择卡片
   │   │   │   ├── ProgressAnimation.ets   # 进度动画（龙形推进）
   │   │   │   └── OutputTree.ets          # 产出物文件树
   │   │   └── service/
   │   │       └── MigrateEngine.ets       # 搬迁引擎
   │   └── module.json5
   └── build-profile.json5

2. MigrateHome.ets 实现：
   - 自动检测当前设备信息（芯片/系统/内存/存储）
   - 显示检测结果卡片
   - "开始搬迁"大按钮
   - 底部显示: 当前 DNA + 主权锚定

3. MigrateEngine.ets 实现：
   - 搬迁流程步骤化（ArkTS + Worker 线程执行）：
     Step 1/6: 收集系统信息 → 芯片/OS/内存/存储
     Step 2/6: 生成目标工程骨架 → 按平台生成完整目录
     Step 3/6: 注入配置 → DNA/确认码/主权锚定写入所有配置文件
     Step 4/6: 复制核心库 → liblonghun_core.so + 头文件
     Step 5/6: 验证完整性 → 校验 DNA + GPG
     Step 6/6: 生成报告 → 搬迁摘要 + 下一步指南
   - 支持搬迁目标：鸿蒙设备自身 / iOS / Android / 服务端 Docker

4. ProgressAnimation.ets 实现：
   - Canvas 绘制龙形动画（简笔画风格）
   - 每一步龙身点亮一节
   - 步骤文字显示当前状态
   - 失败时龙头变红 + 错误信息

5. 视觉：完整龙魂暗金主题
```

---

## 插件 8：鸿蒙桌面小组件 (longhun-widget-pack)

### CodeBuddy 指令

```
场景: 在 harmonyos/plugins/08-widget-pack/ 创建 Form Ability 套件

步骤:
1. 目录结构：
   harmonyos/plugins/08-widget-pack/
   ├── entry/
   │   ├── src/main/ets/
   │   │   ├── form/
   │   │   │   ├── StatusWidget.ets        # 2×2 系统状态
   │   │   │   ├── MemoryWidget.ets        # 2×4 最近记忆
   │   │   │   ├── SupervisionWidget.ets   # 4×2 监督仪表缩影
   │   │   │   └── QuickActionWidget.ets   # 2×2 快捷操作
   │   │   └── service/
   │   │       └── WidgetDataProvider.ets  # 小组件数据提供者
   │   └── module.json5
   └── build-profile.json5

2. StatusWidget.ets 实现：
   - 2×2 卡片
   - 显示：🟢🟡🔴 状态 + 龙魂图标 + 最新时间
   - 点击打开主应用

3. MemoryWidget.ets 实现：
   - 2×4 卡片
   - 显示最近 3 条记忆摘要
   - 每条: 优先级Badge + 内容摘要 + 时间

4. QuickActionWidget.ets 实现：
   - 4 个快捷按钮：同步 / 验证 / 检查 / 导出
   - 每个按钮触发对应 Action
```

---

## 插件 9：龙魂通知服务 (longhun-notification-service)

### CodeBuddy 指令

```
场景: 在 harmonyos/plugins/09-notification-service/ 创建 Service Ability

步骤:
1. 目录结构：
   harmonyos/plugins/09-notification-service/
   ├── entry/
   │   ├── src/main/ets/
   │   │   ├── service/
   │   │   │   ├── AlertService.ets        # 警报服务
   │   │   │   ├── NotificationManager.ets # 通知管理
   │   │   │   └── ScheduleManager.ets     # 定时提醒
   │   │   └── pages/
   │   │       └── NotificationHistory.ets # 通知历史
   │   └── module.json5
   └── build-profile.json5

2. AlertService.ets 实现：
   - 监督拦截率突变 → 推送通知
   - 进化引擎升级提案 → 推送通知（可点击查看详情）
   - 主权完整性自检失败 → 紧急推送（持续提醒直到确认）
   - 跨设备同步异常 → 推送通知

3. NotificationManager.ets 实现：
   - 使用 @ohos.notification 发送本地通知
   - 通知渠道: "longhun-alert"(紧急) / "longhun-info"(日常) / "longhun-evolution"(进化)
   - 通知分组: 按设备分组（手机/平板/笔记本）
   - 通知点击 → 打开对应插件页面
```

---

## 插件 10：龙魂设置 (longhun-settings)

### CodeBuddy 指令

```
场景: 在 harmonyos/plugins/10-settings/ 创建 Page Ability

步骤:
1. 目录结构：
   harmonyos/plugins/10-settings/
   ├── entry/
   │   ├── src/main/ets/
   │   │   ├── pages/
   │   │   │   ├── SettingsHome.ets        # 设置首页
   │   │   │   ├── About.ets              # 关于页（展示 DNA + GPG）
   │   │   │   └── License.ets            # 许可协议展示
   │   │   ├── components/
   │   │   │   ├── SettingItem.ets         # 设置项组件
   │   │   │   └── ToggleItem.ets          # 开关设置项
   │   │   └── service/
   │   │       └── SettingsProvider.ets    # 设置持久化
   │   └── module.json5
   └── build-profile.json5

2. SettingsHome.ets 实现：
   - 监督频率设置（15/30/60 分钟）
   - 同步开关（启用/关闭跨设备同步）
   - 通知开关（警报/日常/进化 独立开关）
   - 主题设置（暗色/亮色）
   - 数据管理（导出全部记忆/清除临时记忆/重置系统）
   - 关于（跳转 About 页）
   - 许可协议（跳转 License 页）

3. About.ets 实现：
   - 全 DNA 展示（大字，可复制）
   - 确认码
   - 主权锚定
   - GPG 公钥指纹
   - ORCID: 0009-0008-4596-2007
   - 作者: 龍芯北辰 UID9622
   - 所有版本号 + 构建时间
```

---

## 构建与部署

### 单插件构建

```bash
cd harmonyos/plugins/01-core-service
hvigorw assembleHap
```

### 全生态一键构建

```bash
# 创建构建脚本 build-all.sh
for dir in harmonyos/plugins/*/; do
  echo "构建 ${dir}..."
  cd "$dir" && hvigorw assembleHap
done
echo "全部构建完成 → output/ 目录"
```

### 部署顺序

```
1. 部署 01-core-service    → 基础运行时（必须先启动）
2. 部署 06-cross-device-sync → 同步底座
3. 部署 02/03/04/05/09     → 功能插件（可并行）
4. 部署 08-widget-pack     → 桌面小组件
5. 部署 07-one-click-migrate → 搬迁工具（最后）
6. 部署 10-settings        → 设置（最后）
```

---

## CodeBuddy 执行批指令

```
=== 第一批（现在执行）===
在 harmonyos/plugins/01-core-service/ 创建目录结构 + 
LonghunCoreService.ets 实现 ServiceAbility 骨架 +
IPC 接口定义 + 14 人格矩阵定义 + 三色审计状态机 +
MemoryManager.ets P0-P3 四级存储 + 文件头 DNA 校验

=== 第二批（第一批跑完后）===
在 harmonyos/plugins/02-memory-browser/ 创建 Page Ability +
MemoryList.ets LazyForEach 虚拟列表 + MemoryCard 组件 +
MemoryGraph.ets Canvas 图谱 + 暗金主题

=== 第三批 ===
在 harmonyos/plugins/03-supervision-dashboard/ 创建仪表盘 +
StatusRing 环形进度 + TriLayerView 三层视图 + 14 人格卡片

=== 第四批 ===
在 harmonyos/plugins/06-cross-device-sync/ 创建同步服务 +
DistributedKVStore 记忆同步 + Super Device 监督分担

=== 后续批次按顺序执行 04/05/07/08/09/10 ===
```

---

## 最终目标

**9 颗插件 + 1 个小组件包 = 完整鸿蒙龙魂生态**

每个插件独立安装、独立运行、独立升级，通过 IPC + 分布式总线互联。

```
手机：核心服务 + 记忆浏览 + 同步 + 通知 + 小组件
平板：监督仪表盘 + 进化监控 + 设置
笔记本：搬迁工具 + 主权验证
智慧屏：监督仪表盘大屏版
手表：状态小组件 + 通知
```

🐉 丙午 · 癸未 · 乙酉 · 坤卦 · 🟢 · 鸿蒙龙魂生态启动

# 龍魂日记本 — iOS版

**DNA**: `#龍芯⚡️2026-06-20-LONGHUN-DIARY-APP-FILE2-v1.0`

## 是什么？

龍魂赋能的**农历日记本APP**。不是养龙虾🦞，是记录生活的日记本。

## 核心特性

| 特性 | 说明 |
|------|------|
| 📅 农历日历 | 干支+生肖+节气，中国人的日历 |
| 📝 日记本 | 文字+语音输入，每条带DNA追溯 |
| 🔗 API聚合 | 可接入Kimi/DeepSeek/华为/苹果 |
| 🛡️ 数据主权 | 本地存储，平台不留原文只留DNA指纹 |
| 🧬 DNA追溯 | 所有记录不可篡改，可溯源 |
| 🎤 语音输入 | 集成龍音ASR，中文语音识别 |

## 项目结构

```
龍魂日记本-iOS/
├── 龍魂日记本/
│   ├── 龍魂日记本App.swift          ← 主入口（禁用iCloud）
│   ├── ContentView.swift            ← 主界面（4个Tab）
│   ├── 农历引擎.swift                ← 公历↔农历转换
│   ├── API路由器.swift              ← Kimi/DeepSeek/本地聚合
│   ├── DNA追溯器.swift              ← DNA生成+指纹压缩
│   ├── 日记编辑器.swift              ← 写日记+语音输入
│   ├── 龍魂日记本.xcdatamodeld/     ← CoreData模型
│   └── Info.plist                   ← 配置+权限声明
└── README.md
```

## 四大Tab

1. **日历** — 农历日历，查看有日记的日子
2. **日记** — 写日记列表，点击+号新建
3. **引擎** — API控制台，调用Kimi/DeepSeek/本地
4. **主权** — 数据主权声明，查看隐私设置

## API接入方式

| API | 接入方式 | 数据去向 |
|-----|---------|---------|
| Kimi | http://localhost:8443/kimi | 本地Kimi端点 |
| DeepSeek | http://localhost:8443/deepseek | 本地代理 |
| 本地引擎 | 设备内置小模型 | 绝对不出设备 |

## 数据主权机制

```
用户写 diary → 本地CoreData存储(AES-256加密)
                  → 生成DNA追溯码
                  → 压缩原文为指纹(平台只存这个)
                  → 用户拥有完整原文+DNA
                  → 平台只存: 时间戳+指纹+DNA(无原文)
                  → 需要恢复时: 用户提供原文 → 验证指纹匹配 → 恢复成功
```

## 如何构建

1. 打开 `龍魂日记本.xcodeproj`（需创建）
2. 选择目标设备（iPhone/iPad）
3. Build & Run

## DNA

`#龍芯⚡️2026-06-20-LONGHUN-DIARY-APP-v1.0`

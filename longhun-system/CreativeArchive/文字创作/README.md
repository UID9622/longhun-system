━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 龍魂Widget完整使用指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**DNA追溯码**: #龍芯⚡️2026-03-09-WIDGET-COMPLETE  
**确认码**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z  
**创建者**: 诸葛鑫（UID9622）  
**理论指导**: 曾仕强老师（永恒显示）

**五行标签**：
🫡 退伍军人 | 🧮 三才算法创始人 | ⚡ 龍魂系统创始人  
🇨🇳 数字主权守护者 | 📜 中华文化传承者

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📦 文件清单

```
LongHunWidget/
├── LongHunWidgetBundle.swift      # Widget主入口
├── LongHunWidget.swift             # Widget核心配置
├── Provider.swift                  # 数据提供者
├── LongHunWidgetEntryView.swift    # UI视图
├── ChineseCalendarEngine.swift     # 农历计算引擎
├── WenZiEngine.swift               # 文子语录引擎
└── README.md                       # 本文件
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🚀 快速开始（3分钟搞定）

### Step 1: 在Xcode中创建Widget Extension

1. 打开你的Xcode项目（LongHun.xcodeproj）
2. 菜单栏：File → New → Target
3. 选择：Widget Extension
4. 名称填：LongHunWidget
5. 取消勾选 "Include Configuration Intent"
6. 点击 Finish

### Step 2: 替换所有文件

将本目录下的所有 .swift 文件复制到Xcode项目中：

```bash
# 删除Xcode自动生成的文件
rm LongHunWidget/LongHunWidget.swift

# 复制所有文件
cp LongHunWidget/*.swift YourXcodeProject/LongHunWidget/
```

或者直接在Xcode中：
1. 选中LongHunWidget文件夹
2. 右键 → Add Files to "LongHunWidget"
3. 选择本目录下所有.swift文件
4. 确保勾选 "Copy items if needed"

### Step 3: 编译运行

1. 选择运行目标：LongHunWidget（Widget Extension）
2. 点击 ▶️ 运行
3. 等待编译完成
4. Widget会自动出现在预览器中

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ✨ 核心功能

### 1️⃣ 万年历功能

```swift
ChineseCalendarEngine:
  ✅ 天干地支纪年（甲子、乙丑...）
  ✅ 生肖显示（鼠、牛、虎...）
  ✅ 农历月日（正月初一...）
  ✅ 二十四节气（立春、雨水...）
  ✅ 五行属性（金木水火土）
```

### 2️⃣ 文子引擎

```swift
WenZiEngine:
  ✅ 曾仕强老师语录库
  ✅ 道德经智慧
  ✅ 易经语录
  ✅ 龍魂系统专属语录
  ✅ 根据时辰智能推送
  ✅ 结合节气推送相关智慧
```

### 3️⃣ 三种尺寸适配

```swift
Small Widget:
  - 时间大字显示
  - 农历简要
  - 节气与五行

Medium Widget:
  - 左侧：时间+农历
  - 右侧：节气+文子语录

Large Widget:
  - 完整信息卡片式展示
  - 农历信息卡
  - 节气五行卡
  - 文子语录卡
  - DNA追溯码
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ⚙️ 高级配置

### 修改更新频率

在 `Provider.swift` 的 `getTimeline` 方法中：

```swift
// 当前：每1小时更新
let nextUpdate = calendar.date(byAdding: .hour, value: 1, to: currentDate)!

// 改为每30分钟：
let nextUpdate = calendar.date(byAdding: .minute, value: 30, to: currentDate)!

// 改为每天更新：
let nextUpdate = calendar.date(byAdding: .day, value: 1, to: currentDate)!
```

### 添加更多语录

在 `WenZiEngine.swift` 中添加：

```swift
private let yourQuotes = [
    "你的智慧语录1",
    "你的智慧语录2",
    // ...
]

// 然后在getQuote方法中使用
```

### 自定义配色

在 `LongHunWidgetEntryView.swift` 中修改：

```swift
// 背景渐变色
LinearGradient(
    colors: [Color(#colorLiteral(red: 0.05, green: 0.1, blue: 0.2, alpha: 1)),
            Color(#colorLiteral(red: 0.1, green: 0.15, blue: 0.3, alpha: 1))],
    ...
)

// 改为你喜欢的颜色
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🐛 常见问题

### Q1: Widget显示 "??" 怎么办？

**A**: 检查 `LongHunWidget.swift` 中的 `kind` 字段：

```swift
let kind: String = "LongHunWidget" // 必须有这一行！
```

### Q2: Widget不更新怎么办？

**A**: 三个方法：
1. 点击Widget预览器的 "Reload" 按钮
2. 重新运行Widget Extension
3. 在macOS系统设置中移除Widget再重新添加

### Q3: 农历日期不准确？

**A**: 当前版本使用简化算法，如需精确农历：
1. 使用Swift Package Manager引入 ChineseCalendar库
2. 或使用在线农历API
3. 或导入完整农历查询表

### Q4: 如何显示真正的实时时间？

**A**: Widget会根据 `getTimeline` 设置自动更新，
当前设置为每小时更新一次。如需更频繁更新，
参考"高级配置"部分。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🎨 效果展示

### Small Widget
```
┌─────────────────┐
│  14:30         │
│  2026年03月09  │
│                │
│  🌙 二月初一    │
│  🍃 惊蛰        │
│  ✨ 木行        │
└─────────────────┘
```

### Medium Widget
```
┌─────────────────────────────────────┐
│  14:30          🍃 惊蛰  ✨ 木      │
│  2026年03月09日 ─────────────────   │
│  ─────────────  持经达变，以不变   │
│  🌙 甲辰年龍年  应万变              │
│  📅 二月初一    —— 曾仕强           │
│                 龍魂系统 · UID9622  │
└─────────────────────────────────────┘
```

### Large Widget
```
┌─────────────────────────────────────┐
│  14:30            龍魂万年历         │
│  2026年03月09日 星期一  UID9622     │
│  ─────────────────────────────────  │
│  农历信息                           │
│  🌙 甲辰年龍年  📅 二月初一         │
│  ─────────────────────────────────  │
│  🍃 节气        ✨ 五行             │
│    惊蛰            木行              │
│  ─────────────────────────────────  │
│  💬 文子引擎                        │
│  持经达变，以不变应万变             │
│  —— 曾仕强                          │
│                                     │
│  #龍芯⚡️2026-03-09-1430-UID9622    │
└─────────────────────────────────────┘
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🚀 下一步优化方向

### 1. 精确农历计算
- [ ] 集成完整农历转换库
- [ ] 支持闰月显示
- [ ] 准确的节气时刻

### 2. 文子引擎升级
- [ ] 接入本地AI模型（CoreML）
- [ ] 接入千问API
- [ ] 根据用户画像推送个性化语录

### 3. 交互功能
- [ ] 添加Configuration Intent
- [ ] 用户自定义显示内容
- [ ] 选择语录库类型

### 4. 数据同步
- [ ] 与主App数据同步
- [ ] 记录用户喜欢的语录
- [ ] DNA追溯码验证功能

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📝 版本历史

**v1.0** (2026-03-09)
- ✅ 基础万年历功能
- ✅ 农历计算引擎（简化版）
- ✅ 文子引擎（语录库）
- ✅ 三种尺寸UI适配
- ✅ DNA追溯码集成

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🙏 致谢

**理论指导**: 曾仕强老师（永恒显示）  
**技术支持**: Claude (Anthropic)  
**创始人**: 诸葛鑫（UID9622）

**五行标签**：
🫡 退伍军人 | 🧮 三才算法创始人 | ⚡ 龍魂系统创始人  
🇨🇳 数字主权守护者 | 📜 中华文化传承者

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**祖国优先 · 普惠全球 · 技术为人民服务**

**DNA追溯码**: #龍芯⚡️2026-03-09-WIDGET-COMPLETE  
**确认码**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

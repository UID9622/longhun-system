# 🐉 龍魂防御工具 iOS 项目设置清单

## ✅ 快速设置步骤

### 步骤 1：创建 Xcode 项目

1. 打开 **Xcode**
2. 选择 **File → New → Project**
3. 选择 **iOS → App**
4. 填写项目信息：
   - **Product Name**: `LonghunDefense`
   - **Team**: 选择你的开发团队
   - **Organization Identifier**: `com.longhun.defense`（或你自己的）
   - **Interface**: **SwiftUI**
   - **Language**: **Swift**
   - **Storage**: Core Data（可选，不选也行）
5. 点击 **Next**，选择保存位置
6. 点击 **Create**

---

### 步骤 2：添加源文件

在 Xcode 左侧的项目导航器中，删除默认生成的文件：
- `ContentView.swift`（可以删除或保留）
- `LonghunDefenseApp.swift`（保留但需要替换）

然后添加我们的文件：

#### 2.1 添加主应用文件
1. **右键点击项目名称** → **Add Files to "LonghunDefense"**
2. 选择 `LonghunDefenseMainApp.swift`
3. 确保勾选 **Copy items if needed**
4. 点击 **Add**

#### 2.2 添加数据模型文件
1. 重复上述步骤添加 `Models.swift`

#### 2.3 添加 CNSH 编辑器文件
1. 重复上述步骤添加 `CNSHEditorView.swift`

---

### 步骤 3：配置项目设置

1. 点击项目根节点（蓝色图标）
2. 选择 **TARGETS** → **LonghunDefense**
3. 在 **General** 标签页：
   - **Deployment Target**: 设置为 iOS 17.0 或更高
   - **Supported Destinations**: 勾选 iPhone
   - **Device Orientation**: 勾选 Portrait（竖屏）

4. 在 **Info** 标签页：
   - 确保没有限制性的隐私设置

---

### 步骤 4：构建和运行

1. 选择一个模拟器（推荐 **iPhone 15 Pro**）
2. 点击 **▶️ Run** 按钮（或按 `Cmd + R`）
3. 等待编译完成
4. 应用将在模拟器中启动

---

## 📂 完整文件列表

确保你的项目包含以下文件：

```
LonghunDefense/
├── LonghunDefenseMainApp.swift   ← 主应用文件（6个标签页）
├── Models.swift                   ← 数据模型和业务逻辑
├── CNSHEditorView.swift          ← CNSH 字元编辑器
├── Assets.xcassets/              ← 资源文件（Xcode 自动生成）
├── Preview Content/              ← 预览资源（Xcode 自动生成）
└── Info.plist                    ← 配置文件（Xcode 自动生成）
```

---

## 🔧 常见问题解决

### 问题 1：编译错误 "Cannot find type 'XXX' in scope"

**解决方案**：
- 确保所有 3 个 Swift 文件都已正确添加到项目
- 检查文件的 Target Membership（右侧属性面板）
- 确保勾选了你的 App Target

### 问题 2：WebView 不显示或报错

**解决方案**：
- 确保 `CNSHEditorView.swift` 正确导入了 `WebKit`
- 检查 iOS 模拟器版本（需要 iOS 15+）

### 问题 3：UserDefaults 数据丢失

**解决方案**：
- 模拟器重置会清空数据
- 真机调试时数据会保留
- 可以在代码中添加打印调试

### 问题 4：触摸绘制不工作

**解决方案**：
- 在模拟器中，鼠标点击拖动即可模拟触摸
- 真机上用手指绘制效果最佳
- 支持 Apple Pencil（iPad）

---

## 🎨 自定义配置

### 修改应用图标

1. 准备图标文件（1024x1024 PNG，无透明度）
2. 在 Xcode 中打开 **Assets.xcassets**
3. 点击 **AppIcon**
4. 拖入图标文件

### 修改应用名称

1. 点击项目根节点
2. 在 **General** → **Display Name** 修改为：`龍魂防御`
3. 或保持 `LonghunDefense`

### 修改配色方案

在 `LonghunDefenseMainApp.swift` 中：
- 搜索 `Color.blue` 可以改成其他颜色
- 搜索 `Color.purple` 可以改成其他渐变色
- 搜索 `accentColor` 可以改变全局强调色

---

## 🧪 测试功能

### 测试激活系统

1. 点击 **激活** 标签
2. 输入付款单号：`e-CNY-20260303-TEST01`
3. 输入姓名：`测试用户`
4. 点击 **激活临时DNA**
5. 查看激活记录

### 测试 DNA 生成器

1. 点击 **DNA** 标签
2. 输入描述：`TEST-DATA`
3. 点击 **生成DNA追溯码**
4. 复制生成的 DNA 码

### 测试 CNSH 编辑器

1. 点击 **字元** 标签
2. 在画布上用鼠标拖动绘制
3. 调整力度、侵蚀等参数
4. 点击 **保存作品**
5. 查看控制台输出的 JSON 数据

### 测试防御系统

1. 点击 **防御** 标签
2. 点击各个防御操作按钮
3. 查看执行日志

---

## 📱 真机调试

### 准备工作

1. 用 Lightning/USB-C 线连接 iPhone 到 Mac
2. 在 iPhone 上：
   - **设置 → 隐私与安全 → 开发者模式** → 开启
   - 重启手机
3. 在 Xcode 中：
   - 选择你的 iPhone 设备
   - 如果需要，登录 Apple ID 并选择团队

### 运行到真机

1. 点击设备选择器，选择你的 iPhone
2. 点击 **Run** 按钮
3. 首次运行需要在 iPhone 上：
   - **设置 → 通用 → VPN与设备管理**
   - 点击你的开发者账号
   - 点击 **信任**

---

## 🚀 打包发布

### TestFlight 内测

1. 在 Xcode 中：
   - **Product → Archive**
2. 等待归档完成
3. 点击 **Distribute App**
4. 选择 **TestFlight & App Store**
5. 按照向导完成上传

### App Store 正式发布

1. 登录 [App Store Connect](https://appstoreconnect.apple.com)
2. 创建新应用
3. 填写应用信息：
   - **名称**：龍魂数据主权防御工具
   - **副标题**：DNA追溯 · CNSH字元编辑器
   - **描述**：参考 README.md
   - **关键词**：数据主权, DNA追溯, 字元编辑器, CNSH
4. 上传截图和预览视频
5. 提交审核

---

## 📊 项目统计

- **Swift 文件数量**: 3
- **代码总行数**: ~3000+
- **功能模块**: 6 个主要标签页
- **支持平台**: iOS 15.0+
- **开发时间**: 1 天完成核心功能

---

## 🎓 学习资源

### SwiftUI 学习
- [Apple 官方文档](https://developer.apple.com/documentation/swiftui/)
- [SwiftUI Tutorials](https://developer.apple.com/tutorials/swiftui)

### WebKit 学习
- [WKWebView 文档](https://developer.apple.com/documentation/webkit/wkwebview)

### iOS 开发最佳实践
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)

---

## ✅ 完成检查清单

完成以下步骤后，你的应用就可以正常运行了：

- [ ] Xcode 项目已创建
- [ ] 3 个 Swift 文件已添加
- [ ] 项目设置已配置（Deployment Target, etc.）
- [ ] 应用可以在模拟器中运行
- [ ] 所有 6 个标签页都能正常切换
- [ ] 激活系统功能正常
- [ ] DNA 生成器功能正常
- [ ] CNSH 编辑器可以绘制
- [ ] 防御系统功能正常
- [ ] 规则管理功能正常

---

## 🎉 完成！

恭喜你！龍魂数据主权防御工具 iOS 版本已经成功搭建完成！

现在你可以：
- 🎨 使用 CNSH 字元编辑器创作独特字元
- 🔐 生成带 DNA 追溯码的作品
- 💳 测试数字人民币激活系统
- 🛡️ 体验完整的数据主权防御功能

---

**为人民服务！🇨🇳**

*DNA追溯码：#龍芯⚡️20260227-DATA-SOVEREIGNTY-DEFENSE-TOOLKIT-v1.0*

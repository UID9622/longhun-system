# 🐉 龍魂9622·浏览器插件 + 本地引擎 v2.0

> 抬头模板: [4] 💬 文档型 · 深度集成版 v2.0 · 2026-09-04
> DNA(v∞): `#龍芯⚡️丙午·丁酉·辛巳-LONGHUN-EXT-README-v2.0-e4a9c1d7`
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> License: MulanPSL v2（工程实现层 · 代码允许商业使用 · 署名）
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 来源: `~/龍魂浏览器插件.zip` (2026-05-21) · 2026-09-04 深度集成入 `longhun-system/extensions/longhun-ext`
> ⚠️ 端口提示: 9622 现由系统 `bin/lh_api.py` 占用 · 自跑引擎需改端口（如 9633）并同步 JS 常量

---

## 📁 文件清单

```
longhun-ext/
├── manifest.json      Chrome/Safari MV3 清单
├── background.js      后台服务·右键菜单·引擎调用
├── content.js         网页内悬浮侧边栏·语音输入
├── popup.html         插件弹窗 UI（工具·对话·MCP·苹果）
├── popup.js           弹窗逻辑
├── install.sh         一键安装脚本（Mac·支持 M 系列芯片）
├── LonghunApp.swift   iOS Swift 伴侣 App（ARKit·本地语音）
└── engine/
    ├── main.py        FastAPI 本地引擎（端口 9622）
    └── notion_sync.py Notion 回写模块
```

---

## 🚀 三步安装（Mac）

```bash
# 第一步：安装引擎
chmod +x install.sh && ./install.sh

# 第二步：填写 API Key
nano ~/longhun-engine/.env

# 第三步：测试引擎
curl http://127.0.0.1:9622/api/health
```

---

## 🌐 Chrome/Edge 安装扩展

1. 打开 `chrome://extensions`
2. 右上角开「开发者模式」
3. 点「加载已解压的扩展程序」→ 选本文件夹
4. 固定到工具栏（📌）
5. 任意网页选中文字 → 右键 → 看到龍魂菜单

---

## 🍎 苹果设备兼容

### Safari（Mac）
```bash
# 用 Xcode 把 Chrome 扩展转为 Safari 扩展
xcrun safari-web-extension-converter ~/longhun-ext/
# 然后在 Xcode 打开并 Build
```

### iPhone/iPad（无需 Xcode）
1. 把 `~/longhun-engine/.env` 里的 `APPLE_MODE=false` 改为 `APPLE_MODE=true`
2. 重启引擎：`launchctl kickstart -k gui/$UID/com.longhun.9622`
3. Mac 终端查看局域网 IP：`ipconfig getifaddr en0`
4. iPhone Safari 打开：`http://[Mac-IP]:9622`

### iOS 原生 App（ARKit + 本地语音）
- 打开 Xcode，新建 iOS App，把 `LonghunApp.swift` 复制进项目
- 修改 `Config.engineHost` 为 Mac 的局域网 IP
- 添加权限：麦克风 + 语音识别 + 相机（ARKit）
- 连接 iPhone，Build and Run

---

## 🎙️ 语音输入

Web Speech API 已内置，**Safari 14.1+ 和 Chrome 均支持**，无需云端，完全本地。
- Chrome/Edge：弹窗或右键 → 语音输入
- Safari（Mac）：同上
- iOS：用 Swift App 的本地语音（`requiresOnDeviceRecognition = true`）

---

## 🔌 MCP 工具扩展

引擎支持通过 `mcp_bridge.py` 接入任意 MCP Server。
默认提供三个占位工具（fs.read / git.status / notion.search），
真实接入方式见 Notion 主控页 §6.5 本地宝宝主权架构。

---

## 📐 CNSH 中文语法对齐

内置规则：翻译偏差检测 + 情绪负载词 + 五行词替换。
在 `engine/main.py` 的 `CNSH_RULES` 列表中添加自定义规则。

---

**技术为人民服务 · 数据主权归于人民 🇨🇳**
**——💎 龍芯北辰｜UID9622**

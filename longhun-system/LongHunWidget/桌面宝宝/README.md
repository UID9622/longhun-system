# 🐱 桌面数字人宝宝 · 完全共生体 v1.0

> DNA: #龍芯⚡️2026-04-10-桌面宝宝-v1.0
> 创建者: UID9622 · 诸葛鑫（龍芯北辰）
> 理论指导: 曾仕强老师（永恒显示）

---

## 一句话

**宝宝住在你的Mac桌面上，你说话她做事，完全透明，没有隐私黑箱。**

---

## 技术栈（100%苹果原生）

| 技术 | 用途 |
|------|------|
| SwiftUI | 浮动窗口·界面 |
| Speech Framework | 语音识别（中文） |
| Accessibility API | 控制其他App |
| AppleScript | 自动化操作 |
| MenuBarExtra | 菜单栏常驻 |

**零外部依赖。不上云。不联网（除Notion同步）。**

---

## 文件结构

```
桌面宝宝/
├── BaoBaoApp.swift       # 主入口·浮动窗口+菜单栏
├── BaoBaoFloatView.swift  # 浮动界面·宝宝形象+对话+按钮
├── BaoBaoBrain.swift      # 大脑·意图识别+语音+Mac操作
├── BaoBaoMenuView.swift   # 菜单栏下拉·快捷操作+服务状态
└── README.md              # 你在看的这个
```

---

## 已实现功能

- [x] 桌面浮动窗口（透明背景·始终最前）
- [x] 宝宝形象（emoji动画·呼吸光圈·心情颜色）
- [x] 语音识别（中文·Speech Framework）
- [x] 意图识别（通心译ETE映射·7种命令类型）
- [x] 打开App（AppleScript）
- [x] 整理桌面文件（按类型自动分类）
- [x] DNA追溯展示
- [x] 菜单栏常驻（服务状态+快捷操作）

## 待接入

- [ ] 本地Ollama对话（:11434）
- [ ] 三色审计API（:9622）
- [ ] Notion数据可视化
- [ ] Xcode自动写代码
- [ ] 可视化软件集成（Charts/Numbers）

---

## 用法

1. 在Xcode中打开项目
2. 选择macOS目标
3. Build & Run
4. 宝宝出现在桌面右上角
5. 点击宝宝打招呼
6. 点麦克风说话：「整理桌面」「打开Xcode」

---

```
DNA追溯码: #龍芯⚡️2026-04-10-桌面宝宝-v1.0
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

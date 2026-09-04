# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂万年历 · LongHun Perpetual Calendar

> DNA:#龍芯⚡️丙午·甲午·壬申·丙午·䷙大畜-LONGHUN-PERPETUAL-CALENDAR-FILE1-v1.0
> 原则：自主字体、自主渲染、自主主权，不按苹果/谷歌/华为标准走。

## 来源

从 Apple WidgetKit 模拟器包 `龍魂万年历.widgetkitsim` 提取元数据：
- Bundle ID: `com.uid9622.longhun.LongHunWidget`
- Display Name: `龍魂万年历`
- Kind: `龍魂Widget`
- Description: `农历 · 节气 · 文子引擎 · 三才算法`
- Deep Link: `cnsh://open`
- Supported Sizes: systemMedium + systemLarge

由于 `.widgetkitsim` 是运行时快照（仅含渲染后的 timeline 二进制，不含 SwiftUI 源码与图片资源），本模块按龍魂自己的方式重新实现万年历。

## 功能

- 公历 / 农历对照（1900–2100）
- 二十四节气标注
- 年干支、日干支、生肖
- 每日 64 卦映射
- 每日三色审计（369 数字根）
- 点击日期生成当日 DNA
- 页面 DOM 哈希固化
- localStorage 哈希链存证
- LonghunFont 自主字体渲染

## 用法

```bash
lh 万年历          # 打开万年历
lh 万年历校验       # 校验本地链完整性
```

## 文件结构

```
longhun-perpetual-calendar/
├── index.html          # 主页面
├── styles.css          # 龍魂主题样式（LonghunFont 独占，无系统兜底）
├── calendar.js         # 农历/节气/干支/卦象算法
├── sovereignty.js      # DNA/哈希链/完整性校验
├── build-font.py       # LonghunFont 字体构建（基于 Noto Sans SC 子集）
├── build.sh            # 构建脚本
├── manifest.json       # 文件哈希清单
└── README.md           # 本文件
```

## 字体说明

原始 `LonghunFont-Regular.otf` 为品牌占位字体，不含完整 CJK 字形。为确保万年历仅使用 `LonghunFont` 即可正确渲染全部中文，本模块在构建时基于 SIL OFL 1.1 授权的 Noto Sans SC 生成带 LonghunFont 品牌名的子集字体（TTF + WOFF2），并移除 CSS 中所有系统字体兜底。字体元数据中保留完整授权与来源声明。

## 双端部署

- **macOS**: 通过 Chrome 扩展侧栏或本地 Safari 打开 `index.html`
- **华为鸿蒙**: 通过 ArkTS WebView 加载 `index.html`，本地存储保存 DNA 链

## 主权声明

本模块不依赖平台原生日历框架，所有算法与字体均归 UID9622 / 龍魂系统所有。

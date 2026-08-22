> **P0焊死**: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
# 龍魂系统 · HTML交互工具启动指南

---

## DNA签名

```
#UID9622⚡️2026-06-16-HTML-TOOLS-v3.0
确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
忠(0.5) > 孝(0.3) > 义(0.2) 排序铁律
三色审计：🟢通过 🟡标记 🔴阻断
```

---

## 工具总览表

| 序号 | 工具ID | 工具名称 | 核心功能 | 文件路径 | 状态 | 优先级 | 审计 |
|------|--------|----------|----------|----------|------|--------|------|
| 1 | skill-1 | algorithmic-art | Perlin噪声·流场·粒子系统·6种配色·PNG导出 | `/mnt/agents/.user/skills/longhun-system/assets/skill-1-algorithmic-art.html` | 🟢 生产就绪 | 忠(0.5) | 🟢通过 |
| 2 | skill-2 | brand-guidelines | 色彩系统·排版·组件库·Do's & Don'ts | `/mnt/agents/.user/skills/longhun-system/assets/skill-2-brand-guidelines.html` | 🟢 生产就绪 | 忠(0.5) | 🟢通过 |
| 3 | skill-3 | canvas-design | 形状·文本·图层管理·导出PNG/SVG | `/mnt/agents/.user/skills/longhun-system/assets/skill-3-canvas-design.html` | 🟢 生产就绪 | 孝(0.3) | 🟢通过 |
| 4 | skill-4 | doc-coauthoring | Markdown实时预览·版本历史·统计导出 | `/mnt/agents/.user/skills/longhun-system/assets/skill-4-doc-coauthoring.html` | 🟢 生产就绪 | 孝(0.3) | 🟢通过 |
| 5 | skill-5 | internal-comms | 消息·状态更新·团队管理·实时统计 | `/mnt/agents/.user/skills/longhun-system/assets/skill-5-internal-comms.html` | 🟢 生产就绪 | 义(0.2) | 🟢通过 |

---

## 工具1：algorithmic-art（算法艺术生成器）

### 功能清单

| 功能模块 | 说明 | 状态 |
|----------|------|------|
| Perlin噪声流场 | 基于p5.js noise()的3D噪声流场驱动粒子运动 | 🟢 正常 |
| 粒子系统 | 支持50-5000个粒子实时渲染 | 🟢 正常 |
| 参数控制面板 | 粒子数量/噪声缩放/流速/粒子大小/透明度 | 🟢 正常 |
| 6种配色方案 | 海洋蓝/火焰红/森林绿/日落橙/赛博紫/黑白 | 🟢 正常 |
| PNG导出 | 一键保存画布为PNG图片 | 🟢 正常 |
| 实时统计 | FPS/帧数/运行状态显示 | 🟢 正常 |
| 响应式布局 | 自适应窗口大小变化 | 🟢 正常 |

### 文件信息

- **文件路径**: `/mnt/agents/.user/skills/longhun-system/assets/skill-1-algorithmic-art.html`
- **文件大小**: 约 420 行 HTML/CSS/JavaScript
- **外部依赖**: p5.js 1.4.0 (CDN: `https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.min.js`)
- **DNA标识**: `#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-ALGORITHMIC-ART-FILE1-FILE1-v1.0-1`

### 启动步骤

1. **方式一：浏览器直接打开**
   - 双击文件或在浏览器地址栏输入文件路径
   - 支持 Chrome / Firefox / Edge / Safari

2. **方式二：本地HTTP服务器**
   ```bash
   cd /mnt/agents/.user/skills/longhun-system
   python3 -m http.server 8766
   # 浏览器访问 http://localhost:8766/assets/skill-1-algorithmic-art.html
   ```

### 使用说明

1. **调整粒子数量**: 拖动"粒子数量"滑块（50-5000），数值越大画面越密集
2. **调整噪声缩放**: 拖动"噪声缩放"滑块（0.001-0.1），控制流场扭曲程度
3. **调整流速**: 拖动"流速"滑块（0.1-5），控制动画速度
4. **调整粒子大小**: 拖动"粒子大小"滑块（1-50）
5. **调整透明度**: 拖动"透明度"滑块（0-100%）
6. **切换配色**: 在下拉菜单中选择6种预设配色方案之一
7. **重置画布**: 点击"🔄 重置"按钮重新开始
8. **导出图片**: 点击"📥 下载"按钮保存PNG

### 界面截图

![algorithmic-art 界面截图](screenshot-skill-1-algorithmic-art.png)

> 截图说明：左侧为粒子流场画布区域，右侧为参数控制面板。面板包含粒子数量、噪声规模、流动速度、粒子大小、不透明度五个滑块控件，配色方案下拉选择器，重置和下载按钮，以及底部FPS/帧数/状态实时统计信息。整体采用深色主题（#0a0e27背景 + #00d4ff青色强调）。

---

## 工具2：brand-guidelines（龍魂品牌指南）

### 功能清单

| 功能模块 | 说明 | 状态 |
|----------|------|------|
| 色彩系统 | 主色调4色 + 语义色彩4色，含HEX/RGB/用途 | 🟢 正常 |
| 排版系统 | H1/H2/正文/标题四级字体规范展示 | 🟢 正常 |
| 组件库 | 按钮(主要/次要)/输入框/标签(成功/错误)/卡片 | 🟢 正常 |
| Do's & Don'ts | 品牌应用正确与错误做法指南 | 🟢 正常 |
| 响应式网格 | 8px基础网格系统可视化展示 | 🟢 正常 |

### 文件信息

- **文件路径**: `/mnt/agents/.user/skills/longhun-system/assets/skill-2-brand-guidelines.html`
- **文件大小**: 约 350 行 HTML/CSS
- **外部依赖**: 无（纯HTML/CSS，零依赖）
- **DNA标识**: `#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-BRAND-GUIDELINES-v1.0`

### 启动步骤

1. **方式一：浏览器直接打开**
   - 双击文件即可在浏览器中打开
   - 无需网络连接，完全离线可用

2. **方式二：本地HTTP服务器**
   ```bash
   cd /mnt/agents/.user/skills/longhun-system
   python3 -m http.server 8766
   # 浏览器访问 http://localhost:8766/assets/skill-2-brand-guidelines.html
   ```

### 使用说明

1. **查看色彩系统**: 滚动到"🎨 色彩系统"章节，查看主色调和语义色彩的颜色样本
2. **查看排版规范**: 滚动到"✍️ 排版系统"章节，查看H1/H2/正文/标题的字体规范
3. **查看组件库**: 滚动到"🧩 组件库"章节，查看按钮、输入框、标签、卡片等组件样式
4. **查看设计规范**: 滚动到"📋 应用指南"章节，查看Do's和Don'ts
5. **查看网格系统**: 滚动到"📐 响应式网格"章节，查看8px基础网格

### 界面截图

![brand-guidelines 界面截图](screenshot-skill-2-brand-guidelines.png)

> 截图说明：页面从上到下依次展示色彩系统（主色调4色+语义色彩4色）、字体规范（H1/H2/正文示例）、组件范围（按钮/输入框/标签/卡片）、设计规范（正确示例与错误示例）。采用深色主题，配色样本以色块+HEX值+RGB值+用途说明的形式展示。

---

## 工具3：canvas-design（画布设计工具）

### 功能清单

| 功能模块 | 说明 | 状态 |
|----------|------|------|
| 矩形绘制 | 点击拖拽绘制矩形，支持填充/边框/透明度 | 🟢 正常 |
| 圆形绘制 | 点击拖拽绘制圆形 | 🟢 正常 |
| 直线绘制 | 点击拖拽绘制直线 | 🟢 正常 |
| 文本工具 | 在画布上添加文本，支持字体大小调整 | 🟢 正常 |
| 选择工具 | 选择和移动已绘制图形 | 🟢 正常 |
| 删除工具 | 选中图形后删除 | 🟢 正常 |
| 属性面板 | 填充颜色/边框颜色/边框宽度/透明度/文本内容/字体大小 | 🟢 正常 |
| 导出PNG | 将画布导出为PNG图片 | 🟢 正常 |
| 导出SVG | 将图形导出为SVG矢量图 | 🟢 正常 |
| 清空画布 | 一键清除所有图形 | 🟢 正常 |

### 文件信息

- **文件路径**: `/mnt/agents/.user/skills/longhun-system/assets/skill-3-canvas-design.html`
- **文件大小**: 约 350 行 HTML/CSS/JavaScript
- **外部依赖**: 无（纯原生Canvas API，零依赖）
- **DNA标识**: 龍魂画布设计工具 v1.0

### 启动步骤

1. **方式一：浏览器直接打开**
   - 双击文件即可在浏览器中打开
   - 推荐 Chrome / Edge 浏览器以获得最佳体验

2. **方式二：本地HTTP服务器**
   ```bash
   cd /mnt/agents/.user/skills/longhun-system
   python3 -m http.server 8766
   # 浏览器访问 http://localhost:8766/assets/skill-3-canvas-design.html
   ```

### 使用说明

1. **选择工具**: 点击左侧工具栏的按钮切换工具（➤选择 / ▢矩形 / ⭕圆形 / ╱直线 / T文本 / ✕删除）
2. **绘制形状**: 选择矩形/圆形/直线工具后，在画布上点击拖拽即可绘制
3. **添加文本**: 选择文本工具，在右侧属性面板输入文本内容，然后在画布上点击放置
4. **调整属性**: 在右侧面板调整填充颜色、边框颜色、边框宽度、透明度、字体大小等
5. **移动图形**: 选择选择工具（➤），点击并拖拽图形到新位置
6. **删除图形**: 选择删除工具（✕），点击要删除的图形
7. **导出PNG**: 点击"📥 导出 PNG"按钮
8. **导出SVG**: 点击"📥 导出 SVG"按钮
9. **清空画布**: 点击"清空"按钮清除所有图形

### 界面截图

![canvas-design 界面截图](screenshot-skill-3-canvas-design.png)

> 截图说明：三栏布局设计。左侧为工具栏（选择/矩形/圆形/线条/文字/删除），中间为画布区域（深色渐变背景），右侧为属性面板（填充颜色、描边颜色、描边宽度、不透明度、文字内容、字体大小滑块，以及导出PNG/导出SVG按钮）。画布上可见示例绘制的矩形、圆形和文字。

---

## 工具4：doc-coauthoring（文档协作工具）

### 功能清单

| 功能模块 | 说明 | 状态 |
|----------|------|------|
| Markdown编辑器 | 左侧编辑器支持完整Markdown语法输入 | 🟢 正常 |
| 实时预览 | 右侧实时渲染Markdown预览，编辑即时同步 | 🟢 正常 |
| 快捷工具栏 | H1/H2/粗体/斜体/链接/列表/代码块/引用一键插入 | 🟢 正常 |
| 版本历史 | 自动保存最近10个版本，可回溯恢复 | 🟢 正常 |
| 统计信息 | 实时显示字数/行数/保存时间 | 🟢 正常 |
| 文档导出 | 导出为 .md Markdown文件 | 🟢 正常 |
| 示例文档 | 内置示例文档快速体验 | 🟢 正常 |

### 文件信息

- **文件路径**: `/mnt/agents/.user/skills/longhun-system/assets/skill-4-doc-coauthoring.html`
- **文件大小**: 约 350 行 HTML/CSS/JavaScript
- **外部依赖**: marked.js (CDN: `https://cdn.jsdelivr.net/npm/marked/marked.min.js`)
- **DNA标识**: 龍魂文档协作工具 v1.0

### 启动步骤

1. **方式一：浏览器直接打开**
   - 双击文件即可在浏览器中打开
   - 需要网络连接以加载marked.js依赖

2. **方式二：本地HTTP服务器**
   ```bash
   cd /mnt/agents/.user/skills/longhun-system
   python3 -m http.server 8766
   # 浏览器访问 http://localhost:8766/assets/skill-4-doc-coauthoring.html
   ```

### 使用说明

1. **编写Markdown**: 在左侧编辑器中输入Markdown文本，右侧自动实时预览
2. **使用快捷工具**: 点击工具栏按钮快速插入Markdown语法
   - H1: 插入 `# ` 一级标题
   - H2: 插入 `## ` 二级标题
   - 粗体: 插入 `**粗体**`
   - 斜体: 插入 `_斜体_`
   - 链接: 插入 `[链接](url)`
   - 列表: 插入 `- 列表项`
   - 代码块: 插入代码块标记
   - 引用: 插入 `> 引用`
3. **保存版本**: 点击"💾 保存"按钮保存当前版本到版本历史（最多保留10个版本）
4. **查看版本历史**: 在右侧面板查看已保存的版本列表，点击可恢复
5. **导出文档**: 点击"📥 导出"按钮下载 .md 文件
6. **加载示例**: 点击"📄 示例文档"加载预设示例内容
7. **清空文档**: 点击"🗑️ 清空文档"清空编辑器内容

### 界面截图

![doc-coauthoring 界面截图](screenshot-skill-4-doc-coauthoring.png)

> 截图说明：顶部为标题栏（保存/导出按钮），工具栏（H1/H2/加粗/斜体/链接/列表/代码块/引用），主区域左右分栏（左侧Markdown编辑器+右侧实时预览），右侧边栏（文档管理/版本历史/统计信息）。预览区域正确渲染标题、粗体、链接、列表、代码块等Markdown元素。

---

## 工具5：internal-comms（内部通讯系统）

### 功能清单

| 功能模块 | 说明 | 状态 |
|----------|------|------|
| 消息发送 | 支持4种消息类型：信息/状态更新/告警/系统公告 | 🟢 正常 |
| 消息展示 | 消息卡片按时间倒序展示，不同类型不同颜色标识 | 🟢 正常 |
| 团队管理 | 展示团队成员列表及在线状态（在线/忙碌/离线） | 🟢 正常 |
| 实时统计 | 总消息数/未读通知/活跃成员实时更新 | 🟢 正常 |
| 示例数据 | 一键加载预设示例消息 | 🟢 正常 |
| 消息清空 | 一键清空所有消息 | 🟢 正常 |

### 文件信息

- **文件路径**: `/mnt/agents/.user/skills/longhun-system/assets/skill-5-internal-comms.html`
- **文件大小**: 约 380 行 HTML/CSS/JavaScript
- **外部依赖**: 无（纯HTML/CSS/JavaScript，零依赖）
- **DNA标识**: `#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-INTERNAL-COMMS-v1.0`

### 启动步骤

1. **方式一：浏览器直接打开**
   - 双击文件即可在浏览器中打开
   - 无需网络连接，完全离线可用

2. **方式二：本地HTTP服务器**
   ```bash
   cd /mnt/agents/.user/skills/longhun-system
   python3 -m http.server 8766
   # 浏览器访问 http://localhost:8766/assets/skill-5-internal-comms.html
   ```

### 使用说明

1. **查看消息**: 页面加载后自动显示示例消息列表
2. **发送消息**:
   - 在"你的姓名"输入框中填写发送者名称（默认UID9622）
   - 在"消息类型"下拉框中选择消息类型
   - 在"消息内容"文本框中输入消息内容
   - 点击"🚀 发送"按钮发送消息
3. **查看统计**: 右侧面板实时显示总消息数、未读通知数、活跃成员数
4. **查看团队成员**: 右侧面板显示团队成员及在线状态（绿色=在线/黄色=忙碌/灰色=离线）
5. **加载示例**: 点击"📥 加载示例"按钮加载预设示例消息
6. **清空消息**: 点击"🗑️ 清空消息"按钮清除所有消息

### 消息类型说明

| 类型 | 标识色 | 用途 |
|------|--------|------|
| 📢 信息通知 | 蓝色 (#00d4ff) | 一般性信息通知 |
| 📊 状态更新 | 绿色 (#4ade80) | 系统状态/进度更新 |
| 🚨 告警通知 | 红色 (#ff006e) | 重要告警/错误通知 |
| 📣 系统公告 | 蓝色 (#00d4ff) | 系统级公告 |

### 界面截图

![internal-comms 界面截图](screenshot-skill-5-internal-comms.png)

> 截图说明：左右两栏布局。左侧上方为消息展示区（显示信息通知/状态更新/告警通知等不同类型的消息卡片，包含发送者头像、名称、时间戳、内容和类型标签），左侧下方为消息发送表单（姓名/消息类型/内容/发送按钮）。右侧为统计信息（总消息数/未读通知/活跃成员）、团队成员列表（带在线状态指示器）和快速操作按钮。

---

## 常见问题排查

### Q1: 工具打开后显示空白页面
- **原因**: 浏览器安全策略阻止了本地文件加载外部CDN资源
- **解决**: 使用本地HTTP服务器方式启动（见各工具的"方式二"）
- **审计**: 🟡标记

### Q2: algorithmic-art的p5.js加载失败
- **原因**: 网络问题导致CDN资源无法加载
- **解决**: 检查网络连接，或下载p5.min.js到本地并修改HTML中的src路径
- **审计**: 🟡标记

### Q3: doc-coauthoring的Markdown预览不工作
- **原因**: marked.js CDN加载失败
- **解决**: 检查网络连接，或下载marked.min.js到本地
- **审计**: 🟡标记

### Q4: canvas-design画布大小异常
- **原因**: 浏览器窗口大小改变后Canvas未正确调整
- **解决**: 刷新页面重新加载，或调整窗口大小后等待自动适配
- **审计**: 🟢通过

### Q5: brand-guidelines排版错乱
- **原因**: 使用了不兼容的浏览器或浏览器版本过旧
- **解决**: 升级到最新版Chrome/Firefox/Edge浏览器
- **审计**: 🟢通过

### Q6: internal-comms消息发送后未显示
- **原因**: 消息内容为空时系统会阻止发送
- **解决**: 确保消息内容不为空再点击发送
- **审计**: 🟢通过

---

## 工具状态汇总表

| 工具 | 文件路径 | 行数 | 依赖 | 状态 | 审计 |
|------|----------|------|------|------|------|
| algorithmic-art | `/mnt/agents/.user/skills/longhun-system/assets/skill-1-algorithmic-art.html` | ~420 | p5.js (CDN) | 🟢 生产就绪 | 🟢通过 |
| brand-guidelines | `/mnt/agents/.user/skills/longhun-system/assets/skill-2-brand-guidelines.html` | ~350 | 无 | 🟢 生产就绪 | 🟢通过 |
| canvas-design | `/mnt/agents/.user/skills/longhun-system/assets/skill-3-canvas-design.html` | ~350 | 无 | 🟢 生产就绪 | 🟢通过 |
| doc-coauthoring | `/mnt/agents/.user/skills/longhun-system/assets/skill-4-doc-coauthoring.html` | ~350 | marked.js (CDN) | 🟢 生产就绪 | 🟢通过 |
| internal-comms | `/mnt/agents/.user/skills/longhun-system/assets/skill-5-internal-comms.html` | ~380 | 无 | 🟢 生产就绪 | 🟢通过 |

---

## 底部DNA签名

```
═══════════════════════════════════════════════════════════
  #UID9622⚡️2026-06-16-HTML-TOOLS-v3.0
  确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
  忠(0.5) > 孝(0.3) > 义(0.2) 排序铁律
  CNSH中文编程规范 · 三色审计：🟢通过 🟡标记 🔴阻断
  责任: UID9622 · 龍芯北辰·诸葛鑫 · 不免责
  状态: 🟢 全部5个HTML工具生产就绪
═══════════════════════════════════════════════════════════
```

---

*本文档由龍魂系统自动生成 | 生成时间: 2026-06-16 | 版本: v3.0*

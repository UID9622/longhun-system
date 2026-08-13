# popup.html | 主界面布局

> Notion URL: https://app.notion.com/p/popup-html-495aa1bdbfa4488d8520b3c6ba91e0b8
> Created: 2025-12-13T05:04:00.000Z
> Last edited: 2026-07-01T14:50:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
# popup.html | LU-SYNC主界面HTML
DNA确认码：#ZHUGEXIN⚡️2025-LU-SYNC-POPUP-HTML-V1.0
## 📋 完整代码
```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>LU-SYNC Dashboard · Visual</title>
  <link rel="stylesheet" href="popup.css" />
</head>
<body>
  <div id="app" class="app">
    <header class="header">
      <div class="logo">
        <div class="taiji-small" id="taijiSmall" title="LU-SYNC · 太极"></div>
        <div class="title">UID9622 · V8</div>
      </div>
      <div class="controls">
        <button id="btnImport">导入 CSV / JSON</button>
        <button id="btnOpenKanban">打开 Kanban</button>
      </div>
    </header>

    <main class="main">
      <!-- 左列：视觉总览 -->
      <section class="left-col">
        <div class="card taiji-card">
          <div id="taijiContainer" class="taiji-container"></div>
          <div class="taiji-caption">太极 · 系统核心（点击展开）</div>
        </div>

        <div class="card matrix-card">
          <h3>五行矩阵</h3>
          <div id="matrixContainer" class="matrix-container"></div>
          <div id="matrixDetails" class="matrix-details"></div>
        </div>

        <div class="card furnace-card">
          <h3>错误炼化炉</h3>
          <div id="furnace" class="furnace"></div>
          <div id="furnaceLog" class="furnace-log">最近炼化：无</div>
        </div>
      </section>

      <!-- 右列：操作与 Kanban -->
      <section class="right-col">
        <div class="card ring-card">
          <h3>学习链进度</h3>
          <div id="learningRing" class="learning-ring"></div>
          <div id="learningStats" class="learning-stats">加载中…</div>
        </div>

        <div class="card kanban-card">
          <div class="kanban-header">
            <h3>Workers 看板</h3>
            <button id="btnAddDummy">+ 添加示例</button>
          </div>
          <div id="kanbanContainer" class="kanban-container"></div>
        </div>
      </section>
    </main>

    <footer class="footer">
      <small>LU-SYNC-LOG · 离线可视化 · 文化优先</small>
    </footer>

    <input type="file" id="fileInput" accept=".csv,.json,.md" style="display:none" />
  </div>

  <script src="../lib/idb.js"></script>
  <script src="../render/matrix.js"></script>
  <script src="../render/kanban.js"></script>
  <script src="popup.js"></script>
</body>
</html>
```
## 🎯 布局结构
### Header（顶部栏）
- 左侧：太极小图标 + 标题
- 右侧：导入按钮 + Kanban按钮
### Main（主体双列）
左列（left-col）：
1. 太极动画卡片
1. 五行矩阵卡片
1. 错误炼化炉卡片
右列（right-col）：
1. 学习链进度环
1. Workers Kanban看板
### Footer（底部）
- 版权说明："LU-SYNC-LOG · 离线可视化 · 文化优先"
## 📊 DOM ID映射
## 🔧 关键设计
### 响应式容器高度
- .taiji-container: 240px
- .matrix-container: 180px
- .furnace: 120px
- .learning-ring: 120px
- .kanban-container: 330px（可滚动）
### 文件导入
- 隐藏的 <input type="file"> 元素
- 支持 .csv, .json, .md 格式
- 通过按钮触发点击事件
---
创建人：💖 文心（技术归档）
源自：ChatGPT对话 - LU-SYNC UI视觉版

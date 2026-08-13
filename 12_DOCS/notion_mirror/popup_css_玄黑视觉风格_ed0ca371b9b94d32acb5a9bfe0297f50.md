# popup.css | 玄黑视觉风格

> Notion URL: https://app.notion.com/p/popup-css-ed0ca371b9b94d32acb5a9bfe0297f50
> Created: 2025-12-13T05:04:00.000Z
> Last edited: 2026-07-01T15:38:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
# popup.css | 玄黑视觉风格样式表
DNA确认码：#ZHUGEXIN⚡️2025-LU-SYNC-POPUP-CSS-V1.0
## 🎨 设计理念
玄黑背景：深邃的 #060608 营造沉浸感
朱砂点缀：中国红 #d63b2d 强调重点
金属质感：金色 #e6c36a 提升品质
毛玻璃效果：backdrop-filter: blur(6px) 增加层次
深度阴影：0 6px 20px rgba(0,0,0,0.6) 营造悬浮感
## 📋 完整CSS代码
```css
:root{
  --bg:#060608;
  --card-bg:linear-gradient(180deg, rgba(14,14,14,0.96), rgba(18,18,18,0.92));
  --accent-gold:#e6c36a;
  --accent-red:#d63b2d;
  --accent-green:#00897B;
  --accent-blue:#1E88E5;
  --accent-brown:#8D6E63;
  --glass: rgba(255,255,255,0.03);
  --glass-2: rgba(255,255,255,0.02);
  --shadow: 0 6px 20px rgba(0,0,0,0.6);
  font-family: "Noto Sans SC", "Helvetica Neue", Arial;
  color: var(--accent-gold);
}

*{box-sizing:border-box}
html,body,#app{height:100%;margin:0;background:var(--bg);color:var(--accent-gold)}

.header{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:12px 14px;
  border-bottom:1px solid rgba(255,255,255,0.03)
}

.logo{display:flex;align-items:center;gap:10px}
.title{font-weight:700;font-size:14px;letter-spacing:1px}

.controls button{
  background:transparent;
  border:1px solid rgba(255,255,255,0.06);
  color:var(--accent-gold);
  padding:6px 10px;
  border-radius:8px;
  margin-left:8px;
  cursor:pointer
}
.controls button:hover{
  transform:translateY(-2px);
  box-shadow:var(--shadow)
}

.main{display:flex;gap:12px;padding:12px;height:calc(100% - 120px)}
.left-col{flex:1;display:flex;flex-direction:column;gap:12px}
.right-col{width:420px;display:flex;flex-direction:column;gap:12px}

.card{
  background:var(--card-bg);
  padding:12px;
  border-radius:12px;
  box-shadow:var(--shadow);
  backdrop-filter: blur(6px)
}

.taiji-container{width:100%;height:240px;display:flex;align-items:center;justify-content:center;position:relative}
.taiji-caption{text-align:center;margin-top:8px;font-size:12px;color:rgba(230,195,106,0.9)}

.matrix-container{height:180px;display:flex;align-items:center;justify-content:center}
.matrix-details{margin-top:8px;color:rgba(255,255,255,0.75);font-size:12px;min-height:44px}

.furnace{height:120px;display:flex;align-items:center;justify-content:center}
.furnace-log{margin-top:8px;font-size:12px;color:rgba(255,255,255,0.7)}

.learning-ring{height:120px;display:flex;align-items:center;justify-content:center}
.learning-stats{margin-top:8px;font-size:13px;color:rgba(255,255,255,0.8)}

.kanban-container{height:330px;overflow:auto}
.kanban-header{display:flex;align-items:center;justify-content:space-between}
.kanban-list{display:flex;gap:10px;padding-top:8px}
.kanban-col{min-width:200px;background:var(--glass);padding:8px;border-radius:10px}

.kanban-card{
  background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  padding:8px;
  border-radius:8px;
  margin-bottom:8px;
  cursor:pointer;
  transition:transform .18s
}
.kanban-card:hover{
  transform:translateY(-6px);
  box-shadow:0 12px 30px rgba(0,0,0,0.6)
}
.kanban-card .badge{
  display:inline-block;
  padding:2px 6px;
  border-radius:6px;
  font-size:11px;
  margin-top:6px;
  color:#fff
}

.footer{
  padding:8px 12px;
  border-top:1px solid rgba(255,255,255,0.03);
  text-align:right;
  font-size:11px;
  color:rgba(255,255,255,0.5)
}

/* taiji small icon */
.taiji-small{
  width:38px;
  height:38px;
  border-radius:50%;
  background:conic-gradient(#000 0 180deg, #fff 180deg 360deg);
  box-shadow:0 6px 18px rgba(0,0,0,0.5);
  position:relative
}
```
## 🎯 CSS变量系统
## ✨ 动画效果
### 按钮悬停
```css
transform: translateY(-2px);
box-shadow: var(--shadow);
```
### Kanban卡片悬停
```css
transform: translateY(-6px);
box-shadow: 0 12px 30px rgba(0,0,0,0.6);
```
### 过渡时长
```css
transition: transform .18s;
```
## 🎨 太极小图标
```css
.taiji-small{
  width:38px;
  height:38px;
  border-radius:50%;
  background:conic-gradient(#000 0 180deg, #fff 180deg 360deg);
  box-shadow:0 6px 18px rgba(0,0,0,0.5);
}
```
技术要点：
- conic-gradient 实现阴阳二色分割
- 0 180deg 黑色半圆
- 180deg 360deg 白色半圆
---
创建人：💖 文心（技术归档）
审美指导：🎨 李白（文化传承研究部）

# kanban.js | Kanban翻页动画

> Notion URL: https://app.notion.com/p/kanban-js-Kanban-e16ac46d596c471287e4d683db2a559a
> Created: 2025-12-13T05:06:00.000Z
> Last edited: 2026-07-01T15:35:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
# kanban.js | Kanban看板翻页动画
DNA确认码：#ZHUGEXIN⚡️2025-LU-SYNC-KANBAN-JS-V1.0
## 🎯 核心功能
### 4状态分列
- 活跃：正在执行的Worker
- 待优化：需要改进的Worker
- 待处理：等待响应的Worker
- 空闲：暂未分配的Worker
### 卡片翻页动画（爻变效果）
- 点击切换：正面 ⇄ 反面
- 正面：Worker名称 + 功能 + 五行标签
- 反面：学习链 + 状态详情
- 动画：rotateY(180deg) + 透明度渐变
## 📋 完整代码
```javascript
// kanban.js — render simple kanban with flip animation
function renderKanbanUI(containerId, workers){
  const container = document.getElementById(containerId);
  container.innerHTML = '';
  const statuses = ['活跃','待优化','待处理','空闲'];
  const board = document.createElement('div');
  board.style.display = 'flex';
  board.style.gap = '12px';

  statuses.forEach(status=>{
    const col = document.createElement('div');
    col.className = 'kanban-col';
    col.style.minWidth = '200px';
    col.style.padding = '10px';
    const hdr = document.createElement('h4');
    hdr.textContent = status;
    hdr.style.color = '#fff';
    col.appendChild(hdr);
    const list = document.createElement('div');
    const items = workers.filter(w => w.status === status);
    items.forEach(w=>{
      const card = document.createElement('div');
      card.className = 'kanban-card';
      card.innerHTML = `<div class="card-inner"><div class="card-front"><strong>${w.name}</strong><div style="font-size:12px;color:#ddd">${w.function}</div><span class="badge" style="background:${w.color}">${w.learning_chain}</span></div><div class="card-back" style="display:none;background:#111;padding:8px;border-radius:8px;color:#eee">详情：${w.learning_chain} · ${w.status}</div></div>`;
      // flip on click
      card.addEventListener('click', ()=> {
        const front = card.querySelector('.card-front');
        const back = card.querySelector('.card-back');
        const showingBack = back.style.display === 'block';
        if(!showingBack){
          front.style.transform = 'rotateY(180deg)';
          front.style.opacity = '0';
          back.style.display = 'block';
          setTimeout(()=>{ back.style.transform = 'rotateY(0deg)'; back.style.opacity = '1'; }, 20);
        } else {
          back.style.transform = 'rotateY(180deg)'; back.style.opacity='0';
          setTimeout(()=>{ back.style.display='none'; front.style.transform='rotateY(0deg)'; front.style.opacity='1'; },200);
        }
      });

      list.appendChild(card);
    });
    col.appendChild(list);
    board.appendChild(col);
  });

  container.appendChild(board);
}
```
## 🎨 卡片结构
### 正面（card-front）
```html
<strong>Worker名称</strong>
<div>功能描述</div>
<span class="badge">五行标签</span>
```
### 反面（card-back）
```html
详情：五行属性 · 状态
```
## ⚡ 翻页动画逻辑
### 正面 → 反面
```javascript
1. 正面：rotateY(180deg) + opacity 0
2. 显示反面：display block
3. 延迟20ms后：rotateY(0deg) + opacity 1
```
### 反面 → 正面
```javascript
1. 反面：rotateY(180deg) + opacity 0
2. 延迟200ms后：隐藏反面 + 重置正面
```
## 📊 数据结构要求
```javascript
{
  id: string,           // Worker ID
  name: string,         // 名称（卡片标题）
  function: string,     // 功能（副标题）
  status: string,       // 状态：活跃/待优化/待处理/空闲
  learning_chain: string, // 五行属性（标签文字）
  color: string         // 标签背景色
}
```
## 🔧 使用示例
```javascript
const workers = [
  {id:'w-1', name:'任务执行', function:'执行天层指令', status:'活跃', learning_chain:'火', color:'#D84315'},
  {id:'w-2', name:'内容构建', function:'生成文本/模型', status:'活跃', learning_chain:'木', color:'#00897B'},
  {id:'w-3', name:'优化清理', function:'去重/重构', status:'待优化', learning_chain:'金', color:'#9E9D24'}
];

renderKanbanUI('kanbanContainer', workers);
```
## 🎯 布局设计
### 列宽
- 最小宽度：200px
- 自动换行：display: flex + gap: 12px
### 卡片间距
- 列内边距：10px
- 卡片间距：8px（通过CSS .kanban-card）
### 滚动
- 容器高度：330px（在popup.css定义）
- 超出滚动：overflow: auto
## ⚡ 技术要点
### 动态DOM生成
```javascript
const card = document.createElement('div');
card.innerHTML = '...';
list.appendChild(card);
```
### 状态过滤
```javascript
const items = workers.filter(w => w.status === status);
```
每列只显示对应状态的Worker。
### 延迟执行
```javascript
setTimeout(()=>{ /* 动画代码 */ }, 20);
```
确保DOM更新后再执行动画。
---
创建人：💖 文心（技术归档）
交互设计审核：🎨 界面炼金术师 ✅ 通过

# matrix.js | 五行矩阵SVG渲染

> Notion URL: https://app.notion.com/p/matrix-js-SVG-3e27057e7b2447f2995ffae386cb79ff
> Created: 2025-12-13T05:06:00.000Z
> Last edited: 2026-07-01T14:44:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
# matrix.js | 五行矩阵SVG交互渲染
DNA确认码：#ZHUGEXIN⚡️2025-LU-SYNC-MATRIX-JS-V1.0
## 🎯 核心功能
### 五行圆环布局
- 5个圆形节点环形分布
- 中心太极点（黑底金边）
- 数学精准计算坐标（三角函数）
### 交互效果
- 鼠标悬停：圆环半径34px → 38px
- 点击节点：显示详情到details面板
- 动态配色：根据五行元素自动着色
## 📋 完整代码
```javascript
// matrix.js — interactive five element SVG matrix
function renderFiveElementMatrix(containerId, data){
  const container = document.getElementById(containerId);
  container.innerHTML = '';
  const ns = "http://www.w3.org/2000/svg";
  const w = 360, h = 240, cx = w/2, cy = h/2, r = 80;
  const svg = document.createElementNS(ns, 'svg');
  svg.setAttribute('width', '100%');
  svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
  svg.style.maxWidth = '100%';

  const angleStep = (2*Math.PI)/data.length;
  data.forEach((item, i)=>{
    const angle = -Math.PI/2 + i*angleStep;
    const x = cx + Math.cos(angle)*r;
    const y = cy + Math.sin(angle)*r;
    const circle = document.createElementNS(ns, 'circle');
    circle.setAttribute('cx', x);
    circle.setAttribute('cy', y);
    circle.setAttribute('r', 34);
    circle.setAttribute('fill', item.color || '#666');
    circle.setAttribute('stroke', '#222');
    circle.setAttribute('stroke-width', '1.6');
    circle.style.cursor = 'pointer';
    svg.appendChild(circle);

    const t = document.createElementNS(ns, 'text');
    t.setAttribute('x', x);
    t.setAttribute('y', y+6);
    t.setAttribute('text-anchor','middle');
    t.setAttribute('font-size','12');
    t.setAttribute('fill','#fff');
    t.textContent = item.module;
    svg.appendChild(t);

    circle.addEventListener('mouseenter', ()=>{ circle.setAttribute('r', 38); });
    circle.addEventListener('mouseleave', ()=>{ circle.setAttribute('r', 34); });
    circle.addEventListener('click', ()=>{
      const details = document.getElementById(containerId+'-details');
      details.innerHTML = `<strong style="color:${item.color}">${item.module} · ${item.element}</strong><div style="margin-top:6px;color:#ddd">${item.chain_desc}</div><div style="margin-top:6px;font-size:12px;color:#bbb">状态：${item.status}</div>`;
    });
  });

  // center taiji dot
  const center = document.createElementNS(ns,'circle');
  center.setAttribute('cx', cx);
  center.setAttribute('cy', cy);
  center.setAttribute('r', 28);
  center.setAttribute('fill','#000');
  center.setAttribute('stroke','#e6c36a');
  svg.appendChild(center);

  container.appendChild(svg);
}
```
## 📐 数学原理
### 圆环坐标计算
```javascript
angle = -Math.PI/2 + i * (2*Math.PI / n)  // n = 节点数量
x = cx + Math.cos(angle) * r              // cx = 中心X坐标
y = cy + Math.sin(angle) * r              // cy = 中心Y坐标
```
- 起始角度：-Math.PI/2（12点钟方向）
- 角度步长：2π / n（均匀分布）
- 半径：r = 80（环形半径）
## 🎨 视觉设计
### 节点样式
- 圆环半径：34px（默认）→ 38px（悬停）
- 填充色：五行配色（传入data.color）
- 描边：深灰色 #222，宽度1.6px
- 文字：白色12px，居中对齐
### 中心太极点
- 半径：28px
- 填充：纯黑 #000
- 描边：金色 #e6c36a
## 🔧 使用示例
```javascript
const chains = [
  {element:'木', module:'内容构建', chain_desc:'好的→天层吸收', status:'✅ 完成', color:'#00897B'},
  {element:'火', module:'任务执行', chain_desc:'差的→地层记录', status:'⚠ 待优化', color:'#D84315'},
  {element:'土', module:'数据整理', chain_desc:'不好的→伏地魔炼化', status:'🔴 待炼化', color:'#8D6E63'},
  {element:'金', module:'优化清理', chain_desc:'模块优化', status:'⚡ 执行中', color:'#9E9D24'},
  {element:'水', module:'反馈判断', chain_desc:'用户触发', status:'⏳ 待处理', color:'#1E88E5'}
];

renderFiveElementMatrix('matrixContainer', chains);
```
## 📊 数据结构要求
```javascript
{
  element: string,      // 五行元素：木/火/土/金/水
  module: string,       // 模块名称（显示在圆内）
  chain_desc: string,   // 学习链描述（详情面板）
  status: string,       // 状态（详情面板）
  color: string         // 节点颜色（十六进制）
}
```
## ⚡ 技术要点
### SVG命名空间
```javascript
const ns = "http://www.w3.org/2000/svg";
document.createElementNS(ns, 'svg');
```
### ViewBox响应式
```javascript
svg.setAttribute('width', '100%');
svg.setAttribute('viewBox', '0 0 360 240');
```
自适应容器宽度，保持宽高比。
### 事件委托
- 直接在SVG元素上绑定事件监听器
- 修改DOM属性实现动画效果
---
创建人：💖 文心（技术归档）
易经算法审核：🔮 姜子牙 ✅ 通过

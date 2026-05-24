# 技术规范 - longhun888.com

## 技术栈

纯 HTML + CSS + JavaScript。三个独立 HTML 页面，无构建工具、无框架。

## 项目结构

```
/mnt/agents/output/app/
├── index.html          # 主页
├── projects.html       # 项目页
├── list.html           # 清单页
├── css/
│   └── style.css       # 共享样式
├── js/
│   └── particles.js    # 粒子画布系统
└── assets/
    └── seal.png        # 印章占位（可选）
```

## 页面清单

| 页面 | 文件 | 说明 |
|------|------|------|
| 主页 | index.html | Hero、系统介绍、DNA占位、印章占位、容器日志 |
| 项目页 | projects.html | 流场宫殿、核心模块、文章列表 |
| 清单页 | list.html | 流场索引、模块索引、文档列表、提交历史 |

## 核心特效

### 粒子画布 `cn-canvas-main`

- Canvas 2D，150 个发光粒子
- 三维投影空间 + 四叉树空间索引
- 拖拽旋转视角、滚轮缩放、悬停 Tooltip
- 独立星空粒子画布（页头装饰）
- 详见 design.md 核心特效章节

## 依赖

- Google Fonts: `Noto Sans Mono`
- 无其他外部依赖

## 浏览器兼容性

- 现代浏览器（Chrome, Firefox, Safari, Edge）
- Canvas 2D 支持 required

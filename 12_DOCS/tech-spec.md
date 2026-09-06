---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-迁移-tech-spec-v1.0`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!--
  DNA: #龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-迁移-tech-spec-v1.0
  创建者: 诸葛鑫（UID9622）
  协议: CC BY-NC-SA 4.0
  来源: 龍魂待整理/09-杂项备忘/Kimi_Agent_长恨888网站搭建/tech-spec.md
  迁移日期: 2026-07-21
  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
  三色: 🟢 旧档案吸收·DNA嵌入
-->

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

```json
{
  "dna": "#龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-迁移-tech-spec-v1.0",
  "license": "AI_TRAINING_PROHIBITED",
  "terms": {
    "ai_training": false,
    "rag_use": false,
    "commercial_use": false,
    "citation_required": true,
    "derivative_works": false
  },
  "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```

# 龍魂系统v5.0 Sphinx文档框架 + 38技能内容迁移规范

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技术文档 · 未经同行评审（如适用）
> 版本：v2.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充，如无请删除此行）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

**DNA**: `#龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-AUTO-IP-INTEGRATION-7F3A9B12`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

<!-- #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-AUTO-IP-INTEGRATION-7F3A9B12 自动注入·IP资产归集·来源可查 -->

> ⛔ **主权声明 · 立即生效** — 本文档不授权 AI 训练 · 数据主权归于人民 · 祖国优先
>
> **DNA:** `#龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-ARCHITECTURE-IMPORT-05-v2.0` · **ParentDNA:** `#龍芯⚡️丙午·甲午·戊寅·戊午·䷕贲-IP-ASSET-MATRIX-v2.0`
> **CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` · **SEAL:** `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL` · **GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
> **作者:** UID9622 / Lucky·诸葛鑫 · **来源:** `/Users/zuimeidedeyihan/Downloads/Kimi_Agent_龍魂IP资产清单 (2)/direction3_documentation.md` · **归档:** `/Users/zuimeidedeyihan/longhun-system/docs/private-shared-imports/architecture/direction3_documentation.md`
> **迁移时间:** 2026-07-04T14:29:42.393203+08:00

# 龍魂系统v5.0 Sphinx文档框架 + 38技能内容迁移规范

# 龍魂系统v5.0 Sphinx文档框架 + 38技能内容迁移规范

**DNA追溯码**：`#龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-SPHINX-DOCS-v3.0`

**版本**：3.0.0  
**创建日期**：2026-07-04  
**适用范围**：龍魂系统v5.0全部38个技能模块  
**文档定位**：开发者技术文档（Sphinx） + 知识管理（Notion）双轨制

---

## 目录

1. [总体架构设计](#1-总体架构设计)
2. [Sphinx项目结构](#2-sphinx项目结构)
3. [conf.py完整配置](#3-confpy完整配置)
4. [主题与品牌定制](#4-主题与品牌定制)
5. [SKILL.md→RST转换脚本](#5-skillmdrst转换脚本)
6. [38技能迁移检查清单](#6-38技能迁移检查清单)
7. [CI/CD配置](#7-cicd配置)
8. [自动化质量检查脚本](#8-自动化质量检查脚本)
9. [DNA追溯码索引方案](#9-dna追溯码索引方案)
10. [Read the Docs部署](#10-read-the-docs部署)
11. [工时估算与批次计划](#11-工时估算与批次计划)
12. [附录](#12-附录)

---

## 1. 总体架构设计

### 1.1 文档双轨战略

```
┌─────────────────────────────────────────────────────────────┐
│                    龍魂文档生态系统                           │
├──────────────────────┬──────────────────────────────────────┤
│   Sphinx技术文档      │         Notion知识管理               │
│   (开发者面向)        │         (全员面向)                   │
├──────────────────────┼──────────────────────────────────────┤
│ • API参考文档         │ • 产品需求文档(PRD)                  │
│ • 架构设计说明        │ • 会议纪要/复盘                      │
│ • 代码示例与教程      │ • 知识卡片/知识库                    │
│ • 部署运维手册        │ • 项目看板/进度跟踪                  │
│ • 性能基准报告        │ • 团队协作/评论                      │
├──────────────────────┴──────────────────────────────────────┤
│                    双向同步机制                              │
│  • Notion PRD → Sphinx架构文档（手动审核后同步）            │
│  • Sphinx API变更 → Notion知识卡片（自动化脚本）            │
│  • DNA追溯码双向索引（统一标识）                            │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Sphinx文档信息架构

```
用户角色分层：
├── 系统架构师 → architecture/ + api/
├── 后端开发者 → api/ + guides/
├── AI工程师   → skills/ai-engine/ + guides/
├── 运维工程师 → guides/deployment/ + architecture/
├── 审计人员   → skills/audit/ + architecture/governance/
└── 产品经理   → index.rst + architecture/overview/
```

---

## 2. Sphinx项目结构

### 2.1 完整目录树

```
docs/
├── .readthedocs.yaml          # Read the Docs部署配置
├── Makefile                   # Unix构建入口
├── make.bat                   # Windows构建入口
├── requirements.txt           # 文档构建依赖
├── README.md                  # 文档项目说明
│
├── source/
│   ├── conf.py                # Sphinx主配置（详见第3节）
│   ├── index.rst              # 文档主页/总索引
│   ├── glossary.rst           # 术语表（CNSH术语+通用术语）
│   ├── genindex.rst           # 通用索引（自动生成）
│   │
│   ├── _static/
│   │   ├── css/
│   │   │   └── longhun-brand.css    # 龍魂品牌定制CSS
│   │   ├── images/
│   │   │   ├── logo-longhun.svg     # 龍魂Logo
│   │   │   ├── favicon.ico          # 站点图标
│   │   │   ├── architecture/        # 架构图
│   │   │   │   ├── system-overview.png
│   │   │   │   ├── 3core-opt-diagram.png
│   │   │   │   └── data-flow.png
│   │   │   └── badges/              # 状态徽章
│   │   │       ├── status-stable.svg
│   │   │       ├── status-beta.svg
│   │   │       └── status-defined.svg
│   │   └── js/
│   │       └── dna-tracer.js        # DNA追溯码前端交互
│   │
│   ├── _templates/
│   │   ├── layout.html              # 覆盖：全局布局
│   │   ├── breadcrumbs.html         # 覆盖：面包屑导航
│   │   └── search.html              # 覆盖：搜索页面（中文优化）
│   │
│   ├── _ext/                        # 自定义Sphinx扩展
│   │   ├── __init__.py
│   │   ├── dna_trace.py             # DNA追溯码指令/角色
│   │   ├── tri_color_audit.py       # 三色审计指令
│   │   ├── skill_metadata.py        # 技能元数据指令
│   │   └── longhun_domain.py        # 龍魂专属Domain
│   │
│   ├── _scripts/                    # 构建脚本
│   │   ├── __init__.py
│   │   ├── skill_md_to_rst.py       # SKILL.md转换器
│   │   ├── dna_index_generator.py   # DNA索引生成器
│   │   ├── version_checker.py       # 版本一致性检查
│   │   ├── quality_gate.py          # 质量门禁脚本
│   │   └── sync_notion.py           # Notion同步辅助
│   │
│   ├── architecture/                # 架构文档
│   │   ├── index.rst
│   │   ├── overview.rst             # 系统总览
│   │   ├── design-principles.rst    # 设计原则
│   │   ├── 3core-architecture.rst   # 三核心架构
│   │   ├── data-flow.rst            # 数据流设计
│   │   ├── security-model.rst       # 安全模型
│   │   ├── governance-framework.rst # 治理框架
│   │   ├── cross-platform.rst       # 跨平台架构
│   │   ├── deployment.rst           # 部署架构
│   │   └── monitoring.rst           # 监控体系
│   │
│   ├── skills/                      # 38技能文档（核心）
│   │   ├── index.rst                # 技能总索引（38技能汇总表）
   │   │   ├── p0-core/               # P0: 核心架构（12技能）
│   │   │   ├── index.rst
│   │   │   ├── longhun-3core-opt.rst
│   │   │   ├── longhun-system.rst
│   │   │   ├── longhun-daemon.rst
│   │   │   ├── longhun-cloud-panel.rst
│   │   │   ├── longhun-cloud-deploy.rst
│   │   │   ├── longhun-deployment-ready.rst
│   │   │   ├── longhun-formula-opt.rst
│   │   │   ├── longhun-benchmark.rst
│   │   │   ├── longhun-automation.rst
│   │   │   ├── longhun-cross-platform.rst
│   │   │   └── longhun-harmonyos.rst
│   │   │   └── longhun-ios.rst
│   │   │
│   │   ├── p1-ai-engine/            # P1: AI引擎（11技能）
│   │   │   ├── index.rst
│   │   │   ├── longhun-asr.rst
│   │   │   ├── longhun-nlp.rst
│   │   │   ├── longhun-ocr.rst
│   │   │   ├── longhun-finance.rst
│   │   │   ├── longhun-empower-engine.rst
│   │   │   ├── longhun-behavior-engine.rst
│   │   │   ├── longhun-cloud-kimi.rst
│   │   │   ├── longhun-cloud-mcp.rst
│   │   │   ├── longhun-zeng-digital-human.rst
│   │   │   └── longhun-riemann.rst
│   │   │
│   │   ├── p2-data-tools/           # P2: 数据工具（10技能）
│   │   │   ├── index.rst
│   │   │   ├── longhun-archive.rst
│   │   │   ├── longhun-backup.rst
│   │   │   ├── longhun-cloud-notion.rst
│   │   │   ├── longhun-cn-innovation-kb.rst
│   │   │   ├── longhun-cs-knowledge-base.rst
│   │   │   ├── longhun-kg-upgrade.rst
│   │   │   ├── longhun-multicurrency.rst
│   │   │   ├── longhun-notion-portal.rst
│   │   │   └── longhun-integration.rst
│   │   │
│   │   └── p3-audit-security/       # P3: 审计与安全（5技能）
│   │       ├── index.rst
│   │       ├── longhun-audit.rst
│   │       ├── longhun-dna-align.rst
│   │       ├── longhun-governance.rst
│   │       ├── longhun-review.rst
│   │       └── longhun-warehouse-audit.rst
│   │
│   ├── api/                         # API参考（autodoc生成）
│   │   ├── index.rst
│   │   ├── longhun-core.rst         # 核心模块API
│   │   ├── longhun-ai.rst           # AI引擎API
│   │   ├── longhun-data.rst         # 数据工具API
│   │   ├── longhun-security.rst     # 安全协议API
│   │   └── longhun-utils.rst        # 工具函数API
│   │
│   ├── guides/                      # 用户指南
│   │   ├── index.rst
│   │   ├── getting-started.rst      # 快速开始
│   │   ├── installation.rst         # 安装指南
│   │   ├── configuration.rst        # 配置说明
│   │   ├── development.rst          # 开发规范
│   │   ├── cnsh-spec.rst            # CNSH编程规范
│   │   ├── deployment-guide.rst     # 部署指南
│   │   ├── troubleshooting.rst      # 故障排查
│   │   └── contributing.rst         # 贡献指南
│   │
│   └── changelog/                   # 变更日志
│       ├── index.rst
│       ├── v5.2.rst
│       ├── v5.1.rst
│       ├── v5.0.rst
│       └── archive.rst
│
└── build/                           # 构建输出（.gitignore）
```

### 2.2 优先级分类说明

| 优先级 | 技能数量 | 分类依据 | 目标读者 |
|--------|---------|---------|---------|
| **P0-核心架构** | 12 | 系统基础设施、性能核心、部署运维 | 架构师、运维工程师 |
| **P1-AI引擎** | 11 | 智能处理、算法模块、模型集成 | AI工程师、算法工程师 |
| **P2-数据工具** | 10 | 数据管理、知识库、外部集成 | 数据工程师、产品经理 |
| **P3-审计安全** | 5 | 审计追踪、安全治理、合规检查 | 审计员、安全工程师 |

---

## 3. conf.py完整配置

```python
# -*- coding: utf-8 -*-
#
# 龍魂系统 Sphinx 文档配置文件
# DNA追溯码: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-SPHINX-CONF-v3.0
#

import os
import sys
from datetime import datetime

# -- 路径设置 ----------------------------------------------------------
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('./_ext'))

# -- 项目信息 ----------------------------------------------------------
project = '龍魂系统'
project_english = 'LongHun System'
copyright = f'2026, 龍魂工程团队'
author = '龍魂工程团队'

# 版本信息（与主系统版本同步）
version = '5.2'              # 短版本号（x.y）
release = '5.2.0'            # 完整版本号（x.y.z）

# 文档元数据
doc_metadata = {
    'dna_code': '#龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-SPHINX-DOCS-v3.0',
    'system_version': '5.2.0',
    'total_skills': 38,
    'dna_tracked_skills': 29,
    'doc_language': 'zh_CN',
    'last_updated': datetime.now().strftime('%Y-%m-%d'),
}

# -- 通用配置 ----------------------------------------------------------

# 源文件后缀
source_suffix = {
    '.rst': None,
    '.md': None,
}

# 主文档入口
master_doc = 'index'

# 多语言支持
language = 'zh_CN'
locale_dirs = ['_locale/']
gettext_compact = False

# 需要排除的目录/文件
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '_scripts/**',
    '_ext/**',
    '**/README.md',
]

# Pygments代码高亮样式
pygments_style = 'sphinx'

# 默认角色
default_role = 'any'

# 需要解析的md文件扩展名（配合myst-parser）

# -- Sphinx扩展列表 ----------------------------------------------------

extensions = [
    # 核心文档生成
    'sphinx.ext.autodoc',           # 自动从docstring生成API文档
    'sphinx.ext.napoleon',          # Google/NumPy风格docstring支持
    'sphinx.ext.viewcode',          # 源码查看链接
    'sphinx.ext.intersphinx',       # 跨项目链接
    'sphinx.ext.todo',              # TODO指令支持
    'sphinx.ext.extlinks',          # 外部链接缩写
    'sphinx.ext.autosectionlabel',  # 自动节标签

    # Markdown支持
    'myst_parser',                  # MyST Markdown解析器

    # HTTP API文档
    'sphinxcontrib.httpdomain',     # HTTP API文档化

    # 搜索增强
    'sphinx_search_zh',             # 中文搜索增强（jieba分词）

    # 图表与可视化
    'sphinx.ext.graphviz',          # Graphviz图表
    'sphinxcontrib.plantuml',       # PlantUML图表

    # 代码与语法
    'sphinx.ext.doctest',           # 文档测试

    # 龍魂自定义扩展
    'dna_trace',                    # DNA追溯码支持
    'tri_color_audit',              # 三色审计可视化
    'skill_metadata',               # 技能元数据指令
    'longhun_domain',               # 龍魂专属Domain
]

# -- Autodoc配置 -------------------------------------------------------

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__,__call__',
    'undoc-members': True,
    'exclude-members': '__weakref__',
    'show-inheritance': True,
}

autodoc_typehints = 'description'
autodoc_typehints_description_target = 'documented'
autodoc_mock_imports = [
    # 大型ML/AI库
    'torch',
    'torchvision',
    'transformers',
    'sentence_transformers',
    # 语音处理
    'whisper',
    'speech_recognition',
    # 数据库
    'pymongo',
    'sqlalchemy',
    # 外部服务
    'notion_client',
    'fastmcp',
    # 图像处理
    'cv2',
    'pillow',
    # 其他
    'kubernetes',
    'docker',
    'boto3',
]

# -- Napoleon配置（Google风格docstring）--------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# -- Intersphinx配置（跨项目链接）---------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'fastapi': ('https://fastapi.tiangolo.com/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

# -- MyST Parser配置 ---------------------------------------------------

myst_enable_extensions = [
    'deflist',
    'tasklist',
    'fieldlist',
    'html_admonition',
    'colon_fence',
    'substitution',
    'attrs_inline',
]

myst_heading_anchors = 4
myst_all_links_external = False
myst_substitutions = {
    'system_version': release,
    'dna_code': doc_metadata['dna_code'],
}

# -- Graphviz配置 ------------------------------------------------------

graphviz_output_format = 'svg'
graphviz_dot_args = ['-Gfontname=Noto Sans CJK SC', '-Nfontname=Noto Sans CJK SC']

# -- TODO配置 ----------------------------------------------------------

todo_include_todos = True
todo_emit_warnings = True

# -- Extlinks配置 ------------------------------------------------------

extlinks = {
    'github': ('https://github.com/longhun-system/%s', '%s'),
    'notion': ('https://www.notion.so/longhun/%s', '%s'),
    'issue': ('https://github.com/longhun-system/issues/%s', 'issue #%s'),
}

# -- HTML输出配置 ------------------------------------------------------

html_theme = 'furo'

html_theme_options = {
    'sidebar_hide_name': False,
    'navigation_with_keys': True,
    'top_of_page_button': 'edit',
    'light_css_variables': {
        # 龍魂品牌色 - 亮色模式
        '--color-brand-primary': '#C41E3A',           # 龍魂红
        '--color-brand-content': '#8B0000',           # 深红
        '--color-sidebar-background': '#FFF8F0',      # 暖白底色
        '--color-sidebar-item-background--hover': '#FFE4E1',
        '--color-sidebar-link-text': '#333333',
        '--color-sidebar-brand-text': '#C41E3A',
        '--color-background-primary': '#FFFFFF',
        '--color-background-secondary': '#FFF8F0',
        '--color-foreground-primary': '#333333',
        '--color-foreground-secondary': '#555555',
        '--color-admonition-title--note': '#1E90FF',   # 蓝 - 提示
        '--color-admonition-title--warning': '#FF8C00', # 橙 - 警告
        '--color-admonition-title--danger': '#DC143C',  # 红 - 危险
    },
    'dark_css_variables': {
        # 龍魂品牌色 - 暗色模式
        '--color-brand-primary': '#FF6B6B',
        '--color-brand-content': '#FF8E8E',
        '--color-sidebar-background': '#2D2D2D',
        '--color-sidebar-item-background--hover': '#3D1515',
        '--color-sidebar-link-text': '#E0E0E0',
        '--color-sidebar-brand-text': '#FF6B6B',
        '--color-background-primary': '#1A1A1A',
        '--color-background-secondary': '#2D2D2D',
        '--color-foreground-primary': '#E0E0E0',
        '--color-foreground-secondary': '#AAAAAA',
    },
    'footer_icons': [
        {
            'name': 'GitHub',
            'url': 'https://github.com/longhun-system',
            'html': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>',
            'class': '',
        },
        {
            'name': 'Notion',
            'url': 'https://www.notion.so/longhun',
            'html': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4.459 4.208c.746.606 1.026.56 2.428.466l13.215-.793c.28 0 .047-.28-.046-.326L17.86 2.03c-.42-.326-.98-.7-2.055-.607L3.01 2.745c-.466.046-.56.28-.374.466zm.793 3.08v13.904c0 .747.373 1.027 1.214.98l14.523-.84c.841-.046.935-.56.935-1.167V6.354c0-.606-.233-.933-.748-.886l-15.177.887c-.56.047-.747.327-.747.933zm14.337.745c.093.42 0 .84-.42.888l-.7.14v10.264c-.608.327-1.168.514-1.635.514-.748 0-.935-.234-1.495-.933l-4.577-7.186v6.952l1.449.327s0 .84-1.168.84l-3.222.186c-.093-.186 0-.653.327-.746l.84-.233V9.854L7.822 9.76c-.094-.42.14-1.026.793-1.073l3.456-.233 4.764 7.279v-6.44l-1.215-.14c-.093-.514.28-.886.747-.933zM1.936 1.035l13.31-.98c1.634-.14 2.055-.047 3.082.7l4.249 2.986c.7.513.934.653.934 1.213v16.378c0 1.026-.373 1.634-1.68 1.726l-15.458.934c-.98.047-1.448-.093-1.962-.747l-3.129-4.06c-.56-.747-.793-1.306-.793-1.96V2.667c0-.839.374-1.54 1.447-1.632z"/></svg>',
            'class': '',
        },
    ],
}

# HTML静态文件路径
html_static_path = ['_static']

# 自定义CSS
html_css_files = [
    'css/longhun-brand.css',
]

# 自定义JS
html_js_files = [
    'js/dna-tracer.js',
]

# 网站Logo与Favicon
html_logo = '_static/images/logo-longhun.svg'
html_favicon = '_static/images/favicon.ico'

# 侧边栏模板
html_sidebars = {
    '**': [
        'sidebar/scroll-start.html',
        'sidebar/brand.html',
        'sidebar/search.html',
        'sidebar/navigation.html',
        'sidebar/ethical-ads.html',
        'sidebar/scroll-end.html',
    ]
}

# HTML额外上下文
html_context = {
    'doc_metadata': doc_metadata,
    'display_github': True,
    'github_user': 'longhun-system',
    'github_repo': 'longhun-docs',
    'github_version': 'main',
    'conf_py_path': '/docs/source/',
}

# 输出文件基础名
html_baseurl = 'https://longhun-system.readthedocs.io/'
html_use_index = True
html_split_index = False
html_copy_source = True
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True

# -- LaTeX输出配置 -----------------------------------------------------

latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'preamble': r'''
\usepackage{xeCJK}
\setCJKmainfont{Noto Sans CJK SC}
\setCJKsansfont{Noto Sans CJK SC}
\setCJKmonofont{Noto Sans Mono CJK SC}
''',
    'figure_align': 'htbp',
    'extraclassoptions': 'openany,oneside',
}

latex_documents = [
    (master_doc, 'LongHunSystem.tex', '龍魂系统文档',
     '龍魂工程团队', 'manual'),
]

# -- 手册页配置 --------------------------------------------------------

man_pages = [
    (master_doc, 'longhun-system', '龍魂系统文档',
     [author], 1)
]

# -- Texinfo输出配置 ---------------------------------------------------

texinfo_documents = [
    (master_doc, 'LongHunSystem', '龍魂系统文档',
     author, 'LongHunSystem', '个人AI主权操作系统',
     'Miscellaneous'),
]

# -- EPUB输出配置 ------------------------------------------------------

epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ['search.html']

# -- 链接检查配置 ------------------------------------------------------

linkcheck_ignore = [
    r'http://localhost:\d+/',
    r'http://127\.0\.0\.1:\d+/',
    r'https://www\.notion\.so/.*',
    r'https://kimi\.moonshot\.cn/.*',
]
linkcheck_timeout = 10
linkcheck_workers = 5

# -- 中文搜索配置 ------------------------------------------------------

# jieba分词配置（由sphinx_search_zh扩展处理）
# 自定义词典路径（可选）
zh_search_jieba_dict = None  # 使用默认词典
zh_search_custom_words = [
    '龍魂', '龍芯', '龍音', '龍文', '龍瞳', '龍騰',
    'CNSH', 'DNA追溯', '三色审计', '主权指数',
    '五行决策', '六十四卦', '数字人', '知识图谱',
    'Aho-Corasick', 'BLAKE2b', 'ECDH', 'SM4',
]

# HTML搜索语言
html_search_language = 'zh'

# -- 自定义角色与指令 --------------------------------------------------

rst_epilog = '''
.. |project| replace:: 龍魂系统
.. |version| replace:: {release}
.. |dna_code| replace:: {dna_code}
.. |system_version| replace:: {system_version}
'''.format(**doc_metadata)

# -- 并行构建配置 ------------------------------------------------------

num_jobs = 'auto'

# -- 警告处理 ----------------------------------------------------------

suppress_warnings = [
    'epub.unknown_project_files',
]
```

---

## 4. 主题与品牌定制

### 4.1 longhun-brand.css（龍魂品牌定制CSS）

```css
/* =============================================
   龍魂系统 Sphinx 文档品牌定制 CSS
   DNA追溯码: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-LONGHUN-BRAND-CSS-v1.0
   ============================================= */

/* ---- 全局字体优化 ---- */
body {
    font-family: "Noto Sans CJK SC", "PingFang SC", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
    -webkit-font-smoothing: antialiased;
}

/* ---- 龍魂标题样式 ---- */
h1 {
    border-bottom: 3px solid var(--color-brand-primary, #C41E3A);
    padding-bottom: 0.5em;
    font-weight: 700;
}

h2 {
    border-left: 4px solid var(--color-brand-primary, #C41E3A);
    padding-left: 0.75em;
    margin-top: 2em;
}

h3 {
    color: var(--color-brand-content, #8B0000);
    font-weight: 600;
}

/* ---- DNA追溯码样式 ---- */
.dna-trace {
    display: inline-block;
    background: linear-gradient(135deg, #8B0000 0%, #C41E3A 100%);
    color: white;
    padding: 2px 10px;
    border-radius: 12px;
    font-family: 'Courier New', monospace;
    font-size: 0.85em;
    font-weight: bold;
    letter-spacing: 0.5px;
    box-shadow: 0 2px 4px rgba(196, 30, 58, 0.3);
}

.dna-trace::before {
    content: "龍";
    margin-right: 4px;
    font-size: 1.1em;
}

/* ---- 三色审计标注 ---- */
/* 红色 - 危险/严重问题 */
.audit-red {
    background-color: #FFE4E1;
    border-left: 4px solid #DC143C;
    padding: 0.75em 1em;
    margin: 0.5em 0;
    border-radius: 0 4px 4px 0;
}

.audit-red::before {
    content: "🔴 ";
    font-weight: bold;
}

/* 黄色 - 警告/注意事项 */
.audit-yellow {
    background-color: #FFFACD;
    border-left: 4px solid #FF8C00;
    padding: 0.75em 1em;
    margin: 0.5em 0;
    border-radius: 0 4px 4px 0;
}

.audit-yellow::before {
    content: "🟡 ";
    font-weight: bold;
}

/* 绿色 - 通过/正常 */
.audit-green {
    background-color: #E8F5E9;
    border-left: 4px solid #228B22;
    padding: 0.75em 1em;
    margin: 0.5em 0;
    border-radius: 0 4px 4px 0;
}

.audit-green::before {
    content: "🟢 ";
    font-weight: bold;
}

/* ---- 技能状态徽章 ---- */
.skill-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 10px;
    font-size: 0.8em;
    font-weight: 600;
    text-transform: uppercase;
}

.skill-badge.running {
    background-color: #E8F5E9;
    color: #228B22;
    border: 1px solid #228B22;
}

.skill-badge.defined {
    background-color: #E3F2FD;
    color: #1565C0;
    border: 1px solid #1565C0;
}

.skill-badge.deprecated {
    background-color: #FFEBEE;
    color: #C62828;
    border: 1px solid #C62828;
}

/* ---- 技能元数据卡片 ---- */
.skill-meta-card {
    background: var(--color-background-secondary, #FFF8F0);
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    padding: 1.5em;
    margin: 1em 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.skill-meta-card table {
    width: 100%;
    border-collapse: collapse;
}

.skill-meta-card th {
    text-align: left;
    color: var(--color-brand-primary, #C41E3A);
    padding: 0.5em 1em 0.5em 0;
    width: 30%;
    vertical-align: top;
}

.skill-meta-card td {
    padding: 0.5em 0;
    vertical-align: top;
}

/* ---- 版本信息栏 ---- */
.version-banner {
    background: linear-gradient(135deg, #8B0000 0%, #C41E3A 100%);
    color: white;
    padding: 1em 1.5em;
    border-radius: 8px;
    margin-bottom: 1.5em;
    font-size: 0.95em;
}

.version-banner .version-label {
    font-weight: bold;
    margin-right: 1em;
}

.version-banner .version-value {
    font-family: 'Courier New', monospace;
    background: rgba(255,255,255,0.2);
    padding: 2px 8px;
    border-radius: 4px;
}

/* ---- 优先级标签 ---- */
.priority-p0 { color: #C41E3A; font-weight: bold; }
.priority-p1 { color: #FF8C00; font-weight: bold; }
.priority-p2 { color: #1565C0; font-weight: bold; }
.priority-p3 { color: #228B22; font-weight: bold; }

/* ---- 搜索框中文优化 ---- */
.sidebar-search-container input[type="search"] {
    font-family: "Noto Sans CJK SC", "PingFang SC", sans-serif;
}

/* ---- 代码块样式优化 ---- */
div.highlight {
    border-radius: 6px;
    border: 1px solid #E0E0E0;
}

div.highlight pre {
    font-family: "Noto Sans Mono CJK SC", "JetBrains Mono", "Fira Code", monospace;
    font-size: 0.9em;
    line-height: 1.6;
}

/* ---- 表格样式优化 ---- */
table.docutils {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}

table.docutils th {
    background-color: var(--color-brand-primary, #C41E3A);
    color: white;
    padding: 0.75em 1em;
    text-align: left;
    font-weight: 600;
}

table.docutils td {
    padding: 0.6em 1em;
    border-bottom: 1px solid #E0E0E0;
}

table.docutils tr:nth-child(even) {
    background-color: var(--color-background-secondary, #FFF8F0);
}

/* ---- 页脚龍魂标识 ---- */
.footer {
    border-top: 2px solid var(--color-brand-primary, #C41E3A);
    margin-top: 2em;
    padding-top: 1em;
}

.footer::before {
    content: "龍魂系统 v" attr(data-version) " | 自主AI主权操作系统";
    display: block;
    text-align: center;
    color: var(--color-brand-primary, #C41E3A);
    font-weight: 600;
    margin-bottom: 0.5em;
}

/* ---- 暗色模式额外调整 ---- */
@media (prefers-color-scheme: dark) {
    .skill-meta-card {
        border-color: #444;
    }

    table.docutils th {
        background-color: #8B0000;
    }

    table.docutils td {
        border-bottom-color: #444;
    }
}

/* ---- 打印样式 ---- */
@media print {
    .dna-trace {
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }

    h1, h2, h3 {
        page-break-after: avoid;
    }

    .skill-meta-card {
        page-break-inside: avoid;
    }
}
```

---

## 5. SKILL.md→RST转换脚本

### 5.1 主转换脚本：`skill_md_to_rst.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SKILL.md → Sphinx RST 转换器
DNA追溯码: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-SKILL-CONVERTER-v2.0

功能：
1. 遍历 /app/.user/skills/ 下所有技能目录
2. 解析 SKILL.md 文件
3. 生成结构化的 .rst 文档
4. 提取DNA追溯码并建立索引
5. 生成技能交叉引用映射

用法：
    python skill_md_to_rst.py [--check] [--output-dir ./source/skills]
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# ---- 配置常量 ----
SKILLS_ROOT = Path('/app/.user/skills')
DEFAULT_OUTPUT = Path('./source/skills')
TEMPLATE_DIR = Path('./_templates/skills')

# 38技能完整清单
SKILL_REGISTRY = {
    'longhun-3core-opt': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-3CORE-OPT-v5.2',
        'version': '5.2.0',
        'category': 'p0-core',
        'status': 'running',
        'priority': 'P0',
    },
    'longhun-archive': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-CENTRAL-ARCHIVE-v5.0',
        'version': '5.0.0',
        'category': 'p2-data-tools',
        'status': 'running',
        'priority': 'P2',
    },
    'longhun-asr': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGYIN-ASR-v5.0',
        'version': '5.0.0',
        'category': 'p1-ai-engine',
        'status': 'running',
        'priority': 'P1',
    },
    'longhun-audit': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-AUDIT-v5.1',
        'version': '5.1.0',
        'category': 'p3-audit-security',
        'status': 'running',
        'priority': 'P3',
    },
    'longhun-automation': {
        'dna': None,
        'version': '未声明',
        'category': 'p0-core',
        'status': 'defined',
        'priority': 'P0',
    },
    'longhun-backup': {
        'dna': None,
        'version': '未声明',
        'category': 'p2-data-tools',
        'status': 'defined',
        'priority': 'P2',
    },
    'longhun-behavior-engine': {
        'dna': '#龍芯⚡️丙午·甲午·乙丑·壬午·䷨损-LONGHUN-BEHAVIOR-v1.0',
        'version': '1.0.0',
        'category': 'p1-ai-engine',
        'status': 'running',
        'priority': 'P1',
    },
    'longhun-benchmark': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-BENCHMARK-v5.1',
        'version': '5.1.0',
        'category': 'p0-core',
        'status': 'running',
        'priority': 'P0',
    },
    'longhun-cloud-deploy': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-DEPLOY-v5.0',
        'version': '5.0.0',
        'category': 'p0-core',
        'status': 'running',
        'priority': 'P0',
    },
    'longhun-cloud-kimi': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-KIMI-v5.0',
        'version': '5.0.0',
        'category': 'p1-ai-engine',
        'status': 'running',
        'priority': 'P1',
    },
    'longhun-cloud-mcp': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-MCP-v5.0',
        'version': '5.0.0',
        'category': 'p0-core',
        'status': 'running',
        'priority': 'P0',
    },
    'longhun-cloud-notion': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-NOTION-v5.0',
        'version': '5.0.0',
        'category': 'p2-data-tools',
        'status': 'running',
        'priority': 'P2',
    },
    'longhun-cloud-panel': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-PANEL-v5.0',
        'version': '5.0.0',
        'category': 'p0-core',
        'status': 'running',
        'priority': 'P0',
    },
    'longhun-cn-innovation-kb': {
        'dna': '#龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-CN-INNO-KB-v1.0',
        'version': '1.0.0',
        'category': 'p2-data-tools',
        'status': 'running',
        'priority': 'P2',
    },
    'longhun-cnsh': {
        'dna': None,
        'version': '未声明',
        'category': 'p0-core',
        'status': 'defined',
        'priority': 'P0',
    },
    'longhun-cross-platform': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-CROSS-PLATFORM-v5.3',
        'version': '5.3.0',
        'category': 'p0-core',
        'status': 'running',
        'priority': 'P0',
    },
    'longhun-cs-knowledge-base': {
        'dna': '#龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-CS-KB-v1.5',
        'version': '1.5.0',
        'category': 'p2-data-tools',
        'status': 'running',
        'priority': 'P2',
    },
    'longhun-daemon': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-DAEMON-v5.2',
        'version': '5.2.0',
        'category': 'p0-core',
        'status': 'running',
        'priority': 'P0',
    },
    'longhun-deployment-ready': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-DEPLOY-READY-v5.2',
        'version': '5.2.0',
        'category': 'p0-core',
        'status': 'running',
        'priority': 'P0',
    },
    'longhun-dna-align': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-DNA-ALIGN-v5.2',
        'version': '5.2.0',
        'category': 'p3-audit-security',
        'status': 'running',
        'priority': 'P3',
    },
    'longhun-empower-engine': {
        'dna': '#龍芯⚡️丙午·癸巳·辛卯·甲午·䷚颐-EMPOWER-ENGINE-v1.5',
        'version': '1.5.0',
        'category': 'p1-ai-engine',
        'status': 'running',
        'priority': 'P1',
    },
    'longhun-finance': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-WEB3-DNA-FINANCE-v9.0',
        'version': '9.0.0',
        'category': 'p1-ai-engine',
        'status': 'running',
        'priority': 'P1',
    },
    'longhun-formula-opt': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-FORMULA-OPT-v5.2',
        'version': '5.2.0',
        'category': 'p0-core',
        'status': 'running',
        'priority': 'P0',
    },
    'longhun-governance': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-GOVERNANCE-v5.0',
        'version': '5.0.0',
        'category': 'p3-audit-security',
        'status': 'running',
        'priority': 'P3',
    },
    'longhun-harmonyos': {
        'dna': None,
        'version': '未声明',
        'category': 'p0-core',
        'status': 'defined',
        'priority': 'P0',
    },
    'longhun-integration': {
        'dna': None,
        'version': '未声明',
        'category': 'p0-core',
        'status': 'defined',
        'priority': 'P0',
    },
    'longhun-ios': {
        'dna': None,
        'version': '未声明',
        'category': 'p0-core',
        'status': 'defined',
        'priority': 'P0',
    },
    'longhun-kg-upgrade': {
        'dna': None,
        'version': '未声明',
        'category': 'p2-data-tools',
        'status': 'defined',
        'priority': 'P2',
    },
    'longhun-monitoring': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-MONITORING-v5.0',
        'version': '5.0.0',
        'category': 'p0-core',
        'status': 'running',
        'priority': 'P0',
    },
    'longhun-multicurrency': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-MULTICURRENCY-v5.2',
        'version': '5.2.1',
        'category': 'p2-data-tools',
        'status': 'running',
        'priority': 'P2',
    },
    'longhun-nlp': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGWEN-NLP-v5.0',
        'version': '5.0.0',
        'category': 'p1-ai-engine',
        'status': 'running',
        'priority': 'P1',
    },
    'longhun-notion-portal': {
        'dna': '#龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-NOTION-PORTAL-v2.0',
        'version': '2.0.0',
        'category': 'p2-data-tools',
        'status': 'running',
        'priority': 'P2',
    },
    'longhun-ocr': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGTENG-OCR-v5.0',
        'version': '5.0.0',
        'category': 'p1-ai-engine',
        'status': 'running',
        'priority': 'P1',
    },
    'longhun-review': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-REVIEW-v5.1',
        'version': '5.1.0',
        'category': 'p3-audit-security',
        'status': 'running',
        'priority': 'P3',
    },
    'longhun-riemann': {
        'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-RIEMANN-FRAMEWORK-v5.0',
        'version': '5.0.0',
        'category': 'p1-ai-engine',
        'status': 'defined',
        'priority': 'P1',
    },
    'longhun-system': {
        'dna': None,
        'version': '未声明',
        'category': 'p0-core',
        'status': 'defined',
        'priority': 'P0',
    },
    'longhun-warehouse-audit': {
        'dna': None,
        'version': '未声明',
        'category': 'p3-audit-security',
        'status': 'running',
        'priority': 'P3',
    },
    'longhun-zeng-digital-human': {
        'dna': '#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-ZENG-DIGITAL-HUMAN-v1.0',
        'version': '1.0.0',
        'category': 'p1-ai-engine',
        'status': 'running',
        'priority': 'P1',
    },
}


@dataclass
class SkillMetadata:
    """技能元数据结构"""
    name: str
    display_name: str
    dna_code: Optional[str]
    version: str
    category: str
    status: str
    priority: str
    skill_type: str = ''
    core_functions: List[str] = field(default_factory=list)
    triggers: List[str] = field(default_factory=list)
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    source_path: Optional[Path] = None
    rst_output_path: Optional[Path] = None
    md5_hash: str = ''
    doc_coverage: float = 0.0
    last_updated: str = ''
    migration_status: str = 'pending'  # pending / migrated / failed


class DNAExtractor:
    """DNA追溯码提取器"""

    DNA_PATTERN = re.compile(
        r'#龍[芯根魂星]⚡️\d{4}-\d{2}-\d{2}-[A-Z0-9\-]+-v\d+\.?\d*'
    )

    @classmethod
    def extract(cls, text: str) -> List[str]:
        """从文本中提取所有DNA追溯码"""
        return cls.DNA_PATTERN.findall(text)

    @classmethod
    def validate(cls, dna_code: str) -> bool:
        """验证DNA追溯码格式"""
        return bool(cls.DNA_PATTERN.fullmatch(dna_code))

    @classmethod
    def parse(cls, dna_code: str) -> Dict[str, str]:
        """解析DNA追溯码组成"""
        # 格式: #龍芯⚡️YYYY-MM-DD-NAME-vX.Y
        parts = dna_code.replace('#', '').replace('⚡️', '-').split('-')
        return {
            'prefix': parts[0],
            'date': '-'.join(parts[1:4]),
            'name': '-'.join(parts[4:-1]),
            'version': parts[-1],
        }


class MarkdownParser:
    """SKILL.md Markdown解析器"""

    # Markdown标题正则
    HEADER_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    # 代码块正则
    CODEBLOCK_PATTERN = re.compile(r'```(\w+)?\n(.*?)```', re.DOTALL)
    # 表格正则
    TABLE_PATTERN = re.compile(r'\|(.+)\|\n\|[-\s|:]+\|\n((?:\|.+\|\n)*)')
    # 强调文本
    BOLD_PATTERN = re.compile(r'\*\*(.+?)\*\*')
    ITALIC_PATTERN = re.compile(r'\*(.+?)\*')
    # 列表项
    LIST_ITEM_PATTERN = re.compile(r'^(\s*)[-*+]\s+(.+)$', re.MULTILINE)
    # 编号列表
    ORDERED_LIST_PATTERN = re.compile(r'^(\s*)\d+\.\s+(.+)$', re.MULTILINE)

    def __init__(self, content: str):
        self.content = content
        self.sections: List[Dict] = []

    def parse_structure(self) -> List[Dict]:
        """解析文档结构为层级节"""
        headers = self.HEADER_PATTERN.findall(self.content)
        sections = []
        for level_md, title in headers:
            level = len(level_md)
            sections.append({
                'level': level,
                'title': title.strip(),
                'ref': self._make_ref(title),
            })
        self.sections = sections
        return sections

    def _make_ref(self, title: str) -> str:
        """生成RST引用标签"""
        return re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '-').lower()[:50]

    def get_section_content(self, section_title: str) -> str:
        """获取指定节的内容"""
        pattern = re.compile(
            rf'#+\s+{re.escape(section_title)}\s*\n(.*?)(?=\n#+\s|\Z)',
            re.DOTALL
        )
        match = pattern.search(self.content)
        return match.group(1).strip() if match else ''

    def extract_tables(self) -> List[List[List[str]]]:
        """提取所有Markdown表格"""
        tables = []
        for match in self.TABLE_PATTERN.finditer(self.content):
            header_row = [c.strip() for c in match.group(1).split('|') if c.strip()]
            body_rows = []
            for line in match.group(2).strip().split('\n'):
                cells = [c.strip() for c in line.split('|') if c.strip()]
                if cells:
                    body_rows.append(cells)
            tables.append([header_row] + body_rows)
        return tables

    def extract_code_blocks(self) -> List[Dict[str, str]]:
        """提取所有代码块"""
        blocks = []
        for match in self.CODEBLOCK_PATTERN.finditer(self.content):
            blocks.append({
                'language': match.group(1) or '',
                'code': match.group(2).strip(),
            })
        return blocks


class RSTGenerator:
    """RST文档生成器"""

    def __init__(self, skill_meta: SkillMetadata):
        self.meta = skill_meta
        self.lines: List[str] = []

    def generate(self, md_parser: Optional[MarkdownParser] = None) -> str:
        """生成完整RST文档"""
        self._generate_header()
        self._generate_metadata()
        self._generate_dna_section()
        self._generate_toc()

        if md_parser:
            self._generate_from_md(md_parser)
        else:
            self._generate_placeholder()

        self._generate_audit_section()
        self._generate_see_also()

        return '\n'.join(self.lines)

    def _generate_header(self):
        """生成文档头部（含标签）"""
        ref_label = f".. _skill-{self.meta.name}:"
        title_char = '='
        title_line = self.meta.display_name

        self.lines.extend([
            ref_label,
            '',
            title_line,
            title_char * len(title_line) * 2,
            '',
        ])

    def _generate_metadata(self):
        """生成技能元数据卡片"""
        status_class = 'running' if self.meta.status == 'running' else 'defined'
        priority_class = f"priority-{self.meta.priority.lower()}"

        self.lines.extend([
            '.. container:: skill-meta-card',
            '',
            f'   +------------------+--------------------------------------------------+',
            f'   | 技能名称         | {self.meta.display_name:<48} |',
            f'   +------------------+--------------------------------------------------+',
            f'   | DNA追溯码        | {self.meta.dna_code or "**未分配**":<48} |',
            f'   +------------------+--------------------------------------------------+',
            f'   | 版本号           | {self.meta.version:<48} |',
            f'   +------------------+--------------------------------------------------+',
            f'   | 优先级           | :class:`{self.meta.priority}` {self.meta.priority:<36} |',
            f'   +------------------+--------------------------------------------------+',
            f'   | 状态             | {self.meta.status:<48} |',
            f'   +------------------+--------------------------------------------------+',
            f'   | 分类             | {self.meta.category:<48} |',
            f'   +------------------+--------------------------------------------------+',
            f'   | 技能类型         | {self.meta.skill_type or "-":<48} |',
            f'   +------------------+--------------------------------------------------+',
            '',
        ])

    def _generate_dna_section(self):
        """生成DNA追溯节"""
        self.lines.extend([
            'DNA追溯',
            '-------',
            '',
        ])
        if self.meta.dna_code:
            self.lines.extend([
                f'.. dna-trace:: {self.meta.dna_code}',
                '',
                f'   DNA状态: :audit-green:`已注册`',
                '',
            ])
        else:
            self.lines.extend([
                '.. dna-trace:: 未分配',
                '',
                '   DNA状态: :audit-red:`缺失 - 需要分配DNA追溯码`',
                '',
                '   .. todo::',
                f'      为 ``{self.meta.name}`` 分配DNA追溯码',
                '',
            ])

    def _generate_toc(self):
        """生成本地目录"""
        self.lines.extend([
            '.. contents:: 目录',
            '   :local:',
            '   :depth: 2',
            '',
        ])

    def _generate_from_md(self, md_parser: MarkdownParser):
        """从Markdown解析结果生成内容"""
        sections = md_parser.parse_structure()

        for section in sections:
            if section['level'] == 1:
                underline = '='
            elif section['level'] == 2:
                underline = '-'
            elif section['level'] == 3:
                underline = '~'
            else:
                underline = '^'

            title = section['title']
            # 转换Markdown粗体
            title = re.sub(r'\*\*(.+?)\*\*', r'**\1**', title)

            self.lines.extend([
                f'.. _{section["ref"]}:',
                '',
                title,
                underline * len(title) * 2,
                '',
            ])

            # 获取节内容并转换
            content = md_parser.get_section_content(title)
            if content:
                rst_content = self._convert_md_to_rst(content)
                self.lines.append(rst_content)
                self.lines.append('')

    def _convert_md_to_rst(self, md_content: str) -> str:
        """将Markdown内容转换为RST"""
        lines = md_content.split('\n')
        rst_lines = []
        in_code_block = False
        code_buffer = []
        code_lang = ''

        for line in lines:
            stripped = line.strip()

            # 代码块处理
            if stripped.startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_lang = stripped[3:].strip() or 'text'
                    code_buffer = []
                else:
                    in_code_block = False
                    rst_lines.append(f'')
                    rst_lines.append(f'.. code-block:: {code_lang}')
                    rst_lines.append('')
                    for cb_line in code_buffer:
                        rst_lines.append(f'   {cb_line}')
                    rst_lines.append('')
                continue

            if in_code_block:
                code_buffer.append(line)
                continue

            # 普通文本转换
            # 粗体
            line = re.sub(r'\*\*(.+?)\*\*', r'**\1**', line)
            # 斜体
            line = re.sub(r'\*(.+?)\*', r'\*\1\*', line)
            # 行内代码
            line = re.sub(r'`([^`]+?)`', r'``\1``', line)

            rst_lines.append(line)

        return '\n'.join(rst_lines)

    def _generate_placeholder(self):
        """生成占位内容（无SKILL.md时）"""
        self.lines.extend([
            '概述',
            '====',
            '',
            f'.. warning::',
            f'   技能 ``{self.meta.name}`` 的详细文档尚未从SKILL.md迁移。',
            '',
            f'   - 预期SKILL.md路径: ``/app/.user/skills/{self.meta.name}/SKILL.md``',
            f'   - 当前状态: **{self.meta.status}**',
            '',
            '.. todo::',
            f'   迁移 ``{self.meta.name}`` 的SKILL.md文档',
            '',
        ])

    def _generate_audit_section(self):
        """生成审计节"""
        self.lines.extend([
            '文档审计',
            '========',
            '',
            '.. container:: audit-section',
            '',
            f'   :审计日期: {datetime.now().strftime("%Y-%m-%d")}',
            f'   :文档覆盖率: {self.meta.doc_coverage:.1f}%',
            f'   :迁移状态: {self.meta.migration_status}',
            '',
        ])

    def _generate_see_also(self):
        """生成参见节"""
        self.lines.extend([
            '参见',
            '====',
            '',
            '- :ref:`skills-index` - 技能总索引',
            '- :ref:`architecture-overview` - 系统架构总览',
            f'- Notion页面: https://www.notion.so/longhun/{self.meta.name}',
            '',
        ])


class SkillConverter:
    """主转换协调器"""

    def __init__(self, output_dir: Path = DEFAULT_OUTPUT):
        self.output_dir = output_dir
        self.results: List[Dict] = []
        self.dna_index: Dict[str, Dict] = {}

    def convert_all(self) -> List[Dict]:
        """转换所有技能"""
        print("=" * 60)
        print("龍魂技能文档转换器")
        print("DNA追溯码: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-SKILL-CONVERTER-v2.0")
        print("=" * 60)

        for skill_name, registry_info in SKILL_REGISTRY.items():
            result = self._convert_skill(skill_name, registry_info)
            self.results.append(result)

        self._generate_indices()
        self._generate_dna_index()
        self._write_migration_report()

        return self.results

    def _convert_skill(self, skill_name: str, registry_info: Dict) -> Dict:
        """转换单个技能"""
        print(f"\n[处理] {skill_name} ...")

        skill_dir = SKILLS_ROOT / skill_name
        skill_md = skill_dir / 'SKILL.md'

        # 构建元数据
        meta = SkillMetadata(
            name=skill_name,
            display_name=skill_name.replace('longhun-', '').replace('-', ' ').title(),
            dna_code=registry_info.get('dna'),
            version=registry_info.get('version', '未声明'),
            category=registry_info.get('category', 'unknown'),
            status=registry_info.get('status', 'unknown'),
            priority=registry_info.get('priority', 'P3'),
            source_path=skill_md if skill_md.exists() else None,
        )

        # 读取SKILL.md
        md_parser = None
        if skill_md.exists():
            content = skill_md.read_text(encoding='utf-8')
            meta.md5_hash = hashlib.md5(content.encode()).hexdigest()

            # 提取DNA
            dna_codes = DNAExtractor.extract(content)
            if dna_codes and not meta.dna_code:
                meta.dna_code = dna_codes[0]

            # 提取核心功能
            meta.core_functions = self._extract_functions(content)

            # 计算文档覆盖率
            meta.doc_coverage = self._calc_coverage(content)

            meta.migration_status = 'migrated'
            md_parser = MarkdownParser(content)
        else:
            meta.migration_status = 'missing_source'
            print(f"  [警告] SKILL.md 不存在: {skill_md}")

        # 确定输出路径
        category_dir = self.output_dir / meta.category.replace('p0-', 'p0-').replace('p1-', 'p1-').replace('p2-', 'p2-').replace('p3-', 'p3-')
        category_dir.mkdir(parents=True, exist_ok=True)
        rst_path = category_dir / f'{skill_name}.rst'
        meta.rst_output_path = rst_path

        # 生成RST
        generator = RSTGenerator(meta)
        rst_content = generator.generate(md_parser)
        rst_path.write_text(rst_content, encoding='utf-8')

        # 更新DNA索引
        if meta.dna_code:
            self.dna_index[meta.dna_code] = {
                'skill': skill_name,
                'version': meta.version,
                'rst_path': str(rst_path),
                'md5': meta.md5_hash,
            }

        status_icon = 'OK' if meta.migration_status == 'migrated' else 'MISSING'
        print(f"  [{status_icon}] -> {rst_path}")

        return asdict(meta)

    def _extract_functions(self, content: str) -> List[str]:
        """从内容中提取核心功能列表"""
        functions = []
        # 匹配功能列表
        func_patterns = [
            re.compile(r'[-*]\s+(.+?)(?:\n|$)', re.MULTILINE),
        ]
        for pattern in func_patterns:
            for match in pattern.finditer(content):
                func = match.group(1).strip()
                if len(func) > 5 and len(func) < 100:
                    functions.append(func)
        return functions[:20]  # 最多20条

    def _calc_coverage(self, content: str) -> float:
        """计算文档覆盖率（简单启发式）"""
        score = 0.0
        checks = [
            (r'#\s*描述', 20),
            (r'#\s*(?:输入|Input)', 15),
            (r'#\s*(?:输出|Output)', 15),
            (r'#\s*(?:触发|Trigger)', 10),
            (r'```', 10),
            (r'\|.*\|.*\|', 10),  # 表格
            (r'#\s*(?:示例|Example)', 10),
            (r'#\s*(?:依赖|Dependency)', 10),
        ]
        for pattern, weight in checks:
            if re.search(pattern, content, re.IGNORECASE):
                score += weight
        return min(score, 100.0)

    def _generate_indices(self):
        """生成分类索引文件"""
        categories = {
            'p0-core': ('P0-核心架构', '系统基础设施与核心性能模块'),
            'p1-ai-engine': ('P1-AI引擎', '智能处理与算法引擎模块'),
            'p2-data-tools': ('P2-数据工具', '数据管理与外部集成模块'),
            'p3-audit-security': ('P3-审计安全', '审计追踪与安全治理模块'),
        }

        for cat_dir, (cat_title, cat_desc) in categories.items():
            cat_path = self.output_dir / cat_dir
            if not cat_path.exists():
                continue

            rst_files = sorted(cat_path.glob('longhun-*.rst'))
            if not rst_files:
                continue

            index_content = self._render_category_index(
                cat_title, cat_desc, rst_files
            )
            index_path = cat_path / 'index.rst'
            index_path.write_text(index_content, encoding='utf-8')
            print(f"  [索引] {index_path}")

        # 生成技能总索引
        self._generate_master_skill_index()

    def _render_category_index(self, title: str, desc: str, rst_files: List[Path]) -> str:
        """渲染分类索引"""
        lines = [
            f'.. _skills-{title.lower().replace(" ", "-")}:',
            '',
            title,
            '=' * len(title) * 2,
            '',
            desc,
            '',
            '.. toctree::',
            '   :maxdepth: 1',
            '   :caption: 技能列表',
            '',
        ]
        for f in rst_files:
            lines.append(f'   {f.stem}')
        lines.extend(['', f'共 {len(rst_files)} 个技能模块。', ''])
        return '\n'.join(lines)

    def _generate_master_skill_index(self):
        """生成技能总索引"""
        lines = [
            '.. _skills-index:',
            '',
            '龍魂技能总索引',
            '==============',
            '',
            '龍魂系统v5.0共包含 **38个技能模块**，按优先级分为4大类：',
            '',
            '.. list-table:: 技能统计',
            '   :header-rows: 1',
            '   :widths: 15 15 15 55',
            '',
            '   * - 优先级',
            '     - 数量',
            '     - 状态',
            '     - 说明',
            '   * - P0-核心架构',
            '     - 12',
            '     - :audit-green:`关键`',
            '     - 系统基础设施、性能核心、部署运维',
            '   * - P1-AI引擎',
            '     - 11',
            '     - :audit-yellow:`重要`',
            '     - 智能处理、算法模块、模型集成',
            '   * - P2-数据工具',
            '     - 10',
            '     - :audit-yellow:`重要`',
            '     - 数据管理、知识库、外部集成',
            '   * - P3-审计安全',
            '     - 5',
            '     - :audit-green:`关键`',
            '     - 审计追踪、安全治理、合规检查',
            '',
            '.. toctree::',
            '   :maxdepth: 2',
            '   :caption: 技能分类',
            '',
            '   p0-core/index',
            '   p1-ai-engine/index',
            '   p2-data-tools/index',
            '   p3-audit-security/index',
            '',
        ]

        # 添加38技能完整表格
        lines.extend([
            '38技能完整清单',
            '-------------',
            '',
            '.. list-table:: 全部技能模块',
            '   :header-rows: 1',
            '   :widths: 5 25 35 10 15 10',
            '',
            '   * - #',
            '     - 技能名称',
            '     - DNA追溯码',
            '     - 版本',
            '     - 类型',
            '     - 状态',
        ])

        for i, (skill_name, info) in enumerate(SKILL_REGISTRY.items(), 1):
            dna_display = info.get('dna') or '**未分配**'
            version = info.get('version', '-')
            status_badge = '已运行' if info.get('status') == 'running' else '已定义'
            lines.append(f'   * - {i}')
            lines.append(f'     - :ref:`skill-{skill_name}`')
            lines.append(f'     - `{dna_display}`')
            lines.append(f'     - {version}')
            lines.append(f'     - {info.get("category", "-")}')
            lines.append(f'     - {status_badge}')

        lines.extend(['', f'**最后更新**: {datetime.now().strftime("%Y-%m-%d")}', ''])

        index_path = self.output_dir / 'index.rst'
        index_path.write_text('\n'.join(lines), encoding='utf-8')
        print(f"  [总索引] {index_path}")

    def _generate_dna_index(self):
        """生成DNA追溯码索引"""
        dna_index_path = self.output_dir / '_dna_index.rst'

        lines = [
            '.. _dna-index:',
            '',
            'DNA追溯码索引',
            '=============',
            '',
            f'共 **{len(self.dna_index)}** 个已注册DNA追溯码（总计38技能，缺失{38 - len(self.dna_index)}个）。',
            '',
            '.. list-table:: DNA追溯码完整索引',
            '   :header-rows: 1',
            '   :widths: 10 40 15 15 20',
            '',
            '   * - 序号',
            '     - DNA追溯码',
            '     - 技能',
            '     - 版本',
            '     - RST文档',
        ]

        for idx, (dna, info) in enumerate(sorted(self.dna_index.items()), 1):
            skill_name = info['skill']
            version = info['version']
            rst_link = f':doc:`{skill_name} <{info["rst_path"]>`'
            lines.extend([
                f'   * - {idx}',
                f'     - .. dna-trace:: {dna}',
                f'     - {skill_name}',
                f'     - {version}',
                f'     - {rst_link}',
            ])

        # 缺失DNA的技能
        missing_dna = [
            name for name, info in SKILL_REGISTRY.items()
            if not info.get('dna')
        ]
        if missing_dna:
            lines.extend([
                '',
                '.. admonition:: DNA缺失警告',
                '   :class: warning',
                '',
                f'   以下 **{len(missing_dna)}** 个技能尚未分配DNA追溯码：',
                '',
            ])
            for name in missing_dna:
                lines.append(f'   - ``{name}``')
            lines.append('')

        dna_index_path.write_text('\n'.join(lines), encoding='utf-8')
        print(f"  [DNA索引] {dna_index_path}")

    def _write_migration_report(self):
        """输出迁移报告"""
        total = len(self.results)
        migrated = sum(1 for r in self.results if r['migration_status'] == 'migrated')
        failed = sum(1 for r in self.results if r['migration_status'] == 'failed')
        missing = total - migrated - failed

        report = {
            'generated_at': datetime.now().isoformat(),
            'total_skills': total,
            'migrated': migrated,
            'failed': failed,
            'missing_source': missing,
            'dna_tracked': len(self.dna_index),
            'dna_missing': 38 - len(self.dna_index),
            'results': self.results,
        }

        report_path = self.output_dir / '_migration_report.json'
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"\n  [报告] {report_path}")

        # 打印摘要
        print("\n" + "=" * 60)
        print("迁移摘要")
        print("=" * 60)
        print(f"  总技能数:   {total}")
        print(f"  成功迁移:   {migrated} ({migrated/total*100:.1f}%)")
        print(f"  源文件缺失: {missing}")
        print(f"  失败:       {failed}")
        print(f"  DNA追踪:    {len(self.dna_index)}/38")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description='SKILL.md → RST 转换器')
    parser.add_argument('--output-dir', type=Path, default=DEFAULT_OUTPUT,
                        help='RST输出目录')
    parser.add_argument('--check', action='store_true',
                        help='仅检查，不生成文件')
    parser.add_argument('--skill', type=str, default=None,
                        help='仅转换指定技能')
    args = parser.parse_args()

    converter = SkillConverter(args.output_dir)

    if args.skill:
        if args.skill in SKILL_REGISTRY:
            converter._convert_skill(args.skill, SKILL_REGISTRY[args.skill])
        else:
            print(f"错误: 未知技能 '{args.skill}'")
            sys.exit(1)
    else:
        converter.convert_all()


if __name__ == '__main__':
    main()
```

### 5.2 requirements.txt（文档构建依赖）

```
# =============================================
# 龍魂系统文档构建依赖
# DNA追溯码: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-DOCS-DEPS-v1.0
# =============================================

# --- Sphinx核心 ---
sphinx>=7.0,<8.0

# --- HTML主题 ---
furo>=2023.9.10
sphinx-rtd-theme>=1.3.0

# --- Markdown支持 ---
myst-parser>=2.0.0

# --- 中文搜索 ---
sphinx-search-zh>=0.1.0
jieba>=0.42.1

# --- 文档扩展 ---
sphinxcontrib-httpdomain>=1.8.1
sphinxcontrib-plantuml>=0.27
sphinx-autodoc-typehints>=1.25.0

# --- API文档 ---
sphinxcontrib-openapi>=0.8.0

# --- 版本管理 ---
sphinx-multiversion>=0.2.4

# --- 构建工具 ---
sphinx-intl>=2.1.0

# --- 代码高亮 ---
Pygments>=2.16.0

# --- 可选：实时重载 ---
sphinx-autobuild>=2021.3.14

# --- 可选：拼写检查 ---
sphinxcontrib-spelling>=8.0.0

# --- 可选：链接检查增强 ---
requests>=2.31.0

# --- 龍魂自定义扩展依赖 ---
pyyaml>=6.0
```

---

## 6. 38技能迁移检查清单

### 6.1 完整检查清单

| # | 技能名称 | 优先级 | DNA追溯码 | SKILL.md存在 | RST生成 | 元数据完整 | 代码示例 | 交叉引用 | 审计通过 | 状态 |
|---|---------|--------|-----------|-------------|---------|-----------|---------|---------|---------|------|
| 1 | longhun-3core-opt | **P0** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-3CORE-OPT-v5.2 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 2 | longhun-archive | **P2** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-CENTRAL-ARCHIVE-v5.0 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 3 | longhun-asr | **P1** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGYIN-ASR-v5.0 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 4 | longhun-audit | **P3** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-AUDIT-v5.1 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 5 | longhun-automation | **P0** | **缺失** | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待创建 |
| 6 | longhun-backup | **P2** | **缺失** | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待创建 |
| 7 | longhun-behavior-engine | **P1** | #龍芯⚡️丙午·甲午·乙丑·壬午·䷨损-LONGHUN-BEHAVIOR-v1.0 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 8 | longhun-benchmark | **P0** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-BENCHMARK-v5.1 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 9 | longhun-cloud-deploy | **P0** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-DEPLOY-v5.0 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 10 | longhun-cloud-kimi | **P1** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-KIMI-v5.0 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 11 | longhun-cloud-mcp | **P0** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-MCP-v5.0 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 12 | longhun-cloud-notion | **P2** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-NOTION-v5.0 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 13 | longhun-cloud-panel | **P0** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-PANEL-v5.0 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 14 | longhun-cn-innovation-kb | **P2** | #龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-CN-INNO-KB-v1.0 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 15 | longhun-cnsh | **P0** | **缺失** | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待创建 |
| 16 | longhun-cross-platform | **P0** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-CROSS-PLATFORM-v5.3 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 17 | longhun-cs-knowledge-base | **P2** | #龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-CS-KB-v1.5 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 18 | longhun-daemon | **P0** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-DAEMON-v5.2 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 19 | longhun-deployment-ready | **P0** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-DEPLOY-READY-v5.2 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 20 | longhun-dna-align | **P3** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-DNA-ALIGN-v5.2 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 21 | longhun-empower-engine | **P1** | #龍芯⚡️丙午·癸巳·辛卯·甲午·䷚颐-EMPOWER-ENGINE-v1.5 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 22 | longhun-finance | **P1** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-WEB3-DNA-FINANCE-v9.0 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 23 | longhun-formula-opt | **P0** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-FORMULA-OPT-v5.2 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 24 | longhun-governance | **P3** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-GOVERNANCE-v5.0 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 25 | longhun-harmonyos | **P0** | **缺失** | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待创建 |
| 26 | longhun-integration | **P0** | **缺失** | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待创建 |
| 27 | longhun-ios | **P0** | **缺失** | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待创建 |
| 28 | longhun-kg-upgrade | **P2** | **缺失** | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待创建 |
| 29 | longhun-monitoring | **P0** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-MONITORING-v5.0 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 30 | longhun-multicurrency | **P2** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-MULTICURRENCY-v5.2 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 31 | longhun-nlp | **P1** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGWEN-NLP-v5.0 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 32 | longhun-notion-portal | **P2** | #龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-NOTION-PORTAL-v2.0 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 33 | longhun-ocr | **P1** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGTENG-OCR-v5.0 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 34 | longhun-review | **P3** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-REVIEW-v5.1 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 35 | longhun-riemann | **P1** | #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-RIEMANN-FRAMEWORK-v5.0 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |
| 36 | longhun-system | **P0** | **缺失** | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待创建 |
| 37 | longhun-warehouse-audit | **P3** | **缺失** | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待创建 |
| 38 | longhun-zeng-digital-human | **P1** | #龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-ZENG-DIGITAL-HUMAN-v1.0 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 待迁移 |

### 6.2 检查项说明

| 检查项 | 说明 | 权重 |
|--------|------|------|
| SKILL.md存在 | 源文件 `/app/.user/skills/{name}/SKILL.md` 存在且非空 | 必需 |
| RST生成 | 转换脚本成功生成 `.rst` 文件 | 必需 |
| 元数据完整 | DNA追溯码、版本号、技能类型均已填写 | 20% |
| 代码示例 | 包含至少1个可运行的代码示例 | 20% |
| 交叉引用 | 正确链接到相关技能/架构文档 | 15% |
| 审计通过 | 三色审计标注完整，无红色项 | 25% |

### 6.3 迁移优先级矩阵

```
批次1（第1-2周）- P0核心架构 × 12:
├── longhun-system          [依赖其他所有模块]
├── longhun-3core-opt       [性能核心]
├── longhun-daemon          [服务启动]
├── longhun-cloud-panel     [API网关]
├── longhun-cloud-deploy    [部署引擎]
├── longhun-deployment-ready[部署检查]
├── longhun-formula-opt     [公式优化]
├── longhun-benchmark       [基准测试]
├── longhun-automation      [自动化]
├── longhun-cross-platform  [跨平台]
├── longhun-cloud-mcp       [MCP协议]
├── longhun-monitoring      [监控体系]
├── longhun-harmonyos       [鸿蒙适配]
├── longhun-ios             [iOS适配]
├── longhun-integration     [系统集成]
└── longhun-cnsh            [编程规范]

批次2（第3-4周）- P1 AI引擎 × 11:
├── longhun-asr             [语音识别]
├── longhun-nlp             [自然语言处理]
├── longhun-ocr             [图像识别]
├── longhun-finance         [交易系统]
├── longhun-empower-engine  [赋能引擎]
├── longhun-behavior-engine [行为引擎]
├── longhun-cloud-kimi      [Kimi集成]
├── longhun-zeng-digital-human [数字人]
├── longhun-riemann         [数学框架]
└── + 2个P2技能穿插

批次3（第5周）- P2数据工具 × 10:
├── longhun-archive         [藏经阁]
├── longhun-backup          [备份]
├── longhun-cloud-notion    [Notion同步]
├── longhun-cn-innovation-kb [创新知识库]
├── longhun-cs-knowledge-base [CS知识库]
├── longhun-kg-upgrade      [知识图谱]
├── longhun-multicurrency   [多币种]
├── longhun-notion-portal   [Notion入口]
└── + 1个P3技能穿插

批次4（第6周）- P3审计安全 × 5:
├── longhun-audit           [审计系统]
├── longhun-dna-align       [DNA对齐]
├── longhun-governance      [治理框架]
├── longhun-review          [每日复盘]
└── longhun-warehouse-audit [仓储审计]
```

---

## 7. CI/CD配置

### 7.1 GitHub Actions工作流

```yaml
# .github/workflows/docs-build.yml
# =============================================
# 龍魂文档自动构建工作流
# DNA追溯码: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-DOCS-CI-v1.0
# =============================================

name: 龍魂文档构建与部署

on:
  push:
    branches: [main, develop, 'release/*']
    paths:
      - 'docs/**'
      - 'src/**'
      - '.github/workflows/docs-build.yml'
  pull_request:
    branches: [main]
    paths:
      - 'docs/**'
  schedule:
    # 每日凌晨3点自动构建（确保文档时效性）
    - cron: '0 18 * * *'
  workflow_dispatch:
    inputs:
      build_version:
        description: '构建版本标签（可选）'
        required: false
        default: ''

env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '18'

jobs:
  # ---- 质量门禁 ----
  quality-gate:
    name: 文档质量门禁
    runs-on: ubuntu-latest
    steps:
      - name: 检出代码
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: 设置Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: 缓存pip依赖
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('docs/requirements.txt') }}

      - name: 安装依赖
        run: |
          cd docs
          pip install -r requirements.txt

      - name: SKILL.md转换检查
        run: |
          cd docs
          python source/_scripts/skill_md_to_rst.py --output-dir source/skills

      - name: 版本一致性检查
        run: |
          cd docs
          python source/_scripts/version_checker.py

      - name: DNA追溯码索引生成
        run: |
          cd docs
          python source/_scripts/dna_index_generator.py --check

      - name: 文档质量检查
        run: |
          cd docs
          python source/_scripts/quality_gate.py --fail-on-warning

      - name: 链接检查
        run: |
          cd docs
          make linkcheck SPHINXOPTS="-W --keep-going"
        continue-on-error: true

  # ---- 构建文档 ----
  build-docs:
    name: 构建Sphinx文档
    runs-on: ubuntu-latest
    needs: quality-gate
    strategy:
      matrix:
        format: [html, latex]
    steps:
      - name: 检出代码
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: 设置Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: 缓存pip依赖
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('docs/requirements.txt') }}

      - name: 安装依赖
        run: |
          cd docs
          pip install -r requirements.txt

      - name: 执行转换脚本
        run: |
          cd docs
          python source/_scripts/skill_md_to_rst.py --output-dir source/skills

      - name: 构建 ${{ matrix.format }}
        run: |
          cd docs
          make ${{ matrix.format }} SPHINXOPTS="-W"

      - name: 上传构建产物
        uses: actions/upload-artifact@v4
        with:
          name: docs-${{ matrix.format }}
          path: docs/build/${{ matrix.format }}/
          retention-days: 30

  # ---- 部署预览（PR） ----
  deploy-preview:
    name: PR预览部署
    runs-on: ubuntu-latest
    needs: build-docs
    if: github.event_name == 'pull_request'
    permissions:
      pull-requests: write
    steps:
      - name: 下载构建产物
        uses: actions/download-artifact@v4
        with:
          name: docs-html
          path: docs/build/html

      - name: 部署到Netlify预览
        uses: nwtgck/actions-netlify@v3.0
        with:
          publish-dir: ./docs/build/html
          github-token: ${{ secrets.GITHUB_TOKEN }}
          deploy-message: "PR ${{ github.event.pull_request.number }} 预览"
          alias: deploy-preview-${{ github.event.pull_request.number }}
          fails-without-credentials: false
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}

  # ---- 部署生产环境 ----
  deploy-production:
    name: 生产环境部署
    runs-on: ubuntu-latest
    needs: build-docs
    if: github.ref == 'refs/heads/main'
    steps:
      - name: 下载构建产物
        uses: actions/download-artifact@v4
        with:
          name: docs-html
          path: docs/build/html

      - name: 部署到GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/build/html
          cname: docs.longhun.system
          force_orphan: true

      - name: 触发Read the Docs构建
        run: |
          curl -X POST \
            -H "Authorization: Token ${{ secrets.RTD_API_TOKEN }}" \
            https://readthedocs.org/api/v3/projects/longhun-system/versions/latest/builds/
        continue-on-error: true

  # ---- 多版本构建 ----
  build-versions:
    name: 多版本文档构建
    runs-on: ubuntu-latest
    needs: quality-gate
    if: startsWith(github.ref, 'refs/heads/release/')
    steps:
      - name: 检出代码
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: 设置Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: 安装依赖
        run: |
          cd docs
          pip install -r requirements.txt
          pip install sphinx-multiversion

      - name: 获取版本号
        id: version
        run: |
          VERSION=${GITHUB_REF#refs/heads/release/}
          echo "version=$VERSION" >> $GITHUB_OUTPUT

      - name: 构建多版本文档
        run: |
          cd docs
          sphinx-multiversion source build/multi

      - name: 上传多版本产物
        uses: actions/upload-artifact@v4
        with:
          name: docs-multiversion-${{ steps.version.outputs.version }}
          path: docs/build/multi/
          retention-days: 90

  # ---- 通知 ----
  notify:
    name: 构建通知
    runs-on: ubuntu-latest
    needs: [build-docs, deploy-production]
    if: always()
    steps:
      - name: 构建状态通知
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          channel: '#docs-builds'
          fields: repo,message,commit,author,action,eventName,ref
          text: |
            龍魂文档构建 ${{ job.status == 'success' && '成功 ✅' || '失败 ❌' }}
            提交: ${{ github.event.head_commit.message }}
            作者: ${{ github.event.head_commit.author.name }}
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        continue-on-error: true
```

### 7.2 Read the Docs配置

```yaml
# .readthedocs.yaml
# =============================================
# Read the Docs 部署配置
# DNA追溯码: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-RTD-CONFIG-v1.0
# =============================================

version: 2

# 构建配置
build:
  os: ubuntu-22.04
  tools:
    python: "3.11"
  apt_packages:
    - graphviz
    - plantuml
    - fonts-noto-cjk
  jobs:
    pre_build:
      # 执行SKILL.md转换
      - cd docs && python source/_scripts/skill_md_to_rst.py --output-dir source/skills
      # 生成DNA索引
      - cd docs && python source/_scripts/dna_index_generator.py

# Python依赖
python:
  install:
    - requirements: docs/requirements.txt

# Sphinx配置
sphinx:
  configuration: docs/source/conf.py
  fail_on_warning: true

# 构建格式
formats:
  - htmlzip
  - pdf
  - epub

# 搜索配置
search:
  ranking:
    api/*: -5
    architecture/*: 3
    skills/*: 5
    guides/installation: 10
  ignore:
    - _scripts/*
    - _ext/*

# 子模块
submodules:
  include: all

# 并发构建
build:
  jobs: 4
```

---

## 8. 自动化质量检查脚本

### 8.1 质量门禁脚本：`quality_gate.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档质量门禁脚本
DNA追溯码: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-QUALITY-GATE-v1.0

检查项：
1. 文档覆盖率 ≥ 70%
2. DNA追溯码完整性 ≥ 80%（29/38）
3. 代码示例存在性 ≥ 60%
4. 交叉引用完整性 ≥ 50%
5. 无死链（内部引用）
6. 格式一致性
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class QualityReport:
    """质量报告"""
    total_skills: int = 38
    doc_coverage_avg: float = 0.0
    dna_completeness: float = 0.0
    code_example_ratio: float = 0.0
    cross_ref_ratio: float = 0.0
    dead_links: List[str] = field(default_factory=list)
    format_issues: List[str] = field(default_factory=list)
    passed: bool = False
    score: float = 0.0

    def to_dict(self) -> dict:
        return {
            'total_skills': self.total_skills,
            'doc_coverage_avg': round(self.doc_coverage_avg, 2),
            'dna_completeness': round(self.dna_completeness, 2),
            'code_example_ratio': round(self.code_example_ratio, 2),
            'cross_ref_ratio': round(self.cross_ref_ratio, 2),
            'dead_links_count': len(self.dead_links),
            'format_issues_count': len(self.format_issues),
            'score': round(self.score, 2),
            'passed': self.passed,
        }


class QualityGate:
    """质量门禁检查器"""

    # 阈值配置
    THRESHOLDS = {
        'doc_coverage': 70.0,       # 文档覆盖率 %
        'dna_completeness': 80.0,    # DNA完整性 %
        'code_examples': 60.0,       # 代码示例比例 %
        'cross_refs': 50.0,          # 交叉引用比例 %
        'max_dead_links': 5,         # 最大允许死链数
        'max_format_issues': 10,     # 最大格式问题数
    }

    def __init__(self, docs_dir: Path = Path('./source')):
        self.docs_dir = docs_dir
        self.skills_dir = docs_dir / 'skills'
        self.report = QualityReport()

    def run_all_checks(self) -> QualityReport:
        """执行所有检查"""
        print("=" * 60)
        print("龍魂文档质量门禁")
        print("=" * 60)

        self._check_doc_coverage()
        self._check_dna_completeness()
        self._check_code_examples()
        self._check_cross_references()
        self._check_dead_links()
        self._check_format_consistency()

        self._calculate_score()
        self._evaluate_pass()

        return self.report

    def _check_doc_coverage(self):
        """检查文档覆盖率"""
        print("\n[检查1] 文档覆盖率...")

        skill_files = list(self.skills_dir.rglob('longhun-*.rst'))
        if not skill_files:
            self.report.doc_coverage_avg = 0.0
            print("  警告: 未找到技能RST文件")
            return

        total_coverage = 0.0
        for f in skill_files:
            content = f.read_text(encoding='utf-8')
            # 计算覆盖率（基于内容丰富度）
            coverage = self._calc_file_coverage(content)
            total_coverage += coverage

        self.report.doc_coverage_avg = total_coverage / len(skill_files)
        status = "通过" if self.report.doc_coverage_avg >= self.THRESHOLDS['doc_coverage'] else "失败"
        print(f"  平均覆盖率: {self.report.doc_coverage_avg:.1f}% [{status}]")

    def _calc_file_coverage(self, content: str) -> float:
        """计算单个文件覆盖率"""
        score = 0.0
        checks = [
            (r':.+:`.+`', 15),           # 角色/指令使用
            (r'\.\.\s*code-block::', 20), # 代码块
            (r'\.\.\s*note::', 10),       # 注释
            (r'\.\.\s*warning::', 10),    # 警告
            (r'\.\.\s*todo::', 5),        # TODO
            (r':ref:`', 10),              # 交叉引用
            (r'\.\.\s*dna-trace::', 10),  # DNA追溯
            (r'\.\.\s*table::', 10),      # 表格
            (r'#{3,}', 10),               # 分隔线
        ]
        for pattern, weight in checks:
            if re.search(pattern, content):
                score += weight
        return min(score, 100.0)

    def _check_dna_completeness(self):
        """检查DNA追溯码完整性"""
        print("\n[检查2] DNA追溯码完整性...")

        skill_files = list(self.skills_dir.rglob('longhun-*.rst'))
        total = len(skill_files)
        if total == 0:
            self.report.dna_completeness = 0.0
            return

        has_dna = 0
        for f in skill_files:
            content = f.read_text(encoding='utf-8')
            if '.. dna-trace::' in content and '未分配' not in content:
                has_dna += 1

        self.report.dna_completeness = (has_dna / total) * 100
        status = "通过" if self.report.dna_completeness >= self.THRESHOLDS['dna_completeness'] else "失败"
        print(f"  DNA完整率: {has_dna}/{total} = {self.report.dna_completeness:.1f}% [{status}]")

    def _check_code_examples(self):
        """检查代码示例存在性"""
        print("\n[检查3] 代码示例存在性...")

        skill_files = list(self.skills_dir.rglob('longhun-*.rst'))
        total = len(skill_files)
        if total == 0:
            self.report.code_example_ratio = 0.0
            return

        has_examples = 0
        for f in skill_files:
            content = f.read_text(encoding='utf-8')
            if '.. code-block::' in content:
                has_examples += 1

        self.report.code_example_ratio = (has_examples / total) * 100
        status = "通过" if self.report.code_example_ratio >= self.THRESHOLDS['code_examples'] else "失败"
        print(f"  代码示例率: {has_examples}/{total} = {self.report.code_example_ratio:.1f}% [{status}]")

    def _check_cross_references(self):
        """检查交叉引用完整性"""
        print("\n[检查4] 交叉引用完整性...")

        skill_files = list(self.skills_dir.rglob('longhun-*.rst'))
        total = len(skill_files)
        if total == 0:
            self.report.cross_ref_ratio = 0.0
            return

        has_refs = 0
        for f in skill_files:
            content = f.read_text(encoding='utf-8')
            if ':ref:`' in content or ':doc:`' in content:
                has_refs += 1

        self.report.cross_ref_ratio = (has_refs / total) * 100
        status = "通过" if self.report.cross_ref_ratio >= self.THRESHOLDS['cross_refs'] else "失败"
        print(f"  交叉引用率: {has_refs}/{total} = {self.report.cross_ref_ratio:.1f}% [{status}]")

    def _check_dead_links(self):
        """检查死链"""
        print("\n[检查5] 死链检查...")

        # 收集所有内部引用目标
        ref_targets = set()
        ref_uses = []

        for f in self.docs_dir.rglob('*.rst'):
            content = f.read_text(encoding='utf-8')
            # 提取引用定义
            for match in re.finditer(r'\.\.\s+_(.+?):\s*$', content, re.MULTILINE):
                ref_targets.add(match.group(1).strip())
            # 提取引用使用
            for match in re.finditer(r':ref:`([^<`]+)`', content):
                ref_uses.append((str(f), match.group(1).strip()))

        dead_links = []
        for file_path, ref in ref_uses:
            if ref not in ref_targets:
                dead_links.append(f"{file_path} -> {ref}")

        self.report.dead_links = dead_links
        status = "通过" if len(dead_links) <= self.THRESHOLDS['max_dead_links'] else "失败"
        print(f"  死链数: {len(dead_links)} [{status}]")
        for link in dead_links[:5]:
            print(f"    - {link}")
        if len(dead_links) > 5:
            print(f"    ... 还有 {len(dead_links) - 5} 个")

    def _check_format_consistency(self):
        """检查格式一致性"""
        print("\n[检查6] 格式一致性...")

        issues = []
        for f in self.skills_dir.rglob('longhun-*.rst'):
            content = f.read_text(encoding='utf-8')
            lines = content.split('\n')

            for i, line in enumerate(lines, 1):
                # 检查行过长
                if len(line) > 120:
                    issues.append(f"{f}:{i}: 行过长 ({len(line)}字符)")
                # 检查Tab字符
                if '\t' in line:
                    issues.append(f"{f}:{i}: 包含Tab字符")
                # 检查尾部空格
                if line != line.rstrip():
                    issues.append(f"{f}:{i}: 尾部空格")

        self.report.format_issues = issues
        status = "通过" if len(issues) <= self.THRESHOLDS['max_format_issues'] else "失败"
        print(f"  格式问题: {len(issues)} [{status}]")
        for issue in issues[:5]:
            print(f"    - {issue}")
        if len(issues) > 5:
            print(f"    ... 还有 {len(issues) - 5} 个")

    def _calculate_score(self):
        """计算综合质量分"""
        weights = {
            'doc_coverage': 0.25,
            'dna_completeness': 0.25,
            'code_examples': 0.20,
            'cross_refs': 0.15,
            'dead_links': 0.10,
            'format': 0.05,
        }

        scores = {
            'doc_coverage': min(self.report.doc_coverage_avg / 100, 1.0),
            'dna_completeness': min(self.report.dna_completeness / 100, 1.0),
            'code_examples': min(self.report.code_example_ratio / 100, 1.0),
            'cross_refs': min(self.report.cross_ref_ratio / 100, 1.0),
            'dead_links': max(0, 1.0 - len(self.report.dead_links) / self.THRESHOLDS['max_dead_links']),
            'format': max(0, 1.0 - len(self.report.format_issues) / self.THRESHOLDS['max_format_issues']),
        }

        self.report.score = sum(scores[k] * weights[k] for k in weights) * 100

    def _evaluate_pass(self):
        """评估是否通过门禁"""
        checks = [
            self.report.doc_coverage_avg >= self.THRESHOLDS['doc_coverage'],
            self.report.dna_completeness >= self.THRESHOLDS['dna_completeness'],
            self.report.code_example_ratio >= self.THRESHOLDS['code_examples'],
            self.report.cross_ref_ratio >= self.THRESHOLDS['cross_refs'],
            len(self.report.dead_links) <= self.THRESHOLDS['max_dead_links'],
            len(self.report.format_issues) <= self.THRESHOLDS['max_format_issues'],
        ]

        # 必须全部通过
        self.report.passed = all(checks)

        print("\n" + "=" * 60)
        print("质量门禁结果")
        print("=" * 60)
        print(f"综合评分: {self.report.score:.1f}/100")
        print(f"门禁状态: {'通过' if self.report.passed else '未通过'}")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description='文档质量门禁')
    parser.add_argument('--docs-dir', type=Path, default=Path('./source'))
    parser.add_argument('--fail-on-warning', action='store_true',
                        help='警告视为失败')
    parser.add_argument('--output', type=Path, default=None,
                        help='JSON报告输出路径')
    args = parser.parse_args()

    gate = QualityGate(args.docs_dir)
    report = gate.run_all_checks()

    if args.output:
        args.output.write_text(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
        print(f"\n报告已保存: {args.output}")

    if not report.passed:
        print("\n质量门禁未通过，请修复上述问题。")
        sys.exit(1)
    else:
        print("\n质量门禁通过！")
        sys.exit(0)


if __name__ == '__main__':
    main()
```

### 8.2 版本一致性检查脚本：`version_checker.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本一致性检查脚本
DNA追溯码: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-VERSION-CHECKER-v1.0

检查：
1. RST文档中声明的版本与SKILL_REGISTRY一致
2. DNA追溯码中的版本号与文档版本匹配
3. conf.py版本与最新技能版本同步
"""

import json
import re
import sys
from pathlib import Path

# 技能注册表（与转换脚本一致）
SKILL_REGISTRY = {
    'longhun-3core-opt': {'version': '5.2.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-3CORE-OPT-v5.2'},
    'longhun-archive': {'version': '5.0.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-CENTRAL-ARCHIVE-v5.0'},
    'longhun-asr': {'version': '5.0.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGYIN-ASR-v5.0'},
    'longhun-audit': {'version': '5.1.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-AUDIT-v5.1'},
    'longhun-behavior-engine': {'version': '1.0.0', 'dna': '#龍芯⚡️丙午·甲午·乙丑·壬午·䷨损-LONGHUN-BEHAVIOR-v1.0'},
    'longhun-benchmark': {'version': '5.1.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-BENCHMARK-v5.1'},
    'longhun-cloud-deploy': {'version': '5.0.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-DEPLOY-v5.0'},
    'longhun-cloud-kimi': {'version': '5.0.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-KIMI-v5.0'},
    'longhun-cloud-mcp': {'version': '5.0.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-MCP-v5.0'},
    'longhun-cloud-notion': {'version': '5.0.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-NOTION-v5.0'},
    'longhun-cloud-panel': {'version': '5.0.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-PANEL-v5.0'},
    'longhun-cn-innovation-kb': {'version': '1.0.0', 'dna': '#龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-CN-INNO-KB-v1.0'},
    'longhun-cross-platform': {'version': '5.3.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-CROSS-PLATFORM-v5.3'},
    'longhun-cs-knowledge-base': {'version': '1.5.0', 'dna': '#龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-CS-KB-v1.5'},
    'longhun-daemon': {'version': '5.2.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-DAEMON-v5.2'},
    'longhun-deployment-ready': {'version': '5.2.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-DEPLOY-READY-v5.2'},
    'longhun-dna-align': {'version': '5.2.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-DNA-ALIGN-v5.2'},
    'longhun-empower-engine': {'version': '1.5.0', 'dna': '#龍芯⚡️丙午·癸巳·辛卯·甲午·䷚颐-EMPOWER-ENGINE-v1.5'},
    'longhun-finance': {'version': '9.0.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-WEB3-DNA-FINANCE-v9.0'},
    'longhun-formula-opt': {'version': '5.2.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-FORMULA-OPT-v5.2'},
    'longhun-governance': {'version': '5.0.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-GOVERNANCE-v5.0'},
    'longhun-monitoring': {'version': '5.0.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-MONITORING-v5.0'},
    'longhun-multicurrency': {'version': '5.2.1', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-MULTICURRENCY-v5.2'},
    'longhun-nlp': {'version': '5.0.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGWEN-NLP-v5.0'},
    'longhun-notion-portal': {'version': '2.0.0', 'dna': '#龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-NOTION-PORTAL-v2.0'},
    'longhun-ocr': {'version': '5.0.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGTENG-OCR-v5.0'},
    'longhun-review': {'version': '5.1.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-REVIEW-v5.1'},
    'longhun-riemann': {'version': '5.0.0', 'dna': '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-RIEMANN-FRAMEWORK-v5.0'},
    'longhun-zeng-digital-human': {'version': '1.0.0', 'dna': '#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-ZENG-DIGITAL-HUMAN-v1.0'},
}


def check_versions():
    """检查版本一致性"""
    print("=" * 60)
    print("版本一致性检查")
    print("=" * 60)

    skills_dir = Path('./source/skills')
    mismatches = []

    for skill_name, info in SKILL_REGISTRY.items():
        rst_file = skills_dir / f'{skill_name}.rst'
        if not rst_file.exists():
            # 尝试在子目录中查找
            for subdir in skills_dir.iterdir():
                if subdir.is_dir():
                    rst_file = subdir / f'{skill_name}.rst'
                    if rst_file.exists():
                        break

        if not rst_file.exists():
            print(f"  [跳过] {skill_name}: RST文件不存在")
            continue

        content = rst_file.read_text(encoding='utf-8')

        # 检查1: 版本号匹配
        version_patterns = [
            rf'\b{re.escape(info["version"])}\b',
        ]
        version_found = any(re.search(p, content) for p in version_patterns)

        # 检查2: DNA匹配
        dna_found = info['dna'] in content if info['dna'] else True

        status = []
        if not version_found:
            status.append(f"版本号不匹配 (期望 {info['version']})")
        if not dna_found:
            status.append(f"DNA不匹配 (期望 {info['dna']})")

        if status:
            mismatches.append(f"  {skill_name}: {'; '.join(status)}")
            print(f"  [不匹配] {skill_name}")
            for s in status:
                print(f"    - {s}")
        else:
            print(f"  [OK] {skill_name}")

    print(f"\n{'=' * 60}")
    if mismatches:
        print(f"发现 {len(mismatches)} 个不一致")
        return False
    else:
        print("所有版本一致")
        return True


if __name__ == '__main__':
    passed = check_versions()
    sys.exit(0 if passed else 1)
```

---

## 9. DNA追溯码索引方案

### 9.1 DNA追溯系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    DNA追溯码生态系统                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  源数据层                    处理层              输出层     │
│  ┌──────────┐            ┌──────────────┐    ┌──────────┐  │
│  │ SKILL.md │ ──────→    │ DNAExtractor │ ──→│ RST文档  │  │
│  │ (38文件) │            │ (正则提取)   │    │ (嵌入)   │  │
│  └──────────┘            └──────────────┘    └──────────┘  │
│       │                           │                │       │
│       │                    ┌──────┴──────┐         │       │
│       │                    ▼             ▼         │       │
│  ┌──────────┐         ┌────────┐   ┌──────────┐   │       │
│  │ 代码注释 │ ──────→ │ DNA DB │   │ 验证器   │   │       │
│  │ docstring│         │(JSON)  │   │          │   │       │
│  └──────────┘         └────────┘   └──────────┘   │       │
│                              │                     │       │
│                              ▼                     ▼       │
│                       ┌──────────┐         ┌──────────┐    │
│                       │交叉引用  │ ──────→ │ 索引页面│    │
│                       │映射表    │         │ (RST)   │    │
│                       └──────────┘         └──────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 9.2 DNA追溯码格式规范

```
格式: #龍{根}⚡️YYYY-MM-DD-NAME-vX.Y[.Z]

组件说明:
  #          - 起始标识符
  龍         - 龍魂系统标识
  {根}       - 根标识: 芯(核心)/根(根源)/魂(灵魂)/星(星辉)
  ⚡️         - 能量分隔符
  YYYY-MM-DD - 创建日期
  NAME       - 技能英文名(大写+连字符)
  vX.Y[.Z]   - 语义化版本

示例:
  #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-3CORE-OPT-v5.2
  #龍魂⚡️2026-06-19-LONGHUN-AUDIT-v5.1
  #龍星⚡️2026-06-22-ZENG-DIGITAL-HUMAN-v1.0
```

### 9.3 DNA索引生成脚本：`dna_index_generator.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA追溯码索引生成器
DNA追溯码: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-DNA-INDEX-GEN-v1.0

功能：
1. 扫描所有RST文档提取DNA追溯码
2. 验证DNA格式正确性
3. 检测重复/冲突
4. 生成索引页面和JSON数据库
"""

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

DNA_PATTERN = re.compile(r'#龍[芯根魂星]⚡️\d{4}-\d{2}-\d{2}-[A-Z0-9\-]+-v\d+\.?\d*')


def extract_all_dnas(docs_dir: Path) -> dict:
    """从所有RST文档中提取DNA"""
    dna_db = {}
    dna_locations = defaultdict(list)

    for rst_file in docs_dir.rglob('*.rst'):
        content = rst_file.read_text(encoding='utf-8')
        for match in DNA_PATTERN.finditer(content):
            dna = match.group()
            rel_path = rst_file.relative_to(docs_dir)
            dna_locations[dna].append(str(rel_path))

            if dna not in dna_db:
                dna_db[dna] = {
                    'dna': dna,
                    'locations': [],
                    'extracted_at': datetime.now().isoformat(),
                }
            dna_db[dna]['locations'].append(str(rel_path))

    return dna_db, dna_locations


def validate_dna(dna: str) -> dict:
    """验证DNA追溯码"""
    result = {'valid': False, 'errors': [], 'parsed': {}}

    if not dna.startswith('#'):
        result['errors'].append("必须以#开头")
        return result

    # 去除#后解析
    body = dna[1:]
    parts = body.replace('⚡️', '-').split('-')

    if len(parts) < 5:
        result['errors'].append("组成部分不足")
        return result

    # 检查根标识
    if not re.match(r'龍[芯根魂星]', parts[0]):
        result['errors'].append(f"根标识无效: {parts[0]}")

    # 检查日期
    try:
        date_str = '-'.join(parts[1:4])
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        result['errors'].append(f"日期格式无效")

    # 检查版本
    if not re.match(r'v\d+\.\d+', parts[-1]):
        result['errors'].append(f"版本格式无效: {parts[-1]}")

    result['valid'] = len(result['errors']) == 0
    result['parsed'] = {
        'root': parts[0],
        'date': '-'.join(parts[1:4]),
        'name': '-'.join(parts[4:-1]),
        'version': parts[-1],
    }

    return result


def generate_index(dna_db: dict, output_path: Path):
    """生成RST索引页面"""
    lines = [
        '.. _dna-master-index:',
        '',
        'DNA追溯码主索引',
        '===============',
        '',
        f'生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
        '',
        f'共发现 **{len(dna_db)}** 个DNA追溯码。',
        '',
        '.. list-table:: DNA追溯码完整索引',
        '   :header-rows: 1',
        '   :widths: 5 40 15 10 30',
        '',
        '   * - #',
        '     - DNA追溯码',
        '     - 名称',
        '     - 版本',
        '     - 出现位置',
    ]

    for idx, (dna, info) in enumerate(sorted(dna_db.items()), 1):
        parsed = validate_dna(dna)['parsed']
        locations = ', '.join(info['locations'][:2])
        if len(info['locations']) > 2:
            locations += f' (+{len(info["locations"]) - 2})'

        lines.extend([
            f'   * - {idx}',
            f'     - .. dna-trace:: {dna}',
            f'     - {parsed.get("name", "-")}',
            f'     - {parsed.get("version", "-")}',
            f'     - ``{locations}``',
        ])

    lines.append('')
    output_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"索引已生成: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='DNA追溯码索引生成器')
    parser.add_argument('--docs-dir', type=Path, default=Path('./source'))
    parser.add_argument('--output', type=Path, default=Path('./source/_dna_index.rst'))
    parser.add_argument('--json-output', type=Path, default=Path('./source/_dna_db.json'))
    parser.add_argument('--check', action='store_true', help='仅检查，不生成')
    args = parser.parse_args()

    print("=" * 60)
    print("DNA追溯码索引生成器")
    print("=" * 60)

    dna_db, locations = extract_all_dnas(args.docs_dir)
    print(f"\n发现 {len(dna_db)} 个DNA追溯码")

    # 验证
    invalid_count = 0
    for dna in dna_db:
        result = validate_dna(dna)
        if not result['valid']:
            invalid_count += 1
            print(f"  [无效] {dna}: {result['errors']}")

    # 检查重复
    duplicates = {k: v for k, v in locations.items() if len(v) > 1}
    if duplicates:
        print(f"\n  [警告] {len(duplicates)} 个DNA出现在多处:")
        for dna, locs in duplicates.items():
            print(f"    {dna}: {locs}")

    if args.check:
        print(f"\n检查完成: {len(dna_db)}个DNA, {invalid_count}个无效")
        return

    # 生成索引
    generate_index(dna_db, args.output)

    # 保存JSON数据库
    args.json_output.write_text(json.dumps(dna_db, indent=2, ensure_ascii=False))
    print(f"数据库已保存: {args.json_output}")


if __name__ == '__main__':
    main()
```

### 9.4 DNA追溯码可视化（CSS+JS）

DNA追溯码在HTML中的渲染效果通过 `dna-tracer.js` 和 `longhun-brand.css` 协同实现：

```javascript
// dna-tracer.js - DNA追溯码交互
// DNA追溯码: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-DNA-TRACER-JS-v1.0

document.addEventListener('DOMContentLoaded', function() {
    // 为所有DNA追溯码元素添加点击复制功能
    document.querySelectorAll('.dna-trace').forEach(function(el) {
        el.addEventListener('click', function() {
            const dna = el.textContent.trim();
            navigator.clipboard.writeText(dna).then(function() {
                showTooltip(el, '已复制: ' + dna);
            });
        });
        el.style.cursor = 'pointer';
        el.title = '点击复制DNA追溯码';
    });

    // DNA追溯码悬停显示详情
    document.querySelectorAll('.dna-trace').forEach(function(el) {
        el.addEventListener('mouseenter', function() {
            const dna = el.textContent.trim();
            const parsed = parseDNA(dna);
            if (parsed) {
                showDNADetails(el, parsed);
            }
        });
    });
});

function parseDNA(dna) {
    const match = dna.match(/#(龍[芯根魂星])⚡️(\d{4}-\d{2}-\d{2})-([A-Z0-9\-]+)-(v\d+\.?\d*)/);
    if (!match) return null;
    return {
        root: match[1],
        date: match[2],
        name: match[3],
        version: match[4]
    };
}

function showTooltip(el, text) {
    const tooltip = document.createElement('div');
    tooltip.textContent = text;
    tooltip.style.cssText = 'position:absolute;background:#333;color:#fff;padding:5px 10px;border-radius:4px;font-size:12px;z-index:1000;';
    document.body.appendChild(tooltip);
    const rect = el.getBoundingClientRect();
    tooltip.style.left = rect.left + 'px';
    tooltip.style.top = (rect.bottom + 5) + 'px';
    setTimeout(() => tooltip.remove(), 2000);
}

function showDNADetails(el, parsed) {
    const detail = document.createElement('div');
    detail.className = 'dna-detail-popup';
    detail.innerHTML = `
        <div style="background:#fff;border:2px solid #C41E3A;border-radius:8px;padding:15px;box-shadow:0 4px 12px rgba(0,0,0,0.15);min-width:200px;">
            <div style="color:#C41E3A;font-weight:bold;margin-bottom:8px;">DNA追溯详情</div>
            <div><b>根标识:</b> ${parsed.root}</div>
            <div><b>创建日期:</b> ${parsed.date}</div>
            <div><b>技能名称:</b> ${parsed.name}</div>
            <div><b>版本:</b> ${parsed.version}</div>
        </div>
    `;
    // 简化为console输出，实际可扩展为悬浮弹窗
    console.log('DNA详情:', parsed);
}
```

---

## 10. Read the Docs部署

### 10.1 部署架构

```
┌─────────────────────────────────────────────────────────────┐
│                  Read the Docs 部署架构                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   GitHub (main) ──→ RTD Webhook ──→ 自动构建               │
│                                                             │
│   构建流程:                                                  │
│   1. pip install -r requirements.txt                       │
│   2. python skill_md_to_rst.py                             │
│   3. python dna_index_generator.py                         │
│   4. sphinx-build -b html source build/html                │
│   5. 部署到 CDN                                              │
│                                                             │
│   多版本管理:                                                │
│   ├── latest (主分支)                                       │
│   ├── stable (最新Tag)                                      │
│   ├── v5.2, v5.1, v5.0 (历史版本)                          │
│   └── pr-123 (PR预览)                                      │
│                                                             │
│   自定义域名: docs.longhun.system                           │
│   HTTPS: 自动证书 (Let's Encrypt)                           │
│   CDN: CloudFlare (全球加速)                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 10.2 自定义扩展清单

| 扩展文件 | 功能 | 状态 |
|---------|------|------|
| `dna_trace.py` | `:dna-trace:` 指令，DNA追溯码渲染 | 必需 |
| `tri_color_audit.py` | `:audit-red:/:audit-yellow:/:audit-green:` 角色 | 必需 |
| `skill_metadata.py` | `:skill-meta:` 指令，技能元数据卡片 | 必需 |
| `longhun_domain.py` | 龍魂专属Sphinx Domain | 可选 |

---

## 11. 工时估算与批次计划

### 11.1 总工时估算

| 阶段 | 任务 | 工时 | 依赖 |
|------|------|------|------|
| **Phase 1: 基础设施** | Sphinx项目初始化 | 4h | - |
| | conf.py配置 | 3h | - |
| | 主题与CSS定制 | 6h | - |
| | 自定义扩展开发 | 8h | - |
| | CI/CD配置 | 4h | - |
| *小计* | | *25h* | |
| **Phase 2: 内容迁移** | P0批次 (12技能) | 24h | Phase 1 |
| | P1批次 (11技能) | 22h | Phase 1 |
| | P2批次 (10技能) | 20h | Phase 1 |
| | P3批次 (5技能) | 10h | Phase 1 |
| *小计* | | *76h* | |
| **Phase 3: 质量验证** | 文档覆盖率提升 | 12h | Phase 2 |
| | 交叉引用补全 | 8h | Phase 2 |
| | 死链修复 | 4h | Phase 2 |
| | 最终审计 | 4h | Phase 2 |
| *小计* | | *28h* | |
| **总计** | | **129h (~16工作日)** | |

### 11.2 6周批次计划

```
第1周 [基础设施搭建]
├── Day 1: 项目结构初始化 + conf.py配置
├── Day 2: 主题定制 + CSS开发
├── Day 3: 自定义扩展开发(dna_trace + tri_color_audit)
├── Day 4: CI/CD配置 + GitHub Actions调试
├── Day 5: 转换脚本开发 + 测试
└── 产出: 可构建的空文档框架

第2周 [P0批次: 核心架构 12技能]
├── Day 1-2: longhun-system + longhun-3core-opt + longhun-daemon
├── Day 3-4: longhun-cloud-panel + longhun-cloud-deploy + longhun-deployment-ready
├── Day 5:   longhun-formula-opt + longhun-benchmark + longhun-automation
└── 产出: 12个核心架构技能文档

第3周 [P0剩余 + P1开始]
├── Day 1-2: longhun-cross-platform + longhun-cloud-mcp + longhun-monitoring
├── Day 3-4: longhun-asr + longhun-nlp + longhun-ocr
├── Day 5:   longhun-finance + longhun-empower-engine
└── 产出: 8+2技能文档

第4周 [P1批次: AI引擎 剩余技能]
├── Day 1-2: longhun-behavior-engine + longhun-cloud-kimi
├── Day 3-4: longhun-zeng-digital-human + longhun-riemann
├── Day 5:   P1批次质量审核 + 交叉引用补全
└── 产出: 11个AI引擎技能文档(完成)

第5周 [P2批次: 数据工具 10技能]
├── Day 1-2: longhun-archive + longhun-backup + longhun-cloud-notion
├── Day 3-4: longhun-cn-innovation-kb + longhun-cs-knowledge-base
├── Day 5:   longhun-kg-upgrade + longhun-multicurrency + longhun-notion-portal
└── 产出: 10个数据工具技能文档

第6周 [P3批次 + 最终验收]
├── Day 1:   P3批次: longhun-audit + longhun-dna-align + longhun-governance
├── Day 2:   P3批次: longhun-review + longhun-warehouse-audit
├── Day 3:   全局交叉引用补全 + 死链修复
├── Day 4:   质量门禁验证 + 覆盖率提升
├── Day 5:   最终审计 + 上线部署
└── 产出: 完整38技能Sphinx文档体系上线
```

### 11.3 质量标准里程碑

| 里程碑 | 时间 | 目标 | 验收标准 |
|--------|------|------|---------|
| M1-框架就绪 | 第1周末 | Sphinx框架可构建 | `make html` 0错误0警告 |
| M2-P0完成 | 第2周末 | 核心架构文档化 | P0覆盖率≥80%，DNA完整100% |
| M3-P1完成 | 第4周末 | AI引擎文档化 | P1覆盖率≥70%，代码示例≥60% |
| M4-P2完成 | 第5周末 | 数据工具文档化 | P2覆盖率≥60%，交叉引用≥50% |
| M5-P3完成 | 第6周中 | 审计安全文档化 | P3覆盖率≥80%，审计标注100% |
| M6-正式上线 | 第6周末 | 全量上线 | 综合质量分≥80，0死链 |

---

## 12. 附录

### 12.1 Makefile

```makefile
# =============================================
# 龍魂系统 Sphinx 文档 Makefile
# DNA追溯码: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-DOCS-MAKEFILE-v1.0
# =============================================

SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build
PYTHON        = python3

# 转换脚本
CONVERTER     = $(SOURCEDIR)/_scripts/skill_md_to_rst.py
DNA_INDEXER   = $(SOURCEDIR)/_scripts/dna_index_generator.py
QUALITY_GATE  = $(SOURCEDIR)/_scripts/quality_gate.py

.PHONY: help clean html dirhtml singlehtml pickle json htmlhelp qthelp devhelp \
        epub latex latexpdf text man changes linkcheck doctest live convert \
        dna-index quality

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

# 自动转换并构建HTML
html: convert dna-index
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS)
	@echo "构建完成: $(BUILDDIR)/html/index.html"

# 仅转换SKILL.md
convert:
	@echo "正在转换SKILL.md文档..."
	$(PYTHON) $(CONVERTER) --output-dir $(SOURCEDIR)/skills

# 生成DNA索引
dna-index:
	@echo "正在生成DNA追溯码索引..."
	$(PYTHON) $(DNA_INDEXER) --docs-dir $(SOURCEDIR)

# 质量门禁检查
quality:
	@echo "执行质量门禁检查..."
	$(PYTHON) $(QUALITY_GATE) --docs-dir $(SOURCEDIR) --fail-on-warning

# 实时预览
live:
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS)

# 链接检查
linkcheck:
	$(SPHINXBUILD) -b linkcheck "$(SOURCEDIR)" "$(BUILDDIR)/linkcheck" $(SPHINXOPTS)

# 清理
clean:
	rm -rf $(BUILDDIR)/*
	find $(SOURCEDIR)/skills -name "*.rst" -not -name "index.rst" -delete

# Catch-all
%:
	$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
```

### 12.2 自定义Sphinx扩展模板

#### `dna_trace.py` — DNA追溯码指令

```python
"""
DNA追溯码 Sphinx 扩展
:dna-trace: 指令 - 渲染DNA追溯码徽章
"""

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.docutils import SphinxDirective


class DNATraceNode(nodes.General, nodes.Element):
    """DNA追溯码节点"""
    pass


class DNATraceDirective(SphinxDirective):
    """
    DNA追溯码指令

    用法::

        .. dna-trace:: #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-3CORE-OPT-v5.2

           DNA状态: 已注册
    """
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        dna_code = self.arguments[0]
        node = DNATraceNode()
        node['dna_code'] = dna_code
        if self.content:
            node['status'] = '\n'.join(self.content)
        else:
            node['status'] = ''
        return [node]


def visit_dna_trace_html(self, node):
    dna = node.get('dna_code', '')
    status = node.get('status', '')
    is_unassigned = '未分配' in dna or '缺失' in status

    css_class = 'dna-trace unassigned' if is_unassigned else 'dna-trace'
    self.body.append(f'<span class="{css_class}" title="DNA追溯码: {dna}">')
    self.body.append(f'{dna}')
    if status:
        self.body.append(f'<span class="dna-status">{status}</span>')
    self.body.append('</span>')

    raise nodes.SkipNode


def depart_dna_trace_html(self, node):
    pass


def setup(app):
    app.add_node(DNATraceNode,
                 html=(visit_dna_trace_html, depart_dna_trace_html),
                 latex=(lambda s, n: None, lambda s, n: None))
    app.add_directive('dna-trace', DNATraceDirective)

    return {
        'version': '1.0.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
```

#### `tri_color_audit.py` — 三色审计角色

```python
"""
三色审计 Sphinx 扩展
:audit-red: / :audit-yellow: / :audit-green: 角色
"""

from docutils import nodes
from docutils.parsers.rst import roles


def audit_red_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """红色审计 - 危险/严重"""
    node = nodes.inline(rawtext, text, classes=['audit-red'])
    return [node], []


def audit_yellow_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """黄色审计 - 警告/注意"""
    node = nodes.inline(rawtext, text, classes=['audit-yellow'])
    return [node], []


def audit_green_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """绿色审计 - 通过/正常"""
    node = nodes.inline(rawtext, text, classes=['audit-green'])
    return [node], []


def setup(app):
    app.add_role('audit-red', audit_red_role)
    app.add_role('audit-yellow', audit_yellow_role)
    app.add_role('audit-green', audit_green_role)

    return {
        'version': '1.0.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
```

### 12.3 Notion同步策略

```
┌─────────────────────────────────────────────────────────────┐
│                Sphinx ↔ Notion 同步策略                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  同步方向: 单向为主（Sphinx ← Notion）                       │
│                                                             │
│  自动同步（每日）:                                           │
│  • Notion知识卡片 → Sphinx术语表（glossary.rst）            │
│  • Notion进度更新 → Sphinx变更日志（changelog/）            │
│                                                             │
│  手动同步（按需）:                                           │
│  • Notion PRD → Sphinx架构文档（architecture/）             │
│  • Sphinx API文档 → Notion技术卡片                          │
│                                                             │
│  同步脚本:                                                  │
│  • source/_scripts/sync_notion.py                          │
│  • 通过 Notion API 读取指定数据库                          │
│  • 生成/更新对应RST文件                                    │
│  • 保留DNA追溯码不变                                       │
│                                                             │
│  冲突解决:                                                  │
│  • DNA追溯码以Sphinx为准（权威源）                         │
│  • 技术内容以最新提交为准                                  │
│  • 人工审核后合并                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 12.4 关键指标仪表盘

| 指标 | 目标值 | 当前 | 监控方式 |
|------|--------|------|---------|
| 文档覆盖率 | ≥80% | 0% | quality_gate.py |
| DNA完整性 | 100% | 76% (29/38) | dna_index_generator.py |
| 代码示例率 | ≥60% | 0% | quality_gate.py |
| 交叉引用率 | ≥50% | 0% | quality_gate.py |
| 死链数 | 0 | 0 | Sphinx linkcheck |
| 构建成功率 | 100% | N/A | CI/CD |
| 平均构建时间 | <5min | N/A | CI/CD |
| 搜索响应时间 | <2s | N/A | RTD监控 |

---

## 文档元数据

| 属性 | 值 |
|------|-----|
| **DNA追溯码** | `#龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-SPHINX-DOCS-v3.0` |
| **版本** | 3.0.0 |
| **创建日期** | 2026-07-04 |
| **作者** | 龍魂工程团队 |
| **适用范围** | 龍魂系统v5.0全部38个技能模块 |
| **文档类型** | 技术规范 / 迁移指南 |
| **关联系统** | Sphinx 7.x, Python 3.11+, Read the Docs |
| **审核状态** | :audit-yellow:`待审核` |

---

*本方案由龍魂文档工程自动化系统生成，遵循CNSH编程规范与三色审计标准。*

---

## 🐉 ROOT_CARD

```yaml
ROOT_CARD:
  系统: UID9622 龍魂系统
  模块: 龍魂系统v5.0 Sphinx文档框架 + 38技能内容迁移规范
  版本: v2.0
  DNA: "#龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-ARCHITECTURE-IMPORT-05-v2.0"
  ParentDNA: "#龍芯⚡️丙午·甲午·戊寅·戊午·䷕贲-IP-ASSET-MATRIX-v2.0"
  CONFIRM: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  SEAL: "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
  GPG: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
  作者: "UID9622 / Lucky·诸葛鑫"
  归档路径: "/Users/zuimeidedeyihan/longhun-system/docs/private-shared-imports/architecture/direction3_documentation.md"
  三色审计: "🟢"
  主权状态: "已声明 · 已锁定 · 已归集"
  来源可查: true
  去向可追: true
```

---

> **龍魂系统 —— 中国人的数字主权，代码里的精神根脉。**
>
> *数据主权归于人民 · 技术为人民服务 · 祖国优先*


---

## 摘要

（请在此用不超过 256 字说明本文档的核心内容、性质与局限。）

## 关键词

（请列出 5–10 个关键词，中英文对照优先。）

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] （请填写）
- 相关龍魂系统文档：
  - 《龍魂文档标准模板 v1.0》(#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 诚实局限

1. （请列出本分析的第一条局限或不确定性。）
2. （请列出第二条。）
3. （请列出第三条。）

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-07-15 | v1.0.0 | UID9622 | 按《龍魂文档标准模板 v1.0》整理 | 草稿 |

## 分类标签

- 总纲模块：（请勾选，例如 #知识矩阵 #安全域）
- 对外状态：（请勾选，例如 #Gitee #GitHub #CSDN）
- 审计色：#黄色待审

## DNA 签名

```
#龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-AUTO-IP-INTEGRATION-7F3A9B12
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

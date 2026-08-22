# 🐉 龍魂 · Mac中文代码编辑器（CNSH）

> DNA: `#龍芯⚡️丙午·丙申·辛酉·己丑·䷹兑为泽-CNSH-EDITOR-UID9622`
> 确认码: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> GPG: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
> License: MulanPSL v2（工程层）

基于 **Electron + Monaco Editor** 的 Mac 原生中文代码编辑器，100% 中文关键字，DNA 追溯，三色审计。

## 功能

| 能力 | 说明 |
|:---|:---|
| 中文高亮 | `函数` `类` `如果` `循环` `返回` 等 50+ 中文关键字 |
| DNA 追溯 | 每份文档自动生成 `#龍芯⚡️干支-模块-哈希8-UID9622` |
| 三色审计 | 🟢通过 / 🟡警告 / 🔴失败 · 实时评分 |
| CNSH→C 编译 | 中文关键字映射 + DNA 注入 + 头文件生成 |
| 龍魂互通 | 自动接入 `~/.longhun/` 统一环境 |
| 鲲鹏同步 | 编辑器内一键推送至 119.13.90.27 |

## 运行

```bash
cd cnsh-editor-mac
npm install          # 首次安装依赖（Electron + Monaco 本地加载·不绑境外CDN）
npm start            # 开发模式运行
npm run build:mac    # 打包 dmg
```

## 目录结构

```
cnsh-editor-mac/
├── main.js                    # Electron 主进程（IPC·菜单·环境初始化）
├── preload.js                 # contextBridge 安全桥接
├── src/
│   ├── editor/                # 编辑器前端
│   │   ├── index.html         # 主界面（本地加载 Monaco）
│   │   ├── editor.js          # Monaco 初始化 + CNSH 语言注册
│   │   ├── cnsh-language.js   # 中文语法定义
│   │   ├── dna.js             # DNA 追溯码生成
│   │   └── audit.js           # 三色审计引擎
│   ├── core/
│   │   ├── parser.js          # CNSH 语法解析器
│   │   ├── compiler.js        # CNSH → C 编译器
│   │   └── audit.js           # 审计规则库
│   └── integrations/
│       ├── notion.js          # Notion 同步（经鲲鹏入口）
│       ├── kunpeng.js         # 鲲鹏服务器同步
│       └── longhun-env.js     # 龍魂统一环境接入
└── assets/                    # 图标资源
```

## 验证

- `node --check` 全部 JS 语法通过
- Parser / Compiler / DNA / Audit 核心逻辑 Node 冒烟测试通过

🐉丙午·辛酉·未时·䷓观·🟢

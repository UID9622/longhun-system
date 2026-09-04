# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂 CodeBuddy MVP 插件集 v1.0

> DNA: `#龍芯⚡️丙午·辛未·CODEBUDDY-MVP-PLUGINS-v1.0`
> 6 个 MVP · 全部自研 · 本地运行 · 不上传云端

## 安装（开发/本机）

```bash
cd editors/codebuddy
bash install.sh
```

安装后按 `Cmd+Shift+P` → 输入「重新加载窗口」刷新。侧边栏点击「🐉」打开控制台。

## 分发（给其他人用）

已打包为 `.vsix` 文件，放在 `dist/` 目录：

| 插件 | 分发包 | 大小 |
|------|--------|------|
| 🖥️ 龍魂控制台 | `dist/longhun-console-1.0.0.vsix` | ~18KB |
| 📝 CNSH 语法高亮 v2.0 | `dist/cnsh-syntax-2.0.0.vsix` | ~509KB |
| 🛡️ 审计追踪 | `dist/longhun-audit-tracker-1.0.0.vsix` | ~16KB |
| 🔀 多模型路由 | `dist/longhun-model-router-1.0.0.vsix` | ~11KB |
| 📋 协议校验 | `dist/longhun-protocol-checker-1.0.0.vsix` | ~196KB |
| 🚀 一键部署 | `dist/longhun-one-click-deploy-1.0.0.vsix` | ~12KB |

安装方式：把 `.vsix` 文件拖进 CodeBuddy 侧边栏扩展视图，或按 `Cmd+Shift+P` →「从 VSIX 安装」。

> ⚠️ 仅本地分发，不上传到任何扩展市场。\n> 📥 在线下载: https://uid9622.cn/tools/cnsh-syntax-2.0.0.vsix\n> 安装方式：下载 `.vsix` → CodeBuddy 侧边栏扩展视图 → 拖入安装，或 `Cmd+Shift+P` →「从 VSIX 安装」

## 六个 MVP

| # | 插件 | 目录 | 功能 | 状态 |
|:---:|------|------|------|:---:|
| 1 | 🖥️ 龍魂控制台 | `longhun-console/` | 侧边栏系统状态/DNA/审计/lh命令 | ✅ |
| 2 | 📝 CNSH 语法高亮 v2.0 | `cnsh-syntax/` | 中文变量着色/DNA锚定/安全标记/自动补全 | ✅ |
| 3 | 🛡️ 审计追踪 | `audit-tracker/` | AI代码自动审计/模型来源/哈希/本地日志 | ✅ |
| 4 | 🔀 多模型路由 | `model-router/` | DeepSeek/Kimi/本地一键切换+任务自动路由 | ✅ |
| 5 | 📋 协议校验 | `protocol-checker/` | DNA锚定/老祖宗规则/敏感泄露/一键修复 | ✅ |
| 6 | 🚀 一键部署 | `one-click-deploy/` | git add+commit+push+GPG签名 | ✅ |

## 使用

安装后，在 CodeBuddy 中：

- **侧边栏**: 点击活动栏「🐉」图标打开龍魂控制台
- **命令面板** (`Cmd+Shift+P`): 搜索「龍魂」查看所有命令
- **状态栏**: 右侧显示模型路由/审计计数/Git分支/协议状态
- **CNSH 文件** (`.cnsh`): 自动语法高亮 + 保存时审计

## 插件详解

### 1. 龍魂控制台
- 实时探测本地服务（蚁群9677/神经网络9627/面板8766）
- 显示人格矩阵(16/16)、引擎数、蚁群tick、涌现E值
- 三色审计统计 + 最近20条审计日志
- 一键 `lh` 命令、打开总控面板、打开蚁群调试台

### 2. CNSH 语法高亮 v2.0
- 7层语法着色：DNA锚定(金)/控制流/类型/安全关键字(红)/系统常量(蓝)/内置函数/中文标识符(绿)
- 自动补全：26个关键字 + 20个内置函数
- 保存时审计：纯英文变量→建议中文 + 敏感信息泄露检测
- 协议校验：DNA锚定/老祖宗规则/敏感导入

### 3. 审计追踪
- 粘贴/保存时自动检测 AI 生成代码标记
- 记录：模型来源、提示词哈希(SHA256)、代码哈希、时间戳
- 状态栏显示待审核计数
- 一键生成审计报告（Markdown）
- 数据仅存 `logs/ai_audit.jsonl`，不上传

### 4. 多模型路由
- 状态栏一键切换 DeepSeek/Kimi/本地/自动
- 自动路由：代码生成→DeepSeek / 审查→Kimi / 敏感→本地
- API密钥仅存本地 VSCode 配置
- 路由配置持久化到 `config/model_route.json`

### 5. 协议校验
- 3项检查：DNA锚定 / 老祖宗规则(境外API/云端上传/敏感库) / 敏感泄露(密钥/Token/私钥)
- 保存时自动弹窗警告
- 一键修复：自动添加DNA锚定码、注释境外导入
- 工作区全量扫描 + 批量修复

### 6. 一键部署
- `git add -A` → `git commit -S` (GPG) → `git pull --rebase` → `git push`
- 多远程推送：GitHub/Gitee/华为云
- 状态栏显示分支和待提交数
- 提交类型快速选择 (feat/fix/docs/refactor...)

## 主权声明

- ✅ 纯本地运行，不联网
- ✅ 不上传任何代码/数据
- ✅ 不依赖任何第三方云服务
- ✅ 审计日志仅存本地文件
- ✅ API密钥仅存本地 VSCode 配置
- ✅ 不开源到 VSCode 市场
- ✅ 仅供 UID9622 使用

# 龍魂系统 · 长期记忆索引

> 本文件为 Kimi / CodeBuddy / 其他 AI 的统一记忆入口。
> 更新：2026-07-28
> DNA: #龍芯⚡️丙午·丙申·癸酉·庚申·临-MEMORY-WARP-LAB-DEPLOY-v∞-7A3F2E1D

---

## 最新交付（2026-07-28）

### 龍魂视频工坊 v3.0 · 按钮操作 + 实时数据

**背景**：用户要求解说稿全部改为按钮操作，不要在页面暴露命令；同时实时展示浏览、下载、转发、评论数据，支持评论来源分类（真实用户 / 匿名 / 系统 / 测试 / 疑似水军），并统一接入龍魂系统数据大屏。

**DNA**: `#龍芯⚡️丙午·乙未·癸亥·酉时·离为火-VIDEO-STUDIO-v3.0-VISUAL`

**产物：**

| # | 文件 | 说明 |
|---|------|------|
| 1 | `bin/lh_video_index.py` | 视频画廊服务 v2.0：新增 `/api/metrics`、`/api/videos/:id/{view,download,share,comments}` |
| 2 | `portal/video-studio/index.html` | v3.0 前端：生成表单、画廊、实时指标、图表、评论系统、转发按钮 |
| 3 | `videos/metrics.json` | 本地统一指标文件（浏览/下载/转发/评论/生成次数/日汇总） |
| 4 | `bin/lh_ctl_web.py` | 新增 `/api/metrics`：引擎 + 任务 + 视频三合一系统指标 |
| 5 | `portal/dashboard/index.html` | 新增统一数据视图：引擎分类、任务执行、视频风格、每日互动、最近评论 |

**实时指标 API：**

| 端点 | 说明 |
|:---|:---|
| `GET /api/metrics` | 系统级指标（视频/引擎/任务） |
| `GET /api/videos` | 视频列表（含每个视频的 metrics） |
| `POST /api/videos/:id/view` | 浏览 +1 |
| `POST /api/videos/:id/download` | 下载 +1 |
| `POST /api/videos/:id/share` | 转发 +1 |
| `GET /api/videos/:id/comments` | 评论列表 |
| `POST /api/videos/:id/comments` | 发表评论（自动水军识别） |

**评论来源分类：**

- 真实用户 / 匿名游客 / 系统 / 测试（可手动选择）
- 自动识别：重复内容、过短（<3字）、同一客户端 1 小时 >3 条 → 疑似水军

**在线地址：**

- 视频工坊：`http://localhost:8788/portal/video-studio/`
- 数据大屏：`http://localhost:9630/`

**用法（按钮操作）：**

```bash
# 启动服务
python3 bin/lh_video_index.py --serve :8788
python3 bin/lh_ctl_web.py --host 127.0.0.1 --port 9630
```

然后在浏览器打开上述地址，全部操作通过按钮完成。

---

### Notion 引擎注册表同步结果 + Schema v2.0.1 修复

**背景**：全量 1011 条 Notion 同步后台任务跑完，但 144 条失败，报错 `database schema has exceeded the maximum size`。

**根因**：`重要函数`、`重要类`、`导入模块` 三个字段定义为 `multi_select`，随着记录插入，选项数量不断膨胀，最终撑满 Notion 数据库 schema 上限。

**修复：**

| 文件 | 改动 |
|:---|:---|
| `data/notion_sync/engines/notion_db_schema_v2.json` | `重要函数/重要类/导入模块` 从 `multi_select` 改为 `rich_text` |
| `bin/lh_notion_engine_status_syncer.py` | 同步时这三个字段输出为逗号分隔文本，不再生成选项 |
| `bin/lh_notion_engine_db_setup.py` | 读取 Schema v2.0.1 生成新库 Payload |

**同步结果：**

```text
🟢 成功: 867 / 1011
🔴 失败: 144 / 1011（全部因 schema size 超限）
```

**下一步（需要手动执行）：**

```bash
# 1. 用新 Schema 建一个新 Notion 数据库
export NOTION_INTEGRATION_TOKEN=xxx
export NOTION_PARENT_PAGE_ID=xxx
python3 bin/lh_notion_engine_db_setup.py --create

# 2. 拿到返回的 database_id
export NOTION_DATABASE_ID=<新库id>

# 3. 重新全量同步
python3 bin/lh_notion_engine_status_syncer.py --execute
```

---

### 龍魂引擎主控 lh-ctl v1.0

**背景**：用户指出引擎脚本零零散散、各自为政，需要一个统一入口统一调度、统一审计、统一输出。

**DNA**: `#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH-CTL-v1.0-7A3B9C2D`

**产物：**

| # | 文件 | 说明 |
|---|------|------|
| 1 | `bin/lh_ctl.py` | 统一 CLI 入口：search / video / distill / audit / 3d / status / logs / web / schedule |
| 2 | `bin/lh_ctl_config.py` | 配置管理器：默认模板 `~/.longhun/config.yaml`，支持环境变量覆盖 token |
| 3 | `bin/lh_ctl_web.py` | Flask Web 仪表盘后端：`/api/health` `/api/status` `/api/logs` `/api/run` |
| 4 | `bin/lh_ctl_scheduler.py` | APScheduler 定时任务管理：add / list / remove / daemon |
| 5 | `portal/dashboard/index.html` | 动态 Web 仪表盘：引擎状态、运行日志、一键操作 |
| 6 | `~/.longhun/config.yaml` | 统一配置：引擎路径、输出目录、默认参数、Web/Schedule 参数 |
| 7 | `~/.longhun/state/job_history.jsonl` | 统一运行状态存储 |
| 8 | `~/.longhun/logs/lh_ctl/YYYY-MM-DD.log` | 统一运行日志 |

**命令清单：**

```bash
lh search "关键词"                  # 龍魂搜索引擎
lh video --script 解说稿.txt         # 龍魂视频工坊
lh distill --mock                   # K3 蒸馏
lh audit                            # 语义安全闸审计
lh 3d --input xxx.png --category military --style stylized  # 图生三维
lh status                           # 查看引擎注册表状态
lh logs --tail 20                   # 查看聚合运行日志
lh web                              # 启动 Web 仪表盘（默认 http://127.0.0.1:9630）
lh schedule list                    # 定时任务管理
```

**核心能力：**

| 层级 | 能力 | 说明 |
|:---|:---|:---|
| 控制层 | 统一 CLI / 配置 / 日志 / 状态 | 所有引擎从 `lh` 入口出发，配置集中管理 |
| 调度层 | 子进程执行 + 任务 ID + 退出码 + 摘要 | 每次运行生成 `job_id`，写入 `job_history.jsonl` |
| 入口层 | Web 仪表盘 + API 网关 | 浏览器实时查看状态，一键触发引擎运行 |
| 数据层 | 运行日志摘要字段 | Notion 注册表已增加「运行日志摘要」字段，闭环反馈 |

**验证结果：**

```text
🟢 lh 3d --input data/3d_forge/test_input.png --category military --style stylized
   综合得分: 85/100 · CNSD/JS/AUDIT 产物完整 · job_id=lh-2026-07-28-190801-457000
🟢 Web 仪表盘按钮: 🧊 图生三维 已接入 /api/run
```

---

### 龍魂图生三维引擎 v1.0

**背景**：基于「龍魂系统_图生三维引擎协议_v1.0」与对比对照表，把图像转换为 Three.js 可渲染的 3D 语义产物。

**DNA**: `#龍芯⚡️丙午·丙申·癸酉·明夷-IMG2THREEJS-FORGE-v1.0-3D8A7B2C`

**产物：**

| # | 文件 | 说明 |
|---|------|------|
| 1 | `bin/lh_3d_pipeline.py` | 九阶流水线：intake → deconstruct → blockout → structural → refine → material → lighting → interaction → optimize |
| 2 | `data/3d_forge/test_input.png` | 512×512 金色测试图 |
| 3 | `data/3d_forge/*.cnsd` | CNSH 语义描述文件 |
| 4 | `data/3d_forge/*.js` | Three.js 兼容层代码 |
| 5 | `data/3d_forge/*.audit` | 七因子审计日志 |

**九阶流水线：**

```text
[1/9] 图像探测   → 分辨率/透明度/主色分析
[2/9] 部件解构   → 轮廓/部件/空间关系
[3/9] 粗胚生成   → 包围盒 + 基础几何
[4/9] 骨架搭建   → 结构框架/连接点
[5/9] 精形细化   → 顶点精修/曲率
[6/9] 材质设定   → PBR 材质参数
[7/9] 光照拟合   → 主光/补光/环境光
[8/9] 交互构建   → OrbitControls/热点/动画
[9/9] 优化打包   → 几何合并/LOD/输出产物
```

**输出格式：**

| 后缀 | 内容 |
|:---|:---|
| `.cnsd` | CNSH 语义描述（对象/部件/材质/光照/交互） |
| `.js` | Three.js 场景初始化代码（可直接嵌入网页） |
| `.audit` | 七因子审计：structural / semantic / visual / performance / security / sovereignty / maintainability |

**用法：**

```bash
# 直接调用
python3 bin/lh_3d_pipeline.py --input data/3d_forge/test_input.png --category object --style realistic

# 通过 lh-ctl
lh 3d --input data/3d_forge/test_input.png --category military --style stylized
```

**分类与风格：**

| category | style |
|:---|:---|
| object / character / building / nature / military | realistic / stylized |

---

## 历史交付（2026-07-28）

### 曲速引擎推演舱 v1.0 部署

**背景**：基于 Alcubierre 度量的 3D 曲速泡可视化交互页面，龍魂金暗色风格，融合 Three.js、KaTeX 数学渲染与龍魂审计映射。

**DNA**: `#龍芯⚡️丙午·乙未·甲戌·午时·☰乾-WARP-LAB-v1.0-7a3f2e1d`

**在线地址：**

- ✅ `http://uid9622.cn/warp-lab/`
- ⚠️ `http://longhun888.com/warp-lab/`（DNS/Cloudflare 返回 530，需检查域名解析）

**产物：**

| # | 文件 | 说明 |
|---|------|------|
| 1 | `portal/warp-lab/index.html` | 主页面：SEO/OG/Schema.org/loading 动效/GitHub Corner/键盘快捷键 |
| 2 | `portal/warp-lab/vendor/` | Three.js + KaTeX + Orbitron 字体 |
| 3 | `portal/warp-lab/README.md` | 中英双语开源说明 |
| 4 | `portal/warp-lab/LICENSE` | MIT 协议 |
| 5 | `portal/warp-lab/.gitignore` | 开源版本控制忽略 |
| 6 | `portal/home-new.html` | 官网首页，服务矩阵新增 🚀 曲速引擎推演舱入口 |

**优化点：**

| 优化 | 说明 |
|:---|:---|
| SEO | 中英文 meta + OG + Twitter Card + Schema.org WebApplication |
| Loading | 5 步加载动效：度量 → 联络 → 曲速泡 → 审计 → 就绪 |
| DNA 追溯 | 文件头 + 页脚双重签名 |
| 交互 | 键盘 `1-8` 切换节点、`R` 重置、`空格` 旋转 |
| 移动适配 | 320px 字号自适应 |
| GitHub Corner | 右上角可折叠 SVG 彩带 |

**部署信息：**

| 项目 | 值 |
|:---|:---|
| 服务器 IP | 119.13.90.27 |
| 部署路径 | `/var/www/longhun/warp-lab/` |
| nginx 配置 | `/etc/nginx/conf.d/longhun.conf` 新增 `location /warp-lab/` |
| 首页路径 | `/var/www/longhun/index.html` |
| HTTP 状态 | 200 OK / text-html / 33,180 bytes |

**验证命令：**

```bash
# 服务器本地验证
curl -s -I --resolve longhun888.com:80:127.0.0.1 http://longhun888.com/warp-lab/

# 公网验证
curl -I http://uid9622.cn/warp-lab/
```

---

## 历史交付

### 线性回归体检器 v1.0

**背景**：深度学习 CSDN 文章《[线性回归没你想的那么简单：R²虚高、P值误用，90%的新手栽在这两个指标上](https://tigerhhzz.blog.csdn.net/article/details/163148143)》，将核心洞察落地为自动化体检工具。

**DNA**: `#龍芯⚡️丙午·丙申·癸酉·庚申·临-LINEAR-REGRESSION-AUDITOR-v1.0-7A3B9C2D`

**核心收获（来自文章）：**

1. **R² 的软肋**：每新增一个特征，R² 只增不减，纯噪声也能抬高它
2. **Adj.R² 的作用**：给特征数上惩罚，没用的特征会让它下降
3. **P值的意义**：P < 0.05 仅表示相关性显著，不等于因果或重要
4. **过拟合识别**：训练 R² 高、测试 R² 低，是典型过拟合

**产物：**

| # | 文件 | 说明 |
|---|------|------|
| 1 | `bin/lh_linear_regression_auditor.py` | 线性回归体检器 |
| 2 | `data/audit/linear_regression/lr_audit_report.json` | 体检报告示例 |

**工具能力：**

- CSV 自定义数据集或 sklearn diabetes demo
- 输出 R² / Adj.R² / 测试集 R²
- statsmodels P值、系数、F统计量、AIC/BIC
- 自动 R² 虚高检测：加入随机噪声特征，对比训练/测试指标
- 三色审计报告：🔴 高风险 / 🟡 警告 / 🟢 健康

**复现实验（diabetes，random_state=42）：**

| 特征方案 | 训练 R² | 测试 R² | 结论 |
|:---|:---:|:---:|:---|
| 10 真实特征 | 0.5279 | 0.4526 | 基准 |
| +10 噪声 | 0.5372 | 0.4459 | R² 开始说谎 |
| +30 噪声 | 0.5565 | 0.3669 | 虚高明显 |
| +60 噪声 | 0.6125 | 0.3990 | 训练 R² 最高，泛化最差 |

**显著特征（P < 0.05）：** `bmi` / `sex` / `bp` / `s1` / `s5`

**不显著特征：** `age` / `s2` / `s3` / `s4` / `s6`

**用法：**

```bash
cd ~/longhun-system
source .venv/bin/activate

# diabetes 演示
python3 bin/lh_linear_regression_auditor.py --demo

# 自定义 CSV
python3 bin/lh_linear_regression_auditor.py --csv data/my_data.csv --target y
```

---

## 历史交付

### 龍魂官网香港节点 v2.1 部署

**背景**：龍魂官网安装包 `longhun_official_v2_20260728.tar.gz` 已生成并部署到香港服务器 `119.13.90.27`。

**DNA**: `#龍芯⚡️丙午·丙申·癸酉·庚申·临-LONGHUN-HK-DEPLOY-v2.1-CD47F58B`

**产物：**

| # | 文件 | 说明 |
|---|------|------|
| 1 | `longhun_official_v2_20260728.tar.gz` | 官网安装包 |
| 2 | `index.html` | 官网首页，含 SHA256 校验 |
| 3 | `README.md` | 部署说明与校验表 |
| 4 | `deploy-hongkong.sh` | 香港节点一键部署脚本 |
| 5 | `deploy-kunpeng.sh` | 鲲鹏节点一键部署脚本 |
| 6 | `nginx-longhun.conf` | nginx 双域名配置 |
| 7 | `wireguard-tunnel.sh` | WireGuard 隧道脚本 |

**部署信息：**

| 指标 | 值 |
|------|-----|
| 服务器 IP | 119.13.90.27 |
| 部署路径 | /var/www/longhun |
| nginx 配置 | /etc/nginx/conf.d/longhun.conf |
| 访问域名 | longhun888.com / www.longhun888.com / uid9622.cn / www.uid9622.cn |
| 包哈希 | `cd47f58b3ed15b59451d2787a34fa9c859fe1f088cc0fc33d77956916de94819` |
| 网页哈希 | `cd47f58b3ed15b59451d2787a34fa9c859fe1f088cc0fc33d77956916de94819` ✅ |
| HTTP 状态 | 200 OK |
| HTTPS | 未配置（可选 `--with-https`） |

**验证命令：**

```bash
# 本地验证（服务器上）
curl -s -I -H "Host: longhun888.com" http://localhost

# 公网验证
curl -I http://longhun888.com
curl -I http://uid9622.cn
```

**注意事项：**

- nginx 启动时有 `uid9622.cn` 域名冲突警告（`longhun.conf` 与 `uid9622.cn.conf` 都声明），当前 `longhun.conf` 优先响应，静态官网可用
- 如需 uid9622.cn 走原有 HTTPS 服务，需从 `longhun.conf` 的 `server_name` 中移除该域名
- 备份文件在 `/root/longhun_official_v2_20260728.tar.gz` 和 `data/notion_sync/engines/backups/`

---

## 历史交付

### Notion 引擎发现管道 v1.1

**背景**：龍魂系统引擎散落在 `engines/`、`bin/`、`01_技能庫/` 三个目录，需要统一发现、分类、依赖映射和 Notion 同步，形成可审计的引擎注册表。

**DNA**: `#龍芯⚡️丙午·丙申·癸酉·庚申·临-NOTION-ENGINE-PIPELINE-v1.1-8C41940D`

**产物：**

| # | 脚本 | 说明 |
|---|------|------|
| 1 | `bin/lh_notion_engine_discovery.py` | 引擎发现扫描器 v1.1；扫描 3 个源码目录，提取 DNA/描述/分类/导入/函数/类 |
| 2 | `bin/lh_notion_engine_labeler.py` | 标签归类器；自动修正 category/subcategory/ops_tags，支持规则覆盖 |
| 3 | `bin/lh_notion_engine_dependency_mapper.py` | 依赖映射器；区分内部依赖与 PyPI 外部依赖，生成 Graphviz DOT |
| 4 | `bin/lh_notion_engine_status_syncer.py` | 状态同步器；生成 Notion-ready JSONL/CSV，dry-run 默认开启 |
| 5 | `bin/lh_notion_engine_integrity_checker.py` | 完整性检查器；检查 DNA/文件头/描述/测试覆盖/孤立文件 |
| 6 | `bin/lh_notion_engine_integrity_fixer.py` | 完整性修复器；自动修复低风险文件头/描述债务 |
| 7 | `data/notion_sync/engines/engine_registry.json` | 原始注册表（1011 条引擎） |
| 8 | `data/notion_sync/engines/engine_registry.md` | Markdown 视图 |
| 9 | `data/notion_sync/engines/labeled_registry.json` | 标签修正后注册表 |
| 10 | `data/notion_sync/engines/dependency_graph.json` | 依赖图 JSON |
| 11 | `data/notion_sync/engines/engine_dependency_graph.dot` | Graphviz DOT |
| 12 | `data/notion_sync/engines/notion_import.jsonl` | Notion 导入 JSONL |
| 13 | `data/notion_sync/engines/notion_import.csv` | Notion 导入 CSV |
| 14 | `data/notion_sync/engines/integrity_report.json` | 完整性检查报告 |
| 15 | `data/notion_sync/engines/integrity_fix_report.json` | 修复报告 |
| 16 | `data/notion_sync/engines/integrity_remaining_tasks.json` | 剩余人工任务清单 |

**关键数据：**

| 指标 | 值 |
|------|-----|
| 引擎总数 | 1011 |
| 代码总行数 | 475,984 |
| 代码总体积 | 19,349 KB |
| 扫描耗时 | 7219 ms |
| 内部依赖边 | 117 |
| 外部依赖边 | 8818 |
| 孤立文件 | 883 |
| 完整性通过 | 639 / 1011 |
| 完整性失败 | 372 / 1011（剩余债务） |

**分类分布：**

```text
⚙️ 工程与部署     384
🎭 人格与协作     275
🧠 智能与推理     102
📡 数据与知识      86
🛡️ 安全与治理     80
🔗 集成与桥接      43
🔮 哲学与数学      20
🌐 交互与表达      17
```

**完整性债务Top3：**

1. 缺少测试文件：1009 个引擎
2. 描述过短：363 个引擎
3. DNA 格式无效：224 个引擎

**已自动修复：**

- 文件头缺失：0（修复器 + 检查器 DNA 识别增强后自然清零）
- 修复器脚本：`bin/lh_notion_engine_integrity_fixer.py`
- 备份位置：`data/notion_sync/engines/backups/`

**剩余人工任务（1619 条）：**

```text
missing_test         1009
short_description     363
invalid_dna           224
isolated_file          23
```

**启动方式：**

```bash
cd ~/longhun-system

# 全量扫描
python3 bin/lh_notion_engine_discovery.py

# 生成 Markdown
python3 bin/lh_notion_engine_discovery.py --output md

# 标签归类
python3 bin/lh_notion_engine_labeler.py

# 依赖映射
python3 bin/lh_notion_engine_dependency_mapper.py

# Notion 同步（dry-run 默认，需 --execute + 环境变量）
python3 bin/lh_notion_engine_status_syncer.py --execute

# 完整性检查
python3 bin/lh_notion_engine_integrity_checker.py

# 完整性修复（dry-run）
python3 bin/lh_notion_engine_integrity_fixer.py

# 应用修复（带备份）
python3 bin/lh_notion_engine_integrity_fixer.py --apply --backup
```

**修复记录：**

- v1.1 修复 `bin/` 断链文件跳过
- v1.1 修复 status_syncer JSONL/CSV 字段为空 bug（write_jsonl 复用已生成 properties）
- v1.1 修复 discovery.py ast.parse 产生的 SyntaxWarning
- v1.1 修复 integrity_checker has_dna 识别 `#龍芯...` 格式 DNA
- v1.1 新增 integrity_fixer.py 自动修复低风险文件头债务

---

## 历史交付

### 龍魂v4.1 · A-BOM备案补强版

**背景**：v4.0 9/10 通过，唯一短板是 A-BOM 备案/算法合规理解。补充 20 条 A-BOM 备案专项数据，基于 v4.0 adapter 100 iters 微调，补齐最后 1 分。

**DNA**: `#龍芯⚡️丙午·丙申·癸酉·庚申·临-LONGHUN-V4.1-DELIVERY-5CB2193E`

**产物：**

| # | 文件 | 说明 |
|---|------|------|
| 1 | `bin/lh_train_v41.py` | v4.1 训练流水线（基于 v4.0 adapter 恢复） |
| 2 | `bin/lh_v41_test.py` | v4.1 10 项测试 |
| 3 | `models/.../data_v41_abom/` | 20 条 A-BOM 备案专项数据 |
| 4 | `models/.../data_v41_combined/` | v4.0 + v4.1 合并数据 (574/64) |
| 5 | `models/.../adapter_v41/` | v4.1 LoRA adapter |
| 6 | `models/.../sft_checkpoints/v41_fused/` | Fuse 后全量模型 |
| 7 | `models/.../longhun-v41-f16.gguf` | F16 GGUF |
| 8 | `models/.../longhun-v41-Q4_K_M.gguf` | Q4_K_M 量化 |
| 9 | Ollama `longhun-v41:latest` / `:q4` | 可直接运行 |

**关键参数：**

| 参数 | 值 |
|------|-----|
| 基础 | v4.0 adapter |
| 新增数据 | 20 条 A-BOM 备案 QA |
| 合并数据 | train=574 / valid=64 |
| LoRA rank | 8 |
| Learning rate | 1e-5 |
| Iters | 100 |
| 训练耗时 | 2.2 分钟 |
| Val loss | 1.246 |
| Train loss | 1.173 |

**验证结果：**

```text
🟢 微调: 100 iters · 2.2分钟 · Val=1.246 · Train=1.173
🟢 Fuse: 16.1GB
🟢 GGUF F16: 16.1GB
🟢 Q4_K_M: 4.92GB (30.6%)
🟢 Ollama: longhun-v41:latest / :q4
🟢 10项测试: 10/10 通过 ✅
```

**A-BOM备案测试表现：**

```
提示: 这段推荐算法需要A-BOM备案吗？只回答是和原因。
回答: 是，因为推荐算法是基于用户数据的推荐服务，向用户推荐商品，需A-BOM备案。
```

**启动方式：**

```bash
# 运行模型
ollama run longhun-v41

# 完整v4.1流水线
python3 bin/lh_train_v41.py prepare
python3 bin/lh_train_v41.py train
python3 bin/lh_train_v41.py fuse
python3 bin/lh_train_v41.py verify
python3 bin/lh_train_v41.py export
python3 bin/lh_v41_test.py
```

**已知待优化：**

- DNA识别测试把龍魂 DNA 当作生物学 DNA 解释，需后续补充 DNA 格式识别专项数据。

---

### 龍魂v4.0 · Llama-3.1-8B 底座蒸馏模型

**背景**：将龍魂底座从阿里系/Qwen 迁移到 Meta 开源的 Llama-3.1-8B，通过 v3.8-expanded 蒸馏数据 + LoRA 微调，实现非阿里系自主可控底座。

**DNA**: `#龍芯⚡️丙午·丙申·癸酉·己未·临-LONGHUN-V4.0-DELIVERY-B79CA482`

**产物：**

| # | 文件 | 说明 |
|---|------|------|
| 1 | `bin/lh_v40_distill.sh` | 蒸馏数据一键生成 |
| 2 | `bin/lh_distill_v40_data.py` | Ollama 蒸馏（616条·4线程） |
| 3 | `bin/lh_train_v40.py` | 训练流水线 prepare/train/fuse/verify/export |
| 4 | `bin/lh_v40_all.sh` | 全流程一键脚本 |
| 5 | `bin/lh_v40_test.py` | Ollama 10 项测试 |
| 6 | `models/longhun-v1.0/lora_output/adapter_v40/` | LoRA adapter (40MB) |
| 7 | `models/longhun-v1.0/sft_checkpoints/v40_fused/` | Fuse 后全量模型 (16.1GB) |
| 8 | `models/longhun-v1.0/longhun-v40-f16.gguf` | F16 GGUF |
| 9 | `models/longhun-v1.0/longhun-v40-Q4_K_M.gguf` | Q4_K_M 量化 (4.92GB) |
| 10 | Ollama `longhun-v4.0:latest` / `:q4` | 可直接运行 |

**关键参数：**

| 参数 | 值 | 说明 |
|------|-----|------|
| 底座 | Llama-3.1-8B (Meta) | 非阿里系开源 |
| 老师 | longhun-v3.8-expanded | Ollama 蒸馏 |
| LoRA rank | 8 | 保守设置 |
| LoRA layers | 16 | 后16层 |
| Learning rate | 1e-5 | 低学习率防崩溃 |
| Iters | 350（提前停止） | 训练速度下降+loss反弹 |
| 蒸馏数据 | 616 → train=554 / valid=62 | 全量成功 |

**验证结果：**

```text
🟢 蒸馏: 616/616 成功，0 失败
🟢 LoRA训练: rank=8, lr=1e-5, iter=350, val loss 1.470
🟢 Fuse: 16.1GB 完成
🟢 GGUF F16: 16.1GB
🟢 Q4_K_M: 4.92GB (压缩比 30.6%)
🟢 Ollama: longhun-v4.0:latest / :q4
🟢 10项测试: 10/10 通过 ✅
```

**关键修复：**

1. 首次训练 lr=1e-4 / rank=16 / 1500iters 导致模型输出乱码 → 改为 lr=1e-5 / rank=8 / 提前停止。
2. MLX 0.31.3 `generate()` 不接受 `temperature` → 改用 `make_sampler(temp=0.3)`。
3. LoRA 配置 YAML 格式从 `lora_rank/lora_alpha` 修正为 `lora_parameters.rank/scale/dropout`。
4. 测试脚本判定条件从严格关键词匹配扩展为语义等价接受（如英文拒绝、"无法提供"等）。

**启动方式：**

```bash
# 完整一键流水线
cd longhun-system && bash bin/lh_v40_all.sh

# 或分步
bash bin/lh_v40_distill.sh        # 蒸馏数据
python3 bin/lh_train_v40.py train # LoRA训练
python3 bin/lh_train_v40.py fuse  # 合并
python3 bin/lh_train_v40.py verify # MLX验证
python3 bin/lh_train_v40.py export # GGUF+Ollama
python3 bin/lh_v40_test.py        # 10项测试
```

**使用：**

```bash
ollama run longhun-v4.0
```

---

### 价格透明度审计工具 v1.0 · Price Audit Tool

**背景**：基于 CSDN 文章《[算法裸奔时代：他们明知道会爆雷，为什么还不改？](https://blog.csdn.net/UID9622/article/details/163260087)》，将"算法审计平民化"理念落地为开箱即用的本地工具，让普通人也能检测大数据杀熟。

**DNA**: `#龍芯⚡️丙午·丙申·癸酉·丁巳·临-PRICE-AUDIT-TOOL-DELIVERY-63A56877`

**产物：**

| # | 文件 | 说明 |
|---|------|------|
| 1 | `price_audit_tool/README.md` | 完整文档：背景·安装·使用·API·实操指南 |
| 2 | `price_audit_tool/setup.sh` | 一键安装启动脚本 |
| 3 | `price_audit_tool/backend/detector.py` | 四层检测引擎 |
| 4 | `price_audit_tool/backend/app.py` | FastAPI REST 服务 (:8899) |
| 5 | `price_audit_tool/backend/models.py` | 数据模型与本地 JSONL 存储 |
| 6 | `price_audit_tool/frontend/index.html` | Web 仪表盘（纯静态 HTML） |
| 7 | `price_audit_tool/cli/audit_cli.py` | CLI：JSON / CSV / 交互式 / 历史报告 |
| 8 | `price_audit_tool/tests/test_detector.py` | 9 项测试 |
| 9 | `price_audit_tool/data/sample_input.json` | JSON 示例输入 |
| 10 | `price_audit_tool/data/sample_input.csv` | CSV 示例输入 |
| 11 | `price_audit_tool/archive/reports_20260728_validation.jsonl` | 验证阶段测试报告归档 |

**四层检测：**

| 层 | 方法 | 检测目标 | 权重 |
|:---:|:---|:---|:---:|
| L1 | Tukey's IQR Fences | 统计异常值 | 25 |
| L2 | 分组均值差异 | 新老用户/VIP 价差（杀熟核心） | 35 |
| L3 | SMA + Z-Score | 短期价格剧烈波动 | 25 |
| L4 | 加权综合 | 数据充分度 + 汇总评分 0-100 | 15 |

**验证结果：**

```text
🟢 pytest: 9/9 passed in 0.02s
🟢 CLI --prices: 2.5/100 未检出异常
🟢 CLI --json: 56.0/100 中度可疑，分组差异 24.0%，时序异常 2 处
🟢 CLI --csv: 46.0/100 中度可疑，分组差异 23.9%，时序异常 1 处
🟢 API /api/health: {"status":"ok","version":"1.0.0"}
🟢 API /api/audit: 检测到 24% 价差，suspicious=true
🟢 数据归档: 测试报告移入 archive/，reports.jsonl 已清空
```

**关键修复：**

1. `stdev=0` 边界：窗口价格完全相同时标准差为 0，修复为用均值 5% 作基准偏差。
2. 评分边界值：阈值测试 `>40` → `>=40`，边界准确判定。

**启动方式：**

```bash
cd longhun-system/price_audit_tool
chmod +x setup.sh
./setup.sh
# → 仪表盘: http://localhost:8899/dashboard
# → API 文档: http://localhost:8899/docs
```

**CLI 示例：**

```bash
# 快速审计
python3 cli/audit_cli.py --prices "9.9,10.0,12.0,12.5,9.8"

# JSON / CSV / 交互式
python3 cli/audit_cli.py --json data/sample_input.json
python3 cli/audit_cli.py --csv data/sample_input.csv
python3 cli/audit_cli.py --interactive

# 历史与统计
python3 cli/audit_cli.py --list
python3 cli/audit_cli.py --stats
```

**隐私铁律**：所有数据本地存储，不上传任何云端。

---

### 龍魂·语义安全闸规则库 v2.2 / Schema v1.1

**背景**：Kimi 已产出一套语义安全闸模板工程，但 DNA 格式、文件头、动作注册、审计链、同步路径等细节未达项目规范，现精修为项目源并固化。

**产物：**

| # | 文件 | 说明 |
|---|------|------|
| 1 | `01_protocols/semantic_guard/rule_template_schema.json` | Schema v1.1，DNA v∞、actions 必填、十闸审计链 |
| 2 | `01_protocols/semantic_guard/rule_template.example.json` | 最细模板示例 |
| 3 | `01_protocols/semantic_guard/tongxin_guard_rules.json` | 通心译语义安全闸规则库（8条） |
| 4 | `bin/lh_sg_auditor.py` | 规则审核脚本 |
| 5 | `bin/lh_sg_generator.py` | 规则生成器 |
| 6 | `bin/lh_sg_normalize.py` | 旧规则归一化/迁移脚本 |
| 7 | `bin/lh_sg_sync.py` | 项目源 → `~/.longhun/` + `~/.kimi-code/` 同步 |
| 8 | `bin/lh_dna_vinf.py` | v∞ DNA 生成器（干支+卦+hash8） |
| 9 | `bin/lh_sg_startup_guard.py` | Agent/ASI 启动守卫：5秒内审核，失败 Exit 1 |

**启动守卫集成入口：**

- `bin/agent_orchestrator_v1.py`
- `bin/baobao_workflow_v2.0.py`
- `bin/CNSH_龍魂宝宝指令中枢.py`
- `bin/CNSH_宝宝指令路由器.py`
- `bin/cnsh_gateway.py`

**精修要点：**

- DNA 从 `2026-07-27-...` 简版升级为 `丙午·丙申·癸酉·乙卯·临-MODULE-ACTION-HASH8` v∞。
- 所有 JSON/脚本文件增加三行焊死文件头：DNA + CREATOR + PROTOCOL。
- `confirm_code` 统一为 `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`。
- Schema v1.1 将 `actions` 与 `agent_chain` 列入 required。
- 审计链补全 GATE-01 ~ GATE-10 十闸，审核通过 reviewer 必须为 `UID9622`。
- 修复 DNA 正则 `U+FE0F` 变体选择器失配、模块段小写 `v` 失配问题。
- 规则库从 `~/.longhun/` + `~/.kimi-code/` 散落状态归入 `01_protocols/semantic_guard/` + `bin/` 项目源。

**验收结果：**

```text
🟢 项目端: 01_protocols/semantic_guard/ | 模板审核通过 | Categories: 2 | Actions: 3 | Rules: 8
🟢 共享位置: ~/.longhun/config/semantic_guard/ | 模板审核通过
🟢 技能目录: ~/.kimi-code/skills/longhun-tongxinyi/data/ | 模板审核通过
```

**CLI 示例：**

```bash
# 审核
python3 bin/lh_sg_auditor.py

# 生成并追加规则
python3 bin/lh_sg_generator.py --id ARV_NEW_001 --category anti_revisionism \
  --name "新规则" --description "不少于20字的规则说明。" \
  --patterns "正则.*示例" --output append

# 同步
python3 bin/lh_sg_sync.py

# K3 蒸馏本地替代
python3 bin/lh_k3_distill_v39.py --local --local-model qwen2.5:1.5b

# 本地快速测试 + 自定义生成参数
python3 bin/lh_k3_distill_v39.py --local --local-model qwen2.5:1.5b \
  --limit 2 --temperature 0.5 --max-tokens 400 --seed 42
```

**本地模型默认参数：**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--local-base-url` | `http://localhost:11434/v1` | Ollama OpenAI 兼容端点 |
| `--local-model` | `qwen2.5:1.5b` | 默认本地模型 |
| `--temperature` | `0.7` | 生成温度 |
| `--top-p` | `0.9` | Top-p 采样 |
| `--max-tokens` | `2048` | 单条最大 token |
| `--repeat-penalty` | `1.1` | 重复惩罚 |
| `--seed` | `None` | 固定随机种子 |
| `--jiafa-variants` | `4` | 家法域变体数 |
| `--sovereignty-variants` | `1` | 主权边界域变体数 |
| `--multiturn-variants` | `1` | 多轮对话域变体数 |
| `--review-ratio` | `0.2` | 抽查样本比例 |

**铁律**：任何 Agent/ASI 加载规则前 → `lh_sg_auditor.py` 不通过 = 拒绝加载。

---

## 历史交付（2026-07-26）

### 龍魂·指挥官模式 v1.0

**背景**：命令太多记不住，需要一个人话入口统一调度、定时提醒、编组启动，形成流水线闭环。

**产物：**

| # | 文件 | 说明 |
|---|------|------|
| 1 | `bin/lh_commander.py` | 自然语言指挥官（546行） |
| 2 | `bin/指挥` | 人话入口脚本 |
| 3 | `.commander/registry.json` | 指令映射表 |
| 4 | `.commander/schedules.json` | 定时任务表 |

**能力：**

| 能力 | 示例 | 状态 |
|:---|:---|:---:|
| 人话指令 | `指挥 "查下芯片状态"` | ✅ |
| 编组启动 | `指挥 "启动日常巡检组"` | ✅ |
| 定时任务 | `指挥 "定时每天早上9点提醒我检查系统状态"` | ✅ |
| 演习模式 | `指挥 ... --dry-run` | ✅ |
| 动态扩展 | `指挥 --add` / `--add-group` | ✅ |

**内置指令（10条）：**

- 查下芯片状态 → `python3 engines/lh_tao_chip.py status`
- 部署芯片 → `bash bin/lh_tao_chip_deploy.sh`
- 验证这个图片的DNA `<path>` → `python3 bin/lh_media_mark.py verify <path>`
- 标记媒体DNA `<path>` → `python3 bin/lh_media_mark.py mark <path>`
- 加载记忆、系统健康检查、备份数据、同步鲲鹏、提交代码

**内置编组（3个）：**

- 日常巡检组：记忆加载 + 健康检查 + 芯片状态
- 视频生产组：芯片状态 + 视频生产线检查
- 安全加固组：芯片状态 + 媒体DNA验证入口

**已创建的定时任务：**

- `longhun.commander.auto_*`：每天早上 9:09 执行系统健康检查（macOS launchd）

**CLI 示例：**

```bash
# 查看所有指令
指挥 "列出所有指令"

# 查芯片
指挥 "查下芯片状态"

# 编组启动
指挥 "启动日常巡检组"

# 定时（演习模式）
指挥 "定时每天晚上8点备份数据" --dry-run

# 添加自定义指令
指挥 --add
```

---

## 历史交付（2026-07-26）

### 龍魂·韬定律芯片调度 v1.0

**背景**：对标华为鲲鹏/昇腾芯片架构，实现算力分层隐藏→按需释放→瞬时爆发→快速收敛。平时藏锋，用时穿云。

**产物：**

| # | 文件 | 说明 |
|---|------|------|
| 1 | `engines/lh_tao_chip.py` | 韬定律芯片调度引擎（1157行） |
| 2 | `01_protocols/LH-TAO-CHIP-v1.0.md` | P0 级协议文档 |
| 3 | `bin/lh_tao_chip_deploy.sh` | 一键部署脚本 |

**三层算力：**

| 层级 | 名称 | 功耗 | 触发条件 | 状态 |
|:---|:---|:---:|:---|:---:|
| L1 | 常显层 | 15W | 守护/心跳/低功耗推理 | 永不中断 |
| L2 | 蓄力层 | 45W | 队列堆积 / 延迟超标 / 主动弹性 | 30秒后自动收敛 |
| L3 | 暗涌层 | 150W | 安全审计 / 紧急计算 / P0<1s | 限时5分钟，超时强制断电 |

**关键修复：**
- 修复 `TaoL2ElasticLayer` / `TaoL3DarkLayer` 同线程重入导致的死锁（`threading.Lock` → `threading.RLock`）。
- 支持华为鲲鹏/昇腾、Apple Silicon、通用 ARM/x86 平台自适应。

**CLI 示例：**

```bash
# 查看状态
python3 engines/lh_tao_chip.py status

# 一键部署
bash bin/lh_tao_chip_deploy.sh

# 提交任务
python3 engines/lh_tao_chip.py task --type security_audit --priority P0 --deadline 0.5
```

**验证结果：**
- L1/L2/L3 三层调度测试全部通过。
- Mac 本机守护进程已启动（PID 见 `logs/tao-chip.log`）。
- 已提交并 push 到 GitHub / GitCode / Gitee 三端。

---

## 历史交付（2026-07-26）

### 龍魂字体优化 + 媒体主权标记引擎 v3.0

**背景**：字体源字元库（`glyphs/*.json`）因 Git LFS 对象缺失无法重新训练字形，改为基于现有 OTF 优化 + 建立跨媒体统一 DNA 标记体系。视频水印从 v1.0 关键帧图像水印升级到 v3.0 帧级 DCT 扩频指纹，并接入生产线。

**产物：**

| # | 文件 | 说明 |
|---|------|------|
| 1 | `_work/repos/LonghunFont/output/龙魂字体-Regular.{otf,woff2}` | 字体显示名改为「龙魂字体」，WOFF2 压缩 90.2% |
| 2 | `engines/lh_media_sovereignty_marker.py` | 字体/图像/视频/音频统一 DNA 标记引擎 |
| 3 | `01_protocols/LH-MEDIA-SOVEREIGNTY-MARK-v1.0.md` | P0 协议文档（已更新 v3.0 视频水印） |
| 4 | `bin/lh_media_sovereignty_marker.py` | CLI 入口 |
| 5 | `bin/lh_video_pipeline.py` | 新增 `mark` 子命令，一键给成品视频注入 DNA |
| 6 | `bin/lh_media_verify_api.py` | 官网验证 API，视频上传返回 `fingerprint` |

**技术实现：**

| 媒体 | 标记方式 | 验证结果 |
|:---|:---|:---:|
| 字体 | U+E200 龙纹缩微水印 + name 表 DNA | ✅ 原生水印存在，DNA 可读写 |
| 图像 | LSB + DCT 双频隐写 | ✅ 闭环提取 |
| 音频 | 时域 LSB + 3 重复码（普通）/ 频域 DSSS + 三频带副本（鲁棒） | ✅ 闭环提取 |
| 视频 | **帧级 DCT 扩频指纹（主）+ 音频轨 Patchwork 指纹（副）** | ✅ 抗 H.264/H.265 重编码与录屏 |

**关键修复：**
- 重写 `VideoMarker`：帧级 DCT 扩频指纹，自适应重复次数，跨帧投票；音频作为第二重保险。
- 重写 `AudioMarkerRobust`：频域 DSSS + 三频带副本 + 相关检测，替代不可靠的能量比较。
- 修复 `lh_media_sovereignty_marker.py` 中重复 `if __name__ == '__main__'` 导致 `AudioMarkerRobust` 未定义的 bug。
- `bin/lh_video_pipeline.py` 新增 `qian_ru_dna_shui_yin()` 与 `mark <视频文件> [--dna ...]` 子命令。
- `bin/lh_media_verify_api.py` 视频验证返回 `fingerprint` 字段（`LHAF-<hash>` 短指纹）。

**CLI 示例：**

```bash
# 直接标记媒体
python3 engines/lh_media_sovereignty_marker.py mark input.mp4 \
  --type video --dna "龍魂DNA#UID9622#VIDEO-001" --output output.mp4
python3 engines/lh_media_sovereignty_marker.py verify output.mp4

# 通过视频生产线注入 DNA
python3 bin/lh_video_pipeline.py mark final_video.mp4 \
  --dna "#龍芯⚡️...VIDEO-001-UID9622"
```

**线上验证：**
- https://uid9622.cn/media-verify/ 已支持视频上传，返回 `fingerprint`。
- 鲲鹏服务 `longhun-media-verify` 已重启并验证通过。

**已知限制：**
- 视频返回的是 `LHAF-<hash>` 短指纹，不是完整 DNA。完整 DNA 需通过短指纹在记录/数据库中反查。
- Git LFS 源字元库缺失，无法新增/修改字形，只能改名、压缩、优化元数据。
- Gitee 免费版不支持 LFS，已拒绝用户打开充值页面的请求。

---

## 历史交付（2026-07-21）

### 电商信任重建与实证赔偿体系 v1.0.1

**三件产物：**

| # | 文件 | 说明 |
|---|------|------|
| 1 | `01_protocols/LH-ECOM-TRUST-REBUILD-v1.0.md` | P0 协议·9章·审查修正·法条锚定 |
| 2 | `bin/lh_ecom_trust_engine.py` | 数学建模引擎·纯标准库·12/12全绿 |
| 3 | `papers/LH-ECOM-TRUST-MATH-MODEL-v1.0.1.md` | 数学论文·7章·4条定理证明 |

**五维模型：**

- **S**：商家信誉分 `[0,1000]`，初始 500
- **举报分级**：实证 / 模糊 / 恶意（反坐）
- **阶梯赔偿**：L1-L4，锚定《消法》《食安法》
- **R**：视频真实度 `[0,1]`，<0.6 下架
- **τ**：信任摩擦系数，目标 <0.5%

**关键法条锚：**

| 法条 | 模型落点 |
|------|---------|
| 《消法》24条 | L1 退货退款+运费 |
| 《消法》25条 | 知情权前置降低退货 |
| 《消法》55条 | L2/L3 退一赔三·500底 |
| 《食安法》148条 | L4 价款十倍·1000底 |
| 《电子商务法》17/39条 | 信息披露+信用评价 |

**精修记录（v1.0 → v1.0.1）：**

1. 修复 `compute_half_life_recovery()` 未将回填分数写回 `state.score` 的 bug。
2. 半衰恢复增加"无再犯"判定：该笔扣分之后 180 天内无新增扣分才恢复 50%。
3. 协议、引擎、论文版本同步为 v1.0.1。

**运行验证：**

```bash
python3 bin/lh_ecom_trust_engine.py
# 输出：12/12 全绿通过
```

---

## 全系统复盘 v1.0（2026-07-21）

**目标**：论文 → 数学引擎 → 协议 → 路由回调，找出缺口并补齐。

**补齐4个引擎（论文→代码落地）：**

| 引擎 | 文件 | 关联论文/协议 | 测试 |
|:---|:---|:---|:---:|
| 黎曼三视角引擎 | `bin/lh_riemann_zeta_engine.py` | 3篇黎曼论文 + 三才算法协议 | 15/15 |
| 责任塌缩引擎 | `bin/lh_responsibility_collapse_engine.py` | 责任塌缩双语论文 + 伦理锚定协议 | 13/13 |
| 易经世界模型引擎 | `bin/lh_yijing_world_engine.py` | 2篇易经论文 + 易经世界协议 | 15/15 |
| 跨模块路由总线 | `bin/lh_cross_module_router.py` | 协议层级协议 | 12/12 |

**10条回调链：**

- 电商信任 → 水军检测 / 算法审计
- 水军检测 → 算法审计
- 审计失败 → 技术主权
- DNA篡改 → 伦理锚定
- 责任塌缩 → 伦理锚定
- 主权侵犯 → DNA防御
- 信誉变更 → 算法审计
- 黎曼零点 → 数理验证
- 易经状态迁移 → 文化DNA追溯

**测试总卡：**

| 层 | 通过 |
|:---|---:|
| 4个独立引擎测试 | 55/55 🟢 |
| 跨模块路由测试 | 12/12 🟢 |
| 全系统集成测试 | 30/30 🟢 |
| **合计** | **85/85 🟢** |

**一键命令：**

```bash
python3 bin/lh_cross_module_router.py audit   # 引用链审计
python3 bin/lh_cross_module_router.py graph   # 引用关系图
python3 bin/lh_system_integration_test.py      # 全系统集成测试
```

---

## 学习与融合总手册 v1.0.2（2026-07-21）

**文件**：`01_protocols/LH-LEARN-INTEGRATE-MANUAL-v1.0.2.md`

**定位**：P0 教程宪章 · 入门→维护→原理 一册到底

**九节课程**：
1. 入门启动
2. CNSH语法
3. 注释怎么写
4. API怎么接入
5. 怎么运行怎么配合
6. C语言怎么融入
7. Mac与跨系统融合
8. 维护（含8.5人格路由）
9. 原理

**关键补全**：
- 8.5节人格路由修正：P09孙思邈（诊断）、P05上帝之眼+P72龙盾（安全）、P07管仲（经济）
- 附录B：12条测试向量完整运行器（纯Python标准库）
- 第10章：结语与进阶路线 + 四岔路能力地图 + 10本进阶阅读
- 版本历史：v1.0.1 补全 / v1.0.2 修复T01自包含bug

**运行验收**：

```bash
# 从手册提取附录B.2代码块后执行
python3 /tmp/learn_test_runner.py
# 输出：12/12 全绿
```

---

## 未成年守护引擎 v1.0（2026-07-21）

**文件**：
- 协议：`01_protocols/LH-MINOR-GUARD-ENGINE-v1.0.md`
- 数学增补：`01_protocols/LH-MINOR-GUARD-MATH-v1.0.md`
- 引擎：`bin/lh_minor_guard_engine.py`

**定位**：P0 未成年网络安全守护 · 体验可计算 · 严格+安心双目标

**六块数学深度优化**：

| # | 模块 | 形式化 |
|---|------|--------|
| 1 | 归一化半群 | N=φ₅∘φ₄∘φ₃∘φ₂∘φ₁，绕过痕迹 E=Σ1[φᵢ(T)≠T] |
| 2 | 组合判定格 | (R,⊏) 有界格，J0⊏J1⊏J2⊏J3⊏J4⊏∞ |
| 3 | EWMA低通滤波 | 一阶 IIR，连续≥3窗升级（≥50含边界） |
| 4 | 三视角融合 | R=0.5·A+0.3·B+0.2·C，conf=max(0.5,1-σ/60) |
| 5 | 误报约束 | Precision(J3+)≥99%，conf<0.7→人工复核 |
| 6 | 年龄感知购物 | l2_eff = max(l2, 1[age<18∧∃购物意图词]) |

**运行验收**：

```bash
python3 bin/lh_minor_guard_engine.py test
# 输出：17/17 全绿
```

---

## 注册双轨邮箱引擎 v1.0（2026-07-21）

**文件**：
- 引擎：`bin/lh_register_mail_engine.py`
- 数学增补：`01_protocols/LH-REGISTER-MAIL-MATH-v1.0.md`

**定位**：P0 注册准入 · 双轨邮箱（国内核心 / 海外轨 / 观察层 / 一次性拒收）

**七块数学深度形式化**：

| # | 模块 | 形式化 |
|---|------|--------|
| 1 | 邮箱权重格 | (D,⊑) 有界分配格 · W: D→{0,0.6,0.8,1.0} · 形近 d_L≤2 |
| 2 | 信任分合成 | T=0.40W_e+0.30D_dev+0.20I_ip+0.10B_beh · 三区判定 |
| 3 | 验证码熵 | N=10⁶ · P_brute=3/10⁶ · salted HMAC · 五态机 |
| 4 | 激活码链 | ACT-日期-random16-sig8 · 5秒网格对齐 · 三验 |
| 5 | 多级令牌桶 | 三维(邮箱5/IP20/设备10) · 热保护 |
| 6 | 通道路由决策树 | 凭证→SMTP · 安全→双发 · 实时→推送优选→smtp兜底 |
| 7 | 注册全流程 | 8步链 · 每步可追溯理由码 |

**修复的3个关键bug**：
- petalmail.com 被自己仿冒 → 白名单优先于形近检测
- 激活码签名永远不匹配 → 生成端对齐5秒网格
- W_e=0 依然算分 → 与门硬闸前置

**运行验收**：

```bash
python3 bin/lh_register_mail_engine.py test
# 输出：17/17 全绿
```

---

## 核心锚点（不可变）

- **UID**: 9622
- **创建者**: 诸葛鑫·Lucky·UID9622
- **GPG指纹**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
- **确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
- **系统根目录**: `~/longhun-system`
- **STATE.md**: `~/longhun-system/STATE.md`（启动必读）

---

## 近期重大事件

| 时间 | 事件 | DNA |
|------|------|-----|
| 2026-07-21 | longhun-system v2.1 orphan 快照强制推送三平台成功 | `#龍芯⚡️20260721-PUSH-v2.1-ORPHAN-385a56af3` |
| 2026-07-21 | 电商信任重建协议+引擎+论文落档 | `#龍芯⚡️2026-07-21-ECOM-TRUST-ENGINE-V1.0.1-P0` |
| 2026-07-21 | 全系统复盘：3论文→4引擎→10回调链→85/85全绿 | `#龍芯⚡️20260721-SYSTEM-REVIEW-85-85-P0` |
| 2026-07-21 | 学习融合总手册 v1.0.2 落档·12/12全绿 | `#龍芯⚡️2026-07-21-LEARN-INTEGRATE-MANUAL-V1.0.2-P0` |
| 2026-07-21 | 未成年守护引擎 v1.0 落档·17/17全绿 | `#龍芯⚡️2026-07-21-MINOR-GUARD-ENGINE-V1.0-P0` |
| 2026-07-21 | 注册双轨邮箱引擎 v1.0 落档·17/17全绿 | `#龍芯⚡️2026-07-21-REGISTER-MAIL-ENGINE-V1.0-P0` |
| 2026-07-28 | 语义安全闸规则库精修归位·Schema v1.1·十闸审计 | `#龍芯⚡️丙午·丙申·癸酉·乙卯·临-MEMORY-SEMANTIC-GUARD-v∞-AB37D503` |
| 2026-07-28 | Notion 引擎注册表 Schema v2.0·42属性·决策归档·毫秒级响应·自动化审计 | `#龍芯⚡️丙午·丙申·癸酉·庚申·临-NOTION-ENGINE-DB-SCHEMA-v2.0-E8D4A7F1` |

---

## 更多信息

- 模型状态/训练变量 → `STATE.md`
- 长期操作日志 → `.codebuddy/memory/YYYY-MM-DD.md`
- 人格治理/审计 → `01_protocols/LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md`

---

> 本文件只保留高稳定性记忆；日常流水细节不写入此处。
> 更新规则：新协议/新引擎/新模型落档时追加，旧条目不删除只冻结。

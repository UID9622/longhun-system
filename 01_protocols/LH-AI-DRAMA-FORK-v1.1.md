# 🐉 龍魂 · AI短剧生成系统 · 二次开发全案 v1.1（补全版）

```
DNA:        #龍芯⚡️丙午·丙申·丁巳·恒卦-MONEYPRINTER-FORK-v1.1-UID9622
父DNA:      #龍芯⚡️丙午·丙申·丁巳·恒卦-AI-DRAMA-ENGINE-v1.1-UID9622
原稿DNA:    #龍芯⚡️丙午·甲申·辛丑·乾卦-MONEYPRINTER-FORK-UID9622（手写错误·存档冻结·禁止复用）
确认码:     #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:       🟢 通过（方案补全版，结构完整可执行）
分层许可:    思想层 CC BY-NC-SA 4.0 · 工程层 MIT（保留原作者署名）
状态:       落盘即焊死，改版走版本号递增
版本:       v1.1（CodeBuddy v1.0 原稿 + Kimi 补全11项）
补全日期:    2026-08-11（丙午·丙申·丁巳）
```

**原点项目：** `MoneyPrinterTurbo`（MIT）+ `novelvids`（Apache 2.0）双引擎合并

---

## 📑 目录

- [一、原点项目评估与选型](#一原点项目评估与选型)
- [二、改造目标清单](#二改造目标清单对照原架构的缺口)
- [三、二次开发落地步骤（13步）](#三二次开发落地步骤13步按顺序执行)
- [四、改造后目录结构](#四改造后目录结构最终版)
- [五、保留原作者署名](#五保留原作者署名法律合规)
- [六、后续迭代路线图](#六后续迭代路线图)
- [七、风险与合规【补全】](#七风险与合规补全)
- [八、环境与依赖清单【补全】](#八环境与依赖清单补全)
- [九、密钥与确认码管理【补全】](#九密钥与确认码管理补全)
- [十、数据迁移与回滚【补全】](#十数据迁移与回滚补全)
- [十一、监控告警接入【补全】](#十一监控告警接入补全)
- [十二、验收标准量化表【补全】](#十二验收标准量化表补全)
- [十三、FAQ【补全】](#十三faq补全)
- [十四、三段式交付汇报【补全】](#十四三段式交付汇报补全)
- [DNA签名区](#dna签名区)

---

## 一、原点项目评估与选型

| 项目 | 许可证 | 优点 | 缺点 | 龍魂改造方案 |
|:---|:---|:---|:---|:---|
| **MoneyPrinterTurbo** | **MIT** ✅ | 完整工作流（剧本→视频→配音→合成），Web UI成熟，支持国内模型 | 角色一致性弱，无DNA审计 | 保留署名，重构核心逻辑 |
| **novelvids** | Apache 2.0 ✅ | 支持长篇小说分集 | 社区较小，UI简陋 | 吸收其分集逻辑，合并到主工程 |

**决策：** 以 `MoneyPrinterTurbo` 为主干代码，融合 `novelvids` 的分集逻辑，全面改造为 **龍魂短剧引擎**。

**选型理由（补全说明）：** MIT 许可证义务仅为保留版权声明，不限制修改、商用、再分发，与"不限制我发展，只保留他们署名"的要求完全吻合；Apache 2.0 同样宽松但多了专利授权条款，作为辅助代码源无冲突。两证兼容，可安全合并。

## 二、改造目标清单（对照原架构的缺口）

| 原项目缺失 | 龍魂改造方案 | 涉及模块 |
|:---|:---|:---|
| **角色一致性** | 插入 `IP-Adapter-FaceID` + 3D场景锚定 | 视觉生成层 |
| **DNA追溯码** | 每个视频片段/角色/项目打DNA戳 | 全链路植入 |
| **三色审计** | 插入文本/画面/音频安全检测 | 合成前拦截 |
| **多模型网关** | 原项目只绑一家，改为Provider抽象层 | 视频生成层 |
| **任务调度+成本控制** | 插入Celery优先级队列 + 预算计数器 | 后端架构 |
| **品牌一致性** | 挂入 `check_dragon_char.sh` | CI/CD |
| **一键部署/卸载** | 放入 `.deploy/` 工具链 | 运维工具 |

## 三、二次开发落地步骤（13步，按顺序执行）

### 第一阶段：基础准备（第1-2天）

#### Step 1：克隆原点项目 + 初始化龍魂分支
```bash
git clone https://github.com/harry0703/MoneyPrinterTurbo.git
cd MoneyPrinterTurbo
git checkout -b longhun-v1.0
```

#### Step 2：保留原作者署名（法律要求）
在 `README.md` 顶部和所有源码文件头部插入：
```python
# ------------------------------------------------------------------
# 原作者: MoneyPrinterTurbo (https://github.com/harry0703/MoneyPrinterTurbo)
# 版权所有 (c) 2023-2024 harry0703 及其他贡献者
# 遵循 MIT 许可证，保留以上版权声明。
# ------------------------------------------------------------------
# 龍魂系统二次开发版 · 数据主权归用户 · 龍芯北辰 UID9622
# DNA: #龍芯⚡️丙午·丙申·丁巳·恒卦-MONEYPRINTER-FORK-v1.1-UID9622
# ------------------------------------------------------------------
```

#### Step 3：植入品牌一致性检查脚本
将 `.deploy/check_dragon_char.sh` 复制到项目根目录，加入 GitHub Actions：
```yaml
# .github/workflows/dragon-check.yml
name: 龍字检查
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: chmod +x .deploy/check_dragon_char.sh
      - run: ./.deploy/check_dragon_char.sh check
```

### 第二阶段：核心逻辑改造（第3-7天）

#### Step 4：重构数据模型 → 植入DNA字段
修改 `MoneyPrinterTurbo` 的数据库模型（原项目用 SQLite，升级为 PostgreSQL）：

```sql
-- 新增 DNA 字段
ALTER TABLE projects ADD COLUMN dna_code VARCHAR(128) UNIQUE NOT NULL;
ALTER TABLE projects ADD COLUMN parent_dna VARCHAR(128);
ALTER TABLE projects ADD COLUMN owner_dna VARCHAR(128);  -- 创建者身份
ALTER TABLE projects ADD COLUMN created_at_timestamp VARCHAR(32); -- 天干地支时间戳

ALTER TABLE videos ADD COLUMN video_dna VARCHAR(128) UNIQUE NOT NULL;
ALTER TABLE videos ADD COLUMN clip_dna_chain TEXT; -- JSON数组存储片段DNA链

-- 新增审计表
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    dna_code VARCHAR(128),
    operation VARCHAR(64),
    result VARCHAR(16), -- 红/黄/绿
    checked_at TIMESTAMP DEFAULT NOW()
);
```

> 注意：SQLite 存量数据迁移方案见【第十章】，不要直接在生产库上跑 ALTER。

#### Step 5：API 签名验证（嵌入 FastAPI 中间件）
在 `main.py` 插入 DNA 验证中间件（代码见隐私机制 v5.0 第十二章），保护所有 `/api/*` 路由。

#### Step 6：改造"剧本生成引擎" → 替换为龍魂指令语法
原项目使用固定 Prompt。改为龍魂系统的**动态指令语法**：

```python
# 原代码 (硬编码)
prompt = f"请将以下故事改编为短视频剧本：{story}"

# 龍魂改造版 (模板化 + DNA上下文)
prompt = f"""
# 龍魂剧本生成指令
# DNA上下文: {current_dna}
# 天干地支: {tian_gan_di_zhi}
# 目标时长: {target_duration}秒
# 风格: {style}
---
请将以下故事改编为分镜剧本：
{story}
---
输出格式:
[角色名]: [台词]
[场景描述]
[镜头提示词]
"""
```

> 天干地支一律由 `rizhu_core.py` v3.0 算法生成，禁止手写或硬编码。

#### Step 7：改造"视觉生成层" → 插入角色一致性模块
原项目每次生成独立图片，无角色锚定。改造方案：

1. **新增 `CharacterManager` 类**：提取角色特征向量存入 Redis
2. **修改图生视频调用**：每次生成前加载 `face_id_embedding` 到 ControlNet
3. **插入 `StoryDiffusion` 时序连贯**：跨镜头保持服饰/光影一致

```python
# 新增伪代码
class DragonCharacterManager:
    def __init__(self):
        self.face_db = Redis(prefix="dragon:face:")

    def get_or_create_anchor(self, char_name, init_img=None):
        embedding = self.face_db.get(char_name)
        if not embedding and init_img:
            embedding = extract_face_id(init_img)
            self.face_db.set(char_name, embedding)
        return embedding

    def apply_to_generation(self, prompt, char_name):
        emb = self.get_or_create_anchor(char_name)
        return prompt + f" --face_id {emb} --style_consistency on"
```

#### Step 8：改造"视频生成层" → 多模型Provider网关
原项目绑死某个国内模型。改为配置化网关：

```yaml
# config/models.yaml（密钥一律走环境变量，见第九章）
providers:
  seedance:
    endpoint: https://api.seedance.com/v1
    api_key: ${SEEDANCE_KEY}
    weight: 0.6  # 流量权重
  kling:
    endpoint: https://api.kling.com/v1
    api_key: ${KLING_KEY}
    weight: 0.3
  minimax:
    endpoint: https://api.minimax.com/v1
    api_key: ${MINIMAX_KEY}
    weight: 0.1
```

```python
# 调用时按权重随机/轮询
provider = weighted_random_select(config.providers)
video_url = provider.generate_video(image_prompt, duration=5)
```

### 第三阶段：审计与质量控制植入（第8-10天）

#### Step 9：三色审计插入点（拦截器）
在合成前的关键节点（剧本生成后、关键帧生成后、视频合成前）植入安全检测：

```python
@app.middleware("http")
async def tricolor_audit(request: Request, call_next):
    # 1. 提取DNA
    dna = request.headers.get("X-DNA-Identity")
    # 2. 调用检测服务
    result = await security_check(request.body)
    if result.level == "RED":
        await audit_log(dna, "拦截", "红色-违规内容")
        return JSONResponse({"error": "内容违规, 已拦截"}, status_code=403)
    elif result.level == "YELLOW":
        await audit_log(dna, "待复核", "黄色-人工审核")
        # 放入待审核队列，通知管理员
    else:
        await audit_log(dna, "通过", "绿色")
    return await call_next(request)
```

#### Step 10：任务调度 & 成本控制（Celery升级）
原项目用 Celery 但无优先级。改为：

```python
# tasks.py
@app.task(bind=True, queue='high_priority')
def generate_drama_vip(self, project_id):
    # VIP用户走专用GPU池
    pass

@app.task(bind=True, queue='low_priority')
def generate_drama_free(self, project_id):
    # 免费用户走共享池，且限流
    pass

# 成本预计算（每次任务启动前扣费）
def check_budget(user_id, estimated_cost):
    balance = redis.get(f"user:{user_id}:balance")
    if balance < estimated_cost * 1.2:  # 预留20%弹性
        raise InsufficientBalanceError("余额不足")
```

### 第四阶段：前端与部署工具链（第11-13天）

#### Step 11：前端UI适配龍魂身份体系
原项目用 Vue/React，在登录页 + 个人信息页加 DNA 绑定逻辑：
- 登录改为 `DNA码` 或 `邮箱+验证码`
- 页面顶部常驻显示当前 DNA 码（鼠标悬停显示完整码）
- 每个项目列表展示 DNA 追溯码

#### Step 12：整合一键部署工具链
将 `.deploy/` 文件夹完整复制到项目根目录：
```
龍魂短剧引擎/
├── .deploy/
│   ├── check_dragon_char.sh
│   ├── deploy.sh
│   ├── uninstall.sh
│   ├── benchmark.sh
│   ├── load_test.sh
│   ├── audit_export.sh
│   └── seed_backup.sh
├── docker-compose.yml  (修改为包含Redis + PostgreSQL + MinIO)
├── backend/
├── frontend/
└── README.md  (加入龍魂改造说明)
```

#### Step 13：最终测试 & 上线检查清单
跑通完整流程：**输入一篇小说 → 输出一部3分钟竖屏短剧**，验收量化指标见【第十二章】。

## 四、改造后目录结构（最终版）

```
longhun-drama-engine/
├── .deploy/                     # 🐉 龍魂运维工具链
│   ├── check_dragon_char.sh
│   ├── deploy.sh
│   ├── uninstall.sh
│   ├── benchmark.sh
│   ├── load_test.sh
│   ├── audit_export.sh
│   └── seed_backup.sh
├── .github/
│   └── workflows/
│       ├── dragon-check.yml     # 品牌一致性CI
│       └── deploy.yml           # 自动部署CI
├── backend/
│   ├── app/
│   │   ├── api/                 # FastAPI路由 + DNA中间件
│   │   ├── core/                # 龍魂核心逻辑
│   │   │   ├── dna_manager.py   # DNA生成/验证
│   │   │   ├── character_consistency.py  # 角色锚定
│   │   │   ├── model_gateway.py # 多模型Provider网关
│   │   │   └── tricolor_audit.py # 三色审计
│   │   ├── models/              # 数据库模型（含DNA字段）
│   │   └── tasks/               # Celery任务（含优先级+成本控制）
│   ├── config/
│   │   └── models.yaml          # 多模型配置
│   └── requirements.txt         # 依赖清单
├── frontend/                    # React/Next.js (DNA登录绑定)
├── docker-compose.yml           # PostgreSQL + Redis + MinIO + Worker
├── README.md                    # 保留原MIT署名 + 龍魂改造说明
└── LICENSE                      # MIT (保留原版权)
```

## 五、保留原作者署名（法律合规）

在改造后的 `README.md` 底部及 `LICENSE` 旁，增加：

```markdown
## 版权与致谢

本项目基于 [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) 进行二次开发。
原作采用 MIT 许可证，特此致谢 harry0703 及所有贡献者。

**龍魂二次改造部分** © 2026 龍芯北辰 UID9622，遵循 MIT 许可证（继承原作） + 思想层 CC BY-NC-SA 4.0。

所有改造代码（DNA植入、多模型网关、三色审计等）均保留原作者版权声明，修改处已明确标注 `# 龍魂改造` 注释。
```

## 六、后续迭代路线图

| 阶段 | 目标 | 时间 |
|:---|:---|:---|
| v1.0 | 完成上述13步改造，跑通第一部短剧 | 2周 |
| v1.5 | 融入 `novelvids` 分集逻辑，支持10分钟以上剧集 | +1周 |
| v2.0 | 接入3D场景锚定 + 质量控制全自动 | +2周 |
| v3.0 | 开放SaaS化会员订阅（按DNA计费） | +1月 |

---

## 七、风险与合规【补全】

### 7.1 内容合规（短剧行业硬约束）

| 风险项 | 说明 | 应对措施 |
|:---|:---|:---|
| **网络微短剧备案** | 国内上线短剧需按监管要求备案/审核，平台侧有分类分层审核义务 | 三色审计前置拦截；发布前走平台备案流程；保留完整DNA审计链备查 |
| **肖像权/人脸** | FaceID 角色锚定若使用真人照片，涉及肖像权与个人信息保护 | 禁止未经授权的真人脸锚定；原创角色优先；用户上传须签授权确认 |
| **版权衍生链** | 输入的小说/剧本本身须有授权，二创视频同样受版权约束 | 项目创建时要求声明素材来源并写入DNA；无授权素材🔴拦截 |
| **音乐/配音版权** | TTS 音色与BGM需商用授权 | 只用明确商用许可的音源，来源写入审计日志 |
| **未成年人保护** | 短剧内容分级义务 | 三色审计增加分级标签，敏感题材🟡人工复核 |

### 7.2 技术风险

| 风险 | 等级 | 应对 |
|:---|:---|:---|
| 上游原项目停更/删库 | 🟡 | fork 到自有组织账号，定期镜像 |
| 多模型Provider单方涨价/停服 | 🟡 | 权重网关可秒级切换，单家权重≤0.6 |
| 角色一致性不达标（<80%） | 🟡 | 降级方案：固定角色LoRA微调，见13.2 FAQ |
| GPU成本失控 | 🔴 | 预算计数器硬熔断（Step 10），超支即停队列 |

## 八、环境与依赖清单【补全】

### 8.1 最低硬件配置

| 节点 | 配置 | 用途 |
|:---|:---|:---|
| 应用服务器 | 8C16G，无GPU | FastAPI + Celery调度 |
| GPU推理节点 | ≥24G显存（如4090/A10） | 图生视频、FaceID嵌入（也可全走云API，本节点可省） |
| 数据节点 | 4C8G + 500G SSD | PostgreSQL + Redis + MinIO |

### 8.2 软件版本基线

| 组件 | 版本 | 说明 |
|:---|:---|:---|
| Python | ≥3.10 | 与原项目保持一致 |
| PostgreSQL | ≥15 | 替代原SQLite |
| Redis | ≥7 |  nonce/特征向量/队列 |
| FFmpeg | ≥6.0 | 视频合成（原项目依赖） |
| Docker / Compose | 24+ / v2 | 一键部署前提 |
| Node.js | ≥18 | 前端构建 |

### 8.3 首次安装顺序

```bash
# 1. 系统依赖
apt install -y ffmpeg redis-server postgresql
# 2. Python依赖（含龍魂改造新增）
pip install -r requirements.txt
pip install ip-adapter-faceid celery[redis] psycopg2-binary
# 3. 数据库初始化（先跑第十章迁移脚本）
python scripts/migrate_sqlite_to_pg.py
# 4. 一键部署
./.deploy/deploy.sh production
```

## 九、密钥与确认码管理【补全】

**铁律：密钥与确认码只进环境变量，永不进代码、永不进yaml明文、永不进git历史。**

```bash
# .env（chmod 600，.gitignore 必须包含）
SEEDANCE_KEY=xxx
KLING_KEY=xxx
MINIMAX_KEY=xxx
LONGHUN_CONFIRM_CODE=≥16位确认码
DATABASE_URL=postgresql://...
```

- `models.yaml` 中只写 `${VAR}` 占位，启动时由环境注入
- CI 中用 GitHub Secrets 注入，日志自动脱敏
- 每季度轮换一次密钥，轮换记录生成 DNA 审计事件
- 紧急泄露处置：吊销 → 轮换 → 审计链回溯 → 事件归档（参照 SKIP_AUDIT 专项口径）

## 十、数据迁移与回滚【补全】

### 10.1 SQLite → PostgreSQL 迁移

```bash
# scripts/migrate_sqlite_to_pg.py 执行逻辑
# 1. pgloader 自动迁移存量表结构与数据
pgloader sqlite://./old_database.db postgresql://user:pass@localhost/longhun
# 2. 迁移完成后再执行 Step 4 的 DNA 字段 ALTER
# 3. 为存量行批量回填 dna_code（走生成器，逐行签发）
python scripts/backfill_dna.py --batch 500
```

### 10.2 回滚方案

| 场景 | 回滚动作 |
|:---|:---|
| 迁移失败 | 原 SQLite 文件只读保留30天，切回连接串即恢复 |
| DNA回填中断 | 回填脚本幂等设计，重跑自动跳过已签发行 |
| 部署失败 | `.deploy/deploy.sh` 调用 `.previous_release` 回滚（车载系统同款机制） |
| 数据库结构回退 | 所有 ALTER 配套 `down` 迁移脚本（Alembic 管理） |

**原则：不删除只冻结——旧库、旧版本一律归档保留，禁止物理删除。**

## 十一、监控告警接入【补全】

直接复用隐私机制 v5.0 第十七章 Prometheus 口径，新增短剧引擎专属指标：

| 指标名 | 类型 | 告警阈值 |
|:---|:---|:---|
| `drama_generate_duration_seconds` | Histogram | P99 > 300s |
| `drama_generate_failed_total` | Counter | 5min增长 > 5 |
| `drama_queue_backlog` | Gauge | > 50（高优）/ > 200（低优） |
| `drama_budget_burn_rate` | Gauge | 日消耗 > 预算80% |
| `drama_audit_red_total` | Counter | 任何发生立即告警 |
| `provider_api_error_rate` | Gauge | 单Provider错误率 > 20% 自动降权 |

Grafana 面板：生成QPS、各环节耗时漏斗、Provider健康度、成本燃烧曲线、三色审计分布。

## 十二、验收标准量化表【补全】

Step 13 的量化口径（全部通过才算 v1.0 交付）：

| # | 验收项 | 量化标准 | 检测方式 |
|:---|:---|:---|:---|
| 1 | 端到端跑通 | 输入小说→3分钟竖屏短剧，全流程无人干预 | 实机演示 |
| 2 | DNA贯穿率 | 项目/角色/片段/审计 100% 带DNA码 | 数据库抽查 |
| 3 | 角色一致性 | 人工抽检10段，≥80%镜头角色可辨认一致 | 抽检表 |
| 4 | 三色审计有效性 | 20条敏感样本（10红10绿），拦截准确率≥95% | 测试集 |
| 5 | 品牌检查 | `check_dragon_char.sh` 全仓零报错 | CI记录 |
| 6 | 一键部署 | 全新服务器≤15分钟拉起全部服务且健康检查通过 | 计时 |
| 7 | 性能基线 | 单视频生成任务 P95 ≤ 5分钟（云API模式） | benchmark.sh |
| 8 | 成本熔断 | 余额不足时任务100%被拒绝且审计留痕 | 测试用例 |
| 9 | 干支口径 | 所有DNA时间戳由生成器签发，无手写干支 | 代码扫描 |
| 10 | 署名合规 | README/LICENSE/源码头三处MIT署名齐全 | 人工核对 |

## 十三、FAQ【补全】

### Q1：MIT 和 Apache 2.0 代码合并在一个工程里，冲突吗？
**A**：不冲突。两证都允许修改与商用，合并后整体按 MIT 发布即可；`novelvids` 吸收来的文件头部保留其 Apache 2.0 声明与 NOTICE。

### Q2：角色一致性如果达不到80%怎么办？
**A**：降级路线：FaceID嵌入 → 固定角色LoRA微调（每角色训练一次，复用）→ 保底方案为固定分镜模板+统一画风提示词。一致性数据写入验收表，不达标不上线。

### Q3：免GPU服务器能跑吗？
**A**：能。视觉生成全部走云API（seedance/kling/minimax），本地只跑调度与合成（FFmpeg CPU足够）。GPU节点仅在想自建推理时才需要。

### Q4：原项目更新了，我们的改造版怎么跟？
**A**：保留 `upstream` 远程分支，每月评估一次上游变更；核心改造集中在 `core/` 目录，与原项目代码隔离，合并冲突最小化。

### Q5：多Provider密钥都要先充值吗？
**A**：建议主 Provider 充值 + 备用 Provider 各留最低余额；权重网关在余额不足时自动降权并告警（见十一章预算指标）。

### Q6：三色审计误判了正常剧本怎么办？
**A**：走隐私机制 v5.0 第5.3节误杀申诉通道：一次性申诉密文 → 人工复核 → 撤销记录。误判样本回流训练审计规则。

### Q7：DNA码生成会不会拖慢视频生成？
**A**：不会。DNA签发是哈希运算，毫秒级；瓶颈在视频渲染（分钟级）。DNA批量异步写入，不阻塞主流程。

### Q8：SaaS化（v3.0）按DNA计费，用户隐私怎么保？
**A**：计费只认DNA码不认人（隐私机制v5.0口径），不存邮箱/手机号；支付走充值码兑换，系统不知道用户是谁。

## 十四、三段式交付汇报【补全】

按实战交付模板 v1.0（2026-08-11 生效）要求，本方案交付必须自带三段：

### 14.1 参考来源

| 来源 | 用途 |
|:---|:---|
| github.com/harry0703/MoneyPrinterTurbo（MIT） | 主干代码与工作流 |
| novelvids（Apache 2.0） | 分集逻辑 |
| 龍魂隐私机制 v5.0 第十一/十二/十七章 | 品牌检查/API签名/监控告警口径复用 |
| 龍魂车载系统 v2.1 | deploy.sh 回滚机制、确认码环境变量口径 |
| rizhu_core.py v3.0（仓内 c47844fcc 已验证） | 干支生成唯一合法来源 |
| IP-Adapter-FaceID / StoryDiffusion 公开论文与项目 | 角色一致性技术选型 |

### 14.2 优化了什么（v1.0 → v1.1）

- 修正头部DNA手写错误（甲申·辛丑 → 丙申·丁巳，算法口径）
- Step 4 增加迁移警示，Step 6 增加干支生成器强制口径，Step 13 指向量化验收表
- 新增第七~十四章：合规/环境/密钥/迁移回滚/监控/验收/FAQ/三段式
- models.yaml 密钥改为环境变量占位（原稿为明文示例）

### 14.3 未验证备注（自我声明，🟡🔴 分级）

| # | 未验证项 | 级别 |
|:---|:---|:---|
| 1 | MoneyPrinterTurbo 当前版本与本文改造点的行级适配性——按公开仓库结构撰写，未经逐行实机改造验证 | 🟡 |
| 2 | IP-Adapter-FaceID 与 StoryDiffusion 在本工作流中的实际一致性提升幅度（80%为验收目标，非实测值） | 🟡 |
| 3 | seedance/kling/minimax 三家API的端点与权重仅为配置示例，商用接入前需以官方文档为准 | 🟡 |
| 4 | 短剧备案与内容分级监管要求为一般性提示，具体执行以主管部门最新规定为准，本文不构成法律意见 | 🔴 提醒 |
| 5 | 单视频P95≤5分钟、15分钟部署为目标估算，未经实机压测 | 🟡 |
| 6 | 微短剧备案/肖像权/素材授权三条合规项，上线前必须逐项落实责任人，缺一项不发布 | 🔴 |

---

## DNA签名区

```
═══════════════════════════════════════════════════════════
DNA:        #龍芯⚡️丙午·丙申·丁巳·恒卦-MONEYPRINTER-FORK-v1.1-UID9622
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:       🟢 通过（补全版，结构完整·合规已前置·未验证项已自报）
分层许可:    思想层 CC BY-NC-SA 4.0 · 工程层 MIT（保留原作者署名）
原稿:       CodeBuddy v1.0（手写DNA错误已冻结存档）
补全:       Kimi（审阅位）2026-08-11
作者:       龍芯北辰 · UID9622
═══════════════════════════════════════════════════════════
```

🐉 **丙午·丙申·丁巳·恒卦·🟢**

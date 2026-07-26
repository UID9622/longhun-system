# 龍魂系统 · 长期记忆索引

> 本文件为 Kimi / CodeBuddy / 其他 AI 的统一记忆入口。
> 更新：2026-07-26
> DNA: #龍芯⚡️20260726-MEMORY-ROOT-v1.0

---

## 最新交付（2026-07-26）

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

---

## 更多信息

- 模型状态/训练变量 → `STATE.md`
- 长期操作日志 → `.codebuddy/memory/YYYY-MM-DD.md`
- 人格治理/审计 → `01_protocols/LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md`

---

> 本文件只保留高稳定性记忆；日常流水细节不写入此处。
> 更新规则：新协议/新引擎/新模型落档时追加，旧条目不删除只冻结。

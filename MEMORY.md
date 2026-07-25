# 龍魂系统 · 长期记忆索引

> 本文件为 Kimi / CodeBuddy / 其他 AI 的统一记忆入口。
> 更新：2026-07-26
> DNA: #龍芯⚡️20260726-MEMORY-ROOT-v1.0

---

## 最新交付（2026-07-26）

### 龍魂字体优化 + 媒体主权标记引擎 v1.0

**背景**：字体源字元库（`glyphs/*.json`）因 Git LFS 对象缺失无法重新训练字形，改为基于现有 OTF 优化 + 建立跨媒体统一 DNA 标记体系。

**三件产物：**

| # | 文件 | 说明 |
|---|------|------|
| 1 | `_work/repos/LonghunFont/output/龙魂字体-Regular.{otf,woff2}` | 字体显示名改为「龙魂字体」，WOFF2 压缩 90.2% |
| 2 | `engines/lh_media_sovereignty_marker.py` | 字体/图像/视频/音频统一 DNA 标记引擎 |
| 3 | `01_protocols/LH-MEDIA-SOVEREIGNTY-MARK-v1.0.md` | P0 协议文档 |
| 4 | `bin/lh_media_mark.py` | CLI 入口 |

**技术实现：**

| 媒体 | 标记方式 | 验证结果 |
|:---|:---|:---:|
| 字体 | U+E200 龙纹缩微水印 + name 表 DNA | ✅ 原生水印存在，DNA 可读写 |
| 图像 | LSB + DCT 双频隐写 | ✅ 闭环提取 |
| 音频 | 时域 LSB + 3 重复码 | ✅ 闭环提取 |
| 视频 | 关键帧图像水印 | ⚠️ v1.0 部分支持 |

**关键修复：**
- 图像提取从严格前缀匹配改为 `_looks_like_dna()`，支持自定义 DNA。
- 音频从有偏 FFT 扩频改为时域 LSB + 3 重复码，解决负样本溢出与原始 LSB 混叠问题。

**CLI 示例：**

```bash
python3 bin/lh_media_mark.py verify /Users/zuimeidedeyihan/longhun-system/_work/repos/LonghunFont/output/龙魂字体-Regular.otf
python3 bin/lh_media_mark.py mark input.png --type image --dna "龍魂DNA#UID9622#IMAGE-001" --output output.png
python3 bin/lh_media_mark.py mark input.wav --type audio --dna "龍魂DNA#UID9622#AUDIO-001" --output output.wav
```

**已知限制：**
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

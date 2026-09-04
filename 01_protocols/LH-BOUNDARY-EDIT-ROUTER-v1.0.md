> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 边界定义与自动编辑归类路由

> **DNA**: `#龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-BOUNDARY-EDIT-ROUTER-v1.0`
> **来源**: UID9622 老版决策流场总控页 §八+§七（2026-07-16 对齐矫正）
> **优先级**: P0 永恒级（不可降级、不可绕过）
> **确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` ✅
> **状态**: 🔒 已锁定，与反钓鱼反贪心协议互锁
> **关联**: `LH-ANTI-FISHING-GREED-v1.0.md`（反钓鱼反贪心）

---

## 一句话边界

系统只在"**可归类 + 可追溯 + 可回滚**"三条件满足时才允许改动；否则一律归档为候选资产，不新建、不扩散。

---

## 边界检查清单（B1-B4）

| 检查项 | 通过标准 | 不通过处置 |
|--------|----------|------------|
| **B1 归类** | 能否命中主线标签词并指向固定落点 | `ARCHIVE`（收集箱/候选资产），禁止新建 |
| **B2 分身** | 同主题是否已存在可更新的页面/段落 | 存在→必须`UPDATE`原页；不存在→才允许评估`CREATE` |
| **B3 追溯** | 能否给出DNA/索引回链或创建原因 | 不通过→禁止进入运行主线 |
| **B4 回滚** | 能否明确回滚点（旧URL/旧段落/旧版本） | 不通过→禁止批量改动，只允许归档或出推演稿 |

---

## 三个硬拦截动作

### 拦截1：禁止自动新建页面（默认）

- 默认 `create_allowed = false`
- 只有同时满足以下三个条件才允许新建：
  1. 查无同主题落点
  2. 用途明确不同（不是升级）
  3. 已指定父DNA/父页面/落点

### 拦截2：不确定就入库，不要乱落地

- 任何"表达很杂/目标不清"的输入 → `ARCHIVE_AS_BACKLOG`
- 入库到 `.archive/` 或候选资产区，不进入运行主线

### 拦截3：一次只改一个主线容器

- 默认只允许更新 `primary_destination`
- 需要跨页联动时，必须先给出"联动清单"并等老大确认

---

## P0 固定模板：自动编辑归类路由

```yaml
# P0-AUTO-EDIT-ROUTER-V1.0
confirm_code: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

input_raw: "（原话，不用整理）"

route:
  tag: "家|DNA|索引|安全|审计|自动化|翻译器|模板|知识库|推演"
  primary_destination: "（固定主线页面/库）"

classification:
  intent_type: "UPDATE|CREATE|ARCHIVE"
  create_allowed: false  # 默认禁止新建
  create_allowed_only_if:
    - "查无同主题落点"
    - "明确不同用途（不是升级）"
    - "已指定父页面/父DNA/落点"

fallback:
  when_uncertain: "ARCHIVE"  # 不确定就进候选资产，防分身

audit:
  event_file: "evt_YYYYMMDD-HHMMSS+0700__AUTO_EDIT__<short>.json"
  reason_code: "AUTO_EDIT_UPDATE|AUTO_EDIT_CREATE|AUTO_EDIT_ARCHIVE|AUTO_EDIT_BLOCKED"
  exit_code_success: "OK_AUTO_EDIT_200"
  exit_code_fail: "ERR_AUTO_EDIT_500"
```

---

## 与反钓鱼反贪心协议的衔接

- 自动编辑路由在执行前先过反钓鱼反贪心门卫（`AntiFishingGatekeeper`）
- 检测到钓鱼/贪心信号 → 直接 `AUTO_EDIT_BLOCKED`，不进入路由
- 通过后 → 按本协议 B1-B4 检查 → 决定 UPDATE/CREATE/ARCHIVE

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|:----:|:----:|----------|
| v1.0 | 丙午·辛未·乙酉 | 从 UID9622 老版决策流场总控页 §七+§八 提取矫正，新建协议 |

---

*🐉 龍芯北辰｜UID9622｜为人民服务*
*DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-BOUNDARY-EDIT-ROUTER-v1.0*

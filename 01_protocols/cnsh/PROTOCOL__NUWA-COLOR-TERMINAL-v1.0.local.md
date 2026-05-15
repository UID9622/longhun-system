# 女娲五彩石 · 主权终端 UI 协议 v1.0（NUWA_COLOR_PROTOCOL）

M::
  dna: "#龍芯⚡️2026-05-16-NUWA-COLOR-SOVEREIGN-TERMINAL-v1.0"
  alias: "NUWA_COLOR_PROTOCOL"
  behavior_layer: "TERMINAL_BEHAVIOR_LAYER"
  ipa: "[IPA-MAIN-CONTROL]"
  confirm: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  seal: "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
  gpg: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
  route_id: "NUWA-COLOR-TERMINAL"
  tier: L1
  audit: "🟢"
  related_l5: "01_protocols/cnsh/PROTOCOL__DNA-L5-ARCHITECTURE-v1.4.local.md"

---

## 定盘

目标不是炫技皮肤，而是 **行为语义界面（Behavior Semantic Interface）**：颜色约束行为，类似驾驶舱——降误操作、降情绪乱操作、降 AI 漂移、降不可逆执行。

**原则：** 颜色 **刺激约束人，不刺激停留**；与互联网「诱导点击 / 上瘾」哲学相反。

**与 L5 叙事区分：** `PROTOCOL__DNA-L5-ARCHITECTURE` 中「女娲五彩石×层级」是 **时间 / 权限 / 衰减** 叙事坐标；本协议是 **终端运行时** 的 **五色语义 + 状态机**。日后若统一调色板，单开「NUWA↔L5 映射卷」修订，本 v1.0 不改 L5 正文。

---

## 一、语义颜色体系（低频稳定色 · 禁止霓虹夜店风）

| 石（隐喻） | 语义 | 系统态 | 风险 | 行为 |
|------------|------|--------|------|------|
| 黄土金 | 稳定 · 根基 · 主权 | ROOT | 通行 | 可执行 |
| 赤火红 | 熔断 · 警戒 · 越界 | BREAKER | 阻断 | 停止 |
| 深海青 | 推演 · 思考 · 分析 | THINK | 待审 | 待确认 |
| 玉白色 | 只读 · 审计 · 回放 | AUDIT | 中性只读 | 不修改 |
| 苍木绿 | 恢复 · 同步 · 生长 | RESTORE | 通行 | 可恢复 |

### HEX 锚点（工程落地）

| Token | 含义 | HEX |
|-------|------|-----|
| ROOT_GOLD | 主权 / 正常执行 | `#C6A664` |
| BREAKER_RED | 熔断 / 危险 | `#A61B1B` |
| THINK_BLUE | 推演 / 分析 | `#1C3D5A` |
| AUDIT_WHITE | 只读审计 | `#D9D4C7` |
| RESTORE_GREEN | 恢复 / 同步 | `#3F5E45` |

---

## 二、颜色 → 状态 → 权限 → 风险 → 行为（映射层）

完整链：**Color Semantic Router** 输入 `triColor` / `fuse_level` / `namespace` / `audit_mode`，输出终端 tokens（主题、状态栏、跑马灯、一次动效）。

禁止缺失映射就上色；禁止「好看」但无语义。

---

## 三、TERMINAL_BEHAVIOR_LAYER（状态机草案）

```yaml
TERMINAL_BEHAVIOR_LAYER:
  SAFE_MODE:
    color: "ROOT_GOLD"
    hex: "#C6A664"
    animation: "none"
    permission: "stable"
  THINK_MODE:
    color: "THINK_BLUE"
    hex: "#1C3D5A"
    animation: "slow_breath"
    permission: "analysis"
  BREAKER_MODE:
    color: "BREAKER_RED"
    hex: "#A61B1B"
    animation: "single_flash"
    permission: "blocked"
  AUDIT_MODE:
    color: "AUDIT_WHITE"
    hex: "#D9D4C7"
    animation: "none"
    permission: "readonly"
  RESTORE_MODE:
    color: "RESTORE_GREEN"
    hex: "#3F5E45"
    animation: "wave_restore"
    permission: "recover"
```

---

## 四、动画规则（硬约束）

**禁止：** 高频闪烁 · 持续流光 · 彩虹动态 · 大面积发光 · 代码区蹦迪式动效。

**允许：** 单次状态闪烁 · 低频呼吸（THINK）· DNA 提交完成 ≤0.5s 轻扫光 · 熔断瞬时警告一次后稳态常亮。

### 事件驱动的克制仪式感（示例）

| 事件 | 动效 | 其它动作 |
|------|------|----------|
| AI_DRIFT_DETECTED | 红闪 **一次** → 常亮 | 写审计日志 |
| DNA_COMMIT_OK | 金轻扫 ~0.5s | chain_hash 已验 |
| AUDIT_MODE | 全局灰白只读 | 禁止编辑态 |
| THINK_MODE | 深蓝呼吸 | 可略降低扰动亮度 |

---

## 五、推荐栈（外挂语义层，不 hack 编辑器本体）

```
Cursor / VS Code
  → CNSH Theme Layer（语义主题）
  → DNA State Engine（runtime_state.json 等）
  → Terminal Behavior Layer（本文件 §三）
  → Color Semantic Router
```

**数据源（工程化时）：** 建议 `runtime/runtime_state.json` 字段：`dna` `namespace` `risk` `digital_root` `audit` `ai_state` `git_summary` —— 由扩展或本地 daemon 监听更新；**未实装前** 本文件为规格真源。

---

## 六、跑马灯（Runtime Semantic Marquee）

由固定口号升级为动态条，字段示例：

`[工程] | [DNA 摘要] | [人格/路由] | [Audit 🟢🟡🔴] | [Git dirty/clean] | [dr]`  

例：熔断态 `CIRCUIT BREAKER | POLICY TRACE REQUIRED | ROOT=dr9`。

---

## 七、未来扩展：cnsh-runtime-layer（验收提纲）

独立仓库/目录实现时参考（**非本文件闭环**）：

- 动态顶部跑马灯 + 状态栏三色 +（可选）Webview 低透明粒子背景 · **CPU 与 30FPS 预算** 见老大 Cursor 包约束。
- Git 变更刷新 marquee；namespace 切换主题包（TECH / AUDIT / WRITING / VOID）。
- **一票否决：** 不 Electron 注入、不改用户源码、不阻塞编辑器、关扩展即恢复原样。

---

## 八、诚实

- v1.0 = **协议与映射**；VS Code 扩展 / `runtime_state.json` **可另库实装**。
- 与 `cnsh/gate_v3` 数字 dr 三色：终端 BREAKER 应对齐 **GATE-01** 的 🔴 语义；柱⑥ 共生 dr 仍为叙事层，见共生时间桥 v2。

---

*UID9622 · 本地规格 2026-05-16 · 女娲五彩石主权终端*

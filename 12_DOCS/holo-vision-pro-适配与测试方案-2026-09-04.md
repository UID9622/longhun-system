# 🥽 龍魂全息页面 · Vision Pro 适配与测试方案

> DNA: `#龍芯⚡️2026-09-04-HOLO-VISIONPRO-ADAPT-v1.0-UID9622`
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）
> License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> 三色审计: 🟡 代码已改·未真机实测（诚实标注）

---

## 一、改动清单（2026-09-04 · `10_PORTAL/holo/index.html`）

| 项 | 改动 | 目的 |
|:---|:---|:---|
| 1 | WebXR 可用性分级提示 | 无 WebXR 浏览器显示可见文案而非静默隐藏 |
| 2 | 参考空间降级链 `immersive-vr(local-floor/bounded/hand-tracking) → immersive-vr(viewer) → inline` | 兼容 visionOS 各版本参考空间支持差异 |
| 3 | XR 会话 `select` 事件 → 凝视中心拾取节点 | Vision Pro 注视+捏合、Quest 扳机均可选中节点 |
| 4 | 节点脉冲高亮（`pulseNode`） | XR 内视觉反馈（DOM 在沉浸中不可见） |
| 5 | 进入/退出 XR 自动切 HUD 隐藏态 | 防平面 UI 残留干扰 |
| 6 | `.btn:disabled` 态 + 按钮文字反馈 | 进入中/失败状态可见 |

既有基础（v1.0 已含）：`renderer.xr.enabled`、`immersive-vr` 检测、退出会话恢复动画循环。

## 二、真机测试清单（📱 需在 Vision Pro 上逐项验证）

前置：Vision Pro Safari 打开全息页（`https://uid9622.cn/holo/` 或 portal 内网）。

| # | 验证项 | 预期 | 通过 |
|:---:|:---|:---|:---:|
| T1 | 页面加载 | 三色球壳+粒子正常渲染，无报错 | ☐ |
| T2 | 「🥽 进入沉浸模式」按钮 | 可见可点 | ☐ |
| T3 | 点击进入 | 成功进沉浸空间，场景以真实尺度呈现 | ☐ |
| T4 | 头部转动 | 场景随视线稳定（不自转抖动） | ☐ |
| T5 | 注视节点+捏合 | 节点白闪 6 次（脉冲反馈） | ☐ |
| T6 | 退出沉浸 | 回平面态，HUD 恢复，动画循环恢复 | ☐ |
| T7 | 无 WebXR 浏览器 | 按钮显示禁用文案而非消失 | ☐ |

## 三、已知边界（诚实声明）

- ⚠️ **未真机实测**：改动经 JS 语法校验 + 逻辑走查，Vision Pro 实机需按 T1-T7 验证。
- XR 沉浸中 DOM 详情卡不可见 → 选中反馈=脉冲高亮，退出后详情卡可见（`showDetail` 已保留）。
- 凝视拾取以屏幕中心为准（Vision Pro 注视点不在正中心时可能偏差）→ 后续可升级为 `XRFrame` 凝视射线精确拾取。
- `inline` 模式无 6DoF 头部追踪 → 仅作降级兜底，不承诺沉浸体验。

## 四、测试执行人

- 代码改动：AI（CodeBuddy）· 真机验证：UID9622（老大）/ P14 吕蒙部署侧复核

---

## 签名

```
DNA:    #龍芯⚡️2026-09-04-HOLO-VISIONPRO-ADAPT-v1.0-UID9622
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:   🟡 适配已落地·真机 T1-T7 待验（诚实标注·不标🟢已验证）
```

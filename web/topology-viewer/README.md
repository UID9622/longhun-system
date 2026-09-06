# 龍魂拓扑 · 神经网络全览

> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
> DNA: #龍芯⚡️2026-08-30-TOPOLOGY-VIEWER-v1.5-BUILD-UID9622

龍魂系统神经网络拓扑的**三端离线可视化**，一份产物 macOS / iOS / 鸿蒙通用。

**全部数据内嵌单页。不联网、不上传、不收集、不追踪任何数据。**

## 功能总览

| 模块 | 内容 |
|:---|:---|
| 🏯 九层架构 | L0-L9 洛书九宫骨架 · 中宫 UID9622 · 八方锚定 |
| 🧬 人格矩阵 | 16 核心 + 3 子系统 · 权重分组 · 应用人格小队 |
| 🕸️ 神经网络 | 全部真实连接边 · 高权重主干金色高亮 · 图例可读 |
| ⚙️ 引擎清单 | 192 引擎 · 实时搜索过滤 · 活跃/弃用/暂缓状态区分 |
| 🧰 技能总线 | 全部分类与工具 · 计数徽章 |
| 🤖 数字人 | 7 数字人联动卡片 |
| 🌐 生态 | 四层级 · 价格 · 服务清单 |
| 🚪 三闸门 | 决策流场 · 人性 11 维 · 思考循环 7 阶段 |

## 产物清单

| 文件 | 说明 |
|:---|:---|
| `index.html` | 单页应用（数据内嵌 · 离线可看） |
| `sw.js` | Service Worker（PWA 真离线缓存） |
| `manifest.webmanifest` | PWA 清单（含版本 + DNA） |
| `icon.svg` | 龍字印章矢量图标 |
| `icon-180/192/512.png` | 位图图标（iOS/鸿蒙主屏必需） |
| `../../dist/龍魂拓扑.dmg` | macOS 安装包（app + 三端说明） |

## 三端使用

**macOS**：打开 `dist/龍魂拓扑.dmg` → 双击「龍魂拓扑.app」→ 自动在浏览器打开；可拖入「应用程序」。

**iOS（iPhone / iPad）**：
1. 将本目录部署到任意 https 站点（如 `uid9622.cn`）或局域网 http 服务
2. Safari 打开 `index.html`
3. 分享 →「添加到主屏幕」→ 桌面生成龍魂拓扑图标
4. 首次联网打开后，Service Worker 完成离线缓存，之后离线可用

**鸿蒙 HarmonyOS（手机 / 平板 / 车机）**：
1. 同上游览器打开 `index.html`
2. 浏览器菜单 →「添加到桌面」
3. 首次联网打开后离线可用

## 工程流程（完整链）

```bash
# 1. 构建（含拓扑契约校验 · 缺字段即拒绝产出）
python3 bin/lh_topology_viewer_build.py

# 2. 产物校验（三色 · 必检项失败返回非零）
python3 bin/lh_topology_verify.py

# 3. macOS 打包 dmg（零第三方依赖 · 临时目录自动清理）
bash bin/lh_topology_make_dmg.sh

# 4. 一键发布（构建→校验→GPG签名→dmg→校验→部署可选）
bash bin/lh_topology_publish.sh                      # 本地发布
bash bin/lh_topology_publish.sh --deploy root@鲲鹏:/路径   # 发布+部署
```

### 数据源

`../../.codebuddy/longhun_neural_net.json`（v4.0 拓扑）· 变更后重跑步骤 1-4 即全链更新。

## FAQ

**Q: 为什么 iOS/鸿蒙不能直接装 dmg？**
A: dmg 是 macOS 专属格式；iOS 装 ipa、鸿蒙装 hap。本方案用「离线单页 + PWA 添加到主屏」，三端行为一致且无需签名证书。

**Q: 离线真的可靠吗？**
A: 是。数据本身内嵌在 HTML；Service Worker 额外缓存全量资源（离线缓存自 v1.1 加固引入 · 当前产物 v1.5）。前提是至少首次在线打开过一次。

**Q: 数据会泄露吗？**
A: 不会。单页内嵌、零请求、零 SDK、零埋点。源码可审。

**Q: 如何更新版本？**
A: 拓扑 JSON 有变 → 重跑 `lh_topology_publish.sh` 即可；dmg 内说明同步携带最新版本号。

## 版本记录

| 版本 | 日期 | 说明 |
|:---|:---|:---|
| v1.5 | 2026-09-05 | 版本标签全链统一：SW 注释对齐缓存键 v1.5 · manifest/index 与构建器 VERSION 一致 |
| v1.1 | 2026-08-30 | 审计修复：真 SW 离线缓存 · PNG 位图图标 · 边图自适应布局（真实 edges 驱动）· 全段错误边界 · 契约校验内置 · 校验/发布流程新增 |
| v1.0 | 2026-08-30 | 首版：单页 + PWA 清单 + dmg |

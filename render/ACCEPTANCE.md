# M75 渲染引擎验收清单

> DNA: #龍芯⚡️2026-08-25-RENDER-ENV-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622） · 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> License: MulanPSL v2
> 验收日期: 2026-08-25 · 本机 macOS + 鲲鹏 x86_64 双端实测

| # | 检查项 | 三色 | 说明 |
|:---:|------|:---:|------|
| 1 | Web 渲染打开页面，截图+文本提取 OK | 🟢 | `lh render open https://example.com` 实测 · 截图已存 `data/renders/` |
| 2 | DOM 树提取为 JSON，深度 ≥ 4 层 | 🟢 | 测试 T4 通过 · 深度上限 6 可配 |
| 3 | 视觉模板匹配，置信度 ≥ 0.8 触发点击 | 🟢 | 实测: gov.cn 头模板同站 score=1.0 / baidu 异站 0.1295（<0.8 反例）· 样例 `render/data/renders/templates/gov_header.png` |
| 4 | HarmonyOS 截图 + 组件树提取 OK | 🟡 | `harmonyos_adapter.py` 就绪 · hdc 已装(SDK)但无真机连接(`hdc list targets` 空) · 待设备实测 |
| 5 | PaddleOCR 识别中文准确率 ≥ 95% | 🟡 | 依赖已全装(bookworm+numpy1.24.4+pyclipper post4+libgomp1)可导入 · 模型已手动就位 · **运行时 paddle2.6.2 推理 SIGABRT**(oneDNN/AVX-512 深层兼容问题·`free(): invalid pointer`/inflateReset2·禁mkldnn/单线程均无效) · DOM 文本提取🟢兜底 · 建议后续试 paddle 3.x |
| 6 | CNSH 指令 `渲染.打开()` 正常解析执行 | 🟢 | `lh render run` 多指令会话实测 18/18 |
| 7 | 主权边界：拒绝列表域名被龍盾拦截 | 🟢 | 测试 T2 通过 · `PermissionError 龍盾拦截` |
| 8 | DNA 每次渲染自动生成唯一标识 | 🟢 | `#龍芯⚡️2026-08-25-RENDER-XXXX-UID9622` 实测（本地+鲲鹏） |
| 9 | 鲲鹏 Docker `docker compose up` 无报错 | 🟢 | 实测: 镜像 `longhun-lh-render` 构建+容器运行+真实渲染 gov.cn 🟢（截图 940KB·DNA 生成）· **鲲鹏实为 x86_64**(Intel Xeon 6348)，非 ARM64 |
| 10 | 批量渲染 10 URL · 全部成功 | 🟢 | 实测: gov/people/xinhua/qq/baidu/163/csdn/cnblogs/bilibili/zhihu 10/10 ok · 115s(轻量模式) · audit 3🟢+7🟡 |
| 11 | REST API `/render/execute` 返回变量环境 | 🟢 | 实测: 本地+鲲鹏 execute `渲染.打开(url=...)` 均返回 title/audit/dna/截图 · :8972(原:8766被主权网关占用已迁) |
| 12 | 截图 + DNA 注册哈希引擎 M73 打通 | 🟢 | `render/core/hash_registry.py` 落地: 截图 SHA-256 + DNA 绑定 + Merkle 链式注册表(append-only `data/renders/hash_registry.jsonl`) · 渲染/截图自动登记 · CNSH `渲染.注册哈希/验证哈希` · 测试 T7 全过 |

## 已实测链路

```
lh render status                       🟢 引擎状态
lh render open <url>                   🟢 打开+全量提取（标题/文本/链接/表单/表格/截图/审计/DNA）
lh render run '渲染.打开("url"); 渲染.提取文本(选择器="h1")'   🟢 CNSH 多指令会话
python3 render/tests/test_render.py    🟢 冒烟测试 24/24（T1-T6 + T7 M73哈希产权）
lh render server                       🟢 REST 服务 :8972 后台常驻（原:8766被主权网关占用已迁走）
curl POST /render/batch 10 URL         🟢 批量轻量模式 10/10 ok · 115s
curl POST /render/execute              🟢 本地+鲲鹏真实渲染（title/audit🟢/DNA/截图）
视觉模板匹配样例                        🟢 gov 正例 score=1.0 · baidu 反例 0.1295
渲染.注册哈希 / 渲染.验证哈希          🟢 M73 产权登记+溯源（截图SHA256+DNA绑定·Merkle链）
bash render/deploy_render.sh local     🟡 本机一键部署
bash render/deploy_render.sh kunpeng   🟢 鲲鹏部署（rsync+Docker·x86_64 实测跑通）
```

## 2026-08-25 部署实测要点（端口/架构/依赖焊死）

- **端口**: 8766 被主权网关 `lh_sovereign_gateway.py` 焊死占用 → 迁移 **:8972**（7 文件同步修改）
- **架构**: 鲲鹏实测 `uname -m` = **x86_64**（Intel Xeon Gold 6348），非 ARM64 → 基镜像用 `python:3.11-slim-bookworm`，compose `platform: linux/amd64`
- **依赖坑**: numpy 锁 1.24.4（paddle 2.6 需 <1.25）· libgomp1（paddle 运行库）· pyclipper 1.3.0.post3 · pip 用清华源
- **构建坑**: trixie(deb13) 的 zlib ABI 与 paddle 不兼容 → 必须 bookworm 基镜像
- **批量性能**: 原 networkidle 死等 30s×2 拖垮批量 → domcontentloaded 主等待 + 1.2s 动态渲染，单站 3~11s

## 三色总结

- 🟢 10/12 双端实测通过（核心 Web 渲染链路 + 批量 10 URL + REST + 视觉匹配 + 鲲鹏部署 + M73 哈希产权全绿）
- 🟡 2/12 待办（鸿蒙需真机设备 · OCR 运行时环境问题待换 paddle3.x）
- 🔴 0

> 理念: 截图是被动的眼睛，M75 是主动的眼睛。CNSH 说看哪里，系统就渲染哪里，数据只存本地，DNA 全程追溯，M73 哈希产权链让每一张截图都有主，主权永远在手。

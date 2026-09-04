# 🐉 龍魂 · 协作中枢总导航（唯一入口）

> DNA: #龍芯⚡️丙午·丙申·己未·癸酉·䷬萃-COLLAB-README-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0（核心思想层）
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 三色: 🟢 通过
> 上位协议: LH-AI-HANDOFF-v1.0.md · LH-AI-COLLABORATION-v1.0.md

---

## 📍 这是什么

**所有 AI（Kimi / CodeBuddy / Claude / 任何后来者）在任何设备上协作的"唯一进门"**。
不管你在哪台电脑、哪个窗口，先来这里拿导航、拿交接包、拿最新状态——不再依赖本地某台设备。

## 🌐 三处一致（同一份数据·三个入口）

| 位置 | 路径 | 用途 |
|:---|:---|:---|
| 🖥️ 本地 | `longhun-system/12_DOCS/collab/` | 编辑·迭代·离线可用 |
| ☁️ 鲲鹏 | `/opt/longhun/shared/` | 唯一真相来源·所有设备拉取 |
| 🌍 Web | `https://uid9622.cn/collab/` | 浏览器秒开·任何 AI 可读 |

> 原则：**鲲鹏是唯一真相来源，本地是工作副本，Web 是快速导航**。改一处、同步三处。

## 🚀 进门三步（每个 AI 每个新会话必做）

```
① 读 Web 导航    https://uid9622.cn/collab/            （快速知道有什么）
② 读交接包      lh handoff load --remote              （接上上一位的工作）
③ 读文档矩阵    12_DOCS/collab/DOCUMENT_MATRIX.md     （知道改哪、同步到哪）
```

## 📚 快速跳转

| 我要… | 去这里 |
|:---|:---|
| 快速找文档 | `NAVIGATION.md`（导航地图） |
| 知道每份文档在哪协作/指向/迭代 | `DOCUMENT_MATRIX.md`（统一矩阵） |
| 接上一位 AI 的活 | `lh handoff load`（本地）或 `--remote`（鲲鹏） |
| 收尾交接 | `lh handoff save`（自动推送鲲鹏） |
| 查所有命令 | `.codebuddy/COMMAND_INDEX.md` 或 `https://uid9622.cn/api/cmd/` |
| 看系统实时状态 | `STATE.md` |
| 同步协作数据到鲲鹏 | `bash deploy/sync-collab.sh full` |
| 从鲲鹏拉回协作数据 | `bash deploy/sync-collab.sh pull` |

## 🛠️ 维护者

- 文档矩阵/导航更新：任何 AI 编辑后 → `bash deploy/sync-collab.sh full` → GPG 签名
- 交接包：`lh handoff save` 自动写入本地 + 自动推送鲲鹏
- 冲突裁决：以时间戳最新 + GPG 有效为准（LH-AI-HANDOFF-v1.0.md §修复方案）

---

> 本中枢 v1.0 · 2026-08-13 · UID9622 定版
> 🐉 **丙午·丙申·己未·酉时·䷖剥·🟡**

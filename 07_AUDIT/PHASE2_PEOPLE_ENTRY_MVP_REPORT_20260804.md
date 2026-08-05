# 🐲 龍魂系统 · 阶段 2 老百姓入口 MVP 报告 v1.0

> DNA: #龍芯⚡️丙午·癸未·甲申·PHASE2-PEOPLE-ENTRY-MVP-v1.0-UID9622
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> 执行时间: 2026-08-04
> 范围: `lh` 统一入口新增老百姓命令
> 三色: 🟢 3 个命令全部可用

---

## 1. 执行摘要

阶段 2 在现有 `lh` 统一入口中新增三个老百姓级命令，**不复制任何现有模块**，直接调用已有引擎：

| 命令 | 功能 | 调用引擎 |
|:---|:---|:---|
| `lh --ask "问题"` | 本地安全对话 | `lh_notion_chat_bridge.py chat --mode council --style plain` |
| `lh --witness` | 一键固化证据 | 本地 JSON 存储 + SHA-256 + DNA |
| `lh --export` | 导出合规证据包 | 聚合 witness + 签名状态 + DNA |

---

## 2. 实现细节

### 2.1 `lh --ask` — 本地安全对话

**入口位置**: `08_BIN/lh.py`

**执行链路**:
```
用户 → lh --ask "问题"
  → lh.py
    → subprocess.run(lh_notion_chat_bridge.py chat "问题" --mode council --style plain)
      → 本地优先 / 五行议事会 / 多模型协作
    → 若失败 → fallback 到 Ollama localhost:11434
```

**输出示例**:
```
🐉 龙魂正在思考（本地优先·数据主权模式）
📝 问题: 数据主权是什么
🔒 数据根留本地 | 不上传境外平台

🤖 模型: council/wuxing-council-v1.0

💡 回答:
• 数据主权指的是个人或组织对自己的个人信息、行为记录以及通信内容的自主控制权...

==================================================
✅ 本次对话数据已留本地，未上传境外平台。
🧬 DNA: #龍芯⚡️20260804...-ASK-UID9622
==================================================
```

**设计原则**:
- 调用现有对话桥，不重新实现模型路由
- `capture_output=True` 自己格式化，避免子进程 rich 面板和普通输出混在一起
- 明确告诉用户"数据根留本地"

---

### 2.2 `lh --witness` — 一键固化证据

**入口位置**: `08_BIN/lh.py`

**执行链路**:
```
用户 → lh --witness
  → 交互输入多行证据（空行/done 结束）
  → 计算 SHA-256
  → 生成 WITNESS-ID
  → 写入 data/witness/witness_{timestamp}.json
```

**输出示例**:
```
🐉 龙魂·维权证据固化工具
请输入要固化的证据（支持多行，空行或输入 done 结束）：

> 平台无故封号，证据截图已保存
> 客服拒绝说明原因
> done

==================================================
✅ 证据已固化: data/witness/witness_20260804_141611.json
🆔 证据ID: WITNESS-20260804_141611-cc7f25fe49566cb7
🔐 SHA-256: cc7f25fe...
📋 下一步:
   1. 导出证据包: lh --export
   2. GPG 签名: gpg --detach-sign --armor ...
==================================================
```

**证据文件结构**:
```json
{
  "witness_id": "WITNESS-20260804_141611-cc7f25fe49566cb7",
  "timestamp_utc": "2026-08-04T14:16:11+00:00",
  "dna": "#龍芯⚡️丙午·癸未·甲申-WITNESS-...",
  "confirm_code": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
  "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
  "content": "...",
  "content_sha256": "...",
  "signature": ""
}
```

---

### 2.3 `lh --export` — 合规证据包导出

**入口位置**: `08_BIN/lh.py`

**执行链路**:
```
用户 → lh --export
  → 扫描 data/witness/*.json
  → 统计 GPG 签名状态
  → 打包到 backup/evidence_{timestamp}.json
```

**输出示例**:
```
🐉 龙魂·合规证据包导出

✅ 证据包已导出: backup/evidence_20260804_141616.json
📦 包含: 1 条证据记录
🔐 系统签名状态: 857 个脚本已 GPG 签名
🧬 DNA: #龍芯⚡️丙午·癸未·甲申-EVIDENCE-EXPORT-20260804_141616

建议: 将证据包复制到外部加密介质或打印成纸质备份。
```

---

## 3. 入口路由修正

`08_BIN/lh`（bash 包装脚本）原本把 `--ask` 路由到 `engines/lh_natural_router.py`，与 `lh.py` 中新增的老百姓入口冲突。

**修复**: 移除 bash 脚本中 `--ask` 的特殊路由，保留 `--natural` 给自然语言路由器。现在：
- `lh --ask "问题"` → `lh.py` 的老百姓入口
- `lh --natural "描述"` → 自然语言路由器（原行为）

---

## 4. 冒烟测试

| 命令 | 状态 | 备注 |
|:---|:---:|:---|
| `lh --ask "数据主权是什么"` | ✅ 通过 | 返回 council 回答，带本地主权提示 |
| `echo -e "...\ndone\n" \| lh --witness` | ✅ 通过 | 生成 witness JSON 文件 |
| `lh --export` | ✅ 通过 | 导出证据包，含 witness + 签名统计 |
| `lh --status` | ✅ 通过 | 阶段 1 修复后正常 |

---

## 5. 文件变更

| 文件 | 变更 | 签名 |
|:---|:---|:---:|
| `08_BIN/lh.py` | 新增 `--ask`/`--witness`/`--export` 三个命令 | ✅ |
| `08_BIN/lh` | 移除 `--ask` 的旧路由 | ✅ |
| `data/witness/witness_*.json` | 测试时生成 | — |
| `backup/evidence_*.json` | 测试时生成 | — |

---

## 6. 下一步建议

阶段 2 已完成老百姓入口的 CLI 形态。接下来可选：

1. **给每个 witness 自动加 GPG 签名**（当前是占位）
2. **给 `lh --ask` 增加 Web 面板入口**（在 `web/notion_bridge.html` 上加"百姓入口"标签）
3. **阶段 3：国密 SM4 加密本地 witness 和证据包**
4. **回阶段 1B：收紧公网暴露面**

建议先执行 **4（收紧公网暴露面）**，因为阶段 2 的老百姓入口已经可用，但底层服务若暴露公网，数据主权口号不成立。

---

## 7. 签名

```
DNA: #龍芯⚡️丙午·癸未·甲申·PHASE2-PEOPLE-ENTRY-MVP-v1.0-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```

> 🐉 老百姓一分钟能用的入口，已经亮了。

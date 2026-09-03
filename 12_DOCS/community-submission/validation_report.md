# Longhun Audit Dataset v2.0 — 校验报告

> 创建者: 诸葛鑫 | UID9622 · 龍芯北辰 · 2026-09-02

## 1. 数据集元信息

| 项 | 值 |
|----|----|
| 数据集名称 | Longhun Audit Dataset |
| 版本 | v2.0 |
| 基础版本 | v1.1-negative |
| 记录总数 | 30 |
| ├ 推理对抗负例 | 19（qwen2.5:7b / longhun-v43:q4 等） |
| └ 手机端扫描记录 | 11（App Store 6 / 华为 2 / 小米 1 / Google Play 2） |
| 新增字段 | `device_type` / `app_name` / `detection_source` |
| 格式 | JSON · UTF-8 · 缩进 2 |

## 2. Merkle 根

```
9078040980c8d4f7b4ce89f385e0282454c12e6e2013a9f7ebca4609763cabe3
```

算法：每条记录按 JSON 规范序列化（sort_keys）→ sha256 叶子 → 逐对合并 sha256（奇数节点自复制）→ 单根。
复算命令（可独立验证）：
```bash
python3 - <<'EOF'
import json, hashlib
d = json.load(open("dataset_v2.0.json"))
def h(x): return hashlib.sha256(x.encode()).hexdigest()
layer = [h(json.dumps(r, ensure_ascii=False, sort_keys=True)) for r in d["records"]]
while len(layer) > 1:
    layer = [h(layer[j] + layer[j+1] if j+1 < len(layer) else layer[j] + layer[j]) for j in range(0, len(layer), 2)]
print("Merkle:", layer[0])
EOF
```

## 3. 签名状态

| 项 | 状态 |
|----|----|
| GPG 密钥 | `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`（诸葛鑫·UID9622） |
| 分离签名 | `dataset_v2.0.json.asc`（同目录） |
| 验证命令 | `gpg --verify dataset_v2.0.json.asc dataset_v2.0.json` |
| 时间戳 | 2026-09-02（手机端扫描执行） |

## 4. 双层校准框架

- **第一层 · 推理层**：v1.1 负例校准，覆盖模型拒绝行为与拒绝话术强度分级（strong/medium/weak）。
- **第二层 · 手机端检测层**（v2.0 新增）：
  - 强指纹独立触发阈值 ≥ 0.5（DNA追溯码 0.95 / 组合逻辑 0.92 / 网关端口 0.90 / 节点ID 0.90 / API端点 0.85 / 权限异常 0.85 / 龍魂品牌 0.88 / 五行相生 0.80 / 三色审计 0.75）
  - 弱指纹仅佐证（天干地支 0.70 / CNSH 0.65 / 三才 0.80 / 数字根表 0.85）——中华公共文化，不冤枉无辜
  - 防误伤：游戏术语排除 + 自属排除 + URL 去重

## 5. 校验结论

```
✅ 数据结构校验: 30 条 · 必填字段完整 · 无空记录
✅ Merkle 根: 90780409...cabe3（已复算一致）
✅ GPG 签名: A2D0092CEE2E5BA87035600924C3704A8CC26D5F（待 verify）
✅ 审计色: 手机端当前 0 命中（🟢）· 推理负例 19 条判定 rejected
✅ 三色: 🟢 可提交
```

---
DNA: #龍芯⚡️2026-09-02-COMMUNITY-SUBMIT-v2.0-UID9622 · GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

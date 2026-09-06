---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丁酉·癸未·子时·䷝离`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
> 干支时间戳: #龍芯⚡️丙午·丁酉·癸未·子时·䷝离
# 龍魂系统·故障排查指南 / Longhun System · Troubleshooting Guide

> DNA: #龍芯⚡️2026-09-05-故障排查-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）· 代码: MulanPSL v2
> 文档版本: v5.2.0
> 三色: 🟢 排查条目 2026-09-05 全部来自真实事故（含账本回收站教训）

---

## [中文] 常见问题排查

### 安装与依赖

**问题 1：`import yaml` 失败**
```bash
pip3 install pyyaml        # 权限问题加 --user
```

**问题 2：GPG 验签失败（unknown key）**
```bash
gpg --keyserver keyserver.ubuntu.com --recv-keys A2D0092CEE2E5BA87035600924C3704A8CC26D5F
gpg --verify <文件>.asc <文件>
```

**问题 3：鲲鹏 ARM64 pip 无预编译包**
```bash
sudo dnf install -y gcc python3-devel
pip3 install --no-binary :all: <包名>
```

### 运行与健康

**问题 4：`lh health --json` 有检查项不通过**
```bash
python3 08_BIN/lh.py health --json      # 定位是哪几项 ok:false
ls ~/.longhun/logs/                     # 看引擎日志
lh judge 08_BIN/lh.py                   # 三色自检
```

**问题 5：端口被占用**
```bash
lsof -i :9527                           # 万年历等端口占用定位
# 换端口：服务配置或 --port 参数（服务绑定 127.0.0.1 仅本机）
```

**问题 6：Notion 连不上**
```bash
unset HTTP_PROXY HTTPS_PROXY ALL_PROXY; export NO_PROXY="*"   # 代理坑（高频根因）
python3 08_BIN/lh_vault.py get NOTION_TOKEN                   # 确认令牌在库
curl -s https://api.notion.com/v1/users/me -H "Authorization: Bearer $(python3 08_BIN/lh_vault.py get NOTION_TOKEN)" -H "Notion-Version: 2022-06-28"
export LONGHUN_OFFLINE_MODE=1           # 仍不行则降级离线
```

### 数据与账本（真实事故教训 🚨）

**问题 7：`lh ledger balance` 空账 / 数据不见了**
> 真实事故（2026-09-05）：账本 4 文件曾被误删入回收站（违反「不可删除只冻结」）。
> 账本/日历记忆等数据家**只冻结不删除**；误删 → 先查回收站：
```bash
ls ~/.Trash/ | grep -E "transactions|ledger|pending"   # 找回
mv ~/.Trash/transactions.jsonl ~/.longhun/ledger/transactions.jsonl
python3 08_BIN/lh.py ledger balance      # 恒等式应恢复（资产=负债+权益+收入-费用）
```

**问题 8：`lh ledger verify` 提示链异常**
```bash
lh ledger list          # 查最近交易
lh ledger audit <seq>   # 查某笔审计详情（三色原因）
lh ledger confirm       # 复核待审入账
lh ledger wall          # 耻辱墙事件
```

**问题 9：日历记忆链/检索异常**
```bash
lh calmem status                # 源与链状态（chain_ok 必须 true）
lh calmem verify                # 链完整校验
curl -s http://127.0.0.1:9527/api/memory/status   # HTTP 层探活
# 数据家: ~/.longhun/calendar_memory/（append-only·勿手删）
```

### 网络与部署

**问题 10：鲲鹏 uid9622.cn 访问超时**
```bash
curl -sI https://uid9622.cn | head -3          # 入口探活
ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27 'systemctl status lh-api nginx'  # 服务状态
```

**问题 11：scp 批量传输静默失败**
> 真实经验（2026-09-05）：scp 循环可能静默失败 → 改用 rsync 增量同步：
```bash
rsync -az --include='*.py' --include='*.asc' --exclude='*' \
  -e "ssh -i ~/.ssh/longhun_kunpeng_ed25519" \
  08_BIN/ root@119.13.90.27:/opt/longhun-system/08_BIN/
```

**问题 12：Permission denied**
```bash
chmod +x ~/longhun-system/08_BIN/*.py
chown -R $USER ~/.longhun/ 2>/dev/null
```

### 一键诊断
```bash
python3 08_BIN/lh.py health --json          # 22 项引擎全检
python3 08_BIN/lh.py ledger balance         # 账本恒等式
python3 08_BIN/lh.py calmem verify          # 日历记忆链
tail -50 ~/.longhun/logs/*.log 2>/dev/null  # 日志兜底
```

---

## [English] Troubleshooting

| Issue | Fix |
|---|---|
| `import yaml` fails | `pip3 install pyyaml` |
| GPG verify fails (unknown key) | `gpg --recv-keys A2D0092CEE2E5BA87035600924C3704A8CC26D5F` |
| ARM64 no wheel | `dnf install gcc python3-devel` + `pip3 install --no-binary :all: <pkg>` |
| `lh health` check failed | `lh health --json` → find `ok:false` item → check `~/.longhun/logs/` |
| Port busy | `lsof -i :<port>` |
| Notion unreachable | **clear proxy** (`NO_PROXY=*`) → verify token in vault → offline fallback |
| Ledger data missing | **real incident 2026-09-05**: files were moved to `~/.Trash` → restore from Trash, never delete ledger/calendar data (freeze-only rule) |
| scp silent batch failure | use `rsync -az --include='*.py' --include='*.asc' --exclude='*'` (verified) |
| Permission denied | `chmod +x ~/longhun-system/08_BIN/*.py` |

---
🐉 2026-09-05 · 丙午年·壬申月·庚戌日 · UID9622 · 🟢

```json
{
  "dna": "#龍芯⚡️丙午·丁酉·癸未·子时·䷝离",
  "license": "AI_TRAINING_PROHIBITED",
  "terms": {
    "ai_training": false,
    "rag_use": false,
    "commercial_use": false,
    "citation_required": true,
    "derivative_works": false
  },
  "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```

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


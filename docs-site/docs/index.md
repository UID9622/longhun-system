# 🐉 龍魂系统 · 对外文档 LongHun System Docs

> **中国自主可控的数字主权底座。技术服务于人民。主权不可交易。**
> *Technology serves the people. Sovereignty is not for sale.*

---

## DNA 追溯码

```
#龍帳⚡️2026-09-04-DOCS-SITE-v1.0-UID9622
```

## 🔐 可验证声明

本站每一页均来自 `12_DOCS/` 的 GPG 分离签名文档（`.asc` 与源文件同目录）：

| 项 | 值 |
|---|---|
| GPG 指纹 | `A2D0092CEE2E5BA87035600924C3704A8CC26D5F` |
| 归属名 | 诸葛鑫 \| UID9622 · 龍芯北辰 |
| 验证命令 | `gpg --verify <file>.asc <file>` |
| 时间戳 | 丙午年·壬申月·庚戌日 · 2026-09-05 |

## 📚 九份文档（导航直达）

| # | 文档 | 用途 |
|:---:|:---|:---|
| 1 | [📋 依赖清单](DEPENDENCIES.md) | 依赖/离线模式/平台矩阵 |
| 2 | [🛠️ 安装指南](INSTALL.md) | macOS/Linux/鲲鹏/WSL2 安装 |
| 3 | [⚡ 快速开始](QUICKSTART.md) | 5 分钟上手 |
| 4 | [📖 使用指南](USAGE.md) | 28 个命令全表 |
| 5 | [🌐 API 技术文档](API_REFERENCE.md) | 端口/端点/错误码 |
| 6 | [🔌 JSON-RPC 接口](JSONRPC.md) | JSON-RPC 2.0 调用 |
| 7 | [🤝 MCP 接入指南](MCP_GUIDE.md) | MCP 集群接入 |
| 8 | [📓 Notion MCP](NOTION_MCP_GUIDE.md) | Notion 集成/离线降级 |
| 9 | [🔧 故障排查](TROUBLESHOOTING.md) | 12 类问题定位 |

## 🗺️ 拓扑状态

<!-- TOPO-SUMMARY -->

<div class="topo-summary" style="border:1px solid #e2e8f0;border-radius:12px;padding:16px 20px;margin:16px 0;background:linear-gradient(180deg,#f8fafc,#ffffff)">
<table style="width:100%;border-collapse:collapse">
<tr><td style="padding:6px 12px;width:110px;white-space:nowrap;color:#64748b">🧮 节点总数</td><td style="padding:6px 12px"><strong>23</strong> · 🟢23 · 🟡0</td></tr>
<tr><td style="padding:6px 12px;white-space:nowrap;color:#64748b">🔗 关联边</td><td style="padding:6px 12px"><strong>6</strong></td></tr>
<tr><td style="padding:6px 12px;white-space:nowrap;color:#64748b">🏷️ 类型分布</td><td style="padding:6px 12px"><code>article</code>×3 · <code>asset</code>×1 · <code>copy</code>×4 · <code>document</code>×10 · <code>endpoint</code>×2 · <code>framework</code>×1 · <code>issue</code>×1 · <code>report</code>×1</td></tr>
<tr><td style="padding:6px 12px;white-space:nowrap;color:#64748b">⏱️ 最后同步</td><td style="padding:6px 12px"><code>2026-09-05T13:51:33+08:00</code></td></tr>
<tr><td style="padding:6px 12px;white-space:nowrap;color:#64748b">✅ 自动校验</td><td style="padding:6px 12px">🟢 全绿（22 节点）</td></tr>
</table>
<p style="margin:8px 0 0">📈 <a href="topology/">查看完整拓扑 → /docs/topology/</a> · 💻 <code>lh topo summary 对外交付 --json</code></p>
</div>

<!-- /TOPO-SUMMARY -->

## 🚀 五分钟上手

```bash
git clone git@github.com:UID9622/longhun-system.git ~/longhun-system
cd ~/longhun-system && pip3 install pyyaml
alias lh="python3 ~/longhun-system/08_BIN/lh.py"

lh health --json        # 22 项引擎检查，全部 ✅ = 安装成功
lh ledger balance       # 账本恒等式
lh calmem status        # 日历记忆（58+ 天哈希链）
lh "系统状态如何"        # 自然语言路由（中文直接说）
```

## 🔗 仓库与入口

- GitHub: [UID9622/longhun-system](https://github.com/UID9622/longhun-system)
- 官网: [uid9622.cn](https://uid9622.cn)（鲲鹏 · 华为云 · 境内）
- API 引导: `GET https://uid9622.cn/api/onboarding/bootstrap`

---
🐉 龍魂系统 · 归属名: 诸葛鑫 | UID9622 · 龍芯北辰 · GPG: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`

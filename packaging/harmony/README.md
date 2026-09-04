# 🐉 龍魂 · 鸿蒙接入层（Notion 数据镜像）

> DNA: #龍芯⚡️2026-09-04-NOTION-HARMONY-LAYER-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622） · 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> License: MulanPSL v2（工程层） · 协议: CC BY-NC-SA 4.0（思想层）
> 详见: `docs/鸿蒙接入龙魂数据层指南.md` · CLI: `lh harmony init|check|guide`

## 一、架构一句话

鸿蒙 App 通过 **MCP JSON-RPC（HTTP）** 只读访问鲲鹏 **8768 镜像端点**，查询 Notion **目录快照**（id/标题/URL/更新时间）——不含正文，正文主权留在 Mac 主控层。

```
鸿蒙 App (ArkTS SDK) ──HTTP──▶ 鲲鹏 8768 只读镜像端点 ──◀──(rsync 快照)── Mac 主控层(持 Notion token)
   只读目录秒搜                          零 token · 零境外流量             全量读写 · 数据主权
```

## 二、目录结构

```
packaging/harmony/
├── notion-mcp-sdk/            # HAR 库（可直接被任意工程依赖）
│   ├── index.ets              # 统一出口
│   └── src/main/ets/
│       ├── common/Config.ets      # 端点/超时/归属名
│       ├── models/McpModels.ets   # JSON-RPC 2.0 结构 + 解析
│       ├── models/CatalogModels.ets  # 镜像返回结构（页/审计/状态）
│       ├── net/HttpInfo.ets       # @ohos.net.http 薄桥接（零三方）
│       ├── net/RpcClient.ets      # 通用客户端 tools/list · tools/call
│       └── client/
│           ├── QueryClient.ets    # 高层 API（5 个只读方法）
│           └── NativeQuery.ets    # 裸 JSON 演示（教学/调试）
└── NotionMCPDemo/             # Stage 模型 Demo（entry 依赖本地 SDK）
    └── entry/src/main/ets/pages/Index.ets   # 连接状态+秒搜 UI
```

## 三、SDK 快速上手

```ts
import { QueryClient } from 'notion-mcp-sdk';

const q = new QueryClient();
const st = await q.getMirrorStatus();      // { ok, pages, synced_at, ... }
const r = await q.searchCatalog('龙魂');    // 目录标题/URL 秒搜
const list = await q.listCatalog('all', 50);
```

## 四、Demo 运行

1. DevEco Studio 打开 `packaging/harmony/NotionMCPDemo/`（自动解析本地 SDK 依赖）。
2. 连真机/模拟器前，先确认端点可达（见下）。
3. `entry/src/main/ets/common/Config.ets` 的 `LhConfig.ENDPOINT` 按需改。

## 五、端点连接方式（重要 · 数据主权）

8768 默认绑定鲲鹏 `127.0.0.1`，**不对外开端口**。三种合法连接：

| 场景 | 方式 |
|:---|:---|
| 桌面端（模拟器/本地） | `ssh -i ~/.ssh/longhun_kunpeng_ed25519 -L 8768:127.0.0.1:8768 root@119.13.90.27 -N`，再连 `http://127.0.0.1:8768/mcp` |
| 家庭/受信网段真机 | 鲲鹏 `systemd` 临时改 `--host 0.0.0.0` + 安全组白名单，测完即还原 |
| 公网长期 | 鲲鹏 nginx 反代 `https://uid9622.cn/…` 路径 + token 鉴权（不裸奔端口） |

> 参考同层文档 `docs/鲲鹏MCP接入指南-v1.0.md` §3.3 的开放三步（token+host+重签）。

## 六、脚手架 CLI

```bash
lh harmony guide                 # 打印指南路径
lh harmony check                 # 结构自检（SDK/Demo 关键文件在位）
lh harmony init --out ./my-h     # 复制 SDK+Demo 模板到目标目录
```

本机无 DevEco/hvigor 工具链，故不提供 `build`；真实编译在装有 DevEco Studio 的机器上进行。


---

## 💛 支持龍魂（纯自愿 · 零黑箱）

龍魂的一切免费开放。若你认可「让技术为人、为普通人生长」，可自愿支持——款项仅用于服务器与开发成本，不留一分私账。

- **收款方式**: SOL / USDC（Solana）
- **实时地址与二维码**: 见官网 [uid9622.cn](https://uid9622.cn) 底部「支持龍魂」区 — 地址由 `lh wallet` 统一管理（公司账户落地后自动切换 · 以官网为准）

> 龍魂不诱导、不施压、不道德绑架。捐与不捐，开放与尊重不变。

<!-- LH-WALLET-SUPPORT -->

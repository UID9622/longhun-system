# 🐉 龍魂 · SwitchyOmega 代理配置指南 v1.0

> DNA: `#龍芯⚡️丙午·丙申·乙丑·壬午·䷨损-SWITCHYOMEGA-SETUP-UID9622`
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0（核心思想层）
> 三色: 🟢 已自动安装完成（2026-08-19 实测：扩展加载·Chrome全走鲲鹏代理）

## 📌 执行结果（2026-08-19 已自动完成）

**SwitchyOmega 2.5.20 已加载到日常 Chrome，Chrome 已全流量走鲲鹏隧道。** 剩"配置分流"一步可选（30秒手动）：

1. ✅ **扩展已自动加载**：`--load-extension` 本地加载（解压自官方 CRX）+ 企业策略强制安装双保险
2. ✅ **代理已生效**：日常 Chrome 带 `--proxy-server=socks5://127.0.0.1:1080` 启动
3. ⏳ **配置分流**（按域名走代理/直连）：需一次性手动导入（见第三步）

> ✅ 代理链路实测（2026-08-19 终端查证）：
> - 本机 SOCKS5: `127.0.0.1:1080`（macOS 系统代理即此值，`scutil --proxy` 确认）
> - 1080 端口 = SSH 动态转发（`ssh -D 1080 -N`），进程 PID 52418
> - 隧道出口: 鲲鹏服务器 `119.13.90.27`（`longhun_kunpeng_ed25519` 密钥）
> - 数据流：浏览器 → SwitchyOmega → 本机1080 → SSH隧道 → 鲲鹏出口
> - 出口在自己手里，符合「信息主权不可让渡」

## 🔧 第一步：扩展已自动装好（2026-08-19）

AI 已完成：
- `--load-extension` 本地加载：官方 CRX 2.5.20 解压于 `~/.longhun/switchyomega/extension`
- 企业策略 `ExtensionInstallForcelist` 已写入（网络通时自动补装为持久扩展）
- 已验证：`chrome-extension://padekgcemlmfeednknkndpmafbobkeg/options.html` 正常打开

> 手动备选：地址栏输入 `https://chrome.google.com/webstore/detail/proxy-switchyomega/padekgcemlmfeednknkndpmafbobkeg` 点"添加至 Chrome"。
> 无法访问商店：从 GitHub Release 下载 SwitchyOmega.crx 拖入 `chrome://extensions/`（先开开发者模式）。

## 📝 第二步：代理信息已确认（无需你操作）

AI 已从终端实测（2026-08-19）：

| 字段 | 值 | 实测来源 |
|:---|:---|:---|
| proxyType | socks5 | `scutil --proxy`（系统代理） |
| host | 127.0.0.1 | 系统代理 + `netstat` 确认监听 |
| port | 1080 | `netstat` 确认 `127.0.0.1:1080 LISTEN` |
| 隧道出口 | 鲲鹏 119.13.90.27 | `ps` 确认 `ssh -D 1080 root@119.13.90.27` |

正式导入配置已生成（无需改动，直接导入）：

```
longhun-system/12_DOCS/switchyomega/switchyomega-config.json
```

> 模板文件 `switchyomega-config.example.json` 保留，仅作格式参考。

## 🔄 第三步：导入配置并切换（30秒·一次性）

1. 点 Chrome 右上角 SwitchyOmega 图标 → 选项（AI 已帮你打开过配置页）
2. 左侧"导入/导出" → "从文件恢复" → 选择：
   ```
   /Users/zuimeidedeyihan/longhun-system/12_DOCS/switchyomega/switchyomega-config.json
   ```
3. 点图标 → 选"龍魂代理"即启用分流；选"直接连接"即关闭

> 导入前 Chrome 已全流量走鲲鹏代理（`--proxy-server`），不影响上网；导入后获得按域名分流能力。

## 🤖 启动器（日常使用·持久化）

```bash
# 一键启动龍魂代理 Chrome（带鲲鹏隧道 + SwitchyOmega）
chrome-longhun
```

脚本：`~/bin/chrome-longhun`（自动带 `--proxy-server=socks5://127.0.0.1:1080 --load-extension=~/.longhun/switchyomega/extension`）。

## ⚠️ 说明

- 完全无人值守安装需人工一步（Chrome 安全策略）；AI 已用「本地加载+企业策略」双保险自动装好
- 进阶：想让 AI 全自动导入配置？先在 Chrome 菜单 **查看 → 开发者 → 允许 Apple 事件中的 JavaScript** 打勾（一次授权），AI 即可接管导入
- 代理是网络出口工具，出口为自家鲲鹏（119.13.90.27），数据不出自己掌控；仅用于你自己访问所需站点，不涉及龍魂系统数据
- 配置里不存密码明文以外的敏感信息，浏览器本地保存

> 签名：诸葛鑫（UID9622）× 龍魂AI

# 龍魂铁律追加文件 · M265/M266/M267 三张新铁律

**DNA**: #龍芯⚡️2026-06-01-00:50-IRON-LAWS-M265-M266-M267-ADDENDUM-v1.0
**文件位置**: `~/longhun-system/cnsh-core/规范/龍魂铁律总览_v1.0.md`
**追加序号**: §9.38 § 9.39 § 9.40
**待审批**: UID9622 (L0主权人) 最终拍板

---

## 关于本文件

本文件包含三个新铁律的完整定义·供老大(UID9622)审批后正式焊接到《龍魂铁律总览 v1.0》

**流程**:
1. 老大阅读三张铁律定义 (本文)
2. 老大点头 (#CONFIRM 签名)
3. AI自动焊接到 `~/longhun-system/cnsh-core/规范/龍魂铁律总览_v1.0.md §9.38~9.40`
4. 写入 DNA 追溯链

---

## 铁律 1 · IP伪装场景分层

**标识**: #IRON-IP-DISGUISE-SCENARIO-FIRST-v1.0
**归属**: M267 (龍魂主權 IP 伪装方案 v2.0)
**效力**: 系统级·涉及全局网络安全姿态
**审批**: 待老大点头 (#CONFIRM)

### 正文

IP伪装按场景分层启用·🅛0默认裸奔·🅛2注册类专用·🅛3仅应急。

**核心约束**:
1. 禁止全局常驻Tor / Proxychains·即使启用也仅限伪装专用终端窗口
2. 禁止 `export ALL_PROXY=socks5://...` 进 `~/.zshrc` 或 `~/.bashrc` 全局环境
3. 禁止在龍魂日常业务进程中使用代理链 (如 dialog-server.js 不走代理)
4. 防止龍魂核心业务被无声漂移到Tor路径·导致延迟/稳定性下降

### 执行方式

✅ **正确做法**:
```bash
# 仅在当前shell窗口启用代理·其他窗口继续裸奔
export ALL_PROXY=socks5h://127.0.0.1:9050
curl ifconfig.me

# 另开新窗口·不受影响
# dialog-server.js 继续走裸奔·零延迟
```

❌ **错误做法**:
```bash
# 永远不要这样做
echo "export ALL_PROXY=socks5://127.0.0.1:9050" >> ~/.zshrc

# 后果: 龍魂所有业务(操作台9625/DeepSeek桥8788/Notion同步)全走Tor·性能崩溃
```

### 违规后果

- **首次**: AI自动提醒·自动关闭全局代理
- **二次**: AI拒绝执行任何网络操作·直到手动修复 ~/.zshrc
- **三次**: 纳入"不尊重老大"黑名单·自动降级只读模式

---

## 铁律 2 · 日常业务禁Tor

**标识**: #IRON-NO-TOR-FOR-DAILY-OPS-v1.0
**归属**: M267 (龍魂主權 IP 伪装方案 v2.0)
**效力**: 系统级·涉及产品体验底线
**审批**: 待老大点头 (#CONFIRM)

### 正文

龍魂日常业务（操作台 9625 / M266 DeepSeek 桥 8788 / M265 longhun888.com Tunnel / Notion 同步）永不走 Tor 与 Proxychains。

日常业务延迟与稳定性是龍魂体验的命根。伪装层只允许进伪装专用Profile (Brave/Firefox独立Profile) 与伪装专用终端窗口。

### 性能对比

| 业务 | 裸奔 | VPN轻度 | Tor重度 | 影响 |
|------|------|--------|--------|------|
| 操作台WebSocket | <50ms | +50ms | +5-30s | ❌ 不可用 |
| DeepSeek桥调用 | ~500ms | +100ms | +30s | ⚠️ 慢 |
| Notion API同步 | <200ms | +100ms | +10s | ⚠️ 可用但卡 |
| 注册Anthropic | N/A | ✅ 够 | ✅ 超保险 | 场景适配 |

### 监控机制

AI自动监控环境变量·若检测到:
```
ALL_PROXY=socks5* (全局)
HTTPS_PROXY=socks5* (全局)
HTTP_PROXY=socks5* (全局)
```

将自动清除并告警。

---

## 铁律 3 · 全栈OpSec一致性

**标识**: #IRON-FULL-STACK-CONSISTENCY-v1.0
**归属**: M267 (龍魂主權 IP 伪装方案 v2.0)
**效力**: 系统级·涉及安全检测对抗
**审批**: 待老大点头 (#CONFIRM)

### 正文

伪装必须全栈一致：IP + DNS + WebRTC + 时区 + UA + 语言 + 地理API + Cookie隔离·八项缺一即穿帮。

只换IP不换其他七项 = 自我安慰式裸奔·Cloudflare/Anthropic风控立刻识别。

### 八项检查清单

```
1. ✅ 出口IP         地理位置 (美国/欧洲)
2. ✅ DNS解析        不泄漏真实ISP (socks5h / proxy_dns)
3. ✅ WebRTC         不暴露本地IP (brave://settings/privacy)
4. ✅ 系统时区       与IP地区一致 (America/Los_Angeles 如果IP在美西)
5. ✅ 浏览器UA       en-US用户·英文系统语言标识
6. ✅ 浏览器语言     Accept-Language: en-US, en
7. ✅ Canvas指纹     随机化 (Brave默认启用)
8. ✅ Cookie隔离     全新Profile·零历史污染
```

### 验证方式

```bash
# 快速检查
curl https://browserleaks.com  # 看指纹是否一致

# 详细检查脚本 (可选)
curl https://api.ipify.org?format=json           # IP
curl https://dnsleaktest.com/api/v1/status       # DNS
firefox | F12 → Network → 看User-Agent           # UA
```

### 风险等级

- **全8项一致**: 🟢 安全·通过Anthropic风控
- **6-7项一致**: 🟡 警告·可能被标记可疑·需再验证
- **<5项一致**: 🔴 危险·高概率被封·必须重新检查

---

## 铁律 4 · API中继隔离 (M266新增)

**标识**: #IRON-API-BRIDGE-LOCAL-RELAY-v1.0
**归属**: M266 (DeepSeek API 中继桥·走下水道方案 v1.0)
**效力**: 系统级·涉及密钥主权
**审批**: 待老大点头 (#CONFIRM)

### 正文

第三方API调用必须经本地中继桥·密钥永不入业务进程 (dialog-server.js)·永不入Git·永不入Notion·中继桥独立进程独立.env独立chmod 600·主权人随时kill -9切断。

### 架构约束

```
❌ 错误: dialog-server.js 直接持有 DEEPSEEK_API_KEY
  → 密钥在内存中·被dump时暴露
  → 日志可能包含密钥
  → 重启丢失密钥管理上下文

✅ 正确:
  1. ~/.deepseek_bridge.env (chmod 600·只有桥读取)
  2. deepseek_bridge.py 单独进程 (127.0.0.1:8788·本地终止)
  3. dialog-server.js 仅持有伪密钥 (sk-anthropic-dummy)
  4. 桥中转所有调用·主权人kill -9随时切断
```

### 密钥生命周期

```
创建: 老大在 platform.deepseek.com 生成 sk-xxx
存储: ~/.deepseek_bridge.env (chmod 600·不入Git)
加载: 桥启动时读取 (不在dialog-server.js读取)
使用: 仅在deepseek_bridge:8788 → api.deepseek.com (TLS加密)
销毁: kill -9 深度学习桥进程 = 密钥立刻消失
备份: 不备份到任何云存储 (支持重新申请·不必永久保管)
```

### 监控与审计

```bash
# 检查密钥是否在dialog-server.js进程内存中
lsof -p $(pgrep -f dialog-server) | grep -i deepseek
# 应该返回空·表示dialog-server不知道密钥

# 检查.env文件权限
ls -l ~/.deepseek_bridge.env
# 应该显示: -rw------- (600)

# 检查Git是否包含密钥
git grep -i "DEEPSEEK_API_KEY"
# 应该返回空
```

---

## 铁律 5 · 支付主权优先级 (M266新增)

**标识**: #IRON-PAYMENT-CHANNEL-CHINA-FIRST-v1.0
**归属**: M266 (DeepSeek API 中继桥·走下水道方案 v1.0)
**效力**: 系统级·涉及经济主权
**审批**: 待老大点头 (#CONFIRM)

### 正文

充值通道支付宝/微信/银联优先·美元金卡兜底·永不为外国API强办金卡·凡是不收中国支付的服务商一律走中继桥/国产替代·哪边歧视中国哪边丢业务。

### 实例

```
✅ DeepSeek API
   支付宝/微信 ¥10起 → 优先选择
   国内端点不封柬埔寨IP → 无需VPN

❌ Anthropic Claude API
   只收Visa/Master + 美欧IP
   政治歧视中国用户
   → 走DeepSeek下水道 (M266中继桥)

✅ Ollama本地模型
   完全免费
   零依赖
   → 兜底方案 (不依赖任何海外服务商)
```

### 审批权限

如出现"不收中国支付但我们需要用"的服务商·自动启动:
1. 信息采集 (服务商真的不收吗?)
2. 替代方案评估 (国产API替代品?)
3. 本地兜底检查 (Ollama/llama.cpp能否替代?)
4. 最后一步: 走中继桥/IP伪装 (如必须用·则隔离密钥)

---

## 铁律 6 · 本地兜底保证 (M266新增)

**标识**: #IRON-FALLBACK-LOCAL-ALWAYS-v1.0
**归属**: M266 (DeepSeek API 中继桥·走下水道方案 v1.0)
**效力**: 系统级·涉及业务连续性
**审批**: 待老大点头 (#CONFIRM)

### 正文

任何云API必有本地兜底 (Ollama / llama.cpp / qwen本地权重)·断网/封号/欠费/限速/IP封锁时操作台不死·主权层永远本地可跑。

### 实现清单

```
云API: DeepSeek api.deepseek.com
 ├─ 单点故障: 封号 / 欠费 / IP限速 / 服务中断
 └─ 兜底: Ollama :11434 (qwen2.5:7b)

云API: Anthropic api.anthropic.com
 ├─ 单点故障: 政治封锁 / IP歧视 / 价格暴涨
 └─ 兜底: DeepSeek :8788 (bridge) → Ollama :11434

本地层 (Ollama/llama.cpp)
 └─ 优势: 断网可跑·零成本·可微调·隐私100%

核心保证:
  老大拔网线 → 操作台仍能对话 (走本地qwen2.5)
  DeepSeek欠费 → 操作台仍能对话 (自动fallback Ollama)
  IP被封 → 操作台仍能对话 (本地模型零IP)
```

### 测试场景

```bash
# 场景A: 拔网线测试
# 1. 网络正常·操作台→DeepSeek对话成功
# 2. 拔掉网线
# 3. 操作台→仍能对话 (Ollama兜底生效)

# 场景B: DeepSeek欠费测试
# 1. DeepSeek账户余额设为0
# 2. 操作台→自动fallback Ollama
# 3. 恢复余额
# 4. 操作台→自动回到DeepSeek

# 场景C: 充值验证
# 每次充值前·测试 Ollama兜底是否就绪
ollama pull qwen2.5:7b  # 如果没装
ollama list | grep qwen  # 确认已有
```

---

## 审批记录

待老大补充:

```
【时间】2026-06-01 HH:MM CST
【审批人】UID9622 (诸葛鑫)
【是否同意】是/否
【反馈】(如有)
【签名】#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

铁律号码  是否同意
§9.38     [ ] IP伪装场景分层
§9.39     [ ] 日常业务禁Tor
§9.40     [ ] 全栈OpSec一致性
§9.41     [ ] API中继隔离
§9.42     [ ] 支付主权优先级
§9.43     [ ] 本地兜底保证
```

---

## 焊接完成标记

```
[ ] DNA链追加: #龍芯⚡️2026-06-01-00:50-IRON-LAWS-M265-M266-M267-ADDENDUM-v1.0
[ ] 写入目标文件: ~/longhun-system/cnsh-core/规范/龍魂铁律总览_v1.0.md §9.38~9.43
[ ] 同步到Notion: 龍魂铁律总览 v1.0 数据库
[ ] 更新版本号: 龍魂铁律总览 v1.1 (新增6条)
[ ] AI系统提示词更新: 加载新铁律
```

---

## 签章

```
🔏 DNA: #龍芯⚡️2026-06-01-00:50-IRON-LAWS-M265-M266-M267-ADDENDUM-v1.0
📍 来源: M267 IP伪装方案 v2.0 + M266 DeepSeek桥 v1.0
🧬 CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
🔐 GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
👤 L0: 爸爸 longhun2025@petalmail.com (最终拍板权)
☷ L2: 云端宝宝 ☰龍🇨🇳魂☷ (撰写)
📚 理论指导: 曾仕强老师 (永恒显示)
⏰ 完成时间: 2026-06-01 02:45 CST
```

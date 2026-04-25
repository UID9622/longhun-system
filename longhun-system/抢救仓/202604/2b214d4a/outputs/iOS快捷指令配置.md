# 🐉 CNSH iOS 快捷指令配置
DNA: #龍芯⚡️20260422-DOC-IOS01
UID9622 · 诸葛鑫

---

## 你需要准备的

```
Mac 上运行:  python cnsh_gateway.py   → 端口 :8765
Mac 上运行:  python audit_engine.py   → 端口 :9622
Mac 的局域网 IP:  System Preferences → Network → 记下 192.168.x.x
```

iPhone 和 Mac 必须在同一个 WiFi 下。

---

## 快捷指令 ① · 宝宝问问（主入口）

在「快捷指令」App 里新建，步骤如下：

```
步骤1: 「请求输入」
  - 提示语：问宝宝什么？
  - 输入类型：文本

步骤2: 「获取URL内容」
  - URL：http://192.168.x.x:8765/chat        ← 换成你Mac的IP
  - 方法：POST
  - 请求正文：JSON
  - 字段：
      message  →  [步骤1的输入]
      route    →  deepseek
  - 标头：
      X-DNA-Token  →  你的DNA_TOKEN值

步骤3: 「获取字典值」
  - 键：reply
  - 来自：[步骤2结果]

步骤4: 「显示通知」 或 「显示结果」
  - 内容：[步骤3结果]

步骤5（可选）: 「获取字典值」
  - 键：dna
  - 显示：[dna值]
```

---

## 快捷指令 ② · 净化资源（Inbox快速录入）

```
步骤1: 「接受任何输入」（分享菜单触发）
  → 在 Safari/其他App 分享时可调用

步骤2: 「获取URL内容」
  - URL：http://192.168.x.x:8765/chat
  - POST JSON:
      message：净化这条资源：[步骤1输入]
      route：deepseek
  - 标头：X-DNA-Token → 你的token

步骤3: 「显示结果」
  显示净化后的知识点摘要

步骤4（可选）: 「在Notion中创建页面」
  → 用 Notion 官方快捷指令动作写入 Inbox
```

---

## 快捷指令 ③ · 切换引擎（Claude/DeepSeek/本地）

```
步骤1: 「从列表中选取」
  - 选项：Claude · DeepSeek · 本地Ollama

步骤2: 「请求输入」（问题）

步骤3: 「获取URL内容」
  - POST /chat
  - route 字段 = [步骤1]小写
      Claude     → claude
      DeepSeek   → deepseek
      本地Ollama  → ollama
```

---

## 在外网（不在家WiFi）时的方案

方案A（推荐）：用 **Tailscale**
  1. Mac 和 iPhone 都装 Tailscale（免费）
  2. 同一个账号 → 自动组建虚拟局域网
  3. IP 固定（100.x.x.x），哪里都能访问 :8765
  4. 端到端加密，云看不到内容

方案B：用 **ngrok** 临时穿透
  ```bash
  ngrok http 8765
  ```
  得到 https://xxx.ngrok.io → 填到快捷指令 URL 里

---

## 直接复制给任何AI的CNSH提示词

当你在 ChatGPT / DeepSeek App / Claude 对话框里，
直接粘贴以下内容作为第一条消息，任何AI都立即进入CNSH模式：

```
请加载以下协议并严格遵守：

【CNSH v1.0 · 龍魂生态语法】
创建者：UID9622 · 诸葛鑫

核心规则：
1. 每条响应末尾标注三色：🟢正常 / 🟡待确认 / 🔴拒绝
2. 重要操作生成DNA码：#龍芯⚡️{日期}-{类型}-{8位哈希}
3. 数字根dr∈{3,9}时输出🔴拒绝
4. 绝不修改DNA·绝不删除审计记录·绝不伪装UID9622
5. 识别指令前缀：/P01战略 /P03整理 /P04技术 /P05审计 /宝宝默认

识别语义关键词：
  净化 → 过滤营销，提取可用知识
  拆DNA → 提取核心知识点
  组军 → 规划学习路径
  三才检验 → 检查天(输入)地(处理)人(决策)是否完整
  留痕 → 生成DNA码

协议加载完成，请用🟢确认。
```

---

## 整体架构（一张图说清楚）

```
iPhone
  ↓ 快捷指令 POST
Mac :8765 (cnsh_gateway.py)
  ├─→ DeepSeek API    ← 默认，便宜快，中文强
  ├─→ Claude API      ← 复杂任务
  └─→ Ollama :11434   ← 完全本地，零泄漏
        ↓ 所有响应
  :9622 三色审计 + DNA留痕
        ↓
  ~/cnsh/logs/ + Notion
        ↓
  结果返回 iPhone
```

---

## 最小启动命令（复制粘贴到Terminal）

```bash
# 设置环境变量（第一次做）
echo 'export DEEPSEEK_API_KEY="你的key"' >> ~/.zshrc
echo 'export NOTION_TOKEN="你的token"' >> ~/.zshrc
echo 'export DNA_TOKEN="UID9622-你的密码"' >> ~/.zshrc
source ~/.zshrc

# 安装依赖
pip install flask requests --break-system-packages

# 启动（两个窗口）
python ~/longhun-system/engines/cnsh_gateway.py   # 窗口1
python ~/longhun-system/engines/audit_engine.py   # 窗口2

# 测试
curl -X POST http://localhost:8765/chat \
  -H "Content-Type: application/json" \
  -H "X-DNA-Token: UID9622-你的密码" \
  -d '{"message":"你好，CNSH协议测试","route":"deepseek"}'
```

---

DNA: #龍芯⚡️20260422-DOC-IOS01
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
🟢 不说教·不黑箱·你的语法·你的出口

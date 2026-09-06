---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂本地服务器 · 设备接入手册 v1.0

> **Mac IP**: `192.168.1.34`（路由器DHCP分配，变IP就更新此文件）
> **前提**: 设备和Mac连**同一个WiFi/局域网**
> **DNA**: `#龍芯⚡️丙午·丙申·乙卯·辰时·䷄需-DEVICE-SETUP-v1.0`

---

## 🗺️ 集群端口速查

| 端口 | 服务 | 设备用途 |
|:---:|------|------|
| **8443** | API网关（主入口） | PWA/Web/快捷指令 · 代理一切API |
| **8777** | 通心译翻译引擎 | 鸿蒙手机翻译、剪贴板翻译 |
| **8788** | 本地AI中继 | AI对话（MLX→Ollama大→Ollama小三级降级） |

> 💡 **手机只要记住 `http://192.168.1.34:8443` 一个地址就够了**，网关会自动路由。

---

## 📱 设备接入指南

### 1. 鸿蒙手机（通心译App）

**已配置，无需手动操作：**
- `ServerConfig.ets` 默认已指向 `http://192.168.1.34:8777`
- 编译安装后自动连接
- 若Mac IP变了，在App设置页改地址即可

**测试连接：** 手机浏览器打开 `http://192.168.1.34:8777/health` → 看到 JSON 即通

---

### 2. iPhone（快捷指令）

创建快捷指令：

```
1. 新建快捷指令 → 添加"获取URL内容"
2. URL: http://192.168.1.34:8443/api/cnsh/clipboard-translate
3. 方法: POST
4. 请求体: JSON → {"text":"{{剪贴板}}"}
5. 添加"显示结果"
```

**触发方式：** 共享表单 / 双击背面 / Siri语音

---

### 3. 任何手机/平板（PWA网页版）

1. 手机浏览器打开：`http://192.168.1.34:8443/ecosystem-dashboard`
2. 添加到主屏幕 → 即用即走

---

### 4. Mac本机命令行

```bash
# 健康检查
curl http://127.0.0.1:8443/health

# AI对话（直接走本地AI中继）
curl -X POST http://127.0.0.1:8788/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5:14b","messages":[{"role":"user","content":"你好"}]}'

# 通心译翻译
curl -X POST http://127.0.0.1:8777/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text":"帮我分析这段话的意思"}'
```

---

### 5. 其他电脑（同局域网）

直接浏览器访问：
- 操作台：`http://192.168.1.34:8443/`
- 通心译：`http://192.168.1.34:8777/health`
- AI中继：`http://192.168.1.34:8788/health`

---

## 🔧 IP变动怎么办？

路由器的 DHCP 可能分配不同 IP，变IP时：

1. **查Mac新IP：**
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```

2. **修改本文件** → 全局替换 `192.168.1.34` 为新IP

3. **更新鸿蒙配置文件：**
   `integrations/harmonyos/tongxinyi/entry/src/main/ets/utils/ServerConfig.ets`
   修改 `DEFAULT_SERVER` 为新IP

4. **重启服务（可选）：**
   ```bash
   # 一般不需要，直接能用
   ```

> 💡 建议：在路由器设置里把Mac的MAC地址绑定固定IP（DHCP保留），一劳永逸。

---

## 🔒 安全说明

- 所有服务仅局域网可访问（`192.168.x.x`），**不暴露到公网**
- 没有公网端口映射，外面打不进来
- 数据全程本地：你手机 → Mac → 本地AI → 结果回手机
- 外部AI（Claude/DeepSeek）仅在本地AI不可用时兜底
- 每条请求绑定DNA追溯码，日志append-only

---

## 📊 当前运行状态

```
🟢 8081 MLX 龍魂自训练模型
🟢 8443 API 统一网关 (CORS全开·设备入口)
🟢 8777 通心译翻译引擎 (鸿蒙直连)
🟢 8788 本地AI中继 (MLX→Ollama大→Ollama小)
🟢 9001 人格路由API
🟢 9622 主控操作台
🟢 11434 Ollama (22个模型)
🟢 19862 浏览器守护进程
```

---

*手册版本: v1.0 · 2026-07-11 · 自动生成*
*下次更新: Mac IP 变动时*

```json
{
  "dna": "#龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622",
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

# 🐱 宝宝·Siri接入说明 v1.0
DNA: #龍芯⚡️2026-04-07-SIRI-BAOBAO-SETUP-v1.0
作者: 诸葛鑫（UID9622）

---

## 现在就能用（不需要编译App）

### 第一步：开启宝宝补丁服务

终端跑这个：
```bash
python3 ~/longhun-system/app_patch.py
```

开了之后访问：http://localhost:8001  就是总控台

---

### 第二步：Mac Siri 快捷指令接入宝宝

1. 打开 **快捷指令** app（Shortcuts，Mac自带）
2. 点左上角 **＋** 新建
3. 搜索 **"获取URL内容"**（Get Contents of URL）
4. 填写：
   - URL: `http://localhost:8001/chat`
   - 方法: POST
   - 请求正文: JSON
   - 添加字段: `message` = **快捷指令输入**（拖"快捷指令输入"变量进去）
   - 添加字段: `persona` = `宝宝`
5. 搜索添加 **"从JSON中获取值"**
   - 获取 `reply` 字段
6. 搜索添加 **"朗读文本"**（Speak Text）
   - 文本 = 上一步结果
7. 快捷指令名字改成 **"宝宝"**
8. 右上角添加 Siri 短语：说 **"宝宝"** 触发

完成后说「嘿 Siri，宝宝」就接上了。

---

### 第三步（可选）：iPhone也能用

同样的快捷指令在 iPhone 上设置，要求：
- iPhone 和 Mac 在同一 WiFi
- Mac 上的 app_patch.py 要跑着
- iPhone 快捷指令里 URL 改成 Mac 的局域网 IP：
  `http://192.168.x.x:8001/chat`（在 Mac 系统偏好→网络里看IP）

---

## App版（需要Xcode编译）

Swift文件已加入第10个意图：`宝宝对话Intent`

触发词：
- "宝宝"
- "宝宝在吗"
- "宝宝帮我"
- "叫宝宝"

文件位置：`~/longhun-system/LongHunWidget/LongHunIntent.swift`

---

## 宝宝的工作逻辑

```
你说"宝宝"
→ Siri调用 localhost:8001/chat
→ 8001转发给 localhost:8000/chat（主引擎）
→ 8000返回回复
→ 8001加上🐱前缀
→ Siri朗读给你听
→ 8000离线时：本地兜底回复，提示你开引擎
```

---

## 测试命令（终端验证）

```bash
# 健康检查
curl http://localhost:8001/health

# 叫宝宝
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -H "X-UID: 9622" \
  -d '{"message": "宝宝在吗", "persona": "宝宝"}'

# 看系统状态
curl http://localhost:8001/status

# 看最近记忆
curl http://localhost:8001/memory | python3 -m json.tool | head -30
```

---

DNA: #龍芯⚡️2026-04-07-SIRI-BAOBAO-SETUP-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
乔前辈肯定没想到，有人把Siri按倒了重新站起来 🐱

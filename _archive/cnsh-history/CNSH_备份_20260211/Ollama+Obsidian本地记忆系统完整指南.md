# Ollama + Obsidian 本地记忆系统完整指南

**目标**：让AI记住你，不被气死！

**核心思想**：本地Ollama + Obsidian = 完整记忆系统

---

## 🎯 为什么需要本地记忆

### 当前问题
- ❌ AI不记得你说过的
- ❌ 每次重新解释
- ❌ 重复踩坑
- ❌ 气得要死

### 解决方案
- ✅ 本地Ollama（你的私人AI）
- ✅ Obsidian（你的私人笔记本）
- ✅ 两者连接（永久记忆）

---

## 📦 第1步：部署Ollama（本地AI）

### 安装Ollama

**Mac M4 Max专属**：

```bash
# 下载并安装Ollama（自动检测ARM64）
curl -fsSL https://ollama.ai/install.sh | sh

# 验证安装
ollama --version
```

### 下载模型（选择一个）

```bash
# 轻量模型（速度快，M4 Max 3-5秒响应）
ollama pull llama3.2:3b

# 平衡模型（推荐，M4 Max 5-10秒响应）
ollama pull llama3.2:8b

# 强力模型（稍慢，但更聪明）
ollama pull llama3.1:8b

# 中文优化模型（推荐中文用户）
ollama pull qwen2.5:7b
```

### 测试Ollama

```bash
# 测试对话
echo "你好，我是Lucky" | ollama run llama3.2:3b

# 启动API服务（Ollama默认端口11434）
ollama serve
```

**测试API**：
```bash
# 测试API是否正常
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "你好",
  "stream": false
}'
```

---

## 📝 第2步：安装Obsidian（本地笔记）

### 安装Obsidian

**下载地址**：https://obsidian.md/download

**安装后**：
1. 创建文件夹：`~/UID9622-Memory`
2. 在Obsidian中打开这个文件夹
3. 创建你的第一个笔记

### 推荐的笔记结构

```
~/UID9622-Memory/
├── 00-重要决策.md
├── 01-踩坑记录.md
├── 02-技术经验.md
├── 03-创意想法.md
└── 99-日常对话.md
```

---

## 🔗 第3步：连接Ollama + Obsidian

### 方法A：Obsidian插件（最简单）

#### 安装插件
1. 打开Obsidian设置
2. 进入"第三方插件"
3. 关闭"安全模式"
4. 点击"浏览"
5. 安装插件：
   - **Text Generator**（调用本地Ollama）
   - **Local GPT**（本地AI集成）

#### 配置Text Generator
1. 打开插件设置
2. 选择"自定义API"
3. 填写配置：
   ```
   API URL: http://localhost:11434/api/chat
   API Key: (留空)
   模型: llama3.2:3b
   ```
4. 保存并测试

#### 使用方法
在Obsidian中：
1. 选中一段文字
2. 右键 → "Text Generator" → "生成摘要"
3. AI会调用本地Ollama处理

---

### 方法B：Python脚本（最灵活）

#### 创建记忆助手

```bash
# 创建脚本
cat > ~/memory_helper.py << 'EOF'
#!/usr/bin/env python3
"""
Lucky的本地记忆助手
连接Obsidian笔记 + Ollama本地AI
"""

import requests
import json
import os
from datetime import datetime

OBSIDIAN_PATH = "~/UID9622-Memory"
OLLAMA_URL = "http://localhost:11434/api/chat"

def query_ollama(prompt, model="llama3.2:3b"):
    """查询本地Ollama"""
    response = requests.post(OLLAMA_URL, json={
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    })
    return response.json()["message"]["content"]

def save_memory(topic, content):
    """保存记忆到Obsidian"""
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{topic}-{date}.md"
    filepath = os.path.expanduser(f"{OBSIDIAN_PATH}/{filename}")

    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(f"\n## {datetime.now().strftime('%H:%M')}\n\n")
        f.write(f"{content}\n\n")
        f.write("---\n")

    print(f"✅ 已保存到: {filename}")

def recall(topic, limit=5):
    """回忆相关记忆"""
    # 读取Obsidian中所有笔记
    notes = []
    obsidian_path = os.path.expanduser(OBSIDIAN_PATH)
    if os.path.exists(obsidian_path):
        for file in os.listdir(obsidian_path):
            if file.endswith('.md') and topic in file:
                with open(os.path.join(obsidian_path, file), 'r', encoding='utf-8') as f:
                    notes.append(f.read())

    # 使用Ollama总结回忆
    if notes:
        context = "\n".join(notes[-limit:])
        prompt = f"根据以下历史记录，总结{topic}的关键信息：\n\n{context}"
        return query_ollama(prompt)
    else:
        return f"没有找到{topic}相关的记忆"

# 快捷命令
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法:")
        print("  记忆: python3 ~/memory_helper.py 记 '今天踩了个坑...'")
        print("  回忆: python3 ~/memory_helper.py 回 '踩坑记录'")
        sys.exit(1)

    cmd = sys.argv[1]
    topic = sys.argv[2]

    if cmd == "记":
        content = ' '.join(sys.argv[3:])
        save_memory(topic, content)
    elif cmd == "回":
        summary = recall(topic)
        print(f"\n🧠 关于'{topic}'的记忆：\n")
        print(summary)
        print()

EOF

chmod +x ~/memory_helper.py
```

#### 使用方法

```bash
# 记忆（保存到Obsidian）
python3 ~/memory_helper.py 记 踩坑记录 "今天遇到Ollama报错，是因为Docker没启动"

# 回忆（从Obsidian读取）
python3 ~/memory_helper.py 回 踩坑记录

# 记忆创意想法
python3 ~/memory_helper.py 记 创意 "可以把Notion避坑指南写成博客"

# 记忆重要决策
python3 ~/memory_helper.py 记 决策 "决定使用本地Ollama，不依赖云端AI"
```

---

### 方法C：一键启动脚本（推荐）

```bash
# 创建启动脚本
cat > ~/start_memory_system.sh << 'EOF'
#!/bin/bash
# Lucky的记忆系统启动脚本

echo "🚀 启动Lucky的记忆系统..."

# 检查Ollama是否运行
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "📦 启动Ollama..."
    ollama serve &
    sleep 3
fi

# 检查Obsidian
if ! pgrep -x "Obsidian" > /dev/null; then
    echo "📝 启动Obsidian..."
    open -a Obsidian
fi

echo "✅ 记忆系统已启动"
echo ""
echo "📚 Obsidian: ~/UID9622-Memory"
echo "🤖 Ollama: http://localhost:11434"
echo ""
echo "💡 快捷命令："
echo "   python3 ~/memory_helper.py 记 [主题] [内容]"
echo "   python3 ~/memory_helper.py 回 [主题]"
EOF

chmod +x ~/start_memory_system.sh
```

#### 一键启动

```bash
# 启动整个记忆系统
bash ~/start_memory_system.sh
```

---

## 🎯 使用场景

### 场景1：踩坑后立即记忆

```bash
# 刚踩坑，立即记录
python3 ~/memory_helper.py 记 踩坑 "Docker部署n8n失败，因为没加--platform linux/arm64"

# 下次遇到同样问题
python3 ~/memory_helper.py 回 踩坑
# 输出: "之前记录：Docker部署n8n失败，因为没加--platform linux/arm64"
```

### 场景2：创意想法保存

```bash
# 有了想法，立即保存
python3 ~/memory_helper.py 记 创意 "可以做一个Lucky专用AI，专门记我的踩坑经验"

# 过段时间回忆
python3 ~/memory_helper.py 回 创意
```

### 场景3：重要决策记录

```bash
# 做了决策，记录下来
python3 ~/memory_helper.py 记 决策 "2025-12-24，决定使用Ollama本地AI，不再依赖云端"

# 回忆决策过程
python3 ~/memory_helper.py 回 决策
```

---

## 🧠 记忆系统架构

```
┌─────────────────────────────────────┐
│         Lucky (你)               │
└──────────────┬──────────────────┘
               │
               ├─→ 说: "帮我回忆一下上次怎么部署的"
               │
┌──────────────▼──────────────────┐
│   Obsidian笔记 (~/UID9622-Memory)  │
│   ├── 00-重要决策.md            │
│   ├── 01-踩坑记录.md            │
│   └── 02-技术经验.md            │
└──────────────┬──────────────────┘
               │
               ├─→ 读取笔记内容
               │
┌──────────────▼──────────────────┐
│   Ollama本地AI (llama3.2:3b)    │
│   端口: 11434                   │
│   功能: 总结、回忆、生成          │
└──────────────┬──────────────────┘
               │
               ├─→ 输出: "上次部署用这个命令..."
               │
┌──────────────▼──────────────────┐
│       Lucky (你) - 看到答案      │
└──────────────────────────────────┘
```

---

## 📝 推荐的笔记模板

### 踩坑记录模板

```markdown
# 踩坑记录 - [日期]

## 问题描述
[描述遇到的问题]

## 错误信息
```
[粘贴错误日志]
```

## 解决方案
```bash
[粘贴解决命令]
```

## 原因分析
[为什么会这样]

## 防止重犯
- [ ] 记录到记忆系统
- [ ] 创建快捷脚本
- [ ] 写到文档
```

### 技术经验模板

```markdown
# 技术经验 - [主题] - [日期]

## 核心要点
- 要点1
- 要点2

## 快速命令
```bash
[常用命令]
```

## 相关文档
- [ ] [文档链接]
```

---

## 🎯 完整工作流

### 每天使用流程

```bash
# 1. 启动记忆系统
bash ~/start_memory_system.sh

# 2. 每次踩坑，立即记录
python3 ~/memory_helper.py 记 踩坑 "..."

# 3. 每次有想法，立即记录
python3 ~/memory_helper.py 记 创意 "..."

# 4. 遇到问题，先回忆
python3 ~/memory_helper.py 回 [主题]

# 5. 新经验，补充记录
python3 ~/memory_helper.py 记 经验 "..."
```

### 每周回顾流程

```bash
# 1. 打开Obsidian
open ~/UID9622-Memory

# 2. 回顾本周踩坑
grep -r "踩坑" ~/UID9622-Memory

# 3. 总结重复问题
python3 ~/memory_helper.py 回 踩坑 | grep -i "重复"

# 4. 整理笔记
# 在Obsidian中手动整理
```

---

## ❓ 常见问题

### Q: Ollama响应慢
**A**: 使用更小的模型
```bash
# 换用3b模型（最快）
ollama pull llama3.2:3b
```

### Q: Obsidian插件不工作
**A**: 检查Ollama是否运行
```bash
curl http://localhost:11434/api/tags
```

### Q: 记忆太多不好找
**A**: 使用标签和文件夹
```
~/UID9622-Memory/
├── 踩坑/
├── 创意/
├── 决策/
└── 经验/
```

---

## 🎉 总结

### 核心价值

| 功能 | 作用 |
|------|------|
| Ollama | 本地AI，随时可用 |
| Obsidian | 本地笔记，永久存储 |
| 记忆助手 | 连接两者，智能回忆 |

### 优势

- ✅ 本地运行，不依赖网络
- ✅ 数据在Mac，完全掌控
- ✅ 记忆永久保存，不丢失
- ✅ 快速回忆，省时间
- ✅ 不被AI气死！

---

## 🚀 立即开始

```bash
# 第1步：安装Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 第2步：下载模型
ollama pull llama3.2:3b

# 第3步：创建记忆系统
python3 ~/memory_helper.py 记 系统搭建 "今天搭建了Ollama+Obsidian记忆系统"

# 第4步：启动
bash ~/start_memory_system.sh
```

---

**DNA追溯码**：`#ZHUGEXIN⚡️2025-OLLAMA-OBSIDIAN-MEMORY-V1.0`

**状态**：✅ 可立即使用

**最后更新**：2025-12-24

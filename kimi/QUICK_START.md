# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🚀 Kimi 集成快速开始

## 1️⃣ 设置环境变量 (30 秒)

```bash
# 写入 ~/.longhun/secrets.env（不上传 Git）
export KIMI_API_KEY="<YOUR_KIMI_API_KEY>"
```

## 2️⃣ 验证连接 (1 分钟)

```bash
cd ~/longhun-system/kimi
python3 -c "from kimi_client import KimiClient; c = KimiClient(); print('✅ OK' if c.health_check() else '❌ FAIL')"
```

## 3️⃣ 运行测试 (5 分钟)

```bash
python3 test_kimi_integration.py
```

## 4️⃣ 四种使用方式

### 方式 1: 备用推理模型 (故障转移)
```python
from kimi import KimiIntegration
kimi = KimiIntegration()
result = kimi.infer_with_fallback("你的问题")
print(result)
```

### 方式 2: 多模态处理 (图像/文档)
```python
# 分析图像
result = kimi.process_image(
    "https://example.com/image.jpg",
    "描述这个图像"
)

# 分析文档
result = kimi.process_document(
    "/path/to/file.pdf",
    "总结这个文档"
)
```

### 方式 3: 实时聊天
```python
session = kimi.start_realtime_chat("user_001")
result = kimi.send_message(session["session_id"], "你好")
print(result["kimi_response"])
```

### 方式 4: Skill 引擎
```python
result = kimi.use_kimi_for_skill(
    "skill-3-canvas-design",
    {"description": "设计一个仪表板"}
)
print(result["kimi_output"])
```

## 📚 更多信息

- 完整指南: `KIMI_INTEGRATION_GUIDE.md`
- 完成报告: `KIMI_INTEGRATION_COMPLETION_REPORT.md`
- 部署步骤: `../DEPLOYMENT_RUNBOOK_FOR_TEAM.md` (第 11 部分)

---

**DNA**:#龍芯⚡️丙午·甲午·癸丑·戊午·䷨损-KIMI-QUICK-START-v1.0

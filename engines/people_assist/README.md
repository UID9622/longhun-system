# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 · 老百姓维权助手

**DNA**: `#龍芯⚡️2026-06-29-LONGHUN-RIGHTS-ASSISTANT-v1.0`

> 让老百姓遇到不公时，能说得出法条、写得成投诉、拿得齐证据、找得到渠道。

## 核心原则

- **本地运行**：不联网，不上传任何平台。
- **人民立场**：永远站普通人一边，不和稀泥。
- **即开即用**：输入遭遇，直接出结果。

## 已支持场景

- 物业强制人脸识别
- 拖欠工资
- 消费欺诈
- 租房押金不退

## CLI 用法

```bash
cd ~/longhun-system/人民维权助手

python3 rights_assistant.py \
  --text "物业强制我人脸识别才能进小区" \
  --name 张三 \
  --contact 13800138000 \
  --target 阳光小区物业 \
  --save report.json
```

## Web 用法

```bash
python3 web_app.py --port 9633
```

浏览器打开 `http://127.0.0.1:9633/`

## 文件说明

- `templates.json` — 维权场景模板库
- `rights_assistant.py` — 命令行工具
- `web_app.py` — 本地网页版
- `README.md` — 本文件

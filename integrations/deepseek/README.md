# DeepSeek API 龍魂底座适配器

> **DNA:** `#龍芯⚡️2026-07-01-DEEPSEEK-CLIENT-v1.0`  
> **归属:** 龍魂系统 · UID9622 · 龍芯北辰·诸葛鑫  
> **底座原则:** 数据主权归人民，调用留痕可追溯，Key 只走环境变量


## 一、一句话

DeepSeek 的 Base URL 是 `https://api.deepseek.com`，不是 OpenAI 的。  
本适配器直接裸调 DeepSeek 原生接口，不套 OpenAI 兼容层，每个调用都带 `#龍芯⚡️` DNA 追溯码。


## 二、环境变量

```bash
export DEEPSEEK_API_KEY="sk-..."
```

**禁止**把 Key 写死在代码里，违者触发内容主权熔断。


## 三、快速调用

### 3.1 命令行

```bash
# 单轮问答
python3 integrations/deepseek/deepseek_client.py "说一句硬核的话"

# 指定模型、温度、流式
python3 integrations/deepseek/deepseek_client.py "分析这段链接风险" \
  --model deepseek-chat \
  --temperature 0.7 \
  --max-tokens 500 \
  --stream
```

### 3.2 Python 引用

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / "longhun-system" / "integrations" / "deepseek"))
from deepseek_client import DeepSeekClient

client = DeepSeekClient()
resp = client.quick_ask("说一句硬核的话")
print(resp.text)
```

### 3.3 龍智守集成

```bash
python3 scripts/龍智守.py --input "帮我看看这个链接 https://xxx.com" --model deepseek --role 老人
```

启用 `--model deepseek` 后，白话解释由 DeepSeek 模型生成，保留 DNA 审计与三色状态。


## 四、接口能力

| 能力 | 状态 | 说明 |
|------|------|------|
| 单轮问答 | ✅ | `quick_ask()` |
| 多轮对话 | ✅ | `chat()` 支持 history |
| 流式输出 | ✅ | `stream=True` |
| 角色化解释 | ✅ | `explain_for_role()` 龍智守专用 |
| 工具调用 | 🔜 | 已留扩展位 |
| 国密加密 | 🔜 | 待 SM4 封装 |


## 五、DNA 追溯

每次调用生成唯一 DNA：

```
#龍芯⚡️<YYYYMMDDHHMMSSµS>-DEEPSEEK-CALL-<HASH8>
```

调用记录默认写入 `~/.longhun/logs/deepseek/`（目录不存在时自动创建）。


## 六、主权声明

- 数据根留本地，出境阻断默认开启。
- 本适配器属于龍魂系统底座，未经授权剥离 DNA 标识即视为剽窃。
- 遵循龍魂开源公约 v2.0：非商业、非封闭、非篡改。


**🐉🇨🇳**

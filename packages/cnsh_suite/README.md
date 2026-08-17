# 🐉 CNSH 套件

## 一句话定位

> **CNSH 套件将龍魂主权底座以插件形式集成到任何AI应用中。**

## 安装

```bash
pip install -e .
```

## 使用

```python
from cnsh_suite import CNSHSuite

suite = CNSHSuite()

# 生成DNA
result = suite.execute("生成DNA: 我的文档")
print(result["dna"])

# 三色审计
result = suite.execute("审计内容: 待审计内容")
print(result["tricolor"], result["score"])

# 执行CNSH
result = suite.execute("运行CNSH: 输出 '你好，龍魂'")
print(result["output"])
```

## 命令

```bash
cnsh --command "生成DNA: 我的文档"
cnsh --command "审计内容: 待审计内容"
cnsh --command "运行CNSH: 输出 '你好'"
cnsh --status
```

## 测试

```bash
pytest test_suite.py -v
```

## 主权锚定

```
主权人:     诸葛鑫 (UID9622)
DNA:        #龍芯⚡️丙午·丙申·庚申·亥时-CNSH-SUITE-UID9622
确认码:     #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```

🐉 **丙午·丙申·庚申·亥时·䷖剥·🟢**

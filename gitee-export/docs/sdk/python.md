# Python SDK

> **v2.1.0** — 内联引擎已对接。PersonaRouter / CNSHParser / Auditor 零外部依赖即可运行。
> 语音/视觉模块需对接本地模型引擎后可用。
> 详见 [CHANGELOG](../../CHANGELOG.md)。

---

## 安装

```bash
pip install longhun
```

要求：Python 3.10+

## 核心类

### PersonaRouter

人格路由器，核心入口。**v2.1 内联路由表可用。**

```python
from longhun import PersonaRouter, RouteResult, RouteInfo

router = PersonaRouter()

# 自动路由（内联路由表·30+意图域）
result: RouteResult = router.route("检查系统安全")
print(result)
# → 🟢 P05 上帝之眼 · audit
#    confidence: 0.80
#    DNA: #龍芯⚡️丙午·丙申·丙辰·戊子·坎-ROUTE-AUDIT-XXXXXXXX

# 指定人格（跳过自动匹配）
result = router.route("任意内容", persona="P00")
# → P00 文心 · dispatch

# 获取路由详情
info: RouteInfo = router.info("检查系统安全")
print(info.persona, info.keywords)
```

### CNSHParser

语义解析器。**v2.1 内联语义域可用。**

```python
from longhun import CNSHParser, Intent

parser = CNSHParser()

intent: Intent = parser.parse("帮我看下还有多少token")
print(intent.domain)    # → "system"
print(intent.action)    # → "token_check"
print(intent.keywords)  # → ["token", "Token"]
print(intent.confidence) # → 0.7
```

### DNA

追溯码生成与验证（v2.0 起可用）。

```python
from longhun import DNA

dna = DNA.generate(module="API", action="route")
# → #龍芯⚡️丙午·丙申·丙辰·戊子·坎-API-ROUTE-A1B2C3D4

# 验证（含六十四卦卦名合法性校验）
DNA.verify("#龍芯⚡️丙午·丙申·丙辰·戊子·坎-API-ROUTE-A1B2C3D4")
# → True
```

### Auditor

三色安全审计。**v2.1 内联引擎可用。**

```python
from longhun import Auditor, AuditReport

auditor = Auditor()

# 外部内容（全量扫描）
report: AuditReport = auditor.scan("外部输入的内容", source="external")
print(report.level)    # → "green" | "yellow" | "red"
print(report.score)    # → 0.0 ~ 1.0
print(report.red_count, report.yellow_count)

# 自研内容（黄警豁免）
report = auditor.scan("优化一下这段代码", source="self")
# → 🟢 通过（黄色警报仅记录不判定）

# 对接原生引擎（当在龍魂系统内运行时）
auditor_native = Auditor(engine="native")
report = auditor_native.scan("外部内容")
# → 自动探测 bin/lh_anti_tamper.py，降级到内联引擎
```

---

## 完整示例

```python
from longhun import PersonaRouter, CNSHParser, DNA, Auditor

# 1. 解析意图
parser = CNSHParser()
intent = parser.parse("检查服务状态")
print(f"意图: {intent.domain} → {intent.action}")

# 2. 路由分发
router = PersonaRouter()
result = router.route("检查服务状态")
print(f"人格: {result.persona} {result.persona_name}")

# 3. DNA 追溯
dna = DNA.generate(module="HEALTH", action="CHECK")
print(f"DNA: {dna} (验证: {DNA.verify(dna)})")

# 4. 安全审计
auditor = Auditor()
report = auditor.scan("这是一段需要审计的内容")
print(f"审计: {report.level} (红色:{report.red_count} 黄色:{report.yellow_count})")
```

---

## 配置

```json
// ~/.longhun/config.json
{
  "locale": "zh-CN",
  "local_model": "http://127.0.0.1:8081",    // ← 本地模型端口，按实际修改
  "fallback_model": "http://127.0.0.1:11434",  // ← 回退模型端口
  "log_level": "info"
}
```
> 生产环境请使用 HTTPS 并确保端口安全。

---

## API 参考

| 类 | 方法 | 说明 | 状态 |
|:---|:---|:---|:---:|
| `PersonaRouter` | `route(text, persona?)` | 路由分发 → `RouteResult` | ✅ v2.1 |
| `PersonaRouter` | `info(text)` | 路由元信息 → `RouteInfo` | ✅ v2.1 |
| `CNSHParser` | `parse(text)` | 意图解析 → `Intent` | ✅ v2.1 |
| `DNA` | `generate(module, action)` | 生成追溯码 | ✅ |
| `DNA` | `verify(dna)` | 验证追溯码+卦名 | ✅ |
| `Auditor` | `scan(content, source)` | 安全审计 → `AuditReport` | ✅ v2.1 |
| `Auditor` | `scan(content)` engine=native | 对接 lh_anti_tamper.py | ✅ v2.1 |
| `VoiceSynthesizer` | `speak(text, speed)` | 文字→语音 | 🟡 Preview |
| `PersonaVoice` | `set_persona(p)` / `speak(text)` | 人格音色 | 🟡 Preview |
| `VoiceDNA` | `register()` / `verify()` / `export()` | 声纹DNA | ✅ 模拟 |
| `VisionAnalyzer` | `analyze()` / `recognize_symbol()` | 图像分析 | 🟡 Preview |
| `VisionBridge` | `describe(path, prompt)` | 本地视觉桥 | 🟡 Preview |

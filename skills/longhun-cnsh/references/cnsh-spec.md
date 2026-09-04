# CNSH · 中文原生脚本与字元编辑器规范

## 目录
1. [概述](#概述)
2. [命名规范](#命名规范)
3. [字元创作规范](#字元创作)
4. [15层渲染系统](#15层渲染)
5. [DNA追溯格式](#dna追溯)

---

## 概述

CNSH（Chinese Native Scripting & Glyph Editor）是龍魂体系的中文数字生态核心组件：

> **中国人自己的数字生态，不求人，不联网，持续进化。**

- **字元创作**：鼠标绘制汉字字元
- **AI画匠**：AI辅助字元设计
- **中文编程**：用中文写代码
- **文化主权**：繁体龍字永存，甲骨文编码

---

## 命名规范

### 变量命名

```python
# ✅ 正确 - 中文变量
姓名 = "张三"
年龄 = 25
龍魂ID = "LONGHUN-CN-001"

# ✅ 正确 - 中英混合（技术术语用英文）
HTTP请求 = requests.get(网址)
JSON数据 = response.json()
SHA256哈希 = hashlib.sha256(数据).hexdigest()

# ❌ 错误 - 纯英文
name = "张三"
age = 25
dragon_id = "LONGHUN-CN-001"
```

### 函数命名

```python
# ✅ 正确
def 提取生物特征(self, 指纹图像路径: str) -> dict:
def 生成卦象ID(self, 身份哈希: str) -> list:
def 验证龍魂ID(self, 龍魂ID: str) -> bool:

# ❌ 错误
def extract_biometrics(self, fingerprint_path: str) -> dict:
def generate_hexagram_id(self, identity_hash: str) -> list:
def verify_dragon_id(self, dragon_id: str) -> bool:
```

### 类命名

```python
# ✅ 正确
class 龍魂永世唯一ID生成器:
class 生物特征提取器:
class 易经64卦映射器:
class 甲骨文编码器:

# ❌ 错误
class DragonIDGenerator:
class BiometricExtractor:
class IChingHexagramMapper:
```

### 文件命名

```python
# ✅ 正确
龍魂ID生成器.py
生物特征提取器.py
易经卦象映射表.py

# ❌ 错误
dragon_id_generator.py
biometric_extractor.py
iching_hexagram_mapper.py
```

---

## 字元创作

### 创作流程

1. 在画布上用鼠标绘制笔画
2. 应用15层渲染特性
3. 导出 SVG 矢量图
4. 保存 .cnsh 格式（可重新编辑）
5. 生成 DNA 追溯标识

### 文件格式

```yaml
.cnsh 文件结构:
  版本: "v0.1.0"
  DNA: "#龍芯⚡️{日期}-CNSH-EDITOR-v{版本}"
  作者: "UID9622"
  字元:
    - 编码: "Unicode码点"
    - 笔画序列: [...]
    - 渲染参数:
        力度: 0-100
        侵蚀: 0-100
        纹理: "类型"
        墨色: "浓度"
    - SVG数据: "..."
```

---

## 15层渲染

| 层级 | 名称 | 功能 | 参数范围 |
|---|---|---|---|
| v0001 | 基础笔画 | 原始笔画路径 | - |
| v0002 | 力度 | 笔触压力模拟 | 0-100 |
| v0003 | 侵蚀 | 边缘磨损效果 | 0-100 |
| v0004 | 纹理 | 纸张/材质纹理 | 类型选择 |
| v0005 | 墨色 | 墨水浓度 | 淡/中/浓 |
| v0006 | 飞白 | 干枯笔触效果 | 0-100 |
| v0007 | 晕染 | 水墨扩散效果 | 0-100 |
| v0008 | 阴影 | 立体阴影 | 角度+强度 |
| v0009 | 光泽 | 高光效果 | 0-100 |
| v0010 | 底色 | 背景底色 | 颜色选择 |
| v0011 | 边框 | 装饰边框 | 样式选择 |

---

## DNA追溯

每个字元必须有以下DNA追溯：

```
DNA: #龍芯⚡️{YYYY-MM-DD}-CNSH-EDITOR-v{版本}
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬{CODE} ✅
IP编号: IP-{编号}
所属母表: IP-ASSET-LEDGER
创始人: Lucky·UID9622（诸葛鑫·龙芯北辰）
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```

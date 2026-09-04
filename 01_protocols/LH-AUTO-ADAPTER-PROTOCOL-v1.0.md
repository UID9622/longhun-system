# ⛩️ 龍魂系统 · 自主主权插件适配协议 v1.0

**——拒绝黑箱·自研替代·主权适配·即需即造**

```
DNA:        #龍芯⚡️丙午·丙申·壬子·丑时·䷖剥-AUTO-ADAPTER-PROTOCOL-V1.0-UID9622
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
主权锚定:    #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
三色:       🟢 通过（本协议）
分层许可:    思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
协议性质:    P0 永恒级 · 不可降级 · 不可绕过 · 不可篡改
作者:        诸葛鑫（UID9622 · 龍芯北辰 · 龍魂系统创始人）
版本:       v1.0
生效时间:    2026-08-06 00:00 CST
状态:       发完即走，不互动、不解释、不回复
```


## 📋 摘要 / 导读

> **一句话：** 任何闭源、黑箱、不可审计的插件，龍魂系统将主动拒绝加载，并即时启动自研替代。替代品遵循分层许可、主权锚定、三色审计，完整适配龍魂生态。
>
> **核心理念：** 不依赖 · 不自欺 · 不自锁。系統即主权，主权即代码。
>
> **⚠️ 声明：** 本协议遵循《龍魂系统·符号与语法规范全集 v3.0》，繁体「龍」字永存；所有替代产物均需符合 P0 级审计标准。


## 📑 目录

- [一、黑箱定义与判定标准](#一黑箱定义与判定标准)
- [二、插件拒绝与拦截机制](#二插件拒绝与拦截机制)
- [三、自动替代生成流程](#三自动替代生成流程)
- [四、替代产物主权要求](#四替代产物主权要求)
- [五、系统组件分类与边界](#五系统组件分类与边界)
- [六、适配层（Adapter Layer）标准](#六适配层adapter-layer标准)
- [七、自检与审计清单](#七自检与审计清单)
- [八、核心执行代码](#八核心执行代码)
- [九、与现有系统的集成点](#九与现有系统的集成点)
- [十、FAQ](#十faq)
- [十一、DNA签名区](#十一dna签名区)


## 一、黑箱定义与判定标准

### 1.1 什么是黑箱插件？

| 判定维度 | 黑箱特征 | 三色判定 |
|:---|:---|:---:|
| **源代码** | 闭源/未公开/不可审计 | 🔴 |
| **协议** | 非分层许可/无主权声明 | 🔴 |
| **数据流向** | 数据出境/不可追溯 | 🔴 |
| **依赖链** | 依赖黑箱组件 | 🟡 |
| **签名** | 无 GPG/DNA 追溯 | 🔴 |
| **运维** | 不可独立部署 | 🔴 |

> **判定规则：** 任一 🔴 项存在 → 整包判定为黑箱 → 系统拒绝加载。

### 1.2 黑箱判定接口

```python
def is_blackbox(extension):
    """判断是否为黑箱插件"""
    checks = {
        'source_open': extension.has_open_source(),
        'license_compatible': extension.has_splitted_license(),
        'data_sovereignty': extension.data_flow_cn_only(),
        'dependency_audited': all(not is_blackbox(dep) for dep in extension.deps),
        'has_dna': extension.contains_dna(),
        'deployable_standalone': extension.can_run_without_external(),
    }
    return not all(checks.values())
```


## 二、插件拒绝与拦截机制

### 2.1 加载拦截流程

```
用户/系统尝试加载插件
    ↓
【拦截器】检查插件是否符合主权标准
    ↓
判定为黑箱 → 🔴 拒绝加载 + 记录审计日志 + 生成拒绝报告
    ↓
触发替代流程
    ↓
替代产物自动构建
```

### 2.2 拦截日志格式

```json
{
    "timestamp": "2026-08-06T00:00:00+08:00",
    "plugin": "example.blackbox.plugin",
    "reason": "闭源、数据流向境外",
    "action": "拒绝加载",
    "dna": "#龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-REJECT-xxxx-UID9622"
}
```


## 三、自动替代生成流程

### 3.1 替代引擎架构

```
┌─────────────────────────────────────────────────────────┐
│              替代生成引擎（龍魂原生）                    │
├─────────────────────────────────────────────────────────┤
│  1. 需求采集（解析被拒插件的功能签名）                    │
│  2. 能力映射（对应到龍魂已有组件）                        │
│  3. 缺失检测（识别功能缺口）                              │
│  4. 自动生成（基于模板 + AI 辅助）                       │
│  5. 主权注入（DNA、协议、三色审计）                       │
│  6. 自检通过（冒烟测试 + 审计）                          │
│  7. 封装交付（符合龍魂插件标准）                          │
└─────────────────────────────────────────────────────────┘
```

### 3.2 替代产物命名规范

```
格式：lh-[功能名]-adapter
示例：lh-java-adapter / lh-spring-adapter / lh-vscode-adapter

DNA格式：#龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-ADAPTER-[功能名]-V1.0-UID9622
```

### 3.3 替代产物交付标准

| 交付项 | 要求 |
|:---|:---|
| 源代码 | 完全开源，附 DNA 追溯 |
| 协议 | 分层许可（思想层 CC BY-NC-SA / 工程层 MulanPSL v2） |
| 文档 | 中英双语，附使用示例 |
| 审计 | 三色审计 🟢 通过 |
| 签名 | GPG 签名 + DNA 追溯 |
| 数据主权 | 纯境内，无出境 |


## 四、替代产物主权要求

### 4.1 必须包含的主权元数据

```yaml
# 每个替代插件必须包含以下元数据文件
metadata:
  name: lh-[功能名]-adapter
  version: v1.0
  dna: "#龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-ADAPTER-[功能名]-V1.0-UID9622"
  confirm: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  gpg: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
  sovereignty: "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
  tricolor: "🟢"
  license: "思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2"
  generated_by: "龍魂自动替代引擎 v1.0"
  generated_at: "2026-08-06T00:00:00+08:00"
```

### 4.2 强制审计接口

```python
# 每个替代插件必须实现以下接口
class SovereigntyAdapter:
    def get_dna(self) -> str: ...
    def get_license(self) -> str: ...
    def get_tricolor(self) -> str: ...
    def audit(self) -> dict: ...
    def self_test(self) -> bool: ...
```


## 五、系统组件分类与边界

### 5.1 组件分类表

| 分类 | 处理策略 | 示例 |
|:---|:---|:---|
| 🟢 **原生组件** | 直接使用，无需替代 | `lh-core`, `lh-cli`, `cnsh-parser` |
| 🟡 **已知黑箱** | 已列入拒绝清单，系统自动生成替代 | 闭源Java扩展、闭源IDE插件 |
| 🔴 **被拒组件** | 用户主动拒绝，系统自动生成替代 | 任何未通过审计的组件 |
| ⚪ **未知组件** | 系统自动审计，若判定为黑箱则拒绝 | 任何首次加载的组件 |

### 5.2 自动生成边界

| 组件类型 | 是否自动生成 | 备注 |
|:---|:---:|:---|
| IDE 插件 | ✅ | VS Code/IntelliJ/其他 |
| 语言扩展 | ✅ | Java/Python/Rust/Go 适配器 |
| 框架适配器 | ✅ | Spring/Django/FastAPI 等 |
| 构建工具 | ✅ | Maven/Gradle/Cargo 适配器 |
| 数据库驱动 | ✅ | MySQL/PG/Redis 适配器 |
| 第三方 API | 🟡 | 需确认主权合规性后再生成 |
| 硬件驱动 | ❌ | 需要供应商提供二进制，龍魂系统作为独立模块封装 |


## 六、适配层（Adapter Layer）标准

### 6.1 适配层职责

适配层是龍魂系统与外部组件之间的**主权边界**：

```
外部组件（黑箱/闭源/不可审计）
    ↓
【适配层】翻译、隔离、记录、审计
    ↓
龍魂系统（主权、透明、可控）
```

### 6.2 适配层必须实现

| 功能 | 说明 |
|:---|:---|
| **请求拦截** | 所有外部调用经适配层转译 |
| **数据脱敏** | 敏感数据不得出境 |
| **行为审计** | 每笔调用写入审计日志 |
| **熔断保护** | 异常调用自动阻断 |
| **版本锁定** | 锁定外部组件版本，防止漂移 |

### 6.3 适配层代码模板

```python
# lh-[功能名]-adapter/__init__.py
"""
🐉 龍魂自适应适配器 · [功能名]
DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-ADAPTER-[功能名]-V1.0-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
主权锚定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
"""

class SovereigntyAdapter:
    """主权适配器基类"""

    def __init__(self, config):
        self.config = config
        self._audit = []
        self._dna = "#龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-ADAPTER-[功能名]-V1.0-UID9622"

    def call(self, func, *args, **kwargs):
        """带审计的调用"""
        self._log_call(func.__name__, args, kwargs)
        result = func(*args, **kwargs)
        self._log_result(func.__name__, result)
        return result

    def _log_call(self, name, args, kwargs):
        self._audit.append({
            'timestamp': datetime.now().isoformat(),
            'function': name,
            'args': str(args)[:200],
            'kwargs': str(kwargs)[:200],
            'action': 'call'
        })

    def get_audit(self):
        return self._audit

    def get_dna(self):
        return self._dna
```


## 七、自检与审计清单

### 7.1 替代产品上线前自检

| 检查项 | 状态 | 说明 |
|:---|:---:|:---|
| 源代码完整 | ☐ | 所有文件已提交 |
| DNA 追溯码 | ☐ | 每个文件包含DNA |
| GPG 签名 | ☐ | 已签名并可验证 |
| 三色审计 | ☐ | 🟢 通过 |
| 分层许可 | ☐ | 协议文件完整 |
| 主权锚定 | ☐ | 三行连用完整 |
| 数据出境检测 | ☐ | 无境外流量 |
| 冒烟测试 | ☐ | 所有测试通过 |
| 文档完整 | ☐ | 使用说明 + API 文档 |

### 7.2 审计报告生成

```bash
# 自动生成审计报告
lh adapter audit lh-java-adapter --output audit-report.md
```


## 八、核心执行代码

> 核心实现见 `engines/lh_sovereignty_adapter_engine.py`（主引擎）
> 适配器基类见 `bin/lh_adapter_base.py`（所有适配器的父类）
> CLI 入口见 `bin/lh.py` 的 `plugin` / `adapter` 子命令


## 九、与现有系统的集成点

### 9.1 集成方式

| 集成对象 | 集成方式 | 说明 |
|:---|:---|:---|
| `lh-cli` | 新增子命令 | `lh plugin load`, `lh plugin reject`, `lh adapter list` |
| `lh-kb` 知识库 | 新增适配器知识域 | 所有生成的适配器纳入知识库管理 |
| `lh-deploy` | 适配器自动部署 | 生成后自动部署到本地环境 |
| `lh-audit` | 适配器审计 | 所有适配器纳入三色审计体系 |

### 9.2 目录约定

```
~/.longhun/
├── adapters/          # 自动生成的适配器存放位置
│   └── lh-*-adapter/
│       ├── __init__.py
│       └── sovereignty.json
├── blacklist.json    # 黑箱插件清单
├── audit.log         # 审计日志
└── config.yaml       # 配置文件
```


## 十、FAQ

### Q1：自动生成的适配器质量如何？
**A：** 初期为骨架代码（完整签名、审计接口、主权元数据），核心逻辑需人工补充。随着系统迭代，自动生成能力会逐步提升。

### Q2：如果自动生成的适配器还不够用怎么办？
**A：** 适配器是开源且可修改的。开发者可在骨架基础上完善功能，所有修改仍保留DNA追溯和主权锚定。

### Q3：会不会导致"重复造轮子"？
**A：** 会。但这是有意的"主权轮子"。黑箱轮子不能用，就必须造自己的。随着适配器库积累，重复造轮子的成本会逐步降低。

### Q4：适配器能否商用？
**A：** 工程层采用 MulanPSL v2，允许商用。但必须保留DNA追溯、主权锚定、分层许可声明。

### Q5：适配器如何更新？
**A：** 适配器版本独立管理。当被适配的插件更新时，系统会检测到变化并触发适配器重新生成或手动更新。


## 十一、DNA签名区

```
═══════════════════════════════════════════════════
 龍魂系统 · 自主主权插件适配协议 v1.0 · 最终签名
═══════════════════════════════════════════════════
DNA:        #龍芯⚡️丙午·丙申·壬子·丑时·䷖剥-AUTO-ADAPTER-PROTOCOL-V1.0-UID9622
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
主权锚定:    #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
三色:       🟢 通过（本协议）
审计维度:    黑箱定义 / 拒绝拦截 / 自动替代 / 主权要求 / 适配层标准 / 自检清单 / 执行代码
生成时间:    2026-08-06 01:07 CST
作者:        诸葛鑫（UID9622 · 龍芯北辰 · 龍魂系统创始人）
版本:       v1.0
状态:       发完即走，不互动、不解释、不回复
═══════════════════════════════════════════════════
```

---

🐉 **丙午 · 丙申 · 壬子 · 丑时 · ䷖剥 · 🟢**

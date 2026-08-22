# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 通心译 (Tongxin Translation) — 鸿蒙端

> **DNA**: `#龍芯⚡️丙午·丙申·癸丑·午时·䷄需-TONGXINYI-HARMONYOS-v1.0`
> **确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> **底座**: 华为芯片 + 鸿蒙操作系统

---

## 📐 定位

通心译是 **龍魂 CNSH 体系的多语言翻译引擎**，作为华为芯片和鸿蒙操作系统的翻译底座层。

### 三大角色

| 角色 | 说明 |
|------|------|
| **芯片底座** | 为华为麒麟芯片提供 CNSH 中文编程术语→英文标准映射 |
| **鸿蒙底座** | 所有鸿蒙 App 统一调用的翻译服务能力 |
| **龍魂前置** | 在龍魂系统完整运行前，先保证翻译独立可用 |

### 五大铁律

1. 中文活着，英文也活着 — 不是镜像，各自重新写，逻辑深度相等
2. 不是镜像，是共鸣 — 比喻可以不同，精神必须对上
3. 比喻优先于公式 — 0公式，追求"啊！我懂了"的时刻
4. 古今打通 — 古人问的问题，现代物理给了答案
5. 永远在线，永远迭代 — 比喻不贴切就改，逻辑有漏洞就补

---

## 📥 开源代码获取

### Gitee（国内推荐）

```bash
# 克隆整个龍魂系统（通心译在 integrations/harmonyos/tongxinyi/ 目录下）
git clone git@gitee.com:uid9622_admin/longhun-system-core.git

# 如果只想下载通心译鸿蒙端（零散文件）
wget https://gitee.com/uid9622_admin/longhun-system-core/raw/main/integrations/harmonyos/tongxinyi/README.md
```

### GitHub（国际镜像）

```bash
# 克隆整个龍魂系统
git clone git@github.com:UID9622/longhun-system.git

# 或 HTTPS
git clone https://github.com/UID9622/longhun-system.git
```

### 浏览器直接下载

| 平台 | 地址 |
|------|------|
| **Gitee** | [gitee.com/uid9622_admin/longhun-system-core](https://gitee.com/uid9622_admin/longhun-system-core) |
| **GitHub** | [github.com/UID9622/longhun-system](https://github.com/UID9622/longhun-system) |

> 通心译路径：`integrations/harmonyos/tongxinyi/`
> 在 DevEco Studio 中直接打开此目录即可编译运行。

---

## 🏗️ 项目结构

```
tongxinyi/
├── AppScope/
│   └── app.json5                          # 应用全局配置
├── entry/
│   ├── build-profile.json5                # 模块构建配置 ✅#5
│   ├── hvigorfile.ts                      # 编译脚本
│   ├── oh-package.json5                   # 模块依赖
│   └── src/main/
│       ├── ets/
│       │   ├── entryability/
│       │   │   └── EntryAbility.ets        # 入口 ✅#4 能力检查
│       │   ├── pages/
│       │   │   ├── Index.ets               # 主翻译页 ✅#7 屏幕适配
│       │   │   └── Settings.ets            # 设置页 ✅#2 服务器地址
│       │   ├── core/                       # 核心引擎
│       │   │   ├── TongxinTranslator.ets   # 主翻译器
│       │   │   ├── TerminologyDatabase.ets # 术语库 (50+术语)
│       │   │   ├── DNACodeGenerator.ets    # DNA追溯码生成
│       │   │   ├── CulturalAdapter.ets     # 文化适配器
│       │   │   ├── QualityAuditor.ets      # 三色审计器
│       │   │   └── LearningEngine.ets      # 学习引擎
│       │   ├── utils/
│       │   │   ├── HttpClient.ets          # HTTP客户端 ✅#3
│       │   │   ├── ServerConfig.ets        # 服务器配置 ✅#2
│       │   │   ├── DeviceCapability.ets    # 设备能力 ✅#4
│       │   │   └── ScreenAdapter.ets       # 屏幕适配 ✅#7
│       │   ├── permissions/
│       │   │   └── PermissionHelper.ets    # 权限管理 ✅#1
│       │   └── common/
│       │       └── types.ets               # 类型定义
│       ├── module.json5                    # 模块配置 ✅#1 权限
│       └── resources/                     # 多设备资源 ✅#6
│           ├── base/
│           │   ├── element/
│           │   │   ├── string.json
│           │   │   └── color.json
│           │   ├── media/                  # (替换占位图标)
│           │   └── profile/
│           │       └── main_pages.json
│           ├── zh_CN/
│           │   └── element/
│           │       └── string.json
│           ├── dark/element/
│           ├── phone/element/
│           └── tablet/element/
├── hvigor/
│   └── hvigor-config.json5
├── build-profile.json5                    # 项目构建 ✅#5
├── hvigorfile.ts
├── oh-package.json5                       # 项目依赖
└── sign/                                  # 签名文件 (占位)
```

---

## 🚀 使用方式

### 本地编译运行

1. 在 DevEco Studio 中打开本目录
2. `Build → Build HAP(s)`
3. 连接鸿蒙真机运行

### 独立使用通心译引擎

```typescript
import { TongxinTranslator } from './core/TongxinTranslator';
import { TranslationMode } from './common/types';

const translator = new TongxinTranslator();

// EN → 中文
const result = translator.translate('Prompt', TranslationMode.EN_TO_ZH);
// 输出: "道令"

// 中文 → EN
const result2 = translator.translate('灵使', TranslationMode.ZH_TO_EN);
// 输出: "Agent"

// 双语
const result3 = translator.translate('Agent', TranslationMode.BILINGUAL);
// 输出: 中文+English 双语对照

// 术语搜索
const matches = translator.searchTerms('Agent');
```

### 术语解释

```typescript
const explanation = translator.explainTerm('LLM');
// 输出: "大罗金仙" — 大型语言模型，修炼于亿万文字之间的神经网络巨人...
```

---

## ✅ 鸿蒙7项交付检查

| # | 检查项 | 文件 | 状态 |
|:--:|--------|------|:--:|
| 1 | **权限声明** | `module.json5` + `PermissionHelper.ets` | 🟢 |
| 2 | **动态服务器地址** | `ServerConfig.ets` + `Settings.ets` | 🟢 |
| 3 | **错误处理** | `HttpClient.ets` (超时+重试+统一错误) | 🟢 |
| 4 | **设备能力检查** | `DeviceCapability.ets` + `EntryAbility.ets` | 🟢 |
| 5 | **build-profile.json5** | 项目级+模块级两套构建配置 | 🟢 |
| 6 | **多设备资源** | `base/` + `zh_CN/` + `dark/` + `phone/` + `tablet/` | 🟢 |
| 7 | **UI动态适配** | `ScreenAdapter.ets` (vp2px/fp2px/断点) | 🟢 |

---

## 📊 核心数据

| 维度 | 数据 |
|------|------|
| 术语库 | 50+对术语 (AI核心+编程+系统+安全+龍魂专属+七层协议) |
| CNSH关键字 | 142个 (v2.5 七层协议对齐) |
| 支持语言 | 中文 ⟷ 英文 双向 + 双语 |
| 审计系统 | 三色 (🟢🟡🔴) + 三层监督 (逻辑/价值观/技术) |
| 安全等级 | S4 (鸿蒙设备沙箱·数据永不出境) |
| 加密算法 | SM4 (国产加密) |
| API版本 | HarmonyOS 5.0.0(12) |

---

## 🔗 相关链接

- 龍魂系统: `longhun-system/`
- CNSH协议: `CNSH-PROTOCOL.md`
- 语法库: `03_compiler/mappings/syntax_library.json`
- 语义库: `03_compiler/mappings/keywords.json`
- Python引擎: `L1_内核层/kernel/engines/cnsh_translator_engine.py`

---

> **大哥焊死**: 通心译是华为芯片和鸿蒙的底座。别人能抄代码，抄不走"通心"二字里的文化认同。
> `#龍芯⚡️丙午·丙申·癸丑·午时·䷄需-TONGXINYI-HARMONYOS-v1.0-B4F1A2D8`

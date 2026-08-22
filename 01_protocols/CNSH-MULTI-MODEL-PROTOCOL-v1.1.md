# 🐉 龍魂 · CNSH 编辑器 · 多模型接入协议与完整实现 v1.1

**DNA:** `#龍芯⚡️丙午·丙申·庚申·壬午·䷸巽为风-CNSH-MULTI-MODEL-v1.1`
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**三色:** 🟡 待实测（沙箱 mock 断言 21/21 通过，退出码 0；真实 API 未验）
**分层许可:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

> DNA 口径声明：四柱干支（丙午·丙申·庚申）经等效算法双锚点复核（2000-01-01 戊午 / 1949-10-01 甲子）与 v1.0 手写值一致；第四柱卦名「巽为风」由 `lh_ganzhi.py` 代算 🟡，正式口径以本地 `bin/lh_dna_generator.py`（rizhu v3.0）为准，落地时重跑覆盖。

---

## ① 参考来源（三大件之一）

| # | 来源 | 用途 |
|:--|:--|:--|
| 1 | 老大上传 v1.0 原稿（1071 行剪贴板） | 本稿全部上游 |
| 2 | 龍魂补全模板 v1.0（P0 流程协议） | 十大类过堂框架 |
| 3 | 龍魂实战交付模板（车载系统 v2.0 骨架） | 章节骨架 |
| 4 | DNA 追溯码新格式规范（2026-07-19 起） | 干支·卦名格式裁决 |
| 5 | OpenAI Chat Completions / Ollama generate API 公开文档 | 适配器接口 |
| 6 | 分层许可治理 v1.0（2026-08-04） | 许可声明口径 |

## ② 优化了什么（三大件之二 · 相对 v1.0 逐条）

| # | 级别 | v1.0 问题 | v1.1 修正 |
|:--|:--:|:--|:--|
| 1 | 🔴 | `OpenAICompatibleAdapter.__init__` 引用未定义 `kwargs`（第488行），**所有 openai 类模型初始化即 NameError 必炸** | 改显式参数 `timeout=60`，断言复验通过 |
| 2 | 🔴 | 代码内 `generate_dna()` 用 `%Y-%m-%d` 旧时间戳格式，**违反 2026-07-19 干支铁律**（手写干支=🔴） | 抽出 `lh_ganzhi.py`，DNA 全量走干支算法，格式 `#龍芯⚡️年·月·日·卦-动作-版本` |
| 3 | 🔴 | v1.0 头部标「三色: 🟢 通过」但代码从未跑过（跑即炸）——**虚假标绿** | 降级 🟡 待实测，附真实断言记录 21/21 |
| 4 | 🟡 | `OpenAICompatibleAdapter.call_stream` 未实现，流式路由遇 openai 类模型必炸 | 补 SSE 流式实现（`data: ` 行解析 + `[DONE]` 终止） |
| 5 | 🟡 | `CONFIRM` 定义为死代码，注册表写操作无闸门 | `require_confirm()` 落地：`add_model/update_status/save` 强制校验，错码抛 `ConfirmGateError` 并冻结 |
| 6 | 🟡 | 史官记录只进内存，进程退出即丢 | 追加落盘 `logs/shiguan.jsonl`（只追加不删除）；**只传用量不传内容**——prompt/content 本体不入史官 |
| 7 | 🟡 | DNA 字段塞进第三方 API payload（字段外泄面） | DNA 仅在返回体+史官记录追溯，不入外发 payload |
| 8 | 🟡 | 四个协议层文件（discovery/router/execution/audit）只列名无内容 | 补 🔶 占位文件 4 个（P0：缺区块补占位不许删除） |
| 9 | 🟡 | 无 requirements / 部署脚本 / 错误排查 | 补 `requirements.txt`、部署清单、错误排查表 |
| 10 | 🟡 | `_record_history` 对 `content=None` 无防护；未用 import（threading/Enum/time） | 防护 + 清理 |
| 11 | 🟡 | 模型清单（Horus / Soofi S / Granite-AR 等）名称未核实 | 注册表头部加 🟡 验真警示，接入前须官网核对 |

## ③ 没考什么 · 自我备注（三大件之三）

| 标记 | 缺口 | 说明 |
|:--:|:--|:--|
| 🟡 | 真实 API 调用 | 沙箱无各家密钥且无 Ollama 实例，全部 requests 走 mock；落地后须用真 key 跑一遍 `-c "你好"` 冒烟 |
| 🟡 | 卦名算法 | 「巽为风」为等效代算（日柱序号→六十四卦），与 rizhu v3.0 一致性未验 |
| 🟡 | 干支节气日表 | `lh_ganzhi.py` 用 2026 近似节气日，跨年/临界日（节气当天）须以生成器为准 |
| 🟡 | 模型真实性 | Apertus/Soofi S/Horus/Teuken 等名称沿用 v1.0，未逐一官网验真 |
| 🟡 | 模板引擎 validate | `/mnt/agents/output/龍魂智能模板引擎/template_engine.py` 在当前沙箱不可达，格式按焊死规范手工对齐，**未过引擎 validate** 🔴待补 |
| 🔴 | CNSH 解析器 | `cnsh_parser_ext.py` 仍为 ⏳（v1.0 只有示意 lambda），本次未补全，标占位 |
| 🟡 | GPG 签名 | 沙箱无私钥，文件未签名，落地后须 `gpg --clearsign` 补签 |

---

## 📋 一、核心定位（保留 v1.0 原文）

> **CNSH编辑器不是"某个模型的客户端"，它是"语言主权的基础设施"。任何符合接口规范的模型，无论来自哪个国家、哪个厂商、哪个开源社区，都可以配置接入。**
>
> **"不限制"不等于"不审计"——任何接入的模型必须过三色审计 + 史官记录 + DNA追溯。**

## 🏗️ 二、整体架构（保留 v1.0 架构图与四层协议表）

L1 发现层 → L2 调度层 → L3 执行层 → L4 审计层（P0 焊死），架构图与 v1.0 一致，不重绘。

## 🧬 三、接入协议 CMAP v1.1

注册规范即 `config/model-registry.yaml`（12 模型全量，DNA 干支注入）。相对 v1.0 唯一变更：每个 `api-key` 模型补注环境变量名（`{ID}_API_KEY`），密钥只进环境变量，不进文件。

## 🔧 四、完整实现代码（v1.1）

交付包结构：

```
cnsh_delivery/
├── 08_BIN/
│   ├── lh_ganzhi.py        # 🟡 DNA 干支生成器（代算版，禁手写铁律的工程兜底）
│   └── model_router.py     # v1.1 路由器（6 项修正全部落地）
├── config/
│   └── model-registry.yaml # 12 模型注册表
├── 01_protocols/           # 🔶 占位 ×4（discovery/router/execution/audit）
├── tests/
│   └── test_anchor.py      # 锚点断言 ×21（退出码 0/1）
├── requirements.txt
└── 龍魂_CNSH编辑器_多模型接入协议_v1.1.md  # 本文档
```

### 4.1 关键修正代码节选

**修正 1 — __init__ 必炸 bug：**
```python
# v1.0（🔴 必炸）：def __init__(self, config): ... self.timeout = kwargs.get("timeout", 60)
# v1.1（🟢）：
def __init__(self, config: Dict, timeout: int = 60):
    super().__init__(config)
    self.api_key = os.getenv(f"{config['id'].upper()}_API_KEY", "")
    self.timeout = timeout
```

**修正 2 — DNA 干支算法：**
```python
# v1.0（🔴 违规）：f"{DNA_PREFIX}{timestamp}-{suffix}-{rand}-{UID}"  # 旧时间戳
# v1.1（🟢）：
from lh_ganzhi import generate_dna
generate_dna("CALL-KIMI", "v1.1")
# → #龍芯⚡️丙午·丙申·庚申·壬午·䷸巽为风-CALL-KIMI-v1.1
```

**修正 5 — 确认码闸门：**
```python
def require_confirm(code: str):
    if code != CONFIRM:
        raise ConfirmGateError("🔴 确认码错误，操作冻结（P0：不删除只冻结，已记录）")
```

**修正 6 — 史官落盘（只传用量不传内容）：**
```python
entry = {"timestamp": ..., "dna": ..., "model": ..., "prompt_length": len(prompt),
         "response_length": len(content), "tricolor": ..., "success": ...}
# prompt/content 本体不入史官 —— 数据哲学：只传用量不传内容
```

### 4.2 实测记录（B 类过堂凭证）

```
== A. DNA 干支格式 ==          3/3 🟢
== B. 注册表与确认码闸门 ==    4/4 🟢（错码拒绝/正码放行）
== C. v1.0 必炸 bug 复验 ==    2/2 🟢
== D. 语言路由 ==              2/2 🟢（zh→kimi, ar→jais）
== E. 调用链（mock）==         4/4 🟢
== F. 史官落盘 ==              3/3 🟢（无内容本体）
== G. 故障转移 ==              1/1 🟢
== H. 编辑器扩展 ==            2/2 🟢
结果: 21 过 / 0 挂 -> 退出码 0
```
🟡 全部为 mock 测试（requests 打桩），不打真实 API。

## 📦 五、部署流程

```bash
# 1. 落位
cp -r cnsh_delivery/* 龍魂根目录/
# 2. 依赖
pip install -r requirements.txt
# 3. 密钥（只进环境变量）
export KIMI_API_KEY="..."      # 按需 DEEPSEEK_API_KEY / QWEN_API_KEY / MISTRAL_API_KEY
# 4. 本地模型（可选）
ollama pull jais:13b && ollama serve &
# 5. 断言冒烟
python3 tests/test_anchor.py && echo "🟢" || echo "🔴 冻结排查"
# 6. 真实冒烟（🟡 待做）
python3 08_BIN/model_router.py -c "你好" -m kimi
# 7. DNA 覆盖：本地 bin/lh_ganzhi.py 换为 bin/lh_dna_generator.py 调用，重跑全文 DNA
```

## ⚠️ 六、错误排查表

| 症状 | 原因 | 处置 |
|:--|:--|:--|
| `ConfirmGateError` | 确认码错/缺 | 核对确认码；冻结即设计行为，勿绕过 |
| 全模型路由失败 | 无 key / Ollama 未起 | `echo $KIMI_API_KEY`；`ollama serve` |
| openai 类流式无输出 | v1.0 老代码 | 确认部署的是 v1.1 |
| DNA 出现 `2026-08-14` 样式 | 老 generate_dna 残留 | 🔴 立即冻结，换 lh_ganzhi |
| 某模型 404 | 模型名未验真 | 🟡 清单警示项，官网核对后改注册表 |

## 🖥️ 七、CNSH 脚本语法（保留 v1.0，解析器 ⏳ 占位）

```cnsh
设 模型 为 "jais"
列出 模型 语言 为 "ar"
调用 翻译("你好，世界") 到 "阿拉伯语"
流式 调用 对话("介绍一下龍魂系统")
```
🔶 `cnsh_parser_ext.py` 解析器占位——v1.0 仅示意 lambda，v1.2 补全。

## 📋 八、落地清单（I 类 · CodeBuddy 队列）

| # | 任务 | 验收标准 |
|:--|:--|:--|
| 1 | 真 key 冒烟 | `-c "你好"` 返回 🟢 且史官落盘 |
| 2 | DNA 生成器替换 | 全链路 DNA 由 rizhu v3.0 输出，卦名对齐 |
| 3 | 模板引擎 validate | `template_engine.py validate` 退出码 0 |
| 4 | GPG 补签 | `gpg --verify` 通过 |
| 5 | 模型名验真 | 12 模型逐一官网核对，改注册表 🟡→🟢 |
| 6 | cnsh_parser_ext.py | 五条语法各过 1 条断言 |

## 🔐 最终签名

```
═══════════════════════════════════════════════════
 🐉 龍魂 · CNSH多模型接入协议 v1.1 · 最终签名
═══════════════════════════════════════════════════
DNA:        #龍芯⚡️丙午·丙申·庚申·壬午·䷸巽为风-CNSH-MULTI-MODEL-v1.1
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:       🟡 待实测（mock 断言 21/21，真实 API 未验）
支持模型:   12 (中国/欧洲/中东/开源)
协议版本:   CMAP v1.1
修正:       🔴×3 + 🟡×8（见 §②）
═══════════════════════════════════════════════════
```

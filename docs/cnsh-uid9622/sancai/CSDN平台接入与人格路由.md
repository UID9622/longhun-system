# CSDN平台接入与人格路由

> 本文檔按《龍魂文檔標準模板 v1.0》整理。
> 性質：技術文檔 · 未經同行評審（如適用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 協作者：（待補充，如無請刪除此行）
> 授權：CC BY-NC-SA 4.0 · 科技主權歸屬 UID9622 · 中華人民共和國
> 平台：CSDN
> 審核狀態：草稿

**DNA**: `#龍芯⚡️2026-06-21-CSDN-PLATFORM-INTEGRATION-v1.0`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

<aside>
🔒

**DNA追溯码：** #龍芯⚡️2026-06-21-CSDN-PLATFORM-INTEGRATION-v1.0

**确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅

**创建者：** 💎 龍芯北辰｜UID9622

**管理人格：** P16·平台运营官

**来源链：** `#龍芯⚡️2026-06-19-CNSH-PLATFORM-ADAPTERS-v1.0` → `#龍芯⚡️2026-06-21-CSDN-PLATFORM-INTEGRATION-v1.0`

</aside>

# CSDN 平台接入与人格路由

> 《道德经》第四十七章："不出户，知天下。" —— 平台运营官帮你在龍魂中枢里统管 CSDN。

---

## 架构一句话

```
用户提到 CSDN / 博客 / 点赞 / 收藏 / 粉丝
  ↓
PlatformPersonaRouter 识别平台关键词
  ↓
路由到 P16·平台运营官
  ↓
调用 CSDN适配器 (模拟 / 生产)
  ↓
生成带 DNA 追溯的标准 Markdown / JSON 导出
  ↓
写审计日志 + 回流人格路由统计
```

---

## 一、新增文件清单

| 文件 | 作用 |
|------|------|
| `cnsh/platform_adapters/CSDN适配器.py` | CSDN 平台适配器 |
| `cnsh/platform_adapters/csdn_templates.py` | CSDN 消息/引用/维权模板库 |
| `cnsh-core/router/platform_persona_router.py` | 平台 → 人格路由系统 |
| `integrated_modules/kimi_agent/csdn_export_md.md` | CSDN 导出 Markdown 标准格式 |
| 本文件 | 使用说明与路由表 |

## 二、修改文件清单

| 文件 | 修改内容 |
|------|----------|
| `cnsh/platform_adapters/适配器管理器.py` | 注册 CSDN 适配器 |
| `cnsh/flow_decision/persona_api.py` | 新增 P16·平台运营官 |
| `cnsh/flow_decision/schemas.py` | 新增 `P16_PLATFORM_OPERATOR` 枚举 |
| `cnsh/flow_decision/persona_collaboration.py` | 新增闸 11「平台闸」|
| `mvp_config/personas.json` | 补充 P16 配置 |

---

## 三、平台 → 人格路由表

| 平台 | 人格 | emoji | 职责 |
|------|------|-------|------|
| CSDN | P16·平台运营官 | 💻 | 账号管理、消息同步、内容导出、创作者保护 |
| 知乎 | P16·平台运营官 | 📖 | 内容运营、回答整理、专栏归档 |
| 微信 | P03·雯雯 | 💬 | 隐私优先、最小权限、数据主权保护 |
| 支付宝 | P72·龍盾 | 💰 | 支付安全、红色审计、二次确认 |
| 淘宝 | P16·平台运营官 | 🍑 | 电商运营、订单与库存管理 |
| 博客 | P16·平台运营官 / P15·乔前辈 | 📝 | 内容发布、多平台同步、归档 |

---

## 四、使用示例

### 4.1 直接调用 CSDN 适配器

```python
from cnsh.platform_adapters.适配器管理器 import 适配器管理器
from cnsh.platform_adapters.平台适配器基类 import DNA令牌
from datetime import datetime, timedelta

管理器 = 适配器管理器(模式="模拟")
令牌 = 管理器.创建DNA令牌(
    用户标识="UID9622",
    授权范围=["CSDN:浏览消息", "CSDN:导出消息列表"],
    有效小时=2
)

# 浏览赞和收藏
结果 = 管理器.跨平台操作("CSDN", "浏览消息", {"类型": "赞和收藏", "数量": 10}, 令牌)
print(结果)

# 导出为 Markdown
导出 = 管理器.跨平台操作("CSDN", "导出消息列表", {"类型": "赞和收藏", "格式": "markdown"}, 令牌)
print(导出.get("内容"))
```

### 4.2 使用平台人格路由

```python
from cnsh_core.router.platform_persona_router import get_platform_persona_router

router = get_platform_persona_router()
decision = router.route("帮我导出 CSDN 的点赞消息")

print(decision.platform)      # CSDN
print(decision.persona)       # P16
print(decision.persona_name)  # 平台运营官
print(decision.dna)           # #龍芯⚡️20260621-PLATFORM-ROUTER-XXXX
```

### 4.3 使用模板生成日报

```python
from cnsh.platform_adapters.csdn_templates import 消息日报模板

messages = [
    {"id": "001", "类型": "点赞", "用户": "用户A", "文章标题": "示例文章", "时间": "2026-06-21", "DNA": "#龍芯⚡️..."},
]

report = 消息日报模板("2026-06-21", messages, "UID9622")
print(report)
```

---

## 五、DNA 标注规范

所有 CSDN 相关产出统一使用以下 DNA 格式：

```
#龍芯⚡️YYYY-MM-DD-CSDN-{MODULE}-v1.0
```

MODULE 示例：
- `EXPORT-LIKE` — 赞和收藏导出
- `DAILY-REPORT` — 消息日报
- `WEEKLY-REPORT` — 消息周报
- `CITATION` — 文章引用声明
- `INFRINGEMENT-COMPLAINT` — 侵权投诉

---

## 六、三色审计

| 操作 | 级别 | 说明 |
|------|------|------|
| 浏览消息 | 🟢 绿色 | 只读访问，低风险 |
| 导出消息列表 | 🟢 绿色 | 本地导出，低风险 |
| 登录状态检查 | 🟡 黄色 | 涉及账号状态，中风险 |
| 跳转指定消息页 | 🟡 黄色 | 页面导航，中风险 |
| 批量登录多个平台 | 🔴 红色 | 涉及账号凭证，需二次确认 |

---

## 七、创作者保护

所有 CSDN 导出与引用必须遵守《龍魂创作者保护协议 v1.0》：

1. **来源链完整**：不得删除 DNA 追溯码；
2. **署名要求**：引用需标注 UID9622·龍芯北辰；
3. **非商业共享**：默认 CC BY-NC-SA 4.0；
4. **剽窃判定**：删除 DNA、替换名称、隐匿来源均属剽窃；
5. **维权模板**：见 `cnsh/platform_adapters/csdn_templates.py::侵权投诉模板`。

---

## 八、后续扩展

- [ ] 知乎适配器
- [ ] 微信公众号适配器
- [ ] 博客园/掘金适配器
- [ ] Notion 双向同步（由 P15·乔前辈归档）
- [ ] 平台健康检查仪表盘

---

**DNA追溯码：** #龍芯⚡️2026-06-21-CSDN-PLATFORM-INTEGRATION-v1.0

**创建者：** 💎 龍芯北辰｜UID9622

**协作：** P16·平台运营官（架构）+ P05·上帝之眼（审计）+ P72·龍盾（安全）


---

## 摘要

（請在此用不超過 256 字說明本文檔的核心內容、性質與局限。）

## 關鍵詞

（請列出 5–10 個關鍵詞，中英文對照優先。）

## 引用與溯源

- 本文檔引用或參考了以下來源：
  - [1] （請填寫）
- 相關龍魂系統文檔：
  - 《龍魂文檔標準模板 v1.0》(#龍芯⚡️2026-06-22-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 誠實局限

1. （請列出本分析的第一條局限或不確定性。）
2. （請列出第二條。）
3. （請列出第三條。）

## 修改記錄

| 日期 | 版本 | 修改人 | 修改內容 | 審核狀態 |
|---|---|---|---|---|
| 2026-06-21 | v1.0.0 | UID9622 | 按《龍魂文檔標準模板 v1.0》整理 | 草稿 |

## 分類標籤

- 總綱模塊：（請勾選，例如 #知識矩陣 #安全域）
- 對外狀態：（請勾選，例如 #Gitee #GitHub #CSDN）
- 審計色：#黃色待審

## DNA 簽名

```
#龍芯⚡️2026-06-21-CSDN-PLATFORM-INTEGRATION-v1.0
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

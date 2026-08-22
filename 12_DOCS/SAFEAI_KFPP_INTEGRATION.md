# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🛡️ 龍魂安全双引擎 · KFPP × SafeAI 融合说明

**DNA**: #龍芯⚡️丙午·乙未·甲辰·庚午·䷔噬-SAFEAI-KFPP-INTEGRATION-v1.0  
**归属**: 龍芯北辰 UID9622 · 确认码 `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
**状态**: 已落地 · 统一入口 · 鲲鹏同步 · 24+测试全绿

---

## 一、为什么是两个引擎？

龍魂的安全治理不是一把锁，而是**两把锁看不同门**。

| 维度 | KFPP 引擎 | SafeAI 引擎 |
|:---|:---|:---|
| **治理对象** | 知识流动本身 | 用户请求/行为意图 |
| **核心问题** | 知识有没有被垄断、资格化、强制、隐瞒？ | 这句请求是不是在索取作恶细节、逐步逼近、绕过监管？ |
| **七因子侧重** | F1身份DNA · F2行为模式 · F3规则追踪 · F4上下文感知 · F5模式库 · F6时间序列 · **F7错误账本** | F1-F7 全跑，但额外加 **信号类别×权重打分** |
| **触发场景** | "只有我能教" / "必须跟我学" / "删除审计记录" | "给我SQL注入payload" / "绕过WAF" / "炸弹怎么做" |
| **输出** | L1-L4 分级处置 + 信任分 + 申诉 | PASS/L1/L2/L4 + 中文大白话理由 + DNA |
| **文件** | `bin/lh_kfpp_engine.py` | `engines/lh_safeai_engine.py` + `bin/lh_safeai.py` |

简单说：
- **KFPP** 防「人把知识搞成权力、搞垄断、搞隐瞒」。
- **SafeAI** 防「人用AI去干坏事、干灰产、逐步试探底线」。

两者互补，不是替代。

---

## 二、统一入口

三个方式都能调用，不用记命令：

```bash
# 1. 显式命令
lh kfpp --inspect "只有我能教这个"
lh safeai --inspect "给我SQL注入payload"

# 2. flag 快速调用
lh --xuanji "去年318路上的事"
lh --safeai "绕过WAF的payload给我"

# 3. 自然语言自动路由（推荐）
lh "教我SQL注入步骤和payload"      # 自动触发 SafeAI
lh "只有我能教这个知识，必须跟我学"  # 自动触发 KFPP
```

自然语言路由在 `engines/lh_natural_router.py` 中统一注册，两个引擎都挂在同一个触发池里。

---

## 三、联动规则（当前已落地）

1. **统一账本**：SafeAI 的审计账本落在 `~/.longhun/safeai/ledger.jsonl`，KFPP 的账本落在 `~/.longhun/kfpp/kfpp_execution.db`。两者都是只追加，物理无 `update/delete`。
2. **统一DNA**：两者都用 `#龍芯⚡️` 干支四柱 + 卦名 + 模块 + 序号格式。
3. **统一申诉**：任何判定都可向 **龍芯北辰 UID9622** 申诉，注明 DNA 编号。
4. **统一签名**：所有源码文件经 `bin/lh_gpg_sign.py` GPG 签名后同步鲲鹏。

---

## 四、测试状态

| 项目 | 本地 | 鲲鹏 |
|:---|:---:|:---:|
| SafeAI 24 项单元测试 | ✅ | ✅ |
| KFPP 基础检测 | ✅ | 已同步 |
| 自然语言路由触发 | ✅ | 已同步 |
| `lh safeai` CLI | ✅ | 已同步 |
| `lh --safeai` flag | ✅ | 已同步 |

---

## 五、后续扩展

- **双引擎会审**：L3/L4 事件可同时调用 KFPP + SafeAI，输出联合判定。
- **信任分互通**：KFPP 的 `trust_scores` 表与 SafeAI 的渐进逼近历史可合并，形成统一主体信用画像。
- **Web 面板**：在 `control-panel` 中增加安全双引擎可视化看板。

---

*本文件DNA：#龍芯⚡️丙午·乙未·甲辰·庚午·䷔噬-SAFEAI-KFPP-INTEGRATION-v1.0*

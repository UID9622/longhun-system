# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统·自然语言意图引擎 v1.0

> 作者：龍芯北辰·UID9622
> 发布时间：2026-08-15
> 来源：longhun-system/bin/lh_natural.py
> 入库DNA：#龍芯⚡️丙午·丁酉·辛卯·丙申-NATURAL-ENGINE-UID9622

---

> 你说人话，AI自动理解、自动执行、自动验证。
> 不需要记命令，不需要背端口号，不需要当实验室操作员。

---

## P0 核心原则

1. 自然语言即指令
2. 先通心译解析，再内置意图兜底
3. 自动识别任务、自动执行、自动审计
4. 所有操作入史官
5. 失败时给出人话可读的错误

---

## P1 支持的意图

| 人话示例 | 识别任务 |
|---|---|
| "帮我把网关和小艺链路搞通，史官记录我要看一眼" | deploy_gateway + check_gateway |
| "看看现在系统状态" | check_status |
| "清理端口，把占着的服务释放掉" | clean_ports |
| "打开浏览器 / 关闭浏览器" | browser_open / browser_close |
| "我的记忆呢" | memory_check |
| "看看剪贴板" | clipboard_status |

---

## P2 集成组件

```
人说人话
    │
    ▼
通心译 (longhun-tongxinyi)
    │
    ▼
内置意图解析器
    │
    ▼
任务执行器
    ├─ 主权网关 (lh_sovereign_gateway.py)
    ├─ 浏览器控制 (lh_browser_controller.py)
    ├─ 剪贴板中枢 (lh_clipboard_hub.py)
    ├─ 记忆文件 (~/.longhun/memory/latest_digest.json)
    └─ 系统状态 (ports / processes)
    │
    ▼
史官审计 (04_AUDIT/natural_engine.jsonl)
```

---

## P3 使用方式

```bash
# 直接调用
python3 ~/longhun-system/bin/lh_natural.py "看看系统状态"

# 通过 lh 入口
./bin/lh natural "帮我把网关和小艺链路搞通"
./bin/lh ask "我的记忆呢"
./bin/lh 问 "清理端口"
```

---

## P4 文件位置

- 引擎核心：`bin/lh_natural.py`
- `lh` 入口：`bin/lh`
- 史官记录：`04_AUDIT/natural_engine.jsonl`

---

## 签章

```
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#龍芯⚡️丙午·丁酉·辛卯·丙申-NATURAL-ENGINE-UID9622
```

---

> 不是命令行，是人话行。
> 不是工程师，是主人。
> 不是背指令，是表达意图。

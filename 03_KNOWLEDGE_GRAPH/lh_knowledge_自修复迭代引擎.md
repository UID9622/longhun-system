# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统·自修复/自迭代引擎 v1.0

> 作者：龍芯北辰·UID9622
> 发布时间：2026-08-15
> 来源：longhun-system/bin/lh_self_heal.py
> 入库DNA：#龍芯⚡️丙午·丁酉·辛卯·丙申-SELF-HEAL-UID9622

---

> 自动发现 → 自动修复 → 迭代验证。
> 系统自己体检，自己吃药，自己写病历。

---

## P0 核心原则

1. 定期自动巡检
2. 能修则修，不能修则报
3. 多轮迭代直到稳定
4. 所有修复动作入史官
5. 鲲鹏服务器可定时 cron 运行

---

## P1 检查项

| 类别 | 检查内容 | 修复动作 |
|---|---|---|
| 目录 | 08_STATE / 04_AUDIT / logs 是否存在 | 自动创建 |
| 依赖 | pytest / fastapi / uvicorn / httpx | 自动 pip install |
| shebang | bin/ 下 shell 脚本首行是否为 shebang | 自动置顶 |
| Python 语法 | 核心 .py 文件是否能编译 | 报告错误位置 |
| 端口 | 8766 / 9766 是否监听 | 提示人工确认 |
| pyright | pyrightconfig.json 是否存在 | 自动生成 |

---

## P2 使用方式

```bash
# 本地运行，默认 3 轮迭代
python3 ~/longhun-system/bin/lh_self_heal.py

# 只跑 1 轮
python3 ~/longhun-system/bin/lh_self_heal.py 1
```

---

## P3 鲲鹏自动部署

```bash
bash ~/longhun-system/deploy_self_heal_kunpeng.sh
```

部署后每 6 小时自动巡检一次：
- 同步脚本到 `/opt/longhun-system/bin/lh_self_heal.py`
- 写入 crontab
- 日志：`/opt/longhun-system/logs/self_heal.log`
- 审计：`/opt/longhun-system/04_AUDIT/self_heal.jsonl`

---

## P4 文件位置

- 引擎核心：`bin/lh_self_heal.py`
- 部署脚本：`deploy_self_heal_kunpeng.sh`
- 本地史官：`04_AUDIT/self_heal.jsonl`
- pyright 配置：`pyrightconfig.json`

---

## 签章

```
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#龍芯⚡️丙午·丁酉·辛卯·丙申-SELF-HEAL-UID9622
```

---

> 不是运维，是自医。
> 不是告警，是自愈。
> 不是人工巡检，是系统自省。

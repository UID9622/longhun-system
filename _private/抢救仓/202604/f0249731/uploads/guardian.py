#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════
# 龍魂系统·道德哨兵守护脚本 v1.0
# DNA: #龍芯⚡️2026-02-22-道德哨兵守护脚本-v1.0
# 创建者：龍芯北辰｜UID9622
# 运行：每天凌晨3点
# crontab: 0 3 * * * cd /root && python3 guardian.py >> 哨兵.log 2>&1
# ═══════════════════════════════════════════════════════════

import json
import datetime
import os

CONFIG = {
    "UID": "UID9622",
    "主控邮箱": "luckyoathnotlog@proton.me",
    "日志文件": "龍魂_webhook.log",
    "DNA根码": "#龍芯⚡️2026-02-22-道德哨兵守护脚本-v1.0",
}

def 生成DNA(类型):
    日期 = datetime.datetime.now().strftime("%Y-%m-%d")
    时间 = datetime.datetime.now().strftime("%H%M%S")
    return f"#龍芯⚡️{日期}-哨兵-{类型}-{时间}"

def 扫描今日日志():
    今日 = datetime.datetime.now().strftime("%Y-%m-%d")
    善小清单 = []
    恶小清单 = []
    总记录数 = 0

    try:
        with open(CONFIG["日志文件"], "r", encoding="utf-8") as f:
            for 行 in f:
                try:
                    记录 = json.loads(行.strip())
                    if 记录.get("时间", "").startswith(今日):
                        总记录数 += 1
                        三色 = 记录.get("三色", "🟢")
                        事件 = 记录.get("原始数据", {}).get("type", "unknown")
                        DNA = 记录.get("DNA", "")
                        时间 = 记录.get("时间", "")

                        if 三色 == "🔴":
                            恶小清单.append({"时间": 时间, "事件": 事件, "DNA": DNA, "等级": "严重恶"})
                        elif 三色 == "🟡":
                            恶小清单.append({"时间": 时间, "事件": 事件, "DNA": DNA, "等级": "微小恶"})
                        else:
                            善小清单.append({"时间": 时间, "事件": 事件, "DNA": DNA, "等级": "正常"})
                except:
                    continue
    except FileNotFoundError:
        pass

    return {
        "日期": 今日,
        "总记录数": 总记录数,
        "善小清单": 善小清单,
        "恶小清单": 恶小清单,
        "善恶比": f"{len(善小清单)}:{len(恶小清单)}",
        "系统健康度": "🟢" if len(恶小清单) == 0 else ("🟡" if len(恶小清单) < 3 else "🔴")
    }

def 生成报告(扫描结果):
    今日DNA = 生成DNA("日报")

    善小部分 = "\n".join([
        f"  ✅ {i['时间']} | {i['事件']}"
        for i in 扫描结果["善小清单"]
    ]) or "  （今日无记录）"

    恶小部分 = "\n".join([
        f"  ⚠️ {i['时间']} | {i['事件']} | {i['等级']} | {i['DNA']}"
        for i in 扫描结果["恶小清单"]
    ]) or "  （今日无记录）✨"

    if len(扫描结果["恶小清单"]) == 0:
        建议 = "今日系统运行良好，天网未见异常。继续保持！🌟"
    elif len(扫描结果["恶小清单"]) < 3:
        建议 = "检测到少量异常，请关注🟡黄灯条目，及时处理。"
    else:
        建议 = "⚠️ 今日异常较多，建议老大亲自审查🔴红灯条目！"

    报告 = f"""
🐉 龍魂系统·道德哨兵·每日报告
{'='*50}
日期：{扫描结果['日期']}（北京时间凌晨3点自动生成）
系统健康度：{扫描结果['系统健康度']}
总记录数：{扫描结果['总记录数']}
善恶比：{扫描结果['善恶比']}
DNA：{今日DNA}
{'='*50}

🌱 今日善小清单（{len(扫描结果['善小清单'])}条）：
{善小部分}

🕸️ 今日恶小清单（{len(扫描结果['恶小清单'])}条）：
{恶小部分}

{'='*50}
💡 哨兵建议：
  {建议}

{'='*50}
天网恢恢，疏而不失。
每一个小善都落地生根，每一个小恶都无处可藏。

— 龍魂道德哨兵·P30
DNA根码：{CONFIG['DNA根码']}
创建者：龍芯北辰｜UID9622
"""
    return 报告

def 保存报告(报告内容):
    日期 = datetime.datetime.now().strftime("%Y-%m-%d")
    文件名 = f"哨兵日报_{日期}.txt"
    with open(文件名, "w", encoding="utf-8") as f:
        f.write(报告内容)
    print(f"✅ 日报已保存: {文件名}")
    print(报告内容)

if __name__ == '__main__':
    print("🕵️ 龍魂道德哨兵启动...")
    扫描结果 = 扫描今日日志()
    报告 = 生成报告(扫描结果)
    保存报告(报告)
    print("✅ 哨兵任务完成")

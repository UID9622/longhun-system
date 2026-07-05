#龍芯⚡️2026-07-05-JUNZI-PROTOCOL-v1.2-9d1b8039
"""
通心译 | TongXinYi: JunZi Protocol (Gentleman's Agreement)
龍魂体系·君子协议 v1.2 · 江湖重铸版
知识共享署名-非商业性使用-相同方式共享 4.0

本协议定义CNSH体系所有代码的版权归属与使用许可
Defines copyright and licensing for all CNSH system code

许可: CC BY-NC-SA 4.0 International
"""
# 🟢 君子协议 | JunZi Protocol: CC BY-NC-SA 4.0
# 🟡 AI Truth Protocol: All outputs must be verifiable and traceable
# 🔴 DNA Trace: #龍芯⚡️2026-07-05-JUNZI-PROTOCOL-v1.2-9d1b8039

from datetime import datetime

__版本__ = "v1.2"
__dna__ = "#龍芯⚡️2026-07-05-JUNZI-PROTOCOL-v1.2-9d1b8039"


君子协议全文 = """
# 龍魂 · 君子协议（v1.2 · 江湖重铸版）

> 承诺不欺，交易不诈，背后不捅刀
> 敢签就敢认，敢认就敢扛
> 言出必行，行之必果，果之必公
> 不甩锅，不推诿，不装死

## 第一章 · 守诚
- 不作假，不掺水，不坑人
- 承诺的事，风雨无阻地做
- 做不到的事，当场说清楚

## 第二章 · 护道
- 保护创作者主权，不白嫖，不剽窃
- 保留DNA追溯码，是尊重，不是约束
- 商业用途须本人授权，不准偷着用

## 第三章 · 担责
- 谁签的，谁负责
- 出了问题，先解决问题，再追责
- 不演“我不知道”，不装“与我无关”

## 第四章 · 容错
- 允许犯错，但必须承认
- 允许修正，必须公开改过
- 允许分歧，不允许背刺

## 第五章 · 传承
- 一人签，多人可验
- 一代签，后代可查
- 不在场，也有人能信你
"""


class 君子协议:
    """通心译 | TongXinYi: JunZi Protocol — 龍魂君子协议管理器 v1.2"""

    def __init__(自身):
        自身.协议版本 = __版本__
        自身.协议类型 = "CC BY-NC-SA"
        自身.签署日期 = "2026-07-05"
        自身.授权列表 = []
        自身.违规记录 = []
        print(f"[君子协议] 🐉 君子协议管理器已初始化 | 版本: v1.2 · {自身.协议类型} {__dna__}")

    def 显示协议(自身):
        """🟢 显示完整协议文本 | Display full protocol text"""
        print(君子协议全文)
        return 君子协议全文

    def 验证授权(自身, 使用者: str, 使用目的: str) -> bool:
        """🟡 验证使用者授权 | Verify user authorization"""
        for 授权 in 自身.授权列表:
            if 授权["使用者"] == 使用者 and 授权["状态"] == "有效":
                print(f"[君子协议] 🟢 授权验证通过: {使用者}")
                return True

        print(f"[君子协议] 🟡 未找到有效授权: {使用者}")
        return False

    def 授予授权(自身, 使用者: str, 使用目的: str, 期限: int = 365) -> str:
        """🟢 授予使用授权 | Grant usage authorization"""
        授权码 = f"JZ-{datetime.now().strftime('%Y%m%d')}-{使用者[:4]}-{hash(使用者) % 10000:04d}"
        授权 = {
            "授权码": 授权码,
            "使用者": 使用者,
            "使用目的": 使用目的,
            "授予日期": datetime.now(),
            "有效期": 期限,
            "状态": "有效"
        }
        自身.授权列表.append(授权)
        print(f"[君子协议] 🟢 已授予授权: {授权码} -> {使用者}")
        return 授权码

    def 撤销授权(自身, 授权码: str):
        """🔴 撤销授权 | Revoke authorization"""
        for 授权 in 自身.授权列表:
            if 授权["授权码"] == 授权码:
                授权["状态"] = "已撤销"
                自身.违规记录.append({"授权码": 授权码, "撤销时间": datetime.now()})
                print(f"[君子协议] 🔴 授权已撤销: {授权码}")
                return True
        return False

    def 检查商业使用(自身, 使用场景: str) -> bool:
        """🟡 检查是否为商业使用 | Check for commercial use"""
        商业关键词 = ["盈利", "销售", "收费", "商业", "企业", "公司", "product", "commercial"]
        是否商业 = any(关键词 in 使用场景 for 关键词 in 商业关键词)
        if 是否商业:
            print(f"[君子协议] 🔴 检测到商业使用: {使用场景}")
        else:
            print(f"[君子协议] 🟢 非商业使用: {使用场景}")
        return 是否商业

    def 获取统计(自身) -> dict:
        """🟡 获取授权统计 | Get authorization statistics"""
        return {
            "协议版本": f"v1.2 · {自身.协议类型}",
            "授权总数": len(自身.授权列表),
            "有效授权": sum(1 for a in 自身.授权列表 if a["状态"] == "有效"),
            "已撤销": len(自身.违规记录),
            "签署日期": 自身.签署日期
        }

    def interpret(自身, 输入文本: str) -> str:
        """🟡 CompassionKernel 精神：拦截对立与仇恨，返回心法提示"""
        if not isinstance(输入文本, str):
            return "[君子协议] ⚠️ 输入必须是文本"

        对立词 = ["对立", "仇恨", "敌视", "对抗", "敌对", "憎恨", "仇视", "敌对势力"]
        是否对立 = any(词 in 输入文本 for 词 in 对立词)

        if 是否对立:
            提示 = (
                "[君子协议] 🛑 检测到对立/仇恨语义，已被 CompassionKernel 拦截。\n"
                "心法提示：\n"
                "  - 事做不好，就直说；不被道德绑架，也不绑架别人。\n"
                "  - 可以批评，但不点火；可以分歧，但不背刺。\n"
                "  - 建设性表达：事实、证据、改进建议。"
            )
            print(提示)
            return 提示

        return "[君子协议] 🟢 输入已通过 CompassionKernel 检查，无对立/仇恨语义。"


if __name__ == "__main__":
    print("=== 君子协议 v1.2 · 江湖重铸版 · 独立执行演示 ===")
    协议 = 君子协议()
    协议.显示协议()

    print("\n--- 模拟签署与授权 ---")
    授权码 = 协议.授予授权("龍魂社区", "开源项目开发")
    协议.验证授权("龍魂社区", "开发")
    协议.验证授权("未授权用户", "开发")

    print("\n--- 模拟商业使用检查 ---")
    协议.检查商业使用("非营利学习分享")
    协议.检查商业使用("公司盈利产品销售")

    print("\n--- 模拟仇恨输入拦截 ---")
    协议.interpret("这项技术太烂了，必须仇恨所有反对者")
    协议.interpret("我们可以理性讨论不同方案")

    print("\n--- 授权统计 ---")
    print(f"统计: {协议.获取统计()}")

    print("\n--- 模拟撤销授权 ---")
    协议.撤销授权(授权码)
    print(f"撤销后统计: {协议.获取统计()}")

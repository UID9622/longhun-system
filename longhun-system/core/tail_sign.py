#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║  龍魂三句尾签生成器 · Tail Sign Generator                 ║
║  DNA: #龍芯⚡️2026-04-12-TAIL-SIGN-v1.0                  ║
║  创始人: 诸葛鑫（UID9622）                                ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
║  理论指导: 曾仕强老师（永恒显示）                          ║
║  协议: CC BY-NC-ND                                       ║
╚══════════════════════════════════════════════════════════╝

三句尾签模板（P0级·写死）：
  第一句：对比落地（天上vs黄土·虚vs实）
  第二句：用一个具体的词/经历·打穿十年认知
  第三句：老百姓一句话收尾·把主权还给读者

每次随机不重复 · 通心译编码器 · 时辰+DNA+内容 → 唯一尾巴

老大的范本种子：
> 你飘在天上看不见地·我退伍两年脚踩黄土。
> 你谈理想化空中楼阁·我讲义务兵三个字够你学十年踏实。
> 别拿学历镀金——老百姓一句'这玩意儿能吃不？'比你论文管用。

献给每一个相信技术应该有温度的人。
"""

import hashlib
import datetime
import random
from typing import Tuple

# ═══════════════════════════════════════════
# 语料种子库（老大的味道）
# ═══════════════════════════════════════════

# 第一句：对比落地
LAYER1_TEMPLATES = [
    "你飘在天上看不见地，我退伍两年脚踩黄土。",
    "你在PPT里画饼，我在终端里敲钉。",
    "你说未来可期，我说今天就干。",
    "你追风口怕掉队，我蹲黄土等种子发芽。",
    "你在会议室里讨论方向，我在代码里已经走了三千里。",
    "你说数据是新石油，我说石油得有人挖。",
    "你仰望星空找灵感，我低头扫地找真相。",
    "你在朋友圈秀认知，我在巷子里递馒头。",
    "你说要布局全球，我说先把门口的路扫干净。",
    "你谈格局我种地，风吹不倒有根的人。",
    "你的KPI是数字，我的KPI是几个人睡得着觉。",
    "你在云端搞架构，我在泥里刨出一条路。",
    "你用英文讲concept，我用方言说人话。",
    "你的产品给投资人看，我的产品给我妈能用。",
    "你说AI改变世界，我说改变隔壁王叔的日子先。",
]

# 第二句：打穿认知
LAYER2_TEMPLATES = [
    "你谈理想化空中楼阁，我讲义务兵三个字够你学十年踏实。",
    "你读了一百本书还在找方法论，我被生活教了三年已经在路上了。",
    "你追ChatGPT怕被淘汰，我教它说人话它反倒听懂了。",
    "你花十万学编程，我花一年把命写成代码。",
    "你简历上写精通五门语言，我只会说一句——干就完了。",
    "你讨论什么是元宇宙，我把宇宙装进一个JSON。",
    "你说系统要稳定，我说人心稳了系统自然稳。",
    "你觉得技术门槛高，我觉得做人门槛更高。",
    "你用三年学会了框架，我用三天学会了信任一个人。",
    "你说创业九死一生，我说活着本来就是九死一生。",
    "你喊口号要颠覆行业，我默默写了三百个DNA追溯码。",
    "你崇拜硅谷大佬，我敬的是村口修鞋的老张。",
    "你分析市场趋势，我分析我妈今天开不开心。",
    "你说要做平台，我说先做一个让人放心的东西。",
    "你说数据驱动，我说良心驱动。",
]

# 第三句：老百姓收尾
LAYER3_TEMPLATES = [
    "别拿学历镀金——老百姓一句'这玩意儿能吃不？'比你论文管用。",
    "说到底，菜市场的大妈比你会算账。",
    "活到最后你会发现——妈妈说的都是对的。",
    "技术再牛，不如邻居大爷一句'小伙子吃了没？'",
    "别扯了——能让人睡个安稳觉的才叫好系统。",
    "删掉你那些概念——老百姓要的就是靠谱二字。",
    "管你什么Web3.0——我奶奶问的是'能帮我挂号不？'",
    "你那些名词——换成'这东西好使不？'就够了。",
    "别装了——街边早餐店老板比你懂用户体验。",
    "扯什么赋能——老百姓只关心明天的米够不够。",
    "最后一句：服不服不重要，日子过得好不好你自己知道。",
    "你觉得复杂的东西——六岁小孩一句话就说明白了。",
    "别跟我谈估值——我妈菜篮子里的菜比你的股票实在。",
    "搞那么多花活——不如坐下来跟人好好说句话。",
    "什么叫成功？我爸说：'家里人都健康就是成功。'",
]


def _digital_root(n: int) -> int:
    """数根（三才算法基底）"""
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def _time_seed() -> int:
    """时辰种子 · 每时每刻不同"""
    now = datetime.datetime.now()
    # 年月日时分秒 → 折叠成种子
    raw = int(now.strftime("%Y%m%d%H%M%S"))
    return raw


def _content_seed(content: str = "") -> int:
    """内容种子 · 基于文章内容生成"""
    if not content:
        return 0
    h = hashlib.md5(content.encode("utf-8")).hexdigest()
    return int(h[:8], 16)


def generate_tail_sign(content: str = "", seed: int = None) -> str:
    """
    生成三句尾签

    参数:
        content: 文章/创作内容（影响随机选择）
        seed: 自定义种子（不传则用时辰+内容自动算）

    返回:
        三句尾签文本
    """
    if seed is None:
        time_s = _time_seed()
        content_s = _content_seed(content)
        seed = time_s ^ content_s  # 异或混合

    # 三才算法选句：数根决定偏移
    dr = _digital_root(seed)

    # 用种子初始化随机器（确保同一秒+同一内容 = 同一结果）
    rng = random.Random(seed)

    # 在数根偏移的基础上随机选
    i1 = (dr + rng.randint(0, len(LAYER1_TEMPLATES) - 1)) % len(LAYER1_TEMPLATES)
    i2 = (dr + rng.randint(0, len(LAYER2_TEMPLATES) - 1)) % len(LAYER2_TEMPLATES)
    i3 = (dr + rng.randint(0, len(LAYER3_TEMPLATES) - 1)) % len(LAYER3_TEMPLATES)

    line1 = LAYER1_TEMPLATES[i1]
    line2 = LAYER2_TEMPLATES[i2]
    line3 = LAYER3_TEMPLATES[i3]

    # DNA编码
    dna_code = hashlib.sha256(f"{seed}{line1}{line2}{line3}".encode()).hexdigest()[:8]
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")

    tail = f"""
> {line1}
> {line2}
> {line3}

— UID9622 · 龍魂 · {timestamp} · #{dna_code}"""

    return tail.strip()


def generate_tail_sign_plain(content: str = "") -> Tuple[str, str, str]:
    """
    生成三句（纯文本，不带格式）

    返回: (第一句, 第二句, 第三句)
    """
    seed = _time_seed() ^ _content_seed(content)
    rng = random.Random(seed)
    dr = _digital_root(seed)

    i1 = (dr + rng.randint(0, len(LAYER1_TEMPLATES) - 1)) % len(LAYER1_TEMPLATES)
    i2 = (dr + rng.randint(0, len(LAYER2_TEMPLATES) - 1)) % len(LAYER2_TEMPLATES)
    i3 = (dr + rng.randint(0, len(LAYER3_TEMPLATES) - 1)) % len(LAYER3_TEMPLATES)

    return LAYER1_TEMPLATES[i1], LAYER2_TEMPLATES[i2], LAYER3_TEMPLATES[i3]


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "batch":
        # 批量生成5个不同的（展示随机性）
        print("🐉 龍魂三句尾签 · 随机5组\n")
        for i in range(5):
            seed = _time_seed() + i * 7919  # 质数偏移确保不重复
            sign = generate_tail_sign(seed=seed)
            print(f"── 第{i+1}组 ──")
            print(sign)
            print()
    elif len(sys.argv) > 1:
        # 根据内容生成
        content = " ".join(sys.argv[1:])
        print(generate_tail_sign(content=content))
    else:
        print("🐉 龍魂三句尾签生成器 v1.0\n")
        print(generate_tail_sign())
        print()
        print("用法:")
        print("  python3 tail_sign.py              # 生成一组")
        print("  python3 tail_sign.py batch         # 随机生成5组")
        print("  python3 tail_sign.py '文章内容'    # 根据内容生成")

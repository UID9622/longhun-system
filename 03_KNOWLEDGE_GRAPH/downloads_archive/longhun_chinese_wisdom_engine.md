# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 中国智慧引擎 v1.0

> 发布日期: 2026-07-15
> 发布者: UID9622 (龍芯北辰)
> 协议类型: 文化层 · 中国智慧融合引擎
> 适用范围: 龍魂系统人格系统、决策辅助、社交分析、情绪识别
> 核心融合: 红楼梦人情世故 + 易经多变 + 道德经底座

---

## 第一层: 道德经底座 (道)

### 1.1 核心原则

```
道可道，非常道。名可名，非常名。
无名天地之始，有名万物之母。
```

**龍魂映射**: 系统底层不可言说，运行逻辑不可穷尽。规则是死的，执行是活的。

### 1.2 道德经十二铁律 (引擎底座)

| 铁律 | 原文 | 龍魂映射 |
|------|------|---------|
| 无为 | 无为而无不为 | 系统不强制，用户自主 |
| 柔弱 | 柔弱胜刚强 | 以柔克刚，不硬碰硬 |
| 不争 | 夫唯不争，故天下莫能与之争 | 不争排名，只做实事 |
| 知足 | 知足不辱，知止不殆 | 够用就行，不贪多 |
| 反者 | 反者道之动 | 物极必反，留有余地 |
| 少则 | 少则得，多则惑 | 精简聚焦，不扩列 |
| 上善 | 上善若水 | 利万物而不争 |
| 自知 | 知人者智，自知者明 | 知道自己几斤几两 |
| 慎始 | 慎终如始，则无败事 | 开头谨慎，结尾一样 |
| 大成 | 大成若缺，其用不弊 | 完美有缺，反而长久 |
| 信言 | 信言不美，美言不信 | 真实难听，好听虚假 |
| 轻诺 | 轻诺必寡信 | 不随便承诺，承诺必兑现 |

---

## 第二层: 易经多变 (术)

### 2.1 六十四卦决策矩阵

```python
class YijingDecisionMatrix:
    # 易经六十四卦决策矩阵

    HEXAGRAMS = {
        # 乾卦: 天行健，君子以自强不息
        "乾": {"situation": "创业/开拓", "action": "主动进攻", "risk": "过刚易折"},

        # 坤卦: 地势坤，君子以厚德载物
        "坤": {"situation": "守成/承载", "action": "包容接纳", "risk": "过于柔顺"},

        # 屯卦: 水雷屯，君子以经纶
        "屯": {"situation": "初创/艰难", "action": "积蓄力量", "risk": "急于求成"},

        # 蒙卦: 山水蒙，君子以果行育德
        "蒙": {"situation": "蒙昧/学习", "action": "启蒙教育", "risk": "固执己见"},

        # 需卦: 水天需，君子以饮食宴乐
        "需": {"situation": "等待/时机", "action": "耐心等待", "risk": "错失良机"},

        # 讼卦: 天水讼，君子以作事谋始
        "讼": {"situation": "争议/纠纷", "action": "预防为主", "risk": "两败俱伤"},

        # 师卦: 地水师，君子以容民畜众
        "师": {"situation": "团队/组织", "action": "严明纪律", "risk": "刚愎自用"},

        # 比卦: 水地比，君子以建万国亲诸侯
        "比": {"situation": "合作/联盟", "action": "诚信结盟", "risk": "依附小人"},

        # 小畜: 风天小畜，君子以懿文德
        "小畜": {"situation": "小有积蓄", "action": "蓄养待时", "risk": "志得意满"},

        # 履卦: 天泽履，君子以辨上下定民志
        "履": {"situation": "践行/实践", "action": "谨慎行事", "risk": "冒进失礼"},

        # 泰卦: 天地泰，君子以财成天地之道
        "泰": {"situation": "通泰/顺利", "action": "把握时机", "risk": "乐极生悲"},

        # 否卦: 天地否，君子以俭德辟难
        "否": {"situation": "闭塞/不顺", "action": "收敛自保", "risk": "消极沉沦"},

        # 同人: 天火同人，君子以类族辨物
        "同人": {"situation": "团结/共识", "action": "求同存异", "risk": "同而不和"},

        # 大有: 火天大有，君子以遏恶扬善
        "大有": {"situation": "大有收获", "action": "分享成果", "risk": "骄傲自满"},

        # 谦卦: 地山谦，君子以裒多益寡
        "谦": {"situation": "谦虚/低调", "action": "保持谦逊", "risk": "虚伪做作"},

        # 豫卦: 雷地豫，君子以作乐崇德
        "豫": {"situation": "喜悦/安乐", "action": "适度享受", "risk": "耽于享乐"},

        # 随卦: 泽雷随，君子以向晦入宴息
        "随": {"situation": "跟随/顺应", "action": "择善而从", "risk": "盲从附和"},

        # 蛊卦: 山风蛊，君子以振民育德
        "蛊": {"situation": "腐败/整顿", "action": "革新除弊", "risk": "矫枉过正"},

        # 临卦: 地泽临，君子以教思无穷
        "临": {"situation": "领导/监督", "action": "以身作则", "risk": "居高临下"},

        # 观卦: 风地观，君子以省方观民
        "观": {"situation": "观察/审视", "action": "深入观察", "risk": "表面文章"},

        # 噬嗑: 火雷噬嗑，君子以明罚勅法
        "噬嗑": {"situation": "执法/惩戒", "action": "公正严明", "risk": "滥用刑罚"},

        # 贲卦: 山火贲，君子以明庶政
        "贲": {"situation": "装饰/美化", "action": "适度修饰", "risk": "华而不实"},

        # 剥卦: 山地剥，君子以厚下安宅
        "剥": {"situation": "剥落/衰败", "action": "固本培元", "risk": "坐以待毙"},

        # 复卦: 地雷复，君子以闭关修养
        "复": {"situation": "复兴/回归", "action": "休养生息", "risk": "操之过急"},

        # 无妄: 天雷无妄，君子以茂对时育万物
        "无妄": {"situation": "无妄/真实", "action": "实事求是", "risk": "妄动招祸"},

        # 大畜: 山天大畜，君子以多识前言往行
        "大畜": {"situation": "大积蓄", "action": "厚积薄发", "risk": "固步自封"},

        # 颐卦: 山雷颐，君子以慎言语节饮食
        "颐": {"situation": "养生/自养", "action": "节制自律", "risk": "纵欲伤身"},

        # 大过: 泽风大过，君子以独立不惧
        "大过": {"situation": "大过/非常", "action": "非常手段", "risk": "孤注一掷"},

        # 坎卦: 水水坎，君子以常德行习教事
        "坎": {"situation": "险难/困境", "action": "坚守诚信", "risk": "投机取巧"},

        # 离卦: 火火离，君子以继明照于四方
        "离": {"situation": "光明/依附", "action": "依附正道", "risk": "依附邪道"},

        # 咸卦: 泽山咸，君子以虚受人
        "咸": {"situation": "感应/沟通", "action": "虚心接纳", "risk": "轻信盲从"},

        # 恒卦: 雷风恒，君子以立不易方
        "恒": {"situation": "恒久/坚持", "action": "持之以恒", "risk": "固执不变"},

        # 遁卦: 天山遁，君子以远小人
        "遁": {"situation": "退避/隐遁", "action": "适时退避", "risk": "逃避责任"},

        # 大壮: 雷天大壮，君子以非礼弗履
        "大壮": {"situation": "强盛/壮盛", "action": "守礼节制", "risk": "恃强凌弱"},

        # 晋卦: 火地晋，君子以自昭明德
        "晋": {"situation": "晋升/进步", "action": "光明正大", "risk": "钻营投机"},

        # 明夷: 地火明夷，君子以莅众用晦而明
        "明夷": {"situation": "光明受损", "action": "韬光养晦", "risk": "锋芒毕露"},

        # 家人: 风火家人，君子以言有物而行有恒
        "家人": {"situation": "家庭/内部", "action": "正家修身", "risk": "家丑外扬"},

        # 睽卦: 火泽睽，君子以同而异
        "睽": {"situation": "背离/分歧", "action": "求同存异", "risk": "激化矛盾"},

        # 蹇卦: 水山蹇，君子以反身修德
        "蹇": {"situation": "艰难/险阻", "action": "反省自身", "risk": "怨天尤人"},

        # 解卦: 雷水解，君子以赦过宥罪
        "解": {"situation": "解脱/化解", "action": "宽宥包容", "risk": "纵容姑息"},

        # 损卦: 山泽损，君子以惩忿窒欲
        "损": {"situation": "减损/节制", "action": "克制欲望", "risk": "损人利己"},

        # 益卦: 风雷益，君子以见善则迁
        "益": {"situation": "增益/受益", "action": "见贤思齐", "risk": "贪得无厌"},

        # 夬卦: 泽天夬，君子以施禄及下
        "夬": {"situation": "决断/裁决", "action": "果断公正", "risk": "独断专行"},

        # 姤卦: 天风姤，君子以施命诰四方
        "姤": {"situation": "相遇/邂逅", "action": "谨慎交往", "risk": "遇人不淑"},

        # 萃卦: 泽地萃，君子以除戎器戒不虞
        "萃": {"situation": "聚集/汇聚", "action": "凝聚力量", "risk": "乌合之众"},

        # 升卦: 地风升，君子以顺德积小以高大
        "升": {"situation": "上升/进步", "action": "循序渐进", "risk": "急功近利"},

        # 困卦: 泽水困，君子以致命遂志
        "困": {"situation": "困穷/窘迫", "action": "坚守志向", "risk": "放弃原则"},

        # 井卦: 水风井，君子以劳民劝相
        "井": {"situation": "井养/供给", "action": "造福大众", "risk": "竭泽而渔"},

        # 革卦: 泽火革，君子以治历明时
        "革": {"situation": "变革/革新", "action": "顺应天时", "risk": "盲目变革"},

        # 鼎卦: 火风鼎，君子以正位凝命
        "鼎": {"situation": "鼎新/稳定", "action": "正位当权", "risk": "权欲熏心"},

        # 震卦: 雷雷震，君子以恐惧修省
        "震": {"situation": "震动/惊惧", "action": "修身反省", "risk": "惊慌失措"},

        # 艮卦: 山山艮，君子以思不出其位
        "艮": {"situation": "止/静止", "action": "知止当止", "risk": "停滞不前"},

        # 渐卦: 风山渐，君子以居贤德善俗
        "渐": {"situation": "渐进/逐步", "action": "循序渐进", "risk": "急于求成"},

        # 归妹: 雷泽归妹，君子以永终知敝
        "归妹": {"situation": "婚嫁/归宿", "action": "慎重选择", "risk": "草率决定"},

        # 丰卦: 雷火丰，君子以折狱致刑
        "丰": {"situation": "丰盛/盛大", "action": "明断是非", "risk": "盛极而衰"},

        # 旅卦: 火山旅，君子以明慎用刑
        "旅": {"situation": "旅行/漂泊", "action": "谨慎行事", "risk": "漂泊无依"},

        # 巽卦: 风风巽，君子以申命行事
        "巽": {"situation": "顺从/谦逊", "action": "申命执行", "risk": "优柔寡断"},

        # 兑卦: 泽泽兑，君子以朋友讲习
        "兑": {"situation": "喜悦/交流", "action": "和悦交流", "risk": "口是心非"},

        # 涣卦: 风水涣，君子以享于上帝立庙
        "涣": {"situation": "涣散/离散", "action": "凝聚人心", "risk": "分崩离析"},

        # 节卦: 水泽节，君子以制数度议德行
        "节": {"situation": "节制/节约", "action": "适度节制", "risk": "过度吝啬"},

        # 中孚: 风泽中孚，君子以议狱缓死
        "中孚": {"situation": "诚信/中实", "action": "诚信为本", "risk": "虚伪欺诈"},

        # 小过: 雷山小过，君子以行过乎恭
        "小过": {"situation": "小过/过度", "action": "适度调整", "risk": "因小失大"},

        # 既济: 水火既济，君子以思患而豫防
        "既济": {"situation": "完成/成功", "action": "防患未然", "risk": "得意忘形"},

        # 未济: 火水未济，君子以慎辨物居方
        "未济": {"situation": "未完成", "action": "谨慎辨物", "risk": "盲目冒进"}
    }

    def get_decision(self, situation: str) -> dict:
        # 根据情境获取卦象决策
        for hex_name, hex_info in self.HEXAGRAMS.items():
            if hex_info["situation"] in situation:
                return {
                    "hexagram": hex_name,
                    "situation": hex_info["situation"],
                    "action": hex_info["action"],
                    "risk": hex_info["risk"],
                    "advice": f"当前情境: {hex_info['situation']}, "
                              f"建议行动: {hex_info['action']}, "
                              f"注意风险: {hex_info['risk']}"
                }

        return {"error": "未找到对应卦象", "situation": situation}
```

### 2.2 五行权重决策

```python
class WuxingWeight:
    # 五行权重决策系统

    ELEMENTS = {
        "金": {"trait": "刚健/决断", "color": "白", "direction": "西"},
        "木": {"trait": "生长/仁慈", "color": "青", "direction": "东"},
        "水": {"trait": "智慧/流动", "color": "黑", "direction": "北"},
        "火": {"trait": "热情/光明", "color": "赤", "direction": "南"},
        "土": {"trait": "包容/稳定", "color": "黄", "direction": "中"}
    }

    def calculate_weight(self, context: dict) -> dict:
        # 根据上下文计算五行权重

        weights = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}

        # 根据情境调整权重
        if context.get("decision_type") == "战略":
            weights["水"] += 0.3  # 智慧
            weights["土"] += 0.3  # 稳定

        if context.get("urgency") == "高":
            weights["火"] += 0.4  # 热情/行动

        if context.get("risk") == "高":
            weights["金"] += 0.3  # 决断
            weights["水"] += 0.2  # 智慧

        if context.get("team_size") > 10:
            weights["土"] += 0.3  # 包容/稳定

        # 归一化
        total = sum(weights.values())
        if total > 0:
            weights = {k: v/total for k, v in weights.items()}

        # 找出主导元素
        dominant = max(weights, key=weights.get)

        return {
            "weights": weights,
            "dominant": dominant,
            "trait": self.ELEMENTS[dominant]["trait"],
            "advice": f"当前主导元素: {dominant} ({self.ELEMENTS[dominant]['trait']}), "
                      f"建议: {self._get_advice(dominant)}"
        }

    def _get_advice(self, element: str) -> str:
        advice_map = {
            "金": "果断决策，但避免过于刚硬",
            "木": "生长发展，但避免盲目扩张",
            "水": "灵活应变，但避免随波逐流",
            "火": "热情行动，但避免冲动冒进",
            "土": "稳定包容，但避免固步自封"
        }
        return advice_map.get(element, "平衡发展")
```

---

## 第三层: 红楼梦人情世故 (器)

### 3.1 人情世故引擎

```python
class HongloumenSocialEngine:
    # 红楼梦人情世故引擎

    RELATIONSHIP_PATTERNS = {
        # 王熙凤模式: 精明强干，八面玲珑
        "王熙凤": {
            "trait": "精明/强势/掌控",
            "strength": "执行力强，能搞定事",
            "weakness": "树敌太多，不得善终",
            "use_case": "需要快速推进，解决复杂问题",
            "risk": "过于强势，引起反弹"
        },

        # 薛宝钗模式: 稳重圆融，藏愚守拙
        "薛宝钗": {
            "trait": "稳重/圆融/藏拙",
            "strength": "不得罪人，人缘好",
            "weakness": "缺乏真情，过于世故",
            "use_case": "需要维护关系，避免冲突",
            "risk": "过于圆滑，缺乏真诚"
        },

        # 林黛玉模式: 敏感细腻，真情流露
        "林黛玉": {
            "trait": "敏感/细腻/真情",
            "strength": "洞察人心，情感真挚",
            "weakness": "过于敏感，容易受伤",
            "use_case": "需要深度沟通，建立信任",
            "risk": "情绪化，影响判断"
        },

        # 贾宝玉模式: 博爱多情，不谙世事
        "贾宝玉": {
            "trait": "博爱/多情/理想",
            "strength": "真诚待人，有魅力",
            "weakness": "不务正业，缺乏担当",
            "use_case": "需要凝聚人心，激发热情",
            "risk": "过于理想化，脱离现实"
        },

        # 贾母模式: 德高望重，平衡各方
        "贾母": {
            "trait": "权威/平衡/智慧",
            "strength": "一言九鼎，能镇场面",
            "weakness": "年老保守，难以变革",
            "use_case": "需要权威背书，平衡矛盾",
            "risk": "过于保守，阻碍创新"
        },

        # 刘姥姥模式: 朴实智慧，知恩图报
        "刘姥姥": {
            "trait": "朴实/智慧/感恩",
            "strength": "接地气，懂人情",
            "weakness": "地位低，话语权弱",
            "use_case": "需要基层支持，了解民情",
            "risk": "被轻视，难以发挥作用"
        },

        # 贾探春模式: 精明能干，志向远大
        "贾探春": {
            "trait": "精明/能干/志向",
            "strength": "有远见，能改革",
            "weakness": "出身庶出，受限多",
            "use_case": "需要改革创新，突破困境",
            "risk": "阻力大，容易失败"
        },

        # 袭人模式: 忠诚可靠，细心周到
        "袭人": {
            "trait": "忠诚/细心/周到",
            "strength": "可靠，让人放心",
            "weakness": "缺乏主见，依附性强",
            "use_case": "需要执行细节，维护日常",
            "risk": "过于依附，缺乏独立性"
        }
    }

    def analyze_situation(self, characters: list, 
                         context: str) -> dict:
        # 分析红楼情境，给出人情世故建议

        analysis = {
            "characters": characters,
            "context": context,
            "dynamics": [],
            "advice": ""
        }

        # 分析人物关系动态
        for char in characters:
            if char in self.RELATIONSHIP_PATTERNS:
                pattern = self.RELATIONSHIP_PATTERNS[char]
                analysis["dynamics"].append({
                    "character": char,
                    "trait": pattern["trait"],
                    "role": self._determine_role(char, context)
                })

        # 生成建议
        analysis["advice"] = self._generate_advice(analysis["dynamics"])

        return analysis

    def _determine_role(self, character: str, context: str) -> str:
        # 确定人物在情境中的角色
        if "领导" in context or "决策" in context:
            return "决策者"
        elif "执行" in context or "推进" in context:
            return "执行者"
        elif "协调" in context or "沟通" in context:
            return "协调者"
        else:
            return "参与者"

    def _generate_advice(self, dynamics: list) -> str:
        # 根据人物动态生成建议
        if len(dynamics) == 1:
            return f"当前以{dynamics[0]['character']}模式为主，"
                   f"注意{dynamics[0]['trait']}的优缺点"

        # 多人物情况
        traits = [d["trait"] for d in dynamics]
        return f"当前涉及{len(dynamics)}种人格模式: {', '.join(traits)}, "
               f"建议平衡各方，避免极端"
```

### 3.2 话里话外语义规则 (附录A.4)

```python
class ImplicitMeaningDetector:
    # 话里话外语义检测器

    RULES = {
        "你看着办吧": {
            "surface": "授权",
            "actual": "实际不满意",
            "method": "上下文+语气判断"
        },
        "随便": {
            "surface": "无所谓",
            "actual": "不随便/在生气",
            "method": "情绪检测+敷衍标记"
        },
        "行吧": {
            "surface": "同意",
            "actual": "不情愿/勉强",
            "method": "情绪态度分析"
        },
        "你说的都对": {
            "surface": "认同",
            "actual": "反讽",
            "method": "反讽检测"
        },
        "嗯/哦": {
            "surface": "回应",
            "actual": "敷衍/想结束",
            "method": "敷衍标记"
        },
        "没事": {
            "surface": "没关系",
            "actual": "有事不想说",
            "method": "情绪+语义矛盾"
        },
        "挺好的": {
            "surface": "满意",
            "actual": "不好/不满意",
            "method": "语气+语义一致性"
        }
    }

    def detect(self, text: str, tone: str = "neutral") -> dict:
        # 检测话里话外含义

        for phrase, rule in self.RULES.items():
            if phrase in text:
                return {
                    "detected": True,
                    "phrase": phrase,
                    "surface_meaning": rule["surface"],
                    "actual_meaning": rule["actual"],
                    "method": rule["method"],
                    "tone": tone,
                    "confidence": self._calculate_confidence(text, tone, rule)
                }

        return {"detected": False, "text": text}

    def _calculate_confidence(self, text: str, tone: str, 
                               rule: dict) -> float:
        # 计算检测置信度
        confidence = 0.5

        # 语气加成
        if tone == "angry" and rule["actual"] == "在生气":
            confidence += 0.3
        if tone == "sarcastic" and rule["actual"] == "反讽":
            confidence += 0.3

        # 上下文加成
        if "但是" in text or "不过" in text:
            confidence += 0.1

        return min(confidence, 1.0)
```

---

## 第四层: 融合引擎

### 4.1 三层融合决策

```python
class LonghunWisdomEngine:
    # 龍魂中国智慧融合引擎

    def __init__(self):
        self.daodejing = DaodejingBase()  # 道德经底座
        self.yijing = YijingDecisionMatrix()  # 易经多变
        self.honglou = HongloumenSocialEngine()  # 红楼梦人情世故

    def decide(self, situation: str, context: dict) -> dict:
        # 三层融合决策

        # 第一层: 道德经底座 (原则)
        principle = self.daodejing.get_principle(situation)

        # 第二层: 易经决策 (策略)
        strategy = self.yijing.get_decision(situation)

        # 第三层: 红楼梦人情 (执行)
        execution = self.honglou.analyze_situation(
            context.get("characters", []),
            situation
        )

        # 融合三层
        return {
            "principle": principle,  # 道德经: 为什么做
            "strategy": strategy,     # 易经: 怎么做
            "execution": execution,   # 红楼梦: 谁来做
            "final_advice": self._fuse_advice(principle, strategy, execution)
        }

    def _fuse_advice(self, principle: dict, strategy: dict, 
                     execution: dict) -> str:
        # 融合三层建议

        advice = f"【道德经底座】{principle.get('advice', '')}
"
        advice += f"【易经策略】{strategy.get('advice', '')}
"
        advice += f"【红楼执行】{execution.get('advice', '')}
"

        return advice
```

---

## 第五层: 龍魂标识

```
龍魂系统 · 中国智慧引擎 v1.0
道德经底座 · 易经多变 · 红楼梦人情世故

道 (原则) -> 术 (策略) -> 器 (执行)

#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

---

END

#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·癸未·戊午·䷖剥-KNOWLEDGE-CRAWLER-v1.0-7F3A2B1C
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
#龍芯⚡️丙午·乙未·癸未·戊午·䷖剥-KNOWLEDGE-CRAWLER-v1.0-7F3A2B1C
"""
龍魂知识爬虫 · 底座知识采集器 v1.0

爬取中国传统文化底座知识，注入知识图谱：
  - 道德经81章 (逐章原文+译文)
  - 易经64卦 (逐卦卦辞+爻辞)
  - 28星宿
  - 五行生克
  - 河图洛书
  - 天干地支
  - 节气

数据源：公开中文知识站点 (古诗文网/百度百科等)
输出：JSON 注入 graph_data.json + 独立知识文件
"""

import requests
from bs4 import BeautifulSoup  # type: ignore[import-untyped]
import json
import os
import re
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

# ─── 配置 ───
BASE_DIR = Path(__file__).resolve().parent.parent
GRAPH_FILE = BASE_DIR / "03_知識圖譜" / "graph_data.json"
KNOWLEDGE_OUTPUT = BASE_DIR / "03_知識圖譜" / "crawled_knowledge.json"
LOG_FILE = BASE_DIR / "03_知識圖譜" / "crawler_log.jsonl"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 请求间隔（秒），尊重数据源
REQUEST_DELAY = 1.5


def dna(content: str) -> str:
    """生成 DNA 追溯码"""
    h = hashlib.sha256(content.encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-KNOWLEDGE-CRAWL-{h}"


def log(entry: dict[str, Any]):
    """写入爬虫日志"""
    entry["timestamp"] = datetime.now().isoformat()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def safe_get(url: str, timeout: int = 15) -> Optional[str]:
    """安全 HTTP GET"""
    try:
        time.sleep(REQUEST_DELAY)
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.encoding = r.apparent_encoding or "utf-8"
        if r.status_code == 200:
            return r.text
        log({"status": "error", "url": url, "code": r.status_code})
        return None
    except Exception as e:
        log({"status": "error", "url": url, "error": str(e)})
        return None


# ═══════════════════════════════════════════
# 1. 道德经 81章
# ═══════════════════════════════════════════

def crawl_daodejing() -> list[dict[str, Any]]:
    """爬取道德经81章原文"""
    print("📜 爬取道德经...")
    chapters = []

    # 数据源：古诗文网道德经
    base_url = "https://www.gushiwen.cn/guwen/book_"

    for i in range(1, 82):
        url = f"{base_url}{i}.aspx"
        html = safe_get(url)
        if not html:
            # 降级：用百度百科
            chapters.append({
                "chapter": i,
                "source": "fallback",
                "title": f"道德经·第{i}章",
                "content": f"第{i}章内容待补充"
            })
            continue

        soup = BeautifulSoup(html, "lxml")
        title_el = soup.find("h1") or soup.find("title")
        title = title_el.get_text(strip=True) if title_el else f"第{i}章"

        content_els = soup.select(".contson, .content, article, .main-content")
        content = ""
        for el in content_els:
            text = el.get_text(separator="\n", strip=True)
            if len(text) > len(content):
                content = text

        chapters.append({
            "chapter": i,
            "source": url,
            "title": title,
            "content": content[:3000]
        })

        if i % 10 == 0:
            print(f"  道德经: {i}/81")

    print(f"  ✅ 道德经完成: {len(chapters)}章")
    return chapters


# ═══════════════════════════════════════════
# 2. 易经 64卦
# ═══════════════════════════════════════════

YIJING_GUA = [
    (1, "乾", "qián", "天"), (2, "坤", "kūn", "地"),
    (3, "屯", "zhūn", "水雷"), (4, "蒙", "méng", "山水"),
    (5, "需", "xū", "水天"), (6, "讼", "sòng", "天水"),
    (7, "师", "shī", "地水"), (8, "比", "bǐ", "水地"),
    (9, "小畜", "xiǎo xù", "风天"), (10, "履", "lǚ", "天泽"),
    (11, "泰", "tài", "地天"), (12, "否", "pǐ", "天地"),
    (13, "同人", "tóng rén", "天火"), (14, "大有", "dà yǒu", "火天"),
    (15, "谦", "qiān", "地山"), (16, "豫", "yù", "雷地"),
    (17, "随", "suí", "泽雷"), (18, "蛊", "gǔ", "山风"),
    (19, "临", "lín", "地泽"), (20, "观", "guān", "风地"),
    (21, "噬嗑", "shì hé", "火雷"), (22, "贲", "bì", "山火"),
    (23, "剥", "bō", "山地"), (24, "复", "fù", "地雷"),
    (25, "无妄", "wú wàng", "天雷"), (26, "大畜", "dà chù", "山天"),
    (27, "颐", "yí", "山雷"), (28, "大过", "dà guò", "泽风"),
    (29, "坎", "kǎn", "坎为水"), (30, "离", "lí", "离为火"),
    (31, "咸", "xián", "泽山"), (32, "恒", "héng", "雷风"),
    (33, "遁", "dùn", "天山"), (34, "大壮", "dà zhuàng", "雷天"),
    (35, "晋", "jìn", "火地"), (36, "明夷", "míng yí", "地火"),
    (37, "家人", "jiā rén", "风火"), (38, "睽", "kuí", "火泽"),
    (39, "蹇", "jiǎn", "水山"), (40, "解", "xiè", "雷水"),
    (41, "损", "sǔn", "山泽"), (42, "益", "yì", "风雷"),
    (43, "夬", "guài", "泽天"), (44, "姤", "gòu", "天风"),
    (45, "萃", "cuì", "泽地"), (46, "升", "shēng", "地风"),
    (47, "困", "kùn", "泽水"), (48, "井", "jǐng", "水风"),
    (49, "革", "gé", "泽火"), (50, "鼎", "dǐng", "火风"),
    (51, "震", "zhèn", "震为雷"), (52, "艮", "gèn", "艮为山"),
    (53, "渐", "jiàn", "风山"), (54, "归妹", "guī mèi", "雷泽"),
    (55, "丰", "fēng", "雷火"), (56, "旅", "lǚ", "火山"),
    (57, "巽", "xùn", "巽为风"), (58, "兑", "duì", "兑为泽"),
    (59, "涣", "huàn", "风水"), (60, "节", "jié", "水泽"),
    (61, "中孚", "zhōng fú", "风泽"), (62, "小过", "xiǎo guò", "雷山"),
    (63, "既济", "jì jì", "水火"), (64, "未济", "wèi jì", "火水"),
]

GUA_CI = {
    1: "元亨利贞。", 2: "元亨，利牝马之贞。君子有攸往，先迷后得主，利西南得朋，东北丧朋。安贞吉。",
    3: "元亨利贞。勿用有攸往，利建侯。", 4: "亨。匪我求童蒙，童蒙求我。初筮告，再三渎，渎则不告。利贞。",
    5: "有孚，光亨，贞吉。利涉大川。", 6: "有孚，窒惕，中吉，终凶。利见大人，不利涉大川。",
    7: "贞，丈人吉，无咎。", 8: "吉。原筮，元永贞，无咎。不宁方来，后夫凶。",
    11: "小往大来，吉亨。", 12: "否之匪人，不利君子贞，大往小来。",
    15: "亨，君子有终。", 24: "亨。出入无疾，朋来无咎。反复其道，七日来复，利有攸往。",
    29: "习坎，有孚，维心亨，行有尚。", 30: "利贞，亨。畜牝牛，吉。",
    51: "亨。震来虩虩，笑言哑哑。震惊百里，不丧匕鬯。", 52: "艮其背，不获其身，行其庭，不见其人，无咎。",
    57: "小亨，利有攸往，利见大人。", 58: "亨，利贞。",
    63: "亨小，利贞。初吉终乱。", 64: "亨。小狐汔济，濡其尾，无攸利。",
}


def crawl_yijing() -> list[dict[str, Any]]:
    """爬取易经64卦"""
    print("☯️ 爬取易经64卦...")
    gua_list = []

    for idx, name, pinyin, xiang in YIJING_GUA:
        gua = {
            "index": idx,
            "name": name,
            "pinyin": pinyin,
            "xiang": xiang,
            "gua_ci": GUA_CI.get(idx, ""),
        }

        # 尝试在线爬取
        url = f"https://www.gushiwen.cn/guwen/book_{100 + idx}.aspx"
        html = safe_get(url)
        if html:
            soup = BeautifulSoup(html, "lxml")
            content_els = soup.select(".contson, .content, article")
            for el in content_els:
                text = el.get_text(separator="\n", strip=True)
                if len(text) > 20:
                    gua["full_text"] = text[:2000]
                    break

        gua["source"] = url
        gua_list.append(gua)

        if idx % 16 == 0:
            print(f"  易经: {idx}/64")

    print(f"  ✅ 易经完成: {len(gua_list)}卦")
    return gua_list


# ═══════════════════════════════════════════
# 3. 28星宿
# ═══════════════════════════════════════════

XINGXIU = [
    # 东方青龍七宿
    ("角木蛟", "角", "木", "东方青龍", "角宿，东方青龍第一宿，为龍角。主春生之机。"),
    ("亢金龍", "亢", "金", "东方青龍", "亢宿，东方青龍第二宿，为龍颈。主风雨调和。"),
    ("氐土貉", "氐", "土", "东方青龍", "氐宿，东方青龍第三宿，为龍胸。主根基稳固。"),
    ("房日兔", "房", "日", "东方青龍", "房宿，东方青龍第四宿，为龍腹。主明堂政令。"),
    ("心月狐", "心", "月", "东方青龍", "心宿，东方青龍第五宿，为龍心。主帝王之星。"),
    ("尾火虎", "尾", "火", "东方青龍", "尾宿，东方青龍第六宿，为龍尾。主子孙繁衍。"),
    ("箕水豹", "箕", "水", "东方青龍", "箕宿，东方青龍第七宿，为龍粪。主风伯飞扬。"),
    # 北方玄武七宿
    ("斗木獬", "斗", "木", "北方玄武", "斗宿，北方玄武第一宿，为南斗六星。主爵禄荣升。"),
    ("牛金牛", "牛", "金", "北方玄武", "牛宿，北方玄武第二宿，为牵牛星。主牺牲奉献。"),
    ("女土蝠", "女", "土", "北方玄武", "女宿，北方玄武第三宿，为须女星。主婚姻嫁娶。"),
    ("虚日鼠", "虚", "日", "北方玄武", "虚宿，北方玄武第四宿，为墟落。主虚怀若谷。"),
    ("危月燕", "危", "月", "北方玄武", "危宿，北方玄武第五宿，为危屋。主居安思危。"),
    ("室火猪", "室", "火", "北方玄武", "室宿，北方玄武第六宿，为营室。主宫室安居。"),
    ("壁水貐", "壁", "水", "北方玄武", "壁宿，北方玄武第七宿，为东壁。主文章图书。"),
    # 西方白虎七宿
    ("奎木狼", "奎", "木", "西方白虎", "奎宿，西方白虎第一宿，为天库。主文章府库。"),
    ("娄金狗", "娄", "金", "西方白虎", "娄宿，西方白虎第二宿，为天狱。主聚众兴兵。"),
    ("胃土雉", "胃", "土", "西方白虎", "胃宿，西方白虎第三宿，为天仓。主五谷丰登。"),
    ("昴日鸡", "昴", "日", "西方白虎", "昴宿，西方白虎第四宿，为旄头。主胡兵夷狄。"),
    ("毕月乌", "毕", "月", "西方白虎", "毕宿，西方白虎第五宿，为天网。主弋猎兵刑。"),
    ("觜火猴", "觜", "火", "西方白虎", "觜宿，西方白虎第六宿，为虎首。主参商之隔。"),
    ("参水猿", "参", "水", "西方白虎", "参宿，西方白虎第七宿，为参伐。主杀伐征讨。"),
    # 南方朱雀七宿
    ("井木犴", "井", "木", "南方朱雀", "井宿，南方朱雀第一宿，为天井。主水衡法令。"),
    ("鬼金羊", "鬼", "金", "南方朱雀", "鬼宿，南方朱雀第二宿，为舆鬼。主祭祀鬼神。"),
    ("柳土獐", "柳", "土", "南方朱雀", "柳宿，南方朱雀第三宿，为鸟嘴。主庖厨饮食。"),
    ("星日马", "星", "日", "南方朱雀", "星宿，南方朱雀第四宿，为七星。主急事文书。"),
    ("张月鹿", "张", "月", "南方朱雀", "张宿，南方朱雀第五宿，为鸟嗉。主宾客宴享。"),
    ("翼火蛇", "翼", "火", "南方朱雀", "翼宿，南方朱雀第六宿，为羽翼。主远客夷狄。"),
    ("轸水蚓", "轸", "水", "南方朱雀", "轸宿，南方朱雀第七宿，为车轸。主风伯行车。"),
]


def build_xingxiu() -> list[dict[str, Any]]:
    """构建28星宿知识"""
    print("⭐ 构建28星宿...")
    result = []
    for full_name, short_name, element, direction, desc in XINGXIU:
        result.append({
            "full_name": full_name,
            "short_name": short_name,
            "element": element,
            "direction": direction,
            "description": desc
        })
    print(f"  ✅ 28星宿完成")
    return result


# ═══════════════════════════════════════════
# 4. 五行生克
# ═══════════════════════════════════════════

WUXING = {
    "五行生克": {
        "elements": ["金", "木", "水", "火", "土"],
        "生": {
            "金生水": "金熔化成液体，似水流淌",
            "水生木": "水滋润万物，树木生长",
            "木生火": "木为火之源，钻木取火",
            "火生土": "火燃烧万物化为灰烬，灰烬即土",
            "土生金": "土中藏矿，金石从土而出"
        },
        "克": {
            "金克木": "金属刀斧可砍伐树木",
            "木克土": "树木根系可破土而出",
            "土克水": "土筑堤坝可阻挡水流",
            "水克火": "水能灭火",
            "火克金": "火能熔炼金属"
        },
        "direction": {
            "木": "东", "火": "南", "土": "中", "金": "西", "水": "北"
        },
        "season": {
            "木": "春", "火": "夏", "土": "长夏", "金": "秋", "水": "冬"
        },
        "color": {
            "木": "青", "火": "赤", "土": "黄", "金": "白", "水": "黑"
        },
        "organ": {
            "木": "肝", "火": "心", "土": "脾", "金": "肺", "水": "肾"
        },
        "emotion": {
            "木": "怒", "火": "喜", "土": "思", "金": "悲", "水": "恐"
        },
        "virtue": {
            "木": "仁", "火": "礼", "土": "信", "金": "义", "水": "智"
        }
    },
    "五行数字根映射": {
        "1,2": {"element": "木", "direction": "东", "color": "青"},
        "3,4": {"element": "火", "direction": "南", "color": "赤"},
        "5":   {"element": "土", "direction": "中", "color": "黄"},
        "6,7": {"element": "金", "direction": "西", "color": "白"},
        "8,9": {"element": "水", "direction": "北", "color": "黑"},
    }
}


# ═══════════════════════════════════════════
# 5. 河图洛书
# ═══════════════════════════════════════════

HETU_LUOSHU = {
    "河图": {
        "description": "河出图，洛出书，圣人则之。河图为先天八卦之源。",
        "pattern": {
            "天一生水，地六成之": "北",
            "地二生火，天七成之": "南",
            "天三生木，地八成之": "东",
            "地四生金，天九成之": "西",
            "天五生土，地十成之": "中"
        },
        "numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "sum": 55
    },
    "洛书": {
        "description": "洛书为后天八卦之源，九宫数理之根。戴九履一，左三右七，二四为肩，六八为足。",
        "grid": [
            [4, 9, 2],
            [3, 5, 7],
            [8, 1, 6]
        ],
        "properties": {
            "行和": 15, "列和": 15, "对角和": 15,
            "369不动点": "3-6-9为洛书能量主轴",
            "中宫5": "不动点·UID9622主权锚"
        }
    }
}


# ═══════════════════════════════════════════
# 6. 天干地支
# ═══════════════════════════════════════════

TIANGAN_DIZHI = {
    "天干": [
        {"name": "甲", "element": "木", "yin_yang": "阳", "direction": "东"},
        {"name": "乙", "element": "木", "yin_yang": "阴", "direction": "东"},
        {"name": "丙", "element": "火", "yin_yang": "阳", "direction": "南"},
        {"name": "丁", "element": "火", "yin_yang": "阴", "direction": "南"},
        {"name": "戊", "element": "土", "yin_yang": "阳", "direction": "中"},
        {"name": "己", "element": "土", "yin_yang": "阴", "direction": "中"},
        {"name": "庚", "element": "金", "yin_yang": "阳", "direction": "西"},
        {"name": "辛", "element": "金", "yin_yang": "阴", "direction": "西"},
        {"name": "壬", "element": "水", "yin_yang": "阳", "direction": "北"},
        {"name": "癸", "element": "水", "yin_yang": "阴", "direction": "北"},
    ],
    "地支": [
        {"name": "子", "animal": "鼠", "element": "水", "time": "23-1", "month": 11},
        {"name": "丑", "animal": "牛", "element": "土", "time": "1-3", "month": 12},
        {"name": "寅", "animal": "虎", "element": "木", "time": "3-5", "month": 1},
        {"name": "卯", "animal": "兔", "element": "木", "time": "5-7", "month": 2},
        {"name": "辰", "animal": "龍", "element": "土", "time": "7-9", "month": 3},
        {"name": "巳", "animal": "蛇", "element": "火", "time": "9-11", "month": 4},
        {"name": "午", "animal": "马", "element": "火", "time": "11-13", "month": 5},
        {"name": "未", "animal": "羊", "element": "土", "time": "13-15", "month": 6},
        {"name": "申", "animal": "猴", "element": "金", "time": "15-17", "month": 7},
        {"name": "酉", "animal": "鸡", "element": "金", "time": "17-19", "month": 8},
        {"name": "戌", "animal": "狗", "element": "土", "time": "19-21", "month": 9},
        {"name": "亥", "animal": "猪", "element": "水", "time": "21-23", "month": 10},
    ],
    "六十甲子": [
        "甲子","乙丑","丙寅","丁卯","戊辰","己巳","庚午","辛未","壬申","癸酉",
        "甲戌","乙亥","丙子","丁丑","戊寅","己卯","庚辰","辛巳","壬午","癸未",
        "甲申","乙酉","丙戌","丁亥","戊子","己丑","庚寅","辛卯","壬辰","癸巳",
        "甲午","乙未","丙申","丁酉","戊戌","己亥","庚子","辛丑","壬寅","癸卯",
        "甲辰","乙巳","丙午","丁未","戊申","己酉","庚戌","辛亥","壬子","癸丑",
        "甲寅","乙卯","丙辰","丁巳","戊午","己未","庚申","辛酉","壬戌","癸亥",
    ]
}


# ═══════════════════════════════════════════
# 7. 二十四节气
# ═══════════════════════════════════════════

JIEQI = [
    {"name": "立春", "season": "春", "meaning": "春季开始，万物复苏"},
    {"name": "雨水", "season": "春", "meaning": "降雨开始，雨量渐增"},
    {"name": "惊蛰", "season": "春", "meaning": "春雷乍动，惊醒蛰伏"},
    {"name": "春分", "season": "春", "meaning": "昼夜平分，春之正中"},
    {"name": "清明", "season": "春", "meaning": "天气晴朗，草木繁茂"},
    {"name": "谷雨", "season": "春", "meaning": "雨生百谷，播种希望"},
    {"name": "立夏", "season": "夏", "meaning": "夏季开始，万物生长"},
    {"name": "小满", "season": "夏", "meaning": "麦类灌浆，小得盈满"},
    {"name": "芒种", "season": "夏", "meaning": "有芒作物成熟，忙种"},
    {"name": "夏至", "season": "夏", "meaning": "白昼最长，阳极阴生"},
    {"name": "小暑", "season": "夏", "meaning": "暑气渐盛，尚未极热"},
    {"name": "大暑", "season": "夏", "meaning": "一年最热，湿热交蒸"},
    {"name": "立秋", "season": "秋", "meaning": "秋季开始，暑去凉来"},
    {"name": "处暑", "season": "秋", "meaning": "暑气终止，秋高气爽"},
    {"name": "白露", "season": "秋", "meaning": "天气转凉，露凝而白"},
    {"name": "秋分", "season": "秋", "meaning": "昼夜平分，秋之正中"},
    {"name": "寒露", "season": "秋", "meaning": "露水更冷，将凝为霜"},
    {"name": "霜降", "season": "秋", "meaning": "天气渐冷，开始有霜"},
    {"name": "立冬", "season": "冬", "meaning": "冬季开始，万物收藏"},
    {"name": "小雪", "season": "冬", "meaning": "开始降雪，但雪量不大"},
    {"name": "大雪", "season": "冬", "meaning": "降雪量增大，地面积雪"},
    {"name": "冬至", "season": "冬", "meaning": "白昼最短，阴极阳生"},
    {"name": "小寒", "season": "冬", "meaning": "气候开始寒冷"},
    {"name": "大寒", "season": "冬", "meaning": "一年最冷，寒极必反"},
]


# ═══════════════════════════════════════════
# 8. 八卦基础
# ═══════════════════════════════════════════

BAGUA = {
    "先天八卦": [
        {"name": "乾", "symbol": "☰", "nature": "天", "direction": "南", "family": "父", "number": 1},
        {"name": "兑", "symbol": "☱", "nature": "泽", "direction": "东南", "family": "少女", "number": 2},
        {"name": "离", "symbol": "☲", "nature": "火", "direction": "东", "family": "中女", "number": 3},
        {"name": "震", "symbol": "☳", "nature": "雷", "direction": "东北", "family": "长男", "number": 4},
        {"name": "巽", "symbol": "☴", "nature": "风", "direction": "西南", "family": "长女", "number": 5},
        {"name": "坎", "symbol": "☵", "nature": "水", "direction": "西", "family": "中男", "number": 6},
        {"name": "艮", "symbol": "☶", "nature": "山", "direction": "西北", "family": "少男", "number": 7},
        {"name": "坤", "symbol": "☷", "nature": "地", "direction": "北", "family": "母", "number": 8},
    ],
    "后天八卦": [
        {"name": "震", "symbol": "☳", "nature": "雷", "direction": "东", "number": 3},
        {"name": "巽", "symbol": "☴", "nature": "风", "direction": "东南", "number": 4},
        {"name": "离", "symbol": "☲", "nature": "火", "direction": "南", "number": 9},
        {"name": "坤", "symbol": "☷", "nature": "地", "direction": "西南", "number": 2},
        {"name": "兑", "symbol": "☱", "nature": "泽", "direction": "西", "number": 7},
        {"name": "乾", "symbol": "☰", "nature": "天", "direction": "西北", "number": 6},
        {"name": "坎", "symbol": "☵", "nature": "水", "direction": "北", "number": 1},
        {"name": "艮", "symbol": "☶", "nature": "山", "direction": "东北", "number": 8},
    ],
    "八卦取象歌": [
        "乾三连 ☰", "坤六断 ☷", "震仰盂 ☳", "艮覆碗 ☶",
        "离中虚 ☲", "坎中满 ☵", "兑上缺 ☱", "巽下断 ☴"
    ]
}


# ═══════════════════════════════════════════
# 9. 道家核心概念
# ═══════════════════════════════════════════

DAOIST_CONCEPTS = [
    {
        "concept": "道",
        "definition": "道可道，非常道。宇宙的本源和规律，无形无象，先天地生。",
        "properties": ["不可言说", "生万物", "周行不殆", "独立不改"],
        "related": ["德", "无为", "自然"]
    },
    {
        "concept": "德",
        "definition": "道之用也。万物得道而成为自己，德是道在具体事物中的体现。",
        "properties": ["畜养万物", "无为而无不为", "上德不德"],
        "related": ["道", "仁", "义"]
    },
    {
        "concept": "无为",
        "definition": "道常无为而无不为。不是不作为，是不妄为、顺自然而为。",
        "properties": ["不妄为", "顺自然", "为而不恃"],
        "related": ["道", "自然", "不争"]
    },
    {
        "concept": "阴阳",
        "definition": "一阴一阳之谓道。对立统一的两种基本力量。",
        "properties": ["对立统一", "互根互用", "消长转化", "动态平衡"],
        "related": ["太极", "五行", "八卦"]
    },
    {
        "concept": "太极",
        "definition": "易有太极，是生两仪。宇宙从无极到太极，太极生阴阳。",
        "properties": ["混沌未分", "含阴含阳", "万物之始"],
        "related": ["阴阳", "两仪", "四象", "八卦"]
    },
    {
        "concept": "三才",
        "definition": "立天之道曰阴与阳，立地之道曰柔与刚，立人之道曰仁与义。天地人三才。",
        "properties": ["天道", "地道", "人道", "三位一体"],
        "related": ["天地人", "369不动点"]
    },
    {
        "concept": "自然",
        "definition": "人法地，地法天，天法道，道法自然。自己如此，不加造作。",
        "properties": ["自本自根", "不加造作", "万物自化"],
        "related": ["道", "无为"]
    },
    {
        "concept": "不争",
        "definition": "上善若水，水善利万物而不争。不争故天下莫能与之争。",
        "properties": ["利万物", "处下", "以柔克刚"],
        "related": ["水", "无为", "柔弱"]
    },
    {
        "concept": "柔弱",
        "definition": "天下莫柔弱于水，而攻坚强者莫之能胜。柔弱胜刚强。",
        "properties": ["柔能克刚", "弱能胜强", "守柔曰强"],
        "related": ["水", "不争", "无为"]
    },
    {
        "concept": "知足",
        "definition": "知足者富。祸莫大于不知足，咎莫大于欲得。",
        "properties": ["知足常足", "少私寡欲", "去奢去泰"],
        "related": ["道", "德"]
    },
    {
        "concept": "反者道之动",
        "definition": "反者道之动，弱者道之用。事物发展到极点必然向反面转化。",
        "properties": ["物极必反", "周而复始", "否极泰来"],
        "related": ["道", "阴阳", "循环"]
    },
    {
        "concept": "上善若水",
        "definition": "上善若水。水善利万物而不争，处众人之所恶，故几于道。",
        "properties": ["利万物", "不争", "处下", "柔韧"],
        "related": ["道", "不争", "柔弱"]
    },
]


# ═══════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════

def inject_to_graph(knowledge: dict[str, Any]):
    """将爬取的知识注入 graph_data.json"""
    print("\n🔗 注入知识图谱...")

    # 读取现有图谱
    if GRAPH_FILE.exists():
        with open(GRAPH_FILE, "r", encoding="utf-8") as f:
            graph = json.load(f)
    else:
        graph = {"timestamp": "", "nodes": {}, "edges": []}

    nodes = graph.setdefault("nodes", {})
    edges = graph.setdefault("edges", [])
    new_count = 0

    # 注入道德经
    for ch in knowledge.get("daodejing", []):
        node_id = f"knowledge/daodejing/{ch['chapter']}"
        if node_id not in nodes:
            nodes[node_id] = {
                "node_id": node_id,
                "label": f"道德经·第{ch['chapter']}章",
                "type": "scripture",
                "dna": dna(ch.get("content", "")[:100]),
                "description": ch.get("content", "")[:200],
                "source": "crawler",
                "category": "道家经典",
                "related_nodes": ["knowledge/daoist-concepts"]
            }
            edges.append({"from": node_id, "to": "knowledge/daoist-concepts", "relation": "属于"})
            new_count += 1

    # 注入易经
    for gua in knowledge.get("yijing", []):
        node_id = f"knowledge/yijing/{gua['index']}"
        if node_id not in nodes:
            nodes[node_id] = {
                "node_id": node_id,
                "label": f"易经·{gua['name']}卦",
                "type": "scripture",
                "dna": dna(gua.get("gua_ci", "")),
                "description": gua.get("gua_ci", "")[:200],
                "source": "crawler",
                "category": "易经",
                "xiang": gua.get("xiang", ""),
                "pinyin": gua.get("pinyin", ""),
                "related_nodes": ["knowledge/bagua"]
            }
            edges.append({"from": node_id, "to": "knowledge/bagua", "relation": "八卦衍生"})
            new_count += 1

    # 注入28星宿
    for star in knowledge.get("xingxiu", []):
        node_id = f"knowledge/xingxiu/{star['short_name']}"
        if node_id not in nodes:
            nodes[node_id] = {
                "node_id": node_id,
                "label": star["full_name"],
                "type": "astronomy",
                "dna": dna(star["description"]),
                "description": star["description"],
                "source": "crawler",
                "category": "星宿",
                "direction": star["direction"],
                "element": star["element"],
                "related_nodes": ["knowledge/wuxing"]
            }
            edges.append({"from": node_id, "to": "knowledge/wuxing", "relation": "五行归属"})
            new_count += 1

    # 注入五行
    if "knowledge/wuxing" not in nodes:
        nodes["knowledge/wuxing"] = {
            "node_id": "knowledge/wuxing",
            "label": "五行生克体系",
            "type": "philosophy",
            "dna": dna("五行生克"),
            "description": "金木水火土，相生相克，万物运行之基本法则。",
            "source": "crawler",
            "category": "哲学底座"
        }
        new_count += 1

    # 注入河图洛书
    if "knowledge/hetu" not in nodes:
        nodes["knowledge/hetu"] = {
            "node_id": "knowledge/hetu",
            "label": "河图",
            "type": "philosophy",
            "dna": dna("河图"),
            "description": HETU_LUOSHU["河图"]["description"],
            "source": "crawler",
            "category": "哲学底座"
        }
        new_count += 1
    if "knowledge/luoshu" not in nodes:
        nodes["knowledge/luoshu"] = {
            "node_id": "knowledge/luoshu",
            "label": "洛书",
            "type": "philosophy",
            "dna": dna("洛书"),
            "description": HETU_LUOSHU["洛书"]["description"],
            "source": "crawler",
            "category": "哲学底座"
        }
        edges.append({"from": "knowledge/luoshu", "to": "knowledge/hetu", "relation": "河图洛书"})
        new_count += 1

    # 注入天干地支
    if "knowledge/tiangan" not in nodes:
        nodes["knowledge/tiangan"] = {
            "node_id": "knowledge/tiangan",
            "label": "十天干",
            "type": "calendar",
            "dna": dna("天干"),
            "description": "甲乙丙丁戊己庚辛壬癸，与地支配合成六十甲子纪年法。",
            "source": "crawler",
            "category": "历法"
        }
        new_count += 1
    if "knowledge/dizhi" not in nodes:
        nodes["knowledge/dizhi"] = {
            "node_id": "knowledge/dizhi",
            "label": "十二地支",
            "type": "calendar",
            "dna": dna("地支"),
            "description": "子丑寅卯辰巳午未申酉戌亥，配十二生肖与十二时辰。",
            "source": "crawler",
            "category": "历法"
        }
        edges.append({"from": "knowledge/dizhi", "to": "knowledge/tiangan", "relation": "干支合历"})
        new_count += 1

    # 注入节气
    for jq in JIEQI:
        node_id = f"knowledge/jieqi/{jq['name']}"
        if node_id not in nodes:
            nodes[node_id] = {
                "node_id": node_id,
                "label": jq["name"],
                "type": "calendar",
                "dna": dna(jq["meaning"]),
                "description": jq["meaning"],
                "source": "crawler",
                "category": "节气",
                "season": jq["season"]
            }
            new_count += 1

    # 注入八卦
    if "knowledge/bagua" not in nodes:
        nodes["knowledge/bagua"] = {
            "node_id": "knowledge/bagua",
            "label": "八卦体系",
            "type": "philosophy",
            "dna": dna("八卦"),
            "description": "先天八卦+后天八卦，阴阳爻组合而成，易经之基。",
            "source": "crawler",
            "category": "哲学底座"
        }
        new_count += 1

    # 注入道家概念
    if "knowledge/daoist-concepts" not in nodes:
        nodes["knowledge/daoist-concepts"] = {
            "node_id": "knowledge/daoist-concepts",
            "label": "道家核心概念",
            "type": "philosophy",
            "dna": dna("道家概念"),
            "description": "道、德、无为、阴阳、太极、三才等道家哲学核心概念体系。",
            "source": "crawler",
            "category": "哲学底座"
        }
        new_count += 1
    for concept in DAOIST_CONCEPTS:
        node_id = f"knowledge/daoist/{concept['concept']}"
        if node_id not in nodes:
            nodes[node_id] = {
                "node_id": node_id,
                "label": concept["concept"],
                "type": "philosophy",
                "dna": dna(concept["definition"]),
                "description": concept["definition"],
                "source": "crawler",
                "category": "道家概念",
                "properties": concept["properties"],
                "related_nodes": ["knowledge/daoist-concepts"]
            }
            edges.append({"from": node_id, "to": "knowledge/daoist-concepts", "relation": "属于"})
            new_count += 1

    # 更新图谱
    graph["timestamp"] = datetime.now().isoformat()
    with open(GRAPH_FILE, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)

    print(f"  ✅ 注入 {new_count} 个新节点到 graph_data.json")
    return new_count


def save_knowledge_file(knowledge: dict[str, Any]):
    """保存完整知识 JSON"""
    knowledge["metadata"] = {
        "dna": dna("knowledge_crawl_v1.0"),
        "timestamp": datetime.now().isoformat(),
        "crawler": "lh_knowledge_crawler.py v1.0",
        "total_sections": len(knowledge) - 1
    }
    with open(KNOWLEDGE_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(knowledge, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 知识文件: {KNOWLEDGE_OUTPUT}")


def generate_index_md(knowledge: dict[str, Any]):
    """生成知识索引 Markdown"""
    idx_path = BASE_DIR / "03_知識圖譜" / "crawled_knowledge_index.md"
    lines = [
        "# 龍魂知识图谱 · 爬取底座知识索引",
        "",
        f"**DNA**: `{dna('crawled_index')}`",
        f"**时间**: {datetime.now().isoformat()}",
        f"**爬虫**: `bin/lh_knowledge_crawler.py v1.0`",
        "",
        "---",
        "",
        "## 📊 统计",
        "",
        f"- 道德经: {len(knowledge.get('daodejing', []))}章",
        f"- 易经: {len(knowledge.get('yijing', []))}卦",
        f"- 28星宿: {len(knowledge.get('xingxiu', []))}宿",
        f"- 五行生克: 1套完整体系",
        f"- 河图洛书: 2图",
        f"- 天干地支: 天干10 + 地支12 + 六十甲子",
        f"- 二十四节气: {len(knowledge.get('jieqi', JIEQI))}个",
        f"- 八卦: 先天8 + 后天8",
        f"- 道家核心概念: {len(knowledge.get('daoist_concepts', DAOIST_CONCEPTS))}个",
        "",
        "---",
        "",
        "## 📜 道德经",
    ]
    for ch in knowledge.get("daodejing", []):
        lines.append(f"- 第{ch['chapter']}章: {ch.get('title', '')}")
    lines.extend(["", "---", "", "## ☯️ 易经64卦"])
    for gua in knowledge.get("yijing", []):
        lines.append(f"- {gua['index']}. {gua['name']}卦 ({gua.get('xiang', '')}): {gua.get('gua_ci', '')[:60]}")
    lines.extend(["", "---", "", "## ⭐ 28星宿"])
    for star in knowledge.get("xingxiu", []):
        lines.append(f"- {star['full_name']}: {star['description'][:40]}")
    lines.extend(["", "---", "", "## 🔥 五行生克", "详见 `crawled_knowledge.json` 中 `wuxing` 字段。", "", "---", "", "## 📐 河图洛书", "详见 `crawled_knowledge.json` 中 `hetu_luoshu` 字段。", "", "---", "", "## 📅 天干地支 & 节气", "详见 `crawled_knowledge.json` 中 `tiangan_dizhi` 和 `jieqi` 字段。", "", "---", "", "## 🧠 道家核心概念"])
    for c in knowledge.get("daoist_concepts", DAOIST_CONCEPTS):
        lines.append(f"- **{c['concept']}**: {c['definition'][:80]}")

    with open(idx_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✅ 索引文件: {idx_path}")


def main():
    print("=" * 60)
    print("🐉 龍魂知识爬虫 v1.0")
    print("   采集中国传统文化底座知识，注入知识图谱")
    print("=" * 60)

    knowledge = {}

    # 1. 道德经（在线爬取）
    knowledge["daodejing"] = crawl_daodejing()

    # 2. 易经64卦（在线+内置）
    knowledge["yijing"] = crawl_yijing()

    # 3. 28星宿（内置完整数据）
    knowledge["xingxiu"] = build_xingxiu()

    # 4. 五行生克（内置）
    knowledge["wuxing"] = WUXING

    # 5. 河图洛书（内置）
    knowledge["hetu_luoshu"] = HETU_LUOSHU

    # 6. 天干地支（内置）
    knowledge["tiangan_dizhi"] = TIANGAN_DIZHI

    # 7. 二十四节气（内置）
    knowledge["jieqi"] = JIEQI

    # 8. 八卦（内置）
    knowledge["bagua"] = BAGUA

    # 9. 道家概念（内置）
    knowledge["daoist_concepts"] = DAOIST_CONCEPTS

    # 保存 + 注入
    save_knowledge_file(knowledge)
    new_nodes = inject_to_graph(knowledge)
    generate_index_md(knowledge)

    # 统计
    total_items = (
        len(knowledge["daodejing"]) +
        len(knowledge["yijing"]) +
        len(knowledge["xingxiu"]) +
        1 +  # 五行
        2 +  # 河图洛书
        len(knowledge["tiangan_dizhi"]["天干"]) +
        len(knowledge["tiangan_dizhi"]["地支"]) +
        60 +  # 六十甲子
        24 +  # 节气
        16 +  # 八卦
        len(knowledge["daoist_concepts"])
    )

    print("\n" + "=" * 60)
    print(f"✅ 爬取完成!")
    print(f"   📊 知识条目: {total_items}+")
    print(f"   🔗 图谱新节点: {new_nodes}")
    print(f"   📁 输出文件:")
    print(f"      {KNOWLEDGE_OUTPUT}")
    print(f"      {GRAPH_FILE}")
    print(f"      {BASE_DIR / '03_知識圖譜' / 'crawled_knowledge_index.md'}")
    print(f"   🧬 DNA: {dna('crawl_complete')}")
    print("=" * 60)


if __name__ == "__main__":
    main()

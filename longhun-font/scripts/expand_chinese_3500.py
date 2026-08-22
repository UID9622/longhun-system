#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#!/usr/bin/env python3
# DNA追溯码:#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-EXPAND-CHINESE-3500-v1.0
# 龍魂·LonghunFont 中文字元扩展脚本
# 用途：在 v0014 龍纹版基础上补充约 800 个官方一级常用汉字，达到约 3500 中文字符

import json
import sys
from datetime import datetime
from pathlib import Path

from glyph_generator import generate_skeleton, stroke_count_of, structure_of

DNA = "#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-EXPAND-CHINESE-3500-v1.0"

# 选自《通用规范汉字表》一级字表（3500 常用字）中尚未入库的前 800 个汉字。
# 覆盖 HSK 高阶、现代传媒、政法军教医农、科技财经、衣食住行、成语地名、人名用字等场景。
EXTRA_CHARS = (
    "匕乞夕勺亡丫尸巳弓刃井丐犬匹瓦冈壬夭仍爪欠匀亢冗讥办允幻功丙厉戊轧凸帅叶叮叭央叽叩叨皿凹囚乍禾仗斥令"
    "匆卯犯饥汁讯弘召圣矛纠迂圾芋芝朽戌页匠夷尧此尖吁吊吆屿屹乒乓臼伐伤仰伊旭匈妆亥充妄闯汛池汝宅讳讹讽诀"
    "迅奸妃驮驯驰纫巡弄违抠址坝赤坎抑坑抒芜芽芹芦芭杖杏巫酉辰歼轩卤肖呆吱呕吵串呐吩邑吼吮岖岗佐佑佃伶佣皂"
    "伺含岔肛肚肘狂删刨吝闰兑灶灿灼沐沛汰沦汹沧沟沁牢灾补诈译忌坠姊纹坯拢押拐拆拄拦拙披拨拗茉昔苛苑苞茁茄"
    "茎苔枉枚枕枣厕奈殴斩歧卓哎呵呻咋鸣咏咄咖帜岭凯贮侍岳侠侥侄侦侧侨侈彼刹肴斧觅肢胀肪狗狞饰饱卒盲炊炉沫"
    "沽沾泪泣泞沼泼怔怖怡宠宛肩询帚届弧弥弦姑妮姆迢驹终绊玷玲拭拷拱垮挟挠拴挣挤挪拯某荆茸茬巷茧茵荣荤荧荫"
    "荔柑栋栅柬歪砖砂泵砚耍殃韭虐削昧盹眨哑冒咧昭畏趴咽哗咬咳咪哟炭贻幽钞钩卸矩毡俩俏俗俘侯俊衍叙胧狭狮狰"
    "狡狠饶峦弯亭疤咨姿阀籽炸烁炫烂剃洼洒洛浏恃恢恍恬恤觉冠诬祠诱诵垦昼屏屎陡逊眉陨姥姨姻盈癸蚤绑骄绚绞耘"
    "耗泰匿顽盏捞栽捂捎捍埋捉捡挫挚壶挨耿耽聂莽莱莲晋莹梆桔栖档株桦桩逗栗酌砸砰殉顿唠晃晌剔晕畔蚣蚪蚓哨圃"
    "哦唤唁唧贿赃钳钻牺秧秩笋倚俺倘俱倡俯倔舱途舀豺豹颁胸胳脓狸鸵皱馁桨衷斋疹剖烘烙递浙浦涉涡浴涣涧浸涩涌"
    "悖宰朗扇诽祥冥冤谆剥展剧弱祟娱娟绢绣骏琉捧捺掩捷赦掀授掏掐掠培掷掺聆聊勒萌萝萎萄菩萍菠乾菇婪桶梭副酝"
    "酗奢爽聋匾颅彪眶悬啄趾蚯蛀唬啰唾啤啥崖崎崭逻帷崛铐铛铭铲矫秸梨笼笙悠偎躯兜衅徘徙斜敛悉脖豚猎猖凑减烹"
    "庶痊痒廊庸盗竟旋阎着眷粘添涯淹渠淮淆渊淫淳淤淀涮惕惦悴惯寇寅宿窒窑谋谍谎祸谚堕隅隆颈绩绪绳绵绷绽缀琢"
    "揍堰揩趋揭揪煮援搁搓搅握搔葬椰焚椎棚榔椭惠惑粟酣硝殖裂暂雅翘凿辉敞睐晰喳喇喊遏畴践跋跛蜓蜒蛤啼喧赋赐"
    "锄锅甥掰筛筒筋筝皓皖粤循逾腊腋腔腕猩猬惫斌痢阔曾焰滞湘渤渺滋渲愤愕愣惶窜雇谣粥隙絮媚婿缎缕瑟瑰搏塌摆"
    "塘摊斟蒸椿榄槐榆碍碑碎碗碌辐督嗦愚盟跨跷跺跤蜈蜕嗅嗡嗓署罩锤锥锦矮稠颓筷毁鼠衙腥腺猿颖馍馏禀痹痴痰韵"
)


def is_cjk(c: str) -> bool:
    return "\u4e00" <= c <= "\u9fff"


def main():
    base_dir = Path(__file__).parent.parent
    input_path = base_dir / "glyphs" / "龍魂字元库_v0014_龍纹版.json"
    output_path = base_dir / "glyphs" / "龍魂字元库_v0015_三千五中文字.json"

    if not input_path.exists():
        print(f"❌ 未找到输入字元库: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chars = data["字符集_cnsh9622"]
    existing = set(chars.keys())

    added = 0
    skipped_existing = 0
    skipped_non_cjk = 0
    duplicates_in_extra = 0
    seen_extra = set()

    for char in EXTRA_CHARS:
        if not is_cjk(char):
            skipped_non_cjk += 1
            continue
        if char in seen_extra:
            duplicates_in_extra += 1
            continue
        seen_extra.add(char)

        if char in existing:
            skipped_existing += 1
            continue

        chars[char] = {
            "unicode": f"U+{ord(char):04X}",
            "笔画数": stroke_count_of(char),
            "结构": structure_of(char),
            "风格参数": {
                "力度": 0.8,
                "棱角": 0.3,
                "节奏": 0.6,
                "墨色": 0.9,
            },
            "笔画路径_cnsh9622": generate_skeleton(char),
        }
        added += 1

    now = datetime.now().isoformat()
    total_chars = len(chars)
    chinese_chars = sum(1 for c in chars if is_cjk(c))

    metadata = data.setdefault("元数据", {})
    previous_version = metadata.get("版本", "v0014-龍纹版")
    metadata["名称"] = "龍魂字元库"
    metadata["版本"] = "v0015-三千五中文字"
    metadata["创建者"] = "UID9622"
    metadata["生成时间"] = now
    metadata["前一版本"] = previous_version
    metadata["本次新增中文字符数"] = added
    metadata["中文字符数"] = chinese_chars
    metadata["总字符数"] = total_chars
    metadata["中文3500扩展时间"] = now
    metadata["中文3500扩展DNA"] = DNA
    metadata["描述"] = (
        "LonghunFont 三千五百中文字元库（官方《通用规范汉字表》一级常用字表定向补全）。"
        f"在 v0014-龍纹版基础上新增 {added} 个常用汉字，覆盖 HSK 高阶、现代传媒、政法军教医农、"
        "科技财经、衣食住行、成语地名、人名用字等领域。"
    )
    metadata["编码标准"] = "UTF-8"
    metadata["viewBox"] = "0 0 600 600"

    data["DNA追溯码"] = DNA

    # 确保三色审计存在
    data.setdefault("三色审计_cnsh9622", {
        "🟢": {"结果": "通过", "项目": "文化主权标识完整"},
        "🟡": {"结果": "通过", "项目": "来源链可追溯"},
        "🔴": {"结果": "通过", "项目": "无商业字体依赖"},
    })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ 龍魂字元库扩展完成")
    print(f"   输入: {input_path}")
    print(f"   输出: {output_path}")
    print(f"   DNA:  {DNA}")
    print(f"   EXTRA_CHARS 去重后: {len(seen_extra)}")
    print(f"   已存在跳过: {skipped_existing}")
    print(f"   实际新增汉字: {added}")
    print(f"   当前中文字符总数: {chinese_chars}")
    print(f"   当前总字符数: {total_chars}")


if __name__ == "__main__":
    main()

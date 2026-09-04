# DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-ac67d1c7
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-EXPAND-CHINESE-2000-v1.0
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
LonghunFont 中文字元扩展脚本 v1.0

在现有 龍魂字元库_v0010_主权完整版.json 基础上，再追加约 1000 个
常用汉字（CJK Unified Ideographs），生成 v0011-两千中文字 字元库。
"""

import json
from datetime import datetime
from pathlib import Path

from glyph_generator import generate_skeleton, structure_of, stroke_count_of

DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-EXPAND-CHINESE-2000-v1.0"

# 1050 个候选汉字，覆盖 HSK 中高级、常用传统/姓名/文学、科技制造主权、
# 姓氏地名历史、成语常用字、政法国防经济医教等领域。
# 脚本会自动去重并跳过库中已存在的字。
EXTRA_CHARS = (
    "埃唉癌艾隘岸肮盎熬袄奥澳扒拔耙霸拜斑扳版拌瓣邦榜棒镑谤褒堡宝暴鲍卑狈焙"
    "苯崩甭蹦逼鄙碧蔽毙庇闭弊壁避鞭贬辨遍膘憋彬濒宾兵柄秉炳玻播钵勃铂伯舶膊"
    "泊捕哺埠擦裁睬采蔡蚕惨苍仓藏糙曹策册叉碴察诧柴搀馋缠阐昌尝厂畅抄朝潮炒"
    "撤彻臣忱趁称呈程澄逞秤匙弛耻尺翅炽崇酬踌筹绸橱躇雏楚矗揣椽喘疮幢吹捶垂"
    "唇蠢绰茨辞瓷刺聪囱丛醋促篡摧催瘁寸撮措搭瘩歹戴贷待怠担郸旦淡弹荡捣倒祷"
    "悼蹬登凳堤迪笛涤嫡蒂缔掂典垫甸奠殿叼凋掉钓爹迭叠盯钉鼎订董侗冻抖豆痘犊"
    "睹杜渡段堆队吨敦囤遁哆垛朵舵惰峨额娥扼鄂饵贰筏乏珐帆翻矾凡返贩泛芳妨访"
    "菲啡匪吠沸酚氛坟汾忿粪枫疯逢缝奉佛孵拂幅伏浮袱甫辅釜脯赴覆傅阜讣妇咐嘎"
    "溉杆竿秆赣缸纲杠皋羔搞稿戈疙葛阁跟庚埂梗恭躬巩贡勾苟垢辜咕估孤蛊故刮剐"
    "挂乖棺罐灌逛规闺诡桂跪辊棍郭哈氦骇憨韩涵函罕撼旱悍夯壕豪郝浩菏盒阂赫贺"
    "痕哼横恒哄鸿宏喉猴瑚葫狐湖虎互户猾徊环患痪焕宦荒蝗凰煌幌挥徽蛔卉晦秽汇"
    "诲浑豁获霍击畸箕迹姬缉棘籍疾嫉脊冀祭悸寂妓嘉佳颊稼嫁监笺兼艰缄检碱拣俭"
    "荐鉴贱健饯溅僵浆蒋奖酱椒焦浇娇角缴剿轿窖皆阶劫杰睫洁芥借诫巾斤襟仅靳烬"
    "劲兢睛粳景敬径靖竞窘究玖灸救舅疚拘疽菊咀沮拒距锯炬捐倦卷绝钧峻竣郡喀卡"
    "楷慨堪砍慷扛炕烤坷柯磕壳啃恳吭孔扣枯窟库夸挎胯侩筐矿旷盔葵魁馈坤捆廓垃"
    "蜡辣赖栏篮澜揽懒滥狼郎浪劳佬酪涝蕾累垒肋棱厘犁篱漓鲤莉吏丽砾俐沥哩联镰"
    "怜帘恋良晾撩僚燎辽撂廖烈琳邻淋赁拎菱铃羚陵另溜榴刘柳咙窿垄陇搂陋卢庐掳"
    "虏麓赂禄陆驴侣屡虑挛滦抡仑纶罗锣骡骆蚂嘛麦脉蛮曼谩茫氓猫锚铆茂帽玫梅煤"
    "媒寐闷檬猛眯糜谜秘泌棉冕勉缅瞄秒庙蔑抿敏闽谬摹磨抹莫默漠陌牟拇亩墓募睦"
    "穆娜乃耐囊闹呢嫩霓泥拟腻蔫碾捻酿捏孽镊柠凝拧扭纽浓奴怒疟懦诺欧藕偶啪帕"
    "拍湃潘盼叛庞咆炮泡胚裴陪佩盆抨澎蓬篷鹏碰砒劈毗疲痞屁篇飘撇拼聘坪瓶坡颇"
    "魄粕扑仆葡蒲朴普瀑戚凄柒棋畦脐旗祁岂企契迄讫洽扦签谦黔潜谴嵌歉呛羌抢锹"
    "悄乔巧撬峭窍怯钦秦勤擒寝倾擎顷琼丘球曲圈泉拳券瘸雀群冉壤嚷扰惹仁韧妊扔"
    "戎蓉熔绒揉茹儒乳褥蕊锐若撒萨腮伞桑丧骚嫂森莎杀沙傻煞晒杉煽陕赡汕缮赏尚"
    "梢稍芍邵赊舍摄慑申伸绅婶慎牲省胜失诗虱矢驶柿誓嗜仕释氏视售瘦枢殊输淑赎"
    "薯蜀属竖恕墅摔甩栓税瞬舜朔丝斯寺饲耸颂讼搜擞酥速僳肃隋髓遂穗损蓑唆琐锁"
    "塔挞胎抬酞坍贪滩檀潭毯叹汤搪棠唐淌烫涛绦桃淘套腾梯踢蹄嚏涕屉填舔挑眺帖"
    "烃廷挺桐彤捅痛投秃徒屠兔推腿褪屯托脱陀驼拓哇娃袜豌湾挽惋婉汪旺巍韦围惟"
    "苇委伪纬蔚喂渭尉瘟闻吻紊翁挝窝卧沃呜污屋梧吴武舞坞晤悟熙矽嘻稀膝惜溪犀"
    "袭媳洗戏匣暇锨鲜贤舷涎嫌献馅宪厢箱翔响项橡萧霄哮销宵孝啸歇鞋携谐懈泻屑"
)


def main():
    base_dir = Path(__file__).parent.parent
    input_path = base_dir / "glyphs" / "龍魂字元库_v0010_主权完整版.json"
    output_path = base_dir / "glyphs" / "龍魂字元库_v0011_两千中文字.json"

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    charset = data["字符集_cnsh9622"]

    added = 0
    skipped = 0
    invalid = 0

    for char in EXTRA_CHARS:
        if not ("\u4e00" <= char <= "\u9fff"):
            invalid += 1
            continue
        if char in charset:
            skipped += 1
            continue
        charset[char] = {
            "unicode": f"U+{ord(char):04X}",
            "笔画数": stroke_count_of(char),
            "结构": structure_of(char),
            "风格参数": {"力度": 0.8, "棱角": 0.3, "节奏": 0.6, "墨色": 0.9},
            "笔画路径_cnsh9622": generate_skeleton(char),
        }
        added += 1

    cjk_count = sum(1 for c in charset.keys() if "\u4e00" <= c <= "\u9fff")
    total_count = len(charset)

    meta = data.setdefault("元数据", {})
    meta["名称"] = "龍魂字元库"
    meta["版本"] = "v0011-两千中文字"
    meta["描述"] = f"LonghunFont 两千中文字元库，含 {cjk_count} 个汉字及扩展符号"
    meta["总字符数"] = total_count
    meta["中文字符数"] = cjk_count
    meta["中文扩展时间"] = datetime.now().isoformat()
    meta["中文扩展DNA"] = DNA
    meta["说明"] = (
        "v0010 主权完整版 + 约 1000 个常用汉字扩展（HSK 中高级、"
        "科技制造、政法国防、医教经济、姓名地名、成语文学等）"
    )

    data["DNA追溯码"] = DNA

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 字元库已扩展: {output_path}")
    print(f"   DNA: {DNA}")
    print(f"   本次新增汉字: {added}")
    print(f"   跳过（已存在）: {skipped}")
    print(f"   非法字符: {invalid}")
    print(f"   当前中文字符总数: {cjk_count}")
    print(f"   当前总字符数: {total_count}")


if __name__ == "__main__":
    main()

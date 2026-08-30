# DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-832046bb
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-EXPAND-CHINESE-2600-v1.0
# 龍魂·字元库中文扩展脚本 —— 从 v0012 国际符号版扩展至约 2600 中文字符
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 用途：批量新增约 500 个常用汉字（HSK 5-6、科技、医法、财经、文教、地名姓氏、成语用字等）

import json
import unicodedata
from pathlib import Path
from datetime import datetime, timezone

from glyph_generator import generate_skeleton, structure_of, stroke_count_of


DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-EXPAND-CHINESE-2600-v1.0"

BASE_DIR = Path(__file__).parent.parent
INPUT_PATH = BASE_DIR / "glyphs" / "龍魂字元库_v0012_国际符号版.json"
OUTPUT_PATH = BASE_DIR / "glyphs" / "龍魂字元库_v0013_稳定版.json"

# 约 500 个常用汉字扩展集（HSK 中高级、现代媒体、小说新闻、官方文件、专业领域、成语、衣食住行、自然情感）
EXTRA_CHARS = (
    # HSK 5-6 高频字
    "阿啊唉岸暗案傲奥巴拔罢拜搬板般版扮棒傍胞宝暴爆杯悲背倍贝备辈奔笨逼笔币毕闭辟避编扁便辨辩标表宾冰玻博捕步部猜材财采彩菜参残草测层茶差察厂场唱超朝潮沉陈称趁城诚乘持尺齿虫抽筹仇丑初出除础楚处穿船窗床传创垂纯词辞磁刺粗促存错寸达答打代待袋丹担单但诞弹当挡党刀导岛倒稻德登等滴敌笛底抵地弟典点电店垫钓调跌叠丁盯顶订定丢东冬懂动冻洞斗豆独读堵赌度端短段断堆队对吨蹲盾多夺朵额恶饿恩儿而耳发乏罚法番翻凡烦繁反饭范贩方坊房防仿访纺放飞非肥匪废费分纷粉份丰封蜂锋逢凤夫肤扶幅福府父付负妇附复富腹该改盖概干甘赶敢感刚钢港高稿告哥歌革隔格个各给根跟更耕工公供宫共够构购古谷股故顾固瓜挂怪关官观馆管贯光广规归龟轨鬼贵桂滚国果过哈孩海害寒汗汉航毫号好合何和河荷核盒恨横衡轰红宏洪后厚乎呼忽胡湖虎护花划化话怀坏欢还环缓换皇黄灰挥回会汇绘婚混活火或货获机肌鸡积基激及吉级即极急集籍己计记技际剂季济既继寄加夹佳家甲价驾架嫁简见件建剑健渐江将讲交郊娇角脚较叫接皆街节结姐解介戒界借巾今金津仅紧尽进近京经惊精景警净静境究九久酒旧救就居局举巨具距句绝军君开刊看康抗考靠科棵可克刻客课肯空孔恐口扣苦哭库裤块快宽款况亏困扩拉啦来栏蓝览浪劳老乐雷累冷离礼李里理力历立利例隶连联脸练炼良凉两亮谅辆量辽了料列烈林临淋灵领另流留柳龙楼漏路露旅律虑率绿乱轮论罗落妈马码骂买麦卖脉满慢忙芒毛贸貌么没每美妹门们猛梦迷米秘密蜜眠勉面苗秒妙灭民敏名明命摸模膜末抹母亩木目牧墓拿哪内奶耐男南难脑闹呢能尼你年念娘鸟尿捏您宁牛扭农浓努怒女暖欧派盘判旁胖跑陪配喷朋批皮疲脾片骗飘票贫品平苹凭坡破婆迫扑铺朴期七妻奇骑旗企岂启起气弃汽砌恰千迁牵铅前钱潜浅遣枪墙强抢悄桥切且窃亲侵琴勤秦禽轻倾卿清情晴庆穷丘秋求区曲取去趣全权泉劝缺却确然让绕热人仁忍认任日容肉如入软锐瑞若塞赛三伞散丧扫色杀沙纱傻晒山商上尚少舌蛇社设身深神审甚声生升省盛剩师失诗施十石时实食使始士氏世市示式事势视试适室是收手守首寿受书叔殊梳淑疏舒输孰熟暑数术束树竖恕刷衰双水顺瞬说思丝司私死四似松宋送颂诉素速算随岁孙损缩所索他它她塔台太态坛谈探汤唐堂逃套特疼体替天田填挑条跳贴铁厅听庭停通同统痛偷投头突图徒涂土团推退托脱湾丸玩王网往忘危威微为围唯伟伪尾委卫未位味胃谓温文闻蚊问翁我卧乌污屋无吴五午武舞务物误吸息习席喜戏细系下先仙鲜闲显险县现限线宪陷相香乡享想向项象像消小孝笑效些协胁写泄谢心辛新欣信星刑行形型醒兴性姓凶兄休修秀须虚许序畜续宣玄选穴学雪血寻训压牙亚烟言严岩沿研盐颜眼演厌宴验扬羊阳杨洋养样腰摇遥药要爷野业夜液一衣医依仪宜移遗疑乙已以矣蚁义艺异忆议亦役易疫益谊逸意毅因阴音吟银引饮隐印应英婴鹰迎营影映硬拥永泳勇用优忧尤由邮犹油游有友又幼于予余鱼渔愉雨语玉育郁狱预域欲喻寓御遇元园原员缘远怨院愿曰约月越云运杂再载在咱赞脏早造责择泽贼怎增赠渣扎摘窄债站章张掌涨丈帐招找照赵折哲者这贞真针珍诊阵振镇争征睁正证支枝知织执直值职植止只旨至志制治质致智置稚中忠钟肿种仲众周州舟竹逐主助注驻柱祝著筑抓专转庄装壮状追准桌资仔紫字自宗综总纵走奏足组祖最罪尊昨左作坐座"

    # 科技 / 互联网 / 工程
    "算程控算谱磁芯硅嵌端算阵列拟训推码元变量函库框协融描扫链并发容迁移容器镜像源端口协议栈日志缓存队列负载均衡网关域名防火墙路由带宽延迟吞吐丢包崩溃死锁异常警告指标面板"

    # 医卫 / 健康 / 生物
    "疫疫苗抗体病毒菌炎症状诊疗愈愈康复健护理剂药丸胶囊注射输液手术麻醉放射化疗脉血压糖脂尿酸氧脏腑肠胃肝肾脾肺心脏脑骨肌皮肤神经免疫内分泌遗传基因细胞组织器官"

    # 法律 / 政务 / 国防
    "律宪庭检察裁判决诉辩证供嫌疑逮捕拘留监狱刑罚罚款赔偿调解仲裁合同产权专利商标版权侵权泄露密级保密军衔战略导弹舰机炮雷达边防武警警衔勋章表彰惩戒腐败监察审计"

    # 财经 / 商业 / 管理
    "资债务券基期货汇率利息涨跌杠杆并购融资投标拍卖保险理赔税利润亏损预算出纳账户汇款转账支票信用卡储蓄投资股东董事会上市收购兼并垄断供应链仓储物流采购销售客服"

    # 教育 / 文化 / 学术
    "校院系所科教研室导师博硕学士位论文答辩期刊会议专利引文献综述方法论实验假设证明推导公式定理定律模型变量样本显著偏差置信区间同行评审开放获取"

    # 媒体 / 新闻 / 出版
    "报道采访编辑刊发连载专栏评论社论舆论传播直播弹幕订阅转发热搜爆料绯闻专访纪录片动画配音字幕剪辑特效摄制演播幕后台策划赞助广告收视率票房"

    # 地名 / 行政区划 / 民族
    "京沪深穗成渝杭宁武汉西安长沙郑州济南合肥福州厦门昆明贵阳南宁海口兰州西宁银川乌鲁木齐拉萨呼和浩特哈尔滨长春沈阳石家庄太原南昌台北香港澳门"
    "汉族藏回维吾尔苗彝壮布依朝鲜满侗瑶白土家哈尼哈萨克傣黎傈僳佤畲拉祜水东乡纳西景颇柯尔克孜土达斡尔仫佬羌撒拉毛南仡佬锡伯阿昌普米塔吉克怒乌兹别克俄罗斯鄂温克德昂保安裕固京塔塔尔独龙鄂伦春赫哲门巴珞巴基诺"

    # 常见姓氏
    "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮龚"

    # 成语与文学常用字
    "龍鳳龜麟鹤鹿松柏竹梅兰菊兰荷桂芙蓉牡丹蔷薇杜鹃鹧鸪鸳鸯蟋蟀蝉蛙萤鸥鹭莺燕鸿雁鹃鸠鹏鹰麒麟貔貅饕餮耄耋忈忎忐忑意懒阑珊斑驳阑珊蹉跎忖度氤氲叆叇叵测耄耋饕餮"
    "之乎者也矣焉哉兮夫盖故曰谓云尔其于而与以所者然则乃若虽因为故且既亦莫毋勿弗非无未"

    # 情感 / 心理 / 人际
    "喜怒哀惧爱恨怨悔惭愧羞尴尬惊讶兴奋沮丧焦虑忧郁恐惧孤独寂寞思念牵挂依恋信任依赖崇拜嫉妒羡慕怜悯同情感动激动平静安宁幸福满足失望绝望希望期待"

    # 自然 / 天文 / 地理
    "宇宙银河恒星行星卫星彗星流星黑洞星云星系太阳系地球大陆海洋沙漠森林草原冰川火山地震海啸台风暴雨洪涝干旱霜冻雾霾彩虹霞光雷电潮汐沙滩丘陵峡谷瀑布江河湖泊溪泉"

    # 衣食住行之食物
    "米饭面条馒头包子饺子馄饨汤圆粽子烧饼油条豆浆豆腐蔬菜水果肉类鸡鸭鱼猪牛羊虾蟹贝蛋奶油盐酱醋茶糖辣椒花椒葱姜蒜香料糕点糖果饮料酒水"

    # 衣食住行之服饰
    "衬衫裤子裙子外套风衣西装领带皮鞋靴帽围巾手套袜子内衣睡衣棉衣羽绒服旗袍汉服唐装和服西装领带纽扣拉链口袋袖子领子腰带靴子凉鞋拖鞋"

    # 衣食住行之居住
    "房屋楼公寓别墅庭院花园阳台厨房卧室客厅卫生间书房车库电梯楼梯门窗墙壁屋顶地板家具床桌椅柜沙发冰箱洗衣机空调电视电脑灯窗帘地毯"

    # 交通 / 出行
    "轿车公交车地铁火车高铁飞机轮船自行车摩托车出租车卡车救护车警车消防车校车共享单车电动车滑板轮船潜艇火箭卫星导航站台机场港口公路桥梁隧道渡口"

    # 颜色 / 形态 / 感官
    "红橙黄绿青蓝紫粉棕灰黑白色亮暗深浅浓淡鲜艳柔和粗糙光滑软硬冷热干湿酸甜苦辣咸香臭清脆悦耳刺眼芬芳"

    # 动词 / 抽象动作
    "拿放举抬推拉拖拽撕扯切割敲打捏揉按压抚摸拥抱亲吻挥舞跳跃奔跑行走爬游泳飞翔漂浮沉落站立坐卧躺依靠攀爬追赶逃避躲藏寻找发现选择决定判断比较评价接受拒绝"

    # 数字 / 量词 / 时间
    "零壹贰叁肆伍陆柒捌玖拾百千万亿兆春夏秋冬年月日时分秒早晨中午傍晚夜晚凌晨昨天今天明天去年今年明年世纪年代周旬季度节气"

    # 宗教 / 哲学 / 传统
    "儒释道佛禅祭祀祖宗香烛纸钱符咒占卜风水八卦太极阴阳五行命理轮回因果善恶报应忏悔祈福祝愿祭祀庙宇寺观庵堂"

    # 常见二字词首字补足（可能已在但仍补全高频字）
    "龄尚迈雄雌孕婴幼童青少年壮老年逝婚嫁娶孕产抚养赡养辈份亲戚邻居同事同学朋友伙伴敌人对手领导下属客户用户"
)


def is_cjk_unified_ideograph(char: str) -> bool:
    """确认字符为 CJK Unified Ideograph (U+4E00 ~ U+9FFF)"""
    if len(char) != 1:
        return False
    code = ord(char)
    return 0x4E00 <= code <= 0x9FFF


def load_library(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_extra_charset(existing_chars: set) -> tuple:
    """整理扩展字符，去重、校验、跳过已存在"""
    unique_extra = []
    invalid = []
    duplicates_in_list = []
    already_present = []
    seen = set()

    for char in EXTRA_CHARS:
        if char in (" ", "\n", "\t"):
            continue
        if not is_cjk_unified_ideograph(char):
            invalid.append(char)
            continue
        if char in seen:
            duplicates_in_list.append(char)
            continue
        seen.add(char)
        if char in existing_chars:
            already_present.append(char)
            continue
        unique_extra.append(char)

    return unique_extra, invalid, duplicates_in_list, already_present


def add_glyph_entry(char: str, library: dict) -> None:
    """为单个字符生成字元条目并加入字元库"""
    library["字符集_cnsh9622"][char] = {
        "unicode": f"U+{ord(char):04X}",
        "笔画数": stroke_count_of(char),
        "结构": structure_of(char),
        "风格参数": {
            "力度": 0.8,
            "棱角": 0.3,
            "节奏": 0.6,
            "墨色": 0.9
        },
        "笔画路径_cnsh9622": generate_skeleton(char)
    }


def count_chinese_chars(library: dict) -> int:
    """统计当前字元库中 CJK Unified Ideograph 数量"""
    return sum(
        1 for ch in library["字符集_cnsh9622"].keys()
        if is_cjk_unified_ideograph(ch)
    )


def update_metadata(library: dict, added_count: int, before_total: int, before_chinese: int) -> None:
    """更新字元库元数据与 DNA"""
    after_total = before_total + added_count
    after_chinese = before_chinese + added_count

    meta = library["元数据"]
    meta["版本"] = "v0013-稳定版"
    meta["描述"] = (
        "LonghunFont 两千六百中文字元库 + 实用符号 + 国际符号扩展（拼音调号、希腊字母、数学、天气、音乐、棋牌、占星、UI、警示、上下标数字）"
    )
    meta["总字符数"] = after_total
    meta["中文字符数"] = after_chinese
    meta["中文2600扩展时间"] = datetime.now(timezone.utc).isoformat()
    meta["中文2600扩展DNA"] = DNA
    meta["前一版本"] = "v0012-国际符号版"
    meta["本次新增中文字符数"] = added_count

    library["DNA追溯码"] = DNA


def main():
    print(f"🐉 龍魂字元库中文扩展脚本")
    print(f"   DNA: {DNA}")
    print(f"   输入: {INPUT_PATH}")
    print(f"   输出: {OUTPUT_PATH}\n")

    library = load_library(INPUT_PATH)
    existing_chars = set(library["字符集_cnsh9622"].keys())

    before_total = len(existing_chars)
    before_chinese = count_chinese_chars(library)

    print(f"加载完成：总字符 {before_total}，其中中文 {before_chinese}")

    unique_extra, invalid, duplicates_in_list, already_present = build_extra_charset(existing_chars)

    if invalid:
        print(f"⚠️  跳过非 CJK 字符 {len(invalid)} 个: {''.join(invalid[:20])}{'...' if len(invalid) > 20 else ''}")
    if duplicates_in_list:
        print(f"ℹ️  去重 {len(duplicates_in_list)} 个")
    if already_present:
        print(f"ℹ️  已存在跳过 {len(already_present)} 个")

    print(f"\n准备新增 {len(unique_extra)} 个中文汉字...")

    for char in unique_extra:
        add_glyph_entry(char, library)

    update_metadata(library, len(unique_extra), before_total, before_chinese)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(library, f, ensure_ascii=False, indent=2)

    after_total = len(library["字符集_cnsh9622"])
    after_chinese = count_chinese_chars(library)

    print(f"\n✅ 扩展完成！")
    print(f"   新增汉字: {len(unique_extra)}")
    print(f"   输出文件: {OUTPUT_PATH}")
    print(f"   版本: v0013-稳定版")
    print(f"   总字符数: {before_total} → {after_total}")
    print(f"   中文字符数: {before_chinese} → {after_chinese}")
    print(f"   DNA: {DNA}")


if __name__ == "__main__":
    main()

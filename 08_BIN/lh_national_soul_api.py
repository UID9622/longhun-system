#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·不朽民族魂 API v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-NATIONAL-SOUL-API-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

FastAPI服务 - 不朽·民族魂 数字丰碑后端。
端口: 8778

八大区块:
  GET  /api/timeline          - 时间轴·血色长河 (1931-1945)
  GET  /api/battles           - 战役录·铁血铸剑
  GET  /api/heroes            - 英雄谱·民族脊梁
  GET  /api/slogans           - 标语墙·时代吼声
  GET  /api/evidence          - 铁证馆·国耻勿忘
  GET  /api/humiliation       - 国耻墙·百年伤痕 (1840起)
  GET  /api/today-mirror      - 今日鉴·薪火相传
  POST /api/vows              - 不朽誓言·全民接力 (提交)
  GET  /api/vows              - 不朽誓言·全民接力 (列表)
  GET  /api/stats             - 首页聚合统计
  GET  /api/health            - 健康检查

⚖️ 铭记历史 · 缅怀先烈 · 珍爱和平 · 开创未来
"""

import hashlib
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# 路径设置
_BIN_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_DIR = os.path.dirname(_BIN_DIR)
sys.path.insert(0, _PROJECT_DIR)
sys.path.insert(0, _BIN_DIR)

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="不朽·民族魂 API", version="1.0.0",
              description="龍魂·民族数字丰碑后端服务")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── 数据目录 ───
_DATA_DIR = Path(_PROJECT_DIR) / "portal" / "national-soul" / "data"
_DATA_DIR.mkdir(parents=True, exist_ok=True)
_VOWS_FILE = _DATA_DIR / "vows.json"

# ═══════════════════════════════════════
# 一、时间轴·血色长河 (1931-1945)
# ═══════════════════════════════════════
TIMELINE = [
    {"id":1,"date":"1931-09-18","title":"九一八事变","category":"侵略","summary":"日本关东军炸毁沈阳柳条湖附近南满铁路路轨，反诬中国军队所为，随即炮轰东北军北大营，侵占沈阳。东北沦陷开始。","location":"沈阳","significance":"标志着日本帝国主义侵华战争的开始，也拉开了中国人民抗日战争的序幕","tags":["九一八","东北沦陷","关东军"]},
    {"id":2,"date":"1932-01-28","title":"一·二八事变","category":"战役","summary":"日军进攻上海闸北，国民革命军第十九路军奋起抵抗。激战33天，毙伤日军万余人。","location":"上海","significance":"展现了中国人民反抗侵略的坚定意志","tags":["上海","十九路军","淞沪"]},
    {"id":3,"date":"1932-03-01","title":"伪满洲国成立","category":"侵略","summary":"日本在东北扶植溥仪建立傀儡政权\"伪满洲国\"，对东北实行殖民统治长达14年。","location":"长春","significance":"日本殖民东北的正式标志","tags":["伪满洲国","溥仪","殖民"]},
    {"id":4,"date":"1935-12-09","title":"一二·九运动","category":"民众","summary":"北平大中学生数千人举行抗日救国示威游行，反对华北自治，要求保全中国领土完整，掀起了全国抗日救国新高潮。","location":"北平","significance":"标志着中国人民抗日民主运动新高潮的到来","tags":["学生运动","北平","抗日救亡"]},
    {"id":5,"date":"1936-12-12","title":"西安事变","category":"转折","summary":"张学良、杨虎城在西安扣押蒋介石，逼其停止内战一致抗日。在中共调解下，事变和平解决，促成了抗日民族统一战线的形成。","location":"西安","significance":"成为由国内战争走向抗日民族战争的转折点","tags":["张学良","杨虎城","统一战线"]},
    {"id":6,"date":"1937-07-07","title":"卢沟桥事变（七七事变）","category":"战役","summary":"日军在北平西南卢沟桥附近演习时，借口一名士兵\"失踪\"，要求进入宛平城搜查，遭拒后向中国守军开枪射击并炮轰宛平城。全面抗战爆发。","location":"北平宛平","significance":"标志着中华民族全面抗战的开始","tags":["卢沟桥","全面抗战","宛平"]},
    {"id":7,"date":"1937-08-13","title":"淞沪会战开始","category":"战役","summary":"中日双方在上海展开大规模会战，中国投入约80万兵力，激战三个月，毙伤日军4万余人。粉碎了日本\"三个月灭亡中国\"的狂妄计划。","location":"上海","significance":"粉碎了日军速战速决的企图，为工厂、学校内迁争取了时间","tags":["淞沪会战","上海","三个月灭亡中国"]},
    {"id":8,"date":"1937-09-25","title":"平型关大捷","category":"战役","summary":"八路军115师在山西平型关伏击日军辎重部队，歼敌千余人，毁汽车百余辆。这是全面抗战以来中国军队的第一次大胜仗。","location":"山西平型关","significance":"打破了日军\"不可战胜\"的神话，极大地振奋了全国军民抗战信心","tags":["平型关","八路军","首胜"]},
    {"id":9,"date":"1937-12-13","title":"南京大屠杀","category":"暴行","summary":"日军占领南京后，进行了长达六周的有组织、有计划的大规模屠杀、奸淫、抢劫和纵火。30万以上中国平民和战俘被屠杀，约2万妇女被强奸。","location":"南京","significance":"人类文明史上最黑暗的一页，是中国人民心中永远的伤疤","tags":["南京","大屠杀","30万"]},
    {"id":10,"date":"1938-03-23","title":"台儿庄战役","category":"战役","summary":"中国军队在山东台儿庄地区与日军激战，歼敌万余人。这是抗战以来正面战场取得的最大胜利。","location":"山东台儿庄","significance":"正面战场最重大的胜利之一，极大地鼓舞了全国军民的抗战信心","tags":["台儿庄","正面战场","大捷"]},
    {"id":11,"date":"1938-06-09","title":"花园口决堤","category":"灾难","summary":"为阻止日军西进，国民政府在郑州花园口炸开黄河大堤。虽延缓了日军进攻，但造成河南、安徽、江苏44县受灾，89万人溺死，1,200万人流离失所。","location":"郑州花园口","significance":"以巨大代价换取战略时间","tags":["花园口","黄河","决堤"]},
    {"id":12,"date":"1940-08-20","title":"百团大战","category":"战役","summary":"八路军在华北发动的大规模进攻战役，参战兵力105个团约20万人，毙伤日军2万余人、伪军5千余人，破坏铁路470公里、公路1,500公里。","location":"华北","significance":"八路军在华北地区发动的规模最大、持续时间最长的战役","tags":["百团大战","八路军","彭德怀"]},
    {"id":13,"date":"1941-01-06","title":"皖南事变","category":"内政","summary":"新四军军部及所属部队9,000余人在安徽泾县茂林地区遭国民党军8万余人伏击，军长叶挺被俘，副军长项英遇难。仅2,000余人突围。","location":"安徽泾县","significance":"国共关系严重恶化的标志性事件","tags":["皖南事变","新四军","叶挺"]},
    {"id":14,"date":"1941-12-09","title":"中国正式对日宣战","category":"外交","summary":"珍珠港事变后，国民政府正式对日本宣战，同时宣告对德、意宣战。中国从此成为世界反法西斯同盟的重要成员。","location":"重庆","significance":"中国抗战正式纳入世界反法西斯战争体系","tags":["宣战","反法西斯","同盟"]},
    {"id":15,"date":"1945-08-06","title":"广岛原子弹","category":"国际","summary":"美国在广岛投下原子弹，三天后在长崎投下第二颗。","location":"广岛","significance":"加速了日本的无条件投降","tags":["原子弹","广岛","长崎"]},
    {"id":16,"date":"1945-08-08","title":"苏联对日宣战","category":"国际","summary":"苏联对日宣战，出兵中国东北，迅速击溃日本关东军。","location":"东北","significance":"加速日本投降的最后一击","tags":["苏联","关东军","东北解放"]},
    {"id":17,"date":"1945-08-15","title":"日本宣布无条件投降","category":"胜利","summary":"日本天皇裕仁以广播\"终战诏书\"形式，宣布接受《波茨坦公告》，无条件投降。中国人民抗日战争暨世界反法西斯战争取得最终胜利。","location":"东京","significance":"中国人民14年艰苦卓绝的抗战取得最终胜利","tags":["投降","胜利","终战"]},
    {"id":18,"date":"1945-09-02","title":"日本签署投降书","category":"胜利","summary":"在停泊于东京湾的美国\"密苏里号\"战列舰上，日本外相重光葵和参谋总长梅津美治郎签署投降书。第二次世界大战正式结束。","location":"东京湾","significance":"二战正式结束的标志","tags":["投降书","密苏里号","二战结束"]},
]


# ═══════════════════════════════════════
# 二、战役录·铁血铸剑
# ═══════════════════════════════════════
BATTLES = [
    {"id":1,"name":"淞沪会战","date_range":"1937.8.13 — 1937.11.12","location":"上海","belligerents":"中国军队 vs 日本华中方面军","scale":"中国投入约80万人，日军投入约30万人","result":"毙伤日军4万余人，粉碎\"三个月灭亡中国\"计划","significance":"中国军队以巨大牺牲向世界宣告：中国不会亡！淞沪会战为东南沿海的工厂、学校、机关内迁大后方争取了三个月宝贵时间，保存了民族复兴的火种。","description":"中日双方在抗日战争中的第一场大型会战，也是整个抗日战争中规模最大、战斗最惨烈的一场战役。中国军队以血肉之躯对抗日军海陆空立体火力，平均每天伤亡3,000余人。","tags":["淞沪","三个月灭亡中国","会战"],"severity":"critical","image_hint":"淞沪会战历史照片"},
    {"id":2,"name":"平型关大捷","date_range":"1937.9.25","location":"山西平型关","belligerents":"八路军115师 vs 日军第5师团辎重队","scale":"八路军约1.2万人","result":"歼敌千余人，毁汽车百余辆，缴获大量武器弹药","significance":"打破了\"日军不可战胜\"的神话，提高了共产党和八路军的威望，鼓舞了全国人民抗战胜利的信心。","description":"林彪、聂荣臻指挥八路军115师在平型关东北公路两侧高地设伏。当日军辎重部队进入伏击圈后，八路军居高临下发起猛攻，经过一天激战全歼被围日军。","tags":["平型关","八路军","首胜","林彪"],"severity":"high","image_hint":"平型关战场遗址"},
    {"id":3,"name":"台儿庄战役","date_range":"1938.3.23 — 1938.4.7","location":"山东台儿庄","belligerents":"中国第五战区 vs 日军第10师团","scale":"中国约29万人，日军约5万人","result":"毙伤日军1万余人","significance":"抗战以来正面战场取得的最大胜利，沉重打击了日军的嚣张气焰，极大地鼓舞了全国军民的抗战信心。","description":"李宗仁指挥的台儿庄战役是抗战初期正面战场最辉煌的胜利。在台儿庄城内，中国军队与日军展开逐屋争夺的巷战，尸积如山、血流成河。最终以伤亡3万余人的代价取得胜利。","tags":["台儿庄","李宗仁","大捷"],"severity":"critical","image_hint":"台儿庄战场"},
    {"id":4,"name":"百团大战","date_range":"1940.8.20 — 1941.1","location":"华北（晋察冀、晋冀鲁豫、晋绥）","belligerents":"八路军 vs 日军华北方面军","scale":"八路军105个团约20万人","result":"毙伤日军20,645人、伪军5,155人，破坏铁路474公里、公路1,502公里","significance":"八路军在华北发动的最大规模进攻战役，沉重打击了日军的\"囚笼政策\"，粉碎了日军压缩抗日根据地的企图。","description":"彭德怀指挥百团大战，分三个阶段：交通破袭战、攻坚战、反扫荡。八路军对日军在华北的主要交通线和据点发动全面进攻，\"百团\"之名源于参战部队数量。","tags":["百团大战","彭德怀","华北","破袭战"],"severity":"critical","image_hint":"百团大战纪念碑"},
    {"id":5,"name":"长沙会战","date_range":"1939.9 — 1942.1 (三次会战)","location":"湖南长沙","belligerents":"中国第九战区 vs 日军第11军","scale":"中国投入约30-40万人","result":"三次会战均成功保卫长沙，毙伤日军数万人","significance":"以\"天炉战法\"成功保卫长沙，是正面战场少有的城市保卫战胜利，极大振奋了全国民心。","description":"薛岳指挥的三次长沙会战，创造性地运用\"天炉战法\"——诱敌深入、四面合围。日军虽拥有装备优势，但在中国军民配合下始终无法攻克长沙。","tags":["长沙","薛岳","天炉战法"],"severity":"high","image_hint":"长沙会战"},
    {"id":6,"name":"武汉会战","date_range":"1938.6.11 — 1938.10.27","location":"武汉及长江沿线","belligerents":"中国军队 vs 日本华中派遣军","scale":"中国投入约100万人，日军投入约35万人","result":"毙伤日军10余万人，中国军队损失约40万人","significance":"虽然武汉最终失守，但消耗了日军大量有生力量，抗战进入战略相持阶段。","description":"武汉会战是抗日战争中规模最大、时间最长的会战。中国军队在长江南北两岸600余里的广阔战场上顽强抵抗四个多月，虽最终撤退，但彻底打破了日军速战速决的战略企图。","tags":["武汉","相持阶段","长江"],"severity":"high","image_hint":"武汉会战"},
    {"id":7,"name":"忻口战役","date_range":"1937.10.13 — 1937.11.2","location":"山西忻口","belligerents":"中国第二战区 vs 日军第5师团","scale":"中国约18万人","result":"毙伤日军2万余人，中国军队伤亡约10万人","significance":"抗战初期华北战场规模最大、战斗最激烈的战役。郝梦龄军长等高级将领在前线殉国，以身作则为士兵树立了浴血奋战的榜样。","description":"郝梦龄军长在忻口战役中亲临一线指挥，壮烈殉国前留下名言：\"将有必死之心，士无贪生之念！\"","tags":["忻口","郝梦龄","华北"],"severity":"high","image_hint":"忻口战役遗址"},
    {"id":8,"name":"徐州会战","date_range":"1938.1 — 1938.5","location":"江苏徐州","belligerents":"中国第五战区 vs 日本华北、华中方面军","scale":"中国约60万人","result":"台儿庄大捷后战略撤退","significance":"以空间换时间，成功组织战略撤退，保存了有生力量。","description":"李宗仁在徐州会战中指挥多路部队协同作战，以台儿庄大捷震慑日军，然后果断组织60万大军成功突围，避免被日军合围歼灭。","tags":["徐州","李宗仁","突围"],"severity":"high","image_hint":"徐州会战"},
]


# ═══════════════════════════════════════
# 三、英雄谱·民族脊梁
# ═══════════════════════════════════════
HEROES = [
    {"id":1,"name":"杨靖宇","born":"1905","died":"1940","age_at_death":35,"role":"东北抗日联军第一路军总司令","native":"河南省确山县","deed":"在冰天雪地、弹尽粮绝的极端困境中，孤身与大量日寇周旋战斗数昼夜后壮烈牺牲。日军剖开他的腹部，发现胃里只有草根、树皮和棉絮，没有一粒粮食。","last_words":"\"老乡，我们中国人都投降了，还有中国吗？\"","tags":["东北抗联","草根树皮","孤胆英雄"],"image_hint":"杨靖宇将军照片"},
    {"id":2,"name":"赵一曼","born":"1905","died":"1936","age_at_death":31,"role":"东北抗日联军第三军第二团政委","native":"四川省宜宾县","deed":"在一次战斗中受伤被俘。日军对她施以老虎凳、灌辣椒水、电刑等酷刑，她始终坚贞不屈。日军将她游街示众，她在囚车上高呼\"打倒日本帝国主义！\"后英勇就义。","last_words":"\"我的目的，我的主义，我的信念，就是反满抗日。\"\n给儿子的遗书：\"母亲不用千言万语来教育你，就用实行来教育你。在你长大成人之后，希望不要忘记你的母亲是为国牺牲的。\"","tags":["女英雄","酷刑","革命母亲"],"image_hint":"赵一曼烈士"},
    {"id":3,"name":"左权","born":"1905","died":"1942","age_at_death":37,"role":"八路军副参谋长","native":"湖南省醴陵县","deed":"八路军在抗日战场上牺牲的最高级别将领。1942年5月，日军对太行抗日根据地进行\"铁壁合围\"式大扫荡，左权在山西辽县（今左权县）十字岭指挥部队突围时，被炮弹击中头部壮烈殉国。","last_words":"\"太行浩气传千古，留得清漳吐血花。\"——朱德悼词","tags":["八路军","太行山","高级将领"],"image_hint":"左权将军"},
    {"id":4,"name":"狼牙山五壮士","born":"——","died":"1941","age_at_death":"平均22岁","role":"八路军晋察冀军区第一军分区战士","native":"河北省易县","deed":"马宝玉、葛振林、宋学义、胡德林、胡福才五位战士在狼牙山战斗中，为掩护主力部队和群众转移，将敌人引向棋盘陀绝顶。弹药用尽后，他们用石块还击。面对蜂拥而来的日军，五位战士宁死不屈，纵身跳下数十丈深的悬崖。马宝玉、胡德林、胡福才壮烈殉国，葛振林、宋学义被树枝挂住幸免于难。","last_words":"\"打倒日本帝国主义！\"\"中国共产党万岁！\"——跳崖前的呐喊","tags":["狼牙山","跳崖","群体英雄"],"image_hint":"狼牙山五壮士纪念塔"},
    {"id":5,"name":"张自忠","born":"1891","died":"1940","age_at_death":49,"role":"第33集团军总司令（上将）","native":"山东省临清县","deed":"抗日战争中中国军队牺牲的最高级别将领。在枣宜会战中亲率部队渡河作战，身中数弹仍高呼\"杀敌报国\"，最终壮烈殉国。夫人李敏慧得知噩耗后绝食七日而死。","last_words":"\"国家到了如此地步，除我等为其死，毫无其他办法。更相信，只要我等能本此决心，我等国家及我五千年历史之民族，决不至亡于区区三岛倭奴之手！\"","tags":["上将","殉国","枣宜会战"],"image_hint":"张自忠将军"},
    {"id":6,"name":"成本华","born":"1914","died":"1938","age_at_death":24,"role":"和县抗日人民自卫军女战士","native":"安徽省和县","deed":"在一次战斗中被俘。日军对她施以酷刑，她始终没有吐露任何情报。临刑前，她要求日军记者给她拍一张照片。照片中，她双手交叉抱在胸前，轻蔑地微笑着面对死亡。这张照片成为中国人民不屈精神的象征。","last_words":"（轻蔑地微笑）","tags":["女英雄","微笑赴死","不屈"],"image_hint":"成本华就义照片"},
    {"id":7,"name":"吉鸿昌","born":"1895","died":"1934","age_at_death":39,"role":"察哈尔民众抗日同盟军前敌总指挥","native":"河南省扶沟县","deed":"率部在察哈尔地区与日军激战，收复多伦等地。后被国民党特务逮捕，就义前用树枝在地上写下绝命诗。刑场上，他对刽子手说：\"我为抗日而死，不能跪下挨枪，我死了也不能倒下！给我拿把椅子来！\"坐在椅子上，瞪着眼睛看刽子手开枪。","last_words":"\"恨不抗日死，留作今日羞。国破尚如此，我何惜此头！\"","tags":["抗日同盟","察哈尔","坐着死"],"image_hint":"吉鸿昌"},
    {"id":8,"name":"戴安澜","born":"1904","died":"1942","age_at_death":38,"role":"中国远征军第200师师长（少将）","native":"安徽省无为县","deed":"1942年率中国远征军第200师入缅作战，在同古保卫战中与四倍于己的日军激战12天，毙伤日军5,000余人。后在撤退途中遭日军伏击，身负重伤，于缅北茅邦村壮烈殉国。","last_words":"\"现孤军奋斗，决心全部牺牲，以报国家养育！\"","tags":["远征军","缅甸","同古"],"image_hint":"戴安澜将军"},
]


# ═══════════════════════════════════════
# 四、标语墙·时代吼声
# ═══════════════════════════════════════
SLOGANS = [
    {"id":1,"text":"还我河山","source":"岳飞《满江红》精神传承，抗战时期被广泛书写于各地","context":"1931年九一八事变后，全国各地民众高呼此口号要求收复东北失地。许多抗日将士在出征前将此四字刻在阵地、写在军旗上。","author":"源自岳飞，全民传承","era":"1931-1945","tags":["河山","岳飞","收复"]},
    {"id":2,"text":"宁为战死鬼，不作亡国奴","source":"29军口号","context":"1933年长城抗战期间，守卫喜峰口的国民革命军第29军将士以此自励。1937年七七事变时，29军再次喊出此口号，鼓舞全军拼死抵抗。","author":"29军官兵","era":"1933-1937","tags":["29军","长城抗战","誓死"]},
    {"id":3,"text":"打倒日本帝国主义","source":"全民抗战口号","context":"从1931年到1945年，这是全中国人民喊得最多的一句话。从北平学生到延安群众，从正面战场到敌后根据地，这句话凝聚了四万万中国人的共同意志。","author":"人民","era":"1931-1945","tags":["全民","打倒","帝国主义"]},
    {"id":4,"text":"停止内战，一致抗日","source":"中国共产党提出","context":"1935年《八一宣言》首次公开提出。1936年西安事变后成为全国共识，推动了抗日民族统一战线的正式形成。","author":"中国共产党","era":"1935-1937","tags":["内战","统一战线","西安事变"]},
    {"id":5,"text":"一寸山河一寸血，十万青年十万军","source":"知识青年从军运动口号","context":"1944年，国民政府号召知识青年参军，提出\"一寸山河一寸血，十万青年十万军\"的口号。大批青年学生投笔从戎，组成青年军远征印缅。","author":"国民政府","era":"1944","tags":["青年","学生","远征军"]},
    {"id":6,"text":"战则存，不战则亡","source":"抗战动员","context":"全面抗战爆发后，中国社会各界形成共识：退让就是灭亡，只有全民族抗战才能生存。这句话激励了无数中国人走上战场、投身救亡。","author":"全民共识","era":"1937","tags":["存亡","动员","决心"]},
    {"id":7,"text":"地不分南北，人不分老幼，皆有守土抗战之责","source":"蒋介石庐山讲话","context":"1937年7月17日，蒋介石在庐山发表\"最后关头\"讲话，明确指出全面抗战的国策。这句话成为全民总动员的号角。","author":"蒋介石","era":"1937","tags":["全民动员","庐山","守土"]},
    {"id":8,"text":"把我们的血肉，筑成我们新的长城","source":"《义勇军进行曲》（国歌）","context":"田汉作词、聂耳作曲的《义勇军进行曲》在1935年电影《风云儿女》中首次唱响。这首歌唱出了中国人民以血肉之躯捍卫民族尊严的决心，后成为中华人民共和国国歌。","author":"田汉","era":"1935","tags":["国歌","长城","血肉"]},
    {"id":9,"text":"民兵是胜利之本","source":"毛泽东《论持久战》","context":"1938年5月，毛泽东在延安发表《论持久战》，系统阐述了抗战的战略方针。这句话揭示了人民战争的核心思想：战争的伟力之最深厚的根源，存在于民众之中。","author":"毛泽东","era":"1938","tags":["论持久战","人民战争","民兵"]},
    {"id":10,"text":"最后胜利一定是我们的","source":"八路军、新四军常用口号","context":"在最艰难的反扫荡时期、在最黑暗的1941-1942年，这句话支撑着根据地军民坚持抗战。它不仅是口号，更是一种坚定不移的信念。","author":"全军","era":"1937-1945","tags":["信念","胜利","坚持"]},
]


# ═══════════════════════════════════════
# 五、铁证馆·国耻勿忘
# ═══════════════════════════════════════
EVIDENCE = [
    {"id":1,"title":"南京大屠杀","date":"1937.12.13 — 1938.1","location":"南京","type":"大规模屠杀","victims":"30万人以上","description":"日军占领南京后，进行了长达六周的有组织、有计划的大规模屠杀、奸淫、抢劫和纵火。据远东国际军事法庭判定：在日军占领后的最初六个星期内，南京及附近地区被屠杀的平民和战俘达20万以上（不含被日军焚烧和抛入江中的尸体）。中国方面统计遇难人数在30万人以上。","methods":["集体枪杀","活埋","焚烧","刀刺","水溺","奸杀"],"sources":["《远东国际军事法庭判决书》","《拉贝日记》","《魏特琳日记》","《南京大屠杀史料集》","东京审判档案"],"evidence_count":458,"tags":["南京","大屠杀","30万","铁证"],"severity":"critical"},
    {"id":2,"title":"731部队·细菌战","date":"1936 — 1945","location":"哈尔滨平房区","type":"生物武器·人体实验","victims":"至少3,000人在实验中死亡，细菌战造成数十万中国平民死亡","description":"日本关东军731部队在哈尔滨等地设立细菌战研究基地，对活人进行鼠疫、霍乱、炭疽、冻伤、毒气等惨无人道的实验。被实验者被称为\"马路大\"（日语\"圆木\"），在完全清醒的状态下被活体解剖。战后，美国为获取实验数据，秘密豁免了731部队负责人的战争罪责。","methods":["活体解剖","鼠疫感染","炭疽实验","冻伤实验","毒气实验","细菌弹投放"],"sources":["森村诚一《恶魔的饱食》","731部队遗址","美国国家档案馆解密文件","哈巴罗夫斯克审判档案"],"evidence_count":217,"tags":["731","细菌战","人体实验","活体解剖"],"severity":"critical"},
    {"id":3,"title":"慰安妇制度","date":"1932 — 1945","location":"中国、朝鲜半岛、东南亚等日军占领区","type":"性奴隶制度","victims":"约20万中国和朝鲜妇女","description":"日本军队在占领区强迫大量妇女充当\"慰安妇\"（性奴隶），这是人类历史上规模最大的、有组织的性暴力犯罪。大多数受害妇女在战争结束前被杀害或因疾病、虐待死亡。幸存者在战后几十年因羞耻和恐惧而沉默，直到1990年代才开始打破沉默。","methods":["强迫","绑架","欺骗","性暴力","监禁"],"sources":["幸存者证言","日本政府\"河野谈话\"（1993）","联合国调查报告","《二十二》纪录片"],"evidence_count":189,"tags":["慰安妇","性暴力","妇女","人权"],"severity":"critical"},
    {"id":4,"title":"重庆大轰炸","date":"1938.2 — 1943.8","location":"重庆","type":"战略轰炸","victims":"平民伤亡约2.4万人","description":"日军对重庆进行了长达5年半的无差别战略轰炸，出动飞机9,000余架次，投弹2万余枚。最为惨烈的\"六五大隧道窒息惨案\"中，近万避难民众因缺氧和踩踏死亡。日军轰炸目标明确包括平民居住区、医院、学校等非军事目标。","methods":["无差别轰炸","燃烧弹","隧道窒息"],"sources":["重庆大轰炸遗址","《重庆大轰炸档案》","幸存者证言","国际联盟调查报告"],"evidence_count":276,"tags":["重庆","轰炸","隧道","平民"],"severity":"high"},
    {"id":5,"title":"三光政策","date":"1941 — 1942","location":"华北抗日根据地","type":"焦土扫荡","victims":"数百万平民","description":"日军在华北抗日根据地的扫荡中实行'杀光、烧光、抢光'的\"三光政策\"。据不完全统计，仅1941-1942年，日军在华北制造的惨案就有1,300多起，杀害民众约35万人。整个华北抗日根据地人口从1亿锐减至5,000万。","methods":["屠杀","烧村","抢掠","强奸","强征劳工"],"sources":["《华北治安战》（日本防卫厅）","晋察冀根据地档案","幸存者调查记录","根据地方志"],"evidence_count":312,"tags":["三光","扫荡","华北","根据地"],"severity":"critical"},
    {"id":6,"title":"强征劳工","date":"1937 — 1945","location":"日本及中国沦陷区","type":"强制劳动","victims":"约4万中国劳工被强征到日本，近7,000人客死异乡","description":"日本政府和企业强征大量中国劳工到日本本土、中国东北、东南亚等地从事矿山、军工、建筑等高强度体力劳动。劳工在恶劣环境中遭受非人待遇，大量死于饥饿、疾病、虐待和事故。战后数十年来，幸存劳工及遗属持续追讨赔偿。","methods":["抓捕","欺骗","强制押送","监禁","高强度劳动","虐待"],"sources":["日本外务省报告书","《花冈事件》","幸存者证言","三菱综合材料公司和解文件（2016）"],"evidence_count":156,"tags":["劳工","强征","日本","奴役"],"severity":"high"},
]


# ═══════════════════════════════════════
# 六、国耻墙·百年伤痕 (1840起)
# ═══════════════════════════════════════
HUMILIATION = [
    {"id":1,"year":"1840-1842","event":"第一次鸦片战争","treaty":"《南京条约》（1842）","terms":"割让香港岛；开放广州、厦门、福州、宁波、上海五口通商；赔款2,100万银元；协定关税","impact":"中国开始沦为半殖民地半封建社会。这是近代中国第一个不平等条约，也是百年国耻的开端。","tags":["鸦片","香港","半殖民地"]},
    {"id":2,"year":"1856-1860","event":"第二次鸦片战争","treaty":"《天津条约》（1858）、《北京条约》（1860）","terms":"外国公使进驻北京；增开11个通商口岸；允许传教士进入内地；割让九龙半岛；赔款1,600万两白银","impact":"英法联军焚毁圆明园。中国半殖民地程度进一步加深。","tags":["圆明园","英法联军","九龙"]},
    {"id":3,"year":"1894-1895","event":"甲午中日战争","treaty":"《马关条约》（1895）","terms":"中国承认朝鲜\"独立\"（实为日本控制）；割让台湾、澎湖列岛、辽东半岛给日本（后以3,000万两白银赎回辽东半岛）；赔款2亿两白银；开放沙市、重庆、苏州、杭州为通商口岸","impact":"2亿两白银相当于日本4年的财政收入。日本用这笔钱加速工业化，跻身列强行列。台湾自此被日本殖民统治50年（1895-1945）。","tags":["甲午","马关条约","台湾","辽东"]},
    {"id":4,"year":"1900","event":"八国联军侵华","treaty":"《辛丑条约》（1901）","terms":"赔款4.5亿两白银（按中国当时4.5亿人口每人一两），分39年还清本息共9.8亿两；拆毁大沽炮台；允许各国驻兵北京至山海关沿线；划定东交民巷为使馆区","impact":"赔款数额之巨、条件之苛刻为历史上空前。条约签订后，中国完全沦为半殖民地半封建社会。慈禧太后\"量中华之物力，结与国之欢心\"成为千古耻辱。","tags":["庚子赔款","八国联军","东交民巷","慈禧"]},
    {"id":5,"year":"1904-1905","event":"日俄战争在中国土地上打仗","treaty":"《朴茨茅斯条约》（1905）","terms":"日俄两国在中国领土上交战，中国却被迫\"保持中立\"。战后俄国将旅顺、大连租借权和南满铁路转让给日本","impact":"两个帝国在中国土地上打仗，争的是中国领土的权益，而清政府只能\"中立\"旁观——这是国家主权丧尽的极致表现。","tags":["日俄战争","旅顺","中立","丧权"]},
    {"id":6,"year":"1915","event":"\"二十一条\"","treaty":"《中日民四条约》","terms":"日本向北洋政府提出旨在灭亡中国的\"二十一条\"，内容包括：继承德国在山东的全部权益；延长旅顺大连租期至99年；中国政府在政治、财政、军事等方面须聘用日本顾问；中国警察由中日合办；中国军队须向日本购买武器等","impact":"袁世凯为换取日本对其称帝的支持，接受了其中大部分条款。消息传出，全国愤怒，掀起了大规模反日爱国运动。","tags":["二十一条","袁世凯","北洋政府","亡国"]},
    {"id":7,"year":"1931","event":"九一八事变","treaty":"—（未签条约，直接军事占领）","terms":"日军侵占东北三省，面积相当于日本本土的三倍。国际联盟派李顿调查团调查，虽认定日本为侵略者，但未采取任何实质措施。","impact":"东北3,000万同胞开始了14年的亡国奴生活。大量战略资源被日本掠夺，成为其侵略全中国和发动太平洋战争的物质基础。","tags":["九一八","东北","国际联盟","蒋介石不抵抗"]},
    {"id":8,"year":"1937","event":"全面侵华战争爆发","treaty":"—","terms":"日军发动全面侵华战争，占领了中国最富庶的东部和中部地区。","impact":"八年全面抗战（1937-1945），加上1931年以来的局部抗战，共计14年。中国军民伤亡3,500万人以上，直接经济损失1,000亿美元，间接经济损失5,000亿美元。","tags":["全面抗战","卢沟桥","3500万"]},
]


# ═══════════════════════════════════════
# 七、今日鉴·薪火相传
# ═══════════════════════════════════════
TODAY_MIRROR = [
    {"id":1,"pair":"山河在 → 山河壮","historical":"1937年，山河破碎。\"华北之大，已经安放不下一张平静的书桌了。\"","today":"今天，我们拥有世界最长的高铁网络、最完整的工业体系、自主研发的空间站。\"这盛世，如您所愿。\"","keywords":["山河","高铁","工业","空间站"],"image_hint":"历史地图 vs 现代成就"},
    {"id":2,"pair":"卢沟桥的石狮 → 泸定桥的路灯","historical":"1937年7月7日，卢沟桥的狮子见证了日军的第一枪。","today":"大渡河上的泸定桥旁立起了一盏盏路灯，还贴着\"有事找党员\"的牌子。从飞夺泸定桥到廊桥路灯，枪林弹雨变成了万家灯火。","keywords":["卢沟桥","泸定桥","党员","传承"],"image_hint":"卢沟桥 vs 泸定桥"},
    {"id":3,"pair":"技术封锁 → 自主突破","historical":"1840年以来，列强以\"坚船利炮\"轰开国门，用技术优势实施殖民掠夺。","today":"华为在被全球最严厉封锁下，三年内完成13,000多颗元器件国产替代。C919大飞机打破波音空客垄断。\"封锁吧，封锁十年八年，中国的一切问题都解决了。\"","keywords":["华为","C919","封锁","突破"],"image_hint":"坚船利炮 vs 国产大飞机"},
    {"id":4,"pair":"\"东亚病夫\" → 体育强国","historical":"近代中国被蔑称为\"东亚病夫\"——不仅是身体素质的羞辱，更是民族尊严的践踏。","today":"从许海峰1984年射落第一金，到北京双奥之城。中国人不再是\"病夫\"，而是在太空奔跑的民族。","keywords":["东亚病夫","奥运","体育","金牌"],"image_hint":"历史漫画 vs 奥运金牌"},
    {"id":5,"pair":"赔款白银 → 人类命运共同体","historical":"《辛丑条约》赔款4.5亿两白银，\"量中华之物力，结与国之欢心\"。","today":"中国提出的\"人类命运共同体\"理念被写入联合国决议。从被瓜分到共建，从赔款到援建。\"我们不是在做世界的老大，我们是在做世界的大哥。\"","keywords":["赔款","共同体","联合国","援建"],"image_hint":"条约书 vs 联合国"},
    {"id":6,"pair":"\"三个月灭亡中国\" → 不可战胜","historical":"1937年，日本叫嚣\"三个月灭亡中国\"。","today":"今天的中国，拥有世界上最强大的陆军、亚洲最强大的海军、世界第二的空军。我们不侵略，但任何侵略者都将面对14亿人的钢铁长城。","keywords":["灭亡中国","解放军","国防","自信"],"image_hint":"日军海报 vs 国庆阅兵"},
    {"id":7,"pair":"流亡学生 → 教育大国","historical":"抗战时期，北大、清华、南开三校内迁云南昆明，组建西南联合大学。师生们跋涉数千里，在茅草房里上课。","today":"中国拥有世界最大规模的高等教育体系，每年培养近千万大学毕业生。从茅草房到一流大学，知识的火种从未熄灭。","keywords":["西南联大","教育","大学","传承"],"image_hint":"西南联大 vs 现代大学"},
    {"id":8,"pair":"饥荒与苦难 → 粮食安全","historical":"抗战时期，饿殍遍野。花园口决堤、大面积沦陷、封锁禁运——吃不饱是常态。","today":"中国用全球7%的耕地养活了22%的人口。袁隆平的杂交水稻让中国人端稳了自己的饭碗。\"手中有粮，心中不慌。\"","keywords":["粮食","袁隆平","杂交水稻","吃饭"],"image_hint":"饥荒照片 vs 丰收场景"},
]


# ═══════════════════════════════════════
# 八、不朽誓言·全民接力
# ═══════════════════════════════════════
class VowSubmit(BaseModel):
    name: str
    location: str
    message: str


def _load_vows() -> List[Dict]:
    if _VOWS_FILE.exists():
        try:
            vows = json.loads(_VOWS_FILE.read_text())
            # 只保留最新的200条
            if len(vows) > 500:
                vows = vows[-200:]
            return vows
        except Exception:
            pass
    # 初始誓言
    default = [
        {"id":"init-1","name":"诸葛鑫","location":"济南","message":"退役不褪色。我是退伍军人，若有战、召必回。强国有我！","created_at":"2025-07-25T00:00:00","approved":True},
        {"id":"init-2","name":"一个普通大学生","location":"南京","message":"在南京读书四年，每次经过大屠杀纪念馆都想哭。先辈们用命换来今天，我不能浪费。好好学习，报效祖国。","created_at":"2025-07-25T00:00:00","approved":True},
        {"id":"init-3","name":"海外游子","location":"美国·硅谷","message":"在海外十年了，越远越爱国。每次看到有人诋毁中国，我都要站出来说清楚：你们不了解这个民族经历了什么。我不会忘记，永远。" ,"created_at":"2025-07-25T00:00:00","approved":True},
    ]
    _VOWS_FILE.write_text(json.dumps(default, ensure_ascii=False, indent=2))
    return default


def _save_vows(vows: List[Dict]):
    _VOWS_FILE.write_text(json.dumps(vows, ensure_ascii=False, indent=2))


# ═══════════════════════════════════════
# API 端点
# ═══════════════════════════════════════

@app.get("/api/health")
async def health():
    return {"status":"ok","service":"不朽·民族魂 API","version":"1.0.0","timestamp":datetime.now(timezone.utc).isoformat()}


# --- 时间轴 ---
@app.get("/api/timeline")
async def get_timeline(year: Optional[str]=None, category: Optional[str]=None):
    data = TIMELINE
    if year: data = [d for d in data if d["date"].startswith(year)]
    if category: data = [d for d in data if d["category"]==category]
    return {"total":len(data),"events":sorted(data,key=lambda x:x["date"])}


# --- 战役录 ---
@app.get("/api/battles")
async def get_battles(year: Optional[str]=None, severity: Optional[str]=None, search: Optional[str]=None):
    data = BATTLES
    if year: data = [d for d in data if year in d["date_range"]]
    if severity: data = [d for d in data if d["severity"]==severity]
    if search: data = [d for d in data if search in d["name"] or search in d["description"]]
    return {"total":len(data),"battles":data}


# --- 英雄谱 ---
@app.get("/api/heroes")
async def get_heroes(search: Optional[str]=None, tag: Optional[str]=None):
    data = HEROES
    if search: data = [d for d in data if search in d["name"] or search in d["deed"]]
    if tag: data = [d for d in data if tag in d["tags"]]
    return {"total":len(data),"heroes":data}


# --- 标语墙 ---
@app.get("/api/slogans")
async def get_slogans(era: Optional[str]=None):
    data = SLOGANS
    if era: data = [d for d in data if era in d["era"]]
    return {"total":len(data),"slogans":data}


# --- 铁证馆 ---
@app.get("/api/evidence")
async def get_evidence(stype: Optional[str]=None, severity: Optional[str]=None):
    data = EVIDENCE
    if stype: data = [d for d in data if d["type"]==stype]
    if severity: data = [d for d in data if d["severity"]==severity]
    return {"total":len(data),"evidence":data}


# --- 国耻墙 ---
@app.get("/api/humiliation")
async def get_humiliation():
    return {"total":len(HUMILIATION),"treaties":sorted(HUMILIATION,key=lambda x:x["year"])}


# --- 今日鉴 ---
@app.get("/api/today-mirror")
async def get_today_mirror():
    return {"total":len(TODAY_MIRROR),"pairs":TODAY_MIRROR}


# --- 不朽誓言 ---
@app.get("/api/vows")
async def get_vows(page: int=1, page_size: int=50):
    vows = _load_vows()
    approved = [v for v in vows if v.get("approved",True)]
    total = len(approved)
    start = (page-1)*page_size
    items = approved[::-1][start:start+page_size]  # 最新在前
    return {"total":total,"page":page,"page_size":page_size,"vows":items}


@app.post("/api/vows")
async def submit_vow(req: VowSubmit):
    if not req.name.strip() or not req.message.strip():
        raise HTTPException(status_code=400, detail="请填写姓名和誓言")
    if len(req.message) > 200:
        raise HTTPException(status_code=400, detail="誓言请控制在200字以内")
    
    vows = _load_vows()
    new_vow = {
        "id": uuid.uuid4().hex[:8],
        "name": req.name.strip(),
        "location": req.location.strip() or "未知",
        "message": req.message.strip(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "approved": True,  # 先放行，后续可加审核
    }
    vows.append(new_vow)
    _save_vows(vows)
    
    return {
        "status":"published",
        "vow":new_vow,
        "total_vows":len([v for v in vows if v.get("approved",True)]),
        "message":"你的誓言已铭刻在民族魂丰碑之上。薪火相传，强国有我！"
    }


# --- 首页聚合 ---
@app.get("/api/stats")
async def get_stats():
    vows = _load_vows()
    approved = [v for v in vows if v.get("approved",True)]
    return {
        "timeline_events": len(TIMELINE),
        "battles": len(BATTLES),
        "heroes": len(HEROES),
        "slogans": len(SLOGANS),
        "evidence_cases": len(EVIDENCE),
        "humiliation_treaties": len(HUMILIATION),
        "today_mirrors": len(TODAY_MIRROR),
        "vows": len(approved),
        "total_victims_ww2": 35000000,
        "war_years": "1931-1945 (14年)",
        "heroic_quote": "\"宁为战死鬼，不作亡国奴\"",
        "daily_hero": HEROES[4],  # 张自忠
        "daily_slogan": SLOGANS[0],  # 还我河山
    }


# ─── 直接启动 ───
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8780))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

# 研究简报：光刻机（EUV/DUV）技术原理与关键参数

> 调研员报告 | 资料收集时间：2026年（各来源时间已在引用处标注）
> 说明：所有关键数据均标注来源URL；无法核实或存在争议的信息明确标注。

---

## 1. 光刻分辨率公式与波长演进

### 1.1 瑞利（Rayleigh）判据与 R = k1·λ/NA

光刻是将掩膜版上的电路图形经投影光学系统（通常4:1缩小）转移到涂有光刻胶的晶圆上。由于透镜孔径有限，点光源成像为"艾里斑"（衍射斑），可区分两个光斑的最小距离即为分辨率极限，由瑞利判据给出：

**R（或CD）= k1 · λ / NA**

- **λ**：曝光光源波长。波长越短，空间频率越高，分辨率越高。
- **NA（数值孔径）= n·sinα**：n 为像方介质折射率，α 为物镜半孔径角。空气/真空中 n=1；ArF浸没式在镜头与晶圆间注入超纯水（n≈1.44），NA从干式0.93提升至1.35，等效波长 193/1.44≈134nm。
- **k1（工艺因子）**：综合光照条件、光刻胶特性、分辨率增强技术（RET）的经验系数。**单次曝光 k1 的物理理论极限为 0.25**（ASML观点）。通过相移掩模（PSM）、离轴照明（OAI）、光学邻近效应修正（OPC）、多重曝光等技术可逼近甚至等效突破该极限。
- 配套公式**焦深 DOF = k2·λ/NA²**：NA增大时焦深急剧缩小，需与分辨率折中。

来源：
- 虎嗅《全球光刻机技术演进与ASML的垄断地位分析》(2026-03) https://www.huxiu.com/article/4841611.html
- 与非网 https://www.eefocus.com/article/2053266.html
- 百度百科"光刻分辨率" https://baike.baidu.com/item/光刻分辨率/24191184
- CSDN工程力学词条（含DOF公式）https://blog.csdn.net/weixin_49199313/article/details/160111672

### 1.2 波长演进表

| 代际 | 光源 | 波长 | 设备类型 | 典型制程节点 |
|---|---|---|---|---|
| 第一代 | g线（汞灯） | 436nm | 接触式/接近式 | 0.5μm以上 |
| 第二代 | i线（汞灯） | 365nm | 接触/接近/步进 | 0.8–0.25μm |
| 第三代 | KrF准分子激光 | 248nm | 扫描投影式 | 180–130nm |
| 第四代 | ArF准分子激光（干式/浸没式） | 193nm（浸没等效134nm） | 步进扫描/浸没式 | 130–7nm（配合多重曝光） |
| 第五代 | EUV（LPP锡等离子体） | 13.5nm | 极紫外反射式 | 7nm及以下 |

来源：芯源微公告（上交所审核问询回复，2021）http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?stockid=688037&id=7669404 ；36氪《超越EUV光刻》(2025-09-17) https://36kr.com/p/3471595973891712

典型机型参数对照（分辨率按k1≈0.3附近估算，来源给出值）：

| 技术 | 波长 | NA | 分辨率 | 适用节点 |
|---|---|---|---|---|
| KrF DUV | 248nm | 0.60 | ~130nm | 130–65nm |
| ArF浸没式 | 193nm | 1.35 | ~38nm（单次） | 28–7nm |
| EUV (0.33 NA) | 13.5nm | 0.33 | ~13nm | 7–3nm |
| High-NA EUV (0.55 NA) | 13.5nm | 0.55 | ~8nm | ≤2nm |

来源：半导体制造工艺研究报告 https://mp.weixin.qq.com/s?__biz=Mzg5MTU0NTgyOA==&mid=2247483749&idx=1&sn=b1331cbbbaa84c101bb21b3f0f755930 ；ASML/媒体数据 https://meishijournal.com/europe-semiconductor-chips-act-2026/

---

## 2. EUV光刻机工作原理与ASML机型参数

### 2.1 工作原理

1. **LPP（激光产生等离子体）锡滴光源**：真空中锡滴发生器以约每秒5万–10万滴的速度喷射熔融锡滴，用通快（TRUMPF）约30kW的CO₂激光（10.6μm）轰击（现代系统采用预脉冲+主脉冲双脉冲塑形），锡被加热成比太阳表面更热的等离子体，辐射13.5nm EUV光。能量转换效率仅约2–4%。光源功率从2015年约100W提升至当前量产机500–600W；2026年2月ASML宣布实现1000W突破（锡滴频率翻倍至约10万/秒），并称有路径达1500–2000W，2030年产能有望提升50%（至约330wph）。
   - 来源：MIT科技评论中国 (2026-02-23) https://www.mittrchina.com/news/detail/15971 ；IT之家 (2026-02-23) https://www.ithome.com/0/923/005.htm ；腾讯开发者 (2024-08) https://developer.cloud.tencent.com.cn/article/2444565 ；知乎/长春光机所专栏（NXE:3600D配250W、NXE:3800E约300W、EXE:5000目标500W）https://zhuanlan.zhihu.com/p/1897942331476377760

2. **多层反射镜光学**：13.5nm光被几乎所有材料（包括透镜玻璃和空气）吸收，因此整机必须使用**反射镜**而非透镜——采用Mo/Si（钼/硅）多层膜布拉格反射镜，蔡司制造，单镜反射率约70%（约71%）。光线经10余面反射镜后到达晶圆的能量仅剩百分之几。
   - 来源：虎嗅 https://www.huxiu.com/article/4841611.html ；ASML技术分析 https://mp.weixin.qq.com/s?__biz=MzAxMTgwMzU4NA==&mid=2247566388&idx=1&sn=351ab5ba6b8252f6974a7c3c9e10d2f7

3. **真空系统**：空气吸收EUV并影响折射率，整个光路腔体必须保持真空，锡碎片清理、镜面污染控制是主要工程挑战。
   - 来源：虎嗅 https://www.huxiu.com/article/4841611.html

### 2.2 ASML主要机型参数

| 机型 | NA | 产能 (wph) | 套刻精度 | 价格 | 备注 |
|---|---|---|---|---|---|
| NXE:3600D | 0.33 | ~160（@30mJ/cm²） | 1.1nm（matched machine） | >1.5亿美元（报道） | 台积电3nm主力 |
| NXE:3800E | 0.33 | 初期195，目标/实测220+ | 0.9nm（matched） | ~1.8亿美元（报道） | 2023Q4起出货，吞吐提升30%+ |
| EXE:5000 | 0.55 | 研发机型 | — | ~2.5亿欧元 | 2023.12首台交付英特尔 |
| EXE:5200/5200B | 0.55 | >200；5200B为175–200 | — | >3.5亿欧元（约4亿美元，5200B约3.5–4亿美元） | 量产型High-NA，分辨率~8nm |

来源：
- Bits&Chips (2024-03-19，overlay 0.9/1.1nm、220wph) https://bits-chips.com/article/asmls-high-na-euv-technology-is-seeping-into-low-na-tools/
- 腾讯/电子发烧友 (2024-03) https://news.qq.com/rain/a/20240314A0941G00
- c114 (2024-10-17，High-NA约3.5亿美元 vs 标准1.8–2亿美元) https://m.c114.com.cn/w51-1275793.html
- 新浪/首台High-NA交货 (2023-12-22，EXE:5200定价约2.5亿欧元，5200B超3.5亿欧元) https://t.cj.sina.cn/articles/view/3856710564/e5e0bba401901j0m0
- 观察者网 (2026-04-23，>3.5亿欧元/台) https://www.guancha.cn/internation/2026_04_23_814717.shtml

---

## 3. DUV + 多重曝光路线

### 3.1 主要技术

- **LELE（Litho-Etch-Litho-Etch）**：将高密度图形拆到2张低密度掩膜版，两次曝光+两次刻蚀，等效分辨率×2。设计灵活但两次曝光间存在套刻（overlay）误差，成本高。扩展到LELELE（三重）等。台积电初代7nm即用193i+多重曝光量产。
- **SADP（自对准双重成像）**：①光刻定义心轴（mandrel）→ ②共形沉积spacer薄膜（如SiO₂，ALD控制厚度）→ ③各向异性刻蚀只留侧壁spacer → ④去除心轴，spacer作掩膜，图形密度自动×2。最终线宽由**薄膜沉积厚度**决定而非对准精度，故"自对准"、overlay敏感度低，但只适合规则线条图形（Fin、金属线）。
- **SAQP（自对准四重成像）**：对SADP再做一轮spacer（spacer-on-spacer），密度×4。14/10nm节点Fin与金属层主力；中芯国际以ArF浸没式DUV+SADP/SAQP实现7nm等效量产。

来源：
- 优半导体 https://uedu.tw/semiconductor/a/multi-patterning
- 搜狐《多重曝光技术》(2026-03) https://www.sohu.com/a/1000716422_122473145
- 未来智库半导体产业链报告 (2025-02) https://www.vzkoo.com/read/202502188b05d855003afcfc43c1486a55.html
- 知乎光刻工艺专栏 https://zhuanlan.zhihu.com/p/1950953004665635370

### 3.2 套刻（overlay）误差与成本

- **overlay定义**：当前光刻层与前层图形的对准偏差。先进节点要求亚纳米级：NXE:3800E matched-machine overlay 0.9nm；硅片每升温1℃，300mm晶圆膨胀约2.5nm；ASML报告称overlay超过设计值20%时良率可降50%以上。
  - 来源：https://b2bwiki.baidu.com/article/d0r813pftjstjkqndv8g ；Bits&Chips同上。
- **成本增幅估算**（公开报道口径，非精确模型）：
  - 光刻胶用量为单次曝光的2–4倍；中芯7nm DUV路线光刻胶消耗增加约60%；
  - SAQP的沉积/刻蚀步骤使电子气体用量约增至5倍；CMP步骤7nm约30步（28nm约9–10步）；
  - DUV多重曝光等效7nm相对EUV单次曝光：工序时间长50%以上、单位成本高50%以上、良率显著更低（初期良率报道仅20–50%）。
  - 来源：微信公众号AI服务器报告 https://mp.weixin.qq.com/s/c_F-TjQA3MieKczHJs2Wfg ；写给投资者的半导体产业链 https://socratopia.app/library/industrychain-semiconductor-zh/chapter-9 ；头条SAQP报道（工序时间为EUV的3–5倍）https://www.toutiao.com/w/1828041759782019/

---

## 4. 中国光刻机进展（以公开信息为准）

- **SMEE（上海微电子）**：SSA600/20系列（ArF干式）是国内唯一量产前道光刻机，分辨率90nm；截至2025年SSX600系列占国内光刻机市场份额超80%（成熟制程）。
  - 来源：新浪财经/21世纪经济报道 (2026-05-19) https://finance.sina.com.cn/roll/2026-05-19/doc-inhykxft7619519.shtml
- **28nm ArF浸没式（SSA800系列）**：处于样机组装测试/客户验证阶段。**注意信息矛盾**：部分媒体（2026-01东方财富转载）称"已完成多轮工艺验证、套刻精度优于2.5nm、2025年进入批量交付"；但2026-05-19《21世纪经济报道》核实"28nm浸没式光刻机首批交付且良率90–95%"为**不实传闻**，设备仍在调试。本简报以较严谨的核实报道为准：**截至2026年中，SMEE 28nm浸没式光刻机尚未确认量产交付**。
  - 来源：https://finance.sina.com.cn/roll/2026-05-19/doc-inhykxft7619519.shtml ；对照 https://wap.eastmoney.com/a/202601083612783491.html
- **国产化率**：2024年国内光刻机市场规模超400亿元，国产化率仅约2.5%（中信证券/SEMI）；2023年进口光刻机225台、87.54亿美元。
  - 来源：智研咨询 (2025-01) https://m.chyxx.com/industry/1208341.html
- **子系统**：科益虹源193nm ArF准分子激光器已出货（60W/4–6kHz）；国望光学承担28nm ArF浸没式曝光光学系统研发；华卓精科干式双工件台已对SMEE出货，浸没式双工件台在研。
  - 来源：民生证券光刻机深度报告 https://pdf.dfcfw.com/pdf/H3_AP202309081598093079_1.pdf ；微信光刻技术解析 https://mp.weixin.qq.com/s?__biz=Mzg5MjAxMDcxNw==&mid=2247792304&idx=1&sn=644f326557af50392888ef7b937aeadd
- **工信部目录**：《首台（套）重大技术装备推广应用指导目录（2024年版）》披露氟化氩光刻机分辨率≤65nm、套刻≤8nm。
  - 来源：https://m.chyxx.com/industry/1208341.html
- **EUV**：国内EUV整机**未公开**；中科院上海光机所LPP路线报道转换效率3.42%，哈工大DPP、清华SSMB路线在推进（媒体口径，未获官方量产确认）。

---

## 5. 光刻胶与掩膜版

### 5.1 化学放大胶（CAR）原理

- 传统DNQ/酚醛胶"一个光子一次反应"，量子效率低，无法满足KrF/ArF短波长光源低光子通量需求。
- **CAR机制**：光刻胶由主体树脂 + **光致产酸剂（PAG，如三芳基硫鎓盐、二芳基碘鎓盐）** + 碱淬灭剂 + 溶剂组成。曝光时PAG吸光分解产生强酸（"酸潜像"）；**后烘（PEB）**时酸催化树脂脱保护反应（如t-BOC脱除生成羧基，亲水性改变）或交联/主链断裂，改变显影溶解性。**酸不被消耗、可链式催化数百至上千次反应**（催化链长CCL可达800–1000），灵敏度提升10倍以上。
- 代价：酸扩散（典型扩散长度10–20nm）限制分辨率并影响LER（线边缘粗糙度）；EUV光子稀少带来随机性缺陷（stochastic defects）问题。
- **EUV胶**：13.5nm光子数少（同功率下约为ArF的1/10），需减少高吸收元素、提高C/H比；主流为CAR改进型与金属氧化物胶（metal-oxide resist）。目标指标：分辨率<13nm半周期、LER<2nm、灵敏度<30mJ/cm²。
- 来源：嘉峪检测 https://m.anytesting.com/news/1964276.html ；应用化学期刊《面向极紫外：光刻胶的发展回顾与展望》http://yyhx.ciac.jl.cn/EN/article/downloadArticleFile.do?attachType=PDF&id=17823 ；百度百科"化学放大胶" https://baike.baidu.com/item/化学放大胶/22244753 ；方正证券光刻胶框架报告 https://stock.tianyancha.com/qmp/report/2/a9b9ee3af9c6d68378e2d7b19b942d5b.pdf
- **国产化**：g/i线已有基础，KrF批量替代，ArF从验证走向小批量，EUV胶仍由日美企业主导。来源：https://industry7view.com/research/photoresist/

### 5.2 掩膜版（Mask/Reticle）

- **DUV掩膜版**：透射式，石英基板+铬（Cr）吸收层；先进节点用相移掩模（PSM）。
- **EUV掩膜版**：**反射式**——低热膨胀玻璃基板上镀Mo/Si多层膜（布拉格反射，反射率约70%），其上为TaN系吸收层图形；因斜入射存在阴影效应（shadowing），需超薄吸收层与新设计。掩膜缺陷（多层膜内埋缺陷）检测与修复是难点；需EUV pellicle（保护膜，如多晶硅薄膜，要求>88%透过率且耐高功率）防止颗粒污染。
  - 来源：虎嗅（多层布拉格反射镜原理，类同掩膜）https://www.huxiu.com/article/4841611.html ；优半导体 https://uedu.tw/semiconductor/a/multi-patterning ；半导体overlay词条（掩膜版形变控制0.3nm）https://b2bwiki.baidu.com/article/d0r813pftjstjkqndv8g
  - 掩膜数量对比（报道口径）：传统光学路线7nm约需83个掩模；EUV路线约68个光学掩模+5个EUV掩模。来源：https://mp.weixin.qq.com/s/c_F-TjQA3MieKczHJs2Wfg

---

## 6. 关键结论

1. 分辨率由 R=k1·λ/NA 决定；三条演进路径（短波长436→13.5nm、大NA至1.35浸没/0.55 High-NA、k1逼近0.25+多重曝光）共同支撑摩尔定律。
2. EUV核心是LPP锡光源（功率600W→1000W突破中）+ Mo/Si多层反射镜 + 全真空；ASML 0.33NA机型160–220wph、约1.5–2亿美元，0.55NA High-NA（EXE系列）>3.5亿欧元、~8nm分辨率。
3. DUV+SADP/SAQP可实现7nm等效，但成本/时间增加50%以上、良率更低——"节点等效、经济性不等效"。
4. 中国：SMEE 90nm已量产，28nm ArF浸没式仍在调试验证（"已交付"传闻被证伪），EUV整机未公开；国产化率约2.5%。
5. 化学放大胶（PAG+酸催化）是DUV/EUV胶共同基础；EUV掩膜为Mo/Si反射式，pellicle与缺陷控制是难点。

*信息缺口说明：ASML官方逐机型价格、SMEE 28nm机型确切规格、国产EUV整机进展均属未公开或仅有媒体推测，文中已分别标注。*

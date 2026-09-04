// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-5c2a8880
/**
 * 七器长卷数据（works.md S2）
 * DNA 追溯码按 v2.0 规范铸造：#龍芯⚡️{年}·{月}·{日}·{时辰}·{卦符}{卦名}-{ACTION}-{version}-{日序号}-{哈希}
 * 干支四柱以 src/lib/ganzhi.ts 算法实算（落成/发布日）；哈希未知位 ████████ 占位，以站长注册表登记为准。
 */

export interface WorkEntry {
  id: string // 锚点 id（供首页/他页跳转）
  index: string // 01–07
  name: string
  category: 'SCRIPT' | 'ALGORITHM' | 'ENGINE' | 'PROTOCOL' | 'PAPER'
  caption: string // 一句释义
  version: string
  dna: string
  detail: string[] // 展开详情 3–4 行
  searchQuery: string // 「获取源码」快速链接检索词（不裸露原始 URL）
}

export const HASH_PLACEHOLDER_NOTE =
  '哈希位 ████████ 为占位——以站长注册表登记值为准，禁止虚构。'

/** CSDN 快速链接（不裸露原始 URL 于文案） */
export const csdnSearchUrl = (q: string) =>
  `https://so.csdn.net/so/search?q=${encodeURIComponent(q)}`

export const WORKS: WorkEntry[] = [
  {
    id: 'cnsh',
    index: '01',
    name: 'CNSH 中文原生脚本',
    category: 'SCRIPT',
    caption: '中文即代码——母语级编程范式',
    version: 'v1.0',
    dna: '#龍芯⚡️丙午·丙申·己酉·午时·䷂屯-CNSH-SCRIPT-v1.0-0001-████████',
    detail: [
      '以中文为唯一母语的编程范式：关键字、标识符、错误信息皆为中文，让代码回归母语者的直觉。',
      '屯卦立命——万事开头难，中文编程的第一爻由此升起。每一行 CNSH 都自带 DNA 追溯码。',
      '语法即文章，缩进即章法。写代码，就是写一封给未来的中文信。',
    ],
    searchQuery: 'CNSH 中文原生脚本 UID9622',
  },
  {
    id: 'sancai',
    index: '02',
    name: '三才算法',
    category: 'ALGORITHM',
    caption: '天地人三才归一的决策内核',
    version: 'v1.0',
    dna: '#龍芯⚡️丙午·丙申·己酉·午时·䷊泰-SANCAI-ALGORITHM-v1.0-0002-████████',
    detail: [
      '取《易》三才之道：天时（环境变量）、地利（资源约束）、人和（意图目标）三线归一，方得决策。',
      '非黑箱权重，而是可直译的推演规则——每一步判断都可以被人读懂、被人质询。',
      '泰卦为证：天地交而万物通，三才合而决策明。',
    ],
    searchQuery: '三才算法 UID9622',
  },
  {
    id: 'audit',
    index: '03',
    name: '开放审计引擎',
    category: 'ENGINE',
    caption: '零黑箱的机器证明，人人可审',
    version: 'v1.0',
    dna: '#龍芯⚡️丙午·丙申·己酉·午时·䷓观-OPEN-AUDIT-ENGINE-v1.0-0003-████████',
    detail: [
      '把"相信我"换成"验证我"：每一次生成、每一次同步、每一次判定，都产出可复核的机器证明。',
      '观卦之义——观其所行，知其所守。审计接口完全公开，无需权限，无需申请。',
      '与 DNA 验证器同构：粘贴任一出证，即可验其四柱、卦象与哈希是否自洽。',
    ],
    searchQuery: '开放审计引擎 UID9622',
  },
  {
    id: 'csdn',
    index: '04',
    name: 'CSDN 同步引擎',
    category: 'ENGINE',
    caption: '内容主权直通车，一键同步',
    version: 'v1.0',
    dna: '#龍芯⚡️丙午·丙申·己酉·午时·䷹兑-CSDN-SYNC-ENGINE-v1.0-0004-████████',
    detail: [
      '一次撰写，多端同步：官网、CSDN、社区镜像同源发布，DNA 追溯码全程随行。',
      '兑卦之象——泽以通之。内容主权不寄生于任何单一平台，作者始终持有源头。',
      '实战之证见下方数据墙：1,512 点赞 · 844 收藏 · 博客总排名 12,631，真实可查。',
    ],
    searchQuery: '龍芯北辰_UID9622',
  },
  {
    id: 'gentleman',
    index: '05',
    name: '君子协议（中英双语）',
    category: 'PROTOCOL',
    caption: '一诺既出，天下共鉴',
    version: 'v1.0',
    dna: '#龍芯⚡️丙午·己丑·乙巳·午时·䷌同人-GENTLEMAN-ACCORD-v1.0-0005-████████',
    detail: [
      '2026-01-31 以中英双语向世界立约：免费开源、数据主权在民、不作恶、永续冻结。',
      '同人卦为盟——与天下人同此心。GPG 与 SHA-256 双指纹存证，转载须保留 DNA。',
      '双语全文见下卷「君子協議」对照长卷，中缝金线随诵读而进。',
    ],
    searchQuery: '君子协议 中英双语 UID9622',
  },
  {
    id: 'whitepaper',
    index: '06',
    name: '20 人格治理白皮书 v1.4',
    category: 'PAPER',
    caption: '矩阵的完整形态',
    version: 'v1.4',
    dna: '#龍芯⚡️丙午·丙申·己酉·午时·䷼中孚-GOVERNANCE-WHITEPAPER-v1.4-0006-████████',
    detail: [
      '十六人格在阵、四维预备在野：五维思维于二十人格间动态调配的完整治理框架。',
      '含《从对话到自主代理操作系统：演进之路》——主动观察协议 TypeScript 全文公开。',
      '中孚卦为信——治理之要，在于系统对内对外皆可被信任。',
    ],
    searchQuery: '20人格治理白皮书 UID9622',
  },
  {
    id: 'sovereign',
    index: '07',
    name: '无后台主权协议 v3.0',
    category: 'PROTOCOL',
    caption: '无后台，即无命门',
    version: 'v3.0',
    dna: '#龍芯⚡️丙午·丙申·己酉·午时·䷀乾-NO-BACKEND-SOVEREIGNTY-v3.0-0007-████████',
    detail: [
      '架构级承诺：系统不设任何后台入口。没有后台，就没有可被攻破、被胁迫、被收买的命门。',
      '乾卦为纲——天行健，主权以自强不减。信任不靠承诺维持，靠结构上"做不到"维持。',
      'TRUST-EXEC-RULES 全文公开，镜像流传于多个社区，DNA 可逐字验证。',
    ],
    searchQuery: '无后台主权协议 UID9622',
  },
]

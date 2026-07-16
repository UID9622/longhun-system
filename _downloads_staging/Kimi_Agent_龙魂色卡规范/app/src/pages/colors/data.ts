export interface ImmutableColor {
  index: string;
  name: string;
  englishName: string;
  englishSubtitle: string;
  hex: string;
  rgb: string;
  hsl: string;
  lab: string;
  cmyk: string;
  meaning: string;
  description: string;
  bullets: string[];
  textColor: string;
  pulseClass: string;
}

export const IMMUTABLE_COLORS: ImmutableColor[] = [
  {
    index: '01',
    name: '龙魂绿',
    englishName: 'DRAGON GREEN',
    englishSubtitle: 'PASS / NORMAL',
    hex: '#00C853',
    rgb: 'rgb(0, 200, 83)',
    hsl: '145°, 100%, 39%',
    lab: '72.5, -72.3, 48.1',
    cmyk: 'C:100 M:0 Y:59 K:22',
    meaning: '通过 · 正常 · 通行',
    description:
      '当系统状态为绿色时，表示一切正常，继续执行。绿色是木行的代表，象征生长、通畅、无阻。在五行中属木，在三才中关联"人"的生机。',
    bullets: [
      '权重得分 ≥ 90% 时显示',
      '审计通过标记',
      '系统正常运行指示',
      'Human≥0.34 铁律满足时高亮',
    ],
    textColor: '#00C853',
    pulseClass: 'animate-color-pulse-green',
  },
  {
    index: '02',
    name: '龙魂红',
    englishName: 'DRAGON RED',
    englishSubtitle: 'CIRCUIT BREAK / BLOCK',
    hex: '#FF3D00',
    rgb: 'rgb(255, 61, 0)',
    hsl: '14°, 100%, 50%',
    lab: '56.7, 68.2, 58.1',
    cmyk: 'C:0 M:76 Y:100 K:0',
    meaning: '熔断 · 阻断 · 必须停',
    description:
      '红色是最高级别的阻断信号。当系统检测到 dr ∈ {3,9} 时直接熔断，任何操作必须暂停，等待人工介入。红色属火，象征破坏、终止、不可逾越的边界。',
    bullets: [
      'dr ∈ {3,9} 触发熔断',
      '权重得分 < 50% 时警告',
      '人为干预强制标记',
      '协议违规阻断',
    ],
    textColor: '#FF3D00',
    pulseClass: 'animate-color-pulse-red',
  },
  {
    index: '03',
    name: '龙魂黄',
    englishName: 'DRAGON YELLOW',
    englishSubtitle: 'WARNING / REVIEW',
    hex: '#FFD600',
    rgb: 'rgb(255, 214, 0)',
    hsl: '50°, 100%, 50%',
    lab: '85.2, -7.8, 83.9',
    cmyk: 'C:0 M:16 Y:100 K:0',
    meaning: '警示 · 需要看 · 待审查',
    description:
      '黄色是提醒与审视的颜色。不阻断，但要求关注。待审查状态下所有操作记录将被标记黄色，需复核后方可继续。黄色属土，象征审慎、检视、中间态。',
    bullets: [
      '权重得分 50%-90% 区间标记',
      '待审查状态指示',
      '人工复核标记',
      '"中等风险" 默认颜色',
    ],
    textColor: '#FFD600',
    pulseClass: 'animate-color-pulse-yellow',
  },
  {
    index: '04',
    name: '龙魂黑',
    englishName: 'DRAGON BLACK',
    englishSubtitle: 'SHADOW / SILENT',
    hex: '#1A1A2E',
    rgb: 'rgb(26, 26, 46)',
    hsl: '240°, 28%, 14%',
    lab: '8.2, 5.1, -12.7',
    cmyk: 'C:43 M:43 Y:0 K:82',
    meaning: '影子 · 静默运行 · 基座',
    description:
      '黑色不是"不存在"，而是"静默存在"。龙魂黑是系统的基座色，所有面板的底色，所有运行的暗面。属水，象征深度、潜藏、根基。一切颜色在此之上才有意义。',
    bullets: [
      '系统背景基座色',
      '静默运行模式指示',
      '"shadow" 层级标识',
      '数据层底层标记',
    ],
    textColor: '#8A8AB5',
    pulseClass: '',
  },
  {
    index: '05',
    name: '龙魂金',
    englishName: 'DRAGON GOLD',
    englishSubtitle: 'SOVEREIGNTY / MASTER',
    hex: '#FFD700',
    rgb: 'rgb(255, 215, 0)',
    hsl: '51°, 100%, 50%',
    lab: '84.9, -6.1, 82.3',
    cmyk: 'C:0 M:16 Y:100 K:0',
    meaning: '主控 · 你在 · 主权',
    description:
      '金色是主权与主控的颜色。当你在系统中，金色标记你的存在。这是不可被覆盖的最高标识色，代表当前操作者的权威与责任。金色属金，象征决断、权力、光辉。',
    bullets: [
      '当前主控者标记',
      '最高权限指示',
      '不动点协议锚定色',
      '"root" 权限视觉反馈',
    ],
    textColor: '#FFD700',
    pulseClass: 'animate-color-pulse-gold',
  },
];

export interface ColorSpaceRow {
  name: string;
  hex: string;
  rgb: string;
  hsl: string;
  lab: string;
  cmyk: string;
  deltaE: string;
  textColor: string;
}

export const COLOR_SPACE_DATA: ColorSpaceRow[] = IMMUTABLE_COLORS.map((c) => ({
  name: c.name,
  hex: c.hex,
  rgb: c.rgb,
  hsl: c.hsl,
  lab: c.lab,
  cmyk: c.cmyk,
  deltaE: '0.00',
  textColor: c.textColor,
}));

export interface ImmutabilityRule {
  icon: 'lock' | 'grid' | 'book' | 'crown';
  title: string;
  text: string;
  code: string;
  codeColor: string;
}

export const IMMUTABILITY_RULES: ImmutabilityRule[] = [
  {
    icon: 'lock',
    title: '色值不变',
    text: 'hex、rgb、hsl——任何颜色表示空间中的值永远锁定。不允许近似，不允许偏移，不允许"稍微调整一下"。',
    code: 'const dragonGreen = "#00C853" // NEVER CHANGE',
    codeColor: '#00C853',
  },
  {
    icon: 'grid',
    title: '位置不变',
    text: '在五主色序列中的相对位置永恒固定。绿第一，红第二，黄第三，黑第四，金第五。这顺序本身即是协议。',
    code: 'const colorOrder = [GREEN, RED, YELLOW, BLACK, GOLD] // FIXED',
    codeColor: '#FF3D00',
  },
  {
    icon: 'book',
    title: '含义不变',
    text: '绿永远是通过，红永远是熔断，黄永远是警示，黑永远是影子，金永远是主控。含义绑定色值，色值绑定含义。',
    code: 'const meaning = { "#00C853": "PASS", ... } // ETERNAL',
    codeColor: '#FFD600',
  },
  {
    icon: 'crown',
    title: '优先级不变',
    text: '五主色的识别优先级高于一切扩展色。机器在任何色卡中首先识别这五种颜色。扩展色只能附加，不能替代。',
    code: 'priority: IMMUTABLE > EXTENSION > THEME',
    codeColor: '#FFD700',
  },
];

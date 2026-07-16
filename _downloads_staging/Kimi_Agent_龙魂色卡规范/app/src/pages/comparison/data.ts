// ============================================================
// 各国色卡 — Color & Country Data Constants
// ============================================================

export interface ImmutableColor {
  hex: string;
  name: string;
  meaning: string;
  tag: string;
  token: string;
}

export interface ExtensionColor {
  hex: string;
  name: string;
  description: string;
  tag: string;
}

export interface CountryData {
  id: string;
  nameCn: string;
  nameEn: string;
  label: string;
  primaryColor: string;
  extensions: [ExtensionColor, ExtensionColor];
  flagEmoji: string;
  flagBgPos: string; // background-position for sprite
}

// ---- Five Immutable Colors (不动点五主色) ----
export const IMMUTABLE_COLORS: ImmutableColor[] = [
  { hex: '#00C853', name: '龙魂绿', meaning: '通过', tag: '通过', token: '--dragon-green' },
  { hex: '#FF3D00', name: '龙魂红', meaning: '熔断', tag: '熔断', token: '--dragon-red' },
  { hex: '#FFD600', name: '龙魂黄', meaning: '警示', tag: '警示', token: '--dragon-yellow' },
  { hex: '#1A1A2E', name: '龙魂黑', meaning: '影子', tag: '影子', token: '--dragon-black' },
  { hex: '#FFD700', name: '龙魂金', meaning: '主控', tag: '主控', token: '--dragon-gold' },
];

// ---- Country Palette Extensions ----
export const COUNTRIES: CountryData[] = [
  {
    id: 'china',
    nameCn: '中国',
    nameEn: 'China',
    label: '中华人民共和国 · 不动点 + 2',
    primaryColor: '#DE2910',
    extensions: [
      { hex: '#DE2910', name: '中国红', description: '中华人民共和国国旗主色，象征革命与热血', tag: '中国主权标识色' },
      { hex: '#F8B500', name: '琉璃黄', description: '传统琉璃瓦色，象征皇权与文明', tag: '华夏文明象征色' },
    ],
    flagEmoji: '🇨🇳',
    flagBgPos: '0% 0%',
  },
  {
    id: 'japan',
    nameCn: '日本',
    nameEn: 'Japan',
    label: '日本国 · 不动点 + 2',
    primaryColor: '#FFB7C5',
    extensions: [
      { hex: '#FFB7C5', name: '樱花粉', description: '樱花象征物哀之美，是日本文化的精神底色', tag: '日本文化标识色' },
      { hex: '#4B0082', name: '靛蓝', description: '江户时代传统蓝染，象征深沉与工匠', tag: '传统染织物色' },
    ],
    flagEmoji: '🇯🇵',
    flagBgPos: '33.3% 0%',
  },
  {
    id: 'eu',
    nameCn: '欧盟',
    nameEn: 'EU',
    label: 'European Union · 不动点 + 2',
    primaryColor: '#003399',
    extensions: [
      { hex: '#003399', name: '欧盟蓝', description: '欧盟旗帜底色，象征欧洲的统一与和平', tag: '欧洲联盟标识色' },
      { hex: '#FFCC00', name: '星金黄', description: '十二颗金星之色，象征欧洲的完美与团结', tag: '欧盟之星色' },
    ],
    flagEmoji: '🇪🇺',
    flagBgPos: '66.6% 0%',
  },
  {
    id: 'us',
    nameCn: '美国',
    nameEn: 'United States',
    label: 'United States · 不动点 + 2',
    primaryColor: '#3C3B6E',
    extensions: [
      { hex: '#3C3B6E', name: '自由蓝', description: '星条旗蓝色，象征警惕、正义与坚韧', tag: '美国主权标识色' },
      { hex: '#B22234', name: '勇气红', description: '星条旗红色，象征勇气与牺牲', tag: '美国精神色' },
    ],
    flagEmoji: '🇺🇸',
    flagBgPos: '100% 0%',
  },
];

// ---- Full palette strips for machine vision ----
export const FULL_PALETTES: Record<string, string[]> = {
  china:  ['#00C853', '#FF3D00', '#FFD600', '#1A1A2E', '#FFD700', '#DE2910', '#F8B500'],
  japan:  ['#00C853', '#FF3D00', '#FFD600', '#1A1A2E', '#FFD700', '#FFB7C5', '#4B0082'],
  eu:     ['#00C853', '#FF3D00', '#FFD600', '#1A1A2E', '#FFD700', '#003399', '#FFCC00'],
  us:     ['#00C853', '#FF3D00', '#FFD600', '#1A1A2E', '#FFD700', '#3C3B6E', '#B22234'],
};

// ---- Table rows data ----
export interface TableRow {
  colorName: string;
  hex: string;
  china: string;
  japan: string;
  eu: string;
  us: string;
  type: 'immutable' | 'extension';
  status: string;
  statusColor: string;
  leftBorderColor: string;
}

export const TABLE_ROWS: TableRow[] = [
  {
    colorName: '龙魂绿', hex: '#00C853',
    china: '✓', japan: '✓', eu: '✓', us: '✓',
    type: 'immutable', status: '不可变', statusColor: 'var(--dragon-red)',
    leftBorderColor: '#00C853',
  },
  {
    colorName: '龙魂红', hex: '#FF3D00',
    china: '✓', japan: '✓', eu: '✓', us: '✓',
    type: 'immutable', status: '不可变', statusColor: 'var(--dragon-red)',
    leftBorderColor: '#FF3D00',
  },
  {
    colorName: '龙魂黄', hex: '#FFD600',
    china: '✓', japan: '✓', eu: '✓', us: '✓',
    type: 'immutable', status: '不可变', statusColor: 'var(--dragon-red)',
    leftBorderColor: '#FFD600',
  },
  {
    colorName: '龙魂黑', hex: '#1A1A2E',
    china: '✓', japan: '✓', eu: '✓', us: '✓',
    type: 'immutable', status: '不可变', statusColor: 'var(--dragon-red)',
    leftBorderColor: '#555580',
  },
  {
    colorName: '龙魂金', hex: '#FFD700',
    china: '✓', japan: '✓', eu: '✓', us: '✓',
    type: 'immutable', status: '不可变', statusColor: 'var(--dragon-red)',
    leftBorderColor: '#FFD700',
  },
  {
    colorName: '扩展一', hex: '',
    china: '#DE2910 中国红', japan: '#FFB7C5 樱花粉', eu: '#003399 欧盟蓝', us: '#3C3B6E 自由蓝',
    type: 'extension', status: '可变', statusColor: 'var(--dragon-green)',
    leftBorderColor: 'transparent',
  },
  {
    colorName: '扩展二', hex: '',
    china: '#F8B500 琉璃黄', japan: '#4B0082 靛蓝', eu: '#FFCC00 星金黄', us: '#B22234 勇气红',
    type: 'extension', status: '可变', statusColor: 'var(--dragon-green)',
    leftBorderColor: 'transparent',
  },
];

// ---- Five doctrine characters ----
export const DOCTRINE_CHARS = [
  { char: '规', color: '#00C853', meaning: '绿 · 通过' },
  { char: '矩', color: '#FF3D00', meaning: '红 · 熔断' },
  { char: '不', color: '#FFD600', meaning: '黄 · 警示' },
  { char: '动', color: '#8A8AB5', meaning: '影 · 静默' },
  { char: '点', color: '#FFD700', meaning: '金 · 主控' },
];

export const DOCTRINE_ORBS = [
  { char: '通', color: '#00C853', label: '通过' },
  { char: '停', color: '#FF3D00', label: '熔断' },
  { char: '警', color: '#FFD600', label: '警示' },
  { char: '影', color: '#1A1A2E', label: '影子' },
  { char: '控', color: '#FFD700', label: '主控' },
];

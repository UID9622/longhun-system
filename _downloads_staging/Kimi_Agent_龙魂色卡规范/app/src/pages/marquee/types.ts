export interface ColorSegment {
  id: number;
  name: string;
  label: string;
  enLabel: string;
  hex: string;
  state: string;
  meaning: string;
  triggers: string[];
  action: string;
  textColor: string;
}

export interface MarqueeSettings {
  speed: number; // seconds per cycle
  direction: 'left' | 'right';
  mode: 'continuous' | 'pulse' | 'segment';
  isPlaying: boolean;
}

export const COLOR_SEGMENTS: ColorSegment[] = [
  {
    id: 1,
    name: '通过',
    label: '绿 · PASS',
    enLabel: 'PASS / NORMAL',
    hex: '#00C853',
    state: '通过',
    meaning: '一切正常，继续执行',
    triggers: ['权重>=90%', '审计通过', '铁律满足'],
    action: '无需操作，保持监控',
    textColor: '#FFFFFF',
  },
  {
    id: 2,
    name: '熔断',
    label: '红 · BREAK',
    enLabel: 'BREAK / CRITICAL',
    hex: '#FF3D00',
    state: '熔断',
    meaning: '必须停止，人工介入',
    triggers: ['dr∈{3,9}', '权重<50%', '协议违规'],
    action: '立即停止所有操作',
    textColor: '#FFFFFF',
  },
  {
    id: 3,
    name: '警示',
    label: '黄 · WARN',
    enLabel: 'WARN / REVIEW',
    hex: '#FFD600',
    state: '警示',
    meaning: '需要关注，待审查',
    triggers: ['权重50-90%', '待复核标记'],
    action: '复核后决定放行/阻断',
    textColor: '#1A1A2E',
  },
  {
    id: 4,
    name: '影子',
    label: '黑 · SHADOW',
    enLabel: 'SHADOW / SILENT',
    hex: '#1A1A2E',
    state: '影子',
    meaning: '静默运行，基座状态',
    triggers: ['后台进程', '数据层', '静默监控'],
    action: '自动运行，无需干预',
    textColor: '#8A8AB5',
  },
  {
    id: 5,
    name: '主控',
    label: '金 · MASTER',
    enLabel: 'MASTER / CONTROL',
    hex: '#FFD700',
    state: '主控',
    meaning: '你在，主权标识',
    triggers: ['当前操作者标记', 'root权限'],
    action: '确认权限后操作',
    textColor: '#1A1A2E',
  },
  {
    id: 6,
    name: '外联',
    label: '蓝 · LINK',
    enLabel: 'LINK / EXTERNAL',
    hex: '#2962FF',
    state: '外联',
    meaning: '与外部系统通信',
    triggers: ['API调用', '跨系统交互', '数据同步'],
    action: '监控通信安全',
    textColor: '#FFFFFF',
  },
  {
    id: 7,
    name: '进化',
    label: '紫 · EVOLVE',
    enLabel: 'EVOLVE / UPGRADE',
    hex: '#AA00FF',
    state: '进化',
    meaning: '系统升级中',
    triggers: ['版本更新', '功能迭代', '协议升级'],
    action: '等待升级完成',
    textColor: '#FFFFFF',
  },
];

// Title character color mapping per design.md
export const TITLE_CHARS = [
  { char: '七', color: '#AA00FF' },
  { char: '彩', color: '#2962FF' },
  { char: '跑', color: '#FFD700' },
  { char: '马', color: '#1A1A2E', strokeColor: '#FFFFFF' },
  { char: '灯', color: '#FFD600' },
];

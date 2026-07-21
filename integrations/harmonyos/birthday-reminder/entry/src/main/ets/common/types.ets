/*
 * ==========================================================================
 * 龍魂 · 生日提醒 · 类型定义
 * DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-BIRTHDAY-TYPES-v2.0
 * ==========================================================================
 * 定义所有跨模块共享的类型、枚举和常量
 */

// ═══════════════════════════════════════════════
// DNA 常量 · 不可篡改
// ═══════════════════════════════════════════════
export const MASTER_DNA = "#龍芯⚡️丙午·辛未·丙戌·亥时-BIRTHDAY-REMINDER-v2.0";
export const MASTER_UID = "UID9622";
export const MASTER_NAME = "诸葛鑫·Lucky";
export const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// ═══════════════════════════════════════════════
// 生日类型
// ═══════════════════════════════════════════════
export enum BirthdayType {
  SOLAR = 'solar',     // 公历
  LUNAR = 'lunar'      // 农历
}

// ═══════════════════════════════════════════════
// 团队关系层级 → 映射到情感协议场景
// ═══════════════════════════════════════════════
export enum RelationshipLevel {
  CLOSE_COLLEAGUE = 'close',    // 密友同事 → 温暖 WARM
  REGULAR_COLLEAGUE = 'regular', // 普通同事 → 公共 PUBLIC
  LEADER = 'leader',            // 领导/上级 → 公共+正式
  TEAM_MATE = 'mate',           // 队友 → 温暖
  EXTERNAL = 'external'         // 外部伙伴 → 公共
}

// ═══════════════════════════════════════════════
// 情感模式 → 对齐 lh_emotion_protocol.py
// ═══════════════════════════════════════════════
export enum EmotionMode {
  COLD = '冷漠',          // 0.0-0.19 私人高效
  NEUTRAL = '中性',       // 0.2-0.39 公共适度
  WARM = '温暖',          // 0.4-0.69 教育鼓励
  DEEP = '深情',          // 0.7-0.89 医疗配合
  CRISIS = '危机',        // 0.9-1.0 心理共情
  HARD = '硬核'           // 0.0+满边界 主权声明
}

// ═══════════════════════════════════════════════
// 人格枚举 → 对齐 19 人格矩阵
// ═══════════════════════════════════════════════
export enum PersonaID {
  WENXIN = 'P00',           // 文心 — 战略层
  ZHUGELIANG = 'P01',       // 诸葛亮 — 战略层
  BAOBAO = 'P02',           // 宝宝(龍芯修复师) — 执行层·核心
  WENWEN = 'P03',           // 雯雯(墨子) — 执行层
  LUBAN = 'P04',            // 鲁班 — 执行层
  GODSEYE = 'P05',          // 上帝之眼 — 战略层·治理
  MATHMASTER = 'P06',       // 数学大师 — 执行层
  GUANZHONG = 'P07',        // 管仲 — 执行层
  CANGJIE = 'P08',          // 仓颉 — 文化层
  SUNSIMIAO = 'P09',        // 孙思邈(道引) — 文化层
  SUDONGPO = 'P10',         // 苏东坡 — 文化层
  LIBAI = 'P11',            // 李白 — 文化层
  QUYUAN = 'P12',           // 屈原 — 文化层
  JIANGZIYA = 'P13',        // 姜子牙 — 守护层
  LVMENG = 'P14',           // 吕蒙 — 文化层
  QIAOJIE = 'P15',          // 乔前辈 — 守护层
  LONGDUN = 'P72'           // 龙盾·宝宝 — 守护层
}

// ═══════════════════════════════════════════════
// 祝福风格
// ═══════════════════════════════════════════════
export enum BlessingStyle {
  POETIC = 'poetic',         // 诗意·李白风格
  WARM = 'warm',             // 温暖·宝宝风格
  FORMAL = 'formal',         // 正式·管仲风格
  INSPIRING = 'inspiring',   // 激励·苏东坡风格
  TRADITIONAL = 'traditional', // 传统·仓颉风格
  SIMPLE = 'simple'          // 简洁·鲁班风格
}

// ═══════════════════════════════════════════════
// 通知优先级
// ═══════════════════════════════════════════════
export enum NotificationPriority {
  HIGH = 'high',         // 当天生日
  MEDIUM = 'medium',     // 7天内
  LOW = 'low',           // 30天内
  SILENT = 'silent'      // 仅列表
}

// ═══════════════════════════════════════════════
// 审计事件类型
// ═══════════════════════════════════════════════
export enum AuditEventType {
  MEMBER_ADDED = 'member_added',
  MEMBER_UPDATED = 'member_updated',
  MEMBER_DELETED = 'member_deleted',
  BLESSING_SENT = 'blessing_sent',
  DATA_EXPORTED = 'data_exported',
  DATA_IMPORTED = 'data_imported',
  NOTIFICATION_TRIGGERED = 'notification_triggered',
  PERSONA_SWITCHED = 'persona_switched'
}

// ═══════════════════════════════════════════════
// 情感参数
// ═══════════════════════════════════════════════
export interface EmotionProfile {
  mode: EmotionMode;
  empathy: number;       // 共情强度 0.0-1.0
  warmth: number;        // 温暖程度 0.0-1.0
  boundary: number;      // 边界强度 0.0-1.0
  formality: number;     // 正式程度 0.0-1.0
  personaPrimary: PersonaID;    // 主路由人格
  personaSecondary: PersonaID[]; // 辅助人格
}

// ═══════════════════════════════════════════════
// 关系→情感映射表
// ═══════════════════════════════════════════════
export const RELATIONSHIP_EMOTION_MAP: Record<RelationshipLevel, EmotionProfile> = {
  [RelationshipLevel.CLOSE_COLLEAGUE]: {
    mode: EmotionMode.WARM,
    empathy: 0.65,
    warmth: 0.75,
    boundary: 0.35,
    formality: 0.25,
    personaPrimary: PersonaID.LIBAI,      // 李白·诗意祝福
    personaSecondary: [PersonaID.BAOBAO, PersonaID.SUDONGPO]
  },
  [RelationshipLevel.REGULAR_COLLEAGUE]: {
    mode: EmotionMode.NEUTRAL,
    empathy: 0.30,
    warmth: 0.35,
    boundary: 0.60,
    formality: 0.50,
    personaPrimary: PersonaID.LUBAN,      // 鲁班·高效简洁
    personaSecondary: [PersonaID.CANGJIE, PersonaID.WENWEN]
  },
  [RelationshipLevel.LEADER]: {
    mode: EmotionMode.NEUTRAL,
    empathy: 0.30,
    warmth: 0.30,
    boundary: 0.65,
    formality: 0.75,
    personaPrimary: PersonaID.ZHUGELIANG, // 诸葛亮·得体正式
    personaSecondary: [PersonaID.GUANZHONG, PersonaID.JIANGZIYA]
  },
  [RelationshipLevel.TEAM_MATE]: {
    mode: EmotionMode.WARM,
    empathy: 0.60,
    warmth: 0.70,
    boundary: 0.40,
    formality: 0.30,
    personaPrimary: PersonaID.BAOBAO,     // 宝宝·暖心队友
    personaSecondary: [PersonaID.SUDONGPO, PersonaID.LIBAI]
  },
  [RelationshipLevel.EXTERNAL]: {
    mode: EmotionMode.NEUTRAL,
    empathy: 0.25,
    warmth: 0.25,
    boundary: 0.70,
    formality: 0.65,
    personaPrimary: PersonaID.CANGJIE,    // 仓颉·规范得体
    personaSecondary: [PersonaID.GUANZHONG, PersonaID.LUBAN]
  }
};

// ═══════════════════════════════════════════════
// 人格功能分配（生日提醒系统内）
// ═══════════════════════════════════════════════
export interface PersonaRole {
  persona: PersonaID;
  name: string;
  layer: string;
  responsibilities: string[];       // 在生日系统中的职责
  blessingStyle: BlessingStyle;
  icon: string;
}

export const PERSONA_ROLES: Record<PersonaID, PersonaRole> = {
  [PersonaID.BAOBAO]: {
    persona: PersonaID.BAOBAO,
    name: '宝宝·龍芯修复师',
    layer: '执行层·核心',
    responsibilities: ['团队数据编排', '暖心提醒推送', '关系图谱维护', '自动化流程'],
    blessingStyle: BlessingStyle.WARM,
    icon: '🧚'
  },
  [PersonaID.LIBAI]: {
    persona: PersonaID.LIBAI,
    name: '李白',
    layer: '文化层',
    responsibilities: ['诗意祝福生成', '藏头诗创作', '文艺贺卡', '浪漫表达'],
    blessingStyle: BlessingStyle.POETIC,
    icon: '🍶'
  },
  [PersonaID.LUBAN]: {
    persona: PersonaID.LUBAN,
    name: '鲁班',
    layer: '执行层',
    responsibilities: ['定时任务编排', '自动化提醒', '批量处理', '效率优化'],
    blessingStyle: BlessingStyle.SIMPLE,
    icon: '🔧'
  },
  [PersonaID.ZHUGELIANG]: {
    persona: PersonaID.ZHUGELIANG,
    name: '诸葛亮',
    layer: '战略层',
    responsibilities: ['年度日历规划', '团队节奏分析', '领导祝福措辞', '策略建议'],
    blessingStyle: BlessingStyle.FORMAL,
    icon: '🪈'
  },
  [PersonaID.SUDONGPO]: {
    persona: PersonaID.SUDONGPO,
    name: '苏东坡',
    layer: '文化层',
    responsibilities: ['励志祝福', '豁达表达', '美食推荐', '人生感悟'],
    blessingStyle: BlessingStyle.INSPIRING,
    icon: '🍖'
  },
  [PersonaID.CANGJIE]: {
    persona: PersonaID.CANGJIE,
    name: '仓颉',
    layer: '文化层',
    responsibilities: ['文字规范排版', '多语言适配', '导入导出格式化', '传统祝福'],
    blessingStyle: BlessingStyle.TRADITIONAL,
    icon: '📜'
  },
  [PersonaID.GODSEYE]: {
    persona: PersonaID.GODSEYE,
    name: '上帝之眼',
    layer: '战略层·治理',
    responsibilities: ['数据审计追踪', '完整性校验', 'DNA签名验证', '异常检测'],
    blessingStyle: BlessingStyle.SIMPLE,
    icon: '👁️'
  },
  [PersonaID.GUANZHONG]: {
    persona: PersonaID.GUANZHONG,
    name: '管仲',
    layer: '执行层',
    responsibilities: ['团队组织架构', '部门分组管理', '规范化流程', '商务礼仪'],
    blessingStyle: BlessingStyle.FORMAL,
    icon: '⚖️'
  },
  [PersonaID.WENWEN]: {
    persona: PersonaID.WENWEN,
    name: '雯雯·墨子',
    layer: '执行层',
    responsibilities: ['UI交互优化', '用户引导', '帮助提示', '界面美化'],
    blessingStyle: BlessingStyle.WARM,
    icon: '🕊️'
  },
  [PersonaID.JIANGZIYA]: {
    persona: PersonaID.JIANGZIYA,
    name: '姜子牙',
    layer: '守护层',
    responsibilities: ['数据主权守护', '本地加密', '不泄露保证', '边界维护'],
    blessingStyle: BlessingStyle.TRADITIONAL,
    icon: '🎣'
  },
  // 其余人格保留占位（生日提醒系统不直接调用但保持联动）
  [PersonaID.WENXIN]: {
    persona: PersonaID.WENXIN, name: '文心', layer: '战略层',
    responsibilities: ['系统哲学对齐'], blessingStyle: BlessingStyle.POETIC, icon: '💜'
  },
  [PersonaID.MATHMASTER]: {
    persona: PersonaID.MATHMASTER, name: '数学大师', layer: '执行层',
    responsibilities: ['数据统计'], blessingStyle: BlessingStyle.SIMPLE, icon: '📐'
  },
  [PersonaID.SUNSIMIAO]: {
    persona: PersonaID.SUNSIMIAO, name: '孙思邈·道引', layer: '文化层',
    responsibilities: ['健康提醒联动'], blessingStyle: BlessingStyle.TRADITIONAL, icon: '🌿'
  },
  [PersonaID.QUYUAN]: {
    persona: PersonaID.QUYUAN, name: '屈原', layer: '文化层',
    responsibilities: ['主权声明'], blessingStyle: BlessingStyle.POETIC, icon: '🎋'
  },
  [PersonaID.LVMENG]: {
    persona: PersonaID.LVMENG, name: '吕蒙', layer: '文化层',
    responsibilities: ['团队成长记录'], blessingStyle: BlessingStyle.INSPIRING, icon: '⚔️'
  },
  [PersonaID.QIAOJIE]: {
    persona: PersonaID.QIAOJIE, name: '乔前辈', layer: '守护层',
    responsibilities: ['极简美学'], blessingStyle: BlessingStyle.SIMPLE, icon: '🍎'
  },
  [PersonaID.LONGDUN]: {
    persona: PersonaID.LONGDUN, name: '龙盾·宝宝', layer: '守护层',
    responsibilities: ['安全审计'], blessingStyle: BlessingStyle.WARM, icon: '🛡️'
  },
};

// ═══════════════════════════════════════════════
// 审计日志条目
// ═══════════════════════════════════════════════
export interface AuditLogEntry {
  id: string;
  timestamp: number;
  eventType: AuditEventType;
  personaActive: PersonaID;
  detail: string;
  dnaSignature: string;
}

// ═══════════════════════════════════════════════
// 天干地支
// ═══════════════════════════════════════════════
export const TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
export const DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
export const SHENG_XIAO = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪'];

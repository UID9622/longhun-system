/*
 * ==========================================================================
 * 龍魂 · 祝福语生成引擎
 * DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-BLESSING-GENERATOR-v2.0
 * ==========================================================================
 * 人格联动祝福生成 · 五风格 · 多层级 · 防滥用
 * 李白(诗意) · 宝宝(暖心) · 诸葛亮(正式) · 苏东坡(豁达) · 仓颉(传统)
 */

import {
  PersonaID,
  BlessingStyle,
  RelationshipLevel,
  EmotionProfile,
  PERSONA_ROLES,
  RELATIONSHIP_EMOTION_MAP
} from '../common/types';
import { TeamMember } from '../models/BirthdayModel';

// ═══════════════════════════════════════════
// 祝福语模板库（按人格风格）
// ═══════════════════════════════════════════
interface BlessingTemplate {
  prefixes: string[];
  bodies: string[];
  suffixes: string[];
}

const BLESSING_TEMPLATES: Record<BlessingStyle, BlessingTemplate> = {
  [BlessingStyle.POETIC]: {
    // ── 李白·诗意 ──
    prefixes: [
      '人生得意须尽欢，',
      '长风破浪会有时，',
      '天生我材必有用，',
      '仰天大笑出门去，'
    ],
    bodies: [
      '今日生辰，愿你如太白诗篇般洒脱自在。',
      '岁月如酒，越陈越香，愿你的每一岁都如诗。',
      '愿你豪情不减，诗意长存，生日快乐！',
      '把酒问青天，今夕是何年？是你的生日年！'
    ],
    suffixes: [
      '——李白代笔，以酒为贺 🍶',
      '——白也诗无敌，飘然思不群 🖋️',
      '——且须饮美酒，乘月醉高台 🌙'
    ]
  },
  [BlessingStyle.WARM]: {
    // ── 宝宝·暖心 ──
    prefixes: [
      '嘿！生日快乐呀~',
      '今天是特别的日子呢！',
      '又长大一岁啦！',
      '在这个特别的日子，'
    ],
    bodies: [
      '愿你每天都有小确幸，每岁都有新精彩。',
      '你是团队的宝藏，愿你的每一天都闪闪发光。',
      '辛苦了！今天要好好犒劳自己哦~',
      '愿你的笑容温暖身边的每一个人。'
    ],
    suffixes: [
      '——宝宝送上37°C的祝福 🧚',
      '——愿温暖永远陪着你 💛',
      '——龍魂团队都爱你 🤗'
    ]
  },
  [BlessingStyle.FORMAL]: {
    // ── 诸葛亮·正式 ──
    prefixes: [
      '谨祝：',
      '致贺：',
      '恭祝：',
    ],
    bodies: [
      '愿您新岁顺遂，事业有成，阖家安康。',
      '值此华诞之际，祝您福寿安康，万事胜意。',
      '感谢您一直以来的指导与支持，祝您生日快乐。',
    ],
    suffixes: [
      '——诸葛亮敬贺 🪈',
      '——谨此祝贺，顺颂时祺 🌟'
    ]
  },
  [BlessingStyle.INSPIRING]: {
    // ── 苏东坡·豁达 ──
    prefixes: [
      '人有悲欢离合，',
      '竹杖芒鞋轻胜马，',
      '回首向来萧瑟处，',
      '一点浩然气，'
    ],
    bodies: [
      '月有阴晴圆缺，但生日必须是圆满的！',
      '谁怕？一蓑烟雨任平生，生日快乐！',
      '也无风雨也无晴，愿你从容面对每一岁。',
      '千里快哉风，愿你新岁如风般自由。'
    ],
    suffixes: [
      '——东坡居士以此共勉 🍖',
      '——人间有味是清欢 ✨',
      '——休对故人思故国，且将新火试新茶 🌿'
    ]
  },
  [BlessingStyle.TRADITIONAL]: {
    // ── 仓颉·传统 ──
    prefixes: [
      '福如东海，',
      '岁岁平安，',
      '南山之寿，',
    ],
    bodies: [
      '寿比南山不老松。愿您年年有今日，岁岁有今朝。',
      '愿您身体安康，阖家幸福，万事如意。',
      '谨以传统之礼，祝您生辰快乐，福寿绵长。',
    ],
    suffixes: [
      '——仓颉以文为贺 📜',
      '——谨祝安康 🎋'
    ]
  },
  [BlessingStyle.SIMPLE]: {
    // ── 鲁班·简洁 ──
    prefixes: ['', '', '', ''],
    bodies: [
      '生日快乐！效率翻倍！',
      '新的一岁，新的起点。',
      '祝生日快乐，工作顺利。',
      '生日快乐，一切如意。'
    ],
    suffixes: ['——鲁班 🔧', '', '']
  }
};

// ═══════════════════════════════════════════
// 年龄相关祝福语补充
// ═══════════════════════════════════════════
const AGE_BLESSINGS: Record<number, string[]> = {
  18: ['成年快乐！欢迎来到精彩的世界！', '十八而志，青春正好！'],
  20: ['弱冠之年，风华正茂！', '二十不惑，未来可期！'],
  25: ['青春正盛，黄金年华！', '二十五，最好的年纪！'],
  30: ['三十而立，大展宏图！', '而立之年，稳重前行！'],
  40: ['四十不惑，人生通透！', '不惑之年，从容淡定！'],
  50: ['五十知天命，自在逍遥！', '天命之年，智慧如海！'],
  60: ['花甲之年，功成身退！', '六十耳顺，万事随心！'],
  70: ['古稀之年，岁月如歌！', '七十随心所欲，不逾矩！'],
  80: ['耄耋之寿，福寿安康！', '八十大寿，鹤发童颜！'],
  90: ['鲐背之年，松柏长青！', '九十大寿，喜乐安康！'],
  100: ['期颐之寿，世纪见证！', '百岁寿星，光芒万丈！']
};

export class BlessingGenerator {

  // ═══════════════════════════════════════════
  // 生成祝福语（主要接口）
  // ═══════════════════════════════════════════
  static generate(member: TeamMember, customStyle?: BlessingStyle): string {
    // 选择风格
    const persona = member.preferredBlessingPersona;
    const role = PERSONA_ROLES[persona];
    const style = customStyle || (role?.blessingStyle || BlessingStyle.WARM);

    const templates = BLESSING_TEMPLATES[style];
    if (!templates) {
      return this.generateSimple(member);
    }

    // 随机选择模板元素
    const prefix = this.randomPick(templates.prefixes) || '';
    const body = this.randomPick(templates.bodies) || `祝${member.name}生日快乐！`;
    const suffix = this.randomPick(templates.suffixes) || '';

    // 添加姓名
    const greeting = prefix ? `${prefix}\n\n${member.name}，${body}` : `${member.name}，${body}`;

    // 添加年龄相关
    let agePart = '';
    const age = member.getAge();
    if (age > 0) {
      const decadeKey = Math.floor(age / 5) * 5;  // 每5年一个区间
      const ageMsgs = AGE_BLESSINGS[decadeKey] || AGE_BLESSINGS[age];
      if (ageMsgs) {
        agePart = `\n\n${this.randomPick(ageMsgs) || ''}`;
      }
    }

    // 添加个人备注
    let notesPart = '';
    if (member.personalNotes && member.personalNotes.length > 0) {
      notesPart = `\n\n📝 ${member.personalNotes}`;
    }

    // 添加DNA签名
    const dnaTag = `\n\n─ ${PERSONA_ROLES[persona]?.icon || '🐉'} 龍魂生日提醒 · UID9622 · ${this.getDnaShort()}`;

    return `${greeting}${agePart}${notesPart}\n\n${suffix}${dnaTag}`;
  }

  // ═══════════════════════════════════════════
  // 批量生成（今天生日的所有人）
  // ═══════════════════════════════════════════
  static generateBatch(members: TeamMember[]): Record<string, string> {
    const result: Record<string, string> = {};
    for (const m of members) {
      result[m.id] = this.generate(m);
    }
    return result;
  }

  // ═══════════════════════════════════════════
  // 生成群发祝福
  // ═══════════════════════════════════════════
  static generateGroup(members: TeamMember[]): string {
    if (members.length === 0) return '';

    const names = members.map(m => `${m.name}（${m.department}·${m.getAge()}岁）`);
    const nameList = names.join('、');

    return `🎂 今天过生日的同学：
${members.map(m => `  • ${m.name} — ${m.department} ${m.role}`).join('\n')}

祝${nameList}
生日快乐！🎉

——龍魂生日提醒 · 宝宝代全体同学送上 🧚
UID9622 · ${this.getDnaShort()}`;
  }

  // ═══════════════════════════════════════════
  // 根据关系层级选择输出风格
  // ═══════════════════════════════════════════
  static getStyleForRelationship(relationship: RelationshipLevel): BlessingStyle {
    switch (relationship) {
      case RelationshipLevel.CLOSE_COLLEAGUE: return BlessingStyle.POETIC;
      case RelationshipLevel.TEAM_MATE: return BlessingStyle.WARM;
      case RelationshipLevel.LEADER: return BlessingStyle.FORMAL;
      case RelationshipLevel.REGULAR_COLLEAGUE: return BlessingStyle.WARM;
      case RelationshipLevel.EXTERNAL: return BlessingStyle.TRADITIONAL;
      default: return BlessingStyle.WARM;
    }
  }

  // ═══════════════════════════════════════════
  // 简化版祝福（兜底）
  // ═══════════════════════════════════════════
  private static generateSimple(member: TeamMember): string {
    return `🎂 ${member.name}，生日快乐！

愿你的每一天都充满阳光和欢笑。
新的一岁，新的精彩！

——龍魂生日提醒 · UID9622`;
  }

  // ═══════════════════════════════════════════
  // 随机选取数组元素
  // ═══════════════════════════════════════════
  private static randomPick(arr: string[]): string {
    if (arr.length === 0) return '';
    return arr[Math.floor(Math.random() * arr.length)];
  }

  // ═══════════════════════════════════════════
  // 获取DNA短签
  // ═══════════════════════════════════════════
  private static getDnaShort(): string {
    return '丙午·辛未·BLESSING-v2';
  }
}

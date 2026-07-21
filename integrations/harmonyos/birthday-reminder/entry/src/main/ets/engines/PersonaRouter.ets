/*
 * ==========================================================================
 * 龍魂 · 人格路由引擎
 * DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-PERSONA-ROUTER-v2.0
 * ==========================================================================
 * 根据任务类型、关系层级、场景自动路由到最合适的人格。
 * 与 19 人格矩阵 + 情感协议联动。
 */

import {
  PersonaID,
  RelationshipLevel,
  BlessingStyle,
  EmotionMode,
  PERSONA_ROLES,
  RELATIONSHIP_EMOTION_MAP,
  PersonaRole,
  EmotionProfile
} from '../common/types';
import { TeamMember } from '../models/BirthdayModel';

export class PersonaRouter {

  // ═══════════════════════════════════════════
  // 根据关系层级获取情感参数
  // ═══════════════════════════════════════════
  static getEmotionForRelationship(relationship: RelationshipLevel): EmotionProfile {
    return RELATIONSHIP_EMOTION_MAP[relationship];
  }

  // ═══════════════════════════════════════════
  // 根据祝福风格获取人格
  // ═══════════════════════════════════════════
  static getPersonaByBlessingStyle(style: BlessingStyle): PersonaID {
    const role = Object.values(PERSONA_ROLES).find(r => r.blessingStyle === style);
    return role ? role.persona : PersonaID.BAOBAO;
  }

  // ═══════════════════════════════════════════
  // 根据任务类型路由人格
  // ═══════════════════════════════════════════
  static routeForTask(task: string, member?: TeamMember): {
    primary: PersonaID;
    secondary: PersonaID[];
    emotion: EmotionProfile;
    reason: string;
  } {
    // 有成员信息 → 根据关系层级路由
    if (member) {
      return this.routeForMember(member);
    }

    // 通用任务路由
    const taskLower = task.toLowerCase();

    if (taskLower.includes('祝福') || taskLower.includes('贺卡') || taskLower.includes('诗歌')) {
      return {
        primary: PersonaID.LIBAI,
        secondary: [PersonaID.SUDONGPO, PersonaID.BAOBAO],
        emotion: RELATIONSHIP_EMOTION_MAP[RelationshipLevel.CLOSE_COLLEAGUE],
        reason: '诗意祝福任务 → 路由李白主笔'
      };
    }

    if (taskLower.includes('导入') || taskLower.includes('导出') || taskLower.includes('格式化')) {
      return {
        primary: PersonaID.CANGJIE,
        secondary: [PersonaID.LUBAN, PersonaID.BAOBAO],
        emotion: RELATIONSHIP_EMOTION_MAP[RelationshipLevel.REGULAR_COLLEAGUE],
        reason: '数据处理任务 → 路由仓颉'
      };
    }

    if (taskLower.includes('通知') || taskLower.includes('提醒') || taskLower.includes('定时')) {
      return {
        primary: PersonaID.LUBAN,
        secondary: [PersonaID.BAOBAO, PersonaID.WENWEN],
        emotion: RELATIONSHIP_EMOTION_MAP[RelationshipLevel.REGULAR_COLLEAGUE],
        reason: '自动化任务 → 路由鲁班'
      };
    }

    if (taskLower.includes('审计') || taskLower.includes('检查') || taskLower.includes('安全')) {
      return {
        primary: PersonaID.GODSEYE,
        secondary: [PersonaID.JIANGZIYA, PersonaID.LONGDUN],
        emotion: { mode: EmotionMode.NEUTRAL, empathy: 0.1, warmth: 0.0, boundary: 0.95, formality: 0.9, personaPrimary: PersonaID.GODSEYE, personaSecondary: [] },
        reason: '审计任务 → 路由上帝之眼'
      };
    }

    if (taskLower.includes('统计') || taskLower.includes('分析') || taskLower.includes('报告')) {
      return {
        primary: PersonaID.ZHUGELIANG,
        secondary: [PersonaID.MATHMASTER, PersonaID.BAOBAO],
        emotion: RELATIONSHIP_EMOTION_MAP[RelationshipLevel.LEADER],
        reason: '分析任务 → 路由诸葛亮'
      };
    }

    // 默认 → 宝宝
    return {
      primary: PersonaID.BAOBAO,
      secondary: [PersonaID.WENWEN, PersonaID.LUBAN],
      emotion: RELATIONSHIP_EMOTION_MAP[RelationshipLevel.TEAM_MATE],
      reason: '默认任务 → 路由宝宝(龍芯修复师)'
    };
  }

  // ═══════════════════════════════════════════
  // 根据成员关系层级路由
  // ═══════════════════════════════════════════
  static routeForMember(member: TeamMember): {
    primary: PersonaID;
    secondary: PersonaID[];
    emotion: EmotionProfile;
    reason: string;
  } {
    const emotion = RELATIONSHIP_EMOTION_MAP[member.relationship];

    // 如果成员有偏好人格，优先使用
    if (member.preferredBlessingPersona) {
      const role = PERSONA_ROLES[member.preferredBlessingPersona];
      return {
        primary: member.preferredBlessingPersona,
        secondary: emotion.personaSecondary,
        emotion,
        reason: `成员偏好人格: ${role.name}`
      };
    }

    return {
      primary: emotion.personaPrimary,
      secondary: emotion.personaSecondary,
      emotion,
      reason: `关系层级路由: ${member.getRelationshipLabel()} → ${PERSONA_ROLES[emotion.personaPrimary].name}`
    };
  }

  // ═══════════════════════════════════════════
  // 获取人格角色详情
  // ═══════════════════════════════════════════
  static getPersonaRole(persona: PersonaID): PersonaRole | undefined {
    return PERSONA_ROLES[persona];
  }

  // ═══════════════════════════════════════════
  // 获取全部可激活人格列表
  // ═══════════════════════════════════════════
  static getAllActivePersonaIds(): PersonaID[] {
    return [
      PersonaID.BAOBAO, PersonaID.LIBAI, PersonaID.LUBAN,
      PersonaID.ZHUGELIANG, PersonaID.SUDONGPO, PersonaID.CANGJIE,
      PersonaID.GODSEYE, PersonaID.GUANZHONG, PersonaID.WENWEN,
      PersonaID.JIANGZIYA
    ];
  }

  // ═══════════════════════════════════════════
  // 人格功能摘要（仪表盘用）
  // ═══════════════════════════════════════════
  static getPersonaDashboard(): { persona: PersonaID; name: string; icon: string; active: boolean }[] {
    return this.getAllActivePersonaIds().map(p => {
      const role = PERSONA_ROLES[p];
      return {
        persona: p,
        name: role?.name || p,
        icon: role?.icon || '🤖',
        active: true
      };
    });
  }
}

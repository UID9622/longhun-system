/*
 * ==========================================================================
 * 龍魂 · 生日数据模型
 * DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-BIRTHDAY-MODEL-v2.0
 * ==========================================================================
 * 增强：关系层级 + 人格路由 + 情感参数 + DNA签名 + 农历支持
 */

import {
  BirthdayType,
  RelationshipLevel,
  PersonaID,
  EmotionMode,
  MASTER_DNA,
  MASTER_UID,
  TIAN_GAN,
  DI_ZHI,
  SHENG_XIAO
} from '../common/types';
import { LunarEngine } from '../engines/LunarEngine';

// ═══════════════════════════════════════════════
// 团队成员档案（增强版）
// ═══════════════════════════════════════════════
@Observed
export class TeamMember {
  id: string;
  name: string;
  avatar: Resource | string;
  birthdayType: BirthdayType;
  birthdayMonth: number;
  birthdayDay: number;
  birthYear: number;
  department: string;
  role: string;
  phone: string;
  email: string;
  tags: string[];

  // ── 新增：情感协议联动字段 ──
  relationship: RelationshipLevel;         // 关系层级
  preferredBlessingPersona: PersonaID;     // 偏好祝福人格
  emotionMode: EmotionMode;                // 当前激活情感模式
  personalNotes: string;                   // 个人备注
  zodiacSign: string;                      // 生肖（自动推算）
  tianganDizhi: string;                    // 天干地支（自动推算）

  // ── DNA 签名 ──
  dnaSignature: string;
  createdAt: number;
  updatedAt: number;

  constructor(data?: Partial<TeamMember>) {
    const now = Date.now();
    this.id = data?.id || this.generateId();
    this.name = data?.name || '';
    this.avatar = data?.avatar || $r('app.media.default_avatar');
    this.birthdayType = data?.birthdayType || BirthdayType.SOLAR;
    this.birthdayMonth = data?.birthdayMonth || 1;
    this.birthdayDay = data?.birthdayDay || 1;
    this.birthYear = data?.birthYear || 0;
    this.department = data?.department || '未分配';
    this.role = data?.role || '成员';
    this.phone = data?.phone || '';
    this.email = data?.email || '';
    this.tags = data?.tags || [];

    this.relationship = data?.relationship || RelationshipLevel.REGULAR_COLLEAGUE;
    this.preferredBlessingPersona = data?.preferredBlessingPersona || PersonaID.BAOBAO;
    this.emotionMode = data?.emotionMode || EmotionMode.NEUTRAL;
    this.personalNotes = data?.personalNotes || '';

    // 自动推算生肖和干支
    if (this.birthYear > 0) {
      this.zodiacSign = SHENG_XIAO[(this.birthYear - 4) % 12];
      this.tianganDizhi = `${TIAN_GAN[(this.birthYear - 4) % 10]}${DI_ZHI[(this.birthYear - 4) % 12]}`;
    } else {
      this.zodiacSign = '未知';
      this.tianganDizhi = '未知';
    }

    this.createdAt = data?.createdAt || now;
    this.updatedAt = now;
    this.dnaSignature = this.signData();
  }

  private generateId(): string {
    const ts = Date.now().toString(36).slice(-6);
    const rnd = Math.random().toString(36).substring(2, 6);
    return `LH-MBR-${MASTER_UID.slice(-4)}-${ts}-${rnd}`;
  }

  private signData(): string {
    const payload = `${MASTER_DNA}|${this.id}|${this.name}|${this.birthdayMonth}|${this.birthdayDay}`;
    let hash = 0;
    for (let i = 0; i < payload.length; i++) {
      const chr = payload.charCodeAt(i);
      hash = ((hash << 5) - hash) + chr;
      hash |= 0;
    }
    return `SM3-${Math.abs(hash).toString(16).padStart(8, '0')}`;
  }

  // ── 获取下一个生日（日期对象） ──
  getNextBirthday(): Date {
    const now = new Date();
    const currentYear = now.getFullYear();

    if (this.birthdayType === BirthdayType.SOLAR) {
      let next = new Date(currentYear, this.birthdayMonth - 1, this.birthdayDay);
      if (next <= now) {
        next = new Date(currentYear + 1, this.birthdayMonth - 1, this.birthdayDay);
      }
      return next;
    } else {
      return LunarEngine.lunarToSolarNext(currentYear, this.birthdayMonth, this.birthdayDay);
    }
  }

  // ── 获取下一个生日（格式化字符串） ──
  getNextBirthdayString(): string {
    const d = this.getNextBirthday();
    return `${d.getFullYear()}-${(d.getMonth() + 1).toString().padStart(2, '0')}-${d.getDate().toString().padStart(2, '0')}`;
  }

  // ── 生日倒计时天数 ──
  getDaysUntilBirthday(): number {
    const next = this.getNextBirthday();
    const now = new Date();
    now.setHours(0, 0, 0, 0);
    const diff = next.getTime() - now.getTime();
    return Math.ceil(diff / (1000 * 60 * 60 * 24));
  }

  // ── 今天是否生日 ──
  isBirthdayToday(): boolean {
    const now = new Date();
    // 农历生日需要用农历引擎判断
    if (this.birthdayType === BirthdayType.LUNAR) {
      return LunarEngine.isLunarBirthdayToday(this.birthdayMonth, this.birthdayDay);
    }
    return now.getMonth() === this.birthdayMonth - 1 && now.getDate() === this.birthdayDay;
  }

  // ── 计算年龄 ──
  getAge(): number {
    if (this.birthYear <= 0) return 0;
    const now = new Date();
    let age = now.getFullYear() - this.birthYear;
    const bday = new Date(now.getFullYear(), this.birthdayMonth - 1, this.birthdayDay);
    if (now < bday) age--;
    return age;
  }

  // ── 关系中文标签 ──
  getRelationshipLabel(): string {
    const labels: Record<RelationshipLevel, string> = {
      [RelationshipLevel.CLOSE_COLLEAGUE]: '密友',
      [RelationshipLevel.REGULAR_COLLEAGUE]: '同事',
      [RelationshipLevel.LEADER]: '领导',
      [RelationshipLevel.TEAM_MATE]: '队友',
      [RelationshipLevel.EXTERNAL]: '伙伴'
    };
    return labels[this.relationship] || '同事';
  }

  // ── 通知优先级 ──
  getNotificationPriority(): 'high' | 'medium' | 'low' {
    const days = this.getDaysUntilBirthday();
    if (days === 0) return 'high';
    if (days <= 7) return 'medium';
    return 'low';
  }

  // ── 克隆 ──
  clone(overrides?: Partial<TeamMember>): TeamMember {
    return new TeamMember({ ...this, ...overrides, id: this.id });
  }
}

// ═══════════════════════════════════════════════
// 团队状态管理（增强版）
// ═══════════════════════════════════════════════
@Observed
export class TeamState {
  members: TeamMember[] = [];
  filterDepartment: string = '全部';
  filterRelationship: string = '全部';
  filterTag: string = '';
  sortBy: 'date' | 'name' | 'department' | 'relationship' = 'date';
  searchQuery: string = '';

  // ── 人格路由状态 ──
  activePersona: PersonaID = PersonaID.BAOBAO;
  personaHistory: { persona: PersonaID; task: string; timestamp: number }[] = [];
  dnaChain: string[] = [];  // 操作DNA链

  // ── 派生数据：过滤排序后的成员 ──
  get filteredMembers(): TeamMember[] {
    let result = [...this.members];

    if (this.filterDepartment !== '全部') {
      result = result.filter(m => m.department === this.filterDepartment);
    }
    if (this.filterRelationship !== '全部') {
      result = result.filter(m => m.relationship === this.filterRelationship);
    }
    if (this.filterTag) {
      result = result.filter(m => m.tags.includes(this.filterTag));
    }
    if (this.searchQuery) {
      const q = this.searchQuery.toLowerCase();
      result = result.filter(m =>
        m.name.toLowerCase().includes(q) ||
        m.department.toLowerCase().includes(q) ||
        m.role.toLowerCase().includes(q) ||
        m.tags.some(t => t.toLowerCase().includes(q))
      );
    }

    // 排序
    switch (this.sortBy) {
      case 'date':
        result.sort((a, b) => a.getDaysUntilBirthday() - b.getDaysUntilBirthday());
        break;
      case 'name':
        result.sort((a, b) => a.name.localeCompare(b.name, 'zh-CN'));
        break;
      case 'department':
        result.sort((a, b) => a.department.localeCompare(b.department, 'zh-CN'));
        break;
      case 'relationship':
        const relOrder: Record<string, number> = { close: 1, mate: 2, regular: 3, leader: 4, external: 5 };
        result.sort((a, b) => (relOrder[a.relationship] || 9) - (relOrder[b.relationship] || 9));
        break;
    }

    return result;
  }

  // ── 即将过生日（7天内） ──
  get upcomingBirthdays(): TeamMember[] {
    return this.members.filter(m => {
      const d = m.getDaysUntilBirthday();
      return d >= 0 && d <= 7;
    });
  }

  // ── 今天过生日 ──
  get todayBirthdays(): TeamMember[] {
    return this.members.filter(m => m.isBirthdayToday());
  }

  // ── 本月生日 ──
  get thisMonthBirthdays(): TeamMember[] {
    const now = new Date();
    return this.members.filter(m => m.birthdayMonth === now.getMonth() + 1);
  }

  // ── 部门列表 ──
  get departments(): string[] {
    const deps = new Set(this.members.map(m => m.department));
    return ['全部', ...Array.from(deps).sort()];
  }

  // ── 关系类型列表 ──
  get relationshipTypes(): { value: string; label: string }[] {
    return [
      { value: '全部', label: '全部关系' },
      { value: 'close', label: '密友' },
      { value: 'mate', label: '队友' },
      { value: 'regular', label: '同事' },
      { value: 'leader', label: '领导' },
      { value: 'external', label: '伙伴' }
    ];
  }

  // ── 所有标签 ──
  get allTags(): string[] {
    const tags = new Set<string>();
    this.members.forEach(m => m.tags.forEach(t => tags.add(t)));
    return Array.from(tags).sort();
  }

  // ── 成员统计 ──
  get stats(): { total: number; today: number; week: number; month: number; departments: number } {
    const now = new Date();
    const thisMonth = now.getMonth() + 1;
    return {
      total: this.members.length,
      today: this.members.filter(m => m.isBirthdayToday()).length,
      week: this.members.filter(m => m.getDaysUntilBirthday() <= 7).length,
      month: this.members.filter(m => m.birthdayMonth === thisMonth).length,
      departments: new Set(this.members.map(m => m.department)).size
    };
  }

  // ── CRUD 操作 ──
  addMember(member: TeamMember): string {
    this.members.push(member);
    this.recordOperation('ADD', member.id, PersonaID.BAOBAO);
    return member.id;
  }

  removeMember(id: string): boolean {
    const idx = this.members.findIndex(m => m.id === id);
    if (idx >= 0) {
      const name = this.members[idx].name;
      this.members.splice(idx, 1);
      this.recordOperation('DELETE', id, PersonaID.BAOBAO, name);
      return true;
    }
    return false;
  }

  updateMember(id: string, data: Partial<TeamMember>): boolean {
    const idx = this.members.findIndex(m => m.id === id);
    if (idx >= 0) {
      const old = this.members[idx];
      this.members[idx] = old.clone(data);
      this.recordOperation('UPDATE', id, PersonaID.BAOBAO, old.name);
      return true;
    }
    return false;
  }

  findMember(id: string): TeamMember | undefined {
    return this.members.find(m => m.id === id);
  }

  // ── 人格切换 ──
  switchPersona(persona: PersonaID, reason: string): void {
    this.personaHistory.push({ persona, task: reason, timestamp: Date.now() });
    this.activePersona = persona;
  }

  // ── 操作记录 ──
  private recordOperation(action: string, targetId: string, persona: PersonaID, detail: string = ''): void {
    const dna = `${MASTER_DNA}|${action}|${targetId}|${Date.now()}`;
    this.dnaChain.push(dna.slice(-32));
    if (this.dnaChain.length > 100) this.dnaChain.shift(); // 保留最近100条
  }
}

// ═══════════════════════════════════════════════
// 全局单例
// ═══════════════════════════════════════════════
export const teamState = new TeamState();

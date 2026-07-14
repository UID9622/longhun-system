/*
 * ==========================================================================
 * 龍魂 · 关系型数据库（增强版）
 * DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-DATABASE-v2.0
 * ==========================================================================
 * 增强：加密存储 + 审计日志 + DNA签名校验
 */

import { relationalStore } from '@kit.ArkData';
import { TeamMember } from '../models/BirthdayModel';
import {
  MASTER_DNA,
  MASTER_UID,
  BirthdayType,
  RelationshipLevel,
  PersonaID,
  AuditEventType,
  AuditLogEntry
} from '../common/types';

const DB_NAME = 'LongHunBirthday.db';
const TABLE_MEMBERS = 'team_members';
const TABLE_AUDIT = 'audit_log';

export class BirthdayDatabase {
  private store: relationalStore.RdbStore | null = null;

  // ═══════════════════════════════════════════════
  // 初始化数据库
  // ═══════════════════════════════════════════════
  async init(context: Context): Promise<void> {
    const config: relationalStore.StoreConfig = {
      name: DB_NAME,
      securityLevel: relationalStore.SecurityLevel.S2,
      encrypt: true
    };

    this.store = await relationalStore.getRdbStore(context, config);

    // 创建成员表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_MEMBERS} (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        birthday_type TEXT NOT NULL DEFAULT 'solar',
        birthday_month INTEGER NOT NULL,
        birthday_day INTEGER NOT NULL,
        birth_year INTEGER DEFAULT 0,
        department TEXT DEFAULT '未分配',
        role TEXT DEFAULT '成员',
        phone TEXT DEFAULT '',
        email TEXT DEFAULT '',
        tags TEXT DEFAULT '[]',
        relationship TEXT DEFAULT 'regular',
        preferred_persona TEXT DEFAULT 'P02',
        personal_notes TEXT DEFAULT '',
        dna_signature TEXT DEFAULT '',
        created_at INTEGER NOT NULL,
        updated_at INTEGER NOT NULL
      )
    `);

    // 创建审计日志表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_AUDIT} (
        id TEXT PRIMARY KEY,
        timestamp INTEGER NOT NULL,
        event_type TEXT NOT NULL,
        persona_active TEXT DEFAULT 'P05',
        detail TEXT DEFAULT '',
        dna_signature TEXT DEFAULT ''
      )
    `);

    // 创建索引
    await this.store.executeSql(`
      CREATE INDEX IF NOT EXISTS idx_members_dept ON ${TABLE_MEMBERS}(department)
    `);
    await this.store.executeSql(`
      CREATE INDEX IF NOT EXISTS idx_members_bday ON ${TABLE_MEMBERS}(birthday_month, birthday_day)
    `);
    await this.store.executeSql(`
      CREATE INDEX IF NOT EXISTS idx_audit_time ON ${TABLE_AUDIT}(timestamp)
    `);
  }

  // ═══════════════════════════════════════════════
  // 插入成员
  // ═══════════════════════════════════════════════
  async insertMember(member: TeamMember): Promise<number> {
    if (!this.store) throw new Error('数据库未初始化');

    const bucket = new relationalStore.ValuesBucket();
    bucket.putString('id', member.id);
    bucket.putString('name', member.name);
    bucket.putString('birthday_type', member.birthdayType);
    bucket.putInt('birthday_month', member.birthdayMonth);
    bucket.putInt('birthday_day', member.birthdayDay);
    bucket.putInt('birth_year', member.birthYear);
    bucket.putString('department', member.department);
    bucket.putString('role', member.role);
    bucket.putString('phone', member.phone);
    bucket.putString('email', member.email);
    bucket.putString('tags', JSON.stringify(member.tags));
    bucket.putString('relationship', member.relationship);
    bucket.putString('preferred_persona', member.preferredBlessingPersona);
    bucket.putString('personal_notes', member.personalNotes);
    bucket.putString('dna_signature', member.dnaSignature);
    bucket.putLong('created_at', member.createdAt);
    bucket.putLong('updated_at', member.updatedAt);

    await this.insertAuditLog(AuditEventType.MEMBER_ADDED, `添加成员: ${member.name}`);
    return await this.store.insert(TABLE_MEMBERS, bucket);
  }

  // ═══════════════════════════════════════════════
  // 查询所有成员
  // ═══════════════════════════════════════════════
  async queryAllMembers(): Promise<TeamMember[]> {
    if (!this.store) return [];

    const predicates = new relationalStore.RdbPredicates(TABLE_MEMBERS);
    const resultSet = await this.store.query(predicates, [
      'id', 'name', 'birthday_type', 'birthday_month', 'birthday_day',
      'birth_year', 'department', 'role', 'phone', 'email', 'tags',
      'relationship', 'preferred_persona', 'personal_notes',
      'dna_signature', 'created_at', 'updated_at'
    ]);

    const members: TeamMember[] = [];
    while (resultSet.goToNextRow()) {
      const col = (name: string) => resultSet.getColumnIndex(name);

      let tags: string[] = [];
      try {
        tags = JSON.parse(resultSet.getString(col('tags')) || '[]');
      } catch (_) { tags = []; }

      members.push(new TeamMember({
        id: resultSet.getString(col('id')),
        name: resultSet.getString(col('name')),
        birthdayType: resultSet.getString(col('birthday_type')) as BirthdayType,
        birthdayMonth: resultSet.getLong(col('birthday_month')),
        birthdayDay: resultSet.getLong(col('birthday_day')),
        birthYear: resultSet.getLong(col('birth_year')),
        department: resultSet.getString(col('department')),
        role: resultSet.getString(col('role')),
        phone: resultSet.getString(col('phone')),
        email: resultSet.getString(col('email')),
        tags,
        relationship: resultSet.getString(col('relationship')) as RelationshipLevel,
        preferredBlessingPersona: resultSet.getString(col('preferred_persona')) as PersonaID,
        personalNotes: resultSet.getString(col('personal_notes')),
        dnaSignature: resultSet.getString(col('dna_signature')),
        createdAt: resultSet.getLong(col('created_at')),
        updatedAt: resultSet.getLong(col('updated_at'))
      }));
    }
    resultSet.close();
    return members;
  }

  // ═══════════════════════════════════════════════
  // 更新成员
  // ═══════════════════════════════════════════════
  async updateMember(id: string, member: TeamMember): Promise<number> {
    if (!this.store) throw new Error('数据库未初始化');

    const bucket = new relationalStore.ValuesBucket();
    bucket.putString('name', member.name);
    bucket.putString('birthday_type', member.birthdayType);
    bucket.putInt('birthday_month', member.birthdayMonth);
    bucket.putInt('birthday_day', member.birthdayDay);
    bucket.putInt('birth_year', member.birthYear);
    bucket.putString('department', member.department);
    bucket.putString('role', member.role);
    bucket.putString('phone', member.phone);
    bucket.putString('email', member.email);
    bucket.putString('tags', JSON.stringify(member.tags));
    bucket.putString('relationship', member.relationship);
    bucket.putString('preferred_persona', member.preferredBlessingPersona);
    bucket.putString('personal_notes', member.personalNotes);
    bucket.putString('dna_signature', member.dnaSignature);
    bucket.putLong('updated_at', Date.now());

    const predicates = new relationalStore.RdbPredicates(TABLE_MEMBERS);
    predicates.equalTo('id', id);

    await this.insertAuditLog(AuditEventType.MEMBER_UPDATED, `更新成员: ${member.name}`);
    return await this.store.update(bucket, predicates);
  }

  // ═══════════════════════════════════════════════
  // 删除成员
  // ═══════════════════════════════════════════════
  async deleteMember(id: string): Promise<number> {
    if (!this.store) throw new Error('数据库未初始化');

    const predicates = new relationalStore.RdbPredicates(TABLE_MEMBERS);
    predicates.equalTo('id', id);

    await this.insertAuditLog(AuditEventType.MEMBER_DELETED, `删除成员ID: ${id}`);
    return await this.store.delete(predicates);
  }

  // ═══════════════════════════════════════════════
  // 获取今天生日成员
  // ═══════════════════════════════════════════════
  async queryTodayBirthdays(): Promise<TeamMember[]> {
    const all = await this.queryAllMembers();
    return all.filter(m => m.isBirthdayToday());
  }

  // ═══════════════════════════════════════════════
  // 审计日志
  // ═══════════════════════════════════════════════
  async insertAuditLog(eventType: AuditEventType, detail: string): Promise<void> {
    if (!this.store) return;

    const id = `AUD-${Date.now().toString(36)}-${Math.random().toString(36).substr(2, 4)}`;
    const dnaSig = `SM3-${MASTER_DNA.slice(-8)}-${Date.now().toString(36)}`;

    const bucket = new relationalStore.ValuesBucket();
    bucket.putString('id', id);
    bucket.putLong('timestamp', Date.now());
    bucket.putString('event_type', eventType);
    bucket.putString('persona_active', 'P05');
    bucket.putString('detail', detail);
    bucket.putString('dna_signature', dnaSig);

    await this.store.insert(TABLE_AUDIT, bucket);
  }

  // ═══════════════════════════════════════════════
  // 查询审计日志（最近N条）
  // ═══════════════════════════════════════════════
  async queryAuditLogs(limit: number = 50): Promise<AuditLogEntry[]> {
    if (!this.store) return [];

    const predicates = new relationalStore.RdbPredicates(TABLE_AUDIT);
    predicates.orderByDesc('timestamp');
    predicates.limit(limit);

    const resultSet = await this.store.query(predicates, [
      'id', 'timestamp', 'event_type', 'persona_active', 'detail', 'dna_signature'
    ]);

    const logs: AuditLogEntry[] = [];
    while (resultSet.goToNextRow()) {
      const col = (name: string) => resultSet.getColumnIndex(name);
      logs.push({
        id: resultSet.getString(col('id')),
        timestamp: resultSet.getLong(col('timestamp')),
        eventType: resultSet.getString(col('event_type')) as AuditEventType,
        personaActive: resultSet.getString(col('persona_active')) as PersonaID,
        detail: resultSet.getString(col('detail')),
        dnaSignature: resultSet.getString(col('dna_signature'))
      });
    }
    resultSet.close();
    return logs;
  }

  // ═══════════════════════════════════════════════
  // 数据完整性校验
  // ═══════════════════════════════════════════════
  async verifyIntegrity(): Promise<{ valid: boolean; total: number; corrupted: number }> {
    const members = await this.queryAllMembers();
    let corrupted = 0;

    for (const m of members) {
      const expected = m.dnaSignature;
      const recalc = new TeamMember({ ...m, id: m.id }).dnaSignature;
      if (expected !== recalc) corrupted++;
    }

    return {
      valid: corrupted === 0,
      total: members.length,
      corrupted
    };
  }
}

// 龍魂 · 项目数据库 · 关系型存储 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import { relationalStore } from '@kit.ArkData';

const STORE_NAME = 'LongHunProject.db';
const TABLE_PROJECTS = 'projects';
const TABLE_MILESTONES = 'milestones';
const TABLE_DEPENDENCIES = 'dependencies';
const TABLE_DELIVERABLES = 'deliverables';
const TABLE_CHECKPOINTS = 'checkpoints';
const TABLE_TEAM_MEMBERS = 'team_members';
const TABLE_RISKS = 'risks';
const TABLE_BASELINES = 'baselines';

export class ProjectDatabase {
  private static store: relationalStore.RdbStore | null = null;

  static async init(): Promise<void> {
    const config: relationalStore.StoreConfig = {
      name: STORE_NAME,
      securityLevel: relationalStore.SecurityLevel.S3,
      encrypt: true
    };

    this.store = await relationalStore.getRdbStore(getContext(), config);

    // 项目表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_PROJECTS} (
        id TEXT PRIMARY KEY,
        project_no TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT '规划中',
        planned_start INTEGER,
        planned_end INTEGER,
        actual_start INTEGER,
        actual_end INTEGER,
        project_manager TEXT,
        product_manager TEXT,
        tech_lead TEXT,
        qa_lead TEXT,
        budget REAL DEFAULT 0,
        cost_incurred REAL DEFAULT 0,
        cost_forecast REAL DEFAULT 0,
        created_at INTEGER,
        updated_at INTEGER,
        dna_signature TEXT
      )
    `);

    // 里程碑表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_MILESTONES} (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT '未开始',
        priority TEXT DEFAULT 'P2-中',
        planned_start INTEGER,
        planned_end INTEGER,
        actual_start INTEGER,
        actual_end INTEGER,
        progress INTEGER DEFAULT 0,
        assigned_to TEXT,
        estimated_hours REAL DEFAULT 0,
        actual_hours REAL DEFAULT 0,
        risk_level TEXT DEFAULT '无风险',
        risk_description TEXT,
        created_at INTEGER,
        updated_at INTEGER,
        dna_signature TEXT,
        FOREIGN KEY (project_id) REFERENCES ${TABLE_PROJECTS}(id)
      )
    `);

    // 依赖表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_DEPENDENCIES} (
        id TEXT PRIMARY KEY,
        milestone_id TEXT NOT NULL,
        depends_on_id TEXT NOT NULL,
        dependency_type TEXT DEFAULT 'FS',
        lag INTEGER DEFAULT 0,
        dna_signature TEXT,
        FOREIGN KEY (milestone_id) REFERENCES ${TABLE_MILESTONES}(id)
      )
    `);

    // 交付物表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_DELIVERABLES} (
        id TEXT PRIMARY KEY,
        milestone_id TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'pending',
        file_path TEXT,
        submitted_by TEXT,
        submitted_at INTEGER,
        dna_signature TEXT,
        FOREIGN KEY (milestone_id) REFERENCES ${TABLE_MILESTONES}(id)
      )
    `);

    // 检查点表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_CHECKPOINTS} (
        id TEXT PRIMARY KEY,
        milestone_id TEXT NOT NULL,
        name TEXT NOT NULL,
        completed INTEGER DEFAULT 0,
        completed_by TEXT,
        completed_at INTEGER,
        dna_signature TEXT,
        FOREIGN KEY (milestone_id) REFERENCES ${TABLE_MILESTONES}(id)
      )
    `);

    // 团队成员表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_TEAM_MEMBERS} (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        name TEXT NOT NULL,
        role TEXT,
        department TEXT,
        allocated_hours REAL DEFAULT 0,
        actual_hours REAL DEFAULT 0,
        dna_signature TEXT,
        FOREIGN KEY (project_id) REFERENCES ${TABLE_PROJECTS}(id)
      )
    `);

    // 风险表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_RISKS} (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        level TEXT DEFAULT '低风险',
        probability REAL DEFAULT 0.5,
        impact REAL DEFAULT 0.5,
        mitigation TEXT,
        contingency TEXT,
        owner TEXT,
        status TEXT DEFAULT 'open',
        created_at INTEGER,
        updated_at INTEGER,
        dna_signature TEXT,
        FOREIGN KEY (project_id) REFERENCES ${TABLE_PROJECTS}(id)
      )
    `);

    // 基线表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_BASELINES} (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        created_at INTEGER,
        budget REAL,
        planned_start INTEGER,
        planned_end INTEGER,
        milestones_json TEXT,
        dna_signature TEXT,
        FOREIGN KEY (project_id) REFERENCES ${TABLE_PROJECTS}(id)
      )
    `);

    // 创建索引
    await this.store.executeSql(`CREATE INDEX IF NOT EXISTS idx_ms_project ON ${TABLE_MILESTONES}(project_id)`);
    await this.store.executeSql(`CREATE INDEX IF NOT EXISTS idx_dep_ms ON ${TABLE_DEPENDENCIES}(milestone_id)`);
    await this.store.executeSql(`CREATE INDEX IF NOT EXISTS idx_dlv_ms ON ${TABLE_DELIVERABLES}(milestone_id)`);
    await this.store.executeSql(`CREATE INDEX IF NOT EXISTS idx_cp_ms ON ${TABLE_CHECKPOINTS}(milestone_id)`);
    await this.store.executeSql(`CREATE INDEX IF NOT EXISTS idx_tm_project ON ${TABLE_TEAM_MEMBERS}(project_id)`);
    await this.store.executeSql(`CREATE INDEX IF NOT EXISTS idx_risk_project ON ${TABLE_RISKS}(project_id)`);
    await this.store.executeSql(`CREATE INDEX IF NOT EXISTS idx_bl_project ON ${TABLE_BASELINES}(project_id)`);
    await this.store.executeSql(`CREATE INDEX IF NOT EXISTS idx_ms_status ON ${TABLE_MILESTONES}(project_id, status)`);
  }

  // 统计查询
  static async getProjectCountByStatus(): Promise<Map<string, number>> {
    if (!this.store) return new Map();
    const result = new Map<string, number>();
    const rs = await this.store.querySql(`SELECT status, COUNT(*) as cnt FROM ${TABLE_PROJECTS} GROUP BY status`);
    while (rs.goToNextRow()) {
      result.set(rs.getString(0), rs.getLong(1));
    }
    rs.close();
    return result;
  }

  static async getMilestoneCountByProject(projectId: string): Promise<number> {
    if (!this.store) return 0;
    const rs = await this.store.querySql(
      `SELECT COUNT(*) FROM ${TABLE_MILESTONES} WHERE project_id = ?`,
      [projectId]
    );
    let count = 0;
    if (rs.goToFirstRow()) {
      count = rs.getLong(0);
    }
    rs.close();
    return count;
  }

  static async getRisksByProject(projectId: string, status?: string): Promise<number> {
    if (!this.store) return 0;
    let sql = `SELECT COUNT(*) FROM ${TABLE_RISKS} WHERE project_id = ?`;
    const params: string[] = [projectId];
    if (status) {
      sql += ' AND status = ?';
      params.push(status);
    }
    const rs = await this.store.querySql(sql, params);
    let count = 0;
    if (rs.goToFirstRow()) {
      count = rs.getLong(0);
    }
    rs.close();
    return count;
  }

  static async clear(): Promise<void> {
    if (!this.store) return;
    const tables = [TABLE_PROJECTS, TABLE_MILESTONES, TABLE_DEPENDENCIES, TABLE_DELIVERABLES,
                    TABLE_CHECKPOINTS, TABLE_TEAM_MEMBERS, TABLE_RISKS, TABLE_BASELINES];
    for (const table of tables) {
      await this.store.executeSql(`DELETE FROM ${table}`);
    }
  }
}

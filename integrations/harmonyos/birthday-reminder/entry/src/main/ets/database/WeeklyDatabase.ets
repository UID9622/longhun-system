// entry/src/main/ets/database/WeeklyDatabase.ets
// 龍魂 · 周报数据库 · ArkTS

import relationalStore from '@ohos.data.relationalStore';
import { BusinessError } from '@ohos.base';

const DB_NAME = 'LongHunWeekly.db';
const DB_VERSION = 1;

const STORE_CONFIG: relationalStore.StoreConfig = {
  name: DB_NAME,
  securityLevel: relationalStore.SecurityLevel.S3
};

// === 建表SQL ===
const CREATE_TABLE_WEEKLY_REPORTS = `CREATE TABLE IF NOT EXISTS weekly_reports (
  id TEXT PRIMARY KEY,
  report_no TEXT UNIQUE NOT NULL,
  week_start INTEGER NOT NULL,
  week_end INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT '草稿',
  reporter TEXT NOT NULL,
  reporter_id TEXT NOT NULL,
  department TEXT,
  position TEXT,
  total_planned_hours REAL DEFAULT 0,
  total_actual_hours REAL DEFAULT 0,
  total_overtime_hours REAL DEFAULT 0,
  completion_rate INTEGER DEFAULT 0,
  summary TEXT,
  next_plan TEXT,
  need_support TEXT,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  submitted_at INTEGER,
  approved_at INTEGER,
  dna_signature TEXT
)`;

const CREATE_TABLE_WEEKLY_TASKS = `CREATE TABLE IF NOT EXISTS weekly_tasks (
  id TEXT PRIMARY KEY,
  report_id TEXT NOT NULL,
  project_id TEXT,
  project_name TEXT,
  task_type TEXT NOT NULL DEFAULT '其他',
  priority TEXT NOT NULL DEFAULT 'P2-中',
  status TEXT NOT NULL DEFAULT '未开始',
  title TEXT NOT NULL,
  description TEXT,
  planned_hours REAL DEFAULT 0,
  actual_hours REAL DEFAULT 0,
  overtime_hours REAL DEFAULT 0,
  progress INTEGER DEFAULT 0,
  planned_start INTEGER NOT NULL,
  planned_end INTEGER NOT NULL,
  actual_start INTEGER,
  actual_end INTEGER,
  milestone_id TEXT,
  deliverables TEXT,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  dna_signature TEXT,
  FOREIGN KEY (report_id) REFERENCES weekly_reports(id)
)`;

const CREATE_TABLE_NEXT_TASKS = `CREATE TABLE IF NOT EXISTS next_tasks (
  id TEXT PRIMARY KEY,
  report_id TEXT NOT NULL,
  project_id TEXT,
  project_name TEXT,
  task_type TEXT NOT NULL DEFAULT '其他',
  priority TEXT NOT NULL DEFAULT 'P2-中',
  title TEXT NOT NULL,
  description TEXT,
  planned_hours REAL DEFAULT 0,
  planned_start INTEGER NOT NULL,
  planned_end INTEGER NOT NULL,
  dependencies TEXT,
  dna_signature TEXT,
  FOREIGN KEY (report_id) REFERENCES weekly_reports(id)
)`;

const CREATE_TABLE_WEEKLY_ISSUES = `CREATE TABLE IF NOT EXISTS weekly_issues (
  id TEXT PRIMARY KEY,
  report_id TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  severity TEXT NOT NULL DEFAULT 'medium',
  status TEXT NOT NULL DEFAULT 'open',
  related_task_id TEXT,
  solution TEXT,
  resolver TEXT,
  resolved_at INTEGER,
  dna_signature TEXT,
  FOREIGN KEY (report_id) REFERENCES weekly_reports(id)
)`;

const CREATE_TABLE_WEEKLY_RISKS = `CREATE TABLE IF NOT EXISTS weekly_risks (
  id TEXT PRIMARY KEY,
  report_id TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  probability REAL DEFAULT 0.5,
  impact REAL DEFAULT 0.5,
  mitigation TEXT,
  owner TEXT,
  status TEXT NOT NULL DEFAULT 'open',
  dna_signature TEXT,
  FOREIGN KEY (report_id) REFERENCES weekly_reports(id)
)`;

const CREATE_TABLE_APPROVALS = `CREATE TABLE IF NOT EXISTS weekly_approvals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  report_id TEXT NOT NULL,
  level INTEGER NOT NULL,
  approver TEXT NOT NULL,
  approver_id TEXT NOT NULL,
  comment TEXT,
  signature TEXT NOT NULL,
  timestamp INTEGER NOT NULL,
  dna_signature TEXT,
  FOREIGN KEY (report_id) REFERENCES weekly_reports(id)
)`;

const CREATE_TABLE_TEMPLATES = `CREATE TABLE IF NOT EXISTS weekly_templates (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  department TEXT NOT NULL DEFAULT '全部',
  sections TEXT,
  is_default INTEGER DEFAULT 0,
  created_at INTEGER NOT NULL,
  dna_signature TEXT
)`;

// === 索引 ===
const CREATE_INDEX_WR_WEEK_START = `CREATE INDEX IF NOT EXISTS idx_wr_week_start ON weekly_reports(week_start)`;
const CREATE_INDEX_WR_REPORTER = `CREATE INDEX IF NOT EXISTS idx_wr_reporter ON weekly_reports(reporter_id)`;
const CREATE_INDEX_WR_STATUS = `CREATE INDEX IF NOT EXISTS idx_wr_status ON weekly_reports(status)`;
const CREATE_INDEX_WT_REPORT = `CREATE INDEX IF NOT EXISTS idx_wt_report ON weekly_tasks(report_id)`;
const CREATE_INDEX_NT_REPORT = `CREATE INDEX IF NOT EXISTS idx_nt_report ON next_tasks(report_id)`;
const CREATE_INDEX_ISSUE_REPORT = `CREATE INDEX IF NOT EXISTS idx_issue_report ON weekly_issues(report_id)`;
const CREATE_INDEX_RISK_REPORT = `CREATE INDEX IF NOT EXISTS idx_risk_report ON weekly_risks(report_id)`;
const CREATE_INDEX_APPROVAL_REPORT = `CREATE INDEX IF NOT EXISTS idx_approval_report ON weekly_approvals(report_id)`;
const CREATE_INDEX_WR_DEPT_STATUS = `CREATE INDEX IF NOT EXISTS idx_wr_dept_status ON weekly_reports(department, status)`;
const CREATE_INDEX_WR_WEEK_REPORTER = `CREATE INDEX IF NOT EXISTS idx_wr_week_reporter ON weekly_reports(week_start, reporter_id)`;

export class WeeklyDatabase {
  private static store: relationalStore.RdbStore | null = null;

  static async init(): Promise<void> {
    try {
      STORE_CONFIG.name = DB_NAME;
      STORE_CONFIG.securityLevel = relationalStore.SecurityLevel.S3;

      const store = await relationalStore.getRdbStore(DB_NAME, STORE_CONFIG);
      WeeklyDatabase.store = store;

      await store.executeSql(CREATE_TABLE_WEEKLY_REPORTS);
      await store.executeSql(CREATE_TABLE_WEEKLY_TASKS);
      await store.executeSql(CREATE_TABLE_NEXT_TASKS);
      await store.executeSql(CREATE_TABLE_WEEKLY_ISSUES);
      await store.executeSql(CREATE_TABLE_WEEKLY_RISKS);
      await store.executeSql(CREATE_TABLE_APPROVALS);
      await store.executeSql(CREATE_TABLE_TEMPLATES);

      await store.executeSql(CREATE_INDEX_WR_WEEK_START);
      await store.executeSql(CREATE_INDEX_WR_REPORTER);
      await store.executeSql(CREATE_INDEX_WR_STATUS);
      await store.executeSql(CREATE_INDEX_WT_REPORT);
      await store.executeSql(CREATE_INDEX_NT_REPORT);
      await store.executeSql(CREATE_INDEX_ISSUE_REPORT);
      await store.executeSql(CREATE_INDEX_RISK_REPORT);
      await store.executeSql(CREATE_INDEX_APPROVAL_REPORT);
      await store.executeSql(CREATE_INDEX_WR_DEPT_STATUS);
      await store.executeSql(CREATE_INDEX_WR_WEEK_REPORTER);

      console.info('[龍魂] 周报数据库初始化完成·S3加密·7表·10索引');
    } catch (err) {
      const error = err as BusinessError;
      console.error(`[龍魂] 周报数据库初始化失败: ${error.message}`);
    }
  }

  static getStore(): relationalStore.RdbStore | null {
    return WeeklyDatabase.store;
  }

  // === 统计查询 ===
  static async getReportStats(reporterId: string): Promise<{ total: number; draft: number; submitted: number; approved: number }> {
    const store = WeeklyDatabase.store;
    if (!store) return { total: 0, draft: 0, submitted: 0, approved: 0 };

    try {
      const predicates = new relationalStore.RdbPredicates('weekly_reports');
      predicates.equalTo('reporter_id', reporterId);
      const resultSet = await store.query(predicates);

      let total = 0, draft = 0, submitted = 0, approved = 0;
      while (resultSet.goToNextRow()) {
        total++;
        const status = resultSet.getString(resultSet.getColumnIndex('status'));
        if (status === '草稿') draft++;
        if (status === '已提交' || status === '初审中' || status === '终审中') submitted++;
        if (status === '已通过') approved++;
      }
      resultSet.close();
      return { total, draft, submitted, approved };
    } catch (err) {
      const error = err as BusinessError;
      console.error(`[龍魂] 周报统计查询失败: ${error.message}`);
      return { total: 0, draft: 0, submitted: 0, approved: 0 };
    }
  }

  static async getPendingReviewCount(): Promise<number> {
    const store = WeeklyDatabase.store;
    if (!store) return 0;

    try {
      const predicates = new relationalStore.RdbPredicates('weekly_reports');
      const statusList = ['已提交', '初审中'];
      // 简化: 查询status在已提交和初审中的记录数
      const resultSet = await store.query(predicates);
      let count = 0;
      while (resultSet.goToNextRow()) {
        const status = resultSet.getString(resultSet.getColumnIndex('status'));
        if (statusList.includes(status)) count++;
      }
      resultSet.close();
      return count;
    } catch (err) {
      return 0;
    }
  }

  static async getWeekHours(reporterId: string, weekStart: number, weekEnd: number): Promise<number> {
    const store = WeeklyDatabase.store;
    if (!store) return 0;

    try {
      const predicates = new relationalStore.RdbPredicates('weekly_reports');
      predicates.equalTo('reporter_id', reporterId);
      predicates.greaterThanOrEqualTo('week_start', weekStart);
      predicates.lessThanOrEqualTo('week_end', weekEnd);
      const resultSet = await store.query(predicates);

      let totalHours = 0;
      while (resultSet.goToNextRow()) {
        totalHours += resultSet.getDouble(resultSet.getColumnIndex('total_actual_hours'));
      }
      resultSet.close();
      return totalHours;
    } catch (err) {
      return 0;
    }
  }

  static async cleanup(): Promise<void> {
    if (WeeklyDatabase.store) {
      WeeklyDatabase.store = null;
    }
    console.info('[龍魂] 周报数据库连接已关闭');
  }
}

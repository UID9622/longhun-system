// entry/src/main/ets/models/WeeklyModel.ets
// 龍魂 · 周报管理模型 · ArkTS

// === DNA常量 ===
const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// === 周报状态 ===
export enum WeeklyStatus {
  DRAFT = '草稿',
  SUBMITTED = '已提交',
  FIRST_REVIEW = '初审中',
  FINAL_REVIEW = '终审中',
  APPROVED = '已通过',
  REJECTED = '已驳回',
  ARCHIVED = '已归档'
}

// === 任务状态 ===
export enum TaskStatus {
  NOT_STARTED = '未开始',
  IN_PROGRESS = '进行中',
  COMPLETED = '已完成',
  BLOCKED = '被阻塞',
  DELAYED = '已延期',
  CANCELLED = '已取消'
}

// === 任务类型 ===
export enum TaskType {
  DEVELOPMENT = '开发',
  DESIGN = '设计',
  TEST = '测试',
  MEETING = '会议',
  DOCUMENT = '文档',
  RESEARCH = '调研',
  BUGFIX = 'Bug修复',
  OPTIMIZATION = '优化',
  OTHER = '其他'
}

// === 优先级 ===
export enum Priority {
  P0 = 'P0-紧急',
  P1 = 'P1-高',
  P2 = 'P2-中',
  P3 = 'P3-低'
}

// === 审批记录 ===
export interface ApprovalRecord {
  level: number;
  approver: string;
  approverId: string;
  comment: string;
  signature: string;
  timestamp: Date;
  dnaSignature: string;
}

// === 模板区块 ===
export interface TemplateSection {
  id: string;
  title: string;
  type: string;
  required: boolean;
}

// === 周报档案 ===
export class WeeklyReport {
  id: string;
  reportNo: string;
  weekStart: Date;
  weekEnd: Date;
  status: WeeklyStatus;

  reporter: string;
  reporterId: string;
  department: string;
  position: string;

  tasks: WeeklyTask[];
  nextTasks: NextTask[];

  totalPlannedHours: number;
  totalActualHours: number;
  totalOvertimeHours: number;
  completionRate: number;

  issues: WeeklyIssue[];
  risks: WeeklyRisk[];
  approvals: ApprovalRecord[];

  summary: string;
  nextPlan: string;
  needSupport: string;

  createdAt: Date;
  updatedAt: Date;
  submittedAt?: Date;
  approvedAt?: Date;
  dnaSignature: string;

  constructor(data: Partial<WeeklyReport>) {
    this.id = data.id || this.generateId();
    this.reportNo = data.reportNo || this.generateReportNo();
    this.weekStart = data.weekStart || this.getWeekStart();
    this.weekEnd = data.weekEnd || this.getWeekEnd();
    this.status = data.status || WeeklyStatus.DRAFT;

    this.reporter = data.reporter || '';
    this.reporterId = data.reporterId || '';
    this.department = data.department || '';
    this.position = data.position || '';

    this.tasks = data.tasks || [];
    this.nextTasks = data.nextTasks || [];

    this.totalPlannedHours = data.totalPlannedHours || 0;
    this.totalActualHours = data.totalActualHours || 0;
    this.totalOvertimeHours = data.totalOvertimeHours || 0;
    this.completionRate = data.completionRate || 0;

    this.issues = data.issues || [];
    this.risks = data.risks || [];
    this.approvals = data.approvals || [];

    this.summary = data.summary || '';
    this.nextPlan = data.nextPlan || '';
    this.needSupport = data.needSupport || '';

    this.createdAt = data.createdAt || new Date();
    this.updatedAt = data.updatedAt || new Date();
    this.submittedAt = data.submittedAt;
    this.approvedAt = data.approvedAt;
    this.dnaSignature = this.signData();
  }

  private generateId(): string {
    return `WR-${MASTER_UID}-${Date.now().toString(36).substr(-6)}`;
  }

  private generateReportNo(): string {
    const date = new Date();
    const weekNum = this.getWeekNumber(date);
    return `ZB${date.getFullYear()}W${weekNum.toString().padStart(2,'0')}-${Math.floor(Math.random()*999).toString().padStart(3,'0')}`;
  }

  private getWeekStart(): Date {
    const d = new Date();
    const day = d.getDay();
    const diff = d.getDate() - day + (day === 0 ? -6 : 1);
    return new Date(d.setDate(diff));
  }

  private getWeekEnd(): Date {
    const start = this.getWeekStart();
    return new Date(start.getTime() + 6 * 24 * 60 * 60 * 1000);
  }

  private getWeekNumber(date: Date): number {
    const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
    const dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    return Math.ceil((((d.getTime() - yearStart.getTime()) / 86400000) + 1) / 7);
  }

  private signData(): string {
    const payload = `${this.id}-${this.reportNo}-${this.reporter}-${this.status}`;
    return `SM3-${payload.split('').reduce((a,b)=>a+b.charCodeAt(0),0).toString(16).substring(0,16)}`;
  }

  recalculate(): void {
    this.totalPlannedHours = this.tasks.reduce((sum, t) => sum + t.plannedHours, 0);
    this.totalActualHours = this.tasks.reduce((sum, t) => sum + t.actualHours, 0);
    this.totalOvertimeHours = this.tasks.reduce((sum, t) => sum + (t.overtimeHours || 0), 0);

    const completed = this.tasks.filter(t => t.status === TaskStatus.COMPLETED).length;
    this.completionRate = this.tasks.length > 0 ? Math.round((completed / this.tasks.length) * 100) : 0;

    this.updatedAt = new Date();
    this.dnaSignature = this.signData();
  }

  submit(): void {
    this.status = WeeklyStatus.SUBMITTED;
    this.submittedAt = new Date();
    this.updatedAt = new Date();
    this.dnaSignature = this.signData();
  }

  approve(level: number, approver: string, approverId: string, comment: string, signature: string): void {
    this.approvals.push({
      level,
      approver,
      approverId,
      comment,
      signature,
      timestamp: new Date(),
      dnaSignature: this.signApproval(level, approver, signature)
    });

    if (level === 1) this.status = WeeklyStatus.FIRST_REVIEW;
    else if (level === 2) {
      this.status = WeeklyStatus.APPROVED;
      this.approvedAt = new Date();
    }

    this.updatedAt = new Date();
    this.dnaSignature = this.signData();
  }

  reject(approver: string, approverId: string, comment: string): void {
    this.status = WeeklyStatus.REJECTED;
    this.approvals.push({
      level: this.getCurrentLevel(),
      approver,
      approverId,
      comment,
      signature: 'REJECTED',
      timestamp: new Date(),
      dnaSignature: this.signApproval(this.getCurrentLevel(), approver, 'REJECT')
    });
    this.updatedAt = new Date();
    this.dnaSignature = this.signData();
  }

  archive(): void {
    this.status = WeeklyStatus.ARCHIVED;
    this.updatedAt = new Date();
    this.dnaSignature = this.signData();
  }

  private getCurrentLevel(): number {
    return this.approvals.length + 1;
  }

  private signApproval(level: number, approver: string, signature: string): string {
    const payload = `${this.id}-L${level}-${approver}-${signature}-${Date.now()}`;
    return `SM3-${payload.split('').reduce((a,b)=>a+b.charCodeAt(0),0).toString(16).substring(0,16)}`;
  }

  getApprovalProgress(): { current: number; total: number; percentage: number } {
    const total = 2;
    const current = this.approvals.filter(a => a.signature !== 'REJECTED').length;
    return { current, total, percentage: Math.round((current / total) * 100) };
  }

  isEditable(): boolean {
    return this.status === WeeklyStatus.DRAFT || this.status === WeeklyStatus.REJECTED;
  }

  isSubmittable(): boolean {
    return this.tasks.length > 0 && this.isEditable();
  }
}

// === 周任务条目 ===
export class WeeklyTask {
  id: string;
  projectId?: string;
  projectName: string;
  taskType: TaskType;
  priority: Priority;
  status: TaskStatus;

  title: string;
  description: string;

  plannedHours: number;
  actualHours: number;
  overtimeHours: number;

  progress: number;

  plannedStart: Date;
  plannedEnd: Date;
  actualStart?: Date;
  actualEnd?: Date;

  milestoneId?: string;
  deliverables: string[];

  createdAt: Date;
  updatedAt: Date;
  dnaSignature: string;

  constructor(data: Partial<WeeklyTask>) {
    this.id = data.id || `WT-${Date.now()}-${Math.random().toString(36).substr(2,6)}`;
    this.projectId = data.projectId;
    this.projectName = data.projectName || '';
    this.taskType = data.taskType || TaskType.OTHER;
    this.priority = data.priority || Priority.P2;
    this.status = data.status || TaskStatus.NOT_STARTED;

    this.title = data.title || '';
    this.description = data.description || '';

    this.plannedHours = data.plannedHours || 0;
    this.actualHours = data.actualHours || 0;
    this.overtimeHours = data.overtimeHours || 0;
    this.progress = data.progress || 0;

    this.plannedStart = data.plannedStart || new Date();
    this.plannedEnd = data.plannedEnd || new Date();
    this.actualStart = data.actualStart;
    this.actualEnd = data.actualEnd;

    this.milestoneId = data.milestoneId;
    this.deliverables = data.deliverables || [];

    this.createdAt = data.createdAt || new Date();
    this.updatedAt = data.updatedAt || new Date();
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const payload = `${this.id}-${this.title}-${this.status}-${this.progress}`;
    return `SM3-${payload.split('').reduce((a,b)=>a+b.charCodeAt(0),0).toString(16).substring(0,16)}`;
  }

  updateProgress(progress: number): void {
    this.progress = Math.min(100, Math.max(0, progress));
    if (this.progress > 0 && this.status === TaskStatus.NOT_STARTED) {
      this.status = TaskStatus.IN_PROGRESS;
      this.actualStart = this.actualStart || new Date();
    }
    if (this.progress === 100) {
      this.status = TaskStatus.COMPLETED;
      this.actualEnd = new Date();
    }
    this.updatedAt = new Date();
    this.dnaSignature = this.signData();
  }

  getHourVariance(): number {
    return this.actualHours - this.plannedHours;
  }

  isDelayed(): boolean {
    if (this.actualEnd) {
      return this.actualEnd > this.plannedEnd;
    }
    return new Date() > this.plannedEnd && this.status !== TaskStatus.COMPLETED;
  }
}

// === 下周计划条目 ===
export class NextTask {
  id: string;
  projectId?: string;
  projectName: string;
  taskType: TaskType;
  priority: Priority;
  title: string;
  description: string;
  plannedHours: number;
  plannedStart: Date;
  plannedEnd: Date;
  dependencies: string[];
  dnaSignature: string;

  constructor(data: Partial<NextTask>) {
    this.id = data.id || `NT-${Date.now()}-${Math.random().toString(36).substr(2,6)}`;
    this.projectId = data.projectId;
    this.projectName = data.projectName || '';
    this.taskType = data.taskType || TaskType.OTHER;
    this.priority = data.priority || Priority.P2;
    this.title = data.title || '';
    this.description = data.description || '';
    this.plannedHours = data.plannedHours || 0;
    this.plannedStart = data.plannedStart || new Date();
    this.plannedEnd = data.plannedEnd || new Date();
    this.dependencies = data.dependencies || [];
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const payload = `${this.id}-${this.title}-${Date.now()}`;
    return `SM3-${payload.split('').reduce((a,b)=>a+b.charCodeAt(0),0).toString(16).substring(0,16)}`;
  }
}

// === 本周问题 ===
export class WeeklyIssue {
  id: string;
  title: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  status: 'open' | 'resolved' | 'pending';
  relatedTaskId?: string;
  solution?: string;
  resolver?: string;
  resolvedAt?: Date;
  dnaSignature: string;

  constructor(data: Partial<WeeklyIssue>) {
    this.id = data.id || `ISSUE-${Date.now()}-${Math.random().toString(36).substr(2,6)}`;
    this.title = data.title || '';
    this.description = data.description || '';
    this.severity = data.severity || 'medium';
    this.status = data.status || 'open';
    this.relatedTaskId = data.relatedTaskId;
    this.solution = data.solution;
    this.resolver = data.resolver;
    this.resolvedAt = data.resolvedAt;
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const payload = `${this.id}-${this.status}-${Date.now()}`;
    return `SM3-${payload.split('').reduce((a,b)=>a+b.charCodeAt(0),0).toString(16).substring(0,16)}`;
  }
}

// === 风险项 ===
export class WeeklyRisk {
  id: string;
  title: string;
  description: string;
  probability: number;
  impact: number;
  mitigation: string;
  owner: string;
  status: 'open' | 'mitigated' | 'realized';
  dnaSignature: string;

  constructor(data: Partial<WeeklyRisk>) {
    this.id = data.id || `WRISK-${Date.now()}-${Math.random().toString(36).substr(2,6)}`;
    this.title = data.title || '';
    this.description = data.description || '';
    this.probability = data.probability || 0.5;
    this.impact = data.impact || 0.5;
    this.mitigation = data.mitigation || '';
    this.owner = data.owner || '';
    this.status = data.status || 'open';
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const payload = `${this.id}-${this.status}-${Date.now()}`;
    return `SM3-${payload.split('').reduce((a,b)=>a+b.charCodeAt(0),0).toString(16).substring(0,16)}`;
  }

  getRiskScore(): number {
    return this.probability * this.impact;
  }
}

// === 周报模板 ===
export class WeeklyTemplate {
  id: string;
  name: string;
  department: string;
  sections: TemplateSection[];
  isDefault: boolean;
  createdAt: Date;
  dnaSignature: string;

  constructor(data: Partial<WeeklyTemplate>) {
    this.id = data.id || `TMPL-${Date.now()}`;
    this.name = data.name || '默认模板';
    this.department = data.department || '全部';
    this.sections = data.sections || this.getDefaultSections();
    this.isDefault = data.isDefault || false;
    this.createdAt = data.createdAt || new Date();
    this.dnaSignature = this.signData();
  }

  private getDefaultSections(): TemplateSection[] {
    return [
      { id: 's1', title: '本周任务', type: 'tasks', required: true },
      { id: 's2', title: '下周计划', type: 'next_tasks', required: true },
      { id: 's3', title: '问题与风险', type: 'issues', required: false },
      { id: 's4', title: '本周总结', type: 'summary', required: true },
      { id: 's5', title: '需要支持', type: 'support', required: false }
    ];
  }

  private signData(): string {
    const payload = `${this.id}-${this.name}-${Date.now()}`;
    return `SM3-${payload.split('').reduce((a,b)=>a+b.charCodeAt(0),0).toString(16).substring(0,16)}`;
  }
}

// === 统计接口 ===
export interface WeeklyStats {
  totalReports: number;
  myTotal: number;
  myDraft: number;
  mySubmitted: number;
  myApproved: number;
  myRejected: number;
  pendingReview: number;
  avgCompletion: number;
  totalHours: number;
  thisWeekHours: number;
}

// === 工时趋势项 ===
export interface HourTrendItem {
  week: string;
  planned: number;
  actual: number;
  overtime: number;
}

// === 全局状态 ===
@Observed
export class WeeklyState {
  reports: WeeklyReport[] = [];
  templates: WeeklyTemplate[] = [];
  currentReportId: string = '';

  currentUser: string = '';
  currentUserId: string = '';
  currentDept: string = '';
  userRole: 'reporter' | 'reviewer' | 'admin' = 'reporter';

  filterStatus: WeeklyStatus | '全部' = '全部';
  filterDept: string = '全部';
  filterWeek: string = '';
  searchQuery: string = '';

  get filteredReports(): WeeklyReport[] {
    let result = this.reports;

    if (this.filterStatus !== '全部') {
      result = result.filter(r => r.status === this.filterStatus);
    }

    if (this.filterDept !== '全部') {
      result = result.filter(r => r.department === this.filterDept);
    }

    if (this.filterWeek) {
      result = result.filter(r => r.reportNo.includes(this.filterWeek));
    }

    if (this.searchQuery) {
      const q = this.searchQuery.toLowerCase();
      result = result.filter(r =>
        r.reporter.toLowerCase().includes(q) ||
        r.reportNo.toLowerCase().includes(q) ||
        r.department.toLowerCase().includes(q)
      );
    }

    return result.sort((a, b) => b.weekStart.getTime() - a.weekStart.getTime());
  }

  get myReports(): WeeklyReport[] {
    return this.reports
      .filter(r => r.reporterId === this.currentUserId)
      .sort((a, b) => b.weekStart.getTime() - a.weekStart.getTime());
  }

  get pendingFirstReview(): WeeklyReport[] {
    return this.reports.filter(r => r.status === WeeklyStatus.SUBMITTED);
  }

  get pendingFinalReview(): WeeklyReport[] {
    return this.reports.filter(r => r.status === WeeklyStatus.FIRST_REVIEW);
  }

  get currentWeekDraft(): WeeklyReport | undefined {
    const now = new Date();
    return this.reports.find(r =>
      r.reporterId === this.currentUserId &&
      r.weekStart <= now && r.weekEnd >= now &&
      r.status === WeeklyStatus.DRAFT
    );
  }

  get statistics(): WeeklyStats {
    const myList = this.myReports;
    const now = new Date();
    const thisWeek = myList.filter(r => r.weekStart <= now && r.weekEnd >= now);

    return {
      totalReports: this.reports.length,
      myTotal: myList.length,
      myDraft: myList.filter(r => r.status === WeeklyStatus.DRAFT).length,
      mySubmitted: myList.filter(r => r.status === WeeklyStatus.SUBMITTED).length,
      myApproved: myList.filter(r => r.status === WeeklyStatus.APPROVED).length,
      myRejected: myList.filter(r => r.status === WeeklyStatus.REJECTED).length,
      pendingReview: this.pendingFirstReview.length + this.pendingFinalReview.length,
      avgCompletion: myList.length > 0
        ? Math.round(myList.reduce((sum, r) => sum + r.completionRate, 0) / myList.length)
        : 0,
      totalHours: myList.reduce((sum, r) => sum + r.totalActualHours, 0),
      thisWeekHours: thisWeek.reduce((sum, r) => sum + r.totalActualHours, 0)
    };
  }

  get hourTrend(): HourTrendItem[] {
    const trend: HourTrendItem[] = [];
    const myList = this.myReports.slice(0, 8);

    myList.forEach(r => {
      trend.push({
        week: `W${this.getWeekNumber(r.weekStart)}`,
        planned: r.totalPlannedHours,
        actual: r.totalActualHours,
        overtime: r.totalOvertimeHours
      });
    });

    return trend.reverse();
  }

  // 操作
  addReport(report: WeeklyReport): void {
    this.reports.push(report);
    this.persist();
  }

  removeReport(id: string): void {
    const idx = this.reports.findIndex(r => r.id === id);
    if (idx >= 0) {
      this.reports.splice(idx, 1);
      this.persist();
    }
  }

  updateReport(id: string, data: Partial<WeeklyReport>): void {
    const idx = this.reports.findIndex(r => r.id === id);
    if (idx >= 0) {
      const old = this.reports[idx];
      this.reports[idx] = new WeeklyReport({ ...old, ...data, id: old.id });
      this.persist();
    }
  }

  addTask(reportId: string, task: WeeklyTask): void {
    const report = this.reports.find(r => r.id === reportId);
    if (report) {
      report.tasks.push(task);
      report.recalculate();
      this.persist();
    }
  }

  removeTask(reportId: string, taskId: string): void {
    const report = this.reports.find(r => r.id === reportId);
    if (report) {
      const idx = report.tasks.findIndex(t => t.id === taskId);
      if (idx >= 0) {
        report.tasks.splice(idx, 1);
        report.recalculate();
        this.persist();
      }
    }
  }

  updateTaskProgress(reportId: string, taskId: string, progress: number): void {
    const report = this.reports.find(r => r.id === reportId);
    if (report) {
      const task = report.tasks.find(t => t.id === taskId);
      if (task) {
        task.updateProgress(progress);
        report.recalculate();
        this.persist();
      }
    }
  }

  addNextTask(reportId: string, nextTask: NextTask): void {
    const report = this.reports.find(r => r.id === reportId);
    if (report) {
      report.nextTasks.push(nextTask);
      this.persist();
    }
  }

  addIssue(reportId: string, issue: WeeklyIssue): void {
    const report = this.reports.find(r => r.id === reportId);
    if (report) {
      report.issues.push(issue);
      this.persist();
    }
  }

  addRisk(reportId: string, risk: WeeklyRisk): void {
    const report = this.reports.find(r => r.id === reportId);
    if (report) {
      report.risks.push(risk);
      this.persist();
    }
  }

  submitReport(reportId: string): void {
    const report = this.reports.find(r => r.id === reportId);
    if (report && report.isSubmittable()) {
      report.submit();
      this.persist();
    }
  }

  approveReport(reportId: string, level: number, approver: string, approverId: string, comment: string, signature: string): void {
    const report = this.reports.find(r => r.id === reportId);
    if (report) {
      report.approve(level, approver, approverId, comment, signature);
      this.persist();
    }
  }

  rejectReport(reportId: string, approver: string, approverId: string, comment: string): void {
    const report = this.reports.find(r => r.id === reportId);
    if (report) {
      report.reject(approver, approverId, comment);
      this.persist();
    }
  }

  addTemplate(template: WeeklyTemplate): void {
    this.templates.push(template);
    this.persist();
  }

  removeTemplate(id: string): void {
    const idx = this.templates.findIndex(t => t.id === id);
    if (idx >= 0) {
      this.templates.splice(idx, 1);
      this.persist();
    }
  }

  private persist(): void {
    AppStorage.setOrCreate('weekly_reports', JSON.stringify(this.reports));
    AppStorage.setOrCreate('weekly_templates', JSON.stringify(this.templates));
    AppStorage.setOrCreate('weekly_current_id', this.currentReportId);
  }

  load(): void {
    const reports = AppStorage.get<string>('weekly_reports');
    if (reports) {
      try {
        const parsed = JSON.parse(reports);
        this.reports = parsed.map((r: Record<string, Object>) => new WeeklyReport(r as Partial<WeeklyReport>));
      } catch (e) {
        console.error('加载周报数据失败', e);
      }
    }

    const templates = AppStorage.get<string>('weekly_templates');
    if (templates) {
      try {
        const parsed = JSON.parse(templates);
        this.templates = parsed.map((t: Record<string, Object>) => new WeeklyTemplate(t as Partial<WeeklyTemplate>));
      } catch (e) {
        console.error('加载模板数据失败', e);
      }
    }

    this.currentReportId = AppStorage.get<string>('weekly_current_id') || '';
  }

  private getWeekNumber(date: Date): number {
    const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
    const dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    return Math.ceil((((d.getTime() - yearStart.getTime()) / 86400000) + 1) / 7);
  }
}

// 全局状态
export const weeklyState = new WeeklyState();
AppStorage.setOrCreate('weeklyState', weeklyState);

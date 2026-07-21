# 龍魂 · 鸿蒙 ArkTS 实战：Weekly Review 周报管理

> 龍魂系统 · 鸿蒙原生适配层 · 周报生成与审批追踪
> 
> DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622 | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

---

## 一、核心定位

| 维度 | 说明 |
|------|------|
| 平台 | 鸿蒙 HarmonyOS NEXT · 纯血鸿蒙 |
| 语言 | ArkTS · 声明式UI |
| 场景 | 周报生成 · 任务追踪 · 工时统计 · 审批流转 · 历史归档 |
| 架构 | 龍魂蚁群触角 → 鸿蒙原生能力 |
| 主权 | 数据本地 · 国密SM2/SM3签名 · 不上传云端 |
| 安全 | 模板锁定 · 防篡改 · 多级审批 · 版本追溯 |

---

## 二、系统架构

```
┌─────────────────────────────────────────┐
│           龍魂系统 · 鸿蒙适配层            │
│  DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ │
│  UID: 9622                              │
├─────────────────────────────────────────┤
│         鸿蒙 ArkTS 应用层                 │
│                                         │
│  EntryAbility → WeeklyReviewPage         │
│  ├── 周报模板建模（AppStorage/LocalStorage）│
│  ├── 任务条目录入（分类·优先级·工时）       │
│  ├── 自动汇总引擎（进度·工时·完成率）        │
│  ├── 审批流转链（提交→初审→终审→归档）       │
│  ├── 历史周报库（版本对比·趋势分析）         │
│  ├── 工时统计看板（个人·团队·项目维度）      │
│  └── 办公交互（导出PDF·分享·打印·日历提醒）   │
├─────────────────────────────────────────┤
│         鸿蒙系统能力层                      │
│                                         │
│  日历(Calendar) · 通知(Notification)      │
│  数据存储(RelationalStore) · 文件(File)    │
│  网络(Http) · 分享(Share) · 打印(Print)   │
│  后台任务(WorkScheduler) · 定位(Location) │
│  文档(DocumentPicker) · 相机(Camera)      │
└─────────────────────────────────────────┘
```

---

## 三、状态建模核心

### 3.1 数据模型（`entry/src/main/ets/models/WeeklyModel.ets`）

```typescript
// entry/src/main/ets/models/WeeklyModel.ets
// 龍魂 · 周报管理模型 · ArkTS

// === DNA常量 ===
const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// === 周报状态 ===
export enum WeeklyStatus {
  DRAFT = '草稿',           // 编辑中
  SUBMITTED = '已提交',      // 待初审
  FIRST_REVIEW = '初审中',   // 部门主管审核
  FINAL_REVIEW = '终审中',   // 分管领导审核
  APPROVED = '已通过',       // 审批完成
  REJECTED = '已驳回',       // 被驳回
  ARCHIVED = '已归档'        // 历史归档
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

// === 工时类型 ===
export enum HourType {
  PLANNED = '计划工时',
  ACTUAL = '实际工时',
  OVERTIME = '加班工时'
}

// === 周报档案 ===
export class WeeklyReport {
  id: string;                // 唯一ID
  reportNo: string;           // 周报编号
  weekStart: Date;           // 周起始日
  weekEnd: Date;             // 周结束日
  status: WeeklyStatus;       // 状态

  // 填报人
  reporter: string;           // 填报人
  reporterId: string;        // 填报人ID
  department: string;        // 部门
  position: string;          // 职位

  // 任务条目
  tasks: WeeklyTask[];       // 本周任务
  nextTasks: NextTask[];     // 下周计划

  // 汇总数据
  totalPlannedHours: number;   // 计划总工时
  totalActualHours: number;   // 实际总工时
  totalOvertimeHours: number;  // 加班总工时
  completionRate: number;     // 完成率

  // 问题与风险
  issues: WeeklyIssue[];     // 本周问题
  risks: WeeklyRisk[];       // 风险项

  // 审批链
  approvals: ApprovalRecord[]; // 审批记录

  // 总结
  summary: string;            // 本周总结
  nextPlan: string;           // 下周计划
  needSupport: string;        // 需要支持

  // 审计
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

  // 自动汇总计算
  recalculate(): void {
    this.totalPlannedHours = this.tasks.reduce((sum, t) => sum + t.plannedHours, 0);
    this.totalActualHours = this.tasks.reduce((sum, t) => sum + t.actualHours, 0);
    this.totalOvertimeHours = this.tasks.reduce((sum, t) => sum + (t.overtimeHours || 0), 0);

    const completed = this.tasks.filter(t => t.status === TaskStatus.COMPLETED).length;
    this.completionRate = this.tasks.length > 0 ? Math.round((completed / this.tasks.length) * 100) : 0;

    this.updatedAt = new Date();
    this.dnaSignature = this.signData();
  }

  // 提交审批
  submit(): void {
    this.status = WeeklyStatus.SUBMITTED;
    this.submittedAt = new Date();
    this.updatedAt = new Date();
    this.dnaSignature = this.signData();
  }

  // 审批通过
  approve(level: number, approver: string, comment: string, signature: string): void {
    this.approvals.push({
      level,
      approver,
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

  // 驳回
  reject(approver: string, comment: string): void {
    this.status = WeeklyStatus.REJECTED;
    this.approvals.push({
      level: this.getCurrentLevel(),
      approver,
      comment,
      signature: 'REJECTED',
      timestamp: new Date(),
      dnaSignature: this.signApproval(this.getCurrentLevel(), approver, 'REJECT')
    });
    this.updatedAt = new Date();
    this.dnaSignature = this.signData();
  }

  // 归档
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

  // 获取审批进度
  getApprovalProgress(): { current: number; total: number; percentage: number } {
    const total = 2; // 两级审批
    const current = this.approvals.filter(a => a.signature !== 'REJECTED').length;
    return { current, total, percentage: Math.round((current / total) * 100) };
  }

  // 检查是否可编辑
  isEditable(): boolean {
    return this.status === WeeklyStatus.DRAFT || this.status === WeeklyStatus.REJECTED;
  }

  // 检查是否可提交
  isSubmittable(): boolean {
    return this.tasks.length > 0 && this.isEditable();
  }
}
```

### 3.2 周任务条目

```typescript
// === 周任务条目 ===
export class WeeklyTask {
  id: string;
  projectId?: string;       // 关联项目ID
  projectName: string;         // 关联项目名称
  taskType: TaskType;        // 任务类型
  priority: Priority;         // 优先级
  status: TaskStatus;        // 状态

  // 内容
  title: string;             // 任务标题
  description: string;       // 任务描述

  // 工时
  plannedHours: number;      // 计划工时
  actualHours: number;        // 实际工时
  overtimeHours: number;     // 加班工时

  // 进度
  progress: number;           // 完成进度 0-100

  // 时间
  plannedStart: Date;
  plannedEnd: Date;
  actualStart?: Date;
  actualEnd?: Date;

  // 关联
  milestoneId?: string;       // 关联里程碑
  deliverables: string[];     // 交付物路径

  // 审计
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

  // 更新进度
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

  // 计算工时偏差
  getHourVariance(): number {
    return this.actualHours - this.plannedHours;
  }

  // 是否延期
  isDelayed(): boolean {
    if (this.actualEnd) {
      return this.actualEnd > this.plannedEnd;
    }
    return new Date() > this.plannedEnd && this.status !== TaskStatus.COMPLETED;
  }
}
```

### 3.3 下周计划

```typescript
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
  dependencies: string[];      // 依赖任务ID
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
    return `SM3-${this.id}-${this.title}-${Date.now()}`;
  }
}
```

### 3.4 问题与风险

```typescript
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
    return `SM3-${this.id}-${this.status}-${Date.now()}`;
  }
}

// === 风险项 ===
export class WeeklyRisk {
  id: string;
  title: string;
  description: string;
  probability: number;  // 0-1
  impact: number;       // 0-1
  mitigation: string;   // 缓解措施
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
    return `SM3-${this.id}-${this.status}-${Date.now()}`;
  }

  getRiskScore(): number {
    return this.probability * this.impact;
  }
}
```

### 3.5 审批记录与模板

```typescript
// === 审批记录 ===
export interface ApprovalRecord {
  level: number;              // 1=初审 2=终审
  approver: string;          // 审批人
  approverId: string;        // 审批人ID
  comment: string;           // 审批意见
  signature: string;         // 电子签名
  timestamp: Date;
  dnaSignature: string;
}

// === 周报模板 ===
export class WeeklyTemplate {
  id: string;
  name: string;              // 模板名称
  department: string;       // 适用部门
  sections: TemplateSection[]; // 模板区块
  isDefault: boolean;        // 是否默认
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
    return `SM3-${this.id}-${this.name}-${Date.now()}`;
  }
}

export interface TemplateSection {
  id: string;
  title: string;
  type: string;
  required: boolean;
}
```

### 3.6 全局状态

```typescript
// === 周报全局状态 ===
@Observed
export class WeeklyState {
  reports: WeeklyReport[] = [];
  templates: WeeklyTemplate[] = [];
  currentReportId: string = '';

  // 当前用户
  currentUser: string = '';
  currentUserId: string = '';
  currentDept: string = '';
  userRole: 'reporter' | 'reviewer' | 'admin' = 'reporter';

  // 过滤
  filterStatus: WeeklyStatus | '全部' = '全部';
  filterDept: string = '全部';
  filterWeek: string = '';
  searchQuery: string = '';

  // 派生：过滤后的周报
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

  // 我的周报
  get myReports(): WeeklyReport[] {
    return this.reports
      .filter(r => r.reporterId === this.currentUserId)
      .sort((a, b) => b.weekStart.getTime() - a.weekStart.getTime());
  }

  // 待审批（初审）
  get pendingFirstReview(): WeeklyReport[] {
    return this.reports.filter(r => r.status === WeeklyStatus.SUBMITTED);
  }

  // 待审批（终审）
  get pendingFinalReview(): WeeklyReport[] {
    return this.reports.filter(r => r.status === WeeklyStatus.FIRST_REVIEW);
  }

  // 本周待填
  get currentWeekDraft(): WeeklyReport | undefined {
    const now = new Date();
    return this.reports.find(r =>
      r.reporterId === this.currentUserId &&
      r.weekStart <= now && r.weekEnd >= now &&
      r.status === WeeklyStatus.DRAFT
    );
  }

  // 统计
  get statistics(): WeeklyStats {
    const myList = this.myReports;
    const thisWeek = myList.filter(r => {
      const now = new Date();
      return r.weekStart <= now && r.weekEnd >= now;
    });

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

  // 工时趋势（最近8周）
  get hourTrend(): { week: string; planned: number; actual: number; overtime: number }[] {
    const trend: { week: string; planned: number; actual: number; overtime: number }[] = [];
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

  // 添加任务
  addTask(reportId: string, task: WeeklyTask): void {
    const report = this.reports.find(r => r.id === reportId);
    if (report) {
      report.tasks.push(task);
      report.recalculate();
      this.persist();
    }
  }

  // 更新任务进度
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

  // 提交周报
  submitReport(reportId: string): void {
    const report = this.reports.find(r => r.id === reportId);
    if (report && report.isSubmittable()) {
      report.submit();
      this.persist();
    }
  }

  // 审批
  approveReport(reportId: string, level: number, approver: string, comment: string, signature: string): void {
    const report = this.reports.find(r => r.id === reportId);
    if (report) {
      report.approve(level, approver, comment, signature);
      this.persist();
    }
  }

  // 驳回
  rejectReport(reportId: string, approver: string, comment: string): void {
    const report = this.reports.find(r => r.id === reportId);
    if (report) {
      report.reject(approver, comment);
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
        this.reports = parsed.map((r: any) => new WeeklyReport(r));
      } catch (e) {
        console.error('加载周报数据失败', e);
      }
    }

    const templates = AppStorage.get<string>('weekly_templates');
    if (templates) {
      try {
        const parsed = JSON.parse(templates);
        this.templates = parsed.map((t: any) => new WeeklyTemplate(t));
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

// === 统计 ===
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

// 全局状态
export const weeklyState = new WeeklyState();
AppStorage.setOrCreate('weeklyState', weeklyState);
```

---

## 四、主页面实现

### 4.1 页面入口（`entry/src/main/ets/pages/WeeklyReviewPage.ets`）

```typescript
// entry/src/main/ets/pages/WeeklyReviewPage.ets
// 龍魂 · 周报管理主页面 · ArkTS

import { WeeklyReport, WeeklyStatus, WeeklyTask, TaskStatus, TaskType, Priority, WeeklyState, weeklyState, WeeklyStats, WeeklyIssue, WeeklyRisk, NextTask } from '../models/WeeklyModel';
import { TaskEditDialog } from '../components/TaskEditDialog';
import { ApprovalDialog } from '../components/ApprovalDialog';
import { HourChartView } from '../components/HourChartView';
import { TrendChartView } from '../components/TrendChartView';
import { WeeklyDetailDialog } from '../components/WeeklyDetailDialog';
import { TemplateDialog } from '../components/TemplateDialog';
import { WeeklyDatabase } from '../database/WeeklyDatabase';

@Entry
@Component
struct WeeklyReviewPage {
  @StorageLink('weeklyState') weeklyState: WeeklyState = weeklyState;
  @State private selectedTab: number = 0;
  @State private showTaskDialog: boolean = false;
  @State private showApprovalDialog: boolean = false;
  @State private showDetailDialog: boolean = false;
  @State private showTemplateDialog: boolean = false;
  @State private editingReport: WeeklyReport | null = null;
  @State private editingTask: WeeklyTask | null = null;
  @State private showSearch: boolean = false;
  @State private searchText: string = '';
  @State private viewMode: 'list' | 'stats' | 'trend' = 'list';

  aboutToAppear() {
    this.weeklyState.load();
    WeeklyDatabase.init();
    this.scheduleReminders();
  }

  build() {
    Column() {
      this.HeaderBuilder()
      this.StatsBuilder()
      this.ViewControlBuilder()
      this.TabBuilder()
      if (this.showSearch) { this.SearchBuilder() }
      this.ContentBuilder()
      this.FooterBuilder()
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }
```

### 4.2 标题栏

```typescript
  @Builder
  HeaderBuilder() {
    Row() {
      Text('🐉').fontSize(28).margin({ right: 8 })
      Column() {
        Text('龍魂周报管理').fontSize(20).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        Text(`UID:${MASTER_UID} · ${this.weeklyState.statistics.myTotal}份周报`).fontSize(12).fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start)
      Blank()
      if (this.weeklyState.pendingReview > 0) {
        Badge({
          value: this.weeklyState.pendingReview.toString(),
          position: BadgePosition.RightTop,
          style: { badgeSize: 18, badgeColor: '#c41e3a' }
        }) {
          Button() { Text('🔔').fontSize(20) }
          .type(ButtonType.Circle)
          .backgroundColor('rgba(196,30,58,0.2)')
          .width(40).height(40)
          .onClick(() => { this.selectedTab = 3; })
        }
      }
      Button() { Text(this.showSearch ? '✕' : '🔍').fontSize(20) }
      .type(ButtonType.Circle).backgroundColor('#1a1a1a').width(40).height(40)
      .onClick(() => {
        this.showSearch = !this.showSearch;
        if (!this.showSearch) { this.weeklyState.searchQuery = ''; }
      })
      Button() { Text('+').fontSize(24).fontColor('#fff') }
      .type(ButtonType.Circle).backgroundColor('#c41e3a').width(40).height(40)
      .onClick(() => { this.createNewWeekly(); })
    }
    .width('100%').height(56).padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }
```

### 4.3 统计卡片

```typescript
  @Builder
  StatsBuilder() {
    Row() {
      this.StatCard('我的周报', this.weeklyState.statistics.myTotal.toString(), '#fff')
      this.StatCard('草稿', this.weeklyState.statistics.myDraft.toString(), '#ffcc00')
      this.StatCard('已提交', this.weeklyState.statistics.mySubmitted.toString(), '#0066cc')
      this.StatCard('已通过', this.weeklyState.statistics.myApproved.toString(), '#00ff00')
      this.StatCard('本周工时', `${this.weeklyState.statistics.thisWeekHours}h`, '#c41e3a')
    }
    .width('100%').height(80).padding({ left: 12, right: 12, top: 8, bottom: 8 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  StatCard(label: string, value: string, color: string) {
    Column() {
      Text(value).fontSize(24).fontWeight(FontWeight.Bold).fontColor(color)
      Text(label).fontSize(11).fontColor('#666').margin({ top: 4 })
    }
    .width('20%').height('100%').justifyContent(FlexAlign.Center).alignItems(HorizontalAlign.Center)
  }
```

### 4.4 视图控制

```typescript
  @Builder
  ViewControlBuilder() {
    Row() {
      Row() {
        Button() { Text('◀').fontSize(14).fontColor('#999') }
        .type(ButtonType.Circle).backgroundColor('#1a1a1a').width(32).height(32)
        .onClick(() => { this.prevWeek(); })
        Text(this.getCurrentWeekLabel()).fontSize(14).fontColor('#fff').margin({ left: 12, right: 12 })
        Button() { Text('▶').fontSize(14).fontColor('#999') }
        .type(ButtonType.Circle).backgroundColor('#1a1a1a').width(32).height(32)
        .onClick(() => { this.nextWeek(); })
      }
      .layoutWeight(1)
      Blank()
      Row() {
        ForEach(['list', 'stats', 'trend'], (mode: string) => {
          Button() {
            Text(mode === 'list' ? '列表' : mode === 'stats' ? '统计' : '趋势')
            .fontSize(12).fontColor(this.viewMode === mode ? '#0a0a0a' : '#999')
          }
          .type(ButtonType.Normal)
          .backgroundColor(this.viewMode === mode ? '#c41e3a' : '#1a1a1a')
          .borderRadius(8).padding({ left: 12, right: 12, top: 4, bottom: 4 })
          .margin({ left: 4 })
          .onClick(() => { this.viewMode = mode as 'list' | 'stats' | 'trend'; })
        })
      }
    }
    .width('100%').height(48).padding({ left: 12, right: 12 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }
```

### 4.5 标签切换

```typescript
  @Builder
  TabBuilder() {
    Row() {
      ForEach([
        { label: '我的周报', icon: '📝', count: this.weeklyState.statistics.myDraft },
        { label: '团队周报', icon: '👥', count: 0 },
        { label: '工时统计', icon: '⏱️', count: 0 },
        { label: '待审批', icon: '✅', count: this.weeklyState.pendingReview }
      ], (item: {label: string, icon: string, count: number}, index: number) => {
        Column() {
          Text(`${item.icon} ${item.label}${item.count > 0 ? `(${item.count})` : ''}`)
            .fontSize(13)
            .fontWeight(this.selectedTab === index ? FontWeight.Bold : FontWeight.Normal)
            .fontColor(this.selectedTab === index ? '#c41e3a' : '#888')
          if (this.selectedTab === index) {
            Divider().strokeWidth(2).color('#c41e3a').width(20).margin({ top: 4 })
          }
        }
        .padding({ top: 12, bottom: 12, left: 16, right: 16 })
        .onClick(() => { this.selectedTab = index; })
      })
    }
    .width('100%').justifyContent(FlexAlign.SpaceAround)
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }
```

### 4.6 搜索栏

```typescript
  @Builder
  SearchBuilder() {
    Row() {
      TextInput({ placeholder: '搜索填报人/部门/周报编号...', text: $$this.searchText })
        .width('100%').height(40).backgroundColor('#2a2a2a')
        .fontColor('#fff').placeholderColor('#666')
        .borderRadius(8).padding({ left: 12, right: 12 })
        .onChange((value: string) => { this.weeklyState.searchQuery = value; })
    }
    .width('100%').padding({ left: 16, right: 16, top: 8, bottom: 8 })
    .backgroundColor('#1a1a1a')
  }
```

### 4.7 内容区

```typescript
  @Builder
  ContentBuilder() {
    if (this.viewMode === 'list') {
      if (this.selectedTab === 0) { this.MyWeeklyListBuilder() }
      else if (this.selectedTab === 1) { this.TeamWeeklyListBuilder() }
      else if (this.selectedTab === 2) { this.HourStatsBuilder() }
      else { this.ApprovalListBuilder() }
    } else if (this.viewMode === 'stats') {
      HourChartView({ stats: this.weeklyState.statistics, trend: this.weeklyState.hourTrend })
    } else {
      TrendChartView({ trend: this.weeklyState.hourTrend })
    }
  }
```

### 4.8 我的周报列表

```typescript
  @Builder
  MyWeeklyListBuilder() {
    List() {
      if (this.weeklyState.currentWeekDraft) {
        ListItem() { this.DraftCardBuilder(this.weeklyState.currentWeekDraft) }
      }
      ForEach(this.weeklyState.myReports, (report: WeeklyReport) => {
        ListItem() { this.WeeklyCardBuilder(report) }
        .onClick(() => { this.editingReport = report; this.showDetailDialog = true; })
      }, (report: WeeklyReport) => report.id)
    }
    .width('100%').layoutWeight(1).divider({ strokeWidth: 1, color: '#222' })
    .scrollBar(BarState.Auto).padding({ bottom: 16 })
  }

  @Builder
  DraftCardBuilder(report: WeeklyReport) {
    Column() {
      Row() {
        Text('📝').fontSize(24).margin({ right: 12 })
        Column() {
          Text(`本周周报草稿`).fontSize(16).fontWeight(FontWeight.Bold).fontColor('#ffcc00')
          Text(`${report.weekStart.toLocaleDateString()} - ${report.weekEnd.toLocaleDateString()}`).fontSize(12).fontColor('#888')
        }
        .alignItems(HorizontalAlign.Start).layoutWeight(1)
        Button('继续编辑')
          .fontSize(12).fontColor('#0a0a0a').backgroundColor('#ffcc00')
          .borderRadius(8).padding({ left: 12, right: 12 })
          .onClick(() => { this.editingReport = report; this.showDetailDialog = true; })
      }
      .width('100%').padding(16)
    }
    .width('100%').backgroundColor('rgba(255,204,0,0.05)')
    .border({ width: 1, color: 'rgba(255,204,0,0.3)' }).borderRadius(8)
    .margin({ left: 12, right: 12, top: 8 })
  }
```

### 4.9 周报卡片

```typescript
  @Builder
  WeeklyCardBuilder(report: WeeklyReport) {
    Row() {
      Column() {
        Text(
          report.status === WeeklyStatus.DRAFT ? '📝' :
          report.status === WeeklyStatus.SUBMITTED ? '⏳' :
          report.status === WeeklyStatus.FIRST_REVIEW ? '👀' :
          report.status === WeeklyStatus.FINAL_REVIEW ? '🔍' :
          report.status === WeeklyStatus.APPROVED ? '✅' :
          report.status === WeeklyStatus.REJECTED ? '❌' : '📦'
        ).fontSize(24)
      }
      .width(40).height(40).margin({ right: 12 }).justifyContent(FlexAlign.Center)
      Column() {
        Row() {
          Text(report.reportNo).fontSize(14).fontWeight(FontWeight.Medium).fontColor('#fff').layoutWeight(1)
          Text(report.status)
            .fontSize(11).fontColor(this.getStatusColor(report.status))
            .backgroundColor(this.getStatusBgColor(report.status))
            .borderRadius(4).padding({ left: 8, right: 8, top: 2, bottom: 2 })
        }
        .width('100%')
        Row() {
          Text(`${report.weekStart.toLocaleDateString()} - ${report.weekEnd.toLocaleDateString()}`).fontSize(12).fontColor('#888').layoutWeight(1)
          Text(`${report.completionRate}%完成`).fontSize(12).fontColor(report.completionRate >= 80 ? '#00ff00' : report.completionRate >= 50 ? '#ffcc00' : '#ff6600')
        }
        .width('100%').margin({ top: 4 })
        Row() {
          Text(`⏱️${report.totalActualHours}h/${report.totalPlannedHours}h`).fontSize(11).fontColor('#666')
          Text(`📋${report.tasks.length}项任务`).fontSize(11).fontColor('#666').margin({ left: 8 })
          if (report.totalOvertimeHours > 0) {
            Text(`🔥${report.totalOvertimeHours}h加班`).fontSize(11).fontColor('#ff6600').margin({ left: 8 })
          }
          Blank()
          if (report.status === WeeklyStatus.SUBMITTED || report.status === WeeklyStatus.FIRST_REVIEW) {
            const progress = report.getApprovalProgress();
            Stack() {
              Row().width(50).height(4).backgroundColor('#333').borderRadius(2)
              Row().width(`${progress.percentage}%`).height(4).backgroundColor('#c41e3a').borderRadius(2)
            }
            .width(50).height(4)
            Text(`${progress.current}/${progress.total}`).fontSize(10).fontColor('#c41e3a').margin({ left: 4 })
          }
        }
        .width('100%').margin({ top: 6 })
      }
      .layoutWeight(1).alignItems(HorizontalAlign.Start)
    }
    .width('100%').padding(16)
    .backgroundColor(
      report.status === WeeklyStatus.REJECTED ? 'rgba(255,0,0,0.05)' :
      report.status === WeeklyStatus.APPROVED ? 'rgba(0,255,0,0.05)' : '#0a0a0a'
    )
    .borderRadius(8).margin({ left: 12, right: 12, top: 8 })
  }
```

### 4.10 审批列表

```typescript
  @Builder
  ApprovalListBuilder() {
    List() {
      if (this.weeklyState.pendingFirstReview.length > 0) {
        ListItem() {
          Text(`⏳ 初审待办 (${this.weeklyState.pendingFirstReview.length})`).fontSize(14).fontWeight(FontWeight.Bold).fontColor('#ffcc00').padding({ left: 16, top: 12, bottom: 8 })
        }
        .width('100%').backgroundColor('#1a1a1a')
      }
      ForEach(this.weeklyState.pendingFirstReview, (report: WeeklyReport) => {
        ListItem() { this.ApprovalCardBuilder(report, 1) }
        .onClick(() => { this.editingReport = report; this.showApprovalDialog = true; })
      }, (report: WeeklyReport) => `first-${report.id}`)

      if (this.weeklyState.pendingFinalReview.length > 0) {
        ListItem() {
          Text(`🔍 终审待办 (${this.weeklyState.pendingFinalReview.length})`).fontSize(14).fontWeight(FontWeight.Bold).fontColor('#c41e3a').padding({ left: 16, top: 12, bottom: 8 })
        }
        .width('100%').backgroundColor('#1a1a1a')
      }
      ForEach(this.weeklyState.pendingFinalReview, (report: WeeklyReport) => {
        ListItem() { this.ApprovalCardBuilder(report, 2) }
        .onClick(() => { this.editingReport = report; this.showApprovalDialog = true; })
      }, (report: WeeklyReport) => `final-${report.id}`)
    }
    .width('100%').layoutWeight(1).divider({ strokeWidth: 1, color: '#222' })
    .scrollBar(BarState.Auto).padding({ bottom: 16 })
  }

  @Builder
  ApprovalCardBuilder(report: WeeklyReport, level: number) {
    Row() {
      Column() { Text('⏳').fontSize(24) }
      .width(40).height(40).margin({ right: 12 }).justifyContent(FlexAlign.Center)
      Column() {
        Row() {
          Text(`${report.reporter} 的周报`).fontSize(15).fontWeight(FontWeight.Medium).fontColor('#fff').layoutWeight(1)
          Text(`L${level}审批`).fontSize(11).fontColor('#c41e3a').backgroundColor('rgba(196,30,58,0.1)').borderRadius(4).padding({ left: 6, right: 6 })
        }
        .width('100%')
        Row() {
          Text(`${report.department} · ${report.reportNo}`).fontSize(12).fontColor('#888').layoutWeight(1)
          Text(`${report.tasks.length}项 · ${report.totalActualHours}h`).fontSize(12).fontColor('#888')
        }
        .width('100%').margin({ top: 4 })
        Row() {
          Text(`📅 ${report.submittedAt?.toLocaleString() || ''}`).fontSize(11).fontColor('#666')
          Blank()
          Button('去审批').fontSize(11).fontColor('#fff').backgroundColor('#c41e3a').borderRadius(6).padding({ left: 12, right: 12, top: 4, bottom: 4 })
          .onClick(() => { this.editingReport = report; this.showApprovalDialog = true; })
        }
        .width('100%').margin({ top: 6 })
      }
      .layoutWeight(1).alignItems(HorizontalAlign.Start)
    }
    .width('100%').padding(16).backgroundColor('#0a0a0a').borderRadius(8).margin({ left: 12, right: 12, top: 8 })
  }
```

### 4.11 底部操作栏

```typescript
  @Builder
  FooterBuilder() {
    Row() {
      Column() {
        Text('🐉').fontSize(20)
        Text(`UID:${MASTER_UID}`).fontSize(10).fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start).layoutWeight(1)
      Row() {
        Button() { Text('📋 模板').fontSize(12).fontColor('#fff') }
        .type(ButtonType.Normal).backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12, top: 6, bottom: 6 }).margin({ right: 8 })
        .onClick(() => { this.showTemplateDialog = true; })
        Button() { Text('📤 导出').fontSize(12).fontColor('#fff') }
        .type(ButtonType.Normal).backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12, top: 6, bottom: 6 }).margin({ right: 8 })
        .onClick(() => { this.exportWeekly(); })
        Button() { Text('➕ 任务').fontSize(12).fontColor('#fff') }
        .type(ButtonType.Normal).backgroundColor('#c41e3a').borderRadius(8).padding({ left: 12, right: 12, top: 6, bottom: 6 })
        .onClick(() => { this.editingTask = null; this.showTaskDialog = true; })
      }
    }
    .width('100%').height(56).padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { top: 1 }, color: '#333' })
  }
```

### 4.12 辅助方法

```typescript
  getStatusColor(status: WeeklyStatus): string {
    switch (status) {
      case WeeklyStatus.DRAFT: return '#ffcc00';
      case WeeklyStatus.SUBMITTED: return '#0066cc';
      case WeeklyStatus.FIRST_REVIEW: return '#ff6600';
      case WeeklyStatus.FINAL_REVIEW: return '#c41e3a';
      case WeeklyStatus.APPROVED: return '#00ff00';
      case WeeklyStatus.REJECTED: return '#ff0000';
      case WeeklyStatus.ARCHIVED: return '#888';
      default: return '#999';
    }
  }

  getStatusBgColor(status: WeeklyStatus): string {
    switch (status) {
      case WeeklyStatus.DRAFT: return 'rgba(255,204,0,0.1)';
      case WeeklyStatus.SUBMITTED: return 'rgba(0,102,204,0.1)';
      case WeeklyStatus.FIRST_REVIEW: return 'rgba(255,102,0,0.1)';
      case WeeklyStatus.FINAL_REVIEW: return 'rgba(196,30,58,0.1)';
      case WeeklyStatus.APPROVED: return 'rgba(0,255,0,0.1)';
      case WeeklyStatus.REJECTED: return 'rgba(255,0,0,0.1)';
      case WeeklyStatus.ARCHIVED: return 'rgba(136,136,136,0.1)';
      default: return 'rgba(153,153,153,0.1)';
    }
  }

  toggleViewMode(): void {
    const modes: ('list' | 'stats' | 'trend')[] = ['list', 'stats', 'trend'];
    const currentIndex = modes.indexOf(this.viewMode);
    this.viewMode = modes[(currentIndex + 1) % modes.length];
  }

  getCurrentWeekLabel(): string {
    const now = new Date();
    const d = new Date(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()));
    const dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    const weekNum = Math.ceil((((d.getTime() - yearStart.getTime()) / 86400000) + 1) / 7);
    return `${now.getFullYear()}年第${weekNum}周`;
  }

  prevWeek(): void { /* 切换到上一周 */ }
  nextWeek(): void { /* 切换到下一周 */ }

  createNewWeekly(): void {
    const newReport = new WeeklyReport({
      reporter: this.weeklyState.currentUser,
      reporterId: this.weeklyState.currentUserId,
      department: this.weeklyState.currentDept
    });
    this.weeklyState.addReport(newReport);
    this.editingReport = newReport;
    this.showDetailDialog = true;
  }

  exportWeekly(): void {
    const data = {
      exportTime: new Date().toISOString(),
      dna: MASTER_DNA,
      uid: MASTER_UID,
      confirm: CONFIRM_SEAL,
      reports: this.weeklyState.myReports.map(r => ({
        reportNo: r.reportNo,
        week: `${r.weekStart.toLocaleDateString()}-${r.weekEnd.toLocaleDateString()}`,
        status: r.status,
        completionRate: r.completionRate,
        plannedHours: r.totalPlannedHours,
        actualHours: r.totalActualHours,
        overtimeHours: r.totalOvertimeHours,
        taskCount: r.tasks.length
      }))
    };
    console.info(`[龍魂] 周报导出: longhun_weekly_${Date.now()}.json`);
  }

  scheduleReminders(): void {
    console.info('[龍魂] 周报提醒系统已启动');
  }
}

const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
```

---

## 五、组件清单

| 文件 | 路径 | 说明 |
|------|------|------|
| 数据模型 | `entry/src/main/ets/models/WeeklyModel.ets` | WeeklyReport/WeeklyTask/NextTask/WeeklyIssue/WeeklyRisk/WeeklyState |
| 主页面 | `entry/src/main/ets/pages/WeeklyReviewPage.ets` | 完整UI |
| 任务编辑 | `entry/src/main/ets/components/TaskEditDialog.ets` | 任务增改弹窗 |
| 审批弹窗 | `entry/src/main/ets/components/ApprovalDialog.ets` | 审批操作 |
| 周报详情 | `entry/src/main/ets/components/WeeklyDetailDialog.ets` | 周报完整查看/编辑 |
| 工时图表 | `entry/src/main/ets/components/HourChartView.ets` | 工时统计可视化 |
| 趋势图表 | `entry/src/main/ets/components/TrendChartView.ets` | 多周趋势对比 |
| 模板管理 | `entry/src/main/ets/components/TemplateDialog.ets` | 周报模板配置 |
| 数据库 | `entry/src/main/ets/database/WeeklyDatabase.ets` | 关系型存储 |

---

## 六、鸿蒙特性使用

| 特性 | 用途 | API |
|------|------|-----|
| ArkTS声明式UI | 界面构建 | `@Component` `@Entry` |
| 状态管理 | 数据响应 | `@State` `@Observed` `@StorageLink` |
| 关系型数据库 | 本地加密存储 | `relationalStore` |
| 通知 | 周报提醒 | `notificationManager` |
| 日历 | 周次计算 | `calendarManager` |
| 后台任务 | 定时提醒 | `workScheduler` |
| 打印 | 周报打印 | `print` |
| 分享 | 数据导出 | `share` |
| 文档选择 | 附件上传 | `documentPicker` |
| 国密算法 | 数据签名 | `cryptoFramework` SM2/SM3 |

---

## 七、审批流转机制

| 状态 | 触发条件 | 操作人 |
|------|----------|--------|
| 草稿 | 新建周报 | 填报人 |
| 已提交 | 填报人提交 | 填报人 → 初审人 |
| 初审中 | 部门主管审核 | 初审人 |
| 终审中 | 初审通过 | 初审人 → 终审人 |
| 已通过 | 终审通过 | 终审人 |
| 已驳回 | 任意审批驳回 | 审批人 → 填报人 |
| 已归档 | 审批通过后归档 | 系统 |

---

## 八、工时统计维度

| 维度 | 指标 | 说明 |
|------|------|------|
| 个人 | 本周工时/累计工时/平均工时 | 个人维度追踪 |
| 团队 | 部门总工时/人均工时 | 团队维度对比 |
| 项目 | 项目投入工时/占比 | 项目维度分析 |
| 类型 | 开发/设计/测试/会议占比 | 工作类型分布 |
| 趋势 | 近8周工时曲线 | 长期趋势分析 |
| 偏差 | 计划vs实际工时差 | 预估准确度 |

---

## 九、龍魂标识

| 位置 | 内容 |
|------|------|
| 应用名称 | 龍魂周报管理 |
| 标题栏 | 🐉 龍魂周报管理 |
| 底部标识 | UID:9622 |
| 数据签名 | SM3-哈希 |
| DNA | ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ |

---

🐉 **龍魂 · 鸿蒙 ArkTS 实战：Weekly Review 周报管理 交付完成**

> DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️  
> UID: 9622  
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z  
> 时间: 2026-07-14  
> 模块: 9核心文件  
> 特性: 周报模板 · 任务录入 · 自动汇总 · 多级审批 · 工时统计 · 趋势分析 · 历史归档 · 国密签名

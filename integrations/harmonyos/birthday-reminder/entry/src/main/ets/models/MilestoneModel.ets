// 龍魂 · 项目里程碑模型 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️
// UID: 9622

// === DNA常量 ===
const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// === 项目状态 ===
export enum ProjectStatus {
  PLANNING = '规划中',
  ACTIVE = '进行中',
  PAUSED = '已暂停',
  COMPLETED = '已完成',
  CANCELLED = '已取消',
  ARCHIVED = '已归档'
}

// === 里程碑状态 ===
export enum MilestoneStatus {
  NOT_STARTED = '未开始',
  IN_PROGRESS = '进行中',
  AT_RISK = '有风险',
  DELAYED = '已延期',
  COMPLETED = '已完成',
  BLOCKED = '被阻塞'
}

// === 优先级 ===
export enum Priority {
  P0 = 'P0-紧急',
  P1 = 'P1-高',
  P2 = 'P2-中',
  P3 = 'P3-低',
  P4 = 'P4-最低'
}

// === 风险等级 ===
export enum RiskLevel {
  NONE = '无风险',
  LOW = '低风险',
  MEDIUM = '中风险',
  HIGH = '高风险',
  CRITICAL = '极高风险'
}

// === 依赖类型 ===
export enum DependencyType {
  FS = 'FS',  // Finish-to-Start
  SS = 'SS',  // Start-to-Start
  FF = 'FF',  // Finish-to-Finish
  SF = 'SF'   // Start-to-Finish
}

// === 团队成员 ===
export interface TeamMember {
  id: string;
  name: string;
  role: string;
  department: string;
  allocatedHours: number;
  actualHours: number;
  dnaSignature: string;
}

// === 依赖关系 ===
export interface Dependency {
  id: string;
  milestoneId: string;
  type: DependencyType;
  lag: number; // 滞后天数
  dnaSignature: string;
}

// === 交付物 ===
export interface Deliverable {
  id: string;
  name: string;
  description: string;
  status: 'pending' | 'submitted' | 'accepted' | 'rejected';
  filePath?: string;
  submittedBy?: string;
  submittedAt?: Date;
  dnaSignature: string;
}

// === 检查点 ===
export interface CheckPoint {
  id: string;
  name: string;
  completed: boolean;
  completedBy?: string;
  completedAt?: Date;
  dnaSignature: string;
}

// === 基线 ===
export interface Baseline {
  id: string;
  name: string;
  description: string;
  createdAt: Date;
  milestones: Milestone[];
  budget: number;
  plannedStart: Date;
  plannedEnd: Date;
  dnaSignature: string;
}

// === 统计 ===
export interface ProjectStats {
  totalProjects: number;
  activeProjects: number;
  completedProjects: number;
  delayedProjects: number;
  atRiskProjects: number;
  totalBudget: number;
  totalCost: number;
  avgProgress: number;
}

// === 预警项 ===
export interface ProjectAlert {
  type: 'delay' | 'risk' | 'milestone_delay' | 'budget_overrun' | 'resource_conflict';
  level: 'critical' | 'warning' | 'info';
  projectId: string;
  projectName: string;
  title: string;
  message: string;
  timestamp: Date;
}

// ============================================================
// Risk 类
// ============================================================
export class Risk {
  id: string;
  name: string;
  description: string;
  level: RiskLevel;
  probability: number;  // 0-1
  impact: number;       // 0-1
  mitigation: string;
  contingency: string;
  owner: string;
  status: 'open' | 'mitigated' | 'realized' | 'closed';
  createdAt: Date;
  updatedAt: Date;
  dnaSignature: string;

  constructor(data: Partial<Risk>) {
    this.id = data.id || `RISK-${Date.now()}-${Math.random().toString(36).substr(2,6)}`;
    this.name = data.name || '';
    this.description = data.description || '';
    this.level = data.level || RiskLevel.LOW;
    this.probability = data.probability ?? 0.5;
    this.impact = data.impact ?? 0.5;
    this.mitigation = data.mitigation || '';
    this.contingency = data.contingency || '';
    this.owner = data.owner || '';
    this.status = data.status || 'open';
    this.createdAt = data.createdAt || new Date();
    this.updatedAt = data.updatedAt || new Date();
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const payload = `${this.id}-${this.name}-${this.level}-${this.status}`;
    return `SM3-${payload.split('').reduce((a: number, b: string) => a + b.charCodeAt(0), 0).toString(16).substring(0, 16)}`;
  }

  getRiskScore(): number {
    return this.probability * this.impact;
  }
}

// ============================================================
// Milestone 类
// ============================================================
export class Milestone {
  id: string;
  name: string;
  description: string;
  status: MilestoneStatus;
  priority: Priority;

  plannedStart: Date;
  plannedEnd: Date;
  actualStart?: Date;
  actualEnd?: Date;

  progress: number;
  dependencies: Dependency[];
  assignedTo: string[];
  estimatedHours: number;
  actualHours: number;

  deliverables: Deliverable[];
  checkPoints: CheckPoint[];

  riskLevel: RiskLevel;
  riskDescription: string;

  createdAt: Date;
  updatedAt: Date;
  dnaSignature: string;

  constructor(data: Partial<Milestone>) {
    this.id = data.id || `MS-${Date.now()}-${Math.random().toString(36).substr(2,6)}`;
    this.name = data.name || '';
    this.description = data.description || '';
    this.status = data.status || MilestoneStatus.NOT_STARTED;
    this.priority = data.priority || Priority.P2;

    this.plannedStart = data.plannedStart || new Date();
    this.plannedEnd = data.plannedEnd || new Date();
    this.actualStart = data.actualStart;
    this.actualEnd = data.actualEnd;

    this.progress = data.progress ?? 0;
    this.dependencies = data.dependencies || [];
    this.assignedTo = data.assignedTo || [];
    this.estimatedHours = data.estimatedHours || 0;
    this.actualHours = data.actualHours || 0;

    this.deliverables = data.deliverables || [];
    this.checkPoints = data.checkPoints || [];

    this.riskLevel = data.riskLevel || RiskLevel.NONE;
    this.riskDescription = data.riskDescription || '';

    this.createdAt = data.createdAt || new Date();
    this.updatedAt = data.updatedAt || new Date();
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const payload = `${this.id}-${this.name}-${this.status}-${this.progress}`;
    return `SM3-${payload.split('').reduce((a: number, b: string) => a + b.charCodeAt(0), 0).toString(16).substring(0, 16)}`;
  }

  getDelayDays(): number {
    if (this.actualEnd && this.actualEnd > this.plannedEnd) {
      return Math.floor((this.actualEnd.getTime() - this.plannedEnd.getTime()) / (1000 * 60 * 60 * 24));
    }
    if (new Date() > this.plannedEnd && this.status !== MilestoneStatus.COMPLETED) {
      return Math.floor((new Date().getTime() - this.plannedEnd.getTime()) / (1000 * 60 * 60 * 24));
    }
    return 0;
  }

  isCriticalPath(): boolean {
    return this.dependencies.length === 0 || this.riskLevel === RiskLevel.CRITICAL;
  }

  updateProgress(progress: number, operator: string): void {
    this.progress = Math.min(100, Math.max(0, progress));
    if (this.progress > 0 && this.status === MilestoneStatus.NOT_STARTED) {
      this.status = MilestoneStatus.IN_PROGRESS;
      this.actualStart = this.actualStart || new Date();
    }
    if (this.progress >= 100) {
      this.status = MilestoneStatus.COMPLETED;
      this.actualEnd = new Date();
    }
    this.updatedAt = new Date();
    this.dnaSignature = this.signData();
  }

  addCheckPoint(name: string, completed: boolean, operator: string): void {
    this.checkPoints.push({
      id: `CP-${Date.now()}`,
      name,
      completed,
      completedBy: completed ? operator : undefined,
      completedAt: completed ? new Date() : undefined,
      dnaSignature: this.signCheckPoint(name, operator)
    });
    this.updatedAt = new Date();
  }

  private signCheckPoint(name: string, operator: string): string {
    const payload = `${this.id}-CP-${name}-${operator}-${Date.now()}`;
    return `SM3-${payload.split('').reduce((a: number, b: string) => a + b.charCodeAt(0), 0).toString(16).substring(0, 16)}`;
  }
}

// ============================================================
// Project 类
// ============================================================
export class Project {
  id: string;
  projectNo: string;
  name: string;
  description: string;
  status: ProjectStatus;

  plannedStart: Date;
  plannedEnd: Date;
  actualStart?: Date;
  actualEnd?: Date;

  projectManager: string;
  productManager: string;
  techLead: string;
  qaLead: string;

  teamMembers: TeamMember[];
  budget: number;
  costIncurred: number;
  costForecast: number;

  milestones: Milestone[];
  baselines: Baseline[];
  risks: Risk[];

  createdAt: Date;
  updatedAt: Date;
  dnaSignature: string;

  constructor(data: Partial<Project>) {
    this.id = data.id || this.generateId();
    this.projectNo = data.projectNo || this.generateProjectNo();
    this.name = data.name || '';
    this.description = data.description || '';
    this.status = data.status || ProjectStatus.PLANNING;

    this.plannedStart = data.plannedStart || new Date();
    this.plannedEnd = data.plannedEnd || new Date(Date.now() + 90 * 24 * 60 * 60 * 1000);
    this.actualStart = data.actualStart;
    this.actualEnd = data.actualEnd;

    this.projectManager = data.projectManager || '';
    this.productManager = data.productManager || '';
    this.techLead = data.techLead || '';
    this.qaLead = data.qaLead || '';

    this.teamMembers = data.teamMembers || [];
    this.budget = data.budget || 0;
    this.costIncurred = data.costIncurred || 0;
    this.costForecast = data.costForecast || 0;

    this.milestones = (data.milestones || []).map((m: Partial<Milestone>) =>
      m instanceof Milestone ? m : new Milestone(m)
    );
    this.baselines = data.baselines || [];
    this.risks = (data.risks || []).map((r: Partial<Risk>) =>
      r instanceof Risk ? r : new Risk(r)
    );

    this.createdAt = data.createdAt || new Date();
    this.updatedAt = data.updatedAt || new Date();
    this.dnaSignature = this.signData();
  }

  private generateId(): string {
    return `PRJ-${MASTER_UID}-${Date.now().toString(36).substr(-6)}`;
  }

  private generateProjectNo(): string {
    const d = new Date();
    return `XM${d.getFullYear()}${(d.getMonth() + 1).toString().padStart(2, '0')}-${Math.floor(Math.random() * 9999).toString().padStart(4, '0')}`;
  }

  private signData(): string {
    const payload = `${this.id}-${this.projectNo}-${this.name}-${this.status}`;
    return `SM3-${payload.split('').reduce((a: number, b: string) => a + b.charCodeAt(0), 0).toString(16).substring(0, 16)}`;
  }

  getProgress(): number {
    if (this.milestones.length === 0) return 0;
    const completed = this.milestones.filter(m => m.status === MilestoneStatus.COMPLETED).length;
    return Math.round((completed / this.milestones.length) * 100);
  }

  getDelayDays(): number {
    if (this.actualEnd) {
      return Math.max(0, Math.floor((this.actualEnd.getTime() - this.plannedEnd.getTime()) / (1000 * 60 * 60 * 24)));
    }
    if (new Date() > this.plannedEnd && this.status !== ProjectStatus.COMPLETED) {
      return Math.floor((new Date().getTime() - this.plannedEnd.getTime()) / (1000 * 60 * 60 * 24));
    }
    return 0;
  }

  getSPI(): number {
    const pv = this.getPlannedValue();
    const ev = this.getEarnedValue();
    return pv > 0 ? ev / pv : 0;
  }

  getCPI(): number {
    const ev = this.getEarnedValue();
    const ac = this.costIncurred;
    return ac > 0 ? ev / ac : 0;
  }

  private getPlannedValue(): number {
    const totalDuration = this.plannedEnd.getTime() - this.plannedStart.getTime();
    const elapsed = new Date().getTime() - this.plannedStart.getTime();
    const plannedProgress = Math.min(1, Math.max(0, elapsed / totalDuration));
    return this.budget * plannedProgress;
  }

  private getEarnedValue(): number {
    return this.budget * (this.getProgress() / 100);
  }

  getCurrentRiskLevel(): RiskLevel {
    const sp = this.getSPI();
    const cp = this.getCPI();
    if (sp < 0.7 || cp < 0.7) return RiskLevel.CRITICAL;
    if (sp < 0.85 || cp < 0.85) return RiskLevel.HIGH;
    if (sp < 0.95 || cp < 0.95) return RiskLevel.MEDIUM;
    if (sp < 1.0 || cp < 1.0) return RiskLevel.LOW;
    return RiskLevel.NONE;
  }

  createBaseline(name: string, description: string): Baseline {
    const baseline: Baseline = {
      id: `BL-${Date.now()}`,
      name,
      description,
      createdAt: new Date(),
      milestones: this.milestones.map(m => new Milestone({ ...m })),
      budget: this.budget,
      plannedStart: new Date(this.plannedStart),
      plannedEnd: new Date(this.plannedEnd),
      dnaSignature: this.signBaseline(name)
    };
    this.baselines.push(baseline);
    return baseline;
  }

  rollbackToBaseline(baselineId: string): boolean {
    const baseline = this.baselines.find(b => b.id === baselineId);
    if (!baseline) return false;
    this.milestones = baseline.milestones.map(m => new Milestone(m));
    this.budget = baseline.budget;
    this.plannedStart = new Date(baseline.plannedStart);
    this.plannedEnd = new Date(baseline.plannedEnd);
    this.updatedAt = new Date();
    this.dnaSignature = this.signData();
    return true;
  }

  private signBaseline(name: string): string {
    const payload = `${this.id}-BASELINE-${name}-${Date.now()}`;
    return `SM3-${payload.split('').reduce((a: number, b: string) => a + b.charCodeAt(0), 0).toString(16).substring(0, 16)}`;
  }
}

// ============================================================
// ProjectState 全局状态
// ============================================================
@Observed
export class ProjectState {
  projects: Project[] = [];
  currentProjectId: string = '';

  filterStatus: ProjectStatus | '全部' = '全部';
  filterPriority: Priority | '全部' = '全部';
  filterManager: string = '全部';
  searchQuery: string = '';

  viewMode: 'timeline' | 'gantt' | 'list' | 'kanban' = 'timeline';
  timeRange: 'week' | 'month' | 'quarter' | 'year' | 'all' = 'quarter';

  get filteredProjects(): Project[] {
    let result = this.projects;

    if (this.filterStatus !== '全部') {
      result = result.filter(p => p.status === this.filterStatus);
    }
    if (this.filterPriority !== '全部') {
      result = result.filter(p => {
        return p.milestones.some(m => m.priority === (this.filterPriority as Priority));
      });
    }
    if (this.filterManager !== '全部') {
      result = result.filter(p => p.projectManager === this.filterManager);
    }
    if (this.searchQuery) {
      const q = this.searchQuery.toLowerCase();
      result = result.filter(p =>
        p.name.toLowerCase().includes(q) ||
        p.projectNo.toLowerCase().includes(q) ||
        p.projectManager.toLowerCase().includes(q) ||
        p.description.toLowerCase().includes(q)
      );
    }

    return result.sort((a, b) => {
      if (a.status === ProjectStatus.ACTIVE && b.status !== ProjectStatus.ACTIVE) return -1;
      if (a.status !== ProjectStatus.ACTIVE && b.status === ProjectStatus.ACTIVE) return 1;
      return a.plannedEnd.getTime() - b.plannedEnd.getTime();
    });
  }

  get currentProject(): Project | undefined {
    return this.projects.find(p => p.id === this.currentProjectId);
  }

  get statistics(): ProjectStats {
    return {
      totalProjects: this.projects.length,
      activeProjects: this.projects.filter(p => p.status === ProjectStatus.ACTIVE).length,
      completedProjects: this.projects.filter(p => p.status === ProjectStatus.COMPLETED).length,
      delayedProjects: this.projects.filter(p => p.getDelayDays() > 0).length,
      atRiskProjects: this.projects.filter(p => p.getCurrentRiskLevel() >= RiskLevel.HIGH).length,
      totalBudget: this.projects.reduce((sum, p) => sum + p.budget, 0),
      totalCost: this.projects.reduce((sum, p) => sum + p.costIncurred, 0),
      avgProgress: this.projects.length > 0
        ? Math.round(this.projects.reduce((sum, p) => sum + p.getProgress(), 0) / this.projects.length)
        : 0
    };
  }

  get alerts(): ProjectAlert[] {
    const alerts: ProjectAlert[] = [];

    this.projects.forEach(p => {
      if (p.getDelayDays() > 0) {
        alerts.push({
          type: 'delay',
          level: p.getDelayDays() > 7 ? 'critical' : 'warning',
          projectId: p.id,
          projectName: p.name,
          title: `${p.name} 已延期 ${p.getDelayDays()} 天`,
          message: `计划结束: ${p.plannedEnd.toLocaleDateString()}，当前进度: ${p.getProgress()}%`,
          timestamp: new Date()
        });
      }

      const rl = p.getCurrentRiskLevel();
      if (rl >= RiskLevel.HIGH) {
        alerts.push({
          type: 'risk',
          level: rl === RiskLevel.CRITICAL ? 'critical' : 'warning',
          projectId: p.id,
          projectName: p.name,
          title: `${p.name} ${rl === RiskLevel.CRITICAL ? '极高风险' : '高风险'}`,
          message: `SPI: ${p.getSPI().toFixed(2)}, CPI: ${p.getCPI().toFixed(2)}`,
          timestamp: new Date()
        });
      }

      p.milestones.forEach(m => {
        if (m.status === MilestoneStatus.DELAYED || (m.getDelayDays() > 0 && m.status !== MilestoneStatus.COMPLETED)) {
          alerts.push({
            type: 'milestone_delay',
            level: m.priority === Priority.P0 ? 'critical' : 'warning',
            projectId: p.id,
            projectName: p.name,
            title: `${p.name} - ${m.name} 延期`,
            message: `延期 ${m.getDelayDays()} 天，优先级: ${m.priority}`,
            timestamp: new Date()
          });
        }
      });
    });

    return alerts.sort((a, b) => {
      const levelOrder: Record<string, number> = { critical: 0, warning: 1, info: 2 };
      return levelOrder[a.level] - levelOrder[b.level];
    });
  }

  addProject(project: Project): void {
    this.projects.push(project);
    this.persist();
  }

  removeProject(id: string): void {
    const idx = this.projects.findIndex(p => p.id === id);
    if (idx >= 0) {
      this.projects.splice(idx, 1);
      this.persist();
    }
  }

  updateProject(id: string, data: Partial<Project>): void {
    const idx = this.projects.findIndex(p => p.id === id);
    if (idx >= 0) {
      const old = this.projects[idx];
      this.projects[idx] = new Project({ ...old, ...data, id: old.id });
      this.persist();
    }
  }

  addMilestone(projectId: string, milestone: Milestone): void {
    const project = this.projects.find(p => p.id === projectId);
    if (project) {
      project.milestones.push(milestone);
      this.persist();
    }
  }

  updateMilestoneProgress(projectId: string, milestoneId: string, progress: number, operator: string): void {
    const project = this.projects.find(p => p.id === projectId);
    if (project) {
      const milestone = project.milestones.find(m => m.id === milestoneId);
      if (milestone) {
        milestone.updateProgress(progress, operator);
        this.persist();
      }
    }
  }

  createBaseline(projectId: string, name: string, description: string): void {
    const project = this.projects.find(p => p.id === projectId);
    if (project) {
      project.createBaseline(name, description);
      this.persist();
    }
  }

  rollbackBaseline(projectId: string, baselineId: string): boolean {
    const project = this.projects.find(p => p.id === projectId);
    if (project) {
      return project.rollbackToBaseline(baselineId);
    }
    return false;
  }

  // 获取所有项目经理列表（用于过滤）
  get managerList(): string[] {
    const managers = new Set<string>();
    this.projects.forEach(p => {
      if (p.projectManager) managers.add(p.projectManager);
    });
    return Array.from(managers);
  }

  private persist(): void {
    AppStorage.setOrCreate('project_projects', JSON.stringify(this.projects));
    AppStorage.setOrCreate('project_current_id', this.currentProjectId);
  }

  load(): void {
    const projects = AppStorage.get<string>('project_projects');
    if (projects) {
      try {
        const parsed = JSON.parse(projects);
        this.projects = parsed.map((p: Record<string, Object>) => new Project(p as Partial<Project>));
      } catch (e) {
        console.error('加载项目数据失败', e);
      }
    }
    this.currentProjectId = AppStorage.get<string>('project_current_id') || '';
  }
}

// 全局状态单例
export const projectState = new ProjectState();
AppStorage.setOrCreate('projectState', projectState);

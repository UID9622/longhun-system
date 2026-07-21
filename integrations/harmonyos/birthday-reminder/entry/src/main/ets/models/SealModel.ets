// 龍魂 · 印章管理模型 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️
// UID: 9622

// === DNA常量 ===
const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// === 印章类型 ===
export enum SealType {
  OFFICIAL = '公章',
  FINANCE = '财务专用章',
  CONTRACT = '合同专用章',
  LEGAL = '法人章',
  INVOICE = '发票专用章',
  HR = '人事专用章',
  PROJECT = '项目专用章',
  DEPARTMENT = '部门章',
  OTHER = '其他'
}

// === 印章材质 ===
export enum SealMaterial {
  BRONZE = '铜质',
  JADE = '玉质',
  HORN = '牛角',
  WOOD = '木质',
  CRYSTAL = '水晶',
  METAL = '合金',
  OTHER = '其他'
}

// === 印章状态 ===
export enum SealStatus {
  IN_VAULT = '在库',
  IN_USE = '使用中',
  OUTSIDE = '外带',
  MAINTENANCE = '维护中',
  FROZEN = '冻结',
  DESTROYED = '已销毁'
}

// === 用印类型 ===
export enum UsageType {
  CONTRACT = '合同签署',
  FINANCE = '财务票据',
  HR = '人事文件',
  CERTIFICATE = '证明文书',
  AUTHORIZATION = '授权委托',
  OFFICIAL = '公文往来',
  BANK = '银行业务',
  LEGAL = '法律文件',
  OTHER = '其他'
}

// === 审批级别 ===
export enum ApprovalLevel {
  LEVEL0 = '免审批',
  LEVEL1 = '部门主管',
  LEVEL2 = '分管领导',
  LEVEL3 = '总经理',
  LEVEL4 = '董事会'
}

// === 审批记录 ===
export interface ApprovalRecord {
  level: number;
  approver: string;
  comment: string;
  signature: string;
  timestamp: Date;
  dnaSignature: string;
}

// === GPS点 ===
export interface GpsPoint {
  lat: number;
  lng: number;
  accuracy: number;
  timestamp: Date;
  dnaSignature: string;
}

// === 回传记录 ===
export interface CheckInRecord {
  timestamp: Date;
  location: string;
  photoPath: string;
  operator: string;
  dnaSignature: string;
}

// === 统计 ===
export interface SealStats {
  totalSeals: number;
  inVault: number;
  inUse: number;
  outside: number;
  totalApplications: number;
  pendingCount: number;
  todayExecutions: number;
  overdueCount: number;
}

// === 预警项 ===
export interface AlertItem {
  type: 'overdue' | 'pending' | 'low_stock' | 'expired';
  level: 'critical' | 'warning' | 'info';
  title: string;
  message: string;
  timestamp: Date;
}

// === 印章档案 ===
export class Seal {
  id: string;
  sealNo: string;
  name: string;
  type: SealType;
  material: SealMaterial;
  status: SealStatus;

  diameter: number;
  shape: '圆形' | '方形' | '椭圆形' | '其他';
  pattern: string;
  font: string;

  custodian: string;
  deputyCustodian: string;
  department: string;
  vaultLocation: string;
  safeNo: string;

  rfidTag: string;
  fingerprintLock: boolean;
  faceLock: boolean;
  gpsTracker: boolean;

  engraveDate: Date;
  recordDate: Date;
  expiryDate?: Date;
  lastUsedDate?: Date;
  useCount: number;
  destroyDate?: Date;

  createdAt: Date;
  updatedAt: Date;
  dnaSignature: string;

  constructor(data: Partial<Seal>) {
    this.id = data.id || this.generateId();
    this.sealNo = data.sealNo || this.generateSealNo(data.type || SealType.OFFICIAL);
    this.name = data.name || '';
    this.type = data.type || SealType.OFFICIAL;
    this.material = data.material || SealMaterial.BRONZE;
    this.status = data.status || SealStatus.IN_VAULT;

    this.diameter = data.diameter || 40;
    this.shape = data.shape || '圆形';
    this.pattern = data.pattern || '';
    this.font = data.font || '宋体';

    this.custodian = data.custodian || '';
    this.deputyCustodian = data.deputyCustodian || '';
    this.department = data.department || '';
    this.vaultLocation = data.vaultLocation || '';
    this.safeNo = data.safeNo || '';

    this.rfidTag = data.rfidTag || '';
    this.fingerprintLock = data.fingerprintLock || false;
    this.faceLock = data.faceLock || false;
    this.gpsTracker = data.gpsTracker || false;

    this.engraveDate = data.engraveDate || new Date();
    this.recordDate = data.recordDate || new Date();
    this.expiryDate = data.expiryDate;
    this.lastUsedDate = data.lastUsedDate;
    this.useCount = data.useCount || 0;
    this.destroyDate = data.destroyDate;

    this.createdAt = data.createdAt || new Date();
    this.updatedAt = data.updatedAt || new Date();
    this.dnaSignature = this.signData();
  }

  private generateId(): string {
    return `SEAL-${MASTER_UID}-${Date.now().toString(36).substr(-6)}`;
  }

  private generateSealNo(type: SealType): string {
    const prefix = type.substring(0, 2);
    const date = new Date();
    return `${prefix}${date.getFullYear()}${(date.getMonth() + 1).toString().padStart(2, '0')}-${Math.floor(Math.random() * 999).toString().padStart(3, '0')}`;
  }

  private signData(): string {
    const payload = `${this.id}-${this.sealNo}-${this.custodian}-${this.status}`;
    return `SM3-${payload.split('').reduce((a, b) => a + b.charCodeAt(0), 0).toString(16).substring(0, 16)}`;
  }

  updateStatus(newStatus: SealStatus, operator: string): void {
    this.status = newStatus;
    if (newStatus === SealStatus.IN_USE) {
      this.lastUsedDate = new Date();
      this.useCount++;
    }
    this.updatedAt = new Date();
    this.dnaSignature = this.signData();
  }
}

// === 用印申请 ===
export class SealApplication {
  id: string;
  appNo: string;
  sealId: string;
  sealName: string;
  sealType: SealType;

  applicant: string;
  department: string;
  applyDate: Date;
  usageType: UsageType;
  usageDesc: string;
  documentName: string;
  documentCount: number;
  documentPages: number;
  urgency: '普通' | '紧急' | '特急';

  documentPath?: string;
  attachmentPaths: string[];

  approvalLevel: ApprovalLevel;
  approvals: ApprovalRecord[];

  executor?: string;
  executeTime?: Date;
  executeLocation?: string;
  witness?: string;
  photos: string[];
  gpsLocation?: { lat: number; lng: number };
  fingerprintVerify: boolean;
  faceVerify: boolean;

  result: 'pending' | 'approved' | 'rejected' | 'executed' | 'cancelled';
  actualCount?: number;
  remarks: string;

  createdAt: Date;
  updatedAt: Date;
  dnaSignature: string;

  constructor(data: Partial<SealApplication>) {
    this.id = data.id || `APP-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`;
    this.appNo = data.appNo || this.generateAppNo();
    this.sealId = data.sealId || '';
    this.sealName = data.sealName || '';
    this.sealType = data.sealType || SealType.OFFICIAL;

    this.applicant = data.applicant || '';
    this.department = data.department || '';
    this.applyDate = data.applyDate || new Date();
    this.usageType = data.usageType || UsageType.OTHER;
    this.usageDesc = data.usageDesc || '';
    this.documentName = data.documentName || '';
    this.documentCount = data.documentCount || 1;
    this.documentPages = data.documentPages || 1;
    this.urgency = data.urgency || '普通';

    this.documentPath = data.documentPath;
    this.attachmentPaths = data.attachmentPaths || [];

    this.approvalLevel = data.approvalLevel || ApprovalLevel.LEVEL1;
    this.approvals = data.approvals || [];

    this.executor = data.executor;
    this.executeTime = data.executeTime;
    this.executeLocation = data.executeLocation;
    this.witness = data.witness;
    this.photos = data.photos || [];
    this.gpsLocation = data.gpsLocation;
    this.fingerprintVerify = data.fingerprintVerify || false;
    this.faceVerify = data.faceVerify || false;

    this.result = data.result || 'pending';
    this.actualCount = data.actualCount;
    this.remarks = data.remarks || '';

    this.createdAt = data.createdAt || new Date();
    this.updatedAt = data.updatedAt || new Date();
    this.dnaSignature = this.signData();
  }

  private generateAppNo(): string {
    const date = new Date();
    return `YY${date.getFullYear()}${(date.getMonth() + 1).toString().padStart(2, '0')}${date.getDate().toString().padStart(2, '0')}-${Math.floor(Math.random() * 9999).toString().padStart(4, '0')}`;
  }

  private signData(): string {
    const payload = `${this.id}-${this.appNo}-${this.sealId}-${this.applicant}`;
    return `SM3-${payload.split('').reduce((a, b) => a + b.charCodeAt(0), 0).toString(16).substring(0, 16)}`;
  }

  submit(): void {
    this.result = 'pending';
    this.updatedAt = new Date();
    this.dnaSignature = this.signData();
  }

  approve(level: number, approver: string, comment: string, signature: string): void {
    this.approvals.push({
      level,
      approver,
      comment,
      signature,
      timestamp: new Date(),
      dnaSignature: this.signApproval(level, approver, signature)
    });

    const requiredLevels = this.getRequiredLevels();
    if (this.approvals.length >= requiredLevels.length) {
      this.result = 'approved';
    }

    this.updatedAt = new Date();
    this.dnaSignature = this.signData();
  }

  reject(approver: string, comment: string): void {
    this.result = 'rejected';
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

  execute(executor: string, witness: string, photos: string[], location: { lat: number; lng: number }): void {
    this.executor = executor;
    this.witness = witness;
    this.photos = photos;
    this.gpsLocation = location;
    this.executeTime = new Date();
    this.executeLocation = `${location.lat.toFixed(6)},${location.lng.toFixed(6)}`;
    this.result = 'executed';
    this.updatedAt = new Date();
    this.dnaSignature = this.signData();
  }

  private getRequiredLevels(): number[] {
    switch (this.approvalLevel) {
      case ApprovalLevel.LEVEL0:
        return [];
      case ApprovalLevel.LEVEL1:
        return [1];
      case ApprovalLevel.LEVEL2:
        return [1, 2];
      case ApprovalLevel.LEVEL3:
        return [1, 2, 3];
      case ApprovalLevel.LEVEL4:
        return [1, 2, 3, 4];
      default:
        return [1];
    }
  }

  private getCurrentLevel(): number {
    return this.approvals.length + 1;
  }

  private signApproval(level: number, approver: string, signature: string): string {
    const payload = `${this.id}-L${level}-${approver}-${signature}-${Date.now()}`;
    return `SM3-${payload.split('').reduce((a, b) => a + b.charCodeAt(0), 0).toString(16).substring(0, 16)}`;
  }

  getApprovalProgress(): { current: number; total: number; percentage: number } {
    const total = this.getRequiredLevels().length;
    const current = this.approvals.filter(a => a.signature !== 'REJECTED').length;
    return {
      current,
      total,
      percentage: total > 0 ? Math.round((current / total) * 100) : 100
    };
  }
}

// === 印章外带记录 ===
export class SealOutRecord {
  id: string;
  sealId: string;
  sealName: string;
  borrower: string;
  borrowerDept: string;
  borrowDate: Date;
  expectedReturn: Date;
  actualReturn?: Date;
  purpose: string;
  destination: string;
  escort: string;
  gpsTrack: GpsPoint[];
  checkInRecords: CheckInRecord[];
  status: 'out' | 'returned' | 'overdue';
  dnaSignature: string;

  constructor(data: Partial<SealOutRecord>) {
    this.id = data.id || `OUT-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`;
    this.sealId = data.sealId || '';
    this.sealName = data.sealName || '';
    this.borrower = data.borrower || '';
    this.borrowerDept = data.borrowerDept || '';
    this.borrowDate = data.borrowDate || new Date();
    this.expectedReturn = data.expectedReturn || new Date(Date.now() + 24 * 60 * 60 * 1000);
    this.actualReturn = data.actualReturn;
    this.purpose = data.purpose || '';
    this.destination = data.destination || '';
    this.escort = data.escort || '';
    this.gpsTrack = data.gpsTrack || [];
    this.checkInRecords = data.checkInRecords || [];
    this.status = data.status || 'out';
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const payload = `${this.id}-${this.sealId}-${this.borrower}-${this.status}`;
    return `SM3-${payload.split('').reduce((a, b) => a + b.charCodeAt(0), 0).toString(16).substring(0, 16)}`;
  }

  addGpsPoint(lat: number, lng: number, accuracy: number): void {
    this.gpsTrack.push({
      lat, lng, accuracy,
      timestamp: new Date(),
      dnaSignature: this.signGps(lat, lng)
    });
  }

  checkIn(location: string, photoPath: string, operator: string): void {
    this.checkInRecords.push({
      timestamp: new Date(),
      location,
      photoPath,
      operator,
      dnaSignature: this.signCheckIn(location, operator)
    });
  }

  returnSeal(returner: string, witness: string): void {
    this.actualReturn = new Date();
    this.status = 'returned';
    this.dnaSignature = this.signData();
  }

  isOverdue(): boolean {
    return this.status === 'out' && new Date() > this.expectedReturn;
  }

  private signGps(lat: number, lng: number): string {
    return `SM3-${lat.toFixed(6)}-${lng.toFixed(6)}-${Date.now()}`;
  }

  private signCheckIn(location: string, operator: string): string {
    return `SM3-${location}-${operator}-${Date.now()}`;
  }
}

// === 印章全局状态 ===
@Observed
export class SealState {
  seals: Seal[] = [];
  applications: SealApplication[] = [];
  outRecords: SealOutRecord[] = [];

  currentUser: string = '';
  currentDept: string = '';
  userRole: 'admin' | 'custodian' | 'applicant' | 'approver' | 'witness' = 'applicant';

  filterStatus: SealStatus | '全部' = '全部';
  filterType: SealType | '全部' = '全部';
  searchQuery: string = '';

  alertOverdue: boolean = true;
  alertPending: boolean = true;

  get filteredSeals(): Seal[] {
    let result = this.seals;

    if (this.filterStatus !== '全部') {
      result = result.filter(s => s.status === this.filterStatus);
    }

    if (this.filterType !== '全部') {
      result = result.filter(s => s.type === this.filterType);
    }

    if (this.searchQuery) {
      const q = this.searchQuery.toLowerCase();
      result = result.filter(s =>
        s.name.toLowerCase().includes(q) ||
        s.sealNo.toLowerCase().includes(q) ||
        s.custodian.toLowerCase().includes(q) ||
        s.department.toLowerCase().includes(q)
      );
    }

    return result.sort((a, b) => b.useCount - a.useCount);
  }

  get pendingApprovals(): SealApplication[] {
    return this.applications.filter(a => a.result === 'pending');
  }

  get myApplications(): SealApplication[] {
    return this.applications.filter(a => a.applicant === this.currentUser);
  }

  get activeOutRecords(): SealOutRecord[] {
    return this.outRecords.filter(r => r.status === 'out');
  }

  get overdueRecords(): SealOutRecord[] {
    return this.outRecords.filter(r => r.isOverdue());
  }

  get statistics(): SealStats {
    return {
      totalSeals: this.seals.length,
      inVault: this.seals.filter(s => s.status === SealStatus.IN_VAULT).length,
      inUse: this.seals.filter(s => s.status === SealStatus.IN_USE).length,
      outside: this.seals.filter(s => s.status === SealStatus.OUTSIDE).length,
      totalApplications: this.applications.length,
      pendingCount: this.pendingApprovals.length,
      todayExecutions: this.applications.filter(a => {
        if (!a.executeTime)
          return false;
        const today = new Date();
        return a.executeTime.getDate() === today.getDate() &&
          a.executeTime.getMonth() === today.getMonth() &&
          a.executeTime.getFullYear() === today.getFullYear();
      }).length,
      overdueCount: this.overdueRecords.length
    };
  }

  addSeal(seal: Seal): void {
    this.seals.push(seal);
    this.persist();
  }

  removeSeal(id: string): void {
    const idx = this.seals.findIndex(s => s.id === id);
    if (idx >= 0) {
      this.seals.splice(idx, 1);
      this.persist();
    }
  }

  updateSeal(id: string, data: Partial<Seal>): void {
    const idx = this.seals.findIndex(s => s.id === id);
    if (idx >= 0) {
      const old = this.seals[idx];
      this.seals[idx] = new Seal({ ...old, ...data, id: old.id });
      this.persist();
    }
  }

  submitApplication(app: SealApplication): void {
    this.applications.push(app);
    this.persist();
  }

  approveApplication(appId: string, level: number, approver: string, comment: string, signature: string): void {
    const app = this.applications.find(a => a.id === appId);
    if (app) {
      app.approve(level, approver, comment, signature);
      this.persist();
    }
  }

  executeApplication(appId: string, executor: string, witness: string, photos: string[], location: { lat: number; lng: number }): void {
    const app = this.applications.find(a => a.id === appId);
    if (app) {
      app.execute(executor, witness, photos, location);
      const seal = this.seals.find(s => s.id === app.sealId);
      if (seal) {
        seal.updateStatus(SealStatus.IN_USE, executor);
      }
      this.persist();
    }
  }

  registerOut(record: SealOutRecord): void {
    this.outRecords.push(record);
    const seal = this.seals.find(s => s.id === record.sealId);
    if (seal) {
      seal.updateStatus(SealStatus.OUTSIDE, record.borrower);
    }
    this.persist();
  }

  returnSeal(recordId: string, returner: string, witness: string): void {
    const record = this.outRecords.find(r => r.id === recordId);
    if (record) {
      record.returnSeal(returner, witness);
      const seal = this.seals.find(s => s.id === record.sealId);
      if (seal) {
        seal.updateStatus(SealStatus.IN_VAULT, returner);
      }
      this.persist();
    }
  }

  private persist(): void {
    AppStorage.setOrCreate('seal_seals', JSON.stringify(this.seals));
    AppStorage.setOrCreate('seal_applications', JSON.stringify(this.applications));
    AppStorage.setOrCreate('seal_out_records', JSON.stringify(this.outRecords));
  }

  load(): void {
    const seals = AppStorage.get<string>('seal_seals');
    if (seals) {
      try {
        const parsed = JSON.parse(seals);
        this.seals = parsed.map((s: Object) => new Seal(s as Partial<Seal>));
      } catch (e) {
        console.error('加载印章数据失败', e);
      }
    }

    const apps = AppStorage.get<string>('seal_applications');
    if (apps) {
      try {
        const parsed = JSON.parse(apps);
        this.applications = parsed.map((a: Object) => new SealApplication(a as Partial<SealApplication>));
      } catch (e) {
        console.error('加载申请数据失败', e);
      }
    }

    const outs = AppStorage.get<string>('seal_out_records');
    if (outs) {
      try {
        const parsed = JSON.parse(outs);
        this.outRecords = parsed.map((o: Object) => new SealOutRecord(o as Partial<SealOutRecord>));
      } catch (e) {
        console.error('加载外带记录失败', e);
      }
    }
  }
}

// 全局状态实例
export const sealState = new SealState();
AppStorage.setOrCreate('sealState', sealState);

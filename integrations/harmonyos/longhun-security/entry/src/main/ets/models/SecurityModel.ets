// entry/src/main/ets/models/SecurityModel.ets
// 龍魂 · 安防数据模型
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

// === DNA常量 ===
const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// === 进程状态 ===
export enum ProcessStatus {
  RUNNING = 'running',
  SUSPENDED = 'suspended',
  CRASHED = 'crashed',
  RESTARTING = 'restarting',
  STOPPED = 'stopped',
  UNKNOWN = 'unknown'
}

// === 任务类型 ===
export enum TaskType {
  PERIODIC = 'periodic',
  ONE_SHOT = 'one_shot',
  EVENT_DRIVEN = 'event_driven',
  CONDITIONAL = 'conditional'
}

// === 感知类型 ===
export enum PerceptionType {
  MOTION = 'motion',
  SOUND = 'sound',
  TEMPERATURE = 'temperature',
  HUMIDITY = 'humidity',
  LIGHT = 'light',
  PRESSURE = 'pressure',
  PROXIMITY = 'proximity',
  MAGNETIC = 'magnetic',
  ACCELERATION = 'acceleration',
  GYROSCOPE = 'gyroscope',
  CAMERA = 'camera',
  LOCATION = 'location',
  NETWORK = 'network'
}

// === 威胁等级 ===
export enum ThreatLevel {
  NONE = 'none',
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

// === 进程监控数据 ===
export class ProcessMonitor {
  id: string;
  pid: number;
  name: string;
  status: ProcessStatus;
  startTime: number;
  lastHeartbeat: number;
  memoryUsage: number;
  cpuUsage: number;
  restartCount: number;
  crashLog: string;
  dnaSignature: string;

  constructor(data: Partial<ProcessMonitor> = {}) {
    this.id = data.id || `PROC-${Date.now()}`;
    this.pid = data.pid || 0;
    this.name = data.name || 'unknown';
    this.status = data.status || ProcessStatus.UNKNOWN;
    this.startTime = data.startTime || Date.now();
    this.lastHeartbeat = data.lastHeartbeat || Date.now();
    this.memoryUsage = data.memoryUsage || 0;
    this.cpuUsage = data.cpuUsage || 0;
    this.restartCount = data.restartCount || 0;
    this.crashLog = data.crashLog || '';
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const payload = `${this.id}-${this.pid}-${this.name}-${Date.now()}`;
    return `SM3-${this.hashCode(payload)}`;
  }

  private hashCode(str: string): string {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash = hash & hash;
    }
    return Math.abs(hash).toString(16).substring(0, 16);
  }

  isHealthy(): boolean {
    const now = Date.now();
    const heartbeatTimeout = 30000;
    return (now - this.lastHeartbeat) < heartbeatTimeout &&
           this.status === ProcessStatus.RUNNING &&
           this.memoryUsage < 500 &&
           this.cpuUsage < 80;
  }
}

// === 定时任务数据 ===
export class ScheduledTask {
  id: string;
  name: string;
  type: TaskType;
  cronExpression: string;
  nextTriggerTime: number;
  lastTriggerTime: number;
  executeCount: number;
  successCount: number;
  failCount: number;
  isEnabled: boolean;
  handler: string;
  retryCount: number;
  retryInterval: number;
  dnaSignature: string;

  constructor(data: Partial<ScheduledTask> = {}) {
    this.id = data.id || `TASK-${Date.now()}`;
    this.name = data.name || '未命名任务';
    this.type = data.type || TaskType.PERIODIC;
    this.cronExpression = data.cronExpression || '0 * * * *';
    this.nextTriggerTime = data.nextTriggerTime || 0;
    this.lastTriggerTime = data.lastTriggerTime || 0;
    this.executeCount = data.executeCount || 0;
    this.successCount = data.successCount || 0;
    this.failCount = data.failCount || 0;
    this.isEnabled = data.isEnabled ?? true;
    this.handler = data.handler || '';
    this.retryCount = data.retryCount || 3;
    this.retryInterval = data.retryInterval || 5000;
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const payload = `${this.id}-${this.name}-${this.cronExpression}-${Date.now()}`;
    return `SM3-${this.hashCode(payload)}`;
  }

  private hashCode(str: string): string {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash = hash & hash;
    }
    return Math.abs(hash).toString(16).substring(0, 16);
  }

  calculateNextTrigger(): number {
    const now = Date.now();
    const interval = this.parseInterval();
    return now + interval;
  }

  private parseInterval(): number {
    if (this.cronExpression === '0 * * * *') return 3600000;
    if (this.cronExpression === '*/5 * * * *') return 300000;
    if (this.cronExpression === '0 0 * * *') return 86400000;
    return 60000;
  }
}

// === 轨迹数据 ===
export class TrajectoryPoint {
  id: string;
  timestamp: number;
  x: number;
  y: number;
  z: number;
  confidence: number;
  source: string;
  dnaSignature: string;

  constructor(data: Partial<TrajectoryPoint> = {}) {
    this.id = data.id || `TRJ-${Date.now()}`;
    this.timestamp = data.timestamp || Date.now();
    this.x = data.x || 0;
    this.y = data.y || 0;
    this.z = data.z || 0;
    this.confidence = data.confidence || 1.0;
    this.source = data.source || '';
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const payload = `${this.id}-${this.timestamp}-${this.x}-${this.y}-${this.z}`;
    return `SM3-${this.hashCode(payload)}`;
  }

  private hashCode(str: string): string {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash = hash & hash;
    }
    return Math.abs(hash).toString(16).substring(0, 16);
  }
}

// === 感知数据 ===
export class PerceptionData {
  id: string;
  type: PerceptionType;
  value: number;
  unit: string;
  location: string;
  timestamp: number;
  threatLevel: ThreatLevel;
  description: string;
  dnaSignature: string;

  constructor(data: Partial<PerceptionData> = {}) {
    this.id = data.id || `PER-${Date.now()}`;
    this.type = data.type || PerceptionType.MOTION;
    this.value = data.value || 0;
    this.unit = data.unit || '';
    this.location = data.location || '';
    this.timestamp = data.timestamp || Date.now();
    this.threatLevel = data.threatLevel || ThreatLevel.NONE;
    this.description = data.description || '';
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const payload = `${this.id}-${this.type}-${this.value}-${this.timestamp}`;
    return `SM3-${this.hashCode(payload)}`;
  }

  private hashCode(str: string): string {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash = hash & hash;
    }
    return Math.abs(hash).toString(16).substring(0, 16);
  }

  getThreatColor(): string {
    switch (this.threatLevel) {
      case ThreatLevel.NONE: return '#00ff00';
      case ThreatLevel.LOW: return '#88ff00';
      case ThreatLevel.MEDIUM: return '#ffcc00';
      case ThreatLevel.HIGH: return '#ff6600';
      case ThreatLevel.CRITICAL: return '#ff0000';
      default: return '#666';
    }
  }
}

// === 安防全局状态 ===
@Observed
export class SecurityState {
  processes: ProcessMonitor[] = [];
  tasks: ScheduledTask[] = [];
  trajectories: Map<string, TrajectoryPoint[]> = new Map();
  perceptions: PerceptionData[] = [];
  alerts: AlertRecord[] = [];

  get statistics(): SecurityStats {
    return {
      totalProcesses: this.processes.length,
      healthyProcesses: this.processes.filter(p => p.isHealthy()).length,
      totalTasks: this.tasks.length,
      activeTasks: this.tasks.filter(t => t.isEnabled).length,
      totalTrajectories: this.trajectories.size,
      totalPerceptions: this.perceptions.length,
      criticalAlerts: this.alerts.filter(a => a.level === ThreatLevel.CRITICAL).length
    };
  }

  persist(): void {
    AppStorage.setOrCreate('security_processes', JSON.stringify(this.processes.slice(-50)));
    AppStorage.setOrCreate('security_tasks', JSON.stringify(this.tasks.slice(-50)));
    AppStorage.setOrCreate('security_perceptions', JSON.stringify(this.perceptions.slice(-100)));
  }
}

export interface SecurityStats {
  totalProcesses: number;
  healthyProcesses: number;
  totalTasks: number;
  activeTasks: number;
  totalTrajectories: number;
  totalPerceptions: number;
  criticalAlerts: number;
}

export interface AlertRecord {
  id: string;
  level: ThreatLevel;
  message: string;
  timestamp: number;
  source: string;
  resolved: boolean;
}

export const securityState = new SecurityState();
AppStorage.setOrCreate('securityState', securityState);

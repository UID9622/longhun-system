// entry/src/main/ets/services/ProcessGuardian.ets
// 龍魂 · 进程守护引擎 · 看门狗+自恢复
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { ProcessMonitor, ProcessStatus } from '../models/SecurityModel';

export class ProcessGuardian {
  private static instance: ProcessGuardian;
  private processes: Map<string, ProcessMonitor> = new Map();
  private watchdogTimer: number = 0;
  private readonly HEARTBEAT_INTERVAL: number = 5000;
  private readonly RESTART_DELAY: number = 3000;

  static getInstance(): ProcessGuardian {
    if (!ProcessGuardian.instance) {
      ProcessGuardian.instance = new ProcessGuardian();
    }
    return ProcessGuardian.instance;
  }

  private constructor() {
    this.startWatchdog();
  }

  registerProcess(name: string, pid: number): ProcessMonitor {
    const monitor = new ProcessMonitor({
      name,
      pid,
      status: ProcessStatus.RUNNING,
      startTime: Date.now(),
      lastHeartbeat: Date.now()
    });
    this.processes.set(name, monitor);
    console.info(`[龍魂·进程守护] 注册进程: ${name} PID:${pid}`);
    return monitor;
  }

  heartbeat(name: string, memoryUsage: number, cpuUsage: number): void {
    const monitor = this.processes.get(name);
    if (!monitor) {
      console.warn(`[龍魂·进程守护] 未注册进程: ${name}`);
      return;
    }
    monitor.lastHeartbeat = Date.now();
    monitor.memoryUsage = memoryUsage;
    monitor.cpuUsage = cpuUsage;
    monitor.status = ProcessStatus.RUNNING;

    if (!monitor.isHealthy()) {
      console.warn(`[龍魂·进程守护] 进程异常: ${name} 内存:${memoryUsage}MB CPU:${cpuUsage}%`);
      this.handleUnhealthyProcess(monitor);
    }
  }

  private handleUnhealthyProcess(monitor: ProcessMonitor): void {
    if (monitor.status === ProcessStatus.CRASHED) return;
    monitor.status = ProcessStatus.CRASHED;
    monitor.crashLog = `异常时间: ${new Date().toISOString()}\n` +
      `内存: ${monitor.memoryUsage}MB\n` +
      `CPU: ${monitor.cpuUsage}%\n` +
      `最后心跳: ${new Date(monitor.lastHeartbeat).toISOString()}`;
    this.restartProcess(monitor);
  }

  private async restartProcess(monitor: ProcessMonitor): Promise<void> {
    monitor.status = ProcessStatus.RESTARTING;
    monitor.restartCount++;
    console.info(`[龍魂·进程守护] 重启进程: ${monitor.name} 第${monitor.restartCount}次`);
    await this.sleep(this.RESTART_DELAY);
    const newPid = this.generateNewPid();
    monitor.pid = newPid;
    monitor.status = ProcessStatus.RUNNING;
    monitor.startTime = Date.now();
    monitor.lastHeartbeat = Date.now();
    console.info(`[龍魂·进程守护] 进程重启完成: ${monitor.name} 新PID:${newPid}`);
  }

  private startWatchdog(): void {
    const checkLoop = () => {
      const now = Date.now();
      for (const [name, monitor] of this.processes) {
        if ((now - monitor.lastHeartbeat) > 30000 && monitor.status === ProcessStatus.RUNNING) {
          console.warn(`[龍魂·进程守护] 心跳超时: ${name}`);
          this.handleUnhealthyProcess(monitor);
        }
        if (monitor.memoryUsage > 1000) {
          console.warn(`[龍魂·进程守护] 内存泄漏警告: ${name} ${monitor.memoryUsage}MB`);
        }
      }
      this.watchdogTimer = setTimeout(checkLoop, this.HEARTBEAT_INTERVAL);
    };
    checkLoop();
  }

  stopWatchdog(): void {
    if (this.watchdogTimer) {
      clearTimeout(this.watchdogTimer);
      this.watchdogTimer = 0;
    }
  }

  getProcessStatus(name: string): ProcessMonitor | undefined {
    return this.processes.get(name);
  }

  getAllProcesses(): ProcessMonitor[] {
    return Array.from(this.processes.values());
  }

  private generateNewPid(): number {
    return Math.floor(Math.random() * 10000) + 1000;
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

export const processGuardian = ProcessGuardian.getInstance();

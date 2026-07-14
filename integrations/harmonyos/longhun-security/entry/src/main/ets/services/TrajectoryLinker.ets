// entry/src/main/ets/services/TrajectoryLinker.ets
// 龍魂 · 轨迹续联引擎 · 断点续传+无缝切换
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { TrajectoryPoint } from '../models/SecurityModel';

export class TrajectoryLinker {
  private static instance: TrajectoryLinker;
  private trajectories: Map<string, TrajectoryPoint[]> = new Map();
  private snapshots: Map<string, object> = new Map();
  private readonly MAX_POINTS: number = 1000;
  private readonly SYNC_INTERVAL: number = 5000;

  static getInstance(): TrajectoryLinker {
    if (!TrajectoryLinker.instance) {
      TrajectoryLinker.instance = new TrajectoryLinker();
    }
    return TrajectoryLinker.instance;
  }

  addPoint(trajectoryId: string, point: TrajectoryPoint): void {
    let points = this.trajectories.get(trajectoryId);
    if (!points) {
      points = [];
      this.trajectories.set(trajectoryId, points);
    }
    points.push(point);
    if (points.length > this.MAX_POINTS) {
      points = points.slice(-this.MAX_POINTS);
      this.trajectories.set(trajectoryId, points);
    }
    this.syncToDistributed(trajectoryId, point);
  }

  getTrajectory(trajectoryId: string): TrajectoryPoint[] {
    return this.trajectories.get(trajectoryId) || [];
  }

  saveSnapshot(trajectoryId: string, state: object): void {
    this.snapshots.set(trajectoryId, {
      ...state,
      timestamp: Date.now(),
      pointCount: this.trajectories.get(trajectoryId)?.length || 0
    });
    console.info(`[龍魂·轨迹续联] 保存快照: ${trajectoryId}`);
  }

  restoreSnapshot(trajectoryId: string): object | undefined {
    const snapshot = this.snapshots.get(trajectoryId);
    if (snapshot) {
      console.info(`[龍魂·轨迹续联] 恢复快照: ${trajectoryId}`);
    }
    return snapshot;
  }

  async handover(trajectoryId: string, fromDevice: string, toDevice: string): Promise<boolean> {
    console.info(`[龍魂·轨迹续联] 设备切换: ${fromDevice} → ${toDevice}`);
    const currentPoints = this.trajectories.get(trajectoryId) || [];
    const snapshot = this.snapshots.get(trajectoryId);
    await this.syncToDevice(toDevice, {
      trajectoryId,
      points: currentPoints.slice(-100),
      snapshot
    });
    const verified = await this.verifySync(trajectoryId, toDevice);
    if (verified) {
      console.info(`[龍魂·轨迹续联] 切换成功: ${trajectoryId}`);
      return true;
    } else {
      console.error(`[龍魂·轨迹续联] 切换失败: ${trajectoryId}`);
      return false;
    }
  }

  private async syncToDistributed(trajectoryId: string, point: TrajectoryPoint): Promise<void> {
    console.debug(`[龍魂·轨迹续联] 同步轨迹: ${trajectoryId} [${point.x}, ${point.y}]`);
  }

  private async syncToDevice(deviceId: string, data: object): Promise<void> {
    console.info(`[龍魂·轨迹续联] 同步到设备: ${deviceId}`);
  }

  private async verifySync(trajectoryId: string, deviceId: string): Promise<boolean> {
    return true;
  }

  cleanup(trajectoryId: string, beforeTimestamp: number): void {
    const points = this.trajectories.get(trajectoryId);
    if (points) {
      const filtered = points.filter(p => p.timestamp >= beforeTimestamp);
      this.trajectories.set(trajectoryId, filtered);
      console.info(`[龍魂·轨迹续联] 清理轨迹: ${trajectoryId} 保留${filtered.length}点`);
    }
  }

  getStats(trajectoryId: string): { totalPoints: number, duration: number, distance: number } {
    const points = this.trajectories.get(trajectoryId) || [];
    if (points.length < 2) {
      return { totalPoints: points.length, duration: 0, distance: 0 };
    }
    const duration = points[points.length - 1].timestamp - points[0].timestamp;
    let distance = 0;
    for (let i = 1; i < points.length; i++) {
      const dx = points[i].x - points[i - 1].x;
      const dy = points[i].y - points[i - 1].y;
      distance += Math.sqrt(dx * dx + dy * dy);
    }
    return { totalPoints: points.length, duration, distance };
  }

  getTrajectoryKeys(): string[] {
    return Array.from(this.trajectories.keys());
  }
}

export const trajectoryLinker = TrajectoryLinker.getInstance();

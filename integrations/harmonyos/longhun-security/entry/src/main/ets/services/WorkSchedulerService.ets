// entry/src/main/ets/services/WorkSchedulerService.ets
// 龍魂 · 鸿蒙WorkScheduler对接 · 后台保活
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import workScheduler from '@ohos.workScheduler';

export class WorkSchedulerService {
  private static instance: WorkSchedulerService;
  private workId: number = 0;

  static getInstance(): WorkSchedulerService {
    if (!WorkSchedulerService.instance) {
      WorkSchedulerService.instance = new WorkSchedulerService();
    }
    return WorkSchedulerService.instance;
  }

  registerBackgroundWork(): void {
    const workInfo: workScheduler.WorkInfo = {
      workId: this.workId++,
      bundleName: 'com.longhun.security',
      abilityName: 'SecurityAbility',
      networkType: workScheduler.NetworkType.NETWORK_TYPE_ANY,
      isDeepIdle: true,
      idleWaitTime: 5000,
      isRepeat: true,
      repeatCycleTime: 600000,
      repeatCount: workScheduler.REPEAT_INFINITE
    };

    try {
      workScheduler.startWork(workInfo);
      console.info('[龍魂·WorkScheduler] 后台任务注册成功');
    } catch (error) {
      console.error(`[龍魂·WorkScheduler] 注册失败: ${error}`);
    }
  }

  stopBackgroundWork(workId: number): void {
    try {
      workScheduler.stopWork(workId, false);
      console.info('[龍魂·WorkScheduler] 后台任务停止');
    } catch (error) {
      console.error(`[龍魂·WorkScheduler] 停止失败: ${error}`);
    }
  }

  getAllWorks(): workScheduler.WorkInfo[] {
    try {
      return workScheduler.getAllWorks();
    } catch (error) {
      console.error(`[龍魂·WorkScheduler] 获取失败: ${error}`);
      return [];
    }
  }
}

export const workSchedulerService = WorkSchedulerService.getInstance();

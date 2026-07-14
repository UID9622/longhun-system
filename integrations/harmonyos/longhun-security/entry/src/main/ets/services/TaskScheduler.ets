// entry/src/main/ets/services/TaskScheduler.ets
// 龍魂 · 定时任务引擎 · 精确触发+任务链
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { ScheduledTask, TaskType } from '../models/SecurityModel';

export class TaskScheduler {
  private static instance: TaskScheduler;
  private tasks: Map<string, ScheduledTask> = new Map();
  private timers: Map<string, number> = new Map();
  private handlers: Map<string, Function> = new Map();

  static getInstance(): TaskScheduler {
    if (!TaskScheduler.instance) {
      TaskScheduler.instance = new TaskScheduler();
    }
    return TaskScheduler.instance;
  }

  registerHandler(name: string, handler: Function): void {
    this.handlers.set(name, handler);
  }

  addTask(task: ScheduledTask): void {
    this.tasks.set(task.id, task);
    this.scheduleTask(task);
    console.info(`[龍魂·任务调度] 添加任务: ${task.name} [${task.cronExpression}]`);
  }

  private scheduleTask(task: ScheduledTask): void {
    if (!task.isEnabled) return;

    const execute = async () => {
      if (!task.isEnabled) return;

      const handler = this.handlers.get(task.handler);
      if (!handler) {
        console.error(`[龍魂·任务调度] 未找到处理器: ${task.handler}`);
        task.failCount++;
        return;
      }

      task.lastTriggerTime = Date.now();
      task.executeCount++;

      try {
        await handler(task);
        task.successCount++;
        console.info(`[龍魂·任务调度] 任务执行成功: ${task.name}`);
      } catch (error) {
        task.failCount++;
        console.error(`[龍魂·任务调度] 任务执行失败: ${task.name} - ${error}`);
        if (task.failCount < task.retryCount) {
          console.info(`[龍魂·任务调度] 重试任务: ${task.name} 第${task.failCount + 1}次`);
          setTimeout(() => execute(), task.retryInterval);
          return;
        }
      }

      task.nextTriggerTime = task.calculateNextTrigger();

      if (task.type === TaskType.PERIODIC) {
        const delay = task.nextTriggerTime - Date.now();
        const timer = setTimeout(() => execute(), Math.max(delay, 1000));
        this.timers.set(task.id, timer);
      }
    };

    const delay = task.nextTriggerTime - Date.now();
    if (delay <= 0) {
      execute();
    } else {
      const timer = setTimeout(() => execute(), delay);
      this.timers.set(task.id, timer);
    }
  }

  toggleTask(id: string, enabled: boolean): void {
    const task = this.tasks.get(id);
    if (!task) return;
    task.isEnabled = enabled;
    if (enabled) {
      this.scheduleTask(task);
    } else {
      const timer = this.timers.get(id);
      if (timer) {
        clearTimeout(timer);
        this.timers.delete(id);
      }
    }
  }

  removeTask(id: string): void {
    const timer = this.timers.get(id);
    if (timer) {
      clearTimeout(timer);
      this.timers.delete(id);
    }
    this.tasks.delete(id);
  }

  getAllTasks(): ScheduledTask[] {
    return Array.from(this.tasks.values());
  }

  executeNow(id: string): void {
    const task = this.tasks.get(id);
    if (task) {
      const handler = this.handlers.get(task.handler);
      if (handler) {
        handler(task);
      }
    }
  }
}

export const taskScheduler = TaskScheduler.getInstance();

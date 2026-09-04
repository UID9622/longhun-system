// DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-HARMONYOS-WORKER-v1.0-UID9622
// CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 创建者: 诸葛鑫（UID9622）
//
// 龍魂·鸿蒙 Worker 线程
// 在独立线程中加载 Rust .so 库 · 执行计算密集型操作 · 不阻塞 UI

import { worker } from '@kit.ArkTS';
import { logger } from '../utils/Logger';

const TAG = 'LonghunWorker';

/**
 * Worker 消息类型
 */
interface WorkerMessage {
  type: 'supervision' | 'memory' | 'health';
  payload: string; // JSON 格式参数
}

/**
 * Worker 响应类型
 */
interface WorkerResponse {
  id: string;
  success: boolean;
  data: string; // JSON 格式结果
  error?: string;
  elapsed: number; // 执行耗时 ms
}

/**
 * 记忆 Worker 管理器
 * 封装 Worker 线程通信，对外提供 Promise API
 */
export class MemoryWorkerManager {
  private workerInstance: worker.ThreadWorker | null = null;
  private pendingRequests: Map<string, (value: WorkerResponse) => void> = new Map();
  private initialized: boolean = false;

  /**
   * 初始化 Worker 线程
   */
  async initialize(workerScript: string): Promise<void> {
    if (this.initialized) {
      return;
    }

    try {
      this.workerInstance = new worker.ThreadWorker(workerScript);
      this.workerInstance.onmessage = (event: object) => {
        const response = event as WorkerResponse;
        const resolver = this.pendingRequests.get(response.id);
        if (resolver) {
          this.pendingRequests.delete(response.id);
          resolver(response);
        }
      };
      this.workerInstance.onerror = (err: Error) => {
        logger.error(TAG, `Worker 错误: ${err.message}`);
      };
      this.initialized = true;
      logger.info(TAG, 'Worker 线程初始化成功');
    } catch (err) {
      logger.error(TAG, `Worker 初始化失败: ${JSON.stringify(err)}`);
      throw err;
    }
  }

  /**
   * 发送任务到 Worker 线程
   */
  sendTask(msg: WorkerMessage, timeoutMs: number = 30000): Promise<WorkerResponse> {
    return new Promise((resolve, reject) => {
      if (!this.workerInstance || !this.initialized) {
        reject(new Error('Worker 未初始化'));
        return;
      }

      const id = this.generateId();
      this.pendingRequests.set(id, resolve);

      // 超时处理
      const timer = setTimeout(() => {
        this.pendingRequests.delete(id);
        reject(new Error(`Worker 任务超时 (${timeoutMs}ms)`));
      }, timeoutMs);

      try {
        const extendedMsg: object = { ...msg, id, timeout: timeoutMs };
        this.workerInstance.postMessage(extendedMsg);

        // 成功后清除超时
        const originalResolve = resolve;
        this.pendingRequests.set(id, (resp: WorkerResponse) => {
          clearTimeout(timer);
          originalResolve(resp);
        });
      } catch (err) {
        clearTimeout(timer);
        this.pendingRequests.delete(id);
        reject(err);
      }
    });
  }

  /**
   * 释放 Worker 资源
   */
  dispose(): void {
    if (this.workerInstance) {
      this.workerInstance.terminate();
      this.workerInstance = null;
    }
    this.pendingRequests.clear();
    this.initialized = false;
    logger.info(TAG, 'Worker 已释放');
  }

  private generateId(): string {
    return `lh-${Date.now()}-${Math.random().toString(36).substring(2, 8)}`;
  }
}

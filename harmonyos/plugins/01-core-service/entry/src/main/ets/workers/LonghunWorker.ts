/**
 * 🐉 龍魂·Worker 线程入口
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-WORKER-UID9622
 *
 * 进化引擎 Worker 线程
 * 独立线程执行耗时的进化计算，不阻塞主线程
 */

import { worker, MessageEvents } from '@kit.ArkTS';
import { EvolutionMetrics } from '../model/SupervisionTypes';

// Worker 父线程端口
const workerPort = worker.workerPort;

/**
 * 监听主线程消息
 */
workerPort.onmessage = (e: MessageEvents) => {
  const msg = e.data as Record<string, Object>;

  switch (msg['type'] as string) {
    case 'init':
      handleInit(msg['config'] as Record<string, Object>);
      break;
    case 'evolve':
      handleEvolve();
      break;
    case 'metrics':
      handleMetrics();
      break;
    default:
      workerPort.postMessage({ type: 'error', message: 'Unknown command' });
  }
};

/**
 * Worker 错误处理
 */
workerPort.onerror = (e: ErrorEvent) => {
  console.error(`[龍魂·Worker] Error: ${e.message}`);
};

/**
 * 初始化进化引擎
 */
function handleInit(config: Record<string, Object>): void {
  console.info('[龍魂·Worker] 初始化进化引擎');

  const intervalHours = (config?.['check_interval_hours'] as number) ?? 24;

  workerPort.postMessage({
    type: 'init_ok',
    config: { check_interval_hours: intervalHours },
    timestamp: new Date().toISOString()
  });

  // 设置定时进化检查
  setInterval(() => {
    runEvolutionCycle();
  }, intervalHours * 60 * 60 * 1000);

  console.info(`[龍魂·Worker] 🟢 就绪·${intervalHours}h进化周期`);
}

/**
 * 手动触发进化
 */
function handleEvolve(): void {
  console.info('[龍魂·Worker] 手动触发进化');
  runEvolutionCycle();
}

/**
 * 返回当前指标
 */
function handleMetrics(): void {
  const metrics: EvolutionMetrics = {
    intercept_rate: 0.95 + Math.random() * 0.05,
    red_team_success: 0.88 + Math.random() * 0.05,
    entropy: Math.random() * 0.3,
    cycle: 0,
    timestamp: new Date().toISOString()
  };

  workerPort.postMessage({
    type: 'metrics',
    data: metrics
  });
}

/**
 * 执行进化周期
 */
function runEvolutionCycle(): void {
  console.info('[龍魂·Worker] 进化周期开始');

  // 模拟进化计算（实际：分析历史监督数据 → 生成升级提案）
  const results = {
    type: 'evolution_result',
    metrics: {
      intercept_rate: 0.95 + Math.random() * 0.04,
      red_team_success: 0.88 + Math.random() * 0.05,
      entropy: 0.1 + Math.random() * 0.2
    },
    upgrade_recommended: Math.random() > 0.85,
    timestamp: new Date().toISOString(),
    dna: `#龍芯⚡️${new Date().toISOString().split('T')[0]}-WORKER-EVOLVE-UID9622`
  };

  workerPort.postMessage(results);
  console.info('[龍魂·Worker] 进化周期完成');
}

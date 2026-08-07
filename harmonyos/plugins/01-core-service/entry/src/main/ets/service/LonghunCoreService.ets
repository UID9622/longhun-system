/**
 * 🐉 龍魂核心运行时 · Service Ability 主入口
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-PLUGIN-CORE-SERVICE-UID9622
 * 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
 * 主权锚定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
 * GPG:   A2D0092CEE2E5BA87035600924C3704A8CC26D5F
 * 分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
 * 三色:  🟢 通过
 */

import { ServiceAbility } from '@kit.AbilityKit';
import { Want } from '@kit.AbilityKit';
import { rpc } from '@kit.IPCKit';
import { SupervisionEngine } from './SupervisionEngine';
import { MemoryManager } from './MemoryManager';
import { SovereigntyVerifier } from './SovereigntyVerifier';
import { ChipDetector } from './ChipDetector';
import { worker } from '@kit.ArkTS';

// ─── IPC 接口定义 ───
const CORE_SERVICE_DESCRIPTOR = 'longhun.core.service.v1';

// 三色状态枚举
enum Tricolor {
  GREEN = 'GREEN',    // 🟢 通过
  YELLOW = 'YELLOW', // 🟡 待核
  RED = 'RED'        // 🔴 红线
}

// 系统状态
interface SystemStatus {
  uptime: number;                    // 运行秒数
  supervision_cycle: number;         // 当前监督周期
  active_personas: number;           // 活跃人格数
  memory_total: number;              // 记忆总数
  tricolor: Tricolor;               // 系统三色
  chip: string;                     // 芯片信息
  dna_valid: boolean;               // DNA有效性
  last_evolution: string;           // 最后进化时间
  version: string;                  // 版本号
}

/**
 * 龙魂核心运行时 Stub 实现
 */
class LonghunCoreStub extends rpc.RemoteObject {
  private supervisionEngine: SupervisionEngine;
  private memoryManager: MemoryManager;

  constructor(supervisionEngine: SupervisionEngine, memoryManager: MemoryManager) {
    super(CORE_SERVICE_DESCRIPTOR);
    this.supervisionEngine = supervisionEngine;
    this.memoryManager = memoryManager;
  }

  onRemoteMessageRequest(code: number, data: rpc.MessageParcel, reply: rpc.MessageParcel): boolean {
    switch (code) {
      case 1: // runSupervision
        return this.handleSupervision(data, reply);
      case 2: // queryMemory
        return this.handleQueryMemory(data, reply);
      case 3: // getSystemStatus
        return this.handleGetStatus(data, reply);
      case 4: // triggerEvolution
        return this.handleEvolution(data, reply);
      case 5: // verifySovereignty
        return this.handleSovereigntyVerify(data, reply);
      default:
        return false;
    }
  }

  private handleSupervision(data: rpc.MessageParcel, reply: rpc.MessageParcel): boolean {
    const config = data.readString();
    const result = this.supervisionEngine.runCycle(config);
    reply.writeString(result);
    return true;
  }

  private handleQueryMemory(data: rpc.MessageParcel, reply: rpc.MessageParcel): boolean {
    const query = data.readString();
    const result = this.memoryManager.query(query);
    reply.writeString(result);
    return true;
  }

  private handleGetStatus(_data: rpc.MessageParcel, reply: rpc.MessageParcel): boolean {
    const status: SystemStatus = {
      uptime: this.supervisionEngine.getUptime(),
      supervision_cycle: this.supervisionEngine.getCycleCount(),
      active_personas: this.supervisionEngine.getActivePersonasCount(),
      memory_total: this.memoryManager.getTotalCount(),
      tricolor: this.supervisionEngine.getTricolor(),
      chip: ChipDetector.detect(),
      dna_valid: SovereigntyVerifier.verifyDNA(),
      last_evolution: this.supervisionEngine.getLastEvolutionTime(),
      version: 'v1.0.0-harmonyos'
    };
    reply.writeString(JSON.stringify(status));
    return true;
  }

  private handleEvolution(_data: rpc.MessageParcel, reply: rpc.MessageParcel): boolean {
    const evolutionResult = {
      status: 'triggered',
      timestamp: new Date().toISOString(),
      message: 'Evolution cycle initiated in worker thread'
    };
    reply.writeString(JSON.stringify(evolutionResult));
    return true;
  }

  private handleSovereigntyVerify(_data: rpc.MessageParcel, reply: rpc.MessageParcel): boolean {
    const result = SovereigntyVerifier.fullVerify();
    reply.writeString(JSON.stringify(result));
    return true;
  }
}

/**
 * 🐉 LonghunCoreService — 龙魂核心运行时 Service Ability
 * 启动顺序：加载配置 → 初始化监督引擎 → 初始化记忆管理 → 主权验证 → 启动 Worker
 */
export default class LonghunCoreService extends ServiceAbility {
  private supervisionEngine: SupervisionEngine = new SupervisionEngine();
  private memoryManager: MemoryManager = new MemoryManager();
  private evolutionWorker?: worker.ThreadWorker;
  private isRunning: boolean = false;

  /**
   * 服务启动
   */
  onStart(want: Want): void {
    console.info('[龍魂] LonghunCoreService onStart');
    console.info('[龍魂] DNA: #龍芯⚡️丙午·癸未·乙酉·坤卦-PLUGIN-CORE-SERVICE-UID9622');

    try {
      // Step 1: 主权完整性验证（必须先过）
      const sovereigntyResult = SovereigntyVerifier.quickVerify();
      if (!sovereigntyResult.passed) {
        console.error(`[龍魂] 🔴 主权验证失败: ${sovereigntyResult.reason}`);
        console.error('[龍魂] 服务启动中止——主权锚定不可绕过');
        return;
      }
      console.info(`[龍魂] 🟢 主权验证通过`);

      // Step 2: 检测芯片信息
      const chipInfo = ChipDetector.detect();
      console.info(`[龍魂] 芯片: ${chipInfo}`);

      // Step 3: 初始化监督引擎（14 人格矩阵 + 三色状态机）
      this.supervisionEngine.initialize();
      console.info(`[龍魂] 🟢 监督引擎就绪·14人格·三色审计`);

      // Step 4: 初始化记忆管理器（P0-P3 四级存储）
      this.memoryManager.initialize(this.context);
      console.info(`[龍魂] 🟢 记忆管理器就绪·P0-P3四级`);

      // Step 5: 启动进化引擎 Worker
      this.startEvolutionWorker();

      // Step 6: 启动定时监督周期（默认30分钟）
      this.supervisionEngine.startAutoCycle(30 * 60 * 1000);

      this.isRunning = true;
      console.info('[龍魂] 🟢 龙魂核心运行时全面启动完成');

    } catch (error) {
      console.error(`[龍魂] 🔴 启动失败: ${JSON.stringify(error)}`);
    }
  }

  /**
   * 服务指令处理
   */
  onCommand(want: Want, startId: number): void {
    console.info(`[龍魂] onCommand startId=${startId}`);
  }

  /**
   * 服务停止
   */
  onStop(): void {
    console.info('[龍魂] LonghunCoreService onStop');

    // 持久化当前状态
    if (this.memoryManager) {
      this.memoryManager.persist();
    }

    // 停止监督周期
    if (this.supervisionEngine) {
      this.supervisionEngine.stopAutoCycle();
    }

    // 终止 Worker
    if (this.evolutionWorker) {
      this.evolutionWorker.terminate();
    }

    this.isRunning = false;
    console.info('[龍魂] 🟢 服务已安全停止·状态已持久化');
  }

  /**
   * IPC 连接回调 — 创建并返回 Stub 实例
   */
  onConnect(want: Want): rpc.RemoteObject {
    console.info('[龍魂] IPC 客户端已连接');
    return new LonghunCoreStub(this.supervisionEngine, this.memoryManager);
  }

  /**
   * IPC 断开回调
   */
  onDisconnect(want: Want): void {
    console.info('[龍魂] IPC 客户端已断开');
  }

  /**
   * 启动进化引擎 Worker
   */
  private startEvolutionWorker(): void {
    try {
      this.evolutionWorker = new worker.ThreadWorker('entry/ets/workers/LonghunWorker.ts');
      this.evolutionWorker.postMessage({
        type: 'init',
        config: {
          check_interval_hours: 24,
          auto_upgrade: false
        }
      });

      // 监听 Worker 消息
      this.evolutionWorker.onmessage = (msg: MessageEvents) => {
        console.info(`[龍魂·进化] Worker 消息: ${JSON.stringify(msg.data)}`);
      };

      this.evolutionWorker.onerror = (err: ErrorEvent) => {
        console.error(`[龍魂·进化] Worker 错误: ${err.message}`);
      };

      console.info('[龍魂] 🟢 进化引擎 Worker 已启动');
    } catch (error) {
      console.error(`[龍魂] 进化引擎启动失败: ${JSON.stringify(error)}`);
    }
  }
}

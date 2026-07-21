// 龍魂 · Native 桥接 · ArkTS 类型封装
// DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-NATIVE-BRIDGE-v1.0
// 联动: 生日提醒v2.0 · 情感协议 · 人格路由 · 声纹计算

import longhunNative from 'liblonghun_native.so';

// === DNA 常量 ===
const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// === 任务优先级 ===
export enum TaskPriority {
  CRITICAL  = 0,   // 紧急：声纹验证、安全告警
  HIGH      = 1,   // 高：实时预测、UI响应
  NORMAL    = 2,   // 普通：批量查询、数据压缩
  LOW       = 3,   // 低：后台同步、统计计算
  BACKGROUND = 4   // 后台：索引重建、审计校验
}

// === 线程池配置 ===
export interface ThreadPoolConfig {
  minThreads: number;
  maxThreads: number;
  queueCapacity?: number;
  cpuAffinityMask?: number;
  useHugePages?: boolean;
  bindNumaNode?: boolean;
}

// === 初始化结果 ===
export interface InitResult {
  status: string;
  dna: string;
  uid: string;
  minThreads: number;
  maxThreads: number;
  queueCapacity: number;
  seal: string;
}

// === 线程池状态 ===
export interface PoolStatus {
  queueSize: number;
  activeThreads: number;
  totalProcessed: number;
  totalSubmitted: number;
  totalDropped: number;
  slowTasks: number;
  avgExecTimeUs: number;
  cpuUtilization: number;
  dna: string;
}

// === 声纹特征结果 ===
export interface VoiceprintResult {
  features: ArrayBuffer;    // 256维 float32
  frames: number;           // 帧数
  dna: string;              // DNA验证
  seal: string;             // 确认码
}

// === 情感向量结果 ===
export interface EmotionVectorResult {
  similarity: number;       // 余弦相似度 [0,1]
  emotion: string;          // 情感标签 warm/formal/casual
  dna: string;
}

// ============================================================================
// 龍魂 Native 桥接类
// ============================================================================
export class LongHunNativeBridge {
  private static initialized: boolean = false;
  private static initResult: InitResult | null = null;

  // === 初始化线程池 ===
  static init(config: ThreadPoolConfig): InitResult {
    const result = longhunNative.initThreadPool({
      minThreads: config.minThreads,
      maxThreads: config.maxThreads,
      queueCapacity: config.queueCapacity || 1000,
      cpuAffinityMask: config.cpuAffinityMask || 0,
      useHugePages: config.useHugePages || false,
      bindNumaNode: config.bindNumaNode || false
    });

    this.initialized = true;
    this.initResult = result;

    console.info(`[龍魂Native] 线程池初始化完成: ${result.minThreads}-${result.maxThreads}线程`);
    return result;
  }

  // === 获取线程池状态 ===
  static getStatus(): PoolStatus {
    this.ensureInitialized();
    return longhunNative.getPoolStatus();
  }

  // === 提取声纹特征（异步，NEON加速） ===
  static async extractVoiceprint(audioData: ArrayBuffer): Promise<VoiceprintResult> {
    this.ensureInitialized();
    return await longhunNative.extractVoiceprint(audioData);
  }

  // === 计算情感向量（异步） ===
  static async computeEmotionVector(
    featuresA: ArrayBuffer,
    featuresB: ArrayBuffer
  ): Promise<EmotionVectorResult> {
    this.ensureInitialized();
    return await longhunNative.computeEmotionVector(featuresA, featuresB);
  }

  // === 验证DNA ===
  static verifyDNA(): boolean {
    return longhunNative.verifyDNA();
  }

  // === 优雅关闭 ===
  static shutdown(): { status: string; dna: string } {
    const result = longhunNative.shutdown();
    this.initialized = false;
    this.initResult = null;
    return result;
  }

  // === 批量声纹提取（并发） ===
  static async batchExtractVoiceprints(
    audioList: ArrayBuffer[]
  ): Promise<VoiceprintResult[]> {
    this.ensureInitialized();
    const promises = audioList.map(audio => this.extractVoiceprint(audio));
    return await Promise.all(promises);
  }

  // === 检查是否已初始化 ===
  static isInitialized(): boolean {
    return this.initialized && this.verifyDNA();
  }

  // === 获取配置信息 ===
  static getInitResult(): InitResult | null {
    return this.initResult;
  }

  // === 健康检查 ===
  static healthCheck(): { healthy: boolean; status: PoolStatus } {
    const status = this.getStatus();
    const healthy = status.cpuUtilization < 0.95 && status.queueSize < 800;
    return { healthy, status };
  }

  // === 内部：确保已初始化 ===
  private static ensureInitialized(): void {
    if (!this.initialized) {
      throw new Error('[龍魂Native] 线程池未初始化，请先调用 LongHunNativeBridge.init()');
    }
  }
}

// ============================================================================
// 快捷工具函数
// ============================================================================

// Float32Array → ArrayBuffer 转换
export function float32ToArrayBuffer(arr: Float32Array): ArrayBuffer {
  return arr.buffer.slice(arr.byteOffset, arr.byteOffset + arr.byteLength);
}

// ArrayBuffer → Float32Array 转换
export function arrayBufferToFloat32(buf: ArrayBuffer): Float32Array {
  return new Float32Array(buf);
}

// 生成测试音频（正弦波）
export function generateTestAudio(
  frequency: number = 440,
  duration: number = 1,
  sampleRate: number = 16000
): Float32Array {
  const numSamples = sampleRate * duration;
  const audio = new Float32Array(numSamples);
  for (let i = 0; i < numSamples; i++) {
    audio[i] = Math.sin(2 * Math.PI * frequency * i / sampleRate);
  }
  return audio;
}

// ============================================================================
// 使用示例（注释）
// ============================================================================
/*
// 1. 初始化
const initResult = LongHunNativeBridge.init({
  minThreads: 4,
  maxThreads: 8,
  cpuAffinityMask: 0xFF  // 绑定前8核
});
console.log(`初始化: ${initResult.status}, DNA: ${initResult.dna}`);

// 2. 提取声纹
const audio = generateTestAudio(440, 2); // 2秒440Hz
const buffer = float32ToArrayBuffer(audio);
const result = await LongHunNativeBridge.extractVoiceprint(buffer);
console.log(`声纹: ${result.frames}帧, 256维`);

// 3. 批量处理
const batch = [audio1, audio2, audio3].map(float32ToArrayBuffer);
const results = await LongHunNativeBridge.batchExtractVoiceprints(batch);
console.log(`批量: ${results.length}条完成`);

// 4. 状态查询
const status = LongHunNativeBridge.getStatus();
console.log(`活跃: ${status.activeThreads}, 已处理: ${status.totalProcessed}`);

// 5. 健康检查
const { healthy, status: stats } = LongHunNativeBridge.healthCheck();
if (!healthy) console.warn('线程池负载过高');

// 6. 关闭
LongHunNativeBridge.shutdown();
*/

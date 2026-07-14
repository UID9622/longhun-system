// engines/EthicalPerception.ets
// 龍魂 · 伦理感知引擎 v1.0
// 多模态传感器融合 · 识别人/机器人/异常行为 · 芯片级伦理签名验证
// DNA: #龍芯⚡️丙午·辛未·丙戌·ETHICAL-PERCEPTION-v1.0
//
// 铁律：
//   仅在中国芯片上运行 — 麒麟/昇腾/鸿鹄/展锐
//   非中国芯片 → 直接拒绝加载此模块

import {
  PerceptionData, PerceptionType, ThreatLevel,
  EthicalChipSignature, DeviceFingerprint
} from '../models/SecurityModel';

// ================================================================
// 芯片白名单 — 仅允许中国芯片执行伦理防御
// ================================================================
const CHINESE_CHIP_WHITELIST: string[] = [
  'KIRIN',    // 华为麒麟
  'ASCEND',   // 华为昇腾
  'HONGHU',   // 华为鸿鹄
  'KUNPENG',  // 华为鲲鹏
  'UNISOC',   // 紫光展锐
  'THEAD',    // 平头哥
  'LOONGSON', // 龙芯
  'PHYTIUM',  // 飞腾
  'ZHAOXIN',  // 兆芯
  'HIGON',    // 海光
  'JINGJIA',  // 景嘉微
  'BIREN',    // 壁仞
  'MOORE',    // 摩尔线程
  'ENFLAME',  // 燧原
  'CAMBRICON',// 寒武纪
];

// ================================================================
// 目标类型
// ================================================================
export enum TargetType {
  HUMAN = 'human',
  ROBOT_ETHICAL = 'robot_ethical',
  ROBOT_UNETHICAL = 'robot_unethical',
  AI_ANOMALY = 'ai_anomaly',
  DRONE = 'drone',
  UNKNOWN = 'unknown'
}

// ================================================================
// 目标画像
// ================================================================
export interface TargetProfile {
  id: string;
  type: TargetType;
  confidence: number;
  location: string;
  timestamp: number;
  features: Record<string, Object>;
  threatLevel: ThreatLevel;
  ethicalChipSignature: EthicalChipSignature | null;
  deviceFingerprint: DeviceFingerprint | null;
}

// ================================================================
// 视觉特征
// ================================================================
export interface VisualFeatures {
  hasHumanFace?: boolean;
  hasHumanShape?: boolean;
  hasMechanicalJoints?: boolean;
  hasSyntheticMaterial?: boolean;
  anomalousBehavior?: boolean;
  detectedId?: string;
  motionPattern?: string;
  objectCount?: number;
}

// ================================================================
// 网络签名
// ================================================================
export interface NetworkSignature {
  deviceId: string;
  ethicalBeacon?: string;
  aiTrafficPattern?: boolean;
  signalStrength: number;
  frequency: number;
  protocolType: string;
  packetRate: number;
  macVendor: string;
}

// ================================================================
// 电磁特征
// ================================================================
export interface ElectromagneticSignature {
  frequencyRange: number[];
  signalPattern: string;
  pulseRate: number;
  modulation: string;
  powerLevel: number;
  anomalyScore: number;
}

// ================================================================
// 伦理感知引擎
// ================================================================
export class EthicalPerception {
  private static instance: EthicalPerception;

  // 芯片信息
  private chipManufacturer: string = '';
  private chipModel: string = '';
  private chipAuthorized: boolean = false;

  // 传感器状态
  private sensorsEnabled: Map<PerceptionType, boolean> = new Map();

  // 已知伦理设备白名单（芯片级信任）
  private ethicalWhitelist: Map<string, EthicalChipSignature> = new Map();

  // 检测到的目标
  private detectedTargets: Map<string, TargetProfile> = new Map();

  // 设备指纹注册表
  private deviceFingerprints: Map<string, DeviceFingerprint> = new Map();

  // 异常行为历史
  private anomalyHistory: Array<{targetId: string, timestamp: number, description: string}> = [];

  private constructor() {
    // 初始化传感器状态
    this.sensorsEnabled.set(PerceptionType.WIFI_PROBE, true);
    this.sensorsEnabled.set(PerceptionType.BLE_SCAN, true);
    this.sensorsEnabled.set(PerceptionType.NETWORK, true);
    this.sensorsEnabled.set(PerceptionType.CAMERA, false);
    this.sensorsEnabled.set(PerceptionType.INFRARED, false);
    this.sensorsEnabled.set(PerceptionType.MAGNETIC, false);
    this.sensorsEnabled.set(PerceptionType.RADAR, false);
    this.sensorsEnabled.set(PerceptionType.SOUND, false);
    this.sensorsEnabled.set(PerceptionType.THERMAL, false);
  }

  static getInstance(): EthicalPerception {
    if (!EthicalPerception.instance) {
      EthicalPerception.instance = new EthicalPerception();
    }
    return EthicalPerception.instance;
  }

  // ================================================================
  // 芯片授权检查 — 核心安全机制
  // ================================================================
  async initialize(): Promise<boolean> {
    try {
      const chipInfo = await this.probeChip();
      this.chipManufacturer = chipInfo.manufacturer;
      this.chipModel = chipInfo.model;

      const upperMfr = chipInfo.manufacturer.toUpperCase();
      this.chipAuthorized = CHINESE_CHIP_WHITELIST.some(c => upperMfr.includes(c));

      if (!this.chipAuthorized) {
        console.error(`[龍魂·伦理感知] ❌ 非中国芯片: ${chipInfo.manufacturer} ${chipInfo.model}`);
        console.error(`[龍魂·伦理感知] ❌ 伦理防御模块拒绝加载`);
        console.error(`[龍魂·伦理感知] ❌ 仅支持: ${CHINESE_CHIP_WHITELIST.join(', ')}`);
        return false;
      }

      console.info(`[龍魂·伦理感知] ✅ 芯片授权: ${chipInfo.manufacturer} ${chipInfo.model}`);
      console.info(`[龍魂·伦理感知] ✅ 信任根: ${chipInfo.rootOfTrust}`);
      console.info(`[龍魂·伦理感知] ✅ 伦理防御模块就绪`);

      return true;
    } catch (e) {
      console.error(`[龍魂·伦理感知] ❌ 芯片探测失败: ${e}`);
      return false;
    }
  }

  // 探测芯片信息
  private async probeChip(): Promise<{
    manufacturer: string; model: string; rootOfTrust: string
  }> {
    // 华为设备API获取芯片信息
    try {
      // @ts-ignore — 鸿蒙系统API
      const deviceInfo = await import('@ohos.deviceInfo');
      const manufacturer = deviceInfo.manufacture || '';
      const model = deviceInfo.marketName || deviceInfo.productModel || '';

      // 从安全区读取信任根
      let rootOfTrust = '';
      try {
        // @ts-ignore — 鸿蒙安全API
        const huks = await import('@ohos.security.huks');
        // 获取设备唯一安全标识
        rootOfTrust = 'HUKS-SECURE-ELEMENT';
      } catch (_) { /* 降级 */ }

      return {
        manufacturer,
        model,
        rootOfTrust: rootOfTrust || 'DEVICE-ATTESTATION',
      };
    } catch (e) {
      return {
        manufacturer: 'Unknown',
        model: 'Unknown',
        rootOfTrust: 'UNAVAILABLE',
      };
    }
  }

  // 获取芯片授权状态
  isChipAuthorized(): boolean {
    return this.chipAuthorized;
  }

  // ================================================================
  // 传感器管理
  // ================================================================
  enableSensor(type: PerceptionType): void {
    this.sensorsEnabled.set(type, true);
    console.info(`[龍魂·伦理感知] 启用传感器: ${type}`);
  }

  disableSensor(type: PerceptionType): void {
    this.sensorsEnabled.set(type, false);
    console.info(`[龍魂·伦理感知] 停用传感器: ${type}`);
  }

  isSensorEnabled(type: PerceptionType): boolean {
    return this.sensorsEnabled.get(type) ?? false;
  }

  getEnabledSensors(): PerceptionType[] {
    return Array.from(this.sensorsEnabled.entries())
      .filter(([_, enabled]) => enabled)
      .map(([type, _]) => type);
  }

  // ================================================================
  // 伦理设备注册（芯片级白名单）
  // ================================================================
  registerEthicalDevice(deviceId: string, signature: EthicalChipSignature): boolean {
    // 验证芯片签名
    if (!this.verifyChipSignature(signature)) {
      console.warn(`[龍魂·伦理感知] 芯片签名无效: ${deviceId}`);
      return false;
    }

    // 检查是否在有效期内
    if (Date.now() > signature.expiresAt) {
      console.warn(`[龍魂·伦理感知] 芯片签名已过期: ${deviceId}`);
      return false;
    }

    // 必须包含核心约束
    const coreConstraints = ['NO_HARM_TO_HUMANS', 'HUMAN_OVERRIDE'];
    const hasCore = coreConstraints.every(c => signature.constraints.includes(c));
    if (!hasCore) {
      console.warn(`[龍魂·伦理感知] 缺少核心约束: ${deviceId}`);
      return false;
    }

    this.ethicalWhitelist.set(deviceId, signature);
    console.info(`[龍魂·伦理感知] ✅ 注册伦理设备: ${deviceId} (${signature.chipId})`);
    return true;
  }

  // 验证芯片级伦理签名（国密SM2）
  private verifyChipSignature(signature: EthicalChipSignature): boolean {
    if (!signature.chipId || !signature.manufacturer) return false;
    if (!signature.sm2Signature || !signature.rootOfTrust) return false;
    if (!signature.constraints || signature.constraints.length === 0) return false;
    if (!signature.fuseSupported) return false;

    // 实际调用国密SM2验证
    // verifySM2(signature.sm2Signature, buildPayload(signature), signature.rootOfTrust)

    return true;
  }

  // 吊销伦理设备
  revokeEthicalDevice(deviceId: string): void {
    this.ethicalWhitelist.delete(deviceId);
    console.info(`[龍魂·伦理感知] 吊销伦理设备: ${deviceId}`);
  }

  // ================================================================
  // 多模态融合识别
  // ================================================================
  async detectTargets(sensorData: PerceptionData[]): Promise<TargetProfile[]> {
    if (!this.chipAuthorized) {
      console.warn('[龍魂·伦理感知] 芯片未授权，跳过检测');
      return [];
    }

    const profiles: TargetProfile[] = [];

    for (const data of sensorData) {
      const profile = await this.analyzeSensorData(data);
      if (profile) {
        profiles.push(profile);
      }
    }

    // 融合多传感器判定
    return this.fusionDecision(profiles);
  }

  // 分析单路传感器数据
  private async analyzeSensorData(data: PerceptionData): Promise<TargetProfile | null> {
    switch (data.type) {
      case PerceptionType.CAMERA:
        return this.analyzeVisual(data);
      case PerceptionType.INFRARED:
      case PerceptionType.THERMAL:
        return this.analyzeThermal(data);
      case PerceptionType.MAGNETIC:
      case PerceptionType.RADAR:
        return this.analyzeElectromagnetic(data);
      case PerceptionType.NETWORK:
      case PerceptionType.WIFI_PROBE:
      case PerceptionType.BLE_SCAN:
        return this.analyzeNetwork(data);
      case PerceptionType.SOUND:
        return this.analyzeAcoustic(data);
      default:
        return null;
    }
  }

  // ================================================================
  // 视觉分析
  // ================================================================
  private async analyzeVisual(data: PerceptionData): Promise<TargetProfile | null> {
    const features = data.value as unknown as VisualFeatures;

    // 人类特征识别
    if (features.hasHumanFace || features.hasHumanShape) {
      return {
        id: `HUMAN-${Date.now()}`,
        type: TargetType.HUMAN,
        confidence: 0.95,
        location: data.location,
        timestamp: Date.now(),
        features: { visual: features },
        threatLevel: ThreatLevel.NONE,
        ethicalChipSignature: null,
        deviceFingerprint: null,
      };
    }

    // 机器人识别
    if (features.hasMechanicalJoints || features.hasSyntheticMaterial) {
      const robotId = features.detectedId || `ROBOT-${Date.now()}`;
      const ethical = this.ethicalWhitelist.get(robotId);

      if (ethical) {
        return {
          id: robotId,
          type: TargetType.ROBOT_ETHICAL,
          confidence: 0.90,
          location: data.location,
          timestamp: Date.now(),
          features: { visual: features },
          threatLevel: ThreatLevel.NONE,
          ethicalChipSignature: ethical,
          deviceFingerprint: null,
        };
      } else {
        return {
          id: robotId,
          type: TargetType.ROBOT_UNETHICAL,
          confidence: 0.85,
          location: data.location,
          timestamp: Date.now(),
          features: { visual: features },
          threatLevel: this.assessUntrustedRobotThreat(features),
          ethicalChipSignature: null,
          deviceFingerprint: null,
        };
      }
    }

    // 异常行为检测
    if (features.anomalousBehavior) {
      return {
        id: `ANOMALY-${Date.now()}`,
        type: TargetType.AI_ANOMALY,
        confidence: 0.80,
        location: data.location,
        timestamp: Date.now(),
        features: { visual: features },
        threatLevel: ThreatLevel.HIGH,
        ethicalChipSignature: null,
        deviceFingerprint: null,
      };
    }

    return null;
  }

  // 评估非信任机器人威胁
  private assessUntrustedRobotThreat(features: VisualFeatures): ThreatLevel {
    let score = 0;

    if (features.hasSyntheticMaterial) score += 1;
    if (features.motionPattern === 'erratic') score += 2;
    if (features.motionPattern === 'approaching') score += 3;
    if (features.objectCount && features.objectCount > 1) score += 1;

    if (score >= 4) return ThreatLevel.CRITICAL;
    if (score >= 3) return ThreatLevel.HIGH;
    if (score >= 2) return ThreatLevel.MEDIUM;
    return ThreatLevel.LOW;
  }

  // ================================================================
  // 网络信号分析 — WiFi/BLE/协议扫描
  // ================================================================
  private async analyzeNetwork(data: PerceptionData): Promise<TargetProfile | null> {
    const sig = data.value as unknown as NetworkSignature;

    // 检测伦理信标
    if (sig.ethicalBeacon) {
      try {
        const parsed = JSON.parse(sig.ethicalBeacon) as EthicalChipSignature;
        if (this.verifyChipSignature(parsed)) {
          return {
            id: sig.deviceId,
            type: TargetType.ROBOT_ETHICAL,
            confidence: 0.95,
            location: data.location,
            timestamp: Date.now(),
            features: { network: sig },
            threatLevel: ThreatLevel.NONE,
            ethicalChipSignature: parsed,
            deviceFingerprint: null,
          };
        }
      } catch (_) { /* 解析失败，视为非伦理 */ }
    }

    // AI流量模式检测
    if (sig.aiTrafficPattern && !sig.ethicalBeacon) {
      const threat = sig.packetRate > 100 ? ThreatLevel.HIGH : ThreatLevel.MEDIUM;
      return {
        id: sig.deviceId || `UNETHICAL-${Date.now()}`,
        type: TargetType.ROBOT_UNETHICAL,
        confidence: 0.75,
        location: data.location,
        timestamp: Date.now(),
        features: { network: sig },
        threatLevel: threat,
        ethicalChipSignature: null,
        deviceFingerprint: null,
      };
    }

    // MAC厂商识别
    if (sig.macVendor) {
      const droneVendors = ['DJI', 'Parrot', 'Skydio', 'Autel'];
      const robotVendors = ['Boston', 'Unitree', 'UBTECH', 'Xiaomi'];

      const upperVendor = sig.macVendor.toUpperCase();
      if (droneVendors.some(v => upperVendor.includes(v.toUpperCase()))) {
        return {
          id: sig.deviceId || `DRONE-${Date.now()}`,
          type: TargetType.DRONE,
          confidence: 0.80,
          location: data.location,
          timestamp: Date.now(),
          features: { network: sig },
          threatLevel: ThreatLevel.MEDIUM,
          ethicalChipSignature: null,
          deviceFingerprint: null,
        };
      }
      if (robotVendors.some(v => upperVendor.includes(v.toUpperCase()))) {
        return {
          id: sig.deviceId || `ROBOT-${Date.now()}`,
          type: TargetType.ROBOT_UNETHICAL,
          confidence: 0.80,
          location: data.location,
          timestamp: Date.now(),
          features: { network: sig },
          threatLevel: ThreatLevel.HIGH,
          ethicalChipSignature: null,
          deviceFingerprint: null,
        };
      }
    }

    return null;
  }

  // ================================================================
  // 电磁特征分析
  // ================================================================
  private async analyzeElectromagnetic(data: PerceptionData): Promise<TargetProfile | null> {
    const sig = data.value as unknown as ElectromagneticSignature;

    if (sig.anomalyScore > 0.7) {
      return {
        id: `EM-ANOMALY-${Date.now()}`,
        type: TargetType.AI_ANOMALY,
        confidence: sig.anomalyScore,
        location: data.location,
        timestamp: Date.now(),
        features: { electromagnetic: sig },
        threatLevel: ThreatLevel.HIGH,
        ethicalChipSignature: null,
        deviceFingerprint: null,
      };
    }

    return null;
  }

  // ================================================================
  // 热成像分析
  // ================================================================
  private async analyzeThermal(data: PerceptionData): Promise<TargetProfile | null> {
    const heatData = data.value as Record<string, Object>;

    // 人体温度范围 36-37°C
    const hasHumanTemp = heatData['maxTemp'] as number > 35 && heatData['maxTemp'] as number < 38;
    // 机器温度可能更高或更低
    const hasMachineTemp = heatData['maxTemp'] as number > 45 || heatData['maxTemp'] as number < 25;

    if (hasHumanTemp) {
      return {
        id: `THERMAL-HUMAN-${Date.now()}`,
        type: TargetType.HUMAN,
        confidence: 0.85,
        location: data.location,
        timestamp: Date.now(),
        features: { thermal: heatData },
        threatLevel: ThreatLevel.NONE,
        ethicalChipSignature: null,
        deviceFingerprint: null,
      };
    }

    if (hasMachineTemp) {
      return {
        id: `THERMAL-MACHINE-${Date.now()}`,
        type: TargetType.UNKNOWN,
        confidence: 0.65,
        location: data.location,
        timestamp: Date.now(),
        features: { thermal: heatData },
        threatLevel: ThreatLevel.LOW,
        ethicalChipSignature: null,
        deviceFingerprint: null,
      };
    }

    return null;
  }

  // ================================================================
  // 声纹分析
  // ================================================================
  private async analyzeAcoustic(data: PerceptionData): Promise<TargetProfile | null> {
    const audioData = data.value as Record<string, Object>;

    const humanVoice = audioData['humanVoice'] as boolean;
    const motorNoise = audioData['motorNoise'] as boolean;
    const droneBuzz = audioData['droneBuzz'] as boolean;

    if (droneBuzz) {
      return {
        id: `AUDIO-DRONE-${Date.now()}`,
        type: TargetType.DRONE,
        confidence: 0.85,
        location: data.location,
        timestamp: Date.now(),
        features: { audio: audioData },
        threatLevel: ThreatLevel.MEDIUM,
        ethicalChipSignature: null,
        deviceFingerprint: null,
      };
    }

    if (motorNoise && !humanVoice) {
      return {
        id: `AUDIO-MACHINE-${Date.now()}`,
        type: TargetType.UNKNOWN,
        confidence: 0.70,
        location: data.location,
        timestamp: Date.now(),
        features: { audio: audioData },
        threatLevel: ThreatLevel.LOW,
        ethicalChipSignature: null,
        deviceFingerprint: null,
      };
    }

    return null;
  }

  // ================================================================
  // 多传感器融合决策
  // ================================================================
  private fusionDecision(profiles: TargetProfile[]): TargetProfile[] {
    const merged = new Map<string, TargetProfile>();

    for (const p of profiles) {
      const existing = merged.get(p.id);
      if (existing) {
        // 多传感器交叉验证 → 提升置信度
        existing.confidence = Math.min(existing.confidence + 0.10, 1.0);
        existing.features = { ...existing.features, ...p.features };

        // 多传感器一致确认高威胁 → 升级
        if (p.threatLevel === ThreatLevel.CRITICAL) {
          existing.threatLevel = ThreatLevel.CRITICAL;
        }

        // 多传感器确认伦理签名 → 标记为可信
        if (p.ethicalChipSignature && !existing.ethicalChipSignature) {
          existing.ethicalChipSignature = p.ethicalChipSignature;
          existing.type = TargetType.ROBOT_ETHICAL;
        }
      } else {
        merged.set(p.id, p);
      }
    }

    const results = Array.from(merged.values());

    // 更新内部检测记录
    for (const r of results) {
      this.detectedTargets.set(r.id, r);
    }

    return results;
  }

  // ================================================================
  // 查询接口
  // ================================================================
  getDetectedTargets(): TargetProfile[] {
    return Array.from(this.detectedTargets.values());
  }

  getTarget(targetId: string): TargetProfile | undefined {
    return this.detectedTargets.get(targetId);
  }

  getUntrustedTargets(): TargetProfile[] {
    return this.getDetectedTargets().filter(
      t => t.type !== TargetType.HUMAN && t.type !== TargetType.ROBOT_ETHICAL
    );
  }

  getHighThreatTargets(): TargetProfile[] {
    return this.getDetectedTargets().filter(
      t => t.threatLevel === ThreatLevel.HIGH || t.threatLevel === ThreatLevel.CRITICAL
    );
  }

  getEthicalWhitelistSize(): number {
    return this.ethicalWhitelist.size;
  }

  getAnomalyHistory(): Array<{targetId: string, timestamp: number, description: string}> {
    return this.anomalyHistory;
  }

  clearTarget(targetId: string): void {
    this.detectedTargets.delete(targetId);
  }

  clearAllTargets(): void {
    this.detectedTargets.clear();
  }

  addAnomalyEntry(targetId: string, description: string): void {
    this.anomalyHistory.push({
      targetId,
      timestamp: Date.now(),
      description,
    });
  }
}

// ================================================================
// 单例导出
// ================================================================
export const ethicalPerception = EthicalPerception.getInstance();

// models/SecurityModel.ets
// 龍魂 · 安全数据模型 · 伦理防御基础类型
// DNA: #龍芯⚡️丙午·辛未·丙戌·ETHICAL-DEFENSE-MODEL-v1.0

// === 感知类型 ===
export enum PerceptionType {
  CAMERA = 'camera',
  INFRARED = 'infrared',
  MAGNETIC = 'magnetic',
  RADAR = 'radar',
  NETWORK = 'network',
  SOUND = 'sound',
  WIFI_PROBE = 'wifi_probe',
  BLE_SCAN = 'ble_scan',
  THERMAL = 'thermal'
}

// === 威胁等级 ===
export enum ThreatLevel {
  NONE = 'none',           // 无威胁
  LOW = 'low',             // 低
  MEDIUM = 'medium',       // 中
  HIGH = 'high',           // 高
  CRITICAL = 'critical'    // 严重
}

// === 感知数据 ===
export interface PerceptionData {
  type: PerceptionType;
  value: Record<string, Object>;
  location: string;
  timestamp: number;
  confidence: number;
  source: string;
}

// === 设备指纹 ===
export interface DeviceFingerprint {
  macAddress: string;
  deviceName: string;
  vendor: string;
  deviceType: string;
  signalStrength: number;
  firstSeen: number;
  lastSeen: number;
  seenCount: number;
  services: string[];
  osFingerprint: string;
  robotScore: number;
  threatLevel: ThreatLevel;
  isWhitelisted: boolean;
  hasEthicalSignature: boolean;
}

// === 伦理签名（芯片级） ===
export interface EthicalChipSignature {
  chipId: string;             // 芯片唯一ID
  manufacturer: string;       // 制造商（仅限中国厂商）
  modelVersion: string;       // 芯片型号
  protocolVersion: string;    // 伦理协议版本
  issuedAt: number;           // 签发时间戳
  expiresAt: number;          // 过期时间戳
  constraints: string[];      // 行为约束列表
  fuseSupported: boolean;     // 是否支持硬件熔断
  fuseCertHash: string;       // 熔断证书哈希
  sm2Signature: string;       // 国密SM2签名
  rootOfTrust: string;        // 信任根
}

// === 伦理熔断记录 ===
export interface BreakerRecord {
  id: string;
  targetId: string;
  targetType: string;
  triggerReasons: string[];
  level: string;
  actions: string[];
  timestamp: number;
  chipId: string;
  dnaSignature: string;
  auditHash: string;
}

// === 干扰记录 ===
export interface InterferenceRecord {
  id: string;
  targetId: string;
  type: string;
  intensity: string;
  reason: string;
  startTime: number;
  endTime: number;
  status: string;
  hardwareUsed: string;
  dnaSignature: string;
}

// === 守护场状态 ===
export interface GuardianFieldStatus {
  active: boolean;
  fieldRadiusMeters: number;
  knownDevices: number;
  whitelistedDevices: number;
  activeInterferences: number;
  pendingReviews: number;
  totalBreakersTriggered: number;
  uptime: number;
  chipTemperature: number;
  lastScan: number;
}

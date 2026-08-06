/// 🐉 分布式数据模型
/// DNA: #龍芯⚡️2026-08-06-DISTRIBUTED-MODELS-V1.0-UID9622
/// License: MulanPSL v2

/// 分布式设备信息
class DistributedDevice {
  final String deviceId;
  final String deviceName;
  final String deviceType;
  final String osVersion;
  final bool isOnline;
  final bool isTrusted;
  final bool isConnected;
  final String? ipAddress;
  final int? batteryLevel;

  DistributedDevice({
    required this.deviceId, required this.deviceName, required this.deviceType,
    this.osVersion = '', required this.isOnline, required this.isTrusted,
    required this.isConnected, this.ipAddress, this.batteryLevel,
  });

  factory DistributedDevice.fromMap(Map<dynamic, dynamic> map) {
    return DistributedDevice(
      deviceId: map['deviceId'] ?? '', deviceName: map['deviceName'] ?? 'Unknown',
      deviceType: map['deviceType'] ?? 'unknown', osVersion: map['osVersion'] ?? '',
      isOnline: map['isOnline'] ?? false, isTrusted: map['isTrusted'] ?? false,
      isConnected: map['isConnected'] ?? false,
      ipAddress: map['ipAddress'], batteryLevel: map['batteryLevel'],
    );
  }

  Map<String, dynamic> toMap() => {
        'deviceId': deviceId, 'deviceName': deviceName,
        'deviceType': deviceType, 'osVersion': osVersion,
        'isOnline': isOnline, 'isTrusted': isTrusted,
        'isConnected': isConnected, 'ipAddress': ipAddress,
        'batteryLevel': batteryLevel,
      };

  String get statusIcon => isConnected ? '🟢' : isOnline ? '🟡' : '⚪';
  String get statusText => isConnected ? '已连接' : isOnline ? '在线' : '离线';
}

/// 设备事件
class DeviceEvent {
  final String deviceId;
  final String deviceName;
  final String eventType;
  final int timestamp;
  final String dna;

  DeviceEvent({
    required this.deviceId, required this.deviceName,
    required this.eventType, required this.timestamp, required this.dna,
  });

  factory DeviceEvent.fromMap(Map<String, dynamic> map) {
    return DeviceEvent(
      deviceId: map['deviceId'] ?? '', deviceName: map['deviceName'] ?? '',
      eventType: map['eventType'] ?? 'unknown',
      timestamp: map['timestamp'] ?? 0, dna: map['dna'] ?? '',
    );
  }
}

/// 同步事件
class SyncEvent {
  final String key;
  final String sourceDeviceId;
  final String targetDeviceId;
  final bool success;
  final String? error;
  final int timestamp;
  final String dna;

  SyncEvent({
    required this.key, required this.sourceDeviceId,
    required this.targetDeviceId, required this.success,
    this.error, required this.timestamp, required this.dna,
  });

  factory SyncEvent.fromMap(Map<String, dynamic> map) {
    return SyncEvent(
      key: map['key'] ?? '', sourceDeviceId: map['sourceDeviceId'] ?? '',
      targetDeviceId: map['targetDeviceId'] ?? '', success: map['success'] ?? false,
      error: map['error'], timestamp: map['timestamp'] ?? 0, dna: map['dna'] ?? '',
    );
  }
}

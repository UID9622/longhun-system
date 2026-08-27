// 🐉 龙魂·数据模型
// DNA: #龍芯⚡️2026-08-06-BRIDGE-MODELS-V1.0-UID9622
// License: MulanPSL v2

import 'dart:convert';
import 'constants.dart';

// ============================================================
// 设备信息
// ============================================================

class DeviceInfo {
  final String osFullName;
  final String sdkApiVersion;
  final String deviceType;
  final String deviceName;
  final String manufacturer;
  final String serialNumber;

  DeviceInfo({
    required this.osFullName,
    required this.sdkApiVersion,
    required this.deviceType,
    required this.deviceName,
    required this.manufacturer,
    this.serialNumber = '',
  });

  factory DeviceInfo.fromMap(Map<String, dynamic> map) {
    return DeviceInfo(
      osFullName: map['osFullName'] ?? 'OpenHarmony',
      sdkApiVersion: map['sdkApiVersion'] ?? '12',
      deviceType: map['deviceType'] ?? 'unknown',
      deviceName: map['deviceName'] ?? 'HarmonyOS Device',
      manufacturer: map['manufacturer'] ?? 'Unknown',
      serialNumber: map['serialNumber'] ?? '',
    );
  }

  Map<String, dynamic> toMap() => {
        'osFullName': osFullName,
        'sdkApiVersion': sdkApiVersion,
        'deviceType': deviceType,
        'deviceName': deviceName,
        'manufacturer': manufacturer,
        'serialNumber': serialNumber,
      };

  String toJson() => jsonEncode(toMap());
}

// ============================================================
// 审计结果
// ============================================================

class AuditResult {
  final String status; // 🟢 🟡 🔴
  final int score; // 0-100
  final List<String> violations;
  final List<String> warnings;
  final String dna;
  final String timestamp;
  final Map<String, double> dimensions;

  AuditResult({
    required this.status,
    required this.score,
    this.violations = const [],
    this.warnings = const [],
    required this.dna,
    required this.timestamp,
    this.dimensions = const {},
  });

  factory AuditResult.fromMap(Map<String, dynamic> map) {
    return AuditResult(
      status: map['status'] ?? '🟡',
      score: map['score'] ?? 0,
      violations: List<String>.from(map['violations'] ?? []),
      warnings: List<String>.from(map['warnings'] ?? []),
      dna: map['dna'] ?? '',
      timestamp: map['timestamp'] ?? '',
      dimensions: Map<String, double>.from(map['dimensions'] ?? {}),
    );
  }

  Map<String, dynamic> toMap() => {
        'status': status,
        'score': score,
        'violations': violations,
        'warnings': warnings,
        'dna': dna,
        'timestamp': timestamp,
        'dimensions': dimensions,
      };

  String toJson() => jsonEncode(toMap());
  bool get isPassed => status == '🟢';
  bool get needsReview => status == '🟡';
  bool get isRejected => status == '🔴';
}

// ============================================================
// 主权状态
// ============================================================

class SovereigntyStatus {
  final bool isValid;
  final String uid;
  final String owner;
  final String confirmCode;
  final String deviceBind;
  final String deviceId;
  final String signature;
  final String timestamp;

  SovereigntyStatus({
    required this.isValid,
    required this.uid,
    required this.owner,
    required this.confirmCode,
    required this.deviceBind,
    required this.deviceId,
    required this.signature,
    required this.timestamp,
  });

  factory SovereigntyStatus.fromMap(Map<String, dynamic> map) {
    return SovereigntyStatus(
      isValid: map['isValid'] ?? false,
      uid: map['uid'] ?? LonghunConstants.UID,
      owner: map['owner'] ?? LonghunConstants.OWNER,
      confirmCode: map['confirmCode'] ?? LonghunConstants.CONFIRM_CODE,
      deviceBind: map['deviceBind'] ?? LonghunConstants.DEVICE_BIND,
      deviceId: map['deviceId'] ?? '',
      signature: map['signature'] ?? '',
      timestamp: map['timestamp'] ?? '',
    );
  }

  Map<String, dynamic> toMap() => {
        'isValid': isValid,
        'uid': uid,
        'owner': owner,
        'confirmCode': confirmCode,
        'deviceBind': deviceBind,
        'deviceId': deviceId,
        'signature': signature,
        'timestamp': timestamp,
      };
}

// ============================================================
// DNA 信息
// ============================================================

class DNAInfo {
  final String full;
  final String prefix;
  final String date;
  final String type;
  final String random;
  final String uid;

  DNAInfo({
    required this.full,
    required this.prefix,
    required this.date,
    required this.type,
    required this.random,
    required this.uid,
  });

  factory DNAInfo.fromString(String dna) {
    final parts = dna.replaceFirst('#', '').split('⚡️');
    final prefix = parts[0];
    final rest = parts[1];
    final segments = rest.split('-');
    final date = segments[0];
    final type = segments.length > 1 ? segments[1] : '';
    final random = segments.length > 2 ? segments[2] : '';
    final uid = segments.length > 3 ? segments[3] : '';

    return DNAInfo(
      full: dna,
      prefix: prefix,
      date: date,
      type: type,
      random: random,
      uid: uid,
    );
  }

  bool get isValid => full.contains('UID9622');
}

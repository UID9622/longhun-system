// 🐉 龙魂·核心通信桥接插件
// DNA: #龍芯⚡️2026-08-06-BRIDGE-PLUGIN-V2.0-UID9622
// 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// License: MulanPSL v2

import 'dart:async';
import 'package:flutter/services.dart';
import 'constants.dart';
import 'exceptions.dart';
import 'models.dart';

/// 龙魂核心桥接插件
/// 提供MethodChannel和EventChannel的统一封装
class LonghunBridge {
  // ============================================================
  // 单例模式
  // ============================================================

  static final LonghunBridge _instance = LonghunBridge._internal();
  factory LonghunBridge() => _instance;
  LonghunBridge._internal();

  // ============================================================
  // 通道
  // ============================================================

  static const MethodChannel _methodChannel =
      MethodChannel(LonghunConstants.METHOD_CHANNEL);

  static const EventChannel _eventChannel =
      EventChannel(LonghunConstants.EVENT_CHANNEL);

  // ============================================================
  // MethodChannel 接口
  // ============================================================

  /// 获取设备信息
  Future<DeviceInfo> getDeviceInfo() async {
    try {
      final result = await _methodChannel
          .invokeMethod('getDeviceInfo')
          .timeout(LonghunConstants.DEFAULT_TIMEOUT);
      return DeviceInfo.fromMap(Map<String, dynamic>.from(result));
    } on PlatformException catch (e) {
      throw ChannelException('获取设备信息失败: ${e.message}', code: e.code);
    } on TimeoutException {
      throw ChannelException('获取设备信息超时');
    }
  }

  /// 生成DNA追溯码
  Future<String> generateDNA({String? prefix, String? type}) async {
    try {
      final result = await _methodChannel.invokeMethod('generateDNA', {
        'prefix': prefix ?? LonghunConstants.DNA_PREFIX,
        'type': type ?? 'GEN',
      }).timeout(LonghunConstants.DEFAULT_TIMEOUT);
      return result;
    } on PlatformException catch (e) {
      throw DNAException('生成DNA失败: ${e.message}', code: e.code);
    } on TimeoutException {
      throw DNAException('生成DNA超时');
    }
  }

  /// 执行三色审计
  Future<AuditResult> runAudit(Map<String, dynamic> data) async {
    try {
      final result = await _methodChannel
          .invokeMethod('runAudit', data)
          .timeout(LonghunConstants.DEFAULT_TIMEOUT);
      return AuditResult.fromMap(Map<String, dynamic>.from(result));
    } on PlatformException catch (e) {
      throw AuditException('审计失败: ${e.message}', code: e.code);
    } on TimeoutException {
      throw AuditException('审计超时');
    }
  }

  /// 主权验证
  Future<SovereigntyStatus> verifySovereignty() async {
    try {
      final result = await _methodChannel
          .invokeMethod('verifySovereignty')
          .timeout(LonghunConstants.DEFAULT_TIMEOUT);
      return SovereigntyStatus.fromMap(Map<String, dynamic>.from(result));
    } on PlatformException catch (e) {
      throw SovereigntyException('主权验证失败: ${e.message}', code: e.code);
    } on TimeoutException {
      throw SovereigntyException('主权验证超时');
    }
  }

  /// 验证DNA格式
  Future<bool> validateDNA(String dna) async {
    try {
      final result = await _methodChannel
          .invokeMethod('validateDNA', {'dna': dna})
          .timeout(LonghunConstants.DEFAULT_TIMEOUT);
      return result ?? false;
    } on PlatformException {
      return false;
    }
  }

  /// 获取系统状态
  Future<Map<String, dynamic>> getSystemStatus() async {
    try {
      final result = await _methodChannel
          .invokeMethod('getSystemStatus')
          .timeout(LonghunConstants.DEFAULT_TIMEOUT);
      return Map<String, dynamic>.from(result);
    } on PlatformException catch (e) {
      throw ChannelException('获取系统状态失败: ${e.message}', code: e.code);
    }
  }

  // ============================================================
  // EventChannel 接口
  // ============================================================

  /// 监听系统事件
  Stream<Map<String, dynamic>> get systemEvents {
    return _eventChannel
        .receiveBroadcastStream('system')
        .map((event) => Map<String, dynamic>.from(event));
  }

  /// 监听主权状态变化
  Stream<Map<String, dynamic>> get sovereigntyEvents {
    return _eventChannel
        .receiveBroadcastStream('sovereignty')
        .map((event) => Map<String, dynamic>.from(event));
  }

  /// 监听审计事件
  Stream<Map<String, dynamic>> get auditEvents {
    return _eventChannel
        .receiveBroadcastStream('audit')
        .map((event) => Map<String, dynamic>.from(event));
  }

  /// 监听自定义事件
  Stream<Map<String, dynamic>> listenEvent(String type) {
    return _eventChannel
        .receiveBroadcastStream(type)
        .map((event) => Map<String, dynamic>.from(event));
  }
}

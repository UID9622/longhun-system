// 🐉 龙魂·鸿蒙分布式能力插件
// DNA: #龍芯⚡️2026-08-06-DISTRIBUTED-PLUGIN-V2.0-UID9622
// 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// License: MulanPSL v2

import 'dart:async';
import 'package:flutter/services.dart';
import 'models.dart';

/// 鸿蒙分布式能力插件
/// 支持设备发现、连接、数据同步、跨设备调用
class OhosDistributed {
  static const MethodChannel _methodChannel =
      MethodChannel('com.longhun.distributed/method');
  static const EventChannel _eventChannel =
      EventChannel('com.longhun.distributed/event');

  static final OhosDistributed _instance = OhosDistributed._internal();
  factory OhosDistributed() => _instance;
  OhosDistributed._internal();

  /// 发现附近设备
  Future<List<DistributedDevice>> discoverDevices() async {
    try {
      final List<dynamic> result =
          await _methodChannel.invokeMethod('discoverDevices');
      return result.map((d) => DistributedDevice.fromMap(d)).toList();
    } on PlatformException {
      return [];
    }
  }

  /// 连接到设备
  Future<bool> connectDevice(String deviceId) async {
    try {
      final result = await _methodChannel.invokeMethod(
          'connectDevice', {'deviceId': deviceId});
      return result ?? false;
    } on PlatformException {
      return false;
    }
  }

  /// 断开设备连接
  Future<bool> disconnectDevice(String deviceId) async {
    try {
      final result = await _methodChannel.invokeMethod(
          'disconnectDevice', {'deviceId': deviceId});
      return result ?? false;
    } on PlatformException {
      return false;
    }
  }

  /// 获取已连接设备列表
  Future<List<DistributedDevice>> getConnectedDevices() async {
    try {
      final List<dynamic> result =
          await _methodChannel.invokeMethod('getConnectedDevices');
      return result.map((d) => DistributedDevice.fromMap(d)).toList();
    } on PlatformException {
      return [];
    }
  }

  /// 同步数据到其他设备
  Future<bool> syncData(String key, Map<String, dynamic> data,
      {List<String>? targetDevices}) async {
    try {
      final result = await _methodChannel.invokeMethod('syncData', {
        'key': key, 'data': data,
        'targetDevices': targetDevices ?? [],
      });
      return result ?? false;
    } on PlatformException {
      return false;
    }
  }

  /// 从其他设备读取数据
  Future<Map<String, dynamic>?> readData(String key, String deviceId) async {
    try {
      final result = await _methodChannel.invokeMethod(
          'readData', {'key': key, 'deviceId': deviceId});
      return Map<String, dynamic>.from(result);
    } on PlatformException {
      return null;
    }
  }

  /// 设备事件流
  Stream<DeviceEvent> get deviceEvents {
    return _eventChannel
        .receiveBroadcastStream('device')
        .map((event) => DeviceEvent.fromMap(Map<String, dynamic>.from(event)));
  }

  /// 数据同步事件流
  Stream<SyncEvent> get syncEvents {
    return _eventChannel
        .receiveBroadcastStream('sync')
        .map((event) => SyncEvent.fromMap(Map<String, dynamic>.from(event)));
  }
}

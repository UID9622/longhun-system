// 🐉 龙魂·鸿蒙传感器插件
// DNA: #龍芯⚡️2026-08-06-SENSOR-PLUGIN-V2.0-UID9622
// 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// License: MulanPSL v2

import 'dart:async';
import 'package:flutter/services.dart';
import 'models.dart';
import 'enums.dart';

/// 鸿蒙传感器插件
/// 支持加速度计、陀螺仪、磁力计、光线、接近、心率等传感器
class OhosSensors {
  static const MethodChannel _methodChannel =
      MethodChannel('com.longhun.sensors/method');
  static const EventChannel _eventChannel =
      EventChannel('com.longhun.sensors/event');

  static final OhosSensors _instance = OhosSensors._internal();
  factory OhosSensors() => _instance;
  OhosSensors._internal();

  final List<StreamSubscription> _subscriptions = [];

  /// 检查传感器是否可用
  Future<bool> isAvailable(SensorType type) async {
    try {
      final result = await _methodChannel
          .invokeMethod('isSensorAvailable', {'type': type.index});
      return result ?? false;
    } on PlatformException {
      return false;
    }
  }

  /// 订阅传感器数据
  Stream<SensorData> subscribe(SensorType type, {int interval = 100}) {
    return _eventChannel
        .receiveBroadcastStream({'type': type.index, 'interval': interval})
        .map((event) => SensorData.fromMap(Map<String, dynamic>.from(event)));
  }

  /// 订阅并自动管理生命周期
  StreamSubscription<SensorData> subscribeManaged(
    SensorType type, {
    required void Function(SensorData) onData,
    void Function(Object)? onError,
    int interval = 100,
  }) {
    final sub = subscribe(type, interval: interval).listen(onData, onError: onError);
    _subscriptions.add(sub);
    return sub;
  }

  /// 取消所有订阅
  void unsubscribeAll() {
    for (final sub in _subscriptions) {
      sub.cancel();
    }
    _subscriptions.clear();
    _methodChannel.invokeMethod('unsubscribeAll');
  }

  /// 获取当前传感器数据（一次性）
  Future<SensorData?> getCurrentData(SensorType type) async {
    try {
      final result = await _methodChannel
          .invokeMethod('getCurrentData', {'type': type.index});
      if (result != null) {
        return SensorData.fromMap(Map<String, dynamic>.from(result));
      }
      return null;
    } on PlatformException {
      return null;
    }
  }

  /// 获取所有可用传感器列表
  Future<List<SensorType>> getAvailableSensors() async {
    try {
      final result = await _methodChannel.invokeMethod('getAvailableSensors');
      final List<dynamic> list = result ?? [];
      return list.map((e) => SensorType.values[e]).toList();
    } on PlatformException {
      return [];
    }
  }
}

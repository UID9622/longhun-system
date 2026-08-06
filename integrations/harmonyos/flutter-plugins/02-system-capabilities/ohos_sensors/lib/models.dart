/// 🐉 传感器数据模型
/// DNA: #龍芯⚡️2026-08-06-SENSOR-MODELS-V1.0-UID9622
/// License: MulanPSL v2

import 'dart:math';
import 'enums.dart';

class SensorData {
  final SensorType type;
  final List<double> values;
  final double? accuracy;
  final int timestamp;
  final String dna;

  SensorData({
    required this.type,
    required this.values,
    this.accuracy,
    required this.timestamp,
    required this.dna,
  });

  factory SensorData.fromMap(Map<String, dynamic> map) {
    return SensorData(
      type: SensorType.values[map['type'] ?? 0],
      values: List<double>.from(map['values'] ?? [0.0, 0.0, 0.0]),
      accuracy: map['accuracy']?.toDouble(),
      timestamp: map['timestamp'] ?? 0,
      dna: map['dna'] ?? '',
    );
  }

  Map<String, dynamic> toMap() => {
        'type': type.index,
        'values': values,
        'accuracy': accuracy,
        'timestamp': timestamp,
        'dna': dna,
      };

  double get x => values.isNotEmpty ? values[0] : 0.0;
  double get y => values.length > 1 ? values[1] : 0.0;
  double get z => values.length > 2 ? values[2] : 0.0;

  double get magnitude {
    if (values.isEmpty) return 0.0;
    return sqrt(values.fold(0.0, (sum, v) => sum + v * v));
  }
}

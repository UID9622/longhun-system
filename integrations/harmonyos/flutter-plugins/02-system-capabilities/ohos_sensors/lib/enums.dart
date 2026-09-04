/// 🐉 传感器类型枚举
/// DNA: #龍芯⚡️2026-08-06-SENSOR-ENUMS-V1.0-UID9622
/// License: MulanPSL v2

enum SensorType {
  accelerometer,  // 加速度计
  gyroscope,      // 陀螺仪
  magnetic,       // 磁力计
  light,          // 光线
  proximity,      // 接近
  heartRate,      // 心率
  pressure,       // 气压
  temperature,    // 温度
  humidity,       // 湿度
}

extension SensorTypeExtension on SensorType {
  String get displayName {
    switch (this) {
      case SensorType.accelerometer: return '加速度计';
      case SensorType.gyroscope:     return '陀螺仪';
      case SensorType.magnetic:      return '磁力计';
      case SensorType.light:         return '光线传感器';
      case SensorType.proximity:     return '接近传感器';
      case SensorType.heartRate:     return '心率传感器';
      case SensorType.pressure:      return '气压传感器';
      case SensorType.temperature:   return '温度传感器';
      case SensorType.humidity:      return '湿度传感器';
    }
  }

  String get unit {
    switch (this) {
      case SensorType.accelerometer: return 'm/s²';
      case SensorType.gyroscope:     return 'rad/s';
      case SensorType.magnetic:      return 'μT';
      case SensorType.light:         return 'lux';
      case SensorType.proximity:     return 'cm';
      case SensorType.heartRate:     return 'bpm';
      default: return '';
    }
  }
}

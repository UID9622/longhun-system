// 🐉 龙魂·鸿蒙传感器插件（鸿蒙端）
// DNA: #龍芯⚡️2026-08-06-SENSOR-PLUGIN-HM-V2.0-UID9622
// License: MulanPSL v2

import { MethodChannel, EventChannel, MethodResult } from '@ohos.plugin';

const TAG: string = 'OhosSensorPlugin';

export default class OhosSensorPlugin {
  private methodChannel: MethodChannel;
  private eventChannel: EventChannel;
  private subscribed: Map<number, boolean> = new Map();
  private currentData: Map<number, any> = new Map();

  // 传感器类型映射
  private static readonly SENSOR_TYPES: Record<number, string> = {
    0: 'ACCELEROMETER', 1: 'GYROSCOPE', 2: 'MAGNETIC_FIELD',
    3: 'AMBIENT_LIGHT', 4: 'PROXIMITY', 5: 'HEART_RATE',
    6: 'PRESSURE', 7: 'TEMPERATURE', 8: 'HUMIDITY',
  };

  private static readonly DNA_PREFIX = '龍芯⚡️';
  private static readonly UID = '9622';

  constructor(ability: any) {
    this.methodChannel = new MethodChannel(ability, 'com.longhun.sensors/method');
    this.eventChannel = new EventChannel(ability, 'com.longhun.sensors/event');
    this.registerMethods();
  }

  private generateDNA(type: string): string {
    const now = new Date();
    const pad = (n: number) => String(n).padStart(2, '0');
    const date = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
    const rand = Math.random().toString(36).slice(2, 10).toUpperCase();
    return `#${OhosSensorPlugin.DNA_PREFIX}${date}-${type}-${rand}-${OhosSensorPlugin.UID}`;
  }

  private registerMethods(): void {
    this.methodChannel.registerMethod('isSensorAvailable',
      (data: any, result: MethodResult) => {
        const type = data?.type ?? 0;
        result.success(OhosSensorPlugin.SENSOR_TYPES[type] !== undefined);
      });

    this.methodChannel.registerMethod('unsubscribeAll',
      (_d: any, result: MethodResult) => {
        this.subscribed.clear();
        result.success(true);
      });

    this.methodChannel.registerMethod('getCurrentData',
      (data: any, result: MethodResult) => {
        const type = data?.type ?? 0;
        result.success(this.currentData.get(type) || null);
      });

    this.methodChannel.registerMethod('getAvailableSensors',
      (_d: any, result: MethodResult) => {
        const types = Object.keys(OhosSensorPlugin.SENSOR_TYPES).map(Number);
        result.success(types);
      });
  }
}

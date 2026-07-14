// entry/src/main/ets/components/Responsive.ets
// 龍魂 · 响应式装饰器 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { DeviceType, Breakpoint, deviceState } from '../models/DeviceModel';

// === 响应式属性装饰器 ===
export function Responsive<T>(values: Record<Breakpoint, T>) {
  return function (target: Object, propertyKey: string) {
    Object.defineProperty(target, propertyKey, {
      get: () => deviceState.getResponsiveValue(values),
      enumerable: true,
      configurable: true
    });
  };
}

// === 设备专属装饰器 ===
export function DeviceSpecific<T>(values: Record<DeviceType, T>) {
  return function (target: Object, propertyKey: string) {
    Object.defineProperty(target, propertyKey, {
      get: () => deviceState.getDeviceValue(values),
      enumerable: true,
      configurable: true
    });
  };
}

// === 媒体查询类 ===
export class MediaQuery {
  static minWidth(dp: number): boolean {
    return deviceState.windowWidth >= dp;
  }

  static maxWidth(dp: number): boolean {
    return deviceState.windowWidth <= dp;
  }

  static widthBetween(min: number, max: number): boolean {
    return deviceState.windowWidth >= min && deviceState.windowWidth <= max;
  }

  static isLandscape(): boolean {
    return deviceState.windowWidth > deviceState.windowHeight;
  }

  static isPortrait(): boolean {
    return deviceState.windowWidth <= deviceState.windowHeight;
  }

  static isFoldableExpanded(): boolean {
    return deviceState.currentProfile.deviceType === DeviceType.FOLDABLE &&
           deviceState.currentProfile.breakpoint >= Breakpoint.LG;
  }

  static isCar(): boolean {
    return deviceState.currentProfile.deviceType === DeviceType.CAR;
  }

  static isWatch(): boolean {
    return deviceState.currentProfile.deviceType === DeviceType.WATCH;
  }

  static isTV(): boolean {
    return deviceState.currentProfile.deviceType === DeviceType.TV;
  }
}

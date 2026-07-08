/*
 * ==========================================================================
 * 通心译 — 设备能力检查 ✅ 检查项#4
 * DNA:#龍芯⚡️丙午·丙申·癸丑·午时·需-TONGXINYI-CAPABILITY-v1.0
 * ==========================================================================
 * 原则: 调用任何系统API前先检查能力，避免低版本崩溃
 * 检查: 网络 / 剪贴板 / 分布式 / 文件IO / 屏幕信息
 * ==========================================================================
 */

import { deviceInfo } from '@kit.BasicServicesKit';
import { display } from '@kit.ArkUI';

export class DeviceCapability {
  /**
   * 检查系统能力是否可用
   */
  static checkSysCapability(sysCap: string): boolean {
    try {
      // @ts-ignore canIUse
      return globalThis.canIUse?.(sysCap) ?? false;
    } catch {
      return false;
    }
  }

  /**
   * 验证所有必须能力
   */
  static validateRequiredCaps(required: string[]): string[] {
    const missing: string[] = [];
    for (const cap of required) {
      if (!this.checkSysCapability(cap)) {
        missing.push(cap);
      }
    }
    return missing;
  }

  /** 常用能力常量 */
  static readonly CAPS = {
    INTERNET: 'SystemCapability.Communication.NetStack',
    PASTEBOARD: 'SystemCapability.MiscServices.Pasteboard',
    DISTRIBUTED_DATASYNC: 'SystemCapability.DistributedDataManager.DataShare.Consumer',
    FILE_IO: 'SystemCapability.FileManagement.File.FileIO',
    APP_FORM: 'SystemCapability.Ability.Form',
    NETWORK_INFO: 'SystemCapability.Communication.NetManager.Core',
    CRYPTO: 'SystemCapability.Security.CryptoFramework'
  } as const;

  /**
   * 获取设备类型: phone / tablet / 2in1 / car / tv / wearable
   */
  static getDeviceType(): string {
    try {
      return deviceInfo.deviceType;
    } catch {
      return 'default';
    }
  }

  /**
   * 获取屏幕密度
   */
  static getScreenDensity(): number {
    try {
      const defaultDisplay = display.getDefaultDisplaySync();
      return defaultDisplay.densityPixels;
    } catch {
      return 160;
    }
  }

  /**
   * 判断是否为平板/折叠屏
   */
  static isTablet(): boolean {
    const deviceType = this.getDeviceType();
    return deviceType === 'tablet' || deviceType === '2in1';
  }

  /**
   * 获取SDK版本
   */
  static getSDKVersion(): number {
    try {
      return deviceInfo.sdkApiVersion;
    } catch {
      return 12; // HarmonyOS 5.0 默认
    }
  }
}

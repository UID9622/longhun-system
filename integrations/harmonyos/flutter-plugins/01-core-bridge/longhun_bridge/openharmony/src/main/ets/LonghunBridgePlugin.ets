// 🐉 龙魂·鸿蒙核心通信桥接插件（鸿蒙端）
// DNA: #龍芯⚡️2026-08-06-BRIDGE-PLUGIN-HM-V2.0-UID9622
// 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// 主权锚定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
// License: MulanPSL v2

import { MethodChannel, EventChannel, MethodResult } from '@ohos.plugin';
import hilog from '@ohos.hilog';

import { MethodHandler } from './handlers/MethodHandler';
import { EventHandler } from './handlers/EventHandler';
import { SovereigntyManager } from './core/SovereigntyManager';
import { DNAGenerator } from './core/DNAGenerator';
import { Logger } from './utils/Logger';

const TAG: string = 'LonghunBridgePlugin';
const DOMAIN: number = 0xFF00;
const VERSION: string = '2.0.0';

/**
 * 龙魂桥接插件主类
 * 负责初始化所有通道和管理器
 */
export default class LonghunBridgePlugin {
  private methodChannel: MethodChannel;
  private eventChannel: EventChannel;
  private sovereigntyManager: SovereigntyManager;
  private methodHandler: MethodHandler;
  private eventHandler: EventHandler;

  constructor(ability: any) {
    this.sovereigntyManager = new SovereigntyManager();

    // 初始化通道
    this.methodChannel = new MethodChannel(ability, 'com.longhun.bridge/method');
    this.eventChannel = new EventChannel(ability, 'com.longhun.bridge/event');

    // 初始化处理器
    this.methodHandler = new MethodHandler(ability, this.sovereigntyManager);
    this.eventHandler = new EventHandler(ability, this.eventChannel, this.sovereigntyManager);

    // 注册所有方法
    this.registerMethods();

    // 启动事件监听
    this.eventHandler.startListening();

    Logger.info(TAG, `🐉 龙魂桥接插件 v${VERSION} 已初始化`);
    Logger.info(TAG, `📦 DNA: ${DNAGenerator.generate('BRIDGE')}`);
    Logger.info(TAG, `🔐 主权锚定: ${this.sovereigntyManager.getAnchor()}`);
    Logger.info(TAG, `📱 设备ID: ${this.sovereigntyManager.getDeviceId()}`);
  }

  /**
   * 注册所有MethodChannel方法
   */
  private registerMethods(): void {
    this.methodChannel.registerMethod('getDeviceInfo',
      this.methodHandler.getDeviceInfo.bind(this.methodHandler));
    this.methodChannel.registerMethod('generateDNA',
      this.methodHandler.generateDNA.bind(this.methodHandler));
    this.methodChannel.registerMethod('runAudit',
      this.methodHandler.runAudit.bind(this.methodHandler));
    this.methodChannel.registerMethod('verifySovereignty',
      this.methodHandler.verifySovereignty.bind(this.methodHandler));
    this.methodChannel.registerMethod('validateDNA',
      this.methodHandler.validateDNA.bind(this.methodHandler));
    this.methodChannel.registerMethod('getSystemStatus',
      this.methodHandler.getSystemStatus.bind(this.methodHandler));

    Logger.info(TAG, '✅ 已注册所有MethodChannel方法');
  }
}

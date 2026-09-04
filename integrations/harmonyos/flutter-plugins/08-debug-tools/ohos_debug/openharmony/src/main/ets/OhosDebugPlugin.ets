// 🐉 龙魂·调试工具插件（鸿蒙端）
// DNA: #龍芯⚡️2026-08-06-DEBUG-PLUGIN-HM-V2.0-UID9622
// License: MulanPSL v2

import { MethodChannel, MethodResult } from '@ohos.plugin';

export default class OhosDebugPlugin {
  private methodChannel: MethodChannel;

  constructor(ability: any) {
    this.methodChannel = new MethodChannel(ability, 'com.longhun.debug/method');
    this.registerMethods();
  }

  private registerMethods(): void {
    this.methodChannel.registerMethod('getMemoryUsage',
      (_d: any, result: MethodResult) => {
        result.success({ used: '128MB', total: '512MB', percent: 25 });
      });

    this.methodChannel.registerMethod('getAppLogs',
      (_d: any, result: MethodResult) => {
        result.success({ logs: [], count: 0 });
      });
  }
}

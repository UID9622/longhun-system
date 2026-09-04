/**
 * 🐉 龍魂·CoreService 客户端
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-IPC-CLIENT-UID9622
 *
 * 通过 IPC 连接插件1（核心运行时）获取数据
 */

import { rpc } from '@kit.IPCKit';
import { common } from '@kit.AbilityKit';

const CORE_SERVICE_DESCRIPTOR = 'longhun.core.service.v1';
const BUNDLE_NAME = 'com.longhun.coreservice';
const ABILITY_NAME = 'LonghunCoreService';

export class CoreServiceClient {
  private static proxy: rpc.IRemoteObject | null = null;

  /**
   * 连接核心服务
   */
  static async connect(context: common.UIAbilityContext): Promise<boolean> {
    try {
      const want = {
        bundleName: BUNDLE_NAME,
        abilityName: ABILITY_NAME
      };
      this.proxy = await context.connectServiceExtensionAbility(want);
      console.info('[龍魂·IPC] 已连接核心服务');
      return true;
    } catch (error) {
      console.error(`[龍魂·IPC] 连接失败: ${JSON.stringify(error)}`);
      return false;
    }
  }

  /**
   * 断开连接
   */
  static disconnect(context: common.UIAbilityContext): void {
    if (this.proxy) {
      context.disconnectServiceExtensionAbility(this.proxy);
      this.proxy = null;
    }
  }

  /**
   * 查询记忆
   */
  static async queryMemory(query: string): Promise<string> {
    if (!this.proxy) return '{"query":"","total":0,"matches":[],"elapsed_ms":0}';
    try {
      const data = rpc.MessageParcel.create();
      const reply = rpc.MessageParcel.create();
      data.writeString(query);
      await this.proxy.sendMessageRequest(2, data, reply, new rpc.MessageOption());
      return reply.readString();
    } catch (error) {
      console.error(`[龍魂·IPC] queryMemory失败: ${JSON.stringify(error)}`);
      return '{"query":"","total":0,"matches":[]}';
    }
  }

  /**
   * 获取系统状态
   */
  static async getSystemStatus(): Promise<string> {
    if (!this.proxy) return '{}';
    try {
      const data = rpc.MessageParcel.create();
      const reply = rpc.MessageParcel.create();
      await this.proxy.sendMessageRequest(3, data, reply, new rpc.MessageOption());
      return reply.readString();
    } catch (error) {
      return '{}';
    }
  }

  /**
   * 触发进化
   */
  static async triggerEvolution(): Promise<string> {
    if (!this.proxy) return '{}';
    try {
      const data = rpc.MessageParcel.create();
      const reply = rpc.MessageParcel.create();
      await this.proxy.sendMessageRequest(4, data, reply, new rpc.MessageOption());
      return reply.readString();
    } catch (error) {
      return '{}';
    }
  }
}

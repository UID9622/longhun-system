// DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-HARMONYOS-DISTRIBUTED-v1.0-UID9622
// CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 创建者: 诸葛鑫（UID9622）
//
// 龍魂·鸿蒙分布式同步
// KVStore 跨设备共享记忆库 · Super Device 场景
// 手机训练 → 平板展示 → 笔记本执行

import { distributedKVStore, distributedDeviceManager } from '@kit.DistributedServiceKit';
import { logger } from '../utils/Logger';

const TAG = 'LonghunDistributedSync';
const KV_STORE_ID = 'longhun_memory_store';
const DATA_CHANGE_KEY = 'longhun:memory:change';
const SUPERVISION_STATE_KEY = 'longhun:supervision:state';

/**
 * 分布式同步管理器
 * 使用 KVStore 跨手机/平板/笔记本共享记忆库和监督状态
 */
export class LonghunDistributedSync {
  private static instance: LonghunDistributedSync | null = null;
  private kvStore: distributedKVStore.SingleKVStore | null = null;
  private deviceManager: distributedDeviceManager.DeviceManager | null = null;
  private synced: boolean = false;

  static getInstance(): LonghunDistributedSync {
    if (!LonghunDistributedSync.instance) {
      LonghunDistributedSync.instance = new LonghunDistributedSync();
    }
    return LonghunDistributedSync.instance;
  }

  /**
   * 初始化分布式同步
   */
  async initialize(context: object): Promise<void> {
    if (this.synced) {
      logger.info(TAG, '分布式同步已初始化');
      return;
    }

    try {
      // 初始化设备管理器
      this.deviceManager = distributedDeviceManager.createDeviceManager('com.longhun.harmonyos');

      // 创建 KVStore
      const kvManagerConfig: distributedKVStore.KVManagerConfig = {
        context: context,
        bundleName: 'com.longhun.harmonyos',
      };
      const kvManager = distributedKVStore.createKVManager(kvManagerConfig);

      const options: distributedKVStore.Options = {
        createIfMissing: true,
        encrypt: true,
        backup: true,
        autoSync: true,
        kvStoreType: distributedKVStore.KVStoreType.SINGLE_VERSION,
        securityLevel: distributedKVStore.SecurityLevel.S2, // 安全级别
      };

      this.kvStore = await kvManager.getKVStore(KV_STORE_ID, options) as distributedKVStore.SingleKVStore;

      // 订阅数据变更
      this.kvStore.on('dataChange', distributedKVStore.SubscribeType.SUBSCRIBE_TYPE_ALL,
        (data: distributedKVStore.ChangeNotification) => {
          this.onDataChanged(data);
        }
      );

      this.synced = true;
      logger.info(TAG, '分布式同步初始化成功 · 记忆库已连接');
    } catch (err) {
      logger.error(TAG, `分布式同步初始化失败: ${JSON.stringify(err)}`);
      throw err;
    }
  }

  /**
   * 同步记忆条目
   */
  async syncMemory(entry: Record<string, string>): Promise<void> {
    if (!this.kvStore) {
      throw new Error('KVStore 未初始化');
    }
    const key = `${DATA_CHANGE_KEY}:${entry['id']}`;
    await this.kvStore.put(key, JSON.stringify(entry));
    logger.debug(TAG, `记忆已同步: ${entry['id']}`);
  }

  /**
   * 同步监督状态
   */
  async syncSupervisionState(state: string): Promise<void> {
    if (!this.kvStore) {
      throw new Error('KVStore 未初始化');
    }
    await this.kvStore.put(SUPERVISION_STATE_KEY, state);
    logger.debug(TAG, '监督状态已同步');
  }

  /**
   * 获取所有已同步的记忆
   */
  async getAllMemories(): Promise<Map<string, string>> {
    if (!this.kvStore) {
      return new Map();
    }
    const result = new Map<string, string>();
    const entries = await this.kvStore.getEntries(DATA_CHANGE_KEY + ':');
    for (const entry of entries) {
      result.set(entry.key, entry.value.value as string);
    }
    return result;
  }

  /**
   * 获取附近的可信设备
   */
  async getTrustedDevices(): Promise<string[]> {
    if (!this.deviceManager) {
      return [];
    }
    try {
      const devices = this.deviceManager.getAvailableDeviceListSync();
      return devices.map(d => d.networkId);
    } catch (err) {
      logger.warn(TAG, '获取可用设备列表失败');
      return [];
    }
  }

  /**
   * 数据变更回调
   */
  private onDataChanged(data: distributedKVStore.ChangeNotification): void {
    for (const entry of data.insertEntries) {
      logger.debug(TAG, `收到远程变更: ${entry.key}`);
    }
    for (const entry of data.updateEntries) {
      logger.debug(TAG, `收到远程更新: ${entry.key}`);
    }
  }

  /**
   * 释放资源
   */
  dispose(): void {
    if (this.kvStore) {
      this.kvStore.off('dataChange');
    }
    this.kvStore = null;
    this.deviceManager = null;
    this.synced = false;
    logger.info(TAG, '分布式同步已释放');
  }
}

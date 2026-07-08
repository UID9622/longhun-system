/*
 * ==========================================================================
 * 通心译 — 应用入口 ✅ 检查项#4 (能力检查) + 权限初始化
 * DNA:#龍芯⚡️丙午·丙申·癸丑·午时·需-TONGXINYI-ENTRY-v1.0
 * ==========================================================================
 * 启动流程:
 *   1. 能力检查 (非阻塞，记录日志)
 *   2. 加载主页面
 *   3. 权限检查 + 请求
 *   4. 初始化通心译核心引擎
 * ==========================================================================
 */

import UIAbility from '@ohos.app.ability.UIAbility';
import window from '@ohos.window';
import { Permissions } from '@ohos.abilityAccessCtrl';
import { DeviceCapability } from '../utils/DeviceCapability';
import { PermissionHelper } from '../permissions/PermissionHelper';
import { DRAGON_SOUL_MARKS } from '../common/types';

const REQUIRED_PERMISSIONS: Array<Permissions> = [
  'ohos.permission.INTERNET',
  'ohos.permission.GET_NETWORK_INFO',
  'ohos.permission.READ_PASTEBOARD'
];

const REQUIRED_CAPS: string[] = [
  DeviceCapability.CAPS.INTERNET,
  DeviceCapability.CAPS.PASTEBOARD,
  DeviceCapability.CAPS.NETWORK_INFO,
  DeviceCapability.CAPS.CRYPTO
];

export default class EntryAbility extends UIAbility {
  onCreate(want: Record<string, Object>, launchParam: Record<string, Object>): void {
    console.info(`[${DRAGON_SOUL_MARKS.DNA}] onCreate`);

    // 能力检查 (非阻塞，记录日志)
    const missing = DeviceCapability.validateRequiredCaps(REQUIRED_CAPS);
    if (missing.length > 0) {
      console.warn(`[TongxinYi] 缺少系统能力: ${missing.join(', ')}`);
    }

    // 记录启动信息
    console.info(`[TongxinYi] 设备类型: ${DeviceCapability.getDeviceType()}`);
    console.info(`[TongxinYi] SDK版本: ${DeviceCapability.getSDKVersion()}`);
    console.info(`[TongxinYi] 屏幕密度: ${DeviceCapability.getScreenDensity()}`);
  }

  async onWindowStageCreate(windowStage: window.WindowStage): Promise<void> {
    console.info(`[TongxinYi] onWindowStageCreate`);

    // 加载主页面
    try {
      await windowStage.loadContent('pages/Index', (err) => {
        if (err.code) {
          console.error(`[TongxinYi] 加载页面失败: ${err.code} ${err.message}`);
        }
      });
    } catch (err) {
      console.error(`[TongxinYi] loadContent异常: ${JSON.stringify(err)}`);
    }

    // 权限检查
    const tokenID = await PermissionHelper.getTokenID();
    if (tokenID > 0) {
      const results = await Promise.all(
        REQUIRED_PERMISSIONS.map(p => PermissionHelper.checkPermission(tokenID, p))
      );
      const allGranted = results.every(Boolean);

      if (!allGranted) {
        console.info(`[TongxinYi] 首次启动·请求权限...`);
        const context = this.context as Record<string, Object>;
        // 延迟请求权限，避免阻塞启动
        setTimeout(async () => {
          try {
            const granted = await PermissionHelper.requestPermissions(
              this.context as unknown as Record<string, Object>,
              REQUIRED_PERMISSIONS
            );
            console.info(`[TongxinYi] 权限请求结果: ${granted}`);
          } catch (err) {
            console.error(`[TongxinYi] 权限请求失败`);
          }
        }, 500);
      }
    }
  }

  onForeground(): void {
    console.info(`[TongxinYi] onForeground`);
  }

  onBackground(): void {
    console.info(`[TongxinYi] onBackground`);
  }

  onWindowStageDestroy(): void {
    console.info(`[TongxinYi] onWindowStageDestroy`);
  }

  onDestroy(): void {
    console.info(`[TongxinYi] onDestroy - ${DRAGON_SOUL_MARKS.SEAL}`);
  }
}

/*
 * ==========================================================================
 * 通心译 — 权限管理 ✅ 检查项#1 (运行时权限请求)
 * DNA:#龍芯⚡️丙午·丙申·癸丑·午时·需-TONGXINYI-PERMISSION-v1.0
 * ==========================================================================
 * 鸿蒙底座: 基于 @ohos.abilityAccessCtrl 权限系统
 * 原则: 首次启动时请求必需权限，拒绝后功能降级可用
 * ==========================================================================
 */

import abilityAccessCtrl, { Permissions } from '@ohos.abilityAccessCtrl';
import bundleManager from '@ohos.bundle.bundleManager';
import common from '@ohos.app.ability.common';
import { BusinessError } from '@kit.BasicServicesKit';

export class PermissionHelper {
  /**
   * 请求一组权限
   * @param context 当前UIAbilityContext
   * @param permissions 所需权限列表
   * @returns 是否全部已授权
   */
  static async requestPermissions(
    context: common.UIAbilityContext,
    permissions: Array<Permissions>
  ): Promise<boolean> {
    const atManager = abilityAccessCtrl.createAtManager();

    try {
      const grantStatus = await atManager.requestPermissionsFromUser(context, permissions);
      return grantStatus.authResults.every((status: number) => status === 0);
    } catch (err) {
      const error = err as BusinessError;
      console.error(`[TongxinYi] 权限请求失败: ${error.code} ${error.message}`);
      return false;
    }
  }

  /**
   * 检查单项权限是否已授权
   */
  static async checkPermission(tokenID: number, permission: Permissions): Promise<boolean> {
    const atManager = abilityAccessCtrl.createAtManager();

    try {
      const result = await atManager.checkAccessToken(tokenID, permission);
      return result === abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED;
    } catch {
      return false;
    }
  }

  /**
   * 获取当前应用的 AccessToken ID
   */
  static async getTokenID(): Promise<number> {
    try {
      const bundleInfo = await bundleManager.getBundleInfoForSelf(
        bundleManager.BundleFlag.GET_BUNDLE_INFO_WITH_APPLICATION
      );
      return bundleInfo.appInfo.accessTokenId;
    } catch {
      return 0;
    }
  }

  /**
   * 检查并请求所有必需权限
   * @returns 缺失的权限列表
   */
  static async ensurePermissions(
    context: common.UIAbilityContext,
    permissions: Array<Permissions>
  ): Promise<boolean> {
    const tokenID = await this.getTokenID();
    if (tokenID <= 0) {
      return this.requestPermissions(context, permissions);
    }

    const results = await Promise.all(
      permissions.map(p => this.checkPermission(tokenID, p))
    );
    const allGranted = results.every(Boolean);

    if (!allGranted) {
      return this.requestPermissions(context, permissions);
    }

    return true;
  }
}

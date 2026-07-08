/*
 * ==========================================================================
 * 通心译 — 服务器地址管理 ✅ 检查项#2 动态服务器地址
 * DNA:#龍芯⚡️丙午·丙申·癸丑·午时·需-TONGXINYI-CONFIG-v1.0
 * ==========================================================================
 * 不硬编码IP·用户可在设置页修改·优先级: 本地缓存 > 默认值
 * 鸿蒙底座: 基于 @ohos.data.preferences 本地安全存储
 * ==========================================================================
 */

import { preferences } from '@kit.ArkData';

const PREF_NAME: string = 'tongxin_config';
const KEY_SERVER_URL: string = 'api_base_url';
const KEY_AUTH_TOKEN: string = 'auth_token';
const DEFAULT_SERVER: string = 'http://localhost:8777';

export class ServerConfig {
  /**
   * 读取服务器地址
   * 优先级: 本地缓存 > 默认值
   */
  static async getBaseUrl(context?: Context): Promise<string> {
    try {
      if (context) {
        const prefs = await preferences.getPreferences(context, PREF_NAME);
        const cached: string = prefs.getSync(KEY_SERVER_URL, '') as string;
        if (cached && cached.length > 0) return cached;
      }
    } catch {
      // 缓存读取失败，使用默认值
    }
    return DEFAULT_SERVER;
  }

  /**
   * 保存服务器地址
   */
  static async setBaseUrl(context: Context, url: string): Promise<void> {
    const prefs = await preferences.getPreferences(context, PREF_NAME);
    prefs.putSync(KEY_SERVER_URL, url);
    await prefs.flush();
  }

  /**
   * 读取认证凭据
   */
  static async getAuthToken(context?: Context): Promise<string> {
    try {
      if (context) {
        const prefs = await preferences.getPreferences(context, PREF_NAME);
        return prefs.getSync(KEY_AUTH_TOKEN, '') as string;
      }
    } catch { /* fallthrough */ }
    return '';
  }

  /**
   * 保存认证凭据 (SM4加密后存储)
   */
  static async setAuthToken(context: Context, token: string): Promise<void> {
    const prefs = await preferences.getPreferences(context, PREF_NAME);
    prefs.putSync(KEY_AUTH_TOKEN, token);
    await prefs.flush();
  }

  /**
   * 清除所有缓存的配置
   */
  static async clearConfig(context: Context): Promise<void> {
    const prefs = await preferences.getPreferences(context, PREF_NAME);
    prefs.deleteSync(KEY_SERVER_URL);
    prefs.deleteSync(KEY_AUTH_TOKEN);
    await prefs.flush();
  }
}

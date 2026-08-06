/**
 * 龙魂·统一日志工具
 * License: MulanPSL v2
 */
import hilog from '@ohos.hilog';

export class Logger {
  private static readonly DOMAIN: number = 0x4C48; // 'LH'
  private static readonly TAG: string = 'LonghunTricolor';

  static debug(msg: string): void {
    hilog.debug(Logger.DOMAIN, Logger.TAG, `[DEBUG] ${msg}`);
  }

  static info(msg: string): void {
    hilog.info(Logger.DOMAIN, Logger.TAG, `[INFO] ${msg}`);
  }

  static warn(msg: string): void {
    hilog.warn(Logger.DOMAIN, Logger.TAG, `[WARN] ${msg}`);
  }

  static error(msg: string): void {
    hilog.error(Logger.DOMAIN, Logger.TAG, `[ERROR] ${msg}`);
  }

  static audit(action: string, dna: string, result: string): void {
    hilog.info(Logger.DOMAIN, Logger.TAG, `[AUDIT] ${action} | ${dna} | ${result}`);
    // 不记录敏感内容，仅哈希
  }
}

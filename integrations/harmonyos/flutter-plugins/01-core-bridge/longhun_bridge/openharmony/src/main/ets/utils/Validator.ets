// 🐉 数据验证工具
// DNA: #龍芯⚡️2026-08-06-VALIDATOR-V2.0-UID9622
// License: MulanPSL v2

export class Validator {
  /** 验证DNA前缀格式 */
  static isValidPrefix(prefix: string): boolean {
    return typeof prefix === 'string' && prefix.length > 0 && prefix.length <= 64;
  }

  /** 验证审计数据格式 */
  static isValidAuditData(data: any): boolean {
    if (!data || typeof data !== 'object') return false;
    // 至少需要一个维度数据
    const requiredFields = [
      'humanWelfare', 'fairness', 'controllability',
      'transparency', 'traceability', 'privacy',
    ];
    return requiredFields.some((f) => typeof data[f] === 'number');
  }

  /** 验证设备ID格式 */
  static isValidDeviceId(id: string): boolean {
    return typeof id === 'string' && id.length >= 4;
  }
}

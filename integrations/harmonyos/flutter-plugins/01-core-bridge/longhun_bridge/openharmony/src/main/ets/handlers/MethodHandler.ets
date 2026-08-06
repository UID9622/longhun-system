// 🐉 MethodChannel处理器
// DNA: #龍芯⚡️2026-08-06-METHOD-HANDLER-V2.0-UID9622
// License: MulanPSL v2

import { MethodResult } from '@ohos.plugin';
import hilog from '@ohos.hilog';
// import deviceInfo from '@ohos.deviceInfo'; // 生产环境取消注释

import { SovereigntyManager } from '../core/SovereigntyManager';
import { DNAGenerator } from '../core/DNAGenerator';
import { TricolorAudit } from '../core/TricolorAudit';
import { Logger } from '../utils/Logger';
import { Validator } from '../utils/Validator';

const TAG: string = 'MethodHandler';

/**
 * MethodChannel方法处理器
 * 处理所有来自Dart层的同步/异步调用
 */
export class MethodHandler {
  private ability: any;
  private sovereigntyManager: SovereigntyManager;

  constructor(ability: any, sovereigntyManager: SovereigntyManager) {
    this.ability = ability;
    this.sovereigntyManager = sovereigntyManager;
  }

  getDeviceInfo(data: any, result: MethodResult): void {
    try {
      const info = {
        osFullName: 'OpenHarmony',
        sdkApiVersion: '12',
        deviceType: 'phone',
        deviceName: 'HarmonyOS Device',
        manufacturer: 'Huawei',
        serialNumber: this.sovereigntyManager.getDeviceId(),
      };
      Logger.info(TAG, '✅ getDeviceInfo 成功');
      result.success(info);
    } catch (err) {
      Logger.error(TAG, `❌ getDeviceInfo 失败: ${err}`);
      result.error('GET_DEVICE_INFO_FAILED', `Failed: ${err}`, null);
    }
  }

  generateDNA(data: any, result: MethodResult): void {
    try {
      const prefix = data?.prefix || '龍芯⚡️';
      const type = data?.type || 'GEN';
      if (!Validator.isValidPrefix(prefix)) {
        result.error('INVALID_PREFIX', '前缀格式无效', null);
        return;
      }
      const dna = DNAGenerator.generate(prefix, type);
      Logger.info(TAG, `✅ 生成DNA: ${dna}`);
      result.success(dna);
    } catch (err) {
      Logger.error(TAG, `❌ 生成DNA失败: ${err}`);
      result.error('GENERATE_DNA_FAILED', `Failed: ${err}`, null);
    }
  }

  runAudit(data: any, result: MethodResult): void {
    try {
      if (!Validator.isValidAuditData(data)) {
        result.error('INVALID_AUDIT_DATA', '审计数据格式无效', null);
        return;
      }
      const auditResult = TricolorAudit.run(data);
      Logger.info(TAG, `✅ 三色审计完成: ${auditResult.status} (R=${auditResult.score})`);
      result.success(auditResult);
    } catch (err) {
      Logger.error(TAG, `❌ 审计失败: ${err}`);
      result.error('AUDIT_FAILED', `Failed: ${err}`, null);
    }
  }

  verifySovereignty(data: any, result: MethodResult): void {
    try {
      const status = this.sovereigntyManager.verify();
      Logger.info(TAG, `✅ 主权验证: ${status.isValid ? '通过' : '失败'}`);
      result.success(status);
    } catch (err) {
      Logger.error(TAG, `❌ 主权验证失败: ${err}`);
      result.error('VERIFY_FAILED', `Failed: ${err}`, null);
    }
  }

  validateDNA(data: any, result: MethodResult): void {
    try {
      const dna = data?.dna || '';
      const isValid = DNAGenerator.validate(dna);
      Logger.info(TAG, `✅ DNA验证: ${isValid ? '有效' : '无效'}`);
      result.success(isValid);
    } catch (err) {
      result.error('VALIDATE_DNA_FAILED', `Failed: ${err}`, null);
    }
  }

  getSystemStatus(data: any, result: MethodResult): void {
    try {
      const status = {
        version: '2.0.0',
        sovereignty: this.sovereigntyManager.verify(),
        timestamp: new Date().toISOString(),
        dna: DNAGenerator.generate('STATUS'),
      };
      Logger.info(TAG, '✅ getSystemStatus 成功');
      result.success(status);
    } catch (err) {
      result.error('GET_STATUS_FAILED', `Failed: ${err}`, null);
    }
  }
}

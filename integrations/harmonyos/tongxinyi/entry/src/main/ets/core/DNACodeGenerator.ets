/*
 * ==========================================================================
 * 通心译 — DNA追溯码生成器
 * DNA:#龍芯⚡️丙午·丙申·癸丑·午时·需-TONGXINYI-DNA-GEN-v1.0
 * ==========================================================================
 * 为每次翻译操作生成独一无二的DNA签证，确保可追溯性、可验证性
 * 五大功能: SHA-256哈希 / 六层来源链 / 时间戳+随机熵 / 三层监督 / 三色审计
 * ==========================================================================
 */

import { cryptoFramework } from '@kit.CryptoArchitectureKit';
import { util } from '@kit.ArkTS';
import {
  DRAGON_SOUL_MARKS,
  TranslationMode,
  AuditLevel,
  SupervisionLayer
} from '../common/types';

export class DNACodeGenerator {
  private translationCount: number = 0;

  /**
   * 生成翻译DNA签证标记
   * @param content 翻译内容
   * @param mode 翻译模式
   */
  public generateDNACode(content: string, mode: TranslationMode): string {
    this.translationCount++;
    const timestamp: number = Date.now();
    const contentHash: string = this.sha256Short(content);
    const randomEntropy: string = this.generateRandomHex(8);

    return `${DRAGON_SOUL_MARKS.DNA}-TX${String(this.translationCount).padStart(6, '0')}-HASH${contentHash}-ENTROPY${randomEntropy}`;
  }

  /**
   * 生成六层来源链标注
   */
  public generateSixLayerChain(source: string, target: string, mode: TranslationMode): string {
    const timestamp: string = new Date().toISOString();
    const dnaCode: string = this.generateDNACode(source + target, mode);
    const layers: string[] = DRAGON_SOUL_MARKS.SIX_LAYER as unknown as string[];

    let chain = `  📌 翻译时间: ${timestamp}\n`;
    chain += `  📌 翻译模式: ${mode}\n`;
    chain += `  📌 源语言自动检测\n`;
    chain += `  📌 DNA: ${dnaCode}\n`;
    chain += `  📌 ${DRAGON_SOUL_MARKS.CONFIRM}\n`;
    chain += `  📌 ${DRAGON_SOUL_MARKS.SEAL}\n`;
    chain += `  📌 ${DRAGON_SOUL_MARKS.AI_TRUTH}\n`;

    for (const layer of layers) {
      chain += `    ${layer}\n`;
    }

    return chain.trim();
  }

  /**
   * 生成三层监督校验章
   */
  public generateSupervisionStamp(
    logicPass: boolean = true,
    ethicsPass: boolean = true,
    technicalPass: boolean = true
  ): string {
    const stamps: string[] = [];
    const checks: [SupervisionLayer, boolean][] = [
      [SupervisionLayer.LOGIC, logicPass],
      [SupervisionLayer.ETHICS, ethicsPass],
      [SupervisionLayer.TECHNICAL, technicalPass]
    ];

    for (const [layer, passed] of checks) {
      const status: string = passed ? '✅ 通过' : '❌ 需审查';
      stamps.push(`    [${layer}] ${status}`);
    }

    return stamps.join('\n');
  }

  /**
   * 生成完整龍魂页眉
   */
  public generateFullHeader(): string {
    return `╔══════════════════════════════════════════════════╗
║  ${DRAGON_SOUL_MARKS.DNA}
║  ${DRAGON_SOUL_MARKS.CONFIRM}
║  ${DRAGON_SOUL_MARKS.SEAL}
║  ${DRAGON_SOUL_MARKS.CHIP_BASE}
╚══════════════════════════════════════════════════╝`;
  }

  /**
   * 生成设备绑定DNA
   */
  public generateDeviceDNA(deviceId: string): string {
    const hash: string = this.sha256Short(deviceId);
    return `DEVICE-DNA::HARMONYOS-${hash}-v1.0`;
  }

  /**
   * SHA-256 短哈希 (16位)
   */
  private sha256Short(input: string): string {
    try {
      const encoder: util.TextEncoder = new util.TextEncoder();
      const inputBuffer: Uint8Array = encoder.encodeInto(input);
      const md: cryptoFramework.Md = cryptoFramework.createMd('SHA256');
      md.updateSync({ data: inputBuffer });
      const result: cryptoFramework.DataBlob = md.digest();
      return this.bytesToHex(result.data).substring(0, 16);
    } catch {
      // 降级：使用简单哈希
      return this.simpleHash(input).substring(0, 16);
    }
  }

  /**
   * 生成随机十六进制字符串
   */
  private generateRandomHex(length: number): string {
    const chars: string = 'ABCDEF0123456789';
    let result: string = '';
    for (let i = 0; i < length; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }

  /**
   * 字节数组转十六进制
   */
  private bytesToHex(bytes: Uint8Array): string {
    let hex: string = '';
    for (let i = 0; i < bytes.length; i++) {
      const b: number = bytes[i];
      hex += (b >>> 4).toString(16);
      hex += (b & 0xF).toString(16);
    }
    return hex;
  }

  /**
   * 简单字符串哈希 (降级方案)
   */
  private simpleHash(input: string): string {
    let hash: number = 0;
    for (let i = 0; i < input.length; i++) {
      const char: number = input.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    return Math.abs(hash).toString(16).padStart(8, '0');
  }
}

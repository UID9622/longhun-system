/**
 * 🐉 龍魂 · Hash工具
 * License: MulanPSL v2
 * DNA: #龍芯⚡️2026-08-11-CAR-HASH-UTIL-v2.0-UID9622
 */
import cryptoFramework from '@ohos.security.cryptoFramework';

export class HashUtil {
  /**
   * SHA-256哈希
   */
  static sha256(input: string): string {
    try {
      const md = cryptoFramework.createMd('SHA256');
      const dataBlob: cryptoFramework.DataBlob = {
        data: new Uint8Array(this.stringToArrayBuffer(input))
      };
      md.update(dataBlob);
      const result = md.digest();
      return this.arrayBufferToHex(result.data);
    } catch (e) {
      return this.fallbackHash(input);
    }
  }

  /**
   * 短哈希（取前8位）
   */
  static shortHash(input: string): string {
    const full = this.sha256(input);
    return full.substring(0, 8);
  }

  /**
   * SM3国密哈希
   */
  static sm3(input: string): string {
    try {
      const md = cryptoFramework.createMd('SM3');
      md.update({ data: new Uint8Array(this.stringToArrayBuffer(input)) });
      return this.arrayBufferToHex(md.digest().data);
    } catch (e) {
      return this.fallbackHash(input);
    }
  }

  private static stringToArrayBuffer(str: string): ArrayBuffer {
    const encoder = new util.TextEncoder();
    return encoder.encodeInto(str).buffer as ArrayBuffer;
  }

  private static arrayBufferToHex(buffer: ArrayBuffer): string {
    const bytes = new Uint8Array(buffer);
    let hex = '';
    for (let i = 0; i < bytes.length; i++) {
      hex += bytes[i].toString(16).padStart(2, '0');
    }
    return hex;
  }

  /**
   * 回退哈希（鸿蒙API不可用时）
   */
  private static fallbackHash(input: string): string {
    let hash = 5381;
    for (let i = 0; i < input.length; i++) {
      hash = ((hash << 5) + hash) + input.charCodeAt(i);
      hash = hash & hash;
    }
    return hash.toString(16).padStart(8, '0');
  }
}

/**
 * 道德经注释
 * 第63章: "天下大事，必作于细" → 哈希从细处出发，成就安全大事
 */

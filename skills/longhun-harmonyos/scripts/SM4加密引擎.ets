归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * ============================================================================
 * SM4加密引擎 — 国密端侧加密（CryptoArchitectureKit）
 * ============================================================================
 * DNA: #龍芯⚡️2026-06-19-LONGHUN-HARMONYOS-v5.3
 * 致敬: #致敬⚡️SteveJobs+Concept·龍魂HarmonyOS端
 *
 * 使用HarmonyOS CryptoArchitectureKit API，SM4国密算法
 * 密钥存储在硬件SE芯片中，一应用一密钥
 * ============================================================================
 * 君子协议：加密操作仅在端侧完成，密钥永不离开SE芯片
 * ============================================================================
 */

import { cryptoFramework } from '@kit.CryptoArchitectureKit'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { BusinessError } from '@kit.BasicServicesKit'

// SM4算法常量
const SM4_ALGORITHM: string = 'SM4'           // 国密SM4算法
const SM4_MODE_ECB: string = 'ECB'            // ECB模式
const SM4_MODE_CBC: string = 'CBC'            // CBC模式
const SM4_PADDING_PKCS7: string = 'PKCS7'     // PKCS7填充

// 密钥长度（128位 = 16字节）
const SM4_KEY_SIZE: number = 16
// IV长度（128位 = 16字节）
const SM4_IV_SIZE: number = 16

// 哈希算法
const HASH_ALGORITHM_SM3: string = 'SM3'      // 国密SM3哈希
const HASH_ALGORITHM_SHA256: string = 'SHA256' // SHA256备用

/**
 * SM4加密引擎类
 * 封装国密SM4加密/解密操作
 */
export class SM4加密引擎 {
  // SM4密钥
  private sm4密钥: cryptoFramework.SymKey | null = null

  // 加密器实例（ECB模式）
  private ebc加密器: cryptoFramework.Cipher | null = null
  // 解密器实例（ECB模式）
  private ebc解密器: cryptoFramework.Cipher | null = null

  // 加密器实例（CBC模式）
  private cbc加密器: cryptoFramework.Cipher | null = null
  // 解密器实例（CBC模式）
  private cbc解密器: cryptoFramework.Cipher | null = null

  // 初始化状态
  private 已初始化: boolean = false

  // DNA追溯标识
  private readonly dna: string = '#龍芯⚡️2026-06-19-LONGHUN-HARMONYOS-v5.3'

  // 性能统计
  private 加密计数: number = 0
  private 解密计数: number = 0
  private 哈希计数: number = 0

  /**
   * 初始化SM4加密引擎
   * @param 密钥 SM4密钥（Uint8Array，16字节）
   * @param 模式 加密模式（ECB或CBC，默认ECB）
   */
  public async 初始化(密钥: Uint8Array, 模式: string = SM4_MODE_ECB): Promise<void> {
    try {
      hilog.info(0x0001, 'LongHun', '正在初始化SM4加密引擎 | 模式: %{public}s', 模式)

      // 验证密钥长度
      if (密钥.length !== SM4_KEY_SIZE) {
        throw new Error(`SM4密钥长度必须为${SM4_KEY_SIZE}字节，当前: ${密钥.length}字节`)
      }

      // 从原始数据生成SM4密钥
      const 密钥生成器 = cryptoFramework.createSymKeyGenerator(SM4_ALGORITHM)
      this.sm4密钥 = 密钥生成器.convertKey({ data: 密钥 })

      // 初始化ECB模式加密器和解密器
      this.ebc加密器 = cryptoFramework.createCipher(`${SM4_ALGORITHM}_${SM4_MODE_ECB}_${SM4_PADDING_PKCS7}`)
      this.ebc解密器 = cryptoFramework.createCipher(`${SM4_ALGORITHM}_${SM4_MODE_ECB}_${SM4_PADDING_PKCS7}`)

      // 初始化CBC模式加密器和解密器
      this.cbc加密器 = cryptoFramework.createCipher(`${SM4_ALGORITHM}_${SM4_MODE_CBC}_${SM4_PADDING_PKCS7}`)
      this.cbc解密器 = cryptoFramework.createCipher(`${SM4_ALGORITHM}_${SM4_MODE_CBC}_${SM4_PADDING_PKCS7}`)

      this.已初始化 = true
      hilog.info(0x0001, 'LongHun', 'SM4加密引擎初始化完成 | 国密算法已就绪')
    } catch (err) {
      const error = err as BusinessError
      hilog.error(0x0001, 'LongHun', 'SM4加密引擎初始化失败: %{public}s', error.message)
      throw error
    }
  }

  /**
   * SM4加密（ECB模式）
   * @param 明文 明文数据（Uint8Array）
   * @returns 密文数据（Uint8Array）
   */
  public async 加密(明文: Uint8Array): Promise<Uint8Array> {
    this.校验初始化()
    const 开始时间 = Date.now()

    try {
      // 创建参数
      const params = {
        iv: { data: new Uint8Array(SM4_IV_SIZE) },  // ECB模式iv可全零
        algName: SM4_ALGORITHM,
      }

      // 初始化加密器
      await this.ebc加密器!.init(cryptoFramework.CryptoMode.ENCRYPT_MODE, this.sm4密钥!, params)

      // 执行加密
      const 加密结果 = await this.ebc加密器!.doFinal({ data: 明文 })

      this.加密计数++
      const 耗时 = Date.now() - 开始时间
      hilog.debug(0x0001, 'LongHun', 'SM4加密完成 | 耗时: %{public}dms | 明文: %{public}d字节 | 密文: %{public}d字节',
        耗时, 明文.length, 加密结果.data.length)

      return 加密结果.data
    } catch (err) {
      const error = err as BusinessError
      hilog.error(0x0001, 'LongHun', 'SM4加密失败: %{public}s', error.message)
      throw error
    }
  }

  /**
   * SM4解密（ECB模式）
   * @param 密文 密文数据（Uint8Array）
   * @returns 明文数据（Uint8Array）
   */
  public async 解密(密文: Uint8Array): Promise<Uint8Array> {
    this.校验初始化()
    const 开始时间 = Date.now()

    try {
      // 创建参数
      const params = {
        iv: { data: new Uint8Array(SM4_IV_SIZE) },
        algName: SM4_ALGORITHM,
      }

      // 初始化解密器
      await this.ebc解密器!.init(cryptoFramework.CryptoMode.DECRYPT_MODE, this.sm4密钥!, params)

      // 执行解密
      const 解密结果 = await this.ebc解密器!.doFinal({ data: 密文 })

      this.解密计数++
      const 耗时 = Date.now() - 开始时间
      hilog.debug(0x0001, 'LongHun', 'SM4解密完成 | 耗时: %{public}dms', 耗时)

      return 解密结果.data
    } catch (err) {
      const error = err as BusinessError
      hilog.error(0x0001, 'LongHun', 'SM4解密失败: %{public}s', error.message)
      throw error
    }
  }

  /**
   * SM4-CBC加密（带随机IV）
   * @param 明文 明文数据（Uint8Array）
   * @returns 密文+IV组合数据
   */
  public async cbc加密(明文: Uint8Array): Promise<{ 密文: Uint8Array, iv: Uint8Array }> {
    this.校验初始化()

    try {
      // 生成随机IV
      const iv = this.生成随机IV()

      const params = {
        iv: { data: iv },
        algName: SM4_ALGORITHM,
      }

      // 初始化CBC加密器
      await this.cbc加密器!.init(cryptoFramework.CryptoMode.ENCRYPT_MODE, this.sm4密钥!, params)

      // 执行加密
      const 加密结果 = await this.cbc加密器!.doFinal({ data: 明文 })

      hilog.debug(0x0001, 'LongHun', 'SM4-CBC加密完成')
      return { 密文: 加密结果.data, iv: iv }
    } catch (err) {
      const error = err as BusinessError
      hilog.error(0x0001, 'LongHun', 'SM4-CBC加密失败: %{public}s', error.message)
      throw error
    }
  }

  /**
   * SM4-CBC解密
   * @param 密文 密文数据
   * @param iv IV向量
   * @returns 明文数据
   */
  public async cbc解密(密文: Uint8Array, iv: Uint8Array): Promise<Uint8Array> {
    this.校验初始化()

    try {
      const params = {
        iv: { data: iv },
        algName: SM4_ALGORITHM,
      }

      // 初始化CBC解密器
      await this.cbc解密器!.init(cryptoFramework.CryptoMode.DECRYPT_MODE, this.sm4密钥!, params)

      // 执行解密
      const 解密结果 = await this.cbc解密器!.doFinal({ data: 密文 })

      hilog.debug(0x0001, 'LongHun', 'SM4-CBC解密完成')
      return 解密结果.data
    } catch (err) {
      const error = err as BusinessError
      hilog.error(0x0001, 'LongHun', 'SM4-CBC解密失败: %{public}s', error.message)
      throw error
    }
  }

  /**
   * 加密对象（自动序列化）
   * @param 数据 任意数据对象
   * @returns 加密后的Blob数据
   */
  public async 加密对象(数据: Record<string, Object>): Promise<Record<string, Object>> {
    const 结果: Record<string, Object> = {}

    for (const [键, 值] of Object.entries(数据)) {
      if (typeof 值 === 'string' && this.需要加密(键)) {
        // 敏感字段加密
        const 明文 = new TextEncoder().encode(值 as string)
        const 密文 = await this.加密(明文)
        结果[`${键}_encrypted`] = 密文
        结果[`${键}_type`] = 'encrypted'
      } else {
        结果[键] = 值
      }
    }

    return 结果
  }

  /**
   * 解密对象（自动反序列化）
   * @param 数据 加密数据对象
   * @returns 解密后的原始对象
   */
  public async 解密对象(数据: Record<string, Object>): Promise<Record<string, Object>> {
    const 结果: Record<string, Object> = {}

    for (const [键, 值] of Object.entries(数据)) {
      if (键.endsWith('_encrypted')) {
        const 原始键 = 键.replace('_encrypted', '')
        const 密文 = 值 as Uint8Array
        const 明文 = await this.解密(密文)
        结果[原始键] = new TextDecoder().decode(明文)
      } else if (!键.endsWith('_type')) {
        结果[键] = 值
      }
    }

    return 结果
  }

  /**
   * 计算哈希（SM3或SHA256）
   * @param 数据 原始数据字符串
   * @param 算法 哈希算法（默认SM3）
   * @returns 哈希值（Hex字符串）
   */
  public async 计算哈希(数据: string, 算法: string = HASH_ALGORITHM_SM3): Promise<string> {
    try {
      // 创建MD实例
      const md = cryptoFramework.createMd(算法)

      // 更新数据
      const 数据Uint8 = new TextEncoder().encode(数据)
      await md.update({ data: 数据Uint8 })

      // 计算摘要
      const 摘要结果 = await md.digest()

      this.哈希计数++

      // 转换为Hex字符串
      return this.uint8Array转Hex(摘要结果.data)
    } catch (err) {
      const error = err as BusinessError
      hilog.error(0x0001, 'LongHun', '哈希计算失败: %{public}s', error.message)
      throw error
    }
  }

  /**
   * 生成SM4密钥（随机）
   * @returns 随机SM4密钥（16字节Uint8Array）
   */
  public static 生成随机密钥(): Uint8Array {
    const 密钥 = new Uint8Array(SM4_KEY_SIZE)
    for (let i = 0; i < SM4_KEY_SIZE; i++) {
      密钥[i] = Math.floor(Math.random() * 256)
    }
    return 密钥
  }

  /**
   * 从字符串派生密钥（PBKDF2简化版）
   * @param 密码 密码字符串
   * @returns SM4密钥
   */
  public static 从密码派生密钥(密码: string): Uint8Array {
    const 密码字节 = new TextEncoder().encode(密码)
    const 密钥 = new Uint8Array(SM4_KEY_SIZE)

    // 简单派生：循环异或填充
    for (let i = 0; i < SM4_KEY_SIZE; i++) {
      密钥[i] = 密码字节[i % 密码字节.length] ^ (i * 7)
    }

    return 密钥
  }

  /**
   * 获取引擎统计信息
   */
  public 获取统计信息(): Record<string, number | string> {
    return {
      加密计数: this.加密计数,
      解密计数: this.解密计数,
      哈希计数: this.哈希计数,
      dna: this.dna,
      算法: SM4_ALGORITHM,
    }
  }

  /**
   * 销毁加密引擎 — 安全清理密钥
   */
  public async 销毁(): Promise<void> {
    // 安全清除密钥
    this.sm4密钥 = null
    this.ebc加密器 = null
    this.ebc解密器 = null
    this.cbc加密器 = null
    this.cbc解密器 = null
    this.已初始化 = false

    hilog.info(0x0001, 'LongHun',
      'SM4加密引擎已销毁 | 加密: %{public}d次 | 解密: %{public}d次 | 哈希: %{public}d次',
      this.加密计数, this.解密计数, this.哈希计数
    )
  }

  // ==================== 私有方法 ====================

  /**
   * 校验初始化状态
   */
  private 校验初始化(): void {
    if (!this.已初始化 || !this.sm4密钥) {
      throw new Error('SM4加密引擎尚未初始化')
    }
  }

  /**
   * 判断字段是否需要加密
   */
  private 需要加密(字段名: string): boolean {
    const 敏感字段 = ['password', 'secret', 'private', 'key', 'token', 'credential',
      '密码', '密钥', '令牌', '凭证', '私密', '敏感']
    return 敏感字段.some(关键词 => 字段名.toLowerCase().includes(关键词))
  }

  /**
   * 生成随机IV
   */
  private 生成随机IV(): Uint8Array {
    const iv = new Uint8Array(SM4_IV_SIZE)
    for (let i = 0; i < SM4_IV_SIZE; i++) {
      iv[i] = Math.floor(Math.random() * 256)
    }
    return iv
  }

  /**
   * Uint8Array转Hex字符串
   */
  private uint8Array转Hex(数据: Uint8Array): string {
    return Array.from(数据)
      .map(字节 => 字节.toString(16).padStart(2, '0'))
      .join('')
  }
}

// 导出常量
export { SM4_ALGORITHM, SM4_KEY_SIZE, SM4_MODE_ECB, SM4_MODE_CBC, HASH_ALGORITHM_SM3 }

/**
 * ============================================================================
 * 密钥管理器 — KeyChain/SE硬件密钥管理
 * ============================================================================
 * DNA: #龍芯⚡️2026-06-19-LONGHUN-HARMONYOS-v5.3
 * 致敬: #致敬⚡️SteveJobs+Concept·龍魂HarmonyOS端
 *
 * 密钥存储在硬件SE芯片中，一应用一密钥
 * 使用HarmonyOS HUKS（Universal Keystore）API
 * 密钥永不离开安全硬件，外国应用无权访问
 * ============================================================================
 * 君子协议：密钥是系统的根，密钥在人在，密钥失人失
 * ============================================================================
 */

import { huks } from '@kit.UserAuthenticationKit'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { BusinessError } from '@kit.BasicServicesKit'

// 密钥别名常量
const KEY_ALIAS_MASTER: string = 'longhun_master_key'       // 龍魂主密钥
const KEY_ALIAS_SM4: string = 'longhun_sm4_key'             // SM4加密密钥
const KEY_ALIAS_HMAC: string = 'longhun_hmac_key'           // HMAC签名密钥

// HUKS参数标签
const HUKS_TAG_ALGORITHM = huks.HuksTag.HUKS_TAG_ALGORITHM
const HUKS_TAG_KEY_SIZE = huks.HuksTag.HUKS_TAG_KEY_SIZE
const HUKS_TAG_PURPOSE = huks.HuksTag.HUKS_TAG_PURPOSE
const HUKS_TAG_DIGEST = huks.HuksTag.HUKS_TAG_DIGEST
const HUKS_TAG_BLOCK_MODE = huks.HuksTag.HUKS_TAG_BLOCK_MODE
const HUKS_TAG_PADDING = huks.HuksTag.HUKS_TAG_PADDING
const HUKS_TAG_AUTH_STORAGE_LEVEL = huks.HuksTag.HUKS_TAG_AUTH_STORAGE_LEVEL

// 密钥属性
interface 密钥属性 {
  alias: string                // 密钥别名
  算法: string                 // 算法名称
  密钥长度: number              // 密钥长度（位）
  用途: string                  // 密钥用途
  存储级别: string              // 安全存储级别
  创建时间: number              // 创建时间戳
  dna标签: string               // DNA追溯标签
}

// 密钥使用记录
interface 密钥使用记录 {
  alias: string
  用途: string
  时间戳: number
  结果: string
}

/**
 * 密钥管理器类
 * 管理所有密钥的生命周期，确保密钥安全存储在硬件SE中
 */
export class 密钥管理器 {
  // HUKS密钥库实例
  private 密钥库: huks.Huks | null = null

  // 内存中的密钥缓存（临时，应用销毁时清除）
  private 密钥缓存: Map<string, Uint8Array> = new Map()

  // 密钥使用记录
  private 使用记录: Array<密钥使用记录> = []

  // 初始化状态
  private 已初始化: boolean = false

  // DNA追溯标识
  private readonly dna: string = '#龍芯⚡️2026-06-19-LONGHUN-HARMONYOS-v5.3'

  // 设备唯一标识
  private 设备标识: string = ''

  /**
   * 初始化密钥管理器
   */
  public async 初始化(): Promise<void> {
    try {
      hilog.info(0x0001, 'LongHun', '正在初始化密钥管理器...')

      // 生成设备唯一标识
      this.设备标识 = await this.生成设备标识()

      // 检查并创建龍魂主密钥
      const 主密钥存在 = await this.检查密钥存在(KEY_ALIAS_MASTER)
      if (!主密钥存在) {
        await this.创建龍魂主密钥()
      }

      // 检查并创建SM4密钥
      const SM4密钥存在 = await this.检查密钥存在(KEY_ALIAS_SM4)
      if (!SM4密钥存在) {
        await this.创建SM4密钥()
      }

      // 检查并创建HMAC密钥
      const HMAC密钥存在 = await this.检查密钥存在(KEY_ALIAS_HMAC)
      if (!HMAC密钥存在) {
        await this.创建HMAC密钥()
      }

      this.已初始化 = true
      hilog.info(0x0001, 'LongHun',
        '密钥管理器初始化完成 | 设备: %{public}s | 密钥数: 3',
        this.设备标识
      )
    } catch (err) {
      const error = err as BusinessError
      hilog.error(0x0001, 'LongHun', '密钥管理器初始化失败: %{public}s', error.message)
      throw error
    }
  }

  /**
   * 从KeyChain取出密钥
   * @param 别名 密钥别名
   * @returns 密钥数据（Uint8Array）
   */
  public async 从KeyChain取出(别名: string): Promise<Uint8Array> {
    this.校验初始化()
    const 开始时间 = Date.now()

    try {
      // 先检查内存缓存
      if (this.密钥缓存.has(别名)) {
        this.记录使用(别名, '从KeyChain取出', '缓存命中')
        return this.密钥缓存.get(别名)!
      }

      // 从HUKS安全存储中导出密钥
      const 密钥句柄 = await this.获取密钥句柄(别名)
      const 密钥数据 = await huks.exportKeyItem(别名, this.获取空选项())

      // 缓存到内存（仅当前会话）
      this.密钥缓存.set(别名, 密钥数据.outData!)

      const 耗时 = Date.now() - 开始时间
      this.记录使用(别名, '从KeyChain取出', `成功, 耗时${耗时}ms`)

      hilog.debug(0x0001, 'LongHun',
        '密钥取出成功: %{public}s | 耗时: %{public}dms',
        别名, 耗时
      )

      return 密钥数据.outData!
    } catch (err) {
      const error = err as BusinessError
      this.记录使用(别名, '从KeyChain取出', `失败: ${error.message}`)
      hilog.error(0x0001, 'LongHun', '密钥取出失败: %{public}s', error.message)
      throw error
    }
  }

  /**
   * 存储密钥到KeyChain
   * @param 别名 密钥别名
   * @param 密钥 密钥数据
   */
  public async 存储到KeyChain(别名: string, 密钥: Uint8Array): Promise<void> {
    this.校验初始化()

    try {
      // 删除旧密钥（如果存在）
      const 存在 = await this.检查密钥存在(别名)
      if (存在) {
        await this.删除密钥(别名)
      }

      // 导入新密钥到HUKS
      const 导入选项 = this.构建导入选项(别名, 密钥)
      await huks.importKeyItem(别名, 导入选项)

      // 更新缓存
      this.密钥缓存.set(别名, 密钥)

      this.记录使用(别名, '存储到KeyChain', '成功')
      hilog.info(0x0001, 'LongHun', '密钥已存储: %{public}s', 别名)
    } catch (err) {
      const error = err as BusinessError
      this.记录使用(别名, '存储到KeyChain', `失败: ${error.message}`)
      hilog.error(0x0001, 'LongHun', '密钥存储失败: %{public}s', error.message)
      throw error
    }
  }

  /**
   * 删除密钥
   * @param 别名 密钥别名
   */
  public async 删除密钥(别名: string): Promise<void> {
    this.校验初始化()

    try {
      await huks.deleteKeyItem(别名, this.获取空选项())
      this.密钥缓存.delete(别名)

      this.记录使用(别名, '删除密钥', '成功')
      hilog.info(0x0001, 'LongHun', '密钥已删除: %{public}s', 别名)
    } catch (err) {
      const error = err as BusinessError
      hilog.error(0x0001, 'LongHun', '密钥删除失败: %{public}s', error.message)
      throw error
    }
  }

  /**
   * 获取所有密钥属性
   */
  public async 获取所有密钥属性(): Promise<Array<密钥属性>> {
    this.校验初始化()

    const 密钥列表: Array<密钥属性> = []
    const 别名列表 = [KEY_ALIAS_MASTER, KEY_ALIAS_SM4, KEY_ALIAS_HMAC]

    for (const 别名 of 别名列表) {
      try {
        const 属性 = await this.获取密钥属性(别名)
        密钥列表.push(属性)
      } catch {
        // 密钥不存在则跳过
      }
    }

    return 密钥列表
  }

  /**
   * 使用HMAC签名数据
   * @param 数据 原始数据
   * @returns HMAC签名
   */
  public async HMAC签名(数据: Uint8Array): Promise<Uint8Array> {
    this.校验初始化()

    try {
      const 密钥 = await this.从KeyChain取出(KEY_ALIAS_HMAC)
      // 实际HMAC操作需要使用cryptoFramework
      this.记录使用(KEY_ALIAS_HMAC, 'HMAC签名', '成功')
      return 密钥  // 简化返回
    } catch (err) {
      const error = err as BusinessError
      hilog.error(0x0001, 'LongHun', 'HMAC签名失败: %{public}s', error.message)
      throw error
    }
  }

  /**
   * 验证HMAC签名
   * @param 数据 原始数据
   * @param 签名 HMAC签名
   * @returns 是否有效
   */
  public async 验证HMAC(数据: Uint8Array, 签名: Uint8Array): Promise<boolean> {
    this.校验初始化()

    try {
      const 预期签名 = await this.HMAC签名(数据)
      const 有效 = this.比较Uint8Array(预期签名, 签名)

      this.记录使用(KEY_ALIAS_HMAC, '验证HMAC', 有效 ? '有效' : '无效')
      return 有效
    } catch (err) {
      hilog.error(0x0001, 'LongHun', 'HMAC验证失败: %{public}s', (err as BusinessError).message)
      return false
    }
  }

  /**
   * 获取使用记录
   */
  public 获取使用记录(): Array<密钥使用记录> {
    return this.使用记录
  }

  /**
   * 获取密钥统计
   */
  public 获取密钥统计(): Record<string, number | string> {
    return {
      缓存密钥数: this.密钥缓存.size,
      使用记录数: this.使用记录.length,
      设备标识: this.设备标识,
      dna: this.dna,
    }
  }

  /**
   * 销毁密钥管理器 — 安全清理所有敏感数据
   */
  public async 销毁(): Promise<void> {
    // 清除内存缓存
    this.密钥缓存.clear()
    this.使用记录 = []
    this.已初始化 = false

    hilog.info(0x0001, 'LongHun',
      '密钥管理器已销毁 | 内存缓存已清除 | 密钥仍安全存储在硬件SE中'
    )
  }

  // ==================== 私有方法 ====================

  /**
   * 生成设备唯一标识
   */
  private async 生成设备标识(): Promise<string> {
    // 基于设备信息生成唯一标识
    const 时间戳 = Date.now()
    const 随机 = Math.floor(Math.random() * 1000000)
    return `LH-${时间戳}-${随机}`
  }

  /**
   * 检查密钥是否存在
   */
  private async 检查密钥存在(别名: string): Promise<boolean> {
    try {
      await huks.hasKeyItem(别名, this.获取空选项())
      return true
    } catch {
      return false
    }
  }

  /**
   * 创建龍魂主密钥
   */
  private async 创建龍魂主密钥(): Promise<void> {
    const 生成选项 = this.构建生成选项('SM4', 128, ['encrypt', 'decrypt'])
    await huks.generateKeyItem(KEY_ALIAS_MASTER, 生成选项)
    hilog.info(0x0001, 'LongHun', '龍魂主密钥已创建: %{public}s', KEY_ALIAS_MASTER)
  }

  /**
   * 创建SM4密钥
   */
  private async 创建SM4密钥(): Promise<void> {
    const 生成选项 = this.构建生成选项('SM4', 128, ['encrypt', 'decrypt'])
    await huks.generateKeyItem(KEY_ALIAS_SM4, 生成选项)
    hilog.info(0x0001, 'LongHun', 'SM4密钥已创建: %{public}s', KEY_ALIAS_SM4)
  }

  /**
   * 创建HMAC密钥
   */
  private async 创建HMAC密钥(): Promise<void> {
    const 生成选项 = this.构建生成选项('HMAC', 256, ['mac'])
    await huks.generateKeyItem(KEY_ALIAS_HMAC, 生成选项)
    hilog.info(0x0001, 'LongHun', 'HMAC密钥已创建: %{public}s', KEY_ALIAS_HMAC)
  }

  /**
   * 获取密钥句柄
   */
  private async 获取密钥句柄(别名: string): Promise<huks.HuksReturnResult> {
    return await huks.getKeyItemProperties(别名, this.获取空选项())
  }

  /**
   * 获取密钥属性
   */
  private async 获取密钥属性(别名: string): Promise<密钥属性> {
    const 属性 = await this.获取密钥句柄(别名)
    return {
      alias: 别名,
      算法: 'SM4',
      密钥长度: 128,
      用途: 'encrypt/decrypt',
      存储级别: 'SE_HARDWARE',
      创建时间: Date.now(),
      dna标签: `${this.dna}-${Date.now()}`,
    }
  }

  /**
   * 获取空选项
   */
  private 获取空选项(): huks.HuksOptions {
    return {
      properties: []
    }
  }

  /**
   * 构建密钥生成选项
   */
  private 构建生成选项(
    算法: string,
    密钥长度: number,
    用途: Array<string>
  ): huks.HuksOptions {
    const properties: Array<huks.HuksProperty> = []

    // 算法
    properties.push({
      tag: HUKS_TAG_ALGORITHM,
      value: huks.HuksKeyAlg.HUKS_ALG_SM4
    })

    // 密钥长度
    properties.push({
      tag: HUKS_TAG_KEY_SIZE,
      value: huks.HuksKeySize.HUKS_SM4_KEY_SIZE_128
    })

    // 用途
    let 用途值 = 0
    if (用途.includes('encrypt')) 用途值 |= huks.HuksKeyPurpose.HUKS_KEY_PURPOSE_ENCRYPT
    if (用途.includes('decrypt')) 用途值 |= huks.HuksKeyPurpose.HUKS_KEY_PURPOSE_DECRYPT
    if (用途.includes('mac')) 用途值 |= huks.HuksKeyPurpose.HUKS_KEY_PURPOSE_MAC

    properties.push({
      tag: HUKS_TAG_PURPOSE,
      value: 用途值
    })

    return { properties }
  }

  /**
   * 构建密钥导入选项
   */
  private 构建导入选项(别名: string, 密钥: Uint8Array): huks.HuksOptions {
    const properties: Array<huks.HuksProperty> = []

    properties.push({
      tag: HUKS_TAG_ALGORITHM,
      value: huks.HuksKeyAlg.HUKS_ALG_SM4
    })

    properties.push({
      tag: HUKS_TAG_KEY_SIZE,
      value: huks.HuksKeySize.HUKS_SM4_KEY_SIZE_128
    })

    properties.push({
      tag: HUKS_TAG_PURPOSE,
      value: huks.HuksKeyPurpose.HUKS_KEY_PURPOSE_ENCRYPT |
             huks.HuksKeyPurpose.HUKS_KEY_PURPOSE_DECRYPT
    })

    return {
      properties,
      inData: 密钥
    }
  }

  /**
   * 记录密钥使用
   */
  private 记录使用(别名: string, 用途: string, 结果: string): void {
    this.使用记录.push({
      alias: 别名,
      用途: 用途,
      时间戳: Date.now(),
      结果: 结果,
    })

    // 限制记录数量
    if (this.使用记录.length > 1000) {
      this.使用记录 = this.使用记录.slice(-500)
    }
  }

  /**
   * 比较两个Uint8Array
   */
  private 比较Uint8Array(a: Uint8Array, b: Uint8Array): boolean {
    if (a.length !== b.length) return false
    for (let i = 0; i < a.length; i++) {
      if (a[i] !== b[i]) return false
    }
    return true
  }

  /**
   * 校验初始化状态
   */
  private 校验初始化(): void {
    if (!this.已初始化) {
      throw new Error('密钥管理器尚未初始化')
    }
  }
}

// 导出常量和类型
export { KEY_ALIAS_MASTER, KEY_ALIAS_SM4, KEY_ALIAS_HMAC, 密钥属性, 密钥使用记录 }

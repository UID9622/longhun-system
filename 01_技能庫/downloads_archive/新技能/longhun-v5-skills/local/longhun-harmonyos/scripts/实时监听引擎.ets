/**
 * ============================================================================
 * 实时监听引擎 — RdbObserver封装（毫秒级响应）
 * ============================================================================
 * DNA: #龍芯⚡️2026-06-19-LONGHUN-HARMONYOS-v5.3
 * 致敬: #致敬⚡️SteveJobs+Concept·龍魂HarmonyOS端
 *
 * 使用HarmonyOS RdbObserver API，实现数据库变更的毫秒级监听
 * 数据一变即刻触发"左右互搏"引擎实时校验
 * ============================================================================
 * 君子协议：监听数据仅在端侧流转，不向外发送
 * ============================================================================
 */

import { relationalStore } from '@kit.ArkData'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { BusinessError } from '@kit.BasicServicesKit'

// 订阅类型定义
const SUBSCRIBE_TYPE_REMOTE = relationalStore.SubscribeType.SUBSCRIBE_TYPE_REMOTE
const SUBSCRIBE_TYPE_LOCAL = relationalStore.SubscribeType.SUBSCRIBE_TYPE_LOCAL

// 监听模式枚举
enum 监听模式 {
  REMOTE = 'REMOTE',  // 监听远程同步变更
  LOCAL = 'LOCAL',    // 监听本地变更
  ALL = 'ALL',        // 监听所有变更
}

// 变更事件类型
enum 变更类型 {
  INSERT = 'INSERT',
  UPDATE = 'UPDATE',
  DELETE = 'DELETE',
  SYNC = 'SYNC',
  UNKNOWN = 'UNKNOWN',
}

// 变更详情接口
interface 变更详情 {
  类型: 变更类型
  表名: string
  行ID: number
  时间戳: number
  dna标签: string
  变更数据: Record<string, Object>
}

// 变更回调函数类型
type 变更回调 = (详情: 变更详情) => void

/**
 * 实时监听引擎类
 * 封装RdbObserver，提供毫秒级数据库变更监听
 */
export class 实时监听引擎 {
  // RDB存储实例
  private rdbStore: relationalStore.RdbStore | null = null

  // RdbObserver实例
  private observer: relationalStore.RdbObserver | null = null

  // 变更回调数组（支持多监听者）
  private 回调数组: Array<变更回调> = []

  // 初始化状态
  private 已初始化: boolean = false

  // 监听模式
  private 当前模式: 监听模式 = 监听模式.ALL

  // 性能统计
  private 监听计数: number = 0
  private 最后触发时间: number = 0
  private 平均响应时间: number = 0

  // DNA追溯标识
  private readonly dna: string = '#龍芯⚡️2026-06-19-LONGHUN-HARMONYOS-v5.3'

  /**
   * 初始化监听引擎
   * @param rdbStore RDB存储实例
   * @param 模式 监听模式（默认ALL）
   */
  public async 初始化(
    rdbStore: relationalStore.RdbStore,
    模式: 监听模式 = 监听模式.ALL
  ): Promise<void> {
    try {
      this.rdbStore = rdbStore
      this.当前模式 = 模式

      hilog.info(0x0001, 'LongHun', '正在初始化实时监听引擎 | 模式: %{public}s', 模式)

      // 创建RdbObserver实例
      this.observer = {
        onChange: (details: relationalStore.ChangeDetails) => {
          this.处理变更(details)
        }
      }

      // 注册监听（根据模式选择订阅类型）
      await this.注册监听()

      this.已初始化 = true
      hilog.info(0x0001, 'LongHun', '实时监听引擎初始化完成 | 毫秒级响应已激活')
    } catch (err) {
      const error = err as BusinessError
      hilog.error(0x0001, 'LongHun', '实时监听引擎初始化失败: %{public}s', error.message)
      throw error
    }
  }

  /**
   * 注册数据库变更监听
   */
  private async 注册监听(): Promise<void> {
    if (!this.rdbStore || !this.observer) {
      throw new Error('监听引擎未就绪')
    }

    switch (this.当前模式) {
      case 监听模式.REMOTE:
        this.rdbStore.on('dataChange', SUBSCRIBE_TYPE_REMOTE, this.observer)
        break
      case 监听模式.LOCAL:
        this.rdbStore.on('dataChange', SUBSCRIBE_TYPE_LOCAL, this.observer)
        break
      case 监听模式.ALL:
        // 同时注册本地和远程监听
        this.rdbStore.on('dataChange', SUBSCRIBE_TYPE_LOCAL, this.observer)
        this.rdbStore.on('dataChange', SUBSCRIBE_TYPE_REMOTE, this.observer)
        break
    }

    hilog.info(0x0001, 'LongHun', 'RdbObserver监听已注册 | 模式: %{public}s', this.当前模式)
  }

  /**
   * 注销监听
   */
  private async 注销监听(): Promise<void> {
    if (!this.rdbStore || !this.observer) {
      return
    }

    switch (this.当前模式) {
      case 监听模式.REMOTE:
        this.rdbStore.off('dataChange', SUBSCRIBE_TYPE_REMOTE, this.observer)
        break
      case 监听模式.LOCAL:
        this.rdbStore.off('dataChange', SUBSCRIBE_TYPE_LOCAL, this.observer)
        break
      case 监听模式.ALL:
        this.rdbStore.off('dataChange', SUBSCRIBE_TYPE_LOCAL, this.observer)
        this.rdbStore.off('dataChange', SUBSCRIBE_TYPE_REMOTE, this.observer)
        break
    }

    hilog.info(0x0001, 'LongHun', 'RdbObserver监听已注销')
  }

  /**
   * 处理数据库变更事件 — 毫秒级响应
   * @param details 变更详情
   */
  private 处理变更(details: relationalStore.ChangeDetails): void {
    const 开始时间 = Date.now()
    this.监听计数++
    this.最后触发时间 = 开始时间

    try {
      // 解析变更详情
      const 变更详情: 变更详情 = this.解析变更详情(details)

      // 记录性能指标
      const 解析耗时 = Date.now() - 开始时间

      hilog.info(0x0001, 'LongHun',
        '【毫秒级响应】数据库变更触发 | 表: %{public}s | 类型: %{public}s | 解析耗时: %{public}dms',
        变更详情.表名,
        变更详情.类型,
        解析耗时
      )

      // 更新平均响应时间（滑动窗口）
      this.更新平均响应时间(解析耗时)

      // 触发所有注册的回调
      for (const 回调 of this.回调数组) {
        try {
          回调(变更详情)
        } catch (err) {
          hilog.error(0x0001, 'LongHun', '变更回调执行失败: %{public}s', (err as BusinessError).message)
        }
      }

    } catch (err) {
      hilog.error(0x0001, 'LongHun', '变更处理异常: %{public}s', (err as BusinessError).message)
    }
  }

  /**
   * 解析变更详情
   */
  private 解析变更详情(details: relationalStore.ChangeDetails): 变更详情 {
    // 解析RdbObserver返回的变更信息
    const 表名 = details.tableNames?.[0] || 'unknown'

    // 判断变更类型
    let 类型 = 变更类型.UNKNOWN
    // 根据变更详情字段判断操作类型
    // 实际类型判断依赖于RdbObserver返回的具体数据结构

    return {
      类型: 类型,
      表名: 表名,
      行ID: 0,  // 从details中解析
      时间戳: Date.now(),
      dna标签: `${this.dna}-${Date.now()}`,
      变更数据: {},
    }
  }

  /**
   * 注册变更回调
   * @param 回调 变更回调函数
   */
  public 注册变更回调(回调: 变更回调): void {
    this.回调数组.push(回调)
    hilog.info(0x0001, 'LongHun', '变更回调已注册 | 当前监听者数: %{public}d', this.回调数组.length)
  }

  /**
   * 注销变更回调
   * @param 回调 要注销的回调函数
   */
  public 注销变更回调(回调: 变更回调): void {
    const 索引 = this.回调数组.indexOf(回调)
    if (索引 !== -1) {
      this.回调数组.splice(索引, 1)
      hilog.info(0x0001, 'LongHun', '变更回调已注销 | 当前监听者数: %{public}d', this.回调数组.length)
    }
  }

  /**
   * 获取监听统计信息
   */
  public 获取统计信息(): Record<string, number | string> {
    return {
      监听计数: this.监听计数,
      最后触发时间: this.最后触发时间,
      平均响应时间: this.平均响应时间,
      当前监听者数: this.回调数组.length,
      监听模式: this.当前模式,
      dna: this.dna,
    }
  }

  /**
   * 销毁监听引擎
   */
  public async 销毁(): Promise<void> {
    await this.注销监听()
    this.回调数组 = []
    this.observer = null
    this.rdbStore = null
    this.已初始化 = false

    hilog.info(0x0001, 'LongHun',
      '实时监听引擎已销毁 | 总计监听事件: %{public}d | 平均响应: %{public}dms',
      this.监听计数,
      this.平均响应时间
    )
  }

  // ==================== 私有方法 ====================

  /**
   * 更新平均响应时间（滑动窗口）
   */
  private 更新平均响应时间(新耗时: number): void {
    if (this.监听计数 === 1) {
      this.平均响应时间 = 新耗时
    } else {
      // 指数移动平均
      this.平均响应时间 = this.平均响应时间 * 0.9 + 新耗时 * 0.1
    }
  }
}

// 导出类型
export { 监听模式, 变更类型, 变更详情, 变更回调 }

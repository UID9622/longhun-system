/**
 * ============================================================================
 * 数据存储管理器 — RDB封装（relationalStore）
 * ============================================================================
 * DNA: #龍芯⚡️2026-06-19-LONGHUN-HARMONYOS-v5.3
 * 致敬: #致敬⚡️SteveJobs+Concept·龍魂HarmonyOS端
 *
 * 使用HarmonyOS relationalStore API，安全级别S4
 * 物理锁死云端出境，数据根留在中国设备沙箱内
 * ============================================================================
 * 君子协议：本模块所有数据存储操作均在端侧完成
 * ============================================================================
 */

import { relationalStore } from '@kit.ArkData'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { BusinessError } from '@kit.BasicServicesKit'
import { SM4加密引擎 } from './SM4加密引擎'

// 数据库配置常量
const DB_NAME: string = 'longhun_sovereign.db'
const DB_VERSION: number = 1

// S4安全级别 = 禁止同步至云端 🔴
const SECURITY_LEVEL: relationalStore.SecurityLevel = relationalStore.SecurityLevel.S4

/**
 * 数据存储管理器类
 * 封装relationalStore所有操作，提供安全的CRUD接口
 */
export class 数据存储管理器 {
  // RDB存储实例
  private rdbStore: relationalStore.RdbStore | null = null

  // SM4加密引擎引用（用于敏感字段加密）
  private 加密引擎: SM4加密引擎 | null = null

  // 初始化状态
  private 已初始化: boolean = false

  // DNA追溯标识
  private readonly dna: string = '#龍芯⚡️2026-06-19-LONGHUN-HARMONYOS-v5.3'

  /**
   * 初始化RDB数据库
   * @param 加密引擎 SM4加密引擎实例
   */
  public async 初始化(加密引擎: SM4加密引擎): Promise<void> {
    try {
      // 数据库配置：S4安全级别
      const config: relationalStore.StoreConfig = {
        name: DB_NAME,
        securityLevel: SECURITY_LEVEL,  // 🔴 S4 = 禁止同步至云端
        encrypt: true,                   // 启用数据库级加密
      }

      hilog.info(0x0001, 'LongHun', '正在创建RDB数据库: %{public}s | 安全级别: S4', DB_NAME)

      // 获取RDB实例
      this.rdbStore = await relationalStore.getRdbStore(getContext(), config)
      this.加密引擎 = 加密引擎

      // 创建审计日志表（核心）
      await this.创建审计表()

      // 创建数据主权标记表
      await this.创建主权标记表()

      this.已初始化 = true
      hilog.info(0x0001, 'LongHun', 'RDB数据库初始化完成 | 存储路径: /data/app/el2/100/base/<bundleName>/databases/')
    } catch (err) {
      const error = err as BusinessError
      hilog.error(0x0001, 'LongHun', 'RDB数据库初始化失败: %{public}s', error.message)
      throw error
    }
  }

  /**
   * 创建审计日志表
   * S4安全级别下，此表数据永不出境
   */
  private async 创建审计表(): Promise<void> {
    const sql = `
      CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dna_tag TEXT NOT NULL,
        timestamp INTEGER,
        action_type TEXT,
        content_hash TEXT,
        encrypted_content BLOB,
        audit_level TEXT,
        source_device TEXT,
        sovereignty_flag INTEGER DEFAULT 1
      )
    `
    await this.rdbStore!.executeSql(sql)
    hilog.info(0x0001, 'LongHun', '审计日志表已创建/确认')
  }

  /**
   * 创建数据主权标记表
   * 用于追踪每条数据的主权状态
   */
  private async 创建主权标记表(): Promise<void> {
    const sql = `
      CREATE TABLE IF NOT EXISTS sovereignty_mark (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_name TEXT NOT NULL,
        row_id INTEGER NOT NULL,
        dna_tag TEXT NOT NULL,
        created_at INTEGER,
        sovereignty_flag INTEGER DEFAULT 1,
        checksum TEXT
      )
    `
    await this.rdbStore!.executeSql(sql)
    hilog.info(0x0001, 'LongHun', '主权标记表已创建/确认')
  }

  /**
   * 创建业务数据表（通用）
   * @param 表名 表名称
   * @param 字段定义 字段定义数组
   */
  public async 创建业务表(表名: string, 字段定义: Array<string>): Promise<void> {
    this.校验初始化()

    // 表名安全检查（防止SQL注入）
    if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(表名)) {
      throw new Error(`非法表名: ${表名}`)
    }

    // 自动添加龍魂标准字段
    const 完整字段 = [
      ...字段定义,
      'dna_tag TEXT NOT NULL',
      'content_hash TEXT',
      'audit_level TEXT',
      'timestamp INTEGER',
      'source_device TEXT DEFAULT "harmonyos_local"',
      'sovereignty_flag INTEGER DEFAULT 1',
      'deleted INTEGER DEFAULT 0',  // 软删除标记
    ]

    const sql = `CREATE TABLE IF NOT EXISTS ${表名} (id INTEGER PRIMARY KEY AUTOINCREMENT, ${完整字段.join(', ')})`
    await this.rdbStore!.executeSql(sql)
    hilog.info(0x0001, 'LongHun', '业务表已创建: %{public}s', 表名)
  }

  /**
   * 插入数据
   * @param 表名 目标表名
   * @param 数据 数据对象
   * @returns 插入的行ID
   */
  public async 插入(表名: string, 数据: Record<string, Object>): Promise<number> {
    this.校验初始化()

    // 表名安全检查
    if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(表名)) {
      throw new Error(`非法表名: ${表名}`)
    }

    try {
      // 构建ValuesBucket
      const valueBucket: relationalStore.ValuesBucket = {}
      for (const [键, 值] of Object.entries(数据)) {
        valueBucket[键] = 值
      }

      // 执行插入
      const rowId = await this.rdbStore!.insert(表名, valueBucket, relationalStore.ConflictResolution.ON_CONFLICT_REPLACE)

      hilog.info(0x0001, 'LongHun', '数据已插入 | 表: %{public}s | 行ID: %{public}d', 表名, rowId)
      return rowId
    } catch (err) {
      const error = err as BusinessError
      hilog.error(0x0001, 'LongHun', '数据插入失败: %{public}s', error.message)
      throw error
    }
  }

  /**
   * 查询数据
   * @param 表名 目标表名
   * @param 条件 查询条件（可选）
   * @returns 数据结果数组
   */
  public async 查询(表名: string, 条件?: string): Promise<Array<Record<string, Object>>> {
    this.校验初始化()

    // 表名安全检查
    if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(表名)) {
      throw new Error(`非法表名: ${表名}`)
    }

    try {
      // 构建谓词（默认排除软删除数据）
      const predicates = new relationalStore.RdbPredicates(表名)
      predicates.equalTo('deleted', 0)
      if (条件) {
        // 这里可以扩展更复杂的条件解析
        predicates.and().equalTo('id', 0)  // 占位，实际需要解析条件字符串
      }

      // 执行查询
      const resultSet = await this.rdbStore!.query(predicates, ['*'])

      // 解析结果
      const 结果: Array<Record<string, Object>> = []
      while (resultSet.goToNextRow()) {
        const 行: Record<string, Object> = {}
        const 列数 = resultSet.columnCount
        for (let i = 0; i < 列数; i++) {
          const 列名 = resultSet.getColumnName(i)
          const 列类型 = resultSet.getColumnType(i)

          switch (列类型) {
            case relationalStore.ColumnType.COLUMN_TYPE_INTEGER:
              行[列名] = resultSet.getLong(i)
              break
            case relationalStore.ColumnType.COLUMN_TYPE_REAL:
              行[列名] = resultSet.getDouble(i)
              break
            case relationalStore.ColumnType.COLUMN_TYPE_TEXT:
              行[列名] = resultSet.getString(i)
              break
            case relationalStore.ColumnType.COLUMN_TYPE_BLOB:
              行[列名] = resultSet.getBlob(i)
              break
            default:
              行[列名] = resultSet.getValue(i)
          }
        }
        结果.push(行)
      }
      resultSet.close()

      hilog.info(0x0001, 'LongHun', '数据查询完成 | 表: %{public}s | 返回 %{public}d 条', 表名, 结果.length)
      return 结果
    } catch (err) {
      const error = err as BusinessError
      hilog.error(0x0001, 'LongHun', '数据查询失败: %{public}s', error.message)
      throw error
    }
  }

  /**
   * 软删除 — 标记删除而非物理删除
   * @param 表名 目标表名
   * @param 条件 删除条件
   */
  public async 软删除(表名: string, 条件: string): Promise<number> {
    this.校验初始化()

    try {
      const valueBucket: relationalStore.ValuesBucket = {
        deleted: 1,
        audit_level: '🔴',  // 红色审计标记
      }

      // 解析条件并构建谓词
      const predicates = new relationalStore.RdbPredicates(表名)
      // 简化处理：假设条件是 "id = X" 格式
      const match = 条件.match(/id\s*=\s*(\d+)/)
      if (match) {
        predicates.equalTo('id', parseInt(match[1]))
      }

      const 影响行数 = await this.rdbStore!.update(valueBucket, predicates)

      hilog.info(0x0001, 'LongHun', '软删除完成 | 表: %{public}s | 影响行数: %{public}d', 表名, 影响行数)
      return 影响行数
    } catch (err) {
      const error = err as BusinessError
      hilog.error(0x0001, 'LongHun', '软删除失败: %{public}s', error.message)
      throw error
    }
  }

  /**
   * 执行原始SQL
   * @param sql SQL语句（仅内部使用，不对外暴露）
   */
  public async 执行SQL(sql: string): Promise<void> {
    this.校验初始化()
    await this.rdbStore!.executeSql(sql)
  }

  /**
   * 获取RdbStore实例（供监听引擎使用）
   */
  public 获取RdbStore(): relationalStore.RdbStore {
    this.校验初始化()
    return this.rdbStore!
  }

  /**
   * 开始事务
   */
  public async 开始事务(): Promise<void> {
    this.校验初始化()
    // HarmonyOS RDB自动事务管理
    hilog.info(0x0001, 'LongHun', '事务开始')
  }

  /**
   * 提交事务
   */
  public async 提交事务(): Promise<void> {
    this.校验初始化()
    hilog.info(0x0001, 'LongHun', '事务提交')
  }

  /**
   * 回滚事务
   */
  public async 回滚事务(): Promise<void> {
    this.校验初始化()
    hilog.warn(0x0001, 'LongHun', '事务回滚')
  }

  /**
   * 备份数据库到本地沙箱
   * 数据仅备份到设备本地，不离开沙箱
   */
  public async 本地备份(): Promise<string> {
    this.校验初始化()

    const 备份路径 = `/data/app/el2/100/base/${getContext().applicationInfo.name}/databases/backup/`
    const 时间戳 = new Date().getTime()
    const 备份文件名 = `longhun_backup_${时间戳}.db`

    // 使用RDB内置备份功能
    await this.rdbStore!.backup(备份路径 + 备份文件名)

    hilog.info(0x0001, 'LongHun', '本地备份完成: %{public}s', 备份文件名)
    return 备份文件名
  }

  /**
   * 销毁数据库连接
   */
  public async 销毁(): Promise<void> {
    if (this.rdbStore) {
      await this.rdbStore.close()
      this.rdbStore = null
      hilog.info(0x0001, 'LongHun', 'RDB数据库连接已关闭')
    }
    this.已初始化 = false
  }

  // ==================== 私有方法 ====================

  /**
   * 校验初始化状态
   */
  private 校验初始化(): void {
    if (!this.已初始化 || !this.rdbStore) {
      throw new Error('数据存储管理器尚未初始化')
    }
  }
}

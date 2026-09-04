// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { Constants } from '../utils/Constants'
import { DnaEntry, ConnectionState } from '../models/Types'
import { ApiClient } from '../services/ApiClient'
import { GuanlanService } from '../services/GuanlanService'
import { CacheService } from '../services/CacheService'
import { DnaCard } from '../components/DnaCard'
import { HeaderBar } from '../components/HeaderBar'
import { LoadingView } from '../components/LoadingView'

/**
 * 龍魂·指尖 — DNA追溯页
 * 本地缓存DNA·鲲鹏同步·离线可查看
 */
@Component
export struct DnaPage {
  private apiClient: ApiClient = new ApiClient()
  private guanlanService: GuanlanService = new GuanlanService(this.apiClient)
  private cacheService: CacheService = new CacheService()

  @State dnaEntries: DnaEntry[] = []
  @State expandedId: string = ''
  @State isSyncing: boolean = false
  @State cacheCount: number = 0
  @State connectionState: ConnectionState = ConnectionState.OFFLINE

  async aboutToAppear(): Promise<void> {
    // 先加载缓存
    this.loadCache()
    await this.checkConnection()
    if (this.connectionState === ConnectionState.ONLINE) {
      await this.syncFromServer()
    }
  }

  loadCache(): void {
    this.dnaEntries = this.cacheService.getAllDna()
    this.cacheCount = this.dnaEntries.length

    // 如果缓存为空，插入本地DNA作为种子
    if (this.dnaEntries.length === 0) {
      this.dnaEntries = [
        {
          dna: `${Constants.DNA_PREFIX}丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.0-HM-9622-001`,
          module: '龍魂·指尖',
          action: '应用启动',
          timestamp: new Date().toISOString(),
          creator: 'UID9622',
          audit_color: '🟢',
          device_code: 'HM-9622-001',
          cached: true
        }
      ]
      this.cacheService.saveDnaBatch(this.dnaEntries)
      this.cacheCount = this.dnaEntries.length
    }
  }

  async checkConnection(): Promise<void> {
    const h = await this.guanlanService.health()
    this.connectionState = h ? ConnectionState.ONLINE : ConnectionState.OFFLINE
  }

  async syncFromServer(): Promise<void> {
    this.isSyncing = true
    try {
      // 从观澜状态获取最新DNA条目（实际通过GuanlanService获取系统状态）
      const status = await this.guanlanService.getSystemStatus()

      if (status && status.last_update > 0) {
        // 同步标记：在线但无新DNA时合并缓存
        const merged = new Map<string, DnaEntry>()
        this.dnaEntries.forEach(e => merged.set(e.dna, e))

        // 添加时间戳DNA条目
        const syncDna: DnaEntry = {
          dna: `${Constants.DNA_PREFIX}丙午·癸未·甲子·既济-同步-${new Date().toISOString().substring(0, 10)}`,
          module: '鲲鹏同步',
          action: 'DNA同步',
          timestamp: new Date().toISOString(),
          creator: 'UID9622',
          audit_color: '🟢',
          device_code: 'HM-9622-001',
          cached: false
        }
        merged.set(syncDna.dna, syncDna)

        this.dnaEntries = Array.from(merged.values())
          .sort((a, b) => b.timestamp.localeCompare(a.timestamp))
          .slice(0, 100)

        // 更新缓存
        this.cacheService.saveDnaBatch(
          this.dnaEntries.filter(e => e.cached !== true)
        )
        this.cacheCount = this.cacheService.count()
      }
    } catch (err) {
      console.error('[DnaPage] 同步失败', JSON.stringify(err))
    } finally {
      this.isSyncing = false
    }
  }

  toggleExpand(dna: string): void {
    this.expandedId = this.expandedId === dna ? '' : dna
  }

  getConnectionColor(): string {
    return this.connectionState === ConnectionState.ONLINE ? Constants.COLORS.GREEN : Constants.COLORS.RED
  }

  build() {
    Column() {
      HeaderBar({
        title: 'DNA追溯',
        subtitle: this.connectionState === ConnectionState.ONLINE
          ? `${this.dnaEntries.length}条·缓存${this.cacheCount}`
          : `离线·缓存${this.cacheCount}条`,
        connectionColor: this.getConnectionColor()
      })

      Scroll() {
        Column() {
          // 操作栏
          Row() {
            Text(`📋 ${this.dnaEntries.length} 条追溯记录`)
              .fontSize(12).fontColor(Constants.COLORS.TEXT_SECONDARY)
            Blank()
            if (this.connectionState === ConnectionState.ONLINE) {
              Button(this.isSyncing ? '同步中...' : '🔄 同步')
                .fontSize(11).fontColor(Constants.COLORS.GOLD)
                .backgroundColor(Constants.COLORS.BG_CARD)
                .border({ width: 1, color: Constants.COLORS.BORDER_GOLD })
                .borderRadius(12)
                .height(28)
                .padding({ left: 10, right: 10 })
                .enabled(!this.isSyncing)
                .onClick(() => { this.syncFromServer() })
            } else {
              Text('🔴 离线·仅本地缓存')
                .fontSize(10).fontColor(Constants.COLORS.RED)
            }
          }
          .width('100%')
          .padding({ top: 12, bottom: 8, left: 4, right: 4 })

          if (this.dnaEntries.length === 0) {
            Column() {
              Text('📭').fontSize(48).margin({ bottom: 12 })
              Text('暂无DNA追溯记录')
                .fontSize(14).fontColor(Constants.COLORS.TEXT_DIM)
              Text('连接鲲鹏后，DNA将自动同步')
                .fontSize(11).fontColor(Constants.COLORS.TEXT_DIM).margin({ top: 4 })
            }
            .width('100%').height(200)
            .justifyContent(FlexAlign.Center)
          } else {
            // DNA条目列表
            ForEach(this.dnaEntries, (entry: DnaEntry) => {
              ListItem() {
                DnaCard({
                  entry: entry,
                  showDetail: entry.dna === this.expandedId
                })
                .onClick(() => { this.toggleExpand(entry.dna) })
              }
            }, (entry: DnaEntry) => entry.dna)
          }

          // 底部留白
          Row().height(24)
        }
        .width('100%')
        .padding({ left: 12, right: 12 })
      }
      .layoutWeight(1)
      .scrollable(ScrollDirection.Vertical)
      .scrollBar(BarState.Auto)
    }
    .width('100%').height('100%')
    .backgroundColor(Constants.COLORS.BG_PRIMARY)
  }
}

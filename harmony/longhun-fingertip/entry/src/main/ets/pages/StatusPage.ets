// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { Constants } from '../utils/Constants'
import { SystemStatus, EngineInfo, ConnectionState } from '../models/Types'
import { ApiClient } from '../services/ApiClient'
import { GuanlanService } from '../services/GuanlanService'
import { AntennaService } from '../services/AntennaService'
import { StatusCard } from '../components/StatusCard'
import { HeaderBar } from '../components/HeaderBar'
import { LoadingView } from '../components/LoadingView'

/**
 * 龍魂·指尖 — 系统状态页
 * 鲲鹏健康·引擎矩阵·断路器·五行平衡
 */
@Component
export struct StatusPage {
  private apiClient: ApiClient = new ApiClient()
  private guanlanService: GuanlanService = new GuanlanService(this.apiClient)
  private antennaService: AntennaService = new AntennaService(this.apiClient)

  @State systemStatus: SystemStatus = new SystemStatus()
  @State engines: EngineInfo[] = []
  @State wuxingData: Record<string, number> = {}
  @State meshData: Record<string, string> = {}
  @State isLoading: boolean = true
  @State connectionState: ConnectionState = ConnectionState.OFFLINE
  @State lastRefresh: string = ''
  @State errorMsg: string = ''

  async aboutToAppear(): Promise<void> {
    await this.refreshAll()
  }

  async refreshAll(): Promise<void> {
    this.isLoading = true
    this.errorMsg = ''

    try {
      const [status, engineList, wuxing, mesh] = await Promise.all([
        this.guanlanService.getSystemStatus(),
        this.guanlanService.listEngines(),
        this.antennaService.getWuxing(),
        this.antennaService.getMesh()
      ])

      this.systemStatus = status
      this.engines = engineList
      this.wuxingData = wuxing ?? {}
      this.meshData = mesh ?? {}
      this.connectionState = ConnectionState.ONLINE
      this.lastRefresh = new Date().toLocaleTimeString()
    } catch (err) {
      this.errorMsg = '无法连接鲲鹏'
      this.connectionState = ConnectionState.OFFLINE
    } finally {
      this.isLoading = false
    }
  }

  /** 格式化时间 */
  formatUptime(seconds: number): string {
    const d = Math.floor(seconds / 86400)
    const h = Math.floor((seconds % 86400) / 3600)
    const m = Math.floor((seconds % 3600) / 60)
    if (d > 0) return `${d}天${h}时`
    if (h > 0) return `${h}时${m}分`
    return `${m}分钟`
  }

  getConnectionColor(): string {
    return this.connectionState === ConnectionState.ONLINE ? Constants.COLORS.GREEN : Constants.COLORS.RED
  }

  build() {
    Column() {
      HeaderBar({
        title: '系统状态',
        subtitle: this.connectionState === ConnectionState.ONLINE ? `刷新: ${this.lastRefresh}` : '离线',
        connectionColor: this.getConnectionColor()
      })

      if (this.isLoading) {
        LoadingView({ message: '正在探测鲲鹏健康...' })
      } else {
        Scroll() {
          Column() {
            // ── 系统资源 ──
            Text('💻 系统资源')
              .fontSize(14).fontColor(Constants.COLORS.GOLD).fontWeight(FontWeight.Bold)
              .padding({ left: 4, top: 16, bottom: 8 })

            Row() {
              StatusCard({
                label: 'CPU',
                value: this.systemStatus.cpu_percent.toFixed(0),
                unit: '%',
                percent: this.systemStatus.cpu_percent,
                icon: '⚙️',
                color: this.systemStatus.cpu_percent > 80 ? Constants.COLORS.RED : Constants.COLORS.GREEN
              })
              StatusCard({
                label: '内存',
                value: this.systemStatus.memory_percent.toFixed(0),
                unit: '%',
                percent: this.systemStatus.memory_percent,
                icon: '🧠',
                color: this.systemStatus.memory_percent > 80 ? Constants.COLORS.RED : Constants.COLORS.GREEN
              })
            }
            .width('100%')
            .justifyContent(FlexAlign.SpaceBetween)
            .margin({ bottom: 8 })

            Row() {
              StatusCard({
                label: '磁盘',
                value: this.systemStatus.disk_percent.toFixed(0),
                unit: '%',
                percent: this.systemStatus.disk_percent,
                icon: '💾',
                color: this.systemStatus.disk_percent > 80 ? Constants.COLORS.RED : Constants.COLORS.GREEN
              })
              StatusCard({
                label: '运行时间',
                value: this.formatUptime(this.systemStatus.uptime_seconds),
                icon: '⏱️',
                color: Constants.COLORS.BLUE
              })
            }
            .width('100%')
            .justifyContent(FlexAlign.SpaceBetween)

            // ── 人格引擎 ──
            Text('🔄 人格引擎')
              .fontSize(14).fontColor(Constants.COLORS.GOLD).fontWeight(FontWeight.Bold)
              .padding({ left: 4, top: 20, bottom: 8 })

            Row() {
              StatusCard({
                label: '活跃人格',
                value: `${this.systemStatus.active_personas}`,
                icon: '👥',
                color: Constants.COLORS.BLUE
              })
              StatusCard({
                label: '引擎健康',
                value: `${this.systemStatus.engines_healthy}/${this.systemStatus.engines_total}`,
                icon: '🏥',
                color: this.systemStatus.engines_healthy === this.systemStatus.engines_total
                  ? Constants.COLORS.GREEN : Constants.COLORS.GOLD
              })
            }
            .width('100%')
            .justifyContent(FlexAlign.SpaceBetween)

            // ── 断路器 ──
            Row() {
              Circle({ width: 8, height: 8 })
                .fill(this.systemStatus.circuit_breaker_tripped ? Constants.COLORS.RED : Constants.COLORS.GREEN)
              Text(this.systemStatus.circuit_breaker_tripped ? '断路器触发 ⚠️' : '断路器正常')
                .fontSize(12).fontColor(Constants.COLORS.TEXT_SECONDARY).margin({ left: 6 })
            }
            .width('100%').padding({ left: 4, top: 4 })

            // ── 五行平衡 ──
            if (Object.keys(this.wuxingData).length > 0) {
              Text('☯ 五行平衡')
                .fontSize(14).fontColor(Constants.COLORS.GOLD).fontWeight(FontWeight.Bold)
                .padding({ left: 4, top: 20, bottom: 8 })

              Row() {
                ForEach(Object.entries(this.wuxingData), ([k, v]: [string, number]) => {
                  Column() {
                    Text(this.getWuxingEmoji(k))
                      .fontSize(16)
                    Text(k)
                      .fontSize(8).fontColor(Constants.COLORS.TEXT_DIM)
                    Text(`${v}`)
                      .fontSize(11).fontColor(Constants.COLORS.TEXT_PRIMARY).fontWeight(FontWeight.Bold)
                  }
                  .width('18%')
                  .alignItems(HorizontalAlign.Center)
                })
              }
              .width('100%')
              .justifyContent(FlexAlign.SpaceEvenly)
            }

            // ── 引擎列表 ──
            if (this.engines.length > 0) {
              Text('🔌 已注册引擎')
                .fontSize(14).fontColor(Constants.COLORS.GOLD).fontWeight(FontWeight.Bold)
                .padding({ left: 4, top: 20, bottom: 8 })

              ForEach(this.engines.slice(0, 6), (engine: EngineInfo) => {
                Row() {
                  Circle({ width: 6, height: 6 })
                    .fill(engine.status === 'healthy' ? Constants.COLORS.GREEN : Constants.COLORS.GOLD)
                    .margin({ right: 8 })
                  Text(engine.name)
                    .fontSize(12).fontColor(Constants.COLORS.TEXT_PRIMARY).layoutWeight(1)
                  Text(engine.type === 'local' ? '本地' : '☁️')
                    .fontSize(10).fontColor(Constants.COLORS.TEXT_DIM)
                  Text(engine.version)
                    .fontSize(10).fontColor(Constants.COLORS.TEXT_DIM).margin({ left: 6 })
                }
                .width('100%').padding({ top: 4, bottom: 4, left: 4 })
              })
            }

            // ── 刷新按钮 ──
            Button('🔄 刷新状态')
              .fontSize(13).fontColor(Constants.COLORS.GOLD)
              .backgroundColor(Constants.COLORS.BG_CARD)
              .border({ width: 1, color: Constants.COLORS.BORDER_GOLD })
              .borderRadius(20)
              .margin({ top: 24, bottom: 24 })
              .padding({ left: 20, right: 20, top: 8, bottom: 8 })
              .onClick(() => { this.refreshAll() })

            // ── 错误提示 ──
            if (this.errorMsg) {
              Text(`⚠️ ${this.errorMsg}`)
                .fontSize(12).fontColor(Constants.COLORS.RED)
                .padding({ top: 8 })
            }
          }
          .width('100%')
          .padding({ left: 16, right: 16 })
        }
        .layoutWeight(1)
        .scrollable(ScrollDirection.Vertical)
      }
    }
    .width('100%').height('100%')
    .backgroundColor(Constants.COLORS.BG_PRIMARY)
  }

  private getWuxingEmoji(name: string): string {
    switch (name) {
      case '金': return '🔔'
      case '木': return '🌳'
      case '水': return '💧'
      case '火': return '🔥'
      case '土': return '⛰️'
      default: return '☯'
    }
  }
}

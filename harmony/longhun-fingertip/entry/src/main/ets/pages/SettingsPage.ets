// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { Constants } from '../utils/Constants'
import { ServerConfig, ConnectionState } from '../models/Types'
import { ApiClient } from '../services/ApiClient'
import { XiaoyiService } from '../services/XiaoyiService'
import { CacheService } from '../services/CacheService'
import { HeaderBar } from '../components/HeaderBar'

/**
 * 龍魂·指尖 — 设置页
 * 服务器连接·确认码·缓存管理·关于
 */
@Component
export struct SettingsPage {
  private apiClient: ApiClient = new ApiClient()
  private cacheService: CacheService = new CacheService()

  @State serverHost: string = Constants.DEFAULT_HOST
  @State confirmCode: string = Constants.CONFIRM_CODE
  @State cacheCount: number = 0
  @State connectionState: ConnectionState = ConnectionState.OFFLINE
  @State isTesting: boolean = false
  @State testResult: string = ''

  async aboutToAppear(): Promise<void> {
    this.cacheCount = this.cacheService.count()

    // 测试连接
    await this.testConnection()
  }

  async testConnection(): Promise<void> {
    this.isTesting = true
    this.testResult = ''

    const xiaoyiService = new XiaoyiService(this.apiClient)
    const healthy = await xiaoyiService.health()

    this.connectionState = healthy ? ConnectionState.ONLINE : ConnectionState.OFFLINE
    this.testResult = healthy ? '✅ 鲲鹏在线' : '❌ 连接失败'
    this.isTesting = false
  }

  clearCache(): void {
    this.cacheService.clear()
    this.cacheCount = 0
  }

  getConnectionColor(): string {
    return this.connectionState === ConnectionState.ONLINE ? Constants.COLORS.GREEN : Constants.COLORS.RED
  }

  build() {
    Column() {
      HeaderBar({
        title: '设置',
        subtitle: '连接配置 · 数据管理',
        connectionColor: this.getConnectionColor()
      })

      Scroll() {
        Column() {
          // ── 服务器配置 ──
          Text('🔗 鲲鹏连接')
            .fontSize(14).fontColor(Constants.COLORS.GOLD).fontWeight(FontWeight.Bold)
            .padding({ left: 4, top: 16, bottom: 8 })

          // 服务器地址
          Column() {
            Row() {
              Text('服务器地址')
                .fontSize(12).fontColor(Constants.COLORS.TEXT_SECONDARY)
            }
            .width('100%').padding({ bottom: 4 })

            TextInput({ text: this.serverHost })
              .width('100%')
              .height(44)
              .backgroundColor(Constants.COLORS.BG_CARD)
              .borderRadius(8)
              .border({ width: 1, color: Constants.COLORS.BORDER })
              .padding({ left: 14 })
              .fontSize(14)
              .fontColor(Constants.COLORS.TEXT_PRIMARY)
              .onChange((value: string) => { this.serverHost = value })
          }
          .width('100%')
          .padding(12)
          .backgroundColor(Constants.COLORS.BG_CARD)
          .borderRadius(10)
          .border({ width: 1, color: Constants.COLORS.BORDER })
          .margin({ bottom: 12 })

          // 确认码
          Column() {
            Row() {
              Text('确认码 (只读)')
                .fontSize(12).fontColor(Constants.COLORS.TEXT_SECONDARY)
            }
            .width('100%').padding({ bottom: 4 })

            TextInput({ text: this.confirmCode })
              .width('100%')
              .height(44)
              .backgroundColor(Constants.COLORS.BG_CARD)
              .borderRadius(8)
              .border({ width: 1, color: Constants.COLORS.BORDER_GOLD })
              .padding({ left: 14 })
              .fontSize(12)
              .fontColor(Constants.COLORS.GOLD_DIM)
              .enabled(false)
          }
          .width('100%')
          .padding(12)
          .backgroundColor(Constants.COLORS.BG_CARD)
          .borderRadius(10)
          .border({ width: 1, color: Constants.COLORS.BORDER })
          .margin({ bottom: 12 })

          // 测试连接按钮
          Row() {
            Button(this.isTesting ? '检测中...' : '🔄 测试连接')
              .fontSize(13).fontColor(Constants.COLORS.GOLD)
              .backgroundColor(Constants.COLORS.BG_CARD)
              .border({ width: 1, color: Constants.COLORS.BORDER_GOLD })
              .borderRadius(20)
              .padding({ left: 16, right: 16, top: 8, bottom: 8 })
              .enabled(!this.isTesting)
              .onClick(() => { this.testConnection() })

            if (this.testResult) {
              Text(this.testResult)
                .fontSize(12)
                .fontColor(this.connectionState === ConnectionState.ONLINE ? Constants.COLORS.GREEN : Constants.COLORS.RED)
                .margin({ left: 12 })
            }
          }
          .width('100%')
          .padding({ left: 4 })
          .margin({ bottom: 20 })

          // ── 端口配置 ──
          Text('🔌 服务端口')
            .fontSize(14).fontColor(Constants.COLORS.GOLD).fontWeight(FontWeight.Bold)
            .padding({ left: 4, top: 8, bottom: 8 })

          Column() {
            ForEach([
              { name: '知识中枢', port: '8766' },
              { name: '蚁触·八门', port: '8769' },
              { name: '观澜路由', port: '8770' },
              { name: '小艺桥接', port: '8799' }
            ], (item: { name: string, port: string }) => {
              Row() {
                Text(item.name)
                  .fontSize(12).fontColor(Constants.COLORS.TEXT_SECONDARY).layoutWeight(1)
                Text(`:${item.port}`)
                  .fontSize(12).fontColor(Constants.COLORS.GOLD_DIM)
              }
              .width('100%').padding({ top: 6, bottom: 6 })
            })
          }
          .width('100%')
          .padding(12)
          .backgroundColor(Constants.COLORS.BG_CARD)
          .borderRadius(10)
          .border({ width: 1, color: Constants.COLORS.BORDER })
          .margin({ bottom: 20 })

          // ── 缓存管理 ──
          Text('💾 离线缓存')
            .fontSize(14).fontColor(Constants.COLORS.GOLD).fontWeight(FontWeight.Bold)
            .padding({ left: 4, top: 8, bottom: 8 })

          Row() {
            Text(`已缓存 ${this.cacheCount} 条DNA记录`)
              .fontSize(12).fontColor(Constants.COLORS.TEXT_SECONDARY)
            Blank()
            Button('清空缓存')
              .fontSize(11).fontColor(Constants.COLORS.RED)
              .backgroundColor(Constants.COLORS.BG_CARD)
              .border({ width: 1, color: 'rgba(255, 68, 68, 0.3)' })
              .borderRadius(12)
              .height(28)
              .padding({ left: 12, right: 12 })
              .onClick(() => { this.clearCache() })
          }
          .width('100%')
          .padding(12)
          .backgroundColor(Constants.COLORS.BG_CARD)
          .borderRadius(10)
          .border({ width: 1, color: Constants.COLORS.BORDER })
          .margin({ bottom: 20 })

          // ── 关于 ──
          Text('ℹ️ 关于')
            .fontSize(14).fontColor(Constants.COLORS.GOLD).fontWeight(FontWeight.Bold)
            .padding({ left: 4, top: 8, bottom: 8 })

          Column() {
            Text('龍魂·指尖 v1.0')
              .fontSize(13).fontColor(Constants.COLORS.GOLD).fontWeight(FontWeight.Medium)
            Text('龍魂帝国鸿蒙入口 · 三步走第一步')
              .fontSize(11).fontColor(Constants.COLORS.TEXT_SECONDARY).padding({ top: 4, bottom: 8 })
            Text('创作者：龍芯北辰 UID9622')
              .fontSize(10).fontColor(Constants.COLORS.TEXT_DIM)
            Text(`DNA: ${Constants.DNA_PREFIX}丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.0`)
              .fontSize(8).fontColor(Constants.COLORS.GOLD_DIM).padding({ top: 4 })
              .maxLines(2)
            Text(`${Constants.CONFIRM_CODE}`)
              .fontSize(7).fontColor(Constants.COLORS.TEXT_DIM).padding({ top: 2 })
          }
          .width('100%')
          .alignItems(HorizontalAlign.Center)
          .padding(20)
          .backgroundColor(Constants.COLORS.BG_CARD)
          .borderRadius(10)
          .border({ width: 1, color: Constants.COLORS.BORDER })
          .margin({ bottom: 24 })
        }
        .width('100%')
        .padding({ left: 16, right: 16 })
      }
      .layoutWeight(1)
      .scrollable(ScrollDirection.Vertical)
    }
    .width('100%').height('100%')
    .backgroundColor(Constants.COLORS.BG_PRIMARY)
  }
}

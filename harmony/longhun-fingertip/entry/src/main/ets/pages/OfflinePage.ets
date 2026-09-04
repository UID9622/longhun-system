// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-离线模式-v1.1
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

/**
 * 离线模式页面 v1.1
 *
 * 断网能力（v1.1端侧能力修正）：
 * - ✅ 本地DNA查询与展示（缓存）
 * - ✅ 本地审计标签展示（缓存）
 * - ✅ 本地蚂蚁触神经网路由判断（种子人格）
 * - ❌ DNA生成/审计标签生成（仍走鲲鹏API）
 *
 * 数据主权不变：DNA注册表·审计日志·记忆库原始数据不传输。
 */

import { CnsHJsonParser, DnaRegistryEntry, DnaQueryFilter, LayerLevel, AuditColor, AuditLabel } from '../cnsh/JsonParser'
import { WenxinPersona, IntentType, RouteSuggestion } from '../personas/WenxinPersona'
import { BlackAngelPersona, SecurityLevel } from '../personas/BlackAngelPersona'
import { BaobaoPersona, EmotionState } from '../personas/BaobaoPersona'
import { LocalDataService, AuditLogEntry } from '../services/LocalDataService'
import { Constants } from '../utils/Constants'
import { HeaderBar } from '../components/HeaderBar'
import { LoadingView } from '../components/LoadingView'
import promptAction from '@ohos.promptAction'
import router from '@ohos.router'

@Component
export struct OfflinePage {
  @State dnaLoaded: boolean = false
  @State dnaCount: number = 0
  @State dnaLoadedAt: string = ''
  @State searchKeyword: string = ''
  @State filterLayer: string = 'ALL'
  @State filterStatus: string = 'ALL'
  @State searchResults: DnaRegistryEntry[] = []
  @State resultCount: number = 0
  @State totalCount: number = 0
  @State isLoading: boolean = false
  @State showDnaDetail: boolean = false
  @State selectedDna: DnaRegistryEntry | null = null
  @State auditLogs: AuditLogEntry[] = []
  @State showAuditTab: boolean = false
  @State securityCheckInput: string = ''
  @State securityResult: string = ''

  private parser: CnsHJsonParser = new CnsHJsonParser()
  private localData: LocalDataService = LocalDataService.getInstance()
  private wenxin: WenxinPersona = new WenxinPersona()
  private blackAngel: BlackAngelPersona = new BlackAngelPersona()
  private baobao: BaobaoPersona = new BaobaoPersona()

  aboutToAppear(): void {
    this.loadLocalDna()
    this.loadAuditLogs()
  }

  /** 加载本地DNA注册表 */
  async loadLocalDna(): Promise<void> {
    this.isLoading = true
    try {
      const jsonStr = await this.localData.loadDnaRegistry()
      if (jsonStr) {
        const registry = this.parser.loadRegistry(jsonStr)
        if (registry) {
          this.dnaLoaded = true
          this.dnaCount = registry.entries.length
          this.totalCount = registry.entries.length
          const loadedAt = await this.localData.getRegistryLoadedAt()
          this.dnaLoadedAt = loadedAt > 0 ? new Date(loadedAt).toLocaleString() : '未知'
          // 初始加载全部
          const result = this.parser.query({})
          this.searchResults = result.entries.slice(0, 50)
          this.resultCount = result.matched
        }
      }
    } catch (err) {
      console.error(`[OfflinePage] DNA加载失败: ${JSON.stringify(err)}`)
    } finally {
      this.isLoading = false
    }
  }

  /** 加载审计日志 */
  async loadAuditLogs(): Promise<void> {
    try {
      this.auditLogs = await this.localData.getAuditLogs()
    } catch (err) {
      console.error(`[OfflinePage] 审计日志加载失败: ${JSON.stringify(err)}`)
    }
  }

  /** DNA搜索 */
  onSearch(): void {
    if (!this.dnaLoaded) {
      promptAction.showToast({ message: 'DNA注册表未加载', duration: 2000 })
      return
    }

    const filter: DnaQueryFilter = {}
    if (this.searchKeyword.trim()) filter.keyword = this.searchKeyword.trim()
    if (this.filterLayer !== 'ALL') filter.layer = this.filterLayer as LayerLevel
    if (this.filterStatus !== 'ALL') filter.status = this.filterStatus as AuditColor

    const result = this.parser.query(filter)
    this.searchResults = result.entries.slice(0, 50)
    this.resultCount = result.matched
    this.totalCount = result.total

    if (result.matched === 0) {
      promptAction.showToast({ message: '未找到匹配的DNA条目', duration: 2000 })
    }
  }

  /** 显示DNA详情 */
  showDetail(entry: DnaRegistryEntry): void {
    this.selectedDna = entry
    this.showDnaDetail = true
  }

  /** 按层过滤 */
  filterByLayer(layer: string): void {
    this.filterLayer = layer
    this.onSearch()
  }

  /** 按状态过滤 */
  filterByStatus(status: string): void {
    this.filterStatus = status
    this.onSearch()
  }

  /** 安全检查 */
  onSecurityCheck(): void {
    const input = this.securityCheckInput.trim()
    if (!input) return

    const result = this.blackAngel.think(input)
    const wResult = this.wenxin.think(input)
    const bResult = this.baobao.think(input)

    const intent = wResult.data?.['intent'] ?? 'UNKNOWN'
    const route = wResult.data?.['route'] ?? 'REMOTE'
    const level = result.data?.['level'] ?? 'SAFE'

    this.securityResult = [
      `【意图】${intent} → 路由:${route}`,
      `【安全】${level} → ${result.reasoning}`,
      `【情感】${bResult.data?.['emotion'] ?? 'NEUTRAL'} → ${bResult.reasoning}`,
      `【审计】${result.audit}`,
    ].join('\n')
  }

  build() {
    Column() {
      HeaderBar({ title: '🧬 离线模式' })

      if (this.isLoading) {
        LoadingView()
      } else {
        // ── 状态概览 ──
        Row() {
          this.StatusBadge({ label: 'DNA', value: this.dnaLoaded ? `${this.dnaCount}条` : '未加载', color: this.dnaLoaded ? '#00FF88' : '#FF4444' })
          this.StatusBadge({ label: '审计', value: `${this.auditLogs.length}条`, color: '#FFD700' })
          this.StatusBadge({ label: '加载时间', value: this.dnaLoadedAt || '—', color: '#AAAAAA' })
        }
        .width('100%')
        .padding(12)
        .justifyContent(FlexAlign.SpaceAround)

        Tabs({ barPosition: BarPosition.Start }) {
          // ── Tab 1: DNA查询 ──
          TabContent() {
            this.DnaQueryTab()
          }.tabBar('🔍 DNA查询')

          // ── Tab 2: 审计日志 ──
          TabContent() {
            this.AuditLogTab()
          }.tabBar('📋 审计日志')

          // ── Tab 3: 安全检查 ──
          TabContent() {
            this.SecurityCheckTab()
          }.tabBar('🛡️ 安全检查')
        }
        .barHeight(40)
        .barMode(BarMode.Fixed)
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor(Constants.COLORS.BG_PRIMARY)
  }

  @Builder StatusBadge(badge: { label: string; value: string; color: string }) {
    Column() {
      Text(badge.value)
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .fontColor(badge.color)
      Text(badge.label)
        .fontSize(11)
        .fontColor(Constants.COLORS.TEXT_SECONDARY)
        .margin({ top: 2 })
    }
  }

  @Builder DnaQueryTab() {
    Column() {
      // 搜索栏
      Row() {
        TextInput({ placeholder: '搜索DNA·模块·文件...', text: this.searchKeyword })
          .onChange((value: string) => { this.searchKeyword = value })
          .layoutWeight(1)
          .height(40)
          .backgroundColor(Constants.COLORS.BG_CARD)
          .borderRadius(8)

        Button('搜索')
          .onClick(() => this.onSearch())
          .height(40)
          .fontSize(14)
          .margin({ left: 8 })
      }
      .width('100%')
      .padding({ left: 12, right: 12, top: 8 })

      // 过滤器
      Row() {
        Text('层:').fontSize(12).fontColor(Constants.COLORS.TEXT_SECONDARY)
        Button(this.filterLayer).onClick(() => this.cycleFilter('layer')).height(28).fontSize(11)
        Text('状态:').fontSize(12).fontColor(Constants.COLORS.TEXT_SECONDARY).margin({ left: 8 })
        Button(this.filterStatus).onClick(() => this.cycleFilter('status')).height(28).fontSize(11)
        Blank()
        Text(`匹配 ${this.resultCount}/${this.totalCount}`)
          .fontSize(11)
          .fontColor(Constants.COLORS.TEXT_SECONDARY)
      }
      .width('100%')
      .padding({ left: 12, right: 12, top: 4 })

      // 结果列表
      if (this.searchResults.length === 0) {
        Column() {
          Text(this.dnaLoaded ? '没有匹配的DNA条目' : 'DNA注册表未加载')
            .fontSize(14)
            .fontColor(Constants.COLORS.TEXT_SECONDARY)
            .margin({ top: 40 })
          if (!this.dnaLoaded) {
            Button('从鲲鹏同步DNA注册表')
              .onClick(() => router.pushUrl({ url: 'pages/DnaPage' }))
              .margin({ top: 12 })
              .fontSize(13)
          }
        }
        .width('100%')
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
      } else {
        List() {
          ForEach(this.searchResults, (entry: DnaRegistryEntry) => {
            ListItem() {
              Row() {
                Text(entry.status)
                  .fontSize(20)
                  .margin({ right: 8 })
                Column() {
                  Text(entry.module)
                    .fontSize(14)
                    .fontColor(Constants.COLORS.TEXT_PRIMARY)
                    .maxLines(1)
                    .textOverflow({ overflow: TextOverflow.Ellipsis })
                  Text(`${entry.file} · v${entry.version}`)
                    .fontSize(11)
                    .fontColor(Constants.COLORS.TEXT_SECONDARY)
                    .maxLines(1)
                    .textOverflow({ overflow: TextOverflow.Ellipsis })
                }
                .layoutWeight(1)
                .alignItems(HorizontalAlign.Start)

                Text(this.parser.getLayerName(entry.layer))
                  .fontSize(10)
                  .fontColor(Constants.COLORS.BLUE)
                  .padding(4)
                  .border({ width: 1, color: Constants.COLORS.BLUE, radius: 4 })
              }
              .width('100%')
              .padding(10)
            }
            .onClick(() => this.showDetail(entry))
          })
        }
        .layoutWeight(1)
        .width('100%')
      }

      // DNA详情弹窗
      if (this.showDnaDetail && this.selectedDna) {
        this.DnaDetailDialog()
      }
    }
    .width('100%')
    .height('100%')
  }

  @Builder DnaDetailDialog() {
    Column() {
      Column() {
        Text(this.selectedDna!.dna)
          .fontSize(13)
          .fontColor(Constants.COLORS.GOLD)
          .fontFamily('monospace')
          .margin({ bottom: 8 })

        Row() { Text('文件:').fontSize(12).fontColor(Constants.COLORS.TEXT_SECONDARY); Text(this.selectedDna!.file).fontSize(12).margin({ left: 4 }) }
        Row() { Text('模块:').fontSize(12).fontColor(Constants.COLORS.TEXT_SECONDARY); Text(this.selectedDna!.module).fontSize(12).margin({ left: 4 }) }
        Row() { Text('版本:').fontSize(12).fontColor(Constants.COLORS.TEXT_SECONDARY); Text(this.selectedDna!.version).fontSize(12).margin({ left: 4 }) }
        Row() { Text('层:').fontSize(12).fontColor(Constants.COLORS.TEXT_SECONDARY); Text(this.parser.getLayerName(this.selectedDna!.layer)).fontSize(12).margin({ left: 4 }) }
        Row() { Text('权重:').fontSize(12).fontColor(Constants.COLORS.TEXT_SECONDARY); Text(`${this.selectedDna!.weight}`).fontSize(12).margin({ left: 4 }) }
        Row() { Text('审计:').fontSize(12).fontColor(Constants.COLORS.TEXT_SECONDARY); Text(`${this.selectedDna!.status} ${this.parser.getAuditLabel(this.selectedDna!.status).label}`).fontSize(12).margin({ left: 4 }) }

        Button('关闭')
          .onClick(() => { this.showDnaDetail = false; this.selectedDna = null })
          .margin({ top: 12 })
          .fontSize(13)
      }
      .padding(16)
      .backgroundColor(Constants.COLORS.BG_CARD)
      .borderRadius(12)
      .width('90%')
    }
    .width('100%')
    .height('100%')
    .position({ x: 0, y: 0 })
    .backgroundColor('rgba(0,0,0,0.8)')
    .justifyContent(FlexAlign.Center)
    .onClick(() => { this.showDnaDetail = false; this.selectedDna = null })
  }

  @Builder AuditLogTab() {
    Column() {
      if (this.auditLogs.length === 0) {
        Column() {
          Text('暂无审计日志')
            .fontSize(14)
            .fontColor(Constants.COLORS.TEXT_SECONDARY)
        }
        .width('100%')
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
      } else {
        List() {
          ForEach(this.auditLogs, (log: AuditLogEntry) => {
            ListItem() {
              Row() {
                Text(log.audit_color)
                  .fontSize(18)
                  .margin({ right: 8 })
                Column() {
                  Row() {
                    Text(`[${log.persona}]`)
                      .fontSize(11)
                      .fontColor(Constants.COLORS.GOLD)
                    Text(log.action)
                      .fontSize(13)
                      .fontColor(Constants.COLORS.TEXT_PRIMARY)
                      .margin({ left: 4 })
                  }
                  Text(log.timestamp)
                    .fontSize(10)
                    .fontColor(Constants.COLORS.TEXT_SECONDARY)
                }
                .alignItems(HorizontalAlign.Start)
                .layoutWeight(1)
              }
              .width('100%')
              .padding({ left: 12, right: 12, top: 6, bottom: 6 })
            }
          })
        }
        .layoutWeight(1)
        .width('100%')
      }
    }
    .width('100%')
    .height('100%')
  }

  @Builder SecurityCheckTab() {
    Column() {
      Text('本地安全检查（种子人格）')
        .fontSize(13)
        .fontColor(Constants.COLORS.TEXT_SECONDARY)
        .padding({ top: 12, bottom: 8 })

      Text('输入文本，端侧三人格联合判定：文心(意图) + 宝宝(情感) + 黑天使(安全)')
        .fontSize(11)
        .fontColor(Constants.COLORS.TEXT_SECONDARY)
        .padding({ left: 12, right: 12, bottom: 8 })

      TextInput({ placeholder: '输入要检查的文本...', text: this.securityCheckInput })
        .onChange((value: string) => { this.securityCheckInput = value })
        .height(60)
        .backgroundColor(Constants.COLORS.BG_CARD)
        .borderRadius(8)
        .margin({ left: 12, right: 12 })
        .maxLength(500)

      Button('三人格联合检查')
        .onClick(() => this.onSecurityCheck())
        .margin({ top: 12, left: 12 })
        .fontSize(13)

      if (this.securityResult) {
        Text(this.securityResult)
          .fontSize(12)
          .fontColor(Constants.COLORS.TEXT_PRIMARY)
          .fontFamily('monospace')
          .backgroundColor(Constants.COLORS.BG_CARD)
          .borderRadius(8)
          .padding(12)
          .margin(12)
          .width('calc(100% - 24px)')
      }

      Blank()
    }
    .width('100%')
    .height('100%')
  }

  /** 循环切换过滤 */
  cycleFilter(type: string): void {
    if (type === 'layer') {
      const layers = ['ALL', 'L0_ETERNAL', 'L1_SEASONAL', 'L2_DECISION', 'L3_GENERATIONAL', 'L4_INSTANT']
      const idx = layers.indexOf(this.filterLayer)
      this.filterLayer = layers[(idx + 1) % layers.length]
    } else if (type === 'status') {
      const statuses = ['ALL', '🟢', '🟡', '🔴']
      const idx = statuses.indexOf(this.filterStatus)
      this.filterStatus = statuses[(idx + 1) % statuses.length]
    }
    this.onSearch()
  }
}

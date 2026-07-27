// DNA: #龍芯⚡️丙午·癸未·甲子·既济-鸿蒙兼容-指尖-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { Constants } from '../utils/Constants'
import { ChatMessage, ConnectionState } from '../models/Types'
import { ApiClient } from '../services/ApiClient'
import { XiaoyiService } from '../services/XiaoyiService'
import { GuanlanService } from '../services/GuanlanService'
import { ChatBubble } from '../components/ChatBubble'
import { HeaderBar } from '../components/HeaderBar'
import { LoadingView } from '../components/LoadingView'

/**
 * 龍魂·指尖 — AI对话页
 * 核心功能: 21人格集群对话·离线消息缓存·DNA追溯
 */
@Component
export struct ChatPage {
  // ── 服务 ──
  private apiClient: ApiClient = new ApiClient()
  private xiaoyiService: XiaoyiService = new XiaoyiService(this.apiClient)
  private guanlanService: GuanlanService = new GuanlanService(this.apiClient)

  // ── 状态 ──
  @State messages: ChatMessage[] = []
  @State inputText: string = ''
  @State isLoading: boolean = false
  @State connectionState: ConnectionState = ConnectionState.OFFLINE
  @State isInitializing: boolean = true

  // ── 生命周期 ──
  async aboutToAppear(): Promise<void> {
    // 初始欢迎消息
    this.messages.push({
      id: 'welcome',
      role: 'assistant',
      content: '龍魂帝国·鸿蒙指尖。\n我是鲲鹏上的21人格集群。干点啥？',
      persona: '文心',
      dna: `${Constants.DNA_PREFIX}丙午·癸未·甲子·既济-指尖-启动-v1.0`,
      timestamp: Date.now()
    } as ChatMessage)

    await this.checkConnection()
  }

  // ── 连接检测 ──
  async checkConnection(): Promise<void> {
    this.isInitializing = true
    this.connectionState = ConnectionState.RECONNECTING

    const healthy = await this.xiaoyiService.health()
    if (healthy) {
      this.connectionState = ConnectionState.ONLINE
    } else {
      this.connectionState = ConnectionState.OFFLINE
    }
    this.isInitializing = false
  }

  // ── 发送消息 ──
  async sendMessage(): Promise<void> {
    const text = this.inputText.trim()
    if (!text || this.isLoading) return

    // 用户消息入列
    const userMsg: ChatMessage = {
      id: `user_${Date.now()}`,
      role: 'user',
      content: text,
      timestamp: Date.now()
    }
    this.messages = [...this.messages, userMsg]
    this.inputText = ''
    this.isLoading = true

    // 调用小艺桥接 → 路由到相应人格
    try {
      const reply = await this.xiaoyiService.chat(text, this.messages)
      this.messages = [...this.messages, reply]

      if (!reply.isError) {
        this.connectionState = ConnectionState.ONLINE
      }
    } catch (err) {
      const errorMsg: ChatMessage = {
        id: `error_${Date.now()}`,
        role: 'assistant',
        content: '网络不通。鲲鹏可能在沉睡。\n检查一下连接，或稍后再试。',
        persona: '系统',
        timestamp: Date.now(),
        isError: true
      }
      this.messages = [...this.messages, errorMsg]
      this.connectionState = ConnectionState.OFFLINE
    } finally {
      this.isLoading = false
    }
  }

  // ── 获取连接状态颜色 ──
  getConnectionColor(): string {
    switch (this.connectionState) {
      case ConnectionState.ONLINE: return Constants.COLORS.GREEN
      case ConnectionState.RECONNECTING: return Constants.COLORS.GOLD
      default: return Constants.COLORS.RED
    }
  }

  build() {
    Column() {
      // 顶部栏
      HeaderBar({
        title: '龍魂·指尖',
        subtitle: this.connectionState === ConnectionState.ONLINE ? '21人格在线 · 鲲鹏就绪' : '离线 · 等待鲲鹏',
        connectionColor: this.getConnectionColor()
      })

      // 初始化加载
      if (this.isInitializing) {
        LoadingView({ message: '正在连接鲲鹏...' })
      } else {
        // 消息列表
        Scroll(this.scroller) {
          Column() {
            ForEach(this.messages, (msg: ChatMessage, index: number) => {
              ListItem() {
                ChatBubble({
                  message: msg,
                  isLast: index === this.messages.length - 1
                })
              }
            }, (msg: ChatMessage) => msg.id)

            // 加载中指示
            if (this.isLoading) {
              Row() {
                LoadingProgress()
                  .width(20).height(20)
                  .color(Constants.COLORS.GOLD)
                Text('龍魂在思考...').fontSize(12).fontColor(Constants.COLORS.TEXT_DIM).margin({ left: 8 })
              }
              .padding(12)
              .justifyContent(FlexAlign.Center)
            }
          }
          .width('100%')
          .padding({ left: 8, right: 8, top: 8, bottom: 8 })
        }
        .layoutWeight(1)
        .scrollable(ScrollDirection.Vertical)
        .scrollBar(BarState.Auto)
        .onAreaChange(() => {
          // 新消息自动滚到底
          this.scroller.scrollEdge(Edge.Bottom)
        })

        // 输入栏
        Row() {
          TextInput({ placeholder: '跟龍魂说点什么...', text: this.inputText })
            .layoutWeight(1)
            .height(44)
            .backgroundColor(Constants.COLORS.BG_CARD)
            .borderRadius(22)
            .border({ width: 1, color: Constants.COLORS.BORDER })
            .padding({ left: 16, right: 16 })
            .fontSize(14)
            .fontColor(Constants.COLORS.TEXT_PRIMARY)
            .placeholderColor(Constants.COLORS.TEXT_DIM)
            .onChange((value: string) => { this.inputText = value })
            .onSubmit(() => { this.sendMessage() })
            .enabled(!this.isLoading)

          Button() {
            Text(this.isLoading ? '...' : '➤')
              .fontSize(18)
              .fontColor(Constants.COLORS.BG_PRIMARY)
          }
          .width(44).height(44)
          .borderRadius(22)
          .backgroundColor(Constants.COLORS.GOLD)
          .margin({ left: 8 })
          .enabled(!this.isLoading && this.inputText.trim().length > 0)
          .onClick(() => { this.sendMessage() })
        }
        .width('100%')
        .padding({ left: 12, right: 12, top: 8, bottom: 12 })
        .backgroundColor(Constants.COLORS.BG_SECONDARY)
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor(Constants.COLORS.BG_PRIMARY)
  }

  private scroller: Scroller = new Scroller()
}

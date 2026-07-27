// DNA: #龍芯⚡️丙午·癸未·甲子·既济-编辑器落地-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: CC BY-NC-SA 4.0

import { Constants } from '../utils/Constants'
import { dnaGen } from '../utils/DnaGenerator'
import { apiClient, EditorOutput } from '../service/ApiClient'
import { InputArea } from '../components/InputArea'
import { OutputArea } from '../components/OutputArea'
import { AiToolbar } from '../components/AiToolbar'
import dataPreferences from '@ohos.data.preferences'

/**
 * 龍魂·编辑器 — 主页面
 *
 * 布局（上中下）：
 * 1. 顶部 — AI军团调度按钮栏
 * 2. 中部 — 输出展示区（AI回复+协同日志+DNA标签）
 * 3. 底部 — 输入区（多行文本+语音按钮）
 *
 * 交互流程：
 * 用户输入 → 点AI按钮 → ApiClient封装DNA请求 → POST鲲鹏
 * → 鲲鹏InterAgentBus调度人格 → 协同推理
 * → 返回结果+过程日志 → 输出区展示+自动打DNA标签
 */
@Entry
@Component
struct Index {
  // ── 输入状态 ──
  @State inputContent: string = ''
  @State isRecording: boolean = false

  // ── AI调度状态 ──
  @State isProcessing: boolean = false
  @State activeTask: string = ''

  // ── 输出状态 ──
  @State currentOutput: EditorOutput = new EditorOutput()
  @State outputHistory: EditorOutput[] = []
  @State isLogExpanded: boolean = false

  // ── 本地缓存 ──
  private prefs: dataPreferences.Preferences | null = null
  private readonly PREFS_NAME: string = 'longhun_editor'

  async aboutToAppear(): Promise<void> {
    // 初始化本地存储
    try {
      this.prefs = await dataPreferences.getPreferences(getContext(), this.PREFS_NAME)
      // 恢复草稿
      const draft = await this.prefs.get(Constants.CACHE_PREFIX_DRAFT + 'current', '') as string
      if (draft) this.inputContent = draft
    } catch (_) {
      console.warn('[编辑器] 本地存储初始化失败，继续运行')
    }
  }

  aboutToDisappear(): void {
    this.saveDraft()
  }

  /** 输入内容变化时保存草稿 */
  async onInputChange(text: string): Promise<void> {
    this.inputContent = text
    if (this.prefs) {
      try {
        await this.prefs.put(Constants.CACHE_PREFIX_DRAFT + 'current', text)
        await this.prefs.flush()
      } catch (_) {}
    }
  }

  /** 保存草稿 */
  private async saveDraft(): Promise<void> {
    if (this.prefs && this.inputContent.length > 0) {
      try {
        await this.prefs.put(Constants.CACHE_PREFIX_DRAFT + 'current', this.inputContent)
        await this.prefs.flush()
      } catch (_) {}
    }
  }

  // ══════ AI按钮点击处理 ══════

  async onAiButtonClick(task: string): Promise<void> {
    if (this.inputContent.trim().length === 0) {
      this.showEmptyError()
      return
    }

    this.isProcessing = true
    this.activeTask = task

    try {
      const response = await this.dispatchAiTask(task)
      this.handleSuccess(task, response)
    } catch (err) {
      this.handleError(task, err as Error)
    } finally {
      this.isProcessing = false
      this.activeTask = ''
      this.saveDraft()
    }
  }

  /** 分发AI任务到对应鲲鹏端点 */
  private async dispatchAiTask(task: string) {
    const content = this.inputContent.trim()

    switch (task) {
      case 'code':
        return await apiClient.inferCode(content)
      case 'copywriting':
        return await apiClient.inferCopywriting(content)
      case 'audit':
        return await apiClient.submitAudit(content)
      case 'auto_route':
        return await apiClient.autoRoute(content)
      default:
        throw new Error(`未知任务类型: ${task}`)
    }
  }

  /** 处理成功响应 */
  private handleSuccess(task: string, response: any): void {
    const config = Constants.AI_BUTTONS.find(b => b.task === task)

    const output = new EditorOutput()
    output.id = `out_${Date.now()}`
    output.task = config?.label ?? task
    output.personas = config?.personas ?? ''
    output.result = response.result ?? '(空响应)'
    output.processLog = response.process_log ?? [
      `${config?.personas ?? task} → 协同推理`,
      '返回结果'
    ]
    output.dna = response.dna ?? dnaGen.generateDisplayTag(
      config?.label ?? task,
      undefined
    )
    output.auditLevel = response.audit?.level ?? 'L3'
    output.timestamp = Date.now()
    output.isError = false

    this.currentOutput = output
    this.outputHistory = [output, ...this.outputHistory.slice(0, Constants.MAX_HISTORY_ITEMS)]
  }

  /** 处理错误 */
  private handleError(task: string, err: Error): void {
    const config = Constants.AI_BUTTONS.find(b => b.task === task)

    const output = new EditorOutput()
    output.id = `err_${Date.now()}`
    output.task = config?.label ?? task
    output.personas = config?.personas ?? ''
    output.result = ''
    output.processLog = [`${config?.personas ?? task} → 请求失败`]
    output.dna = dnaGen.generateDisplayTag('错误', undefined)
    output.auditLevel = 'L2'
    output.timestamp = Date.now()
    output.isError = true
    output.errorMessage = err.message

    this.currentOutput = output
  }

  /** 输入为空时提示 */
  private showEmptyError(): void {
    const output = new EditorOutput()
    output.id = `warn_${Date.now()}`
    output.task = '提示'
    output.personas = '系统'
    output.result = ''
    output.processLog = ['输入为空，请先输入内容']
    output.dna = dnaGen.generateDisplayTag('提示', undefined)
    output.auditLevel = 'L3'
    output.timestamp = Date.now()
    output.isError = true
    output.errorMessage = '请先输入要处理的内容'

    this.currentOutput = output
  }

  // ══════ 语音相关 ══════

  onVoiceStart(): void {
    this.isRecording = true
    console.info('[编辑器] 语音录制开始')
  }

  onVoiceStop(): void {
    this.isRecording = false
    console.info('[编辑器] 语音录制停止')
    // 语音转文字结果填入输入框（二期实现ASR）
  }

  splitMarkdown(text: string): string[] {
    if (!text) return []
    return text.split('\n').filter(l => l.trim().length > 0)
  }

  // ══════ 页面布局 ══════

  build() {
    Column() {
      // ── 顶部标题栏 ──
      this.buildTitleBar()

      // ── AI军团按钮栏 ──
      AiToolbar({
        isProcessing: this.isProcessing,
        activeButton: this.activeTask,
        onButtonClick: (task: string) => this.onAiButtonClick(task)
      })

      Divider()
        .color(Constants.COLORS.BORDER)
        .width('100%')
        .height(1)

      // ── 输出展示区（可滚动） ──
      Scroll() {
        Column() {
          // 历史输出
          if (this.outputHistory.length > 0) {
            ForEach(this.outputHistory, (item: EditorOutput, index: number) => {
              Column() {
                // 历史项显示简略信息
                if (index > 0) {
                  this.buildHistoryItem(item, index)
                }
              }
            })
          }

          // 当前输出
          if (this.outputHistory.length > 0) {
            OutputArea({
              output: this.currentOutput,
              isExpanded: this.isLogExpanded,
              toggleExpand: () => { this.isLogExpanded = !this.isLogExpanded }
            })
          }
        }
        .width('100%')
      }
      .layoutWeight(1)
      .scrollable(ScrollDirection.Vertical)
      .scrollBar(BarState.Off)

      Divider()
        .color(Constants.COLORS.BORDER)
        .width('100%')
        .height(1)

      // ── 底部输入区 ──
      InputArea({
        content: this.inputContent,
        isRecording: this.isRecording,
        contentChange: (text: string) => this.onInputChange(text),
        voiceStart: () => this.onVoiceStart(),
        voiceStop: () => this.onVoiceStop()
      })
    }
    .width('100%')
    .height('100%')
    .backgroundColor(Constants.COLORS.BG_PRIMARY)
  }

  @Builder
  buildTitleBar() {
    Row() {
      Text('🧬')
        .fontSize(18)
      Text('龍魂·编辑器')
        .fontSize(16)
        .fontColor(Constants.COLORS.GOLD)
        .fontWeight(FontWeight.Bold)
        .margin({ left: 6 })

      Blank()

      Text(`v1.0`)
        .fontSize(10)
        .fontColor(Constants.COLORS.TEXT_DIM)
    }
    .width('100%')
    .height(44)
    .padding({ left: 14, right: 14 })
    .backgroundColor(Constants.COLORS.BG_SECONDARY)
    .border({ width: { bottom: 1 }, color: Constants.COLORS.BORDER_GOLD })
  }

  @Builder
  buildHistoryItem(item: EditorOutput, index: number) {
    Row() {
      Text(`${item.task}`)
        .fontSize(11)
        .fontColor(Constants.COLORS.GOLD)
        .padding({ left: 6, right: 6, top: 2, bottom: 2 })
        .backgroundColor('rgba(255, 215, 0, 0.08)')
        .borderRadius(4)

      Text(item.result.substring(0, 40) + (item.result.length > 40 ? '...' : ''))
        .fontSize(11)
        .fontColor(Constants.COLORS.TEXT_DIM)
        .maxLines(1)
        .layoutWeight(1)
        .margin({ left: 8 })

      Text(FormattingUtil.formatTime(item.timestamp))
        .fontSize(10)
        .fontColor(Constants.COLORS.TEXT_DIM)
    }
    .width('100%')
    .padding({ left: 12, right: 12, top: 6, bottom: 6 })
    .backgroundColor(Constants.COLORS.BG_SECONDARY)
    .border({ width: { bottom: 0.5 }, color: Constants.COLORS.BORDER })
    .onClick(() => {
      this.currentOutput = item
    })
  }
}

/** 格式化工具 */
class FormattingUtil {
  static formatTime(ts: number): string {
    const d = new Date(ts)
    const h = d.getHours().toString().padStart(2, '0')
    const m = d.getMinutes().toString().padStart(2, '0')
    return `${h}:${m}`
  }
}

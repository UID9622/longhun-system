// entry/src/main/ets/components/VoiceAssistant.ets
// 龍魂 · 语音助手组件

import { voiceState, VoiceDialog, ASRStatus, TTSStatus } from '../models/VoiceModel';
import { asrEngine } from '../engine/ASREngine';
import { ttsEngine } from '../engine/TTSEngine';
import { navController } from '../navigation/NavigationController';

@Component
export struct VoiceAssistant {
  @StorageLink('voiceState') voiceState: VoiceState = voiceState;
  @State private inputText: string = '';
  @State private isListening: boolean = false;

  async handleVoiceInput(): Promise<void> {
    if (this.isListening) { await asrEngine.stopRecognition(); this.isListening = false; return; }
    this.isListening = true;
    await asrEngine.startRecognition({ continuous: false, interimResults: true });
    setTimeout(async () => {
      const result = await asrEngine.stopRecognition();
      this.isListening = false;
      if (result?.text) this.processUserInput(result.text);
    }, 5000);
  }

  handleTextInput(): void { if (!this.inputText.trim()) return; this.processUserInput(this.inputText); this.inputText = ''; }

  private processUserInput(text: string): void {
    voiceState.addDialog({ role: 'user', text });
    const intent = this.recognizeIntent(text);
    this.executeIntent(intent, text);
  }

  private recognizeIntent(text: string): { action: string; params: Record<string, any> } {
    if (text.includes('打开项目') || text.includes('查看项目')) return { action: 'navigate', params: { page: 'ProjectList' } };
    if (text.includes('里程碑') || text.includes('时间线')) return { action: 'navigate', params: { page: 'MilestoneTimeline' } };
    if (text.includes('周报')) return { action: 'navigate', params: { page: 'WeeklyReview' } };
    if (text.includes('印章')) return { action: 'navigate', params: { page: 'StampManagement' } };
    if (text.includes('设置')) return { action: 'navigate', params: { page: 'Settings' } };
    if (text.includes('退出') || text.includes('关闭')) return { action: 'exit', params: {} };
    return { action: 'chat', params: { text } };
  }

  private async executeIntent(intent: { action: string; params: Record<string, any> }, text: string): Promise<void> {
    let response = '';
    switch (intent.action) {
      case 'navigate': const page = intent.params.page; navController.push(page); response = `已打开${this.getPageName(page)}`; break;
      case 'exit': response = '正在退出应用'; break;
      default: response = `收到: ${text}。我是龍魂语音助手，可以帮您导航到各个功能页面。`; break;
    }
    voiceState.addDialog({ role: 'assistant', text: response, intent: intent.action, slots: intent.params });
    await ttsEngine.synthesize(response);
  }

  private getPageName(page: string): string {
    const names: Record<string, string> = { 'ProjectList': '项目管理', 'MilestoneTimeline': '里程碑时间线', 'WeeklyReview': '周报管理', 'StampManagement': '印章管理', 'Settings': '设置' };
    return names[page] || page;
  }

  build() {
    Column() {
      this.HeaderBuilder()
      this.DialogListBuilder()
      this.InputBuilder()
    }
    .width('100%').height('100%').backgroundColor('#0a0a0a')
  }

  @Builder
  HeaderBuilder() {
    Row() {
      Text('🤖').fontSize(24).margin({ right: 8 })
      Column() {
        Text('龍魂语音助手').fontSize(18).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        Text(this.voiceState.asrStatus === ASRStatus.IDLE ? '就绪' : this.voiceState.ttsStatus === TTSStatus.PLAYING ? '播报中...' : '工作中').fontSize(12).fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start).layoutWeight(1)
      Button() { Text(this.voiceState.isWakeWordEnabled ? '🔔' : '🔕').fontSize(18) }
      .type(ButtonType.Circle).backgroundColor('#1a1a1a').width(36).height(36).onClick(() => { this.voiceState.isWakeWordEnabled = !this.voiceState.isWakeWordEnabled; })
    }
    .width('100%').height(56).padding({ left: 16, right: 16 }).backgroundColor('#1a1a1a').border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  DialogListBuilder() {
    List() {
      ForEach(this.voiceState.dialogs, (dialog: VoiceDialog) => {
        ListItem() {
          Column() {
            Row() {
              Text(dialog.getRoleIcon()).fontSize(20).margin({ right: 8 })
              Column() {
                Text(dialog.text).fontSize(14).fontColor('#fff').width('100%')
                if (dialog.intent) { Text(`意图: ${dialog.intent}`).fontSize(11).fontColor('#666').margin({ top: 4 }) }
              }
              .alignItems(HorizontalAlign.Start).layoutWeight(1)
              .backgroundColor(dialog.role === 'user' ? 'rgba(196,30,58,0.1)' : dialog.role === 'assistant' ? 'rgba(0,255,0,0.05)' : '#1a1a1a')
              .borderRadius(8).padding(12)
            }
            .width('100%').justifyContent(dialog.role === 'user' ? FlexAlign.End : FlexAlign.Start)
          }
          .width('100%').padding({ left: 16, right: 16, top: 8, bottom: 8 })
        }
      }, (dialog: VoiceDialog) => dialog.id)
    }
    .width('100%').layoutWeight(1).scrollBar(BarState.Auto).padding({ bottom: 16 })
  }

  @Builder
  InputBuilder() {
    Row() {
      Button() { Text(this.isListening ? '⏹' : '🎤').fontSize(20).fontColor(this.isListening ? '#ff0000' : '#fff') }
      .type(ButtonType.Circle).backgroundColor(this.isListening ? 'rgba(255,0,0,0.2)' : '#c41e3a').width(48).height(48).onClick(() => { this.handleVoiceInput(); })
      TextInput({ placeholder: '输入指令或点击麦克风...', text: $$this.inputText }).width('100%').height(48).backgroundColor('#1a1a1a').fontColor('#fff').placeholderColor('#666').borderRadius(24).padding({ left: 16, right: 16 }).layoutWeight(1).margin({ left: 8, right: 8 }).onSubmit(() => { this.handleTextInput(); })
      Button() { Text('➤').fontSize(18).fontColor('#fff') }.type(ButtonType.Circle).backgroundColor('#c41e3a').width(48).height(48).onClick(() => { this.handleTextInput(); })
    }
    .width('100%').height(64).padding({ left: 16, right: 16 }).backgroundColor('#1a1a1a').border({ width: { top: 1 }, color: '#333' })
  }
}

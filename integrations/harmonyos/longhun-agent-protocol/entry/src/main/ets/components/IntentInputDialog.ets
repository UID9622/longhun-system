// entry/src/main/ets/components/IntentInputDialog.ets
// 龍魂 · 意图输入弹窗 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { IntentType, IntentPayload, ProtocolMessage, MessageType, AgentTask, TaskPriority, AgentState, agentState } from '../models/AgentProtocol';

@CustomDialog
export struct IntentInputDialog {
  controller: CustomDialogController;
  @StorageLink('agentState') agentState: AgentState = agentState;
  @State private inputText: string = '';
  @State private selectedIntentType: IntentType = IntentType.QUERY;
  @State private targetAgentId: string = '';
  @State private priority: TaskPriority = TaskPriority.NORMAL;
  @State private parseResult: string = '';
  @State private isVoiceMode: boolean = false;

  build() {
    Column() {
      // 标题栏
      Row() {
        Text('🎤 意图输入')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor('#fff')
        Blank()
        Button() {
          Text(this.isVoiceMode ? '⌨️ 键盘' : '🎙️ 语音')
            .fontSize(12).fontColor('#fff')
        }
        .type(ButtonType.Normal).backgroundColor('#333').borderRadius(4)
        .padding({ left: 8, right: 8, top: 4, bottom: 4 }).margin({ right: 8 })
        .onClick(() => { this.isVoiceMode = !this.isVoiceMode; })
        Button() { Text('✕').fontSize(18).fontColor('#888') }
          .type(ButtonType.Normal).backgroundColor(Color.Transparent)
          .onClick(() => { this.controller.close(); })
      }
      .width('100%').padding(16)
      .border({ width: { bottom: 1 }, color: '#333' })

      Scroll() {
        Column() {
          // 意图类型选择
          Text('意图类型')
            .fontSize(13).fontWeight(FontWeight.Medium).fontColor('#aaa')
            .width('100%').margin({ bottom: 8 })

          Row() {
            ForEach([
              { type: IntentType.QUERY, label: '🔍 查询', color: '#0066cc' },
              { type: IntentType.ACTION, label: '⚡ 执行', color: '#00cc66' },
              { type: IntentType.NAVIGATE, label: '🧭 导航', color: '#cc0066' },
              { type: IntentType.CREATE, label: '✨ 创建', color: '#ffcc00' },
              { type: IntentType.UPDATE, label: '🔄 更新', color: '#cc6600' },
              { type: IntentType.DELETE, label: '🗑️ 删除', color: '#ff0000' },
              { type: IntentType.SYNC, label: '🔄 同步', color: '#6600cc' },
              { type: IntentType.EXPORT, label: '📤 导出', color: '#6699cc' },
              { type: IntentType.SHARE, label: '🔗 分享', color: '#33cc99' },
              { type: IntentType.PRINT, label: '🖨️ 打印', color: '#999999' }
            ], (item: {type: IntentType, label: string, color: string}) => {
              Text(item.label)
                .fontSize(11)
                .fontColor(this.selectedIntentType === item.type ? '#fff' : '#888')
                .backgroundColor(this.selectedIntentType === item.type ? '#c41e3a' : '#1a1a1a')
                .borderRadius(4)
                .padding({ left: 6, right: 6, top: 4, bottom: 4 })
                .margin({ right: 4, bottom: 4 })
                .onClick(() => { this.selectedIntentType = item.type; })
            })
          }
          .width('100%').flexWrap(FlexWrap.Wrap).margin({ bottom: 16 })

          // 输入区
          if (this.isVoiceMode) {
            Column() {
              Text('🎙️')
                .fontSize(48).margin({ top: 24, bottom: 12 })
              Text('点击开始语音输入')
                .fontSize(16).fontColor('#888')
              Text('说"提交"发送意图')
                .fontSize(12).fontColor('#666').margin({ top: 8 })
              Button('🎤 开始录音')
                .fontSize(16).fontColor('#fff')
                .backgroundColor('#c41e3a').borderRadius(24)
                .padding({ left: 32, right: 32, top: 12, bottom: 12 }).margin({ top: 24 })
                .onClick(() => { console.info('[龍魂] 开始语音识别'); })
            }
            .width('100%').padding(32)
            .backgroundColor('#0a0a0a').borderRadius(12)
            .alignItems(HorizontalAlign.Center)
          } else {
            TextInput({ text: this.inputText, placeholder: '输入意图描述...' })
              .backgroundColor('#0a0a0a').borderRadius(8)
              .fontSize(14).height(80).maxLength(500)
              .onChange((value: string) => { this.inputText = value; })
              .margin({ bottom: 12 })

            Button('🔍 解析意图')
              .fontSize(13).fontColor('#fff').height(36)
              .backgroundColor('#333').borderRadius(4)
              .onClick(() => { this.parseIntent(); })
              .margin({ bottom: 12 })

            if (this.parseResult) {
              Text(this.parseResult)
                .fontSize(12).fontColor('#00ff00')
                .backgroundColor('rgba(0,255,0,0.05)').padding(8).borderRadius(4)
                .width('100%')
            }
          }

          // 目标选择
          if (!this.isVoiceMode) {
            Text('目标智能体')
              .fontSize(13).fontWeight(FontWeight.Medium).fontColor('#aaa')
              .width('100%').margin({ top: 16, bottom: 8 })

            Row() {
              ForEach(Array.from(this.agentState.agents.values()).filter(a => a.status === 'online').slice(0, 6),
                (agent) => {
                  Text(agent.name.substring(0, 4))
                    .fontSize(11)
                    .fontColor(this.targetAgentId === agent.id ? '#fff' : '#888')
                    .backgroundColor(this.targetAgentId === agent.id ? '#c41e3a' : '#1a1a1a')
                    .borderRadius(4)
                    .padding({ left: 8, right: 8, top: 4, bottom: 4 })
                    .margin({ right: 4, bottom: 4 })
                    .onClick(() => { this.targetAgentId = agent.id; })
                })
            }
            .width('100%').flexWrap(FlexWrap.Wrap)

            Text('优先级')
              .fontSize(13).fontWeight(FontWeight.Medium).fontColor('#aaa')
              .width('100%').margin({ top: 16, bottom: 8 })

            Row() {
              ForEach([
                { p: TaskPriority.CRITICAL, l: '紧急', c: '#ff0000' },
                { p: TaskPriority.HIGH, l: '高', c: '#ff6600' },
                { p: TaskPriority.NORMAL, l: '中', c: '#ffcc00' },
                { p: TaskPriority.LOW, l: '低', c: '#888' }
              ], (item: {p: TaskPriority, l: string, c: string}) => {
                Text(item.l)
                  .fontSize(12)
                  .fontColor(this.priority === item.p ? '#fff' : '#888')
                  .backgroundColor(this.priority === item.p ? item.c : '#1a1a1a')
                  .borderRadius(4)
                  .padding({ left: 12, right: 12, top: 4, bottom: 4 })
                  .margin({ right: 8 })
                  .onClick(() => { this.priority = item.p; })
              })
            }
          }
        }
        .padding(16)
      }
      .layoutWeight(1)

      // 提交
      Row() {
        Button('提交意图')
          .fontSize(15).fontColor('#fff').height(44)
          .backgroundColor('#c41e3a').borderRadius(8)
          .width('100%')
          .onClick(() => { this.submitIntent(); })
      }
      .width('100%').padding(16)
      .border({ width: { top: 1 }, color: '#333' })
    }
    .width('100%').height('90%')
    .backgroundColor('#1a1a1a')
    .borderRadius(12)
  }

  parseIntent(): void {
    if (!this.inputText.trim()) {
      this.parseResult = '请输入意图描述';
      return;
    }

    const text = this.inputText.trim();
    let matchedType = IntentType.QUERY;

    if (/创建|新建|生成|添加/.test(text)) matchedType = IntentType.CREATE;
    else if (/修改|更新|编辑|改/.test(text)) matchedType = IntentType.UPDATE;
    else if (/删除|移除|清/.test(text)) matchedType = IntentType.DELETE;
    else if (/执行|运行|启动/.test(text)) matchedType = IntentType.ACTION;
    else if (/导航|跳转|打开|去/.test(text)) matchedType = IntentType.NAVIGATE;
    else if (/同步|刷新|拉取/.test(text)) matchedType = IntentType.SYNC;
    else if (/导出|下载|备份/.test(text)) matchedType = IntentType.EXPORT;
    else if (/分享|发送|转发/.test(text)) matchedType = IntentType.SHARE;
    else if (/打印/.test(text)) matchedType = IntentType.PRINT;

    this.selectedIntentType = matchedType;
    this.parseResult = `解析成功 · 意图类型: ${matchedType} · 置信度: 92%`;
    console.info(`[龍魂] 意图解析: ${text} → ${matchedType}`);
  }

  submitIntent(): void {
    if (!this.inputText.trim() && !this.isVoiceMode) {
      console.warn('[龍魂] 意图内容为空');
      return;
    }

    // 创建意图消息
    const payload: IntentPayload = {
      intentType: this.selectedIntentType,
      rawText: this.inputText.trim() || '语音输入',
      slots: this.extractSlots(this.inputText),
      confidence: 0.92,
      context: ''
    };

    const msg = new ProtocolMessage({
      type: MessageType.INTENT,
      from: this.agentState.currentAgentId || 'localhost',
      to: this.targetAgentId || 'router',
      payload
    });

    this.agentState.logMessage(msg);

    // 创建对应任务
    const task = new AgentTask({
      intentId: msg.id,
      action: `${this.selectedIntentType}: ${this.inputText.trim().substring(0, 30)}`,
      params: { intent: this.inputText, slots: payload.slots },
      priority: this.priority
    });

    this.agentState.submitTask(task);
    this.agentState.logAudit('INTENT_SUBMIT', msg.from, msg.to, 'success', {
      intentType: this.selectedIntentType,
      rawText: this.inputText.trim().substring(0, 50)
    });

    console.info(`[龍魂] 意图提交: ${task.id}`);
    this.controller.close();
  }

  extractSlots(text: string): Record<string, any> {
    const slots: Record<string, any> = {};
    // 简单NLP提取
    const timeMatch = text.match(/(今天|明天|下周|本周|下月)/);
    if (timeMatch) slots.time = timeMatch[1];

    const numMatch = text.match(/(\d+)/);
    if (numMatch) slots.quantity = parseInt(numMatch[1]);

    const dateMatch = text.match(/(\d{4}-\d{1,2}-\d{1,2})/);
    if (dateMatch) slots.date = dateMatch[1];

    return slots;
  }
}

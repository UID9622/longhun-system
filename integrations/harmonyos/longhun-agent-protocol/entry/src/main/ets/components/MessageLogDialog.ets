// entry/src/main/ets/components/MessageLogDialog.ets
// 龍魂 · 消息日志弹窗 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { ProtocolMessage, MessageType, AgentState, agentState } from '../models/AgentProtocol';

@CustomDialog
export struct MessageLogDialog {
  controller: CustomDialogController;
  @StorageLink('agentState') agentState: AgentState = agentState;
  @State private filterType: MessageType | 'ALL' = 'ALL';
  @State private showDetailIndex: number = -1;
  @State private searchText: string = '';

  get filteredMessages(): ProtocolMessage[] {
    let msgs = this.agentState.messageLog;
    if (this.filterType !== 'ALL') {
      msgs = msgs.filter(m => m.type === this.filterType);
    }
    if (this.searchText) {
      msgs = msgs.filter(m =>
        m.id.includes(this.searchText) ||
        m.from.includes(this.searchText) ||
        m.to.includes(this.searchText)
      );
    }
    return msgs.slice(-100).reverse();
  }

  build() {
    Column() {
      // 标题栏
      Row() {
        Text('📡 消息日志')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor('#fff')
        Blank()
        Text(`${this.agentState.messageLog.length}条消息`)
          .fontSize(12).fontColor('#666').margin({ right: 12 })
        Button() { Text('✕').fontSize(18).fontColor('#888') }
          .type(ButtonType.Normal).backgroundColor(Color.Transparent)
          .onClick(() => { this.controller.close(); })
      }
      .width('100%').padding(16)
      .border({ width: { bottom: 1 }, color: '#333' })

      // 类型过滤
      Scroller() {
        Row() {
          ForEach([
            { type: 'ALL' as const, label: '全部', color: '#888' },
            { type: MessageType.REGISTER, label: '注册', color: '#00ff00' },
            { type: MessageType.INTENT, label: '意图', color: '#ffcc00' },
            { type: MessageType.TASK, label: '任务', color: '#0066cc' },
            { type: MessageType.RESULT, label: '结果', color: '#00cc66' },
            { type: MessageType.ERROR, label: '错误', color: '#ff0000' },
            { type: MessageType.HEARTBEAT, label: '心跳', color: '#ff6699' },
            { type: MessageType.AUDIT, label: '审计', color: '#cccccc' }
          ], (item: {type: MessageType | 'ALL', label: string, color: string}) => {
            Column() {
              Text(item.label)
                .fontSize(11)
                .fontColor(this.filterType === item.type ? '#fff' : '#888')
                .backgroundColor(this.filterType === item.type ? '#c41e3a' : '#1a1a1a')
                .borderRadius(4)
                .padding({ left: 8, right: 8, top: 4, bottom: 4 })
            }
            .margin({ right: 6 })
            .onClick(() => { this.filterType = item.type; this.showDetailIndex = -1; })
          })
        }
        .padding({ left: 12, right: 12, top: 8, bottom: 8 })
      }
      .width('100%')
      .scrollable(ScrollDirection.Horizontal)
      .scrollBar(BarState.Off)

      // 搜索
      TextInput({ text: this.searchText, placeholder: '搜索消息ID/发送方/接收方' })
        .backgroundColor('#0a0a0a')
        .borderRadius(8)
        .fontSize(13)
        .margin({ left: 12, right: 12, top: 8 })
        .onChange((value: string) => { this.searchText = value; })

      // 消息列表
      List() {
        ForEach(this.filteredMessages, (msg: ProtocolMessage, index: number) => {
          ListItem() {
            Column() {
              Row() {
                Text(this.getTypeIcon(msg.type))
                  .fontSize(16).margin({ right: 8 })
                Column() {
                  Text(msg.type.toUpperCase())
                    .fontSize(12).fontWeight(FontWeight.Medium).fontColor('#fff')
                  Text(`${msg.from} → ${msg.to}`)
                    .fontSize(11).fontColor('#666')
                }
                .alignItems(HorizontalAlign.Start).layoutWeight(1)
                Column() {
                  Text(new Date(msg.timestamp).toLocaleTimeString())
                    .fontSize(10).fontColor('#666')
                  Text(msg.id.substring(0, 8))
                    .fontSize(10).fontColor('#555')
                }
                .alignItems(HorizontalAlign.End)
              }
              .width('100%')

              // 展开详情
              if (this.showDetailIndex === index) {
                Text(JSON.stringify(msg.payload, null, 2))
                  .fontSize(11).fontColor('#888')
                  .backgroundColor('#0a0a0a')
                  .padding(8).borderRadius(4)
                  .width('100%').margin({ top: 8 })
                Text(`签名: ${msg.dnaSignature}`)
                  .fontSize(10).fontColor('#555').margin({ top: 4 })
              }

              Text(this.showDetailIndex === index ? '收起 ▲' : '展开 ▼')
                .fontSize(11).fontColor('#888').margin({ top: 6 })
                .onClick(() => {
                  this.showDetailIndex = this.showDetailIndex === index ? -1 : index;
                })
            }
            .width('100%').padding(12)
            .backgroundColor('#0a0a0a').borderRadius(8)
            .margin({ left: 12, right: 12, top: 8 })
          }
        }, (msg: ProtocolMessage) => msg.id)
      }
      .width('100%').layoutWeight(1)
      .scrollBar(BarState.Auto)
      .divider({ strokeWidth: 1, color: '#222' })
    }
    .width('95%').height('85%')
    .backgroundColor('#1a1a1a')
    .borderRadius(12)
  }

  getTypeIcon(type: MessageType): string {
    const icons: Record<string, string> = {
      'register': '📥',
      'unregister': '📤',
      'intent': '🎤',
      'task': '📋',
      'result': '✅',
      'sync': '🔄',
      'heartbeat': '💓',
      'error': '❌',
      'audit': '📝'
    };
    return icons[type] || '📡';
  }
}

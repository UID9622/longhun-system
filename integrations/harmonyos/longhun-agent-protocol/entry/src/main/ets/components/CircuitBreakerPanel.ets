// entry/src/main/ets/components/CircuitBreakerPanel.ets
// 龍魂 · 熔断器面板 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { CircuitBreaker, AgentState, agentState } from '../models/AgentProtocol';

@CustomDialog
export struct CircuitBreakerPanel {
  controller: CustomDialogController;
  @StorageLink('agentState') agentState: AgentState = agentState;
  @State private newCbTarget: string = '';
  @State private newCbName: string = '';
  @State private newCbThreshold: number = 5;

  build() {
    Column() {
      // 标题栏
      Row() {
        Text('⚡ 熔断器管理')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor('#fff')
        Blank()
        Text(`${this.agentState.statistics.openCircuits}个熔断`)
          .fontSize(12).fontColor('#ff0000').margin({ right: 12 })
        Button() { Text('✕').fontSize(18).fontColor('#888') }
          .type(ButtonType.Normal).backgroundColor(Color.Transparent)
          .onClick(() => { this.controller.close(); })
      }
      .width('100%').padding(16)
      .border({ width: { bottom: 1 }, color: '#333' })

      // 概览统计
      Row() {
        this.OverviewCard('总计', this.agentState.circuitBreakers.size, '#fff')
        this.OverviewCard('正常', Array.from(this.agentState.circuitBreakers.values()).filter(c => c.state === 'closed').length, '#00ff00')
        this.OverviewCard('探测', Array.from(this.agentState.circuitBreakers.values()).filter(c => c.state === 'half-open').length, '#ffcc00')
        this.OverviewCard('熔断', this.agentState.statistics.openCircuits, '#ff0000')
      }
      .width('100%').padding(12).backgroundColor('#0a0a0a')

      // 新建熔断器
      Column() {
        Text('+ 新建熔断器')
          .fontSize(14).fontWeight(FontWeight.Medium).fontColor('#fff')
          .width('100%').padding({ left: 12, top: 8 })

        Row() {
          TextInput({ text: this.newCbName, placeholder: '名称' })
            .backgroundColor('#0a0a0a').borderRadius(4)
            .fontSize(12).height(36).layoutWeight(1).margin({ right: 8 })
            .onChange((value: string) => { this.newCbName = value; })
          TextInput({ text: this.newCbTarget, placeholder: '目标智能体ID' })
            .backgroundColor('#0a0a0a').borderRadius(4)
            .fontSize(12).height(36).layoutWeight(1).margin({ right: 8 })
            .onChange((value: string) => { this.newCbTarget = value; })
          TextInput({ text: this.newCbThreshold.toString(), placeholder: '阈值' })
            .backgroundColor('#0a0a0a').borderRadius(4)
            .fontSize(12).height(36).width(60).margin({ right: 8 })
            .type(InputType.Number)
            .onChange((value: string) => { this.newCbThreshold = parseInt(value) || 5; })
          Button('+').fontSize(16).fontColor('#fff').width(36).height(36)
            .backgroundColor('#c41e3a').borderRadius(4)
            .onClick(() => { this.addCircuitBreaker(); })
        }
        .width('100%').padding({ left: 12, right: 12, bottom: 8 })
      }
      .backgroundColor('#1a1a1a')
      .border({ width: { bottom: 1 }, color: '#333' })

      // 熔断器列表
      List() {
        ForEach(Array.from(this.agentState.circuitBreakers.values()), (cb: CircuitBreaker) => {
          ListItem() {
            Column() {
              Row() {
                Text(
                  cb.state === 'closed' ? '✅' : cb.state === 'open' ? '❌' : '⚠️'
                ).fontSize(24).margin({ right: 12 })
                Column() {
                  Row() {
                    Text(cb.name).fontSize(15).fontWeight(FontWeight.Medium).fontColor('#fff').layoutWeight(1)
                    Text(cb.getStatus()).fontSize(11)
                      .fontColor(cb.state === 'closed' ? '#00ff00' : cb.state === 'open' ? '#ff0000' : '#ffcc00')
                      .backgroundColor(
                        cb.state === 'closed' ? 'rgba(0,255,0,0.1)' :
                        cb.state === 'open' ? 'rgba(255,0,0,0.1)' : 'rgba(255,204,0,0.1)'
                      ).borderRadius(4).padding({ left: 6, right: 6, top: 2, bottom: 2 })
                  }
                  .width('100%')
                  Text(`目标: ${cb.target}`).fontSize(12).fontColor('#888').width('100%')
                  Text(`失败阈值: ${cb.failureCount}/${cb.failureThreshold}`).fontSize(11).fontColor('#666').width('100%')
                }
                .alignItems(HorizontalAlign.Start).layoutWeight(1)
              }
              .width('100%')

              // 统计条
              Row() {
                Text(`总计 ${cb.totalCalls} 次`).fontSize(10).fontColor('#888')
                Text(`✅ ${cb.totalSuccesses}`).fontSize(10).fontColor('#00ff00').margin({ left: 8 })
                Text(`❌ ${cb.totalFailures}`).fontSize(10).fontColor('#ff0000').margin({ left: 8 })
                Text(`失败率 ${cb.totalCalls > 0 ? Math.round(cb.totalFailures / cb.totalCalls * 100) : 0}%`)
                  .fontSize(10).fontColor('#ffcc00').margin({ left: 8 })
              }
              .width('100%').margin({ top: 8 })

              // 操作按钮
              if (cb.state === 'open') {
                Row() {
                  Button('手动重置').fontSize(11).height(28)
                    .backgroundColor('#c41e3a').borderRadius(4)
                    .onClick(() => { cb.state = 'half-open'; cb.halfOpenCalls = 0; cb.successCount = 0; })
                  Button('删除').fontSize(11).height(28)
                    .backgroundColor('#333').borderRadius(4).margin({ left: 8 })
                    .onClick(() => { this.agentState.circuitBreakers.delete(cb.id); })
                }
                .width('100%').justifyContent(FlexAlign.End).margin({ top: 8 })
              }
            }
            .width('100%').padding(16).backgroundColor('#0a0a0a').borderRadius(8)
            .margin({ left: 12, right: 12, top: 8 })
          }
        }, (cb: CircuitBreaker) => cb.id)
      }
      .width('100%').layoutWeight(1)
      .scrollBar(BarState.Auto)
    }
    .width('95%').height('85%')
    .backgroundColor('#1a1a1a')
    .borderRadius(12)
  }

  @Builder
  OverviewCard(label: string, value: number, color: string) {
    Column() {
      Text(value.toString())
        .fontSize(22).fontWeight(FontWeight.Bold).fontColor(color)
      Text(label)
        .fontSize(10).fontColor('#666').margin({ top: 2 })
    }
    .width('25%').alignItems(HorizontalAlign.Center)
  }

  addCircuitBreaker(): void {
    if (!this.newCbName.trim() || !this.newCbTarget.trim()) return;
    const cb = new CircuitBreaker({
      name: this.newCbName.trim(),
      target: this.newCbTarget.trim(),
      failureThreshold: this.newCbThreshold
    });
    this.agentState.circuitBreakers.set(cb.id, cb);
    this.newCbName = '';
    this.newCbTarget = '';
    this.newCbThreshold = 5;
    console.info('[龍魂] 新建熔断器:', cb.name);
  }
}

/**
 * 🐉 龍魂·通知服务 — AlertService + NotificationHistory
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-NOTIFICATION-SERVICE-UID9622
 */

import { ServiceAbility, Want } from '@kit.AbilityKit';
import { notificationManager } from '@kit.NotificationKit';
import { router } from '@kit.ArkUI';

interface Alert { id: string; channel: string; title: string; body: string; time: string; read: boolean; tricolor: string; }

// ─── 警报服务 ───
export default class AlertService extends ServiceAbility {
  onStart(want: Want): void {
    console.info('[龍魂·通知] 警报服务启动');

    // 监听监督引擎状态并推送通知
    // 实际实现中通过IPC订阅核心服务的监督事件
    this.sendTestNotification();
  }

  onStop(): void { console.info('[龍魂·通知] 服务停止'); }

  private async sendTestNotification(): Promise<void> {
    try {
      // 使用鸿蒙通知API
      const request: notificationManager.NotificationRequest = {
        id: 1001,
        content: {
          notificationContentType: notificationManager.ContentType.NOTIFICATION_CONTENT_BASIC_TEXT,
          normal: {
            title: '🐉 龍魂監督',
            text: '監督周期已完成·🟢 全部通過'
          }
        },
        slotType: notificationManager.SlotType.SOCIAL_COMMUNICATION
      };
      await notificationManager.publish(request);
    } catch (e) {
      console.warn('[龍魂·通知] 发送测试通知失败（可能无权限）');
    }
  }
}

// ─── 通知历史页 ───
@Entry
@Component
struct NotificationHistory {
  @State alerts: Alert[] = [
    { id: '1', channel: 'longhun-alert', title: '🔴 監督攔截率異常', body: 'L2執行層攔截率突增至95%·需立即檢查', time: '01:30', read: false, tricolor: '🔴' },
    { id: '2', channel: 'longhun-evolution', title: '🟡 進化升級提案', body: '系統熵值達0.28·建議升級v1.0.4', time: '01:00', read: true, tricolor: '🟡' },
    { id: '3', channel: 'longhun-info', title: '🟢 監督周期完成', body: '#42周期·三層全通過·無異常', time: '00:30', read: true, tricolor: '🟢' },
    { id: '4', channel: 'longhun-alert', title: '🔴 主權異常', body: '跨平台驗證失敗·CSDN連接超時', time: '00:15', read: false, tricolor: '🔴' },
  ];

  build() {
    Column() {
      Row() {
        Text('🐉 通知歷史').fontSize(20).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
        Blank()
        Text(`${this.alerts.filter(a => !a.read).length} 未讀`).fontSize(11).fontColor('#F4A261')
      }.width('100%').padding(16)

      // 渠道过滤
      Row({ space: 8 }) {
        FilterChip('全部', true)
        FilterChip('警报', false)
        FilterChip('进化', false)
        FilterChip('日常', false)
      }.width('100%').padding({ left: 16, bottom: 8 })

      List() {
        ForEach(this.alerts, (a: Alert) => {
          ListItem() {
            Row() {
              // 三色指示条
              Column()
                .width(3).height('100%')
                .backgroundColor(a.tricolor === '🔴' ? '#E63946' : a.tricolor === '🟡' ? '#F4A261' : '#4ADE80')

              Column({ space: 4 }) {
                Row() {
                  Text(a.title).fontSize(13).fontColor('#E5E7EB').fontWeight(a.read ? FontWeight.Normal : FontWeight.Bold).layoutWeight(1)
                  if (!a.read) Circle({ width: 6, height: 6 }).fill('#E63946')
                }
                Text(a.body).fontSize(11).fontColor('#9CA3AF').maxLines(2)
                Row() {
                  Text(a.channel).fontSize(8).fontColor('#6B7280')
                    .padding({ left: 4, right: 4, top: 1, bottom: 1 })
                    .border({ width: 0.5, color: '#334155', style: BorderStyle.Solid }).borderRadius(3)
                  Blank()
                  Text(a.time).fontSize(9).fontColor('#4B5563')
                }
              }
              .alignItems(HorizontalAlign.Start).layoutWeight(1).margin({ left: 10 })
            }
            .width('100%').padding(12).backgroundColor('#1E293B').borderRadius(8)
            .margin({ left: 16, right: 16, top: 3, bottom: 3 })
          }
        })
      }.layoutWeight(1)
    }
    .width('100%').height('100%').backgroundColor('#0F172A')
  }
}

@Component
struct FilterChip {
  @Prop label: string = '';
  @Prop active: boolean = false;

  build() {
    Text(this.label).fontSize(11).fontColor(this.active ? '#0F172A' : '#C9A84C')
      .padding({ left: 12, right: 12, top: 4, bottom: 4 })
      .backgroundColor(this.active ? '#C9A84C' : '#1E293B')
      .borderRadius(12)
  }
}

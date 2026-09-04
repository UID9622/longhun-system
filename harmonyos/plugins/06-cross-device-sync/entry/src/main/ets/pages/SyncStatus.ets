/**
 * 🐉 龍魂·跨设备同步 — 全部页面+服务+小组件
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-CROSS-DEVICE-SYNC-PAGES-UID9622
 */

import { router } from '@kit.ArkUI';
import { ServiceAbility, Want } from '@kit.AbilityKit';

// ─── 同步类型 ───
interface DeviceInfo { id: string; name: string; type: string; status: string; lastSync: string; }
interface SyncRecord { time: string; type: string; count: number; status: string; }

// ─── 同步状态页 ───
@Entry
@Component
struct SyncStatus {
  @State devices: DeviceInfo[] = [
    { id: '1', name: 'Mate 60 Pro', type: 'phone', status: '🟢 在线', lastSync: '刚刚' },
    { id: '2', name: 'MatePad Pro', type: 'tablet', status: '🟢 在线', lastSync: '2分钟前' },
    { id: '3', name: 'MateBook X Pro', type: 'laptop', status: '🟡 离线', lastSync: '12分钟前' },
  ];
  @State records: SyncRecord[] = [
    { time: '01:15', type: 'P0記憶', count: 4, status: '🟢' },
    { time: '01:14', type: 'P1記憶', count: 7, status: '🟢' },
    { time: '01:10', type: '監督狀態', count: 1, status: '🟢' },
    { time: '00:45', type: '進化指標', count: 3, status: '🟡' },
  ];
  @State syncEnabled: boolean = true;
  @State totalMemories: number = 42;

  build() {
    Scroll() {
      Column({ space: 12 }) {
        Row() {
          Text('🐉 跨設備同步').fontSize(20).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
          Blank()
          Toggle({ type: ToggleType.Switch, isOn: this.syncEnabled })
            .onChange((v: boolean) => { this.syncEnabled = v; })
        }.width('100%').padding(16)

        // 统计卡片
        Row({ space: 16 }) {
          StatCard('已連接', '2 / 3', '#4ADE80')
          StatCard('總記憶', `${this.totalMemories}`, '#C9A84C')
          StatCard('最後同步', '剛剛', '#6B7280')
        }.width('100%').padding({ left: 16, right: 16 })

        // 设备列表
        Row() {
          Text('已發現設備').fontSize(14).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
          Blank()
          Text('詳情 →').fontSize(12).fontColor('#C9A84C')
        }.width('100%').padding({ left: 16, right: 16, top: 8 })
        .onClick(() => { router.pushUrl({ url: 'pages/DeviceList' }); })

        ForEach(this.devices, (d: DeviceInfo) => {
          Row() {
            Column() {
              Text(d.type === 'phone' ? '📱' : d.type === 'tablet' ? '📋' : '💻').fontSize(20)
            }.width(40).height(40).borderRadius(20).backgroundColor('#1E293B').justifyContent(FlexAlign.Center)

            Column({ space: 2 }) {
              Text(d.name).fontSize(14).fontColor('#E5E7EB')
              Text(`最后同步: ${d.lastSync}`).fontSize(10).fontColor('#6B7280')
            }.alignItems(HorizontalAlign.Start).margin({ left: 10 }).layoutWeight(1)

            Text(d.status).fontSize(11)
          }
          .width('100%').padding(12).backgroundColor('#1E293B').borderRadius(8).margin({ left: 16, right: 16 })
        })

        // 同步记录
        Text('同步記錄').fontSize(14).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
          .width('100%').padding({ left: 16, top: 8 })

        ForEach(this.records, (r: SyncRecord) => {
          Row() {
            Text(r.time).fontSize(10).fontColor('#6B7280').width(40)
            Text(r.type).fontSize(12).fontColor('#E5E7EB').layoutWeight(1)
            Text(`${r.count}條`).fontSize(11).fontColor('#9CA3AF').margin({ right: 8 })
            Text(r.status).fontSize(14)
          }
          .width('100%').padding({ left: 20, right: 16, top: 6, bottom: 6 })
          .border({ width: { bottom: 0.5 }, color: '#1E293B', style: BorderStyle.Solid })
        })
      }.width('100%').padding({ bottom: 24 })
    }
    .width('100%').height('100%').backgroundColor('#0F172A')
  }
}

@Component
struct StatCard {
  @Prop label: string = '';
  @Prop value: string = '';
  @Prop color: string = '#6B7280';

  build() {
    Column({ space: 4 }) {
      Text(this.value).fontSize(22).fontColor(this.color).fontWeight(FontWeight.Bold)
      Text(this.label).fontSize(10).fontColor('#6B7280')
    }
    .layoutWeight(1).padding(12)
    .backgroundColor('#1E293B').borderRadius(8)
    .alignItems(HorizontalAlign.Center)
  }
}

// ─── 设备列表页 ───
@Entry
@Component
struct DeviceList {
  @State devices: DeviceInfo[] = [
    { id: '1', name: 'Mate 60 Pro', type: 'phone', status: '🟢 在線', lastSync: '剛剛' },
    { id: '2', name: 'MatePad Pro 13.2', type: 'tablet', status: '🟢 在線', lastSync: '2分鐘前' },
    { id: '3', name: 'MateBook X Pro', type: 'laptop', status: '🟡 離線', lastSync: '12分鐘前' },
    { id: '4', name: '華為智慧屏 V5', type: 'tv', status: '🟡 待機', lastSync: '1小時前' },
    { id: '5', name: '華為手錶 GT 4', type: 'watch', status: '🟢 在線', lastSync: '28分鐘前' },
  ];

  build() {
    Column() {
      Row() {
        Text('←').fontSize(16).fontColor('#C9A84C').onClick(() => { router.back(); })
        Blank()
        Text('Super Device').fontSize(18).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
      }.width('100%').padding(16)

      List() {
        ForEach(this.devices, (d: DeviceInfo) => {
          ListItem() {
            Row() {
              Text(d.type === 'phone' ? '📱' : d.type === 'tablet' ? '📋' : d.type === 'laptop' ? '💻' : d.type === 'tv' ? '📺' : '⌚').fontSize(28)
              Column({ space: 2 }) {
                Text(d.name).fontSize(15).fontColor('#E5E7EB').fontWeight(FontWeight.Medium)
                Text(d.status).fontSize(11).fontColor('#6B7280')
              }.alignItems(HorizontalAlign.Start).margin({ left: 12 }).layoutWeight(1)
              Text(d.lastSync).fontSize(10).fontColor('#4B5563')
            }
            .width('100%').padding(14)
            .backgroundColor('#1E293B').borderRadius(10)
            .margin({ left: 16, right: 16, top: 4, bottom: 4 })
          }
        })
      }.layoutWeight(1)
    }
    .width('100%').height('100%').backgroundColor('#0F172A')
  }
}

// ─── 同步后台服务 ───
export default class SyncService extends ServiceAbility {
  onStart(want: Want): void {
    console.info('[龍魂·同步] 跨设备同步服务启动');
    // 使用 DistributedKVStore 初始化
    // initDistributedKV(); 
  }
  onStop(): void { console.info('[龍魂·同步] 服务停止'); }
}

// ─── 桌面同步小组件 ───
@Entry
@Component
struct SyncWidget {
  @State deviceCount: number = 3;
  @State lastSync: string = '剛剛';
  @State memories: number = 42;

  build() {
    Column({ space: 4 }) {
      Text('🐉 龍魂同步').fontSize(12).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
      Row({ space: 12 }) {
        Column() { Text(`${this.deviceCount}`).fontSize(20).fontColor('#4ADE80').fontWeight(FontWeight.Bold)
          Text('設備').fontSize(8).fontColor('#6B7280') }
        Column() { Text(`${this.memories}`).fontSize(20).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
          Text('記憶').fontSize(8).fontColor('#6B7280') }
        Column() { Text('🟢').fontSize(14)
          Text('同步').fontSize(8).fontColor('#6B7280') }
      }
    }
    .width('100%').height('100%')
    .backgroundColor('#0F172A').justifyContent(FlexAlign.Center)
  }
}

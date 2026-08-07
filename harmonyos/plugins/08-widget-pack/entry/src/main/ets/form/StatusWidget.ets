/**
 * 🐉 龍魂·桌面小组件套件
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-WIDGET-PACK-UID9622
 *
 * 4个小组件：系统状态(2×2) · 最近记忆(2×4) · 监督缩影(4×2) · 快捷操作(2×2)
 */

// ─── 2×2 系统状态 ───
@Entry
@Component
struct StatusWidget {
  @State status: string = '🟢';
  @State time: string = '';
  @State cycle: number = 42;

  aboutToAppear(): void { this.time = new Date().toLocaleTimeString(); }

  build() {
    Column({ space: 4 }) {
      Row() {
        Text('🐉').fontSize(14)
        Text('龍魂').fontSize(12).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
      }
      Text(this.status).fontSize(32)
      Text(`週期#${this.cycle}`).fontSize(9).fontColor('#6B7280')
      Text(this.time).fontSize(8).fontColor('#4B5563')
    }
    .width('100%').height('100%').backgroundColor('#0F172A').justifyContent(FlexAlign.Center)
  }
}

// ─── 2×4 最近记忆 ───
@Entry
@Component
struct MemoryWidget {
  @State memories: Record<string, string>[] = [
    { 'priority': 'P0', 'content': 'UID9622·諸葛鑫·唯一主權人', 'time': '01:00' },
    { 'priority': 'P1', 'content': '鲲鹏119.13.90.27·SSH優', 'time': '00:45' },
    { 'priority': 'P2', 'content': '鴻蒙插件生態10顆插件', 'time': '00:30' },
  ];

  build() {
    Column({ space: 2 }) {
      Text('🐉 最近記憶').fontSize(11).fontColor('#C9A84C').fontWeight(FontWeight.Bold).width('100%')
      ForEach(this.memories, (m: Record<string, string>) => {
        Row() {
          Badge(m['priority']).fontSize(8).fontColor(Color.White)
            .padding({ left: 3, right: 3 }).borderRadius(2)
            .backgroundColor(m['priority'] === 'P0' ? '#E63946' : m['priority'] === 'P1' ? '#F4A261' : '#457B9D')
          Text(m['content']).fontSize(9).fontColor('#E5E7EB').layoutWeight(1).maxLines(1)
            .margin({ left: 4 })
          Text(m['time']).fontSize(7).fontColor('#4B5563')
        }.width('100%')
      })
    }
    .width('100%').height('100%').padding(8).backgroundColor('#0F172A')
  }
}

// ─── 4×2 监督缩影 ───
@Entry
@Component
struct SupervisionWidget {
  @State L1: number = 92;
  @State L2: number = 85;
  @State L3: number = 96;

  build() {
    Row({ space: 8 }) {
      GaugeCol('L1', this.L1, '#4ADE80')
      GaugeCol('L2', this.L2, '#F4A261')
      GaugeCol('L3', this.L3, '#4ADE80')
    }
    .width('100%').height('100%').padding(8).backgroundColor('#0F172A').justifyContent(FlexAlign.SpaceEvenly)
  }
}

@Component
struct GaugeCol {
  @Prop label: string = '';
  @Prop value: number = 0;
  @Prop color: string = '';

  build() {
    Column({ space: 2 }) {
      Text(`${this.value}%`).fontSize(18).fontColor(this.color).fontWeight(FontWeight.Bold)
      Progress({ value: this.value, total: 100, type: ProgressType.Capsule })
        .width('100%').height(6).color(this.color).backgroundColor('#1E293B')
      Text(this.label).fontSize(8).fontColor('#6B7280')
    }
  }
}

// ─── 2×2 快捷操作 ───
@Entry
@Component
struct QuickActionWidget {
  build() {
    Grid() {
      GridItem() { ActionBtn('📡', '同步') }
      GridItem() { ActionBtn('🛡️', '驗證') }
      GridItem() { ActionBtn('🔍', '檢查') }
      GridItem() { ActionBtn('📤', '導出') }
    }
    .columnsTemplate('1fr 1fr').rowsTemplate('1fr 1fr')
    .width('100%').height('100%').padding(6).backgroundColor('#0F172A')
  }
}

@Component
struct ActionBtn {
  @Prop icon: string = '';
  @Prop label: string = '';

  build() {
    Column({ space: 2 }) {
      Text(this.icon).fontSize(18)
      Text(this.label).fontSize(8).fontColor('#C9A84C')
    }
    .width('100%').height('100%').backgroundColor('#1E293B').borderRadius(6).justifyContent(FlexAlign.Center)
  }
}

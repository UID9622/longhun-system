// 龍魂足迹 · HarmonyOS · 由龍魂全球开发者平台生成
// DNA: #龍芯⚡️丙午·丙申·戊辰·亥时·☵坎-DEV-DEMO-龍魂足迹-HOS-v1.0-5082eb98
// 创建者: UID9622
// 归属名: UID9622 · 龍芯北辰
// 模板: 全球足迹地图（标记你去过的地方）
// 技术栈: ArkTS · Map Kit + 位置服务
// 生成时间: 2026-08-22T22:15:45.253517

import router from '@ohos.router';

@Entry
@Component
struct Index {
  // 这是你在这个世界留下的第一行代码 🌍
  @State items: string[] = []
  @State newItem: string = ''

  build() {
    Column() {
      Row() {
        TextInput({ placeholder: '输入你的想法...', text: this.newItem })
          .onChange((value: string) => {
            this.newItem = value
          })
          .width('75%')

        Button('添加')
          .onClick(() => {
            if (this.newItem.length > 0) {
              this.items.push(this.newItem)
              this.newItem = ''
            }
          })
          .width('20%')
      }
      .width('100%')
      .padding(12)

      List({ space: 8 }) {
        ForEach(this.items, (item: string) => {
          ListItem() {
            Text(item)
              .width('100%')
              .padding(12)
              .backgroundColor('#F5F5F5')
              .borderRadius(8)
          }
        })
      }
      .width('100%')
      .padding({ left: 12, right: 12 })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Start)
  }
}

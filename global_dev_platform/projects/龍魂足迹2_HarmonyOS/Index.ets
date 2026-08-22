// 龍魂足迹2 · HarmonyOS · 由龍魂全球开发者平台生成
// DNA: #龍芯⚡️丙午·丙申·戊辰·亥时·☵坎-DEV-DEMO-龍魂足迹2-HOS-v1.0-17ee5700
// 创建者: UID9622
// 归属名: UID9622 · 龍芯北辰
// 模板: 待办事项 App（最经典的第一个 App）
// 技术栈: ArkTS · List组件 + Checkbox + 关系型数据库
// 生成时间: 2026-08-22T22:18:23.277407

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

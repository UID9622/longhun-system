// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-c2e3ebe0
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 龍魂路径宇宙 · 搜索栏
// UID9622 | 龍芯北辰 | 2026-07-18

@Component
export struct SearchBar {
  @State searchText: string = '龍魂系统'
  onTrace?: (text: string) => void

  build() {
    Row() {
      TextInput({ placeholder: '输入文本追踪路径...', text: $$this.searchText })
        .width('75%')
        .height(40)
        .backgroundColor('#1a1a1a')
        .borderColor('#FFD700')
        .borderWidth(1)
        .fontColor('#FFD700')
        .placeholderColor('#666')
        .borderRadius(4)
        .padding({ left: 10, right: 10 })
        .onChange((value: string) => {
          this.searchText = value
        })

      Button('追踪')
        .width('20%')
        .height(40)
        .backgroundColor('#FFD700')
        .fontColor('#000')
        .fontWeight(FontWeight.Bold)
        .borderRadius(4)
        .onClick(() => {
          if (this.onTrace && this.searchText.trim().length > 0) {
            this.onTrace(this.searchText.trim())
          }
        })
    }
    .width('100%')
    .padding({ left: 15, right: 15, top: 10, bottom: 10 })
    .backgroundColor('rgba(0,0,0,0.8)')
    .justifyContent(FlexAlign.SpaceBetween)
  }
}

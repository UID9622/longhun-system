// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-7f4fbb48
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 龍魂路径宇宙 · 审计过滤器
// UID9622 | 龍芯北辰 | 2026-07-18

@Component
export struct AuditFilter {
  @Prop currentFilter: string = 'all'
  onFilterChange?: (filter: string) => void

  build() {
    Row() {
      this.FilterButton({ label: '全部', filter: 'all', color: '#FFD700' })
      this.FilterButton({ label: '🟢通行', filter: 'green', color: '#0f0' })
      this.FilterButton({ label: '🟡待审', filter: 'yellow', color: '#ff0' })
      this.FilterButton({ label: '🔴熔断', filter: 'red', color: '#f00' })
    }
    .width('100%')
    .justifyContent(FlexAlign.SpaceEvenly)
    .padding(10)
    .backgroundColor('rgba(0,0,0,0.8)')
  }

  @Builder
  FilterButton(config: { label: string, filter: string, color: string }) {
    Button(config.label)
      .fontSize(11)
      .height(32)
      .backgroundColor(this.currentFilter === config.filter ? config.color : 'rgba(255,215,0,0.1)')
      .fontColor(this.currentFilter === config.filter ? '#000' : config.color)
      .border({ width: 1, color: config.color, radius: 4 })
      .padding({ left: 8, right: 8 })
      .onClick(() => {
        if (this.onFilterChange) {
          this.onFilterChange(config.filter)
        }
      })
  }
}

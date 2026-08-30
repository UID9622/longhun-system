// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-7a3c73f1
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 龍魂路径宇宙 · DNA水印
// UID9622 | 龍芯北辰 | 2026-07-18

import { P0_ANCHOR } from '../utils/Constants'

@Component
export struct DNAWatermark {

  build() {
    Text(`UID9622 | 龍芯北辰 | ${P0_ANCHOR.dna}`)
      .fontSize(8)
      .fontColor('#444')
      .position({ x: 0, y: '98%' })
      .width('100%')
      .textAlign(TextAlign.Center)
  }
}

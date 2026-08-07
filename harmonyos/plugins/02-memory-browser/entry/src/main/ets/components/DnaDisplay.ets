/**
 * 🐉 龍魂·DnaDisplay — DNA 追溯码显示组件
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-DNA-DISPLAY-UID9622
 *
 * 底部小字显示DNA短码，可点击复制
 */

import { clipboard } from '@kit.ArkUI';

@Component
export struct DnaDisplay {
  @Prop dna: string = '';
  @Prop fontSize: number = 9;
  @Prop showCopy: boolean = true;
  private copied: boolean = false;

  build() {
    Row() {
      Text(this.dna.length > 30 ? this.dna.substring(0, 28) + '...' : this.dna)
        .fontSize(this.fontSize)
        .fontColor('#6B7280')
        .fontFamily('monospace')
        .maxLines(1)
        .textOverflow({ overflow: TextOverflow.Ellipsis })
    }
    .onClick(() => {
      if (this.showCopy) {
        try {
          const pasteData = clipboard.createData(clipboard.MIMETYPE_TEXT_PLAIN, this.dna);
          clipboard.getSystemClipboard().setData(pasteData);
          this.copied = true;
          setTimeout(() => { this.copied = false; }, 1500);
        } catch (e) {
          // clipboard在某些设备上可能不可用
        }
      }
    })
  }
}

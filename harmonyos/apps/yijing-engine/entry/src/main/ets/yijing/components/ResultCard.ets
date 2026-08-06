/**
 * 🐉 龙魂·推演结果卡片
 * DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-RESULT-CARD-v1.0
 * License: MulanPSL v2
 * 创建者: 诸葛鑫（UID9622）
 */
import { HexagramReading } from '../engine/models/HexagramModels';

@Component
export struct ResultCard {
  @Prop result: string = ''; // JSON序列化的 HexagramReading
  @Prop showDetail: boolean = false;

  build() {
    if (!this.result) {
      Text('').visibility(Visibility.None)
    } else {
      Column() {
        Text('📜 推演结果')
          .fontSize(16).fontWeight(FontWeight.Bold).fontColor('#D4AF37')
          .margin({ bottom: 12 })

        // 简化展示
        Column() {
          try {
            const r: HexagramReading = JSON.parse(this.result) as HexagramReading;

            Row() {
              Text(r.originalHexagram.symbol).fontSize(36).fontColor('#D4AF37').margin({ right: 12 })
              Column() {
                Text(`${r.originalName}卦`).fontSize(20).fontColor('#E8E6E3').fontWeight(FontWeight.Bold)
                Text(r.ganzhiTime).fontSize(11).fontColor('#888')
              }.alignItems(HorizontalAlign.Start)
            }.margin({ bottom: 8 })

            Text(r.dna).fontSize(10).fontColor('#D4AF37').fontFamily('monospace').margin({ bottom: 8 })

            Row() {
              Text(r.auditStatus === '🟢' ? '🟢 审计通过' :
                r.auditStatus === '🟡' ? '🟡 待核' : '🔴 红线')
                .fontSize(13).fontColor(r.auditStatus === '🟢' ? '#4CAF50' :
                r.auditStatus === '🟡' ? '#FFC107' : '#F44336')
              Text(`R=${r.auditRScore.toFixed(2)}`).fontSize(11).fontColor('#888').margin({ left: 8 })

              if (r.movingYaoIndices.length > 0) {
                Row() {
                  Text(`⚡${r.movingYaoIndices.map(i => r.originalYaos[i].name).join(',')}`)
                    .fontSize(11).fontColor('#EF5350').margin({ left: 12 })
                  if (r.changedHexagram) {
                    Text(`→${r.changedName}${r.changedHexagram.symbol}`)
                      .fontSize(11).fontColor('#D4AF37').margin({ left: 4 })
                  }
                }
              }

              if (r.mutualHexagram) {
                Text(`互:${r.mutualName}${r.mutualHexagram.symbol}`)
                  .fontSize(10).fontColor('#888').margin({ left: 12 })
              }
            }.width('100%').justifyContent(FlexAlign.Start).margin({ bottom: 8 })

            // 世应·六亲·六神
            Text(`世在${getCnPos(r.shiPosition)}·应在${getCnPos(r.yingPosition)}`)
              .fontSize(11).fontColor('#A8A6A3')

            if (this.showDetail && r.interpretation) {
              Text(r.interpretation)
                .fontSize(13).fontColor('#C0C0C0')
                .margin({ top: 12 }).lineHeight(20)
            }
          } catch (e) {
            Text('数据解析异常')
              .fontSize(13).fontColor('#F44336')
          }
        }
        .width('100%').padding(16)
        .borderRadius(12).backgroundColor('#12121F')
        .border({ width: 1, color: '#2A2A3E', radius: 12 })
      }
    }
  }
}

function getCnPos(pos: number): string {
  const m: Record<number, string> = { 1: '初', 2: '二', 3: '三', 4: '四', 5: '五', 6: '上' };
  return m[pos] || '';
}

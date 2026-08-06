/**
 * 🐉 龙魂·易经推演首页
 * DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-YIJING-HOME-PAGE-v1.0
 * License: MulanPSL v2
 * 创建者: 诸葛鑫（UID9622）
 */
import router from '@ohos.router';
import { YijingEngine } from '../yijing/engine/YijingEngine';
import { DivinationMethod, HexagramReading } from '../yijing/engine/models/HexagramModels';

@Entry
@Component
struct YijingHomePage {
  @State question: string = '';
  @State method: number = 0; // 0=coins, 1=time, 2=numbers
  @State isDivinating: boolean = false;
  @State result: HexagramReading | null = null;
  @State errorMsg: string = '';

  private engine = YijingEngine.getInstance();
  private readonly METHOD_LABELS = ['六爻金钱', '时间起卦', '数字起卦'];

  build() {
    Scroll() {
      Column() {
        // 标题
        Text('🐉 龙魂 · 易经推演')
          .fontSize(26).fontWeight(FontWeight.Bold).fontColor('#D4AF37').letterSpacing(2)
          .padding({ top: 24, bottom: 16 })

        Text('以六十四卦参天地 · 以三才之道明吉凶')
          .fontSize(13).fontColor('#A8A6A3').margin({ bottom: 20 })

        // 问题输入
        Column() {
          Text('请输入您要问的事情')
            .fontSize(13).fontColor('#A8A6A3').margin({ bottom: 8 })
          TextInput({
            placeholder: '例如：这次合作是否顺利？',
            text: this.question,
          })
            .width('100%').height(48)
            .backgroundColor('#1A1A2E').borderRadius(10)
            .border({ width: 1, color: '#2A2A3E', radius: 10 })
            .fontColor('#E8E6E3').placeholderColor('#6A6865')
            .onChange((v: string) => { this.question = v; })
        }.width('90%')

        // 起卦方式
        Column() {
          Text('选择起卦方式').fontSize(13).fontColor('#A8A6A3').margin({ top: 16, bottom: 10 })
          Row() {
            ForEach(this.METHOD_LABELS, (label: string, idx: number) => {
              Button(label)
                .width('28%').height(36).borderRadius(8)
                .backgroundColor(this.method === idx ? '#D4AF37' : '#1A1A2E')
                .fontColor(this.method === idx ? '#0A0A12' : '#A8A6A3').fontSize(12)
                .border({ width: 1, color: this.method === idx ? '#D4AF37' : '#2A2A3E', radius: 8 })
                .onClick(() => { this.method = idx; })
            })
          }.width('90%').justifyContent(FlexAlign.SpaceAround)
        }

        // 推演按钮
        Button(this.isDivinating ? '⏳ 推演中...' : '🔮 开始推演')
          .width('80%').height(48).borderRadius(12)
          .backgroundColor('#D4AF37').fontColor('#0A0A12')
          .fontSize(17).fontWeight(FontWeight.Medium)
          .margin({ top: 24 }).enabled(!this.isDivinating)
          .onClick(() => { this.startDivination(); })

        // 错误提示
        if (this.errorMsg) {
          Text(this.errorMsg).fontSize(12).fontColor('#F44336').margin({ top: 8 })
        }

        // 结果展示
        if (this.result) {
          Column() {
            Divider().color('#2A2A3E').margin({ top: 20, bottom: 16 })

            // 卦符+卦名
            Text(this.result.originalHexagram.symbol)
              .fontSize(64).fontColor('#D4AF37').margin({ bottom: 4 })
            Text(`${this.result.originalName}卦`)
              .fontSize(22).fontColor('#E8E6E3').fontWeight(FontWeight.Bold)
              .margin({ bottom: 4 })

            // 卦辞
            Text(this.result.originalHexagram.description)
              .fontSize(14).fontColor('#D4AF37')
              .textAlign(TextAlign.Center).margin({ bottom: 4 })

            // DNA
            Text(this.result.dna)
              .fontSize(9).fontColor('#D4AF37').fontFamily('monospace')
              .margin({ bottom: 8 })

            // 世应行
            Row() {
              Text(`世爻: ${this.getPosName(this.result.shiPosition)}`)
                .fontSize(12).fontColor('#D4AF37')
              Text(`应爻: ${this.getPosName(this.result.yingPosition)}`)
                .fontSize(12).fontColor('#888').margin({ left: 16 })
            }.margin({ bottom: 8 })

            // 六亲
            Text('六亲：' + this.result.sixRelations.map(r =>
              `${this.getPosName(r.position)}${r.relation}`).join('·'))
              .fontSize(11).fontColor('#A8A6A3').margin({ bottom: 4 })

            // 六神
            Text('六神：' + this.result.sixSpirits.map(s =>
              `${this.getPosName(s.position)}${s.spirit}`).join('·'))
              .fontSize(11).fontColor('#A8A6A3').margin({ bottom: 8 })

            // 动爻+变卦+互卦
            if (this.result.movingYaoIndices.length > 0) {
              Text(`⚡ 动爻：${this.result.movingYaoIndices.map(i =>
                this.result!.originalYaos[i].name).join('、')}`)
                .fontSize(13).fontColor('#EF5350').margin({ bottom: 4 })
              if (this.result.changedHexagram) {
                Text(`变卦：${this.result.changedName} ${this.result.changedHexagram.symbol}`)
                  .fontSize(13).fontColor('#FFC107')
              }
            }
            if (this.result.mutualHexagram) {
              Text(`互卦：${this.result.mutualName} ${this.result.mutualHexagram.symbol}`)
                .fontSize(12).fontColor('#888')
            }

            // 爻辞
            Column() {
              Text('📖 爻辞').fontSize(14).fontColor('#D4AF37').margin({ top: 12, bottom: 8 })
              ForEach(this.result.originalYaos, (yao, idx) => {
                Row() {
                  Text(yao.name)
                    .fontSize(12).fontColor(yao.isMoving ? '#EF5350' : '#D4AF37')
                    .fontWeight(yao.isMoving ? FontWeight.Bold : FontWeight.Normal)
                    .width(48)
                  Text(yao.shiYing)
                    .fontSize(10).fontColor(yao.shiYing === '世' ? '#D4AF37' : '#888')
                    .width(24)
                  Text(yao.sixRelation)
                    .fontSize(10).fontColor('#A8A6A3').width(36)
                  Text(yao.sixSpirit)
                    .fontSize(10).fontColor('#888').width(36)
                  Text(this.result ? this.result.originalHexagram.yaoText[idx] : '')
                    .fontSize(11).fontColor('#C0C0C0')
                    .layoutWeight(1).maxLines(2)
                }
                .width('100%').padding(6)
                .backgroundColor(yao.shiYing === '世' ? '#1A1A2E' : '#12121F')
                .borderRadius(6).margin({ bottom: 3 })
                .border({ width: 1, color: yao.shiYing === '世' ? '#D4AF3733' : '#2A2A3E', radius: 6 })
              })
            }.width('90%').margin({ bottom: 12 })

            // 🔥 判断与建议（独立展示）
            Column() {
              Text('【卦象判断】')
                .fontSize(14).fontColor('#D4AF37').fontWeight(FontWeight.Bold)
                .margin({ bottom: 4 })
              Text(this.extractJudgment())
                .fontSize(13).fontColor('#E0E0E0').lineHeight(20)
                .margin({ bottom: 12 })
              Text('【建议】')
                .fontSize(14).fontColor('#D4AF37').fontWeight(FontWeight.Bold)
                .margin({ bottom: 4 })
              Text(this.result.suggestion)
                .fontSize(13).fontColor('#E0E0E0').lineHeight(20)
            }.width('90%').padding(12)
            .borderRadius(8).backgroundColor('#12121F')
            .border({ width: 1, color: '#2A2A3E', radius: 8 })
            .margin({ bottom: 16 })

            // 审计状态
            Row() {
              Text(`${this.result.auditStatus} 审计: R=${this.result.auditRScore.toFixed(2)}`)
                .fontSize(12).fontColor('#888')
              Text(`· ${this.result.ganzhiTime}`)
                .fontSize(11).fontColor('#666')
            }.margin({ bottom: 8 })

          }.width('90%').alignItems(HorizontalAlign.Center)
        }

        Blank()

        // 主权声明
        Text('#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️')
          .fontSize(9).fontColor('#6A6865').fontFamily('monospace').margin({ top: 20, bottom: 16 })
      }
      .width('100%').alignItems(HorizontalAlign.Center)
    }
    .width('100%').height('100%')
    .backgroundColor('#0A0A12')
    .scrollable(ScrollDirection.Vertical)
    .scrollBar(BarState.Off)
  }

  private getPosName(pos: number): string {
    const m: Record<number, string> = { 1: '初', 2: '二', 3: '三', 4: '四', 5: '五', 6: '上' };
    return m[pos] || '';
  }

  private extractJudgment(): string {
    if (!this.result) return '';
    // 取出 interpretation 中【卦象判断】至【建议】之间的内容
    const txt = this.result.interpretation;
    const start = txt.indexOf('【卦象判断】');
    const end = txt.indexOf('【建议】');
    if (start >= 0 && end > start) {
      return txt.substring(start + 6, end).trim();
    }
    return txt;
  }

  private async startDivination() {
    if (!this.question.trim()) {
      this.errorMsg = '请先输入您要问的事情';
      return;
    }
    this.errorMsg = '';
    this.isDivinating = true;

    try {
      const methods = [DivinationMethod.COINS, DivinationMethod.TIME, DivinationMethod.NUMBERS];
      const method = methods[this.method];
      const params: Record<string, Object> = {};
      if (this.method === 0) params['seed'] = Date.now();

      this.result = this.engine.divinate(this.question, method, params);
    } catch (e) {
      this.errorMsg = `推演失败: ${e}`;
    } finally {
      this.isDivinating = false;
    }
  }
}

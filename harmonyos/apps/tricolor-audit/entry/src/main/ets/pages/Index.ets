/**
 * 龙魂·三色审计 — 首页
 * 暗金主题入口
 * License: MulanPSL v2
 */
import { SOVEREIGNTY, ANCHOR_369, DARK_GOLD } from '../models/Constants';
import router from '@ohos.router';

@Entry
@Component
struct Index {
  @State currentTime: string = this.getTime();

  build() {
    Column() {
      // 龙魂 Logo
      Text('龍魂')
        .fontSize(48)
        .fontColor(DARK_GOLD.PRIMARY)
        .fontFamily('LonghunFont')
        .margin({ top: 40, bottom: 8 })

      Text('三色审计系统')
        .fontSize(20)
        .fontColor(DARK_GOLD.TEXT_PRIMARY)

      // 主权声明
      Text(SOVEREIGNTY.CREATOR)
        .fontSize(11)
        .fontColor(DARK_GOLD.TEXT_SECONDARY)
        .margin({ top: 4, bottom: 20 })

      // 369 锚点
      Row() {
        Text(`369不动点: sn=${ANCHOR_369.SN} · log=${ANCHOR_369.LOG} · perm=${ANCHOR_369.PERM}`)
          .fontSize(10)
          .fontColor(DARK_GOLD.TEXT_SECONDARY)
          .fontFamily('monospace')
      }

      // 当前时间
      Text(this.currentTime)
        .fontSize(12)
        .fontColor(DARK_GOLD.PRIMARY)
        .margin({ top: 8, bottom: 30 })

      // 开始审计
      Button('🛡️ 开始审计')
        .fontSize(18)
        .backgroundColor(DARK_GOLD.PRIMARY)
        .fontColor(DARK_GOLD.BG_DARK)
        .width('80%')
        .height(56)
        .borderRadius(28)
        .onClick(() => {
          router.pushUrl({ url: 'pages/AuditPage' });
        })
        .margin({ bottom: 12 })

      // 查看历史
      Button('📋 审计历史')
        .fontSize(16)
        .backgroundColor(DARK_GOLD.BG_CARD)
        .fontColor(DARK_GOLD.PRIMARY)
        .width('60%')
        .height(48)
        .borderRadius(24)
        .border({ width: 1, color: DARK_GOLD.BORDER })
        .onClick(() => {
          router.pushUrl({ url: 'pages/HistoryPage' });
        })

      // 主权锚点底部
      Text(`${SOVEREIGNTY.SHIELD}${SOVEREIGNTY.FLAG}${SOVEREIGNTY.SCALE}${SOVEREIGNTY.PACT} UID9622 · 龍芯北辰`)
        .fontSize(9)
        .fontColor(DARK_GOLD.TEXT_SECONDARY)
        .margin({ top: 40 })
    }
    .width('100%')
    .height('100%')
    .backgroundColor(DARK_GOLD.BG_DARK)
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
  }

  getTime(): string {
    const now = new Date();
    return `${now.getFullYear()}-${(now.getMonth() + 1).toString().padStart(2, '0')}-${now.getDate().toString().padStart(2, '0')} ${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
  }
}

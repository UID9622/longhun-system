/*
 * ==========================================================================
 * 龍魂 · 生日详情弹窗
 * DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-BIRTHDAY-DETAIL-v2.0
 * ==========================================================================
 * 人格联动展示：关系层级、生肖干支、祝福预览、人格切换
 */

import { TeamMember } from '../models/BirthdayModel';
import {
  RelationshipLevel,
  PersonaID,
  EmotionMode,
  PERSONA_ROLES,
  RELATIONSHIP_EMOTION_MAP,
  MASTER_UID
} from '../common/types';
import { BlessingGenerator } from '../engines/BlessingGenerator';
import { PersonaRouter } from '../engines/PersonaRouter';
import { EmotionProtocol } from '../engines/EmotionProtocol';

@CustomDialog
export struct BirthdayDetailDialog {
  controller: CustomDialogController;
  member: TeamMember;
  onPersonaChange?: (persona: PersonaID) => void;
  onBlessingCopy?: (blessing: string) => void;

  @State showBlessingPreview: boolean = false;
  @State generatedBlessing: string = '';

  aboutToAppear() {
    this.generateBlessing();
  }

  build() {
    Column() {
      // ── 顶部 ──
      Row() {
        Button('←')
          .fontSize(20).fontColor('#888')
          .backgroundColor('transparent')
          .onClick(() => this.controller.close())

        Blank()

        Text(this.member.name)
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor('#fff')

        Blank()

        Button('✕')
          .fontSize(18).fontColor('#888')
          .backgroundColor('transparent')
          .onClick(() => this.controller.close())
      }
      .width('100%')
      .padding(16)

      Scroll() {
        Column() {
          // ── 生日倒计时卡片 ──
          this.CountdownCard()

          // ── 基本信息卡片 ──
          this.InfoCard()

          // ── 关系与情感卡片 ──
          this.RelationshipCard()

          // ── 人格路由卡片 ──
          this.PersonaCard()

          // ── 祝福预览卡片 ──
          this.BlessingCard()
        }
        .padding({ left: 16, right: 16, bottom: 16 })
      }
      .layoutWeight(1)
      .scrollBar(BarState.Auto)

      // ── 底部操作 ──
      Row() {
        Button(this.showBlessingPreview ? '隐藏祝福' : '预览祝福')
          .fontSize(14).fontColor('#fff')
          .backgroundColor('#2a2a2a').border({ width: 1, color: '#c41e3a' })
          .borderRadius(8).layoutWeight(1)
          .onClick(() => {
            this.showBlessingPreview = !this.showBlessingPreview;
            if (this.showBlessingPreview) this.generateBlessing();
          })

        Button('复制祝福')
          .fontSize(14).fontColor('#fff')
          .backgroundColor('#c41e3a').borderRadius(8).layoutWeight(1)
          .margin({ left: 8 })
          .onClick(() => {
            if (this.onBlessingCopy) {
              this.onBlessingCopy(this.generatedBlessing);
            }
            this.controller.close();
          })
      }
      .width('100%')
      .padding(16)
      .border({ width: { top: 1 }, color: '#333' })
    }
    .width('100%')
    .height('92%')
    .backgroundColor('#0a0a0a')
    .borderRadius({ topLeft: 16, topRight: 16 })
  }

  // ── 倒计时卡片 ──
  @Builder
  CountdownCard() {
    const days = this.member.getDaysUntilBirthday();
    const isToday = days === 0;

    Column() {
      if (isToday) {
        Text('🎂')
          .fontSize(48)
          .margin({ bottom: 8 })
        Text('今天过生日！')
          .fontSize(24)
          .fontWeight(FontWeight.Bold)
          .fontColor('#fff')
      } else {
        Text(days.toString())
          .fontSize(48)
          .fontWeight(FontWeight.Bold)
          .fontColor('#c41e3a')
        Text('天后过生日')
          .fontSize(16)
          .fontColor('#888')
      }

      Text(this.member.getNextBirthdayString())
        .fontSize(13)
        .fontColor('#666')
        .margin({ top: 8 })

      if (this.member.birthdayType === 'lunar') {
        Text('（农历）')
          .fontSize(12)
          .fontColor('#ffcc00')
          .margin({ top: 4 })
      }

      if (this.member.getAge() >= 0) {
        Text(`${this.member.getAge()}岁`)
          .fontSize(14)
          .fontColor('#ccc')
          .backgroundColor('rgba(196,30,58,0.2)')
          .borderRadius(12)
          .padding({ left: 12, right: 12 })
          .margin({ top: 8 })
      }
    }
    .width('100%')
    .padding({ top: 24, bottom: 24 })
    .backgroundColor('#1a1a1a')
    .borderRadius(12)
    .margin({ bottom: 12 })
  }

  // ── 信息卡片 ──
  @Builder
  InfoCard() {
    Column() {
      this.DetailRow('部门', this.member.department)
      this.DetailRow('职位', this.member.role)

      if (this.member.zodiacSign && this.member.zodiacSign !== '未知') {
        this.DetailRow('生肖', this.member.zodiacSign)
      }
      if (this.member.tianganDizhi && this.member.tianganDizhi !== '未知') {
        this.DetailRow('干支', this.member.tianganDizhi)
      }

      if (this.member.phone) this.DetailRow('电话', this.member.phone)
      if (this.member.email) this.DetailRow('邮箱', this.member.email)

      if (this.member.tags.length > 0) {
        Row() {
          Text('标签')
            .fontSize(13).fontColor('#888').width(60)
          Row() {
            ForEach(this.member.tags.slice(0, 5), (tag: string) => {
              Text(tag)
                .fontSize(11).fontColor('#aaa')
                .backgroundColor('#2a2a2a').borderRadius(4)
                .padding({ left: 6, right: 6 }).margin({ right: 4 })
            })
          }
        }
        .width('100%')
        .padding({ top: 6, bottom: 6 })
      }
    }
    .width('100%')
    .padding(12)
    .backgroundColor('#1a1a1a')
    .borderRadius(12)
    .margin({ bottom: 12 })
  }

  // ── 关系与情感卡片 ──
  @Builder
  RelationshipCard() {
    const emotion = RELATIONSHIP_EMOTION_MAP[this.member.relationship];
    const color = EmotionProtocol.getEmotionColor(emotion.empathy);

    Column() {
      Row() {
        Text('情感档案')
          .fontSize(14).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        Blank()
        Text(this.member.getRelationshipLabel())
          .fontSize(12).fontColor('#fff')
          .backgroundColor(color).borderRadius(4)
          .padding({ left: 8, right: 8 })
      }
      .width('100%')
      .margin({ bottom: 8 })

      this.EmotionBar('共情', emotion.empathy, color)
      this.EmotionBar('温暖', emotion.warmth, color)
      this.EmotionBar('边界', emotion.boundary, '#4a90d9')
      this.EmotionBar('正式', emotion.formality, '#8a8a8a')

      Divider().margin({ top: 8, bottom: 8 })

      Text(EmotionProtocol.getBoundaryIndicator(emotion.boundary))
        .fontSize(12).fontColor('#888')
    }
    .width('100%')
    .padding(12)
    .backgroundColor('#1a1a1a')
    .borderRadius(12)
    .margin({ bottom: 12 })
  }

  // ── 人格路由卡片 ──
  @Builder
  PersonaCard() {
    const route = PersonaRouter.routeForMember(this.member);
    const primaryRole = PERSONA_ROLES[route.primary];

    Column() {
      Row() {
        Text('人格路由')
          .fontSize(14).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        Blank()
        Text(`${route.reason}`)
          .fontSize(11).fontColor('#666').maxLines(1)
      }
      .width('100%')
      .margin({ bottom: 8 })

      Row() {
        Text(primaryRole?.icon || '🐉')
          .fontSize(28)
        Column() {
          Text(primaryRole?.name || route.primary)
            .fontSize(16).fontWeight(FontWeight.Medium).fontColor('#fff')
          Text(`祝福风格: ${primaryRole?.blessingStyle || 'warm'}`)
            .fontSize(12).fontColor('#888')
        }
        .alignItems(HorizontalAlign.Start)
      }
      .width('100%')
      .margin({ bottom: 8 })
      .padding(8)
      .backgroundColor('rgba(196,30,58,0.1)')
      .borderRadius(8)

      Text(`辅助人格: ${route.secondary.map(p => PERSONA_ROLES[p]?.name || p).join(' · ')}`)
        .fontSize(12).fontColor('#666')
    }
    .width('100%')
    .padding(12)
    .backgroundColor('#1a1a1a')
    .borderRadius(12)
    .margin({ bottom: 12 })
  }

  // ── 祝福预览卡片 ──
  @Builder
  BlessingCard() {
    Column() {
      Row() {
        Text('祝福预览')
          .fontSize(14).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        Blank()
        Button('重新生成')
          .fontSize(11).fontColor('#c41e3a')
          .backgroundColor('transparent').border({ width: 1, color: '#c41e3a' })
          .borderRadius(4).padding({ left: 8, right: 8 })
          .onClick(() => this.generateBlessing())
      }
      .width('100%')
      .margin({ bottom: 8 })

      if (this.showBlessingPreview) {
        Text(this.generatedBlessing)
          .fontSize(14)
          .fontColor('#ccc')
          .lineHeight(24)
          .padding(12)
          .backgroundColor('#2a2a2a')
          .borderRadius(8)
          .width('100%')
      } else {
        Text('点击下方"预览祝福"查看')
          .fontSize(13).fontColor('#666').fontStyle(FontStyle.Italic)
          .padding(12)
      }
    }
    .width('100%')
    .padding(12)
    .backgroundColor('#1a1a1a')
    .borderRadius(12)
    .margin({ bottom: 12 })
  }

  // ── 辅助组件 ──
  @Builder
  DetailRow(label: string, value: string) {
    Row() {
      Text(label)
        .fontSize(13).fontColor('#888').width(60)
      Text(value)
        .fontSize(13).fontColor('#ccc')
    }
    .width('100%')
    .padding({ top: 6, bottom: 6 })
  }

  @Builder
  EmotionBar(label: string, value: number, color: string) {
    Row() {
      Text(label)
        .fontSize(12).fontColor('#888').width(40)
      Progress({ value: value * 100, total: 100, type: ProgressType.Linear })
        .width('60%')
        .color(color)
        .style({ strokeWidth: 6, strokeRadius: 3 })
      Text((value * 100).toFixed(0) + '%')
        .fontSize(11).fontColor('#888').margin({ left: 8 })
    }
    .width('100%')
    .padding({ top: 3, bottom: 3 })
  }

  // ── 生成祝福 ──
  private generateBlessing() {
    this.generatedBlessing = BlessingGenerator.generate(this.member);
  }
}

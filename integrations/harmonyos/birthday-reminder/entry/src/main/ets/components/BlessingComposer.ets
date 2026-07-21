/*
 * ==========================================================================
 * 龍魂 · 祝福编辑器
 * DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-BLESSING-COMPOSER-v2.0
 * ==========================================================================
 * 人格风格切换 + 实时预览 + 分享/复制/短信
 */

import { TeamMember } from '../models/BirthdayModel';
import {
  PersonaID,
  BlessingStyle,
  PERSONA_ROLES,
  MASTER_UID
} from '../common/types';
import { BlessingGenerator } from '../engines/BlessingGenerator';

@CustomDialog
export struct BlessingComposer {
  controller: CustomDialogController;
  member: TeamMember;
  onSend?: (blessing: string) => void;

  @State currentStyle: BlessingStyle = BlessingStyle.WARM;
  @State currentPersona: PersonaID = PersonaID.BAOBAO;
  @State blessingText: string = '';
  @State showAllStyles: boolean = false;

  private readonly styleOptions = [
    { style: BlessingStyle.POETIC, persona: PersonaID.LIBAI, label: '🍶 李白·诗意', color: '#ff8c42' },
    { style: BlessingStyle.WARM, persona: PersonaID.BAOBAO, label: '🧚 宝宝·暖心', color: '#ff6b9d' },
    { style: BlessingStyle.INSPIRING, persona: PersonaID.SUDONGPO, label: '🍖 东坡·豁达', color: '#4ecdc4' },
    { style: BlessingStyle.FORMAL, persona: PersonaID.ZHUGELIANG, label: '🪈 孔明·正式', color: '#4a90d9' },
    { style: BlessingStyle.TRADITIONAL, persona: PersonaID.CANGJIE, label: '📜 仓颉·传统', color: '#9b59b6' },
    { style: BlessingStyle.SIMPLE, persona: PersonaID.LUBAN, label: '🔧 鲁班·简洁', color: '#7f8c8d' }
  ];

  aboutToAppear() {
    // 使用成员的偏好风格
    const role = PERSONA_ROLES[this.member.preferredBlessingPersona];
    this.currentStyle = role?.blessingStyle || BlessingStyle.WARM;
    this.currentPersona = this.member.preferredBlessingPersona;
    this.regenerate();
  }

  build() {
    Column() {
      // ── 标题 ──
      Row() {
        Button('←')
          .fontSize(20).fontColor('#888')
          .backgroundColor('transparent')
          .onClick(() => this.controller.close())

        Text('祝福编辑器')
          .fontSize(18).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
          .layoutWeight(1)
          .textAlign(TextAlign.Center)

        Button('复制')
          .fontSize(13).fontColor('#fff')
          .backgroundColor('#c41e3a').borderRadius(6)
          .padding({ left: 12, right: 12 })
          .onClick(() => this.copyBlessing())
      }
      .width('100%')
      .padding(16)
      .border({ width: { bottom: 1 }, color: '#333' })

      // ── 收件人信息 ──
      Row() {
        Text(`收件人: ${this.member.name} · ${this.member.department}`)
          .fontSize(13).fontColor('#888')
      }
      .width('100%')
      .padding({ left: 16, right: 16, bottom: 8 })

      // ── 人格风格选择器 ──
      Row() {
        Text('选择风格:')
          .fontSize(13).fontColor('#ccc')
          .margin({ right: 8 })

        Scroll() {
          Row() {
            ForEach(this.styleOptions, (opt: {style: BlessingStyle, persona: PersonaID, label: string, color: string}) => {
              Text(opt.label)
                .fontSize(11)
                .fontColor(this.currentStyle === opt.style ? '#fff' : '#aaa')
                .backgroundColor(this.currentStyle === opt.style ? opt.color : '#2a2a2a')
                .borderRadius(12)
                .padding({ left: 8, right: 8, top: 4, bottom: 4 })
                .margin({ right: 6 })
                .onClick(() => {
                  this.currentStyle = opt.style;
                  this.currentPersona = opt.persona;
                  this.regenerate();
                })
            })
          }
        }
        .scrollable(ScrollDirection.Horizontal)
        .scrollBar(BarState.Off)
        .layoutWeight(1)
      }
      .width('100%')
      .padding({ left: 16, right: 16, bottom: 8 })

      // ── 祝福文本编辑区 ──
      Scroll() {
        TextArea({ text: this.blessingText })
          .fontSize(15)
          .fontColor('#ccc')
          .lineHeight(26)
          .padding(16)
          .backgroundColor('#1a1a1a')
          .borderRadius(12)
          .minHeight(300)
          .onChange((v: string) => { this.blessingText = v })
      }
      .layoutWeight(1)
      .padding({ left: 16, right: 16, top: 8, bottom: 8 })
      .scrollBar(BarState.Auto)

      // ── 操作按钮 ──
      Row() {
        Button('重新生成')
          .fontSize(14).fontColor('#ccc')
          .backgroundColor('#2a2a2a').border({ width: 1, color: '#444' })
          .borderRadius(8).layoutWeight(1)
          .onClick(() => this.regenerate())

        Button('分享')
          .fontSize(14).fontColor('#fff')
          .backgroundColor('#c41e3a').borderRadius(8).layoutWeight(1)
          .margin({ left: 8 })
          .onClick(() => {
            if (this.onSend) {
              this.onSend(this.blessingText);
            }
            this.controller.close();
          })
      }
      .width('100%')
      .padding(16)
      .border({ width: { top: 1 }, color: '#333' })
    }
    .width('100%')
    .height('88%')
    .backgroundColor('#0a0a0a')
    .borderRadius({ topLeft: 16, topRight: 16 })
  }

  private regenerate() {
    this.blessingText = BlessingGenerator.generate(this.member, this.currentStyle);
  }

  private copyBlessing() {
    // 复制到剪贴板（调用鸿蒙 pasteboard API）
    // 这里简化实现
    console.info('Blessing copied:', this.blessingText.slice(0, 50));
  }
}

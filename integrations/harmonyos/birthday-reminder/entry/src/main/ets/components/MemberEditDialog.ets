/*
 * ==========================================================================
 * 龍魂 · 成员编辑弹窗
 * DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-MEMBER-EDIT-v2.0
 * ==========================================================================
 */

import {
  TeamMember,
} from '../models/BirthdayModel';
import {
  BirthdayType,
  RelationshipLevel,
  PersonaID,
  MASTER_UID
} from '../common/types';

@CustomDialog
export struct MemberEditDialog {
  controller: CustomDialogController;
  member: TeamMember | null = null;
  onConfirm: (member: TeamMember) => void;
  onDelete?: (id: string) => void;

  @State localName: string = '';
  @State localDepartment: string = '';
  @State localRole: string = '';
  @State localMonth: number = 1;
  @State localDay: number = 1;
  @State localYear: number = 0;
  @State localBirthdayType: BirthdayType = BirthdayType.SOLAR;
  @State localRelationship: RelationshipLevel = RelationshipLevel.REGULAR_COLLEAGUE;
  @State localPersona: PersonaID = PersonaID.BAOBAO;
  @State localPhone: string = '';
  @State localEmail: string = '';
  @State localNotes: string = '';
  @State localTags: string = '';

  @State selectedBirthdayTypeIndex: number = 0;
  @State selectedRelationIndex: number = 1;
  @State selectedPersonaIndex: number = 0;

  private readonly birthdayTypes = ['公历', '农历'];
  private readonly relations = [
    { label: '密友', value: RelationshipLevel.CLOSE_COLLEAGUE },
    { label: '同事', value: RelationshipLevel.REGULAR_COLLEAGUE },
    { label: '领导', value: RelationshipLevel.LEADER },
    { label: '队友', value: RelationshipLevel.TEAM_MATE },
    { label: '伙伴', value: RelationshipLevel.EXTERNAL }
  ];
  private readonly personas = [
    { label: '🧚 宝宝·暖心治愈', value: PersonaID.BAOBAO },
    { label: '🍶 李白·诗意洒脱', value: PersonaID.LIBAI },
    { label: '🔧 鲁班·简洁高效', value: PersonaID.LUBAN },
    { label: '🪈 诸葛亮·正式得体', value: PersonaID.ZHUGELIANG },
    { label: '🍖 苏东坡·豁达励志', value: PersonaID.SUDONGPO },
    { label: '📜 仓颉·传统典雅', value: PersonaID.CANGJIE }
  ];

  aboutToAppear() {
    if (this.member) {
      this.localName = this.member.name;
      this.localDepartment = this.member.department;
      this.localRole = this.member.role;
      this.localMonth = this.member.birthdayMonth;
      this.localDay = this.member.birthdayDay;
      this.localYear = this.member.birthYear;
      this.localBirthdayType = this.member.birthdayType;
      this.localRelationship = this.member.relationship;
      this.localPersona = this.member.preferredBlessingPersona;
      this.localPhone = this.member.phone;
      this.localEmail = this.member.email;
      this.localNotes = this.member.personalNotes;
      this.localTags = this.member.tags.join('、');

      this.selectedBirthdayTypeIndex = this.localBirthdayType === BirthdayType.SOLAR ? 0 : 1;
      this.selectedRelationIndex = this.relations.findIndex(r => r.value === this.localRelationship);
      this.selectedPersonaIndex = this.personas.findIndex(p => p.value === this.localPersona);
    }
  }

  build() {
    Column() {
      // ── 标题 ──
      Row() {
        Text(this.member ? '编辑成员' : '添加成员')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor('#c41e3a')

        Blank()

        if (this.member && this.onDelete) {
          Button('删除')
            .fontSize(13)
            .fontColor('#ff4444')
            .backgroundColor('transparent')
            .onClick(() => {
              this.onDelete!(this.member!.id);
              this.controller.close();
            })
        }

        Button('✕')
          .fontSize(18)
          .fontColor('#888')
          .backgroundColor('transparent')
          .onClick(() => this.controller.close())
      }
      .width('100%')
      .padding(16)
      .border({ width: { bottom: 1 }, color: '#333' })

      // ── 表单 ──
      Scroll() {
        Column() {
          this.FormSection('基本信息', () => {
            this.InputField('姓名', '请输入姓名', this.localName, (v: string) => { this.localName = v });
            Row() {
              Column() {
                Text('部门')
                  .fontSize(12).fontColor('#888').margin({ bottom: 4 })
                TextInput({ text: this.localDepartment, placeholder: '部门' })
                  .onChange((v: string) => { this.localDepartment = v })
              }.layoutWeight(1).margin({ right: 8 })
              Column() {
                Text('职位')
                  .fontSize(12).fontColor('#888').margin({ bottom: 4 })
                TextInput({ text: this.localRole, placeholder: '职位' })
                  .onChange((v: string) => { this.localRole = v })
              }.layoutWeight(1)
            }
          });

          this.FormSection('生日信息', () => {
            Row() {
              Text('日历类型')
                .fontSize(13).fontColor('#ccc').layoutWeight(1)
              Select(this.birthdayTypes.map(t => ({ value: t })))
                .selected(this.selectedBirthdayTypeIndex)
                .fontColor('#fff').backgroundColor('#2a2a2a').borderRadius(8)
                .onSelect((index: number) => {
                  this.selectedBirthdayTypeIndex = index;
                  this.localBirthdayType = index === 0 ? BirthdayType.SOLAR : BirthdayType.LUNAR;
                })
            }.width('100%').margin({ bottom: 12 })

            Row() {
              Column() {
                Text('出生年(选填)').fontSize(12).fontColor('#888').margin({ bottom: 4 })
                TextInput({ text: this.localYear > 0 ? this.localYear.toString() : '', placeholder: '1990' })
                  .type(InputType.Number)
                  .onChange((v: string) => { this.localYear = parseInt(v) || 0 })
              }.layoutWeight(1).margin({ right: 8 })

              Column() {
                Text('月').fontSize(12).fontColor('#888').margin({ bottom: 4 })
                TextInput({ text: this.localMonth.toString(), placeholder: '1' })
                  .type(InputType.Number)
                  .onChange((v: string) => { this.localMonth = Math.max(1, Math.min(12, parseInt(v) || 1)) })
              }.layoutWeight(1).margin({ right: 8 })

              Column() {
                Text('日').fontSize(12).fontColor('#888').margin({ bottom: 4 })
                TextInput({ text: this.localDay.toString(), placeholder: '1' })
                  .type(InputType.Number)
                  .onChange((v: string) => { this.localDay = Math.max(1, Math.min(31, parseInt(v) || 1)) })
              }.layoutWeight(1)
            }
          });

          this.FormSection('关系与人格', () => {
            Row() {
              Text('关系层级').fontSize(13).fontColor('#ccc').layoutWeight(1)
              Select(this.relations.map(r => ({ value: r.label })))
                .selected(this.selectedRelationIndex >= 0 ? this.selectedRelationIndex : 0)
                .fontColor('#fff').backgroundColor('#2a2a2a').borderRadius(8)
                .onSelect((index: number) => {
                  this.selectedRelationIndex = index;
                  this.localRelationship = this.relations[index].value;
                })
            }.width('100%').margin({ bottom: 12 })

            Row() {
              Text('祝福风格').fontSize(13).fontColor('#ccc').layoutWeight(1)
              Select(this.personas.map(p => ({ value: p.label })))
                .selected(this.selectedPersonaIndex >= 0 ? this.selectedPersonaIndex : 0)
                .fontColor('#fff').backgroundColor('#2a2a2a').borderRadius(8)
                .onSelect((index: number) => {
                  this.selectedPersonaIndex = index;
                  this.localPersona = this.personas[index].value;
                })
            }
          });

          this.FormSection('联系方式与备注', () => {
            Row() {
              Column() {
                Text('电话').fontSize(12).fontColor('#888').margin({ bottom: 4 })
                TextInput({ text: this.localPhone, placeholder: '手机号' })
                  .type(InputType.PhoneNumber)
                  .onChange((v: string) => { this.localPhone = v })
              }.layoutWeight(1).margin({ right: 8 })
              Column() {
                Text('邮箱').fontSize(12).fontColor('#888').margin({ bottom: 4 })
                TextInput({ text: this.localEmail, placeholder: '邮箱地址' })
                  .type(InputType.Email)
                  .onChange((v: string) => { this.localEmail = v })
              }.layoutWeight(1)
            }.margin({ bottom: 12 })

            Column() {
              Text('标签（用、分隔）').fontSize(12).fontColor('#888').margin({ bottom: 4 })
              TextInput({ text: this.localTags, placeholder: '技术、前端、跑步' })
                .onChange((v: string) => { this.localTags = v })
            }.margin({ bottom: 12 })

            Column() {
              Text('个人备注（用于祝福个性化）').fontSize(12).fontColor('#888').margin({ bottom: 4 })
              TextArea({ text: this.localNotes, placeholder: '比如：喜欢咖啡、最近在学钢琴...' })
                .height(60)
                .onChange((v: string) => { this.localNotes = v })
            }
          });
        }
        .padding({ left: 16, right: 16 })
      }
      .layoutWeight(1)
      .scrollBar(BarState.Auto)

      // ── 底部按钮 ──
      Row() {
        Button('取消')
          .fontSize(14).fontColor('#ccc')
          .backgroundColor('#2a2a2a').border({ width: 1, color: '#444' })
          .borderRadius(8).layoutWeight(1)
          .onClick(() => this.controller.close())

        Button('保存')
          .fontSize(14).fontColor('#fff')
          .backgroundColor('#c41e3a').borderRadius(8).layoutWeight(1)
          .margin({ left: 12 })
          .onClick(() => {
            if (!this.localName.trim()) {
              return;
            }
            const data: Partial<TeamMember> = {
              name: this.localName.trim(),
              department: this.localDepartment.trim(),
              role: this.localRole.trim(),
              birthdayType: this.localBirthdayType,
              birthdayMonth: this.localMonth,
              birthdayDay: this.localDay,
              birthYear: this.localYear,
              relationship: this.localRelationship,
              preferredBlessingPersona: this.localPersona,
              phone: this.localPhone.trim(),
              email: this.localEmail.trim(),
              personalNotes: this.localNotes.trim(),
              tags: this.localTags.split('、').map(t => t.trim()).filter(t => t.length > 0)
            };
            const result = this.member
              ? this.member.clone(data)
              : new TeamMember(data);
            this.onConfirm(result);
            this.controller.close();
          })
      }
      .width('100%')
      .padding(16)
      .border({ width: { top: 1 }, color: '#333' })
    }
    .width('100%')
    .height('90%')
    .backgroundColor('#0a0a0a')
    .borderRadius({ topLeft: 16, topRight: 16 })
  }

  // ── 分组辅助 ──
  @Builder
  FormSection(title: string, content: () => void) {
    Column() {
      Text(title)
        .fontSize(14)
        .fontWeight(FontWeight.Bold)
        .fontColor('#c41e3a')
        .padding({ top: 16, bottom: 8 })
        .width('100%')

      content()
    }
    .width('100%')
  }

  @Builder
  InputField(label: string, placeholder: string, value: string, onChange: (v: string) => void) {
    Column() {
      Text(label)
        .fontSize(12)
        .fontColor('#888')
        .margin({ bottom: 4 })
      TextInput({ text: value, placeholder: placeholder })
        .onChange(onChange)
    }
    .width('100%')
    .margin({ bottom: 12 })
  }
}

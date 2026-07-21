// entry/src/main/ets/components/TemplateDialog.ets
// 龍魂 · 周报模板管理弹窗 · ArkTS

import { WeeklyTemplate, TemplateSection } from '../models/WeeklyModel';

@CustomDialog
export struct TemplateDialog {
  controller: CustomDialogController;
  templates: WeeklyTemplate[] = [];
  onSave?: (template: WeeklyTemplate) => void;
  onDelete?: (id: string) => void;
  onClose?: () => void;

  @State private editingTemplate: WeeklyTemplate | null = null;
  @State private showCreate: boolean = false;
  @State private templateName: string = '';
  @State private templateDept: string = '';
  @State private sections: TemplateSection[] = [];

  aboutToAppear() {
    this.resetCreate();
  }

  resetCreate(): void {
    this.showCreate = false;
    this.templateName = '';
    this.templateDept = '';
    this.sections = [];
    this.editingTemplate = null;
  }

  build() {
    Column() {
      // 标题栏
      Row() {
        Text(this.showCreate ? '创建模板' : '周报模板').fontSize(18).fontWeight(FontWeight.Bold).fontColor('#fff').layoutWeight(1)
        if (this.showCreate) {
          Text('返回').fontSize(14).fontColor('#c41e3a')
          .onClick(() => { this.resetCreate(); })
        }
        Text('✕').fontSize(20).fontColor('#888')
          .onClick(() => { this.onClose?.(); this.controller.close(); })
      }
      .width('100%').padding(16)
      .border({ width: { bottom: 1 }, color: '#333' })

      if (this.showCreate) {
        this.CreateTemplateBuilder()
      } else {
        this.TemplateListBuilder()
      }

      // 底部按钮
      if (!this.showCreate) {
        Row() {
          Button('+ 新建模板').fontSize(14).fontColor('#0a0a0a').backgroundColor('#c41e3a')
          .borderRadius(8).layoutWeight(1).height(44)
          .onClick(() => { this.showCreate = true; })
        }
        .width('100%').padding(16)
        .border({ width: { top: 1 }, color: '#333' })
      }
    }
    .width('100%').height('80%').backgroundColor('#1a1a1a').borderRadius({ topLeft: 16, topRight: 16 })
  }

  @Builder
  TemplateListBuilder() {
    Scroll() {
      Column() {
        if (this.templates.length === 0) {
          this.EmptyStateBuilder()
        } else {
          ForEach(this.templates, (template: Record<string, Object>) => {
            this.TemplateItemBuilder(template)
          })
        }
      }
    }
    .width('100%').layoutWeight(1).scrollBar(BarState.Auto)
  }

  @Builder
  EmptyStateBuilder() {
    Column() {
      Text('📋').fontSize(48).margin({ bottom: 12 })
      Text('暂无周报模板').fontSize(16).fontColor('#888').margin({ bottom: 6 })
      Text('点击底部按钮创建第一个模板').fontSize(12).fontColor('#555')
      Text('默认模板包含: 本周任务、下周计划、问题与风险、本周总结、需要支持').fontSize(11).fontColor('#444').margin({ top: 8 }).width('80%').textAlign(TextAlign.Center)
    }
    .width('100%').height(300).justifyContent(FlexAlign.Center).alignItems(HorizontalAlign.Center)
  }

  @Builder
  TemplateItemBuilder(template: Record<string, Object>) {
    Column() {
      Row() {
        Column() {
          Text((template.name as string) || '未命名').fontSize(15).fontWeight(FontWeight.Medium).fontColor('#fff')
          Text(`部门: ${template.department} · ${(template.sections as TemplateSection[])?.length || 0}个区块`)
            .fontSize(12).fontColor('#888').margin({ top: 4 })
        }
        .alignItems(HorizontalAlign.Start).layoutWeight(1)

        if ((template.isDefault as boolean)) {
          Text('默认').fontSize(10).fontColor('#ffcc00')
            .backgroundColor('rgba(255,204,0,0.1)').borderRadius(4)
            .padding({ left: 8, right: 8, top: 2, bottom: 2 })
        }

        Text('🗑️').fontSize(16).fontColor('#666').margin({ left: 12 })
        .onClick(() => { this.onDelete?.(template.id as string); })
      }
      .width('100%').margin({ bottom: 8 })

      // 区块预览
      Row() {
        ForEach((template.sections as TemplateSection[]) || [], (section: TemplateSection) => {
          Text(section.title)
            .fontSize(10).fontColor(section.required ? '#ffcc00' : '#666')
            .backgroundColor(section.required ? 'rgba(255,204,0,0.1)' : 'rgba(102,102,102,0.1)')
            .borderRadius(4).padding({ left: 6, right: 6, top: 2, bottom: 2 })
            .margin({ right: 4 })
        })
      }
      .width('100%')
    }
    .width('100%').padding(16)
    .backgroundColor('rgba(255,255,255,0.02)').borderRadius(8)
    .border({ width: 1, color: '#333' })
    .margin({ left: 12, right: 12, top: 8 })
  }

  @Builder
  CreateTemplateBuilder() {
    Scroll() {
      Column() {
        // 模板名称
        Column() {
          Text('模板名称 *').fontSize(13).fontColor('#888').margin({ bottom: 6 }).alignSelf(ItemAlign.Start)
          TextInput({ text: $$this.templateName, placeholder: '如: 技术团队周报模板' })
            .width('100%').height(44).backgroundColor('#2a2a2a').fontColor('#fff')
            .placeholderColor('#555').borderRadius(8).padding({ left: 12, right: 12 })
        }
        .width('100%').padding({ left: 16, right: 16, top: 12 })

        // 适用部门
        Column() {
          Text('适用部门').fontSize(13).fontColor('#888').margin({ bottom: 6 }).alignSelf(ItemAlign.Start)
          TextInput({ text: $$this.templateDept, placeholder: '如: 技术部/全部' })
            .width('100%').height(44).backgroundColor('#2a2a2a').fontColor('#fff')
            .placeholderColor('#555').borderRadius(8).padding({ left: 12, right: 12 })
        }
        .width('100%').padding({ left: 16, right: 16, top: 12 })

        // 预设区块选择
        Column() {
          Text('选择模板区块').fontSize(14).fontColor('#fff').margin({ bottom: 12 }).alignSelf(ItemAlign.Start)
          this.PresetSectionCheck('本周任务', 'tasks', true)
          this.PresetSectionCheck('下周计划', 'next_tasks', true)
          this.PresetSectionCheck('问题与风险', 'issues', false)
          this.PresetSectionCheck('本周总结', 'summary', true)
          this.PresetSectionCheck('需要支持', 'support', false)
        }
        .width('100%').padding({ left: 16, right: 16, top: 12 })

        // 提示
        Text('* 标记为必填区块').fontSize(11).fontColor('#555').margin({ top: 12 })
        Text('创建后可设为默认模板').fontSize(11).fontColor('#555').margin({ top: 4 })

        // 保存按钮
        Button('保存模板')
          .fontSize(14).fontColor('#0a0a0a').backgroundColor(this.templateName ? '#c41e3a' : '#444')
          .borderRadius(8).width('100%').height(44)
          .margin({ left: 16, right: 16, top: 24 })
          .onClick(() => { this.handleCreateTemplate(); })
      }
    }
    .width('100%').layoutWeight(1).scrollBar(BarState.Auto)
  }

  @Builder
  PresetSectionCheck(title: string, type: string, isRequired: boolean) {
    Row() {
      const isSelected = this.sections.some(s => s.type === type);
      Checkbox()
        .select(isSelected)
        .selectedColor('#c41e3a')
        .onChange((value: boolean) => {
          if (value) {
            this.sections.push({ id: type, title, type, required: isRequired });
          } else {
            this.sections = this.sections.filter(s => s.type !== type);
          }
        })
      Text(title).fontSize(14).fontColor('#ccc').margin({ left: 8 }).layoutWeight(1)
      if (isRequired) {
        Text('必填').fontSize(10).fontColor('#ffcc00')
          .backgroundColor('rgba(255,204,0,0.1)').borderRadius(4)
          .padding({ left: 6, right: 6, top: 2, bottom: 2 })
      }
    }
    .width('100%').height(44).padding({ left: 4, right: 4 })
    .border({ width: { bottom: 0.5 }, color: '#333' })
  }

  handleCreateTemplate(): void {
    if (!this.templateName.trim()) return;
    const template = new WeeklyTemplate({
      name: this.templateName,
      department: this.templateDept || '全部',
      sections: this.sections.length > 0 ? this.sections : [
        { id: 's1', title: '本周任务', type: 'tasks', required: true },
        { id: 's2', title: '下周计划', type: 'next_tasks', required: true },
        { id: 's3', title: '问题与风险', type: 'issues', required: false },
        { id: 's4', title: '本周总结', type: 'summary', required: true },
        { id: 's5', title: '需要支持', type: 'support', required: false }
      ]
    });
    this.onSave?.(template);
    this.resetCreate();
  }
}

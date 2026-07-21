// 龍魂 · 基线管理弹窗 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import { Project, Baseline } from '../models/MilestoneModel';

@Component
export struct BaselineDialog {
  @Link project: Project | undefined;
  onSave?: (name: string, description: string) => void;
  onRollback?: (baselineId: string) => void;
  onCancel?: () => void;

  @State private name: string = '';
  @State private description: string = '';
  @State private selectedBaselineId: string = '';

  build() {
    Column() {
      // 标题栏
      Row() {
        Text('📊 基线管理')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor('#fff')

        Blank()

        Button() {
          Text('✕')
            .fontSize(20)
            .fontColor('#888')
        }
        .type(ButtonType.Circle)
        .backgroundColor('#00000000')
        .onClick(() => { if (this.onCancel) this.onCancel(); })
      }
      .width('100%')
      .padding(16)

      Scroll() {
        Column() {
          // 项目信息
          if (this.project) {
            Row() {
              Column() {
                Text(this.project.name)
                  .fontSize(16)
                  .fontWeight(FontWeight.Bold)
                  .fontColor('#fff')
                Text(`里程碑: ${this.project.milestones.length} | 进度: ${this.project.getProgress()}%`)
                  .fontSize(12)
                  .fontColor('#888')
                  .margin({ top: 4 })
              }
              .alignItems(HorizontalAlign.Start)
              .layoutWeight(1)
            }
            .width('100%')
            .padding(12)
            .backgroundColor('#1a1a1a')
            .borderRadius(8)
            .margin({ bottom: 16 })
          } else {
            Text('未选择项目，无法管理基线')
              .fontSize(14)
              .fontColor('#888')
              .width('100%')
              .textAlign(TextAlign.Center)
              .margin({ top: 24, bottom: 24 })
          }

          // 创建新基线
          if (this.project) {
            Text('创建新基线')
              .fontSize(14)
              .fontWeight(FontWeight.Bold)
              .fontColor('#c41e3a')
              .width('100%')
              .padding({ top: 8, bottom: 8 })

            Row() {
              Text('名称')
                .fontSize(14)
                .fontColor('#888')
                .width(80)
              TextInput({ text: this.name, placeholder: '如: V1.0基线' })
                .layoutWeight(1)
                .fontColor('#fff')
                .placeholderColor('#555')
                .backgroundColor('#1a1a1a')
                .borderRadius(6)
                .padding({ left: 12, right: 12 })
                .height(40)
                .onChange((v: string) => { this.name = v; })
            }
            .width('100%')
            .margin({ bottom: 8 })

            Row() {
              Text('描述')
                .fontSize(14)
                .fontColor('#888')
                .width(80)
              TextInput({ text: this.description, placeholder: '基线描述...' })
                .layoutWeight(1)
                .fontColor('#fff')
                .placeholderColor('#555')
                .backgroundColor('#1a1a1a')
                .borderRadius(6)
                .padding({ left: 12, right: 12 })
                .height(40)
                .onChange((v: string) => { this.description = v; })
            }
            .width('100%')
            .margin({ bottom: 12 })

            Button() {
              Text('📌 保存当前基线')
                .fontColor('#fff')
                .fontSize(14)
            }
            .type(ButtonType.Normal)
            .backgroundColor('#0066cc')
            .borderRadius(8)
            .width('100%')
            .padding(12)
            .onClick(() => {
              if (!this.name.trim()) {
                AlertDialog.show({
                  title: '提示',
                  message: '请输入基线名称',
                  primaryButton: { value: '确定', action: () => {} }
                });
                return;
              }
              if (this.onSave) this.onSave(this.name, this.description);
              AlertDialog.show({
                title: '基线已保存',
                message: `当前项目快照已保存为基线: ${this.name}`,
                primaryButton: { value: '确定', action: () => {} }
              });
            })
          }

          // 历史基线
          if (this.project && this.project.baselines.length > 0) {
            Text('历史基线')
              .fontSize(14)
              .fontWeight(FontWeight.Bold)
              .fontColor('#c41e3a')
              .width('100%')
              .padding({ top: 20, bottom: 8 })

            ForEach(this.project.baselines, (baseline: Baseline) => {
              Row() {
                Column() {
                  Text(baseline.name)
                    .fontSize(14)
                    .fontWeight(FontWeight.Medium)
                    .fontColor('#fff')

                  Text(baseline.description || '无描述')
                    .fontSize(12)
                    .fontColor('#888')
                    .margin({ top: 2 })
                    .maxLines(1)
                    .textOverflow({ overflow: TextOverflow.Ellipsis })

                  Text(`创建: ${baseline.createdAt.toLocaleString()}`)
                    .fontSize(11)
                    .fontColor('#666')
                    .margin({ top: 2 })
                }
                .alignItems(HorizontalAlign.Start)
                .layoutWeight(1)

                Button() {
                  Text('回滚')
                    .fontSize(11)
                    .fontColor('#ffcc00')
                }
                .type(ButtonType.Capsule)
                .backgroundColor('rgba(255,204,0,0.1)')
                .border({ width: 1, color: '#ffcc00' })
                .padding({ left: 10, right: 10 })
                .onClick(() => {
                  AlertDialog.show({
                    title: '确认回滚',
                    message: `回滚到基线「${baseline.name}」？当前未保存的变更将丢失`,
                    primaryButton: {
                      value: '确认回滚',
                      action: () => {
                        if (this.onRollback) this.onRollback(baseline.id);
                        AlertDialog.show({
                          title: '回滚完成',
                          message: `已回滚到基线: ${baseline.name}`,
                          primaryButton: { value: '确定', action: () => {} }
                        });
                      }
                    },
                    secondaryButton: { value: '取消', action: () => {} }
                  });
                })
              }
              .width('100%')
              .padding(12)
              .backgroundColor('#1a1a1a')
              .borderRadius(8)
              .margin({ top: 8 })
            }, (baseline: Baseline) => baseline.id)
          }

          // 提示
          Text('💡 基线保存当前项目快照，包含所有里程碑状态、预算和时间计划')
            .fontSize(11)
            .fontColor('#555')
            .width('100%')
            .textAlign(TextAlign.Center)
            .padding({ top: 16, bottom: 16 })
        }
        .width('100%')
        .padding({ left: 16, right: 16, bottom: 80 })
      }
      .layoutWeight(1)
      .width('100%')
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }
}

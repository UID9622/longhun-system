/**
 * 龙魂·审计页 — 参数输入 + 执行审计
 * License: MulanPSL v2
 */
import { TricolorAudit } from '../engine/TricolorAudit';
import { AuditInput, AuditResult } from '../models/AuditModels';
import { DARK_GOLD } from '../models/Constants';
import router from '@ohos.router';

@Entry
@Component
struct AuditPage {
  @State description: string = '';
  @State target: string = '';
  @State isLoading: boolean = false;
  @State error: string = '';
  private auditor: TricolorAudit = TricolorAudit.getInstance();

  build() {
    Column() {
      // 标题
      Row() {
        Text('←')
          .fontSize(24)
          .fontColor(DARK_GOLD.PRIMARY)
          .onClick(() => router.back())
        Text('执行审计')
          .fontSize(20)
          .fontColor(DARK_GOLD.TEXT_PRIMARY)
          .margin({ left: 12 })
      }
      .width('100%')
      .padding(16)

      // 审计目标
      TextInput({ placeholder: '审计目标（代码/文档/协议...）', text: this.target })
        .width('90%')
        .height(48)
        .fontSize(15)
        .backgroundColor(DARK_GOLD.BG_CARD)
        .fontColor(DARK_GOLD.TEXT_PRIMARY)
        .placeholderColor(DARK_GOLD.TEXT_SECONDARY)
        .borderRadius(8)
        .border({ width: 1, color: DARK_GOLD.BORDER })
        .onChange((v: string) => { this.target = v; })
        .padding(12)
        .margin({ bottom: 12 })

      // 描述
      TextArea({ placeholder: '描述审计对象的具体内容和背景...', text: this.description })
        .width('90%')
        .height(160)
        .fontSize(14)
        .backgroundColor(DARK_GOLD.BG_CARD)
        .fontColor(DARK_GOLD.TEXT_PRIMARY)
        .placeholderColor(DARK_GOLD.TEXT_SECONDARY)
        .borderRadius(8)
        .border({ width: 1, color: DARK_GOLD.BORDER })
        .onChange((v: string) => { this.description = v; })
        .padding(12)
        .margin({ bottom: 20 })

      // 错误提示
      if (this.error) {
        Text(this.error)
          .fontSize(13)
          .fontColor(DARK_GOLD.ERROR)
          .padding({ left: 20, right: 20, bottom: 10 })
      }

      // 执行按钮
      Button(this.isLoading ? '审计中...' : '🔍 执行三色审计')
        .fontSize(18)
        .backgroundColor(this.isLoading ? '#555' : DARK_GOLD.PRIMARY)
        .fontColor(DARK_GOLD.BG_DARK)
        .width('80%')
        .height(52)
        .borderRadius(26)
        .enabled(!this.isLoading)
        .onClick(() => { this.runAudit(); })

      // 提示
      Text('输入审计目标与描述，系统将自动进行六维加权评估')
        .fontSize(11)
        .fontColor(DARK_GOLD.TEXT_SECONDARY)
        .margin({ top: 16 })
        .padding({ left: 30, right: 30 })
        .textAlign(TextAlign.Center)
    }
    .width('100%')
    .height('100%')
    .backgroundColor(DARK_GOLD.BG_DARK)
  }

  async runAudit() {
    if (!this.target.trim()) {
      this.error = '请输入审计目标';
      return;
    }
    if (!this.description.trim()) {
      this.error = '请输入审计描述';
      return;
    }
    this.error = '';
    this.isLoading = true;

    try {
      const input: AuditInput = {
        auditTarget: this.target.trim(),
        description: this.description.trim(),
        metadata: { source: 'HarmonyOS-TricolorAudit-App' }
      };
      const result: AuditResult = await this.auditor.audit(input);

      // 临时存储结果
      AppStorage.setOrCreate('lastAuditResult', JSON.stringify(result));

      router.pushUrl({ url: 'pages/ResultPage' });
    } catch (e) {
      this.error = `审计异常: ${e}`;
    } finally {
      this.isLoading = false;
    }
  }
}

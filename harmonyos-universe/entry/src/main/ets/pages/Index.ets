归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/*
 * ==========================================================================
 * 通心译 — 主翻译页面
 * DNA:#龍芯⚡️丙午·丙申·癸丑·午时·需-TONGXINYI-INDEX-v1.0
 * ==========================================================================
 * 功能:
 *   1. 文本输入 → 通心译翻译
 *   2. 术语查询 → 搜索解释
 *   3. 术语库浏览 → 全量术语查看
 *   4. 三色审计 → 质量评分
 * ==========================================================================
 */

import { TongxinTranslator } from '../core/TongxinTranslator';
import { TranslationMode, TranslationResult, AuditLevel, AUDIT_EMOJI } from '../common/types';
import { ScreenAdapter } from '../utils/ScreenAdapter';

@Entry
@Component
struct Index {
  @State inputText: string = '';
  @State translatedText: string = '';
  @State sourceLang: string = 'EN → 中文';
  @State auditEmoji: string = '🟢';
  @State auditScore: string = '--';
  @State dnaCode: string = '';
  @State isTranslating: boolean = false;
  @State showTerms: boolean = false;

  private translator: TongxinTranslator = new TongxinTranslator();

  aboutToAppear(): void {
    this.sourceLang = 'EN → 中文';
  }

  build() {
    Column() {
      // ===== 标题栏 =====
      Row() {
        Text('通心译')
          .fontSize(ScreenAdapter.fp2px(24))
          .fontWeight(FontWeight.Bold)
          .fontColor('#1a1a2e')

        Blank()

        Button('术语库')
          .fontSize(ScreenAdapter.fp2px(14))
          .backgroundColor('#e8e8f0')
          .fontColor('#1a1a2e')
          .borderRadius(8)
          .padding({ left: 12, right: 12, top: 6, bottom: 6 })
          .onClick(() => {
            this.showTerms = !this.showTerms;
          })
      }
      .width('100%')
      .padding({ left: 16, right: 16, top: 12, bottom: 8 })

      Divider()
        .color('#e0e0e8')
        .strokeWidth(0.5)

      // ===== 模式切换 =====
      Row() {
        Button('EN → 中文')
          .fontSize(ScreenAdapter.fp2px(14))
          .backgroundColor(this.sourceLang === 'EN → 中文' ? '#4a6cf7' : '#e8e8f0')
          .fontColor(this.sourceLang === 'EN → 中文' ? '#ffffff' : '#666')
          .borderRadius(6)
          .padding({ left: 12, right: 12, top: 4, bottom: 4 })
          .onClick(() => { this.sourceLang = 'EN → 中文'; })

        Button('中文 → EN')
          .fontSize(ScreenAdapter.fp2px(14))
          .backgroundColor(this.sourceLang === '中文 → EN' ? '#4a6cf7' : '#e8e8f0')
          .fontColor(this.sourceLang === '中文 → EN' ? '#ffffff' : '#666')
          .borderRadius(6)
          .margin({ left: 8 })
          .padding({ left: 12, right: 12, top: 4, bottom: 4 })
          .onClick(() => { this.sourceLang = '中文 → EN'; })

        Button('双语')
          .fontSize(ScreenAdapter.fp2px(14))
          .backgroundColor(this.sourceLang === '双语' ? '#4a6cf7' : '#e8e8f0')
          .fontColor(this.sourceLang === '双语' ? '#ffffff' : '#666')
          .borderRadius(6)
          .margin({ left: 8 })
          .padding({ left: 12, right: 12, top: 4, bottom: 4 })
          .onClick(() => { this.sourceLang = '双语'; })
      }
      .width('100%')
      .padding({ left: 16, right: 16, top: 12, bottom: 8 })

      // ===== 术语库视图 (条件展示) =====
      if (this.showTerms) {
        List({ space: 4 }) {
          // 固定显示 10 个核心术语
          ForEach(this.getTopTerms(), (item: TermDisplayItem) => {
            ListItem() {
              Column() {
                Row() {
                  Text(item.en)
                    .fontSize(ScreenAdapter.fp2px(14))
                    .fontWeight(FontWeight.Medium)
                    .fontColor('#1a1a2e')
                  Text(' ↔ ')
                    .fontSize(ScreenAdapter.fp2px(12))
                    .fontColor('#999')
                  Text(item.zh)
                    .fontSize(ScreenAdapter.fp2px(14))
                    .fontColor('#4a6cf7')
                    .fontWeight(FontWeight.Medium)
                }
                Text(item.explanation)
                  .fontSize(ScreenAdapter.fp2px(12))
                  .fontColor('#888')
                  .maxLines(2)
                  .textOverflow({ overflow: TextOverflow.Ellipsis })
                  .margin({ top: 2 })
              }
              .alignItems(HorizontalAlign.Start)
              .width('100%')
              .padding(8)
              .backgroundColor('#f8f8fc')
              .borderRadius(6)
            }
          }, (item: TermDisplayItem) => item.en)
        }
        .height(200)
        .padding({ left: 16, right: 16 })
        .scrollBar(BarState.Off)
      }

      // ===== 输入区域 =====
      TextArea({ placeholder: '输入要翻译的文本...', text: this.inputText })
        .fontSize(ScreenAdapter.fp2px(16))
        .placeholderColor('#bbb')
        .backgroundColor('#ffffff')
        .borderRadius(12)
        .border({ width: 1, color: '#e0e0e8' })
        .padding(16)
        .margin({ left: 16, right: 16, top: 12 })
        .height(ScreenAdapter.isTablet() ? 180 : 120)
        .onChange((value: string) => {
          this.inputText = value;
        })

      // ===== 翻译按钮 =====
      Button(this.isTranslating ? '翻译中...' : '通心译 →')
        .fontSize(ScreenAdapter.fp2px(18))
        .fontWeight(FontWeight.Medium)
        .backgroundColor('#4a6cf7')
        .fontColor('#ffffff')
        .borderRadius(12)
        .width('92%')
        .height(48)
        .margin({ top: 16 })
        .shadow({ radius: 8, color: '#4a6cf740' })
        .enabled(!this.isTranslating)
        .onClick(() => {
          this.doTranslate();
        })

      // ===== 翻译结果 =====
      if (this.translatedText.length > 0) {
        Column() {
          // 审计状态条
          Row() {
            Text(`${this.auditEmoji} 三色审计: ${this.auditScore}分`)
              .fontSize(ScreenAdapter.fp2px(12))
              .fontColor(this.auditEmoji === '🔴' ? '#e74c3c' : (this.auditEmoji === '🟡' ? '#f39c12' : '#27ae60'))
              .padding({ left: 8, right: 8, top: 2, bottom: 2 })
              .backgroundColor('#f5f5fa')
              .borderRadius(4)

            Blank()

            if (this.dnaCode.length > 0) {
              Text(`DNA: ${this.dnaCode.substring(0, 30)}...`)
                .fontSize(ScreenAdapter.fp2px(10))
                .fontColor('#aaa')
                .maxLines(1)
            }
          }
          .width('100%')
          .padding({ left: 16, right: 16, top: 8, bottom: 4 })

          // 翻译结果卡片
          Column() {
            Text(this.translatedText)
              .fontSize(ScreenAdapter.fp2px(15))
              .fontColor('#2c3e50')
              .lineHeight(24)
              .width('100%')
              .textAlign(TextAlign.Start)
          }
          .width('92%')
          .padding(16)
          .backgroundColor('#fdfdfe')
          .borderRadius(12)
          .border({ width: 1, color: '#e8e8f0' })
          .margin({ top: 8 })
        }
        .width('100%')
      }

      // ===== 底部 =====
      Text('🐉 龍魂体系 · 通心译 v1.0 · 华为芯片·鸿蒙底座')
        .fontSize(ScreenAdapter.fp2px(10))
        .fontColor('#ccc')
        .margin({ top: ScreenAdapter.isTablet() ? 32 : 16, bottom: 16 })
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#f5f6fa')
  }

  /**
   * 执行翻译
   */
  private doTranslate(): void {
    if (this.inputText.trim().length === 0) return;

    this.isTranslating = true;

    // 无阻塞翻译 (通心译引擎是纯内存操作)
    let mode: TranslationMode;
    switch (this.sourceLang) {
      case '中文 → EN': mode = TranslationMode.ZH_TO_EN; break;
      case '双语': mode = TranslationMode.BILINGUAL; break;
      default: mode = TranslationMode.EN_TO_ZH;
    }

    const result: TranslationResult = this.translator.translate(this.inputText, mode);

    this.translatedText = result.translated;
    this.dnaCode = result.dnaCode;
    this.auditEmoji = AUDIT_EMOJI[result.auditLevel];
    this.auditScore = result.auditScore.toFixed(0);
    this.isTranslating = false;
  }

  /**
   * 获取高频术语展示列表
   */
  private getTopTerms(): TermDisplayItem[] {
    const items: TermDisplayItem[] = [];
    const allTerms = this.translator.db.getAllTerms();
    const count = 0;
    for (const [en, zh] of allTerms.entries()) {
      if (items.length >= 10) break;
      const zhExpl = this.translator.db.getZHExplanation(zh);
      items.push({
        en: en,
        zh: zh,
        explanation: zhExpl || ''
      });
    }
    return items;
  }
}

interface TermDisplayItem {
  en: string;
  zh: string;
  explanation: string;
}

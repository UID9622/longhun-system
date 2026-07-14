// entry/src/main/ets/pages/GuoxueCreation.ets
// 龍魂 · 国学创作鸿蒙主页面
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622
// CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

import { guoxueState, GuoxueState, CreationType, MASTER_UID } from '../models/GuoxueModel';
import { coupletEngine } from '../engines/CoupletEngine';
import { acrosticEngine } from '../engines/AcrosticEngine';
import { figureEngine } from '../engines/HistoricalFigureEngine';
import { daoDeJingEngine } from '../engines/DaoDeJingEngine';
import { heTuLuoShuEngine } from '../engines/HeTuLuoShuEngine';
import { wuXingBaGuaEngine } from '../engines/WuXingBaGuaEngine';
import { xingXiuEngine } from '../engines/XingXiuEngine';

@Entry
@Component
struct GuoxueCreationPage {
  @StorageLink('guoxueState') guoxueState: GuoxueState = guoxueState;
  @State private selectedTab: number = 0;
  @State private inputText: string = '';
  @State private resultText: string = '';
  @State private detailVisible: boolean = false;
  @State private detailContent: string = '';

  private tabs = [
    { label: '对联', icon: '🏮', type: CreationType.COUPLET },
    { label: '藏头诗', icon: '✒️', type: CreationType.ACROSTIC_POEM },
    { label: '历史人物', icon: '👤', type: CreationType.HISTORICAL_FIGURE },
    { label: '道德经', icon: '📜', type: CreationType.DAO_DE_JING },
    { label: '河图洛书', icon: '🔢', type: CreationType.HE_TU },
    { label: '五行八卦', icon: '☯️', type: CreationType.WU_XING },
    { label: '二十八宿', icon: '⭐', type: CreationType.XING_XIU }
  ];

  build() {
    Column() {
      this.HeaderBuilder()
      this.TabBuilder()
      this.ContentBuilder()
      this.FooterBuilder()
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  @Builder
  HeaderBuilder() {
    Row() {
      Text('🐉').fontSize(28).margin({ right: 8 })
      Column() {
        Text('龍魂国学创作').fontSize(20).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        Text(`UID:${MASTER_UID} · 传统文化引擎`).fontSize(12).fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  TabBuilder() {
    Scroll() {
      Row() {
        ForEach(this.tabs, (tab: { label: string, icon: string, type: CreationType }, index: number) => {
          Column() {
            Text(tab.icon).fontSize(20)
            Text(tab.label)
              .fontSize(11)
              .fontColor(this.selectedTab === index ? '#c41e3a' : '#888')
              .margin({ top: 4 })
            if (this.selectedTab === index) {
              Divider()
                .strokeWidth(2)
                .color('#c41e3a')
                .width(20)
                .margin({ top: 4 })
            }
          }
          .padding({ top: 8, bottom: 8, left: 12, right: 12 })
          .onClick(() => {
            this.selectedTab = index;
            this.resultText = '';
            this.inputText = '';
            this.detailVisible = false;
          })
        })
      }
      .width('100%')
    }
    .scrollBar(BarState.Auto)
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  ContentBuilder() {
    Scroll() {
      Column() {
        this.InputBuilder()
        this.ActionBuilder()
        this.ResultBuilder()
        if (this.detailVisible) {
          this.DetailBuilder()
        }
      }
      .width('100%')
      .padding(16)
    }
    .width('100%')
    .layoutWeight(1)
    .scrollBar(BarState.Auto)
  }

  @Builder
  InputBuilder() {
    Column() {
      Text(this.tabs[this.selectedTab].label + '创作')
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .fontColor('#fff')
        .margin({ bottom: 12 })
        .width('100%')

      // === 对联 ===
      if (this.selectedTab === 0) {
        Text('输入主题（如：春节、龙年、励志）')
          .fontSize(12).fontColor('#666').margin({ bottom: 8 }).width('100%')
        TextInput({ placeholder: '输入主题...', text: $$this.inputText })
          .width('100%').height(44).fontSize(14).fontColor('#fff')
          .placeholderColor('#666').backgroundColor('#1a1a1a')
          .borderRadius(8).padding({ left: 12, right: 12 })
      }

      // === 藏头诗 ===
      if (this.selectedTab === 1) {
        Text('输入藏头字（如：龍魂中国）')
          .fontSize(12).fontColor('#666').margin({ bottom: 8 }).width('100%')
        TextInput({ placeholder: '输入藏头字...', text: $$this.inputText })
          .width('100%').height(44).fontSize(14).fontColor('#fff')
          .placeholderColor('#666').backgroundColor('#1a1a1a')
          .borderRadius(8).padding({ left: 12, right: 12 })
      }

      // === 历史人物 ===
      if (this.selectedTab === 2) {
        Text('输入人物名（如：诸葛亮、岳飞）')
          .fontSize(12).fontColor('#666').margin({ bottom: 8 }).width('100%')
        TextInput({ placeholder: '输入人物名...', text: $$this.inputText })
          .width('100%').height(44).fontSize(14).fontColor('#fff')
          .placeholderColor('#666').backgroundColor('#1a1a1a')
          .borderRadius(8).padding({ left: 12, right: 12 })
      }

      // === 道德经 ===
      if (this.selectedTab === 3) {
        Text('输入章节号(1-81)或关键词')
          .fontSize(12).fontColor('#666').margin({ bottom: 8 }).width('100%')
        TextInput({ placeholder: '输入章节号或关键词...', text: $$this.inputText })
          .width('100%').height(44).fontSize(14).fontColor('#fff')
          .placeholderColor('#666').backgroundColor('#1a1a1a')
          .borderRadius(8).padding({ left: 12, right: 12 })
      }

      // === 河图洛书 ===
      if (this.selectedTab === 4) {
        Text('点击下方按钮查看河图或洛书')
          .fontSize(12).fontColor('#666').margin({ bottom: 8 }).width('100%')
      }

      // === 五行八卦 ===
      if (this.selectedTab === 5) {
        Text('输入五行（金木水火土）或八卦（乾坤震巽坎离艮兑）')
          .fontSize(12).fontColor('#666').margin({ bottom: 8 }).width('100%')
        TextInput({ placeholder: '如：金、乾...', text: $$this.inputText })
          .width('100%').height(44).fontSize(14).fontColor('#fff')
          .placeholderColor('#666').backgroundColor('#1a1a1a')
          .borderRadius(8).padding({ left: 12, right: 12 })
      }

      // === 二十八星宿 ===
      if (this.selectedTab === 6) {
        Text('选择四象方向或输入星宿名称')
          .fontSize(12).fontColor('#666').margin({ bottom: 8 }).width('100%')
        TextInput({ placeholder: '如：角、东方青龙...', text: $$this.inputText })
          .width('100%').height(44).fontSize(14).fontColor('#fff')
          .placeholderColor('#666').backgroundColor('#1a1a1a')
          .borderRadius(8).padding({ left: 12, right: 12 })
      }
    }
  }

  @Builder
  ActionBuilder() {
    Column() {
      // === 河图洛书专用按钮 ===
      if (this.selectedTab === 4) {
        Row() {
          Button('📊 查看河图')
            .fontSize(14).fontColor('#fff')
            .backgroundColor('#1a1a1a')
            .border({ width: 1, color: '#c41e3a' })
            .borderRadius(8).height(40).layoutWeight(1)
            .onClick(() => {
              const heTu = heTuLuoShuEngine.getHeTu();
              this.resultText = '【河图·数字矩阵】\n' +
                heTu.matrix.map(r => r.join('  ')).join('\n') + '\n\n' +
                '【口诀】\n' + heTu.mnemonic.join('\n') + '\n\n' +
                '【说明】\n' + heTu.description;
            })

          Button('🔢 查看洛书')
            .fontSize(14).fontColor('#fff')
            .backgroundColor('#1a1a1a')
            .border({ width: 1, color: '#c41e3a' })
            .borderRadius(8).height(40).layoutWeight(1)
            .margin({ left: 12 })
            .onClick(() => {
              const luoShu = heTuLuoShuEngine.getLuoShu();
              const isValid = heTuLuoShuEngine.validateLuoShu();
              this.resultText = '【洛书·幻方矩阵 幻和=' + luoShu.magicSum + '】\n' +
                luoShu.matrix.map(r => r.join('  ')).join('\n') + '\n\n' +
                '【口诀】\n' + luoShu.mnemonic.join('\n') + '\n\n' +
                '【幻方验证】' + (isValid ? '✅ 通过' : '❌ 失败') + '\n\n' +
                '【说明】\n' + luoShu.description;
            })
        }
        .width('100%')
        .margin({ top: 12 })
      }

      // === 道德经专用按钮 ===
      if (this.selectedTab === 3) {
        Row() {
          Button('📖 随机一页')
            .fontSize(14).fontColor('#fff')
            .backgroundColor('#1a1a1a')
            .border({ width: 1, color: '#c41e3a' })
            .borderRadius(8).height(40).layoutWeight(1)
            .onClick(() => {
              const chapter = daoDeJingEngine.getRandom();
              this.formatDaoChapterResult(chapter);
            })

          Button('📋 全部章节')
            .fontSize(14).fontColor('#fff')
            .backgroundColor('#1a1a1a')
            .border({ width: 1, color: '#c41e3a' })
            .borderRadius(8).height(40).layoutWeight(1)
            .margin({ left: 12 })
            .onClick(() => {
              const all = daoDeJingEngine.getAllChapters();
              this.resultText = '【道德经·' + all.length + '章摘要】\n\n' +
                all.map(c => `第${c.chapter}章 · ${c.title}\n${c.original.substring(0, 30)}...`).join('\n\n');
            })
        }
        .width('100%')
        .margin({ top: 12 })
      }

      // === 五行八卦专用按钮 ===
      if (this.selectedTab === 5) {
        Row() {
          Button('🔄 全部五行').fontSize(12).fontColor('#fff')
            .backgroundColor('#1a1a1a').border({ width: 1, color: '#333' })
            .borderRadius(8).height(36).layoutWeight(1)
            .onClick(() => {
              const all = wuXingBaGuaEngine.getAllWuXing();
              this.resultText = '【五行总览】\n\n' + all.map(w =>
                `${w.element} · ${w.color} · ${w.direction} · ${w.season}\n生${w.generation.replace('生','')} · ${w.restriction}\n脏:${w.organ} · 情:${w.emotion}`
              ).join('\n\n');
            })

          Button('🔄 全部八卦').fontSize(12).fontColor('#fff')
            .backgroundColor('#1a1a1a').border({ width: 1, color: '#333' })
            .borderRadius(8).height(36).layoutWeight(1).margin({ left: 8 })
            .onClick(() => {
              const all = wuXingBaGuaEngine.getAllBaGua();
              this.resultText = '【八卦总览】\n\n' + all.map(g =>
                `${g.symbol} ${g.name} · ${g.nature} · ${g.attribute}\n方位:${g.direction} · 家庭:${g.family} · 数:${g.number}`
              ).join('\n\n');
            })
        }
        .width('100%')
        .margin({ top: 12 })

        Row() {
          Button('⚡ 生克关系').fontSize(12).fontColor('#fff')
            .backgroundColor('#1a1a1a').border({ width: 1, color: '#333' })
            .borderRadius(8).height(36).layoutWeight(1)
            .onClick(() => {
              this.resultText = '【五行生克推演】\n\n金生水·克木 | 木生火·克土\n水生木·克火 | 火生土·克金\n土生金·克水\n\n【八卦配五行】\n乾兑→金 | 震巽→木 | 坎→水\n离→火 | 坤艮→土';
            })
        }
        .width('100%')
        .margin({ top: 8 })
      }

      // === 二十八宿专用按钮 ===
      if (this.selectedTab === 6) {
        Row() {
          ForEach(xingXiuEngine.getFourAnimals(), (animal: string) => {
            Button(xingXiuEngine.getAnimalEmoji(animal) + ' ' + animal.replace('东方','').replace('北方','').replace('西方','').replace('南方',''))
              .fontSize(11).fontColor('#fff')
              .backgroundColor('#1a1a1a').border({ width: 1, color: '#333' })
              .borderRadius(8).height(36).layoutWeight(1).margin({ left: 4, right: 4 })
              .onClick(() => {
                const list = xingXiuEngine.getByDirection(animal);
                this.resultText = `【${animal}七宿】\n\n` + list.map(x =>
                  `${x.auspicious ? '✅' : '⚠️'} ${x.name} · ${x.constellation}\n${x.meaning}`
                ).join('\n\n');
              })
          })
        }
        .width('100%')
        .margin({ top: 12 })

        Row() {
          Button('📊 吉凶统计').fontSize(12).fontColor('#fff')
            .backgroundColor('#1a1a1a').border({ width: 1, color: '#333' })
            .borderRadius(8).height(36).layoutWeight(1)
            .onClick(() => {
              const stats = xingXiuEngine.getAuspiciousCount();
              this.resultText = `【二十八星宿·吉凶统计】\n\n✅ 吉星: ${stats.auspicious}宿\n⚠️ 凶星: ${stats.inauspicious}宿\n\n比率: ${(stats.auspicious / 28 * 100).toFixed(1)}% 为吉`;
            })
        }
        .width('100%')
        .margin({ top: 8 })
      }

      // === 通用查询按钮（对联/藏头诗/历史人物/道德经/五行八卦/星宿） ===
      if (this.selectedTab !== 4) {
        Button('🔍 生成/查询')
          .fontSize(15).fontColor('#fff').fontWeight(FontWeight.Bold)
          .backgroundColor('#c41e3a').borderRadius(8).height(44)
          .width('100%').margin({ top: 12 })
          .onClick(() => {
            this.handleGenerate();
          })
      }
    }
  }

  private handleGenerate(): void {
    if (!this.inputText && this.selectedTab !== 4) {
      this.resultText = '⚠️ 请输入内容';
      return;
    }

    try {
      // 对联
      if (this.selectedTab === 0) {
        const couplet = coupletEngine.generate(this.inputText);
        this.resultText = '【对联·' + couplet.theme + '】\n\n' +
          '上联：' + couplet.upper + '\n' +
          '下联：' + couplet.lower + '\n' +
          '横批：' + couplet.horizontal + '\n\n' +
          '【平仄分析】\n' + couplet.tonePattern + '\n\n' +
          '【DNA签名】\n' + couplet.dnaSignature;
        this.guoxueState.couplets.push(couplet);
      }

      // 藏头诗
      if (this.selectedTab === 1) {
        const poem = acrosticEngine.generate(this.inputText);
        this.resultText = '【藏头诗·' + poem.headWord + '】\n\n' +
          poem.lines.map((l, i) => `${poem.headWord[i]} · ${l}`).join('\n') + '\n\n' +
          '【DNA签名】\n' + poem.dnaSignature;
        this.guoxueState.acrostics.push(poem);
      }

      // 历史人物
      if (this.selectedTab === 2) {
        const figure = figureEngine.query(this.inputText);
        if (figure) {
          this.resultText = '【' + figure.name + '】\n' +
            '朝代：' + figure.dynasty + '\n' +
            '生卒：' + figure.era + '\n\n' +
            '【成就】\n' + figure.achievements.map(a => '· ' + a).join('\n') + '\n\n' +
            '【性格】\n' + figure.personality + '\n\n' +
            '【名言】\n' + figure.famousQuotes.map(q => '「' + q + '」').join('\n') + '\n\n' +
            '【相关事件】\n' + figure.relatedEvents.map(e => '· ' + e).join('\n') + '\n\n' +
            '【DNA签名】\n' + figure.dnaSignature;
          this.guoxueState.figures.push(figure);
        } else {
          // 模糊搜索
          const results = figureEngine.search(this.inputText);
          if (results.length > 0) {
            this.resultText = '【搜索「' + this.inputText + '」找到' + results.length + '位人物】\n\n' +
              results.map(f => f.name + ' · ' + f.dynasty).join('\n');
          } else {
            this.resultText = '未找到「' + this.inputText + '」，试试：\n' + figureEngine.getAllNames().slice(0, 6).join(' / ');
          }
        }
      }

      // 道德经
      if (this.selectedTab === 3) {
        const num = parseInt(this.inputText);
        if (!isNaN(num)) {
          const chapter = daoDeJingEngine.getChapter(num);
          if (chapter) {
            this.formatDaoChapterResult(chapter);
          } else {
            this.resultText = '未找到第' + num + '章，当前收录核心章节：\n' +
              daoDeJingEngine.getAllChapters().map(c => '第' + c.chapter + '章·' + c.title).join(' | ');
          }
        } else {
          const results = daoDeJingEngine.searchByKeyword(this.inputText);
          if (results.length > 0) {
            this.resultText = '【搜索「' + this.inputText + '」找到' + results.length + '章】\n\n' +
              results.map(c => '第' + c.chapter + '章 · ' + c.title + '\n' + c.original.substring(0, 40) + '...').join('\n\n');
          } else {
            this.resultText = '未找到相关章节，可用章节号查询(1/2/3/8/16/25/33/40/42/64/81)';
          }
        }
      }

      // 五行八卦
      if (this.selectedTab === 5) {
        const wx = wuXingBaGuaEngine.getWuXing(this.inputText);
        const bg = wuXingBaGuaEngine.getBaGua(this.inputText);
        if (wx) {
          this.resultText = '【五行·' + wx.element + '】\n' +
            '颜色：' + wx.color + ' | 方位：' + wx.direction + ' | 季节：' + wx.season + '\n' +
            '生克：' + wx.generation + ' · ' + wx.restriction + '\n' +
            '脏腑：' + wx.organ + ' | 情志：' + wx.emotion + '\n\n' +
            '【DNA签名】\n' + wx.dnaSignature;
          this.guoxueState.wuXingList.push(wx);
        } else if (bg) {
          const wxName = wuXingBaGuaEngine.getBaGuaWuXing(this.inputText);
          const desc = wuXingBaGuaEngine.getGuaDescription(this.inputText);
          this.resultText = '【八卦·' + bg.symbol + ' ' + bg.name + '】\n' +
            '自然：' + bg.nature + ' | 属性：' + bg.attribute + '\n' +
            '方位：' + bg.direction + ' | 家庭：' + bg.family + '\n' +
            '卦数：' + bg.number + ' | 配五行：' + wxName + '\n\n' +
            '【卦辞】\n' + desc + '\n\n' +
            '【DNA签名】\n' + bg.dnaSignature;
          this.guoxueState.baGuaList.push(bg);
        } else {
          this.resultText = '请输入：金/木/水/火/土 或 乾/坤/震/巽/坎/离/艮/兑';
        }
      }

      // 二十八星宿
      if (this.selectedTab === 6) {
        const xing = xingXiuEngine.getByName(this.inputText);
        if (xing) {
          this.resultText = '【星宿·' + xing.name + '】\n' +
            '方位：' + xing.direction + ' | 四象：' + xing.animal + '\n' +
            '对应星座：' + xing.constellation + '\n' +
            '吉凶：' + (xing.auspicious ? '✅ 吉' : '⚠️ 凶') + '\n' +
            '含义：' + xing.meaning + '\n\n' +
            '【DNA签名】\n' + xing.dnaSignature;
          this.guoxueState.xingXiuList.push(xing);
        } else {
          const dirList = xingXiuEngine.getByDirection(this.inputText);
          if (dirList.length > 0) {
            this.resultText = `【${this.inputText}七宿】\n\n` + dirList.map(x =>
              `${x.auspicious ? '✅' : '⚠️'} ${x.name} · ${x.constellation}\n${x.meaning}`
            ).join('\n\n');
          } else {
            this.resultText = '请输入星宿名（如：角、斗、奎、井）或四象方向（东方青龙/北方玄武/西方白虎/南方朱雀）';
          }
        }
      }
    } catch (err) {
      this.resultText = '生成出错：' + err;
    }
  }

  private formatDaoChapterResult(chapter: import('../models/GuoxueModel').DaoDeJingChapter): void {
    this.resultText = '【道德经·第' + chapter.chapter + '章】' + chapter.title + '\n\n' +
      '📜 原文：\n' + chapter.original + '\n\n' +
      '📖 译文：\n' + chapter.translation + '\n\n' +
      '💡 解读：\n' + chapter.interpretation + '\n\n' +
      '🔑 关键词：' + chapter.keywords.join(' · ') + '\n\n' +
      '【DNA签名】\n' + chapter.dnaSignature;
  }

  @Builder
  ResultBuilder() {
    if (this.resultText.length > 0) {
      Column() {
        Row() {
          Text('📋 生成结果')
            .fontSize(14).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
            .layoutWeight(1)
          Button('✕')
            .fontSize(14).fontColor('#666').backgroundColor('#0000')
            .width(28).height(28)
            .onClick(() => { this.resultText = ''; })
        }
        .width('100%')
        .margin({ top: 16, bottom: 8 })

        Text(this.resultText)
          .fontSize(13)
          .fontColor('#ddd')
          .width('100%')
          .padding(12)
          .backgroundColor('#1a1a1a')
          .borderRadius(8)
          .border({ width: 1, color: '#333' })
      }
      .width('100%')
    }
  }

  @Builder
  DetailBuilder() {
    Column() {
      Row() {
        Text('📖 详情').fontSize(14).fontWeight(FontWeight.Bold).fontColor('#c41e3a').layoutWeight(1)
        Button('✕').fontSize(14).fontColor('#666').backgroundColor('#0000')
          .width(28).height(28)
          .onClick(() => { this.detailVisible = false; })
      }
      .width('100%').margin({ bottom: 8 })

      Text(this.detailContent)
        .fontSize(13).fontColor('#ddd').width('100%')
        .padding(12).backgroundColor('#1a1a1a')
        .borderRadius(8).border({ width: 1, color: '#333' })
    }
    .width('100%')
    .margin({ top: 12 })
    .padding(12)
    .backgroundColor('#111')
    .borderRadius(8)
  }

  @Builder
  FooterBuilder() {
    Row() {
      Text(`🏮 ${this.guoxueState.statistics.totalCouplets}`).fontSize(11).fontColor('#888').margin({ right: 12 })
      Text(`✒️ ${this.guoxueState.statistics.totalAcrostics}`).fontSize(11).fontColor('#888').margin({ right: 12 })
      Text(`👤 ${this.guoxueState.statistics.totalFigures}`).fontSize(11).fontColor('#888').margin({ right: 12 })
      Text(`📜 ${this.guoxueState.statistics.totalDaoChapters}`).fontSize(11).fontColor('#888')
    }
    .width('100%')
    .height(36)
    .justifyContent(FlexAlign.Center)
    .backgroundColor('#1a1a1a')
    .border({ width: { top: 1 }, color: '#333' })
  }
}

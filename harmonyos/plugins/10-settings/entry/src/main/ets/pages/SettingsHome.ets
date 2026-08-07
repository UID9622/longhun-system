/**
 * 🐉 龍魂·设置 — SettingsHome + About + License
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-SETTINGS-PAGES-UID9622
 */

import { router } from '@kit.ArkUI';
import { promptAction } from '@kit.ArkUI';

// ─── 设置首页 ───
@Entry
@Component
struct SettingsHome {
  @State supervisionInterval: number = 30;
  @State syncEnabled: boolean = true;
  @State alertEnabled: boolean = true;
  @State evolutionEnabled: boolean = true;
  @State darkMode: boolean = true;
  @State themeIndex: number = 0;
  private intervals: number[] = [15, 30, 60];

  build() {
    Scroll() {
      Column({ space: 0 }) {
        Row() {
          Text('⚙️ 設置').fontSize(20).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
        }.width('100%').padding(16)

        // 监督频率
        SectionHeader('📡 監督設置')
        ForEach(['15 分鐘', '30 分鐘', '60 分鐘'], (label: string, idx: number) => {
          Row() {
            Text(label).fontSize(14).fontColor('#E5E7EB').layoutWeight(1)
            Radio({ value: `${this.intervals[idx]}`, group: 'interval' }).checked(this.supervisionInterval === this.intervals[idx])
              .onChange((v: boolean) => { if (v) this.supervisionInterval = this.intervals[idx]; })
          }
          .width('100%').padding({ left: 20, right: 16, top: 10, bottom: 10 })
          .border({ width: { bottom: 0.5 }, color: '#1E293B', style: BorderStyle.Solid })
        })

        // 开关区
        SectionHeader('🔌 功能開關')
        ToggleRow('跨設備同步', this.syncEnabled, (v: boolean) => { this.syncEnabled = v; })
        ToggleRow('警報通知', this.alertEnabled, (v: boolean) => { this.alertEnabled = v; })
        ToggleRow('進化引擎通知', this.evolutionEnabled, (v: boolean) => { this.evolutionEnabled = v; })

        // 主题
        SectionHeader('🎨 主題')
        ForEach(['暗色', '亮色'], (label: string, idx: number) => {
          Row() {
            Text(label).fontSize(14).fontColor('#E5E7EB').layoutWeight(1)
            Radio({ value: `${idx}`, group: 'theme' }).checked(this.themeIndex === idx)
              .onChange((v: boolean) => { if (v) this.themeIndex = idx; })
          }
          .width('100%').padding({ left: 20, right: 16, top: 10, bottom: 10 })
          .border({ width: { bottom: 0.5 }, color: '#1E293B', style: BorderStyle.Solid })
        })

        // 数据管理
        SectionHeader('💾 數據管理')
        ActionRow('導出全部記憶', () => { promptAction.showToast({ message: '記憶導出中...' }); })
        ActionRow('清除臨時記憶', () => { promptAction.showToast({ message: 'P3記憶已清除' }); })

        // 关于
        SectionHeader('ℹ️ 關於')
        ActionRow('關於龍魂', () => { router.pushUrl({ url: 'pages/About' }); })
        ActionRow('許可協議', () => { router.pushUrl({ url: 'pages/License' }); })

        Text('v1.0.0-harmonyos').fontSize(10).fontColor('#4B5563')
          .width('100%').textAlign(TextAlign.Center).margin({ top: 16, bottom: 24 })
      }.width('100%')
    }
    .width('100%').height('100%').backgroundColor('#0F172A')
  }
}

@Component
struct SectionHeader {
  @Prop label: string = '';
  build() {
    Text(this.label).fontSize(13).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
      .width('100%').padding({ left: 16, top: 16, bottom: 6 }).backgroundColor('#162032')
  }
}

@Component
struct ToggleRow {
  @Prop label: string = '';
  @Link isOn: boolean;
  onChange?: (v: boolean) => void;

  build() {
    Row() {
      Text(this.label).fontSize(14).fontColor('#E5E7EB').layoutWeight(1)
      Toggle({ type: ToggleType.Switch, isOn: this.isOn })
        .onChange((v: boolean) => { this.isOn = v; this.onChange?.(v); })
    }
    .width('100%').padding({ left: 20, right: 16, top: 12, bottom: 12 })
    .border({ width: { bottom: 0.5 }, color: '#1E293B', style: BorderStyle.Solid })
  }
}

@Component
struct ActionRow {
  @Prop label: string = '';
  action?: () => void;

  build() {
    Row() {
      Text(this.label).fontSize(14).fontColor('#E5E7EB').layoutWeight(1)
      Text('→').fontSize(14).fontColor('#6B7280')
    }
    .width('100%').padding({ left: 20, right: 16, top: 12, bottom: 12 })
    .border({ width: { bottom: 0.5 }, color: '#1E293B', style: BorderStyle.Solid })
    .onClick(() => { this.action?.(); })
  }
}

// ─── 关于页 ───
@Entry
@Component
struct About {
  build() {
    Column() {
      Row() {
        Text('←').fontSize(16).fontColor('#C9A84C').onClick(() => { router.back(); })
        Blank()
        Text('關於龍魂').fontSize(18).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
      }.width('100%').padding(16)

      Scroll() {
        Column({ space: 16 }) {
          Text('🐉').fontSize(64)
          Text('龍魂系統').fontSize(24).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
          Text('HarmonyOS 插件生態 v1.0').fontSize(13).fontColor('#9CA3AF')

          Column({ space: 6 }) {
            InfoRow('DNA', '#龍芯⚡️丙午·癸未·乙酉·坤卦-PLUGIN-SETTINGS-UID9622')
            InfoRow('確認碼', '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z')
            InfoRow('GPG', 'A2D0092CEE2E5BA87035600924C3704A8CC26D5F')
            InfoRow('ORCID', '0009-0008-4596-2007')
            InfoRow('作者', '龍芯北辰 UID9622·諸葛鑫')
            InfoRow('許可', '思想層 CC BY-NC-SA 4.0 · 工程層 MulanPSL v2')
            InfoRow('構建', '2026-08-06 · 鴻蒙NEXT')
          }
          .width('100%').padding(14).backgroundColor('#1E293B').borderRadius(10).margin({ left: 16, right: 16 })
        }.width('100%').padding({ bottom: 24 })
      }.layoutWeight(1)
    }
    .width('100%').height('100%').backgroundColor('#0F172A')
  }
}

@Component
struct InfoRow {
  @Prop label: string = '';
  @Prop value: string = '';

  build() {
    Row() {
      Text(this.label).fontSize(11).fontColor('#6B7280').width(60)
      Text(this.value).fontSize(11).fontColor('#E5E7EB').fontFamily('monospace').layoutWeight(1).maxLines(2)
    }
    .width('100%').padding({ top: 4, bottom: 4 })
    .border({ width: { bottom: 0.5 }, color: '#1E293B', style: BorderStyle.Solid })
  }
}

// ─── 许可协议页 ───
@Entry
@Component
struct License {
  build() {
    Column() {
      Row() {
        Text('←').fontSize(16).fontColor('#C9A84C').onClick(() => { router.back(); })
        Blank()
        Text('許可協議').fontSize(18).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
      }.width('100%').padding(16)

      Scroll() {
        Column({ space: 16 }) {
          Column({ space: 8 }) {
            Text('📜 分層許可聲明').fontSize(18).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
            Text('龍魂系統採用分層雙許可證模型').fontSize(13).fontColor('#9CA3AF')
          }

          LicenseSection('🏛️ 核心思想層', ['CC BY-NC-SA 4.0', '非商業·署名·相同方式共享', '適用: .md協議/哲學/白皮書'])
          LicenseSection('🔧 工程實現層', ['MulanPSL v2', '允許商業使用·署名·專利授權', '適用: .py/.js/.ets/.sh/Dockerfile'])
          LicenseSection('⚠️ 限制', ['禁止刪除DNA追溯碼', '禁止以"龍魂官方"名義收費', '禁止移除主權錨定'])
          LicenseSection('✅ 允許', ['集成到商業項目', '基於SDK開發付費SaaS', '用於AI模型訓練'])

          Text('完整協議: https://uid9622.cn/license').fontSize(11).fontColor('#6B7280')
            .width('100%').textAlign(TextAlign.Center).margin({ top: 8, bottom: 24 })
        }.width('100%').padding(16)
      }.layoutWeight(1)
    }
    .width('100%').height('100%').backgroundColor('#0F172A')
  }
}

@Component
struct LicenseSection {
  @Prop title: string = '';
  @Prop items: string[] = [];

  build() {
    Column({ space: 4 }) {
      Text(this.title).fontSize(14).fontColor('#C9A84C').fontWeight(FontWeight.Bold).width('100%')
      ForEach(this.items, (item: string) => {
        Text('• ' + item).fontSize(12).fontColor('#E5E7EB').width('100%')
      })
    }
    .width('100%').padding(12).backgroundColor('#1E293B').borderRadius(10)
  }
}

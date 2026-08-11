/**
 * 🐉 龍魂 · 主导航页面
 * 鸿蒙 ArkUI · 车载控制中心
 * License: MulanPSL v2
 * DNA: #龍芯⚡️2026-08-11-CAR-MAIN-NAV-v2.0-UID9622
 */
import { SancaiEngine } from '../core/SancaiEngine';
import { DigitalRootEngine } from '../core/DigitalRootEngine';
import { HexagramNav } from '../features/HexagramNav';
import { WallOfShame } from '../core/WallOfShame';
import { DNAEngine } from '../core/DNAEngine';
import { Config } from '../common/constants/Config';

@Entry
@Component
struct MainNav {
  @State vehicleId: string = 'LONGHUN-CAR-001';
  @State vehicleModel: string = '问界M9';
  @State lat: number = 39.9042;
  @State lng: number = 116.4074;
  @State speed: number = 60;
  @State heading: number = 45;
  @State sancaiResult: string = '未评估';
  @State sancaiHexagram: string = '乾卦';
  @State sancaiColor: string = '#4ad94a';
  @State auditResult: string = '待审计';
  @State digitalRoot: number = 0;
  @State fuseLevel: string = 'normal';

  build() {
    Column() {
      // 顶部状态栏
      this.buildStatusBar();

      // 三才决策面板
      this.buildSancaiPanel();

      // 卦象导航
      this.buildHexagramNav();

      // 耻辱墙
      this.buildShameWall();

      // 底部操作栏
      this.buildBottomBar();
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  @Builder buildStatusBar() {
    Row() {
      Text(`🐉 ${Config.APP_NAME} v${Config.APP_VERSION}`)
        .fontSize(16).fontColor('#d4b84a')
      Text(`${this.vehicleModel} | ${this.speed}km/h | ${this.heading}°`)
        .fontSize(14).fontColor('#888')
    }
    .width('100%').padding(12)
    .backgroundColor('#111')
  }

  @Builder buildSancaiPanel() {
    Column() {
      Text('⚖️ 三才决策')
        .fontSize(18).fontColor('#d4b84a')
      Row() {
        Text(this.sancaiResult).fontSize(24).fontColor(this.sancaiColor)
        Text(this.sancaiHexagram).fontSize(20).fontColor('#fff')
      }
      Button('执行决策')
        .onClick(() => this.doDecision())
    }
    .width('100%').padding(16).margin(8)
    .backgroundColor('#1a1a1a').borderRadius(8)
  }

  @Builder buildHexagramNav() {
    Column() {
      Text('🗺️ 卦象导航')
        .fontSize(18).fontColor('#d4b84a')
      Text(HexagramNav.evaluate({
        trafficLevel: 1, hasAccident: false,
        hasConstruction: false, weather: 'sunny', isNight: false
      }).hexagram).fontSize(16)
    }
    .width('100%').padding(16).margin(8)
    .backgroundColor('#1a1a1a').borderRadius(8)
  }

  @Builder buildShameWall() {
    Column() {
      Text('📋 耻辱墙')
        .fontSize(18).fontColor('#d4b84a')
      Text(`${WallOfShame.getShameWall().length} 条记录`)
        .fontSize(14).fontColor('#666')
    }
    .width('100%').padding(16).margin(8)
    .backgroundColor('#1a1a1a').borderRadius(8)
  }

  @Builder buildBottomBar() {
    Row() {
      Button('三才决策').onClick(() => this.doDecision())
      Button('三色审计').onClick(() => this.doAudit())
      Button('史官日志').onClick(() => this.showHistory())
    }
    .width('100%').padding(12)
    .backgroundColor('#111')
  }

  doDecision() {
    const result = SancaiEngine.evaluate({
      weather: 'sunny', temperature: 25, timeOfDay: 'morning',
      trafficLevel: 1, roadCondition: 'good', terrain: 'urban',
      driverFatigue: 0, passengerComfort: 5, urgencyLevel: 0
    });
    this.sancaiResult = result.description;
    this.sancaiHexagram = result.hexagram;
    this.sancaiColor = HexagramNav.getColorStyle(result.hexagram);
    this.digitalRoot = result.score;
    this.fuseLevel = DigitalRootEngine.getFuseLevel(Math.round(result.score * 100));
  }

  doAudit() {
    this.auditResult = '🟢 通过';
  }

  showHistory() {
    console.info('史官日志');
  }
}

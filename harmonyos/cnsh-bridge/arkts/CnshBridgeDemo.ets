// DNA: #龍芯⚡️2026-09-05-CNSH-BRIDGE-ARKTS-v0.1-UID9622
// 创建者: 诸葛鑫（UID9622）
// 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 用途: ArkTS 调用 CNSH 鸿蒙原生桥（演示页面，并入 entry/src/main/ets/pages/）

import cnshBridge from 'libcnsh_bridge.so';

interface CnshSelfCheck {
  dna: string;
  gpg: string;
  cgen: string;
}

@Entry
@Component
struct CnshBridgeDemo {
  @State greet: string = '';
  @State auditPass: string = '';
  @State auditReject: string = '';
  @State selfCheck: CnshSelfCheck = { dna: '', gpg: '', cgen: '' };

  aboutToAppear(): void {
    // CNSH → C（cnsh_cgen.py）→ N-API 桥 → ArkTS 原生调用
    this.greet = cnshBridge.问候('鸿蒙开发者');
    this.auditPass = cnshBridge.三色审计('你好');
    this.auditReject = cnshBridge.三色审计('');
    this.selfCheck = cnshBridge.自检() as CnshSelfCheck;
  }

  build() {
    Column({ space: 14 }) {
      Text('🐉 龍魂·鸿蒙 CNSH 原生桥')
        .fontSize(22)
        .fontColor('#00d4ff')
        .fontWeight(FontWeight.Bold)
        .letterSpacing(2)

      Text(this.greet)
        .fontSize(18)
        .fontColor('#7ee787')

      Text(this.auditPass)
        .fontSize(16)
        .fontColor('#7ee787')
        .backgroundColor('#0d1a12')
        .borderRadius(8)
        .padding(10)
        .width('92%')

      Text(this.auditReject)
        .fontSize(16)
        .fontColor('#ff7b72')
        .backgroundColor('#1a0d0d')
        .borderRadius(8)
        .padding(10)
        .width('92%')

      Divider().color('#1a1a2e')

      Text('DNA 追溯（编译期常量·自检读取）')
        .fontSize(14)
        .fontColor('#ffab00')
      Text(this.selfCheck.dna)
        .fontSize(11)
        .fontColor('#888')
        .textAlign(TextAlign.Center)
      Text(`GPG: ${this.selfCheck.gpg} · ${this.selfCheck.cgen}`)
        .fontSize(11)
        .fontColor('#888')
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .backgroundColor('#0a0e17')
  }
}

import { AbilityConstant, UIAbility, Want } from '@kit.AbilityKit';
import { window } from '@kit.ArkUI';
import { hilog } from '@kit.PerformanceAnalysisKit';

// 龍魂体系主入口Ability
// DNA: #龍芯⚡️2026-06-18-LONGHUN-HARMONYOS-v1.0
// 创始人: UID9622 · 龍芯北辰 · 诸葛鑫

const TAG = 'EntryAbility';

export default class EntryAbility extends UIAbility {
  // 窗口创建时调用 - 龍魂体系初始化入口
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    hilog.info(0x0000, TAG, '%{public}s', '龍魂AI元服务启动 - onCreate');
    hilog.info(0x0000, TAG, 'DNA: #龍芯⚡️2026-06-18-LONGHUN-HARMONYOS-v1.0');
    hilog.info(0x0000, TAG, '创始人: UID9622 · 龍芯北辰 · 诸葛鑫');

    // 初始化龍魂全局状态
    AppStorage.setOrCreate('longhun_dna', '#龍芯⚡️2026-06-18-LONGHUN-HARMONYOS-v1.0');
    AppStorage.setOrCreate('longhun_version', '5.0.0');
    AppStorage.setOrCreate('longhun_founder', 'UID9622 · 龍芯北辰 · 诸葛鑫');
    AppStorage.setOrCreate('gentleman_signed', false);
  }

  // 窗口销毁时调用
  onDestroy(): void {
    hilog.info(0x0000, TAG, '%{public}s', '龍魂AI元服务关闭 - onDestroy');
  }

  // 窗口Stage创建后调用 - 加载UI
  onWindowStageCreate(windowStage: window.WindowStage): void {
    hilog.info(0x0000, TAG, '%{public}s', '龍魂窗口创建 - onWindowStageCreate');

    // 加载主页面
    windowStage.loadContent('pages/Index', (err) => {
      if (err.code) {
        hilog.error(0x0000, TAG, '加载主页面失败: %{public}s', JSON.stringify(err) ?? '');
        return;
      }
      hilog.info(0x0000, TAG, '%{public}s', '龍魂主页面加载成功');
    });
  }

  // 窗口Stage销毁时调用
  onWindowStageDestroy(): void {
    hilog.info(0x0000, TAG, '%{public}s', '龍魂窗口销毁 - onWindowStageDestroy');
  }

  // 从前台切换到后台时调用
  onBackground(): void {
    hilog.info(0x0000, TAG, '%{public}s', '龍魂进入后台 - onBackground');
  }

  // 从后台切换到前台时调用
  onForeground(): void {
    hilog.info(0x0000, TAG, '%{public}s', '龍魂回到前台 - onForeground');
  }
}
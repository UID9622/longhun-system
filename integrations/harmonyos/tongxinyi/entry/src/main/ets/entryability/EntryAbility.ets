# DNA: #龍芯⚡️丙午·丙申·甲戌·卯时·䷐随-QUAD-SYNC-v1.0-ATTRIBUTION-8c26d5f
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// entry/src/main/ets/entryability/EntryAbility.ets
// 龍魂 · EntryAbility生命周期 · ArkTS

import { AbilityConstant, UIAbility, Want, window } from '@kit.AbilityKit';
import { hilog } from '@kit.PerformanceAnalysisKit';
import { appState } from '../models/AppState';

const TAG = 'LonghunEntryAbility';

export default class EntryAbility extends UIAbility {
  // === 创建时 ===
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    hilog.info(0x0000, TAG, '[龍魂] Ability onCreate');

    // 初始化全局状态
    appState.init();

    // 记录启动参数
    const paramsStr = JSON.stringify(want.parameters || {});
    hilog.info(0x0000, TAG, `[龍魂] 启动参数: ${paramsStr}`);

    // 处理深度链接
    if (want.uri) {
      this.handleDeepLink(want.uri);
    }
  }

  // === 销毁时 ===
  onDestroy(): void {
    hilog.info(0x0000, TAG, '[龍魂] Ability onDestroy');

    // 持久化状态
    appState.persist();
  }

  // === 窗口创建时 ===
  onWindowStageCreate(windowStage: window.WindowStage): void {
    hilog.info(0x0000, TAG, '[龍魂] Ability onWindowStageCreate');

    // 加载主页面
    windowStage.loadContent('pages/Index', (err, data) => {
      if (err.code) {
        hilog.error(0x0000, TAG, `[龍魂] 加载页面失败: ${JSON.stringify(err)}`);
        return;
      }
      hilog.info(0x0000, TAG, '[龍魂] 页面加载成功');

      // 获取窗口实例
      const win = windowStage.getMainWindowSync();

      // 监听窗口大小变化（响应式适配）
      win.on('windowSizeChange', (size: window.Size) => {
        hilog.info(0x0000, TAG, `[龍魂] 窗口变化: ${size.width}x${size.height}`);
        AppStorage.setOrCreate('window_width', size.width);
        AppStorage.setOrCreate('window_height', size.height);
      });

      // 监听窗口失焦/获焦
      win.on('windowFocusChange', (isFocus: boolean) => {
        hilog.info(0x0000, TAG, `[龍魂] 窗口焦点: ${isFocus}`);
        AppStorage.setOrCreate('window_focused', isFocus);
      });
    });
  }

  // === 窗口销毁时 ===
  onWindowStageDestroy(): void {
    hilog.info(0x0000, TAG, '[龍魂] Ability onWindowStageDestroy');
  }

  // === 前台时 ===
  onForeground(): void {
    hilog.info(0x0000, TAG, '[龍魂] Ability onForeground');

    // 恢复状态
    appState.loadNavHistory();
  }

  // === 后台时 ===
  onBackground(): void {
    hilog.info(0x0000, TAG, '[龍魂] Ability onBackground');

    // 保存状态
    appState.persist();
  }

  // === 新Want ===
  onNewWant(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    hilog.info(0x0000, TAG, '[龍魂] Ability onNewWant');

    // 处理新的启动参数（如通知点击）
    if (want.uri) {
      this.handleDeepLink(want.uri);
    }

    if (want.parameters) {
      AppStorage.setOrCreate('launch_params', want.parameters);
    }
  }

  // === 处理深度链接 ===
  private handleDeepLink(uri: string): void {
    hilog.info(0x0000, TAG, `[龍魂] 深度链接: ${uri}`);

    // 解析URI: longhun://page/project?id=123
    const questionIdx = uri.indexOf('?');
    const path = questionIdx >= 0 ? uri.substring(0, questionIdx) : uri;
    const params: Record<string, string> = {};

    if (questionIdx >= 0) {
      const query = uri.substring(questionIdx + 1);
      query.split('&').forEach(pair => {
        const eqIdx = pair.indexOf('=');
        if (eqIdx >= 0) {
          const k = decodeURIComponent(pair.substring(0, eqIdx));
          const v = decodeURIComponent(pair.substring(eqIdx + 1));
          params[k] = v;
        }
      });
    }

    // 存储深度链接信息
    AppStorage.setOrCreate('deep_link_path', path);
    AppStorage.setOrCreate('deep_link_params', JSON.stringify(params));

    hilog.info(0x0000, TAG, `[龍魂] 深度链接解析: path=${path}, params=${JSON.stringify(params)}`);
  }

  // === 内存不足 ===
  onMemoryLevel(level: AbilityConstant.MemoryLevel): void {
    hilog.warn(0x0000, TAG, `[龍魂] 内存警告: ${level}`);

    if (level === AbilityConstant.MemoryLevel.MEMORY_LEVEL_MODERATE ||
        level === AbilityConstant.MemoryLevel.MEMORY_LEVEL_LOW) {
      // 清理非必要缓存
      appState.persist();
    }
  }
}

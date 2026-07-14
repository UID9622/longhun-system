// entry/src/main/ets/utils/OverlayUtils.ets
// 龍魂 · 遮罩工具类

import { overlayState, DialogConfig, ToastConfig, LoadingConfig, DialogButton, AnimationType } from '../models/StackModel';

export class OverlayUtils {
  // === 显示确认弹窗 ===
  static confirm(title: string, message: string, onConfirm: () => void, onCancel?: () => void): void {
    overlayState.showDialog(new DialogConfig({
      title,
      message,
      icon: '❓',
      primaryButton: { label: '确认', type: 'primary', action: onConfirm },
      cancelButton: { label: '取消', type: 'cancel', action: onCancel || (() => {}) },
      enterAnimation: AnimationType.SCALE,
      dismissOnMaskTap: true
    }));
  }

  // === 显示警告弹窗 ===
  static alert(title: string, message: string, onConfirm?: () => void): void {
    overlayState.showDialog(new DialogConfig({
      title,
      message,
      icon: '⚠️',
      primaryButton: { label: '确定', type: 'primary', action: onConfirm || (() => {}) },
      enterAnimation: AnimationType.FADE
    }));
  }

  // === 显示错误弹窗 ===
  static error(title: string, message: string, onConfirm?: () => void): void {
    overlayState.showDialog(new DialogConfig({
      title,
      message,
      icon: '❌',
      primaryButton: { label: '确定', type: 'danger', action: onConfirm || (() => {}) },
      enterAnimation: AnimationType.FADE
    }));
  }

  // === 显示输入弹窗 ===
  static prompt(title: string, placeholder: string, onConfirm: (value: string) => void, defaultValue?: string): void {
    overlayState.showDialog(new DialogConfig({
      title,
      message: '',
      hasInput: true,
      inputPlaceholder: placeholder,
      inputDefaultValue: defaultValue,
      primaryButton: { label: '确认', type: 'primary', action: () => { /* 获取输入值 */ } },
      cancelButton: { label: '取消', type: 'cancel' },
      enterAnimation: AnimationType.SLIDE_UP
    }));
  }

  // === 显示成功 Toast ===
  static success(message: string, duration?: number): void {
    overlayState.showToast(new ToastConfig({
      message,
      icon: '✅',
      position: 'center',
      duration: duration || 2000
    }));
  }

  // === 显示错误 Toast ===
  static errorToast(message: string, duration?: number): void {
    overlayState.showToast(new ToastConfig({
      message,
      icon: '❌',
      position: 'center',
      duration: duration || 3000
    }));
  }

  // === 显示加载 ===
  static showLoading(message?: string, cancelable?: boolean): void {
    overlayState.showLoading(new LoadingConfig({
      message: message || '加载中...',
      cancelable: cancelable || false
    }));
  }

  // === 显示进度加载 ===
  static showProgressLoading(message: string, progress: number): void {
    overlayState.showLoading(new LoadingConfig({
      message,
      progress,
      cancelable: true
    }));
  }

  // === 关闭加载 ===
  static hideLoading(): void {
    overlayState.dismissLoading();
  }

  // === 更新进度 ===
  static updateProgress(progress: number): void {
    if (overlayState.currentLoading) {
      overlayState.currentLoading.progress = progress;
    }
  }

  // === 显示底部弹窗 ===
  static showBottomSheet(title: string, items: { label: string; action: () => void }[]): void {
    // 构建底部弹窗
    console.info(`[龍魂] 显示底部弹窗: ${title}`);
  }

  // === 显示侧边栏 ===
  static showSidebar(width: number, content: () => void): void {
    // 构建侧边栏
    console.info(`[龍魂] 显示侧边栏: ${width}px`);
  }

  // === 清空所有遮罩 ===
  static clearAll(): void {
    overlayState.clearAll();
  }
}

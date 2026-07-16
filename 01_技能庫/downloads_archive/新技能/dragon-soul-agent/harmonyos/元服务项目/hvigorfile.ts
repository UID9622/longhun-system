import { appTasks } from '@ohos/hvigor-ohos-plugin';

// 龍魂体系元服务构建入口
// DNA: #龍芯⚡️2026-06-18-LONGHUN-HARMONYOS-v1.0

export default {
    system: appTasks,
    plugins: [],
    // 龍魂自定义构建钩子
    hooks: {
        preBuild: () => {
            console.log('[龍魂] 开始构建... DNA: #龍芯⚡️2026-06-18-HARMONYOS-v1.0');
        },
        postBuild: () => {
            console.log('[龍魂] 构建完成，君子协议已校验');
        }
    }
}
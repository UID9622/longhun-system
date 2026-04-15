<template>
    <div class="disk-io-tooltip">
        <div v-for="value in item" class="disk-item">
            <div class="title">
                <img width="14" height="14" :src="folderIconUrl" alt="">
                <div class="disk-io-tooltip__label">{{ title }}</div>
            </div>
            <div class="item">
                {{ dic }}：{{ value.fsPath[0] }}
            </div>
            <div class="item">
                {{ read }}：{{ value.readSpeedMbps }}
            </div>
            <div class="item">
                {{ write }}：{{ value.writeSpeedMbps }}
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ITestResult } from '../App.vue';

const props = defineProps<{ item?: ITestResult[], title: string, dic: string, read: string, write: string }>();
const folderIconUrl = new URL('../resources/folder.png', import.meta.url).href;
</script>

<style scoped>
body.vscode-light {
    .disk-io-tooltip {
        width: 284px;
        min-height: 112px;
        overflow-y: auto;
        scrollbar-width: none;
        font-size: 12px;
        box-sizing: border-box;
        padding: 12px 12px 0 12px;

        .disk-item {
            .title {
                display: flex;
                align-items: center;
                color: rgba(25, 25, 25, 1);
                margin-bottom: 11px;

                img {
                    margin-right: 5px;
                }
            }

            .item {
                color: rgba(89, 89, 89, 1);
                word-break: break-all;
            }
        }
    }
}

body.vscode-dark {
    .disk-io-tooltip {
        width: 284px;
        min-height: 112px;
        overflow-y: auto;
        scrollbar-width: none;
        font-size: 12px;
        box-sizing: border-box;
        padding: 12px 12px 0 12px;

        .disk-item {
            .title {
                display: flex;
                align-items: center;
                color: rgba(230, 230, 230, 1);
                margin-bottom: 11px;

                img {
                    margin-right: 5px;
                }
            }

            .item {
                color: rgba(179, 179, 179, 1);
                word-break: break-all;
            }
        }
    }
}

.disk-io-tooltip::-webkit-scrollbar {
    width: 0;
    height: 0;
}
</style>

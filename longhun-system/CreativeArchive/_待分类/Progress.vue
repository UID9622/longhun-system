<template>
    <div v-if="type === 'circular'" class="semi-circle-progress"
        :style="{ width: `${size}px`, height: `${size / 2}px` }">
        <svg :width="size" :height="size / 2" viewBox="0 0 200 100" style="overflow: visible;">
            <!-- 定义渐变色 -->
            <defs>
                <linearGradient :id="`gradient-${uid}`" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop v-for="(color, index) in colors" :key="index" :offset="getOffset(index, colors.length)"
                        :stop-color="color" />
                </linearGradient>
            </defs>

            <!-- 外侧背景半圆 -->
            <path :d="outerRingPath" fill="none" :stroke="outerBackgroundColor" :stroke-width="OUTER_RING_WIDTH"
                stroke-linecap="round" stroke-linejoin="round" />

            <!-- 背景半圆 -->
            <path :d="backgroundPath" fill="none" :stroke="backgroundColor" :stroke-width="strokeWidth"
                stroke-linecap="round" stroke-linejoin="round" />

            <!-- 进度半圆 -->
            <path :d="backgroundPath" fill="none" :stroke="`url(#gradient-${uid})`" :stroke-width="strokeWidth"
                stroke-linecap="round" stroke-linejoin="round" pathLength="100"
                :stroke-dasharray="SEMI_CIRCLE_PATH_LENGTH" :stroke-dashoffset="progressDashoffset"
                class="progress-path" />

            <!-- 刻度 -->
            <line v-for="(tick, index) in tickSegments" :key="index" :x1="tick.x1" :y1="tick.y1" :x2="tick.x2"
                :y2="tick.y2" :stroke-width="TICK_STROKE_WIDTH" stroke-linecap="round" class="tick-line" />

            <!-- 百分比文字 -->
            <text x="100" y="57" text-anchor="middle" class="label-text-up">
                {{ label }}
            </text>

            <text x="100" y="82" text-anchor="middle" class="label-text-down">
                {{ resourceUsage }}
            </text>
        </svg>
    </div>

    <div v-else class="linear-progress-container" :style="{ width: `${size}px` }">
        <svg :width="size" :height="strokeWidth + textHeight" style="overflow: visible;">
            <defs>
                <linearGradient :id="`gradient-linear-${uid}`" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop v-for="(color, index) in colors" :key="index" :offset="getOffset(index, colors.length)"
                        :stop-color="color" />
                </linearGradient>
            </defs>

            <!-- 顶部标签和进度文本 -->
            <text x="0" y="14" class="linear-label-text">
                {{ label }}
            </text>
            <text :x="size" y="14" text-anchor="end" class="linear-percentage-text">
                {{ percentage }}%
            </text>

            <!-- Background -->
            <rect x="0" :y="textHeight" :width="size" :height="strokeWidth" :rx="strokeWidth / 2" :ry="strokeWidth / 2"
                :fill="backgroundColor" />

            <!-- Progress -->
            <rect x="0" :y="textHeight" :width="Math.max(0, (size * percentage) / 100)" :height="strokeWidth"
                :rx="strokeWidth / 2" :ry="strokeWidth / 2" :fill="`url(#gradient-linear-${uid})`"
                style="transition: width 0.3s ease" />
        </svg>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
    type?: 'circular' | 'normal';
    percentage?: number;
    size?: number;
    colors?: string[];
    backgroundColor?: string;
    outerBackgroundColor?: string;
    strokeWidth?: number;
    label: string;
    resourceUsage: string;
}

const props = withDefaults(defineProps<Props>(), {
    type: 'circular',
    percentage: 0,
    size: 144,
    colors: () => [],
    backgroundColor: '',
    outerBackgroundColor: '',
    strokeWidth: 8,
    label: '',
    resourceUsage: ''
});


// 生成唯一 ID，避免多个组件渐变色冲突
const uid = Math.random().toString(36).substr(2, 9);

// 线性进度条文本区域高度
const textHeight = 24;

// 定义几何常量
const RADIUS = 90;
const CENTER_X = 100;
const CENTER_Y = 90; //稍微下移，留出上方stroke的空间
const START_X = CENTER_X - RADIUS; // 20
const END_X = CENTER_X + RADIUS; // 180

// 背景路径（固定满半圆）
const backgroundPath = `M ${START_X} ${CENTER_Y} A ${RADIUS} ${RADIUS} 0 0 1 ${END_X} ${CENTER_Y}`;

const SEMI_CIRCLE_PATH_LENGTH = 100;
const TICK_COUNT = 25;
const TICK_OFFSET = 3;
const TICK_LENGTH = 7;
const TICK_STROKE_WIDTH = 1;
const OUTER_RING_OFFSET = 3;
const OUTER_RING_WIDTH = 1;

interface TickSegment {
    x1: number;
    y1: number;
    x2: number;
    y2: number;
}

const normalizedPercentage = computed(() => Math.min(Math.max(props.percentage, 0), 100));
const progressDashoffset = computed(() => SEMI_CIRCLE_PATH_LENGTH - normalizedPercentage.value);
const outerRingPath = computed(() => {
    const halfStroke = props.strokeWidth / 2;
    const radius = RADIUS + halfStroke + OUTER_RING_OFFSET;
    const startX = CENTER_X - radius;
    const endX = CENTER_X + radius;
    return `M ${startX} ${CENTER_Y} A ${radius} ${radius} 0 0 1 ${endX} ${CENTER_Y}`;
});
const tickSegments = computed<TickSegment[]>(() => {
    if (TICK_COUNT <= 0) {
        return [];
    }
    const halfStroke = props.strokeWidth / 2;
    const startRadius = Math.max(RADIUS - halfStroke - TICK_OFFSET, 0);
    const endRadius = Math.max(startRadius - TICK_LENGTH, 0);
    return Array.from({ length: TICK_COUNT }, (_, index) => {
        const denominator = Math.max(TICK_COUNT - 1, 1);
        const ratio = index / denominator;
        const angle = Math.PI - ratio * Math.PI;
        const x1 = CENTER_X + startRadius * Math.cos(angle);
        const y1 = CENTER_Y - startRadius * Math.sin(angle);
        const x2 = CENTER_X + endRadius * Math.cos(angle);
        const y2 = CENTER_Y - endRadius * Math.sin(angle);
        return { x1, y1, x2, y2 };
    });
});

const getOffset = (index: number, total: number) => {
    // 4色规则: 0%, 34%, 67%, 100%
    if (total === 4) {
        const offsets = [0, 34, 67, 100];
        return `${offsets[index]}%`;
    }

    // 3色规则: 0%, 50%, 100%
    if (total === 3) {
        const offsets = [0, 50, 100];
        return `${offsets[index]}%`;
    }

    // 2色规则: 0%, 100%
    if (total === 2) {
        const offsets = [0, 100];
        return `${offsets[index]}%`;
    }

    // 其他情况默认均匀分布
    return `${(index / (total > 1 ? total - 1 : 1)) * 100}%`;
};
</script>

<style scoped>
body.vscode-dark {
    .semi-circle-progress {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    svg {
        max-width: 100%;
        height: auto;
    }

    .progress-path {
        transition: stroke-dashoffset 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .tick-line {
        stroke: #252525;
    }


    .label-text-up {
        font-size: 14px;
        font-weight: normal;
        fill: rgba(128, 128, 128, 1);
    }

    .label-text-down {
        font-size: 14px;
        font-weight: bold;
        fill: #e5e5e5;
    }

    .percentage-text {
        font-size: 12px;
        font-weight: bold;
        fill: #333;
    }

    .linear-progress-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .linear-label-text {
        font-size: 12px;
        fill: rgba(128, 128, 128, 1);
    }

    .linear-percentage-text {
        font-size: 12px;
        fill: rgba(128, 128, 128, 1);
    }
}

body.vscode-light {

    .semi-circle-progress {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    svg {
        max-width: 100%;
        height: auto;
    }

    .progress-path {
        transition: stroke-dashoffset 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .tick-line {
        stroke: #f5f5f5;
    }


    .label-text-up {
        font-size: 14px;
        font-weight: normal;
        fill: #808080;
    }

    .label-text-down {
        font-size: 14px;
        font-weight: bold;
        fill: #1b1b1b;
    }

    .percentage-text {
        font-size: 12px;
        font-weight: bold;
        fill: #333;
    }

    .linear-progress-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .linear-label-text {
        font-size: 12px;
        fill: rgba(128, 128, 128, 1);
    }

    .linear-percentage-text {
        font-size: 12px;
        fill: rgba(128, 128, 128, 1);
    }
}
</style>

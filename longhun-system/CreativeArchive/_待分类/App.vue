<template>
	<div class="app-container">
		<div class="cpu-memory-section">
			<div class="item">
				<div class="icon-label">
					<img width="14" height="14" :src="cpuIconUrl" alt="">
					<span>CPU</span>
				</div>
				<div class="progress-container">
					<Progress :percentage="cpuData.resourceUsage" :size="144"
						:colors="getColorArray(cpuData.resourceUsage, true)" :strokeWidth="8"
						:label="t('Usage Percentage')" :resourceUsage="cpuData.desc!" :backgroundColor="backgroundColor"
						:outerBackgroundColor="outerBackgroundColor" />
				</div>
			</div>

			<div class="item">
				<div class="icon-label">
					<img width="16" height="16" :src="memoryIconUrl" alt="">
					<span>{{ t('Memory') }}</span>
				</div>
				<div class="progress-container">
					<Progress :percentage="memData.resourceUsage" :size="144"
						:colors="getColorArray(memData.resourceUsage, true)" :strokeWidth="8" :label="t('GB')"
						:resourceUsage="memData.desc!" :backgroundColor="backgroundColor"
						:outerBackgroundColor="outerBackgroundColor" />
				</div>
			</div>
		</div>

		<div class="disk-section">
			<div class="disk-title">
				<img width="12.6" height="12.6" :src="diskIconUrl" alt="">
				<span>{{ t('Disk') }}</span>
				<el-tooltip class="box-item" effect="dark" placement="bottom-end">
					<template #content>
						<DiskIoTooltip :item="ioData" :title="t('DISK I/O') + '：'" :dic="t('Directory')"
							:read="t('Read')" :write="t('Write')" />
					</template>
					<img v-if="ioData.length" width="12" height="12" :src="tipIconUrl" alt="">
				</el-tooltip>
			</div>

			<div class="disk-item" v-for="value in diskData" :key="value.label">
				<Progress :type="'normal'" :percentage="value.resourceUsage" :size="360"
					:colors="getColorArray(value.resourceUsage, false)" :strokeWidth="6" :label="value.label"
					:resourceUsage="value.desc!" :backgroundColor="backgroundColor" />
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { onBeforeMount, onBeforeUnmount, onMounted, ref } from 'vue';
import DiskIoTooltip from './components/DiskIoTooltip.vue';
import Progress from './components/Progress.vue';

enum SignalType {
	CPU = 'cpu',
	MEMORY = 'memory',
	DISK = 'disk',
	DISKIO = 'diskIO',
}

interface FsSizeData {
	fs: string;
	type: string;
	size: number;
	used: number;
	available: number;
	use: number | null;
	mount: string;
	rw: boolean | null;
}

interface ParsedFsSizeData {
	resourceUsage: number,
	label: string,
	desc: string,
}

export interface ITestResult {
	id: number;
	name: [string];
	fsPath: [string];
	readSpeedMbps?: number;
	writeSpeedMbps?: number;
	permissionDenied?: boolean;
}

interface ResourceUsage {
	desc?: string;
	resourceUsage: any;
}

interface CachePayload {
	[key: string]: ResourceUsage;
}

declare function acquireVsCodeApi(): any;
const vscode = acquireVsCodeApi();

const translations = ref<Record<string, string>>({});

const t = (key: string): string => {
	return translations.value[key] || key;
};

const applyCachePayload = (data?: CachePayload) => {
	if (!data) {
		return;
	}
	if (data[SignalType.CPU]) {
		cpuData.value = data[SignalType.CPU];
	}
	if (data[SignalType.MEMORY]) {
		memData.value = data[SignalType.MEMORY];
	}
	if (data[SignalType.DISK]) {
		const diskPayload = data[SignalType.DISK];
		if (Array.isArray(diskPayload?.resourceUsage)) {
			diskData.value = handleDiskData(diskPayload.resourceUsage.filter((e: FsSizeData) => e.use) as FsSizeData[]);
		}
	}
	if (data[SignalType.DISKIO]) {
		ioData.value = data[SignalType.DISKIO].resourceUsage;
	}
};

const listener = (event: MessageEvent) => {
	const command = event.data?.command as string | undefined;
	if (command) {
		switch (command) {
			case 'translations':
				translations.value = event.data.data ?? {};
				return;
			case 'cacheData':
				applyCachePayload(event.data.data as CachePayload);
				return;
			default:
				break;
		}
	}

	const type = event.data?.type;
	switch (type) {
		case SignalType.CPU:
			cpuData.value = event.data.data as ResourceUsage;
			break;
		case SignalType.MEMORY:
			memData.value = event.data.data as ResourceUsage;
			break;
		case SignalType.DISK:
			diskData.value = handleDiskData(event.data.data.resourceUsage.filter((e: FsSizeData) => e.use !== null));
			break;
		case SignalType.DISKIO:
			ioData.value = event.data.data.resourceUsage;
			break;
		default:
			break;
	}
};

const handleDiskData = (data: FsSizeData[] = []): ParsedFsSizeData[] => {
	return data.map((item) => {
		const usage = Number.parseInt(item.use!.toFixed(0));
		return {
			label: item.fs,
			desc: `${usage}%`,
			resourceUsage: usage,
		};
	});
};

onBeforeMount(() => {
	vscode.postMessage({ command: 'getTranslations' });
	vscode.postMessage({ command: 'getCacheData' });
});

onMounted(() => {
	window.addEventListener('message', listener);
	updateTheme();
	themeObserver = new MutationObserver(updateTheme);
	if (document.body) {
		themeObserver.observe(document.body, { attributes: true, attributeFilter: ['class'] });
	}
	if (document.documentElement) {
		themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
	}
	const colorSchemeMedia = window.matchMedia?.('(prefers-color-scheme: dark)');
	colorSchemeMedia?.addEventListener('change', updateTheme);
});

onBeforeUnmount(() => {
	window.removeEventListener('message', listener);
	themeObserver?.disconnect();
	themeObserver = undefined;
	const colorSchemeMedia = window.matchMedia?.('(prefers-color-scheme: dark)');
	colorSchemeMedia?.removeEventListener('change', updateTheme);
});

const cpuData = ref<ResourceUsage>({ desc: '--', resourceUsage: 0 });
const memData = ref<ResourceUsage>({ desc: '--', resourceUsage: 0 });
const diskData = ref<ParsedFsSizeData[]>([]);
const ioData = ref<ITestResult[]>([]);

const isDarkTheme = ref(false);
const backgroundColor = ref('#2d2d2d');
const outerBackgroundColor = ref('#252525');
let themeObserver: MutationObserver | undefined;

const darkCircularColorArray = ['rgba(22, 174, 184, 1)', 'rgba(115, 176, 21, 1)', 'rgba(175, 102, 20, 1)', 'rgba(170, 23, 16, 1)'];
const darkNormalColorArray = ['rgba(21, 125, 175, 1)', 'rgba(17, 63, 190, 1)', 'rgba(90, 40, 176, 1)', 'rgba(141, 24, 165, 1)'];
const lightCircularColorArray = ['rgba(100, 200, 250, 1)', 'rgba(198, 218, 70, 1)', 'rgba(255, 206, 92, 1)', 'rgba(237, 68, 138, 1)'];
const lightNormalColorArray = ['rgba(100, 200, 250, 1)', 'rgba(82, 145, 255, 1)', 'rgba(165, 110, 219, 1)', 'rgba(237, 68, 138, 1)'];

const cpuIconUrl = new URL('./resources/cpu.png', import.meta.url).href;
const memoryIconUrl = new URL('./resources/memory.png', import.meta.url).href;
const diskIconUrl = new URL('./resources/disk.png', import.meta.url).href;
const tipIconUrl = new URL('./resources/tip.png', import.meta.url).href;

const getColorArray = (percentage: number, isCircular: boolean): string[] => {
	const ratio = percentage / 100;
	const colorArray = isDarkTheme.value
		? (isCircular ? darkCircularColorArray : darkNormalColorArray)
		: (isCircular ? lightCircularColorArray : lightNormalColorArray);

	if (ratio <= 0.25) {
		return [colorArray[0]];
	} else if (ratio <= 0.5) {
		return colorArray.slice(0, 2);
	} else if (ratio <= 0.75) {
		return colorArray.slice(0, 3);
	} else {
		return colorArray.slice(0, 4);
	}
};

const updateTheme = () => {
	const bodyClassList = document.body?.classList;
	const htmlClassList = document.documentElement?.classList;
	if (bodyClassList?.contains('vscode-dark') || htmlClassList?.contains('vscode-dark')) {
		isDarkTheme.value = true;
		backgroundColor.value = '#2d2d2d';
		outerBackgroundColor.value = '#252525';
		return;
	}
	if (bodyClassList?.contains('vscode-light') || htmlClassList?.contains('vscode-light')) {
		isDarkTheme.value = false;
		backgroundColor.value = '#f5f5f5';
		outerBackgroundColor.value = '#f5f5f5';
		return;
	}
	const prefersDark = window.matchMedia?.('(prefers-color-scheme: dark)')?.matches;
	if (typeof prefersDark === 'boolean') {
		isDarkTheme.value = prefersDark;
	}
};
</script>

<style scoped>
body.vscode-dark {
	.app-container {
		padding: 20px;
		background: rgba(26, 26, 26, 1);
		font-size: 12px;
		height: 100vh;
		overflow-y: auto;
		border-top: 1px solid rgba(255, 255, 255, 0.05);

		.cpu-memory-section {
			position: sticky;
			top: 0;
			background: rgba(26, 26, 26, 1);
			z-index: 10;

			.item {
				display: inline-block;
				width: 50%;

				.icon-label {
					color: rgba(230, 230, 230, 1);
					display: flex;
					align-items: center;

					img {
						margin-right: 5px;
					}
				}

				.progress-container {
					display: flex;
					margin-top: 10px;
					box-sizing: border-box;
					padding-left: 12px;
				}

				&:nth-child(2) {
					transform: translateX(10px);
				}
			}
		}

		.disk-section {
			margin-top: 21px;

			.disk-title {
				display: flex;
				align-items: center;
				color: rgba(230, 230, 230, 1);

				span {
					margin-left: 4px;
					margin-right: 6px;
				}
			}

			.disk-item {
				margin-top: 12px;
				color: rgba(128, 128, 128, 1);
			}
		}
	}

	:global(.el-popper.is-dark) {
		border-radius: 8px;
		background: rgba(20, 20, 20, 0.95);
		box-shadow: 0 8px 20px rgba(0, 0, 0, 0.45);
		border: 1px solid rgba(53, 54, 56, 1);
	}

	:global(.el-popper.is-dark .el-popper__arrow),
	:global(.el-popper.is-dark .el-popper__arrow::before) {
		display: none;
	}

	/* VSCode webview 标准滚动条 */
	.app-container {
		scrollbar-width: thin;
		scrollbar-color: #2d2d2d rgba(26, 26, 26, 1);
	}
}

body.vscode-light {
	.app-container {
		padding: 20px;
		background: #fff;
		font-size: 12px;
		height: 100vh;
		overflow-y: auto;
		border-top: 1px solid rgba(0, 0, 0, 0.05);

		.cpu-memory-section {
			position: sticky;
			top: 0;
			background: #fff;
			z-index: 10;

			.item {
				display: inline-block;
				width: 50%;

				.icon-label {
					color: rgba(25, 25, 25, 1);
					display: flex;
					align-items: center;

					img {
						margin-right: 5px;
					}
				}

				.progress-container {
					display: flex;
					margin-top: 10px;
					box-sizing: border-box;
					padding-left: 12px;
				}

				&:nth-child(2) {
					transform: translateX(10px);
				}
			}
		}

		.disk-section {
			margin-top: 21px;

			.disk-title {
				display: flex;
				align-items: center;
				color: rgba(25, 25, 25, 1);

				span {
					margin-left: 4px;
					margin-right: 6px;
				}
			}

			.disk-item {
				margin-top: 12px;
				color: rgba(128, 128, 128, 1);
			}
		}
	}

	:global(.el-popper.el-tooltip) {
		border-radius: 8px;
		border: 1px solid rgba(0, 0, 0, 0.05);
		box-shadow: 0px 8px 24px 0px rgba(0, 0, 0, 0.2);
		background: rgba(255, 255, 255, 1);
	}

	:global(.el-popper.is-dark .el-popper__arrow),
	:global(.el-popper.is-dark .el-popper__arrow::before) {
		display: none;
	}

	/* VSCode webview 标准滚动条 */
	.app-container {
		scrollbar-width: thin;
		scrollbar-color: #2d2d2d rgba(26, 26, 26, 1);
	}
}
</style>

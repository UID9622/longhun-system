/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Huawei Technologies Co., Ltd. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

// Localization strings for the welcome setup
const WelcomeLocalizations = {
	'en': {
		welcome: {
			text: 'Welcome to',
			productName: 'CodeArts Agent',
			startButton: 'Get Started'
		},
		import: {
			title: 'Import Configuration',
			description: 'Quickly reuse previous IDE configurations, including extensions, settings, keyboard shortcuts, code snippets, etc.',
			fromVSCode: 'Import from VS Code',
			importing: 'Importing from VS Code',
			skip: 'Skip',
			back: 'Back',
			importingSettings: 'Importing settings...',
			bindingKeybindings: 'Binding keybindings...',
			syncingSnippets: 'Syncing snippets...',
			importCompleted: 'Import completed',
			installingExtension: 'Installing extension ({0}/{1})...'
		},
		login: {
			title: 'Ready to Start',
			productName: 'CodeArts Agent',
			loginButton: 'Sign In',
			skip: 'Skip',
			back: 'Back'
		}
	},
	'zh-cn': {
		welcome: {
			// allow-any-unicode-next-line
			text: '欢迎使用',
			// allow-any-unicode-next-line
			productName: 'CodeArts代码智能体',
			// allow-any-unicode-next-line
			startButton: '开始'
		},
		import: {
			// allow-any-unicode-next-line
			title: '导入配置',
			// allow-any-unicode-next-line
			description: '快速复用过往IDE配置，包括插件、设置、快捷键配置、代码片段等',
			// allow-any-unicode-next-line
			fromVSCode: '从 VS Code 导入',
			// allow-any-unicode-next-line
			importing: '正在从 VS Code 导入',
			// allow-any-unicode-next-line
			skip: '跳过',
			// allow-any-unicode-next-line
			back: '返回',
			// allow-any-unicode-next-line
			importingSettings: '正在导入设置...',
			// allow-any-unicode-next-line
			bindingKeybindings: '正在绑定快捷键...',
			// allow-any-unicode-next-line
			syncingSnippets: '正在同步代码片段...',
			// allow-any-unicode-next-line
			importCompleted: '导入完成',
			// allow-any-unicode-next-line
			installingExtension: '正在安装插件 ({0}/{1})...'
		},
		login: {
			// allow-any-unicode-next-line
			title: '准备就绪，开始体验',
			// allow-any-unicode-next-line
			productName: 'CodeArts代码智能体',
			// allow-any-unicode-next-line
			loginButton: '登录',
			// allow-any-unicode-next-line
			skip: '跳过',
			// allow-any-unicode-next-line
			back: '返回'
		}
	}
};

// Get localized string
function getLocalizedString(page, key, locale = 'en', args = []) {
	const defaultLocale = 'en';
	let message;

	if (!WelcomeLocalizations[locale] || !WelcomeLocalizations[locale][page]) {
		message = WelcomeLocalizations[defaultLocale][page]?.[key] || key;
	} else {
		message = WelcomeLocalizations[locale][page][key];
	}

	if (args && args.length > 0 && typeof message === 'string') {
		message = message.replace(/\{(\d+)\}/g, (_, index) => {
			const argIndex = parseInt(index, 10);
			return args[argIndex] !== undefined ? String(args[argIndex]) : `{${index}}`;
		});
	}

	return message;
}

// Element ID to localization key mapping for each page
const ELEMENT_KEY_MAPS = {
	welcome: {
		welcomeText: 'text',
		productName: 'productName',
		btnStartText: 'startButton'
	},
	import: {
		importTitle: 'title',
		importDescription: 'description',
		btnVsCodeText: 'fromVSCode',
		btnVsCodeLoadingText: 'importing',
		btnSkipText: 'skip',
		importBackText: 'back'
	},
	login: {
		loginTitle: 'title',
		loginProductName: 'productName',
		btnLoginText: 'loginButton',
		btnSkipText: 'skip',
		loginBackText: 'back'
	}
};

// Apply localizations to DOM elements
function applyLocalizations(pageType, locale) {
	const keyMap = ELEMENT_KEY_MAPS[pageType];

	if (!keyMap) {
		return;
	}

	// Process element ID to key mappings
	for (const [elementId, key] of Object.entries(keyMap)) {
		const element = document.getElementById(elementId);
		if (element) {
			element.textContent = getLocalizedString(pageType, key, locale);
		}
	}
}

// Get system locale (fallback to en) - internal function, not exported
function getSystemLocale() {
	// First check URL parameter, then fallback to browser language
	if (typeof window !== 'undefined') {
		const urlParams = new URLSearchParams(window.location.search);
		const urlLocale = urlParams.get('locale');
		if (urlLocale) {
			return urlLocale.toLowerCase().startsWith('zh') ? 'zh-cn' : 'en';
		}
	}
	const locale = (typeof window !== 'undefined' && window.navigator?.language) || 'en';
	return locale.toLowerCase().startsWith('zh') ? 'zh-cn' : 'en';
}

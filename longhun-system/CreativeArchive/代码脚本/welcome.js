/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Huawei Technologies Co., Ltd. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

(function () {
	'use strict';

	// DOM elements
	const btnStart = document.getElementById('btnStart');
	const windowMinimize = document.getElementById('windowMinimize');
	const windowMaxRestore = document.getElementById('windowMaxRestore');
	const windowClose = document.getElementById('windowClose');

	// Initialize
	function init() {
		setupEventListeners();
		applyLocalizations('welcome', getSystemLocale());
	}

	// Setup all event listeners
	function setupEventListeners() {
		// Start button - navigate to import page (in same window)
		btnStart?.addEventListener('click', () => {
			if (window.welcomeAPI) {
				window.welcomeAPI.navigate('import');
			}
		});

		// Window control buttons
		windowMinimize?.addEventListener('click', () => {
			if (window.welcomeAPI) {
				window.welcomeAPI.minimizeWindow();
			}
		});
		windowMaxRestore?.addEventListener('click', () => {
			if (window.welcomeAPI) {
				window.welcomeAPI.maximizeWindow();
			}
		});
		windowClose?.addEventListener('click', () => {
			if (window.welcomeAPI) {
				window.welcomeAPI.closeWindow();
			}
		});
	}

	// Start the app
	init();
})()

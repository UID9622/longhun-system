/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Huawei Technologies Co., Ltd. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

(function () {
	'use strict';

	// DOM elements
	const btnLoginBack = document.getElementById('btnLoginBack');
	const btnLogin = document.getElementById('btnLogin');
	const btnSkip = document.getElementById('btnSkip');
	const windowMinimize = document.getElementById('windowMinimize');
	const windowMaxRestore = document.getElementById('windowMaxRestore');
	const windowClose = document.getElementById('windowClose');

	// Initialize
	function init() {
		setupEventListeners();
		applyLocalizations('login', getSystemLocale());
	}

	// Setup all event listeners
	function setupEventListeners() {
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

		// Back button - navigate to import page (in same window)
		btnLoginBack?.addEventListener('click', () => {
			if (window.welcomeAPI) {
				window.welcomeAPI.navigate('import');
			}
		});

		// Sign In button - login then complete the welcome setup
		btnLogin?.addEventListener('click', async () => {
			if (window.welcomeAPI) {
				await window.welcomeAPI.login();
				await window.welcomeAPI.complete();
			}
		});

		// Skip button - complete the welcome setup without signing in
		btnSkip?.addEventListener('click', async () => {
			if (window.welcomeAPI) {
				await window.welcomeAPI.complete();
			}
		});
	}

	// Start the app
	init();
})()

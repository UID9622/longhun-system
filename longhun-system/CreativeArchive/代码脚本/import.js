/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Huawei Technologies Co., Ltd. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

(function () {
	'use strict';

	// DOM elements
	const btnImportBack = document.getElementById('btnImportBack');
	const btnVsCode = document.getElementById('btnVsCode');
	const btnVsCodeText = document.getElementById('btnVsCodeText');
	const btnVsCodeLoadingText = document.getElementById('btnVsCodeLoadingText');
	const btnSkip = document.getElementById('btnSkip');
	const windowMinimize = document.getElementById('windowMinimize');
	const windowMaxRestore = document.getElementById('windowMaxRestore');
	const windowClose = document.getElementById('windowClose');

	// Initialize
	function init() {
		setupEventListeners();
		applyLocalizations('import', getSystemLocale());
	}

	// Show loading on button
	function showLoading() {
		if (btnVsCode) {
			btnVsCode.classList.add('loading');
			btnVsCode.disabled = true;
		}
		if (btnVsCodeText) {
			btnVsCodeText.style.display = 'none';
		}
		if (btnVsCodeLoadingText) {
			btnVsCodeLoadingText.style.display = 'inline';
		}
		if (btnSkip) {
			btnSkip.disabled = true;
		}
		if (btnImportBack) {
			btnImportBack.disabled = true;
		}
	}

	// Hide loading on button
	function hideLoading() {
		if (btnVsCode) {
			btnVsCode.classList.remove('loading');
			btnVsCode.disabled = false;
		}
		if (btnVsCodeText) {
			btnVsCodeText.style.display = 'inline';
		}
		if (btnVsCodeLoadingText) {
			btnVsCodeLoadingText.style.display = 'none';
		}
		if (btnSkip) {
			btnSkip.disabled = false;
		}
		if (btnImportBack) {
			btnImportBack.disabled = false;
		}
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

		// VS Code import button - import config then navigate to login page
		btnVsCode?.addEventListener('click', async () => {
			if (window.welcomeAPI) {
				showLoading();
				try {
					await window.welcomeAPI.importConfig();
				} catch (error) {
					// Import failed
				} finally {
					hideLoading();
					window.welcomeAPI.navigate('login');
				}
			}
		});

		// Skip button - navigate to login page (in same window)
		btnSkip?.addEventListener('click', () => {
			if (window.welcomeAPI) {
				window.welcomeAPI.navigate('login');
			}
		});

		// Back button - navigate to welcome page (in same window)
		btnImportBack?.addEventListener('click', () => {
			if (window.welcomeAPI) {
				window.welcomeAPI.navigate('welcome');
			}
		});

		if (window.welcomeAPI) {
			window.welcomeAPI.onShowImportProgress((data) => {
				const importProgress = document.querySelector('.import-progress');
				importProgress.style.visibility = 'visible';
				const importProgressText = document.getElementById('importProgressText');

				if (typeof data === 'object' && data !== null && data.key) {
					const locale = getSystemLocale();
					const message = getLocalizedString('import', data.key, locale, data.args || []);
					importProgressText.textContent = message;
				} else {
					importProgressText.textContent = data;
				}
			});
		}
	}

	// Start the app
	init();
})()

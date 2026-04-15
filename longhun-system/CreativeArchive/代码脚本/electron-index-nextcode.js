/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Huawei Technologies Co., Ltd. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
// @ts-check
(function () {
	'use strict';

	const registerVscodeResourceScheme = (function () {
		let hasRegistered = false;
		return () => {
			if (hasRegistered) {
				return;
			}
			hasRegistered = true;
		};
	}());

	const handleClickBlankLink = (event) => {
		if (!event || !event.view || !event.view.document) {
			return;
		}

		let node = event.target;
		while (node) {
			if (node.tagName && node.tagName.toLowerCase() === 'a' && node.href) {
				if (node.target === '_blank') {
					ipcRenderer.sendToHost('did-click-blank-link', node.href.baseVal || node.href);
					event.preventDefault();
				}
				break;
			}
			node = node.parentNode;
		}
	};

	const listeningToEnterKey = (domListenerTargets = [], domActionTarget) => {
		const eventType = 'keydown';
		domListenerTargets.forEach(domTarget => {
			const keydownListener = e => {
				if (e.key === 'Enter') {
					domActionTarget?.click();
				}
			};
			domTarget.addEventListener(eventType, keydownListener);
		});
	}

	const handleIdaaSLogin = (contextBridge, ipcRenderer, params) => {
		// Expose intoProgram method to the embedded iframe for IDaaS Login callback.
		contextBridge.exposeInMainWorld('intoProgram', (mToken) => {
			ipcRenderer.sendToHost('get-mtoken', mToken);
		});

		const domListenerTargetArray = [];
		const usernameInput = document.getElementById('username');
		if (usernameInput) {
			domListenerTargetArray.push(usernameInput);

			// Remember userName.
			usernameInput.focus();
			const username = params.get('username');
			if (username) {
				// @ts-ignore
				usernameInput.value = username;
			}
		}

		// Listening to enter key.
		const passwordInput = document.getElementById('password');
		const domActionTarget = document.getElementsByTagName('button')[0];
		if (passwordInput) {
			domListenerTargetArray.push(passwordInput);
		}
		listeningToEnterKey(domListenerTargetArray, domActionTarget);
	}

	// @ts-ignore
	const { contextBridge, ipcRenderer } = require('electron');

	document.addEventListener('DOMContentLoaded', () => {
		registerVscodeResourceScheme();

		let isMouseDown2 = false;

		document.addEventListener('mousedown', () => {
			isMouseDown2 = true;
		});

		const tryDispatchSyntheticMouseEvent = (e) => {
			if (!isMouseDown2) {
				ipcRenderer.sendToHost('synthetic-mouse-event', { type: e.type, screenX: e.screenX, screenY: e.screenY, clientX: e.clientX, clientY: e.clientY });
			}
		};
		document.addEventListener('mouseup', e => {
			tryDispatchSyntheticMouseEvent(e);
			isMouseDown2 = false;
		});
		document.addEventListener('mousemove', tryDispatchSyntheticMouseEvent);
		document.addEventListener('click', handleClickBlankLink);

		// Forward messages from the embedded iframe
		window.onmessage = (message) => {
			ipcRenderer.sendToHost(message.data.command, message.data.data);
		};

		const params = new URLSearchParams(document.URL);
		if (params.get('loginType') === 'idaas') {
			handleIdaaSLogin(contextBridge, ipcRenderer, params);
		}
	});
}());

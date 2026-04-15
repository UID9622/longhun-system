/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Huawei Technologies Co., Ltd. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
// @ts-check
(function () {
	'use strict';

	let hoverTimeout = null;
	let lastSentElement = null;
	const DEBOUNCE_DELAY = 10;

	let isMouseOut = true;

	const fixedHighLights = new Map();

	let overlays = [];
	let controllers = [];

	const registerVscodeResourceScheme = (function () {
		let hasRegistered = false;
		return () => {
			if (hasRegistered) {
				return;
			}
			hasRegistered = true;
		};
	}());

	const handleInnerClick = (event) => {
		if (!event?.view?.document) {
			return;
		}

		const baseElement = event.view.document.querySelector('base');

		for (const pathElement of event.composedPath()) {
			/** @type {any} */
			const node = pathElement;
			if (node.tagName && node.tagName.toLowerCase() === 'a' && node.href) {
				if (node.getAttribute('href') === '#') {
					event.view.scrollTo(0, 0);
				} else if (node.hash && (node.getAttribute('href') === node.hash || (baseElement && node.href === baseElement.href + node.hash))) {
					const fragment = node.hash.slice(1);
					const decodedFragment = decodeURIComponent(fragment);
					const scrollTarget = event.view.document.getElementById(fragment) ?? event.view.document.getElementById(decodedFragment);
					if (scrollTarget) {
						scrollTarget.scrollIntoView();
					} else if (decodedFragment.toLowerCase() === 'top') {
						event.view.scrollTo(0, 0);
					}
				} else {
					ipcRenderer.sendToHost('did-click-link', { uri: node.href.baseVal || node.href });
				}
				event.preventDefault();
				return;
			}
		}
	};

	const getElementInfo = (element, eventType = 'hover') => {
		if (!element || element.nodeType !== 1) {
			return null;
		}

		let position = null;
		try {
			const rect = element.getBoundingClientRect();
			position = {
				x: Math.round(rect.x),
				y: Math.round(rect.y),
				width: Math.round(rect.width),
				height: Math.round(rect.height),
				top: Math.round(rect.top),
				right: Math.round(rect.right),
				bottom: Math.round(rect.bottom),
				left: Math.round(rect.left)
			}
		} catch (error) {
			console.error('Error getting bounding rect:', error);
		}

		return {
			tagName: element.tagName.toLowerCase(),
			id: element.id || '',
			className: element.className || '',
			position,
			href: element.href || '',
			src: element.src || '',
			alt: element.alt || '',
			title: element.title || '',
			placeholder: element.placeholder || '',
			xpath: getElementXPath(element),
			outerHTML: element.outerHTML || '',
			timestamp: Date.now(),
			eventType: eventType
		};
	};

	const getElementXPath = (element) => {
		if (element.tagName?.toLowerCase() === 'svg') {
			const allSvgElements = Array.from(document.getElementsByTagName('svg'));
			const index = allSvgElements.indexOf(element);
			return `//*[local-name()="svg"][${index + 1}]`;
		}
		if (element.id) {
			return `//*[@id="${element.id}"]`;
		}
		if (element === document.body) {
			return '/html/body';
		}

		let ix = 0;
		const siblings = element.parentNode ? element.parentNode.childNodes : [];

		for (let i = 0; i < siblings.length; i++) {
			const sibling = siblings[i];
			if (sibling === element) {
				return getElementXPath(element.parentNode) +
					'/' + element.tagName?.toLowerCase() +
					(ix > 0 ? '[' + (ix + 1) + ']' : '');
			}
			if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
				ix++;
			}
		}
		return '';
	};

	// Ignore elements that are too small or invisible
	const shouldIgnoreElement = (element) => {
		if (!element) {
			return true;
		}

		const rect = element.getBoundingClientRect();
		const style = window.getComputedStyle(element);

		return (
			rect.width === 0 ||
			rect.height === 0 ||
			style.display === 'none' ||
			style.visibility === 'hidden' ||
			parseFloat(style.opacity) === 0
		);
	};

	const sendElementInfo = (elementInfo, eventType = 'hover') => {
		if (!elementInfo) {
			return;
		}

		if (eventType === 'hover') {
			if (hoverTimeout) {
				clearTimeout(hoverTimeout);
			}

			hoverTimeout = setTimeout(() => {
				if (isMouseOut) {
					return;
				}
				if (eventType === 'hover' &&
					lastSentElement &&
					lastSentElement.xpath === elementInfo.xpath) {
					return;
				}
				ipcRenderer.sendToHost(`${eventType}-element`, elementInfo);

				lastSentElement = {
					...elementInfo,
					timestamp: Date.now()
				};
			}, DEBOUNCE_DELAY);
		} else {
			ipcRenderer.sendToHost(`${eventType}-element`, elementInfo);
		}
	};

	const handleMouseMove = (event) => {
		isMouseOut = false;
		const element = event.target ?? event;
		if (shouldIgnoreElement(element)) {
			return;
		}
		const elementInfo = getElementInfo(element, 'hover');
		if (elementInfo) {
			sendElementInfo(elementInfo, 'hover');
		}
	};

	const handleMouseLeave = () => {
		isMouseOut = true;
		lastSentElement = null;
		ipcRenderer.sendToHost('did-mouse-leave', { clear: true });
	};

	const handleClickElement = (event) => {
		if (lastSentElement) {
			addFixedHighLightElement(lastSentElement);
			sendElementInfo(lastSentElement, 'click');
		}
		event.stopPropagation();
		event.preventDefault();
	};

	const removeFixedHighLightElements = () => {
		fixedHighLights.forEach((element) => {
			element.remove();
		});
		fixedHighLights.clear();
	}

	const addFixedHighLightElement = (event) => {
		removeFixedHighLightElements();

		const element = document.createElement('div');
		element.classList.add('ide-high-light-border');
		element.style.left = `${event.position.left}px`;
		element.style.top = `${event.position.top}px`;
		element.style.width = `${event.position.width}px`;
		element.style.height = `${event.position.height}px`;

		const tagContainer = document.createElement('div');
		tagContainer.style.position = 'absolute';
		tagContainer.style.padding = '4px';

		const tagName = document.createElement('div');
		tagName.classList.add('ide-high-light-tag');
		const tagNameText = document.createElement('span');
		tagNameText.classList.add('ide-high-light-tag-text');
		tagNameText.textContent = event.tagName;
		tagName.appendChild(tagNameText);
		tagContainer.appendChild(tagName);
		element.appendChild(tagContainer);
		document.body.appendChild(element);

		positionTooltipElement(tagContainer, event);
		fixedHighLights.set(event.xpath, element);
	};

	const positionTooltipElement = (element, event) => {
		if (!event.position) {
			return;
		}
		// Above the high light border
		if (event.position.top > element.clientHeight) {
			element.style.top = '-28px' /** tooltip height */;
		}
		// Below the high light border
		else if (document.body.clientHeight - (event.position.top + event.position.height) > element.clientHeight) {
			element.style.top = `${event.position.height - 1}px`;
		}
		// Inside the high light border
		else {
			element.style.top = '-1px';
		}

		// Align to the left
		if (document.body.clientWidth - event.position.left > element.clientWidth) {
			element.style.left = `-3px`;
		}
		// Align to the right
		else if (document.body.clientWidth - event.position.right > element.clientWidth) {
			element.style.left = `${event.position.width - element.clientWidth - 7 /** tooltip padding */}px`;
		}
		// Inside the high light border
		else {
			element.style.left = `-3px`;
		}

		// Show tooltip after selected
		if (element.style.visibility === 'hidden') {
			this.setVisibility(element, true);
		}
	};

	const handleScroll = () => {
		handleWheel();
		// Hide high light border
		ipcRenderer.sendToHost('hover-element', null);
		lastSentElement = null;
	};

	const handleWheel = () => {
		fixedHighLights.forEach((element, xpath) => {
			const targetElement = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
			if (targetElement && targetElement.nodeType === 1) {
				//@ts-ignore
				const rect = targetElement.getBoundingClientRect();
				element.style.left = `${rect.left}px`;
				element.style.top = `${rect.top}px`;
				element.style.width = `${rect.width}px`;
				element.style.height = `${rect.height}px`;
			}
		});
	};

	const createOverlay = (element) => {
		const overlay = document.createElement('div');
		overlay.classList.add('ide-selecting-overlays');

		const rect = element.getBoundingClientRect();
		const scrollX = window.pageXOffset || document.documentElement.scrollLeft;
		const scrollY = window.pageYOffset || document.documentElement.scrollTop;

		overlay.style.left = (rect.left + scrollX) + 'px';
		overlay.style.top = (rect.top + scrollY) + 'px';
		overlay.style.width = rect.width + 'px';
		overlay.style.height = rect.height + 'px';
		document.body.appendChild(overlay);

		overlays.push(overlay);

		const clickController = new AbortController();
		controllers.push(clickController);

		overlay.addEventListener('click', handleClickElement, { signal: clickController.signal });

		const mousemoveController = new AbortController();
		controllers.push(mousemoveController);

		overlay.addEventListener('mousemove', function (e) {
			handleMouseMove(element);
			e.stopPropagation();
			e.preventDefault();
		}, { signal: mousemoveController.signal });
	};

	// Handle elements that cannot be reached through global events
	const handleSpecialTagEvents = () => {
		const specialTags = ['iframe', 'audio', 'svg'];
		specialTags.forEach(tag => {
			const elements = document.querySelectorAll(tag);
			elements.forEach(e => {
				createOverlay(e);
			});
		});
	};

	const clearOverlaysAndListeners = () => {
		controllers.forEach(controller => {
			controller.abort();
		});
		controllers = [];

		overlays.forEach(overlay => {
			overlay.remove();
		});
		overlays = [];
	};

	const { contextBridge, ipcRenderer } = require('electron');

	ipcRenderer.on('message', (e, args) => {
		switch (args.message?.type) {
			case 'start-select-elements':
				{
					document.body.classList.add('ide-selecting-elements');
					document.addEventListener('mousemove', handleMouseMove, { passive: true });
					document.addEventListener('mouseleave', handleMouseLeave);
					document.addEventListener('click', handleClickElement, true);
					document.addEventListener('scroll', handleScroll);
					document.addEventListener('wheel', handleWheel, { passive: false });
					handleSpecialTagEvents();
					break;
				}
			case 'stop-select-elements':
				{
					document.body.classList.remove('ide-selecting-elements');
					document.removeEventListener('mousemove', handleMouseMove);
					document.removeEventListener('mouseleave', handleMouseLeave);
					document.removeEventListener('click', handleClickElement, true);
					document.removeEventListener('scroll', handleScroll);
					document.removeEventListener('wheel', handleWheel);
					removeFixedHighLightElements();
					clearOverlaysAndListeners();
					break;
				}
			case 'cancel-selection':
				{
					removeFixedHighLightElements();
					break;
				}
			case 'select-page':
				{
					const htmlContent = document.documentElement.outerHTML;
					ipcRenderer.sendToHost('send-page', htmlContent);
					break;
				}
			default:
				break;
		}
	});

	const tryUpdateTitle = async () => {
		const maximumAttempts = 5;
		let count = 0;
		let isFinished = false;
		while (count < maximumAttempts && !isFinished) {
			await /** @type {Promise<void>} */(new Promise((resolve) => {
				setTimeout(() => {
					if (document.title) {
						ipcRenderer.sendToHost('update-title', { title: document.title });
						isFinished = true;
					}
					resolve();
				}, 1000);
			}));
			count++;
		}
	};

	const createDefaultStyles = () => {
		const style = document.createElement('style');
		style.innerHTML = `
	body.ide-selecting-elements * {
		cursor: default !important;
	}
	.ide-high-light-border {
		position: fixed;
		border: 2px solid transparent;
		border-image: linear-gradient(-45deg, #7490F3, #D27EFD) 1;
		background-clip: padding-box;
		box-sizing: border-box;
		pointer-events: none;
		z-index: 10000;
	}
	.ide-high-light-tag {
		padding: 0 6px;
		height: 20px;
		border-radius: 6px;
		background: linear-gradient(115deg, #4D42FF, #8d36ff);
		display: flex;
		align-items: center;
		justify-content: center;
		pointer-events: none;
		width: fit-content;
		white-space: nowrap;
	}
	.ide-high-light-tag-text {
		color: white;
		font-size: 10px;
		margin-bottom: 2px;
		font-family: "Segoe WPC", "Segoe UI", sans-serif;
	}
	.ide-selecting-overlays {
		position: absolute;
		z-index: 9999;
		pointer-events: auto;
		background: transparent;
	}
`;
		document.head.appendChild(style);
	};

	document.addEventListener('DOMContentLoaded', () => {
		registerVscodeResourceScheme();

		ipcRenderer.sendToHost('webview-ready', { title: document.title });
		if (!document.title) {
			tryUpdateTitle();
		}

		createDefaultStyles();

		document.addEventListener('click', handleInnerClick);

		// Update input url after the page is redirected
		if (!window.location.href.includes('browserId')) {
			ipcRenderer.sendToHost('update-location-href', window.location.href);
		}

		// Forward messages from the embedded iframe
		window.onmessage = (message) => {
			ipcRenderer.sendToHost(message.data.command, message.data.data);
		};
	});
}());

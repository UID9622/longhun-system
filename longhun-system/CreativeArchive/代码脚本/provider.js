"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateWebviewContent = exports.registerRequestHandlers = exports.getNonce = void 0;
const link_1 = require("../data/link");
function getNonce() {
    let text = '';
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    for (let i = 0; i < 32; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}
exports.getNonce = getNonce;
function registerRequestHandlers(webview, source, subscriptions) {
    const REQUEST_HANDLER_MAP = {
        initialize: () => link_1.linksMap.get(Object.getPrototypeOf(source)),
    };
    webview.onDidReceiveMessage((message) => __awaiter(this, void 0, void 0, function* () {
        const { id, type, what, params } = message;
        if (id === undefined || type === undefined) {
            return;
        }
        switch (type) {
            case 'promise': {
                try {
                    const response = (REQUEST_HANDLER_MAP[what] || source[what].bind(source))(...params);
                    const result = response instanceof Promise ? yield response : response;
                    webview.postMessage({ id, type, result });
                }
                catch (error) {
                    console.error(error);
                }
                break;
            }
            case 'subscription': {
                (REQUEST_HANDLER_MAP[what] || source[what].bind(source))((e) => {
                    webview.postMessage({ id, type, result: e });
                }, params);
                break;
            }
        }
    }), null, subscriptions);
}
exports.registerRequestHandlers = registerRequestHandlers;
function generateWebviewContent(language, nonce, scriptUri, id) {
    return `<!DOCTYPE html>
			<html lang="${language}">
				<head>
					<meta charset="UTF-8">
					<meta name="viewport" content="width=device-width, initial-scale=1.0">
					<title>Git History</title>
				</head>
				<body data-vscode-context='{"preventDefaultContextMenuItems": true}'>
					<div id="${id}"></div>
					<script nonce="${nonce}" src="${scriptUri}"></script>
				</body>
			</html>`;
}
exports.generateWebviewContent = generateWebviewContent;
//# sourceMappingURL=provider.js.map
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
exports.request = exports.subscribe = exports.sendMessage = void 0;
const vscode = acquireVsCodeApi();
/** auto-increment id */
let messageId = 0;
const responseHandles = {};
window.addEventListener("message", (event) => {
    const { id, type } = event.data;
    responseHandles[id](event.data);
    type === "promise" && delete responseHandles[id];
});
function sendMessage(message, timeout) {
    return __awaiter(this, void 0, void 0, function* () {
        return new Promise((resolve, reject) => {
            const id = messageId++;
            vscode.postMessage(Object.assign(Object.assign({ id }, message), { type: "promise" }));
            let isReSolved = false;
            responseHandles[id] = (res) => {
                isReSolved = true;
                resolve(res);
            };
            if (timeout) {
                setTimeout(() => {
                    if (!isReSolved) {
                        reject();
                    }
                }, timeout);
            }
        });
    });
}
exports.sendMessage = sendMessage;
function subscribe(eventName, params, handler) {
    const id = messageId++;
    vscode.postMessage({
        id,
        what: eventName,
        params,
        type: "subscription",
    });
    responseHandles[id] = (res) => {
        handler(res.result);
    };
}
exports.subscribe = subscribe;
function request(what, ...params) {
    return __awaiter(this, void 0, void 0, function* () {
        const response = yield sendMessage({ what, params });
        return response.result;
    });
}
exports.request = request;
//# sourceMappingURL=message.js.map
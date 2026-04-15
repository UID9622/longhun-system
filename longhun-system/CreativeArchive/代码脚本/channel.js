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
exports.ChannelContext = exports.initializeChannel = void 0;
const react_1 = require("react");
const message_1 = require("../utils/message");
function initializeChannel() {
    return __awaiter(this, void 0, void 0, function* () {
        const linkedFuncs = yield (0, message_1.request)("initialize");
        return Object.fromEntries(linkedFuncs.map(({ name, type }) => {
            return [name, buildFunc(name, type)];
        }));
    });
}
exports.initializeChannel = initializeChannel;
function buildFunc(name, type) {
    switch (type) {
        case "promise":
            return (...params) => __awaiter(this, void 0, void 0, function* () { return yield (0, message_1.request)(name, ...params); });
        case "subscription":
            return (handler, params) => (0, message_1.subscribe)(name, params, handler);
    }
}
exports.ChannelContext = (0, react_1.createContext)(undefined);
//# sourceMappingURL=channel.js.map
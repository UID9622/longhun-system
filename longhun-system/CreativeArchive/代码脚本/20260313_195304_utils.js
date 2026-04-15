"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.enumToMap = void 0;
function enumToMap(obj) {
    const res = {};
    Object.keys(obj).forEach((key) => {
        const value = obj[key];
        if (typeof value === 'number') {
            res[key] = value;
        }
    });
    return res;
}
exports.enumToMap = enumToMap;//# sourceMappingURL=https://main.vscode-cdn.net/sourcemaps/2b429d0657ca204151cef6df3a85eaef8efd9c2d/node_modules/undici/lib/llhttp/utils.js.map
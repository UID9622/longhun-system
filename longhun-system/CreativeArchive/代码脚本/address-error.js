"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AddressError = void 0;
class AddressError extends Error {
    constructor(message, parseMessage) {
        super(message);
        this.name = 'AddressError';
        if (parseMessage !== null) {
            this.parseMessage = parseMessage;
        }
    }
}
exports.AddressError = AddressError;//# sourceMappingURL=https://main.vscode-cdn.net/sourcemaps/2b429d0657ca204151cef6df3a85eaef8efd9c2d/node_modules/ip-address/dist/address-error.js.map
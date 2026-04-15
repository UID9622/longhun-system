"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const resolve_1 = require("./resolve");
class MissingRefError extends Error {
    constructor(resolver, baseId, ref, msg) {
        super(msg || `can't resolve reference ${ref} from id ${baseId}`);
        this.missingRef = (0, resolve_1.resolveUrl)(resolver, baseId, ref);
        this.missingSchema = (0, resolve_1.normalizeId)((0, resolve_1.getFullPath)(resolver, this.missingRef));
    }
}
exports.default = MissingRefError;//# sourceMappingURL=https://main.vscode-cdn.net/sourcemaps/2b429d0657ca204151cef6df3a85eaef8efd9c2d/node_modules/ajv/dist/compile/ref_error.js.map
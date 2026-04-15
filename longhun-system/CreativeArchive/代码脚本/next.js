"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const dependentRequired_1 = require("./validation/dependentRequired");
const dependentSchemas_1 = require("./applicator/dependentSchemas");
const limitContains_1 = require("./validation/limitContains");
const next = [dependentRequired_1.default, dependentSchemas_1.default, limitContains_1.default];
exports.default = next;//# sourceMappingURL=https://main.vscode-cdn.net/sourcemaps/2b429d0657ca204151cef6df3a85eaef8efd9c2d/node_modules/ajv/dist/vocabularies/next.js.map
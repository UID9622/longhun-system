"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const dependencies_1 = require("./dependencies");
const def = {
    keyword: "dependentSchemas",
    type: "object",
    schemaType: "object",
    code: (cxt) => (0, dependencies_1.validateSchemaDeps)(cxt),
};
exports.default = def;//# sourceMappingURL=https://main.vscode-cdn.net/sourcemaps/2b429d0657ca204151cef6df3a85eaef8efd9c2d/node_modules/ajv/dist/vocabularies/applicator/dependentSchemas.js.map
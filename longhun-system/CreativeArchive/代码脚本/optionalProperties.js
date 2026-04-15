"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const properties_1 = require("./properties");
const def = {
    keyword: "optionalProperties",
    schemaType: "object",
    error: properties_1.error,
    code(cxt) {
        if (cxt.parentSchema.properties)
            return;
        (0, properties_1.validateProperties)(cxt);
    },
};
exports.default = def;//# sourceMappingURL=https://main.vscode-cdn.net/sourcemaps/2b429d0657ca204151cef6df3a85eaef8efd9c2d/node_modules/ajv/dist/vocabularies/jtd/optionalProperties.js.map
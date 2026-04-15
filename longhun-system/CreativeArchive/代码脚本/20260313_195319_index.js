"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsx_runtime_1 = require("react/jsx-runtime");
const index_module_scss_1 = __importDefault(require("./index.module.scss"));
const TAG_PREFIX = "tag: ";
const GitTag = ({ refName, color }) => {
    const isTag = refName.startsWith(TAG_PREFIX);
    const label = isTag ? refName.slice(TAG_PREFIX.length) : refName;
    return ((0, jsx_runtime_1.jsxs)("div", Object.assign({ className: index_module_scss_1.default["tag-container"], style: {
            backgroundColor: `${color}70`,
        } }, { children: [(0, jsx_runtime_1.jsx)("span", { className: `codicon codicon-${isTag ? "tag" : "git-branch"} ${index_module_scss_1.default.icon}` }), label] })));
};
exports.default = GitTag;
//# sourceMappingURL=index.js.map
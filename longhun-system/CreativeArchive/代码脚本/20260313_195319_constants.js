"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.HEADERS = void 0;
const jsx_runtime_1 = require("react/jsx-runtime");
const ide_ui_1 = require("@cloud/ide-ui");
const commit_1 = require("../../../../git/commit");
const types_1 = require("../../../../git/types");
const GitGraph_1 = __importDefault(require("../GitGraph"));
const GitTag_1 = __importDefault(require("../GitTag"));
let timer = null;
function handleMouseEnter(e, commit) {
    timer = setTimeout(() => {
        ide_ui_1.Hover.show({
            target: e.target,
            content: { value: commit[commit_1.CommitIndex.MESSAGE] },
            showPointer: false
        });
    }, 750);
}
function handleMouseLeave() {
    clearTimeout(timer);
}
exports.HEADERS = [
    {
        prop: "graph",
        label: "Graph",
        width: 70,
        minWidth: 70,
        transformer: (commit) => ((0, jsx_runtime_1.jsx)(GitGraph_1.default, { data: commit[commit_1.CommitIndex.GRAPH_SLICE] })),
    },
    {
        prop: "description",
        label: "description.label",
        width: "fill",
        minWidth: 180,
        filterable: true,
        filterLogOption: "keyword",
        transformer: (commit) => ((0, jsx_runtime_1.jsx)(jsx_runtime_1.Fragment, { children: (0, jsx_runtime_1.jsxs)("span", { children: [commit[commit_1.CommitIndex.REF_NAMES].map((refName) => ((0, jsx_runtime_1.jsx)(GitTag_1.default, { refName: refName, color: commit[commit_1.CommitIndex.GRAPH_SLICE][types_1.CommitGraphSliceIndex.COMMIT_COLOR] }, refName))), (0, jsx_runtime_1.jsx)("span", Object.assign({ onMouseEnter: (e) => handleMouseEnter(e, commit), onMouseLeave: () => handleMouseLeave() }, { children: commit[commit_1.CommitIndex.MESSAGE] }))] }) })),
    },
    {
        prop: "hash",
        label: 'hash.label',
        width: 80,
        minWidth: 80,
        maxWidth: 200,
        locatable: true,
        transformer: (commit) => ((0, jsx_runtime_1.jsx)(jsx_runtime_1.Fragment, { children: (0, jsx_runtime_1.jsx)("span", { children: commit[commit_1.CommitIndex.HASH].slice(0, 6) }) })),
    },
    {
        prop: "author",
        label: 'author.label',
        width: 108,
        minWidth: 120,
        maxWidth: 300,
        filterable: true,
        filterLogOption: "authors",
        transformer: (commit) => commit[commit_1.CommitIndex.AUTHOR_NAME],
    },
    {
        prop: "date",
        label: 'date.label',
        width: 150,
        minWidth: 150,
        maxWidth: 200,
        transformer: (commit) => commit[commit_1.CommitIndex.COMMIT_DATE],
    },
];
//# sourceMappingURL=constants.js.map
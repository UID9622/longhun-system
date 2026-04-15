"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsx_runtime_1 = require("react/jsx-runtime");
const react_1 = require("react");
const react_intl_1 = require("react-intl");
const react_2 = require("@vscode/webview-ui-toolkit/react");
const channel_1 = require("../common/data/channel");
const detail_module_scss_1 = __importDefault(require("./detail.module.scss"));
const Detail = (props) => {
    const channel = (0, react_1.useContext)(channel_1.ChannelContext);
    const [pickedCommits, setPickedCommit] = (0, react_1.useState)();
    const subscribeSwitcher = (0, react_1.useCallback)(() => {
        channel.setDetailSubscriber((commits) => setPickedCommit(commits));
    }, [channel, setPickedCommit]);
    (0, react_1.useEffect)(() => {
        subscribeSwitcher();
    }, [channel, subscribeSwitcher]);
    return ((0, jsx_runtime_1.jsx)("div", Object.assign({ className: detail_module_scss_1.default["detail-container"] }, { children: (pickedCommits === null || pickedCommits === void 0 ? void 0 : pickedCommits.length) && pickedCommits.map((commit, index) => {
            const [hash, , message, , commitDate, authorEmail, authorName,] = commit;
            return ((0, jsx_runtime_1.jsxs)(react_1.Fragment, { children: [(0, jsx_runtime_1.jsxs)("div", Object.assign({ className: detail_module_scss_1.default["commit-item"] }, { children: [(0, jsx_runtime_1.jsx)("div", Object.assign({ className: detail_module_scss_1.default["message"] }, { children: message })), (0, jsx_runtime_1.jsx)("br", {}), (0, jsx_runtime_1.jsxs)("div", Object.assign({ className: detail_module_scss_1.default["info"] }, { children: [(0, jsx_runtime_1.jsx)("span", Object.assign({ className: detail_module_scss_1.default["hash"] }, { children: hash.substring(0, 8) })), (0, jsx_runtime_1.jsxs)("span", Object.assign({ className: detail_module_scss_1.default["author"] }, { children: [" ", props.intl.formatMessage({ id: 'detail.author' }), " ", authorName, " ", (0, jsx_runtime_1.jsx)("a", Object.assign({ href: `mailto:${authorEmail}` }, { children: `<${authorEmail}>` })), ", "] })), (0, jsx_runtime_1.jsx)("div", Object.assign({ className: detail_module_scss_1.default["commit-date"] }, { children: props.intl.formatMessage({ id: 'detail.commitDate' }, { date: commitDate }) }))] }))] })), index < pickedCommits.length - 1 && (0, jsx_runtime_1.jsx)(react_2.VSCodeDivider, {})] }, hash));
        }) })));
};
exports.default = (0, react_intl_1.injectIntl)(Detail);
//# sourceMappingURL=Detail.js.map
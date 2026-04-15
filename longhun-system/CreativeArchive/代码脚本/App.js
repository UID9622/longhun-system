"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const jsx_runtime_1 = require("react/jsx-runtime");
const react_1 = require("react");
const channel_1 = require("../common/data/channel");
const CommitsTable_1 = __importDefault(require("./components/CommitsTable"));
require("@vscode/codicons/dist/codicon.css");
function App() {
    const channel = (0, react_1.useContext)(channel_1.ChannelContext);
    const [isRepoInitialized, setIsRepoInitialized] = (0, react_1.useState)(false);
    (0, react_1.useEffect)(() => {
        channel.getDefaultRepository().then((defaultRepo) => {
            !!defaultRepo && setIsRepoInitialized(true);
        });
        channel.onReposChange((repos) => {
            !!(repos === null || repos === void 0 ? void 0 : repos.length) && setIsRepoInitialized(true);
        });
    }, [channel]);
    return isRepoInitialized ? (0, jsx_runtime_1.jsx)(CommitsTable_1.default, {}) : null;
}
exports.default = App;
//# sourceMappingURL=App.js.map
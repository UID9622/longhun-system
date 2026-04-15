"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getCommandDisposables = void 0;
const filter_1 = require("./filter");
const input_1 = require("./input");
const switch_1 = require("./switch");
const contextmenu_1 = require("./contextmenu");
function getCommandDisposables() {
    return [...(0, filter_1.getFilterCommandsDisposable)(), ...(0, switch_1.getSwitchCommandsDisposable)(), ...(0, input_1.getInputCommandsDisposable)(), ...(0, contextmenu_1.getContextMenuCommandsDisposable)()];
}
exports.getCommandDisposables = getCommandDisposables;
//# sourceMappingURL=index.js.map
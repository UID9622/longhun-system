"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.checkScrollBarVisible = void 0;
function checkScrollBarVisible(element) {
    return element.scrollHeight > element.getBoundingClientRect().width;
}
exports.checkScrollBarVisible = checkScrollBarVisible;
//# sourceMappingURL=element.js.map
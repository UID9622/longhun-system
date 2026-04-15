"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.link = exports.linksMap = void 0;
exports.linksMap = new WeakMap();
function link(type) {
    return (target, propertyKey) => {
        const links = exports.linksMap.get(target) || [];
        links === null || links === void 0 ? void 0 : links.push({ name: propertyKey, type });
        exports.linksMap.set(target, links);
    };
}
exports.link = link;
//# sourceMappingURL=link.js.map
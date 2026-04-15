"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.GitStatusFileDecorationProvider = void 0;
const inversify_1 = require("inversify");
const vscode_1 = require("vscode");
const constants_1 = require("../common/constants");
const status_1 = require("../../git/changes/status");
let GitStatusFileDecorationProvider = class GitStatusFileDecorationProvider {
    constructor() {
        this.STATUS_BADGE_MAP = {
            [1 /* Status.INDEX_ADDED */]: "A",
            [3 /* Status.INDEX_RENAMED */]: "R",
            [5 /* Status.MODIFIED */]: "M",
            [6 /* Status.DELETED */]: "D",
        };
    }
    provideFileDecoration(uri) {
        if (uri.scheme === constants_1.EXTENSION_SCHEME) {
            const { status } = JSON.parse(uri.query);
            return new vscode_1.FileDecoration(this.STATUS_BADGE_MAP[status], (0, status_1.getStatusText)(status), (0, status_1.getColor)(status));
        }
    }
};
GitStatusFileDecorationProvider = __decorate([
    (0, inversify_1.injectable)()
], GitStatusFileDecorationProvider);
exports.GitStatusFileDecorationProvider = GitStatusFileDecorationProvider;
//# sourceMappingURL=GitStatusFileDecorationProvider.js.map
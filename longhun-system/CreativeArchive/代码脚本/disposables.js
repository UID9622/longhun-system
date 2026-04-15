"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.DisposableController = void 0;
const vscode_1 = require("vscode");
const inversify_1 = require("inversify");
const GitStatusFileDecorationProvider_1 = require("./views/changes/GitStatusFileDecorationProvider");
const constants_1 = require("./views/common/constants");
const HistoryViewProvider_1 = require("./views/history/HistoryViewProvider");
const commands_1 = require("./commands");
const ChangeTreeView_1 = require("./views/changes/ChangeTreeView");
const DetailViewProvider_1 = require("./views/detail/DetailViewProvider");
let DisposableController = class DisposableController {
    constructor(_changeTreeView, historyViewWebviewViewProvider, detailViewWebviewProvider, GitStatusFileDecorationProvider) {
        this.historyViewWebviewViewProvider = historyViewWebviewViewProvider;
        this.detailViewWebviewProvider = detailViewWebviewProvider;
        this.GitStatusFileDecorationProvider = GitStatusFileDecorationProvider;
    }
    createDisposables() {
        return [
            ...(0, commands_1.getCommandDisposables)(),
            vscode_1.window.registerWebviewViewProvider(`${constants_1.EXTENSION_SCHEME}.history`, this.historyViewWebviewViewProvider, { webviewOptions: { retainContextWhenHidden: true } }),
            vscode_1.window.registerWebviewViewProvider(`${constants_1.EXTENSION_SCHEME}.detail`, this.detailViewWebviewProvider, { webviewOptions: { retainContextWhenHidden: true } }),
            vscode_1.window.registerFileDecorationProvider(this.GitStatusFileDecorationProvider),
        ];
    }
};
DisposableController = __decorate([
    (0, inversify_1.injectable)(),
    __metadata("design:paramtypes", [ChangeTreeView_1.ChangeTreeView,
        HistoryViewProvider_1.HistoryWebviewViewProvider,
        DetailViewProvider_1.DetailViewProvider,
        GitStatusFileDecorationProvider_1.GitStatusFileDecorationProvider])
], DisposableController);
exports.DisposableController = DisposableController;
//# sourceMappingURL=disposables.js.map
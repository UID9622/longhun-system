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
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.DetailViewProvider = void 0;
const path_1 = __importDefault(require("path"));
const inversify_1 = require("inversify");
const vscode_1 = require("vscode");
const types_1 = require("../../container/types");
const source_1 = require("../common/data/source");
const provider_1 = require("../common/utils/provider");
const constants_1 = require("../common/constants");
let DetailViewProvider = class DetailViewProvider {
    constructor(context, source) {
        this.context = context;
        this.source = source;
    }
    resolveWebviewView(webviewView) {
        const { extensionUri, extensionPath } = this.context;
        const nonce = (0, provider_1.getNonce)();
        const language = this.context.globalState.get('vscodeDisplayLanguage');
        const scriptPath = vscode_1.Uri.file(path_1.default.join(extensionPath, 'dist', 'detail.js'));
        const scriptUri = webviewView.webview.asWebviewUri(scriptPath);
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [vscode_1.Uri.joinPath(extensionUri, 'dist')],
        };
        webviewView.webview.html = (0, provider_1.generateWebviewContent)(language, nonce, scriptUri, constants_1.DETAIL_ROOT_ID);
        (0, provider_1.registerRequestHandlers)(webviewView.webview, this.source, this.context.subscriptions);
    }
};
DetailViewProvider = __decorate([
    (0, inversify_1.injectable)(),
    __param(0, (0, inversify_1.inject)(types_1.TYPES.ExtensionContext)),
    __metadata("design:paramtypes", [Object, source_1.Source])
], DetailViewProvider);
exports.DetailViewProvider = DetailViewProvider;
//# sourceMappingURL=DetailViewProvider.js.map
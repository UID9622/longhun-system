"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
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
exports.HistoryWebviewViewProvider = void 0;
const path_1 = __importDefault(require("path"));
const nls = __importStar(require("vscode-nls"));
const inversify_1 = require("inversify");
const vscode_1 = require("vscode");
const types_1 = require("../../container/types");
const source_1 = require("../common/data/source");
const provider_1 = require("../common/utils/provider");
const constants_1 = require("../common/constants");
const localize = nls.loadMessageBundle();
let HistoryWebviewViewProvider = class HistoryWebviewViewProvider {
    constructor(context, source) {
        this.context = context;
        this.source = source;
    }
    resolveWebviewView(webviewView) {
        const { extensionUri, extensionPath } = this.context;
        const nonce = (0, provider_1.getNonce)();
        const language = this.context.globalState.get('vscodeDisplayLanguage');
        const scriptPath = vscode_1.Uri.file(path_1.default.join(extensionPath, 'dist', 'view.js'));
        const scriptUri = webviewView.webview.asWebviewUri(scriptPath);
        const totalCountEmitter = this.source.getCommitsEventEmitter();
        totalCountEmitter.event(({ totalCount, count }) => {
            webviewView.description = localize('webviewView.description', '{1}/{0} commits in total', totalCount, count);
        });
        this.context.subscriptions.push(totalCountEmitter);
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [vscode_1.Uri.joinPath(extensionUri, 'dist')],
        };
        webviewView.webview.html = (0, provider_1.generateWebviewContent)(language, nonce, scriptUri, constants_1.HISTORY_ROOT_ID);
        (0, provider_1.registerRequestHandlers)(webviewView.webview, this.source, this.context.subscriptions);
    }
};
HistoryWebviewViewProvider = __decorate([
    (0, inversify_1.injectable)(),
    __param(0, (0, inversify_1.inject)(types_1.TYPES.ExtensionContext)),
    __metadata("design:paramtypes", [Object, source_1.Source])
], HistoryWebviewViewProvider);
exports.HistoryWebviewViewProvider = HistoryWebviewViewProvider;
//# sourceMappingURL=HistoryViewProvider.js.map
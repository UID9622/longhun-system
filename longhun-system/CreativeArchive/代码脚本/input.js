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
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getInputCommandsDisposable = exports.INPUT_HASH_COMMAND = void 0;
const vscode_1 = require("vscode");
const nls = __importStar(require("vscode-nls"));
const inversify_config_1 = require("../container/inversify.config");
const source_1 = require("../views/common/data/source");
const localize = nls.loadMessageBundle();
exports.INPUT_HASH_COMMAND = "git-history.history.input.hash";
function getInputCommandsDisposable() {
    const source = inversify_config_1.container.get(source_1.Source);
    return [
        vscode_1.commands.registerCommand(exports.INPUT_HASH_COMMAND, () => __awaiter(this, void 0, void 0, function* () {
            const inputBox = vscode_1.window.createInputBox();
            inputBox.placeholder = localize('hash.inputBox.placeholder', 'Input commit hash to locate');
            return new Promise((resolve) => {
                inputBox.onDidAccept(() => {
                    resolve(inputBox.value);
                    inputBox.dispose();
                });
                inputBox.show();
            });
        })),
        vscode_1.commands.registerCommand('git-history.changes.toggleDisplayMode', () => {
            source.toggleDisplay();
        })
    ];
}
exports.getInputCommandsDisposable = getInputCommandsDisposable;
//# sourceMappingURL=input.js.map
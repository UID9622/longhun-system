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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getFilterCommandsDisposable = exports.FILTER_MESSAGE_COMMAND = exports.FILTER_AUTHOR_COMMAND = void 0;
const vscode_1 = require("vscode");
const nls = __importStar(require("vscode-nls"));
const inversify_config_1 = require("../container/inversify.config");
const service_1 = require("../git/service");
const state_1 = __importDefault(require("../views/common/data/state"));
const source_1 = require("../views/common/data/source");
const switch_1 = require("./switch");
const localize = nls.loadMessageBundle();
exports.FILTER_AUTHOR_COMMAND = 'git-history.history.filter.author';
exports.FILTER_MESSAGE_COMMAND = 'git-history.history.filter.message';
function getFilterCommandsDisposable() {
    const gitService = inversify_config_1.container.get(service_1.GitService);
    const source = inversify_config_1.container.get(source_1.Source);
    return [filterAuthor(source, gitService), filterMessage(source)];
}
exports.getFilterCommandsDisposable = getFilterCommandsDisposable;
function filterAuthor(source, gitService) {
    return vscode_1.commands.registerCommand(exports.FILTER_AUTHOR_COMMAND, () => __awaiter(this, void 0, void 0, function* () {
        var _a;
        const switchSubscriber = source.getSwitchSubscriber();
        if (!switchSubscriber) {
            return;
        }
        const CLEAR_ALL_SELECTIONS_ID = 'clear-all';
        const quickPick = vscode_1.window.createQuickPick();
        quickPick.title = localize('author.quickPick.title', 'Select Authors');
        quickPick.placeholder = localize('author.quickPick.placeholder', 'Search author by name');
        quickPick.canSelectMany = true;
        quickPick.busy = true;
        quickPick.buttons = [
            {
                iconPath: new vscode_1.ThemeIcon(CLEAR_ALL_SELECTIONS_ID),
                tooltip: localize('author.quickPick.buttons.tooltip', 'Clear all selections'),
            },
        ];
        // TODO: set config
        quickPick.onDidTriggerButton(({ iconPath }) => {
            if (iconPath.id === CLEAR_ALL_SELECTIONS_ID) {
                quickPick.selectedItems = [];
            }
        });
        quickPick.show();
        const authorItems = ((_a = (yield gitService.getAuthors(state_1.default.logOptions))) === null || _a === void 0 ? void 0 : _a.map(({ name, email, isSelf }) => {
            var _a;
            return ({
                label: name + (isSelf ? ' (You)' : ''),
                description: email,
                value: `${name} <${email}>`,
                picked: (_a = state_1.default.logOptions.authors) === null || _a === void 0 ? void 0 : _a.includes(name),
            });
        })) || [];
        quickPick.busy = false;
        quickPick.items = authorItems;
        quickPick.selectedItems = authorItems.filter(({ value }) => { var _a; return (_a = state_1.default.logOptions.authors) === null || _a === void 0 ? void 0 : _a.includes(value); });
        quickPick.onDidAccept(() => {
            quickPick.dispose();
            const selectedAuthors = quickPick.selectedItems.map(({ value }) => value);
            state_1.default.logOptions.authors = selectedAuthors;
            if (quickPick.selectedItems.length === 0) {
                vscode_1.commands.executeCommand(switch_1.RESET_COMMAND);
                return;
            }
            source.getCommits(switchSubscriber, state_1.default.logOptions);
        });
    }));
}
function filterMessage(source) {
    return vscode_1.commands.registerCommand(exports.FILTER_MESSAGE_COMMAND, () => __awaiter(this, void 0, void 0, function* () {
        const switchSubscriber = source.getSwitchSubscriber();
        if (!switchSubscriber) {
            return;
        }
        const inputBox = vscode_1.window.createInputBox();
        inputBox.placeholder = localize('description.inputBox.placeholder', 'Input message keywords to filter commits');
        inputBox.value = state_1.default.logOptions.keyword || '';
        inputBox.show();
        inputBox.onDidAccept(() => {
            inputBox.dispose();
            state_1.default.logOptions.keyword = inputBox.value;
            source.getCommits(switchSubscriber, state_1.default.logOptions);
        });
    }));
}
//# sourceMappingURL=filter.js.map
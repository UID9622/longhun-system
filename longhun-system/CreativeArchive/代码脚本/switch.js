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
exports.getSwitchCommandsDisposable = exports.SWITCH_BRANCH_COMMAND = exports.SWITCH_REPO_COMMAND = exports.REFRESH_COMMAND = exports.RESET_COMMAND = void 0;
/* eslint-disable no-undef */
const vscode_1 = require("vscode");
const nls = __importStar(require("vscode-nls"));
const inversify_config_1 = require("../container/inversify.config");
const service_1 = require("../git/service");
const source_1 = require("../views/common/data/source");
const state_1 = __importDefault(require("../views/common/data/state"));
exports.RESET_COMMAND = 'git-history.history.reset';
exports.REFRESH_COMMAND = 'git-history.history.refresh';
exports.SWITCH_REPO_COMMAND = 'git-history.history.switch.repo';
exports.SWITCH_BRANCH_COMMAND = 'git-history.history.switch.branch';
const REF_TYPE_DETAIL_MAP = {
    heads: {
        icon: 'git-branch',
        descriptionPrefix: '',
    },
    remotes: { icon: 'git-branch', descriptionPrefix: 'Remote branch at ' },
    tags: { icon: 'tag', descriptionPrefix: 'Tag at ' },
};
const localize = nls.loadMessageBundle();
const DEBOUNCE_INTERVAL = 1000;
function getSwitchCommandsDisposable() {
    const gitService = inversify_config_1.container.get(service_1.GitService);
    const source = inversify_config_1.container.get(source_1.Source);
    return [reset(source, gitService), refresh(source), switchRepo(source, gitService), switchBranch(source, gitService)];
}
exports.getSwitchCommandsDisposable = getSwitchCommandsDisposable;
function reset(source, gitService) {
    const debouncedReset = debounceImmediate((switchSubscriber) => source.getCommits(switchSubscriber, state_1.default.logOptions), DEBOUNCE_INTERVAL);
    return vscode_1.commands.registerCommand(exports.RESET_COMMAND, () => __awaiter(this, void 0, void 0, function* () {
        const switchSubscriber = source.getSwitchSubscriber();
        if (!switchSubscriber) {
            return;
        }
        state_1.default.logOptions = {
            repo: gitService.getDefaultRepository(),
        };
        debouncedReset(switchSubscriber);
    }));
}
function refresh(source) {
    const debouncedRefresh = debounceImmediate((switchSubscriber) => source.getCommits(switchSubscriber, state_1.default.logOptions), DEBOUNCE_INTERVAL);
    return vscode_1.commands.registerCommand(exports.REFRESH_COMMAND, () => __awaiter(this, void 0, void 0, function* () {
        const switchSubscriber = source.getSwitchSubscriber();
        if (!switchSubscriber) {
            return;
        }
        debouncedRefresh(switchSubscriber);
    }));
}
function switchRepo(source, gitService) {
    return vscode_1.commands.registerCommand(exports.SWITCH_REPO_COMMAND, () => __awaiter(this, void 0, void 0, function* () {
        const quickPick = vscode_1.window.createQuickPick();
        const items = gitService
            .getRepositories()
            .sort()
            .map((repo) => ({
            label: repo,
        })) || [];
        quickPick.title = localize('icon.switch.repository', 'Switch Repository');
        quickPick.placeholder = localize('repository.quickPick.placeholder', 'Search repo by path');
        quickPick.items = items;
        quickPick.activeItems = items.filter(({ label }) => label === state_1.default.logOptions.repo);
        quickPick.onDidChangeSelection((selection) => {
            const [item] = selection;
            const { label: repo } = item;
            const switchSubscriber = source.getSwitchSubscriber();
            if (!switchSubscriber || repo === state_1.default.logOptions.repo) {
                return quickPick.dispose();
            }
            state_1.default.logOptions = { repo };
            source.getCommits(switchSubscriber, state_1.default.logOptions);
            quickPick.dispose();
        });
        quickPick.show();
    }));
}
function switchBranch(source, gitService) {
    return vscode_1.commands.registerCommand(exports.SWITCH_BRANCH_COMMAND, () => __awaiter(this, void 0, void 0, function* () {
        const quickPick = vscode_1.window.createQuickPick();
        quickPick.title = localize('reference.quickPick.title', 'Select Reference');
        quickPick.placeholder = localize('reference.quickPick.placeholder', 'Search ref by name');
        quickPick.busy = true;
        quickPick.show();
        const refs = (yield gitService.getRefs(state_1.default.logOptions)) || [];
        const localBranchRefs = [];
        const remoteBranchRefs = [];
        const otherRefs = refs.filter((ref) => {
            if (ref.type === 'heads') {
                localBranchRefs.push(ref);
                return false;
            }
            if (ref.type === 'remotes') {
                remoteBranchRefs.push(ref);
                return false;
            }
            return true;
        });
        const branchItems = [...localBranchRefs, ...remoteBranchRefs, ...otherRefs].map(({ type, name, hash }) => {
            var _a, _b;
            return ({
                label: `$(${(_a = REF_TYPE_DETAIL_MAP[type]) === null || _a === void 0 ? void 0 : _a.icon}) ${name}`,
                description: `${(_b = REF_TYPE_DETAIL_MAP[type]) === null || _b === void 0 ? void 0 : _b.descriptionPrefix}${hash.substring(0, 8)}`,
                ref: name,
            });
        });
        // first item to select all branches
        branchItems.unshift({
            label: `$(check-all) ${localize('reference.allBranches', 'All branches')}`,
            ref: '',
        });
        quickPick.items = branchItems;
        quickPick.activeItems = branchItems.filter(({ ref }) => ref === (state_1.default.logOptions.ref || ''));
        quickPick.onDidChangeSelection((selection) => {
            const [item] = selection;
            const { ref } = item;
            const switchSubscriber = source.getSwitchSubscriber();
            if (!switchSubscriber) {
                return;
            }
            state_1.default.logOptions.ref = ref;
            source.getCommits(switchSubscriber, state_1.default.logOptions);
            quickPick.dispose();
        });
        quickPick.busy = false;
    }));
}
function debounceImmediate(fn, wait) {
    let timer = null;
    return (subscriber) => {
        if (timer) {
            return;
        }
        fn(subscriber);
        timer = setTimeout(() => {
            timer = null;
            clearTimeout(timer);
        }, wait);
    };
}
//# sourceMappingURL=switch.js.map